## 练习题

### 题1：实现一个简单 RAG

**题目：** 请补全下面的 RAG 流程代码，实现根据用户问题从知识库检索相关文档，并基于文档回答。

```python
def simple_rag(question: str) -> str:
    # 第1步：把问题转成向量（用 OpenAI embedding）
    query_embedding = ...

    # 第2步：向量数据库检索 Top-3 相关文档
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    # 第3步：构建 Prompt，把检索结果注入
    context = ...
    prompt = f"根据以下内容回答：{context}\n\n问题：{question}"

    # 第4步：调用模型生成回答
    response = client.chat.completions.create(...)
    return response.choices[0].message.content
```

**提示：**
- 用 `openai.embeddings.create(input=[text], model="text-embedding-3-small")` 获取向量
- ChromaDB 的 `collection.query()` 接受 `query_embeddings` 参数

---

### 题2：RAG vs 直接问答 对比

**题目：** 解释为什么 RAG 能减少模型"幻觉"（编造答案）？什么场景下 RAG 效果不明显？

**参考答案：**

**为什么 RAG 能减少幻觉：**
模型不知道你公司的内部信息，直接回答时会"凭经验编"。RAG 把相关资料注入 Prompt，模型被强制"看资料答题"，减少胡编。

**RAG 效果不明显的场景：**
1. 通用常识问题（"水的沸点是多少"）—— 模型本来就知道，不需要 RAG
2. 推理型问题（"如果...会怎样"）—— 知识库没有推理依据，RAG 帮不上
3. 创意任务（"写一首诗"）—— 不需要准确事实，RAG 反而限制发挥