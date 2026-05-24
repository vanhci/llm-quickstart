#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成文本 Embedding 并计算相似度
功能：用 OpenAI 生成文本向量，计算两段文本的余弦相似度
运行：python 01_embedding.py
依赖：pip install openai
"""

import os, math
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """调用 OpenAI API 获取文本的向量表示"""
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算两个向量的余弦相似度（-1 到 1 之间，越接近 1 越相似）"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    pairs = [
        ("苹果是一种水果", "香蕉也很甜"),
        ("苹果是一种水果", "iPhone 15发布了"),
        ("如何申请退货", "七天无理由退货流程"),
        ("如何申请退货", "今天天气不错"),
    ]

    print("=" * 55)
    print("📐 文本 Embedding 相似度对比")
    print("=" * 55)

    for text1, text2 in pairs:
        emb1 = get_embedding(text1)
        emb2 = get_embedding(text2)
        sim = cosine_similarity(emb1, emb2)
        print(f"\n  A: {text1}")
        print(f"  B: {text2}")
        print(f"  相似度: {sim:.4f}  {'✅ 相似' if sim > 0.5 else '❌ 不相似'}")


if __name__ == "__main__":
    main()