#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统提示词工程与用户记忆
功能：让 Agent 保持角色设定，记住用户偏好，实现个性化对话
运行：python 04_system_prompt_memory.py
依赖：pip install openai
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class AgentWithMemory:
    """
    带记忆的 Agent：
    - 系统提示词定义角色和行为规则
    - 用户历史对话记录在 messages 里，形成上下文记忆
    - 可以保存/恢复对话状态
    """

    def __init__(self, name: str, role: str, personality: str):
        self.name = name
        self.memory = []  # 简化记忆：只存关键信息

        # 系统提示词工程：精确定义 Agent 身份
        self.system_prompt = f"""你是一个叫{name}的{role}。

【角色设定】
{personality}

【行为规则】
1. 回答风格要与角色一致
2. 如果用户提到过偏好，要记住并在后续回应中体现
3. 遇到不确定的问题，诚实说不知道，不要编造
4. 在对话中适时体现记忆（比如："您之前说喜欢..."）

【记忆规则】
对话中用户透露的个人信息要记住，但不要每次都重复。"""

    def chat(self, user_input: str) -> str:
        """发送消息并返回回复"""
        messages = [{"role": "system", "content": self.system_prompt}]

        # 把记忆注入上下文（简化版：每次都带上）
        if self.memory:
            memory_text = "\n".join(f"- {m}" for m in self.memory)
            messages.append({
                "role": "system",
                "content": f"【已知用户信息】\n{memory_text}"
            })

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
        )
        reply = response.choices[0].message.content or ""

        # 提取并保存用户偏好（简单规则）
        self._extract_memory(user_input, reply)

        return reply

    def _extract_memory(self, user_input: str, reply: str):
        """从对话中提取可能需要记忆的信息"""
        keywords = {
            "喜欢": user_input,
            "不喜欢": user_input,
            "过敏": user_input,
            "偏好": user_input,
            "上次": user_input,
            "之前": user_input,
        }
        for kw, text in keywords.items():
            if kw in text and len(text) < 100:
                # 简单存储，实际应该用 NER 或更复杂的逻辑
                if text not in self.memory:
                    self.memory.append(text)


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    # 创建一个保险顾问 Agent
    agent = AgentWithMemory(
        name="小保",
        role="保险顾问",
        personality="专业、耐心、亲切。擅长用通俗语言解释复杂的保险条款，会根据用户情况推荐合适的险种。回答简洁，不推销。"
    )

    print(f"🤖 Agent: {agent.name}（{agent.system_prompt.split('你是一个叫')[1].split('的')[1].split('。')[0]}）")
    print("=" * 50)

    # 多轮对话
    dialogue = [
        "我30岁，男，做IT的，有什么保险推荐？",
        "我平时加班多，熬夜多",
        "那我应该买什么险？",
    ]

    for user_msg in dialogue:
        print(f"\n👤 {user_msg}")
        reply = agent.chat(user_msg)
        print(f"🤖 {reply}")

    print(f"\n📝 Agent 记住了：{agent.memory}")


if __name__ == "__main__":
    main()