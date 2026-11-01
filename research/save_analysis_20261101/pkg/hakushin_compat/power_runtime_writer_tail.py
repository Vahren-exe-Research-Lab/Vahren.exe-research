"""Power runtime writer 0x596AA0 last tagged segment (synthetic inverse).

Verified WRITE order in T014_GROUP_PROBE.txt VA0x596E0B..0x597091:
fixtype/train_max/train_up/base_level raw dwords + home_spot vector.
The writer emits TWO successive empty strings after the home_spot vector.
The target native Power reader 0x5964C0 is not interpreted here.
"""
from __future__ import annotations
from dataclasses import dataclass
from struct import pack,unpack_from
from .native_stream_strings import write_native_cstring

class PowerTailError(ValueError):
    pass

TAGGED_DWORDS=(("fixtype",0xD0),("train_max",0xD4),
               ("train_up",0xD8),("base_level",0xDC))

def _cstring(blob:bytes,pos:int)->tuple[bytes,int]:
    end=blob.find(b"\x00",pos)
    if end<0 or end-pos>65536:
        raise PowerTailError("missing or excessive NUL field")
    field=blob[pos:end]
    if any(c<0x20 or c>0x7F for c in field):
        raise PowerTailError("unverified field byte")
    return field,end+1

@dataclass(frozen=True,slots=True)
class PowerTaggedTail:
    fixtype_d0:int
    train_max_d4:int
    train_up_d8:int
    base_level_dc:int
    home_spot_names:tuple[bytes,...]

    def __post_init__(self)->None:
        for v in (self.fixtype_d0,self.train_max_d4,
                  self.train_up_d8,self.base_level_dc):
            if type(v) is not int or not 0<=v<=0xFFFFFFFF:
                raise PowerTailError("native raw DWORD requires uint32 pattern")
        for n in self.home_spot_names:
            if type(n) is not bytes or not n or any(c<0x20 or c>0x7F for c in n):
                raise PowerTailError("invalid or empty home_spot entry")

def write_power_tail(value:PowerTaggedTail)->bytes:
    out=bytearray()
    for label,number in zip((t for t,_ in TAGGED_DWORDS),
                            (value.fixtype_d0,value.train_max_d4,
                             value.train_up_d8,value.base_level_dc)):
        out+=label.encode("ascii")+b"\x00"+pack("<I",number)
    out+=b"home_spot\x00"
    for name in value.home_spot_names:
        out+=write_native_cstring(name)
    out+=b"\x00\x00"
    return bytes(out)

def read_power_tail_synthetic(
    blob:bytes,*,offset:int=0
)->tuple[PowerTaggedTail,int]:
    """Synthetic inverse; full target Power reader is still unverified."""
    if not isinstance(blob,bytes) or not 0<=offset<=len(blob):
        raise PowerTailError("invalid source or offset")
    pos=offset
    values=[]
    for name,_ in TAGGED_DWORDS:
        actual,pos=_cstring(blob,pos)
        if actual!=name.encode("ascii"):
            raise PowerTailError("incorrect Power numeric tag")
        if len(blob)-pos<4:raise PowerTailError("short scalar")
        values.append(unpack_from("<I",blob,pos)[0])
        pos+=4
    tag,pos=_cstring(blob,pos)
    if tag!=b"home_spot":raise PowerTailError("missing home_spot tag")
    names=[]
    for _ in range(100000):
        item,pos=_cstring(blob,pos)
        if not item:break
        names.append(item)
    else:raise PowerTailError("unbounded home_spot vector")
    final,pos=_cstring(blob,pos)
    if final:raise PowerTailError("missing second empty terminator")
    return PowerTaggedTail(*values,tuple(names)),pos
