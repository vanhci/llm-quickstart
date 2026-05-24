#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客服机器人：四种 Provider 一键切换
功能：电商客服自动回复，支持 OpenAI / DeepSeek / MiniMax / Ollama
运行：python 02_customer_bot_multi_provider.py
依赖：pip install openai
"""

import os
from openai import OpenAI

PROVIDER = os.environ.get("LLM_PROVIDER", "deepseek")

PROVIDER_CONFIGS = {
    "openai": {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    },
    "deepseek": {
        "api_key": os.environ.get("DEEPSEEK_API_KEY", ""),
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    "minimax": {
        "api_key": os.environ.get("MINIMAX_API_KEY", ""),
        "base_url": "https://api.minimaxi.com/v1",
        "model": "MiniMax-M2.7",
    },
    "ollama": {
        "api_key": "ollama",
        "base_url": "http://localhost:11434/v1",
        "model": "qwen2.5:7b",
    },
}

# 知识库
KNOWLEDGE = """
- 发货：工作日24小时内发货，默认顺丰，2-3天到
- 退货：7天无理由退货，收到后3个工作日退款
- 优惠：新人首单减10元，满200减20
- 会员：普通/银卡/金卡/钻石卡，累计消费升级
- 尺寸：商品页有尺码表，对照身高体重选择
"""

SYSTEM_PROMPT = f"""你是一个专业、友好的电商客服。请根据知识库回答用户问题。

【要求】
1. 回复不超过3句话
2. 知识库没有的内容说"帮您转人工"
3. 语气亲切，礼貌专业

【知识库】
{KNOWLEDGE}"""


def get_client():
    cfg = PROVIDER_CONFIGS[PROVIDER]
    return OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])


def customer_service(question: str) -> str:
    """调用 LLM 进行客服回复"""
    client = get_client()
    cfg = PROVIDER_CONFIGS[PROVIDER]
    response = client.chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""


def main():
    cfg = PROVIDER_CONFIGS[PROVIDER]
    print(f"🛒 客服机器人 | Provider: {PROVIDER} | Model: {cfg['model']}")
    print("=" * 50)

    questions = [
        "我想退货，几天可以申请？",
        "新人有什么优惠吗？",
        "你们用什么快递？",
    ]

    for q in questions:
        print(f"\n👤 {q}")
        print(f"🤖 {customer_service(q)}")


if __name__ == "__main__":
    main()
