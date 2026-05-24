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
| Day 6 | [替代方案](./06-open-llm-alternatives/) | 国内可用：Ollama / DeepSeek / Groq |
| Day 7 | [LangChain 快速入门](./07-langchain-fast-start/) | 用主流框架快速搭 LLM 应用 |
| Day 8 | [完整项目实战](./08-complete-project/) | 从 0 搭建可部署的私有知识库系统 |

## 🛠️ 技术栈

- Python 3.11+
- OpenAI SDK (`pip install openai`)
- ChromaDB（向量数据库）
- **多 Provider 支持**：OpenAI / DeepSeek / Groq / Ollama / 硅基流动

## 🚀 快速开始

```bash
git clone https://github.com/vanhci/llm-quickstart.git
cd llm-quickstart
pip install openai chromadb

# 方式1：使用 DeepSeek（推荐国内用户）
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-xxx

# 方式2：使用 Ollama（完全免费，本地运行）
brew install ollama && ollama serve
export LLM_PROVIDER=ollama

# 运行示例
python 01-prompt-engineering/examples/01_basic.py
```

## 📖 每章内容

### Day 1 · 提示词工程
学习如何写好 Prompt，掌握 Few-shot、CoT、角色扮演等高级技巧。

### Day 2 · RAG 核心
让模型能够回答私有知识库的问题，实现"开卷考试"。

### Day 3 · Agent 与工具调用
让模型具备执行能力——查天气、搜资料、执行代码。多步骤任务规划 + 系统提示词工程。

### Day 4 · 向量数据库
理解 Embedding 的本质，掌握相似度检索的原理。

### Day 5 · 生产级实践
监控、成本控制、输出评估，让你的应用稳定可用。

### Day 6 · 替代方案
**国内重点！** OpenAI API 在国内用不了？这一章覆盖：DeepSeek（¥1/百万token）、Groq（免费）、Ollama（本地免费）、硅基流动，统一封装切换只改1行。

### Day 7 · LangChain 快速入门
LangChain 是最流行的 LLM 应用框架，这章只讲最核心的3个组件（LLMChain、RetrievalQA、Agent），让你**代码量减少70%**的同时快速搭出 RAG 和 Agent 原型。

### Day 8 · 完整项目实战
从 0 搭建一个**可部署的私有知识库问答系统**：文档读取 → 分块 → Embedding → 向量库 → 检索 → 生成 → FastAPI API → Docker 部署。学完这章，你的前端/客户端就能调用你的专属 AI 服务了。

---

## 📝 练习说明

每章 `practice/exercise.md` 包含 2 道练习题，带参考答案。建议先自己思考，再看答案对照。