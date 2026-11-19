import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from radar.coverage import compute_coverage, gap_rows
from radar.report import render_gaps, render_report
from radar.state import compare_sources, render_changes
from radar.adapters import parse_gitee_items, gitee_search
from radar.fetch import apply_fetch, parse_headers
from radar.snowball import parse_github_repo, fork_source, snowball as run_snowball
from radar.web import extract_html, detect_license, apply_web, enrich_web
from radar.claims import compute_confidence, evaluate_claims, write_claims
from radar.diff import diff_runs
from radar.model import (RadarError, canonical_url, load_pack, load_seeds,
                         validate_source)

PACK = ROOT / "packs/weak-current/pack.json"
SEEDS = ROOT / "seeds/weak-current.json"


def src(sid, covers, evidence="readme", quotes=None, status="selected"):
    return {
        "id": sid, "platform": "github", "url": "https://example.com/%s" % sid,
        "title": sid, "artifact_type": "readme", "access_status": "public",
        "license": "MIT", "license_status": "clear", "evidence_level": evidence,
        "covers": covers, "quotes": quotes if quotes is not None else ["quote"],
        "status": status, "why_selected": "test",
    }


class TestModel(unittest.TestCase):
    def test_canonical_url(self):
        self.assertEqual(canonical_url("https://www.Example.com/a/?utm_source=x#frag"),
                         "https://example.com/a")
        self.assertEqual(canonical_url("https://example.com/a"), "https://example.com/a")

    def test_pack_and_seeds_valid(self):
        pack = load_pack(PACK)
        seeds = load_seeds(SEEDS, pack)
        self.assertEqual(len(pack["modules"]), 14)
        self.assertEqual(len(pack["subsystems"]), 24)
        self.assertEqual(len(seeds), 13)

    def test_second_pack_valid(self):
        pack = load_pack(ROOT / "packs/pet-hospital/pack.json")
        seeds = load_seeds(ROOT / "seeds/pet-hospital.json", pack)
        self.assertEqual(len(pack["modules"]), 6)
        self.assertEqual(len(pack["subsystems"]), 6)
        self.assertEqual(len(seeds), 3)

    def test_minimal_seed_defaults(self):
        pack = load_pack(PACK)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "minimal.json"
            path.write_text(json.dumps({
                "schema_version": 1, "pack": "weak-current",
                "sources": [{
                    "id": "MIN-001", "url": "https://example.com/doc",
                    "evidence_level": "docs", "covers": ["M01"],
                    "quotes": [], "status": "selected",
                }],
            }), encoding="utf-8")
            seeds = load_seeds(path, pack)
        item = seeds[0]
        self.assertEqual(item["platform"], "web")
        self.assertEqual(item["artifact_type"], "article")
        self.assertEqual(item["access_status"], "public")
        self.assertEqual(item["license"], "unknown")
        self.assertEqual(item["license_status"], "needs_review")
        self.assertEqual(item["why_selected"], "")

    def test_strict_rejects_minimal(self):
        pack = load_pack(PACK)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "minimal.json"
            path.write_text(json.dumps({
                "schema_version": 1, "pack": "weak-current",
                "sources": [{
                    "id": "MIN-001", "url": "https://example.com/doc",
                    "evidence_level": "docs", "covers": ["M01"],
                    "quotes": [], "status": "selected",
                }],
            }), encoding="utf-8")
            with self.assertRaises(RadarError):
                load_seeds(path, pack, strict=True)

    def test_bad_cover_rejected(self):
        pack = load_pack(PACK)
        with self.assertRaises(RadarError):
            validate_source(src("X", ["M99"]), pack)


