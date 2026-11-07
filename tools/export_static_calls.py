#!/usr/bin/env python3
"""Export historical V9 call metadata for explicitly reviewed symbol endpoints.

No native payload, opcode bytes, pseudocode, or original executable is read.
The historical source flag is an index assertion, not new verification.
"""
import argparse
from contextlib import contextmanager
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3

COLUMNS=('caller_va','callee_va','site_va','source_record_id','source_db_sha256','source_state')
SOURCE_STATE='V9_STATIC_INDEX'
SOURCE_DB_SHA256='2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE'
SOURCE_PE_SHA256='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
EXCLUDED_RANGES=((0x5710C0,0x571500),(0x58021E,0x580340),(0x5769B0,0x5769B0))
MARKER=re.compile(r'(?i)(?<![a-z])(HOLD|BLOCKED|REFUSED|forbidden)(?![a-z])|拒否')
ALLOWED_READS={
    'function_range':{'function_entry_va','start_va','end_va'},
    'native_callsite':{'ghidra_ref_id','site_va','target_va','caller_function_va','opcode_kind','instruction_length','independently_verified_target'},
}

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest().upper()

def number(value):
    if isinstance(value,int):
        return value if 0 <= value <= 0xFFFFFFFF else None
    text=str(value or '').strip()
    return int(text,16) if re.fullmatch(r'(?i)(?:0x)?[0-9a-f]{6,8}',text) else None

def va(value):
    return f'0x{value:08X}'

def marked(values):
    return any(MARKER.search(str(value or '')) for value in values)

def in_ranges(value,ranges):
    return any(start <= value <= end for start,end in ranges)

@contextmanager
def readonly(path):
    path=Path(path)
    if not path.is_file():
        raise FileNotFoundError(path.name)
    c=sqlite3.connect(path.resolve().as_uri()+'?mode=ro&immutable=1',uri=True)
    try:
        c.execute('PRAGMA query_only=ON')
        yield c
    finally:
        c.close()

def reviewed_endpoints(path):
    text=Path(path).read_text(encoding='utf-8-sig')
    result=set()
    for row in csv.reader(text.splitlines(),delimiter='\t'):
        if len(row)<6 or row[0].startswith('#') or marked(row[5:]):
            continue
        address=number(row[0])
        if address is not None and row[1]=='func' and row[4] in ('静的確認','実機確認'):
            result.add(address)
    return result

def metadata_authorizer(action,table,column,db,trigger):
    if action==sqlite3.SQLITE_READ:
        return sqlite3.SQLITE_OK if column in ALLOWED_READS.get(table,set()) else sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK if action==sqlite3.SQLITE_SELECT else sqlite3.SQLITE_DENY

