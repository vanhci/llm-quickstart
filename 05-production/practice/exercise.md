## 练习题

### 题1：设计成本告警

**题目：** 你每天 LLM 预算上限是 $10，超过要告警。请补全告警逻辑：

```python
def check_budget(cost_so_far: float, daily_limit: float = 10.0):
    if cost_so_far >= daily_limit:
        print(f"🚨 超过日预算！已用 ${cost_so_far：.2f}")
        send_alert()  # 假设这个函数会发通知
    else:
        remaining = daily_limit - cost_so_far
        print(f"预算正常，剩余 ${remaining：.2f}")
```

**改进思考：** 如何实现"接近上限时提前告警"（比如用了 80% 就提醒）？

**参考答案：**
```python
def check_budget(cost_so_far: float, daily_limit: float = 10.0):
    usage_ratio = cost_so_far / daily_limit
    if usage_ratio >= 1.0:
        print(f"🚨 超过日预算！已用 ${cost_so_far:.2f}")
        send_alert("budget_exceeded")
    elif usage_ratio >= 0.8:
        print(f"⚠️ 预算使用超过 80%，剩余 ${daily_limit - cost_so_far:.2f}")
        send_alert("budget_warning")
    else:
        print(f"✅ 预算正常，剩余 ${daily_limit - cost_so_far:.2f}")
```

---

### 题2：输出质量评估实践

**题目：** 针对"客服自动回复"场景，设计一套评估标准，包括：

1. 回复长度限制（太长浪费，太短不专业）
2. 必须包含的关键词（体现专业性）
3. 不能包含的词（避免敷衍）

**参考答案：**

```python
criteria = {
    "min_length": 30,      # 至少30字才算认真回复
    "max_length": 150,     # 不超过150字
    "keywords": ["您好", "请问", "帮助"],  # 基础礼貌用语
    "banned_words": ["不知道", "不清楚", "你自己"],  # 禁止敷衍用语
}

# 评估时检查
score = 1.0
if len(response) < criteria["min_length"]:
    score -= 0.3
if any(word in response for word in criteria["banned_words"]):
    score -= 0.5  # 出现敷衍用语，大幅扣分
```