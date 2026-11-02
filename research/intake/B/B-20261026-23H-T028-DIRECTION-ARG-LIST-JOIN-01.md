# B-20261026-23H-T028-DIRECTION-ARG-LIST-JOIN-01 — 要求座標argとUnit snapshotからの方向差分・別list経路
research_id: B-20261026-23H-T028-DIRECTION-ARG-LIST-JOIN-01
owner: B
tasks: T028,T012
domain: BATTLE_AI_MORALE
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_DIRECTION_ARG_LIST_JOIN_NATIVE_20261026_23H.md
original_pc_source_sha256: 5A0ECCCA159F03F32E29E23DB68BA0018C23B0A3368677F5A961396BB673127A
sha_checked_at: 2026-11-03 JST, authorized research PC, read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR,INFERRED,VERIFY
source_address_mentions: 0x5769B0;0x579900;0x4EDFE0;0x4EC1E0;0x57A690;0x40EDB0;0x576B0D
offset_mentions_untyped: Unit+0x214;Unit+0x218;Unit+0x18688
prior_research_ids_for_crosslink_not_automatic_supersedes: none confirmed
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_BATTLE_TAKEOVER.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical owner's bounded meaning (not a new discovery)
保存済みx86原作窓に基づくowner報告では補正後pairを使う経路と方向差分に使う要求arg/Unit事前位置snapshotは異なる。座標意味と最終移動・実ゲーム時相は未確認。

## Source, limitations and independent next step
この本文は既存B担当原資料の限定的なサニタイズ要約。上記original_pc_sourceの実測SHAを照合。原作解析用PEおよび現行V9 SQLiteのSHAは今回read-onlyで一致を確認したが、**この研究IDごとの原作ASM/CALL/DATの独立再検証ではない**。STATIC・INFERREDを原作実機の確定挙動に昇格しない。資料中の先行研究IDは重複/訂正の確認候補であり、明示なきsupersedesではない。

次の合法な検証: 補正座標と要求座標が違う合法ケースで出力方角・次tickとlist処理を独立検証。

原作Golden PASS 0、strict MATCH 0、READY 0、CURATED 0。G4外部戦闘結果の反映契約は未実証。過去の安全HOLD・拒否済み内容/操作/対象・他owner研究・原本ゲーム・SAVE・バイナリは非収録。CuratorのみがdevelopのREF/辞書へ出典と訂正を選択的に採録する。
