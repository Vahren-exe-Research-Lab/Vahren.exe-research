# Research duplicate-group triage — 2026-10-31 metadata audit

Status: READ-ONLY METADATA CLASSIFICATION / VERIFY; not a proof of semantic duplication or authority to delete owner documents. PRIVATE KB base: 5c816ce0b5160a5f4da68d3dcfe53be3d1399959.
Inputs: RESEARCH_SOURCE_CATALOG.tsv, RESEARCH_DUPLICATE_CANDIDATES.tsv, RESEARCH_INTEGRATION_SNAPSHOT.md; source metadata is SHA256-checked against the authorized PC research index. The original reports, old error payloads, native source and game binaries were NOT imported or edited.

## 1. Full byte-identical groups: 18
- 16 groups are E offline synchronization MIRRORS: same basename and exact same bytes under tests/E_OFFLINE_SYNC_20261029/ and tests/OFFLINE_UNSYNCED_E_20261028/. Do not re-count them as 32 separate research findings; keep both source locations until E owner decides archival policy.
- 1 SHA256 group is the EMPTY FILE digest, containing 4 zero-byte legacy EXE text files. Empty placeholders are not native evidence.
- 1 group is a pair of byte-identical REA recovered-result JSON files with different relative names. Its provenance/history must remain linked, not silently consolidated.
- Exact SHA equality proves identical file contents, NOT that paths may be removed, source ownership is identical, or different experiment runs/Games were performed.

## 2. Shared primary research ID groups: 144, NOT automatically duplicates
- 70 groups have a two-file .md + .json shape, usually report plus structured evidence; 3 are .md + .txt shape, 65 have three or more files, and 6 have other two-file combinations. These are filename/extension shapes only: inspect owner/state/source SHA before declaring report/evidence roles.
- Previously 144 groups were counted in RESEARCH_INTEGRATION_SNAPSHOT.md but only 143 displayed in RESEARCH_DUPLICATE_CANDIDATES.tsv. The old audit script silently dropped any group larger than eight paths.
- Fixed audit_research.py: emit ALL shared-ID groups, retain the true count and first 8 relative paths per row, add an explicit [OMITTED_N_PATHS] marker if truncated. Example EXP-COLLAB-20261021-2112-01 has 11 indexed files, displays first 8 plus [OMITTED_3_PATHS]. The complete source list remains queryable in RESEARCH_SOURCE_CATALOG.tsv; do not copy all original files.
- Synthetic regression now builds 11 distinct input files sharing one ID and asserts there is one output row, count=11, explicit omitted marker, and consistent snapshot group count. This is a tool correctness fix, not new gameplay knowledge.

## 3. Review order and safety boundary
- Prioritize the 6 unusual two-file shared-ID shapes and the 3 MD/TXT pairs for owner/ID/VA/source meaning checks; then inspect multi-file owner evidence packages. No auto-merge, deletion, rename, confidence increase or Golden/READY promotion on metadata alone.
- For 16 E mirrors, note exact identity but preserve both archival references. For source corrections, retain earlier ID as superseded, newer verified claim and independent proof; never count source mentions as separate discoveries.
- Keep the 21 safety-held B items, unrecovered 10/25 research, forbidden addresses and refused operations BLOCKED. Do not use an alternative tool/path/shell/ZIP to retrieve refused evidence. No full 22k-file GitHub mirroring.
- Scope and counts are a snapshot of 1,823 indexed documents: full catalogue 1,823/1,823 SHA receipts, 0 missing/stale/redacted; exact groups18, shared groups144. Original gameplay Golden PASS=0 and strict MATCH=0.
