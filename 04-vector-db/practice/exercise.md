## 练习题

### 题1：手写余弦相似度

**题目：** 补全下面的余弦相似度函数（不能调用 math 库以外的函数）：

```python
import math

def cosine_sim(a: list[float], b: list[float]) -> float:
    # a 和 b 是等长的一维向量
    # 返回值范围：-1 到 1
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return ...  # 补全这里
```

**参考答案：**
```python
return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0
```

---

### 题2：Embedding 实际应用场景

**题目：** 以下场景哪个适合用 Embedding 向量检索？哪个不适合？

1. 在 100 万篇新闻中找"与某篇内容最相似的文章"
2. 查用户表里"张三"的所有订单（精确匹配）
3. 找"和这段产品描述最接近的现有产品"
4. 验证用户输入的验证码是否正确

**参考答案：**

| 场景 | 是否适合 | 原因 |
|------|---------|------|
| 新闻相似文章推荐 | ✅ 适合 | 语义相似，模糊匹配 |
| 精确查用户订单 | ❌ 不适合 | 需要精确匹配，用 SQL 即可 |
| 相似产品推荐 | ✅ 适合 | 描述相近即可，不需要关键词一样 |
| 验证码校验 | ❌ 不适合 | 精确匹配，错了就错了 |