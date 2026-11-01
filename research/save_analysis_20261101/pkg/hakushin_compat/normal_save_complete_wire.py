"""T014 old-Vahren 0.67: ENTIRE normal .sav original-stream byte codec.

Unlike the earlier frontmatter/envelope-only roundtrip, this builds a
NEW byte stream by independently serializing each modeled section:

  header (u32 + scenario + power + 5*u32)
  numeric tree (preserving duplicate key+aux entries)
  Unit-record map (complete 0x58EFD0 writer-shaped record)
  Spot-record map (0x598CE0 writer-shaped record)
  Power-record map (0x596AA0 writer-shaped record)
  Diplomacy refs/flags (0x471D20)
  WorldGraph (0x435C10, 0x5A93F0, 0x5B0600)

Each native section is terminated exactly once; no "opaque tail"
is copied when building the result. The envelope is encoded with the
captured 28-byte key to compare full original bytes.

This is byte-level SAVED STRUCTURE, not gameplay engine load. Old
native constructors, pointer resolution, vtables, runtime side effects,
audio, graphics, events, RNG and any new-game strict MATCH remain
unimplemented or unverified. Refuse unknown on-disk variants.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from struct import pack

from .real_save_frontmatter import (
    ActualNormalSaveFrontmatter, parse_actual_normal_save,
)
from .save_envelope import TERMINATOR, encode_envelope, SaveFormatError
from .unit_native_full_wire import (
    NativeFullUnitRecord, read_native_full_unit_record, MAX_UNIT_RECORDS,
)
from .spot_native_full_wire import (
    NativeSpotRecord, read_native_spot_record, MAX_GROUP_COUNT,
)
from .power_native_full_wire import (
    NativePowerRecord, read_native_power_record, MAX_RECORDS as MAX_POWER_RECORDS,
)
from .diplomacy_native_wire import (
    NativeDiplomacySection, read_native_diplomacy_section,
)
from .world_graph_native_wire import (
    NativeWorldGraph, read_world_graph,
)


def _read_group(blob:bytes, offset:int, *, reader, max_records:int, label:str):
    items=[]
    for _ in range(max_records):
        if blob[offset:offset+len(TERMINATOR)]==TERMINATOR:
            return tuple(items),offset+len(TERMINATOR)
        item,end=reader(blob,offset=offset)
        if end<=offset or item.pack()!=blob[offset:end]:
            raise SaveFormatError(label+" item raw byte inverse mismatch")
        items.append(item)
        offset=end
    raise SaveFormatError(label+" group unbounded or missing terminator")


@dataclass(frozen=True,slots=True)
class CompleteNormalSave:
    front:ActualNormalSaveFrontmatter
    units:tuple[NativeFullUnitRecord,...]
    spots:tuple[NativeSpotRecord,...]
    powers:tuple[NativePowerRecord,...]
    diplomacy:NativeDiplomacySection
    world_graph:NativeWorldGraph
    source_sha256:str
    source_encoded_bytes:int

    def rebuilt_plaintext(self)->bytes:
        """Make all bytes from fields and records; never append opaque tail."""
        f=self.front
        out=bytearray(pack("<I",f.leading_u32))
        out+=f.scenario_id+b"\x00"+f.power_id+b"\x00"
        for n in f.unknown_u32x5:
            out+=pack("<I",n)
        for row in f.records:
            out+=row.key+b"\x00"+row.aux+b"\x00"+pack("<i",row.signed_value)
        out+=TERMINATOR
        for group in (self.units,self.spots,self.powers):
            for row in group:
                out+=row.pack()
            out+=TERMINATOR
        out+=self.diplomacy.pack()
        out+=self.world_graph.pack()
        return bytes(out)

    def rebuilt_ciphertext(self)->bytes:
        return encode_envelope(self.rebuilt_plaintext(),key=self.front.stored_key28)

    def counts(self)->dict[str,int]:
        return {
            "numeric":len(self.front.records),
            "Unit":len(self.units),
            "Spot":len(self.spots),
            "Power":len(self.powers),
            "DiplomacyPowerRefs":len(self.diplomacy.power_reference_names),
            **self.world_graph.counts(),
        }

    def exact_original_ciphertext(self)->bool:
        rebuilt=self.rebuilt_ciphertext()
        return (len(rebuilt)==self.source_encoded_bytes
                and sha256(rebuilt).hexdigest()==self.source_sha256)

def read_complete_normal_save(raw:bytes)->CompleteNormalSave:
    """Recreate the 6 native serialized sections, fail closed on trailing data."""
    f=parse_actual_normal_save(raw)
    plain=f.plaintext()
    units,offset=_read_group(
        plain,f.numeric_group_end,
        reader=read_native_full_unit_record,
        max_records=MAX_UNIT_RECORDS,label="Unit")
    spots,offset=_read_group(
        plain,offset,reader=read_native_spot_record,
        max_records=MAX_GROUP_COUNT,label="Spot")
    powers,offset=_read_group(
        plain,offset,reader=read_native_power_record,
        max_records=MAX_POWER_RECORDS,label="Power")
    diplomacy,next_offset=read_native_diplomacy_section(plain,offset=offset)
    if diplomacy.pack()!=plain[offset:next_offset]:
        raise SaveFormatError("Diplomacy was not byte exact")
    graph=read_world_graph(plain,offset=next_offset)
    if graph.end_offset!=len(plain):
        raise SaveFormatError("unknown trailing data beyond world graph")
    decoded=CompleteNormalSave(
        front=f,units=units,spots=spots,powers=powers,
        diplomacy=diplomacy,world_graph=graph.graph,
        source_sha256=sha256(raw).hexdigest(),
        source_encoded_bytes=len(raw),
    )
    # Unlike the old front-only proof, these are ALL individually
    # reconstructed bytes. Fail if even one original byte is different.
    if not decoded.exact_original_ciphertext():
        raise SaveFormatError("complete native save bytes do not match original")
    return decoded

