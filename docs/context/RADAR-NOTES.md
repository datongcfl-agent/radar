# RADAR-NOTES · 最新雷达总纲（活文档）

> 状态：**活文档**，不是冻结规格。
> 目的：记录“最新雷达”的原则、接口和边界；行业结论一律放进行业包，不写进这里。
> 如果一条规则只对某个行业成立，它就不属于本文档，属于 pack。

## 0. 一句话

雷达是**行业知识地图 + 证据账本 + 缺口驱动搜索**，不是爬虫，不是通用搜索引擎，也不是自动写 PRD 的作者。

## 1. 定位

### 解决什么

- 模糊需求/新行业，不知道**该有哪些模块**；
- 资料散在 GitHub/Gitee/registry/文档/招标/社区，**找不全、记不住、不可复查**；
- 来源有营销、有二手、有专有许可，**不知道能信到什么程度、能不能用**；
- 每次做新产品都从零搜，**行业知识不沉淀**。

### 不解决什么

- 不收集“所有开源信息”（无底洞，也没必要）；
- 不替代用户访谈、领域专家、商业判断；
- 不保证“完整/正确”，只保证“覆盖到有证据、缺口看得见”；
- 不绕过登录、付费、验证码、访问控制；
- 不把专有/未核实来源写成可复用结论。

### 成功标准

1. 目录每一块都有 `strong/weak/none` 的覆盖判断；
2. 每个结论能追到 URL、许可、证据等级；
3. 下一轮该搜什么，能从缺口直接生成；
4. 换一个行业，只换 pack，不改引擎。

## 2. 形态

```text
引擎（固定） + 行业包（可替换） + 接口（CLI / skill）
```

| 层 | 内容 | 是否随行业变 |
|---|---|---|
| 引擎 | adapters、账本、证据阶梯、访问阶梯、覆盖度、diff、报告 | 不变 |
| 行业包 | 行业名/别名、价值链、模块、子系统/分类、证据物、来源地图、查询模板、权重、样例 | 变 |
| 接口 | `radar run / scan / diff / apply`；agent skill；以后的 review UI | 不变 |

**部署**：local-first。默认不跑中心化爬虫；adapter 可选、可关；数据留在本地/私有仓。

## 3. 核心对象

### 3.1 来源记录

```json
{
  "id": "SRC-001",
  "platform": "github|gitee|npm|pypi|web|docs|tender",
  "url": "https://...",
  "title": "...",
  "artifact_type": "code|readme|prd|quote_sheet|subsystem_list|ui_reference|manual|benchmark",
  "language": "zh|en",
  "retrieved_at": "2026-11-19T...",
  "http_status": 200,
  "access_status": "public|api_limited|login_required|paywalled|blocked|deleted|proprietary|unreachable",
  "license": "MIT|Apache-2.0|proprietary|unknown",
  "license_status": "clear|needs_review|proprietary",
  "evidence_level": "marketing|metadata|readme|docs|real_artifact|code_tests|production",
  "derived_from_real_data": true,
  "covers": ["M-03", "S-12"],
  "borrow_scope": ["workflow", "data_model", "interaction", "boundary_conditions", "engineering_practice"],
  "quotes": ["真正读到的原文"],
  "limitations": ["未深读代码"],
  "status": "selected|rejected|needs_review",
  "why_selected": "..."
}
```

### 3.2 主张记录（claim）

一个来源可以支持多个主张；一个主张可以有多个来源。

```json
{
  "claim_id": "C-001",
  "claim": "该行业常见 N 个子系统",
  "sources": ["SRC-001", "SRC-002"],
  "independent_sources": 2,
  "source_tier": "primary_practitioner|vendor|official|secondary",
  "evidence_level": "real_artifact|docs|readme|marketing",
  "verifiable": true,
  "single_source": false,
  "confidence": "high|medium|low|unverified",
  "contradictions": ["两套名单不同"],
  "decision_impact": "只影响目录粒度，不影响模块存在性"
}
```

### 3.3 行业包

```json
{
  "pack": "example-industry",
  "version": "0.1.0",
  "aliases": ["..."],
  "value_chain": ["阶段1", "阶段2"],
  "modules": [{"id": "M-01", "name": "...", "artifacts": ["..."]}],
  "subsystems": [{"id": "S-01", "name": "...", "tags": ["hotel", "office"]}],
  "source_map": {"github": ["..."], "gitee": ["..."], "web": ["..."]},
  "query_templates": ["{module} {artifact} site:{platform}"],
  "scoring_weights": {"evidence": 0.4, "domain_fit": 0.3, "maintenance": 0.2, "license": 0.1},
  "exemplars": []
}
```

### 3.4 覆盖度单元

```text
coverage[module][source] = none | mention | evidence | strong
```

- `none`：没有来源提到；
- `mention`：只提到名字；
- `evidence`：有流程/字段/规则/截图；
- `strong`：有真实单据/数据/代码/测试，且可复核。

## 4. 三个循环

| 循环 | 做什么 | 频率 | 输出 |
|---|---|---|---|
| 源监控 | 盯已有来源的 release/commit/文档 hash/license/归档 | 周 | `radar-diff.md` |
| 缺口驱动 | 看覆盖度，weak/none 的模块定向补搜 | 月 | 新候选 + 覆盖变化 |
| 包迭代 | 新模块/子系统/来源/查询模板，升 pack 版本 | 季度/重大发现 | `pack` changelog |

**原则**：迭代不是“再全量搜一遍”，是“只处理变化 + 只补缺口”。

## 5. 访问阶梯

