#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电商客服自动回复机器人
功能：根据用户问题自动回复，支持订单查询、退换货、商品咨询
运行：python 01_basic.py
依赖：pip install openai
"""

import os
from openai import OpenAI

# 初始化客户端，API Key 从环境变量读取
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 模拟客服知识库（实际项目中可接数据库或知识库）
KNOWLEDGE = {
    "发货": "我们一般在下单后24小时内发货，默认使用顺丰快递，2-3个工作日到。",
    "退货": "支持7天无理由退货，请联系客服申请退货运单，收到货后3个工作日内退款。",
    "尺寸": "我们的商品页面都有详细尺码表，建议您对照身高体重选择，如有疑问可以咨询客服。",
    "优惠": "新用户首单减10元，满200减20，关注店铺还可领5元无门槛券。",
}


def build_prompt(user_question: str) -> str:
    """
    构建客服对话 Prompt
    技巧：明确角色 + 提供知识背景 + 要求简洁回复
    """
    knowledge_text = "\n".join(f"- {k}：{v}" for k, v in KNOWLEDGE.items())

    prompt = f"""你是一个专业、友好的电商客服。请根据以下知识库回答用户问题。

【知识库】
{knowledge_text}

【要求】
1. 回答简洁，最多3句话
2. 如果知识库没有相关内容，回复"这个我不太清楚，帮您转接人工客服~"
3. 语气亲切有礼貌

【用户问题】
{user_question}"""
    return prompt


def ask_customer_service(question: str) -> str:
    """
    调用 OpenAI API 获取客服回复
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": build_prompt(question)}
        ],
        temperature=0.7,  # 适度创意，但不失准
        max_tokens=200,
    )
    return response.choices[0].message.content


def main():
    print("=" * 50)
    print("🛒 电商客服机器人（输入 q 退出）")
    print("=" * 50)

    while True:
        user_input = input("\n👤 你：").strip()
        if user_input.lower() == "q":
            print("👋 再见！")
            break
        if not user_input:
            continue

        print("🤖 客服：", end="", flush=True)
        reply = ask_customer_service(user_input)
        print(reply)


if __name__ == "__main__":
    # 检查 API Key 是否配置
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置 OPENAI_API_KEY 环境变量：")
        print('   export OPENAI_API_KEY=sk-...')
        exit(1)

    main()