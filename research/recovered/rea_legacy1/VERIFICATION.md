# Verification

Checked2026-11-05 with a new independent verification pass after writing receipts.

- Exactly45 unique literal selected paths;45 metadata, selection, identity and nine-column ledger rows.
- All45 original source SHA256 values re-read and matched; all45 expected byte lengths matched (333,261bytes).
-43 report destinations: full source/destination byte equality and SHA256 equality passed (315,395bytes).
-2 held composites have blank destination and destination SHA; two exact source_path rows exist in DEFERRED.tsv.
-45 distinct source SHA values;0 within-batch aliases. Baseline authorized manifest/root-ledger hash and filename comparison:0 exact aliases and0 differing-body filename variants. Catalog SHA comparison:0 matches.
-43 complete IDENTITY_BYTES receipts; privacy-only transforms0; UTF8 byte ranges cover whole bodies. Prefix/suffix empty-SHA proofs accompany identity records.
-Identity receipts preserve historical named IDs, including37 distinct REA-OFFLINE/REA-E-B-ID-ALIGN IDs. Main report/Library receipt IDs intentionally repeat; this is not a count of new discoveries. Other B and connection IDs remain visible in receipts and retained body text.
-No personal absolute-path token found in any output file. Authored historical Library and/mnt/data labels retained.
-No linked payload or historical verifier executed. No Git/native/game/runtime/Remote operation. Source bytes were not modified; writes confined to rea_legacy1.

These checks establish authored-document recovery and current byte identity only. All native, synthetic, Library readback, formal progress and Golden claims remain historical author assertions. Future coordinator integration must deduplicate concurrent batches by SHA and preserve both whole-body holds.
