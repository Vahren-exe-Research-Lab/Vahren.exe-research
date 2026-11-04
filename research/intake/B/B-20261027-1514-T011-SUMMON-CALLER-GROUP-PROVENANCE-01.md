# B-20261027-1514-T011-SUMMON-CALLER-GROUP-PROVENANCE-01 — caller source differs from optional Group
research_id: B-20261027-1514-T011-SUMMON-CALLER-GROUP-PROVENANCE-01
owner: B; tasks: T011 / T013 cross-reference
original_observed_at: 2026-10-27 15H JST; source_sha_verified_at: 2026-11-02 JST (authorized PC actual SHA256)
source_relative_path: data/T011_SUMMON_CALLER_GROUP_PROVENANCE_NATIVE_20261027_15H.md
source_sha256: FCC6CA977366126DEDC22D025B7FE25429DFBE83C59D9C41DEAB52A4B465B48D
original_PE_relative_path: rea_lab/targets/hakushin067_Vahren.exe
original_PE_sha256_observed_this_run: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
evidence_kind: owner historical STATIC_PE_ASM / STATIC_GHIDRA, with Group semantics INFERRED, final parent/EXP VERIFY
golden_status: original gameplay PASS 0; strict MATCH 0; DYNAMIC 0
ready_status: NOT_READY; reference-level static overview already in develop REF_UNIT_EXP_SUMMON.md §3, no new semantic admission claimed
prior_ids: B-20261027-13H-T011-UNIT-HOLDER-CTOR-SUMMON-JOIN-01; B-20261027-14H-T011-SUMMONFLASH-HOLDER-CHAIN-01
supersedes_or_errata: extends 14H source identity (S from first stack argument), not a replacement for 14H holder chain

## Native sites and provenance (source 1-based lines 5–12)
- 0x54E7F0 [EBP+8] → 0x54E7F6 stack+0x2C; 0x54ED51 / 0x54ED70 uses same S to get H=S+0xC; 0x54ED95 saves source S into SummonFlash+0x7C. Thus holder reference, source pointer, and Skill pointer are separate fields in this local path.
- Four bounded original E8 callers to 0x54E7B0: 0x54DF4B, 0x550219, 0x57F484 and 0x57F492. Current V9 inspect 0x54E7B0 identifies 4 verified native E8 caller edges (not a complete ABI proof). These caller contexts differ.
- 0x54F02F selects S+0x1D0 group for selector==1. Alternative group creation 0x54EFA3→0x567EE0 or group from a tail Unit in S+0x178..0x17C list; EDI may remain NULL. Only EDI!=0 reaches child 0x54F096 CALL0x568710; group pointer can be attached at child+0x1D0 or list-inserted.
- Original report's 0x568710 limited window starts at 0x568710, length 210B SHA256 DC2B73E5F350E9BFE02A51F36B40A1B4F696EFACE1FEEB6DF9902C6FE3C89432 (historical receipt; window SHA not re-measured this run).

## Correction/limits/next
- Do not identify S, group EDI, holder H, or child+0x1D0 as a single unique summon parent/EXP receiver. REF_UNIT_EXP_SUMMON §3 already summarizes this partition; this report preserves original site details and original source SHA.
- Native E8 edges prove bounded calls only. Whether each source is actual parent, whether group determines EXP refund target, game lifetime/roster and G4 external settlement remain VERIFY; Golden not executed.
- Authorized repro: inspect original source lines and `python -B knowledge/tools/v9_coverage.py --root . --inspect 0x54E7B0`. A live test requires unchanged original SAVE/MAP/DAT/input/RNG and explicit Unit identity snapshots, never synthetic claim of MATCH.
