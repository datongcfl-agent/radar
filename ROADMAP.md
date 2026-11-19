# Roadmap

原则：每个版本只加一层；不承诺日期；先定验收，再写功能。

## v0.1 — MVP（已合并）

- pack/seeds 校验、URL 去重、覆盖度、目录/缺口/报告；
- `scan --base` 增量 diff；
- 可选 GitHub metadata；
- 10 个单测。

## v0.2.1 — Seed Lite（已合并）

- 最小 6 字段：`id/url/evidence_level/covers/quotes/status`；
- 其余字段默认值；
- `--strict` 保留 v0.1 完整校验；
- 12 个单测。

## v0.2.2 — 账本层 scan --since（已合并）

- 来源级变更：新增、移除、字段变化（`evidence_level/covers/quotes/license/access/version/content_hash/etag`）；
- `scan --since <旧 run>` 写 `changes.md` + `changes.json`，同时保留覆盖 diff；
- 19 个单测；
- **明确不做**：网络 `--fetch`，不假装已经抓网页；抓取留给 adapter。

## v0.2.3 — Gitee adapter（已合并）

- `GITEE_TOKEN`（env 或 `~/.config/radar/gitee_token`）；
- `Authorization: Bearer`，token 不进 URL/日志；
- `--gitee` + `source_map.gitee` 查询；
- 只做公开仓库 metadata，license 默认 `needs_review`；
- 无 token 明确跳过；
- 21 个单测。

## v0.2.4 — Forward snowballing（已合并）

- GitHub forks：从已选 GitHub 来源取 fork；
- 继承 parent 的 `covers`，`why_selected=forward: fork of <id>`；
- 只做 metadata，不读正文；
- 可选 `--snowball --snowball-per-source --snowball-max`；
- **不做**：GitHub dependents、Gitee forks、引用图（后续）。

## v0.2.5 — 网络 --fetch（已合并）

- `--fetch`：curl 抓 URL 的 ETag/Last-Modified/正文 hash；
- 更新 `http_status/last_seen/content_hash/etag/last_modified`；
- 401→login_required，403→blocked，404→deleted；
- `--fetch-limit` 控制条数；
- 与 `scan --since` 配合：hash 变了就报变化。

## v0.2 — 可迭代

目标：从“手动重跑”变成“只处理变化”。

- 来源状态：`last_seen`、`etag`、`content_hash`、`version`、`license_hash`；
- `scan --since`：只抓变化，不重跑全量；
- 定时触发（cron / DSH schedule）；
- diff 区分：新增、内容变化、许可变化、覆盖变化、删除/归档；
- **forward snowballing**：dependents、fork 网络、文档交叉引用（不能只盯已有来源，否则是引用回音室）；
- **最小种子字段**：`id/url/evidence_level/covers/quotes/status` 六项即可录入，其余由 adapter 补全。

验收：同一批来源，改一个页面/一个 release，`scan` 只报那一处变化。

## v0.3 — 网页抽取 + 许可提示（部分完成）

- `--web`：curl 抓公开 HTML，stdlib 解析 title/description/正文/短引用；
- `--web-limit` 控制条数；
- 最小许可识别：MIT/Apache/GPL/AGPL/LGPL/MPL/BSD/Unlicense/CC0/proprietary；
- 许可只做提示，不替代人工复核；不执行 JS、不绕登录；
- 31 个单测；
- 非 2xx 不冒充 200；中文按标点切句；许可只认强信号；
- **未做**：Playwright/登录页/PDF/OCR/docling/ScanCode；v0.3 只完成静态网页 + 提示。

## v0.3 — 多平台（原方向）

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
