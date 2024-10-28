import config
from news_crawler import get_news
from podcast_generator import PodcastGenerator
from text_to_speech import TextToSpeech
import logging
import os
from datetime import datetime
import json

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

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = setup_logging(timestamp)
    logging.info(f"Starting main program, log file: {log_file}")

    # Create output directory with timestamp
    output_dir = os.path.join(config.OUTPUT_DIR, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Created output directory: {output_dir}")

    # 1. Crawl news
    logging.info("Starting news crawling")
    news_articles = get_news()
    logging.info(f"Successfully crawled {len(news_articles)} articles")
    
    # Save article references
    ref_file = save_article_references(news_articles, output_dir)
    logging.info(f"Article references saved to: {ref_file}")

    for article in news_articles:
        logging.info(f"Article title: {article['title']}")
        logging.info(f"Article source: {article['source']}")
        logging.info(f"Published date: {article['published_date']}")
        logging.info(f"Article summary: {article['content'][:300]}...")  # Log first 300 characters

    # 2. Generate podcast content
    logging.info("Starting podcast content generation")
    podcast_gen = PodcastGenerator(config.LLM_API_URL, config.LLM_API_TOKEN)
    podcast_script = podcast_gen.generate(news_articles)
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
