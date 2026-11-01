# B-20261027-13H-T011-UNIT-HOLDER-CTOR-SUMMON-JOIN-01 — summon Unit holder writer/constructor chain
research_id: B-20261027-13H-T011-UNIT-HOLDER-CTOR-SUMMON-JOIN-01
owner: B; tasks: T011 (T013 cross-reference)
original_observed_at: 2026-10-27 13H JST; source_sha_verified_at: 2026-11-02 JST (authorized PC, SHA256 actual read)
source_relative_path: data/T011_SUMMON_UNIT_HOLDER_INHERITANCE_NATIVE_20261027_13H.md
source_sha256: 407DB54644FAE5EC086B40121D63A19DB75F86022EA70FD4114F7041DB9C52D5
original_PE_relative_path: rea_lab/targets/hakushin067_Vahren.exe
original_PE_sha256_observed_this_run: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
evidence_kind: owner historical STATIC_PE_ASM / STATIC_GHIDRA + INFERRED/VERIFY; new observation: source SHA and V9 E8 index crosscheck only
golden_status: original gameplay PASS 0; strict MATCH 0; DYNAMIC 0
ready_status: NOT_READY (owner); MASTER/curator acceptance not claimed
prior_ids: B-20261013-1134-01, B-20261013-1146-01; successive owner refinement B-20261027-14H-T011-SUMMONFLASH-HOLDER-CHAIN-01
supersedes_or_errata: none; narrows previous unknown base ctor holder behavior, does not supersede unrelated Unit ctor findings

## Reusable native evidence (1-based original report lines 4–12)
- Original PE at 0x56F712 / 0x56F716 loads constructor Unit and H arguments; 0x56F720 writes H into Unit+0xC. Caller 0x56F8BB / 0x56F8C9 / 0x56F8CF passes new Unit and H to base ctor 0x56F6F0. Current V9 inspect 0x56F6F0 reports original verified E8 caller 0x56F8CF (STATIC graph, not live behavior).
- Summon path 0x54F074 reads effect/context EBX+0xC, 0x54F078 passes H, 0x54F07A calls 0x56F880. Thus child Unit+0xC inherits the *passed holder reference* along this path; the holder's identity and H+4 alias remain VERIFY.
- Owner report's bounded original-PE window: 0x56F6F0 length 115B SHA256 7EBB3FF3F88FDF50506948DE38FD6253BC0876426A8FDFD9F1E5C32FC9E4ED5C; 0x56F8A8 length 72B SHA256 C20D6B769C9F84BE95622F0DB45DAB64DCE86CAA448E8507FCE5A5150ADB9673. These are *historically reported*, not independently rehashed this run.

## Boundaries and next validation
- EBX+0xC must not be relabeled a unique summon parent/EXP refund pointer. Other 0x56F880 callers pass different H origins. Ref: develop REF_UNIT_EXP_SUMMON.md §3 (already describes downstream holder chain; source preservation here is not a new semantic discovery).
- This report is not evidence for G4 battle-end commit, summon EXP to persistent UnitData, UI appearance, H+4=Main, or original-game Golden. Recheck original assembly at the specified sites and capture legal same-run source/effect/child holder and EXP/cleanup before promoting.
- Safe read-only reproduction: from authorized research root use `python -B knowledge/tools/v9_coverage.py --root . --inspect 0x56F6F0`; independently inspect original owner source cited lines. No EXE execution, protected-range analysis, prohibited source recovery, or modification of curated REF/dictionaries.
