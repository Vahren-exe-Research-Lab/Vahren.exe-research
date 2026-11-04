# B-20261031-00H-T013-CATEGORY-WEIGHT-RNG-INLINE-HELPER-01 — B T013 historical source recovery

- research_id: `B-20261031-00H-T013-CATEGORY-WEIGHT-RNG-INLINE-HELPER-01`
- owner: B
- tasks: T013 (T024 AI cross-reference only)
- observed_at: 2026-10-31 00H JST
- source_relative_path: `data/T013_CATEGORY_WEIGHT_RNG_INLINE_HELPER_NATIVE_20261031_00H.md`
- source_sha256: `419771cb57f66152d8bd7af92e69f0a40cddfef59f473f6290032d9499102caa` (authorized-PC original report UTF-8 SHA256 and byte length remeasured on 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE source; no fresh PE hash in this intake)
- evidence_va_call_offsets: `0x44CB29/2F/33/60/92,0x449688/68E/692/69F/6A7,0x63B1E8(0.6)/0x63B248(0.3)/0x63B0C8(0.8),0x5D1B80,0x5B6EAB,0x40ED80,0x4496C4→0x577220,Unit+0x1E4FC/+0x1E4F8`
- prior_ids_and_corrections: Earlier 23H and older Unit eligibility gate, RNG helper and Unit field writer; 01H refines x87 0.5 initialization/rounding
- evidence_kind: historical original native STATIC and DAT where expressly stated; INFERRED/VERIFY for live result
- golden_status: original Gameplay PASS0, strict MATCH0, dynamic original observation0
- ready_status: new formal READY0, E MASTER update0
- intake_status: PUBLISHED_INTAKE upon exact GitHub readback; NOT_CURATED

## Original source findings and limitations

Historical original-PE x86 source demonstrates identical category-dependent additive weights in two different writers: raw base integer 200 multiplied by 0.6 for category 0, 0.3 for category 6, or 0.8 for other categories (120/60/160) and added to existing x87 accumulator. Entry requires Unit status bytes `+0x1867C/+0x1867E` zero and signed nonnegative `+0xC0/+0xC8/+0xD0`. One path computes a randomized sample **inline** through `0x5D1B80` and `0x5B6EAB`; another calls common helper `0x40ED80` after `0x4496AF`. Both resemble `1+Convert(RNG()/32768*(Convert(score)-1))` for ordinary finite nonnegative values, not guaranteed identical for FPU exceptional states. The `0x4496C4→0x577220` call carries a label pointer in EDX and sample integer in EBX, writes a label candidate at Unit+0x1E4FC and a max-like wait to +0x1E4F8. Category names and effect on real AI not established.

## Lightweight reproduction and next validation

Compare the two native arithmetic sequences, 01H conversion boundaries and permitted DAT categories, then legal original-game timing; don't promote RNG sampling to action success. Dedicated KB curator must cross-check the permitted V9 native CALL/ASM, original DAT SHA, owner ID/errata and meaning duplicates before adding any formally reviewed REF/struct/symbol to develop. The B owner did not run original game or re-decompile every function; original EXE/DAT/MAP/SAVE, large generated DB, private identities and earlier refused material have not been uploaded.
