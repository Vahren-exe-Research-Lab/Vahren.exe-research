# Recovery verification

Checked 2026-11-05 using local file/metadata operations only. No source audit/probe or project test suite was run.

- Approval-list entries: 45; approved/current source byte total: 160,060.
- Complete body review: 45/45, in bounded non-truncated text reads.
- Root-compatible ledger: 45 rows, exactly nine specified columns.
- Source allowlist membership: 45/45 matched one approved literal path.
- Current source SHA256 matches recorded source SHA256: 45/45.
- Destination SHA256 matches recorded destination SHA256: 45/45.
- Full source/destination byte-by-byte equality (including newline bytes): 45/45.
- Distinct new body destinations: 45; baseline exact aliases: 0; within-batch duplicate aliases: 0; privacy variants: 0; approved-body deferrals: 0.
- Identity, transformation and source-metadata receipts: 45 rows each; TSV field counts consistent.
- Old catalog literal-path absence: 45/45; baseline same-filename candidates: 0.
- Full reviewed bodies and generated metadata privacy scan: 0 personal absolute-path, email/contact or credential-pattern matches; manual review found no private values needing replacement.
- Excluded-range mention: 1 approved readback contains only the historical explicit 5710C0..571500 no-retry prohibition. It supplies no held-body analysis. Excluded scope stays metadata-only.
- Body SHA comparison against the SOURCE_MANIFEST and root-ledger snapshots found no baseline exact match. Input snapshot hashes are recorded in INPUT_RECEIPTS.tsv.

The current REF already curates the Oct29 00H source's selected gates. Its historical header and larger VERIFY limits remain intact and separately recorded. No native or dynamic correctness claim was independently tested here; historical audit PASS/64 counts are not rerun results. No READY, Golden, strict MATCH, formal VERIFIED or new curation count was created.
