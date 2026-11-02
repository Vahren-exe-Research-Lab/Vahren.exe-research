# E-only: local synthetic/statics; never starts the original game.
import hashlib, json, struct, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
CASE=ROOT/'tests'/'T020_E_T013_T028_D0_SORT_IDENTITY_CASES_20261030_12H.json'
SOURCE=ROOT/'data'/'T013_T028_BATTLE_D0_PRODUCER_SORT_COMPARATOR_NATIVE_20261030_12H.md'
PE=ROOT/'rea_lab'/'targets'/'hakushin067_Vahren.exe'
RID='E-AUDIT-20261030-12H-T020-T013-T028-D0-SORT-IDENTITY-01'
B_SHA='552F1ED1E478C0CBFC803DA5FA4A7F6EF2856F30E03FD7A7D6D6AA3D2B2674FD'
PE_SHA='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
NEG=['d0_is_sort_key','sort_is_stable','e4_is_verified_game_name','comparator_is_unsigned',
     'nan_order_is_proven','unit_pointer_is_native_observed','synthetic_is_golden','consumer_identity_is_proven']
def digest(raw): return hashlib.sha256(raw).hexdigest().upper()
def signed(v):
    assert isinstance(v,int) and -(1<<31)<=v<(1<<31)
    return v
def model(route,score,a,b):
    assert route in ('sentinel','compute') and isinstance(score,(float,int))
    d0=1000000.0 if route=='sentinel' else max(2.0,float(score))
    return d0, signed(a)<signed(b)
def init():
    if CASE.exists(): raise FileExistsError('E-owned fixture already exists; no overwrite')
    pairs=[[-1,0],[0,-1],[0,0],[2147483647,-2147483648]]
    rows=[]
    for route in ('sentinel','compute'):
        for score in (0.5,1.99,2.0,20.0):
            for a,b in pairs:
                d0,lt=model(route,score,a,b)
                rows.append(dict(id=f'M{len(rows)+1:03}',kind='model',route=route,score=score,
                                 unit_e4_a=a,unit_e4_b=b,expected_d0=d0,expected_signed_lt=lt))
    edges=[[-2147483648,0],[0,-2147483648],[2147483647,0],[0,2147483647],
           [-2147483648,2147483647],[2147483647,2147483647],
           [-1,-2147483648],[-2147483648,-1]]
    for a,b in edges:
        rows.append(dict(id=f'S{len(rows)+1:03}',kind='signed_edge',route='compute',score=2.0,
                         unit_e4_a=a,unit_e4_b=b,expected_d0=2.0,expected_signed_lt=a<b))
    for claim in NEG:
        rows.append(dict(id=f'N{len(rows)+1:03}',kind='negative',claim=claim,must_reject=True))
    assert len(rows)==48
    CASE.write_text(json.dumps({'research_id':RID,'kind':'STATIC_SYNTHETIC_NOT_GAMEPLAY',
      'case_count':len(rows),'cases':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def native(raw):
    peoff=struct.unpack_from('<I',raw,0x3c)[0]
    assert raw[peoff:peoff+4]==b'PE\0\0'
    coff=peoff+4; num=struct.unpack_from('<H',raw,coff+2)[0]
    opt=coff+20; sz=struct.unpack_from('<H',raw,coff+16)[0]
    base=struct.unpack_from('<I',raw,opt+28)[0]
    def at(va,n):
        rva=va-base
        for i in range(num):
            off=opt+sz+i*40
            vsize,vaddr,rsize,rptr=struct.unpack_from('<IIII',raw,off+8)
            if vaddr<=rva and rva+n<=vaddr+rsize:
                return raw[rptr+rva-vaddr:rptr+rva-vaddr+n]
        raise AssertionError('VA unmapped: '+hex(va))
    windows={0x51EF80:(64,'7D8940F552E10B91ECEBAB4A0310E3AFEA8E8C0D38115E342351FBC503AF17DC'),
             0x5146F0:(67,'66C3916B01E26F9F3D0836F5EB6772BBADC508539F871A13360B16B4BBCA4407'),
             0x447D52:(319,'09D7C23D0018426D64155D10F695AD8A6C736CE086A762B97F2A341F3B66B222')}
    for va,(count,expected) in windows.items():
        assert digest(at(va,count))==expected,hex(va)
    for va,dest in ((0x51EF8F,0x447810),(0x51EFA9,0x47BB50)):
        code=at(va,5)
        assert code[0]==0xe8,hex(va)
        assert ((va+5+struct.unpack('<i',code[1:])[0])&0xffffffff)==dest,hex(va)
    return {'pe_window_sha':3,'direct_e8_calls':2}
def main():
    if '--init' in sys.argv: init()
    assert digest(SOURCE.read_bytes())==B_SHA,'B source modified; stop'
    raw=PE.read_bytes()
    assert digest(raw)==PE_SHA,'Original research copy hash mismatch'
    n=native(raw)
    doc=json.loads(CASE.read_text(encoding='utf-8'))
    rows=doc['cases']
    assert doc['research_id']==RID and doc['case_count']==len(rows)==48
    assert len({r['id'] for r in rows})==len(rows)
    counts={'model':0,'signed_edge':0,'negative':0}
    for row in rows:
        kind=row['kind']
        if kind=='negative':
            assert row['claim'] in NEG and row['must_reject'] is True
        else:
            got=model(row['route'],row['score'],row['unit_e4_a'],row['unit_e4_b'])
            want=(row['expected_d0'],row['expected_signed_lt'])
            assert got==want,(row['id'],got,want)
        counts[kind]+=1
    assert counts=={'model':32,'signed_edge':8,'negative':8}
    print(json.dumps({'research_id':RID,'result':'PASS_SYNTHETIC_STATIC',
      'counts':counts,'native':n,'source_sha256':B_SHA,'pe_sha256':PE_SHA,
      'case_sha256':digest(CASE.read_bytes()),'golden_actual_pass':0,'strict_match':0,
      'gameplay':'NOT_RUN','new_ready':0},ensure_ascii=False))
if __name__=='__main__': main()
