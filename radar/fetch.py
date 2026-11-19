"""Optional network refresh for source state (v0.2.5)."""
from __future__ import annotations

import hashlib
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


def _now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_headers(text):
    """Parse the last header block (redirects can produce several)."""
    headers = {}
    for line in (text or "").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    return headers


def apply_fetch(source, status, headers, content_hash, error=None):
    out = dict(source)
    out["http_status"] = status
    out["last_seen"] = _now()
    if content_hash:
        out["content_hash"] = content_hash
    if headers.get("etag"):
        out["etag"] = headers["etag"]
    if headers.get("last-modified"):
        out["last_modified"] = headers["last-modified"]
    if error:
        out["fetch_error"] = str(error)[:240]
    if status == 200:
        out["access_status"] = "public"
    elif status == 401:
        out["access_status"] = "login_required"
    elif status == 403:
        out["access_status"] = "blocked"
    elif status == 404:
        out["access_status"] = "deleted"
    return out


def fetch_one(url, timeout=20):
    """Returns (status, headers, sha256, error). Uses curl; no Python dep."""
    if not str(url).startswith(("http://", "https://")):
        return 0, {}, None, "非 http(s) URL"
    with tempfile.TemporaryDirectory() as tmp:
        hdr = Path(tmp) / "headers.txt"
        body = Path(tmp) / "body.bin"
        cmd = ["curl", "-sS", "-L", "--max-time", str(timeout),
               "--max-filesize", "8388608", "-D", str(hdr), "-o", str(body),
               "-w", "%{http_code}", url]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        except Exception as exc:
            return 0, {}, None, "curl 异常: %s" % exc
        status = 0
        try:
            status = int((proc.stdout or "0").strip())
        except ValueError:
            status = 0
        headers = parse_headers(hdr.read_text(encoding="utf-8", errors="ignore")) if hdr.exists() else {}
        digest = None
        if body.exists():
            digest = hashlib.sha256(body.read_bytes()).hexdigest()
        err = None
        if proc.returncode != 0:
            err = (proc.stderr or "curl exit %s" % proc.returncode).strip()
        return status, headers, digest, err


def fetch_sources(sources, limit=0, timeout=20):
    """Refresh selected sources; returns (sources, warnings)."""
    out, warnings = [], []
    count = 0
    for src in sources:
        if limit and count >= limit:
            out.append(src)
            continue
        if src.get("status") == "rejected":
            out.append(src)
            continue
        status, headers, digest, err = fetch_one(src.get("url", ""), timeout=timeout)
        if err:
            warnings.append("%s: %s" % (src.get("id"), err[:160]))
        out.append(apply_fetch(src, status, headers, digest, err))
        count += 1
    return out, warnings
