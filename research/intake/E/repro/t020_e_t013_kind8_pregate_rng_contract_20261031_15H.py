"""E/T020 bounded native evidence gate plus abstract, non-Golden kind8 regression."""
from pathlib import Path
from itertools import product
from fractions import Fraction
import hashlib
import json
import struct
import pefile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/T013_KIND8_RANDOM_PAYLOAD_QUEUE_NATIVE_20261031_15H.md"
EXE = ROOT / "rea_lab/targets/hakushin067_Vahren.exe"
OUT = ROOT / "tests/T020_E_T013_KIND8_PREQUEUE_CASES_20261031_15H.json"
SID = "E-AUDIT-20261031-15H-T020-T013-KIND8-PREQUEUE-RNG-GATE-01"
assert hashlib.sha256(SRC.read_bytes()).hexdigest().upper() == "FAEF6FDEF83E746CD0F27A5E601A6662D97A23ECF7757F2A3FD1F7C94F58C03B"
data = EXE.read_bytes()
assert hashlib.sha256(data).hexdigest().upper() == "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
pe = pefile.PE(data=data, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
def native(va, size):
    b = pe.get_data(va - base, size)
    assert len(b) == size
    return b
WINDOWS = [
    (0x577D37, 0x577DFF, "71312B0609A6C7AE044A0D1F750F4CCB96C861AD5C71449CD43F7769A781304C"),
    (0x577AA5, 0x577B42, "CD97DB49175507F32FA94E4C6A2F4A78C1A63F8CB42DAB6088E41833C2D0E2F1"),
    (0x5A3DF0, 0x5A3E9D, "8F700406FD98C2DE262A1D46C5B8D684CE71820713628B5D9740C362DB626EE4"),
    (0x579EB0, 0x579F29, "1CC895784983190A2D489D2B93B9752C6B4071968CD894EB46BB47B6481A38C2"),
]
for lo, hi, expected in WINDOWS:
    assert hashlib.sha256(native(lo, hi-lo)).hexdigest().upper() == expected
CALLS = {
    0x577D47: 0x57A7D0, 0x577D73: 0x402710,
    0x577D82: 0x5A3DF0, 0x577DCB: 0x579EB0,
    0x577ADE: 0x5A3DF0, 0x577B27: 0x579EB0,
    0x5A3E55: 0x5B6EAB, 0x5A3E6E: 0x5D1B80,
    0x579F13: 0x5B6C2B,
}
for at, target in CALLS.items():
    raw = native(at, 5)
    assert raw[0] == 0xE8
    assert at + 5 + int.from_bytes(raw[1:], "little", signed=True) == target
assert native(0x579F04, 3) == bytes.fromhex("395D04")
assert native(0x579F07, 6) == bytes.fromhex("0F82BD020000")
assert native(0x5A3E78, 3) == bytes.fromhex("894628")
assert struct.unpack("<d", native(0x63B080, 8))[0] == 1/32768
assert struct.unpack("<d", native(0x63B060, 8))[0] == 100.0
cases = []
for scheduler, kind8_reached, count, sample in product(
    ("A", "B"), (False, True), (0, 1, 2, 3, 0xFFFFFFFF),
    (0, 1, 16384, 32767)
):
    scaled = Fraction(sample * 100, 32768)
    assert Fraction(0) <= scaled < Fraction(100)
    gate = (count & 0xFFFFFFFF) < 2 if kind8_reached else None
    trace = (["BUILDER_ENTER", "RNG_REQUEST", "CONVERSION_REQUEST",
              "RECORD_RETURN", "QUEUE_ENTRY", "COUNT_COMPARE",
              "MULTI_ELEMENT_SKIPPED" if gate else "MULTI_ELEMENT_PATH"]
             if kind8_reached else ["KIND8_NOT_REACHED"])
    assert (not kind8_reached) or trace.index("RNG_REQUEST") < trace.index("COUNT_COMPARE")
    if kind8_reached and count in (0, 1):
        assert gate and trace[-1] == "MULTI_ELEMENT_SKIPPED"
    if kind8_reached and count in (2, 3, 0xFFFFFFFF):
        assert not gate
    cases.append({
        "case_id": f"K8-{len(cases)+1:03d}", "scheduler_model": scheduler,
        "kind8_reached_assumption": kind8_reached, "count_raw_u32": count,
        "synthetic_rng_sample": sample, "scaled_exact_num": scaled.numerator,
        "scaled_exact_den": scaled.denominator, "post_queue_skip_u32": gate,
        "ordered_abstract_trace": trace, "native_converted_integer": None,
        "actual_rng_draws": None, "actual_game_target": None, "golden": "NOT RUN",
        "reachability": "SYNTHETIC_ASSUMPTION",
    })
assert len(cases) == 80
assert sum(x["post_queue_skip_u32"] is True for x in cases) == 16
assert sum(x["post_queue_skip_u32"] is False for x in cases) == 24
payload = {
    "id": SID, "owner": "E", "task": "T020", "antecedent_owner_task": "B/T013",
    "antecedent_source_sha256": "FAEF6FDEF83E746CD0F27A5E601A6662D97A23ECF7757F2A3FD1F7C94F58C03B",
    "source_exe_sha256": hashlib.sha256(data).hexdigest().upper(),
    "evidence": "4 bounded PE window hashes; 9 direct E8 CALLs; 3 instruction bytes; 2 doubles",
    "scope": "STATIC native and conditional synthetic control-flow only; not actual game",
    "case_count": len(cases), "passed": len(cases),
    "dynamic_observed": 0, "golden_pass": 0, "strict_match": 0,
    "notes": [
        "Call order is proved within the kind8 branch when it reaches both helpers, not globally.",
        "A later queue count<2 may skip multi-item work without undoing the earlier producer call.",
        "Actual RNG seed/draw count, x87 integer conversion, ABI, errors, target and side effects are VERIFY.",
        "0xFFFFFFFF count is a deliberately invalid/unproven-in-game signedness test, not legal Golden.",
    ], "cases": cases
}
blob = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
if OUT.exists():
    assert OUT.read_bytes() == blob, "Existing fixture differs: do not overwrite"
else:
    OUT.write_bytes(blob)
assert OUT.read_bytes() == blob
assert json.loads(OUT.read_text(encoding="utf-8"))["passed"] == len(cases)
print(json.dumps({"id":SID,"pe_window_pass":len(WINDOWS),"call_pass":len(CALLS),
    "instruction_checks":3,"constant_checks":2,"cases_pass":len(cases),
    "skipped_post_queue":16,"continued_post_queue":24,
    "fixture_sha256":hashlib.sha256(blob).hexdigest().upper(),
    "source_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest().upper()},ensure_ascii=False))
