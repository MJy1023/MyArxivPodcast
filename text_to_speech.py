import requests
import json
import time
import os
from pydub import AudioSegment
from config import TTS_CONFIG

class TextToSpeech:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.post(url, params=params)
        return response.json().get("access_token")

    def create_tts_task(self, text, voice_config):
        """Create long text to speech task"""
        url = f"https://aip.baidubce.com/rpc/2.0/tts/v1/create?access_token={self.access_token}"
        
        # Adjust parameters based on language
        language = voice_config['LANGUAGE']
        payload = json.dumps({
            "text": text,
            "format": "mp3-16k",
            "voice": voice_config['VOICE_ID'],
            "lang": language,
            "speed": voice_config['SPEED'],
            "pitch": voice_config['PITCH'],
            "volume": voice_config['VOLUME'],
            "enable_subtitle": 0
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        result = response.json()
        if 'error_code' in result:
            raise Exception(f"Task creation failed: {result}")
        return result.get("task_id")

    def query_tts_result(self, task_id):
        url = f"https://aip.baidubce.com/rpc/2.0/tts/v1/query?access_token={self.access_token}"
        payload = json.dumps({"task_ids": [task_id]})
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        return response.json()

    def convert(self, text, output_path):
        task_id = self.create_tts_task(text)
        while True:
            result = self.query_tts_result(task_id)
            task_info = result.get("tasks_info", [])[0]
            if task_info["task_status"] == "Success":
                speech_url = task_info["task_result"]["speech_url"]
                audio_response = requests.get(speech_url)
                with open(output_path, "wb") as f:
                    f.write(audio_response.content)
                return output_path
            elif task_info["task_status"] == "Failed":
                raise Exception("Text to speech conversion failed")
            time.sleep(2)  # Wait 2 seconds before next query

    def convert_dialog(self, text, output_dir):
        """Convert dialogue text to multiple audio files and merge them"""
        dialog_parts = []
        current_speaker = None
        current_text = []
        
        # Support more dialogue marker formats
        host_markers = ['Host:', '主持人:', '主播:']
        guest_markers = ['Guest:', '嘉宾:', '客人:']
        
        for line in text.split('\n'):
            if any(line.startswith(marker) for marker in host_markers):
                if current_speaker:
                    dialog_parts.append((current_speaker, ''.join(current_text)))
                current_speaker = 'Host'
                # Remove all possible markers
                for marker in host_markers:
                    line = line.replace(marker, '')
                current_text = [line]
            elif any(line.startswith(marker) for marker in guest_markers):
                if current_speaker:
                    dialog_parts.append((current_speaker, ''.join(current_text)))
                current_speaker = 'Guest'
                # Remove all possible markers
                for marker in guest_markers:
                    line = line.replace(marker, '')
                current_text = [line]
            elif line.strip():
                if current_speaker:
                    current_text.append(line)
        
        if current_speaker and current_text:
            dialog_parts.append((current_speaker, ''.join(current_text)))

        # Generate audio for each dialogue part
        audio_files = []
        for i, (speaker, content) in enumerate(dialog_parts):
            content_parts = self._split_text(content)
            voice_config = TTS_CONFIG['HOST'] if speaker == 'Host' else TTS_CONFIG['GUEST']
            
            for j, part in enumerate(content_parts):
                try:
                    # Try using short text API
                    url = "http://tsn.baidu.com/text2audio"
                    params = {
                        "tex": part,
                        "tok": self.access_token,
                        "cuid": "python_demo",
                        "ctp": 1,
                        "lan": voice_config['LANGUAGE'],  # Use language from config
                        "spd": voice_config['SPEED'],
                        "pit": voice_config['PITCH'],
                        "vol": voice_config['VOLUME'],
                        "per": voice_config['VOICE_ID'],
                        "aue": 3
                    }
                    
                    response = requests.post(url, params=params)
                    if response.headers['Content-Type'].startswith('audio'):
                        temp_file = os.path.join(output_dir, f'part_{i}_{j}.mp3')
                        with open(temp_file, "wb") as f:
                            f.write(response.content)
                        audio_files.append(temp_file)
                    else:
                        raise Exception(f"Short text API conversion failed: {response.json()}")
                        
                except Exception as e:
                    print(f"Short text API failed, trying long text API: {str(e)}")
                    # Use long text API
                    try:
                        task_id = self.create_tts_task(part, voice_config)
                        while True:
                            result = self.query_tts_result(task_id)
                            task_info = result.get("tasks_info", [])[0]
                            if task_info["task_status"] == "Success":
                                speech_url = task_info["task_result"]["speech_url"]
                                audio_response = requests.get(speech_url)
                                temp_file = os.path.join(output_dir, f'part_{i}_{j}.mp3')
                                with open(temp_file, "wb") as f:
                                    f.write(audio_response.content)
                                audio_files.append(temp_file)
                                break
                            elif task_info["task_status"] == "Failed":
                                error_msg = task_info.get("task_result", {}).get("error_msg", "Unknown error")
                                raise Exception(f"Long text API conversion failed: {error_msg}")
                            time.sleep(2)
                    except Exception as e:
                        raise Exception(f"All API conversions failed: {str(e)}")

        return audio_files

    def _split_text(self, text):
        """Split long text into smaller segments, with special handling for Chinese text"""
        max_chars = 500
        parts = []
        
        # Use different split logic for Chinese text
        if any('\u4e00' <= char <= '\u9fff' for char in text):
            # Use Chinese punctuation marks for splitting
            separators = ['。', '！', '？', '；']
            current_part = ''
            
            for char in text:
                current_part += char
                if len(current_part) >= max_chars or (char in separators and current_part):
                    parts.append(current_part)
                    current_part = ''
            
            if current_part:
                parts.append(current_part)
        else:
            # Original English split logic
            sentences = text.split('.')
            current_part = []
            current_length = 0
            
            for sentence in sentences:
                sentence = sentence.strip() + '.'
                if current_length + len(sentence) <= max_chars:
                    current_part.append(sentence)
                    current_length += len(sentence)
                else:
                    if current_part:
                        parts.append(''.join(current_part))
                    current_part = [sentence]
                    current_length = len(sentence)
            
            if current_part:
                parts.append(''.join(current_part))
        
        return parts

    def merge_audio_files(self, audio_files, output_path):
        """Merge multiple audio files"""
        try:
            combined = AudioSegment.empty()
            for audio_file in audio_files:
                segment = AudioSegment.from_mp3(audio_file)
                combined += segment
                # Add brief pause
                combined += AudioSegment.silent(duration=500)  # Add 500ms pause
            
            # Export merged audio file
            combined.export(output_path, format="mp3")
            
            # Delete temporary files
            for audio_file in audio_files:
                try:
                    os.remove(audio_file)
                except Exception as e:
                    print(f"Failed to delete temporary file: {e}")
            
            return output_path
        except Exception as e:
            raise Exception(f"Failed to merge audio files: {e}")
