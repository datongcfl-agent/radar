# radar · 最小行业雷达（MVP）

输入一个行业 pack 和一批来源，输出：**目录 + 来源账本 + 覆盖度 + 缺口 + 报告 + diff**。

不是爬虫，不是通用搜索引擎，也不是自动写 PRD。它只做一件事：**把“目录每一块有没有证据”算清楚。**

## 快速开始

```bash
cd radar

python3 -m radar validate \
  --pack packs/weak-current/pack.json \
  --seeds seeds/weak-current.json
# 可选：--strict 要求 v0.1 的完整 12 字段

python3 -m radar run \
  --pack packs/weak-current/pack.json \
  --seeds seeds/weak-current.json \
  --title "弱电管理系统" \
  --out runs/weak-current-demo

# 第二次：基于上次 run 做增量扫描
python3 -m radar scan \
  --pack packs/weak-current/pack.json \
  --seeds seeds/weak-current.json \
  --title "弱电管理系统" \
  --out runs/weak-current-demo-v2 \
  --since runs/weak-current-demo
```

`scan` 会在新 run 里多写 `changes.md`（来源级新增/移除/变化）和 `diff.md`（覆盖变化）。

输出：

```text
runs/weak-current-demo/
├── sources.jsonl     # 每条来源：平台/URL/许可/访问/证据/覆盖
├── coverage.json     # 模块×来源的覆盖矩阵
├── changes.md        # scan --since：来源级变更（新增/移除/字段变化）
├── toc.md            # 目录：模块/子系统 + 覆盖状态
├── coverage.md       # 覆盖明细
├── gaps.md           # 无证据 + 单源待印证
├── report.md         # 汇总/低星发现/许可问题/来源清单
└── state.json        # run 元数据、pack/seeds 哈希
```

## 两个 pack 证明可替换

```bash
python3 -m radar run \
  --pack packs/pet-hospital/pack.json \
  --seeds seeds/pet-hospital.json \
  --title "宠物医院管理系统" \
  --out runs/pet-hospital-demo
```

同一套代码，换 pack 就能跑；弱电和宠物医院互不写死。

## 命令

```bash
python3 -m radar run --pack <pack.json> --seeds <seeds.json> --title "<标题>" --out <dir>
python3 -m radar scan --pack <pack.json> --seeds <seeds.json> --title "<标题>" --out <dir> --base <旧 run>
python3 -m radar validate --pack <pack.json> --seeds <seeds.json>
python3 -m radar diff --from <run-a> --to <run-b> --out <diff.md>
```

可选 GitHub / Gitee 搜索（默认关闭，避免限流）：

```bash
GITHUB_TOKEN=... python3 -m radar run ... --github --limit 3 --max-queries 3
GITEE_TOKEN=...  python3 -m radar run ... --gitee  --limit 3 --max-queries 3

# 可选：forward snowballing（GitHub forks）
GITHUB_TOKEN=... python3 -m radar run ... --snowball --snowball-per-source 2 --snowball-max 5

# 可选：抓 URL 的 ETag/content_hash（网络）
python3 -m radar run ... --fetch --fetch-limit 5

# 可选：抽取公开网页正文 + 许可提示（网络，可遵守 robots）
python3 -m radar run ... --web --web-limit 5 --respect-robots
```

网络选项（`--github/--gitee/--snowball/--fetch/--web`）需要本机有 `curl`；没有会直接报错，不会逐条伪装成 `web_error`。

### Gitee（可选）

1. Gitee → 设置 → 私人令牌 → 新建，最小权限（只读 projects/仓库读取；不要给 admin/hook）；
2. 二选一：
   - `export GITEE_TOKEN=...`；
   - 写入 `~/.config/radar/gitee_token`，`chmod 600`；
3. 运行时加 `--gitee`。

token 只通过 `Authorization: Bearer` 发送，不拼进 URL、不写日志；没有 token 时 `--gitee` 会明确跳过，不会静默返回空。

