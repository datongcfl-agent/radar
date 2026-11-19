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
from .model import RadarError, load_pack, load_seeds, merge_sources, sha256_file
from .report import write_run


def _now():
    return datetime.now().astimezone()


def cmd_run(args):
    pack = load_pack(args.pack)
    seeds = load_seeds(args.seeds, pack)
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
        "options": {"github": bool(args.github), "limit": args.limit,
                    "max_queries": args.max_queries},
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
    seeds = load_seeds(args.seeds, pack)
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


def cmd_diff(args):
    text = diff_runs(args.old, args.new, out=args.out)
    return {"old": args.old, "new": args.new, "out": args.out, "bytes": len(text)}


def build_parser():
    p = argparse.ArgumentParser(prog="radar", description="最小行业雷达：pack + 来源账本 + 覆盖度")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("run", help="跑一次雷达")
    r.add_argument("--pack", required=True)
    r.add_argument("--seeds", required=True)
    r.add_argument("--title", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--github", action="store_true", help="可选：加 GitHub 搜索")
    r.add_argument("--limit", type=int, default=3)
    r.add_argument("--max-queries", type=int, default=3)
    r.set_defaults(func=cmd_run)

    v = sub.add_parser("validate", help="只校验 pack/seeds")
    v.add_argument("--pack", required=True)
    v.add_argument("--seeds", required=True)
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