class TestCoverage(unittest.TestCase):
    def setUp(self):
        self.pack = {"modules": [{"id": "M01", "name": "项目"}],
                     "subsystems": [{"id": "S01", "name": "视频"}]}

    def test_single_source_capped_at_evidence(self):
        cov = compute_coverage(self.pack, [src("A", ["M01"], evidence="real_artifact")])
        row = cov["modules"][0]
        self.assertEqual(row["level"], "evidence")
        self.assertTrue(row["single_source"])

    def test_two_sources_can_be_strong(self):
        cov = compute_coverage(self.pack, [
            src("A", ["M01"], evidence="real_artifact"),
            src("B", ["M01"], evidence="docs"),
        ])
        self.assertEqual(cov["modules"][0]["level"], "strong")
        self.assertFalse(cov["modules"][0]["single_source"])

    def test_no_quote_is_mention(self):
        cov = compute_coverage(self.pack, [src("A", ["M01"], quotes=[])])
        self.assertEqual(cov["modules"][0]["level"], "mention")

    def test_rejected_does_not_count(self):
        cov = compute_coverage(self.pack, [src("A", ["M01"], status="rejected")])
        self.assertEqual(cov["modules"][0]["level"], "none")

    def test_gaps_report_includes_single_source(self):
        cov = compute_coverage(self.pack, [src("A", ["M01"], evidence="real_artifact")])
        text = render_gaps(self.pack, cov)
        self.assertIn("单源待印证", text)
        self.assertIn("M01", text)


    def test_gap_query_artifact_not_joined_list(self):
        # {artifact} 插值应取第一个 artifact，而不是把数组拼成 "readme, docs"
        pack = {"title": "T",
                "modules": [{"id": "M01", "name": "模块", "artifacts": ["readme", "docs"]}],
                "subsystems": [{"id": "S01", "name": "子", "artifacts": ["code"]}],
                "query_templates": ["{module} {artifact} 开源"]}
        cov = compute_coverage(pack, [])  # M01/S01 均无来源 → 均进 gaps
        text = render_gaps(pack, cov)
        self.assertIn("模块 readme 开源", text)
        self.assertNotIn("readme, docs", text)

    def test_gap_query_without_artifacts_field(self):
        # pack 项缺 artifacts 字段时不应崩溃，回退为"资料"
        pack = {"title": "T",
                "modules": [{"id": "M01", "name": "模块"}],
                "subsystems": [{"id": "S01", "name": "子"}],
                "query_templates": ["{module} {artifact} 开源"]}
        cov = compute_coverage(pack, [])
        text = render_gaps(pack, cov)
        self.assertIn("模块 资料 开源", text)

    def test_platform_bias_warning_single_platform(self):
        # 90%+ 来源来自单一平台时应输出平台偏置警告
        state = {"title": "T", "run_id": "r1"}
        pack = {"title": "T", "modules": self.pack["modules"], "subsystems": self.pack["subsystems"], "pack": "p", "version": "0"}
        text = render_report(pack, [src("A", ["M01"])], compute_coverage(self.pack, [src("A", ["M01"])]), state)
        self.assertIn("平台偏置", text)

    def test_platform_bias_no_warning_multi_platform(self):
        state = {"title": "T", "run_id": "r1"}
        pack = {"title": "T", "modules": self.pack["modules"], "subsystems": self.pack["subsystems"], "pack": "p", "version": "0"}
        two = [src("A", ["M01"]), src("B", ["M01"])]
        two[1]["platform"] = "gitee"
        cov = compute_coverage(self.pack, two)
        text = render_report(pack, two, cov, state)
        self.assertNotIn("平台偏置", text)

    def test_low_star_high_coverage_listed(self):
        # 低星（≤50）但覆盖 ≥2 格的来源应被列出
        state = {"title": "T", "run_id": "r1"}
        pack = {"title": "T", "modules": self.pack["modules"], "subsystems": self.pack["subsystems"], "pack": "p", "version": "0"}
        low = src("A", ["M01", "S01"])
        low["stars"] = 3
        cov = compute_coverage(self.pack, [low])
        text = render_report(pack, [low], cov, state)
        self.assertIn("低星但高覆盖", text)
        self.assertIn("覆盖 2 格", text)


