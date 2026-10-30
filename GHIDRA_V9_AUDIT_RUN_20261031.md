# Ghidra V9 / research corpus integration verification — 2026-10-31

- Owner: Research Knowledge curator; scope: GitHub private KB sources and isolated synthetic tests.
- Source: PC unified V9 SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE; target PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
- Ghidra/PE were not executed or rewritten; V9 and original research index were read-only.
- V9 catalog: 11,950 entries, 11,762 internal functions, 243,678 refs, 51,214 native branch/CALL site records.
- Protected area rule: 1 overlapping function and 44 native records excluded from result graphs, never inspected as a target.
- Report references: GHIDRA_V9_COVERAGE_REPORT.md, GHIDRA_V9_GAPS_TOP500.tsv, GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv, GHIDRA_V9_B_REVIEW_TOP150.tsv.
- The full 11,761-row per-function metadata crosswalk is generated locally under knowledge/generated/, not tracked on GitHub.
- Corpus sampled by metadata only: 22,487 files across eight allowed research folders; 3,817 text-like, 1,779 indexed in these folders.
- Index gap inspection classified 1,234 source/unsupported extensions, 799 files outside enabled search depth and 5 files over 3 MB; zero eligible indexed-text omissions at the verification checkpoint.
- During the run, E produced 3 new T020 files. Authorized incremental research_index updated 1,787 to 1,790 indexed sources and the read-only --check returned pending 0.
- Initial development error: V9 references include symbolic targets such as Stack[0x4]. This was corrected by a strict VA-only parser; no original data changed.
- Initial synthetic test failure: a test-only SQLite table omitted native_opcode_hex; test fixture was corrected. Windows temporary fixture cleanup also reported a file lock after that exception; this was not a refusal and did not alter the project.
- Final isolated V9 coverage tests: 3 PASS; protected-range exclusion, branch filtering, native E8 call-site lookup and report output verified. No game Golden testing was performed.
- Status: STATIC INDEX / VERIFY / NOT READY; original gameplay Golden PASS=0, strict MATCH=0. No automatic symbol confidence upgrade.
- New investigation: review AI/EXP/retreat specific candidate queues, compare exact original ASM/DAT, then enter verified meanings only with approved owner/task/source ID.
- Prepublish allowlist audit initially BLOCKED on a synthetic test that contained an absolute Windows user-path literal. The dummy path assertion was removed rather than relaxing the privacy scanner; re-audit is required before release.
【Nested-scope classification addendum】The 799 shallow-index-excluded text-like files were metadata-classified as: plugin work 321, archived history 206, takeover research 180, source snapshot/normalized 52, runtime traces 31, manual review 9. Bulk recursive indexing was not enabled because it would mix archived/duplicate/generated/runtime source with curated research. No nested original source content was uploaded. Local research_index.py --check returned 0 pending after the three newly produced E reports were incrementally indexed. Golden PASS=0/strict MATCH=0.
