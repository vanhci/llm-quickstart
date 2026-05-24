#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多步骤任务规划 Agent
功能：模型自动分解复杂任务，按步骤执行，适合自动化工作流
运行：python 03_workflow_agent.py
依赖：pip install openai
"""

import os
import json
import ast
import operator
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 模拟工具
def search(query: str) -> str:
    data = {
        "英伟达营收2024": "1300亿美元，同比增长122%",
        "特斯拉股价": "约480美元",
        "苹果市值": "约3.8万亿美元",
    }
    return data.get(query, f"找到关于'{query}'的信息")

def calculate(expr: str) -> str:
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
        return str(eval_node(ast.parse(expr, mode="eval")))
    except Exception:
        return "计算失败"

def send_email(to: str, content: str) -> str:
    return f"✅ 邮件已发送给 {to}，内容：{content[:20]}..."

def web_scraper(url: str) -> str:
    return f"已抓取 {url}，获取到页面内容摘要"

TOOLS = {
    "search": search,
    "calculate": calculate,
    "send_email": send_email,
    "web_scraper": web_scraper,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜索信息",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "搜索关键词"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行简单数学计算",
            "parameters": {
                "type": "object",
                "properties": {"expr": {"type": "string", "description": "数学表达式"}},
                "required": ["expr"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送邮件。真实生产环境中，这类工具必须先请求用户确认。",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "收件人邮箱"},
                    "content": {"type": "string", "description": "邮件内容"},
                },
                "required": ["to", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_scraper",
            "description": "抓取网页摘要",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string", "description": "网页 URL"}},
                "required": ["url"],
            },
        },
    },
]


def workflow_agent(task: str) -> str:
    """
    多步骤工作流 Agent
    模型自主规划步骤，逐条执行，直到完成
    """
    messages = [
        {
            "role": "system",
            "content": """你是一个任务规划助手。当用户给出一个目标时，你需要：
1. 分析任务需要哪几步
2. 每一步使用工具完成子任务
3. 把上一步的结果作为下一步的输入

可用工具：
- search(query): 搜索信息
- calculate(expr): 计算数学表达式
- send_email(to, content): 发送邮件
- web_scraper(url): 抓取网页

每次只说一个步骤，然后调用工具。等工具返回结果后，再规划下一步。
当所有步骤完成后，明确输出"✅ 任务完成"。"""
        },
        {"role": "user", "content": task}
    ]

    print(f"\n🎯 目标：{task}")
    print("-" * 50)

    max_steps = 8
    for step in range(max_steps):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )
        msg = resp.choices[0].message
        messages.append(msg)

        content = msg.content or ""

        # 任务完成
        if "✅ 任务完成" in content or "任务完成" in content:
            print(f"\n{content}")
            return content

        # 检查是否需要调用工具
        if msg.tool_calls:
            for call in msg.tool_calls:
                fn = call.function.name
                args = json.loads(call.function.arguments or "{}")
                print(f"  🎬 步骤{step+1}: {fn}({args})")

                if fn in TOOLS:
                    result = TOOLS[fn](**args)
                else:
                    result = f"未知工具: {fn}"

                print(f"     结果: {result}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                })
        else:
            # 无工具调用，直接回答
            print(f"\n💡 {content}")
            return content

    return "达到最大步骤数"


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    tasks = [
        "帮我查一下英伟达的营收，然后算一下比去年增长了多少亿美元，最后发邮件给我",
    ]

    for t in tasks:
        workflow_agent(t)


if __name__ == "__main__":
    main()