class TestClaims(unittest.TestCase):
    def _strong(self, sid, host):
        s = src(sid, ["M01"], evidence="real_artifact", quotes=["q"])
        s["url"] = "https://%s.example/x" % host
        return s

    def test_strong_two_hosts(self):
        by = {"A": self._strong("A", "a"), "B": self._strong("B", "b")}
        claim = {"id": "C1", "statement": "s", "covers": ["M01"],
                 "sources": ["A", "B"], "contradicts": []}
        r = compute_confidence(claim, by)
        self.assertEqual(r["confidence"], 0.8)
        self.assertEqual(r["label"], "high")
        self.assertEqual(r["reasons"], [])

    def test_single_source_cap(self):
        by = {"A": self._strong("A", "a")}
        claim = {"id": "C1", "statement": "s", "covers": ["M01"],
                 "sources": ["A"], "contradicts": []}
        r = compute_confidence(claim, by)
        self.assertEqual(r["confidence"], 0.55)
        self.assertIn("single_source", r["reasons"])

    def test_no_quote_cap(self):
        s = self._strong("A", "a"); s["quotes"] = []
        claim = {"id": "C1", "statement": "s", "covers": ["M01"],
                 "sources": ["A"], "contradicts": []}
        r = compute_confidence(claim, {"A": s})
        self.assertEqual(r["confidence"], 0.3)
        self.assertIn("no_quote", r["reasons"])

    def test_contradiction_contested(self):
        by = {"A": self._strong("A", "a"), "B": self._strong("B", "b")}
        claim = {"id": "C1", "statement": "s", "covers": ["M01"],
                 "sources": ["A", "B"], "contradicts": ["C2"]}
        r = compute_confidence(claim, by)
        self.assertEqual(r["status"], "contested")
        self.assertEqual(r["confidence"], 0.4)

    def test_unknown_source_rejected(self):
        pack = load_pack(PACK)
        data = {"schema_version": 1, "pack": "weak-current", "claims": [{
            "id": "C1", "statement": "s", "covers": ["M01"], "sources": ["NOPE"]}]}
        with self.assertRaises(RadarError):
            evaluate_claims(data, pack, [])


class TestWeb(unittest.TestCase):
    def test_extract_html(self):
        page = extract_html("<html><head><title>弱电报价</title>"
                            "<meta name='description' content='这是一个用于弱电工程报价与成本管理的页面内容'>"
                            "</head><body><script>bad()</script><p>弱电工程报价清单与成本管理说明。</p></body></html>")
        self.assertEqual(page["title"], "弱电报价")
        self.assertNotIn("bad()", page["text"])
        self.assertTrue(page["quotes"])

    def test_detect_license(self):
        mit = "Permission is hereby granted, free of charge, to any person obtaining a copy"
        self.assertEqual(detect_license(mit)[:2], ("MIT", "clear"))
        self.assertEqual(detect_license("licensed under the Apache License, Version 2.0")[:2],
                         ("Apache-2.0", "clear"))
        self.assertEqual(detect_license("All rights reserved.")[:2], ("proprietary", "proprietary"))
        self.assertEqual(detect_license("A 项目采用 Apache 协议")[:2], ("Apache-2.0", "needs_review"))
        self.assertEqual(detect_license("MIT License")[:2], ("MIT", "needs_review"))
        self.assertEqual(detect_license("hello")[:2], ("unknown", "needs_review"))

    def test_apply_web(self):
        out = apply_web({"id": "A", "url": "https://example.com", "title": "x",
                         "license": "unknown", "license_status": "needs_review"},
                        {"title": "T", "description": "",
                         "text": "Permission is hereby granted, free of charge, to any person obtaining a copy",
                         "quotes": ["q"]})
        self.assertEqual(out["license"], "MIT")
        self.assertEqual(out["license_status"], "clear")
        self.assertIn("q", out["quotes"])

    def test_chinese_quotes_not_glued(self):
        text = ("这是弱电工程报价与成本管理的第一段内容，覆盖询价、清单和毛利。"
                "这是第二段内容，说明合同、采购和施工进度的边界。")
        page = extract_html("<p>%s</p>" % text)
        self.assertGreaterEqual(len(page["quotes"]), 2)
        for q in page["quotes"]:
            self.assertLessEqual(len(q), 241)

    def test_web_404_not_success(self):
        src = {"id": "W1", "url": "https://example.com/404", "platform": "web",
               "status": "selected", "access_status": "public", "title": "x"}
        with mock.patch("radar.web.fetch_text", return_value=(None, 404, "HTTP 404")):
            out, warnings = enrich_web([src], limit=1)
        self.assertEqual(out[0]["web_error"], "HTTP 404")
        self.assertEqual(out[0]["http_status"], 404)
        self.assertNotEqual(out[0]["access_status"], "public")
        self.assertTrue(warnings)


