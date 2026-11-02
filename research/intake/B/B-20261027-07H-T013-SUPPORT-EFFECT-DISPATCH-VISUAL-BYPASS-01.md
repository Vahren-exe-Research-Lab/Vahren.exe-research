# B-20261027-07H-T013-SUPPORT-EFFECT-DISPATCH-VISUAL-BYPASS-01 — support候補→effect dispatchの視覚登録枝とcore合流
research_id: B-20261027-07H-T013-SUPPORT-EFFECT-DISPATCH-VISUAL-BYPASS-01
owner: B
tasks: T013,T012
domain: TARGET_SELECTION
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T013_SUPPORT_EFFECT_VISUAL_BYPASS_NATIVE_20261027_07H.md
original_pc_source_sha256: F3BBE0F0C839CF12D1ED1902B750C8CA13EFB3538BA0EBD1F5BB86216A18AE3C
sha_checked_at: 2026-11-03 JST, authorized PC, read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR,INFERRED,VERIFY
source_address_mentions: 0x57FA99;0x57FE17;0x54E0B0;0x54E2BC;0x54E30D
offset_mentions_untyped: effect+0x78;effect+0x80;effect+0x85;effect+0x94
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261013-1122-01
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_SKILL_POST_ACTION.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner study: bounded reusable meaning
support単体と複数候補経路は54E0B0へCALLし、effect objectの視覚登録を通る/迂回する枝があっても後続coreに合流するというB保存報告。見た目やUI通知の有無をHP/MP/status実効果の成功とみなさない。

## Source and next independent validation
Research-PC source report path and actual SHA256 rechecked read-only in this run. Isolated ver0.67 game PE and the current unified V9 SQLite SHA256 were also rechecked for **identity only**; original ASM/CALL and DAT report assertions are not newly independently proven. Related IDs refer to possible prior meaning or correction; do not auto-count them as additional discoveries or automatic supersedes. Prior local owner READY, if any, is historical, not formal new READY or Golden proof. ABI, C++ type, gameplay target/HP/EXP/status and G4 side effects remain VERIFY.

Next authorized check: 支援候補数・視覚分岐とHealCoreの合流、合法原作の可視効果/HP/stateを区別確認。

Curator selectively verifies allowed original DAT/ASM and corrections before moving any statement to develop REF or dictionaries. Raw binary/pseudocode, denied operations/content, refused address ranges, original SAVE/ZIP, other-owner evidence and user game excluded. PUBLISHED_INTAKE ≠ CURATED. Original-game Golden PASS0, strict MATCH0, new READY0, formal CURATED0; G4 external result settlement NOT PROVEN.
