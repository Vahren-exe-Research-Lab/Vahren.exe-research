# B-20261031-21H-T013-FIRST-NODE-SENTINEL-TO-COORD-01 — B historic T013 source intake

- research_id: `B-20261031-21H-T013-FIRST-NODE-SENTINEL-TO-COORD-01`
- owner: B
- tasks: T013 (Unit candidate lists / target-selection prerequisites)
- observed_at: 2026-10-31 21H JST
- source_relative_path: `data/T013_FIRST_HEAD_SENTINEL_COORD_BRANCH_NATIVE_20261031_21H.md`
- source_sha256: `28b10830eda389b377a9ffcebeb28a21c87297a2382cccf2e8acb85b0da89d29` (2026-11-02 JST authorized PC original Markdown SHA256/byte-length verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no new executable hash during intake)
- evidence_va_call_offsets: `0x57DD10,0x57DD13,0x57DD42,0x57DDD3/DA/DC/E2/E4/E7/ED/F6/FB,Unit+0x18650/+0x18654,+0x186C8/+0x186CC,0x57DE95→0x4C1860`
- prior_ids_and_corrections: B-20261031-20H-T013-UNIT18654-LIST-WRITER-REMOVE-01 count reader known; 22H follows conditional clear, 23H rect helper ABI
- evidence_kind: historical source STATIC original ASM / V9 CALL and INFERRED, VERIFY for interpretation; original game DYNAMIC=0
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / no E MASTER formal update
- intake_status: PUBLISHED_INTAKE on exact GitHub readback; NOT_CURATED until independent KB review

## Reusable historical evidence

Historical native check of `0x57DD10` finds prerequisite nonzero `Unit+0x198` and `+0x1E580` and state gates before the candidate-list branch. With `Unit+0x18654` nonzero, `0x57DDDC..0x57DDE4` takes the first node pointer from `Unit+0x18650`. If that head candidate has `+0x40==1` OR `+0x26D!=0`, native `0x57DDF6..0x57DE01` writes sentinel `0x80000008` to **both** `Unit+0x186C8` and `+0x186CC`. Otherwise the local path can return without the two writes. This is a **conditioned sentinel update**, not proof of attack coordinates, closest target, or actual movement. The later `0x57DE95→0x4C1860` rect test, `0x576660` list reset, and `0x543DE0` postprocessing are studied in 22H/23H; do not conflate those independent fields or infer complete final target.

## Provenance and next verification

Link corrected 22H reset and 23H rectangle BOOL semantics, inspect V9 head/flag writer and consumers of +0x186C8/CC within safe scope. This owner-created sanitized summary references the real B source by relative path and measured SHA. It does not constitute new full decompilation, original-game execution, G4 external battle-result settlement or verified final target. Dedicated curator alone may interpret REF/typed dictionary/develop based on independent native/DAT and errata audit; original game files, large index, private paths and refused payloads are excluded.
