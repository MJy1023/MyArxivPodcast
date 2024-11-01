# Target websites and keywords
TARGET_WEBSITES = [
    "https://arxiv.org/"
]
KEYWORDS = ["LLM", "agent"]

# Crawl articles from the last DAYS_BACK days
DAYS_BACK = 5

# LLM API settings
LLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
LLM_API_TOKEN = "your-api-key"
LLM_MODLE = "glm-4-plus"

# Baidu Text-to-Speech API settings
BAIDU_API_KEY = "your-baidu-api-key"
BAIDU_SECRET_KEY = "your-baidu-secret-key"

# Output path settings
OUTPUT_DIR = "output"
PODCAST_SCRIPT_DIR = "output/scripts"
PODCAST_AUDIO_DIR = "output/podcasts"

# Language settings
LANGUAGE = "zh"  # Change to "en" for English

# Section names for different languages
SECTION_NAMES = {
    "en": {
        "RESEARCH_BACKGROUND": "Research Background & Motivation",
        "TECHNICAL_INNOVATION": "Technical Innovation & Methodology",
        "EXPERIMENTAL_RESULTS": "Experimental Results Analysis",
        "INDUSTRY_IMPACT": "Industry Impact & Future Prospects",
        "SUMMARY": "Summary"
    },
    "zh": {
        "RESEARCH_BACKGROUND": "研究背景与动机",
        "TECHNICAL_INNOVATION": "技术创新与方法",
        "EXPERIMENTAL_RESULTS": "实验结果分析",
        "INDUSTRY_IMPACT": "行业影响与展望",
        "SUMMARY": "总结"
    }
}

# Voice ID mappings for different languages
VOICE_IDS = {
    "en": {
        "HOST": 5,     # English male voice
        "GUEST": 4     # English female voice
    },
    "zh": {
        "HOST": 4140,  # Chinese male voice (Du Xiaoxin)
        "GUEST": 4129  # Chinese female voice (Du Xiaoyan)
    }
}

# Audio synthesis configuration
TTS_CONFIG = {
    # Basic settings
    'MAX_CHARS': 100,  # Maximum characters per request
    'PAUSE_DURATION': 500,  # Pause duration between dialogues (ms)
    
    # Host voice settings
    'HOST': {
        'LANGUAGE': LANGUAGE,
        'VOICE_ID': VOICE_IDS[LANGUAGE]["HOST"],
        'SPEED': 7,     # Speech rate
        'PITCH': 8,     # Pitch
        'VOLUME': 5     # Volume
    },
    
    # Guest voice settings
    'GUEST': {
        'LANGUAGE': LANGUAGE,
        'VOICE_ID': VOICE_IDS[LANGUAGE]["GUEST"],
        'SPEED': 6,
        'PITCH': 8,
        'VOLUME': 5
    }
}

# Temporary file settings
TEMP_AUDIO_DIR = "temp_audio"  # Temporary audio files directory
CLEAN_TEMP_FILES = True        # Whether to clean temporary files
