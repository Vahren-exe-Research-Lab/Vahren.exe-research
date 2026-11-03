"""E/T020 static corpus scope test: never claims runtime Golden compatibility."""
from pathlib import Path
import hashlib, json, sys

def main():
    repo = Path(__file__).resolve().parents[1]
    spec = json.loads((Path(__file__).parent / 'T020_GAMECLEAR_CENSUS_SCOPE_20261021.json').read_text(encoding='utf-8-sig'))
    root = repo / Path(spec['source_root'])
    assert root.is_dir(), f'missing normalized corpus: {root}'
    found = {}
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in ('.dat', '.txt'):
            continue
        lines = p.read_text(encoding='utf-8-sig').splitlines()
        hits = [idx for idx, line in enumerate(lines, 1) if 'setGameClear' in line]
        if hits:
            found[p.relative_to(root).as_posix()] = hits
    assert found == spec['expected'], f'source mismatch: {found!r}'
    for rel, known_sha in spec['sha256'].items():
        digest = hashlib.sha256((root / rel).read_bytes()).hexdigest().upper()
        assert digest == known_sha, f'hash mismatch: {rel}'
    dat = {k: v for k, v in found.items() if k.endswith('.dat')}
    txt = {k: v for k, v in found.items() if k.endswith('.txt')}
    for kind, group in [('DAT', dat), ('TXT', txt), ('TOTAL', found)]:
        assert (sum(map(len, group.values())), len(group)) == (spec['buckets'][kind]['matches'], spec['buckets'][kind]['files']), kind
    assert spec['gameplay_dynamic'] == 'NOT_RUN' and spec['strict_match'] == 0
    print('PASS STATIC ONLY: DAT=13/9 TXT=2/1 TOTAL=15/10; SHA256=2/2; Gameplay NOT RUN')

if __name__ == '__main__':
    main()
