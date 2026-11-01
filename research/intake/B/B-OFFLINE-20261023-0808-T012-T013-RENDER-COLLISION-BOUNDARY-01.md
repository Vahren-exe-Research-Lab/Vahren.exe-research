# B-OFFLINE-20261023-0808-T012-T013-RENDER-COLLISION-BOUNDARY-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261023-0808-T012-T013-RENDER-COLLISION-BOUNDARY-01`
- owner/tasks: B / T012, T013
- source_relative_path: `data/B_T012_T013_RENDER_COLLISION_BOUNDARY_OFFLINE_20261023_0808.md`
- source_sha256: `c924f08fbecc70cb6facd99abc6d7d4bc540d6d7a338b173e13097a47ee7234c` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 7916
- original research date: 20261023; source_sha_verified: 2026-11-02
- title: 迫真戦記 ver0.67｜B担当 T012/T013 空間候補列挙の用途分離（2026-10-23 08:08 JST）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X00515470`, `0X004E6D10`, `0X004BC4F0`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261023-0716-T012-T013-SPATIAL-CELL-MIGRATION-01`
- evidence_kind: STATIC source (historical saved Ghidra/REA); INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L43 ## 3. 検証
- L45 独立検証用Pythonは標準ライブラリでPEヘッダとsection/RVAを読取り、実EXEから期待バイトを抽出し、`E8 rel32`の呼出先を復号。SQLiteは `mode=ro` で読む。対象5関数の擬似CをDB収録ハッシュと再照合した。
- L47 - 原作EXE SHA一致、検索DB SHA一致、SQLite quick_check `ok`。
- L48 - 24箇所のopcode anchor **24/24 PASS**。
- L49 - 直接CALLサイトの原作E8復号とSQLite索引 **6/6 PASS**。
- L50 - Ghidra擬似Cの再ハッシュ **5/5 PASS**。
- L51 - 間接vtable先の完全復元、画面描画順と実際の攻撃対象順との一致：**未検証**。
- L52 - 原作Golden PASS **0**、strict MATCH **0**、READY **0**、DONE増加 **0**。
- L60 ## 5. 次の未解明P0 / 再開点
- L62 1. **T013**：`0x00515470 → 0x004E6D10` のmanagerが保持する候補treeのノード登録元と順序を、空間セルvectorとは独立に辿る。候補の反復順（tree order / 登録順 / 早期return）をASMで検証。`0x004BC4F0`は直接の命中候補入口ではないので再調査を繰り返さない。
- L64 3. **T011**：`object+0x54` stampのreader群と `grid+0x28`マスク初期化、Skill `+0x134/+0x1FD`のwriter範囲。
- L65 4. **T024/T028**：戦闘AIの最終対象選択、士気・敗走は今回未着手のP0維持。
- L67 **Golden NOT RUN条件**：同一原作EXE/DAT/MAP/SAVE/tick/入力/RNGで、同セル複数オブジェクト、key(+4,+8)同点/相違、描画矩形と命中対象矩形を区別。旧セルswap-back後の描画バケット順と、`0x004E6D10`候補treeの反復順、実際の攻撃対象、HP/RNGを別々に記録する。フレーム描画のソートと戦闘命中を取り違えない。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
