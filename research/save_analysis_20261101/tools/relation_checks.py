"""Step 4b: cross-record relations in the real saves (read-only observations)."""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, 'pkg'))
from hakushin_compat.normal_save_body_and_tail import read_normal_save_body_and_tail
from run_body_tail import SAVEDIR


def d(b):
    return b.decode('ascii', 'replace')


def check(name):
    s = read_normal_save_body_and_tail(open(os.path.join(SAVEDIR, name), 'rb').read()).save
    r = {}
    units = {d(u.key): u for u in s.units}
    # Unit+0x1C vs key without '+N'
    r['unit_1C_eq_key_base'] = f"{sum(d(u.prelude.strings[0x1C]) == d(u.key).split('+')[0] for u in s.units)}/{len(s.units)}"
    r['unit_1C_eq_key'] = f"{sum(d(u.prelude.strings[0x1C]) == d(u.key) for u in s.units)}/{len(s.units)}"
    r['unit_54_startswith_1C'] = f"{sum(d(u.prelude.strings[0x54]).startswith(d(u.prelude.strings[0x1C])) for u in s.units if u.prelude.strings[0x54])}/{sum(1 for u in s.units if u.prelude.strings[0x54])}"
    # Spot member sets vs Unit+0x84
    member_of = collections.Counter()
    for sp in s.spots:
        for m in sp.value.tree_key_names:
            member_of[d(m)] += 1
    roaming = {k for k, u in units.items() if u.prelude.strings[0x84]}
    inspot = set(member_of)
    r['units_total'] = len(units)
    r['units_in_some_spot_set'] = len(inspot)
    r['units_in_two_or_more_spot_sets'] = sum(1 for v in member_of.values() if v > 1)
    r['roaming_units(+0x84 nonempty)'] = len(roaming)
    r['roaming_and_in_spot_set'] = len(roaming & inspot)
    neither = sorted(set(units) - inspot - roaming)
    r['neither_spot_set_nor_roaming'] = neither[:10]
    r['neither_count'] = len(neither)
    r['neither_flags74_7A'] = {k: list(units[k].prelude.flags_74_to_7a) for k in neither[:5]}
    # Power: byte_1c vs nonempty +0x68 vs diplomacy refs
    p1c = {d(p.key) for p in s.powers if p.byte_1c}
    p68 = {d(p.key) for p in s.powers if p.tree68_names}
    dip = {d(x) for x in s.diplomacy.power_reference_names}
    r['power_1c_set==power_with_68'] = p1c == p68
    r['power_1c_set==diplomacy_refs'] = p1c == dip
    r['diplomacy_minus_1c'] = sorted(dip - p1c)
    r['1c_minus_diplomacy'] = sorted(p1c - dip)
    own = collections.Counter(d(x) for p in s.powers for x in p.tree68_names)
    r['spot_in_two_power_68_sets'] = sum(1 for v in own.values() if v > 1)
    r['spots_owned'] = len(own)
    # Power+0x24 -> Unit: is that unit's flag 0x74 (master) set?
    m = []
    for p in s.powers:
        u = units.get(d(p.name24))
        m.append((d(p.key), d(p.name24), None if u is None else u.prelude.flags_74_to_7a[0],
                  None if u is None else d(u.prelude.strings[0x84])))
    r['power_24_unit_flag74'] = {str(k): v for k, v in collections.Counter(x[2] for x in m).items()}
    r['power_24_examples'] = m[:4]
    # header power vs byte_1d
    r['header_power'] = d(s.front.power_id)
    r['byte_1d_powers'] = [d(p.key) for p in s.powers if p.byte_1d]
    # Unit flag 0x74 unit & its Spot set membership
    m74 = [k for k, u in units.items() if u.prelude.flags_74_to_7a[0]]
    r['flag74_units'] = m74
    # Unit +0xD4 children: each child points back? (child +0x54 / +0x1C)
    kids = [(k, d(c)) for k, u in units.items() for c in u.prelude.string_vectors[0]]
    r['units_with_D4'] = sum(1 for u in s.units if u.prelude.string_vectors[0])
    r['D4_children_distinct'] = len({c for _, c in kids})
    r['D4_child_in_two_lists'] = sum(1 for v in collections.Counter(c for _, c in kids).values() if v > 1)
    r['D4_child_in_same_spot_as_parent'] = None
    spot_of = {}
    for sp in s.spots:
        for mm in sp.value.tree_key_names:
            spot_of[d(mm)] = d(sp.key)
    r['D4_child_same_spot'] = f"{sum(spot_of.get(p) == spot_of.get(c) for p, c in kids)}/{len(kids)}"
    r['Unit_E8_vs_D4'] = {str(k): v for k, v in collections.Counter((u.prelude.flag_e8, bool(u.prelude.string_vectors[0])) for u in s.units).items()}
    r['Unit_E8_vs_child'] = {str(k): v for k, v in collections.Counter((units[c].prelude.flag_e8) for _, c in kids if c in units).items()}
    return r


if __name__ == '__main__':
    out = {}
    for n in ('save1.sav', 'save3.sav'):
        out[n] = check(n)
        print(n, json.dumps(out[n], ensure_ascii=False, default=str))
    json.dump(out, open(os.path.join(WORK, 'out', 'relation_checks.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, default=str)
