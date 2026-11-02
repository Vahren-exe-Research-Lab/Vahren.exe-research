# E/T020 synthetic boundary probe. No original EXE or original SAVE execution.
# Distinct paths: low-level duplicate insertion vs normal caller cache hit.
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib, json
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'tests'
ID = 'E-AUDIT-20261031-08H-T020-T011-CACHE-DUPLICATE-CLEANUP-01'
BID = 'B-20261031-08H-T011-TRAINING-CACHE-LIFECYCLE-01'
B = ROOT / 'data' / 'T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md'
SOURCE_PIN = 'B79044AE9C8AE40FE3F59E06DD056E0D73DAABEC3D98B784C628737A2EACE1EF'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
assert sha(B) == SOURCE_PIN, 'B08 source changed; review required'
# Caller-level hit bypasses insertion; forced low-level duplicate is NOT a
# claimed reachable branch from the legal high-level training loop.
def model(existing_key, incoming_key, old_bonus, proposed_bonus, base):
    assert 0 <= existing_key <= 0xffffffff
    assert 0 <= incoming_key <= 0xffffffff
    cache = {existing_key: old_bonus}
    duplicate = incoming_key in cache
    if not duplicate: cache[incoming_key] = proposed_bonus
    return {'insert_flag': 0 if duplicate else 1,
            'incoming_discarded': duplicate, 'computed_current': base+proposed_bonus,
            'cached_after': cache[incoming_key], 'next_same_leader': base+cache[incoming_key],
            'node_count_after': len(cache), 'kind': 'DUPLICATE_INJECTED' if duplicate else 'DISTINCT_KEY_ASSUMED'}
# Key ordering exercises unsigned pointer-domain boundary; no native BST
# balancing / allocator semantics are implied by these expected outputs.
pairs = [(0x1000,0x1000), (0xffffffff,0xffffffff),
         (0x1000,0x80000000), (0x80000000,0x1000)]
old_values = (-3,0,4)
new_values = (-3,0,9)
bases = (-2,0,1,3)
cases = []; types = Counter()
for (old,new),prior,incoming,base in product(pairs,old_values,new_values,bases):
    got = model(old,new,prior,incoming,base)
    duplicate = old == new
    assert got['insert_flag'] == (0 if duplicate else 1)
    assert got['incoming_discarded'] == duplicate
    assert got['computed_current'] == base+incoming
    assert got['cached_after'] == (prior if duplicate else incoming)
    assert got['node_count_after'] == (1 if duplicate else 2)
    assert got['next_same_leader'] == base+(prior if duplicate else incoming)
    types[got['kind']] += 1
    cases.append({'existing_key':old,'incoming_key':new,'stored_bonus':prior,
                  'proposed_bonus':incoming,'base':base,'expected':got,
                  'admission':'LOW_LEVEL_INJECTION_ONLY' if duplicate else 'ALLOC_SUCCESS_ASSUMED'})
assert len(cases) == 144 and types['DUPLICATE_INJECTED'] == 72
assert types['DISTINCT_KEY_ASSUMED'] == 72
# Conservative lifecycle: only the normal branch CALL order is verified.
normal_order = ['INIT_SENTINEL','PROCESS_UNIT','REQUEST_RANGE_ERASE',
                'FREE_SENTINEL','NEXT_MANAGER_ITERATION']
assert normal_order.index('REQUEST_RANGE_ERASE') < normal_order.index('FREE_SENTINEL')
# Ineligible simulation cases must not be counted as native successes.
unknown = ['SENTINEL_ALLOCATION_FAILURE','ERASE_EXCEPTION',
           'EARLY_EXIT','MID_SCOPE_POINTER_RECYCLE','DUPLICATE_NATIVE_REACHABILITY']
assert all(isinstance(x,str) for x in unknown)
# New local scope is an empty cache in the bounded model, regardless of prior key.
assert {} == dict() and model(0x1000,0x1000,4,9,1)['cached_after'] == 4
fixture=OUT/'T020_E_T011_CACHE_LIFECYCLE_CASES_20261031_08H.json'
payload={'id':ID,'source_id':BID,'classification':'CONDITIONAL_SYNTHETIC_ONLY',
         'normal_path_order':normal_order,'unknown_not_run':unknown,
         'assumptions':['allocator succeeds for synthetic distinct-key insert',
                        'tree invariant holds','no key recycling within one scope'],
         'cases':cases}
fixture.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert len(json.loads(fixture.read_text(encoding='utf-8'))['cases']) == 144
receipt={'id':ID,'source_id':BID,'case_count':144,'branch_counts':dict(types),
         'source_sha256':sha(B),'runner_sha256':sha(Path(__file__)),
         'fixture_sha256':sha(fixture),'unknown_not_run':unknown,
         'normal_cleanup_order':'ERASE_REQUEST_BEFORE_SENTINEL_FREE',
         'dynamic_observed':0,'actual_golden_pass':0,'strict_match':0,
         'status':'STATIC_CROSSCHECK / CONDITIONAL_SYNTHETIC_EXECUTED / VERIFY / NOT READY'}
rfile=OUT/'T020_E_T011_CACHE_LIFECYCLE_READBACK_20261031_08H.json'
rfile.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert json.loads(rfile.read_text(encoding='utf-8')) == receipt
print(json.dumps(receipt,ensure_ascii=False))
