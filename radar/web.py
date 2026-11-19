"""Minimal web extraction + license hints (v0.3), standard library only."""
from __future__ import annotations

import re
import subprocess
from datetime import datetime
from html.parser import HTMLParser


class _Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.desc, self.parts = [], "", []
        self.in_title = False
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = (attrs.get("name") or attrs.get("property") or "").lower()
            if name in {"description", "og:description"} and not self.desc:
                self.desc = attrs.get("content") or ""
        elif tag in {"script", "style", "noscript", "svg"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.skip:
            return
        (self.title if self.in_title else self.parts).append(data.strip())


def _sentences(text):
    parts = re.split(r"(?<=[。！？.!?])\s+", text or "")
    return [p.strip() for p in parts if 20 <= len(p.strip()) <= 240]


def extract_html(html, max_chars=20000):
    parser = _Extractor()
    try:
        parser.feed(html or "")
    except Exception:
        pass
    text = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()[:max_chars]
    quotes = []
    if parser.desc and len(parser.desc) >= 20:
        quotes.append(parser.desc[:240])
    quotes.extend(_sentences(text)[:2])
    return {"title": re.sub(r"\s+", " ", " ".join(parser.title)).strip(),
            "description": parser.desc.strip(), "text": text,
            "quotes": list(dict.fromkeys(quotes))[:3]}


def detect_license(text):
    """Return (license, status, evidence). Conservative: unknown stays needs_review."""
    t = (text or "").lower()
    rules = [
        (r"gnu affero", "AGPL-3.0", "clear"),
        (r"gnu lesser general public", "LGPL-3.0", "clear"),
        (r"gnu general public license.*(version 3|v3)", "GPL-3.0", "clear"),
        (r"gnu general public license.*(version 2|v2)", "GPL-2.0", "clear"),
        (r"apache license|apache-2\.0", "Apache-2.0", "clear"),
        (r"mit license|permission is hereby granted, free of charge", "MIT", "clear"),
        (r"mozilla public license", "MPL-2.0", "clear"),
        (r"(bsd|berkeley).*(3-clause|three-clause)", "BSD-3-Clause", "clear"),
        (r"(bsd|berkeley).*(2-clause|two-clause)", "BSD-2-Clause", "clear"),
        (r"unlicense", "Unlicense", "clear"),
        (r"cc0|creative commons zero", "CC0-1.0", "clear"),
        (r"all rights reserved|版权所有|proprietary", "proprietary", "proprietary"),
    ]
    for pattern, lic, status in rules:
        m = re.search(pattern, t, re.S)
        if m:
            return lic, status, m.group(0)[:80]
    return "unknown", "needs_review", ""


def _now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def apply_web(source, page):
    out = dict(source)
    if page.get("title") and (not out.get("title") or out["title"] == out.get("url")):
        out["title"] = page["title"]
    old = out.get("quotes") or []
    out["quotes"] = list(dict.fromkeys(old + page.get("quotes", [])))[:5]
    out["web_text_chars"] = len(page.get("text", ""))
    out["web_extracted"] = True
    out["last_seen"] = _now()
    out["http_status"] = 200
    out["access_status"] = "public"
    lic, status, evidence = detect_license(" ".join([
        page.get("title", ""), page.get("description", ""), page.get("text", "")]))
    if status == "clear" and out.get("license_status") in (None, "", "unknown", "needs_review"):
        out["license"], out["license_status"] = lic, "clear"
        out["license_evidence"] = evidence
    elif status == "proprietary" and out.get("license_status") in (None, "", "needs_review"):
        out["license"], out["license_status"] = "proprietary", "proprietary"
        out["license_evidence"] = evidence
    return out


def fetch_text(url, timeout=20):
    if not str(url).startswith(("http://", "https://")):
        return None, "非 http(s) URL"
    cmd = ["curl", "-sS", "-L", "--max-time", str(timeout),
           "--max-filesize", "5242880", url]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    except Exception as exc:
        return None, "curl 异常: %s" % exc
    if proc.returncode != 0:
        return None, (proc.stderr or "curl exit %s" % proc.returncode).strip()[:240]
    return proc.stdout, None


def enrich_web(sources, limit=5, timeout=20):
    out, warnings = [], []
    count = 0
    for src in sources:
        if limit and count >= limit:
            out.append(src)
            continue
        if src.get("status") == "rejected" or src.get("platform") not in {"web", "docs"}:
            out.append(src)
            continue
        text, err = fetch_text(src.get("url", ""), timeout=timeout)
        if err:
            item = dict(src)
            item["web_error"] = err
            warnings.append("%s: %s" % (src.get("id"), err[:160]))
            out.append(item)
            count += 1
            continue
        out.append(apply_web(src, extract_html(text)))
        count += 1
    return out, warnings
