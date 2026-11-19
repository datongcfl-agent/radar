# MVP 验收

## 范围

- CLI：`run / validate / diff`；
- 单行业 pack + seeds；
- 可选 GitHub metadata 搜索；
- 输出目录/覆盖度/缺口/报告/diff；
- 不做 Gitee/浏览器/UI/自动 PRD/全量爬虫。

## 验收标准

1. `validate` 对两个 pack 都通过；
2. `run` 能生成 7 个文件；
3. 每个模块/子系统都有 `none/mention/evidence/strong`；
4. 单源模块被降级为 `evidence`，并出现在 `gaps.md` 的“单源待印证”；
5. 两次 run 能 `diff` 出新增/移除/覆盖变化；
6. 换 pack 不改代码能跑（weak-current → pet-hospital）；
7. 专有来源在 `report.md` 里标“不可复用”。

## 已知不足

- seeds 是人工/agent 填的，不是自动发现；
- `--github` 只到 metadata，不读正文；
- 没有 Gitee/浏览器/登录；
- 没有抽取/摘要/自动写 PRD；
- 没有定时任务/增量扫描（下一步）；
- 许可只到 `clear/needs_review/proprietary`，没有文件级判断。

## 下一步

1. 加 `scan --since` + 定时任务；
2. 接 Gitee/网页正文；
3. 接 docling/trafilatura 抽取；
4. 接 grant/ScanCode 许可；
5. 第二个真实行业 pack（不是 smoke test）。
