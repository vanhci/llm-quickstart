# 运行说明

## 1. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. 配置 API Key

Linux / macOS:

```bash
export OPENAI_API_KEY=sk-xxx
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="sk-xxx"
```

也可以参考 `.env.example` 配置不同模型 Provider。

## 3. 推荐运行顺序

```bash
python 01-prompt-engineering/examples/01_basic.py
python 02-rag-basics/examples/01_simple_rag.py
python 03-agent-tool-use/examples/01_tool_calling.py
python 04-vector-db/examples/01_embedding.py
python 05-production/examples/01_cost_control.py
```

完整项目：

```bash
cd 08-complete-project
python examples/01_knowledge_base_setup.py
python examples/02_rag_qa_system.py
uvicorn examples.03_api_deploy:app --reload --port 8000
```

如果因为模块名以数字开头导致 `uvicorn examples.03_api_deploy:app` 无法导入，可以进入 `examples` 目录后运行：

```bash
cd 08-complete-project/examples
uvicorn 03_api_deploy:app --reload --port 8000
```

## 4. 常见问题

### 没有设置 API Key

报错：

```text
请先设置 OPENAI_API_KEY
```

解决：按第 2 步设置环境变量。

### ChromaDB 数据库不存在

报错：

```text
向量数据库不存在，请先运行 01_knowledge_base_setup.py
```

解决：

```bash
cd 08-complete-project
python examples/01_knowledge_base_setup.py
```

### 模型或价格信息不一致

模型名、价格、免费额度可能变化。真实项目请以各平台官方文档为准。

MiniMax 官方 OpenAI 兼容接口可用 `https://api.minimaxi.com/v1`，模型示例为 `MiniMax-M2.7`。
