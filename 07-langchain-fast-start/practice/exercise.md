## 练习题

### 题1：用 LangChain 实现客服机器人

**题目：** 用 `LLMChain` 重写第一章的电商客服机器人，比较手写版和 LangChain 版本的代码量差异。

**参考（LangChain 版本核心代码）：**
```python
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = PromptTemplate.from_template("""你是专业电商客服，请根据知识库回答：
{knowledge}
用户：{question}
要求：不超过3句话""")

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.invoke({"knowledge": "退货7天，发货24h...", "question": "几天能到？"})
```

---

### 题2：对比 RetrievalQA 的三种 chain_type

**题目：** LangChain 的 `RetrievalQA.from_chain_type` 支持不同的 `chain_type`，请查阅并对比 `stuff` / `map_reduce` / `refine` 三种模式的适用场景。

**参考答案：**

| 模式 | 原理 | 适用场景 | 缺点 |
|------|------|---------|------|
| `stuff` | 把所有检索结果塞进一个 Prompt | 数据量小（<5个文档） | 超出模型上下文就崩 |
| `map_reduce` | 每个文档单独回答，再汇总 | 大量文档（>10个） | 慢，可能丢细节 |
| `refine` | 逐文档迭代优化答案 | 答案需要逐步完善 | 最慢 |

**实操建议：** 小知识库用 `stuff`，大知识库用 `map_reduce`。