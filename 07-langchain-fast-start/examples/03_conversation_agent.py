#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangChain ConversationalAgent：带记忆的对话助手
功能：Agent 能记住对话历史，实现多轮上下文对话
运行：python 03_conversation_agent.py
依赖：pip install langchain langchain-openai
"""

import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory

# 模拟工具
@tool
def get_weather(city: str) -> str:
    """查询城市天气"""
    data = {"北京": "晴，26度", "上海": "小雨，22度", "广州": "多云，30度"}
    return data.get(city, f"{city}未收录")

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        return str(eval(expression))
    except:
        return "计算失败"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 对话记忆
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def create_conversation_agent():
    """创建带记忆的对话 Agent"""
    tools = [get_weather, calculate]

    # ConversationalAgent：专门处理多轮对话，保留上下文
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
    )
    return agent


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    print("=" * 55)
    print("💬 带记忆的对话助手（输入 q 退出）")
    print("=" * 55)

    agent = create_conversation_agent()

    # 预设对话流程演示多轮记忆
    dialogue = [
        "我叫张三，帮我记一下",
        "我的名字是什么？",
        "北京今天天气怎么样？",
        "再查一下上海",
        "我叫什么名字？",
    ]

    for msg in dialogue:
        print(f"\n👤 {msg}")
        response = agent.invoke({"input": msg})
        print(f"🤖 {response['output']}")

    print("\n📝 对话历史（记忆内容）：")
    for msg in memory.chat_memory.messages:
        print(f"  {msg.type}: {msg.content[:60]}...")


if __name__ == "__main__":
    main()