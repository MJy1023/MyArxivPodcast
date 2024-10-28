import requests
import json
from prompt import talk_generate_prompt_en, talk_generate_prompt_zh
import re
import logging
import config
logging.basicConfig(level=logging.INFO)

class PodcastGenerator:
    def __init__(self, api_url, api_token, max_retries=3):
        self.api_url = api_url
        self.api_token = api_token
        self.max_retries = max_retries

    def generate(self, news_articles):
        prompt = self._create_prompt(news_articles)
        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "glm-4-plus",
                    "messages": [{"role": "user", "content": prompt}]
                }
                response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
                response_json = response.json()
                content = response_json['choices'][0]['message']['content']
                logging.info(f"Generated content:\n {content}")
                
                # Try to parse and process content
                processed_content = self._post_process_content(content)
                return processed_content

            except (json.JSONDecodeError, KeyError) as e:
                retry_count += 1
                last_error = str(e)
                logging.warning(f"Generation attempt {retry_count} failed: {last_error}")
                
                if retry_count < self.max_retries:
                    # Add error message to prompt and retry
                    error_message = f"""

Last generation failed with error: {last_error}
Please ensure the generated content is valid JSON format and strictly follows this structure:
{{
    "podcast": {{
        "opening": [
            {{"role": "host", "content": "..."}},
            {{"role": "guest", "content": "..."}}
        ],
        "main_content": [
            {{
                "article_index": 1,
                "discussion": [
                    {{"role": "host", "content": "..."}},
                    {{"role": "guest", "content": "..."}}
                ]
            }}
        ],
        "closing": [
            {{"role": "host", "content": "..."}},
            {{"role": "guest", "content": "..."}}
        ]
    }}
}}

Please regenerate the content:
"""
                    prompt += error_message
                else:
                    logging.error(f"Reached maximum retry attempts ({self.max_retries}), generation failed")
                    raise Exception(f"Failed to generate podcast content, last error: {last_error}")

    def _create_prompt(self, news_articles):
        # Select prompt based on language setting
        prompt = talk_generate_prompt_en if config.LANGUAGE == "en" else talk_generate_prompt_zh
        
        # Add language-specific formatting for articles
        article_format = {
            "en": "Title: {}\nDate: {}\nContent: {}\nSource: {}\n\n",
            "zh": "标题：{}\n日期：{}\n内容：{}\n来源：{}\n\n"
        }
        
        for article in news_articles:
            prompt += article_format[config.LANGUAGE].format(
                article['title'],
                article['published_date'],
                article['content'],
                article['source']
            )
        
        # Add language-specific closing instruction
        closing_instruction = {
            "en": "Please present in dialogue form, including host and guest interactions, maintaining an engaging and professional tone.",
            "zh": "请以对话形式呈现，包含主持人和嘉宾的互动，保持专业性和趣味性。"
        }
        prompt += closing_instruction[config.LANGUAGE]
        return prompt

    def _post_process_content(self, content):
        """Post-process the generated content to ensure correct format"""
        try:
            # Use regex to match JSON content
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                content = json_match.group(0)
            
            # Parse JSON content
            podcast_data = json.loads(content)
            processed_lines = []
            
            # Use language-specific role names
            role_names = {
                "en": {"host": "Host", "guest": "Guest"},
                "zh": {"host": "主持人", "guest": "嘉宾"}
            }[config.LANGUAGE]
            
            # Process opening
            for dialog in podcast_data['podcast']['opening']:
                role = role_names["host"] if dialog['role'] == "host" else role_names["guest"]
                processed_lines.append(f"{role}: {dialog['content']}")
            
            # Process main content
            for article in podcast_data['podcast']['main_content']:
                for dialog in article['discussion']:
                    role = role_names["host"] if dialog['role'] == "host" else role_names["guest"]
                    processed_lines.append(f"{role}: {dialog['content']}")
            
            # Process closing
            for dialog in podcast_data['podcast']['closing']:
                role = role_names["host"] if dialog['role'] == "host" else role_names["guest"]
                processed_lines.append(f"{role}: {dialog['content']}")
            
            return '\n'.join(processed_lines)
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed, invalid format: {str(e)}")
            raise
        except KeyError as e:
            logging.error(f"JSON structure incomplete, missing required keys: {str(e)}")
            raise
