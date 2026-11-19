"""Two-run diff: coverage changes + source adds/removals."""
from __future__ import annotations

import json
from pathlib import Path

from .model import LEVELS


def _load(run):
    run = Path(run)
    cov = json.loads((run / "coverage.json").read_text(encoding="utf-8"))
    srcs = [json.loads(line) for line in (run / "sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    state_path = run / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    return cov, srcs, state


def _rows(cov):
    return {r["id"]: r for r in cov["modules"] + cov["subsystems"]}


def diff_runs(old, new, out=None):
    old_cov, old_src, old_state = _load(old)
    new_cov, new_src, new_state = _load(new)
    same_pack = old_state.get("pack") == new_state.get("pack")
    old_rows, new_rows = _rows(old_cov), _rows(new_cov)
    old_map = {s.get("url"): s.get("id") for s in old_src}
    new_map = {s.get("url"): s.get("id") for s in new_src}
    old_urls = set(old_map)
    new_urls = set(new_map)
    lines = ["# 雷达 Diff", "",
             "旧：`%s` → 新：`%s`" % (old, new), ""]
    if not same_pack:
        lines.extend(["> **不同 pack**：`%s` → `%s`。不比较覆盖变化，只列来源变化。" % (
            old_state.get("pack"), new_state.get("pack")), ""])
    lines.extend(["## 覆盖变化", "",
                  "| ID | 名称 | 旧 | 新 |", "| --- | --- | --- | --- |"])
    changes = 0
    for rid in sorted(set(old_rows) | set(new_rows)) if same_pack else []:
        a = old_rows.get(rid, {}).get("level", "none")
        b = new_rows.get(rid, {}).get("level", "none")
        if LEVELS.get(a, 0) != LEVELS.get(b, 0):
            changes += 1
            name = (new_rows.get(rid) or old_rows.get(rid) or {}).get("name", "")
            lines.append("| `%s` | %s | %s | %s |" % (rid, name, a, b))
    if not changes:
        lines.append("| — | 无变化/不比较 | — | — |")
    lines.extend(["", "## 新增来源", ""])
    added = [(u, new_map.get(u)) for u in sorted(new_urls - old_urls) if u]
    lines.extend(["- `%s` %s" % (sid, u) for u, sid in added] or ["- 无"])
    lines.extend(["", "## 移除来源", ""])
    removed = [(u, old_map.get(u)) for u in sorted(old_urls - new_urls) if u]
    lines.extend(["- `%s` %s" % (sid, u) for u, sid in removed] or ["- 无"])
    lines.extend(["", "## 汇总", "",
                  "- 覆盖变化：%d 个模块/子系统" % changes,
                  "- 新增来源：%d" % len(added),
                  "- 移除来源：%d" % len(removed), ""])
    text = "\n".join(lines)
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return text
