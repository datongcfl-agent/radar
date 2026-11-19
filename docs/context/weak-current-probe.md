# 弱电管理系统 · 新雷达第二次试验

日期：2026-11-19
方法：多平台（GitHub + Gitee + 公开网页）+ 按证据物搜（报价清单/子系统/点位/竣工/维保）+ 许可与证据分级 + 覆盖度矩阵。

## 这次新增了什么

第一次只搜 GitHub 的“管理系统”，漏掉了 Gitee 的 `eeops`。这次补上了：

- Gitee 仓库：`shmilytqq/eeops`（弱电工程运营管理系统）。
- Gitee 的报价 Excel 分析报告：从 4 份酒店弱电报价里统计出 18 个子系统。
- 公开行业文章：德立云《解锁弱电智能化：18 大系统构建智能世界》，给出另一套 18 系统。
- Gitee 的 IoT/设备/机房类仓库：`MicroCommunityIot`（Apache-2.0）、`idcops`（Apache-2.0）、`easyaiot`（MIT）、`iot_api`（MulanPSL-2.0）。

## 关键发现：18 不是标准，是“常见桶数”

两套 18 系统并不一样：

| 类别 | EEOPS 的 18 个（4 份酒店报价统计） | 德立云的 18 个（行业文章） |
|---|---|---|
| 基础 | 综合布线、网络/WIFI、机房 UPS | 综合布线、网络、综合管路、UPS |
| 安全 | 视频监控、门禁、巡更、入侵报警 | 视频监控、门禁、防盗报警、周界防范、巡更 |
| 楼控 | BA、公区温控、智能照明 | 楼宇自控、环境监控、照明控制、能源管理 |
| 信息 | 程控电话、背景音乐、IPTV、五方对讲、信息发布 | 通讯、有线电视、信息发布 |
| 会议/客房 | 多功能厅、客控、厨房排油烟 | 会议系统 |
| 停车 | — | 停车场 |

- 重叠约 12 个；
- EEOPS 独有 6 个：背景音乐、IPTV、五方对讲、客控、公区温控、厨房排油烟；
- 德立云独有 6 个：综合管路、周界防范、环境监控、能源管理、有线电视、停车场；
- **并集约 24 个**。

这说明：**“18 个板块”是行业里常见的分类粒度，不是固定清单。** 酒店、园区、医院、学校的 18 个会不一样。PRD 里不能写死 18 章，应该建一张“子系统主数据表”，带项目类型标签（酒店/办公/园区/医院/学校），按项目勾选。

## 两层目录，不是二选一

第一次的 14 个“管理模块”和这次的 24 个“子系统”是正交的：

- **管理主线（14）**：项目、合同、采购、施工、竣工、成本、发票、回款、售后、权限……
- **子系统主数据（24）**：综合布线、网络、视频、门禁、报警、巡更、BA、照明、能源、停车、会议、信息发布、背景音乐、IPTV、对讲、客控……

交叉关系举例：

- 报价/成本：按子系统拆分（每个子系统一行/一个 Sheet）。
- 点位/图纸：点位必须挂子系统类型（摄像头/门禁/网络/BA）。
- 竣工资料：按子系统出测试报告/验收表。
- 维保：按子系统建设备台账/工单。
- 合同/发票/回款：不按子系统，按项目/合同。

所以完整目录应该是：

```text
管理主线（14）+ 子系统主数据（24）+ 交叉矩阵（报价/点位/成本/竣工/维保按子系统展开）
```

## 这次找到的可复用/不可复用

