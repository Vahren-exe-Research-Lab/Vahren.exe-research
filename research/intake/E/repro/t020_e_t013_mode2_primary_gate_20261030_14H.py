# E-owned, pure synthetic T013/T020 acceptance gate; never runs Vahren.
import hashlib, json, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
RID = 'E-AUDIT-20261030-14H-T020-T013-MODE2-PRIMARY-GATE-01'
FIX = ROOT/'tests'/'T020_E_T013_MODE2_PRIMARY_CASES_20261030_14H.json'
SRC = ROOT/'data'/'T013_MODE2_PRIMARY_UNIT_MODE3_GATE_NATIVE_20261030_14H.md'
PE = ROOT/'rea_lab'/'targets'/'hakushin067_Vahren.exe'
SRC_HASH = '9046C2F241508441F72A6E5C9FB1150AF70FDC112EE68D7119EDD2BDC3946401'
PE_HASH = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
WINDOWS = [(0x44BCE0,272,'AF7CA919852D359769BD6A9231243F48E3FD47A01FB8CAC027450F36712F3FD8'),
           (0x44BDF2,160,'1A3E39624256AB888FF7E2DC474A25C93FED069C501A598F983705D397C4D0C1')]
PATTERNS = [[],[1],[0],[1,0],[0,0],[1,1],[1,0,1],[1,1,0]]
NEG = ['selected_unit_is_always_first','empty_group_selects_non_null',
       'scratch_zero_means_no_unit','scratch_nonzero_means_mode_unchanged',
       'nested_flag_alone_forces_mode3','mode3_change_is_gameplay_observed',
       'group_b8_is_proven_persistent','unit_1867c_has_proven_gameplay_meaning',
       'all_groups_share_same_selected','mode1_aggregates_equal_mode2_selection']
def digest(buf): return hashlib.sha256(buf).hexdigest().upper()
def selected_flag_index(flags):
    return next((i for i,v in enumerate(flags) if v==0), None)
def local_gate(scratch, nested):
    return 'WRITE_3_AT_44BE0A' if scratch==0 and nested!=0 else (
        'BRANCH_44BEC5_UNKNOWN' if scratch!=0 else 'NO_WRITE_AT_44BE0A')
def init_fixture():
    if FIX.exists(): raise FileExistsError('Existing fixture; never overwrite')
    cases=[]
    for flags in PATTERNS:
      for scratch in (0,1):
       for nested in (0,1):
        cases.append({'id':f'S{len(cases)+1:03}', 'type':'synthetic',
          'unit_1867c_values':flags,'scratch68':scratch,'nested_1ef22c':nested,
          'selected_index':selected_flag_index(flags),
          'local_gate':local_gate(scratch,nested)})
    for claim in NEG:
      cases.append({'id':f'N{len(cases)+1:03}', 'type':'negative',
                    'unsupported_claim':claim,'must_reject':True})
    assert len(cases)==42
    FIX.write_text(json.dumps({'research_id':RID,
       'source_type':'B_14H_STATIC_PLUS_E_SYNTHETIC',
       'not_old_gameplay':True,'cases':cases},ensure_ascii=False,indent=2)+'\n',
       encoding='utf-8')
def pe_section_reader(raw):
    peoff=struct.unpack_from('<I',raw,0x3c)[0]
    assert raw[peoff:peoff+4]==b'PE\x00\x00'
    coff=peoff+4
    opt=coff+20
    n=struct.unpack_from('<H',raw,coff+2)[0]
    sz=struct.unpack_from('<H',raw,coff+16)[0]
    base=struct.unpack_from('<I',raw,opt+28)[0]
    def at(va,size):
      rva=va-base
      for i in range(n):
        off=opt+sz+i*40
        virt_size,virt_addr,raw_size,raw_ptr=struct.unpack_from('<IIII',raw,off+8)
        if virt_addr<=rva and rva+size<=virt_addr+raw_size:
          return raw[raw_ptr+(rva-virt_addr):raw_ptr+(rva-virt_addr)+size]
      raise AssertionError('Unmapped native VA '+hex(va))
    return at
def verify_native():
    assert digest(SRC.read_bytes())==SRC_HASH,'B owner primary changed'
    raw=PE.read_bytes()
    assert digest(raw)==PE_HASH,'Research PE identity changed'
    at=pe_section_reader(raw)
    for va,size,expected in WINDOWS:
      assert digest(at(va,size))==expected,'Native window mismatch '+hex(va)
    call=at(0x44A100,5)
    assert call[0]==0xe8, 'caller is not E8'
    target=0x44A105+struct.unpack_from('<i',call,1)[0]
    assert target==0x44BBB0,hex(target)
    return {'native_windows_sha256':2,'direct_call_verified':1,
            'source_sha256':SRC_HASH,'exe_sha256':PE_HASH}
def run():
    if '--init' in sys.argv: init_fixture()
    native=verify_native()
    data=json.loads(FIX.read_text(encoding='utf-8'))
    rows=data['cases']
    assert data['research_id']==RID and len(rows)==42
    assert len({row['id'] for row in rows})==42
    results={'synthetic':0,'negative':0}
    for row in rows:
      if row['type']=='negative':
        assert row['unsupported_claim'] in NEG and row['must_reject'] is True
        results['negative']+=1
      else:
        assert selected_flag_index(row['unit_1867c_values'])==row['selected_index']
        assert local_gate(row['scratch68'],row['nested_1ef22c'])==row['local_gate']
        results['synthetic']+=1
    assert results=={'synthetic':32,'negative':10}
    print(json.dumps({'status':'PASS_SYNTHETIC_STATIC','research_id':RID,
        'checks':42,'counts':results,'source':native,
        'fixture_sha256':digest(FIX.read_bytes()),'original_gameplay':'NOT_RUN',
        'dynamic_observed':0,'actual_golden_pass':0,'strict_match':0,
        'new_ready':0},ensure_ascii=False))
if __name__=='__main__': run()
