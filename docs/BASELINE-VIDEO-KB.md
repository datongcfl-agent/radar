# video-kb 基线（v0.7.0）

## 数字

| 项 | 值 |
| --- | ---: |
| 公开来源 | 30 |
| selected / needs_review | 22 / 8 |
| 模块 / 子系统 | 10 / 16 |
| strong / evidence / mention / none | **0 / 25 / 1 / 0** |
| 单源单元 | 9（M03、M07、M09、S01、S06、S09、S12、S13、S16） |

对应产物：`runs/video-kb-demo/`。  
`state.json` 的 `seeds_sha256` / `pack_sha256` 与仓库内文件一致。

## 来源构成

- 语音/转写：Whisper、whisper.cpp、faster-whisper、FunASR、WhisperX、pyannote、Private-ASR；
- 采集/下载：bili2text、VideoTranscribe、yt-dlp；
- 文档/结构化：Docling、Fabric；
- 知识库/笔记：SiYuan、Memos、Logseq、Obsidian；
- 检索/RAG：Khoj、Reor、RAGFlow、AnythingLLM、Qdrant、LangChain；
- 复习/闪卡：Anki；
- 官方文档：OpenAI Speech-to-Text、Ollama、Qdrant、LangChain、Obsidian、Anki。

## 为什么 strong 是 0

30 条来源的 `quote_verified` 都是 `unknown`，没有跑 `--web` 机器验证；按 v0.6 门禁，最高 evidence。  
这不是数据失败，是“没有经过本次抓取验证的 quote 不能算 strong”。

## 缺口

- 唯一 mention：`S07` 结构化笔记模板；
- 9 个单源：M03、M07、M09、S01、S06、S09、S12、S13、S16；
- 这些是下一轮搜索方向，不是完整性证明。

## 结论

第 2 个真实 pack 已能跑：同一套引擎，换 pack 不改代码；30 条来源覆盖 10 模块 / 16 子系统，0 none。  
但 strong=0、9 个单源，说明“有来源”不等于“有独立验证”。
