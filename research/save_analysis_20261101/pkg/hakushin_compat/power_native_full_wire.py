"""Native 0.67 Power save *wire* reader/writer from original assembly.

Saved writer 0x596AA0..0x597091, reader 0x5964C0 still has possible
mode-specific side effects not reproduced. This reconstructs literal
save bytes, not running Unit/Spot/Power objects in a playable engine.

Fields: registry key; strings +00; byte flags +1C/+1D each UINT32LE;
dword+5C; strings +24/+40; dwords +20/+60; string +74;
+68 name tree (empty-delimited), +90 name vector (empty-delimited),
+A4 name tree (empty-delimited); +B4 key/rawDWORD pairs until
"fixtype" *without preceding empty-string marker*, four tagged DWORDs,
"home_spot" names, two adjacent empty-string markers.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from struct import pack,unpack_from

from .real_save_frontmatter import _read_native_ascii_z
from .save_envelope import SaveFormatError,TERMINATOR
from .power_runtime_writer_tail import (
    PowerTaggedTail, write_power_tail,read_power_tail_synthetic,
)

MAX_RECORDS=1000
MAX_NESTED_ENTRIES=10000


def _u32(n:int,where:str)->int:
    if type(n) is not int or not 0<=n<=0xffffffff:
        raise SaveFormatError(where+": unsigned native DWORD required")
    return n


def _str(n:bytes,where:str,*,allow_empty:bool=True)->bytes:
    if type(n) is not bytes or len(n)>65536:
        raise SaveFormatError(where+": byte native string required")
    if not allow_empty and not n:
        raise SaveFormatError(where+": nonempty native string required")
    if any(byte<0x20 or byte>0x7f for byte in n):
        raise SaveFormatError(where+": not native printable ASCII")
    return n


def _next_u32(blob:bytes,at:int)->tuple[int,int]:
    if at+4>len(blob):
        raise SaveFormatError("Power raw dword truncated")
    return unpack_from("<I",blob,at)[0],at+4


def _str_vector(blob:bytes,at:int)->tuple[tuple[bytes,...],int]:
    out=[]
    for _ in range(MAX_NESTED_ENTRIES):
        value,at=_read_native_ascii_z(blob,at)
        if not value:
            return tuple(out),at
        out.append(value)
    raise SaveFormatError("Power string collection missing terminator")


@dataclass(frozen=True,slots=True)
class NativePowerRecord:
    key:bytes
    name00:bytes
    byte_1c:int
    byte_1d:int
    dword_5c:int
    name24:bytes
    name40:bytes
    dword_20:int
    dword_60:int
    name74:bytes
    tree68_names:tuple[bytes,...]
    vector90_names:tuple[bytes,...]
    treea4_names:tuple[bytes,...]
    treeb4_pairs:tuple[tuple[bytes,int],...]
    tail:PowerTaggedTail

    def pack(self)->bytes:
        out=bytearray(_str(self.key,"Power registry key",allow_empty=False)+b"\x00")
        if self.key==TERMINATOR[:-1]:
            raise SaveFormatError("Power key collides with outer marker")
        out+=_str(self.name00,"Power+0")+b"\x00"
        for name,x in (("+1C",self.byte_1c),("+1D",self.byte_1d)):
            if _u32(x,name)>255:
                raise SaveFormatError("byte-in-RAM must fit 8 bits")
            out+=pack("<I",x)
        out+=pack("<I",_u32(self.dword_5c,"Power+5C"))
        for value,where in ((self.name24,"+24"),(self.name40,"+40")):
            out+=_str(value,where)+b"\x00"
        out+=pack("<I",_u32(self.dword_20,"Power+20"))
        out+=pack("<I",_u32(self.dword_60,"Power+60"))
        out+=_str(self.name74,"Power+74")+b"\x00"
        for field,values in (("Power+68",self.tree68_names),
                             ("Power+90",self.vector90_names),
                             ("Power+A4",self.treea4_names)):
            if len(values)>MAX_NESTED_ENTRIES:
                raise SaveFormatError("unbounded native Power collection")
            for val in values:
                out+=_str(val,field,allow_empty=False)+b"\x00"
            out+=b"\x00"
        if len(self.treeb4_pairs)>MAX_NESTED_ENTRIES:
            raise SaveFormatError("unbounded Power+B4 tree")
        for key,val in self.treeb4_pairs:
            field=_str(key,"Power+B4",allow_empty=False)
            if field==b"fixtype":
                raise SaveFormatError("reserved fixtype sentinel in Power+B4")
            out+=field+b"\x00"+pack("<I",_u32(val,"Power+B4 value"))
        if not isinstance(self.tail,PowerTaggedTail):
            raise SaveFormatError("typed Power tagged tail required")
        out+=write_power_tail(self.tail)
        return bytes(out)

def read_native_power_record(
    blob:bytes,*,offset:int=0
)->tuple[NativePowerRecord,int]:
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("valid Power record source and offset required")
    key,pos=_read_native_ascii_z(blob,offset)
    if not key or key==TERMINATOR[:-1]:
        raise SaveFormatError("not a concrete Power entry")
    name00,pos=_read_native_ascii_z(blob,pos)
    flag1,pos=_next_u32(blob,pos)
    flag2,pos=_next_u32(blob,pos)
    if flag1>255 or flag2>255:
        raise SaveFormatError("Power stored RAM-byte exceeds 255")
    dw5c,pos=_next_u32(blob,pos)
    name24,pos=_read_native_ascii_z(blob,pos)
    name40,pos=_read_native_ascii_z(blob,pos)
    dw20,pos=_next_u32(blob,pos)
    dw60,pos=_next_u32(blob,pos)
    name74,pos=_read_native_ascii_z(blob,pos)
    tree68,pos=_str_vector(blob,pos)
    vector90,pos=_str_vector(blob,pos)
    treea4,pos=_str_vector(blob,pos)
    treeb4=[]
    for _ in range(MAX_NESTED_ENTRIES):
        entry,pos=_read_native_ascii_z(blob,pos)
        if entry==b"fixtype":
            # Existing PowerTaggedTail expects to read this tag, so
            # rewind to the first byte of the fixtype literal.
            pos-=len(b"fixtype")+1
            break
        if not entry:raise SaveFormatError("empty Power+B4 before fixtype")
        value,pos=_next_u32(blob,pos)
        treeb4.append((entry,value))
    else:raise SaveFormatError("Power+B4 tree unbounded")
    tail,pos=read_power_tail_synthetic(blob,offset=pos)
    item=NativePowerRecord(key,name00,flag1,flag2,dw5c,name24,name40,
                           dw20,dw60,name74,tree68,vector90,treea4,
                           tuple(treeb4),tail)
    return item,pos


@dataclass(frozen=True,slots=True)
class PowerGroupByteProof:
    record_count:int
    unique_keys:int
    first_name:bytes|None
    last_name:bytes|None
    terminal_start:int
    end_offset:int
    exact_record_roundtrips:int
    byte_sha256:str


def validate_native_power_group(blob:bytes,*,offset:int)->PowerGroupByteProof:
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("Power group source offset invalid")
    start=offset
    first=None
    last=None
    names=set()
    for i in range(MAX_RECORDS):
        if blob[offset:offset+len(TERMINATOR)]==TERMINATOR:
            return PowerGroupByteProof(
                i,len(names),first,last,offset,offset+len(TERMINATOR),
                i,sha256(blob[start:offset+len(TERMINATOR)]).hexdigest())
        item,end=read_native_power_record(blob,offset=offset)
        if item.pack()!=blob[offset:end]:
            raise SaveFormatError("Power record byte inverse mismatch")
        if i==0:first=item.key
        last=item.key
        names.add(item.key)
        offset=end
    raise SaveFormatError("Power group unbounded or delimiter missing")

