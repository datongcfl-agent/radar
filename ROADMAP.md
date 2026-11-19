# Roadmap

原则：每个版本只加一层；不承诺日期；先定验收，再写功能。

## v0.1 — MVP（当前）

- pack/seeds 校验、URL 去重、覆盖度、目录/缺口/报告；
- `scan --base` 增量 diff；
- 可选 GitHub metadata；
- 10 个单测。

## v0.2 — 可迭代

目标：从“手动重跑”变成“只处理变化”。

- 来源状态：`last_seen`、`etag`、`content_hash`、`version`、`license_hash`；
- `scan --since`：只抓变化，不重跑全量；
- 定时触发（cron / DSH schedule）；
- diff 区分：新增、内容变化、许可变化、覆盖变化、删除/归档；
- **forward snowballing**：dependents、fork 网络、文档交叉引用（不能只盯已有来源，否则是引用回音室）；
- **最小种子字段**：`id/url/evidence_level/covers/quotes/status` 六项即可录入，其余由 adapter 补全。

验收：同一批来源，改一个页面/一个 release，`scan` 只报那一处变化。

## v0.3 — 多平台

目标：不只 GitHub。

- Gitee adapter（token 或 `site:gitee.com`）；
- 网页正文（trafilatura）与浏览器（Playwright，可选）；
- 文档抽取（docling）；
- 许可扫描（grant / ScanCode）+ 人工复核。

验收：同一模块至少来自 2 个平台；许可状态可解释；不绕过登录。

## v0.4 — 证据层

目标：从“来源清单”变成“主张账本”。

- claim schema：主张、来源、独立性、可验证性、矛盾、置信度；
- `single_source` / `contradiction` / `evidence_level` 进入报告；
- 明确 `EV_RANK` 是“存在性阶梯”，不是“质量排序”；
- 人工复核队列（CSV/Markdown，Label Studio 后置）；
- 覆盖度从“来源数”升级为“证据强度”。

验收：每条关键主张有 URL + quote + 置信度；矛盾不被强行合并。

## v0.5 — 真实行业包

目标：证明换行业不是 smoke test。

- 第二个真实行业 pack（30–50 条来源，不是 3 条占位）；
- 与人工基线对比：覆盖召回、许可判对率、耗时；
- 记录“哪些查询有效、哪些平台没价值”。

验收：换 pack 不改引擎；覆盖度能指导下一轮搜索。

## v1.0 — 稳定契约

- engine/pack/ledger schema 冻结；
- 迁移脚本与版本兼容；
- 文档、测试、handoff 完整；
- 可选：DSH plugin / MCP wrapper（不是核心）。

验收：旧 pack 能在新引擎跑；坏数据有明确报错；交接不靠口头。

## 不承诺

- 不承诺具体日期；
- 不承诺“收集所有开源信息”；
- 不承诺自动写 PRD；
- 不承诺绕过登录/付费/验证码；
- 不承诺单源结论等于事实。
