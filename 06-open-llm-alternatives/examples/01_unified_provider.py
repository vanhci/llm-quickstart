#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一 Provider 封装：四种 LLM 一键切换
功能：DeepSeek / Groq / 硅基流动 / Ollama 只需改 1 行配置
运行：python 01_unified_provider.py
依赖：pip install openai
环境变量：LLM_PROVIDER（openai/deepseek/groq/ollama）+ 对应 API Key
"""

import os
from openai import OpenAI

# ============ 只需改这里 ============
# 可选值：openai / deepseek / groq / ollama
PROVIDER = os.environ.get("LLM_PROVIDER", "deepseek")
# ====================================


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
    "groq": {
        "api_key": os.environ.get("GROQ_API_KEY", ""),
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.2-3b-preview",
    },
    "ollama": {
        "api_key": "ollama",  # Ollama 不需要真实 key
        "base_url": "http://localhost:11434/v1",
        "model": "qwen2.5:7b",  # 或 llama3.2:latest
    },
}


def get_client():
    """根据当前 PROVIDER 创建客户端"""
    cfg = PROVIDER_CONFIGS[PROVIDER]
    return OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])


def chat(prompt: str, model: str = None) -> str:
    """统一 chat 接口，兼容所有 provider"""
    client = get_client()
    cfg = PROVIDER_CONFIGS[PROVIDER]
    chosen_model = model or cfg["model"]

    response = client.chat.completions.create(
        model=chosen_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    if not os.environ.get("LLM_PROVIDER"):
        print("⚠️ 未设置 LLM_PROVIDER，默认为 deepseek")

    cfg = PROVIDER_CONFIGS[PROVIDER]
    print(f"当前 Provider：{PROVIDER}")
    print(f"使用模型：{cfg['model']}")
    print(f"API 地址：{cfg['base_url']}")
    print("-" * 50)

    # 简单测试
    question = "用一句话解释什么是 RAG"
    print(f"❓ {question}")
    print(f"💡 {chat(question)}")


if __name__ == "__main__":
    main()