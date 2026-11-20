# 缺口清单

## 没有证据的模块

没有缺口：所有模块至少有 `evidence` 级来源。

## 单源待印证

这些模块只有 1 个来源；按单源规则，最高只能算 `evidence`，需要第二源。

- `M03` 文本结构化（evidence，来源 `SRC-014, SRC-015, SRC-018`）
- `M07` 跨端与同步（evidence，来源 `SRC-006, SRC-028`）
- `M08` 学习闭环（evidence，来源 `SRC-013, SRC-030`）
- `M09` 隐私与本地化（evidence，来源 `SRC-008, SRC-012, SRC-019, SRC-025`）
- `S01` 字幕优先抓取（evidence，来源 `SRC-017`）
- `S06` LLM 摘要与大纲（evidence，来源 `SRC-014, SRC-018`）
- `S07` 结构化笔记模板（evidence，来源 `SRC-002, SRC-031`）
- `S09` 自动标签与聚类（evidence，来源 `SRC-010`）
- `S12` 桌面客户端（evidence，来源 `SRC-009`）
- `S13` 移动端（evidence，来源 `SRC-030, SRC-032`）
- `S15` 复习/闪卡（evidence，来源 `SRC-013, SRC-030`）
- `S16` 本地模型运行（evidence，来源 `SRC-019, SRC-025`）

## 同源待印证

这些模块有 ≥2 条证据，但来自同一 host；不能当独立互证。

- `M01` 采集与导入（独立 host 1）
- `M02` 语音转写（独立 host 1）
- `M06` 检索与问答（独立 host 1）
- `M10` 部署与运维（独立 host 1）
- `S02` 视频下载（独立 host 1）
- `S03` Whisper 转写引擎（独立 host 1）
- `S04` 说话人分离（独立 host 1）
- `S05` 长音频切分/VAD（独立 host 1）
- `S10` 向量化/embedding（独立 host 1）
- `S11` RAG 问答（独立 host 1）
