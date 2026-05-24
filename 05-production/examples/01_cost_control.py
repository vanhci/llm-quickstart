#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 计费与成本控制
功能：统计 LLM 调用消耗，按模型单价计算成本，展示节省技巧
运行：python 01_cost_control.py
依赖：pip install openai
"""

import os
from openai import OpenAI
from dataclasses import dataclass
from typing import Optional

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 2024 年官方定价（每 1M tokens 的美元价格）
MODEL_PRICES = {
    "gpt-4o":       {"input": 5.00,  "output": 15.00},
    "gpt-4o-mini":  {"input": 0.15,  "output": 0.60},
    "gpt-4-turbo":  {"input": 10.00, "output": 30.00},
}

@dataclass
class UsageRecord:
    """记录一次 LLM 调用的用量"""
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


def calc_cost(model: str, input_tok: int, output_tok: int) -> float:
    """根据 token 数和模型单价计算费用（美元）"""
    prices = MODEL_PRICES.get(model, {"input": 0, "output": 0})
    return (input_tok / 1_000_000) * prices["input"] + \
           (output_tok / 1_000_000) * prices["output"]


class CostTracker:
    """成本追踪器：累计调用次数、token 消耗、总成本"""

    def __init__(self):
        self.records: list[UsageRecord] = []
        self.total_cost = 0.0

    def add(self, model: str, input_tok: int, output_tok: int):
        cost = calc_cost(model, input_tok, output_tok)
        self.records.append(UsageRecord(model, input_tok, output_tok, cost))
        self.total_cost += cost

    def report(self):
        print(f"\n{'='*50}")
        print(f"💰 成本报告")
        print(f"{'='*50}")
        print(f"调用次数：{len(self.records)}")
        total_in = sum(r.input_tokens for r in self.records)
        total_out = sum(r.output_tokens for r in self.records)
        print(f"输入 Token：{total_in:,}  ({total_in/1_000_000:.4f}M)")
        print(f"输出 Token：{total_out:,}  ({total_out/1_000_000:.4f}M)")
        print(f"总成本：${self.total_cost:.4f}")
        print(f"\n按模型分布：")
        for model in set(r.model for r in self.records):
            model_records = [r for r in self.records if r.model == model]
            model_cost = sum(r.cost_usd for r in model_records)
            print(f"  {model}: ${model_cost:.4f}  ({len(model_records)}次调用)")


def llm_call(model: str, prompt: str, tracker: Optional[CostTracker] = None) -> str:
    """封装 LLM 调用，自动统计 token 和成本"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    msg = response.choices[0].message
    usage = response.usage

    if tracker:
        tracker.add(model, usage.prompt_tokens, usage.completion_tokens)

    return msg.content or ""


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    tracker = CostTracker()

    prompts = [
        "用一句话解释量子计算",
        "写一首关于春天的诗",
        "Python 和 JavaScript 有什么区别？",
    ]

    # 使用 gpt-4o-mini（便宜 30 倍）处理简单任务
    for p in prompts:
        print(f"❓ {p}")
        ans = llm_call("gpt-4o-mini", p, tracker)
        print(f"💡 {ans[:60]}...")

    tracker.report()

    print("\n" + "=" * 50)
    print("💡 成本优化建议")
    print("=" * 50)
    print("1. 简单任务用 gpt-4o-mini（便宜 30 倍）")
    print("2. Prompt 里限制输出长度，避免浪费 token")
    print("3. 缓存高频相同问题的回答（用 hash 做 key）")


if __name__ == "__main__":
    main()