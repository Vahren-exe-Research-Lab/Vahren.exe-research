"""Normal .sav reader that stops at the end of the native body.

Work copy (2026-11-01, Claude). Built on normal_save_complete_wire.
The native writer 0x460000 opens the file with CreateFileA OPEN_ALWAYS and
never truncates (T014 A18). When a shorter save overwrites a longer one,
the old bytes after the new body stay in the file. The native reader
0x45E1E0 stops after the world graph (0x435550), so those bytes are not
part of the current save.

This module:
  * parses header / numeric / Unit / Spot / Power / Diplomacy / graph,
  * proves the body is byte-exact by re-encoding it with the stored key
    and comparing to the same file prefix,
  * returns everything after the body as `stale_tail` (raw file bytes)
    without interpreting it.
Read-only. No gameplay or load-success claim.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .normal_save_complete_wire import CompleteNormalSave, _read_group
from .real_save_frontmatter import parse_actual_normal_save
from .save_envelope import SaveFormatError, encode_envelope, HEADER_SIZE
from .unit_native_full_wire import read_native_full_unit_record, MAX_UNIT_RECORDS
from .spot_native_full_wire import read_native_spot_record, MAX_GROUP_COUNT
from .power_native_full_wire import read_native_power_record, MAX_RECORDS as MAX_POWER
from .diplomacy_native_wire import read_native_diplomacy_section
from .world_graph_native_wire import read_world_graph


@dataclass(frozen=True, slots=True)
class BodyAndTail:
    save: CompleteNormalSave
    body_plain_len: int          # plaintext bytes of the current save body
    body_file_len: int           # = HEADER_SIZE + body_plain_len
    file_len: int
    stale_tail: bytes            # raw (still encrypted) file bytes after body
    section_offsets: dict        # plaintext offsets of section starts

    @property
    def stale_tail_len(self) -> int:
        return len(self.stale_tail)


def read_normal_save_body_and_tail(raw: bytes) -> BodyAndTail:
    f = parse_actual_normal_save(raw)
    plain = f.plaintext()
    offs = {"numeric": f.numeric_group_start}
    offs["Unit"] = f.numeric_group_end
    units, o = _read_group(plain, f.numeric_group_end, reader=read_native_full_unit_record,
                           max_records=MAX_UNIT_RECORDS, label="Unit")
    offs["Spot"] = o
    spots, o = _read_group(plain, o, reader=read_native_spot_record,
                           max_records=MAX_GROUP_COUNT, label="Spot")
    offs["Power"] = o
    powers, o = _read_group(plain, o, reader=read_native_power_record,
                            max_records=MAX_POWER, label="Power")
    offs["Diplomacy"] = o
    dip, o2 = read_native_diplomacy_section(plain, offset=o)
    if dip.pack() != plain[o:o2]:
        raise SaveFormatError("Diplomacy was not byte exact")
    offs["WorldGraph"] = o2
    graph = read_world_graph(plain, offset=o2)
    body_end = graph.end_offset
    offs["end"] = body_end
    body_file_len = HEADER_SIZE + body_end
    save = CompleteNormalSave(front=f, units=units, spots=spots, powers=powers,
                              diplomacy=dip, world_graph=graph.graph,
                              source_sha256=sha256(raw[:body_file_len]).hexdigest(),
                              source_encoded_bytes=body_file_len)
    rebuilt = save.rebuilt_plaintext()
    if len(rebuilt) != body_end or rebuilt != plain[:body_end]:
        raise SaveFormatError("rebuilt body plaintext differs")
    enc = encode_envelope(rebuilt, key=f.stored_key28)
    if enc != raw[:body_file_len]:
        raise SaveFormatError("re-encoded body differs from file prefix")
    return BodyAndTail(save=save, body_plain_len=body_end, body_file_len=body_file_len,
                       file_len=len(raw), stale_tail=raw[body_file_len:],
                       section_offsets=offs)
