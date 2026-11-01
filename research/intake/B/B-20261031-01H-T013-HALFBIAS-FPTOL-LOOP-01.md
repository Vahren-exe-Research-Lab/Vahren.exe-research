# B-20261031-01H-T013-HALFBIAS-FPTOL-LOOP-01 — B T013 historical source recovery

- research_id: `B-20261031-01H-T013-HALFBIAS-FPTOL-LOOP-01`
- owner: B
- tasks: T013 (T024 AI cross-reference only)
- observed_at: 2026-10-31 01H JST
- source_relative_path: `data/T013_HALF_BIAS_FPTOL_RNG_LOOP_NATIVE_20261031_01H.md`
- source_sha256: `990a703dfc830f1db16b98ee0a3536044a46c583576af503ae6d9f1b36d9f571` (authorized-PC original report UTF-8 SHA256 and byte length remeasured on 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE source; no fresh PE hash in this intake)
- evidence_va_call_offsets: `0x44951C/0x4496C9/0x44C9D0/0x44CBE6,0x63B050=0.5,0x5D1B80..0x5D1BD9,0x5B6EAB..0x5B6EC6,0x4496AF,0x4496B9→0x40ED80,Unit+0x1E4F8`
- prior_ids_and_corrections: B-20261031-00H-T013-CATEGORY-WEIGHT-RNG-INLINE-HELPER-01 (coefficients and helper), earlier RNG implementation known
- evidence_kind: historical original native STATIC and DAT where expressly stated; INFERRED/VERIFY for live result
- golden_status: original Gameplay PASS0, strict MATCH0, dynamic original observation0
- ready_status: new formal READY0, E MASTER update0
- intake_status: PUBLISHED_INTAKE upon exact GitHub readback; NOT_CURATED

## Original source findings and limitations

The old bounded native report identifies double `0.5` at `0x63B050` loaded at category-loop starts `0x44951C/0x44C9D0` and reloaded before the next Unit after `0x4496C9/0x44CBE6`. Combined with the prior 0H multipliers on base 200, finite positive candidate upper counts can be interpreted as trunc(0.5 + 200*c), producing 120/60/160 for c=0.6/0.3/0.8. The historical RNG `0x5B6EAB` uses an LCG step then SHR16 and AND0x7FFF, returning 0..32767. Conversion helper `0x5D1B80` branches between SSE CVTTSD2SI and x87 FISTP-related adjustment depending on a global feature value; for ordinary finite positive values the net result is consistent with truncation toward zero, but exceptional control-word/overflow/NaN behavior remains VERIFY. Formula for a sample `1+trunc((RNG()/32768)*(N-1))` therefore has ordinary candidate ranges 1..119, 1..59, 1..159 rather than achieving N; these are **inferences**, not actual game observations.

## Lightweight reproduction and next validation

Verify finite-case numeric behavior under original feature flag and x87 control state; distinguish signed/negative input and RNG actual tick consumption before Golden. Dedicated KB curator must cross-check the permitted V9 native CALL/ASM, original DAT SHA, owner ID/errata and meaning duplicates before adding any formally reviewed REF/struct/symbol to develop. The B owner did not run original game or re-decompile every function; original EXE/DAT/MAP/SAVE, large generated DB, private identities and earlier refused material have not been uploaded.
