## 练习题

### 题1：切换到 Ollama（本地免费）

**题目：** 把上面的客服机器人从 DeepSeek 切换到 Ollama，需要几步？写出环境变量配置。

**参考答案：**
```bash
# 1. 安装 Ollama
brew install ollama

# 2. 下载模型
ollama pull qwen2.5:7b

# 3. 启动服务（后台运行）
ollama serve

# 4. 设置环境变量（只改这2个）
export LLM_PROVIDER=ollama
# 不需要 API_KEY，Ollama 是本地的

# 5. 运行
python 02_customer_bot_multi_provider.py
```

---

### 题2：给统一封装添加 MiniMax

**题目：** 在 `PROVIDER_CONFIGS` 中添加 MiniMax Token Plan，需要什么配置？

**参考答案：**
```python
"minimax": {
    "api_key": os.environ.get("MINIMAX_API_KEY", ""),
    "base_url": "https://api.minimaxi.com/v1",
    "model": "MiniMax-M2.7",  # 或 MiniMax-M2.7-highspeed
},
```

注册地址：https://platform.minimaxi.com
