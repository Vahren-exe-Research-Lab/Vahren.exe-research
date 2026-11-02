# E-owned static provenance and synthetic acceptance; no original gameplay execution.
import hashlib, json, struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
CASES=ROOT/'tests'/'T020_E_T028_THIRD_SELECTOR_EAX_CASES_20261030_10H.json'
DETAIL=ROOT/'data'/'T028_THIRD_SELECTOR_CALLER_RETURN_GATE_NATIVE_20261030_10H.md'
PE=ROOT/'rea_lab'/'targets'/'hakushin067_Vahren.exe'
RID='E-AUDIT-20261030-10H-T020-T028-THIRD-SELECTOR-OPAQUE-EAX-01'
B_SHA='B2273C621C9B4E1E5A7AFFF4061C85F3809246EDFBADD9EAD8ABF57960E45268'
PE_SHA='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
def sha(d): return hashlib.sha256(d).hexdigest().upper()
def model_producer(upstream,cache,constructed):
    if upstream: return 'upstream',upstream
    if cache: return 'cache',cache
    if constructed: return 'constructed',constructed
    return 'null',0
def model_flag(selector_return,flags):
    if selector_return==0: return 'zero_due_to_null_selector'
    if any(v != 0 for v in flags): return 'zero_due_to_unit_flag'
    return 'retain_value_unproven'
ANTI={
 'ghidra_void_proves_eax_unused','producer_eax_always_original_unit',
 'third_argument_may_be_1_at_0x447c2f','null_producer_skips_selector_call',
 'nonnull_selector_guarantees_local_flag_1','unit_1ad_nonzero_proves_unit_death',
 'cache_hit_proves_constructed_object','synthetic_pass_proves_golden'}
def native_audit(raw):
    pe=struct.unpack_from('<I',raw,0x3C)[0]
    assert raw[pe:pe+4]==bytes((80,69,0,0))
    coff=pe+4; num=struct.unpack_from('<H',raw,coff+2)[0]
    opt=coff+20; size=struct.unpack_from('<H',raw,coff+16)[0]
    img=struct.unpack_from('<I',raw,opt+28)[0]
    def at(va,n):
        rva=va-img
        for i in range(num):
            off=opt+size+40*i
            vsize,addr,rsize,rptr=struct.unpack_from('<IIII',raw,off+8)
            if addr <= rva and rva+n <= addr+rsize:
                pos=rptr+(rva-addr);return raw[pos:pos+n]
        raise AssertionError(f'PE unmapped VA {va:X}')
    windows={0x447BF0:(134,'B391F245139097AAE360B4BD4CD8ECEF2BCDF9205C64EB21968291395074BD09'),
             0x597BA0:(234,'C5FDFE7EC82F8511005516AAA84A0209C09C200A13E5C80DB329BD98B8F04F27')}
    for va,(length,expected) in windows.items(): assert sha(at(va,length))==expected
    target={0x447C23:0x597BA0,0x447C2F:0x5AC1A0,0x5682B5:0x597BA0,
            0x5682C3:0x5AC1A0,0x597BDF:0x49E490,0x597C6B:0x5A8110}
    for va,tgt in target.items():
        blob=at(va,5);assert blob[0]==0xE8,(hex(va),blob.hex())
        rel=struct.unpack('<i',blob[1:])[0]
        assert (va+5+rel)&0xFFFFFFFF==tgt,(hex(va),hex((va+5+rel)&0xFFFFFFFF),hex(tgt))
    return {'pe_base':hex(img),'pe_windows':len(windows),'e8_calls':len(target)}
def main():
    assert sha(DETAIL.read_bytes())==B_SHA,'B source changed; VERIFY rather than silently accept'
    raw=PE.read_bytes();assert sha(raw)==PE_SHA,'wrong PE epoch'
    native=native_audit(raw)
    doc=json.loads(CASES.read_text(encoding='utf-8'))
    assert doc['research_id']==RID and len(doc['cases'])==doc['case_count']==56
    assert len({c['id'] for c in doc['cases']})==56
    passes={'model':0,'anti_overclaim':0}
    for c in doc['cases']:
        if c['kind']=='model':
            assert c['caller_reached'] is True
            assert all(type(c[k]) is int and c[k]>=0 for k in ('upstream','cache','constructed','selector_return'))
            assert isinstance(c['scan_1ad'],list) and all(v in (0,1) for v in c['scan_1ad'])
            assert model_producer(c['upstream'],c['cache'],c['constructed'])==(c['expected_source'],c['expected_eax']),c['id']
            assert model_flag(c['selector_return'],c['scan_1ad'])==c['expected_flag_action'],c['id']
        else:
            assert c['kind']=='anti_overclaim' and c['claim'] in ANTI and c['must_reject'] is True
        passes[c['kind']]+=1
    assert passes=={'model':48,'anti_overclaim':8}
    print(json.dumps({'research_id':RID,'result':'PASS_STATIC_SYNTHETIC','cases':passes,
       'native':native,'B_source_sha256':B_SHA,'PE_sha256':PE_SHA,'fixture_sha256':sha(CASES.read_bytes()),
       'target_gameplay':'NOT_RUN','golden_pass':0,'strict_match':0,'ready':False},ensure_ascii=False))
if __name__=='__main__': main()
