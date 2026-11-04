# Batch7 verification

Verified 2026-11-05 by an independent post-write local readback. The verification used approved Markdown bytes and metadata only; no historical audit or native/game analysis was executed.

- Literal approval set, ledger, current metadata, identity receipts and transform receipts: 45/45 rows aligned; no omitted or extra approved source.
- Ledger schema: exactly the nine root-ledger columns.
- Current originals: all 45 SHA256 and byte lengths match recorded receipts and approved sizes; approval hash fields were not supplied.
- Exact copies: 44/44 complete byte comparisons passed.
- Privacy derivative: 1/1 original-token hash, zero-based half-open UTF-8 byte interval, replacement bytes, unchanged prefix/suffix and whole destination hash/length passed.
- Archived bodies: 45 distinct source hashes and 45 report files; no same-filename variants, baseline SHA aliases or within-batch aliases.
- Research identities: 23 historical IDs; paired primary/readback identity is explicit; catalog-ID collisions 0.
- Approved-body deferrals: 0. Seven held boundaries remain metadata-only.
- Every generated UTF-8 file, including reports and receipts, passed the personal absolute-user-path scan.
- Approval and metadata/reference input snapshot SHA256 values remained unchanged at readback.

No original, root/shared ledger, Git, code, linked payload or synced project write was performed. All recovery writes are under this batch folder. Historical STATIC/SYNTHETIC/VERIFY distinctions and Golden 0 remain unchanged; verification is of document recovery and proofs only.
