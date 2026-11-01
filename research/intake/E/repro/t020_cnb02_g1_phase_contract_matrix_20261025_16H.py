"""E/T020: standalone synthetic G1 chronology policy regression; no native Golden verdict."""
import math
import re
import unittest

EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"

def baseline():
    return {
        "run_id": "synthetic-run", "g0_run": "synthetic-run",
        "g1_run": "synthetic-run", "g2_run": "synthetic-run",
        "battle_id": "synthetic-battle", "pid": 111,
        "exe_sha": EXE_SHA, "save_sha": "a" * 64, "input_sha": "b" * 64,
        "save_ref": "mock-save", "input_ref": "mock-input",
        "ui_open": 10.0, "save_commit": 9.0, "attack_commit": 11.0,
        "active_enter": 12.0, "g2_capture": 12.5, "save_receipt": 13.0,
        "domains": ["run-clock"] * 5,
        "state_changed_after_save": False, "continuity_proven": False,
    }

def assess(x):
    issues = []
    add = issues.append
    run = x.get("run_id")
    if not isinstance(run, str) or not run or any(x.get(k) != run for k in ("g0_run", "g1_run", "g2_run")):
        add("CROSS_RUN_ID")
    if not isinstance(x.get("pid"), int) or isinstance(x.get("pid"), bool) or x["pid"] <= 0 or not x.get("battle_id"):
        add("BAD_IDENTITY")
    if x.get("exe_sha") != EXE_SHA:
        add("EXE_SHA_MISMATCH")
    sha_ok = lambda v: isinstance(v, str) and bool(re.fullmatch(r"[0-9a-fA-F]{64}", v))
    if not sha_ok(x.get("save_sha")) or not sha_ok(x.get("input_sha")):
        add("SHA_FORMAT_INVALID")
    if not x.get("save_ref") or not x.get("input_ref"):
        add("PRIMARY_SOURCE_REFERENCE_MISSING")
    fields = ("ui_open", "save_commit", "attack_commit", "active_enter", "g2_capture")
    t = {k: x.get(k) for k in fields}
    if any(v is not None and (not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v)) for v in t.values()):
        add("BAD_TIMESTAMP")
    elif not isinstance(x.get("domains"), list) or len(x["domains"]) != 5 or len(set(x["domains"])) != 1:
        add("CLOCK_DOMAIN_VERIFY")
    else:
        ui, save, commit, active, g2 = (t[k] for k in fields)
        if ui is None:
            add("G0_UI_UNOBSERVED")
        if save is None:
            add("SAVE_COMMIT_UNOBSERVED")
        if active is None:
            add("ACTIVE_ENTER_UNOBSERVED")
        if g2 is None:
            add("G2_CAPTURE_UNOBSERVED")
        if active is not None:
            if save is not None and save >= active:
                add("SAVE_NOT_PRE_ACTIVE")
            if ui is not None and ui >= active:
                add("UI_NOT_PRE_ACTIVE")
            if g2 is not None and g2 < active:
                add("G2_PRE_ACTIVE")
        if commit is None:
            add("ATTACK_COMMIT_UNPROVEN")
        else:
            if active is not None and commit >= active:
                add("COMMIT_NOT_PRE_ACTIVE")
            if ui is not None and commit < ui:
                add("COMMIT_PRE_UI")
            if save is not None and save == commit:
                add("EQUAL_COMMIT_SAVE_VERIFY")
            if save is not None and save > commit:
                add("SAVE_AFTER_COMMIT_VERIFY")
    if x.get("state_changed_after_save") and not x.get("continuity_proven"):
        add("STATE_CONTINUITY_VERIFY")
    return {"issues": sorted(set(issues)), "evidence_level": "SYNTHETIC_SCHEMA_ONLY",
            "actual_golden_pass": False, "strict_match": False}

CASES = [
    ("P01_save_ui_commit", {}, []),
    ("P02_ui_save_commit", {"ui_open": 8.0, "save_commit": 9.0}, []),
    ("P03_generic_attack", {"attack_commit": None}, ["ATTACK_COMMIT_UNPROVEN"]),
    ("P04_equal_save_commit", {"save_commit": 11.0}, ["EQUAL_COMMIT_SAVE_VERIFY"]),
    ("P05_late_save_receipt", {"save_receipt": 20.0}, []),
    ("P06_state_change", {"state_changed_after_save": True}, ["STATE_CONTINUITY_VERIFY"]),
    ("P07_cross_run", {"g2_run": "unrelated"}, ["CROSS_RUN_ID"]),
    ("P08_post_active_save", {"save_commit": 13.0}, ["SAVE_AFTER_COMMIT_VERIFY", "SAVE_NOT_PRE_ACTIVE"]),
    ("P09_clock_mismatch", {"domains": ["ui", "save", "ui", "ui", "ui"]}, ["CLOCK_DOMAIN_VERIFY"]),
    ("P10_missing_source", {"save_ref": ""}, ["PRIMARY_SOURCE_REFERENCE_MISSING"]),
    ("P11_g2_early", {"g2_capture": 11.5}, ["G2_PRE_ACTIVE"]),
    ("P12_invalid_pid", {"pid": -7}, ["BAD_IDENTITY"]),
    ("P13_nan_timestamp", {"save_commit": float("nan")}, ["BAD_TIMESTAMP"]),
    ("P14_exe_mismatch", {"exe_sha": "f" * 64}, ["EXE_SHA_MISMATCH"]),
    ("P15_save_after_proven_commit", {"save_commit": 11.5}, ["SAVE_AFTER_COMMIT_VERIFY"]),
    ("P16_ui_missing", {"ui_open": None}, ["G0_UI_UNOBSERVED"]),
    ("P17_commit_after_active", {"attack_commit": 13.0}, ["COMMIT_NOT_PRE_ACTIVE"]),
    ("P18_g2_missing", {"g2_capture": None}, ["G2_CAPTURE_UNOBSERVED"]),
]

class SyntheticPhaseTests(unittest.TestCase):
    pass

def make_test(patch, expected):
    def check(self):
        data = baseline()
        data.update(patch)
        result = assess(data)
        self.assertEqual(result["issues"], expected)
        self.assertFalse(result["actual_golden_pass"])
        self.assertFalse(result["strict_match"])
    return check

for i, (name, patch, expected) in enumerate(CASES, 1):
    setattr(SyntheticPhaseTests, f"test_{i:02d}_{name}", make_test(patch, expected))

if __name__ == "__main__":
    unittest.main(verbosity=1)