细节见 [docs/GITEE.md](docs/GITEE.md)。

## 覆盖度规则

- `strong`：至少 2 个来源，且至少 1 个达到 `real_artifact/code_tests/production` + 有 quote；
- `evidence`：有 `readme/docs` + quote；**单源最高只能到 evidence**；
- `mention`：只提到名字，没有 quote；
- `none`：没有来源。

单源不是不能用，是不能当“已证实”用。`gaps.md` 会单独列“单源待印证”。

### 证据阶梯的方向

`production > code_tests > real_artifact` 是**存在性阶梯**：在产系统能证明“这个做法真的存在”，不等于“工程质量更好”。  
判断质量时要另看测试、文档、维护、边界；不要把存在性排序当质量排序。

## 当前 MVP 的边界

- **包含**：Seed Lite（最小 6 字段 + 默认值 + `--strict`）、pack/seeds 校验、URL 去重、覆盖度、目录/缺口/报告、`scan --since` 账本层变更检测 + 覆盖 diff、可选 GitHub/Gitee metadata 搜索、`--snowball`（GitHub forks）、`--fetch`（ETag/content_hash）、`--web`（静态正文抽取 + 许可提示，可选 `--respect-robots`）；
- **不包含**：浏览器/登录、全量爬虫、UI、自动 PRD、OCR、定时任务（scan 是手动触发）、Gitee forks、GitHub dependents/引用图；`--fetch` 只抓公开 URL 的头/体 hash；`--web` 只做静态 HTML，不执行 JS、不绕登录；Playwright/docling/ScanCode 未做，v0.3 是**部分完成**；
- **来源**：seeds 是人工/agent 填的；`--github` 只到 metadata，不读正文；
- **许可**：专有来源只进参考池，不能复用；`needs_review` 要人工复核。

## 路线图

| 版本 | 主题 | 关键交付 |
| --- | --- | --- |
| v0.1 | MVP（当前） | pack/seeds、覆盖度、缺口、`scan --base`、GitHub metadata |
| v0.2 | 可迭代 | `scan --since`、来源 hash/ETag、定时触发 |
| v0.3 | 多平台 | Gitee、网页/浏览器、docling、grant/ScanCode |
| v0.4 | 证据层 | claim/置信度/矛盾/复核队列 |
| v0.5 | 真实行业包 | 第二个真实行业 + 人工基线对比 |
| v1.0 | 稳定契约 | schema 冻结、迁移、handoff、可选 plugin/MCP |

详见 [ROADMAP.md](ROADMAP.md)。不承诺日期，也不承诺“收集所有开源信息”。

## 测试

```bash
python3 -m unittest discover -s tests -v
```

31 个用例覆盖：pack/seeds 校验、Seed Lite 默认值、`--strict` 拒绝最小字段、URL 规范化、单源上限、双源 strong、mention/none、gaps、来源级变更、Gitee metadata 映射、fetch 状态、snowball fork 映射、HTML 抽取、中文 quote、404 不冒充成功、license 提示、CLI run/scan/diff。

## 交给其他 Agent

- [HANDOFF.md](HANDOFF.md)：三种交接方式（DSH skill / CLI / 只读）；
- [AGENT-TASK.md](AGENT-TASK.md)：给对方的任务书；
- `./make_handoff.sh`：打一个可发送的 tar.gz。

## 设计依据

- 路线图：[ROADMAP.md](ROADMAP.md)
- Pack 写法：[docs/PACK.md](docs/PACK.md)
- MVP 验收：[docs/MVP.md](docs/MVP.md)
- Agent 规矩：[AGENTS.md](AGENTS.md)

## 目录

```text
radar/
├── radar/            # CLI + 校验 + 覆盖度 + diff
├── packs/            # weak-current / pet-hospital
├── seeds/            # 两个行业的种子来源
├── tests/            # 31 个单测
├── docs/             # PACK / MVP
├── .dsh/skills/radar # Skill
└── runs/             # demo 输出
```
