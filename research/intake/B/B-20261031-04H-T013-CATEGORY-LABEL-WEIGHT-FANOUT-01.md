# B-20261031-04H-T013-CATEGORY-LABEL-WEIGHT-FANOUT-01 — B T013 historical source recovery

- research_id: `B-20261031-04H-T013-CATEGORY-LABEL-WEIGHT-FANOUT-01`
- owner: B
- tasks: T013 (T024 AI cross-reference only)
- observed_at: 2026-10-31 04H JST
- source_relative_path: `data/T013_CATEGORY_LABEL_WEIGHT_VECTOR_FANOUT_NATIVE_20261031_04H.md`
- source_sha256: `04fbcbb5eda02856fd7b9c7e711c141e53e40eed2897eddd560959f256fae31c` (authorized-PC original report UTF-8 SHA256 and byte length remeasured on 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE source; no fresh PE hash in this intake)
- evidence_va_call_offsets: `0x4495E3/0x4495F0,0x449704 table,0x44968E..0x4496A7,0x44963B..0x4496E5,0x4496AF→0x5D1B80,0x4496B9→0x40ED80,0x4496C4→0x577220,manager+0x78..+0x7C`
- prior_ids_and_corrections: Earlier 23H category-to-label table and 00H weights known; this source corrects any assumption that one visible label implies one numeric weight
- evidence_kind: historical original native STATIC and DAT where expressly stated; INFERRED/VERIFY for live result
- golden_status: original Gameplay PASS0, strict MATCH0, dynamic original observation0
- ready_status: new formal READY0, E MASTER update0
- intake_status: PUBLISHED_INTAKE upon exact GitHub readback; NOT_CURATED

## Original source findings and limitations

Historical native jump table `0x449704` maps categories to visible LABEL candidates: 0→hold,1→even,2→even,3→push,4/5→hold(default),6→advance,7→even,8→back. The separate weight branch at `0x44968E..0x4496A7` assigns 0.6 only for category 0, 0.3 only for category 6, and 0.8 for all other numeric categories. Thus 0/4/5 can display the same "hold" label but receive **different numeric weight**; this is a source-level static distinction, not a claim those categories are all legal runtime cases. `0x44963B..0x4496E5` loops through the manager's Unit* vector and processes each eligible Unit (five independent validity gates); it is a conditional **fan-out**, not selecting only one Unit. Each eligible iteration samples RNG and can call `0x577220` to update a label and wait field; ineligible candidates locally skip those writes. Actual final order, events and live display remain VERIFY.

## Lightweight reproduction and next validation

Check category producers (05H mode3, other paths), vector mutation during iteration and original game action before naming an official AI choice. Dedicated KB curator must cross-check the permitted V9 native CALL/ASM, original DAT SHA, owner ID/errata and meaning duplicates before adding any formally reviewed REF/struct/symbol to develop. The B owner did not run original game or re-decompile every function; original EXE/DAT/MAP/SAVE, large generated DB, private identities and earlier refused material have not been uploaded.
