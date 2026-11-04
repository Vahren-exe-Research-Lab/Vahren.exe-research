# B-OFFLINE-20261022-2113-T012-T013-ATTR-MAP-COLLISION-01: B_T012_T013_COLLISION_ATTRMAP_ORDER_OFFLINE_20261022_2113

- research_id: `B-OFFLINE-20261022-2113-T012-T013-ATTR-MAP-COLLISION-01`
- owner: B
- tasks: T012/T013
- observed_at: historical owner study; recovered 2026-11-02 JST
- source_relative_path: `data/B_T012_T013_COLLISION_ATTRMAP_ORDER_OFFLINE_20261022_2113.md`
- source_sha256: `5b4555caa6f0d1741e6e12720a126f051e7beb20967b9b70fc6d4e529da04753` (PC actual Markdown SHA and byte length verified against SAFE134 recovery inventory)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target identifier; not PE rehashed in this intake)
- prior_ids_and_corrections: B-OFFLINE-20261022-2016-T012-T013-MISSILE-COLLISION-VCALL-01; B-OFFLINE-20261022-2245-T011-T012-T013-OFFSET-ATTR-GATE-01 (later parser correction)
- evidence_kind: historical STATIC-GHIDRA / STATIC-ASM / INFERRED or SYNTHETIC according to source; live behavior VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / new DYNAMIC0
- ready_status: newly confirmed READY0; E MASTER updated0
- intake_status: PUBLISHED_INTAKE only on exact GitHub readback, NOT_CURATED

## Meaning and reproducible evidence anchors

Historical ASM/pseudo-C study of the candidate traversal tree from `Missile+0x78 → manager+0x1D4 → context+0x1C → tree+0x68` at `0x515484`. It described `Skill+0x134` as a candidate map cardinality and per-candidate key check before AABB; the later **22:45 `offset` vs `attr` parser correction supersedes the earlier field-name assumption**, so do not assert the collection's source is literally `attr`. Tree iterator sequence, not simple insertion chronology, can affect the first acceptable AABB candidate in that local route. This is NOT proof of final common targeting, actual hit, or runtime tree instance equivalence. Curator to retain the old finding with explicit erratum link and verify string key writer from DAT.

## Next validation and limitations

Use original owner relative source and SHA; review only permitted current V9 ASM/CALL and relevant DAT, reconcile all ID/semantic corrections and counterexamples. Do not assert complete battle outcome, actual target or G4 postbattle transaction from static callsites alone. No raw game, private identity/path, previous safety-refused payload or giant generated database was copied. Dedicated KB curator alone may promote to formal REF/structures/dictionary/develop.
