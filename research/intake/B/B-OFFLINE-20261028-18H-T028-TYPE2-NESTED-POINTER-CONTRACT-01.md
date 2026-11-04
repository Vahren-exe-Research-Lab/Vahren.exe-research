# B-OFFLINE-20261028-18H-T028-TYPE2-NESTED-POINTER-CONTRACT-01 — 0x583C0D type2 double-indirect read and exact two conditional branch destinations

- **Owner / tasks:** B / T028,T011; domain: MORALE_RETREAT_RESULT.
- **Source and verification date:** data/B_T028_TYPE2_NESTED_POINTER_CONTRACT_OFFLINE_20261028_18H.md (relative to _REDEV_RESEARCH); source Markdown SHA256 `9BFEBFA7F68DCD24DD989CA6FB7AB943A0EDD16EA476DEED7BB5B344278495CF`, bytes read and SHA measured directly on authorized PC **2026-11-02**. Earlier report time stays historical; no claim of a new research ID.
- **Target identity:** original research PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (2,910,720 bytes) directly rehashed 2026-11-02; V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (141,033,472 bytes) rehashed read-only 2026-11-02. Hash identity is not native semantic verification.
- **Status:** `PUBLISHED_INTAKE` only after GitHub exact readback; `NOT_CURATED`; STATIC_NATIVE_BOUNDED,INFERRED,VERIFY; **new** original gameplay Golden PASS 0, strict MATCH 0, new formal READY 0. No G4 external-result or casualty/EXP contract confirmed.
- **Independent check level:** PC_SOURCE_SHA256_AND_NATIVE_BRANCH_BYTES_MATCH_20261102.

## Bounded previously researched meaning

Bounded machine instructions `0x583C0D MOV EAX,[EDI+0x1A4]`, `0x583C13 MOV ECX,[EAX+0x2C]`, `0x583C16 CMP DWORD PTR [ECX+0x1EF140],5` imply a two-step pointer traversal; exact type, reaching definitions, NULL guarantees and object identity are **VERIFY**. Relative branch bytes at `0x498BB3` and `0x583B51` target `0x498D5A` and `0x583B5A` respectively (bounded byte-level verification; not a full function ABI).

## Exact evidence and provenance

2026-11-02 original PE read-only 16B [0x583C0D,0x583C1D) SHA256 `3A8AD127C4B04DE840D368C0000D727FA0538786C5577A615B069D70A820FD82`; branch raw bytes `0F84A1010000` and `7E07` re-read independently. Prior owner secondary-source report predates current PC access; new proof is only this bounded native window and PE identity. This research *refines* the earlier T028 17H ID; previous return branch discovery is not recounted.

- **VA mentions (not all function entries):** `0x498BB3`, `0x498D5A`, `0x583B51`, `0x583B5A`, `0x583C0D`, `0x583C13`, `0x583C16`
- **Offset/raw-field mentions:** EDI+0x1A4; EAX+0x2C; ECX+0x1EF140.
- **Prior IDs / overlap (NOT supersession without direct proof):** `B-OFFLINE-20261028-1712-T028-MERCENARY-ELIGIBILITY-BOOL-01`.

## Reproduction boundary and next step

Read-only reproduce the source digest with SHA-256, compare the precisely cited original DAT lines or current original PE windows (only where explicitly marked as verified above), and check V9/REF/symbol links for already-curated meaning; do not run the real game, reconstruct denied objects, or treat any inferred ABI as certain. Check legitimate reaching definition for EDI/first and second pointer, caller preconditions and post-return membership effect without presuming NULL crashes.

**Owner handoff:** preserve this one existing study ID, its source SHA and uncertainty; no edits to other owners, MASTER, `develop`, REF, symbols/structs or original game files. Blocked evidence remains excluded.
