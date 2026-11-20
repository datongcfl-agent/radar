# Quote 验证（v1.1）

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

v1.1 用 `--verify-quotes --require-web-verify` 实抓：

- weak-current：**3 strong**（M01/M06/M13）、19 evidence、9 mention、6 none；
- video-kb：**0 strong**、24 evidence、2 mention、0 none。

没有匹配到正文的 quote 降为 mention。  
加 `--require-web-verify` 后，seeds 自带的 `quote_verified` 会被当作 `unknown`，只有本次验证通过才可能 strong。

## 边界

- 这是**机械子串校验**，不是语义真伪；引用被篡改/拼接仍可能通过；
- 不抓登录/付费页；
- `unknown` 不等于假，只是“没验证”，所以不能升 strong。
