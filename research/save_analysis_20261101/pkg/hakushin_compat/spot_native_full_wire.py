"""Entire Spot *wire record* codec for original Vahren 0.67 saves.

Native 0x598CE0 writer and reader 0x598980 are separate from semantic
runtime scene restoration. Reuses the already validated SpotWriterFragment
rather than editing old code owned by another research task.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256

from .real_save_frontmatter import _read_native_ascii_z
from .save_envelope import SaveFormatError, TERMINATOR
from .spot_runtime_writer_fragment import (
    SpotWriterFragment,parse_spot_fragment_synthetic,write_spot_fragment,
)

MAX_GROUP_COUNT=1500


@dataclass(frozen=True,slots=True)
class NativeSpotRecord:
    key:bytes
    value:SpotWriterFragment

    def pack(self)->bytes:
        if type(self.key) is not bytes or not self.key or self.key==TERMINATOR[:-1]:
            raise SaveFormatError("Spot key must be nonempty and not group marker")
        if len(self.key)>65536 or any(c<0x20 or c>0x7f for c in self.key):
            raise SaveFormatError("Spot key not in verified writer byte range")
        if not isinstance(self.value,SpotWriterFragment):
            raise SaveFormatError("typed SpotWriterFragment required")
        return self.key+b"\x00"+write_spot_fragment(self.value)


def read_native_spot_record(blob:bytes,*,offset:int=0)->tuple[NativeSpotRecord,int]:
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("Spot source bytes and offset required")
    key,pos=_read_native_ascii_z(blob,offset)
    if not key or key==TERMINATOR[:-1]:
        raise SaveFormatError("Spot group marker or empty key is not a concrete record")
    fragment,pos=parse_spot_fragment_synthetic(blob,offset=pos)
    return NativeSpotRecord(key,fragment),pos


@dataclass(frozen=True,slots=True)
class SpotGroupByteProof:
    record_count:int
    distinct_keys:int
    first_name:bytes|None
    last_name:bytes|None
    terminal_start:int
    end_offset:int
    full_record_byte_roundtrips:int
    group_sha256:str


def validate_native_spot_group(blob:bytes,*,offset:int)->SpotGroupByteProof:
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("Spot group bytes and bounded offset required")
    start=offset
    names=set()
    first=last=None
    for i in range(MAX_GROUP_COUNT):
        if blob[offset:offset+len(TERMINATOR)]==TERMINATOR:
            return SpotGroupByteProof(
                i,len(names),first,last,offset,offset+len(TERMINATOR),
                i,sha256(blob[start:offset+len(TERMINATOR)]).hexdigest())
        record,end=read_native_spot_record(blob,offset=offset)
        if record.pack()!=blob[offset:end]:
            raise SaveFormatError("Spot record byte roundtrip mismatch")
        if i==0:first=record.key
        last=record.key
        names.add(record.key)
        offset=end
    raise SaveFormatError("Spot group too long or no terminator")
