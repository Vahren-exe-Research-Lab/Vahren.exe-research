"""E-owned synthetic contract test; NOT old-EXE execution or native result."""
# Based on B-20261027-07H-T013-SUPPORT-EFFECT-DISPATCH-VISUAL-BYPASS-01.
import unittest

def synthetic_support(actor, skill, candidate, display_branch, outcome, abort=False):
    """Only models B's normal-flow join: VFX optional; effect CALL is separate."""
    assert outcome in ("early", "change")
    record = {"visual": [], "effect_calls": [], "hp_delta": 0,
              "flag": None, "valid_old_capture": False}
    if abort:
        return record  # synthetic interruption before join, not native claim
    if display_branch:
        record["visual"].append("register_attempt")
        record["flag"] = 1
    else:
        record["flag"] = 0x0101
    context = (actor, skill)
    record["effect_calls"].append((context, candidate))
    if outcome == "change":
        record["hp_delta"] = 5  # toy example, NOT original HP rule
    return record

class SupportEffectAdmission(unittest.TestCase):
    def setUp(self):
        self.actor = object()
        self.skill = object()
        self.candidate = object()

    def call(self, visual=False, outcome="early", abort=False):
        return synthetic_support(self.actor, self.skill, self.candidate,
                                 visual, outcome, abort)

    def test_no_visual_still_invokes_core(self):
        self.assertEqual(len(self.call(False)["effect_calls"]), 1)

    def test_visual_also_invokes_core(self):
        self.assertEqual(len(self.call(True)["effect_calls"]), 1)

    def test_no_visual_sets_distinct_branch_flag(self):
        r = self.call(False)
        self.assertEqual(r["flag"], 0x0101)
        self.assertFalse(r["visual"])

    def test_visual_branch_does_not_prove_visible_vfx(self):
        self.assertEqual(self.call(True)["visual"], ["register_attempt"])

    def test_actor_and_skill_context_forwarded(self):
        ctx, _ = self.call()["effect_calls"][0]
        self.assertIs(ctx[0], self.actor)
        self.assertIs(ctx[1], self.skill)

    def test_candidate_reference_forwarded(self):
        _, candidate = self.call()["effect_calls"][0]
        self.assertIs(candidate, self.candidate)

    def test_core_call_not_equal_hp_change(self):
        r = self.call(False, "early")
        self.assertEqual(len(r["effect_calls"]), 1)
        self.assertEqual(r["hp_delta"], 0)

    def test_synthetic_change_independent_of_visual(self):
        self.assertEqual(self.call(False, "change")["hp_delta"],
                         self.call(True, "change")["hp_delta"])

    def test_interruption_before_join_is_unverified(self):
        r = self.call(True, "early", abort=True)
        self.assertEqual(r["effect_calls"], [])
        self.assertIsNone(r["flag"])

    def test_effect_target_is_not_deployed_roster(self):
        r = self.call(True)
        self.assertFalse(r["valid_old_capture"])
        self.assertNotIn("deployed_roster", r)

if __name__ == "__main__":
    unittest.main(verbosity=2)
