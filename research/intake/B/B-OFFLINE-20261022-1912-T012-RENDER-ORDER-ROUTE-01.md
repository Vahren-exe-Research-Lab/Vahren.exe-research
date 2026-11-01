# B-OFFLINE-20261022-1912-T012-RENDER-ORDER-ROUTE-01: B_T012_RENDER_ORDER_ROUTE_OFFLINE_20261022_1912

- research_id: `B-OFFLINE-20261022-1912-T012-RENDER-ORDER-ROUTE-01`
- owner: B
- tasks: T012/T011
- observed_at: historical owner study; recovered 2026-11-02 JST
- source_relative_path: `data/B_T012_RENDER_ORDER_ROUTE_OFFLINE_20261022_1912.md`
- source_sha256: `72ce80c33ad05d19fd2522272dcf190c8dc8cba5542e245b2a20dbf59a88e5e2` (PC actual Markdown SHA and byte length verified against SAFE134 recovery inventory)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target identifier; not PE rehashed in this intake)
- prior_ids_and_corrections: B-OFFLINE-20261022-1813-T011-T012-MISSILE-VTABLE-SLOT38-01; prior registration-source studies
- evidence_kind: historical STATIC-GHIDRA / STATIC-ASM / INFERRED or SYNTHETIC according to source; live behavior VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / new DYNAMIC0
- ready_status: newly confirmed READY0; E MASTER updated0
- intake_status: PUBLISHED_INTAKE only on exact GitHub readback, NOT_CURATED

## Meaning and reproducible evidence anchors

Old STATIC/INFERRED study distinguishes at least **two Missile ordering families** rather than assuming render order is collision/target order. The Missile and SimpleMissile virtual slot `+0x48` candidates are recorded as returning zero on their observed implementations; nonzero alternative slots may route to another draw list. Another route enumerates spatial-bucket candidates before drawing. Bucket-3 comparator in the source uses signed comparison of `object+0x04`, and on equality `+0x08`, e.g. native `0x4BBC64/6C/73/78/7C/84`. Rendering sort, active collision order, AI choice and actual frame visibility are **different assertions**. Native sites were checked in the historical report, but not repeated during intake. Recheck vtables, draw-list ownership and compare sites in V9; do not implement one global sort for all systems.

## Next validation and limitations

Use original owner relative source and SHA; review only permitted current V9 ASM/CALL and relevant DAT, reconcile all ID/semantic corrections and counterexamples. Do not assert complete battle outcome, actual target or G4 postbattle transaction from static callsites alone. No raw game, private identity/path, previous safety-refused payload or giant generated database was copied. Dedicated KB curator alone may promote to formal REF/structures/dictionary/develop.
