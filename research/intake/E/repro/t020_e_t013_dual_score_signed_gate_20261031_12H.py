"""T020 E-only conditional dual-score / signed-int32 gate, not native gameplay."""
from pathlib import Path
from itertools import product
import hashlib
import json
import struct
import pefile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tests"
NATIVE = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
B_SOURCE = ROOT / "data" / "T013_DUAL_SCORE_RANK_FIELD_NATIVE_20261031_12H.md"
ID = "E-AUDIT-20261031-12H-T020-T013-SIGNED-DUAL-FIELD-GATE-01"
B_ID = "B-20261031-12H-T013-DUAL-SCORE-COMPARATORS-01"
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WINDOWS = {
    "two_comparators": (0x447240, 58, "A69CBAFBFE589DA7988FB807B026B8CACC7D30E9FA9FF007DC1B10B9FF72F331"),
    "score_reset": (0x448FA6, 35, "9FDB45530E09C4595B54A6DC37083283B4EE812C1B97866B7E6A4D91C6892EDF"),
    "rank_gate": (0x449296, 52, "84B6C58F369C56C438E442CFEF40DA4C8D725A9D2489F729DD7B761FDA90D6FF"),
}
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def signed32(n):
    return struct.unpack("<i", struct.pack("<I", n & 0xffffffff))[0]

assert digest(NATIVE) == PE_SHA, "original PE identity mismatch"
pe = pefile.PE(str(NATIVE), fast_load=True)
for label, (va, size, expected) in WINDOWS.items():
    assert hashlib.sha256(pe.get_data(va - pe.OPTIONAL_HEADER.ImageBase, size)).hexdigest().upper() == expected, label

values = [-2147483648, -2147483547, -2147483546, -1, 0, 1, 2147483647]
modes = [0, 1, 2, 3]
cases = []
for mode, score_a, score_b in product(modes, values, values):
    # Deliberately opposing fields: an incorrect offset selection is detectable.
    fields = {"+0xA0C": [score_a, score_b], "+0xA10": [score_b, score_a]}
    chosen = "+0xA0C" if mode == 2 else "+0xA10"
    observed = signed32(fields[chosen][0]) > signed32(fields[chosen][1])
    expected = (score_a > score_b) if mode == 2 else (score_b > score_a)
    assert observed == expected, (mode, score_a, score_b)
    cases.append({"kind": "signed_comparator", "mode": mode, "fields": fields, "selected": chosen, "predicate_gt": expected})
for mode, score, changed in product(modes, values, [False, True]):
    # This models the signed JLE exclusion only; no global sort or rank order.
    native_gate = changed and signed32(score) > signed32(0x80000065)
    reference = changed and score > -2147483547
    assert native_gate == reference, (mode, score, changed)
    cases.append({"kind": "rank_write_gate", "mode": mode, "score": score, "changed": changed, "eligible_write": reference})
assert len(cases) == 252
assert cases[0]["selected"] == "+0xA10"
assert next(c for c in cases if c["kind"] == "signed_comparator" and c["mode"] == 2)["selected"] == "+0xA0C"
assert not any(c["eligible_write"] for c in cases if c["kind"] == "rank_write_gate" and c["score"] == -2147483547)
assert any(c["eligible_write"] for c in cases if c["kind"] == "rank_write_gate" and c["score"] == -2147483546)
payload = {"research_id": ID, "owner": "E/T020", "source_owner": "B/T013", "source_research_id": B_ID, "state": "STATIC/SYNTHETIC/VERIFY/NOT READY", "golden_pass": 0, "strict_match": 0, "cases": cases}
fixture = OUT / "T020_E_T013_DUAL_SCORE_SIGNED_CASES_20261031_12H.json"
report = OUT / "T020_E_T013_DUAL_SCORE_SIGNED_ACCEPTANCE_20261031_12H.md"
manifest = OUT / "T020_E_T013_DUAL_SCORE_SIGNED_READBACK_20261031_12H.json"
fixture_bytes = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
if fixture.exists():
    assert fixture.read_bytes() == fixture_bytes, "fixture content drift"
else:
    with fixture.open("xb") as f:
        f.write(fixture_bytes)
b_sha = digest(B_SOURCE)
lines = [
    "# T020 E 12H — dual-score signed comparator acceptance (STATIC / VERIFY)",
    f"- ID: {ID}; E/T020; source B/T013 {B_ID}; not an additional B finding.",
    f"- Native original PE SHA256: {PE_SHA}. Checked directly, read-only. Source B detail SHA256: {b_sha}.",
    "- Exact x86 read-only window SHA: two_comparators 0x447240..0x44727A (exclusive), score_reset 0x448FA6..0x448FC9, rank_gate 0x449296..0x4492CA: 3/3 equal to B proof.",
    "- New synthetic comparator cases: 196/196 PASS across mode 0/1/2/3, signed INT32 extremes, ties and deliberately opposed +0xA0C/+0xA10 fields.",
    "- New synthetic signed-rank-write gate cases: 56/56 PASS, with threshold -2147483547 and score-change guard; total 252/252 PASS.",
    "- These gates do NOT prove 0x47BB50 sorting, stable tie ordering, mode semantics, true target selection, ABI, no overflow, or actual rank counter; all VERIFY.",
    "- T019: no new confirmed source contradiction or game bug. V9 NOT_FOUND of two comparator codelets is an indexing limitation, not missing native bytes.",
    "- T018: C-NB02 legal same-run G0 battle UI, G1 unmodified pre-battle SAVE+input, G2 real MAP/three sides/ordered Unit/Troop still need primary receipts; G3/G4 pending.",
    "- Required original golden for this rank path: unchanged EXE/DAT/SAVE/MAP/input, same run/tick, eligible mode2/non2, tied/different scores, legal visible candidate identity, target and next-tick trace; unknown native values remain INELIGIBLE.",
    "- DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0; new READY=0. Synthetic only; no executable gameplay run.",
    "- KB_CANDIDATE: source B-ID above; E validation only, VA 0x448E90, compare 0x447240/260, field offsets +0xA0C/+0xA10, callsite 0x449276->0x47BB50, source SHA above, STATIC/VERIFY/NOT READY. Dedicated KB curator decides publication.",
    "- Not changed: MASTER, A-D, REA, dev_lab, Git, shared knowledge, source EXE/DAT/SAVE/ZIP, schedules. Older safety holds retained; no prohibited VA inspected.",
    "- Next: read-only inspect 0x47BB50's comparator calling convention, and acquire lawful same-run G0/G1/G2; do not infer stable sort or accept READY until original target is observed."
]
report_bytes = ("\n".join(lines) + "\n").encode("utf-8")
if report.exists():
    assert report.read_bytes() == report_bytes, "report content drift"
else:
    with report.open("xb") as f:
        f.write(report_bytes)
readback = {"research_id": ID, "files": {fixture.name: {"sha256": digest(fixture), "bytes": fixture.stat().st_size}, report.name: {"sha256": digest(report), "bytes": report.stat().st_size}}, "native_windows_checked": 3, "synthetic_cases": len(cases), "pass": len(cases), "golden_pass": 0, "strict_match": 0, "readback": "PENDING_INDEPENDENT"}
if manifest.exists():
    old = json.loads(manifest.read_text(encoding="utf-8"))
    assert old["files"] == readback["files"] and old["pass"] == len(cases), "manifest drift"
else:
    with manifest.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(readback, f, ensure_ascii=False, indent=2)
        f.write("\n")
print(json.dumps({"status": "SYNTHETIC PASS", "cases": len(cases), "source_sha256": b_sha, "results": readback["files"], "manifest_sha256": digest(manifest)}))

