# LLM 应用开发两阶段学习路线

目标：从零开始掌握 LLM 应用开发，并能独立搭建一个可部署、可评估、可维护的智能体或 RAG 应用。

本教程分为两个阶段：

- **阶段一：快速入门**。用 8 天建立完整概念地图，跑通 Prompt、RAG、Agent、向量数据库、LangChain、API 和 Docker Demo。
- **阶段二：独立开发能力**。补齐工程化 Agent、进阶 RAG、评测、安全、部署和真实项目交付能力。

## 适合人群

- 会写基础 Python，希望进入大模型应用开发。
- 想从 Demo 走向真实业务系统。
- 想独立搭建智能体、知识库问答、自动化工作流或企业内部 AI 助手。

## 学完应具备的能力

完成阶段一后，你应该能：

- 调用主流大模型 API。
- 编写可靠的 Prompt。
- 搭建简单 RAG 知识库问答。
- 理解 Embedding、向量检索和 ChromaDB。
- 实现简单工具调用和 Agent 原型。
- 用 FastAPI 暴露一个基础问答接口。

完成阶段二后，你应该能：

- 设计可扩展的 Agent 状态机和工具系统。
- 处理工具调用失败、重试、权限控制和人工确认。
- 构建带元数据、引用、重排、增量更新的 RAG 系统。
- 建立评测集，做 RAG 和 Agent 回归测试。
- 处理 Prompt Injection、敏感信息和越权调用风险。
- 部署带日志、监控、配置和依赖锁定的生产服务。

## 阶段一：快速入门

| 天数 | 章节 | 内容 |
|------|------|------|
| Day 1 | [提示词工程](./01-prompt-engineering/) | Prompt、Few-shot、CoT、角色设定 |
| Day 2 | [RAG 核心](./02-rag-basics/) | 知识库问答、Embedding、检索增强生成 |
| Day 3 | [Agent 与工具调用](./03-agent-tool-use/) | Function calling、ReAct、多步骤执行 |
| Day 4 | [向量数据库](./04-vector-db/) | 向量相似度、ChromaDB 基础操作 |
| Day 5 | [生产级实践](./05-production/) | 日志、成本控制、简单评估 |
| Day 6 | [模型替代方案](./06-open-llm-alternatives/) | OpenAI、DeepSeek、Groq、Ollama、硅基流动 |
| Day 7 | [LangChain 快速入门](./07-langchain-fast-start/) | Chain、Retriever、Agent 快速原型 |
| Day 8 | [完整项目实战](./08-complete-project/) | 私有知识库、API、Docker 部署 |

## 阶段二：独立开发能力

| 模块 | 章节 | 目标 |
|------|------|------|
| Module 1 | [Agent 工程化](./09-agent-engineering/) | 从简单工具调用升级为可靠 Agent 状态机 |
| Module 2 | [RAG 进阶](./10-rag-advanced/) | 提升召回质量、答案可信度和知识库可维护性 |
| Module 3 | [评测与测试](./11-evaluation-testing/) | 建立可重复的质量评估和回归测试 |
| Module 4 | [安全与部署](./12-security-deployment/) | 处理安全风险，并上线可观测服务 |

## 技术栈

- Python 3.11+
- OpenAI SDK
- ChromaDB
- FastAPI + uvicorn
- LangChain / LangGraph 思路
- Docker / docker-compose
- 可选模型 Provider：OpenAI、DeepSeek、Groq、Ollama、硅基流动

## 快速开始

```bash
git clone https://github.com/vanhci/llm-quickstart.git
cd llm-quickstart
pip install -r requirements.txt

# OpenAI
export OPENAI_API_KEY=sk-xxx

# 或 DeepSeek
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-xxx

python 01-prompt-engineering/examples/01_basic.py
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="sk-xxx"
python 01-prompt-engineering/examples/01_basic.py
```

## 推荐学习方式

1. 先按阶段一顺序跑通所有示例，不急着改框架。
2. 每章至少完成一个练习，把示例改成自己的业务场景。
3. 进入阶段二后，以 `08-complete-project` 为基础逐步升级，不要重新造一个项目。
4. 每次升级都补一条测试或评估样例，避免只凭感觉判断效果。

## 项目结构

```text
.
├── 01-prompt-engineering
├── 02-rag-basics
├── 03-agent-tool-use
├── 04-vector-db
├── 05-production
├── 06-open-llm-alternatives
├── 07-langchain-fast-start
├── 08-complete-project
├── 09-agent-engineering
├── 10-rag-advanced
├── 11-evaluation-testing
├── 12-security-deployment
└── requirements.txt
```

## 重要提醒

- 教程示例偏学习用途，真实上线前必须补鉴权、日志、限流、输入校验、错误处理和安全策略。
- 不要在生产环境使用 `eval()` 执行模型返回内容。
- 模型价格、模型名和接口能力会变化，实际开发时应以各平台官方文档为准。
