#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库构建：从文档到向量数据库
功能：读取 docs/ 目录下的文档，分块后存入向量数据库
运行：python 01_knowledge_base_setup.py
依赖：pip install langchain langchain-openai langchain-chroma pymupdf python-docx
"""

import os, glob
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 配置
PERSIST_DIR = "./chroma_data"
DOCS_DIR = "./docs"
CHUNK_SIZE = 500      # 每段字数
CHUNK_OVERLAP = 50    # 段之间重叠字数


def load_documents(docs_dir: str) -> list[str]:
    """读取 docs 目录下所有文档内容"""
    texts = []
    for filepath in glob.glob(f"{docs_dir}/*"):
        ext = os.path.splitext(filepath)[1].lower()
        try:
            if ext == ".txt":
                with open(filepath, "r", encoding="utf-8") as f:
                    texts.append(f.read())
            elif ext == ".pdf":
                import pymupdf
                doc = pymupdf.open(filepath)
                content = "\n".join(page.get_text() for page in doc)
                texts.append(content)
            elif ext in [".docx", ".doc"]:
                import docx
                doc = docx.Document(filepath)
                texts.append("\n".join(p.text for p in doc.paragraphs))
            print(f"✅ 读取：{os.path.basename(filepath)}（{len(texts[-1])}字符）")
        except Exception as e:
            print(f"❌ 读取失败：{filepath} → {e}")
    return texts


def split_texts(texts: list[str]) -> list[str]:
    """文本分块"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", " ", ""],
    )
    chunks = splitter.split_text("\n\n".join(texts))
    print(f"📦 分块完成：{len(chunks)} 个片段")
    return chunks


def build_vector_db(chunks: list[str]):
    """存入向量数据库"""
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    db.add_texts(chunks)
    print(f"✅ 向量数据库已更新：{len(chunks)} 条，保存至 {PERSIST_DIR}")


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 请先设置：export OPENAI_API_KEY=sk-...")
        exit(1)

    # 创建示例文档（如果没有）
    os.makedirs(DOCS_DIR, exist_ok=True)
    if not glob.glob(f"{DOCS_DIR}/*"):
        sample_text = """
        退货政策：收到商品7天内可申请退货，运费由买家承担。
        发货时间：工作日下单后24小时内发货，周末订单周一处理。
        会员等级：普通/银卡/金卡/钻石卡，累计消费满额升级。
        优惠活动：新人首单减10元，满200减20，满500减50。
        发票申请：在个人中心 → 订单详情 → 申请电子或纸质发票。
        """
        with open(f"{DOCS_DIR}/sample.txt", "w", encoding="utf-8") as f:
            f.write(sample_text)
        print("📝 已创建示例文档 docs/sample.txt")

    print("=" * 55)
    print("📚 知识库构建")
    print("=" * 55)

    texts = load_documents(DOCS_DIR)
    if not texts:
        print("❌ 没有读取到任何文档")
        exit(1)

    chunks = split_texts(texts)
    build_vector_db(chunks)
    print("\n✅ 知识库构建完成！下一步运行 02_rag_qa_system.py")


if __name__ == "__main__":
    main()