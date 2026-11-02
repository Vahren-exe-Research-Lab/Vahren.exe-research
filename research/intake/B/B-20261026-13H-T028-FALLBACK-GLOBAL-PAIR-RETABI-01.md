# B-20261026-13H-T028-FALLBACK-GLOBAL-PAIR-RETABI-01 — fallback移動候補2系統のglobal pair returnとcaller閾値
research_id: B-20261026-13H-T028-FALLBACK-GLOBAL-PAIR-RETABI-01
owner: B
tasks: T028,T012
domain: BATTLE_AI_MORALE
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_FALLBACK_GLOBAL_PAIR_RETABI_NATIVE_20261026_13H.md
original_pc_source_sha256: 50739E6AD242100598A4A88DD0A484A6A4A9715F33D2155EF19DDCF7AD3BA0D7
sha_checked_at: 2026-11-03 JST, authorized PC, read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR,INFERRED,VERIFY
source_address_mentions: 0x4E7770;0x4E7A9A;0x4E7E68;0x579831;0x5797F0;0x57984C
offset_mentions_untyped: manager+0x3C;Unit+0x228;Unit+0x186D0;Unit+0x1E4AC
prior_research_ids_for_crosslink_not_automatic_supersedes: none confirmed
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_BATTLE_TAKEOVER.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historic B owner evidence and its limits
B既存x86報告は0x4E7770が2DWORD座標候補へのポインタまたはNULLをEAXで返し、manager modeによって別global pairを利用する。callerのthreshold/Unit状態により代替移動へ進むが再入・最終移動の保証ではない。

## Independent validation, errata and safety
Authorized-PC original report SHA256 was remeasured read-only. Authorized isolated game PE and current V9 SQLite SHA256 were remeasured and matched, **identity only**; this summary does not independently re-decode original machine instructions or establish original gameplay. Reported prior READY is historical owner-state only; new formal READY=0. Related IDs are references for dedup/supersedes review, not automatic corrections. Avoid overclaiming structure types/ABI/HP/target/result or native G4 settlement.

Next legal check: 候補pairのlifetimeとcallerの正常return、合法原作の閾値境界と次tick移動を独立確認。

Sanitized source summary only; no prior denied source/VA/payload or original EXE/DAT/SAVE content, no disallowed repeat attempt, no other owner edits. Original-game Golden PASS 0, strict MATCH 0, new formal READY 0, formal CURATED 0. Curator-only selective develop REF/dictionary promotion after allowed source inspection.
