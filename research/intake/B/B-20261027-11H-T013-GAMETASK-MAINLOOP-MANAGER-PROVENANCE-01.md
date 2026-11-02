# B-20261027-11H-T013-GAMETASK-MAINLOOP-MANAGER-PROVENANCE-01 — GameTask tick manager and Heal registration provenance (bounded STATIC)

research_id: B-20261027-11H-T013-GAMETASK-MAINLOOP-MANAGER-PROVENANCE-01
owner: B
research_tasks: T013,T012
source_observed_at: 2026-10-27 11H JST (historical owner study)
source_relative_path: data/T013_GAMETASK_MAINLOOP_MANAGER_PROVENANCE_NATIVE_20261027_11H.md
source_report_sha256: DFF856060A6C90DB61789A4B66BC9313865A6AA9DDC5DD6363CAD2F3B0873B40
source_sha256_reverified: authorized research PC, read-only whole-file SHA-256 on 2026-11-03 (matches)
isolated_original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (identity only)
current_composite_V9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE (identity only)
evidence_kind: HISTORICAL_OWNER_STATIC / INFERRED / VERIFY; not a new independent machine-code recheck
intake_stage: PUBLISHED_INTAKE after exact GitHub content readback; NOT newly CURATED
original_game_Golden_PASS_new: 0
strict_MATCH_new: 0
formal_READY_new: 0

## Searchable meaning and exact bounded sites
- Historical owner report: at 0x4B996B the Main-local EDI is derived as Main+0xC; the dispatch converges at 0x4B99DF, with E8 site 0x4B99E0 calling 0x4C24B0. Inside this tick path 0x4C2714 calls 0x4C28D0, which accesses an active list via +0x2C. These are **owner-reported static relationships**, not rerun x86 proof in this intake.
- Previously reported Heal effect production associates effect+0xC with a holder H from S+0xC, and the registration path (0x54E2DE -> 0x4C2240) derives a pending manager from [H+4]+0xC. Other cited direct sites: 0x54E11E -> 0x550980 and 0x4C2714 -> 0x4C28D0 (historical native E8 report, not fresh call validation).
- The proposed equality of registration manager and tick manager requires [ [S+0xC] +4 ] == Main in the same session. The holder's writer/alias/lifetime is **not verified**; equality of actual instances and every-frame execution are NOT established.
- Offset hints (not newly named struct layout): Main+0xC, Main+0x1EF144, active-list +0x2C, holder+0x4, effect+0xC. Do not promote ambiguous manager/Unit/ABI identities to established C++ types.

## Prior work, errata and downstream limit
- Owner report distinguishes its 0x4B9930 upper-caller mapping from earlier B Heal effect generation, vtable and pending/tick research (07H–10H); prior reports are *references*, not duplicated new discoveries or READY. Related curated entrypoints to compare: REF_BATTLE_AI_MORALE.md, REF_BATTLE_TAKEOVER.md, REF_SKILL_POST_ACTION.md and current develop symbols/structs. Exact prior B IDs remain for curator ID/SHA cross-reference, not inferred here.
- The historical source mentioned older search.sqlite and legacy V3 output; current V9 was SHA-identified but its native function boundaries/direct CALL sites were not freshly reconstructed in this run.
- No denied native body, refused original evidence, protected VA, binary, save, DAT, runtime packet, or private absolute device path has been reproduced. No earlier blocked write was retried.

## Verification and selective curator adoption
- Recheck permitted original-PE windows/calls against current V9; independently trace legal holder S+0xC writer and owner identity before asserting M_register == M_tick. Validate one unmodified native Heal case with identical SAVE/MAP/seed/input to observe pending vs active transitions, HP/MP/status and RNG. These tests are NOT RUN; Gameplay Golden PASS=0, strict MATCH=0, new READY=0.
- Curator may adopt only independent STATIC call/offset facts after checking source SHA, old B studies and errata, and allowed DAT/native evidence; do not merge the divergent owner Draft PR wholesale or declare G4 result-commit proven.
