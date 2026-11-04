# REA batch9 verification

Independent post-write readback completed 2026-11-05.

- PASS: approved selection, selection receipts, current metadata, identity receipts and nine-column report ledger each account for exactly 45 literal paths; no extra original body was selected.
- PASS: all 45 current originals still match measured source hashes and approved byte counts (167,656 bytes total).
- PASS: all 45 archived destinations match their recorded SHA256 and valid UTF-8; no duplicate destination body hash exists.
- PASS: 41 complete source/destination byte identities; four complete privacy derivatives reconstructed solely from the documented replacements match archived bytes exactly.
- PASS: all 45 transform receipts have correct original token SHA256, half-open UTF-8 byte offsets, original/destination lengths and prefix/suffix SHA256 proofs. No newline normalization, trimming or prose edit occurs outside privacy tokens.
- PASS: no personal absolute drive path appears anywhere in the batch's reports or metadata.
- PASS: counts are 41 exact, 4 privacy-only derivatives, 0 exact aliases, 0 same-name baseline differing variants, 0 approved-body deferrals, 23 historical IDs. Ten generic metadata-only held-scope rows carry blank source_path; no approved ledger destination is blank.
- PASS: readback identities and pending statuses remain historical; original audit success/failure, STATIC/DERIVED/SYNTHETIC/VERIFY/NOT READY and Golden NOT RUN boundaries remain complete. Current curated REF priority is explicitly preserved.

Baseline comparison used source-manifest hashes and recovery-ledger destination hashes only; linked baseline bodies were not opened. Input snapshots are identified in INPUT_RECEIPTS.tsv. Original bytes, receipt reconstruction and destination hashes were verified independently after writing. Metadata-only held boundaries and caller-site refusal treatment were reviewed without opening helper internals. No claim of new native, runtime, Golden or READY validation follows from these archive checks.

Only this new rea_batch9 directory was written. No Git operation, native analysis, historical audit, original/shared/root/code edit or Remote tool was used. One initial verification setup command contained an unmatched parenthesis and stopped before execution; it produced no writes and was corrected before recovery.
