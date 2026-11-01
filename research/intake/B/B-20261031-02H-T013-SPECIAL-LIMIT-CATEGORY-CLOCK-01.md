# B-20261031-02H-T013-SPECIAL-LIMIT-CATEGORY-CLOCK-01 — B T013 historical source recovery

- research_id: `B-20261031-02H-T013-SPECIAL-LIMIT-CATEGORY-CLOCK-01`
- owner: B
- tasks: T013 (T024 AI cross-reference only)
- observed_at: 2026-10-31 02H JST
- source_relative_path: `data/T013_SPECIAL_BTL_LIMIT_C_CATEGORY_CLOCK_NATIVE_20261031_02H.md`
- source_sha256: `0a125bc3a4e287e4dffc2f5ba38ad2d2f43f3157dd98e41e9c3971c84598177d` (authorized-PC original report UTF-8 SHA256 and byte length remeasured on 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE source; no fresh PE hash in this intake)
- evidence_va_call_offsets: `0x449515/0x44952B..0x4495B7,0x449549,0x44955E/0x449564→0x46F4C0,0x449581→0x5D1B80,0x4495B3/B5/B7,0x4495BF..0x4495D7,group+0x1EF244,manager+0x98/+0x18,clock+0x67B938/+0x67B93C`
- prior_ids_and_corrections: Earlier 23H category6→7 rewrite and older clock sentinel; 03H checks actual DAT btl_limit values and getter cache
- evidence_kind: historical original native STATIC and DAT where expressly stated; INFERRED/VERIFY for live result
- golden_status: original Gameplay PASS0, strict MATCH0, dynamic original observation0
- ready_status: new formal READY0, E MASTER update0
- intake_status: PUBLISHED_INTAKE upon exact GitHub readback; NOT_CURATED

## Original source findings and limitations

Historical original-PE ASM finds that category 1 and 7 are subject to a special limit comparison when `manager+0x98>10`. A group flag `+0x1EF244` selects the string key `btl_limit` or `btl_limit_c` for getter `0x449564→0x46F4C0` with default integer 500. The threshold on normally finite integers is `trunc(0.5+0.2*property)`, compared with signed clock-like K derived from global start/current counters `0x67B938/3C`. At `0x4495B3/B5`, `K>=threshold` retains category1/7, `K<threshold` rewrites it to 6; a separate already-known `groupflag !=0 && manager+0x18==0` rule can rewrite 6 to 7. The historical source distinguishes sentinel/zero start-clock cases, but does not prove actual game time or AI action. Earlier `manager+0x98<=10` branch may force nonzero category to 6 before this special route.

## Lightweight reproduction and next validation

Use 03H actual unmodified DAT values instead of blindly assuming default500; compare current V9 clock/gate and legal input categories. Dedicated KB curator must cross-check the permitted V9 native CALL/ASM, original DAT SHA, owner ID/errata and meaning duplicates before adding any formally reviewed REF/struct/symbol to develop. The B owner did not run original game or re-decompile every function; original EXE/DAT/MAP/SAVE, large generated DB, private identities and earlier refused material have not been uploaded.
