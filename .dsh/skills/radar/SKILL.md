---
name: radar
description: 用行业 pack + 来源账本 + 覆盖度矩阵，产出目录/缺口/报告的最小行业雷达。
---

# radar

当用户要“按行业找需求、看覆盖度、找缺口”时使用；不是通用搜索，也不是自动写 PRD。

## 怎么用

```bash
cd <radar-repo>
python3 -m radar validate --pack packs/weak-current/pack.json --seeds seeds/weak-current.json
# 可选：--strict 要求 v0.1 的完整 12 字段
python3 -m radar run --pack packs/weak-current/pack.json --seeds seeds/weak-current.json \
  --title "弱电管理系统" --out runs/weak-current-demo
# 可选：Gitee 需要 GITEE_TOKEN（env 或 ~/.config/radar/gitee_token）
python3 -m radar run ... --gitee --limit 3 --max-queries 3
# 可选：forward snowballing / 网络刷新
python3 -m radar run ... --snowball --snowball-max 5
python3 -m radar run ... --fetch --fetch-limit 5
python3 -m radar scan --pack packs/weak-current/pack.json --seeds seeds/weak-current.json \
  --title "弱电管理系统" --out runs/weak-current-demo-v2 --since runs/weak-current-demo
python3 -m radar diff --from runs/a --to runs/b --out runs/diff.md
```

## 输出契约

- `toc.md`：模块/子系统 + 覆盖级别；
- `coverage.md`：模块×来源；
- `gaps.md`：无证据 + 单源待印证；
- `report.md`：汇总/低星/许可/来源清单；
- `sources.jsonl`：机器可读账本；
- `scan` 额外写 `changes.md`（来源级新增/移除/变化）和 `diff.md`（覆盖变化）。

## 硬规则

- 单源最高 `evidence`，不能 `strong`；
- 专有来源只进参考池，不能复用；
- `needs_review` 要人工复核；
- 不绕过登录/付费/验证码；
- 不把行业结论写进引擎，写进 pack；
- 没有 quote 的来源最多 `mention`。

## 边界

- seeds 由人或 agent 填；`--github` 只到 metadata；
- 不做 Gitee forks/GitHub dependents/浏览器/UI/自动 PRD；
- 结果用于“找缺口”，不是“证明完整”。