class TestFetch(unittest.TestCase):
    def test_parse_headers_and_apply(self):
        headers = parse_headers("HTTP/2 200\r\nETag: \"abc\"\r\nLast-Modified: Wed, 01 Jan 2026 00:00:00 GMT\r\n")
        self.assertEqual(headers["etag"], '"abc"')
        out = apply_fetch({"id": "A", "url": "https://example.com"}, 200, headers, "hash1")
        self.assertEqual(out["access_status"], "public")
        self.assertEqual(out["content_hash"], "hash1")
        self.assertEqual(out["etag"], '"abc"')
        self.assertIn("last_seen", out)

    def test_apply_fetch_auth_statuses(self):
        self.assertEqual(apply_fetch({}, 401, {}, None)["access_status"], "login_required")
        self.assertEqual(apply_fetch({}, 403, {}, None)["access_status"], "blocked")
        self.assertEqual(apply_fetch({}, 404, {}, None)["access_status"], "deleted")


class TestSnowball(unittest.TestCase):
    def test_parse_github_repo(self):
        self.assertEqual(parse_github_repo("https://github.com/demo/elv"), "demo/elv")
        self.assertIsNone(parse_github_repo("https://gitee.com/demo/elv"))

    def test_fork_source_inherits_covers(self):
        parent = src("A", ["M01", "S01"])
        parent["url"] = "https://github.com/demo/elv"
        fork = {"full_name": "other/elv", "html_url": "https://github.com/other/elv",
                "stargazers_count": 1, "language": "Python", "license": {"spdx_id": "MIT"}}
        out = fork_source(fork, parent, 1)
        self.assertEqual(out["platform"], "github")
        self.assertEqual(out["covers"], ["M01", "S01"])
        self.assertEqual(out["license_status"], "clear")
        self.assertIn("fork of A", out["why_selected"])

    def test_snowball_uses_forks(self):
        parent = src("A", ["M01"])
        parent["url"] = "https://github.com/demo/elv"
        forks = [{"full_name": "other/elv", "html_url": "https://github.com/other/elv",
                  "stargazers_count": 1, "license": {"spdx_id": "MIT"}}]
        with mock.patch("radar.snowball.github_forks", return_value=(forks, None)):
            out, warns = run_snowball([parent], {"modules": [{"id": "M01", "name": "项目", "keywords": ["项目"]}], "subsystems": [{"id": "S01", "name": "子系统", "keywords": ["子系统"]}]})
        self.assertEqual(len(out), 1)
        self.assertEqual(warns, [])
        self.assertEqual(out[0]["covers"], ["M01"])


class TestGitee(unittest.TestCase):
    def test_parse_gitee_items(self):
        pack = load_pack(PACK)
        items = [{
            "full_name": "demo/elv-quote", "html_url": "https://gitee.com/demo/elv-quote",
            "description": "弱电 报价 清单", "stargazers_count": 3,
            "updated_at": "2026-11-01T00:00:00+08:00", "language": "Python",
        }]
        out = parse_gitee_items(items, pack, "弱电 报价")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["platform"], "gitee")
        self.assertEqual(out[0]["license"], "unknown")
        self.assertEqual(out[0]["license_status"], "needs_review")
        self.assertIn("M06", out[0]["covers"])

    def test_gitee_without_token_is_explicit(self):
        pack = load_pack(PACK)
        got, warn = gitee_search("弱电", pack, token=None)
        self.assertEqual(got, [])
        self.assertIn("GITEE_TOKEN", warn)


