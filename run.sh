# 批量生成中文播客
python main.py --mode batch --language zh

# 生成单篇英文播客
python main.py --mode single --language en --topic "LLM Agent"

# 通过ID生成特定文章的播客
python main.py --mode single --language zh --identifier "2401.xxxxx"