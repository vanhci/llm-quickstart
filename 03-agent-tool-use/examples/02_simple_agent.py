#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单 Agent 实现：多步推理执行
功能：模型自己规划步骤，逐步执行，最终给出答案
运行：python 02_simple_agent.py
依赖：pip install openai
"""

import os
import json
import ast
import operator
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# 模拟工具
def search_web(query: str) -> str:
    """模拟网页搜索"""
    results = {
        "特斯拉股价": "截至2024年Q4，特斯拉(TSLA)股价约$480",
        "苹果市值": "苹果(AAPL)市值约$3.8万亿美元",
        "英伟达营收": "英伟达FY2025营收$1300亿美元，同比增长122%",
    }
    return results.get(query, f"没有找到关于'{query}'的相关信息")

def calculate(expression: str) -> str:
    """模拟计算器"""
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](eval_node(node.operand))
        raise ValueError("只支持数字和四则运算")

    try:
        result = eval_node(ast.parse(expression, mode="eval"))
        return str(result)
    except Exception:
        return "计算表达式无效"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索网络信息，输入搜索关键词",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行简单数学计算，只允许数字和四则运算符",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，如：(123 + 456) * 2"}
                },
                "required": ["expression"],
            },
        },
    },
]


def simple_agent(question: str) -> str:
    """
    简单 Agent：模型自己决定要调用哪个工具
    循环：思考 → 决定工具 → 执行 → 获取结果 → 继续或结束
    """
    messages = [
        {
            "role": "system",
            "content": f"""你是一个助手，可以调用工具来回答问题。
可用工具：
- search_web(query): 搜索网络信息
- calculate(expression): 计算数学表达式

当用户问题需要查资料或计算时，调用对应工具。"""
        },
        {"role": "user", "content": question}
    ]

    max_steps = 5  # 防止无限循环

    for step in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_msg = response.choices[0].message
        messages.append(assistant_msg)

        # 没有工具调用，说明已经可以直接回答
        if not assistant_msg.tool_calls:
            return assistant_msg.content

        # 执行工具调用
        for call in assistant_msg.tool_calls:
            fn_name = call.function.name
            args = json.loads(call.function.arguments or "{}")

            if fn_name == "search_web":
                result = search_web(**args)
            elif fn_name == "calculate":
                result = calculate(**args)
            else:
                result = f"未知工具：{fn_name}"

            print(f"  🎬 步骤{step+1}: 调用 {fn_name}({args}) → {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    return "问题太复杂，已达到最大步数限制"


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    tasks = [
        "英伟达的营收是多少？",
        "帮我算一下 (123 + 456) * 2",
        "特斯拉和苹果哪个市值更大？",
    ]

    for task in tasks:
        print(f"\n{'='*50}")
        print(f"❓ {task}")
        print(f"{'='*50}")
        result = simple_agent(task)
        print(f"💡 {result}")


if __name__ == "__main__":
    main()
