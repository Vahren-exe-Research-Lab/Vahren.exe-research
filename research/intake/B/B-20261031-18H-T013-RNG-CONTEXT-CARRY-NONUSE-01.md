# B-20261031-18H-T013-RNG-CONTEXT-CARRY-NONUSE-01 — B historic T013 source intake

- research_id: `B-20261031-18H-T013-RNG-CONTEXT-CARRY-NONUSE-01`
- owner: B
- tasks: T013 (Unit candidate lists / target-selection prerequisites)
- observed_at: 2026-10-31 18H JST
- source_relative_path: `data/T013_RNG_CONTEXT_CARRY_NO_DIRECT_CMP_NATIVE_20261031_18H.md`
- source_sha256: `6eacb969ddec6e7f40408a342d17fd32a9401b9664c21f8a7071c05db70298f3` (2026-11-02 JST authorized PC original Markdown SHA256/byte-length verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no new executable hash during intake)
- evidence_va_call_offsets: `0x5A3E55/0x5A3E78;0x577D82/0x577DC4/0x577DC8/0x577DCB;0x577ADE/0x577B20/0x577B24/0x577B27;0x579FF6/0x57A094/0x57A14A;0x57A890→0x5A3EA0;record+0x28`
- prior_ids_and_corrections: B-20261031-15H-T013-KIND8-RANDOM-PAYLOAD-QUEUE-01 (record+0x28 writer), 16H B-20261031-16H-T013-BUCKET-LIST-MERGE-COMPARATOR-01 (callback), 17H input-drain/merge (not recounted)
- evidence_kind: historical source STATIC original ASM / V9 CALL and INFERRED, VERIFY for interpretation; original game DYNAMIC=0
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / no E MASTER formal update
- intake_status: PUBLISHED_INTAKE on exact GitHub readback; NOT_CURATED until independent KB review

## Reusable historical evidence

The historical native source follows a separately generated random/context field `record+0x28` from `0x5A3E55→0x5B6EAB` and `0x5A3E78` into both kind8 (`0x577DC4/0x577DC8`) and non-kind8 (`0x577B20/0x577B24`) wrapper records before `0x579EB0`. Three bucket-merge caller sites `0x579FF6`, `0x57A094`, `0x57A14A` copy the same stack-carried `+0x28` context to another temporary record before `0x57A830` merges. Although `0x57A890→0x5A3EA0` is the comparison callback, its original native body is NOT shown to compare `record+0x28` directly: observed score predicates refer to other candidate fields, including `+0xA14`. Thus "RNG context is propagated" is supported as STATIC while "this integer directly determines final priority" is NOT. Actual order, RNG consumption and end result VERIFY.

## Provenance and next verification

Cross-check 19H candidate+0xA14 RNG writer against 18H record+0x28, all legal comparator operands and native ABI; do not conflate two random-related values. This owner-created sanitized summary references the real B source by relative path and measured SHA. It does not constitute new full decompilation, original-game execution, G4 external battle-result settlement or verified final target. Dedicated curator alone may interpret REF/typed dictionary/develop based on independent native/DAT and errata audit; original game files, large index, private paths and refused payloads are excluded.
