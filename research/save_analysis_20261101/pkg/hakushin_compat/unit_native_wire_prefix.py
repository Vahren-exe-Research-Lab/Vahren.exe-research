"""Corrected native-wire Unit prefix for ver0.67 normal save.

This is a safe companion to unit_runtime_prefix.py, which remains
untouched due to shared ownership. Saved assembly proves writer
0x4708A0 MOVZX AL then writes SIZE=4 via 0x4628F0
(T014_RECORD_CODEC_PROBE.txt 0x4708A0..0x4708C2).
Thus each Unit+0x74..0x7A and Unit+0xE8 byte in memory occupies
a full UINT32LE in the save stream, not one byte.

Uses the shared UnitPrelude typed memory fields/validated strings and
native 0x58EFD0/0x58E870 order, but does NOT model the Unit+0x130
RB tree, arbeit, item_skill or rest of the Unit object.
"""
from __future__ import annotations

from struct import pack,unpack_from

from .unit_runtime_prefix import (
    UnitPrelude,UnitPrefixError,HEADER_LAYOUT,_zread,
)

MAX_ITEMS_PER_VECTOR=100000


def write_unit_native_wire_prefix(item:UnitPrelude)->bytes:
    if not isinstance(item,UnitPrelude):
        raise UnitPrefixError("typed UnitPrelude required")
    out=bytearray()
    for kind,field in HEADER_LAYOUT:
        if kind=="z":
            out+=item.strings[field]+b"\x00"
        elif kind=="dw":
            out+=pack("<I",item.dwords[field])
        else:
            out+=pack("<I",item.flags_74_to_7a[field-0x74])
    for n,group in enumerate(item.string_vectors):
        for raw in group:
            out+=raw+b"\x00"
        out+=b"\x00"
        if n==0:
            out+=pack("<I",item.dwords[0xE4])
            out+=pack("<I",item.flag_e8)
    return bytes(out)


def read_unit_native_wire_prefix(raw:bytes,*,offset:int=0)->tuple[UnitPrelude,int]:
    if type(raw) is not bytes or type(offset) is not int or not 0<=offset<=len(raw):
        raise UnitPrefixError("binary input and valid offset required")
    pos=offset
    strings={}
    dwords={}
    flags=bytearray(7)
    for kind,field in HEADER_LAYOUT:
        if kind=="z":
            strings[field],pos=_zread(raw,pos)
        else:
            if pos+4>len(raw):
                raise UnitPrefixError("native u32 read truncated")
            val=unpack_from("<I",raw,pos)[0]
            pos+=4
            if kind=="dw":
                dwords[field]=val
            else:
                if val>0xff:
                    raise UnitPrefixError("byte stored as native u32 out of range")
                flags[field-0x74]=val
    groups=[]
    flag_e8=None
    for n in range(4):
        members=[]
        for _ in range(MAX_ITEMS_PER_VECTOR):
            value,pos=_zread(raw,pos)
            if not value:break
            members.append(value)
        else:
            raise UnitPrefixError("unbounded native string vector")
        groups.append(tuple(members))
        if n==0:
            if pos+8>len(raw):
                raise UnitPrefixError("truncated +E4 int32 and +E8 encoded u32")
            dwords[0xE4]=unpack_from("<I",raw,pos)[0]
            flag_e8=unpack_from("<I",raw,pos+4)[0]
            pos+=8
            if flag_e8>0xff:
                raise UnitPrefixError("+E8 memory-byte encoded u32 >255")
    return UnitPrelude(strings,dwords,bytes(flags),flag_e8,tuple(groups)),pos

