## 练习题

### 题1：加入自己的知识库

**题目：** 把你自己的文档（PDF / TXT / Markdown）放入 `docs/` 目录，重新构建知识库并测试。

**步骤：**
```bash
# 1. 放入文档
cp 你的文档.pdf 08-complete-project/docs/

# 2. 重新构建
python 08-complete-project/examples/01_knowledge_base_setup.py

# 3. 测试问答
python 08-complete-project/examples/02_rag_qa_system.py
```

**思考：**
- 分块大小（CHUNK_SIZE）调大调小对效果有什么影响？
- 什么情况下需要调整 overlap？

---

### 题2：换用 DeepSeek 模型

**题目：** 把 `02_rag_qa_system.py` 中的模型从 GPT-4o-mini 换成 DeepSeek，保持其他代码不变。

**提示：** 查看第一章的 Provider 封装，修改 `generate_answer` 函数中的 LLM 初始化。

**参考答案：**
```python
from openai import OpenAI

# 替换 LLM 初始化部分
llm = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
# 调用方式改为：
response = llm.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}]
)
```

---

### 题3：部署到云服务器

**题目：** 把服务部署到云服务器（阿里云 / 腾讯云 / Vultr），实现公网可访问。

**关键步骤：**
1. 服务器安装 Docker：`curl -fsSL https://get.docker.com | sh`
2. 上传项目代码（`scp -r 08-complete-project/ root@你的IP:/app/`）
3. 配置 `.env` 文件
4. `docker-compose up -d`
5. 安全组开放 8000 端口

**验证：** 访问 `http://你的服务器IP:8000/docs`

**加分项：**
- 配置 Nginx 反向代理（域名访问 + HTTPS）
- 配置 UFW 防火墙，只开放 80/443 端口