"""T014/T031 ver0.67 additive envelope and synthetic global.sav records.

No original save bytes have been executed or matched. This implements only
the statically confirmed 32-byte header and key/aux/int32 record grammar.
No disk IO, file overwrite policy or battle/Unit state serialization here.
"""
from __future__ import annotations
from dataclasses import dataclass
from struct import pack, unpack
from typing import Mapping
from .legacy_rng import LegacyRng

MAGIC = b"\x01\x02\x03\x04"
KEY_SIZE = 28
HEADER_SIZE = 32
TERMINATOR = b"----------\x00"

class SaveFormatError(ValueError):
    pass

def _validate_key(key: bytes) -> bytes:
    key = bytes(key)
    if len(key) != KEY_SIZE:
        raise SaveFormatError("additive key must contain exactly 28 bytes")
    return key

def generate_key(rng: LegacyRng) -> bytes:
    """Native codec: 28 rand() draws, floor(rand15*112/32768)+8."""
    return bytes(8 + (rng.rand15() * 112) // 32768
                 for _ in range(KEY_SIZE))

def encode_envelope(payload: bytes, *, key: bytes | None = None,
                    rng: LegacyRng | None = None) -> bytes:
    if (key is None) == (rng is None):
        raise ValueError("supply exactly one of fixed key or seeded rng")
    selected = _validate_key(key) if key is not None else generate_key(rng)
    return MAGIC + selected + bytes(
        (b + selected[(i + HEADER_SIZE) % KEY_SIZE]) & 0xFF
        for i,b in enumerate(payload)
    )

def decode_envelope(data: bytes) -> bytes:
    if len(data) < HEADER_SIZE or data[:4] != MAGIC:
        raise SaveFormatError("invalid or truncated native envelope header")
    key = data[4:HEADER_SIZE]
    return bytes((b - key[(i + HEADER_SIZE) % KEY_SIZE]) & 0xFF
                 for i,b in enumerate(data[HEADER_SIZE:]))

def overwrite_prefix_nontruncating(old: bytes, new: bytes) -> bytes:
    """Pure model of OPEN_ALWAYS+write-at-start, NOT proof of loader behavior."""
    return new + old[len(new):] if len(old)>len(new) else new

@dataclass(frozen=True,slots=True)
class GlobalValue:
    value: int
    aux: str = ""
    def __post_init__(self) -> None:
        if not (-2**31 <= self.value <= 2**31 - 1):
            raise SaveFormatError("native global value is signed int32")
        _ascii(self.aux, field="aux")

def _ascii(value: str, *, field: str) -> bytes:
    try:
        encoded = value.encode("ascii", "strict")
    except UnicodeEncodeError as exc:
        raise SaveFormatError(f"{field} not in verified ASCII subset") from exc
    # The saved 0x470830 assembly accepts bytes 0x20..0x7F inclusive;
    # this includes DEL (0x7F), despite its usual classification as control.
    if any(ch < 0x20 or ch > 0x7F for ch in encoded):
        raise SaveFormatError(f"{field} contains unverified control/non-ASCII byte")
    return encoded

def pack_global_records(records: Mapping[str,GlobalValue]) -> bytes:
    """Stable key order and a terminal marker; no record count."""
    out = bytearray()
    for name in sorted(records, key=lambda s:s.encode("ascii",errors="strict")):
        if not name or name == "----------":
            raise SaveFormatError("empty or reserved global key")
        item = records[name]
        if not isinstance(item, GlobalValue):
            raise TypeError("record values must be GlobalValue")
        out += _ascii(name, field="key") + b"\x00"
        out += _ascii(item.aux, field="aux") + b"\x00"
        out += pack("<i", item.value)
    out += TERMINATOR
    return bytes(out)

def _read_cstring(data: bytes, pos: int) -> tuple[str,int]:
    end = data.find(b"\x00",pos)
    if end<0:
        raise SaveFormatError("unterminated global record string")
    raw = data[pos:end]
    try:
        value = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise SaveFormatError("non-ASCII record field") from exc
    _ascii(value,field="record")
    return value,end+1

def unpack_global_records(data: bytes) -> dict[str,GlobalValue]:
    records: dict[str,GlobalValue] = {}
    pos = 0
    while True:
        if pos >= len(data):
            raise SaveFormatError("missing global-record terminator")
        key,pos = _read_cstring(data,pos)
        if key == "----------":
            if pos != len(data):
                # Old OPEN_ALWAYS trailing garbage may exist, but the native
                # loader handling of it is unverified; fail closed for now.
                raise SaveFormatError("unverified bytes after terminator")
            return records
        if not key or key in records:
            raise SaveFormatError("empty or duplicate record key")
        aux,pos = _read_cstring(data,pos)
        if pos+4 > len(data):
            raise SaveFormatError("truncated int32 record value")
        value = unpack("<i",data[pos:pos+4])[0]
        pos+=4
        records[key] = GlobalValue(value,aux)

@dataclass(slots=True)
class GlobalStore:
    """Logical gread/gwrite; disk and scene numeric map are separate."""
    records: dict[str,GlobalValue]

    def __init__(self, records: Mapping[str,GlobalValue] | None = None):
        self.records=dict(records or {})

    def gread(self, key: str) -> GlobalValue:
        return self.records.get(key,GlobalValue(0,""))

    def gwrite(self, key: str, value: int, aux: str = "") -> None:
        if not key or key == "----------":
            raise SaveFormatError("invalid global key")
        _ascii(key,field="key")
        self.records[key]=GlobalValue(value,aux)

    def plaintext(self) -> bytes:
        return pack_global_records(self.records)

    def encrypted(self, *, key: bytes | None = None,
                  rng: LegacyRng | None = None) -> bytes:
        return encode_envelope(self.plaintext(),key=key,rng=rng)

    @classmethod
    def from_encrypted(cls, data: bytes) -> "GlobalStore":
        return cls(unpack_global_records(decode_envelope(data)))
