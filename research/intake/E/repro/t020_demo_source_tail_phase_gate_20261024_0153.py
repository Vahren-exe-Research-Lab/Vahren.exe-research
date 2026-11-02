"""E-owned synthetic negative fixture checker; no original gameplay execution."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REA = ROOT / 'rea_lab' / 'decomp_task'
TESTS = ROOT / 'tests'
SOURCES = {
    'REA_20261024_0137_P0_DEMO_VSLOT0C_SOURCE_TAIL_STATIC.md': '842397FAEFFFD3860FDE70A46CC024D608FA5AA69B4C4442146727889BE48ED0',
    'REA_20261024_0137_P0_DEMO_VSLOT0C_SOURCE_TAIL_EVIDENCE.json': 'A797B683BF88311189F9041D54ABC0AEB7006413549AE3FA0F7171435296D686',
}

def classify(c):
    if c['run'] == 'different': return 'CROSSRUN_CONFLICT'
    if c['run'] != 'same': return 'VERIFY_RUN_ID'
    if c['kind'] == 'E8': return 'OPCODE_KIND_CONFLICT'
    if c['kind'] != 'E9': return 'VERIFY_OPCODE'
    if c['vptr'] != 'match': return 'VERIFY_DYNAMIC_VPTR'
    if c['tail'] == 'not_seen': return 'NO_LATE_VCALL'
    if c['tail'] != 'seen': return 'VERIFY_LATE_VCALL'
    if c['source'] == 'unknown': return 'VERIFY_SOURCE_AT_TAIL'
    if c['source'] == 'null':
        return 'CONTRADICTION_SAME_INVOCATION' if c['write'] == 'seen' else 'NULL_SKIP_NOT_G2'
    if c['write'] != 'seen': return 'VERIFY_POSTGUARD_WRITE'
    return 'INELIGIBLE_G2' if c['g2'] else 'STATIC_CONSISTENT_NOT_G2'

def main():
    checked = 0
    for name, expected in SOURCES.items():
        actual = hashlib.sha256((REA / name).read_bytes()).hexdigest().upper()
        assert actual == expected, f'source SHA drift: {name}'
        checked += 1
    evidence = json.loads((REA / 'REA_20261024_0137_P0_DEMO_VSLOT0C_SOURCE_TAIL_EVIDENCE.json').read_text(encoding='utf-8-sig'))
    findings = evidence['new_findings']
    assert any(f.get('type') == 'selector_A' and f.get('callsite') == '0x0040F383' for f in findings)
    assert any(f.get('type') == 'selector_B' and f.get('subselector_e9_site') == '0x00583CE6' for f in findings)
    assert any(f.get('type') == 'late_vcall' and f.get('sites') == ['0x004103D5', '0x004103E2'] for f in findings)
    assert any(f.get('type') == 'source_guard' and f.get('jump_if_null') == '0x004478D8 -> 0x0044861A' for f in findings)
    fixture = json.loads((TESTS / 'T020_DEMO_SOURCE_TAIL_PHASE_NEGATIVES_20261024_0153.json').read_text(encoding='utf-8-sig'))
    cases = fixture['cases']
    assert len({c['id'] for c in cases}) == len(cases)
    actual = [(c['id'], classify(c), c['expected']) for c in cases]
    failures = [x for x in actual if x[1] != x[2]]
    assert not failures, failures
    print(json.dumps({'source_sha_verified': checked, 'static_claim_checks': 4, 'synthetic_fixture_pass': len(cases),
                      'synthetic_fixture_fail': len(failures), 'original_gameplay': 'NOT_RUN',
                      'actual_golden_pass': 0, 'strict_match': 0, 'ready_integrated': 0}, ensure_ascii=False))

if __name__ == '__main__':
    main()
