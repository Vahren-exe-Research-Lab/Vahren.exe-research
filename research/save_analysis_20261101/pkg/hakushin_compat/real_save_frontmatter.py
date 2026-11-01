"""T014 limited ACTUAL ver0.67 normal-save frontmatter and numeric group.

Evidence: user-produced save1/auto/save2 (2026-10-11), with original
files preserved read-only in dev_lab/_work; saved native 0x460000 writer
and 0x45E1E0 reader; additive envelope 0x427040/0x4270F0.
Numerical map terminates with b"----------\\x00" (same engine string
as the global map), NOT b"\\x00". This correction was proven from
three actual savs and normal writer 0x4602A3 + unit writer 0x58EFD0.
This parses ONLY leading fields and numeric group. Unit/Spot/Power,
diplomacy, world graph and rest of save remain opaque bytes.
Do not infer field meanings, deduplicate names, or claim gameplay parity.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from struct import pack, unpack_from

from .save_envelope import (
    SaveFormatError, decode_envelope, encode_envelope, HEADER_SIZE, TERMINATOR,
)

MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_RECORDS = 100_000
MAX_STRING_BYTES = 65_536

def _read_native_ascii_z(data:bytes, pos:int)->tuple[bytes,int]:
    if not 0<=pos<len(data):
        raise SaveFormatError("unexpected end of native string stream")
    end=data.find(b"\x00",pos,min(len(data),pos+MAX_STRING_BYTES+1))
    if end<0:
        raise SaveFormatError("missing NUL in bounded native string")
    raw=data[pos:end]
    if any(byte<0x20 or byte>0x7F for byte in raw):
        raise SaveFormatError("non-native printable ASCII field")
    return raw,end+1


@dataclass(frozen=True,slots=True)
class NativeNumericRecord:
    key:bytes
    aux:bytes
    signed_value:int

    def __post_init__(self)->None:
        if type(self.key) is not bytes or not self.key or self.key == TERMINATOR[:-1]:
            raise SaveFormatError("numeric record requires nonempty non-sentinel key")
        for raw in (self.key,self.aux):
            if type(raw) is not bytes or len(raw)>MAX_STRING_BYTES:
                raise SaveFormatError("invalid record byte string")
            if any(not 0x20<=b<=0x7F for b in raw):
                raise SaveFormatError("unverified record string")
        if type(self.signed_value) is not int or not -(2**31)<=self.signed_value<2**31:
            raise SaveFormatError("native numeric value must be signed int32")

@dataclass(frozen=True,slots=True)
class ActualNormalSaveFrontmatter:
    leading_u32:int
    scenario_id:bytes
    power_id:bytes
    unknown_u32x5:tuple[int,int,int,int,int]
    records:tuple[NativeNumericRecord,...]
    unparsed_suffix:bytes
    stored_key28:bytes
    numeric_group_start:int
    numeric_group_end:int
    source_sha256:str
    decoded_sha256:str

    def plaintext(self)->bytes:
        """Rebuild the full byte stream without parsing its unknown tail."""
        result=bytearray(pack("<I",self.leading_u32))
        for text in (self.scenario_id,self.power_id):
            result+=text+b"\x00"
        for field in self.unknown_u32x5:
            result+=pack("<I",field)
        if len(result)!=self.numeric_group_start:
            raise SaveFormatError("prelude bytes do not match inspected offset")
        for r in self.records:
            result+=r.key+b"\x00"+r.aux+b"\x00"+pack("<i",r.signed_value)
        result+=TERMINATOR
        if len(result)!=self.numeric_group_end:
            raise SaveFormatError("numeric group bytes do not match inspected offset")
        return bytes(result)+self.unparsed_suffix

    def reencrypt_with_captured_key(self)->bytes:
        """BYTE preservation only, NOT game write/load or new-key RNG."""
        return encode_envelope(self.plaintext(),key=self.stored_key28)

    @property
    def duplicate_record_count(self)->int:
        seen=set();duplicates=0
        for record in self.records:
            if record.key in seen:duplicates+=1
            seen.add(record.key)
        return duplicates


def parse_actual_normal_save(raw:bytes)->ActualNormalSaveFrontmatter:
    if type(raw) is not bytes or not HEADER_SIZE+32<=len(raw)<=MAX_FILE_BYTES:
        raise SaveFormatError("bounded actual normal save bytes required")
    plain=decode_envelope(raw)
    pos=0
    if len(plain)<4:raise SaveFormatError("missing first normal-save scalar")
    marker=unpack_from("<I",plain,pos)[0];pos+=4
    scenario,pos=_read_native_ascii_z(plain,pos)
    power,pos=_read_native_ascii_z(plain,pos)
    if not scenario or not power:
        raise SaveFormatError("actual normal-save identifiers are nonempty")
    if pos+20>len(plain):
        raise SaveFormatError("truncated pre-numeric five dwords")
    unknown=tuple(unpack_from("<I",plain,pos+4*i)[0] for i in range(5))
    pos+=20
    group_start=pos

    entries=[]
    for _ in range(MAX_RECORDS):
        key,pos=_read_native_ascii_z(plain,pos)
        if key==TERMINATOR[:-1]:
            break
        if not key:
            raise SaveFormatError("empty numeric key before native dash terminator")
        aux,pos=_read_native_ascii_z(plain,pos)
        if pos+4>len(plain):
            raise SaveFormatError("truncated normal-save int32")
        value=unpack_from("<i",plain,pos)[0];pos+=4
        entries.append(NativeNumericRecord(key,aux,value))
    else:
        raise SaveFormatError("numeric group exceeds bounded record limit")
    return ActualNormalSaveFrontmatter(
        leading_u32=marker,scenario_id=scenario,power_id=power,
        unknown_u32x5=unknown,records=tuple(entries),
        unparsed_suffix=plain[pos:],stored_key28=raw[4:HEADER_SIZE],
        numeric_group_start=group_start,numeric_group_end=pos,
        source_sha256=sha256(raw).hexdigest(),
        decoded_sha256=sha256(plain).hexdigest(),
    )

