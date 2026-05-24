#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chain of Thought 数学解题助手
功能：用 CoT 引导模型一步步解题，提升复杂推理准确率
运行：python 02_advanced.py
依赖：pip install openai
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def solve_math_cot(problem: str) -> str:
    """
    用 Chain of Thought 让模型分步解题

    核心技巧：在 Prompt 里明确要求"分步骤思考"
    CoT 能让复杂问题的准确率提升 30-50%
    """

    cot_prompt = f"""请分步骤解答以下数学问题，每一步都要写出推导过程。

【问题】
{problem}

【要求】
1. 分步骤解答，每步格式：第N步：...
2. 最后给出答案
3. 如果是应用题，要写出计算公式再代入数字"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": cot_prompt}],
        temperature=0.3,  # 推理任务降低创意，保持严谨
        max_tokens=500,
    )
    return response.choices[0].message.content


def solve_math_direct(problem: str) -> str:
    """不用 CoT，直接要答案（对比用）"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"解答：{problem}"}],
        temperature=0.3,
        max_tokens=200,
    )
    return response.choices[0].message.content


def main():
    print("=" * 60)
    print("🧮 Chain of Thought 数学解题助手")
    print("=" * 60)

    problems = [
        "小明有 23 元，小红比小明多 15 元，两人一共有多少元？",
        "一件商品原价比现价多 120 元，现价是原价的 60%，原价是多少元？",
        "一个长方形长 8cm，宽比长短 3cm，面积是多少平方厘米？",
    ]

    for i, problem in enumerate(problems, 1):
        print(f"\n{'='*60}")
        print(f"📌 第{i}题：{problem}")

        print("\n🔵 直接回答：")
        direct = solve_math_direct(problem)
        print(direct)

        print("\n🟢 Chain of Thought（分步解答）：")
        cot = solve_math_cot(problem)
        print(cot)


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置 OPENAI_API_KEY 环境变量：")
        print('   export OPENAI_API_KEY=sk-...')
        exit(1)

    main()