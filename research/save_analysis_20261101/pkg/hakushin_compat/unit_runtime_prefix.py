"""Unit runtime serialization prelude, verified by saved reader/writer pair.

Strictly prefix only: Ghidra 0x58EFD0 writer / 0x58E870 reader.
This is NOT the complete Unit, not a normal .sav wrapper, and cannot
parse RB-tree arbeit/item_skill/friend or the downstream 0x58E480 helper.
Values marked dword are raw unsigned 32-bit bit patterns, not verified
gameplay signedness. Unknown suffix bytes remain untouched.
"""
from __future__ import annotations
from dataclasses import dataclass
from struct import pack,unpack_from
from typing import Mapping

STR_OFFSETS=(0x00,0x1C,0x38,0x54,0x84)
DW_OFFSETS=(0x70,0x80,0xC8,0xCC,0x174,0xBC,0xC0,0xC4,0xD0,0xE4)
VECTOR_OFFSETS=((0xD4,0xD8),(0xEC,0xF0),(0xFC,0x100),(0x10C,0x110))
HEADER_LAYOUT=(("z",0x00),("z",0x1C),("dw",0x70),
               ("z",0x38),("z",0x54),
               *(("byte",o) for o in range(0x74,0x7B)),
               ("dw",0x80),("z",0x84),
               *(("dw",o) for o in (0xC8,0xCC,0x174,0xBC,0xC0,0xC4,0xD0)))

class UnitPrefixError(ValueError):
    pass

def _verified_bytes(raw:bytes,*,allow_empty:bool)->bytes:
    if type(raw) is not bytes or (not raw and not allow_empty):
        raise UnitPrefixError("expected verified nonempty bytes value")
    if any(b<0x20 or b>0x7F for b in raw):
        raise UnitPrefixError("unverified string collapses to empty sentinel")
    return raw

def _zread(raw:bytes,pos:int)->tuple[bytes,int]:
    end=raw.find(b"\x00",pos)
    if end<0 or end-pos>65536:
        raise UnitPrefixError("missing or excessive NUL string")
    value=raw[pos:end]
    _verified_bytes(value,allow_empty=True)
    return value,end+1

@dataclass(frozen=True,slots=True)
class UnitPrelude:
    strings:Mapping[int,bytes]
    dwords:Mapping[int,int]
    flags_74_to_7a:bytes
    flag_e8:int
    string_vectors:tuple[tuple[bytes,...],...]

    def __post_init__(self)->None:
        if set(self.strings)!=set(STR_OFFSETS):
            raise UnitPrefixError("five exact string offsets required")
        for field in self.strings.values():
            _verified_bytes(field,allow_empty=True)
        if set(self.dwords)!=set(DW_OFFSETS):
            raise UnitPrefixError("ten exact dword offsets required")
        for value in self.dwords.values():
            if type(value) is not int or not 0<=value<=0xFFFFFFFF:
                raise UnitPrefixError("raw dword must be uint32")
        if type(self.flags_74_to_7a) is not bytes or len(self.flags_74_to_7a)!=7:
            raise UnitPrefixError("exactly 7 raw flags required")
        if type(self.flag_e8) is not int or not 0<=self.flag_e8<=0xFF:
            raise UnitPrefixError("raw +0xE8 flag is one byte")
        if len(self.string_vectors)!=4:
            raise UnitPrefixError("four ordered string vectors required")
        for group in self.string_vectors:
            for value in group:
                _verified_bytes(value,allow_empty=False)

def write_unit_prelude(obj:UnitPrelude)->bytes:
    result=bytearray()
    for kind,offset in HEADER_LAYOUT:
        if kind=="z":result+=obj.strings[offset]+b"\x00"
        elif kind=="dw":result+=pack("<I",obj.dwords[offset])
        else:result.append(obj.flags_74_to_7a[offset-0x74])
    for n,group in enumerate(obj.string_vectors):
        for value in group:result+=value+b"\x00"
        result+=b"\x00"  # no count, only an empty string terminator
        if n==0:
            result+=pack("<I",obj.dwords[0xE4])
            result.append(obj.flag_e8)
    return bytes(result)

def read_unit_prelude(raw:bytes,*,offset:int=0)->tuple[UnitPrelude,int]:
    if not isinstance(raw,bytes) or not 0<=offset<=len(raw):
        raise UnitPrefixError("bad raw input or starting offset")
    pos=offset
    strings:dict[int,bytes]={}
    dwords:dict[int,int]={}
    flags=bytearray(7)
    for kind,field in HEADER_LAYOUT:
        if kind=="z":
            strings[field],pos=_zread(raw,pos)
        elif kind=="dw":
            if len(raw)-pos<4:raise UnitPrefixError("truncated header dword")
            dwords[field]=unpack_from("<I",raw,pos)[0]
            pos+=4
        else:
            if pos>=len(raw):raise UnitPrefixError("truncated header flag")
            flags[field-0x74]=raw[pos]
            pos+=1
    groups:list[tuple[bytes,...]]=[]
    flag_e8=-1
    for n in range(4):
        values:list[bytes]=[]
        for _ in range(100000):
            value,pos=_zread(raw,pos)
            if not value:break
            values.append(value)
        else:raise UnitPrefixError("vector exceeds conservative item limit")
        groups.append(tuple(values))
        if n==0:
            if len(raw)-pos<5:raise UnitPrefixError("truncated +E4/+E8")
            dwords[0xE4]=unpack_from("<I",raw,pos)[0]
            flag_e8=raw[pos+4]
            pos+=5
    return UnitPrelude(strings,dwords,bytes(flags),flag_e8,tuple(groups)),pos
