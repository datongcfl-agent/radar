#!/usr/bin/env python3
"""Audit ledger trust: wide covers, short quotes, and strong support."""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
pack = json.loads((ROOT / "packs/weak-current/pack.json").read_text(encoding="utf-8"))
seeds = json.loads((ROOT / "seeds/weak-current.json").read_text(encoding="utf-8"))["sources"]
units = {x["id"]: x["name"] for x in pack["modules"] + pack["subsystems"]}
support = defaultdict(list)
for s in seeds:
    for cid in s.get("covers", []):
        support[cid].append(s)

wide = [s for s in seeds if len(s.get("covers", [])) >= 5]
wide_only = [uid for uid in units if support[uid] and all(len(s["covers"]) >= 5 for s in support[uid])]
short = [s for s in seeds if any(0 < len(q) < 40 for q in (s.get("quotes") or []))]
no_quote = [s for s in seeds if not (s.get("quotes") or [])]
print("sources=%d units=%d" % (len(seeds), len(units)))
print("wide_covers>=5: %s" % ([s["id"] for s in wide] or "none"))
print("units_only_wide: %s" % (wide_only or "none"))
print("short_quotes<40: %s" % ([s["id"] for s in short] or "none"))
print("no_quote (mention-ok): %s" % ([s["id"] for s in no_quote] or "none"))

state_path = ROOT / "runs/weak-current-demo/state.json"
if state_path.exists():
    state = json.loads(state_path.read_text(encoding="utf-8"))
    import hashlib
    seed_hash = hashlib.sha256((ROOT / "seeds/weak-current.json").read_bytes()).hexdigest()
    pack_hash = hashlib.sha256((ROOT / "packs/weak-current/pack.json").read_bytes()).hexdigest()
    hash_ok = state.get("seeds_sha256") == seed_hash and state.get("pack_sha256") == pack_hash
    print("state_hashes: %s" % ("OK" if hash_ok else "MISMATCH"))
else:
    hash_ok = True
    print("state_hashes: no sample run")

if wide or wide_only or short or not hash_ok:
    sys.exit(1)
print("audit: PASS")
