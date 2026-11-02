"""E/T020 18H: independent bounded original-x86 +0x28 transit acceptance gate; STATIC only."""
from pathlib import Path
from hashlib import sha256
import json
import re
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
CASES = ROOT / "tests" / "T020_E_T013_RNG_CONTEXT_TRANSFER_CASES_20261031_18H.json"
EXPECTED_PE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WINDOWS = [
    (0x5A3E33, 0x5A3E91, "CBA31B2E4955934BF5779DEBA0A54C312CA0229C8E1AFC710D20C0C1FAE2576F"),
    (0x577D37, 0x577DDE, "ABF51D76D7CD20025AA04B9C52FD5C26C1ED685C172C959B9982516F92446378"),
    (0x579FC6, 0x57A00A, "74DE9F2CF0C9A50C5E0CE47037EF64E625BED1A3C16A20CE92AB8FD9E7E6385C"),
    (0x57A07D, 0x57A0A6, "3C2C9C892B85A20AFBA22A95E9570128E653F415B0AF6A6396B03BA73530A929"),
    (0x57A120, 0x57A15B, "C8BE2F68AC94DB482B811E285B9DE573752669AD59324C34E4C7B20385B3951F"),
    (0x57A869, 0x57A8B8, "B6BEEF3D61C61A59C6D2136604315158402DC8F8C124C775504A406C918D338F"),
    (0x5A3EA0, 0x5A3F28, "609FF12208204D9B263A3980257BAB849C4A61EEED00B74274047236B3394673"),
    (0x5A3F18, 0x5A4006, "A1A68BA1E5AA2B07834BDFF919F81767BD267CB2AC23A59C85B1A8ADDEB65C1B"),
]
MOVS = {
    0x5A3E78: "[esi + 0x28]", 0x577DC4: "[esi + 0x28]",
    0x577DC8: "[edi + 0x28]", 0x577B20: "[esi + 0x28]",
    0x577B24: "[edi + 0x28]", 0x579FF6: "[edi + 0x28]",
    0x57A094: "[esi + 0x28]", 0x57A14A: "[esi + 0x28]",
}
CALLS = {
    0x577D82: 0x5A3DF0, 0x577DCB: 0x579EB0,
    0x577ADE: 0x5A3DF0, 0x577B27: 0x579EB0,
    0x579FF9: 0x57A830, 0x57A097: 0x57A830,
    0x57A14D: 0x57A830, 0x57A890: 0x5A3EA0,
}
raw = SOURCE.read_bytes()
assert sha256(raw).hexdigest().upper() == EXPECTED_PE, "PE SHA mismatch"
pe = pefile.PE(data=raw, fast_load=True)
decoder = Cs(CS_ARCH_X86, CS_MODE_32)
def get_bytes(va, size):
    out = pe.get_data(va - pe.OPTIONAL_HEADER.ImageBase, size)
    assert len(out) == size, hex(va)
    return out
def ins_at(va):
    ins = list(decoder.disasm(get_bytes(va, 16), va, count=1))
    assert len(ins) == 1, hex(va)
    return ins[0]
for lo, hi, expected in WINDOWS:
    assert sha256(get_bytes(lo, hi-lo)).hexdigest().upper() == expected, f"window SHA {lo:X}"
for va, operand in MOVS.items():
    ins = ins_at(va)
    assert ins.mnemonic == "mov" and operand in ins.op_str, f"MOV {va:X} {ins.mnemonic} {ins.op_str}"
for va, dst in CALLS.items():
    ins = ins_at(va)
    assert ins.mnemonic == "call" and int(ins.op_str, 16) == dst, f"CALL {va:X} {ins.mnemonic} {ins.op_str}"
compare_raw = get_bytes(0x5A3EA0, 0x5A4006-0x5A3EA0)
compare_ins = list(decoder.disasm(compare_raw, 0x5A3EA0))
uses_direct_disp28 = [hex(x.address) for x in compare_ins if re.search(r"\+ 0x28\]", x.op_str)]
assert not uses_direct_disp28, f"comparator +0x28 displacement: {uses_direct_disp28}"
assert any("+ 0x1c]" in x.op_str for x in compare_ins), "expected context+0x1C control missing"
fixtures = json.loads(CASES.read_text(encoding="utf-8"))
assert len(fixtures["cases"]) == len({c["case_id"] for c in fixtures["cases"]})
for case in fixtures["cases"]:
    assert case["golden_status"] == "DESIGNED_NOT_RUN"
    assert case["strict_match"] is None and case["original_dynamic_observed"] is False
    assert case["unsupported_shortcut"] in ("PAYLOAD_IS_SORT_KEY", "NO_RNG_CONSUMPTION", "FINAL_TARGET_PROVEN")
print(f"STATIC_NATIVE_PASS={len(WINDOWS)+len(MOVS)+len(CALLS)+2}, DESIGN_FIXTURES={len(fixtures['cases'])}, ORIGINAL_GAMEPLAY_PASS=0, STRICT_MATCH=0")
print("STATUS=STATIC BYTE VERIFIED / ACCEPTANCE DESIGNED_NOT_RUN / VERIFY / NOT READY")