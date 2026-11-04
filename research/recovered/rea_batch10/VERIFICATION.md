# REA batch10 verification

Independent post-write readback completed2026-11-05.

- PASS: all45 literal approved paths are accounted for exactly once by selection receipts, current metadata, identity receipts and the root-schema nine-column report ledger; no extra source body was selected.
- PASS: all45 original files still match measured source hashes and approved byte counts,228,475 bytes total; blank approved hashes remain explicitly unsupplied.
- PASS:44 complete archived report bodies match source bytes and recorded destination SHA256 exactly,222,444 bytes total. UTF-8 decoding succeeds; original line endings and all authored qualifiers are retained.
- PASS: all44 identity transform receipts have verified whole-body token hash, zero-based half-open UTF-8 byte bounds, complete sizes and empty prefix/suffix proofs. Privacy-only derivatives0; baseline aliases0; within-batch aliases0; same-name differing-body variants0. No duplicate archived body hash exists.
- PASS: one held dependent composite has blank ledger destination/hash and no transform/body artifact: the Oct21 1735 sentry contrast report containing prior-refused0x429620 material. Its approved source_path is explicitly recorded in DEFERRED.tsv. Eleven generic held-boundary rows have blank source_path.
- PASS: all four input snapshots still match their recorded sizes and hashes. All45 paths are absent from the supplied old catalog; current metadata is a supplement, not retroactive approval. There are41 historical research IDs and five readback-role inputs.
- PASS: no personal absolute drive/home/UNC path tokens were found in batch reports or receipts. No prose edit, trimming, newline normalization or partial-body redaction occurred.
- REVIEWED: current curated REF priority, historical STATIC/DERIVED/SYNTHETIC/VERIFY/NOT READY, pending/readback statuses, original audit limits/failures/corrections and Golden DESIGNED/NOT RUN remain explicit in complete recovered bodies and README. Metadata-only deferral does not recover a helper body or permit retry.

Verification examined only the approved Markdown originals, generated owned outputs and authorized input metadata; no linked payload, baseline report body, native executable, historical script, JSON/log/SQLite/HANDOFF/archive was opened or executed. No new native/runtime/ABI/Golden/READY claim follows from these byte-archive checks. No Git, REA/Ghidra/game or Remote tool was used; writes are confined to this new batch10 directory.
