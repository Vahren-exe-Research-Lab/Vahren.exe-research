"""Read-only E/T020 audit: compare 2026-10-28 Library-pinned bytes against PC staging."""
from pathlib import Path
import hashlib
import json

TESTS = Path(__file__).resolve().parent
STAGING = TESTS / 'E_OFFLINE_SYNC_20261029'
OFFLINE = TESTS / 'OFFLINE_UNSYNCED_E_20261028'
MANIFEST = STAGING / 'T020_E_LIBRARY_SOURCE_MANIFEST_20261029_04H.json'

def check(folder, entries):
    out = {'match': [], 'missing': [], 'hash_mismatch': []}
    for row in entries:
        p = folder / row['name']
        if not p.is_file():
            out['missing'].append(row['name'])
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest().upper()
        out['match' if h == row['sha256'] and p.stat().st_size == row['bytes'] else 'hash_mismatch'].append(row['name'])
    return out

def main():
    doc = json.loads(MANIFEST.read_bytes())
    entries = doc['items']
    assert len(entries) == 23 and len({x['name'] for x in entries}) == 23
    assert sum(x['bytes'] for x in entries) == 210955
    results = {'source_pin_count': len(entries), 'staging': check(STAGING, entries), 'offline': check(OFFLINE, entries)}
    pinned = STAGING / 'T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149_LIBPIN_7D574F25.json'
    results['canonical_21h_pin_sha'] = hashlib.sha256(pinned.read_bytes()).hexdigest().upper()
    assert results['canonical_21h_pin_sha'] == '7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA'
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
