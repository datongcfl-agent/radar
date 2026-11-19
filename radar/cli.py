"""radar CLI: run / validate / diff."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from .adapters import collect_github
from .coverage import compute_coverage
from .diff import diff_runs
from .model import (RadarError, load_json, load_pack, load_seeds, merge_sources,
                    sha256_file, write_json)
from .report import write_run


def _now():
    return datetime.now().astimezone()


def cmd_run(args):
    pack = load_pack(args.pack)
    seeds = load_seeds(args.seeds, pack, strict=args.strict)
    warnings = []
    sources = list(seeds)
    if args.github:
        got, warns = collect_github(pack, limit_per_query=args.limit,
                                    max_queries=args.max_queries,
                                    token=os.environ.get("GITHUB_TOKEN"))
        sources.extend(got)
        warnings.extend(warns)
    sources = merge_sources(sources)
    coverage = compute_coverage(pack, sources)
    run_id = _now().strftime("%Y%m%d-%H%M%S")
    out = Path(args.out)
    state = {
        "schema_version": 1,
        "run_id": run_id,
        "title": args.title,
        "created_at": _now().isoformat(timespec="seconds"),
        "pack": pack["pack"],
        "pack_version": pack.get("version"),
        "pack_sha256": sha256_file(args.pack),
        "seeds_sha256": sha256_file(args.seeds),
        "mode": "run",
        "base": None,
        "options": {"github": bool(args.github), "limit": args.limit,
                    "max_queries": args.max_queries, "strict": bool(args.strict)},
        "counts": {"sources": len(sources), "modules": len(coverage["modules"]),
                   "subsystems": len(coverage["subsystems"])},
        "warnings": warnings,
    }
    write_run(out, pack, sources, coverage, state)
    return {
        "run": str(out),
        "sources": len(sources),
        "modules": len(coverage["modules"]),
        "subsystems": len(coverage["subsystems"]),
        "summary": coverage["summary"],
        "warnings": warnings,
    }


def cmd_validate(args):
    pack = load_pack(args.pack)
    seeds = load_seeds(args.seeds, pack, strict=args.strict)
    return {
        "pack": pack["pack"],
        "pack_version": pack.get("version"),
        "modules": len(pack["modules"]),
        "subsystems": len(pack["subsystems"]),
        "sources": len(seeds),
        "selected": sum(1 for s in seeds if s["status"] == "selected"),
        "needs_review": sum(1 for s in seeds if s["status"] == "needs_review"),
        "rejected": sum(1 for s in seeds if s["status"] == "rejected"),
    }


def cmd_scan(args):
    result = cmd_run(args)
    out = Path(args.out)
    diff_path = out / "diff.md"
    text = diff_runs(args.base, str(out), out=str(diff_path))
    state = load_json(out / "state.json")
    state["mode"] = "scan"
    state["base"] = args.base
    write_json(out / "state.json", state)
    result["diff"] = str(diff_path)
    result["diff_bytes"] = len(text)
    return result


def cmd_diff(args):
    text = diff_runs(args.old, args.new, out=args.out)
    return {"old": args.old, "new": args.new, "out": args.out, "bytes": len(text)}


def build_parser():
    p = argparse.ArgumentParser(prog="radar", description="最小行业雷达：pack + 来源账本 + 覆盖度")
    sub = p.add_subparsers(dest="command", required=True)

    def add_run_args(p):
        p.add_argument("--pack", required=True)
        p.add_argument("--seeds", required=True)
        p.add_argument("--title", required=True)
        p.add_argument("--out", required=True)
        p.add_argument("--github", action="store_true", help="可选：加 GitHub 搜索")
        p.add_argument("--limit", type=int, default=3)
        p.add_argument("--max-queries", type=int, default=3)
        p.add_argument("--strict", action="store_true", help="要求 v0.1 的完整 12 字段")

    r = sub.add_parser("run", help="跑一次雷达")
    add_run_args(r)
    r.set_defaults(func=cmd_run)

    sc = sub.add_parser("scan", help="增量扫描：新 run + 与 base diff")
    add_run_args(sc)
    sc.add_argument("--base", required=True, help="上一次 run 目录")
    sc.set_defaults(func=cmd_scan)

    v = sub.add_parser("validate", help="只校验 pack/seeds")
    v.add_argument("--pack", required=True)
    v.add_argument("--seeds", required=True)
    v.add_argument("--strict", action="store_true", help="要求 v0.1 的完整 12 字段")
    v.set_defaults(func=cmd_validate)

    d = sub.add_parser("diff", help="比较两次 run")
    d.add_argument("--from", dest="old", required=True)
    d.add_argument("--to", dest="new", required=True)
    d.add_argument("--out", default=None)
    d.set_defaults(func=cmd_diff)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except RadarError as exc:
        print("[fail] %s" % exc, file=sys.stderr)
        return 1
