# B-OFFLINE-20261028-1712-T028-MERCENARY-ELIGIBILITY-BOOL-01 — 0x583A80 AL-returned eligibility gate before a mercenary-path branch

- **Owner / tasks:** B / T028; domain: MORALE_RETREAT_RESULT.
- **Source and verification date:** data/B_T028_MERCENARY_ELIGIBILITY_BOOL_OFFLINE_20261028_17H.md (relative to _REDEV_RESEARCH); source Markdown SHA256 `03753FD71E450A91F6126A24A04400354DB37E58A964DA4452381E1D88128494`, bytes read and SHA measured directly on authorized PC **2026-11-02**. Earlier report time stays historical; no claim of a new research ID.
- **Target identity:** original research PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (2,910,720 bytes) directly rehashed 2026-11-02; V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (141,033,472 bytes) rehashed read-only 2026-11-02. Hash identity is not native semantic verification.
- **Status:** `PUBLISHED_INTAKE` only after GitHub exact readback; `NOT_CURATED`; STATIC_NATIVE_BOUNDED,INFERRED,VERIFY; **new** original gameplay Golden PASS 0, strict MATCH 0, new formal READY 0. No G4 external-result or casualty/EXP contract confirmed.
- **Independent check level:** PC_SOURCE_SHA256_AND_NATIVE_WINDOW_MATCH_20261102.

## Bounded previously researched meaning

Historical owner report identifies a direct `CALL 0x583A80` at `0x498BAC` and `TEST AL,AL` at `0x498BB1`; `JE 0x498D5A` skips a later candidate mercenary path when AL=0. Return conditions were grouped by raw object fields `+0x94`, `+0x7C` and dependent branches (`+0x74`, `+0x174`, `+0xB0`, `+0x1A4`). These are bounded native facts/candidate state meanings, **not** proof that the game actually changes affiliation, morale or retreat state.

## Exact evidence and provenance

Current read-only original PE function range [`0x583A80`,`0x583C4E`) 462B SHA256 `9EDCE848273B6290F0B04263C5F9304A687BD46B9969162F630486E133DAD74F` and caller [`0x498BAA`,`0x498BB9`) 15B SHA256 `29C46EFB0E5B235066B5BD300B81A94FDB70E451D99DFC1B51B5855DE6741498` independently match prior report on 2026-11-02. Older 2026-10-21 search SQLite was a historical secondary cross-check, **not the current V9**. Previous exact 32/32 instruction / 9/9 E8 checks are historical, not rerun.

- **VA mentions (not all function entries):** `0x498BAC`, `0x498BB1`, `0x498BB3`, `0x498D5A`, `0x583A80`, `0x583AB1`, `0x583C0D`, `0x583C16`, `0x583C23`
- **Offset/raw-field mentions:** object+0x94; object+0x7C; object+0x174; object+0x1A4.
- **Prior IDs / overlap (NOT supersession without direct proof):** `B-OFFLINE-20261028-18H-T028-TYPE2-NESTED-POINTER-CONTRACT-01`.

## Reproduction boundary and next step

Read-only reproduce the source digest with SHA-256, compare the precisely cited original DAT lines or current original PE windows (only where explicitly marked as verified above), and check V9/REF/symbol links for already-curated meaning; do not run the real game, reconstruct denied objects, or treat any inferred ABI as certain. Trace legitimate nonblocked caller outcome and separately prove any persistent membership/world result; do not call return AL actual gameplay success.

**Owner handoff:** preserve this one existing study ID, its source SHA and uncertainty; no edits to other owners, MASTER, `develop`, REF, symbols/structs or original game files. Blocked evidence remains excluded.
