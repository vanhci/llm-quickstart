# Day 8 · 完整项目实战 —— 私有知识库问答系统

## 项目目标

从 0 搭建一个**可部署的私有知识库问答系统**：

- 支持上传文档（PDF/TXT/Markdown）
- 自动分块 + Embedding + 存入向量数据库
- 用户提问 → 检索相关段落 → 生成回答
- 提供 API 接口，支持流式输出
- 可 Docker 部署到服务器

---

## 项目架构

```
用户上传文档（PDF/TXT/MD）
         ↓
文档解析 → 文本分块（chunking）
         ↓
Embedding 模型（转成向量）
         ↓
存入 ChromaDB 向量数据库
         ↓
用户提问 → 检索 Top-K 相关块 → 注入 Prompt
         ↓
LLM 生成回答（流式输出）
         ↓
FastAPI 接口 → 前端 / 客户端调用
```

---

## 技术选型

| 模块 | 选型 | 说明 |
|------|------|------|
| 文档解析 | PyMuPDF / python-docx | PDF/Word/TXT 通用 |
| 分块策略 | 固定字数重叠 | 简单有效，够用 |
| Embedding | OpenAI text-embedding-3-small | 效果好，速度快 |
| 向量库 | ChromaDB | 轻量，易部署 |
| LLM | gpt-4o-mini / DeepSeek | 按需切换 |
| API 层 | FastAPI + uvicorn | Python 原生，性能好 |
| 部署 | Docker + docker-compose | 一键部署 |

---

## 项目文件结构

```
08-complete-project/
├── examples/
│   ├── 01_knowledge_base_setup.py    # 知识库构建
│   ├── 02_rag_qa_system.py           # 完整 RAG 问答系统
│   ├── 03_api_deploy.py              # FastAPI 服务
│   └── 04_docker_deploy.py            # Docker 配置
├── docs/                              # 示例文档
│   └── sample.txt
├── practice/
│   └── exercise.md
└── README.md
```

---

## 📂 示例代码

| 文件 | 内容 |
|------|------|
| `examples/01_knowledge_base_setup.py` | 文档读取 → 分块 → Embedding → 存入向量库 |
| `examples/02_rag_qa_system.py` | 完整 RAG 问答（检索 + 生成） |
| `examples/03_api_deploy.py` | FastAPI 服务，支持流式输出 |
| `examples/04_docker_deploy.py` | Docker + docker-compose 配置 |

---

## 🚀 快速体验

```bash
pip install langchain langchain-openai langchain-chroma fastapi uvicorn pymupdf python-docx

# 第1步：构建知识库
python examples/01_knowledge_base_setup.py

# 第2步：启动 RAG 问答
python examples/02_rag_qa_system.py

# 第3步：启动 API 服务
uvicorn examples/03_api_deploy:app --reload
# 访问 http://localhost:8000/docs 查看 API 文档
```

---

## 📝 练习题

[`practice/exercise.md`](./practice/exercise.md) — 3道实践题，带参考答案