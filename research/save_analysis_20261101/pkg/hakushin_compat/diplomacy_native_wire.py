"""Vahren 0.67 normal-save Diplomacy section writer bytes, not semantics.

Writer at 0x471D20:
 * memory u8 +09 and +0A via 0x4708A0 -> u32 LE each
 * memory dword +14, +38 -> u32 LE each
 * names of Power pointer vector +0x18..+0x20 -> NUL strings
 * one empty-string terminator.
Reader 0x471AF0 rereads these and resolves Power references by name,
but this Python module does not perform runtime pointer resolution.

Follows FOUR normal-save group separators (numeric, Unit, Spot, Power),
precedes SpotElm/SpotPath/SpotEscapePath world-graph section.
"""
from __future__ import annotations
from dataclasses import dataclass
from struct import pack,unpack_from
from .real_save_frontmatter import _read_native_ascii_z
from .save_envelope import SaveFormatError

MAX_POWER_REFS=1000


def _u32(value:int,label:str)->int:
    if type(value) is not int or not 0<=value<=0xffffffff:
        raise SaveFormatError(label+" requires native raw DWORD")
    return value


def _text(raw:bytes,*,empty:bool=False)->bytes:
    if type(raw) is not bytes or len(raw)>65536 or (not empty and not raw):
        raise SaveFormatError("diplomacy reference requires NUL-terminated native ASCII")
    if any(b<0x20 or b>0x7f for b in raw):
        raise SaveFormatError("invalid diplomacy reference byte")
    return raw


@dataclass(frozen=True,slots=True)
class NativeDiplomacySection:
    memory_byte_09:int
    memory_byte_0a:int
    scalar_u32_14:int
    scalar_u32_38:int
    power_reference_names:tuple[bytes,...]

    def pack(self)->bytes:
        for val,label in ((self.memory_byte_09,"+09 byte"),(self.memory_byte_0a,"+0A byte")):
            if _u32(val,label)>255:
                raise SaveFormatError("RAM byte stored as DWORD outside 0..255")
        if len(self.power_reference_names)>MAX_POWER_REFS:
            raise SaveFormatError("too many Power references")
        out=bytearray(pack("<IIII",
            self.memory_byte_09,self.memory_byte_0a,
            _u32(self.scalar_u32_14,"+14"),_u32(self.scalar_u32_38,"+38")))
        for name in self.power_reference_names:
            out+=_text(name)+b"\x00"
        out+=b"\x00"
        return bytes(out)


def read_native_diplomacy_section(
    blob:bytes,*,offset:int=0
)->tuple[NativeDiplomacySection,int]:
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("diplomacy requires valid bytes/offset")
    if offset+16>len(blob):
        raise SaveFormatError("truncated native diplomacy header")
    a,b,c,d=unpack_from("<IIII",blob,offset)
    if a>255 or b>255:
        raise SaveFormatError("native RAM byte stored as u32 >255")
    at=offset+16
    names=[]
    for _ in range(MAX_POWER_REFS):
        key,at=_read_native_ascii_z(blob,at)
        if not key:
            break
        names.append(key)
    else:
        raise SaveFormatError("unbounded Power-ref list")
    return NativeDiplomacySection(a,b,c,d,tuple(names)),at
