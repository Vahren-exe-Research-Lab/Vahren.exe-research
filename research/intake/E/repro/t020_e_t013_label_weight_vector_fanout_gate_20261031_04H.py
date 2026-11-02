"""E/T020: byte-pinned, conditional AI fan-out regression. Never runs game."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json
import struct
import pefile

ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
B_NOTE = ROOT / "data" / "T013_CATEGORY_LABEL_WEIGHT_VECTOR_FANOUT_NATIVE_20261031_04H.md"
OUT = Path(__file__).with_name("T020_E_T013_LABEL_WEIGHT_FANOUT_CASES_20261031_04H.json")
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
B_SHA = "04FBCBB5EDA02856FD7B9C7E711C141E53E40EED2897EDDD560959F256FAE31C"
raw = GAME.read_bytes()
assert sha256(raw).hexdigest().upper() == EXE_SHA, "EXE source mismatch"
assert sha256(B_NOTE.read_bytes()).hexdigest().upper() == B_SHA, "B source changed: rereview"
pe = pefile.PE(data=raw, fast_load=True)
def at(va, n):
    offset = pe.get_offset_from_rva(va - pe.OPTIONAL_HEADER.ImageBase)
    out = raw[offset:offset+n]
    assert len(out) == n
    return out

checks = {}
checks["writer_window"] = sha256(at(0x4495C3, 0x4496F3-0x4495C3)).hexdigest().upper()
checks["label_jump_table"] = sha256(at(0x449704, 36)).hexdigest().upper()
assert checks["writer_window"] == "E94D6BC79B299C67E444DDBCDB4B80C6B289279502F17EA1BB44BF5756A8291C"
assert checks["label_jump_table"] == "D38E53A02F5435DFDFA275A045BC57B1EA4CB76F51C1A8F1D8D614752255CAD5"
for site, target in [(0x4496AF,0x5D1B80),(0x4496B9,0x40ED80),(0x4496C4,0x577220)]:
    ins = at(site, 5)
    assert ins[0] == 0xE8 and (site+5+int.from_bytes(ins[1:],"little",signed=True)) == target
checks["native_call_sites"] = 3
for va, value in [(0x63B1E8,0.6),(0x63B248,0.3),(0x63B0C8,0.8)]:
    assert abs(struct.unpack("<d",at(va,8))[0]-value) < 1e-12
checks["native_coefficients"] = 3
assert at(0x6357D0,5) == b"hold\x00" and at(0x6357D8,5) == b"hold\x00"
labels = ("hold","even","even","push","hold","hold","advance","even","back")
def admissible(unit):
    return (unit["f7c"] == 0 and unit["f7e"] == 0 and
            unit["c0"] >= 0 and unit["d0"] >= 0 and unit["c8"] >= 0)
fields = ("f7c","f7e","c0","d0","c8")
cases = []
for category in range(9):
    weight = 120 if category == 0 else 60 if category == 6 else 160
    for mask in range(32):
        units = [dict(f7c=0,f7e=0,c0=0,d0=0,c8=0) for _ in range(5)]
        for i in range(5):
            if mask & (1<<i):
                units[i][fields[i]] = 1 if i < 2 else -1
        actual = [i for i,u in enumerate(units) if admissible(u)]
        expected = [i for i in range(5) if not (mask & (1<<i))]
        assert actual == expected
        assert len(actual) == 5-mask.bit_count()
        cases.append(dict(category=category,model_label=labels[category],
                          model_weight=weight,invalid_gate_mask=mask,
                          model_writer_indices=actual,model_rng_calls=len(actual),
                          verdict="SYNTHETIC_ONLY_NOT_ORIGINAL_GAMEPLAY"))
assert len(cases) == 288
assert labels[0] == labels[4] == labels[5] == "hold"
assert (120,160,160) == (cases[0]["model_weight"],cases[4*32]["model_weight"],cases[5*32]["model_weight"])
doc = dict(id="E-AUDIT-20261031-04H-T020-T013-LABEL-WEIGHT-FANOUT-01",
           classification="STATIC_BYTE_PINNED_CONDITIONAL_SYNTHETIC_VERIFY_NOT_READY",
           source_exe_sha256=EXE_SHA,source_b_note_sha256=B_SHA,
           static_checks=checks, cases=cases,
           caveat="Vector may mutate; cache, RNG order, writer ABI, final gameplay NOT OBSERVED")
serialized = json.dumps(doc,ensure_ascii=False,indent=2)+"\n"
if OUT.exists():
    assert OUT.read_text(encoding="utf-8") == serialized, "Fixture differs: do not overwrite"
else:
    OUT.write_text(serialized, encoding="utf-8")
assert json.loads(OUT.read_text(encoding="utf-8")) == doc
print("PASS STATIC", checks, "SYNTHETIC",len(cases), "ORIGINAL_GAMEPLAY",0)
print("FIXTURE_SHA256",sha256(OUT.read_bytes()).hexdigest().upper())
