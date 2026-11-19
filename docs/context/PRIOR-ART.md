# 先例核实（prior art）

日期：2026-11-19
范围：快速公开检索，不是专利/学术查新。结论只代表“这次查到的”，不代表“世界上没有”。

## 结论

**你不是第一个想到这些组件的人；但“行业包 + 证据/许可账本 + 覆盖度矩阵 + agent 产出目录/PRD”这个组合，这次没找到完全一致的产品。**

所以：

- 不要宣称“首创”；
- 可以说“这是一个特定组合”；
- 真正的差异不在概念，在**执行层**：证据分级、许可/访问账本、覆盖度驱动、行业包复用。

## 组件先例

| 你的组件 | 先例 | 它做了什么 | 它没做什么 |
|---|---|---|---|
| 技术雷达 | [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar) | 用 adopt/trial/assess/hold 分环，编辑团队给技术趋势判断 | 不是行业需求发现；没有来源许可/覆盖度账本 |
| 模糊想法→PRD | [ChatPRD](https://www.chatprd.ai/product/features/write-prd) | 从粗想法/会议记录生成 PRD、用户故事、技术规格；模板、上下文、gap 分析、版本 | 不做开源/行业检索，不做来源许可/覆盖度 |
| AI 研究/综述 | [GPT-Researcher](https://github.com/assafelovic/gpt-researcher)、[STORM](https://github.com/stanford-oval/storm) | 多源检索 + 长报告生成 | 不保证证据等级/许可/覆盖度 |
| LLM 需求获取 | [LLM Requirements Elicitation 综述](https://zenodo.org/records/20100876)、[AI-assisted RE 系统综述](https://dl.acm.org/doi/abs/10.1145/3696673.3723053) | 研究 LLM 如何辅助需求获取/分析 | 多是方法/实验，不是行业雷达产品 |
| 行业参考模型/能力地图 | [Gartner 能力清单讨论](https://www.gartner.com/peer-community/post/we-looking-perform-business-driven-application-portfolio-governance-program-however-i-read-we-start-tie-applications)、[LeanIX 能力建模](https://help.sap.com/docs/leanix/ea/business-capabilities-modeling-v3?locale=en-US&q=reference+catalog)、BIAN/TM Forum/ACORD/HL7 | 行业通用能力/流程/数据模型 | 不是开源证据检索；不解决 0 星资料/许可 |
| 系统综述/滚雪球 | [Snowballing 方法](https://www.bodleian.ox.ac.uk/sites/default/files/bodreader/documents/media/systematicreviews4-snowballingandwriteup-transcript.pdf)、PRISMA | 引用链追踪、系统性检索、纳入/排除 | 学术流程重，不是产品化雷达 |
| 来源可信度 | [Admiralty Code](https://www.sans.org/blog/admiralty-code-part-2-ticketmaster-data-breach-claims)、GRADE | 来源可靠性 + 信息可信度分级 | 没和需求/行业包打通 |
| 需求覆盖/追溯 | [reqcov](https://pypi.org/project/reqcov/0.3.0/)、Doorstop、StrictDoc、Duvet | 需求↔实现↔测试的覆盖/追溯 | 不负责“来源发现”和“行业目录” |
| 行业包/垂直模板 | [Vertical packs](https://deepwiki.com/ruvnet/metaharness/2.2-templates-and-vertical-packs)、行业云模板 | 按行业给模板/组件 | 模板不是证据账本，也不做覆盖度 |

## 你的组合到底新在哪

不是“雷达”这个词，也不是“AI 写 PRD”，而是这几件事同时成立：

1. **行业包**决定“该有哪些模块/子系统”，不是让模型自由发挥；
2. **证据/许可/访问账本**决定“每条信息能信到什么程度、能不能用”；
3. **覆盖度矩阵**决定“下一轮搜什么”，不是排个榜；
4. **低星/灰文献优先**，不按 star；
5. **agent 编排 + 一次人工拍板**，不是问卷；
6. **换行业只换 pack**，引擎不变。

这套组合这次没找到完全一样的现成产品；但每个零件都有人做过。

## 没查到的

这次是快速公开检索，没做：

- 专利检索（Google Patents/CNIPA）；
- ACM/IEEE/arXiv 系统查新；
- Product Hunt/G2/垂直 SaaS 目录；
- 创业公司数据库/融资信息；
- 中文专利/论文库。

所以不能下“全球首创”的结论。

## 判断

- **概念层**：不是第一个；技术雷达、能力地图、系统综述、AI 研究 agent、AI PRD 都有先例。
- **组合层**：这次没找到完全一致的；可能是较早把“行业包 + 证据账本 + 覆盖度 + agent”做成插件的人。
- **壁垒**：不在“想到”，在**行业包库 + 证据账本 + 执行纪律**。这三样越用越厚，别人复制概念容易，复制数据/判断难。

建议对外表述：

> 不是一个全新的雷达概念，而是把技术雷达、行业参考模型、系统综述、证据分级和 AI 研究 agent 组合成一个“行业需求雷达”：先出目录，再出证据/覆盖度，最后才写 PRD。
