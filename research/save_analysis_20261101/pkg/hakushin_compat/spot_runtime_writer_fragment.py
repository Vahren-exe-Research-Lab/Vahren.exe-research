"""Saved T014 Spot writer 0x598CE0: limited plaintext segment schema.

Source verified by native writer disassembly in T014_GROUP_PROBE.txt.
The tag "capacity" follows tree names without an empty-string delimiter.
Reader 0x598980 internals are not analyzed here, so decode is synthetic.
No entire Spot, Power or .sav format is claimed to be compatible.
"""
from __future__ import annotations
from dataclasses import dataclass
from struct import pack,unpack_from
from .native_stream_strings import write_native_cstring

class SpotFragmentError(ValueError):
    pass

def _z(raw:bytes,at:int)->tuple[bytes,int]:
    end=raw.find(b"\x00",at)
    if end<0 or end-at>65536:
        raise SpotFragmentError("unterminated field")
    data=raw[at:end]
    if any(c<0x20 or c>0x7F for c in data):
        raise SpotFragmentError("out-of-contract field byte")
    return data,end+1

def _v(raw:bytes,nonempty:bool=False)->bytes:
    if not isinstance(raw,bytes) or (nonempty and not raw):
        raise SpotFragmentError("spot string must be verified bytes")
    if any(c<0x20 or c>0x7F for c in raw):
        raise SpotFragmentError("invalid data collapses in native writer")
    return raw

def _dw(v:int)->bytes:
    if type(v) is not int or not 0<=v<=0xFFFFFFFF:
        raise SpotFragmentError("raw dword must be unsigned bit pattern")
    return pack("<I",v)

@dataclass(frozen=True,slots=True)
class SpotWriterFragment:
    name_00:bytes
    name_2c:bytes
    name_64:bytes
    dword_80:int
    dword_84:int
    tree_key_names:tuple[bytes,...]
    capacity_88:int
    castlebattle_8c:int
    fightvalue_90:int
    dunname_48:bytes

def write_spot_fragment(item:SpotWriterFragment)->bytes:
    out=bytearray()
    for value in (item.name_00,item.name_2c,item.name_64):
        out+=write_native_cstring(_v(value))
    out+=_dw(item.dword_80)+_dw(item.dword_84)
    for name in item.tree_key_names:
        checked=_v(name,nonempty=True)
        if checked==b"capacity":
            raise SpotFragmentError("reserved capacity boundary as tree key")
        out+=write_native_cstring(checked)
    for name,value in (
        (b"capacity",item.capacity_88),
        (b"castlebattle",item.castlebattle_8c),
        (b"fightvalue",item.fightvalue_90)):
        out+=name+b"\x00"+_dw(value)
    out+=b"dunname\x00"+write_native_cstring(_v(item.dunname_48))
    out+=b"\x00" # final empty string in saved writer
    return bytes(out)

def parse_spot_fragment_synthetic(
    raw:bytes,*,offset:int=0
)->tuple[SpotWriterFragment,int]:
    """Parse inverse of writer for tests; target Spot reader still VERIFY."""
    if not isinstance(raw,bytes) or not 0<=offset<=len(raw):
        raise SpotFragmentError("bad input or offset")
    pos=offset
    strings=[]
    for _ in range(3):
        s,pos=_z(raw,pos)
        strings.append(s)
    if len(raw)-pos<8:raise SpotFragmentError("truncated initial scalars")
    init0,init1=unpack_from("<II",raw,pos)
    pos+=8
    names=[]
    for _ in range(100000):
        name,pos=_z(raw,pos)
        if name==b"capacity":break
        if not name:raise SpotFragmentError("empty tree key before capacity")
        names.append(name)
    else:raise SpotFragmentError("missing capacity boundary")
    dwords=[]
    for tag in (b"capacity",b"castlebattle",b"fightvalue"):
        if tag != b"capacity":
            actual,pos=_z(raw,pos)
            if actual!=tag:raise SpotFragmentError("unexpected numeric tag")
        if len(raw)-pos<4:raise SpotFragmentError("missing tag dword")
        dwords.append(unpack_from("<I",raw,pos)[0])
        pos+=4
    name,pos=_z(raw,pos)
    if name!=b"dunname":raise SpotFragmentError("missing dunname tag")
    dungeon,pos=_z(raw,pos)
    terminator,pos=_z(raw,pos)
    if terminator:raise SpotFragmentError("missing final empty sentinel")
    return SpotWriterFragment(
        strings[0],strings[1],strings[2],init0,init1,tuple(names),
        dwords[0],dwords[1],dwords[2],dungeon),pos
