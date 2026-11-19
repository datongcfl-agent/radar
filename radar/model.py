"""Pack/source loading and validation for the radar MVP."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

LEVELS = {"none": 0, "mention": 1, "evidence": 2, "strong": 3}
LEVEL_NAMES = {v: k for k, v in LEVELS.items()}

PLATFORMS = {"github", "gitee", "npm", "pypi", "maven", "web", "docs", "tender"}
ACCESS = {"public", "api_limited", "login_required", "paywalled", "blocked",
          "deleted", "proprietary", "unreachable"}
LICENSE_STATUS = {"clear", "needs_review", "proprietary"}
EVIDENCE = {"marketing", "metadata", "readme", "docs", "real_artifact",
            "code_tests", "production"}
STATUS = {"selected", "rejected", "needs_review"}
ARTIFACTS = {"code", "readme", "prd", "quote_sheet", "subsystem_list",
             "ui_reference", "manual", "benchmark", "article", "docs"}

TRACKING = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
            "spm", "from", "share_token"}


class RadarError(Exception):
    pass


def load_json(path):
    path = Path(path)
    if not path.exists():
        raise RadarError("文件不存在: %s" % path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RadarError("JSON 解析失败: %s (%s)" % (path, exc)) from exc


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_url(url):
    """Canonicalize for dedup: lowercase host, strip www/fragment/tracking."""
    if not url:
        return ""
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path.rstrip("/") or "/"
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if k.lower() not in TRACKING]
    return urlunsplit((parts.scheme or "https", host, path, urlencode(query), ""))


def _require(cond, msg):
    if not cond:
        raise RadarError(msg)


def load_pack(path):
    data = load_json(path)
    _require(isinstance(data, dict), "pack 顶层必须是对象")
    for key in ("schema_version", "pack", "version", "title", "modules", "subsystems"):
        _require(key in data, "pack 缺少字段 %s" % key)
    _require(data.get("schema_version") == 1, "pack.schema_version 必须是 1")
    _require(str(data.get("pack", "")).strip(), "pack.pack 不能为空")
    _require(str(data.get("title", "")).strip(), "pack.title 不能为空")
    _require(isinstance(data["modules"], list) and data["modules"], "pack.modules 至少 1 条")
    _require(isinstance(data["subsystems"], list) and data["subsystems"], "pack.subsystems 至少 1 条")

    ids = set()
    for kind in ("modules", "subsystems"):
        prefix = "M" if kind == "modules" else "S"
        for i, item in enumerate(data[kind]):
            where = "%s[%d]" % (kind, i)
            _require(isinstance(item, dict), "%s 必须是对象" % where)
            for key in ("id", "name", "artifacts", "keywords"):
                _require(key in item, "%s 缺少 %s" % (where, key))
            _require(re.match(r"^%s\d{2}$" % prefix, str(item["id"])), "%s.id 格式应为 %s01" % (where, prefix))
            _require(item["id"] not in ids, "id 重复: %s" % item["id"])
            ids.add(item["id"])
            _require(str(item["name"]).strip(), "%s.name 不能为空" % where)
            _require(isinstance(item["artifacts"], list) and item["artifacts"], "%s.artifacts 至少 1 条" % where)
            _require(isinstance(item["keywords"], list) and item["keywords"], "%s.keywords 至少 1 条" % where)
    return data


def validate_source(src, pack, index=0):
    where = "sources[%d]" % index
    _require(isinstance(src, dict), "%s 必须是对象" % where)
    for key in ("id", "platform", "url", "title", "artifact_type", "access_status",
                "license", "license_status", "evidence_level", "covers",
                "status", "why_selected"):
        _require(key in src, "%s 缺少字段 %s" % (where, key))
    _require(str(src["id"]).strip(), "%s.id 不能为空" % where)
    _require(src["platform"] in PLATFORMS, "%s.platform 非法: %s" % (where, src["platform"]))
    _require(str(src["url"]).startswith(("http://", "https://")), "%s.url 必须是 http(s)" % where)
    _require(src["artifact_type"] in ARTIFACTS, "%s.artifact_type 非法" % where)
    _require(src["access_status"] in ACCESS, "%s.access_status 非法" % where)
    _require(src["license_status"] in LICENSE_STATUS, "%s.license_status 非法" % where)
    _require(src["evidence_level"] in EVIDENCE, "%s.evidence_level 非法" % where)
    _require(src["status"] in STATUS, "%s.status 非法" % where)
    _require(isinstance(src["covers"], list) and src["covers"], "%s.covers 至少 1 条" % where)
    valid_ids = {m["id"] for m in pack["modules"]} | {s["id"] for s in pack["subsystems"]}
    for cid in src["covers"]:
        _require(cid in valid_ids, "%s.covers 含不存在的 id: %s" % (where, cid))
    if "quotes" in src:
        _require(isinstance(src["quotes"], list), "%s.quotes 必须是数组" % where)
    return src


def load_seeds(path, pack):
    data = load_json(path)
    _require(isinstance(data, dict), "seeds 顶层必须是对象")
    _require(data.get("schema_version") == 1, "seeds.schema_version 必须是 1")
    _require(data.get("pack") in (None, pack["pack"]), "seeds.pack 与 pack 不一致")
    sources = data.get("sources")
    _require(isinstance(sources, list) and sources, "seeds.sources 至少 1 条")
    seen = set()
    for i, src in enumerate(sources):
        validate_source(src, pack, i)
        _require(src["id"] not in seen, "source id 重复: %s" % src["id"])
        seen.add(src["id"])
    return sources


def level_for_source(src):
    if src.get("status") == "rejected":
        return "none"
    has_quote = bool(src.get("quotes"))
    ev = src.get("evidence_level")
    if has_quote and ev in {"real_artifact", "code_tests", "production"}:
        return "strong"
    if has_quote and ev in {"readme", "docs"}:
        return "evidence"
    return "mention"


def merge_sources(sources):
    """Dedup by canonical URL, merge covers/quotes, keep the strongest evidence."""
    by_url = {}
    for src in sources:
        key = canonical_url(src["url"])
        if not key:
            key = src["id"]
        if key not in by_url:
            by_url[key] = dict(src)
            by_url[key]["_merged_from"] = [src["id"]]
            continue
        cur = by_url[key]
        cur["_merged_from"].append(src["id"])
        cur["covers"] = sorted(set(cur.get("covers", [])) | set(src.get("covers", [])))
        cur["quotes"] = list(dict.fromkeys((cur.get("quotes") or []) + (src.get("quotes") or [])))
        if LEVELS[level_for_source(src)] > LEVELS[level_for_source(cur)]:
            keep_merged = cur["_merged_from"]
            cur.update(src)
            cur["_merged_from"] = keep_merged
        if src.get("access_status") == "unreachable":
            cur["access_status"] = "unreachable"
    return list(by_url.values())
