"""E/T020: receipt-shape gate; synthetic unit tests, NOT a gameplay emulator."""
import unittest

REQUIRED_STAGES = ("g0", "g1", "g2", "g3", "g4")
REQUIRED_HASHES = ("old_exe", "old_save", "old_dat", "old_map", "old_input")

def gate(r):
    if not r.get("old_observed"):
        return "DESIGNED_NOT_RUN"
    runs = [r.get("stage_runs", {}).get(k) for k in REQUIRED_STAGES]
    if any(v is None for v in runs) or len(set(runs)) != 1:
        return "REJECT_EVIDENCE"
    if not all(r.get("old_hashes", {}).get(k) for k in REQUIRED_HASHES):
        return "REJECT_EVIDENCE"
    if not all(r.get("captures", {}).get(k) for k in REQUIRED_STAGES):
        return "VERIFY"
    if r.get("commit_paths") == ["native", "new_api"] or r.get("commit_paths") == ["new_api", "native"]:
        return "REJECT_DOUBLE_COMMIT"
    if r.get("commit_paths") not in (["native"], ["new_api"]):
        return "VERIFY"
    if r.get("route_evidence") != "DYNAMIC_OBSERVED":
        return "VERIFY"
    if not r.get("new_build_sha") or not r.get("new_capture_sha"):
        return "NO_STRICT_COMPARISON"
    return "SYNTHETIC_SCHEMA_READY" if r.get("synthetic") else "READY_FOR_COMPARISON"

class BattleEndGateTests(unittest.TestCase):
    def base(self):
        return dict(synthetic=True, old_observed=True,
                    stage_runs={k: "r1" for k in REQUIRED_STAGES},
                    old_hashes={k: "present" for k in REQUIRED_HASHES},
                    captures={k: "capture" for k in REQUIRED_STAGES},
                    commit_paths=["native"], route_evidence="DYNAMIC_OBSERVED",
                    new_build_sha="present", new_capture_sha="present")

    def test_no_old_observation(self):
        r=self.base(); r["old_observed"]=False
        self.assertEqual(gate(r), "DESIGNED_NOT_RUN")

    def test_missing_world_capture(self):
        r=self.base(); r["captures"]["g4"]=None
        self.assertEqual(gate(r), "VERIFY")

    def test_cross_session(self):
        r=self.base(); r["stage_runs"]["g4"]="r2"
        self.assertEqual(gate(r), "REJECT_EVIDENCE")

    def test_double_commit(self):
        r=self.base(); r["commit_paths"]=["native","new_api"]
        self.assertEqual(gate(r), "REJECT_DOUBLE_COMMIT")

    def test_static_route_not_observed(self):
        r=self.base(); r["route_evidence"]="STATIC"
        self.assertEqual(gate(r), "VERIFY")

    def test_missing_new_build(self):
        r=self.base(); r["new_build_sha"]=None
        self.assertEqual(gate(r), "NO_STRICT_COMPARISON")

    def test_missing_old_hash(self):
        r=self.base(); r["old_hashes"]["old_save"]=None
        self.assertEqual(gate(r), "REJECT_EVIDENCE")

    def test_full_synthetic_is_not_gameplay_match(self):
        r=self.base()
        self.assertEqual(gate(r), "SYNTHETIC_SCHEMA_READY")

if __name__ == "__main__":
    unittest.main()