# 覆盖度明细

| 层级 | 数量 |
| --- | ---: |
| none | 0 |
| mention | 0 |
| evidence | 26 |
| strong | 0 |

## 管理模块

### M01 采集与导入 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-001` | github | evidence | MIT | public |
| `SRC-017` | github | evidence | Unlicense | public |

### M02 语音转写 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-001` | github | evidence | MIT | public |
| `SRC-002` | github | mention | unknown | public |
| `SRC-003` | github | evidence | MIT | public |
| `SRC-004` | github | mention | MIT | public |
| `SRC-005` | github | mention | MIT | public |
| `SRC-015` | github | mention | MIT | public |
| `SRC-016` | github | evidence | MIT | public |
| `SRC-022` | github | evidence | BSD-2-Clause | public |
| `SRC-024` | docs | mention | unknown | public |

### M03 文本结构化 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-014` | github | mention | MIT | public |
| `SRC-015` | github | mention | MIT | public |
| `SRC-018` | github | evidence | MIT | public |

### M04 知识库存储 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-006` | github | mention | AGPL-3.0 | public |
| `SRC-008` | github | mention | AGPL-3.0 | public |
| `SRC-028` | docs | evidence | unknown | public |
| `SRC-029` | docs | evidence | unknown | public |
| `SRC-031` | github | evidence | unknown | public |

### M05 归类与关联 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-008` | github | mention | AGPL-3.0 | public |
| `SRC-010` | github | evidence | AGPL-3.0 | public |
| `SRC-029` | docs | evidence | unknown | public |

### M06 检索与问答 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-009` | github | evidence | AGPL-3.0 | public |
| `SRC-010` | github | evidence | AGPL-3.0 | public |
| `SRC-011` | github | mention | Apache-2.0 | public |
| `SRC-012` | github | mention | MIT | public |
| `SRC-021` | github | evidence | MIT | public |
| `SRC-027` | docs | mention | unknown | public |

### M07 跨端与同步 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-006` | github | mention | AGPL-3.0 | public |
| `SRC-028` | docs | evidence | unknown | public |

### M08 学习闭环 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-013` | github | evidence | unknown | public |
| `SRC-030` | docs | mention | unknown | public |

### M09 隐私与本地化 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-008` | github | mention | AGPL-3.0 | public |
| `SRC-012` | github | mention | MIT | public |
| `SRC-019` | github | evidence | MIT | public |
| `SRC-025` | docs | mention | unknown | public |

### M10 部署与运维 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `SRC-007` | github | evidence | MIT | public |
| `SRC-019` | github | evidence | MIT | public |

## 子系统

- **S01 字幕优先抓取** — evidence（1 个来源）
- **S02 视频下载** — evidence（2 个来源）
- **S03 Whisper 转写引擎** — evidence（7 个来源）
- **S04 说话人分离** — evidence（4 个来源）
- **S05 长音频切分/VAD** — evidence（2 个来源）
- **S06 LLM 摘要与大纲** — evidence（2 个来源）
- **S07 结构化笔记模板** — evidence（2 个来源）
- **S08 Markdown/双链存储** — evidence（3 个来源）
- **S09 自动标签与聚类** — evidence（1 个来源）
- **S10 向量化/embedding** — evidence（4 个来源）
- **S11 RAG 问答** — evidence（7 个来源）
- **S12 桌面客户端** — evidence（1 个来源）
- **S13 移动端** — evidence（2 个来源）
- **S14 同步机制** — evidence（2 个来源）
- **S15 复习/闪卡** — evidence（2 个来源）
- **S16 本地模型运行** — evidence（2 个来源）

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
