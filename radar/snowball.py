"""Forward snowballing (v0.2.4): who forked a selected GitHub source.

This is intentionally minimal: forks are a public "who derived from it" signal.
Dependents / citation graphs can be added later without changing the record model.
"""
from __future__ import annotations

import urllib.parse
from urllib.parse import urlsplit

from .adapters import CLEAR_LICENSES, _curl_json


def parse_github_repo(url):
    parts = urlsplit(url)
    if not (parts.hostname or "").endswith("github.com"):
        return None
    path = [p for p in parts.path.split("/") if p]
    if len(path) < 2:
        return None
    return "%s/%s" % (path[0], path[1].replace(".git", ""))


def github_forks(repo, token=None, limit=3):
    url = ("https://api.github.com/repos/%s/forks?per_page=%d"
           % (repo, max(1, min(limit, 10))))
    data, err = _curl_json(url, token)
    if err:
        return [], "GitHub forks 查询失败: %s" % err
    if isinstance(data, dict):
        return [], "GitHub forks 返回异常: %s" % str(data.get("message") or data)[:160]
    if not isinstance(data, list):
        return [], "GitHub forks 返回异常"
    return data, None


def fork_source(fork, parent, idx):
    covers = parent.get("covers") or []
    if not covers:
        return None
    lic = (fork.get("license") or {}).get("spdx_id") or "unknown"
    return {
        "id": "SF-%03d" % idx,
        "platform": "github",
        "url": fork.get("html_url", ""),
        "title": fork.get("full_name", ""),
        "artifact_type": "code",
        "language": fork.get("language") or "unknown",
        "retrieved_at": fork.get("updated_at"),
        "http_status": 200,
        "access_status": "public",
        "license": lic,
        "license_status": "clear" if lic in CLEAR_LICENSES else "needs_review",
        "evidence_level": "metadata",
        "derived_from_real_data": False,
        "stars": fork.get("stargazers_count"),
        "covers": list(covers),
        "borrow_scope": ["workflow"],
        "quotes": [],
        "limitations": "forward snowballing: 仅 fork metadata，未读正文/代码",
        "status": "needs_review",
        "why_selected": "forward: fork of %s" % parent.get("id"),
    }


def snowball(sources, pack, token=None, per_source=2, max_sources=5):
    out, warnings = [], []
    seen = {s.get("url") for s in sources}
    idx = 0
    for parent in sources:
        if len(out) >= max_sources:
            break
        if parent.get("platform") != "github" or parent.get("status") == "rejected":
            continue
        repo = parse_github_repo(parent.get("url", ""))
        if not repo:
            continue
        forks, warn = github_forks(repo, token=token, limit=per_source)
        if warn:
            warnings.append("%s: %s" % (parent.get("id"), warn))
            continue
        for fork in forks[:per_source]:
            if len(out) >= max_sources:
                break
            url = fork.get("html_url")
            if not url or url in seen:
                continue
            item = fork_source(fork, parent, idx + 1)
            if not item:
                continue
            idx += 1
            out.append(item)
            seen.add(url)
    return out, warnings
