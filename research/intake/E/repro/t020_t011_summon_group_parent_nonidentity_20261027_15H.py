"""E T020: B15 summon source/group is not a proven parent or G2 roster.
SYNTHETIC ONLY; original gameplay and Golden comparisons are NOT RUN.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B_DETAIL = ROOT / "data/T011_SUMMON_CALLER_GROUP_PROVENANCE_NATIVE_20261027_15H.md"
B_SHA = "FCC6CA977366126DEDC22D025B7FE25429DFBE83C59D9C41DEAB52A4B465B48D"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
CALLERS = {"0x54DF4B", "0x550219", "0x57F484", "0x57F492"}
HEX64 = re.compile(r"[0-9a-fA-F]{64}\Z")


def sample(**kw):
    x = dict(source_sha256=EXE_SHA, origin="B_STATIC_ASM", run_id="synthetic-r1",
             generation=1, caller_va="0x54DF4B", source_ptr="S1", holder_ptr="H1",
             effect_source_ptr="S1", group_ptr="G1", child_ptr="C1",
             child_creation_phase="IN_BATTLE", parent_id=None, parent_receipt_sha256=None,
             synthetic=True)
    return dict(x, **kw)
def review(entries):
    """Classification only. No input grants a verified parent or gameplay parity."""
    issues = set()
    if not isinstance(entries, list) or not entries:
        issues.add("NO_VALID_CASES")
        entries = []
    groups, pointers = {}, {}
    for e in entries:
        if not isinstance(e, dict):
            issues.add("INVALID_CASE")
            continue
        if e.get("source_sha256") != EXE_SHA:
            issues.add("EXE_SOURCE_MISMATCH")
        if e.get("caller_va") not in CALLERS:
            issues.add("UNMAPPED_CALLER")
        if e.get("source_ptr") != e.get("effect_source_ptr"):
            issues.add("STATIC_SOURCE_EFFECT_FLOW_CONFLICT")
        if e.get("child_creation_phase") == "IN_BATTLE":
            issues.add("POST_G2_CHILD_NOT_INITIAL_DEPLOYMENT")
        elif e.get("child_creation_phase") != "PRE_BATTLE":
            issues.add("CHILD_PHASE_UNVERIFIED")
        parent = e.get("parent_id")
        if parent is None:
            issues.add("PARENT_ID_UNPROVEN")
        else:
            proof = e.get("parent_receipt_sha256")
            if not isinstance(proof, str) or not HEX64.fullmatch(proof):
                issues.add("PARENT_LABEL_WITHOUT_VALID_RECEIPT_DIGEST")
            issues.add("PARENT_LABEL_REQUIRES_ORIGINAL_BYTE_ATTESTATION")
        if e.get("origin") != "LEGAL_ORIGINAL_RUNTIME" or e.get("synthetic", True):
            issues.add("NOT_ORIGINAL_RUNTIME_PROVENANCE")
        group = e.get("group_ptr")
        epoch = (e.get("run_id"), e.get("generation"))
        if group is not None:
            groups.setdefault((*epoch, group), set()).add(e.get("source_ptr"))
        ptr = e.get("source_ptr")
        if ptr is not None:
            pointers.setdefault(ptr, set()).add(epoch)
    if any(len(sources) > 1 for sources in groups.values()):
        issues.add("GROUP_SHARED_BY_DISTINCT_SOURCES")
    if any(len(epochs) > 1 for epochs in pointers.values()):
        issues.add("SOURCE_POINTER_REUSED_ACROSS_EPOCHS")
    return {"issues": sorted(issues), "verdict": "REVIEW_ONLY_NOT_GOLDEN",
            "actual_golden_pass": False, "strict_match": False}


class SummonSourceGroupRegressions(unittest.TestCase):
    def check(self, rows, flags=()):
        original = repr(rows)
        out = review(rows)
        self.assertEqual(repr(rows), original)
        self.assertEqual(out["verdict"], "REVIEW_ONLY_NOT_GOLDEN")
        self.assertFalse(out["actual_golden_pass"])
        self.assertFalse(out["strict_match"])
        for flag in flags:
            self.assertIn(flag, out["issues"])
        return out

    def test_01_b_owner_source_bytes_are_pinned(self):
        self.assertEqual(hashlib.sha256(B_DETAIL.read_bytes()).hexdigest().upper(), B_SHA)

    def test_02_static_source_effect_equality_is_not_parent(self):
        self.check([sample()], ["PARENT_ID_UNPROVEN", "NOT_ORIGINAL_RUNTIME_PROVENANCE"])

    def test_03_group_shared_by_two_sources_is_nonunique(self):
        a, b = sample(), sample(source_ptr="S2", effect_source_ptr="S2", child_ptr="C2")
        self.check([a, b], ["GROUP_SHARED_BY_DISTINCT_SOURCES"])

    def test_04_two_groups_does_not_establish_two_parents(self):
        a, b = sample(), sample(group_ptr="G2", child_ptr="C2")
        o = self.check([a, b], ["PARENT_ID_UNPROVEN"])
        self.assertNotIn("GROUP_SHARED_BY_DISTINCT_SOURCES", o["issues"])

    def test_05_group_null_is_optional_not_negative_parent_evidence(self):
        self.check([sample(group_ptr=None)], ["PARENT_ID_UNPROVEN"])
    def test_06_cross_run_group_address_not_merged(self):
        a, b = sample(), sample(run_id="synthetic-r2", source_ptr="S2",
                               effect_source_ptr="S2", child_ptr="C2")
        out = self.check([a, b])
        self.assertNotIn("GROUP_SHARED_BY_DISTINCT_SOURCES", out["issues"])

    def test_07_source_address_across_generation_is_not_identity(self):
        self.check([sample(), sample(generation=2, child_ptr="C2")],
                   ["SOURCE_POINTER_REUSED_ACROSS_EPOCHS"])

    def test_08_bad_caller_is_not_a_known_static_entry(self):
        self.check([sample(caller_va="0x123456")], ["UNMAPPED_CALLER"])

    def test_09_source_exe_mismatch_fails_closed(self):
        self.check([sample(source_sha256="0" * 64)], ["EXE_SOURCE_MISMATCH"])

    def test_10_effect_pointer_flow_conflict(self):
        self.check([sample(effect_source_ptr="S2")], ["STATIC_SOURCE_EFFECT_FLOW_CONFLICT"])

    def test_11_unattested_parent_label_is_not_proof(self):
        self.check([sample(parent_id="PARENT1")],
                   ["PARENT_LABEL_WITHOUT_VALID_RECEIPT_DIGEST"])

    def test_12_plausible_digest_still_not_byte_attestation(self):
        self.check([sample(parent_id="PARENT1", parent_receipt_sha256="a" * 64,
                           origin="LEGAL_ORIGINAL_RUNTIME", synthetic=False)],
                   ["PARENT_LABEL_REQUIRES_ORIGINAL_BYTE_ATTESTATION"])

    def test_13_summoned_child_not_in_initial_g2_roster(self):
        self.check([sample()], ["POST_G2_CHILD_NOT_INITIAL_DEPLOYMENT"])

    def test_14_null_and_malformed_cases_fail_closed(self):
        self.check(None, ["NO_VALID_CASES"])
        self.check([None], ["INVALID_CASE"])


if __name__ == "__main__":
    unittest.main(verbosity=2)