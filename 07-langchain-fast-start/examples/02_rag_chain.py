#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangChain RAG Chain：用 RetrievalQA 实现知识库问答
功能：从向量数据库检索相关文档，让模型基于检索结果回答
运行：python 02_rag_chain.py
依赖：pip install langchain langchain-openai langchain-chroma
"""

import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

# 初始化组件
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


def init_knowledge_base():
    """初始化知识库（存入几条文档）"""
    docs = [
        "退货政策：收到商品7天内可申请退货，运费由买家承担。",
        "发货时间：工作日下单后24小时内发货，周末订单周一处理。",
        "会员等级：普通/银卡/金卡/钻石卡，累计消费满额升级。",
        "优惠活动：新人首单减10元，满200减20，满500减50。",
        "发票申请：在个人中心 → 订单详情 → 申请电子或纸质发票。",
    ]
    # 从已有数据加载或新建
    try:
        db = Chroma(persist_directory="./chroma_data", embedding_function=embeddings)
        if db._collection.count() > 0:
            print("✅ 知识库已存在，直接加载")
            return db
    except Exception:
        pass

    db = Chroma(persist_directory="./chroma_data", embedding_function=embeddings)
    db.add_texts(docs, ids=[f"doc_{i}" for i in range(len(docs))])
    print(f"✅ 知识库初始化完成，存入 {len(docs)} 条文档")
    return db


def rag_qa(question: str, db: Chroma) -> str:
    """RAG 问答：检索 + 生成"""
    # 创建检索问答链
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff",  # 把所有检索结果塞进一个 Prompt
        return_source_documents=True,
    )

    result = qa_chain.invoke({"query": question})
    return result["result"]


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    print("=" * 55)
    print("📚 LangChain RAG 知识库问答")
    print("=" * 55)

    db = init_knowledge_base()

    questions = [
        "我想退货，几天可以申请？",
        "新人有什么优惠？",
        "会员等级有哪些？",
    ]

    for q in questions:
        print(f"\n❓ {q}")
        print(f"💡 {rag_qa(q, db)}")


if __name__ == "__main__":
    main()