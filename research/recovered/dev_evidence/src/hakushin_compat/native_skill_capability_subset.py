"""Original EXE *local* skill category and capability-flag assembly contracts.

Only saved native ranges 0x5739E4..0x573A48, 0x577843..0x577997.
A computed result is the local REGISTER/FLAG update of these branches,
not proof the original battle AI chooses, launches or executes that skill.

Skill+0x40 kinds 5/6 have special paths (including +0x130 pointer writer)
which MUST NOT be projected into the ordinary 1..4 flag writer.
0x577843 action dispatch is also entered under extra function preconditions
(kind+0x40==8, +0x120!=0); unknown/failing gates stay unverified.
"""
from __future__ import annotations

from dataclasses import dataclass


class NativeSkillContractUnknown(ValueError):
    """Insufficient native evidence to assert the requested local branch."""


NATIVE_FLAG_VA_START=0x5739E4
NATIVE_FLAG_VA_END=0x573A48
NATIVE_ACTION_VA_START=0x577843
NATIVE_ACTION_VA_END=0x577997

# These are raw byte *offsets* in Unit, not effective gameplay skill names.
ACTION_BRANCHES={
    "sword": (0x134,1,0),
    "bow": (0x135,2,0),
    "magic": (0x136,2,1),
    "heal": (0x137,3,0),
    "care": (0x137,3,1),
    "powerup": (0x137,3,2),
    "summon": (0x138,4,0),
}


@dataclass(frozen=True,slots=True)
class LocalCapabilityWrite:
    skill_kind_40:int
    written_unit_byte_offsets:tuple[int,...]
    field_278_nonzero:bool
    field_4c_positive:bool
    source_va_begin:int=NATIVE_FLAG_VA_START
    source_va_end:int=NATIVE_FLAG_VA_END
    original_native_execution_observed:bool=False
    full_skill_capabilities_reconstructed:bool=False


@dataclass(frozen=True,slots=True)
class LocalActionDispatch:
    action_name:str
    source_skill_kind_40:int
    required_unit_byte_offset:int
    written_kind_value:int
    written_subtype_value:int
    source_va_begin:int=NATIVE_ACTION_VA_START
    source_va_end:int=NATIVE_ACTION_VA_END
    actual_game_skill_invoked:bool=False
    effective_skill_set_resolved:bool=False


def _raw_s32(value:int,label:str)->int:
    if type(value) is not int or not -(1<<31)<=value<(1<<31):
        raise NativeSkillContractUnknown(label+" requires signed 32-bit raw value")
    return value


def one_resolved_skill_local_flag_writes(
    kind_40:int,raw_278:int,raw_4c:int
)->LocalCapabilityWrite:
    """Return only the Unit byte-offset writes of the saved x86 branch.

    Does not decide whether an original skill entered this scanner or
    whether a 1 at one offset remains in the *final* capability cache.
    """
    _raw_s32(kind_40,"Skill+0x40")
    _raw_s32(raw_278,"Skill+0x278")
    _raw_s32(raw_4c,"Skill+0x4C")
    # Kind 5 writes the first pointer at Unit+0x130 and kind 6 branches
    # past this ordinary scanner; stop instead of silently treating as zero.
    if kind_40 not in (1,2,3,4):
        raise NativeSkillContractUnknown(
            "only ordinary 1..4 native skill-kind flag paths are reconstructed"
        )
    target={
        1:0x134,
        2:0x136 if raw_278!=0 else 0x135,
        3:0x137,
        4:0x138,
    }[kind_40]
    offsets=(target,0x139) if raw_4c>0 else (target,)
    return LocalCapabilityWrite(
        kind_40,offsets,raw_278!=0,raw_4c>0
    )


def local_action_subtype_under_verified_preconditions(
    action_name:str,
    unit_capability_byte_offsets:tuple[int,...],
    *,
    skill_kind_40:int,
    field_120_nonzero:bool
)->LocalActionDispatch:
    """Assert result ONLY for 0x577843..997 success branches.

    This disassembly segment first checks Skill+0x40==8 and
    Skill+0x120!=0. Missing capability means branch FALLTHROUGH to
    0x577999 etc, not a proof of globally rejected action.
    """
    if (not isinstance(action_name,str)
            or not isinstance(unit_capability_byte_offsets,tuple)
            or any(type(v) is not int for v in unit_capability_byte_offsets)
            or type(field_120_nonzero) is not bool):
        raise NativeSkillContractUnknown("typed action and capability preconditions required")
    if skill_kind_40!=8 or not field_120_nonzero:
        raise NativeSkillContractUnknown(
            "0x577843 dispatch action gate is not satisfied"
        )
    if action_name not in ACTION_BRANCHES:
        raise NativeSkillContractUnknown(
            "action string has no saved confirmed subtype branch"
        )
    offset,kind,subtype=ACTION_BRANCHES[action_name]
    if offset not in unit_capability_byte_offsets:
        raise NativeSkillContractUnknown(
            "required Unit capability byte false: downstream fallback unknown"
        )
    return LocalActionDispatch(action_name,skill_kind_40,offset,kind,subtype)
