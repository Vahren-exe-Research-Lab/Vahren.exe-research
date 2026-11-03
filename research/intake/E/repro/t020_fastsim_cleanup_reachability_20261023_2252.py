from pathlib import Path
import hashlib, json
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
FIX = Path(__file__).with_name("T020_FASTSIM_CLEANUP_NEGATIVES_20261023_2252.json")
SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest().upper() == SHA, "source EXE mismatch"
pe = pefile.PE(data=raw, fast_load=True)
cs = Cs(CS_ARCH_X86, CS_MODE_32)

def decoded(start, size):
    off = pe.get_offset_from_rva(start - pe.OPTIONAL_HEADER.ImageBase)
    return {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(raw[off:off + size], start)}

code = decoded(0x0048F002, 0x72) | decoded(0x00415A60, 0x32)
expected = {
    0x0048F00B: ("mov", "byte ptr [ebp + 0x1eec71], 1"),
    0x0048F012: ("test", "esi, esi"),
    0x0048F014: ("je", "0x48f02a"),
    0x0048F01C: ("call", "0x415a60"),
    0x0048F022: ("call", "0x5b6bbb"),
    0x0048F033: ("call", "0x5b6bbb"),
    0x0048F04E: ("ret", "4"),
    0x00415A67: ("cmp", "dword ptr [esi + 0x14], 0x10"),
    0x00415A70: ("call", "0x5b6bbb"),
    0x00415A89: ("add", "esi, 0x1c"),
}
bad = {hex(k): (v, code.get(k)) for k, v in expected.items() if code.get(k) != v}
assert not bad, bad
fixtures = json.loads(FIX.read_text(encoding="utf-8"))
ids = [f["id"] for f in fixtures["fixtures"]]
assert len(ids) == len(set(ids)) == 7
assert fixtures["gameplay_not_run"] and fixtures["actual_golden_pass"] == fixtures["strict_match"] == 0
print("STATIC_NATIVE_CHECK PASS", len(expected), "/", len(expected), "EXE_SHA PASS; fixture IDs", len(ids), "; GAMEPLAY NOT RUN")