```text
官方 API / 公开接口
→ 公开页面（必要时浏览器渲染）
→ 镜像/缓存/Wayback/Software Heritage/registry
→ 登录/授权会话
→ 二手资料/引用
→ 一手调研（访谈/用户提供）
→ 记缺口
```

必须记录：

- `access_status`：为什么不通；
- `unlock_path`：token / proxy / mirror / official_api / human / purchase；
- `fallback_sources`：替代源。

**不可达 ≠ 0 结果**；**登录墙 ≠ 没内容**；**专有 ≠ 可复用**。

## 6. 证据与可信度

### 6.1 证据阶梯

```text
marketing < metadata < readme < docs < real_artifact < code_tests < production
```

### 6.2 可信度维度

- 来源层级：一手/官方 > 一手实践者 > 二手 > 营销 > 匿名；
- 独立性：是否同一作者的转载/软文；
- 可验证性：能否对到代码、数据、测试、原始文件；
- 交叉印证：是否有第二个独立来源；
- 时效/版本；
- 具体性：有数字/字段/流程，还是泛泛而谈。

### 6.3 单源规则

- 单源可以当**线索**，不能当**定论**；
- 单源上限：除非是“可验证的一手证据”，否则最高 `medium`；
- 关键事实（价格、合规、安全、用户需求）需要 2 个独立来源或一手证据；
- 矛盾不强行合并，记 `contradiction`，保留两种说法。

## 7. 覆盖度矩阵

- 行：行业包的模块/子系统；
- 列：来源；
- 值：`none/mention/evidence/strong`；
- 它不是“排行榜”，是“下一步搜什么”的导航。

报告至少输出：

- 每个模块的“最强证据”；
- 没有 strong 的模块；
- 互相矛盾的来源；
- 平台覆盖（含 `unreachable`）。

## 8. 许可与合规

- `access` 与 `license` 分开：能读 ≠ 能复用；
- 无许可 = `needs_review`；source-available ≠ open source；
- 专有来源只进“参考池”，不进“可复用池”；
- 文档级许可要单独判断（代码许可 ≠ 文档/数据许可）；
- 不绕过访问控制，不违反平台条款，不批量抓；
- 本文档不提供法律意见。

## 9. 版本与迭代

三层版本：

```text
engine vX    # 采集/解析/覆盖度逻辑
pack vY      # 行业目录/来源/查询/权重
run vZ       # 每次扫描的账本快照
```

每次 run 产生：

- `radar-diff.md`：新增/更新/许可变化/矛盾/覆盖变化；
- `ledger.jsonl`：快照；
- `pack` 变更记录（如果更新了包）。

低风险（新增候选、版本更新）可自动入账；高风险（许可变专有、来源删除、矛盾）必须人工复核。

## 10. 角色分工

| 角色 | 做什么 |
|---|---|
| Agent / Superagent | 查询规划、读内容、抽证据、写摘要、判断取舍 |
| 脚本 | 抓取、快照、规范化、去重、覆盖度、diff、报告 |
| 人 | 一次拍板（目录+章节/样章）；高风险许可/矛盾决策 |

雷达不替代 agent，也不替代人；它让 agent 的阅读可复查，让人的拍板有依据。

## 11. MVP 与路线图

### Phase 0：账本 + 包 + 覆盖度（不写爬虫）

- 记录 schema、pack schema；
- 先选一个行业，手工种子 + `gh search` + agent web 搜索；
- 输出覆盖度 + 缺口，验证“目录每块有没有证据”。

### Phase 1：接采集/快照/去重/许可

- GitHub/Gitee/registry adapters；
- snapshot + content hash；
- datasketch/dedupe；
- grant/ScanCode + 人工复核。

### Phase 2：抽取/复核/diff/调度

- docling/trafilatura；
- CSV/Markdown 审核队列；
- `scan --since` + `diff`；
- 定时任务（周/月）。

### Phase 3：多行业包 + 可选 UI

- 第二个行业包验证“只换 pack”；
- Label Studio/自建 review UI（可选）；
- 远程/多人协作（可选）。

## 12. 边界与失败模式

| 失败模式 | 表现 | 对策 |
|---|---|---|
| star 排名 | 只找热门，漏 0 星好文档 | 按模块/证据物搜，star 只作弱信号 |
| 单源自信 | 一份 README 当行业标准 | `single_source` 标记 + 置信度上限 |
| 平台偏置 | 只搜 GitHub | 平台覆盖表 + unreachable 记录 |
| 专有抄袭 | 把专有文档改几个字 | 参考池/复用池分开，clean-room 重写 |
| 过度工程 | 又陷进爬虫/大 UI | Phase 0 先账本+覆盖度 |
| 假完整 | 覆盖表全绿但都是 mention | 区分 mention/evidence/strong |

## 13. 这份文档怎么改

- 只对某个行业成立的规则 → 放进 pack，不放进本文档；
- 改引擎接口/状态机 → 加一条变更记录，说明影响；
- 新增平台 → 先加 `platform` 与 `access_status`，再写 adapter；
- 不要在这份文档里写“弱电 18 个子系统”之类的行业结论；
- 本文档的版本跟引擎走，不跟 pack 走。

## 附录：弱电样例（不放进核心）

- [research-probe-v2.md](../research-probe-v2.md)：两套 18 系统、并集 24、管理与子系统双层目录；
- [radar-meta/README.md](README.md)：meta-run 的候选/覆盖/组装；
- [radar-meta-pack.md](radar-meta-pack.md)：雷达工程的模块与查询示例；
- [resource-radar 的 automation-boundary/source-policy/design-basis](../../../probe/radar/docs/)：原始雷达的边界思想。

这些只是**样例和证据**，不是雷达的核心规则。
