# Claim 账本（v1.3）

## 输入

```json
{
  "schema_version": 1,
  "pack": "weak-current",
  "claims": [
    {
      "id": "C001",
      "statement": "一句可核对的主张",
      "covers": ["M01"],
      "sources": ["SRC-001", "SRC-003"],
      "contradicts": []
    }
  ]
}
```

- `sources` 必须是已有 run 的 `sources.jsonl` 里的 ID；
- `covers` 必须是 pack 里的模块/子系统 ID；
- `contradicts` 填其他 claim ID，不能指向自己。

## 置信度

| 条件 | 数值 |
| --- | ---: |
| best level = strong | 0.80 |
| best level = evidence | 0.60 |
| best level = mention / none | 0.30 / 0.00 |
| 单源或同一 host | 上限 0.55 |
| 没有任何来源有 quote | 上限 0.40 |
| claim.covers 与被引来源 covers 交集为空 | 上限 0.30，reason `unsupported_by_sources` |
| 被引来源没有 web 验证通过 | 上限 0.40，reason `no_verified_source` |
| claim.covers 与已验证来源 covers 交集为空 | 上限 0.30，reason `unsupported_by_verified_sources` |
| 存在矛盾 | 上限 0.40，状态 `contested`，双向标记 |

`high >= 0.75`，`medium >= 0.50`，其余 `low`。  
`reasons` 会写 `single_source` / `no_quote` / `unsupported_by_sources` / `no_verified_source` / `unsupported_by_verified_sources` / `contradiction` / `proprietary_reference`。

- `no_verified_source` 的 `next_action` 是「先跑 --verify-quotes」；
- `unsupported_by_verified_sources` 的 `next_action` 是「换已验证来源或改主张」；
- `unsupported_by_sources` 的 `next_action` 是「换来源或改主张」；
- 矛盾双向标记：A 指向 B 时，A/B 都变 `contested`；`claims.json` 保留 `declared_contradicts` 方便追溯原始声明；
- `proprietary_reference` 的 `next_action` 是「换可复用来源或人工复核许可」；
- `review.csv` 对以 `= + - @` 开头的字段加前导 `'`，避免 Excel 公式注入。

## 输出

```bash
python3 -m radar claims --pack packs/weak-current/pack.json \
  --run runs/weak-current-demo --claims examples/claims.weak-current.json \
  --out runs/claims-demo
```

- `claims.md`：人读；
- `claims.json`：机器读；
- `review.csv`：`next_action` 列（找第二来源/补 quote/复核矛盾/可进入需求底稿）。

## 边界

- 这是**规则账本**，不是 LLM 自动判定；
- 置信度是启发式，不是统计概率；
- claim 由人或 agent 写，引擎不自动生成主张；
- 单源上限仍生效，不会因为 claim 写得肯定就变高。
