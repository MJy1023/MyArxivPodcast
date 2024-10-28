# 🎙️ Arxiv学术论文播客生成器 | Arxiv Academic Paper Podcast Generator

[English](README.md#english) | [中文](README.md#chinese)

---
<a name="chinese"></a>

# 🎙️ AI 科技新闻播客生成器

🤖 这是一个基于人工智能的科技新闻播客自动生成系统。该系统可以自动爬取最新的科技新闻,通过 LLM 生成播客脚本,并利用文本转语音技术生成逼真的播客音频。

## ✨ 功能特点

- 🔍 自动爬取 arXiv 等网站的最新科技新闻
- 🧠 使用大语言模型生成结构化的播客对话脚本
- 🎯 支持自定义关键词和时间范围的新闻筛选
- 🗣️ 通过百度文本转语音 API 生成自然的播客音频
- 📝 完整的日志记录和文章引用追踪
- 🎨 支持多种音色和语音参数调节

## 🛠️ 系统要求

- 🐍 Python 3.7+
- 📦 依赖包详见 requirements.txt

## 🚀 快速开始

### 1️⃣ 克隆项目并安装依赖:
```bash
git clone https://github.com/MJy1023/MyLLMPodcasts.git
cd MyLLMPodcasts
pip install -r requirements.txt
```

### 2️⃣ 配置 API 密钥:
在 `config.py` 中配置以下参数:
- 🔑 LLM API 密钥 (支持智谱AI)
- 🎤 百度文本转语音 API 密钥
- 🎯 目标网站和关键词设置

### 3️⃣ 运行程序:
```bash
python main.py
```

## 📂 输出内容

程序会在 `output` 目录下生成带时间戳的文件夹,包含:
- 📝 播客脚本文本 (podcast_script.txt)
- 🎵 音频文件 (podcast.mp3)
- 📊 文章引用信息 (article_references.json)
- 📋 运行日志 (logs/podcast_generation_*.log)

## ⚙️ 配置说明

可以在 `config.py` 中自定义以下配置:
- 🌐 目标网站和关键词
- ⏰ 新闻爬取的时间范围
- 🔧 API 设置
- 🎛️ 音频合成参数(语速、音调等)
- 📁 输出路径设置

## 📁 项目结构

```
.
├── main.py              # 🎯 主程序入口
├── config.py            # ⚙️ 配置文件
├── news_crawler.py      # 🕷️ 新闻爬虫模块
├── podcast_generator.py # 🎙️ 播客内容生成模块
├── text_to_speech.py   # 🗣️ 语音合成模块
├── prompt.py           # 💭 LLM 提示词模板
└── README.md           # 📖 项目说明文档
```

## 📄 许可证

[MIT License](LICENSE)

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目！让我们一起把这个项目变得更好！ 💪

## ⚠️ 注意事项

- 💫 请确保有足够的 API 调用额度
- ⏳ 音频生成可能需要较长时间,请耐心等待
- 🧹 建议定期清理临时文件和日志

## 🌟 Star History

如果你喜欢这个项目，欢迎点个 Star！✨

## 📮 联系方式

如有任何问题或建议，欢迎通过以下方式联系：
- 📧 Email: maojiayi1023@163.com
- 💬 Issues: [GitHub Issues](https://github.com/MJy1023/MyLLMPodcasts/issues)

---
<a name="english"></a>

# 🎙️ AI Tech News Podcast Generator

🤖 An AI-powered system that automatically generates tech news podcasts. It crawls the latest tech news, generates podcast scripts using LLM, and converts them into natural-sounding audio using text-to-speech technology.

## ✨ Features

- 🔍 Automatically crawl tech news from sources like arXiv
- 🧠 Generate structured podcast scripts using LLM
- 🎯 Customizable keywords and time range for news filtering
- 🗣️ Natural podcast audio generation via Baidu TTS API
- 📝 Complete logging and article reference tracking
- 🎨 Multiple voice options and audio parameter adjustments

## 🛠️ Requirements

- 🐍 Python 3.7+
- 📦 See requirements.txt for dependencies

## 🚀 Quick Start

### 1️⃣ Clone and Install:
```bash
git clone https://github.com/MJy1023/MyLLMPodcasts.git
cd MyLLMPodcasts
pip install -r requirements.txt
```

### 2️⃣ Configure API Keys:
```bash
# Copy configuration template
cp config.template.py config.py
```

Then configure in `config.py`:
- 🔑 LLM API key (Zhipu AI)
- 🎤 Baidu TTS API keys
- 🎯 Other settings...

### 3️⃣ Run:
```bash
python main.py
```

## 📂 Output

The program generates a timestamped folder in the `output` directory containing:
- 📝 Podcast script (podcast_script.txt)
- 🎵 Audio file (podcast.mp3)
- 📊 Article references (article_references.json)
- 📋 Logs (logs/podcast_generation_*.log)

## ⚙️ Configuration

Customize in `config.py`:
- 🌐 Target websites and keywords
- ⏰ News crawling timeframe
- 🔧 API settings
- 🎛️ Audio synthesis parameters
- 📁 Output path settings

## 📁 Project Structure

```
.
├── main.py              # 🎯 Main entry
├── config.py            # ⚙️ Configuration
├── news_crawler.py      # 🕷️ News crawler
├── podcast_generator.py # 🎙️ Content generator
├── text_to_speech.py   # 🗣️ TTS module
├── prompt.py           # 💭 LLM prompts
└── README.md           # 📖 Documentation
```

## 📄 License

[MIT License](LICENSE)

## 🤝 Contributing

Issues and PRs are welcome! Let's make this project better together! 💪

## ⚠️ Notes

- 💫 Ensure sufficient API quota
- ⏳ Audio generation may take time
- 🧹 Regular cleanup of temp files recommended

## 🌟 Star History

If you like this project, please give it a star! ✨

## 📮 Contact

For any questions or suggestions:
- 📧 Email: maojiayi1023@163.com
- 💬 Issues: [GitHub Issues](https://github.com/MJy1023/MyLLMPodcasts/issues)
