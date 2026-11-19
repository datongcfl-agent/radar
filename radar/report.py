"""Markdown/JSONL writers for a radar run."""
from __future__ import annotations

import json
from pathlib import Path

from .coverage import gap_rows
from .model import level_for_source, write_json


def _md(text):
    return str(text or "").replace("|", "\\|")


def _source_row(s):
    lic = s.get("license", "unknown")
    if s.get("license_status") == "proprietary":
        lic += "（不可复用）"
    elif s.get("license_status") == "needs_review":
        lic += "（需复核）"
    return "| `%s` | [%s](%s) | %s | %s | %s | %s |" % (
        s["id"], _md(s["title"]), s["url"], s.get("platform", ""),
        level_for_source(s), lic, s.get("access_status", ""),
    )


def render_toc(pack, coverage):
    lines = [
        "# %s · 雷达目录" % pack["title"],
        "",
        "Pack: `%s` v%s" % (pack["pack"], pack.get("version", "")),
        "",
        "## 管理模块",
        "",
        "| ID | 模块 | 覆盖 | 来源数 | 最强来源 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in coverage["modules"]:
        single = "（单源）" if row.get("single_source") else ""
        lines.append("| `%s` | %s | **%s**%s | %d | %s |" % (
            row["id"], _md(row["name"]), row["level"], single, row["source_count"],
            row["strongest"] or "—"))
    lines.extend(["", "## 子系统", "",
                  "| ID | 子系统 | 覆盖 | 来源数 | 最强来源 |",
                  "| --- | --- | --- | ---: | --- |"])
    for row in coverage["subsystems"]:
        single = "（单源）" if row.get("single_source") else ""
        lines.append("| `%s` | %s | **%s**%s | %d | %s |" % (
            row["id"], _md(row["name"]), row["level"], single, row["source_count"],
            row["strongest"] or "—"))
    lines.extend(["", "## 怎么读", "",
                  "- `strong`：有一手证据/可验证数据；`evidence`：文档/README 有流程或字段；",
                  "- `mention`：只提到名字；`none`：没有来源；",
                  "- 覆盖度不是质量排名，它只说明“这块有没有证据、下一步该补什么”。", ""])
    return "\n".join(lines)


def render_coverage(pack, sources, coverage):
    smap = {s["id"]: s for s in sources}
    lines = ["# 覆盖度明细", "",
             "| 层级 | 数量 |", "| --- | ---: |"]
    for k, v in coverage["summary"].items():
        lines.append("| %s | %d |" % (k, v))
    lines.extend(["", "## 管理模块", ""])
    for row in coverage["modules"]:
        lines.append("### %s %s — %s" % (row["id"], row["name"], row["level"]))
        lines.append("")
        if not row["sources"]:
            lines.append("没有来源。")
        else:
            lines.append("| 来源 | 平台 | 等级 | 许可 | 访问 |")
            lines.append("| --- | --- | --- | --- | --- |")
            for sid in row["sources"]:
                s = smap[sid]
                lines.append("| `%s` | %s | %s | %s | %s |" % (
                    sid, s["platform"], level_for_source(s),
                    s.get("license", ""), s.get("access_status", "")))
        lines.append("")
    lines.extend(["## 子系统", ""])
    for row in coverage["subsystems"]:
        lines.append("- **%s %s** — %s（%d 个来源）" % (
            row["id"], row["name"], row["level"], row["source_count"]))
    lines.append("")
    return "\n".join(lines)


def render_gaps(pack, coverage):
    gaps = gap_rows(coverage, "evidence")
    single = [r for r in coverage["modules"] + coverage["subsystems"] if r.get("single_source")]
    lines = ["# 缺口清单", "",
             "## 没有证据的模块", ""]
    if not gaps:
        lines.append("没有缺口：所有模块至少有 `evidence` 级来源。")
    for row in gaps:
        lines.append("## %s %s — %s" % (row["id"], row["name"], row["level"]))
        lines.append("")
        lines.append("下一轮查询建议：")
        for tpl in pack.get("query_templates", []):
            try:
                q = tpl.format(module=row["name"], artifact=", ".join(
                    next((x["artifacts"] for x in pack["modules"] + pack["subsystems"]
                          if x["id"] == row["id"]), ["资料"])), industry=pack["title"],
                    subsystem=row["name"], platform="github")
            except Exception:
                q = tpl
            lines.append("- `%s`" % q)
        lines.append("")
    lines.extend(["", "## 单源待印证", "",
                  "这些模块只有 1 个来源；按单源规则，最高只能算 `evidence`，需要第二源。", ""])
    if single:
        for row in single:
            lines.append("- `%s` %s（%s，来源 `%s`）" % (
                row["id"], row["name"], row["level"], ", ".join(row["sources"])))
    else:
        lines.append("- 无")
    lines.append("")
    return "\n".join(lines)


def render_report(pack, sources, coverage, state):
    low = [s for s in sources if isinstance(s.get("stars"), int) and s["stars"] <= 10]
    issues = [s for s in sources if s.get("access_status") != "public"
              or s.get("license_status") != "clear"]
    lines = [
        "# %s · 雷达运行报告" % state.get("title", pack["title"]),
        "",
        "Run: `%s` · Pack: `%s` v%s" % (
            state.get("run_id", ""), pack["pack"], pack.get("version", "")),
        "",
        "## 一句话",
        "",
        "本次用 %d 条来源，覆盖 %d 个管理模块 + %d 个子系统；强/证据/提及/空 = %d/%d/%d/%d。" % (
            len(sources), len(coverage["modules"]), len(coverage["subsystems"]),
            coverage["summary"]["strong"], coverage["summary"]["evidence"],
            coverage["summary"]["mention"], coverage["summary"]["none"]),
        "",
        "## 平台覆盖",
        "",
        "| 平台 | 来源数 |",
        "| --- | ---: |",
    ]
    for p, n in sorted(coverage["platforms"].items()):
        lines.append("| %s | %d |" % (p, n))
    lines.extend(["", "## 低星但相关的发现", ""])
    if low:
        for s in low:
            lines.append("- `%s` [%s](%s) — %d★，%s" % (
                s["id"], _md(s["title"]), s["url"], s["stars"], s.get("why_selected", "")))
    else:
        lines.append("- 本次没有 stars ≤ 10 的来源；这不代表没有低星好资料。")
    lines.extend(["", "## 访问/许可需要注意", ""])
    if issues:
        for s in issues:
            lines.append("- `%s` access=%s, license_status=%s：%s" % (
                s["id"], s.get("access_status"), s.get("license_status"),
                s.get("limitations", "") or "需人工复核"))
    else:
        lines.append("- 本次来源均为 public + clear。")
    singles = [r for r in coverage["modules"] + coverage["subsystems"] if r.get("single_source")]
    lines.extend(["", "## 单源模块", ""])
    if singles:
        for r in singles:
            lines.append("- `%s` %s（%s）" % (r["id"], r["name"], r["level"]))
    else:
        lines.append("- 无")
    lines.extend(["", "## 来源清单", "",
                  "| ID | 标题 | 平台 | 等级 | 许可 | 访问 |",
                  "| --- | --- | --- | --- | --- | --- |"])
    for s in sources:
        lines.append(_source_row(s))
    lines.extend(["", "## 边界", "",
                  "- 大多数来源只到 metadata/readme/docs，不等于代码已验证；",
                  "- 专有来源只进参考池，不进可复用池；",
                  "- 覆盖度不是完整性证明，只是“有没有证据”的导航。", ""])
    return "\n".join(lines)


def write_run(out_dir, pack, sources, coverage, state):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "sources.jsonl").open("w", encoding="utf-8") as fh:
        for s in sources:
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")
    write_json(out / "coverage.json", coverage)
    write_json(out / "state.json", state)
    (out / "toc.md").write_text(render_toc(pack, coverage), encoding="utf-8")
    (out / "coverage.md").write_text(render_coverage(pack, sources, coverage), encoding="utf-8")
    (out / "gaps.md").write_text(render_gaps(pack, coverage), encoding="utf-8")
    (out / "report.md").write_text(render_report(pack, sources, coverage, state), encoding="utf-8")
