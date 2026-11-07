"""Portable reference regression checks using a small independent source fixture."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("reference", Path(__file__).with_name("reference.py"))
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "reference").mkdir()
        (self.root / "symbols.tsv").write_text(
            "0x55BC60\tfunc\tStatusWnd_Layout\t詳細パネルの解雇ボタン\t実機確認\tF§95\n", encoding="utf-8")
        (self.root / "structs.tsv").write_text(
            "StatusWnd\t0x1C6\tu8\tbtnDismiss\t解雇の印\t静的確認\tF§95\n", encoding="utf-8")
        source = self.root / "evidence.md"
        source.write_text("# Evidence\n関数が印を書く。\n", encoding="utf-8")
        relation = {
            "id": "dismiss-write", "subject": "va:0x0055BC60", "predicate": "writes",
            "object": "field:StatusWnd:0x1C6", "summary": "解雇の印を書く",
            "confidence": "静的確認", "target_version": "ver0.67",
            "source": {"path": "evidence.md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                       "start_line": 2, "end_line": 2}}
        self.relation = relation
        self.save_relation()

    def save_relation(self):
        (self.root / "reference/relations.jsonl").write_text(
            json.dumps(self.relation, ensure_ascii=False) + "\n", encoding="utf-8")

    def test_address_names_and_reverse_field_lookup(self):
        data = reference.load(self.root)
        for query in ("0x55BC60", "0055bc60", "Vahren.exe+15BC60", "StatusWnd_Layout", "解雇"):
            self.assertTrue(reference.search(data, query), query)
        matches = reference.search(data, "StatusWnd+0x1C6")
        self.assertTrue(any(row.get("id") == "dismiss-write" for row in matches))

    def test_build_links_both_directions_and_preserves_confidence(self):
        data = reference.load(self.root)
        files = reference.render(self.root, data)
        symbol = files["reference/symbols/0055BC60.md"]
        structure = files["reference/structs/StatusWnd.md"]
        self.assertIn("../structs/StatusWnd.md#field-1c6", symbol)
        self.assertIn("../symbols/0055BC60.md", structure)
        self.assertIn("実機確認", symbol)
        self.assertIn("静的確認", symbol)
        self.assertIn("evidence.md?plain=1#L2-L2", symbol)

    def test_stale_source_and_escape_are_rejected(self):
        (self.root / "evidence.md").write_text("changed", encoding="utf-8")
        with self.assertRaises(ValueError):
            reference.load(self.root)
        self.relation["source"]["path"] = "../outside.md"
        self.save_relation()
        with self.assertRaises(ValueError):
            reference.load(self.root)

    def test_invalid_line_range_is_rejected(self):
        self.relation["source"]["end_line"] = 100
        self.save_relation()
        with self.assertRaises(ValueError):
            reference.load(self.root)

    def test_address_search_is_case_insensitive(self):
        data = reference.load(self.root)
        self.assertTrue(reference.search(data, "0X55bc60"))

    def test_structure_filename_and_link_keep_names_inside_directory(self):
        self.assertEqual(reference.struct_filename("A/B"), "A%2FB.md")
        self.assertIn("A%252FB.md", reference.endpoint_link("struct:A/B", {}))

    def add_recovery_ledger(self):
        directory = self.root / "research/recovered"
        directory.mkdir(parents=True)
        report = directory / "native.md"
        report.write_text("# Native report\nVA0x55BC60 calls 0X5739E4; field +0x1C6.\n", encoding="utf-8")
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        ledger = directory / "RECOVERY_LEDGER.tsv"
        ledger.write_text("destination\tdestination_sha256\nresearch/recovered/native.md\t" + digest + "\n", encoding="utf-8")
        return report, ledger

    def test_recovered_unknown_address_is_searchable_with_line_provenance(self):
        self.add_recovery_ledger()
        data = reference.load(self.root)
        hits = reference.search(data, "0x5739e4")
        self.assertEqual(len(hits), 1)
        mention = hits[0]
        self.assertEqual(mention["kind"], "source_mention")
        self.assertEqual(mention["source"]["start_line"], 2)
        self.assertIn("検証なし", mention["confidence"])
        self.assertFalse(reference.search(data, "va:0x000001C6"))

    def test_existing_symbol_links_mention_without_promoting_confidence(self):
        self.add_recovery_ledger()
        data = reference.load(self.root)
        page = reference.render(self.root, data)["reference/symbols/0055BC60.md"]
        self.assertIn("研究文書での言及", page)
        self.assertIn("native.md?plain=1#L2-L2", page)
        self.assertIn("辞書の確度　実機確認", page)
        self.assertIn("意味・動作の検証なし", page)

    def test_obsolete_hypothesis_keeps_ledger_correction_in_json_and_page(self):
        report, ledger = self.add_recovery_ledger()
        report.write_text("# Historical hypothesis\n0x55BC60 always grants EXP.\n", encoding="utf-8")
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        limitation = "旧仮説は後日の研究で撤回。経験値付与の根拠として使わない。"
        ledger.write_text(
            "destination\tdestination_sha256\tcoverage_state\tprior_coverage\tlimitations\n"
            f"research/recovered/native.md\t{digest}\tRECOVERED_HISTORICAL\tLOCAL_ONLY\t{limitation}\n",
            encoding="utf-8")
        tool = Path(__file__).with_name("reference.py")
        result = subprocess.run(
            [sys.executable, "-B", str(tool), "--root", str(self.root), "search", "0x55BC60", "--json"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        mention = next(row for row in json.loads(result.stdout) if row.get("kind") == "source_mention")
        self.assertEqual(mention["summary"], "0x55BC60 always grants EXP.")
        self.assertEqual(mention["recovery"]["limitations"], limitation)
        self.assertEqual(mention["recovery"]["coverage_state"], "RECOVERED_HISTORICAL")
        self.assertEqual(mention["recovery"]["prior_coverage"], "LOCAL_ONLY")
        plain = subprocess.run(
            [sys.executable, "-B", str(tool), "--root", str(self.root), "search", "0x55BC60"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertIn(limitation, plain.stdout)
        page = reference.render(self.root, reference.load(self.root))["reference/symbols/0055BC60.md"]
        self.assertIn(limitation, page)
        self.assertIn("RECOVERY_LEDGER.tsv?plain=1#L2-L2", page)
        self.assertIn("always grants EXP", page)

    def add_citation_registry(self):
        source = self.root / "findings.md"
        source.write_text('<a id="f-95"></a>\n## 95. Panel\nHistorical research\n', encoding="utf-8")
        registry = {"F": {"path": "findings.md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                          "sections": {"95": "f-95"}, "limitations": "Partially redacted historical research"}}
        (self.root / "reference/sources.json").write_text(json.dumps(registry), encoding="utf-8")
        return source, registry

    def test_citations_resolve_for_symbols_fields_and_subsections(self):
        self.add_citation_registry()
        symbol_path = self.root / "symbols.tsv"
        symbol_path.write_text(symbol_path.read_text(encoding="utf-8").replace("F§95", "F§95.2, F§999, X§1"), encoding="utf-8")
        data = reference.load(self.root)
        symbol = reference.search(data, "0x55BC60")[0]
        self.assertEqual(symbol["source_links"][0]["label"], "F§95.2")
        self.assertEqual(symbol["source_links"][0]["anchor"], "f-95")
        self.assertEqual(symbol["unresolved_citations"], ["F§999", "X§1"])
        self.assertIn("Partially redacted", symbol["source_links"][0]["limitations"])
        self.assertEqual(data["fields"][0]["source_links"][0]["label"], "F§95")
        pages = reference.render(self.root, data)
        for path in ("reference/symbols/0055BC60.md", "reference/structs/StatusWnd.md"):
            self.assertIn("[F§95", pages[path])
            self.assertIn("../../findings.md#f-95", pages[path])
            self.assertIn("Partially redacted historical research", pages[path])
        self.assertIn("F§999", pages["reference/symbols/0055BC60.md"])
        self.assertNotIn("#f-999", pages["reference/symbols/0055BC60.md"])

    def test_citation_registry_stale_hash_missing_anchor_and_escape_fail(self):
        source, registry = self.add_citation_registry()
        source.write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Stale"):
            reference.load(self.root)
        registry["F"]["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        path = self.root / "reference/sources.json"
        path.write_text(json.dumps(registry), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "anchor"):
            reference.load(self.root)
        registry["F"]["path"] = "../outside.md"
        path.write_text(json.dumps(registry), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "escapes"):
            reference.load(self.root)

    def test_explicit_parenthesized_citations_keep_label_and_subsection(self):
        _, registry = self.add_citation_registry()
        registry["C"] = registry["F"]
        (self.root / "reference/sources.json").write_text(json.dumps(registry), encoding="utf-8")
        path = self.root / "structs.tsv"
        path.write_text(path.read_text(encoding="utf-8").replace("F§95", "C(§95), C(§95.2), Z(§93)"), encoding="utf-8")
        data = reference.load(self.root)
        field = data["fields"][0]
        self.assertEqual([item["label"] for item in field["source_links"]], ["C(§95)", "C(§95.2)"])
        self.assertEqual([item["anchor"] for item in field["source_links"]], ["f-95", "f-95"])
        self.assertEqual(field["unresolved_citations"], ["Z(§93)"])
        page = reference.render(self.root, data)["reference/structs/StatusWnd.md"]
        self.assertIn("[C(§95.2)](../../findings.md#f-95)", page)

    def test_explicit_recovered_source_paths_link_all_variants_not_basenames(self):
        report, ledger = self.add_recovery_ledger()
        variant = report.with_name("native_variant.md")
        variant.write_text("# Corrected historical variant\n0x55BC60\n", encoding="utf-8")
        ledger.write_text(
            "source_path\tdestination\tdestination_sha256\tlimitations\n"
            f"data/native.md\tresearch/recovered/native.md\t{hashlib.sha256(report.read_bytes()).hexdigest()}\tOriginal report\n"
            f"data/native.md\tresearch/recovered/native_variant.md\t{hashlib.sha256(variant.read_bytes()).hexdigest()}\tLater variant\n",
            encoding="utf-8")
        path = self.root / "symbols.tsv"
        original = path.read_text(encoding="utf-8")
        path.write_text(original.replace("F§95", "data/native.md"), encoding="utf-8")
        data = reference.load(self.root)
        links = data["symbols"][0]["source_links"]
        self.assertEqual(len(links), 2)
        self.assertEqual([row["anchor"] for row in links], ["", ""])
        self.assertEqual(links[1]["limitations"], "Later variant")
        tool = Path(__file__).with_name("reference.py")
        result = subprocess.run(
            [sys.executable, "-B", str(tool), "--root", str(self.root), "search", "0x55BC60", "--json"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["source_links"], links)
        page = reference.render(self.root, data)["reference/symbols/0055BC60.md"]
        self.assertIn("[data/native.md](../../research/recovered/native.md)", page)
        self.assertIn("[data/native.md](../../research/recovered/native_variant.md)", page)
        self.assertNotIn("native.md#", page)
        path.write_text(original.replace("F§95", "native.md, other/data/native.md, data/native.md.bak"), encoding="utf-8")
        self.assertEqual(reference.load(self.root)["symbols"][0]["source_links"], [])
        report.write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Stale"):
            reference.load(self.root)
        report.unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            reference.load(self.root)

    def add_field_report(self):
        report, ledger = self.add_recovery_ledger()
        report.write_text(
            "# Report-local memory\nUnit+0x18654 stores a flag.\n"
            "record + 0x28 differs from candidate+0xA14; record+0x28 repeated.\n"
            "eax+0x20, ESP + 0x24, 0x28, 0x55BC60 + 0x28.\n", encoding="utf-8")
        ledger.write_text(
            "destination\tdestination_sha256\tlimitations\nresearch/recovered/native.md\t"
            + hashlib.sha256(report.read_bytes()).hexdigest() + "\tHistorical local owner labels\n", encoding="utf-8")
        return report

    def test_report_local_field_lookup_works_without_registered_type(self):
        self.add_field_report()
        data = reference.load(self.root)
        unit = reference.search(data, "Unit + 0x18654")
        self.assertEqual(len(unit), 1)
        self.assertEqual(unit[0]["kind"], "field_mention")
        self.assertEqual(unit[0]["owner_text"], "Unit")
        self.assertEqual(unit[0]["offset"], "0x18654")
        self.assertIn("Historical", unit[0]["recovery"]["limitations"])
        self.assertEqual(unit[0]["source"]["start_line"], 2)
        self.assertEqual(len(reference.search(data, "record+0x28")), 1)
        self.assertEqual(reference.search(data, "record+0xA14"), [])
        self.assertEqual(reference.search(data, "candidate+0x28"), [])
        self.assertEqual(len(reference.search(data, "candidate+0xa14")), 1)
        self.assertFalse(reference.search(data, "eax+0x20"))
        self.assertFalse(reference.search(data, "esp+0x24"))
        self.assertEqual(len(data["field_mentions"]), 3)

    def test_field_index_links_context_is_stable_and_honors_aliases(self):
        report = self.add_field_report()
        self.add_layout_alias(["TempStatusWnd"])
        data = reference.load(self.root)
        self.assertTrue(reference.search(data, "TempStatusWnd+0x1C6"))
        pages = reference.render(self.root, data)
        index = pages["reference/FIELD_MENTIONS.md"]
        self.assertIn("Unit + 0x18654", index)
        field_pages = "\n".join(value for key, value in pages.items() if key.startswith("reference/fields/"))
        self.assertIn("native.md?plain=1#L2-L2", field_pages)
        self.assertIn("Historical local owner labels", field_pages)
        self.assertIn("FIELD_MENTIONS.md", pages["reference/README.md"])
        self.assertEqual(pages, reference.render(self.root, reference.load(self.root)))
        report.write_text("changed", encoding="utf-8")
        with self.assertRaises(ValueError):
            reference.load(self.root)

    def add_run_results(self):
        directory = self.root / "research/recovered"
        directory.mkdir(parents=True)
        ledger_rows = []
        for run_id, status in (("first-run", "VERIFY"), ("second-run", "VERIFIED")):
            relative = f"research/recovered/runs/{run_id}/RUN_RESULT.json"
            path = self.root / relative
            path.parent.mkdir(parents=True)
            run = {"runId": run_id, "records": [{
                "address": "0x55BC60", "related_task": "T012", "title": "攻撃値の調査",
                "status": status, "methods": {"procedure_info": {"ok": status == "VERIFIED", "evidence_id": "ev_info"}}},
                {"address": "0x550D80", "related_task": "T012", "title": "未知関数の調査",
                 "status": status, "methods": {}}]}
            path.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            ledger_rows.append(f"{relative}\t{digest}\tHistorical acquisition only\n")
        ledger = directory / "RECOVERY_LEDGER.tsv"
        ledger.write_text("destination\tdestination_sha256\tlimitations\n" + "".join(ledger_rows), encoding="utf-8")
        return ledger

    def test_run_title_and_unknown_va_search_preserve_both_attempts(self):
        self.add_run_results()
        data = reference.load(self.root)
        hits = reference.search(data, "攻撃値")
        self.assertEqual(len(hits), 2)
        self.assertEqual([row["reported_status"] for row in hits], ["VERIFY", "VERIFIED"])
        self.assertEqual([row["run_id"] for row in hits], ["first-run", "second-run"])
        self.assertTrue(all(row["kind"] == "research_run_record" for row in hits))
        self.assertEqual(hits[1]["methods"]["procedure_info"]["evidence_id"], "ev_info")
        self.assertNotEqual(hits[1]["confidence"], "実機確認")
        self.assertEqual(len(reference.search(data, "0x550D80")), 2)
        self.assertFalse(any(row["kind"] == "source_mention" for row in data["mentions"]))
        page = reference.render(self.root, data)["reference/symbols/0055BC60.md"]
        self.assertIn("first-run", page)
        self.assertIn("VERIFIED", page)
        self.assertIn("ev_info", page)
        self.assertIn("procedure_info", page)
        self.assertIn("<details>", page)
        source = hits[0]["source"]
        lines = (self.root / source["path"]).read_text(encoding="utf-8").splitlines()
        self.assertIn('"address": "0x55BC60"', lines[source["start_line"] - 1])

    def test_run_records_must_have_methods_and_literal_address_location(self):
        ledger = self.add_run_results()
        report = self.root / "research/recovered/runs/first-run/RUN_RESULT.json"
        payload = json.loads(report.read_text(encoding="utf-8"))
        del payload["records"][0]["methods"]
        report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        ledger.write_text("destination\tdestination_sha256\nresearch/recovered/runs/first-run/RUN_RESULT.json\t" + digest + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "run record"):
            reference.load(self.root)
        payload["records"][0]["methods"] = {}
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).replace('"address"', '"\\u0061ddress"')
        with self.assertRaisesRegex(ValueError, "address line"):
            reference.run_records(encoded, "RUN_RESULT.json", "fixture", {})

    def test_recovered_ledger_rejects_stale_missing_and_escaping_sources(self):
        report, ledger = self.add_recovery_ledger()
        report.write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Stale"):
            reference.load(self.root)

        report.unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            reference.load(self.root)
        ledger.write_text("destination\tdestination_sha256\n../escape.md\t00\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "escapes"):
            reference.load(self.root)

    def test_large_field_groups_are_paginated_without_losing_context(self):
        self.add_field_report()
        data = reference.load(self.root)
        sample = data["field_mentions"][0]
        data["field_mentions"] = [dict(sample, id=f"field-{i}", owner_text="Unit", offset="0x28",
                                       summary=f"unique-source-{i}") for i in range(205)]
        pages = reference.render(self.root, data)
        field_pages = {name: text for name, text in pages.items() if name.startswith("reference/fields/")}
        self.assertEqual(len(field_pages), 3)
        self.assertLess(len(pages["reference/FIELD_MENTIONS.md"]), 2000)
        content = "\n".join(field_pages.values())
        for i in range(205):
            self.assertEqual(content.count(f"unique-source-{i}</") + content.count(f"unique-source-{i}\n"), 1)
        self.assertTrue(all(text.count("native.md?plain=1") <= 100 for text in field_pages.values()))

    def test_field_owner_names_cannot_collide_on_windows(self):
        self.add_field_report()
        data = reference.load(self.root)
        row = data["field_mentions"][0]
        data["field_mentions"] = [dict(row, owner_text="Unit"), dict(row, owner_text="unit")]
        pages = reference.render(self.root, data)
        paths = [name for name in pages if name.startswith("reference/fields/")]
        self.assertEqual(len(paths), 2)
        self.assertEqual(len({name.casefold() for name in paths}), 2)

    def add_layout_alias(self, aliases):
        with (self.root / "symbols.tsv").open("a", encoding="utf-8") as stream:
            stream.write("0x8BCD48\tobject\tg_TempStatusWnd\t一時パネル\t静的確認\tF§95\n")
        layout = dict(self.relation, id="temp-layout", subject="va:0x008BCD48",
                      predicate="uses_layout", object="struct:StatusWnd", aliases=aliases)
        self.write_relations([self.relation, layout])
        return layout

    def write_relations(self, rows):
        (self.root / "reference/relations.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")

    def test_explicit_layout_alias_resolves_field_and_reverse_relations(self):
        self.add_layout_alias(["TempStatusWnd"])
        data = reference.load(self.root)
        for query in ("TempStatusWnd+0x1C6", "tempstatuswnd + 0x1c6"):
            hits = reference.search(data, query)
            self.assertTrue(any(row["id"] == "field:StatusWnd:0x1C6" for row in hits))
            self.assertTrue(any(row["id"] == "dismiss-write" for row in hits))

    def test_alias_requires_explicit_layout_and_rejects_bad_names(self):
        layout = self.add_layout_alias(["TempStatusWnd"])
        for aliases in ([""], ["StatusWnd"], "TempStatusWnd", [9]):
            layout["aliases"] = aliases
            self.write_relations([self.relation, layout])
            with self.assertRaises(ValueError):
                reference.load(self.root)
        layout["aliases"] = ["TempStatusWnd"]
        layout["predicate"] = "calls"
        self.write_relations([self.relation, layout])
        with self.assertRaises(ValueError):
            reference.load(self.root)

    def test_alias_cannot_point_to_two_layouts(self):
        layout = self.add_layout_alias(["TempStatusWnd"])
        with (self.root / "structs.tsv").open("a", encoding="utf-8") as stream:
            stream.write("OtherWnd\t0x10\tu8\tflag\t印\t静的確認\tF§95\n")
        conflicting = dict(layout, id="other-layout", object="struct:OtherWnd")
        self.write_relations([self.relation, layout, conflicting])
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            reference.load(self.root)

    def test_duplicate_dictionary_identity_is_rejected(self):
        for filename in ("symbols.tsv", "structs.tsv"):
            path = self.root / filename
            original = path.read_text(encoding="utf-8")
            path.write_text(original + original, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate dictionary ID"):
                reference.load(self.root)
            path.write_text(original, encoding="utf-8")

    def test_check_detects_obsolete_generated_pages_without_deleting(self):
        tool = Path(__file__).with_name("reference.py")
        command = [sys.executable, "-B", str(tool), "--root", str(self.root)]
        built = subprocess.run(command + ["build"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(built.returncode, 0, built.stderr)
        directory = self.root / "reference/symbols"
        custom = directory / "notes.md"
        custom.write_text("User notes\n", encoding="utf-8")
        checked = subprocess.run(command + ["check"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(checked.returncode, 0, checked.stderr)
        obsolete = directory / "00000001.md"
        obsolete.write_text("<!-- Generated by tools/reference.py. -->\nold", encoding="utf-8")
        checked = subprocess.run(command + ["check"], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(checked.returncode, 0)
        self.assertIn("00000001.md", checked.stderr)
        self.assertTrue(obsolete.exists())
        self.assertEqual(custom.read_text(encoding="utf-8"), "User notes\n")


if __name__ == "__main__":
    unittest.main()
