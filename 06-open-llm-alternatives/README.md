# Day 6 · 替代方案 —— 国内可用的免费/低价 LLM

## 为什么需要替代方案？

OpenAI API 在国内：
- ❌ 需要信用卡和外币支付
- ❌ 封号频繁
- ❌ 网络不稳定，延迟高

所以这套教程提供了**4种平替方案**，用统一的封装代码，**切换 provider 只需改 1 行**。

---

## 四种替代方案对比

| 方案 | 费用 | 国内可用 | 速度 | 适合场景 |
|------|------|---------|------|---------|
| **Ollama（本地）** | 完全免费 | ✅ | 慢（本地） | 学习、测试 |
| **DeepSeek** | 极低（¥1/百万token） | ✅ | 快 | 生产环境 |
| **MiniMax Token Plan** | 订阅额度 / 按量 | ✅ | 快 | 原型、生产 |

---

## 1. Ollama：本地模型（完全免费）

**特点：** 模型跑在你自己的电脑上，不需要 API Key，不需要网络。

```bash
# 安装（macOS/Linux）
brew install ollama

# 下载模型（约 4GB）
ollama pull qwen2.5:7b

# 运行
ollama run qwen2.5:7b
```

**适用模型：**
- `qwen2.5:7b` — 国产阿里模型，中文友好，7B 足够入门
- `llama3.2:3b` — 轻量，适合低配电脑
- `deepseek-r1:7b` — 推理能力强

**优缺点：**
- ✅ 完全免费，无限使用
- ✅ 隐私（数据不离开电脑）
- ❌ 速度慢（取决于电脑配置）
- ❌ 效果不如 GPT-4

---

## 2. DeepSeek：国产低价 API

**特点：** 国产，便宜得像白嫖，效果对标 GPT-4。

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxxxxxx",  # 从 DeepSeek 平台获取
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
```

**价格：**
- 输入：¥1 / 百万 tokens
- 输出：¥2 / 百万 tokens
- 注册送 ¥5，可以玩很久

**注册地址：** https://platform.deepseek.com

---

## 3. MiniMax：Token Plan / OpenAI 兼容

**特点：** 兼容 OpenAI SDK，可用 Token Plan Key 或普通 API Key 接入。

```python
from openai import OpenAI

client = OpenAI(
    api_key="mm-xxxxx",  # 从 MiniMax 平台获取
    base_url="https://api.minimaxi.com/v1"
)

response = client.chat.completions.create(
    model="MiniMax-M2.7",
    messages=[{"role": "user", "content": "你好"}]
)
```

**模型：**
- `MiniMax-M2.7`
- `MiniMax-M2.7-highspeed`

**说明：** Token Plan 适合学习和持续使用，OpenAI 兼容接口可直接接入现有代码。

---

## 统一封装：切换只需改 1 行

```python
# providers.py — 统一封装，切换 provider 只需改 PROVIDER

import os
from openai import OpenAI

PROVIDER = os.environ.get("LLM_PROVIDER", "deepseek")  # 改这里就行

PROVIDER_CONFIGS = {
    "openai": {
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    },
    "deepseek": {
        "api_key": os.environ.get("DEEPSEEK_API_KEY"),
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    "minimax": {
        "api_key": os.environ.get("MINIMAX_API_KEY"),
        "base_url": "https://api.minimaxi.com/v1",
        "model": "MiniMax-M2.7",
    },
    "ollama": {
        "api_key": "ollama",  # 固定值，Ollama 不需要真 key
        "base_url": "http://localhost:11434/v1",
        "model": "qwen2.5:7b",
    },
}

def get_client():
    cfg = PROVIDER_CONFIGS[PROVIDER]
    return OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])

def chat(prompt: str) -> str:
    client = get_client()
    cfg = PROVIDER_CONFIGS[PROVIDER]
    response = client.chat.completions.create(
        model=cfg["model"],
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

**使用方式：**
```bash
# 用 DeepSeek
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-xxx
python app.py

# 换成 MiniMax
export LLM_PROVIDER=minimax
export MINIMAX_API_KEY=mm_xxx
python app.py
```

---

## 📂 示例代码

| 文件 | 内容 |
|------|------|
| `examples/01_unified_provider.py` | 四种 provider 统一调用演示 |
| `examples/02_customer_bot_multi_provider.py` | 客服机器人，4种 provider 一键切换 |

---

## 📝 练习题

[`practice/exercise.md`](./practice/exercise.md) — 2道练习题
