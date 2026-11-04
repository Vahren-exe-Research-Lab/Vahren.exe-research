# Batch8 verification

Verified 2026-11-05 in a separate local process after writing. PASS:

- Approval selection equals all 45 report-ledger paths, with no duplicate source paths or source hashes.
- All 45 current source sizes match approved sizes; source hashes match current metadata and final read-only original remeasurement.
- All 44 archived files equal the complete original byte arrays and destination SHA256 values. Total archived body bytes: 146,193. Total reviewed original bytes: 149,345.
- Exactly one approved primary is deferred with no destination or destination hash and no archived body. It is not reconstructed from the separately retained readback.
- Nine-column report schema matches root. Identity/current metadata rows: 45 each. Identity transform receipts: 44. Privacy derivative receipts: 0. Seven held-scope metadata rows plus one approved-body deferral: 8.
- Baseline and within-batch SHA256 alias checks: 0 aliases; same-filename differing-body candidates: 0. Exact copies: 44; privacy variants: 0; approved-body deferrals: 1.
- All six receipted input snapshots remain hash-identical at final verification.
- Authored metadata and archived text contain no detected personal absolute path. No original secret/replacement token was published.

Verification checked document identity, selection and recovery receipts only. Historical author audits, instructions, native code, linked scripts/JSON/logs/DBs, game runtime, READY, ABI and Golden claims were not executed or revalidated. Coordinator supplied base a91676b; no Git query or write was performed. All output files are within this new batch folder.
