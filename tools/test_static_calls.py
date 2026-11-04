"""Synthetic metadata-only static call exporter tests."""
import csv
import hashlib
from pathlib import Path
import sqlite3
import tempfile
import unittest
import export_static_calls as ex

class StaticCallsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.db=self.root/'source.sqlite'
        self.symbols=self.root/'symbols.tsv'
        self.symbols.write_text('# va\tkind\tname\tsummary\tconfidence\tsource\n'+''.join(
            f'{va}\t{kind}\t{name}\tsummary\t{confidence}\t{source}\n'
            for va,kind,name,confidence,source in [
                ('0x00401000','func','one','静的確認','review'),
                ('0X00402000','func','two','実機確認','review'),
                ('0x00403000','func','denied-owner','静的確認','review'),
                ('0x00404000','func','guess','推定','review'),
                ('0x00405000','global','global','静的確認','review'),
                ('0x00406000','func','hold','静的確認','HoLd: excluded'),
                ('0x005710C0','func','protected','実機確認','review'),
                ('0x0058021E','func','historic-address','実機確認','review'),
                ('0x005769B0','func','historic-point','実機確認','review')]),encoding='utf-8')
        c=sqlite3.connect(self.db)
        # Deliberately omit opcode/body columns: exporter must not need them.
        c.execute('CREATE TABLE native_callsite(ghidra_ref_id INTEGER,site_va TEXT,target_va TEXT,caller_function_va TEXT,opcode_kind TEXT,instruction_length INTEGER,independently_verified_target INTEGER)')
        c.execute('CREATE TABLE function_range(function_entry_va TEXT,start_va TEXT,end_va TEXT)')
        c.executemany('INSERT INTO function_range VALUES(?,?,?)',[
            ('00401000','00401000','004010FF'),('00402000','00402000','004020FF'),
            ('00403000','00403000','004030FF'),('0X00403000','005710c0','005710c1'),
            ('00403000','00600000','006000FF')])
        rows=[(1,'0X00401010','00402000','00401000','E8_DIRECT_CALL',5,1)]
        for i,target in enumerate(['00403000','00404000','00405000','00406000','005710C0','0058021E','005769B0','00999999'],2):
            rows.append((i,'00401020',target,'00401000','E8_DIRECT_CALL',5,1))
        rows += [(20,'00600010','00402000','00401000','E8_DIRECT_CALL',5,1),
                 (21,'00401020','00402000','00401000','E9_TAIL_JMP',5,1),
                 (22,'00401020','00402000','00401000','E8_DIRECT_CALL',5,0),
                 (23,'00580340','00402000','00401000','E8_DIRECT_CALL',5,1),
                 (24,'00403010','00402000','00403000','E8_DIRECT_CALL',5,1),
                 (25,'00401040','00402000','00401000','REFUSED',5,1)]
        c.executemany('INSERT INTO native_callsite VALUES(?,?,?,?,?,?,?)',rows)
        c.commit();c.close()
        self.sha=hashlib.sha256(self.db.read_bytes()).hexdigest().upper()

    def test_metadata_selection_and_excluded_owner_all_ranges(self):
        rows,meta=ex.collect(self.db,self.symbols,self.sha)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['caller_va'],'0x00401000')
        self.assertEqual(rows[0]['callee_va'],'0x00402000')
        self.assertEqual(rows[0]['site_va'],'0x00401010')
        self.assertEqual(rows[0]['source_record_id'],'1')
        self.assertEqual(meta['counts']['reviewed_endpoints_before_exclusions'],6)
        self.assertEqual(meta['counts']['eligible_endpoints'],2)
        self.assertEqual(meta['selection']['eligible_endpoint_vas'],['0x00401000','0x00402000'])
        self.assertEqual(len(meta['selection']['eligible_endpoint_vas']),meta['counts']['eligible_endpoints'])
        self.assertEqual(meta['counts']['denied_range_owners'],1)
        self.assertEqual(meta['source_db_sha256'],self.sha)
        self.assertNotIn(str(self.root),str(meta))

    def test_readonly_connection(self):
        before=self.db.read_bytes()
        with ex.readonly(self.db) as c:
            self.assertEqual(c.execute('PRAGMA query_only').fetchone()[0],1)
            with self.assertRaises(sqlite3.OperationalError):
                c.execute('CREATE TABLE forbidden(x)')
        self.assertEqual(before,self.db.read_bytes())

    def test_hash_mismatch_fails_before_sqlite(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):
            ex.collect(self.db,self.symbols,'0'*64)

    def test_hash_and_source_unchanged(self):
        before=self.db.read_bytes()
        ex.collect(self.db,self.symbols,self.sha)
        self.assertEqual(before,self.db.read_bytes())

    def test_payload_reads_denied(self):
        c=sqlite3.connect(self.db)
        c.execute('ALTER TABLE native_callsite ADD COLUMN native_opcode_hex TEXT')
        c.execute('ALTER TABLE function_range ADD COLUMN body_bytes INTEGER')
        c.commit();c.close()
        with ex.readonly(self.db) as c:
            c.set_authorizer(ex.metadata_authorizer)
            for query in ('SELECT native_opcode_hex FROM native_callsite','SELECT body_bytes FROM function_range'):
                with self.assertRaises(sqlite3.DatabaseError):
                    c.execute(query)

    def test_source_markers_and_semantic_summary(self):
        original=self.symbols.read_text(encoding='utf-8')
        for marker in ('hold','BLOCKED','Refused','拒否','forbidden'):
            self.symbols.write_text(original.replace('summary\t静的確認\treview','summary\t静的確認\t'+marker,1),encoding='utf-8')
            rows,_=ex.collect(self.db,self.symbols,self.sha)
            self.assertEqual(rows,[],marker)
        self.symbols.write_text(original.replace('summary','拒否を処理する',1),encoding='utf-8')
        rows,_=ex.collect(self.db,self.symbols,self.sha)
        self.assertEqual(len(rows),1)

    def test_historical_owner_all_ranges_and_inclusive_end(self):
        c=sqlite3.connect(self.db)
        c.executemany('INSERT INTO function_range VALUES(?,?,?)',[
            ('0x00401000','0X00580340','0X00580341'),
            ('00401000','00610000','00610010')])
        c.commit();c.close()
        self.sha=ex.sha256(self.db)
        rows,meta=ex.collect(self.db,self.symbols,self.sha)
        self.assertEqual(rows,[])
        self.assertEqual(meta['counts']['denied_range_owners'],2)

    def test_export_reproducible_receipt(self):
        output=self.root/'calls.tsv'; receipt=self.root/'receipt.json'
        meta=ex.export(self.db,self.symbols,output,receipt,self.sha)
        self.assertEqual(meta['static_calls_sha256'],ex.sha256(output))
        first=(output.read_bytes(),receipt.read_bytes())
        ex.export(self.db,self.symbols,output,receipt,self.sha)
        self.assertEqual(first,(output.read_bytes(),receipt.read_bytes()))
        self.assertEqual(output.read_text().splitlines()[0].split('\t'),list(ex.COLUMNS))

    def test_export_cannot_overwrite_inputs(self):
        for output,receipt in ((self.db,self.root/'r.json'),(self.root/'c.tsv',self.symbols),
                               (self.root/'same',self.root/'same')):
            with self.assertRaisesRegex(ValueError,'distinct'):
                ex.export(self.db,self.symbols,output,receipt,self.sha)

if __name__=='__main__':
    unittest.main()

