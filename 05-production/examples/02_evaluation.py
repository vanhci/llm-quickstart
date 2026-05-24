#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单输出质量评估
功能：对 LLM 输出进行基础质量检查：关键词覆盖、长度、结构验证
运行：python 02_evaluation.py
依赖：pip install openai
"""

import os, json, re
from openai import OpenAI
from dataclasses import dataclass

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@dataclass
class EvalResult:
    score: float        # 0.0 ~ 1.0
    reasons: list[str]  # 不合格的原因


def eval_response(response: str, criteria: dict) -> EvalResult:
    """
    评估 LLM 输出质量

    criteria 支持：
    - max_length: 最大字数
    - min_length: 最小字数
    - keywords: 必须包含的关键词列表
    - format: "json" | "plain" 期望的格式
    """
    reasons = []
    score = 1.0

    # 长度检查
    if criteria.get("max_length") and len(response) > criteria["max_length"]:
        reasons.append(f"超出最大长度 ({len(response)} > {criteria['max_length']})")
        score -= 0.2
    if criteria.get("min_length") and len(response) < criteria["min_length"]:
        reasons.append(f"内容过短 ({len(response)} < {criteria['min_length']})")
        score -= 0.2

    # 关键词检查
    if criteria.get("keywords"):
        found = sum(1 for kw in criteria["keywords"] if kw in response)
        ratio = found / len(criteria["keywords"])
        if ratio < 1.0:
            reasons.append(f"缺少关键词：{[kw for kw in criteria['keywords'] if kw not in response]}")
        score -= 0.3 * (1 - ratio)

    # 格式检查
    if criteria.get("format") == "json":
        try:
            json.loads(response)
        except Exception:
            reasons.append("期望 JSON 格式，但解析失败")
            score -= 0.3

    return EvalResult(max(0.0, score), reasons)


def ask_and_eval(question: str, criteria: dict):
    """问问题，评估回答质量"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
    )
    answer = response.choices[0].message.content or ""

    result = eval_response(answer, criteria)

    print(f"\n❓ 问题：{question}")
    print(f"💡 回答：{answer}")
    print(f"📊 评分：{result.score:.2f}  {'✅ 通过' if result.score >= 0.8 else '❌ 不合格'}")
    if result.reasons:
        for r in result.reasons:
            print(f"   → {r}")


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    print("=" * 55)
    print("📊 LLM 输出质量评估示例")
    print("=" * 55)

    # 测试1：关键词覆盖
    ask_and_eval(
        "解释什么是 RAG？",
        {"min_length": 50, "keywords": ["检索", "生成"]}
    )

    # 测试2：JSON 格式
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "以 JSON 格式返回你的名字和职业"}],
    )
    answer = response.choices[0].message.content or ""
    result = eval_response(answer, {"format": "json"})
    print(f"\n💡 JSON 格式测试：{answer}")
    print(f"📊 评分：{result.score:.2f}  {'✅ 通过' if result.score >= 0.8 else '❌ 不合格'}")
    if result.reasons:
        for r in result.reasons:
            print(f"   → {r}")


if __name__ == "__main__":
    main()