# 数据中心动环/DCIM · 雷达目录

Pack: `data-center-ops` v0.1.0

## 管理模块

| ID | 模块 | 覆盖 | 来源数 | 最强来源 |
| --- | --- | --- | ---: | --- |
| `M01` | 资产与容量 | **evidence** | 7 | DC-012 |
| `M02` | 供配电 | **evidence** | 5 | VND-RARITAN |
| `M03` | 制冷与环境 | **evidence**（单源） | 4 | VND-SUNBIRD |
| `M04` | 监控与告警 | **evidence** | 9 | DC-015 |
| `M05` | 消防与安全 | **evidence**（单源） | 5 | VND-SIEMENS |
| `M06` | 巡检与工单 | **evidence**（单源） | 4 | VND-IBM-MAXIMO |
| `M07` | 能效与PUE | **evidence**（单源） | 1 | VND-GREENGRID |
| `M08` | 容量规划与报表 | **mention** | 3 | VND-NLYTE |
| `M09` | 合规与标准 | **mention** | 7 | VND-UPTIME |
| `M10` | 集成与自动化 | **evidence**（单源） | 1 | DC-010 |

## 子系统

| ID | 子系统 | 覆盖 | 来源数 | 最强来源 |
| --- | --- | --- | ---: | --- |
| `S01` | 机柜/U位 | **evidence**（单源） | 2 | DC-011 |
| `S02` | 配电/列头柜 | **evidence**（单源） | 1 | VND-RARITAN |
| `S03` | UPS/电池 | **evidence**（单源） | 2 | DC-006 |
| `S04` | 柴发 | **mention** | 1 | VND-GENERAC |
| `S05` | 精密空调 | **mention** | 1 | VND-VERTIV |
| `S06` | 温湿度/漏水 | **evidence**（单源） | 2 | VND-SUNBIRD |
| `S07` | 消防联动 | **evidence**（单源） | 1 | VND-SIEMENS |
| `S08` | 门禁 | **mention** | 1 | VND-HID |
| `S09` | 视频监控 | **evidence**（单源） | 2 | DC-014 |
| `S10` | 动环监控 | **evidence** | 7 | DC-008 |
| `S11` | 告警/工单 | **evidence**（单源） | 1 | DC-015 |
| `S12` | 巡检 | **evidence**（单源） | 1 | VND-IBM-MAXIMO |
| `S13` | 能效/PUE | **evidence**（单源） | 1 | VND-GREENGRID |
| `S14` | 容量规划 | **mention** | 2 | VND-NLYTE |
| `S15` | 资产/维保 | **evidence**（单源） | 1 | DC-012 |
| `S16` | API/集成 | **evidence** | 2 | DC-010 |

## 怎么读

- `strong`：有一手证据/可验证数据；`evidence`：文档/README 有流程或字段；
- `mention`：只提到名字；`none`：没有来源；
- 覆盖度不是质量排名，它只说明“这块有没有证据、下一步该补什么”。
