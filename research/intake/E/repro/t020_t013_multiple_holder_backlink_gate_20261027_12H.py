"""E-owned T020: B-12H multiple holder backlink is not Unit holder proof."""
import hashlib
import unittest
from pathlib import Path

EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
B_DOC_SHA = "2C4DA4C87D0830B1747A87003F673D41B1B65E39B2B66AB81DED9C4D197F5126"
MAIN = 0x008BE2F0
KNOWN = {"Hwin": 0x008BE378, "Hscene": 0x008BE7F4, "Haux": 0x00AAD7A4}
TICK_MANAGER = MAIN + 0xC

def decide(c):
    """Conditional gate only; never a Golden result."""
    if c["exe_sha"] != EXE_SHA:
        return "SOURCE_MISMATCH"
    if not c["initialized"]:
        return "INIT_PHASE_UNKNOWN"
    if c["holder"] not in KNOWN:
        return "UNKNOWN_HOLDER_FAMILY"
    if c["backlink"] != MAIN:
        return "BACKLINK_NOT_MAIN"
    if c["unit_holder"] is None:
        return "UNIT_HOLDER_NOT_PROVEN"
    if c["unit_holder"] != KNOWN[c["holder"]]:
        return "UNIT_HOLDER_MISMATCH"
    if not c["session"]:
        return "SESSION_NOT_BOUND"
    if c["creator_generation"] is None or c["tick_generation"] is None:
        return "GENERATION_UNKNOWN"
    if c["creator_generation"] != c["tick_generation"]:
        return "GENERATION_MISMATCH"
    if not c["runtime_observed"]:
        return "SYNTHETIC_ALIAS_ONLY"
    return "REVIEW_ONLY_NOT_GOLDEN"

def case(**changes):
    d = dict(exe_sha=EXE_SHA, initialized=True, holder="Hwin",
             backlink=MAIN, unit_holder=KNOWN["Hwin"], session="synthetic-run",
             creator_generation=1, tick_generation=1, runtime_observed=False)
    d.update(changes)
    return d

class MultipleHolderGate(unittest.TestCase):
    def test_b12_document_bytes(self):
        root = Path(__file__).resolve().parent.parent
        source = root / "data" / "T013_GAMEMANAGER_GLOBAL_BACKLINKS_NATIVE_20261027_12H.md"
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest().upper(), B_DOC_SHA)

    def test_static_backlinks_are_many_to_one(self):
        self.assertEqual(len(set(KNOWN.values())), 3)
        self.assertEqual({MAIN + 0xC for _ in KNOWN}, {TICK_MANAGER})

    def test_static_receipt_lacks_unit_link(self):
        self.assertEqual(decide(case(unit_holder=None)), "UNIT_HOLDER_NOT_PROVEN")

    def test_each_holder_is_insufficient_without_unit_link(self):
        for name in KNOWN:
            with self.subTest(holder=name):
                self.assertEqual(decide(case(holder=name, unit_holder=None)),
                                 "UNIT_HOLDER_NOT_PROVEN")

    def test_uninitialized_backlink(self):
        self.assertEqual(decide(case(initialized=False)), "INIT_PHASE_UNKNOWN")

    def test_different_backlink(self):
        self.assertEqual(decide(case(backlink=MAIN + 4)), "BACKLINK_NOT_MAIN")

    def test_wrong_unit_holder(self):
        self.assertEqual(decide(case(unit_holder=KNOWN["Haux"])), "UNIT_HOLDER_MISMATCH")

    def test_missing_session(self):
        self.assertEqual(decide(case(session=None)), "SESSION_NOT_BOUND")

    def test_missing_generation(self):
        self.assertEqual(decide(case(creator_generation=None)), "GENERATION_UNKNOWN")

    def test_reused_pointer_generation(self):
        self.assertEqual(decide(case(tick_generation=2)), "GENERATION_MISMATCH")

    def test_synthetic_alias_not_dynamic(self):
        self.assertEqual(decide(case()), "SYNTHETIC_ALIAS_ONLY")

    def test_runtime_claim_not_gold(self):
        self.assertEqual(decide(case(runtime_observed=True)), "REVIEW_ONLY_NOT_GOLDEN")

    def test_unknown_holder_not_ruled_out(self):
        self.assertEqual(decide(case(holder="Hnew")), "UNKNOWN_HOLDER_FAMILY")

    def test_different_exe_baseline(self):
        self.assertEqual(decide(case(exe_sha="0" * 64)), "SOURCE_MISMATCH")

    def test_manager_address_arithmetic(self):
        self.assertEqual(TICK_MANAGER, 0x008BE2FC)

if __name__ == "__main__":
    unittest.main(verbosity=2)
