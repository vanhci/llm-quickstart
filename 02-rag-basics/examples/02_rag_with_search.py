#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带关键词预筛选的 RAG
功能：先用关键词过滤候选文档，再用向量检索，提高准确性
运行：python 02_rag_with_search.py
依赖：pip install chromadb openai
"""

import os, re
from openai import OpenAI
import chromadb

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("kb_with_filter")


# 带元数据的文档（可用于关键词过滤）
DOCS = [
    {"id": "p1", "text": "退货政策：7天内可申请退货，运费由买家承担，需要商品完好。", "category": "售后"},
    {"id": "p2", "text": "发货时间：工作日24小时内发货，周末周一发，默认顺丰。", "category": "物流"},
    {"id": "p3", "text": "会员等级：普通/银卡/金卡/钻石卡，累计消费升级。", "category": "会员"},
    {"id": "p4", "text": "优惠：新人减10元，满200减20，满500减50。", "category": "优惠"},
    {"id": "p5", "text": "发票申请：个人中心 → 订单详情 → 申请电子或纸质发票。", "category": "售后"},
]

# 初始化
for doc in DOCS:
    collection.add(documents=[doc["text"]], ids=[doc["id"]])


def keyword_filter(query: str, docs: list) -> list:
    """关键词预筛选：根据问题中的关键词过滤候选文档"""
    # 提取问题中的关键词（简单实现）
    keywords = re.findall(r'[\w]{2,}', query)
    filtered = []
    for doc in docs:
        text_lower = doc["text"].lower()
        matched = sum(1 for kw in keywords if kw.lower() in text_lower)
        if matched > 0:
            filtered.append((doc, matched))
    # 按匹配度排序
    filtered.sort(key=lambda x: x[1], reverse=True)
    return [f[0] for f in filtered]


def hybrid_search(query: str, top_k: int = 3) -> list[str]:
    """混合搜索：关键词筛选 + 向量检索"""
    # 1. 向量检索
    results = collection.query(query_texts=[query], n_results=top_k)
    vector_hits = results["documents"][0] if results["documents"] else []

    # 2. 关键词筛选
    filtered = keyword_filter(query, DOCS)

    # 3. 合并去重（向量命中的优先）
    seen = set()
    combined = []
    for doc in vector_hits:
        combined.append(doc)
        seen.add(doc)

    for doc_data in filtered:
        if doc_data["text"] not in seen and len(combined) < top_k:
            combined.append(doc_data["text"])
            seen.add(doc_data["text"])

    return combined[:top_k]


def rag_answer(question: str) -> str:
    """带预筛选的 RAG 回答"""
    hits = hybrid_search(question)
    if not hits:
        return "没有找到相关信息。"

    context = "\n".join(f"- {h}" for h in hits)
    prompt = f"""根据以下知识库回答：

{context}

问题：{question}
回答（简洁）："""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    for q in ["我想申请发票", "退货怎么操作", "会员有什么优惠"]:
        print(f"\n❓ {q}")
        print(f"💡 {rag_answer(q)}")


if __name__ == "__main__":
    main()