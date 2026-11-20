# 通用来源底座（issue #20）

目标是让新 pack 不再从零找 30 条来源：先用跨行业底座，再补本行业垂直层。

## 五类底座

| 类别 | 域名 | 适用 | 限制 |
| --- | --- | --- | --- |
| 标准 | ndls.org.cn / openstd.samr.gov.cn | 技术规格、行业规范、验收依据 | 部分正文需登录/阅读器；只取公开页/摘要 |
| 招投标 | ccgp.gov.cn / ggzy.gov.cn | 真实项目、设备清单、预算、验收要求 | 公告页可抓，附件常为 PDF/压缩包 |
| 企业 | gsxt.gov.cn / cninfo.com.cn | 企业真实存在、财报/招股书、行业成本 | 登录/验证码页不抓；只用公开公告 |
| 统计 | stats.gov.cn | 市场规模、投资、增速 | 宏观口径，不能替代项目证据 |
| 报告 | iresearch.com.cn / 36kr.com | 行业趋势、厂商格局 | 免费摘要为主，适合 mention |

## 行业垂直层

每个 pack 只补 2 类：

- 本行业协会官网；
- 本行业门户/媒体（如弱电=千家网）。

## 抓取规则

- 只抓公开页面；登录/付费/验证码不纳入；
- 记录 `access_status` / `license_status`；
- 底座域名通常互相独立，可用于独立 host 判定；
- 底座来源多数是 `metadata` / `docs`，不自动等于 strong；
- 优先用 `--verify-quotes` 验证 quote。

## 当前落地

- `weak-current` 新增 `SRC-035`：GB 50311-2016 综合布线标准页（NDLS，metadata）；
- 第三 pack 将在底座基础上只补本行业垂直来源。
