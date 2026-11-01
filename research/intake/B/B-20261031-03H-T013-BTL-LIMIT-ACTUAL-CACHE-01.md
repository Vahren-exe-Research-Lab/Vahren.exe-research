# B-20261031-03H-T013-BTL-LIMIT-ACTUAL-CACHE-01 — B T013 historical source recovery

- research_id: `B-20261031-03H-T013-BTL-LIMIT-ACTUAL-CACHE-01`
- owner: B
- tasks: T013 (T024 AI cross-reference only)
- observed_at: 2026-10-31 03H JST
- source_relative_path: `data/T013_BTL_LIMIT_EFFECTIVE_DAT_AND_GETTER_CACHE_NATIVE_20261031_03H.md`
- source_sha256: `7955fa4e9d75300bfa7c89f5c87265975c55113586586ec73acaeab4e8436e57` (authorized-PC original report UTF-8 SHA256 and byte length remeasured on 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE source; no fresh PE hash in this intake)
- evidence_va_call_offsets: `0x46F4C0,0x46F5CE/D2/DA,0x46F60B,0x46F66F/675,0x46F6A2/A4/C9,0x449549..0x4495B7;source normalized a_default/script/context.dat btl_limit=1300,btl_limit_c=1500`
- prior_ids_and_corrections: B-20261031-02H-T013-SPECIAL-LIMIT-CATEGORY-CLOCK-01 caller and K/T threshold, generic getter insert-if-absent known in T009
- evidence_kind: historical original native STATIC and DAT where expressly stated; INFERRED/VERIFY for live result
- golden_status: original Gameplay PASS0, strict MATCH0, dynamic original observation0
- ready_status: new formal READY0, E MASTER update0
- intake_status: PUBLISHED_INTAKE upon exact GitHub readback; NOT_CURATED

## Original source findings and limitations

Original owner source verified `context.dat` in the **normalized source snapshot**, recording `btl_limit=1300` and `btl_limit_c=1500`; these are not fallback500. Historic original PE getter `0x46F4C0` returns a cached value on `0x46F5DA` hit, else resolves a property and caches its value; an absent property takes caller fallback500, while **present integer zero remains zero**. For the 02H finite threshold `T=trunc(0.5+0.2*L)`, normalized actual property candidates yield T=260 for btl_limit and T=300 for btl_limit_c; 500 fallback would yield T=100. Group flag chooses key and hence corresponding threshold, conditional category 1/7→6/7 handling as described in 02H. Cache invalidation timing, group-specific key identity and true in-game inheritance/use of normalized DAT remain VERIFY; do not equate a sourced DAT literal with a runtime Golden result.

## Lightweight reproduction and next validation

Validate actual allowed pre-modification DAT SHA, property resolution/cache under original game and group flags before treating T260/T300 as observed action. Dedicated KB curator must cross-check the permitted V9 native CALL/ASM, original DAT SHA, owner ID/errata and meaning duplicates before adding any formally reviewed REF/struct/symbol to develop. The B owner did not run original game or re-decompile every function; original EXE/DAT/MAP/SAVE, large generated DB, private identities and earlier refused material have not been uploaded.
