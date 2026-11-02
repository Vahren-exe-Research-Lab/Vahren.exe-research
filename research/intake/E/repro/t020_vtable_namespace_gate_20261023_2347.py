"""E T020: source receipt metadata and SYNTHETIC vtable provenance cases only."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE_SHA = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
REA_SHA = '216031E676D8D6389D3FC9A2F0AB970994AD9707DC1160B4AD48CBDA514577B7'
CALL_ORDER = ['0x0040E42E', '0x0040E445']
DEFAULT = {
    'slot_identity': 'demo_secondary_0x04',
    'runtime_same_run': True,
    'edi': '0x008B8C90',
    'globals_rechecked': True,
    'demo_vptr': '0x00638054',
    'counter': 'positive',
    'vcall_sites': CALL_ORDER,
}

def check_source():
    p = ROOT / 'rea_lab' / 'decomp_task' / 'REA_20261023_23H_P0_BATTLEWND_DEMO_GLOBAL_IDENTITY_EVIDENCE.json'
    raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest().upper() == REA_SHA, 'REA research evidence changed'
    ev = json.loads(raw)
    assert ev['source_exe_sha256'] == EXE_SHA
    assert ev['counts']['total'] == ev['counts']['passed'] == 25
    assert all(x['pass'] for k in ('mechanical_pe_tests','vtable_tests','direct_call_tests') for x in ev[k])
    assert len(ev['mechanical_pe_tests']) == 18
    assert len(ev['vtable_tests']) == 4 and len(ev['direct_call_tests']) == 3
    assert int(ev['derived_object_base'], 16) + 0x1C8 == int(ev['global_slots'][0]['absolute'], 16)
    assert int(ev['derived_object_base'], 16) + 0x1CC == int(ev['global_slots'][1]['absolute'], 16)
    ptr = {int(x['address'],16):int(x['target'],16) for x in ev['vtable_tests']}
    assert ptr[0x638058] == 0x449730 and ptr[0x63803C] == 0x447810
    assert ev['bounds']['original_runtime_type'] == 'UNPROVEN'
    e_doc = (ROOT / 'tests' / 'T020_FASTSIM_RETURN0_PRIMARY_VTABLE_DRAW_GATE_20261023_1850.md').read_text(encoding='utf-8')
    for witness in ('0x00638080', '0x00452D90', '0x006380CC', '0x0040E220'):
        assert witness in e_doc, f'missing E primary/secondary witness {witness}'
    return ev['counts']['passed']

def classify(receipt):
    if receipt['slot_identity'] != 'demo_secondary_0x04':
        return 'REJECT_VTABLE_NAMESPACE'
    if not receipt['runtime_same_run']:
        return 'REJECT_CROSS_RUN'
    if receipt['edi'] != '0x008B8C90':
        return 'VERIFY_THIS_IDENTITY'
    if not receipt['globals_rechecked']:
        return 'VERIFY_POINTER_LIFETIME'
    if receipt['demo_vptr'] != '0x00638054':
        return 'VERIFY_RUNTIME_VPTR'
    if receipt['counter'] == 'unknown':
        return 'VERIFY_COUNTER_BRANCH'
    if receipt['counter'] != 'positive':
        return 'OTHER_LOOP_BRANCH'
    if receipt['vcall_sites'] != CALL_ORDER:
        return 'VERIFY_DUAL_DISPATCH'
    # Never grant a Golden result from this internal-only synthetic model.
    return 'SYNTHETIC_INTERNAL_ONLY'

def main():
    source_count = check_source()
    p = Path(__file__).with_name('T020_VTABLE_NAMESPACE_SYNTHETIC_CASES_20261023_2347.json')
    suite = json.loads(p.read_text(encoding='utf-8'))
    assert suite['status'] == 'DESIGNED_SYNTHETIC_ONLY'
    seen = set()
    for case in suite['cases']:
        assert case['id'] not in seen, 'duplicate fixture ID'
        seen.add(case['id'])
        row = {**DEFAULT, **case['override']}
        result = classify(row)
        assert result == case['expected'], f'{case["id"]}: {result} vs {case["expected"]}'
    print(f'REA_EVIDENCE_METADATA={source_count}/25 PASS; SYNTHETIC={len(seen)}/{len(seen)} PASS; GAMEPLAY=NOT_RUN; GOLDEN=0; STRICT_MATCH=0')

if __name__ == '__main__':
    main()
