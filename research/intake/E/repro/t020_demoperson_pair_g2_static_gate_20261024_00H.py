"""E-owned read-only source pin + STATIC pair-init crosswalk; NEVER a Gameplay Golden runner."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / 'tests' / 'T020_DEMOPERSON_PAIR_G2_NEGATIVES_20261024_00H.json'
casebook = json.loads(FIX.read_text(encoding='utf-8'))
def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

for pin in casebook['source_pins']:
    source = ROOT / pin['path']
    assert source.is_file() and sha256(source) == pin['sha256'], f'source drift: {source}'

ev_path = ROOT / casebook['source_pins'][1]['path']
ev = json.loads(ev_path.read_text(encoding='utf-8'))
slots = ev['vtable_slot']
abi = ev['function_abi_local']
first, second = ev['indirect_sites']
facts = casebook['static_expected']
checks = {
    'source_exe': ev['original_exe_sha256'] == casebook['original_exe_sha256'],
    'source_status': ev['state'] == 'STATIC_VERIFY_NOT_READY',
    'slot': slots['slot_va'] == facts['vtable_slot_va'],
    'target': slots['little_endian_pointer'] == facts['target'],
    'abi_ret': abi['epilogue'] == 'RET 0x0C',
    'first_site': first['site'] == facts['first_call'],
    'second_site': second['site'] == facts['second_call'],
    'tag_pair': (first['this_plus_0x18'], second['this_plus_0x18']) == (0, 1),
    'peer_reciprocal': first['this_plus_0x1C'] == '[0x008B8E5C]' and second['this_plus_0x1C'] == '[0x008B8E58]',
    'state100': first['this_plus_0x20'] == second['this_plus_0x20'] == facts['initial_state_value'],
    'indirect': first['opcode'] == 'FF D2' and second['opcode'] == 'FF D0',
    'not_direct_e8': ev['direct_E8_callers_to_0x514A80'] == 0,
}
assert all(checks.values()), {key: value for key, value in checks.items() if not value}
cases = casebook['cases']
ids = [x['id'] for x in cases]
assert len(cases) == len(set(ids)) == 12
allowed = {'REJECT_PROMOTION', 'VERIFY_MAPPING', 'REJECT_SEMANTICS', 'VERIFY_SEMANTICS', 'REJECT_CALLER_INFERENCE', 'REJECT_TYPE_ALIAS', 'REJECT_RUN_JOIN', 'REJECT_READY_PROMOTION', 'VERIFY_RUNTIME_VPTR'}
assert all(x['bad_claim'] and x['expected'] in allowed for x in cases)
assert casebook['state'] == 'STATIC_CROSSWALK_DESIGNED_NOT_RUN'
print(f'STATIC_SOURCE_PIN {len(casebook["source_pins"])} / {len(casebook["source_pins"])} PASS')
print(f'STATIC_PAIR_INVARIANTS {sum(checks.values())} / {len(checks)} PASS')
print(f'T020_FIXTURE_STRUCTURE {len(cases)} / {len(cases)} PASS; COMPARISON_RUNNER NOT RUN')
print('OLD_GAMEPLAY DYNAMIC_OBSERVED=0 GOLDEN_PASS=0 STRICT_MATCH=0; REA/B NOT READY')
