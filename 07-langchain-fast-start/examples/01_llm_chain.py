#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangChain LLMChain 三种用法演示
功能：展示 ChatOpenAI / PromptTemplate / LLMChain 的基础用法
运行：python 01_llm_chain.py
依赖：pip install langchain langchain-openai
"""

import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 初始化模型（自动读取 OPENAI_API_KEY）
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# ---------- 用法1：基础 LLMChain ----------
def demo_basic():
    """最基础的用法：Prompt + Model"""
    prompt = PromptTemplate.from_template("用一句话解释：{topic}")
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"topic": "什么是 RAG"})
    print("=== 基础用法 ===")
    print(f"结果：{result['text']}\n")


# ---------- 用法2：对话 Prompt ----------
def demo_chat():
    """Chat 风格的 Prompt（System + Human 消息）"""
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "你是一个{role}，回答风格：{style}"
        ),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({
        "role": "旅行顾问",
        "style": "热情、专业、简短",
        "question": "去日本旅游有什么推荐？"
    })
    print("=== 对话 Prompt ===")
    print(f"结果：{result['text']}\n")


# ---------- 用法3：带输出解析 ----------
def demo_with_output_parser():
    """结合 OutputParser 指定输出格式"""
    from langchain.output_parsers import CommaSeparatedListOutputParser
    from langchain.chains import LLMChain

    parser = CommaSeparatedListOutputParser()
    prompt = PromptTemplate.from_template(
        "列出 {topic} 的 {n} 个优点，以逗号分隔",
        output_parser=parser,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"topic": "学习 Python", "n": 5})
    print("=== 带输出解析 ===")
    print(f"结果：{result['text']}")
    print(f"解析后：{parser.parse(result['text'])}\n")


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    print("=" * 55)
    print("🔗 LangChain LLMChain 示例")
    print("=" * 55)

    demo_basic()
    demo_chat()
    demo_with_output_parser()


if __name__ == "__main__":
    main()