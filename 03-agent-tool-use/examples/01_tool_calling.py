#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础工具调用：模拟天气查询
功能：让模型判断何时需要调用工具，并获取工具执行结果
运行：python 01_tool_calling.py
依赖：pip install openai
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 模拟工具：天气查询
def get_weather(city: str) -> str:
    """模拟天气查询工具"""
    weather_data = {
        "北京": "晴，26°C，东南风2级，空气良",
        "上海": "小雨，22°C，东风3级，有雾",
        "广州": "多云，30°C，南风2级，紫外线强",
        "深圳": "晴，29°C，东南风1级，适宜出行",
        "西安": "阴，24°C，东风2级，PM2.5 轻度",
    }
    return weather_data.get(city, f"{city}的天气数据暂不可用")


# 工具定义（给模型看）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


def ask_with_tool(user_question: str) -> str:
    """带工具调用的对话"""
    messages = [
        {
            "role": "system",
            "content": "你是一个助手，可以根据用户问题调用合适的工具。工具返回结果后，基于结果回答用户。"
        },
        {"role": "user", "content": user_question}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message

    # 模型需要调用工具
    if assistant_message.tool_calls:
        tool_call = assistant_message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = eval(tool_call.function.arguments)  # 将 JSON 转成 dict

        print(f"🤖 模型决定调用工具：{function_name}({arguments})")

        # 执行工具
        if function_name == "get_weather":
            result = get_weather(**arguments)

        # 把工具结果反馈给模型
        messages.append(assistant_message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        # 再次调用模型，让它基于工具结果回答
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return final_response.choices[0].message.content

    return assistant_message.content


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    questions = [
        "北京今天天气怎么样？",
        "帮我查一下上海的天气",
        "你好！",
    ]

    for q in questions:
        print(f"\n❓ {q}")
        answer = ask_with_tool(q)
        print(f"💡 {answer}")


if __name__ == "__main__":
    main()