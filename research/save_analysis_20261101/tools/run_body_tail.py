"""Step 1: read save1..3/auto with the body+stale-tail parser (read-only)."""
import hashlib, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, 'pkg'))
from hakushin_compat.normal_save_body_and_tail import read_normal_save_body_and_tail

SAVEDIR = os.environ.get('HAKUSHIN_SAVE_DIR') or os.path.join(WORK, '..', 'startup_clean_20261025',
                       '新約迫真戦記―ほのぼの神話ver0.67 豪華版', 'a_default')
NAMES = ['save1.sav', 'save2.sav', 'save3.sav', 'auto.sav']


def main():
    out = {}
    for n in NAMES:
        p = os.path.join(SAVEDIR, n)
        st = os.stat(p)
        raw = open(p, 'rb').read()
        t0 = time.time()
        r = read_normal_save_body_and_tail(raw)
        f = r.save.front
        out[n] = {
            'file_len': r.file_len, 'file_sha256': hashlib.sha256(raw).hexdigest(),
            'mtime_local': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime)),
            'body_plain_len': r.body_plain_len, 'body_file_len': r.body_file_len,
            'stale_tail_len': r.stale_tail_len,
            'body_reencode_exact': True,
            'leading_u32': f.leading_u32, 'scenario': f.scenario_id.decode(),
            'power': f.power_id.decode(), 'u32x5': list(f.unknown_u32x5),
            'counts': r.save.counts(), 'section_offsets': r.section_offsets,
            'key28_hex': f.stored_key28.hex(), 'sec': round(time.time() - t0, 1),
        }
        print(n, json.dumps(out[n], ensure_ascii=False))
    with open(os.path.join(WORK, 'out', 'body_tail_summary.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    os.makedirs(os.path.join(WORK, 'out'), exist_ok=True)
    main()
