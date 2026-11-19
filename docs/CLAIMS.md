# Claim 账本（v0.4）

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
| 存在矛盾 | 上限 0.40，状态 `contested` |

`high >= 0.75`，`medium >= 0.50`，其余 `low`。  
`reasons` 会写 `single_source` / `no_quote` / `contradiction` / `proprietary_reference`。

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
