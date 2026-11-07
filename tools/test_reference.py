"""Portable reference regression checks using a small independent source fixture."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

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

    def write_corrections(self, rows):
        (self.root / "reference/corrections.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")

    def correction(self, **changes):
        return dict({"id": "dismiss-history", "subject": "va:0x0055BC60", "status": "corrected",
                     "previous_interpretation": "obsolete redraw routine",
                     "current_interpretation": "current dismiss button layout",
                     "summary": "Historical label corrected", "confidence": "文書照合",
                     "target_version": "ver0.67", "source": dict(self.relation["source"])}, **changes)

    def test_corrections_search_old_current_wording_and_endpoint_without_live_claims(self):
        self.write_corrections([self.correction(kind="func"), self.correction(
            id="field-history", subject="field:StatusWnd:0x1C6")])
        data = reference.load(self.root)
        for query in ("obsolete redraw", "current dismiss", "0x55BC60", "StatusWnd_Layout",
                      "StatusWnd+0x1C6", "field:StatusWnd:0x1C6"):
            with self.subTest(query=query):
                hits = [row for row in reference.search(data, query) if row.get("kind") == "correction"]
                self.assertTrue(hits)
                self.assertTrue(all(row["status"] == "corrected" for row in hits))
        self.assertEqual(len(data["relations"]), 1)
        self.assertFalse(any("obsolete redraw" in json.dumps(row) for row in data["symbols"] + data["fields"] + data["relations"]))
        command = [sys.executable, "-B", str(Path(reference.__file__)), "--root", str(self.root),
                   "search", "obsolete redraw", "--json"]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({row["kind"] for row in json.loads(result.stdout)}, {"correction"})

    def test_corrections_render_history_source_links_and_overview(self):
        self.write_corrections([self.correction(), self.correction(
            id="field-history", subject="field:StatusWnd:0x1C6")])
        pages = reference.render(self.root, reference.load(self.root))
        for name in ("reference/symbols/0055BC60.md", "reference/structs/StatusWnd.md",
                     "reference/CORRECTIONS.md"):
            with self.subTest(page=name):
                self.assertIn(name, pages)
                self.assertIn("訂正履歴", pages[name])
                self.assertIn("訂正済みの旧解釈", pages[name])
                self.assertIn("obsolete redraw routine", pages[name])
                self.assertIn("現在の解釈", pages[name])
                self.assertIn("current dismiss button layout", pages[name])
                self.assertIn("evidence.md?plain=1#L2-L2", pages[name])
                self.assertIn("ver0.67", pages[name])
        self.assertIn("CORRECTIONS.md", pages["reference/README.md"])
        self.assertIn("symbols/0055BC60.md", pages["reference/CORRECTIONS.md"])
        self.assertIn("structs/StatusWnd.md#field-1c6", pages["reference/CORRECTIONS.md"])

    def test_optional_corrections_absence_keeps_search_and_build_available(self):
        data = reference.load(self.root)
        self.assertEqual(data.get("corrections", []), [])
        self.assertTrue(reference.search(data, "0x55BC60"))
        self.assertIn("reference/README.md", reference.render(self.root, data))

    def test_correction_accepts_explicit_ver067_image_base_target(self):
        self.write_corrections([self.correction(
            target_version="迫真戦記 ver0.67 / Vahren.exe image base 0x400000")])
        self.assertEqual(len(reference.search(reference.load(self.root), "obsolete redraw")), 1)

    def test_human_cli_marks_old_interpretation_as_corrected_history(self):
        self.write_corrections([self.correction()])
        result = subprocess.run(
            [sys.executable, "-B", str(Path(reference.__file__)), "--root", str(self.root),
             "search", "obsolete redraw"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("訂正済みの旧解釈", result.stdout)
        self.assertIn("obsolete redraw routine", result.stdout)
        self.assertIn("現在の解釈", result.stdout)
        self.assertIn("current dismiss button layout", result.stdout)

    def test_corrections_reject_invalid_identity_status_and_required_text(self):
        invalid = [{"subject": "va:0x00000001"}, {"subject": "struct:StatusWnd"},
                   {"status": "current"}, {"target_version": "ver0.68"},
                   {"id": "dismiss-write"}, {"id": "va:0x0055BC60"},
                   {"id": "field:StatusWnd:0x1C6"}]
        for key in ("id", "subject", "status", "previous_interpretation", "current_interpretation",
                    "summary", "confidence", "target_version"):
            invalid.extend(({key: "  "}, {key: 1}, {key: None}))
        for changes in invalid:
            with self.subTest(changes=changes):
                self.write_corrections([self.correction(**changes)])
                with self.assertRaises(ValueError):
                    reference.load(self.root)
        self.write_corrections([self.correction(), self.correction()])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            reference.load(self.root)

    def test_corrections_verify_source_checksum_path_and_line_bounds(self):
        cases = [{"sha256": "0" * 64}, {"path": "../outside.md"}, {"path": "missing.md"},
                 {"start_line": 0}, {"start_line": 2, "end_line": 1}, {"end_line": 3},
                 {"start_line": True}, {"end_line": "2"}, {"sha256": None}, {"path": None}]
        for changes in cases:
            with self.subTest(changes=changes):
                self.write_corrections([self.correction(source=dict(self.relation["source"], **changes))])
                with self.assertRaises(ValueError):
                    reference.load(self.root)

    def test_corrections_reject_missing_keys_and_malformed_rows(self):
        for row in ([], "invalid", {"id": "partial"}, self.correction(source=None)):
            with self.subTest(row=row):
                self.write_corrections([row])
                with self.assertRaises(ValueError):
                    reference.load(self.root)
        correction = self.correction()
        del correction["source"]["end_line"]
        self.write_corrections([correction])
        with self.assertRaises(ValueError):
            reference.load(self.root)

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

    def test_local_field_tokens_separate_japanese_prose_from_ascii_owners(self):
        rows = reference.local_field_mentions(
            "AL1ならengine+0x1EEC3C。calleeはowner+0x2EC、bodyとslot+0x90。"
            "処理はUnit+0x90を読む。ScriptEngine + 0x1EED60を初期化。"
            "Ns::Unit+0x28 / owner\u3000+\u30000x2EC", "report.md", "a" * 64, {}, 7)
        self.assertEqual([(row["owner_text"], row["offset"]) for row in rows], [
            ("engine", "0x1EEC3C"), ("owner", "0x2EC"), ("slot", "0x90"),
            ("Unit", "0x90"), ("ScriptEngine", "0x1EED60"), ("Ns::Unit", "0x28")])
        self.assertTrue(all(row["source"] == {
            "path": "report.md", "sha256": "a" * 64, "start_line": 7, "end_line": 7}
            for row in rows))

    def test_local_field_tokens_keep_identifier_and_offset_boundaries(self):
        content = ("Unit状態+0x90 0x005470FF+0x28 eax+0x20 R8D+0x20 "
                   "owner+0x90G owner+0x90_tail ::Unit+0x28 "
                   "fooUnit+0x90 Unit+0x9a unit+0x9A")
        rows = reference.local_field_mentions(content, "report.md", "a" * 64, {}, 1)
        self.assertEqual([(row["owner_text"], row["offset"]) for row in rows], [
            ("fooUnit", "0x90"), ("Unit", "0x9A"), ("unit", "0x9A")])

    def test_japanese_adjacent_field_lookup_preserves_saved_source(self):
        report, ledger = self.add_recovery_ledger()
        payload = "# 日本語の研究\r\n処理はUnit+0x90を読む。AL1ならengine+0x1EEC3C。\r\n".encode("utf-8")
        report.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        ledger.write_text("destination\tdestination_sha256\tlimitations\n"
                          f"research/recovered/native.md\t{digest}\tLocal owner only\n", encoding="utf-8")
        data = reference.load(self.root)
        hits = reference.search(data, "Unit+0x90")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["kind"], "field_mention")
        self.assertEqual(hits[0]["source"], {
            "path": "research/recovered/native.md", "sha256": digest, "start_line": 2, "end_line": 2})
        self.assertEqual([row["owner_text"] for row in data["field_mentions"]], ["Unit", "engine"])
        self.assertEqual(report.read_bytes(), payload)

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

    def add_static_calls(self):
        with (self.root / "symbols.tsv").open("a", encoding="utf-8") as stream:
            stream.write("0x560650\tfunc\tStatusWnd_Down\t押下\t静的確認\tF§95\n")
        payload = ("caller_va\tcallee_va\tsite_va\tsource_record_id\tsource_db_sha256\tsource_state\n"
                   + "".join(f"0x0055BC60\t0x00560650\t{site}\t{i}\t{'a' * 64}\tV9_STATIC_INDEX\n"
                             for i, site in enumerate(("0x0055BD00", "0x0055BD10"), 1)))
        path = self.root / "reference/static_calls.tsv"
        path.write_text(payload, encoding="utf-8", newline="\n")
        receipt = {"format_version": 1, "source_state": "V9_STATIC_INDEX",
                   "source_db_sha256": "a" * 64,
                   "source_pe_sha256": "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187",
                   "static_calls_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                   "selection": {"eligible_endpoint_vas": ["0x0055BC60", "0x00560650"]},
                   "counts": {"eligible_endpoints": 2, "exported_calls": 2}}
        meta = self.root / "reference/static_calls_source.json"
        meta.write_text(json.dumps(receipt), encoding="utf-8")
        return path, meta, receipt

    def test_static_call_index_links_both_directions_without_semantic_promotion(self):
        self.add_static_calls()
        data = reference.load(self.root)
        self.assertEqual(len(reference.call_edges(data, "StatusWnd_Layout", incoming=False)), 2)
        callers = reference.call_edges(data, "0x560650", incoming=True)
        self.assertEqual(len(callers), 2)
        self.assertTrue(all(row["confidence"].startswith("静的索引") for row in callers))
        self.assertEqual(data["symbols"][0]["confidence"], "実機確認")
        self.assertTrue(any(row["kind"] == "static_callsite" for row in reference.search(data, "0x560650")))
        pages = reference.render(self.root, data)
        self.assertIn("00560650.md", pages["reference/symbols/0055BC60.md"])
        self.assertIn("0055BC60.md", pages["reference/symbols/00560650.md"])
        self.assertIn("0x0055BD10", pages["reference/symbols/00560650.md"])

    def test_static_call_index_rejects_tampering_unknown_endpoints_and_exclusions(self):
        path, meta, receipt = self.add_static_calls()
        original = path.read_text(encoding="utf-8")
        path.write_text(original + "changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "checksum"):
            reference.load(self.root)
        for replacement in ("0x005710C0", "0x00580280", "0x005769B0", "0x00400000"):
            path.write_text(original.replace("0x00560650", replacement), encoding="utf-8", newline="\n")
            receipt["static_calls_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            meta.write_text(json.dumps(receipt), encoding="utf-8")
            with self.assertRaises(ValueError):
                reference.load(self.root)

    def test_static_call_index_supports_fresh_clone_cli_and_new_dictionary_entries(self):
        self.add_static_calls()
        with (self.root / "symbols.tsv").open("a", encoding="utf-8") as stream:
            stream.write("0x401000\tfunc\tNewFinding\t新しい発見\t推定\tfixture\n")
        data = reference.load(self.root)
        self.assertEqual(len(reference.call_edges(data, "0x560650", incoming=True)), 2)
        command = [sys.executable, str(Path(reference.__file__)), "--root", str(self.root),
                   "callers", "0x560650", "--json"]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 2)

    def add_prose_report(self):
        directory = self.root / "research/recovered"
        directory.mkdir(parents=True)
        report = directory / "T025_DREAM_GUARD.md"
        report.write_text("preamble\n# 夢世界の防御調査\n研究番号 TASK-PROSE-025\n"
                          + "前" * 600 + "本文だけの日本語照合" + "後" * 600
                          + "\n末尾の目印\n", encoding="utf-8")
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        ledger = directory / "RECOVERY_LEDGER.tsv"
        ledger.write_text("source_path\tdestination\tdestination_sha256\tcoverage_state\tprior_coverage\tlimitations\n"
                          f"old/report.md\tresearch/recovered/{report.name}\t{digest}\tpartial\tmissing\tHistorical partial prose\n"
                          f"alias/report.md\tresearch/recovered/{report.name}\t{digest}\tpartial\tmissing\talias\n",
                          encoding="utf-8")
        return report, ledger

    def test_reviewed_text_evidence_formats_search_with_hash_lines_and_limits(self):
        directory = self.root / "research/recovered"
        directory.mkdir(parents=True)
        fixtures = {
            "json": ('{\n  "id": "AUDIT-001",\n  "note": "証拠単語(json)",\n  "status": "PASS"\n}\n', 3),
            "txt": ("# plain raw heading\n証拠単語(txt)\n", 2),
            "py": ('raise RuntimeError("証拠単語(py)")\n', 1),
            "csv": ("id,note\nA,証拠単語(csv)\n", 2),
            "tsv": ("id\tnote\nA\t証拠単語(tsv)\n", 2),
            "jsonl": ('{"id":1}\n{"note":"証拠単語(jsonl)"}\n', 2),
        }
        entries = []
        for suffix, (content, line) in fixtures.items():
            report = directory / ("format-" + suffix + "." + suffix)
            report.write_text(content, encoding="utf-8")
            digest = hashlib.sha256(report.read_bytes()).hexdigest()
            entries.append(f"research/recovered/{report.name}\t{digest}\tHistorical receipt; not runtime proof\n")
        hidden = directory / "unreviewed.json"
        hidden.write_text('{"note":"unreviewed evidence wording"}', encoding="utf-8")
        binary = directory / "opaque.bin"
        binary.write_text("unsupported evidence wording", encoding="utf-8")
        entries.append("research/recovered/opaque.bin\t" + hashlib.sha256(binary.read_bytes()).hexdigest() + "\tunsupported extension\n")
        (directory / "RECOVERY_LEDGER.tsv").write_text(
            "destination\tdestination_sha256\tlimitations\n" + "".join(entries), encoding="utf-8")
        data = reference.load(self.root)
        self.assertEqual(len(data["documents"]), len(fixtures))
        for suffix, (_, line) in fixtures.items():
            hits = reference.search(data, "証拠単語(" + suffix + ")")
            self.assertEqual(len(hits), 1)
            hit = hits[0]
            self.assertEqual(hit["kind"], "document_match")
            self.assertEqual(hit["name"], "format-" + suffix + "." + suffix)
            self.assertEqual(hit["source"]["start_line"], line)
            self.assertEqual(hit["source"]["sha256"], hashlib.sha256(
                (self.root / hit["source"]["path"]).read_bytes()).hexdigest())
            self.assertIn("not runtime proof", hit["recovery"]["limitations"])
            self.assertNotIn("reported_status", hit)
            self.assertNotIn("target_version", hit)
        self.assertEqual(reference.search(data, "unreviewed evidence wording"), [])
        self.assertEqual(reference.search(data, "unsupported evidence wording"), [])
        pages = reference.render(self.root, data)
        self.assertIn("format-json.json?plain=1#L1-L1", pages["reference/DOCUMENTS.md"])

    def test_evidence_unicode_separators_do_not_change_physical_source_lines(self):
        directory = self.root / "research/recovered"
        directory.mkdir(parents=True)
        receipt = directory / "unicode.json"
        content = json.dumps({"note": "before\u2028needle-json\u2029tail\u0085end"}, ensure_ascii=False) + "\r\n"
        receipt.write_bytes(content.encode("utf-8"))
        text_report = directory / "unicode.txt"
        text_report.write_bytes("prefix\u2028inline\r\nneedle-txt\r\n".encode("utf-8"))
        entries = [f"research/recovered/{path.name}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\n"
                   for path in (receipt, text_report)]
        (directory / "RECOVERY_LEDGER.tsv").write_text(
            "destination\tdestination_sha256\n" + "".join(entries), encoding="utf-8")
        data = reference.load(self.root)
        for query, expected in (("needle-json", 1), ("needle-txt", 2)):
            hits = reference.search(data, query)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0]["source"]["start_line"], expected)
            self.assertEqual(hits[0]["source"]["end_line"], expected)
        source = {"path": "research/recovered/unicode.json",
                  "sha256": hashlib.sha256(receipt.read_bytes()).hexdigest(),
                  "start_line": 2, "end_line": 2}
        with self.assertRaisesRegex(ValueError, "source lines"):
            reference.validate_source(self.root, source, "bad-physical-line")

    def test_generic_receipt_does_not_replace_structured_run_results(self):
        ledger = self.add_run_results()
        receipt = ledger.parent / "audit.json"
        receipt.write_text('{"note":"攻撃値 receipt-only", "status":"PASS"}\n', encoding="utf-8")
        with ledger.open("a", encoding="utf-8") as stream:
            stream.write("research/recovered/audit.json\t" + hashlib.sha256(receipt.read_bytes()).hexdigest()
                         + "\tHistorical audit only\n")
        data = reference.load(self.root)
        hits = reference.search(data, "攻撃値")
        self.assertEqual(sum(hit["kind"] == "research_run_record" for hit in hits), 2)
        docs = [hit for hit in hits if hit["kind"] == "document_match"]
        self.assertEqual(len(docs), 1)
        self.assertNotIn("reported_status", docs[0])
        self.assertEqual(len(data["documents"]), 1)

    def test_document_search_finds_title_id_filename_and_body_with_cited_excerpt(self):
        report, _ = self.add_prose_report()
        data = reference.load(self.root)
        for query, line in (("夢世界の防御調査", 2), (report.name.lower(), 2),
                            ("TASK-PROSE-025", 3), ("本文だけの日本語照合", 4), ("末尾の目印", 5)):
            with self.subTest(query=query):
                hits = reference.search(data, query)
                self.assertEqual(len(hits), 1)
                hit = hits[0]
                self.assertEqual(hit["kind"], "document_match")
                self.assertEqual(hit["name"], "夢世界の防御調査")
                self.assertEqual(hit["confidence"], "研究本文の一致（意味・動作の検証なし）")
                self.assertNotIn("target_version", hit)
                source = hit["source"]
                self.assertEqual(source["path"], "research/recovered/" + report.name)
                self.assertEqual(source["sha256"], hashlib.sha256(report.read_bytes()).hexdigest())
                self.assertEqual((source["start_line"], source["end_line"]), (line, line))
                self.assertLessEqual(len(hit["summary"]), 400)
                self.assertNotIn("lines", hit)
                self.assertNotIn("body", hit)
                self.assertEqual(hit["recovery"]["limitations"], "Historical partial prose")
                self.assertEqual(hit["recovery"]["ledger"]["start_line"], 2)
        body = reference.search(data, "本文だけの日本語照合")[0]["summary"]
        self.assertIn("本文だけの日本語照合", body)
        self.assertTrue(body.startswith("前") and body.endswith("後"))
        self.assertEqual(reference.search(data, "存在しない調査文"), [])
        self.assertEqual(reference.search(data, "Historical partial prose"), [])
        self.assertEqual(len(data["documents"]), 1)
        for section in ("symbols", "fields", "relations", "mentions", "field_mentions"):
            self.assertNotIn("TASK-PROSE-025", json.dumps(data[section], ensure_ascii=False))

    def test_document_ranking_precedes_cap_and_preserves_ties_sources_and_inputs(self):
        # Earlier incidental mentions must not crowd filename/title matches out of the cap.
        directory = self.root / "research/recovered"
        directory.mkdir(parents=True)
        query = "target-report.md"
        body_names = [f"body-{i:02d}.md" for i in range(21, -1, -1)]
        fixtures = [(name, "# Ordinary report\n" + "p" * 600 + query + "s" * 600
                     + "\nsecond " + query + "\n") for name in body_names]
        fixtures += [
            ("title-z.md", "preamble\n# Review target-report.md\n"),
            ("title-a.md", "preamble\n# Another target-report.md review\n"),
            ("z-target-report.md", "preamble\n# Filename evidence Z\n"),
            ("a-target-report.md", "preamble\n# Filename evidence A\n"),
        ]
        rows = []
        for name, content in fixtures:
            report = directory / name
            report.write_bytes(content.encode("utf-8"))
            rows.append(f"research/recovered/{name}\t"
                        + hashlib.sha256(report.read_bytes()).hexdigest() + "\n")
        ledger = directory / "RECOVERY_LEDGER.tsv"
        ledger.write_text("destination\tdestination_sha256\n" + "".join(rows), encoding="utf-8")
        before_bytes = {path: path.read_bytes() for path in directory.iterdir()}
        data = reference.load(self.root)
        before_documents = json.dumps(data["documents"], ensure_ascii=False, sort_keys=True)

        hits = reference.document_matches(data["documents"], query.upper())

        expected_names = ["z-target-report.md", "a-target-report.md",
                          "title-z.md", "title-a.md"] + body_names[:16]
        self.assertEqual([Path(hit["source"]["path"]).name for hit in hits], expected_names)
        self.assertEqual(len(hits), 20)
        self.assertTrue(all(hit["total_document_matches"] == 26 for hit in hits))
        self.assertTrue(all(hit["document_matches_truncated"] for hit in hits))
        self.assertTrue(all(hit["source"]["start_line"] == 2
                            and hit["source"]["end_line"] == 2 for hit in hits))
        self.assertEqual(hits[0]["summary"], "# Filename evidence Z")
        self.assertEqual(hits[2]["summary"], "# Review target-report.md")
        self.assertEqual(hits[4]["summary"], "p" * 192 + query + "s" * 192)
        self.assertEqual(json.dumps(data["documents"], ensure_ascii=False, sort_keys=True),
                         before_documents)
        self.assertEqual({path: path.read_bytes() for path in directory.iterdir()}, before_bytes)
        self.assertEqual(reference.document_matches(data["documents"], query.upper()), hits)

    def test_document_search_cap_order_first_match_and_filename_fallback(self):
        report, _ = self.add_prose_report()
        data = reference.load(self.root)
        sample = data["documents"][0]
        data["documents"] = [dict(sample, id=f"document:{i}") for i in range(25)]
        self.assertEqual([row["id"] for row in reference.search(data, "目印")],
                         [f"document:{i}" for i in range(20)])
        hits = reference.search(data, "目印")
        self.assertTrue(all(row["total_document_matches"] == 25 and row["document_matches_truncated"] for row in hits))
        report.write_text("first plain line\nsecond needle\nthird needle\n", encoding="utf-8")
        ledger = report.parent / "RECOVERY_LEDGER.tsv"
        ledger.write_text("destination\tdestination_sha256\nresearch/recovered/" + report.name
                          + "\t" + hashlib.sha256(report.read_bytes()).hexdigest() + "\n", encoding="utf-8")
        data = reference.load(self.root)
        self.assertEqual(reference.search(data, report.name)[0]["source"]["start_line"], 1)
        self.assertEqual(reference.search(data, "needle")[0]["source"]["start_line"], 2)

    def test_document_overview_and_fresh_cli_show_sources_without_full_body(self):
        report, _ = self.add_prose_report()
        data = reference.load(self.root)
        pages = reference.render(self.root, data)
        overview = pages["reference/DOCUMENTS.md"]
        self.assertIn("夢世界の防御調査", overview)
        self.assertIn(report.name + "?plain=1#L2-L2", overview)
        self.assertIn("Historical partial prose", overview)
        self.assertIn("partial", overview)
        self.assertIn("RECOVERY_LEDGER.tsv?plain=1#L2-L2", overview)
        self.assertIn("20", overview)
        self.assertIn("400", overview)
        self.assertIn("DOCUMENTS.md", pages["reference/README.md"])
        self.assertEqual(pages, reference.render(self.root, reference.load(self.root)))
        command = [sys.executable, "-B", str(Path(reference.__file__)), "--root", str(self.root),
                   "search", "本文だけの日本語照合"]
        for option in ([], ["--json"]):
            result = subprocess.run(command + option, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Historical partial prose", result.stdout)
            self.assertIn(report.name, result.stdout)
            self.assertNotIn("前" * 500, result.stdout)
            if option:
                self.assertEqual(json.loads(result.stdout), reference.search(data, "本文だけの日本語照合"))
            else:
                self.assertIn(":4-4", result.stdout)
                self.assertIn(hashlib.sha256(report.read_bytes()).hexdigest(), result.stdout)
                self.assertIn("RECOVERY_LEDGER.tsv", result.stdout)

    def test_document_cli_reports_cap_and_preserves_critical_recovery_limits(self):
        report, ledger = self.add_prose_report()
        limits = "Historical partial prose " + "context " * 70 + "HOLD_FOR_ID_RECONCILIATION"
        entries = []
        for number in range(24, -1, -1):
            path = report.with_name(f"reviewed-{number:02d}.md")
            path.write_text(f"# Shared lookup {number}\nbody\n", encoding="utf-8")
            entries.append(f"research/recovered/{path.name}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\t{limits}\n")
        ledger.write_text("destination\tdestination_sha256\tlimitations\n" + "".join(entries), encoding="utf-8")
        unreviewed = report.with_name("unreviewed.md")
        unreviewed.write_text("# Unreviewed secret wording\n", encoding="utf-8")
        data = reference.load(self.root)
        self.assertEqual(reference.search(data, "secret wording"), [])
        self.assertEqual(reference.search(data, "Shared lookup")[0]["name"], "Shared lookup 24")
        self.assertIn("HOLD_FOR_ID_RECONCILIATION", reference.render(self.root, data)["reference/DOCUMENTS.md"])
        command = [sys.executable, "-B", str(Path(reference.__file__)), "--root", str(self.root),
                   "search", "Shared lookup"]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("25", result.stdout)
        self.assertIn("20", result.stdout)
        self.assertIn("HOLD_FOR_ID_RECONCILIATION", result.stdout)
        result = subprocess.run(command + ["--json"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        hits = json.loads(result.stdout)
        self.assertEqual(len(hits), 20)
        self.assertTrue(all(hit["total_document_matches"] == 25 and hit["document_matches_truncated"] for hit in hits))
        self.assertTrue(all(hit["recovery"]["limitations"] == limits for hit in hits))

    def pagination_fixture(self, count):
        directory = self.root / "research/recovered"
        directory.mkdir(parents=True, exist_ok=True)
        report = directory / "pagination.md"
        ledger = directory / "RECOVERY_LEDGER.tsv"
        entries = []
        for number in range(count):
            path = report.with_name(f"pagination-{number:03d}.md")
            path.write_text(f"# Pagination title {number:03d}\nbody {number}\n", encoding="utf-8")
            entries.append(f"research/recovered/{path.name}\t{hashlib.sha256(path.read_bytes()).hexdigest()}"
                           f"\tpartial\tprior-{number}\tlimit-{number} " + "context " * 70
                           + "HOLD_FOR_ID_RECONCILIATION\n")
        ledger.write_text("destination\tdestination_sha256\tcoverage_state\tprior_coverage\tlimitations\n"
                          + "".join(entries), encoding="utf-8")
        return reference.load(self.root)

    def test_document_pagination_keeps_all_provenance_and_resolves_nested_links(self):
        data = self.pagination_fixture(101)
        pages = reference.render(self.root, data)
        overview = pages["reference/DOCUMENTS.md"]
        names = ["reference/documents/page-001.md", "reference/documents/page-002.md"]
        self.assertEqual(sorted(name for name in pages if name.startswith("reference/documents/")), names)
        self.assertIn("documents/page-001.md", overview)
        self.assertIn("documents/page-002.md", overview)
        self.assertIn("101", overview)
        self.assertIn("100", overview)
        self.assertIn("Pagination title 000", overview)
        self.assertIn("Pagination title 099", overview)
        self.assertIn("Pagination title 100", overview)
        self.assertNotIn("?plain=1#L", overview)
        self.assertNotIn("HOLD_FOR_ID_RECONCILIATION", overview)
        self.assertLess(len(overview), 3000)
        for page_name, expected in zip(names, (data["documents"][:100], data["documents"][100:])):
            content = pages[page_name]
            self.assertEqual(content.count("制約・訂正"), len(expected))
            self.assertIn("../DOCUMENTS.md", content)
            self.assertIn("../README.md", content)
            for document in expected:
                source, recovery = document["source"], document["recovery"]
                ledger = recovery["ledger"]
                self.assertIn(document["name"], content)
                self.assertIn(source["sha256"], content)
                self.assertIn(recovery["limitations"], content)
                self.assertIn(recovery["prior_coverage"], content)
                self.assertIn(f"../../{source['path']}?plain=1#L{source['start_line']}-L{source['end_line']}", content)
                self.assertIn(f"../../{ledger['path']}?plain=1#L{ledger['start_line']}-L{ledger['end_line']}", content)
            for target in re.findall(r"\]\(([^)]+)\)", content):
                relative = unquote(urlsplit(target).path)
                resolved = (self.root / page_name).parent.joinpath(relative).resolve()
                generated = resolved.relative_to(self.root).as_posix()
                self.assertTrue(resolved.is_file() or generated in pages, target)
        self.assertIn("page-002.md", pages[names[0]])
        self.assertNotIn("page-000.md", pages[names[0]])
        self.assertIn("page-001.md", pages[names[1]])
        self.assertNotIn("page-003.md", pages[names[1]])

    def test_document_pagination_keeps_empty_and_hundred_document_overviews_inline(self):
        for count in (0, 100):
            with self.subTest(count=count):
                data = self.pagination_fixture(count)
                pages = reference.render(self.root, data)
                self.assertFalse(any(name.startswith("reference/documents/") for name in pages))
                overview = pages["reference/DOCUMENTS.md"]
                self.assertEqual(overview, reference.render_documents(data["documents"]))
                self.assertEqual(overview.count("制約・訂正"), count)
                if count:
                    self.assertIn("../research/recovered/pagination-099.md?plain=1#L1-L1", overview)
                    self.assertIn("HOLD_FOR_ID_RECONCILIATION", overview)

    def test_document_pagination_shrink_reports_obsolete_pages_without_deletion(self):
        self.pagination_fixture(101)
        command = [sys.executable, "-B", str(Path(reference.__file__)), "--root", str(self.root)]
        built = subprocess.run(command + ["build"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(built.returncode, 0, built.stderr)
        page = self.root / "reference/documents/page-002.md"
        self.assertTrue(page.is_file())
        self.pagination_fixture(1)
        checked = subprocess.run(command + ["check"], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(checked.returncode, 0)
        self.assertIn("reference/documents/page-002.md (obsolete generated page; review removal)", checked.stderr)
        self.assertTrue(page.exists())

    def test_document_search_optional_ledger_and_rejects_bad_alias_hash_and_escape(self):
        self.assertEqual(reference.load(self.root).get("documents"), [])
        report, ledger = self.add_prose_report()
        original = ledger.read_text(encoding="utf-8")
        ledger.write_text(original.splitlines()[0] + "\n", encoding="utf-8")
        self.assertEqual(reference.load(self.root)["documents"], [])
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        ledger.write_text(original.replace("alias/report.md\tresearch/recovered/" + report.name + "\t" + digest,
                                           "alias/report.md\tresearch/recovered/" + report.name + "\t" + "0" * 64), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Stale"):
            reference.load(self.root)
        ledger.write_text("destination\tdestination_sha256\n../escape.md\t00\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "escapes"):
            reference.load(self.root)

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
