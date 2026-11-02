"""E-only T018/T020 synthetic Golden capture semantic binding regression.

Run:
    python t020_golden_capture_semantic_binding_gate_20261028_2149.py --db /path/search.sqlite

Static read-only 2026-10-21 index. This is NOT native authentication.
The strengthened semantic capture is synthetic-only and cannot establish actual Golden.
"""
import argparse
import base64
import copy
import hashlib
import json
import runpy
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PARENT=next((p for p in (ROOT.parent/'E_20261028_2045',ROOT)
             if (p/'t020_golden_lineage_content_bound_gate_20261028_2045.py').is_file()),
            ROOT.parent/'E_20261028_2045')
PARENT_FIXTURE=PARENT/'T020_GOLDEN_LINEAGE_CONTENT_BOUND_CASES_20261028_2045.json'
PARENT_SCRIPT=PARENT/'t020_golden_lineage_content_bound_gate_20261028_2045.py'
F=json.loads((ROOT/'T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json').read_text(encoding='utf-8'))
parser=argparse.ArgumentParser()
parser.add_argument('--db',required=True)
args=parser.parse_args()
DB=Path(args.db).resolve()
if not DB.is_file():
    raise FileNotFoundError(DB)

# Reuse previous E gate exactly as saved, rather than duplicating/refactoring its behavior.
old_args=sys.argv
try:
    sys.argv=[str(PARENT_SCRIPT),'--db',str(DB)]
    P=runpy.run_path(str(PARENT_SCRIPT),run_name='e2149_import_e2045')
finally:
    sys.argv=old_args
prior_ready=P['hardened_synthetic_ready']
original_actual_golden=P['OLD']['actual_golden']


def digest(raw):
    return hashlib.sha256(raw).hexdigest().upper()


def canonical_payload(rec,stage):
    """Illustrative synthetic-only capture contract, not original engine format."""
    fields={k:v for k,v in rec.items() if k not in ('capture_sha','capture_b64')}
    blob={'format':F['schema'],'stage':stage,'fields':fields}
    return json.dumps(blob,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')


def bind_synthetic(c):
    """Self-sign a synthetic fixture; explicitly *not* independent authenticity."""
    for stage in ('g1','g0','g2'):
        r=c[stage]
        if stage=='g0':
            r['previous_capture_sha']=c['g1']['capture_sha']
        if stage=='g2':
            r['previous_capture_sha']=c['g0']['capture_sha']
        raw=canonical_payload(r,stage)
        r['capture_b64']=base64.b64encode(raw).decode('ascii')
        r['capture_sha']=digest(raw)
    return c


def semantic_ready(c):
    """Schema lint only. Cannot certify native provenance or legal original UI."""
    if not prior_ready(c):
        return False
    try:
        for stage in ('g1','g0','g2'):
            rec=c[stage]
            # Unknown fields require a versioned schema update, not silent acceptance.
            if set(rec)!=set(F['allowed_keys'][stage]):
                return False
            raw=base64.b64decode(rec['capture_b64'],validate=True)
            if raw!=canonical_payload(rec,stage):
                return False
        return True
    except (KeyError,TypeError,ValueError,UnicodeError,OverflowError):
        return False


def apply_changes(c,changes):
    result=copy.deepcopy(c)
    for p,v in changes:
        loc=result
        for key in p[:-1]:
            loc=loc[int(key) if isinstance(loc,list) else key]
        loc[int(p[-1]) if isinstance(loc,list) else p[-1]]=v
    return result


def make_record(row):
    c=apply_changes(F['base'],row['changes'])
    if row['mode']=='rebind':
        c=bind_synthetic(c)
    elif row['mode'] in ('noncanonical_capture','duplicate_key_capture'):
        # Deliberately make a *cryptographically internally consistent* opaque
        # capture. Previous E20h logic checks hashes/parent edges but not the
        # decoded payload's correspondence to the visible manifest fields.
        raw=base64.b64decode(c['g0']['capture_b64'],validate=True)
        if row['mode']=='noncanonical_capture':
            raw=b'not-canonical:'+raw
        else:
            assert b'"stage":"g0"' in raw
            raw=raw.replace(b'"stage":"g0"',b'"stage":"forged","stage":"g0"',1)
        c['g0']['capture_b64']=base64.b64encode(raw).decode('ascii')
        c['g0']['capture_sha']=digest(raw)
        # Rebuild the downstream G2 link, but leave G0 payload itself opaque.
        c['g2']['previous_capture_sha']=c['g0']['capture_sha']
        rec=c['g2']
        blob=canonical_payload(rec,'g2')
        rec['capture_b64']=base64.b64encode(blob).decode('ascii')
        rec['capture_sha']=digest(blob)
    elif row['mode']!='changes':
        raise ValueError(row['mode'])
    return c


class EvidenceGate(unittest.TestCase):
    def test_parent_fixture_unmodified(self):
        self.assertEqual(digest(PARENT_FIXTURE.read_bytes()),F['parent_fixture_sha256'])

    def test_parent_gate_unmodified(self):
        self.assertEqual(digest(PARENT_SCRIPT.read_bytes()),F['parent_gate_sha256'])

    def test_20261021_db_sha_read_only(self):
        self.assertEqual(digest(DB.read_bytes()),F['sqlite_sha256'])
        with sqlite3.connect('file:'+DB.as_posix()+'?mode=ro&immutable=1',uri=True) as conn:
            conn.execute('PRAGMA query_only=ON')
            self.assertEqual(conn.execute('PRAGMA quick_check').fetchone()[0],'ok')

    def test_source_zip_recorded_not_rehashed_here(self):
        self.assertEqual(F['source_zip_sha256'],'911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2')

    def test_semantically_bound_synthetic_control(self):
        self.assertTrue(prior_ready(F['base']))
        self.assertTrue(semantic_ready(F['base']))

    def test_schema_has_exact_stage_keys(self):
        for stage in ('g0','g1','g2'):
            self.assertEqual(set(F['base'][stage]),set(F['allowed_keys'][stage]))

    def test_native_claims_must_remain_zero(self):
        self.assertEqual(F['golden'],dict(dynamic_observed=0,actual_golden_pass=0,strict_match=0))
        self.assertFalse(original_actual_golden(F['base']))

    def test_new_detection_count(self):
        self.assertEqual(len(F['cases']),36)
        self.assertEqual(sum(row['prior_accept'] and not row['semantic_accept'] for row in F['cases']),31)

    def test_synthetic_self_reseal_is_not_native(self):
        rec=make_record(next(r for r in F['cases'] if r['case']=='valid_rebound_scenario'))
        self.assertTrue(semantic_ready(rec))
        self.assertFalse(original_actual_golden(rec))


def case_test(row):
    def test(self):
        c=make_record(row)
        self.assertIs(prior_ready(c),row['prior_accept'],row['case']+' prior')
        self.assertIs(semantic_ready(c),row['semantic_accept'],row['case']+' semantic')
        self.assertFalse(original_actual_golden(c),row['case']+' native')
    return test

for i,row in enumerate(F['cases']):
    setattr(EvidenceGate,f"test_synthetic_{i:02d}_{row['case']}",case_test(row))

if __name__=='__main__':
    unittest.main(argv=[__file__],verbosity=2)
