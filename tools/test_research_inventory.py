#!/usr/bin/env python3
"""Standalone synthetic fixture tests for read-only research inventory."""
import hashlib
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_research as audit

class ResearchInventoryTests(unittest.TestCase):
    def test_domain_and_master(self):
        self.assertEqual(audit.classify("data/T013_TEST.md","# T013"),("B",["013"],"AI_TARGET"))
        self.assertEqual(audit.classify("MASTER_LEDGER.md","# T018"),("COORD",[],"COORDINATION"))

    def test_exact_duplicate_is_not_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"knowledge/generated").mkdir(parents=True)
            (root/"data").mkdir()
            originals={
                "data/T011_A.md":b"# T011\n",
                "data/T011_B.md":b"# T011\n",
                "data/T013_C.md":b"# T013\n",
            }
            conn=sqlite3.connect(root/"knowledge/generated/research.sqlite")
            conn.execute("CREATE TABLE docs(path TEXT,sha256 TEXT,bytes INT,lines INT,mentions INT)")
            for path,raw in originals.items():
                (root/path).write_bytes(raw)
                conn.execute("INSERT INTO docs VALUES (?,?,?,?,?)",
                    (path,hashlib.sha256(raw).hexdigest(),len(raw),1,0))
            conn.commit()
            conn.close()
            output=root/"review"
            with patch.object(sys,"argv",["inventory","--root",str(root),"--out",str(output)]):
                audit.main()
            lines=(output/"RESEARCH_SOURCE_CATALOG.tsv").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines),4)
            duplicates=(output/"RESEARCH_DUPLICATE_CANDIDATES.tsv").read_text(encoding="utf-8")
            self.assertIn("EXACT_SHA256",duplicates)
            for path,raw in originals.items():
                self.assertEqual((root/path).read_bytes(),raw)
            summary=(output/"RESEARCH_INTEGRATION_SNAPSHOT.md").read_text(encoding="utf-8")
            self.assertIn("Indexed research documents: 3",summary)
            self.assertIn("Shared-primary-ID candidate groups: 0",summary)

    def test_shared_id_more_than_eight_is_reported_without_hidden_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"knowledge/generated").mkdir(parents=True)
            (root/"data").mkdir()
            con=sqlite3.connect(root/"knowledge/generated/research.sqlite")
            con.execute("CREATE TABLE docs(path TEXT,sha256 TEXT,bytes INT,lines INT,mentions INT)")
            research_id="EXP-COLLAB-LARGEGROUP-20261031-01"
            for i in range(11):
                path=f"data/T011_GROUP_{i:02d}.md"
                raw=(f"# T011 evidence {i}\nresearch_id: {research_id}\n").encode("utf-8")
                (root/path).write_bytes(raw)
                con.execute("INSERT INTO docs VALUES (?,?,?,?,?)",
                            (path,hashlib.sha256(raw).hexdigest(),len(raw),2,0))
            con.commit()
            con.close()
            out=root/"review"
            with patch.object(sys,"argv",["audit","--root",str(root),"--out",str(out)]):
                audit.main()
            text=(out/"RESEARCH_DUPLICATE_CANDIDATES.tsv").read_text(encoding="utf-8")
            match=[x for x in text.splitlines() if x.startswith("SHARED_ID_REVIEW\t")]
            self.assertEqual(len(match),1)
            self.assertEqual(match[0].split("\t")[2],"11")
            self.assertIn("[OMITTED_3_PATHS]",match[0])
            self.assertIn("Shared-primary-ID candidate groups: 1",
                          (out/"RESEARCH_INTEGRATION_SNAPSHOT.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