class TestChanges(unittest.TestCase):
    def test_added_removed_changed(self):
        a = src("A", ["M01"]); a["quotes"] = ["old"]
        b = src("B", ["S01"])
        a2 = src("A", ["M01"]); a2["quotes"] = ["new"]
        c = src("C", ["M01"])
        result = compare_sources([a, b], [a2, c])
        self.assertEqual([x["id"] for x in result["added"]], ["C"])
        self.assertEqual([x["id"] for x in result["removed"]], ["B"])
        self.assertEqual(len(result["changed"]), 1)
        self.assertIn("quotes", result["changed"][0]["fields"])
        self.assertIn("新增", render_changes(result))

    def test_no_change(self):
        a = src("A", ["M01"])
        result = compare_sources([a], [dict(a)])
        self.assertEqual(result["added"], [])
        self.assertEqual(result["removed"], [])
        self.assertEqual(result["changed"], [])
        self.assertEqual(result["unchanged"], 1)


class TestCLI(unittest.TestCase):
    def test_run_and_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            out1 = tmp / "run1"
            subprocess.run([sys.executable, "-m", "radar", "run", "--pack", str(PACK),
                            "--seeds", str(SEEDS), "--title", "测试", "--out", str(out1)],
                           cwd=ROOT, check=True, capture_output=True, text=True)
            for name in ["sources.jsonl", "coverage.json", "toc.md", "coverage.md",
                         "gaps.md", "report.md", "state.json"]:
                self.assertTrue((out1 / name).exists(), name)

            data = json.loads(SEEDS.read_text(encoding="utf-8"))
            data["sources"] = [s for s in data["sources"] if s["id"] != "SRC-013"]
            seeds2 = tmp / "seeds2.json"
            seeds2.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            out2 = tmp / "run2"
            subprocess.run([sys.executable, "-m", "radar", "run", "--pack", str(PACK),
                            "--seeds", str(seeds2), "--title", "测试", "--out", str(out2)],
                           cwd=ROOT, check=True, capture_output=True, text=True)
            diff = tmp / "diff.md"
            diff_runs(out1, out2, out=diff)
            text = diff.read_text(encoding="utf-8")
            self.assertIn("移除来源", text)
            self.assertIn("SRC-013", text)

            scan_out = tmp / "scan"
            subprocess.run([sys.executable, "-m", "radar", "scan", "--pack", str(PACK),
                            "--seeds", str(seeds2), "--title", "测试", "--out", str(scan_out),
                            "--since", str(out1)], cwd=ROOT, check=True, capture_output=True, text=True)
            self.assertTrue((scan_out / "diff.md").exists())
            self.assertTrue((scan_out / "changes.md").exists())
            self.assertIn("SRC-013", (scan_out / "diff.md").read_text(encoding="utf-8"))
            self.assertIn("SRC-013", (scan_out / "changes.md").read_text(encoding="utf-8"))
            state = json.loads((scan_out / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "scan")
            self.assertEqual(state["since"], str(out1))
            self.assertEqual(state["radar_version"], "0.4.0")
            self.assertIn("radar_commit", state)
            self.assertIn("Radar: v0.4.0", (scan_out / "report.md").read_text(encoding="utf-8"))

            claims_file = tmp / "claims.json"
            claims_file.write_text(json.dumps({
                "schema_version": 1, "pack": "weak-current",
                "claims": [{"id": "C1", "statement": "测试主张", "covers": ["M01"],
                            "sources": ["SRC-001"], "contradicts": []}],
            }, ensure_ascii=False), encoding="utf-8")
            claims_out = tmp / "claims"
            subprocess.run([sys.executable, "-m", "radar", "claims", "--pack", str(PACK),
                            "--run", str(out1), "--claims", str(claims_file),
                            "--out", str(claims_out)], cwd=ROOT, check=True,
                           capture_output=True, text=True)
            self.assertTrue((claims_out / "claims.md").exists())
            self.assertTrue((claims_out / "review.csv").exists())
            self.assertEqual(json.loads((claims_out / "state.json").read_text())["radar_version"], "0.4.0")


if __name__ == "__main__":
    unittest.main()
