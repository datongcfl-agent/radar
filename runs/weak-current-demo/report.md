# 弱电管理系统 · 雷达运行报告

Run: `20261119-210619` · Pack: `weak-current` v0.1.0

## 一句话

本次用 13 条来源，覆盖 14 个管理模块 + 24 个子系统；强/证据/提及/空 = 25/13/0/0。

## 平台覆盖

| 平台 | 来源数 |
| --- | ---: |
| docs | 1 |
| gitee | 3 |
| github | 5 |
| web | 4 |

## 低星但相关的发现

- `SRC-001` [EEOPS 弱电工程运营管理系统](https://gitee.com/shmilytqq/eeops) — 1★，管理主线 + 18 子系统 + 报价 Excel 分析，最贴近弱电；但只能读，不能抄。
- `SRC-003` [弱电智能化工程项目管理系统（PMS）](https://github.com/fanzhuangzhuang000-svg/Project-Management-System) — 0★，0 星但业务主线最完整，含实际成本/动态毛利/发票勾稽/UI 令牌。
- `SRC-004` [BidCraft 弱电投标文件编制系统](https://github.com/yaoyongli1974-dotcom/BidCraft) — 0★，事实台账 + 行业规则包 + 生成门禁，是证据/许可约束的最好参考。
- `SRC-005` [smart-system-costing 智能化项目估算](https://github.com/wanglizuishuai-arch/smart-system-costing) — 0★，MIT，容量/清单/取费/毛利公式可直接借鉴；0 星但对口。
- `SRC-006` [CAD 弱电点位与网络拓扑存档系统](https://github.com/FnGas/cad-topo-system) — 1★，CAD 点位/拓扑/DXF 回导，正好补 M03 的交互与数据模型。
- `SRC-007` [myerp 弱电/安防工程商业务管理](https://github.com/kaier0922/myerp) — 4★，MIT，报价→合同→应收→项目成本主线，可交叉验证 PMS。
- `SRC-009` [HC 物联网系统（社区/园区设备）](https://gitee.com/bigstar2018/MicroCommunityIot) — 0★，Apache-2.0，设备模型/点位授权/道闸监控，补 S05/S06/S13/S17。

## 访问/许可需要注意

- `SRC-001` access=public, license_status=proprietary：Gitee 未声明许可证，README 写私有；18 个子系统来自 4 份酒店报价，不是行业标准；未验证代码与 README 是否一致。
- `SRC-002` access=public, license_status=proprietary：厂商文章，不是标准；第二套 18 与 EEOPS 只有约 12 个重叠，说明 18 是常见桶数，不是固定清单。
- `SRC-003` access=public, license_status=proprietary：专有许可，禁止复制/修改/分发；README 是产品说明，不是独立验证；0 星。
- `SRC-004` access=public, license_status=proprietary：专有许可；偏投标文件，不是项目管理全流程；不能抄代码/文档。
- `SRC-006` access=public, license_status=needs_review：未声明许可证；只支持 DXF，不是 DWG；无版本/审计。
- `SRC-008` access=public, license_status=needs_review：通用项目管理，不是弱电专用；GPL 需注意分发。
- `SRC-011` access=public, license_status=proprietary：商业闭源产品博客，不是独立评测；不能抄实现。
- `SRC-012` access=public, license_status=proprietary：厂商营销文章，不是规格；不能抄。
- `SRC-013` access=public, license_status=proprietary：厂商官方页，产品视角；深度手册可能需登录；不代表行业通用。

## 单源模块

- `S03` 综合管路（evidence）
- `S08` 周界防范（evidence）
- `S11` 环境监控（evidence）
- `S16` IPTV（evidence）
- `S18` 停车场（evidence）
- `S20` 背景音乐（evidence）
- `S21` 五方对讲（evidence）
- `S22` 客控系统（evidence）
- `S23` 公区温控联网（evidence）
- `S24` 智能厨房排油烟（evidence）

## 来源清单

| ID | 标题 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- | --- |
| `SRC-001` | [EEOPS 弱电工程运营管理系统](https://gitee.com/shmilytqq/eeops) | gitee | strong | proprietary（不可复用） | public |
| `SRC-002` | [德立云：18 大系统构建智能世界](https://www.deliyun.com/newsinfo/8795439.html) | web | evidence | proprietary（不可复用） | public |
| `SRC-003` | [弱电智能化工程项目管理系统（PMS）](https://github.com/fanzhuangzhuang000-svg/Project-Management-System) | github | evidence | proprietary（不可复用） | public |
| `SRC-004` | [BidCraft 弱电投标文件编制系统](https://github.com/yaoyongli1974-dotcom/BidCraft) | github | evidence | proprietary（不可复用） | public |
| `SRC-005` | [smart-system-costing 智能化项目估算](https://github.com/wanglizuishuai-arch/smart-system-costing) | github | evidence | MIT | public |
| `SRC-006` | [CAD 弱电点位与网络拓扑存档系统](https://github.com/FnGas/cad-topo-system) | github | evidence | unknown（需复核） | public |
| `SRC-007` | [myerp 弱电/安防工程商业务管理](https://github.com/kaier0922/myerp) | github | evidence | MIT | public |
| `SRC-008` | [OpenProject 项目管理](https://www.openproject.org/docs/getting-started/openproject-introduction/) | docs | evidence | GPL-3.0（需复核） | public |
| `SRC-009` | [HC 物联网系统（社区/园区设备）](https://gitee.com/bigstar2018/MicroCommunityIot) | gitee | evidence | Apache-2.0 | public |
| `SRC-010` | [idcops 数据中心资源管理](https://gitee.com/decbe/idcops) | gitee | evidence | Apache-2.0 | public |
| `SRC-011` | [PinMy 安装公司图纸钉点](https://pinmy.co/zh/blog/app-for-installers-zh/) | web | evidence | proprietary（不可复用） | public |
| `SRC-012` | [众和：弱电工程信息孤岛](https://www.zhonghesoft.com/xwzx/gcgl/itemid_3590.html) | web | evidence | proprietary（不可复用） | public |
| `SRC-013` | [海康威视 服务支持/工具专区](https://www.hikvision.com/cn/support/) | web | evidence | proprietary（不可复用） | public |

## 边界

- 大多数来源只到 metadata/readme/docs，不等于代码已验证；
- 专有来源只进参考池，不进可复用池；
- 覆盖度不是完整性证明，只是“有没有证据”的导航。
