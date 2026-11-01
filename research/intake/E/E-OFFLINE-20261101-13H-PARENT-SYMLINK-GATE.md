# E/T018-T020 — G0/G1/G2 receipt parent-path alias admission gap (uncurated)

- research_id: E-OFFLINE-20261101-13H-T018-T020-PARENT-SYMLINK-RUN-ROOT-01
- owner: E; tasks: T018,T020; T019 carries prior contradiction state only.
- observed_at: 2026-11-01 13H JST; context: 2026-11-01 09–12H independent synthetic validation (historical snapshots).
- source_relative_path: Library/T018_T020_G012_PARENT_SYMLINK_RUN_ROOT_AUDIT_20261101_13h.md
- source_sha256: 3B2967D293393EA934429F9CB8D7FB2238598259DD575FAF69E29F34FAEC43C5 (2026-11-01 materialized raw bytes independently verified).
- prior_ids: E 11H source-byte gate; E 12H cross-run alias preflight; later correction E-OFFLINE-20261101-14H-T018-T020-PINNED-HANDLE-TOCTOU-01.
- va/call/offset: N/A; no new native PE analysis.
- evidence_kind: STATIC prior comparator review / SYNTHETIC / VERIFY / original DYNAMIC 0.
- golden_status: G0/G1/G2 NOT RUN; original actual Golden PASS0, strict MATCH0.
- ready_status: NOT READY; PUBLISHED_INTAKE is storage only.
- kb_candidate: E/T018-T020-G012-PARENT-SYMLINK, independent receipt role/path ancestry gate.

## Bounded reusable finding
Earlier standalone evidence gate distinguished relative prefixes original/ and replacement/, and used resolved absolute paths/file identity for selected files, but could miss an alias introduced by an intermediate **parent directory symlink** into a different role's unused file. Leaf-only symlink exclusion and canonical path inside a common synthetic root are insufficient. This audit created an independent per-component lstat/role-scoped check; five types of parent alias × three seeds = 15 rejected former holes, plus 36/36 expected outcomes in the independent synthetic gate as later counted in 15H cross-audit. A successful classification of a synthetic fixture does not prove the actual native battle observed or the Windows reparse behavior.

The subsequent 14H study found that a pre-check of path components is still not equivalent to using the **same open file handle** for byte reads, so this gate is an intermediate solution, not a final airtight collector. Windows file ID, atomic capture, collection authenticity, G0 lawful UI, G1 same-run prebattle SAVE and ordered inputs, G2 actual MAP/three Power sides/Unit/Troop order remain VERIFY or NOT RUN.

## T019 / recovery / next
No newly confirmed T019 contradiction. Historic GameClear DAT13/TXT2 enumeration-domain difference remains RESOLVED, script2 runtime priority / TXT loader remain VERIFY. Study's PC connector was unavailable (session terminated, connectivity not safety denial); this batch now uses its independently materialized Library source. Authorized PC current MASTER was independently readable in the current E pass, but latest full reconciliation was not done: last formal checkpoint196, READY596 (A115/B229/C136/D116), 34 task status DONE9/IN_PROGRESS21/VERIFY4 are old last-confirmed only. New formal READY0. Historic safety-denied content and operations are excluded, not retried.

Next: use the separate 14H pinned-handle review; native Windows validation and lawful same-battle G0/G1/G2 remain prerequisites for strict comparison.