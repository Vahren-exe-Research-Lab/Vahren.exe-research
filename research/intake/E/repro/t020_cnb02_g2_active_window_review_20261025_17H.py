"""E/T020: synthetic guard that G2 capture belongs to the *active* battle window.
This reviews the separate 16H chronology gate, without editing it or native files.
"""
import math
import unittest
import t020_cnb02_g1_phase_contract_matrix_20261025_16H as prior

def sample():
    x = prior.baseline()
    x.update(
        active_exit=20.0, exit_clock="run-clock",
        exit_run="synthetic-run", exit_battle="synthetic-battle", exit_pid=111,
        capture_phase="BATTLE_ACTIVE",
        guard_before={"mode": 2, "active": 1},
        guard_after={"mode": 2, "active": 1},
        coherence_witness="SYNTHETIC_ONLY"
    )
    return x

def review(x):
    prior_result = prior.assess(x)
    issues = list(prior_result["issues"])
    add = issues.append
    start, end, capture = x.get("active_enter"), x.get("active_exit"), x.get("g2_capture")
    numeric = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    if end is None:
        add("ACTIVE_EXIT_UNOBSERVED")
    elif not numeric(end):
        add("ACTIVE_EXIT_TIMESTAMP_INVALID")
    elif numeric(start):
        if end <= start:
            add("ACTIVE_WINDOW_INVALID")
        if numeric(capture):
            if capture >= end:
                add("G2_AT_OR_AFTER_EXIT")
            elif capture == start:
                add("G2_AT_ENTER_BOUNDARY_VERIFY")
    domains = x.get("domains")
    exit_clock = x.get("exit_clock")
    if (not isinstance(exit_clock, str) or not exit_clock
        or not isinstance(domains, list) or len(domains) != 5
        or any(d != exit_clock for d in domains)):
        add("EXIT_CLOCK_UNCALIBRATED")
    for key, expected in (("exit_run", x.get("run_id")),
                          ("exit_battle", x.get("battle_id")),
                          ("exit_pid", x.get("pid"))):
        if x.get(key) != expected:
            add("EXIT_IDENTITY_MISMATCH")
    if x.get("capture_phase") != "BATTLE_ACTIVE":
        add("G2_ACTIVE_PHASE_UNPROVEN")
    before, after = x.get("guard_before"), x.get("guard_after")
    for guard in (before, after):
        if not isinstance(guard, dict):
            add("G2_GUARD_MISSING")
        elif (type(guard.get("mode")) is not int or guard["mode"] != 2
              or type(guard.get("active")) is not int or guard["active"] != 1):
            add("G2_GUARD_NOT_ACTIVE")
    witness = x.get("coherence_witness")
    if not isinstance(witness, str) or not witness:
        add("G2_COHERENCE_WITNESS_MISSING")
    return {"review_flags": sorted(set(issues)), "prior_flags": prior_result["issues"],
            "status": "SYNTHETIC_REVIEW_ONLY", "actual_golden_pass": False,
            "strict_match": False}

CASES = [
    ("W01_active_synthetic", {}, []),
    ("W02_post_exit_invisible_to_prior", {"g2_capture": 25.0}, ["G2_AT_OR_AFTER_EXIT"]),
    ("W03_exit_boundary", {"g2_capture": 20.0}, ["G2_AT_OR_AFTER_EXIT"]),
    ("W04_exit_missing", {"active_exit": None}, ["ACTIVE_EXIT_UNOBSERVED"]),
    ("W05_inverted_window", {"active_exit": 11.0}, ["ACTIVE_WINDOW_INVALID", "G2_AT_OR_AFTER_EXIT"]),
    ("W06_capture_at_enter", {"g2_capture": 12.0}, ["G2_AT_ENTER_BOUNDARY_VERIFY"]),
    ("W07_exit_clock_diff", {"exit_clock": "other"}, ["EXIT_CLOCK_UNCALIBRATED"]),
    ("W08_after_guard_strategic", {"guard_after": {"mode": 1, "active": 0}}, ["G2_GUARD_NOT_ACTIVE"]),
    ("W09_postbattle_label", {"capture_phase": "POSTBATTLE"}, ["G2_ACTIVE_PHASE_UNPROVEN"]),
    ("W10_missing_coherence", {"coherence_witness": ""}, ["G2_COHERENCE_WITNESS_MISSING"]),
    ("W11_cross_battle", {"exit_battle": "other"}, ["EXIT_IDENTITY_MISMATCH"]),
    ("W12_guard_absent", {"guard_before": None}, ["G2_GUARD_MISSING"]),
    ("W13_nonfinite_exit", {"active_exit": float("inf")}, ["ACTIVE_EXIT_TIMESTAMP_INVALID"]),
    ("W14_bool_exit", {"active_exit": True}, ["ACTIVE_EXIT_TIMESTAMP_INVALID"]),
    ("W15_cross_run", {"exit_run": "other"}, ["EXIT_IDENTITY_MISMATCH"]),
    ("W16_ui_then_save_allowed_for_review", {"ui_open": 8.0}, []),
    ("W17_receipt_late_unrelated", {"save_receipt": 999.0}, []),
    ("W18_post_exit_old_false_negative", {"g2_capture": 100.0, "active_exit": 20.0}, ["G2_AT_OR_AFTER_EXIT"]),
    ("W19_same_alternate_clock", {"exit_clock": "native-mono", "domains": ["native-mono"] * 5}, []),
    ("W20_missing_exit_clock", {"exit_clock": None}, ["EXIT_CLOCK_UNCALIBRATED"]),
    ("W21_boolean_active_guard", {"guard_before": {"mode": 2, "active": True}}, ["G2_GUARD_NOT_ACTIVE"]),
    ("W22_boolean_coherence", {"coherence_witness": True}, ["G2_COHERENCE_WITNESS_MISSING"]),
]

class ActiveWindowTests(unittest.TestCase):
    pass

def make_test(patch, expected):
    def check(self):
        x = sample()
        x.update(patch)
        got = review(x)
        self.assertEqual(got["review_flags"], sorted(expected))
        self.assertFalse(got["actual_golden_pass"])
        self.assertFalse(got["strict_match"])
        if "post_exit" in self._testMethodName:
            self.assertEqual(got["prior_flags"], [])  # Demonstrates a bounded 16H schema gap.
    return check

for idx, (label, patch, expected) in enumerate(CASES, 1):
    setattr(ActiveWindowTests, f"test_{idx:02d}_{label}", make_test(patch, expected))

if __name__ == "__main__":
    unittest.main(verbosity=1)