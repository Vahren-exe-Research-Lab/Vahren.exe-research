"""Local native x86 Skill kind/capability contract, NOT full action parity."""
import unittest
from dataclasses import FrozenInstanceError

from hakushin_compat.native_skill_capability_subset import (
    NativeSkillContractUnknown,ACTION_BRANCHES,
    one_resolved_skill_local_flag_writes,
    local_action_subtype_under_verified_preconditions,
)


class TestOneSkillNativeFlagWrite(unittest.TestCase):
    def test_kind_1_sword_bit_and_optional_positive_4c(self):
        self.assertEqual(
            one_resolved_skill_local_flag_writes(1,0,0).written_unit_byte_offsets,
            (0x134,)
        )
        self.assertEqual(
            one_resolved_skill_local_flag_writes(1,0,1).written_unit_byte_offsets,
            (0x134,0x139)
        )
        self.assertEqual(
            one_resolved_skill_local_flag_writes(1,0,-1).written_unit_byte_offsets,
            (0x134,)
        )

    def test_kind_2_separates_bow_from_magic_using_raw_278_nonzero(self):
        self.assertEqual(
            one_resolved_skill_local_flag_writes(2,0,0).written_unit_byte_offsets,
            (0x135,)
        )
        for value in (-1,1,2147483647,-2147483648):
            with self.subTest(raw278=value):
                self.assertEqual(
                    one_resolved_skill_local_flag_writes(
                        2,value,0).written_unit_byte_offsets,(0x136,)
                )

    def test_kind_3_and_4_use_distinct_supported_offsets(self):
        self.assertEqual(
            one_resolved_skill_local_flag_writes(3,0,0).written_unit_byte_offsets,
            (0x137,)
        )
        self.assertEqual(
            one_resolved_skill_local_flag_writes(4,0,0).written_unit_byte_offsets,
            (0x138,)
        )

    def test_kind_5_pointer_and_kind_6_skip_not_collapsed(self):
        for kind in (0,5,6,7,-1,8):
            with self.subTest(kind=kind),self.assertRaises(NativeSkillContractUnknown):
                one_resolved_skill_local_flag_writes(kind,0,100)

    def test_invalid_register_width_and_python_bool_rejected(self):
        for arguments in (
            (1,0,1<<31), (2,-(1<<31)-1,0), (1<<32,0,0),
            (True,0,0),(1,False,0),(1,0,False),
        ):
            with self.subTest(args=arguments),self.assertRaises(NativeSkillContractUnknown):
                one_resolved_skill_local_flag_writes(*arguments)

    def test_returned_contract_does_not_claim_runtime_execution(self):
        result=one_resolved_skill_local_flag_writes(3,1,5)
        self.assertFalse(result.original_native_execution_observed)
        self.assertFalse(result.full_skill_capabilities_reconstructed)
        self.assertEqual(result.written_unit_byte_offsets,(0x137,0x139))
        self.assertEqual(result.source_va_begin,0x5739E4)
        with self.assertRaises(FrozenInstanceError):
            result.full_skill_capabilities_reconstructed=True


class TestNativeActionSubtype(unittest.TestCase):
    def action(self,name,flags):
        return local_action_subtype_under_verified_preconditions(
            name,flags,skill_kind_40=8,field_120_nonzero=True,
        )

    def test_all_seven_action_subtype_success_branches(self):
        for name,(offset,kind,subtype) in ACTION_BRANCHES.items():
            with self.subTest(name=name):
                hit=self.action(name,(offset,))
                self.assertEqual(hit.required_unit_byte_offset,offset)
                self.assertEqual((hit.written_kind_value,hit.written_subtype_value),
                                 (kind,subtype))
                self.assertFalse(hit.actual_game_skill_invoked)
                self.assertFalse(hit.effective_skill_set_resolved)

    def test_heal_care_powerup_share_137_but_keep_subtype(self):
        results=[self.action(kind,(0x137,)) for kind in ("heal","care","powerup")]
        self.assertEqual({a.required_unit_byte_offset for a in results},{0x137})
        self.assertEqual([a.written_subtype_value for a in results],[0,1,2])

    def test_failing_capability_is_unknown_fallthrough_not_global_false(self):
        for name,(offset,_,_) in ACTION_BRANCHES.items():
            with self.subTest(name=name),self.assertRaisesRegex(
                NativeSkillContractUnknown,"fallback unknown"):
                self.action(name,())

    def test_preconditions_skill_8_and_field_120_are_explicit(self):
        for kind,g in ((0,True),(7,True),(8,False),(9,True)):
            with self.subTest(kind=kind,field=g),self.assertRaises(
                NativeSkillContractUnknown):
                local_action_subtype_under_verified_preconditions(
                    "sword",(0x134,),skill_kind_40=kind,field_120_nonzero=g
                )

    def test_unknown_action_strictly_not_invented(self):
        for name in ("", "sword2", "attack", "heal2", "sUmMoN", "move"):
            with self.subTest(name=name),self.assertRaises(
                NativeSkillContractUnknown):
                self.action(name,(0x134,0x135,0x136,0x137,0x138))

    def test_wrong_capabilities_and_untyped_gate_rejected(self):
        for options in ((0x134,), [0x134], (True,), (0x137,"bad")):
            if isinstance(options,tuple) and len(options)==1 and options[0]==0x134:
                continue
            with self.subTest(flags=options),self.assertRaises(NativeSkillContractUnknown):
                self.action("sword",options)
        with self.assertRaises(NativeSkillContractUnknown):
            local_action_subtype_under_verified_preconditions(
                "sword",(0x134,),skill_kind_40=8,field_120_nonzero=1)

if __name__=="__main__":
    unittest.main()
