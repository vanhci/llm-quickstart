#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI 服务：RAG 问答 API
功能：把 RAG 系统包装成 REST API，支持流式输出
运行：uvicorn 03_api_deploy:app --reload --port 8000
依赖：pip install fastapi uvicorn langchain langchain-openai langchain-chroma
访问：http://localhost:8000/docs 查看 API 文档
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

app = FastAPI(title="RAG 知识库问答 API", version="1.0.0")

# CORS：允许前端调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局组件（启动时加载）
DB: Optional[Chroma] = None
LLM: Optional[ChatOpenAI] = None


@app.on_event("startup")
def load_components():
    """启动时加载向量数据库和模型"""
    global DB, LLM
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("请设置 OPENAI_API_KEY")

    DB = Chroma(persist_directory="./chroma_data", embedding_function=OpenAIEmbeddings())
    LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    print(f"✅ 启动完成，数据库含 {DB._collection.count()} 条文档")


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3
    stream: bool = True


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]


@app.post("/qa", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    """问答接口"""
    if DB is None:
        raise HTTPException(503, "服务未初始化")
    if LLM is None:
        raise HTTPException(503, "模型未初始化")
    if not req.question.strip():
        raise HTTPException(400, "问题不能为空")
    if req.top_k < 1 or req.top_k > 10:
        raise HTTPException(400, "top_k 必须在 1 到 10 之间")

    docs = DB.similarity_search(req.question, k=req.top_k)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"基于以下内容回答：\n{context}\n\n问题：{req.question}"
    response = LLM.invoke([{"role": "user", "content": prompt}])

    return AnswerResponse(
        answer=response.content,
        sources=[d.page_content for d in docs]
    )


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok", "docs_count": DB._collection.count() if DB else 0}


@app.get("/")
def root():
    return {"message": "RAG 知识库问答 API", "docs": "/docs"}


# 运行方式：uvicorn 03_api_deploy:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
