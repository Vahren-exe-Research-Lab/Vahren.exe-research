"""Step 7: check FINDINGS meanings against the real saves (read-only).

F§58/§62: +0x77 = master of a (non-event) power, +0x78 = troop leader,
+0x74 = player's own unit (ctx+0x50), +0x80 rank (+0x77 -> 4),
+0xC0 loyal, +0xC4 trust (<=100), +0xC8 acted turn, +0xD0 leave turn,
+0xD4 members, Power+0x24 master, Power+0x64 territory, Power+0xD0 fix.
"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, 'pkg'))
from hakushin_compat.normal_save_body_and_tail import read_normal_save_body_and_tail
from run_body_tail import SAVEDIR


def d(b):
    return b.decode('ascii', 'replace')


def check(n):
    s = read_normal_save_body_and_tail(open(os.path.join(SAVEDIR, n), 'rb').read()).save
    U = {d(u.key): u for u in s.units}
    turn = s.diplomacy.scalar_u32_14
    r = {'turn(+0x14)': turn}
    masters = {d(p.name24) for p in s.powers}
    active_masters = {d(p.name24) for p in s.powers if p.byte_1c}
    f77 = {k for k, u in U.items() if u.prelude.flags_74_to_7a[3]}
    r['+0x77 units == masters of +0x1C powers'] = f77 == (active_masters & set(U))
    r['+0x77 minus masters'] = sorted(f77 - masters)[:5]
    r['active masters without +0x77'] = sorted((active_masters & set(U)) - f77)[:5]
    f74 = [k for k, u in U.items() if u.prelude.flags_74_to_7a[0]]
    player = [p for p in s.powers if p.byte_1d]
    r['+0x74 units'] = f74
    r['player power master'] = [d(p.name24) for p in player]
    r['rank(+0x80) of +0x77 units'] = dict(collections.Counter(U[k].prelude.dwords[0x80] for k in f77))
    leaders = {k for k, u in U.items() if u.prelude.flags_74_to_7a[4]}
    members = {d(c) for u in s.units for c in u.prelude.string_vectors[0]}
    r['+0x78 leaders'] = len(leaders)
    r['units with members (+0xD4)'] = sum(1 for u in s.units if u.prelude.string_vectors[0])
    r['members that are leaders'] = len(members & leaders)
    r['units with +0xD4 but not +0x78'] = sum(1 for k, u in U.items() if u.prelude.string_vectors[0] and k not in leaders and not u.prelude.strings[0x84])
    r['spot-set units: leaders+members+others'] = None
    inspot = {d(m) for sp in s.spots for m in sp.value.tree_key_names}
    r['spot-set units that are neither leader nor member'] = len(inspot - leaders - members)
    r['+0xC8 max <= turn'] = max(u.prelude.dwords[0xC8] - (1 << 32) if u.prelude.dwords[0xC8] >= 1 << 31 else u.prelude.dwords[0xC8] for u in s.units) <= turn
    r['+0xC4 <= 100'] = all(u.prelude.dwords[0xC4] <= 100 for u in s.units)
    r['+0xD0 values'] = dict(collections.Counter(u.prelude.dwords[0xD0] for u in s.units).most_common(3))
    r['+0xE4 top'] = collections.Counter(u.prelude.dwords[0xE4] for u in s.units).most_common(4)
    r['Power+0xD0 fix values'] = dict(collections.Counter(p.tail.fixtype_d0 for p in s.powers))
    r['Power+0x5C player'] = [p.dword_5c for p in player]
    r['Power+0x60 all 0x80000008'] = all(p.dword_60 == 0x80000008 for p in s.powers)
    r['+0x174 nonzero units'] = sum(1 for u in s.units if u.prelude.dwords[0x174])
    r['+0x174 nonzero and +0x7C/+0xA0'] = sum(1 for u in s.units if u.prelude.dwords[0x174] and (u.arbeit_7c_u32 or u.arbeit_user_a0))
    return r


if __name__ == '__main__':
    out = {n: check(n) for n in ('save1.sav', 'save3.sav')}
    for n, r in out.items():
        print('==', n)
        for k, v in r.items():
            print('  ', k, ':', v)
    json.dump(out, open(os.path.join(WORK, 'out', 'findings_vs_save.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, default=str)
