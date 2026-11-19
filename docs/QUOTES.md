# Quote 验证（v0.6）

## 字段

每个 source 增加 `quote_verified`：

| 值 | 含义 | 最高覆盖 |
| --- | --- | --- |
| `true` | 抓取成功，quote 归一化后是正文子串 | strong |
| `false` | 抓到了正文，但 quote 不在里面 | mention |
| `unknown` | 没验证过（默认） | evidence |

## 怎么产生

- `--web` 抓取公开 HTML 后，会拿已有 quote 与提取正文做归一化子串匹配；
- 新加入的页面 quote 来自正文，标 `true`；
- 抓取失败或正文太短时保持 `unknown`，不硬判。

## 当前基线

seeds 里不再有人工 `quote_verified: true`；当前没有 `--web` 机器验证过的 quote，所以 **strong = 0**。  
有 quote 的来源最高 evidence；这不是数据退步，是门禁生效后的诚实结果。

## 边界

- 这是**机械子串校验**，不是语义真伪；引用被篡改/拼接仍可能通过；
- 不抓登录/付费页；
- `unknown` 不等于假，只是“没验证”，所以不能升 strong。
