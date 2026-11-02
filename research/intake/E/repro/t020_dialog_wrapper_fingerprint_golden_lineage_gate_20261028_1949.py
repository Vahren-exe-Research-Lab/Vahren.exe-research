"""E-only static dialog-wrapper fingerprint + synthetic T018 lineage gate.

Usage: python t020_dialog_wrapper_fingerprint_golden_lineage_gate_20261028_1949.py --db /path/search.sqlite
Does not execute the original game. Never classifies synthetic examples as actual Golden PASS.
"""
import argparse
import hashlib
import json
import re
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--db', required=True)
ARGS = PARSER.parse_args()
DB = Path(ARGS.db).resolve()
F = json.loads((ROOT / 'T020_DIALOG_WRAPPER_FINGERPRINT_GOLDEN_LINEAGE_CASES_20261028_1949.json').read_text('utf8'))
CONN = sqlite3.connect('file:' + DB.as_posix() + '?mode=ro&immutable=1', uri=True)
CONN.execute('PRAGMA query_only=ON')
HEX64 = re.compile(r'^[0-9A-Fa-f]{64}$')

def source_code(va):
    row = CONN.execute('SELECT code FROM functions WHERE entry_va=?', (va,)).fetchone()
    if not row or not row[0]:
        raise AssertionError(f'No code for {va}')
    return row[0]

def rows(va):
    return [[a, b] for a, b in CONN.execute('SELECT site_va,callee_va FROM calls WHERE caller_va=? ORDER BY site_va', (va,))]

def digest(x):
    return isinstance(x, str) and bool(HEX64.fullmatch(x))

def schema_ready(c):
    if c.get('capture_source') != 'SYNTHETIC':
        return False  # Synthetic runner only: never validates an external native trace
    try:
        g0, g1, g2 = (c[k] for k in ('g0', 'g1', 'g2'))
        for key in ('run_id', 'scenario'):
            v = g0[key]
            if not isinstance(v, str) or not v or any(g[key] != v for g in (g1, g2)):
                return False
        for key in ('exe_sha', 'dat_sha'):
            v = g0[key]
            if not digest(v) or any(g[key] != v for g in (g1, g2)):
                return False
        if any(not digest(g['capture_sha']) for g in (g0, g1, g2)):
            return False
        if not (g1['at'] <= g0['at'] <= g2['at']):
            return False
        if g0['ui_legal'] is not True or g0['started'] is not True:
            return False
        if g1['unmodified_save'] is not True or not digest(g1['save_sha']) or not digest(g1['input_sha']):
            return False
        if not digest(g2['map_sha']):
            return False
        sides = g2['sides']
        if not isinstance(sides, list) or len(sides) != 3:
            return False
        if [side.get('role') for side in sides] != ['attack', 'defend', 'support']:
            return False
        side_ids = [side.get('id') for side in sides]
        if any(not isinstance(x, str) or not x for x in side_ids) or len(set(side_ids)) != 3:
            return False
        if not isinstance(g2['deployed'], list) or not g2['deployed']:
            return False
        if [row.get('order') for row in g2['deployed']] != list(range(len(g2['deployed']))):
            return False
        for row in g2['deployed']:
            if not all(k in row for k in ('side_id', 'troop', 'unit', 'x', 'y')):
                return False
            if (row['side_id'] not in side_ids or not row['troop'] or not row['unit']
                    or not isinstance(row['x'], int) or not isinstance(row['y'], int)):
                return False
        return True
    except (KeyError, TypeError, ValueError):
        return False

def actual_golden(c):
    # No authority to authenticate native captures in this synthetic/static runner.
    return False

def small_string_pointer_route(n):
    return 'inline_address' if n < 0x10 else 'external_pointer'

class StaticIndex(unittest.TestCase):
    def test_index_sha(self):
        self.assertEqual(hashlib.sha256(DB.read_bytes()).hexdigest().upper(), F['index_sha256'])
    def test_index_quickcheck(self):
        self.assertEqual(CONN.execute('PRAGMA quick_check').fetchone()[0], 'ok')
    def test_source_manifest_sha(self):
        self.assertEqual(F['source_exe_sha256'], 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187')
    def test_five_direct_callers_no_extra(self):
        observed = {r[0] for r in CONN.execute('SELECT DISTINCT caller_va FROM calls WHERE callee_va=?', ('0x0043F470',))}
        self.assertEqual(observed, {r['va'] for r in F['wrappers']})
    def test_sso_flag_branch_precedes_copy(self):
        s = source_code('0x0052D3D0')
        phrases = ['if (in_stack_00000018 < 0x10)', 'pcVar2 = (char *)&param_1;',
                   'cVar1 = *pcVar2;', "while (cVar1 != '\\0');", 'FUN_00402800();', 'FUN_0043f470();']
        pos = [s.index(x) for x in phrases]
        self.assertEqual(pos, sorted(pos))
    def test_inline_route_not_generic_to_all_wrappers(self):
        for r in F['wrappers']:
            if r['va'] != '0x0052D3D0':
                self.assertNotIn('if (in_stack_00000018 < 0x10)', source_code(r['va']))
    def test_wrapper_precedes_dialog_with_initializer(self):
        for r in F['wrappers']:
            s = source_code(r['va'])
            self.assertLess(s.index('FUN_0052ad90();'), s.index('FUN_0043f470();'))
    def test_string_copy_cleanup_not_same_as_display(self):
        r = next(x for x in F['wrappers'] if x['va'] == '0x0052D2E0')
        self.assertEqual(r['counts']['0x005B6BBB'], 0)  # local static call absence only
        self.assertEqual(r['counts']['0x00402800'], 4)
        self.assertIn('FUN_0043f470();', source_code(r['va']))
        self.assertNotIn('screen_display_confirmed', source_code(r['va']))
    def test_claimed_native_zero(self):
        self.assertEqual((F['claimed_native_observed'], F['claimed_actual_golden_pass'], F['claimed_strict_match']), (0, 0, 0))

def make_wrapper_test(r,what):
    def test(self):
        if what == 'sha':
            self.assertEqual(hashlib.sha256(source_code(r['va']).encode('utf8')).hexdigest().upper(), r['code_sha256'])
        elif what == 'site_matrix':
            self.assertEqual(rows(r['va']), r['edges'])
        elif what == 'counts':
            observed = rows(r['va'])
            self.assertEqual({k:sum(x[1] == k for x in observed) for k in r['counts']}, r['counts'])
        elif what == 'dialog_once':
            self.assertEqual(sum(x[1]=='0x0043F470' for x in rows(r['va'])), 1)
    return test

for ix,r in enumerate(F['wrappers']):
    for part in ('sha','site_matrix','counts','dialog_once'):
        setattr(StaticIndex, f'test_wrapper_{ix:02}_{part}', make_wrapper_test(r,part))
for ix,c in enumerate(F['synthetic_cases']):
    if 'record' in c:
        def test(self,c=c):
            self.assertIs(schema_ready(c['record']), c['structure_expected'], c['case'])
            self.assertIs(actual_golden(c['record']), c['actual_expected'], c['case'])
        setattr(StaticIndex, f'test_lineage_synthetic_{ix:02}', test)
    else:
        def test(self,c=c):
            self.assertEqual(small_string_pointer_route(c['sso_value']),c['sso_expected'],c['case'])
        setattr(StaticIndex, f'test_sso_synthetic_{ix:02}', test)

if __name__ == '__main__':
    unittest.main(argv=[__file__],verbosity=2)
