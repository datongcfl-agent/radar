# 视频转知识库（学习用途） · 雷达目录

Pack: `video-kb` v0.1.0

## 管理模块

| ID | 模块 | 覆盖 | 来源数 | 最强来源 |
| --- | --- | --- | ---: | --- |
| `M01` | 采集与导入 | **evidence** | 2 | SRC-017 |
| `M02` | 语音转写 | **evidence** | 9 | SRC-022 |
| `M03` | 文本结构化 | **evidence**（单源） | 3 | SRC-018 |
| `M04` | 知识库存储 | **evidence** | 4 | SRC-028 |
| `M05` | 归类与关联 | **evidence** | 3 | SRC-029 |
| `M06` | 检索与问答 | **evidence** | 6 | SRC-021 |
| `M07` | 跨端与同步 | **evidence**（单源） | 2 | SRC-028 |
| `M08` | 学习闭环 | **evidence**（单源） | 2 | SRC-013 |
| `M09` | 隐私与本地化 | **evidence**（单源） | 4 | SRC-019 |
| `M10` | 部署与运维 | **evidence** | 2 | SRC-019 |

## 子系统

| ID | 子系统 | 覆盖 | 来源数 | 最强来源 |
| --- | --- | --- | ---: | --- |
| `S01` | 字幕优先抓取 | **evidence**（单源） | 1 | SRC-017 |
| `S02` | 视频下载 | **evidence** | 2 | SRC-017 |
| `S03` | Whisper 转写引擎 | **evidence** | 7 | SRC-016 |
| `S04` | 说话人分离 | **evidence** | 4 | SRC-023 |
| `S05` | 长音频切分/VAD | **evidence** | 2 | SRC-023 |
| `S06` | LLM 摘要与大纲 | **evidence**（单源） | 2 | SRC-018 |
| `S07` | 结构化笔记模板 | **mention** | 1 | SRC-002 |
| `S08` | Markdown/双链存储 | **evidence** | 3 | SRC-028 |
| `S09` | 自动标签与聚类 | **evidence**（单源） | 1 | SRC-010 |
| `S10` | 向量化/embedding | **evidence** | 4 | SRC-020 |
| `S11` | RAG 问答 | **evidence** | 7 | SRC-021 |
| `S12` | 桌面客户端 | **evidence**（单源） | 1 | SRC-009 |
| `S13` | 移动端 | **mention** | 1 | SRC-030 |
| `S14` | 同步机制 | **evidence** | 2 | SRC-028 |
| `S15` | 复习/闪卡 | **evidence**（单源） | 2 | SRC-013 |
| `S16` | 本地模型运行 | **evidence**（单源） | 2 | SRC-019 |

## 怎么读

- `strong`：有一手证据/可验证数据；`evidence`：文档/README 有流程或字段；
- `mention`：只提到名字；`none`：没有来源；
- 覆盖度不是质量排名，它只说明“这块有没有证据、下一步该补什么”。
