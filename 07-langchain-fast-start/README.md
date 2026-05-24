# Day 7 · LangChain 快速入门 —— 用主流框架搭 LLM 应用

## 为什么要学 LangChain？

手写 RAG、Agent 链路代码很长？LangChain 把这些都封装好了，**同样的功能，代码少 70%**。

> 学框架不是为了依赖它，而是**快速搭原型，验证思路**，验证完可以用手写实现替换核心部分。

---

## 核心三件套（学会就够了）

LangChain 内容很多，但**90% 的场景只需要这3个**：

### 1. LLMChain —— 提示词 + 模型封装

最基础的链：Prompt → Model → Output

```python
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# 1. 定义 Prompt
prompt = PromptTemplate.from_template(
    "你是一个{role}，用{style}风格回答：{question}"
)

# 2. 创建模型
llm = ChatOpenAI(model="gpt-4o-mini")

# 3. 组合成 Chain
chain = LLMChain(llm=llm, prompt=prompt)

# 4. 一行调用
result = chain.invoke({
    "role": "厨师",
    "style": "幽默",
    "question": "怎么做红烧肉"
})
print(result["text"])
```

---

### 2. RetrievalQA —— RAG 专用链

把文档检索和问答连起来，一行实现 RAG。

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

# 向量数据库
embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory="./chroma_data", embedding_function=embeddings)

# RAG 问答链
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    chain_type="stuff"  # 把检索结果塞进一个 Prompt
)

# 一行问答
result = qa_chain.invoke("退货政策是什么？")
print(result["result"])
```

---

### 3. AgentExecutor —— Agent 执行循环

自动多步推理 + 工具调用，一条命令搞定。

```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool

@tool
def search_weather(city: str) -> str:
    """查询城市天气"""
    return f"{city}今天晴，26度"

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [search_weather]

# 初始化 Agent
agent = initialize_agent(
    tools, llm, agent_type="react-docstore", verbose=True
)

# 自动多步执行
result = agent.invoke("北京今天天气怎么样？")
print(result["output"])
```

---

## 快速对比：手写 vs LangChain

| 任务 | 手写（行数） | LangChain（行数） |
|------|------------|-----------------|
| 简单对话 | 30行 | 10行 |
| RAG 问答 | 80行 | 15行 |
| 带工具的 Agent | 150行 | 30行 |

---

## 📂 示例代码

| 文件 | 内容 |
|------|------|
| `examples/01_llm_chain.py` | LLMChain 三种用法演示 |
| `examples/02_rag_chain.py` | RetrievalQA 实现 RAG 问答 |
| `examples/03_conversation_agent.py` | ConversationalAgent 实现记忆对话 |

```bash
pip install langchain langchain-openai langchain-chroma
python examples/01_llm_chain.py
```

---

## 安装依赖

```bash
pip install langchain langchain-openai langchain-chroma langchain-community
```

---

## 📝 练习题

[`practice/exercise.md`](./practice/exercise.md) — 2道练习题，带参考答案