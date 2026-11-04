# B-OFFLINE-20261024-18H-T012-PRESENCE-TAIL-CFG-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261024-18H-T012-PRESENCE-TAIL-CFG-01`
- owner/tasks: B / T012
- source_relative_path: `data/B_T012_PRESENCE_TAIL_CFG_OFFLINE_20261024_18H.md`
- source_sha256: `21ffaf19539c25263e7cebde546983324aa303c2ada62a1aba24cb911f246bc4` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 4112
- original research date: 20261024; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T012 属性存在判定の肯定分岐と関数範囲監査（2026-10-24 18時台）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X004644C3`, `0X004645A0`, `0X004645B5`, `0X004645B7`, `0X004644BC`
- prior_ids / possible errata / crossrefs: not separately enumerated; consult original
- evidence_kind: STATIC source (historical saved Ghidra/REA); INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L34 ## 重複・互換性・次P0
- L36 2026-10-21オフラインスナップショットのB HANDOFF/T012/Master、および17時台MD/JSONに`0x004644C3`・`0x004645A0`・`0x004645B5`・`0x004645B7`の完全一致記録なし。PC最新正本での意味重複・owner・READY照合は未実施。存在チェックがtrueとなる経路を単に「属性キーあり」へ短絡する前に、二段階キー、親探索、最初の対象ノード、null/sentinel、探索50回上限を照合する。
- L38 次は`0x004644BC`前後の検索結果のnil判定と`0x004645A0`への到達条件を同じフィールド形式でまとめ、Ghidra関数ボディの範囲を検証する。合法DATにおける親・子・欠損・明示0、階層境界の**到達条件はVERIFY**。Goldenには原作無改造PE・原DAT・同一SAVE/MAP/seed/inputを使用し、Skill+0x288、ダメージ・HP・状態・次tickの実測比較を必要とする。
- L40 **原作Gameplay Golden PASS 0 / strict MATCH 0 / B新規正式READY 0 / MASTER統合 0 / Task DONE増分 0**。静的確認を動的実証へ格上げしない。PC B HANDOFF未同期。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
