# 覆盖度明细

| 层级 | 数量 |
| --- | ---: |
| none | 0 |
| mention | 15 |
| evidence | 11 |
| strong | 0 |

## 管理模块

### M01 资产与容量 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `DC-009` | github | evidence | NOASSERTION | public |
| `VND-SUNBIRD` | web | mention | unknown | public |
| `VND-NLYTE` | web | mention | unknown | public |
| `VND-DEVICE42` | web | mention | unknown | public |
| `VND-OCP` | web | mention | unknown | public |
| `VND-DCMAP` | web | mention | unknown | public |
| `DC-011` | github | evidence | Apache-2.0 | public |
| `DC-012` | github | evidence | unknown | public |

### M02 供配电 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `DC-006` | github | evidence | NOASSERTION | public |
| `VND-SCHNEIDER` | web | mention | unknown | public |
| `VND-EATON` | web | mention | unknown | public |
| `VND-RARITAN` | web | mention | unknown | public |
| `VND-CUMMINS` | web | mention | unknown | public |

### M03 制冷与环境 — mention

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `VND-VERTIV` | web | mention | unknown | public |
| `VND-SCHNEIDER` | web | mention | unknown | public |
| `VND-OCP` | web | mention | unknown | public |

### M04 监控与告警 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `DC-001` | github | evidence | Apache-2.0 | public |
| `DC-002` | github | evidence | AGPL-3.0 | public |
| `DC-003` | github | evidence | NOASSERTION | public |
| `DC-004` | github | evidence | Apache-2.0 | public |
| `DC-005` | github | evidence | GPL-3.0 | public |
| `DC-007` | github | evidence | MIT | public |
| `DC-008` | github | evidence | NOASSERTION | public |
| `DC-009` | github | evidence | NOASSERTION | public |
| `DC-015` | github | evidence | Apache-2.0 | public |

### M05 消防与安全 — mention

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `VND-DCD` | web | mention | unknown | public |
| `VND-DCK` | web | mention | unknown | public |
| `VND-SIEMENS` | web | mention | unknown | public |
| `VND-HID` | web | mention | unknown | public |
| `VND-AXIS` | web | mention | unknown | public |

### M06 巡检与工单 — mention

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `VND-DCD` | web | mention | unknown | public |
| `VND-DCK` | web | mention | unknown | public |
| `VND-DCF` | web | mention | unknown | public |
| `VND-IBM-MAXIMO` | web | mention | unknown | public |

### M07 能效与PUE — mention

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `VND-GREENGRID` | web | mention | unknown | public |

### M08 容量规划与报表 — mention

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `VND-SUNBIRD` | web | mention | unknown | public |
| `VND-NLYTE` | web | mention | unknown | public |
| `VND-DEVICE42` | web | mention | unknown | public |
| `VND-DCMAP` | web | mention | unknown | public |

### M09 合规与标准 — mention

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `BASE-STD` | docs | mention | unknown | public |
| `BASE-TENDER` | docs | mention | unknown | public |
| `BASE-CORP` | docs | mention | unknown | public |
| `BASE-STAT` | docs | mention | unknown | public |
| `BASE-REPORT` | docs | mention | unknown | public |
| `VND-UPTIME` | web | mention | unknown | public |
| `VND-TIA` | web | mention | unknown | public |

### M10 集成与自动化 — evidence

| 来源 | 平台 | 等级 | 许可 | 访问 |
| --- | --- | --- | --- | --- |
| `DC-010` | github | evidence | GPL-3.0 | public |

## 子系统

- **S01 机柜/U位** — evidence（2 个来源）
- **S02 配电/列头柜** — mention（1 个来源）
- **S03 UPS/电池** — evidence（2 个来源）
- **S04 柴发** — mention（1 个来源）
- **S05 精密空调** — mention（1 个来源）
- **S06 温湿度/漏水** — mention（1 个来源）
- **S07 消防联动** — mention（1 个来源）
- **S08 门禁** — mention（1 个来源）
- **S09 视频监控** — evidence（2 个来源）
- **S10 动环监控** — evidence（7 个来源）
- **S11 告警/工单** — evidence（1 个来源）
- **S12 巡检** — mention（1 个来源）
- **S13 能效/PUE** — mention（1 个来源）
- **S14 容量规划** — mention（3 个来源）
- **S15 资产/维保** — evidence（1 个来源）
- **S16 API/集成** — evidence（2 个来源）

## 同源待印证

这些模块有 ≥2 条证据，但来自同一 host；不能当独立互证。

- `M01` 资产与容量（独立 host 1）
- `M04` 监控与告警（独立 host 1）
- `S10` 动环监控（独立 host 1）
- `S16` API/集成（独立 host 1）