| 来源 | 平台 | 许可 | 用途 | 结论 |
|---|---|---|---|---|
| [eeops](https://gitee.com/shmilytqq/eeops) | Gitee | 未声明，README 写私有 | 管理模块、18 子系统、报价 Excel 分析、CAD 服务 | 只能读，不能抄 |
| [EEOPS 报价分析](https://gitee.com/shmilytqq/eeops/blob/main/%E5%BC%B1%E7%94%B5%E6%8A%A5%E4%BB%B7Excel%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A.md) | Gitee | 同上 | 18 子系统、报价表结构、汇总结构 | 高价值现场数据 |
| [德立云 18 大系统](https://www.deliyun.com/newsinfo/8795439.html) | Web | 商业文章 | 第二套 18 系统、系统定义 | 可作行业常识，非标准 |
| [MicroCommunityIot](https://gitee.com/bigstar2018/MicroCommunityIot) | Gitee | Apache-2.0 | 门禁/道闸/监控/水电表/梯控/门锁的设备模型 | 可借鉴设备/点位 |
| [idcops](https://gitee.com/decbe/idcops) | Gitee | Apache-2.0 | 机房/机柜/设备/跳线/库存 | 可借鉴设备台账 |
| [easyaiot](https://gitee.com/gsmith/easyaiot) | Gitee | MIT | 摄像头接入/AI 算法平台 | 可借鉴视频接入 |
| [iot_api](https://gitee.com/ttgzs/iot_api) | Gitee | MulanPSL-2.0 | 智慧工地/人员/安全/进度 | README 营销味重，证据低 |
| [smart-system-costing](https://github.com/wanglizuishuai-arch/smart-system-costing) | GitHub | MIT | 容量公式/清单计价/取费/毛利 | 可直接借鉴 |
| [Project-Management-System](https://github.com/fanzhuangzhuang000-svg/Project-Management-System) | GitHub | 专有 | 管理主线/UI 令牌 | 只能读 |
| [BidCraft](https://github.com/yaoyongli1974-dotcom/BidCraft) | GitHub | 专有 | 事实台账/弱电 YAML/核对规则 | 只能读 |
| [cad-topo-system](https://github.com/FnGas/cad-topo-system) | GitHub | 未声明 | DXF 点位/拓扑 | 只能读 |

## 覆盖度矩阵（这次跑完）

| 目录块 | 覆盖 | 主要证据 |
|---|---|---|
| 项目/合同/变更 | 高 | PMS、myerp、eeops |
| 报价/清单/成本 | 高 | eeops 报价 Excel、smart-system-costing、myerp |
| 发票/收付款/账龄 | 高 | PMS、myerp |
| 采购/材料/库存 | 中高 | PMS、eeops、idcops |
| 施工/进度/现场 | 中 | eeops、iot_api、PinMy |
| 竣工/验收/资料 | 中 | eeops docx、众和 |
| 维保/工单/巡检 | 中高 | PMS、eeops、MicroCommunityIot |
| CAD/点位/拓扑 | 高 | cad-topo、eeops cad-service、PinMy |
| 子系统主数据 | 高（名称层） | eeops、德立云 |
| 子系统技术规格 | 低 | 只有名称/少量参数，缺逐系统技术规格 |
| UI/交互 | 中 | PMS UI 令牌、OpenProject、idcops 截图 |
| 权限/审计/备份 | 中高 | PMS、OpenProject、eeops |
| 真实角色/权限矩阵 | 低 | 无公开资料 |
| 真实报价原文件 | 低 | 只有分析报告，没有 4 份原始 Excel |

## 这次雷达的真实进步

- 第一次：只有 GitHub，14 个管理模块，漏掉 18 子系统。
- 第二次：补 Gitee，找到两套 18，形成 24 个子系统并集；管理模块 + 子系统双层目录。
- 覆盖度从“管理主线约 60%”提升到“管理主线 + 子系统名称约 80%”；但子系统技术规格、角色矩阵、原始报价文件仍然低。

## 仍然没解决

- Gitee 的 `/search/repositories` API 返回 0（可能需要 token/索引），这次靠 `site:gitee.com` 网页搜索绕过；这是 adapter 的缺口。
- 没有拿到 4 份原始报价 Excel，只能读分析报告。
- 没有权威标准；24 个是并集，不是标准。
- 没有真实用户访谈/权限矩阵。
- UI 只到令牌/截图，没到高保真。
- 最贴合的几个来源是专有许可，只能重写。

## 判断

新雷达的方向是对的：**多平台 + 按证据物搜 + 双层目录 + 覆盖度矩阵**，这次确实把上次漏掉的“18 子系统”捞回来了，而且发现“18 不是标准，是常见桶数”。

但雷达仍然不是全自动：Gitee 搜索接口、原始 Excel、技术规格、角色矩阵，都需要人/agent 继续补。它能保证“不遗漏大类、能解释来源”，不能保证“每个子系统都读到规格”。
