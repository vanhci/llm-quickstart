#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整 RAG 问答系统
功能：加载向量数据库，实现问答交互（支持流式输出）
运行：python 02_rag_qa_system.py
依赖：pip install langchain langchain-openai langchain-chroma
"""

import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.schema import HumanMessage

# 配置
PERSIST_DIR = "./chroma_data"


def load_vector_db():
    """加载向量数据库"""
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)


def retrieve(question: str, db: Chroma, top_k: int = 3) -> list[str]:
    """检索最相关的文档片段"""
    docs = db.similarity_search(question, k=top_k)
    return [doc.page_content for doc in docs]


def generate_answer(question: str, context: list[str], stream: bool = True):
    """基于检索结果生成回答，支持流式"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    context_text = "\n\n".join(f"- {c}" for c in context)

    prompt = f"""基于以下知识库内容回答用户问题。如果知识库没有相关信息，说"我没有找到相关内容"。

【知识库】
{context_text}

【问题】
{question}

回答要求：简洁，不超过3句话，引用相关段落。"""

    if not stream:
        # 非流式（一次性返回）
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    # 流式输出
    print("💡 ", end="", flush=True)
    full_response = ""
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        text = chunk.content if hasattr(chunk, 'content') else ""
        if text:
            print(text, end="", flush=True)
            full_response += text
    print("\n")
    return full_response


def chat_loop(db: Chroma):
    """问答交互循环"""
    print("=" * 55)
    print("💬 RAG 知识库问答（输入 q 退出）")
    print("=" * 55)

    while True:
        question = input("\n❓ 你的问题：").strip()
        if question.lower() == "q":
            break
        if not question:
            continue

        print("🔍 检索相关文档...")
        docs = retrieve(question, db)
        print(f"   找到 {len(docs)} 条相关内容")

        print("🤖 生成回答...")
        generate_answer(question, docs)


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    if not os.path.exists(PERSIST_DIR):
        print(f"❌ 向量数据库不存在，请先运行 01_knowledge_base_setup.py")
        exit(1)

    db = load_vector_db()
    count = db._collection.count()
    print(f"✅ 向量数据库加载完成，共 {count} 条文档")

    chat_loop(db)


if __name__ == "__main__":
    main()