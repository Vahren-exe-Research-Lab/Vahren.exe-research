"""Complete *writer-shaped* Unit record/group byte codec for Vahren 0.67.

Confirmed from saved 0x58EFD0..0x58F7B2 assembly and 0x58E870
reader entry, plus actual save1/save2/auto.sav captures. This is an
ordered byte reconstruction, not the runtime Unit class implementation.
All dwords are UNINTERPRETED raw uint32; names are opaque ASCII bytes.

The original Unit memory flags +0x74..0x7A, +0xE8 occupy one byte in
RAM, but 0x4708A0 emits *four* bytes on disk. See unit_native_wire_prefix.

Source order:
 map-key; Unit prefix; +0x130 key/u32 tree till "@@@@";
 "arbeit"+Unit+7C u32; "arbeit_user"+Unit+A0 string;
 "item_skill"+Unit+11C vector till empty; "friend"+Unit+15C
 tree of string keys till empty; "@@@@" marker; Unit+13C string;
 fourteen final raw dwords in the exact native call sequence.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from struct import pack,unpack_from

from .real_save_frontmatter import _read_native_ascii_z
from .save_envelope import SaveFormatError,TERMINATOR
from .unit_native_wire_prefix import (
    read_unit_native_wire_prefix,write_unit_native_wire_prefix
)
from .unit_runtime_prefix import UnitPrelude

MAX_UNIT_RECORDS=20000
MAX_MEMBER_RECORDS=10000
FIRST_TREE_END=b"@@@@\x00"
TAG_ARBEIT=b"arbeit\x00"
TAG_ARBEIT_USER=b"arbeit_user\x00"
TAG_ITEM_SKILL=b"item_skill\x00"
TAG_FRIEND=b"friend\x00"
# Raw tail DWORD order from writer 0x58F659..0x58F7B2, not struct order.
TAIL_OFFSETS=(0x168,0x16C,0x170,0x178,0x17C,0x180,0x184,
              0x188,0x18C,0x194,0x190,0x198,0x19C,0x1A0)


def _take_u32(blob:bytes,idx:int)->tuple[int,int]:
    if idx+4>len(blob):
        raise SaveFormatError("truncated native Unit dword")
    return unpack_from("<I",blob,idx)[0],idx+4


def _must_consume(blob:bytes,at:int,tag:bytes)->int:
    if blob[at:at+len(tag)]!=tag:
        raise SaveFormatError("Unit missing mandatory native tag "+repr(tag))
    return at+len(tag)


def _native_str(b:bytes,*,allow_empty:bool=False)->bytes:
    if type(b) is not bytes or (not allow_empty and not b):
        raise SaveFormatError("Unit field requires native string bytes")
    if len(b)>65536 or any(c<0x20 or c>0x7f for c in b):
        raise SaveFormatError("Unit string outside verified printable ASCII")
    return b


def _read_terminated_vector(blob:bytes,pos:int,*,marker:bytes=b"")->tuple[tuple[bytes,...],int]:
    values=[]
    for _ in range(MAX_MEMBER_RECORDS):
        key,pos=_read_native_ascii_z(blob,pos)
        if key==marker:return tuple(values),pos
        if not key:raise SaveFormatError("empty Unit string entry not allowed")
        values.append(key)
    raise SaveFormatError("Unit vector did not terminate")


@dataclass(frozen=True,slots=True)
class NativeFullUnitRecord:
    key:bytes
    prelude:UnitPrelude
    tree_130:tuple[tuple[bytes,int],...]
    arbeit_7c_u32:int
    arbeit_user_a0:bytes
    item_skill_11c:tuple[bytes,...]
    friend_15c:tuple[bytes,...]
    string_13c:bytes
    tail_dwords:tuple[int,...]

    def pack(self)->bytes:
        key=_native_str(self.key)
        if key==TERMINATOR[:-1]:
            raise SaveFormatError("Unit key collides with outer delimiter")
        result=bytearray(key+b"\x00")
        result+=write_unit_native_wire_prefix(self.prelude)
        for k,n in self.tree_130:
            if _native_str(k)==FIRST_TREE_END[:-1]:
                raise SaveFormatError("reserved first Unit tree marker")
            if type(n) is not int or not 0<=n<=0xffffffff:
                raise SaveFormatError("Unit +130 tree requires raw u32")
            result+=k+b"\x00"+pack("<I",n)
        result+=FIRST_TREE_END
        if type(self.arbeit_7c_u32) is not int or not 0<=self.arbeit_7c_u32<=0xffffffff:
            raise SaveFormatError("arbeit Unit+7C requires raw u32")
        result+=TAG_ARBEIT+pack("<I",self.arbeit_7c_u32)
        result+=TAG_ARBEIT_USER+_native_str(self.arbeit_user_a0,allow_empty=True)+b"\x00"
        result+=TAG_ITEM_SKILL
        for item in self.item_skill_11c:
            result+=_native_str(item)+b"\x00"
        result+=b"\x00"
        result+=TAG_FRIEND
        for name in self.friend_15c:
            result+=_native_str(name)+b"\x00"
        result+=b"\x00"+FIRST_TREE_END
        result+=_native_str(self.string_13c,allow_empty=True)+b"\x00"
        if len(self.tail_dwords)!=len(TAIL_OFFSETS):
            raise SaveFormatError("Unit post-marker requires 14 raw dwords")
        for field in self.tail_dwords:
            if type(field) is not int or not 0<=field<=0xffffffff:
                raise SaveFormatError("invalid Unit tail raw uint32")
            result+=pack("<I",field)
        return bytes(result)

def read_native_full_unit_record(
    blob:bytes,*,offset:int=0
)->tuple[NativeFullUnitRecord,int]:
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("bounded bytes and start offset required")
    name,pos=_read_native_ascii_z(blob,offset)
    if not name or name==TERMINATOR[:-1]:
        raise SaveFormatError("not a concrete native Unit record")
    prelude,pos=read_unit_native_wire_prefix(blob,offset=pos)
    entries=[]
    for _ in range(MAX_MEMBER_RECORDS):
        key,pos=_read_native_ascii_z(blob,pos)
        if key==FIRST_TREE_END[:-1]:
            break
        if not key:
            raise SaveFormatError("unexpected empty Unit+0x130 tree key")
        value,pos=_take_u32(blob,pos)
        entries.append((key,value))
    else:
        raise SaveFormatError("Unit+0x130 tree unbounded")
    pos=_must_consume(blob,pos,TAG_ARBEIT)
    arbeit,pos=_take_u32(blob,pos)
    pos=_must_consume(blob,pos,TAG_ARBEIT_USER)
    user,pos=_read_native_ascii_z(blob,pos)
    pos=_must_consume(blob,pos,TAG_ITEM_SKILL)
    skill,pos=_read_terminated_vector(blob,pos)
    pos=_must_consume(blob,pos,TAG_FRIEND)
    friends,pos=_read_terminated_vector(blob,pos)
    pos=_must_consume(blob,pos,FIRST_TREE_END)
    string13c,pos=_read_native_ascii_z(blob,pos)
    vals=[]
    for _ in TAIL_OFFSETS:
        v,pos=_take_u32(blob,pos)
        vals.append(v)
    record=NativeFullUnitRecord(name,prelude,tuple(entries),arbeit,user,
                                skill,friends,string13c,tuple(vals))
    return record,pos


@dataclass(frozen=True,slots=True)
class UnitGroupByteProof:
    record_count:int
    distinct_names:int
    first_name:bytes|None
    last_name:bytes|None
    start_offset:int
    terminal_start:int
    end_offset:int
    full_record_byte_roundtrips:int
    raw_group_sha256:str


def validate_native_unit_group(blob:bytes,*,offset:int)->UnitGroupByteProof:
    """Walk original group's ENTIRE extent and roundtrip every Unit record."""
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("valid original decoded buffer and offset required")
    start=offset
    seen=set()
    first=last=None
    for i in range(MAX_UNIT_RECORDS):
        if blob[offset:offset+len(TERMINATOR)]==TERMINATOR:
            end=offset+len(TERMINATOR)
            return UnitGroupByteProof(
                i,len(seen),first,last,start,offset,end,i,
                sha256(blob[start:end]).hexdigest(),
            )
        entry,end=read_native_full_unit_record(blob,offset=offset)
        if entry.pack()!=blob[offset:end]:
            raise SaveFormatError("full Unit record writer roundtrip mismatch")
        if i==0:first=entry.key
        last=entry.key
        seen.add(entry.key)
        offset=end
    raise SaveFormatError("Unit group record ceiling or missing dash marker")

