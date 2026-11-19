# MVP 验收

## 范围

- CLI：`run / scan / claims / validate / diff`；
- 单行业 pack + seeds（weak-current 34 条，pet-hospital 3 条占位）；
- 可选 GitHub/Gitee metadata 搜索、GitHub forks、`--fetch`、`--web`；
- 输出目录/覆盖度/缺口/报告/diff/claim 账本；
- 不做浏览器/UI/自动 PRD/全量爬虫。

## 验收标准

1. `validate` 对所有 pack 都通过；
2. `run` 能生成 7 个文件；
3. 每个模块/子系统都有 `none/mention/evidence/strong`；
4. 单源模块被降级为 `evidence`，并出现在 `gaps.md` 的“单源待印证”；
5. 两次 run 能 `diff` 出新增/移除/覆盖变化；
6. 换 pack 不改代码能跑（weak-current → pet-hospital）；
7. 专有来源在 `report.md` 里标“不可复用”。

## 已知不足

- seeds 是人工/agent 填的，不是自动发现；
- seeds 仍是人工/agent 填的，不是自动发现；
- Gitee 只做公开仓库 metadata；
- `--web` 只做静态 HTML，不执行 JS/登录；
- claim 由人写，置信度是规则启发式；
- 许可只到 `clear/needs_review/proprietary`，没有文件级判断；
- 第二个真实行业 pack 还没做。

## 下一步

1. 第二真实行业 pack（30+ 来源，证明换 pack 不改引擎）；
2. v1.0 契约冻结：pack/seeds/claims/state schema、迁移、handoff；
3. 定时任务/浏览器/ScanCode 等按需，不先加依赖。
