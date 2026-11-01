"""Step 4: per-field statistics of Unit / Spot / Power in the real saves.

For each saved field: kind, distinct count, examples, and reference checks
(does every non-empty value equal a Unit / Spot / Power key, or the
record's own key?). These are observations on 2 save states
(save1 = early, save3 = later); they support but do not prove meanings.
Read-only. Output: out/field_stats.json
"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, 'pkg'))
from hakushin_compat.normal_save_body_and_tail import read_normal_save_body_and_tail
from run_body_tail import SAVEDIR


def d(b):
    return b.decode('ascii', 'replace') if isinstance(b, bytes) else b


def str_field(values, refs, own_keys=None):
    vals = [d(v) for v in values]
    ne = [v for v in vals if v]
    c = collections.Counter(vals)
    out = {'kind': 'str', 'n': len(vals), 'empty': len(vals) - len(ne), 'distinct': len(c),
           'top': c.most_common(5)}
    for rn, rs in refs.items():
        if ne:
            out['in_' + rn] = f"{sum(v in rs for v in ne)}/{len(ne)}"
    if own_keys is not None:
        out['equals_own_key'] = f"{sum(a == b for a, b in zip(vals, own_keys))}/{len(vals)}"
    return out


def num_field(values):
    c = collections.Counter(values)
    return {'kind': 'u32', 'n': len(values), 'distinct': len(c), 'min': min(values) if values else None,
            'max': max(values) if values else None, 'top': c.most_common(6)}


def list_field(lists, refs):
    flat = [d(x) for l in lists for x in l]
    c = collections.Counter(flat)
    out = {'kind': 'list', 'records_nonempty': sum(1 for l in lists if l), 'items': len(flat),
           'distinct': len(c), 'top': c.most_common(6)}
    for rn, rs in refs.items():
        if flat:
            out['in_' + rn] = f"{sum(v in rs for v in flat)}/{len(flat)}"
    return out


def analyse(name):
    raw = open(os.path.join(SAVEDIR, name), 'rb').read()
    s = read_normal_save_body_and_tail(raw).save
    U = {d(u.key) for u in s.units}
    S = {d(x.key) for x in s.spots}
    P = {d(x.key) for x in s.powers}
    N = {d(x.key) for x in s.front.records}
    refs = {'Unit': U, 'Spot': S, 'Power': P}
    res = {'Unit': {}, 'Spot': {}, 'Power': {}}
    uk = [d(u.key) for u in s.units]
    for off in (0x00, 0x1C, 0x38, 0x54, 0x84):
        res['Unit'][f'+0x{off:02X} str'] = str_field([u.prelude.strings[off] for u in s.units], refs, uk)
    for off in (0x70, 0x80, 0xC8, 0xCC, 0x174, 0xBC, 0xC0, 0xC4, 0xD0, 0xE4):
        res['Unit'][f'+0x{off:02X} u32'] = num_field([u.prelude.dwords[off] for u in s.units])
    for i in range(7):
        res['Unit'][f'+0x{0x74 + i:02X} u8'] = num_field([u.prelude.flags_74_to_7a[i] for u in s.units])
    res['Unit']['+0xE8 u8'] = num_field([u.prelude.flag_e8 for u in s.units])
    for i, (b, _) in enumerate(((0xD4, 0), (0xEC, 0), (0xFC, 0), (0x10C, 0))):
        res['Unit'][f'+0x{b:02X} vec<str>'] = list_field([u.prelude.string_vectors[i] for u in s.units], refs)
    res['Unit']['+0x130 map<str,u32> keys'] = list_field([[k for k, _ in u.tree_130] for u in s.units],
                                                        {**refs, 'numeric': N})
    res['Unit']['+0x130 values'] = num_field([v for u in s.units for _, v in u.tree_130] or [0])
    res['Unit']['+0x7C u32 (arbeit)'] = num_field([u.arbeit_7c_u32 for u in s.units])
    res['Unit']['+0xA0 str (arbeit_user)'] = str_field([u.arbeit_user_a0 for u in s.units], refs, uk)
    res['Unit']['+0x11C vec<str> (item_skill)'] = list_field([u.item_skill_11c for u in s.units], refs)
    res['Unit']['+0x158 set<str> (friend)'] = list_field([u.friend_15c for u in s.units], refs)
    res['Unit']['+0x13C str'] = str_field([u.string_13c for u in s.units], refs, uk)
    for off, v in zip((0x168, 0x16C, 0x170, 0x178, 0x17C, 0x180, 0x184, 0x188, 0x18C, 0x194, 0x190,
                       0x198, 0x19C, 0x1A0), zip(*[u.tail_dwords for u in s.units])):
        vv = [x - (1 << 32) if x >= 1 << 31 else x for x in v]
        res['Unit'][f'+0x{off:03X} i32'] = num_field(vv)
    sk = [d(x.key) for x in s.spots]
    for f in ('name_00', 'name_2c', 'name_64', 'dunname_48'):
        res['Spot'][f] = str_field([getattr(x.value, f) for x in s.spots], refs, sk)
    for f in ('dword_80', 'dword_84', 'capacity_88', 'castlebattle_8c', 'fightvalue_90'):
        res['Spot'][f] = num_field([getattr(x.value, f) for x in s.spots])
    res['Spot']['+0x1C set<str> (tree)'] = list_field([x.value.tree_key_names for x in s.spots], refs)
    pk = [d(x.key) for x in s.powers]
    for f in ('name00', 'name24', 'name40', 'name74'):
        res['Power'][f] = str_field([getattr(x, f) for x in s.powers], refs, pk)
    for f in ('byte_1c', 'byte_1d', 'dword_5c', 'dword_20', 'dword_60'):
        res['Power'][f] = num_field([getattr(x, f) for x in s.powers])
    res['Power']['+0x68 set<str>'] = list_field([x.tree68_names for x in s.powers], refs)
    res['Power']['+0x90 vec<str>'] = list_field([x.vector90_names for x in s.powers], refs)
    res['Power']['+0xA4 set<str>'] = list_field([x.treea4_names for x in s.powers], refs)
    res['Power']['+0xB4 map<str,u32> keys'] = list_field([[k for k, _ in x.treeb4_pairs] for x in s.powers], refs)
    res['Power']['+0xB4 values'] = num_field([v for x in s.powers for _, v in x.treeb4_pairs] or [0])
    for f in ('fixtype_d0', 'train_max_d4', 'train_up_d8', 'base_level_dc'):
        res['Power'][f] = num_field([getattr(x.tail, f) for x in s.powers])
    res['Power']['home_spot vec<str>'] = list_field([x.tail.home_spot_names for x in s.powers], refs)
    res['Power']['byte_1d==1 keys'] = [d(x.key) for x in s.powers if x.byte_1d]
    res['Power']['byte_1c==1 keys'] = [d(x.key) for x in s.powers if x.byte_1c]
    res['header_power'] = d(s.front.power_id)
    res['Unit_flag74_keys_sample'] = [d(u.key) for u in s.units if u.prelude.flags_74_to_7a[0]][:5]
    return res


if __name__ == '__main__':
    out = {n: analyse(n) for n in ('save1.sav', 'save3.sav')}
    json.dump(out, open(os.path.join(WORK, 'out', 'field_stats.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    for n, r in out.items():
        print('=====', n, 'header_power', r['header_power'], 'P1d', r['Power']['byte_1d==1 keys'],
              'P1c', r['Power']['byte_1c==1 keys'], 'U74', r['Unit_flag74_keys_sample'])
        for grp in ('Unit', 'Spot', 'Power'):
            for k, v in r[grp].items():
                if isinstance(v, dict):
                    vv = {a: b for a, b in v.items() if a not in ('n',)}
                    print(grp, k, json.dumps(vv, ensure_ascii=False)[:260])
