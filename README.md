# 🧠 LLM 应用开发快速入门

从零开始，5天搞定 LLM 应用开发。

## 📚 学习路径

| 天数 | 章节 | 内容 |
|------|------|------|
| Day 1 | [提示词工程](./01-prompt-engineering/) | 写好 Prompt，让模型听懂你的话 |
| Day 2 | [RAG 核心](./02-rag-basics/) | 让模型"读懂"你的知识库 |
| Day 3 | [Agent 与工具调用](./03-agent-tool-use/) | 让模型帮你执行操作 |
| Day 4 | [向量数据库](./04-vector-db/) | 理解 Embedding 与相似度检索 |
| Day 5 | [生产级实践](./05-production/) | 监控、成本控制、评估 |

## 🛠️ 技术栈

- Python 3.11+
- OpenAI SDK (`pip install openai`)
- ChromaDB (`pip install chromadb`)
- 环境变量: `OPENAI_API_KEY`

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/vanhci/llm-quickstart.git
cd llm-quickstart

# 安装依赖
pip install openai chromadb

# 设置 API Key
export OPENAI_API_KEY=sk-...

# 运行示例
python 01-prompt-engineering/examples/01_basic.py
```

## 📖 每章内容

### Day 1 · 提示词工程
学习如何写好 Prompt，掌握 Few-shot、CoT、角色扮演等高级技巧。

### Day 2 · RAG 核心
让模型能够回答私有知识库的问题，实现"开卷考试"。

### Day 3 · Agent 与工具调用
让模型具备执行能力——查天气、搜资料、执行代码。

### Day 4 · 向量数据库
理解 Embedding 的本质，掌握相似度检索的原理。

### Day 5 · 生产级实践
监控、成本控制、输出评估，让你的应用稳定可用。

---

## 📝 练习说明

每章 `practice/exercise.md` 包含 2 道练习题，带参考答案。建议先自己思考，再看答案对照。