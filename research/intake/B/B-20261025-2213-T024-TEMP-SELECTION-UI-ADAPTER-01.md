# B-20261025-2213-T024-TEMP-SELECTION-UI-ADAPTER-01 — 0x528700一時選択listと0x56BA80描画gateの責務分離
research_id: B-20261025-2213-T024-TEMP-SELECTION-UI-ADAPTER-01
owner: B
tasks: T024,T013
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T024_TEMP_SELECTION_UI_ADAPTER_NATIVE_20261025_22H.md
original_pc_source_sha256: 25C25671A69083672105C58384E0A9D71D59C7E764EB71FA32FF35F1DC1691AE
sha_checked_at: 2026-11-03 JST by SHA256 read-only authorized PC file measurement
target_original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_unified_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED_UI,VERIFY
source_address_mentions: 0x528700;0x528727;0x528790;0x5287D6;0x56BA80;0x56BA89;0x56BBA6;0x56BC63
offset_mentions_untyped: owner+0x364;owner+0x368;owner+0x358;Unit+0x1F9
prior_research_ids_for_crosslink: B-20261025-21H-T024-POSTUNLINK-ZERO-TAILJMP-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Bounded historical owner finding (not a new discovery)
The earlier B native report describes `0x528700` as an adaptive temporary list adapter: it checks an owner vector span (`+0x364/+0x368`), clears a temporary intrusive list for nonempty candidates, and may create a single wrapper referring to owner `+0x358`. A separate `0x56BA80` conditional-refresh path checks UI state, branches on candidate `Unit+0x1F9`, and uses Win32 drawing calls. These support **UI presentation/selection refresh** as a bounded inference, not completed battle AI target, durable Unit roster, or postbattle result. Owner source based part of the graph on historical V3; this intake **does not endorse V3 as current authority** and requires V9/source recheck before curation.

## Evidence boundaries and curator follow-up
Crosscheck permitted function ranges in current V9 and source-exact report, confirm temporary-list ownership/lifetime and candidate producers; verify original-game visuals separately. No raw native decoding or Golden in this intake.

The source Markdown hash is measured on the authorized research PC in this run; source-reported static claims, prior x86 evidence, original normalized DAT lines and derived ABI were **not** independently revalidated merely by hashing. The isolated original PE and current unified V9 SQLite were identity-checked by SHA256 only. Original-game Golden=0, strict MATCH=0, formal READY=0, and G4 external result settlement remains unproven. Original binaries/DAT/SAVE/ZIP and blocked material are **not** included. This file is private B-owner searchable intake; only the curator may selectively and independently admit supported meaning into develop REF/dictionary.
