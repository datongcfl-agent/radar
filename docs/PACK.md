# Pack 写法

一个 pack 就是一个行业的地图；**行业结论只放这里，不放引擎**。

## 最小 pack

```json
{
  "schema_version": 1,
  "pack": "example",
  "version": "0.1.0",
  "title": "示例行业",
  "aliases": ["别名"],
  "modules": [
    {"id": "M01", "name": "模块", "artifacts": ["证据物"], "keywords": ["关键词"]}
  ],
  "subsystems": [
    {"id": "S01", "name": "子系统", "artifacts": ["证据物"], "keywords": ["关键词"]}
  ],
  "source_map": {"github": ["查询"], "web": ["查询"]},
  "query_templates": ["{industry} {module} 需求"]
}
```

## 规则

- `modules` id 用 `M01`…；`subsystems` id 用 `S01`…；不能重复；
- 每个模块/子系统至少有 1 个 `artifact` 和 1 个 `keyword`；
- `keywords` 用于 GitHub 结果自动映射覆盖；
- `source_map` 只是建议查询，不是硬编码；
- `query_templates` 用于 `gaps.md` 的下一轮建议。

## 种子来源

```json
{
  "id": "SRC-001",
  "platform": "github|gitee|web|docs|npm|pypi|maven|tender",
  "url": "https://...",
  "title": "...",
  "artifact_type": "code|readme|docs|prd|quote_sheet|subsystem_list|ui_reference|manual|benchmark|article",
  "access_status": "public|api_limited|login_required|paywalled|blocked|deleted|proprietary|unreachable",
  "license": "MIT|Apache-2.0|proprietary|unknown",
  "license_status": "clear|needs_review|proprietary",
  "evidence_level": "marketing|metadata|readme|docs|real_artifact|code_tests|production",
  "covers": ["M01", "S01"],
  "quotes": ["真正读到的原文"],
  "status": "selected|rejected|needs_review",
  "why_selected": "..."
}
```

`covers` 必须引用 pack 里存在的 id；`quotes` 为空会让来源最多算 `mention`。

## 换行业

复制一个 pack，改模块/子系统/关键词/来源地图；引擎代码不动。`packs/pet-hospital` 就是最小示例。


## 最小种子字段（现状 vs 目标）

当前 `v0.1` 校验要求 12 个字段（`id/platform/url/title/artifact_type/access_status/license/license_status/evidence_level/covers/status/why_selected`）。

`v0.2` 目标是最小 6 个字段就能录入：

```text
id / url / evidence_level / covers / quotes / status
```

其余由 adapter 补默认值（platform、title、artifact_type、access_status、license 等），避免“账本录入太贵 → 人懒得记 → 退回聊天记录”。
