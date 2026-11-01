"""E T020 C-NB02 receipt evidence shape; never asserts original gameplay PASS."""
import re
import unittest

OLD_EXE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
STAGES = ("g0", "g1", "g2", "g3", "g4")
REQUIRED = ("old_save", "old_dat", "old_map", "old_input")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")

def sha_ok(value):
    return isinstance(value, str) and HEX64.fullmatch(value) is not None

def gate(r):
    if r.get("eligible") is False:
        return "INELIGIBLE"
    if not r.get("old_observed"):
        return "DESIGNED_NOT_RUN"
    if r.get("source_class") != "ORIGINAL_UI" or r.get("old_exe_sha") != OLD_EXE:
        return "REJECT_SOURCE"
    if not all(sha_ok(r.get(k)) for k in REQUIRED):
        return "REJECT_EVIDENCE"
    stages = r.get("stages", {})
    if not all(k in stages for k in STAGES):
        return "VERIFY"
    runs = {stages[k].get("run_id") for k in STAGES}
    if None in runs or len(runs) != 1 or r.get("run_id") not in runs:
        return "REJECT_EVIDENCE"
    for k in STAGES:
        s = stages[k]
        if s.get("source_class") != "ORIGINAL_UI":
            return "REJECT_SOURCE"
        if not sha_ok(s.get("capture_sha")):
            return "REJECT_EVIDENCE"
        ts = s.get("t_ms")
        if isinstance(ts, bool) or not isinstance(ts, (int, float)) or ts < 0:
            return "REJECT_EVIDENCE"
    t = {k: stages[k]["t_ms"] for k in STAGES}
    # G0 UI entrance and G1 pre-battle SAVE may interleave; both precede deployment.
    if not (t["g0"] < t["g2"] and t["g1"] < t["g2"] <= t["g3"] < t["g4"]):
        return "REJECT_EVIDENCE"
    g2 = stages["g2"]
    if not g2.get("map_id") or not isinstance(g2.get("roster"), list) or not g2["roster"]:
        return "VERIFY"
    sides = g2.get("sides")
    if not isinstance(sides, dict) or set(sides) != {"attack", "defense", "support"}:
        return "VERIFY"
    if any(not isinstance(sides[side], list) for side in sides):
        return "VERIFY"
    if any(not all(item.get(k) for k in ("side", "unit_visible", "troop_visible"))
           for item in g2["roster"] if isinstance(item, dict)):
        return "VERIFY"
    if any(not isinstance(item, dict) for item in g2["roster"]):
        return "VERIFY"
    paths = r.get("commit_paths")
    if isinstance(paths, list) and "native" in paths and "new_api" in paths:
        return "REJECT_DOUBLE_COMMIT"
    if paths not in (["native"], ["new_api"]):
        return "VERIFY"
    if not sha_ok(r.get("new_build_sha")) or not sha_ok(r.get("new_capture_sha")):
        return "NO_STRICT_COMPARISON"
    # Passing schema is never a gameplay observation or strict MATCH.
    return "SYNTHETIC_SCHEMA_ONLY" if r.get("synthetic") else "ELIGIBLE_FOR_REVIEW_NOT_MATCH"

class ReceiptProvenanceTests(unittest.TestCase):
    def base(self):
        stages = {k: dict(run_id="r1", source_class="ORIGINAL_UI",
                          capture_sha="a"*64, t_ms=(i+1)*10)
                  for i, k in enumerate(STAGES)}
        stages["g2"].update(map_id="observed-map", sides={
            "attack": ["red"], "defense": ["blue"], "support": []},
            roster=[dict(side="attack", unit_visible="u1", troop_visible="t1")])
        return dict(synthetic=True, eligible=True, old_observed=True,
                    source_class="ORIGINAL_UI", old_exe_sha=OLD_EXE,
                    run_id="r1", stages=stages, commit_paths=["native"],
                    new_build_sha="b"*64, new_capture_sha="c"*64,
                    **{k:"d"*64 for k in REQUIRED})
    def check_mutation(self, expected, mutate):
        r = self.base()
        mutate(r)
        self.assertEqual(gate(r), expected)
    def test_no_old_capture(self):
        self.check_mutation("DESIGNED_NOT_RUN", lambda r:r.update(old_observed=False))
    def test_ineligible(self):
        self.check_mutation("INELIGIBLE", lambda r:r.update(eligible=False))
    def test_wrong_exe(self):
        self.check_mutation("REJECT_SOURCE", lambda r:r.update(old_exe_sha="0"*64))
    def test_placeholder_sha(self):
        self.check_mutation("REJECT_EVIDENCE", lambda r:r.update(old_save="present"))
    def test_missing_g4(self):
        self.check_mutation("VERIFY", lambda r:r["stages"].pop("g4"))
    def test_cross_run(self):
        self.check_mutation("REJECT_EVIDENCE", lambda r:r["stages"]["g4"].update(run_id="r2"))
    def test_static_not_capture(self):
        self.check_mutation("REJECT_SOURCE", lambda r:r["stages"]["g2"].update(source_class="STATIC"))
    def test_fake_capture_sha(self):
        self.check_mutation("REJECT_EVIDENCE", lambda r:r["stages"]["g2"].update(capture_sha="capture"))
    def test_missing_roster(self):
        self.check_mutation("VERIFY", lambda r:r["stages"]["g2"].update(roster=[]))
    def test_g1_after_deployment(self):
        self.check_mutation("REJECT_EVIDENCE", lambda r:r["stages"]["g1"].update(t_ms=35))
    def test_g0_after_deployment(self):
        self.check_mutation("REJECT_EVIDENCE", lambda r:r["stages"]["g0"].update(t_ms=35))
    def test_g1_before_g0_allowed(self):
        r = self.base(); r["stages"]["g1"]["t_ms"] = 5
        self.assertEqual(gate(r), "SYNTHETIC_SCHEMA_ONLY")
    def test_double_commit(self):
        self.check_mutation("REJECT_DOUBLE_COMMIT", lambda r:r.update(commit_paths=["new_api","native"]))
    def test_unknown_commit(self):
        self.check_mutation("VERIFY", lambda r:r.update(commit_paths=[]))
    def test_missing_new_capture(self):
        self.check_mutation("NO_STRICT_COMPARISON", lambda r:r.update(new_capture_sha=None))
    def test_full_synthetic(self):
        self.assertEqual(gate(self.base()), "SYNTHETIC_SCHEMA_ONLY")
    def test_schema_cannot_issue_match(self):
        r = self.base(); r["synthetic"] = False
        self.assertEqual(gate(r), "ELIGIBLE_FOR_REVIEW_NOT_MATCH")

if __name__ == "__main__":
    unittest.main()
