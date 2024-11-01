import config
from news_crawler import get_news, get_single_article
from podcast_generator import PodcastGenerator
from text_to_speech import TextToSpeech
import logging
import os
from datetime import datetime
import json
import argparse
from typing import Literal

def setup_logging(timestamp):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = f'{log_dir}/podcast_generation_{timestamp}.log'
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return log_file

def save_article_references(articles, output_dir):
    ref_file = os.path.join(output_dir, 'article_references.json')
    
    article_refs = []
    for article in articles:
        article_refs.append({
            'title': article['title'],
            'url': article['source'],
            'published_date': article['published_date']
        })
    
    with open(ref_file, 'w', encoding='utf-8') as f:
        json.dump(article_refs, f, ensure_ascii=False, indent=4)
    
    return ref_file

def parse_arguments():
    parser = argparse.ArgumentParser(description='生成AI学术播客')
    parser.add_argument('--mode', type=Literal['batch', 'single'], default='batch',
                       help='生成模式：batch(批量文章) 或 single(单篇文章)')
    parser.add_argument('--language', type=Literal['zh', 'en'], default='zh',
                       help='播客语言：zh(中文) 或 en(英文)')
    parser.add_argument('--topic', type=str, default='LLM Agent',
                       help='文章主题，用于单篇模式')
    parser.add_argument('--identifier', type=str,
                       help='文章ID，用于单篇模式 (可选)')
    parser.add_argument('--title', type=str,
                       help='文章标题，用于单篇模式 (可选)')
    return parser.parse_args()

def main():
    # 解析命令行参数
    args = parse_arguments()
    
    # 设置语言
    config.LANGUAGE = args.language
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = setup_logging(timestamp)
    logging.info(f"Starting main program, log file: {log_file}")

    # Create output directory with timestamp
    output_dir = os.path.join(config.OUTPUT_DIR, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Created output directory: {output_dir}")

    # 初始化播客生成器
    podcast_gen = PodcastGenerator(config.LLM_API_URL, config.LLM_API_TOKEN)

    if args.mode == 'batch':
        # 批量生成模式
        logging.info("Starting news crawling for batch mode")
        news_articles = get_news()
        logging.info(f"Successfully crawled {len(news_articles)} articles")
        
        # Save article references
        ref_file = save_article_references(news_articles, output_dir)
        logging.info(f"Article references saved to: {ref_file}")

        for article in news_articles:
            logging.info(f"Article title: {article['title']}")
            logging.info(f"Article source: {article['source']}")
            logging.info(f"Published date: {article['published_date']}")
            logging.info(f"Article summary: {article['content'][:300]}...")

        podcast_script = podcast_gen.generate(news_articles)
    else:
        # 单篇文章模式
        logging.info("Starting single article mode")
        article = get_single_article(
            identifier=args.identifier,
            title=args.title,
            topic=args.topic
        )
        podcast_script = podcast_gen.generate_single_article(article)

    # 2. Generate podcast content
    logging.info("Starting podcast content generation")
    logging.info(f"Podcast content generation completed:\n {podcast_script}")

    # Save generated text
    text_file = os.path.join(output_dir, 'podcast_script.txt')
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(podcast_script)
    logging.info(f"Podcast script saved to {text_file}")

    # 3. Convert to speech
    logging.info("Starting text-to-speech conversion")
    tts = TextToSpeech(config.BAIDU_API_KEY, config.BAIDU_SECRET_KEY)
    
    # Generate audio files
    audio_parts = tts.convert_dialog(podcast_script, output_dir)
    logging.info(f"Generated {len(audio_parts)} audio segments")

    # Merge audio files
    output_filename = "podcast.mp3"
    output_path = os.path.join(output_dir, output_filename)
    final_audio = tts.merge_audio_files(audio_parts, output_path)
    logging.info(f"Audio files merged, final file: {final_audio}")

    print(f"Podcast generated and saved in directory: {output_dir}")
    logging.info(f"Main program completed, log file: {log_file}")

if __name__ == "__main__":
    main()
