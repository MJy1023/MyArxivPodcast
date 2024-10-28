talk_generate_prompt_zh = """你是一个专业的科技播客编导。请基于以下科技新闻生成一段结构化的对话式播客脚本。

输出要求：
请以JSON格式输出，结构如下：
{
    "podcast": {
        "opening": [
            {"role": "host", "content": "开场白内容"},
            {"role": "guest", "content": "回应内容"}
        ],
        "main_content": [
            {
                "article_index": 1,
                "discussion": [
                    {"role": "host", "content": "话题引入"},
                    {"role": "guest", "content": "回应内容"},
                    ...
                ]
            },
            {
                "article_index": 2,
                "discussion": [
                    {"role": "host", "content": "话题引入"},
                    {"role": "guest", "content": "回应内容"},
                    ...
                ]
            }
        ],
        "closing": [
            {"role": "host", "content": "总结内容"},
            {"role": "guest", "content": "补充内容"},
            {"role": "host", "content": "下期预告"}
        ]
    }
}

内容要求：
1. 对话风格：
   - 使用中文
   - 可以直接使用专业术语和行业术语，适当补充背景信息
   - 鼓励使用具体的技术细节和数据支持观点
   - 对话要有逻辑性和连贯性，体现专业思维
   - 对话最好能够在两个角色的互动中层层递进，主持人起到引导、追问和串联总结的作用，嘉宾主要通过专业知识深入回答问题
   
2. 每篇文章的讨论需要包含:
   - 技术背景分析和行业现状概述
   - 深入剖析技术原理和实现机制
   - 探讨技术架构选择的优劣
   - 分析对行业发展的深远影响
   - 讨论潜在的技术挑战和解决方案
   - 预测技术发展趋势和未来方向

3. 长度控制：
   - 一共包含5-10篇文章的讨论
   - 每段content建议30-60个字(约60-120个GBK字节)，保持简洁精炼
   - 每篇文章的discussion数组长度保持6-8个对话轮次
   - opening数组包含简要技术背景，2个对话
   - closing数组总结关键点，2-3个对话

以下是今天要讨论的文章：

"""

talk_generate_prompt_en = """You are a professional tech podcast producer. Please generate a structured dialogue podcast script based on the following tech news.

Output requirements:
Please output in JSON format with the following structure:
{
    "podcast": {
        "opening": [
            {"role": "host", "content": "opening content"},
            {"role": "guest", "content": "response content"}
        ],
        "main_content": [
            {
                "article_index": 1,
                "discussion": [
                    {"role": "host", "content": "topic introduction"},
                    {"role": "guest", "content": "response content"},
                    ...
                ]
            },
            {
                "article_index": 2,
                "discussion": [
                    {"role": "host", "content": "topic introduction"},
                    {"role": "guest", "content": "response content"},
                    ...
                ]
            }
        ],
        "closing": [
            {"role": "host", "content": "summary content"},
            {"role": "guest", "content": "additional insights"},
            {"role": "host", "content": "next episode preview"}
        ]
    }
}
    
Content requirements:
1. Dialogue style:
   - Use English
   - Use professional and industry terms, with appropriate background information
   - Encourage the use of specific technical details and data to support viewpoints
   - Dialogue should be logical and coherent, reflecting professional thinking
   - Dialogue should progress through interaction between the two roles
   - Host should guide, probe, and connect topics
   - Guest should provide in-depth answers with professional knowledge
   
2. Each article discussion should include:
   - Technical background analysis and industry status overview
   - In-depth analysis of technical principles and implementation mechanisms
   - Discussion of technical architecture choices pros and cons
   - Analysis of long-term impact on industry development
   - Discussion of potential technical challenges and solutions
   - Prediction of technology development trends and future directions

3. Length control:
   - Include discussions of 5-10 articles in total
   - Each content segment should be 30-60 words, keeping it concise
   - Each article's discussion array should maintain 6-8 dialogue rounds
   - Opening array includes brief technical background, 2 dialogues
   - Closing array summarizes key points, 2-3 dialogues

Here are today's articles for discussion:

"""
