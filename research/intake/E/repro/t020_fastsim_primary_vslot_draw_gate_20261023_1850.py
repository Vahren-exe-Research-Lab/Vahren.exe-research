#!/usr/bin/env python3
"""E-owned static byte gate; no native gameplay execution or filesystem mutation."""
from pathlib import Path
import hashlib
import json
import struct
import sys
import pefile

HERE = Path(__file__).resolve().parent
FIX = json.loads((HERE / 'T020_FASTSIM_PRIMARY_VSLOT_DRAW_FIXTURES_20261023_1850.json').read_text(encoding='utf-8'))
EXE = HERE.parent / 'rea_lab' / 'targets' / 'hakushin067_Vahren.exe'
PRIMARY_VPTR = '0x00638074'
ALLOWED = {'STATIC_BODY_ELIGIBLE', 'STATIC_BODY_SUPPRESSED', 'VERIFY_VPTR', 'VERIFY_MODE', 'VERIFY_FLAG', 'VERIFY_ARG'}

def classify(case):
    arg = case['arg2']
    if not isinstance(arg, int) or not 0 <= arg <= 255:
        return 'VERIFY_ARG'
    if arg == 0:
        return 'STATIC_BODY_ELIGIBLE'  # bypasses the virtual guard
    if case['vptr'] != PRIMARY_VPTR:
        return 'VERIFY_VPTR'  # runtime vptr is not guaranteed
    if case['mode'] is None:
        return 'VERIFY_MODE'
    if int(case['mode'], 16) != 0x80000008:
        return 'STATIC_BODY_SUPPRESSED'
    if case['flag84'] is None:
        return 'VERIFY_FLAG'
    return 'STATIC_BODY_ELIGIBLE' if (case['flag84'] & 0xff) != 0 else 'STATIC_BODY_SUPPRESSED'

def main():
    raw = EXE.read_bytes()
    sha = hashlib.sha256(raw).hexdigest().upper()
    pe = pefile.PE(data=raw, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    at = lambda va, n: pe.get_data(va - base, n)
    checks = {
        'source_sha256': sha == FIX['source_exe_sha256'],
        'primary_slot_plus_0c': struct.unpack('<I', at(0x638080, 4))[0] == 0x452D90,
        'secondary_slot_plus_04': struct.unpack('<I', at(0x6380D0, 4))[0] == 0x40E220,
        'caller_vcall_push1': at(0x40D26C, 13).hex() == '8b078b500c6a01ffd284c00f84',
        'getter_full_body': at(0x452D90, 33).hex() == '807c240400741181b9a400000008000080740532c0c204008a8184000000c20400',
        'return0_argument1': at(0x40E284, 15).hex() == '8be86a018bce85ed750de88defffff',
        'normal_draw_argument0': at(0x40D0CB, 12).hex() == '6a00b9908c8b00e849010000',
    }
    cases = FIX['cases']
    rows = [{'id': c['id'], 'got': classify(c), 'expected': c['expected']} for c in cases]
    case_pass = sum(x['got'] == x['expected'] and x['got'] in ALLOWED for x in rows)
    unique = len({c['id'] for c in cases}) == len(cases)
    ok = all(checks.values()) and unique and case_pass == len(rows) and FIX['tier'] == 'STATIC_SYNTHETIC_NOT_NATIVE_GOLDEN'
    result = {'id': FIX['research_id'], 'source_sha256': sha, 'checks': checks, 'cases_pass': case_pass, 'cases_total': len(rows), 'ids_unique': unique, 'native_gameplay': 'NOT_RUN', 'actual_golden_pass': 0, 'strict_match': 0, 'status': 'STATIC_SYNTHETIC_PASS' if ok else 'FAILED', 'failures': [x for x in rows if x['got'] != x['expected']]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 2

if __name__ == '__main__':
    sys.exit(main())
