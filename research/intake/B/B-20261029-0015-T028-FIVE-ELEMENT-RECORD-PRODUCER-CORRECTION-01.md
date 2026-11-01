# B-20261029-0015-T028-FIVE-ELEMENT-RECORD-PRODUCER-CORRECTION-01 — B historic T028 result/queue research

- research_id: `B-20261029-0015-T028-FIVE-ELEMENT-RECORD-PRODUCER-CORRECTION-01`
- owner: B
- tasks: T028 (result/notification candidates; T012/T013 crossreference only)
- observed_at: 2026-10-29 original owner study
- source_relative_path: `data/T028_FIVE_ELEMENT_RECORD_PRODUCER_CORRECTION_NATIVE_20261029_00H.md`
- source_sha256: `960ed4610d1a340855528a6c131ac07decbc7a44ba3525ed6a619e98edbefcdf` (authorized PC Markdown real SHA256+bytes measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous measured original target, no fresh PE rehash)
- native_evidence_va_call_offsets: `0x434B10/0x434B5A→0x415530,0x434BD0→0x429A00,0x434BF6/0x434C02/0x434C0E→0x415530,0x434B82→0x5D1779,0x48C880,0x48CC95→0x5B7576,tuple 5×0x1C`
- prior_ids_and_errata: Old B 10/28 21H/22H two-element producer interpretation CORRECTED (five elements); B 10/28 23H consumer five 28-byte records already known
- evidence_kind: historical original ASM STATIC / old V3 index supplement / INFERRED and VERIFY for ABI, gameplay
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: owner PUBLISHED_INTAKE upon matching GitHub fetch; NOT_CURATED

## Reusable owner research facts

Historical original x86 corrects older 22H description of `0x434B10` "two appended elements": its producer actually appends **FIVE consecutive 0x1C-byte string-like records** to the manager vector at `+0x1EEC74`: record0 through `0x434B5A→0x415530`, record1 (ECX converted to decimal through `0x5D1779`) via `0x434BD0→0x429A00`, records2,3,4 via `0x434BF6/0x434C02/0x434C0E→0x415530`. The resulting 0x8C-byte tuple matches the historical `0x48C880` five-element consumer; consumer index1 is converted with `_atol`, and index3 chooses between existing sink routes. Exact meaning of four text fields, 18 input callers and live display/result semantics remain VERIFY; previous two sinks are NOT new findings.

## Next verification

Cross-check 01H caller-mode matrix and 02H boundary/sink common dialog; do not infer Unit affiliation or morale from the tuple structure. Curator must validate permitted current V9 original ASM/DAT and existing corrections before any REF/symbols/develop acceptance. No original game files, large DB, private addresses, or previously refused operation content was uploaded. Static event/queue control is not proof of original game action or G4 external battle settlement.
