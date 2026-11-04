# B-20261029-1410-T013-TRIG1000-OUTPUT-ALIAS-NATIVE-01 — historical B/T013 source intake

- research_id: `B-20261029-1410-T013-TRIG1000-OUTPUT-ALIAS-NATIVE-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_TRIG1000_OUTPUT_ALIAS_NATIVE_20261029_14H.md`
- source_sha256: `6d6e4f8bdc0e5721b0e9ec1994d9010aee0956e34eb26eabfaa08910011d4d82` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `0x57DB38/3E/4E/52/5C/60→0x5E743A/65/6E/72/75→0x420900;0x420901/907/90F cos/914/918/91E,0x420923/929 sin/92E/932/938/93D;0x420927/93F output ESI and ESI+4;0x57DB7A/7E/81/83/91..0x57DB99 upstream CALL only`
- prior_ids_and_corrections: 11H four-sector,12H angle ABI,13H distance condition, old 2026-10-21 cos/-sin helper recognized (not new)
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

Historical PE-native local caller reads constant double 1000.0 and builds angle via `0x57DB60→0x5E743A` plus stored π. It passes the prior coordinate-output array address in ESI to helper `0x420900`, which **overwrites both integer output slots** at `[ESI]` and `[ESI+4]`; do not interpret it as return-EAX-only. Helper computes `φ=θ+stored π/2`, `Δx=CRT_integer(1000*cosφ+0.5)`, `Δy=-CRT_integer(1000*sinφ+0.5)` with x87/C++ CRT conversion still VERIFY for exceptional values. The caller then adds these Δ to the current coordinate pair and passes them downstream, whereas the skipped correction branch passes previously written pair unchanged. This makes a branch-dependent local output alias/writer difference, NOT proof of actual movement, final target, or downstream effects; blocked callee interior is excluded.

## Next validation and excluded evidence

Audit permitted helper math/caller V9 bytes and original game geometry comparison, but keep prohibited callee details out of this report. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
