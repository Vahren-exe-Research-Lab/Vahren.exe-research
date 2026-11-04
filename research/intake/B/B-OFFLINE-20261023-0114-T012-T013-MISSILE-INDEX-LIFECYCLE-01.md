# B-OFFLINE-20261023-0114-T012-T013-MISSILE-INDEX-LIFECYCLE-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261023-0114-T012-T013-MISSILE-INDEX-LIFECYCLE-01`
- owner/tasks: B / T012, T013
- source_relative_path: `data/B_T012_T013_MISSILE_INDEX_LIFECYCLE_OFFLINE_20261023_0114.md`
- source_sha256: `6bae6a270892b6ec487f34f354d53e0259ff4d0bbc7580cf40c187cd3981be67` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 7840
- original research date: 20261023; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜2026-10-23 01時台・T012/T013 ミサイル登録と二段階清掃の静的解析
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X552030`, `0X5158E0`, `0X581FA6`, `0X581FB0`, `0X40E528`, `0X581F80`, `0X581F86`, `0X581F93`, `0X581F96`, `0X581FA0`, `0X565780`, `0X581F8D`, `0X549E87`, `0X549EB7`, `0X515905`, `0X515990`, `0X51599B`, `0X55203F`, `0X55204E`, `0X552071`, `0X579AA0`, `0X552086`, `0X510850`, `0X55208B`, `0X552091`, `0X552092`, `0X40E700`, `0X552097`, `0X40E2F0`, `0X40E220`, `0X40E27F`, `0X40E4FF`, `0X40E526`, `0X40E53D`, `0X40E5F1`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261023-0009-T012-T013-COLLISION-CLEANUP-OWNER-01`
- evidence_kind: STATIC source (historical saved Ghidra/REA); INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L7 ## 先行回収と証拠源
- L9 - **既存未同期記録**: `B-RECOVERY-20261020-1113-UNSYNCED-INDEX-01`を読み、2026-10-23 00時台の研究 `B-OFFLINE-20261023-0009-T012-T013-COLLISION-CLEANUP-OWNER-01` との境界を確認。00時台の清掃CALL 6箇所、接触tree参照、0x552030直接清掃は**既存成果**で再加算しない。
- L10 - **静的入力**: Libraryの `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC PASS）、読み取り専用の同梱 `search.sqlite`（SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、quick_check ok）、原作 `Vahren.exe`（SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）。ローカル正本・原本の変更なし。Zip収録MASTERは旧スナップショット。
- L11 - **出典と重複**: ZIP内 `research_snapshot/evidence/LANE_B_HANDOFF.md`/`research_snapshot/data/T012_BATTLE_CALC.md`/旧MASTERと会話内00時台研究を参照し、今回の `0x5158E0`・`0x581FA6/0x581FB0`・`0x40E528` の結合は未登録の独立増分と判定。ただし最新PC正本との意味的重複はVERIFY。
- L13 ## 新たに解明した増分：登録→即時index清掃→遅延清掃キュー
- L15 ### 1) `Skill+0x1FD != 0` ならMissileポインタを所有者側treeへ登録
- L17 原作ASM（EXE VA）：`0x581F80`で生成物`EBP+0x80`のSkill候補を取得し、`0x581F86`でSkill `+0x1FD`を検査。非0経路では `0x581F93`が `EBP+0x78`（owner）を取得、`0x581F96`が `owner+0x1D4` を間接参照、`0x581FA0`で`+0x68`を加算する。
- L19 続いて `0x581FA6 → 0x565780` で20byte treeノード候補を確保・初期化し、`0x581FB0 → 0x5158E0` でtreeへ挿入する。`0x581F8D`により格納された生成物ポインタEBPがキーとして渡る経路。さらに **別creator** `0x549E87`～`0x549EB7`でも同じSkillゲート・tree登録方式を確認。
- L21 `0x5158E0`では `Node+0x0C`を**符号なし整数**として比較（`0x515905 setb`）、既存の同じキーがある場合は新規ノードを解放 (`0x515990`)し、新規挿入フラグを0 (`0x51599B`) にする。**ユニークキーtree**という静的結論を支持。ただしポインタ再利用・別オーナー間の挙動はVERIFY。
- L23 ### 2) SimpleMissileの終了側は、treeを先に消し、別コンテナに後処理を登録
- L25 `0x55203F`：SimpleMissile候補 `+0xF8 != 0` の経路。`0x55204E`でSkill `+0x1FD != 0`なら `owner->0x1D4+0x68` へ `0x552071 → 0x579AA0`（ポインタキーからiterator範囲）、`0x552086 → 0x510850`（範囲消去）を行う。
- L27 **追加新発見**：Skillフラグの真偽と独立してこの分岐を通ると、`0x55208B`で`Missile+0xA8`の管理ポインタを取り、`0x552091 push EBP`後、`0x552092 → 0x40E700`をCALL、`0x552097`で`Missile+0x6C=0`に設定して戻る。
- L29 `0x40E700`は管理オブジェクト `+0x278/+0x27C/+0x280` をbegin/end/capacityとして扱い、渡された**Missileポインタをvector末尾へpush**する関数で、**ここでオブジェクトをfreeしない**。00時台資料で「vector管理CALL」とだけ呼んだ箇所の実作用を今回具体化した。
- L31 ### 3) キュー側の参照も見つかった：`0x40E2F0`の処理
- L33 `0x40E220`の`0x40E27F → 0x40E2F0`から到達するフレーム処理候補では、管理オブジェクトの`+0x278/+0x27C`を走査し（`0x40E4FF`）、各4-byteキー（`0x40E526 mov eax,ebx`）で `0x40E528 → 0x579AA0` を呼ぶ。検索するtreeは **同じ管理オブジェクトの`+0x248`**。そして `0x40E53D → 0x510850` で該当キー範囲を削除する。
- L35 処理後、`0x40E5F1`で`end`を`begin`に戻す経路があり、保留キューは論理的に空になる。したがって、SimpleMissileの終了経路は **owner側treeの即時清掃** と **別のmanager側treeの遅延削除要求キュー** の2段構成を強く支持する。ただし`Missile+0xA8`と `0x40E2F0` の実行時manager実体が同一であるかは**VERIFY**（creatorのGhidra擬似Cでは `Missile+0xA8 = &DAT_008B8C90` と復元）。
- L37 ## 意味付けの限界と再現上の注意
- L38 - `+0xF8`は「終了側に入るゲート」と表現し、死亡・命中確定・freeと断定しない。`+0x6C=0`のゲーム内意味も未確定。
- L39 - `0x40E700`はvectorへの**追加**であって解放ではない。`0x510850`はtreeノード削除であり、Missile本体解放とは同一視しない。即時削除と遅延削除の対象treeも混同しない。
- L40 - 生成後のtree登録は`+0x1FD`が有効な経路で行われる。各呼出しの条件が成立すること、重複INSERTの意味、global manager同期、entry/exit全てを静的に確定したわけではない。
- L41 - 旧B成果の`offset_on=on`/`offset=on`がSkill `+0x1FD`に作用する点とは**関連**するが、以前のDAT意味論や接触矩形選択を今回の新成果として二重計上しない。
- L43 ## 機械的検証
- L45 - 原作EXEは指定SHA256と一致、ZIP CRC PASS、SQLite quick_check OK。
- L46 - E8 rel32のEXE CALLとSQLite `calls`索引との一致：**10/10**。
- L47 - 対象ASM opcode一致：**19/19**。
- L48 - 擬似CソースDB内 `code_sha256` と実本文の一致：**11/11**。
- L49 - 初回調査の原作実機Golden PASS **0**、strict MATCH **0**。STATIC検索・ASM照合PASSをGameplay PASSへ転用しない。
- L51 ## Golden必要条件・未解明P0・再開点
- L53 原作ver0.67 SHAが一致した無改変EXE、無改変DAT・MAP・SAVE、同一戦闘位置、入力列・RNG状態・tick進行を揃える。Skill `offset_on`系フラグON/OFF、複数ミサイルの同一tick終了、ポインタ再利用、登録→即時tree消去→遅延vector投入→フレーム終了でのtree消去、ownerとglobal manager実体をログで別々に観測する。HP/MP/状態・命中・RNG順序は別測定。
- L55 優先検索先：`0x40E220`へ到達する更新ループとmanager実体同定、`0x40E2F0`のtree `+0x248` のINSERT producer、`0x5158E0`の他caller/未検証別creator、`0x552030`の`+0xF8`を設定する全経路。次点にT013最終対象選択、T012 HP反映、T024 AI、T028士気・敗走。**最新正本確認・非重複・READY認定・E統合は保留。**

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
