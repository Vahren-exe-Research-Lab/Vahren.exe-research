# Verification

Checked 2026-11-05. Approved inputs: 45; root-schema report ledger rows: 45; columns: 9. Measured input SHA256 and byte lengths match every supplied approval SHA/length. Five input rows had no prior catalog SHA pin; their observed SHA256 is recorded without claiming a pre-existing pin.

Recovered bodies: 40. Exact-body/alias destination hash checks: 41/41; mismatches: 0. Four whole-body deferrals have blank destination and destination_sha256 fields. No transformations; TRANSFORMS.tsv contains only its header.

Alias: tests/OFFLINE_UNSYNCED_E_20261028/T020_T028_DIALOG_ROUTE_PROVENANCE_20261028_1645.md points to research/recovered/tests_batch5/T020_T028_DIALOG_ROUTE_PROVENANCE_20261028_1645.md. Independent complete-byte comparison returned True; source and destination SHA256 are a1fe3562b386c52e490ecf4343998dc834f930315bbbbf0e76a8bef93e9f726c (8,462 bytes). The accepted canonical body was fully reviewed once.

No exact source-SHA match was found in the baseline root RECOVERY_LEDGER.tsv or SOURCE_MANIFEST.tsv metadata during selection. This is a document-identity check, not a semantic deduplication claim. Original source paths remain separate even when bytes coincide.

No native binary execution, fixture replay, game/runtime observation, Golden qualification or READY promotion occurred. No Git operations or changes outside this batch directory were made.
