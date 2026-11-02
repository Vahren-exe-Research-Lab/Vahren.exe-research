"""E T020: keep source pins, visual pixel diff, and native Golden disjoint."""
from __future__ import annotations
import ast
import hashlib
import re
import unittest
from pathlib import Path
import t020_e_source_pin_admission_20261029_06H as pin

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
VISUAL = ROOT / "dev_lab" / "src" / "hakushin_compat" / "battle_compare.py"
VISUAL_TEST = ROOT / "dev_lab" / "tests" / "test_battle_compare.py"
HEX64 = re.compile(r"[0-9a-fA-F]{64}\Z")
PIXEL = "PIXEL_DIFF_ONLY__NO_GAMEPLAY_PARITY"
STATIC = "SOURCE_PINNED_STATIC_ONLY_NOT_NATIVE"
SYNTH = "SYNTHETIC_G2_CROSS_CONTRACT_CONSISTENT_NOT_NATIVE"

def bridge_preflight(source_record, visual_record, anchors):
    """An E diagnostic only; NEVER approves actual native Golden or strict MATCH."""
    issues = []
    if not isinstance(source_record, dict) or source_record.get("status") != STATIC:
        issues.append("UNPINNED_SOURCE")
    if not isinstance(visual_record, dict) or visual_record.get("status") != PIXEL:
        issues.append("NOT_RECOGNIZED_PIXEL_COMPARISON")
    if not isinstance(anchors, dict):
        issues.append("NO_NATIVE_STAGE_RECEIPTS")
        anchors = {}
    stages = [anchors.get(s) for s in ("G0", "G1", "G2")]
    if any(not isinstance(s, dict) or not s.get("run_id") for s in stages):
        issues.append("MISSING_STAGE_LINEAGE")
    elif len({s["run_id"] for s in stages}) != 1:
        issues.append("CROSS_RUN_MIX")
    if not isinstance(stages[0], dict) or not stages[0].get("legal_ui"):
        issues.append("NO_G0_LEGAL_UI_WITNESS")
    if not isinstance(stages[1], dict) or not stages[1].get("input_receipt"):
        issues.append("NO_G1_INPUT_WITNESS")
    for ix, key in ((1, "save_sha256"), (2, "map_sha256")):
        s = stages[ix]
        h = s.get(key) if isinstance(s, dict) else None
        if not isinstance(h, str) or not HEX64.fullmatch(h):
            issues.append("MISSING_OR_BAD_" + key.upper())
    if not isinstance(stages[2], dict) or not stages[2].get("ordered_roster"):
        issues.append("NO_G2_DEPLOYMENT_WITNESS")
    return {"status": "NOT_QUALIFIED" if issues else "REVIEW_ONLY_NOT_NATIVE",
            "issues": issues, "actual_golden_pass": False,
            "strict_match": False, "evidence_class": "STATIC_CROSSWALK"}

def sample():
    return {"G0": {"run_id": "run-01", "legal_ui": True},
            "G1": {"run_id": "run-01", "input_receipt": "input.bin",
                   "save_sha256": "a"*64},
            "G2": {"run_id": "run-01", "map_sha256": "b"*64,
                   "ordered_roster": [{"side": "A", "unit": "u"}]}}
class ComparatorKindBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = pin.resolve("library", pin.NAME21)
        cls.source = {"status": cls.raw["status"]}
        cls.visual = {"status": PIXEL, "mean_abs_rgb_diff": 0,
                      "reference_is_original_exe_verified": False,
                      "aligned_camera_verified": False}
    def test_01_pinned_source_is_real_bytes_and_static_only(self):
        self.assertEqual(self.raw["sha256"],
                         hashlib.sha256(self.raw["bytes"]).hexdigest().upper())
        self.assertEqual(self.raw["status"], STATIC)
    def test_02_visual_comparator_implements_only_pixel_diff(self):
        src = VISUAL.read_text(encoding="utf-8")
        tree = ast.parse(src)
        names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        self.assertIn("compare_reference_screenshot", names)
        self.assertIn(PIXEL, src)
        self.assertIn('"reference_is_original_exe_verified":False', src)
        self.assertIn('"aligned_camera_verified":False', src)
    def test_03_visual_test_rejects_identical_image_as_golden(self):
        src = VISUAL_TEST.read_text(encoding="utf-8")
        self.assertIn("same_render_reference_yields_zero_pixel_difference_but_not_golden", src)
        self.assertIn("self.assertFalse(stats[\"reference_is_original_exe_verified\"])", src)
    def test_04_even_zero_pixel_delta_not_gameplay(self):
        r = bridge_preflight(self.source, self.visual, sample())
        self.assertFalse(r["actual_golden_pass"])
        self.assertFalse(r["strict_match"])
        self.assertEqual(r["status"], "REVIEW_ONLY_NOT_NATIVE")
    def test_05_visual_claim_forgery_does_not_promote(self):
        v = dict(self.visual, reference_is_original_exe_verified=True,
                 aligned_camera_verified=True, actual_golden_pass=True)
        self.assertFalse(bridge_preflight(self.source, v, sample())["strict_match"])
    def test_06_pin_claim_forgery_does_not_promote(self):
        x = dict(self.source, actual_golden_pass=True, strict_match=True)
        self.assertFalse(bridge_preflight(x, self.visual, sample())["actual_golden_pass"])
    def test_07_synthetic_g2_not_accepted_as_native_source(self):
        x = {"status": SYNTH}
        self.assertIn("UNPINNED_SOURCE", bridge_preflight(x, self.visual, sample())["issues"])
    def test_08_cross_run_is_not_qualified(self):
        x=sample(); x["G2"]["run_id"]="run-02"
        self.assertIn("CROSS_RUN_MIX", bridge_preflight(self.source, self.visual, x)["issues"])
    def test_09_missing_g1_is_not_qualified(self):
        x=sample(); del x["G1"]
        self.assertIn("MISSING_STAGE_LINEAGE", bridge_preflight(self.source, self.visual, x)["issues"])
    def test_10_bad_save_digest_is_not_qualified(self):
        x=sample(); x["G1"]["save_sha256"]="short"
        self.assertIn("MISSING_OR_BAD_SAVE_SHA256", bridge_preflight(self.source, self.visual, x)["issues"])
    def test_11_bad_map_digest_is_not_qualified(self):
        x=sample(); x["G2"]["map_sha256"]=None
        self.assertIn("MISSING_OR_BAD_MAP_SHA256", bridge_preflight(self.source, self.visual, x)["issues"])
    def test_12_empty_roster_is_not_qualified(self):
        x=sample(); x["G2"]["ordered_roster"]=[]
        self.assertIn("NO_G2_DEPLOYMENT_WITNESS", bridge_preflight(self.source, self.visual, x)["issues"])
    def test_13_missing_ui_is_not_qualified(self):
        x=sample(); x["G0"]["legal_ui"]=False
        self.assertIn("NO_G0_LEGAL_UI_WITNESS", bridge_preflight(self.source, self.visual, x)["issues"])
    def test_14_wrong_pixel_status_is_not_qualified(self):
        x={"status": "GOLDEN_PASS", "mean_abs_rgb_diff": 0}
        self.assertIn("NOT_RECOGNIZED_PIXEL_COMPARISON",
                      bridge_preflight(self.source, x, sample())["issues"])
    def test_15_complete_self_report_is_still_review_only(self):
        x=sample()
        for v in x.values(): v["native_gameplay_confirmed"]=True
        r=bridge_preflight(self.source, self.visual, x)
        self.assertEqual(r["status"], "REVIEW_ONLY_NOT_NATIVE")
        self.assertFalse(r["actual_golden_pass"])
        self.assertFalse(r["strict_match"])

if __name__ == "__main__":
    unittest.main(verbosity=2)