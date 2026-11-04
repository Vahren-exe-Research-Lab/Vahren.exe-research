# B-20261027-16H-T011-SUMMON-CALLER-SOURCE-TRIAD-01 — three source branches vs optional ECX
research_id: B-20261027-16H-T011-SUMMON-CALLER-SOURCE-TRIAD-01
owner: B; tasks: T011 / T013 cross-reference
original_observed_at: 2026-10-27 16H JST; source_sha_verified_at: 2026-11-02 JST (authorized PC actual SHA256)
source_relative_path: data/T011_SUMMON_CALLER_SOURCE_TRIAD_SENTINEL_NATIVE_20261027_16H.md
source_sha256: A6D51795E5416FF4E624258445E6EB89BF69352B42ADAA3BAC9013A3A2924753
original_PE_relative_path: rea_lab/targets/hakushin067_Vahren.exe
original_PE_sha256_observed_this_run: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
evidence_kind: owner historical STATIC_PE_ASM / STATIC_GHIDRA plus INFERRED/VERIFY
golden_status: original gameplay PASS 0; strict MATCH 0; DYNAMIC 0
ready_status: NOT_READY; some meaning already summarized in develop REF_UNIT_EXP_SUMMON §3; underlying owner proof needed
prior_ids: B-20261027-1514-T011-SUMMON-CALLER-GROUP-PROVENANCE-01
supersedes_or_errata: refines 15H four-caller map with actual guarded source branches; does not replace it

## Reusable evidence (source 1-based lines 4–10)
- At 0x5501DC candidate [ESI+0x1D8], then flags 0x5501E2 (+0x65) and 0x5501E8 (+0x6D) select EBX from one of [ESI+0x1D8], ESI+8, [ESI+0x80]. Gated 0x550219 E8→0x54E7B0 receives this source S. Do not collapse all three into a single intrinsic parent ID.
- At 0x54DF4B caller, Skill+0x40==4, source [ESI+0x78] and branch involving source+0x1D4+0x24 / global 0x65BD68 and Skill+0x74 apply; source type still provisional.
- At 0x57F484 / 0x57F492, both push same EBP source. Sentinel compare 0x57F477 to 0x80000008 branches between ECX=NULL and ECX=&[ESP+0x20]; it changes optional ECX, *not* the source S argument. The interpretation 'coordinate-like' is INFERRED.
- Old original PE E8 rel32 4/4 links and old Ghidra inspection described in source line 9; current V9 0x54E7B0 lists 4 native E8 callers, no original-game dynamic observation.

## Boundaries/next
- S, child Unit, effect+0x7C, holder H, optional Group, and caller ECX must remain separately typed in a G4 candidate receipt. Parent relationship, true EXP refund receiver, path-specific life cycle, original Unit appearance and settlement are VERIFY.
- Source details complement already curated summary in develop REF_UNIT_EXP_SUMMON §3. Original source manuscript is kept here for recovery, not counted as new finding or upgraded READY.
- Legal repro: compare original source lines and read-only `python -B knowledge/tools/v9_coverage.py --root . --inspect 0x54E7B0`; use same-run original-game input/RNG only with separately approved capture.
