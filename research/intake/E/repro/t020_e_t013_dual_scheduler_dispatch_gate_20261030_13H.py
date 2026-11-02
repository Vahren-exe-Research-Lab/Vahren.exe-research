# E-only synthetic regression for B T013 dual scheduler; never executes Vahren.
import hashlib, json, struct, sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent
RID='E-AUDIT-20261030-13H-T020-T013-DUAL-SCHEDULER-STATIC-GATE-01'
CASE=R/'tests'/'T020_E_T013_DUAL_SCHEDULER_CASES_20261030_13H.json'
BS=R/'data'/'T013_BATTLE_AI_DUAL_MODE_DISPATCH_JUMPTABLE_NATIVE_20261030_13H.md'
PE=R/'rea_lab'/'targets'/'hakushin067_Vahren.exe'
B_SHA='937AD21872E14AE302E3852CAE487B60344842510A84E30FDCB72EEFC5DAB2F1'
PE_SHA='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
NEG=['scheduler_paths_are_equivalent','negative_mode_is_mode0','mode1_never_changes',
     'flag_always_changes_mode','mode0_always_calls_b240','all_targets_observed',
     'producer_consumer_same_object','synthetic_pass_is_golden']
def sha(data): return hashlib.sha256(data).hexdigest().upper()
def route_a(mode,rem):
    if rem: return 'EARLY_TICK_RET'
    if mode==0: return 'CALL_44AE70'
    if mode in (1,2,3): return 'CALL_44CD70'
    return 'SKIP_CALLS'
def route_b(mode,flag,rem):
    if flag==0 and rem: return ('EARLY_RET',mode)
    eff=2 if (mode==1 and flag!=0) else mode
    return ({0:'MODE0_OPTIONAL_B240',1:'MODE1_GATED_B240',
             2:'MODE2_BBB0',3:'MODE3_CD70'}.get(eff,'DEFAULT'),eff)
def fixture():
    if CASE.exists(): raise FileExistsError('unique fixture exists; refuse overwrite')
    items=[]
    for mode in (-1,0,1,2,3,4):
      for flag in (0,1):
       for rem in (0,1):
        a=('EARLY_TICK_RET' if rem else ('CALL_44AE70' if mode==0 else
           'CALL_44CD70' if 1<=mode<=3 else 'SKIP_CALLS'))
        if flag==0 and rem: b,eff='EARLY_RET',mode
        else:
         eff=2 if mode==1 and flag else mode
         b={0:'MODE0_OPTIONAL_B240',1:'MODE1_GATED_B240',
            2:'MODE2_BBB0',3:'MODE3_CD70'}.get(eff,'DEFAULT')
        for scheduler in ('A','B'):
         items.append({'id':f'C{len(items)+1:03}', 'kind':'synthetic',
          'scheduler':scheduler,'mode':mode,'flag':flag,'nonzero_remainder':rem,
          'expected_route':a if scheduler=='A' else b,
          'expected_effective_mode':mode if scheduler=='A' else eff})
    for claim in NEG:
     items.append({'id':f'N{len(items)+1:03}','kind':'negative',
                   'claim':claim,'must_reject':True})
    assert len(items)==56
    CASE.write_text(json.dumps({'research_id':RID,'classification':'SYNTHETIC_NOT_GAMEPLAY',
      'case_count':len(items),'cases':items},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def native(raw):
    peoff=struct.unpack_from('<I',raw,0x3c)[0]
    assert raw[peoff:peoff+4]==b'PE\x00\x00'
    coff=peoff+4; n=struct.unpack_from('<H',raw,coff+2)[0]
    opt=coff+20; sz=struct.unpack_from('<H',raw,coff+16)[0]
    base=struct.unpack_from('<I',raw,opt+28)[0]
    def at(va,length):
      rva=va-base
      for i in range(n):
       off=opt+sz+i*40
       _,addr,rsz,rptr=struct.unpack_from('<IIII',raw,off+8)
       if addr<=rva and rva+length<=addr+rsz:
        return raw[rptr+rva-addr:rptr+rva-addr+length]
      raise AssertionError('VA not mapped: '+hex(va))
    windows=[(0x449850,146,'A8C820929F2B0E76FD77F12B82E94246A60ACFFC42EA8D535E5CB2101C0210D2'),
     (0x44A048,256,'2BDA5D54EFBAAFA5084F3C2D8785A1C83DEECFF37A74E3853D4A32CEFF4E891A'),
     (0x44A188,16,'C03FC54A969A33497B689A11B4B23AF78BAD4FBBAD4E45AE746DB3BA1B920CEA')]
    for va,length,digest in windows: assert sha(at(va,length))==digest,hex(va)
    table=struct.unpack('<4I',at(0x44A188,16))
    assert table==(0x44A097,0x44A0CE,0x44A0F8,0x44A11C),table
    return {'pe_sha_windows':3,'jump_table_entries':4}
def main():
    if '--init' in sys.argv: fixture()
    assert sha(BS.read_bytes())==B_SHA,'B primary document changed'
    raw=PE.read_bytes(); assert sha(raw)==PE_SHA,'original research PE changed'
    n=native(raw)
    doc=json.loads(CASE.read_text(encoding='utf-8'))
    rows=doc['cases']
    assert doc['research_id']==RID and doc['case_count']==len(rows)==56
    assert len({x['id'] for x in rows})==56
    counts={'A':0,'B':0,'negative':0}
    for row in rows:
     if row['kind']=='negative':
      assert row['claim'] in NEG and row['must_reject'] is True
      counts['negative']+=1; continue
     mode,flag,rem=row['mode'],row['flag'],row['nonzero_remainder']
     if row['scheduler']=='A':
      assert (route_a(mode,rem),mode)==(row['expected_route'],row['expected_effective_mode'])
      counts['A']+=1
     else:
      assert route_b(mode,flag,rem)==(row['expected_route'],row['expected_effective_mode'])
      counts['B']+=1
    assert counts=={'A':24,'B':24,'negative':8}
    print(json.dumps({'research_id':RID,'status':'PASS_SYNTHETIC_STATIC',
      'counts':counts,'native':n,'cases_sha256':sha(CASE.read_bytes()),
      'source_sha256':B_SHA,'old_pe_sha256':PE_SHA,
      'gameplay':'NOT_RUN','dynamic_observed':0,'golden_pass':0,
      'strict_match':0,'new_ready':0},ensure_ascii=False))
if __name__=='__main__': main()
