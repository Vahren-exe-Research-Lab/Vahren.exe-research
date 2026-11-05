# Verification: pending_models2

Post-write checks on2026-11-05:

- Two exact approved original paths partitioned into two accepted rows and zero deferred; original total355,864bytes. One full authored T025 study and one pointer-only T034 are distinct coverage roles.
- Root accepted ledger schema is exactly nine columns. Metadata, identity, dedup and transform each have two rows; REVIEW_COVERAGE has three contiguous assigned review records; INPUT_RECEIPTS has five snapshots. DEFERRED and PRIVACY_SPANS are header-only, not omitted.
- Complete T025 LF1–1149 coverage is supported by reviewer1–600 plus helper601–1149, source SHA pinned unchanged. Explicit220–241 reread repairs the earlier truncated output. T034 fullpointerLF1–3 reviewed. No substantive known held payload found; no partial substitute/excerpt of a held source archived.
- Both saved bodies equal their approved originals byte for byte; current/catalog source SHA and size match. Strict UTF-8, terminal LF and physical LF counts verified. Identity spans cover [0,source_bytes), with no replacements and empty prefix/suffix hashes.
- Baseline root ledger1,613 rows: no selected source/destination SHA alias; two source hashes distinct. Existing primary T034 source/destination/SHA linkage comes from that baseline metadata only.
- All five input receipt snapshots matched at final verification; all output files except the manifest itself are listed with actual SHA/bytes in OUTPUT_MANIFEST.tsv. Two body files only; no unexpected body files, personal-path variants or scratch publication files.
- Only task-owned directory written. Originals and measured root ledger/current inventory/selection unchanged; no Git/code/shared write or linked/native/runtime execution.

Verification establishes recovery integrity and scope, not new native semantics, dictionary fields/relations, type/class/ABI identity, Golden PASS or READY. Future coordinator metadata edits are separate from these preparation-point snapshots.
