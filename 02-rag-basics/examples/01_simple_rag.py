#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单 RAG 实现：基于 ChromaDB 的知识库问答
功能：预先存入文档，用户提问时检索相关段落，再让模型基于检索结果回答
运行：python 01_simple_rag.py
依赖：pip install chromadb openai
"""

import os
from openai import OpenAI
import chromadb

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 初始化 ChromaDB（持久化存储到本地）
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("knowledge_base")


def init_knowledge_base():
    """初始化知识库：存入几条文档"""
    docs = [
        "我们的退货政策是收到商品后7天内可以申请退货，运费由买家承担。",
        "发货时间：工作日下单后24小时内发货，周末订单周一处理。默认使用顺丰快递。",
        "会员等级分为普通、银卡、金卡、钻石卡，升级需要累计消费满一定金额。",
        "如何申请发票：在个人中心 → 订单详情 → 申请发票，支持电子发票和纸质发票。",
        "优惠活动：新人首单减10元，满200减20，满500减50，关注店铺领5元券。",
    ]
    collection.add(
        documents=docs,
        ids=[f"doc_{i}" for i in range(len(docs))]
    )
    print(f"✅ 知识库初始化完成，存入 {len(docs)} 条文档")


def retrieve(query: str, top_k: int = 3) -> list[str]:
    """检索最相关的文档"""
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0] if results["documents"] else []


def rag_answer(question: str) -> str:
    """RAG 流程：检索 + 生成"""
    # 1. 从知识库检索相关文档
    relevant_docs = retrieve(question)
    if not relevant_docs:
        return "抱歉，知识库中没有找到相关信息。"

    # 2. 把检索结果注入 Prompt
    context = "\n".join(f"- {doc}" for doc in relevant_docs)
    prompt = f"""基于以下知识库回答用户问题。如果知识库没有相关信息，请说"我没有找到相关内容"。

【知识库】
{context}

【用户问题】
{question}

【要求】回答简洁，结合知识库内容。"""

    # 3. 调用大模型生成
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300,
    )
    return response.choices[0].message.content


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    # 初始化知识库
    init_knowledge_base()

    # 测试问答
    questions = [
        "我想退货，几天可以申请？",
        "新人有什么优惠？",
        "一般几天能收到货？",
    ]

    print("\n" + "=" * 50)
    print("🔍 RAG 知识库问答测试")
    print("=" * 50)

    for q in questions:
        print(f"\n❓ 问题：{q}")
        print(f"💡 回答：{rag_answer(q)}")


if __name__ == "__main__":
    main()