def collect(db,symbols,expected_sha=SOURCE_DB_SHA256):
    db=Path(db);symbols=Path(symbols)
    source_sha=sha256(db)
    if source_sha != expected_sha.upper():
        raise ValueError('Source DB SHA256 mismatch')
    dictionary_sha=sha256(symbols)
    endpoints=reviewed_endpoints(symbols)
    before=len(endpoints)
    denied_owners=set()
    ranges=[]
    rows=[]
    with readonly(db) as c:
        c.set_authorizer(metadata_authorizer)
        for owner_text,start_text,end_text in c.execute(
                'SELECT function_entry_va,start_va,end_va FROM function_range'):
            owner,start,end=map(number,(owner_text,start_text,end_text))
            if owner is None:
                raise ValueError('Invalid function range owner metadata')
            if start is None or end is None or end<start:
                raise ValueError('Invalid function range boundary metadata')
            ranges.append((owner,start,end))
            if marked((owner_text,start_text,end_text)) or in_ranges(owner,EXCLUDED_RANGES) or any(
                    start <= hi and end >= lo for lo,hi in EXCLUDED_RANGES):
                denied_owners.add(owner)
        denied_ranges=list(EXCLUDED_RANGES)+[(start,end) for owner,start,end in ranges if owner in denied_owners]
        endpoints={x for x in endpoints if x not in denied_owners and not in_ranges(x,denied_ranges)}
        scanned=0
        for record,site_text,target_text,caller_text,kind,length,verified in c.execute(
                'SELECT ghidra_ref_id,site_va,target_va,caller_function_va,opcode_kind,instruction_length,independently_verified_target FROM native_callsite'):
            scanned+=1
            if marked((record,site_text,target_text,caller_text,kind)):
                continue
            site,target,caller=map(number,(site_text,target_text,caller_text))
            if kind!='E8_DIRECT_CALL' or verified!=1 or length!=5:
                continue
            if None in (site,target,caller) or caller not in endpoints or target not in endpoints:
                continue
            if any(in_ranges(x,denied_ranges) for x in (site,target,caller)):
                continue
            if not isinstance(record,int) or record<0:
                continue
            rows.append(dict(zip(COLUMNS,(va(caller),va(target),va(site),str(record),source_sha,SOURCE_STATE))))
    if sha256(db)!=source_sha or sha256(symbols)!=dictionary_sha:
        raise ValueError('Source changed during export')
    rows.sort(key=lambda r:(r['caller_va'],r['callee_va'],r['site_va'],int(r['source_record_id'])))
    meta={
        'format_version':1,'source_state':SOURCE_STATE,
        'source_db_sha256':source_sha,'source_pe_sha256':SOURCE_PE_SHA256,'symbols_sha256':dictionary_sha,
        'selection':{
            'endpoint_kind':'func','endpoint_confidences':['静的確認','実機確認'],
            'eligible_endpoint_vas':[va(x) for x in sorted(endpoints)],
            'opcode_kind':'E8_DIRECT_CALL','instruction_length':5,'independently_verified_target':1,
            'source_flag_meaning':'Historical V9 source assertion only; no new confidence or execution verification.',
            'endpoint_rule':'Both endpoints must be in the explicitly reviewed dictionary set.',
            'denied_markers':['HOLD','BLOCKED','REFUSED','拒否','forbidden'],
            'denied_owner_rule':'Any overlapping range denies its owner and every range belonging to that owner.',
            'metadata_columns':{table:sorted(columns) for table,columns in ALLOWED_READS.items()},
        },
        'excluded_ranges':[{'start_va':va(a),'end_va':va(b),'inclusive':True} for a,b in EXCLUDED_RANGES],
        'counts':{'reviewed_endpoints_before_exclusions':before,'eligible_endpoints':len(endpoints),
                  'denied_range_owners':len(denied_owners),'source_callsite_records_scanned':scanned,'exported_calls':len(rows)},
        'limitations':['Static historical index only; no runtime observations.',
                       'Unnamed, unreviewed, indirect, tail-jump, and excluded endpoints are omitted.'],
    }
    return rows,meta

def export(db,symbols,output,receipt,expected_sha=SOURCE_DB_SHA256):
    paths=[Path(p).resolve() for p in (db,symbols,output,receipt)]
    if len(set(paths))!=len(paths) or any(
            a.exists() and b.exists() and a.samefile(b)
            for i,a in enumerate(paths) for b in paths[i+1:]):
        raise ValueError('Inputs and outputs must use distinct files')
    rows,meta=collect(db,symbols,expected_sha)
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=COLUMNS,delimiter='\t',lineterminator='\n')
    writer.writeheader();writer.writerows(rows)
    payload=stream.getvalue().encode('utf-8')
    meta['static_calls_sha256']=hashlib.sha256(payload).hexdigest().upper()
    Path(output).write_bytes(payload)
    Path(receipt).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return meta

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-db',type=Path,required=True)
    p.add_argument('--symbols',type=Path,default=Path(__file__).resolve().parents[1]/'symbols.tsv')
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'reference/static_calls.tsv')
    p.add_argument('--receipt',type=Path,default=Path(__file__).resolve().parents[1]/'reference/static_calls_source.json')
    args=p.parse_args()
    meta=export(args.source_db,args.symbols,args.output,args.receipt)
    print(json.dumps(meta['counts'],ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()

