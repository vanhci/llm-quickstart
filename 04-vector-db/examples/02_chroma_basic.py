#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChromaDB 基础操作：增删改查、相似度检索
功能：ChromaDB 的 CRUD 操作，以及基于向量的语义检索
运行：python 02_chroma_basic.py
依赖：pip install chromadb openai
"""

import os
from openai import OpenAI
import chromadb

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 初始化 ChromaDB 持久化客户端
chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_or_create_collection("demo")

# 初始化一些文档
INIT_DOCS = [
    "Python 是一门易学的编程语言，适合初学者",
    "JavaScript 主要用于网页前端开发",
    "机器学习是人工智能的一个分支",
    "数据分析用 Python 的 pandas 库很方便",
    "React 是 Facebook 开发的 UI 框架",
]
if collection.count() == 0:
    collection.add(
        documents=INIT_DOCS,
        ids=[f"doc_{i}" for i in range(len(INIT_DOCS))]
    )


def get_embedding(text: str) -> list[float]:
    """获取文本向量"""
    resp = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return resp.data[0].embedding


def search_similar(query: str, top_k: int = 3) -> list[dict]:
    """语义检索：找与 query 最相似的文档"""
    q_emb = get_embedding(query)
    results = collection.query(query_embeddings=[q_emb], n_results=top_k)
    hits = []
    for i in range(len(results["ids"][0])):
        hits.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i] if results.get("distances") else None,
        })
    return hits


def add_doc(doc_id: str, text: str):
    """新增文档"""
    collection.add(documents=[text], ids=[doc_id])
    print(f"✅ 新增文档: [{doc_id}] {text[:30]}...")


def delete_doc(doc_id: str):
    """删除文档"""
    collection.delete(ids=[doc_id])
    print(f"🗑️ 删除文档: {doc_id}")


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    print("=" * 55)
    print("📚 ChromaDB 基础操作演示")
    print("=" * 55)

    # 语义检索示例
    queries = ["编程入门推荐", "网页开发用什么", "AI 相关的内容"]
    for q in queries:
        print(f"\n🔍 搜索：{q}")
        hits = search_similar(q)
        for i, hit in enumerate(hits, 1):
            print(f"  {i}. [{hit['id']}] {hit['text']}  (距离: {hit['distance']:.4f})")

    # 增删示例
    print("\n" + "-" * 40)
    add_doc("doc_new", "Go 是 Google 开发的编译型编程语言")
    hits = search_similar("Google 的编程语言")
    print(f"  → 结果: {hits[0]['text']}")


if __name__ == "__main__":
    main()