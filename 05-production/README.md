# Day 5 · 生产级实践 —— 监控、成本控制、评估

## 监控与日志

生产环境必须能看到：
- 每分钟请求数、错误率
- 平均响应时间（P99）
- Token 消耗速度

```python
import time, logging

logger = logging.getLogger(__name__)

def call_llm(prompt: str):
    start = time.time()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        elapsed = time.time() - start
        logger.info(f"耗时: {elapsed:.2f}s | tokens: {response.usage.total_tokens}")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM 调用失败: {e}")
        raise
```

---

## 成本控制策略

### 1. 用小模型处理简单任务
- 客服FAQ、分类、摘要 → 用 GPT-4o-mini 或 Haiku
- 复杂推理 → 才用 GPT-4o

### 2. 控制输出长度
```python
# 在 Prompt 里加限制
prompt = """回答不超过3句话，每句不超过20字。"""
```

### 3. 缓存常用回答
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_answer(question: str):
    # 相同的常见问题直接返回缓存
    return call_llm(question)
```

### 4. Token 计费参考
| 模型 | 输入成本 | 输出成本 |
|------|---------|---------|
| GPT-4o | $5/1M | $15/1M |
| GPT-4o-mini | $0.15/1M | $0.60/1M |

---

## 输出质量评估

### 简单评估方法
1. **关键词命中率**：回答中是否包含预期关键词
2. **长度检查**：不超过/不低于阈值
3. **结构化输出验证**：如果是 JSON，检查格式是否正确

### 自动评估示例
```python
def evaluate_response(response: str, criteria: dict) -> float:
    """简单评分：0-1分"""
    score = 0.0
    if criteria.get("max_length") and len(response) <= criteria["max_length"]:
        score += 0.3
    if criteria.get("keywords"):
        keywords_found = sum(1 for k in criteria["keywords"] if k in response)
        score += 0.4 * (keywords_found / len(criteria["keywords"]))
    # 更多维度...
    return min(score, 1.0)
```

---

## 常见陷阱与解决方案

| 陷阱 | 解决方案 |
|------|---------|
| 模型编造答案（幻觉） | 接入 RAG，提供参考资料 |
| 回复太慢 | 用流式输出 (stream=True)，或换小模型 |
| 成本暴涨 | 加 Prompt 限制 + 缓存 + 模型分级 |
| 输出格式不稳定 | 用 Few-shot + 输出格式强制约束 |
| 用户输入恶意 Prompt | 输入过滤 + Prompt 注入检测 |

---

## 📂 示例代码

| 文件 | 内容 |
|------|------|
| `examples/01_cost_control.py` | Token 计费统计与成本控制 |
| `examples/02_evaluation.py` | 简单输出质量评估 |

```bash
python examples/01_cost_control.py
```

---

## 📝 练习题

[`practice/exercise.md`](./practice/exercise.md) — 2道练习题，带参考答案