# -*- coding: utf-8 -*-
"""E/T020 synthetic-only source-pinned T028 count/release branch acceptance."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/T020_E_T028_RESERVATION_COUNT_RELEASE_CASES_20261029_23H.json"
PINS = {
 ROOT / "data/T028_RETREAT_SPOT_RESERVATION_RELEASE_NATIVE_20261029_23H.md": "E2A056108081F370199A0E7990979277D4D8B19269EBD979EAE69D5A51DD205D",
 ROOT / "data/T028_RETREAT_SPOT_CAPACITY_STRICT_GATE_NATIVE_20261029_22H.md": "D2E746997C492CE294EFF9BD9B61D7D45C14DBF5FE7030DAC02C624BE5ED26F6",
 ROOT / "tests/t020_e_t028_capacity_strict_gate_20261029_22H.py": "9A6E36AD65892FD7F708AE804C452418D0D336CA36D18AA69601638ABFD18DA4",
}
def classify(kind, c):
    if kind == "count":
        entries = c.get("entries")
        if type(entries) is not list: return "INVALID_SCHEMA"
        if "UNKNOWN" in entries: return "INSUFFICIENT_INPUT"
        if any(x is not None and (type(x) is not int or x < 0 or x > 255) for x in entries): return "INVALID_SCHEMA"
        return "COUNT_" + str(sum(x is not None and x != 0 for x in entries))
    if kind != "release": return "INVALID_SCHEMA"
    reach = c.get("at_cmp")
    if reach is None: return "INSUFFICIENT_INPUT"
    if type(reach) is not bool: return "INVALID_SCHEMA"
    if not reach: return "OUTSIDE_SITE"
    ebx, linked = c.get("ebx"), c.get("linked_now")
    if ebx is None: return "INVALID_PRECONDITION"
    if linked is None: return "INSUFFICIENT_INPUT"
    if not isinstance(ebx, str) or not isinstance(linked, str) or not ebx or not linked: return "INVALID_SCHEMA"
    if ebx != linked: return "SKIP_DEC_SITE"
    before = c.get("b8_before")
    if before is not None and (type(before) is not int or before < -2147483648 or before > 2147483647): return "INVALID_SCHEMA"
    if before == 0: return "DEC_ZERO_VERIFY"
    if before == -2147483648: return "DEC_INTMIN_VERIFY"
    return "DEC_SITE_ONLY"
def main():
    for p, digest in PINS.items():
        got = hashlib.sha256(p.read_bytes()).hexdigest().upper()
        assert got == digest, f"SOURCE_CHANGED: {p.name}: {got}"
    f = json.loads(CASES.read_text(encoding="utf-8-sig"))
    assert f["origin"] == "SYNTHETIC_STATIC_BRANCH_ONLY" and f["owner"] == "E"
    assert f["b_status"] == "VERIFY_NOT_READY" and f["actual_golden_pass"] == f["strict_match"] == 0
    cases = f["cases"]
    assert len(cases) == 21 and len({x["id"] for x in cases}) == len(cases)
    for row in cases:
        result = classify(row["kind"], row["input"])
        assert result == row["expected"], f'{row["id"]}: {result} vs {row["expected"]}'
    print(f"SOURCE_PINS {len(PINS)}/{len(PINS)} PASS")
    print(f"SYNTHETIC_COUNT_RELEASE {len(cases)}/{len(cases)} PASS")
    print("NO ORIGINAL GAMEPLAY; GOLDEN=0; STRICT_MATCH=0; B23 NOT_READY")
if __name__ == "__main__":
    main()
