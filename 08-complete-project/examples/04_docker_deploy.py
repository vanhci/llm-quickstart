#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker 部署配置
功能：生成 Dockerfile 和 docker-compose.yml，一键部署
运行：docker-compose up -d
依赖：Docker + docker-compose 已安装
"""

DOCKERFILE = '''\
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（PDF 解析需要）
RUN apt-get update && apt-get install -y --no-install-recommends \\
    libmupdf-dev mupdf-tools \\
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 初始化知识库（如需）
RUN python 01_knowledge_base_setup.py || true

EXPOSE 8000

CMD ["uvicorn", "03_api_deploy:app", "--host", "0.0.0.0", "--port", "8000"]
'''

REQUIREMENTS = '''\
langchain
langchain-openai
langchain-chroma
fastapi
uvicorn
pymupdf
python-docx
'''

DOCKER_COMPOSE = '''\
version: '3.8'

services:
  rag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./chroma_data:/app/chroma_data
      - ./docs:/app/docs
    restart: unless-stopped
'''

# 生成文件
files = {
    "Dockerfile": DOCKERFILE,
    "requirements.txt": REQUIREMENTS,
    "docker-compose.yml": DOCKER_COMPOSE,
}

for filename, content in files.items():
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 生成 {filename}")

print("\n📝 使用方法：")
print("1. 创建 .env 文件：OPENAI_API_KEY=sk-xxx")
print("2. 放入 docs/ 目录放你要的文档")
print("3. 运行：docker-compose up -d")
print("4. 访问：http://localhost:8000/docs")