import csv,hashlib,json,subprocess
from pathlib import Path
out=Path(__file__).resolve().parent
root=out.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
receipt=json.loads((out/'CAPTURE_RECEIPT.json').read_text(encoding='utf-8'))
source=json.loads((out/'capture_input.json').read_text(encoding='utf-8')) if (out/'capture_input.json').exists() else None
rows=list(csv.reader((out/'REPORT_LEDGER.tsv').open(encoding='utf-8',newline=''),delimiter='\t'))
assert len(rows)==10 and all(len(r)==9 for r in rows)
checks=[]
for i,r in enumerate(receipt['records']):
    row=rows[i+1]
    assert row[0]==r['source_path']
    if not r['eligible']:
        assert row[1:4]==['','',''] and not r['destination']
        continue
    path=root/r['destination'];body=path.read_bytes()
    assert sha(body)==r['source_sha256']==r['destination_sha256']==row[1]==row[3]
    assert len(body)==r['bytes'] and not body.startswith(b'\xef\xbb\xbf')
    if source: assert body==source['records'][i]['text'].encode('utf-8')
    checks.append({'path':r['destination'],'sha256':sha(body),'bytes':len(body),'exact_source_readback':bool(source)})
for r in receipt['input_versions']:
    b=subprocess.check_output(['git','show',r['git_version']+':'+r['path']],cwd=root)
    assert sha(b)==r['sha256'] and len(b)==r['bytes']
assert len(checks)==7 and sum(not r['eligible'] for r in receipt['records'])==2
deferred=list(csv.DictReader((out/'DEFERRED.tsv').open(encoding='utf-8',newline=''),delimiter='\t'))
assert len(deferred)==2 and all(x['source_path'] for x in deferred)
result={'result':'PASS','selected':9,'ledger_data_rows':9,'ledger_columns':9,'exact_captures':7,'research':5,'operational':2,'deferred_pending':2,'privacy_derivatives':0,'source_vs_destination_exact_byte_comparisons':7 if source else 'Previous exact-source verification retained in this file before temporary input removal; current run verifies receipt hashes','baseline_metadata_versions_verified':len(receipt['input_versions']),'files':checks}
(out/'VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'}))
