# Day 4 · 向量数据库 —— 理解 Embedding 与相似度检索

## 什么是向量数据库？

专门存储"向量"的数据库，核心能力是：**找相似**。

传统数据库：精确匹配（WHERE name = "张三"）
向量数据库：相似搜索（找跟"张三"最相似的人）

---

## 什么是 Embedding？

**Embedding（嵌入）** 是把文字/图片/音频转换成一大串数字（向量）的技术。

转换规则：语义相近的内容，向量也"相近"。

```
"苹果水果"     → [0.23, -0.45, 0.78, 0.12, ...]
"新鲜橙子"     → [0.25, -0.43, 0.80, 0.10, ...]  ← 和上面很接近！
"iPhone 15"   → [-0.12, 0.67, -0.23, 0.89, ...] ← 差异较大
```

**相似度算法：** 余弦相似度、点积等。数值越高越相似。

---

## 传统数据库 vs 向量数据库

| | 传统数据库 | 向量数据库 |
|---|---|---|
| 存储内容 | 结构化数据 | 向量 + 原数据 |
| 查询方式 | 精确匹配 | 相似度检索 |
| 典型场景 | 订单、用户表 | 语义搜索、推荐 |
| 代表产品 | MySQL | ChromaDB, Milvus, Pinecone |

---

## ChromaDB 快速入门

ChromaDB 是最轻量的向量数据库，Python 原生支持，适合学习和中小规模应用。

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("my_docs")

# 添加文档
collection.add(
    documents=["苹果是水果", "香蕉也很甜"],
    ids=["1", "2"]
)

# 查询最相似的文档
results = collection.query(
    query_texts=["什么水果很甜？"],
    n_results=1
)
print(results)  # → ["香蕉也很甜"]
```

---

## 📂 示例代码

| 文件 | 内容 |
|------|------|
| `examples/01_embedding.py` | 用 OpenAI 生成 Embedding，计算文本相似度 |
| `examples/02_chroma_basic.py` | ChromaDB 基础：增删改查、相似度检索 |

```bash
pip install chromadb openai
python examples/01_embedding.py
```

---

## 📝 练习题

[`practice/exercise.md`](./practice/exercise.md) — 2道练习题，带参考答案