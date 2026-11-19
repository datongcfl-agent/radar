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
python3 -m radar run --pack packs/weak-current/pack.json --seeds seeds/weak-current.json \
  --title "弱电管理系统" --out runs/weak-current-demo
python3 -m radar scan --pack packs/weak-current/pack.json --seeds seeds/weak-current.json \
  --title "弱电管理系统" --out runs/weak-current-demo-v2 --base runs/weak-current-demo
python3 -m radar diff --from runs/a --to runs/b --out runs/diff.md
```

## 模糊需求 → pack 的拆解方法

用户给的需求多半是一句话（如"视频转文字放知识库，用于学习"），不要拿原话去搜，先拆 pack：

1. **切价值链**：需求按"输入→处理→存储→使用→输出"切阶段（如：采集→转写→结构化→入库→检索→使用）；
2. **每阶段 1–2 个管理模块**（M），模块下再拆子系统（S），先粗后细；
3. **每格填 keywords 时先收集该领域的黑话**：英文平台用英文行话（如 diarization/VAD/ASR，而不是"说话人分离"）；
4. **最小起步**：第一版 pack 控制在 10 格左右，跑一轮看查询命中率与缺口，再细化格子——不要一步拍 26 格。

## 搜索纪律

- 查询词 = **模块 × 证据物 × 黑话**，禁止拿需求原话当查询词（原话召回极低）；
- 每格中英双语各搜一轮；同义词组轮换（如 whisper/ASR/transcribe）；
- GitHub 中文长查询经常 0 结果——返回空时先怀疑查询词，换黑话重试，不要直接记为"无来源"；
- star 只作弱信号，按模块/证据物搜，不按 star 排名搜。

## seeds 录入标准

- URL 必须**当场经 API/页面核实存在**（禁止凭记忆写 URL）；
- `quotes` 只写**真实读到的原文**，没读到就不写（无 quote 最多 mention）；
- 元数据（stars/license/description）当场拉取，不靠记忆补；
- 检索时间写进 `retrieved_at`；拿不准的许可标 `needs_review`，不猜。

## 输出契约

- `toc.md`：模块/子系统 + 覆盖级别；
- `coverage.md`：模块×来源；
- `gaps.md`：无证据 + 单源待印证；
- `report.md`：汇总/低星/许可/来源清单；
- `sources.jsonl`：机器可读账本；
- `scan` 额外写 `diff.md`（新增/移除/覆盖变化）。

## 硬规则

- 单源最高 `evidence`，不能 `strong`；
- 专有来源只进参考池，不能复用；
- `needs_review` 要人工复核；
- 不绕过登录/付费/验证码；
- 不把行业结论写进引擎，写进 pack；
- 没有 quote 的来源最多 `mention`。

## 边界

- seeds 由人或 agent 填；`--github` 只到 metadata；
- 不做 Gitee/浏览器/UI/自动 PRD；
- 结果用于“找缺口”，不是“证明完整”。
