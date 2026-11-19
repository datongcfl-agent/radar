import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from radar.coverage import compute_coverage, gap_rows
from radar.report import render_gaps, render_report
from radar.state import compare_sources, render_changes
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


if __name__ == "__main__":
    unittest.main()
