# radar · 最小行业雷达（MVP）

输入一个行业 pack 和一批来源，输出：**目录 + 来源账本 + 覆盖度 + 缺口 + 报告 + diff**。

不是爬虫，不是通用搜索引擎，也不是自动写 PRD。它只做一件事：**把“目录每一块有没有证据”算清楚。**

## 快速开始

```bash
cd radar

python3 -m radar validate \
  --pack packs/weak-current/pack.json \
  --seeds seeds/weak-current.json

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
  --base runs/weak-current-demo
```

`scan` 会在新 run 里多写一个 `diff.md`（新增/移除/覆盖变化）。

输出：

```text
runs/weak-current-demo/
├── sources.jsonl     # 每条来源：平台/URL/许可/访问/证据/覆盖
├── coverage.json     # 模块×来源的覆盖矩阵
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

可选 GitHub 搜索（默认关闭，避免限流）：

```bash
GITHUB_TOKEN=... python3 -m radar run ... --github --limit 3 --max-queries 3
```

## 覆盖度规则

- `strong`：至少 2 个来源，且至少 1 个达到 `real_artifact/code_tests/production` + 有 quote；
- `evidence`：有 `readme/docs` + quote；**单源最高只能到 evidence**；
- `mention`：只提到名字，没有 quote；
- `none`：没有来源。

单源不是不能用，是不能当“已证实”用。`gaps.md` 会单独列“单源待印证”。

## 当前 MVP 的边界

- **包含**：pack/seeds 校验、URL 去重、覆盖度、目录/缺口/报告、`scan --base` 增量 diff、可选 GitHub 搜索；
- **不包含**：Gitee/浏览器/登录、全量爬虫、UI、自动 PRD、OCR、定时任务（scan 是手动触发）；
- **来源**：seeds 是人工/agent 填的；`--github` 只到 metadata，不读正文；
- **许可**：专有来源只进参考池，不能复用；`needs_review` 要人工复核。

## 测试

```bash
python3 -m unittest discover -s tests -v
```

10 个用例覆盖：pack/seeds 校验、URL 规范化、单源上限、双源 strong、mention/none、gaps、CLI run、diff。

## 交给其他 Agent

- [HANDOFF.md](HANDOFF.md)：三种交接方式（DSH skill / CLI / 只读）；
- [AGENT-TASK.md](AGENT-TASK.md)：给对方的任务书；
- `./make_handoff.sh`：打一个可发送的 tar.gz。

## 设计依据

- 雷达总纲：[RADAR-NOTES.md](../elv-mgmt/radar-meta/RADAR-NOTES.md)
- 先例核实：[PRIOR-ART.md](../elv-mgmt/radar-meta/PRIOR-ART.md)
- 弱电试验：[research-probe-v2.md](../elv-mgmt/research-probe-v2.md)
- Pack 写法：[docs/PACK.md](docs/PACK.md)
- MVP 验收：[docs/MVP.md](docs/MVP.md)

## 目录

```text
radar/
├── radar/            # CLI + 校验 + 覆盖度 + diff
├── packs/            # weak-current / pet-hospital
├── seeds/            # 两个行业的种子来源
├── tests/            # 10 个单测
├── docs/             # PACK / MVP
├── .dsh/skills/radar # Skill
└── runs/             # demo 输出
```
