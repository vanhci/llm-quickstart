# LLM 应用开发快速入门教程生成任务

## 项目目录
/Users/vanhci/works/llm-quickstart

## 任务描述

在指定目录下创建一套完整的 LLM 应用开发快速入门教程，用于 GitHub 发布。

## 需要创建的文件

### 1. 根目录 README.md（教程索引）

内容：
- 标题：🧠 LLM 应用开发快速入门
- 副标题：从零开始，5天搞定 LLM 应用开发
- 学习路径表格（Day 1-5）
- 技术栈说明（Python 3.11+, OpenAI SDK, ChromaDB）
- 快速开始代码块（克隆、安装依赖、设置KEY、运行示例）

### 2. 第一章：01-prompt-engineering/

**README.md**：
- Day 1 · 提示词工程
- 通俗解释什么是 Prompt Engineering（100字）
- 核心原则：清晰具体 + 给例子 + 分解任务
- 常用技巧：Few-shot、Chain of Thought、角色扮演
- 2个 Mermaid ASCII 流程图
- 2个完整可运行 Python 示例引用
- 练习题引用

**examples/01_basic.py**：
- 文件名：电商客服自动回复机器人
- 功能：根据用户问题自动回复
- 要求：使用 os.environ.get('OPENAI_API_KEY')，完整可运行，中文注释

**examples/02_advanced.py**：
- 文件名：Chain of Thought 数学解题助手
- 功能：用 CoT 引导模型一步步解题
- 要求：完整可运行，中文注释

**practice/exercise.md**：
- 2道练习题 + 参考答案

### 3. 第二章：02-rag-basics/

**README.md**：
- Day 2 · RAG 核心
- 通俗解释 RAG 是什么（类比"开卷考试"）
- RAG 工作流程图（Mermaid）
- Embedding 概念通俗解释
- 完整可运行示例引用

**examples/01_simple_rag.py**：
- 简单 RAG 实现：知识库问答
- 要求：使用 ChromaDB 存储向量，完整可运行，中文注释

**examples/02_rag_with_search.py**：
- 带搜索的 RAG 实现
- 要求：中文注释，完整可运行

**practice/exercise.md**：
- 2道练习题 + 参考答案

### 4. 第三章：03-agent-tool-use/

**README.md**：
- Day 3 · Agent 与工具调用
- 通俗解释 Agent（像"实习生"一样工作）
- ReAct 模式流程（Mermaid图）
- 工具调用示例图

**examples/01_tool_calling.py**：
- 基础工具调用：让模型搜索天气
- 要求：模拟工具调用，中文注释，完整可运行

**examples/02_simple_agent.py**：
- 简单 Agent 实现
- 要求：中文注释，完整可运行

**practice/exercise.md**：
- 2道练习题 + 参考答案

### 5. 第四章：04-vector-db/

**README.md**：
- Day 4 · 向量数据库
- 通俗解释 Embedding 和向量相似度
- ChromaDB 快速入门
- 对比传统数据库 vs 向量数据库

**examples/01_embedding.py**：
- 生成文本 Embedding
- 计算相似度
- 要求：使用 OpenAI embeddings API，中文注释

**examples/02_chroma_basic.py**：
- ChromaDB 基础操作
- 要求：中文注释，完整可运行

**practice/exercise.md**：
- 2道练习题 + 参考答案

### 6. 第五章：05-production/

**README.md**：
- Day 5 · 生产级实践
- 监控与日志
- 成本控制策略
- 输出质量评估
- 常见陷阱与解决方案

**examples/01_cost_control.py**：
- Token 计费与成本控制示例
- 要求：中文注释，完整可运行

**examples/02_evaluation.py**：
- 简单输出评估示例
- 要求：中文注释，完整可运行

**practice/exercise.md**：
- 2道练习题 + 参考答案

## 重要规范

1. **所有文档和代码注释使用中文**
2. **Python 代码必须完整可运行**，使用 `os.environ.get('OPENAI_API_KEY')` 读取 API key
3. **代码必须有中文注释**
4. **每个示例代码要有使用说明注释**（顶部说明功能、运行方式）
5. **GitHub 提交时使用中文 commit message**
6. **案例要贴近真实场景**

## 执行顺序

1. 先写 README.md 索引
2. 按顺序写第1-5章，每章写完报告进度
3. 最后初始化 git 仓库

## 输出要求

每写完一章，在终端输出「✅ 第X章完成」
全部写完后输出「🎉 全部完成」并显示创建的文件列表。