# B-OFFLINE-20261022-2016-T012-T013-MISSILE-COLLISION-VCALL-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-2016-T012-T013-MISSILE-COLLISION-VCALL-01`
- owner/tasks: B / T012, T013
- source_relative_path: `data/B_T012_T013_MISSILE_COLLISION_ROUTE_OFFLINE_20261022_2016.md`
- source_sha256: `be39f825a743ed6223b79c6caa92eb00fa8e7ddd8728343168aea4f9c29d6a0d` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 10194
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 ver0.67｜新B T012/T013 ミサイル接触候補探索と双方向仮想CALL
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X515470`, `0X4E6D10`, `0X00515470`, `0X515471`, `0X515477`, `0X515480`, `0X515484`, `0X515489`, `0X004E6D10`, `0X4E70BC`, `0X4E70CB`, `0X5D1B80`, `0X0054BA00`, `0X54C97D`, `0X54C990`, `0X54C99A`, `0X00552030`, `0X55268A`, `0X55269D`, `0X5526A8`, `0X54BA00`, `0X552030`, `0X0063A544`, `0X0054DB60`, `0X580280`, `0X4E1550`, `0X0063A5A4`, `0X00552E60`, `0X547FC0`, `0X54DB81`, `0X54DB87`, `0X552E7F`, `0X552E85`, `0X599BD0`, `0X46FCE0`, `0X54DBCD`, `0X54DC22`, `0X54DC63`, `0X54DC7F`, `0X552ECD`, `0X65CD54`, `0X54DB60`, `0X552E60`, `0X514D60`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261022-1813-T011-T012-MISSILE-VTABLE-SLOT38-01`, `B-OFFLINE-20261022-1912-T012-RENDER-ORDER-ROUTE-01`
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L28 ## 2. 新規増分A：ミサイルの接触候補探索 `0x515470 → 0x4E6D10`
- L30 - **`0x00515470`**：ASM `0x515471` で `this+0xB0` をたどり、`0x515477` の `[skill-like+0x134] == 0` なら `0x515480 xor eax,eax` で候補なし。非ゼロなら `0x515484 add edx,0x68` で管理コンテナ相当への参照を作成し、**`0x515489 → CALL 0x004E6D10`**。
- L31 - **`0x004E6D10`**：保存擬似Cに、`param_2+4` にあるtree/sentinel候補を順番に走査し、候補の `+0x40/+0x44/+0x48/+0x4C` 相当の矩形範囲と入力候補範囲を比較する処理が存在する。条件はおおむね `leftA < rightB && leftB < rightA && topA < bottomB && topB < bottomA` の**厳密不等号の四辺AABB重なり判定**（擬似C）。
- L32 - 先に重なる候補を見つけたとき **`0x4E70BC mov eax,esi` → return**。末尾到達で**`0x4E70CB xor eax,eax` → return 0**。調査した経路には「全候補から最短距離を選ぶ」ロジックはなく、**走査順で最初の適格な重複候補を返す局所仕様**と整理できる。これはT013の**全スキル共通の最終攻撃対象選択**ではない。
- L33 - 候補間の `+0x130` 系一致によるスキップ等が存在するが、何を同一視するかはABI/型のVERIFY。
- L34 - 入力側スキル候補の `+0x3B1` が有効だと、矩形比・`+0x4A/+0x2B9` の分岐により最大100個の細分化矩形を使う場合がある。この分岐で **`0x5D1B80` の直接CALL**が4箇所存在し、RNG消費順の再現が要る可能性（RNG意味論は未確定）。単一矩形判定と**結果/負荷/RNGが異なる可能性**を今後のGolden条件に分離。
- L36 ## 3. 新規増分B：命中候補に対して双方の仮想関数 `+0x54` を順に呼ぶ
- L38 確認した**2つの上位実行経路**：
- L40 | 上位関数 | 候補探索CALL | 候補側 `+0x54` CALL | 発射元側 `+0x54` CALL |
- L41 |---|---|---|---|
- L42 | `0x0054BA00`（Missile系） | `0x54C97D → 0x515470` | `0x54C990 call eax` | `0x54C99A call eax` |
- L43 | `0x00552030`（SimpleMissile系） | `0x55268A → 0x515470` | `0x55269D call eax` | `0x5526A8 call eax` |
- L45 各CALLの直前に `mov eax,[edx+0x54]` が存在する。つまり、適格な接触候補があれば、**候補オブジェクト側の関数を先に、発射元側の関数を後に**呼ぶ。候補側のvtableは実行時オブジェクトに依存し、必ずMissileとは限らない。双方が何を変更するか、同じ対象か、HP反映があるかはDYNAMIC/Golden未実施。
- L47 候補探索には、発射元 `+0xF8`、技能の `+0x134`、周期 `+0x1C4`、オブジェクトの非ゼロ寸法等の前提分岐がある。`0x54BA00` と `0x552030` の前提は完全同一とは限らず、単純共通化は危険。双方CALL後に発射元 `+0xF8` を再評価する分岐を持つ。
- L49 ## 4. 新規増分C：Missile/SimpleMissileの接触後の副作用の違い
- L51 両クラスのvtableは18時台に既に登録先のみ確認済み：
- L53 | vtable | `[vtable+0x54]` | 今回解析した副作用 |
- L54 |---|---|---|
- L55 | Missile `0x0063A544` | `0x0054DB60` | 符号付き優先数値ゲート後にSkill `+0x178` または全体フラグで `0x580280` を起動、それ以外は `"MissileFlash"` を用いて `0x4E1550` へ接続。許可経路は発射元 `+0xF8=1`。 |
- L56 | SimpleMissile `0x0063A5A4` | `0x00552E60` | 同じ形式の符号付き優先数値ゲート後、Skill `+0x178` 非ゼロで `0x547FC0` 起動。フラグ0でもゲート通過なら `+0xF8=1`。この関数単体に `0x580280`/`0x4E1550` CALLはない。 |
- L58 優先値の取得は **`[[source+0xB0]+0x1C8] <= [[counterpart+0x80]+0x1C8]`** と復元できる。ASM `0x54DB81 cmp`/`0x54DB87 jg` と `0x552E7F cmp`/`0x552E85 jg` で**符号付きのゲート**が確認できる。`0x599BD0`で同じ「大きいSkillレコードの+0x1C8」を数値として設定し、`0x46FCE0`でコピーすることも旧DB擬似Cに記録。ここでのSkill-like `+0x1C8`をUnit構造体の同名オフセットと取り違えないこと。
- L60 Missileの内部：`0x54DBCD` および `0x54DC22` から **`0x580280`**（既知関数）へのCALLを実バイト照合。`0x54DC63`は原作内文字列 `MissileFlash` のアドレスをPUSH、`0x54DC7F` は **`0x4E1550`** をCALL。SimpleMissileでは `0x552ECD` から **`0x547FC0`** をCALL。新規内容は既存 `0x580280` 自体の再解析ではなく、**衝突候補からの双方向配送、各クラスのゲートと副作用差分**。
- L62 **注意：**`+0xF8=1`は候補処理のフラグ更新というSTATICのみ。消滅・貫通・ダメージ確定等のゲーム上の意味をまだ付さない。`0x1C8`のDATプロパティ名、`0x178`の正式意味、`DAT_0065CD54`の設定条件、実際のHP/MP減算位置、間接CALLの全型はVERIFY。
- L64 ## 5. 合成分岐検証・範囲限定
- L66 2型 × 優先値ゲート成否 × `+0x178` 0/非0 × `DAT_0065CD54` 0/非0 の**16条件**で分岐表を作成し整合性検算。具体的結果と操作は証拠JSON参照。**16条件は合成モデルの組合せ**であり、原作実機で観測した16個の事実ではない。描画順（前回19時台研究）と接触候補列挙順は独立。未確認の関数戻り型と副作用に対して「最終敵ターゲット」「攻撃命中」「貫通」等の確定名称をつけない。
- L68 ## 6. 既存成果との重複・権限
- L72 書込先はB独立`data`成果のみ。原作EXE・DAT・SAVE・他lane・MASTER・Git・スケジュールの変更なし。README/search.sqlite/検索元ZIPの改変なし。Libraryへの保存と読み戻し状態は実際の操作結果に基づいて報告（PC未同期を継続）。
- L74 ## 7. Golden要件と次の検索先
- L76 **必要な原作観測**：Missile/SimpleMissileを分け、① `Skill+0x134` 0/非0、② `source+0xF8` 0/非0、③ 重なりなし・辺接触のみ・2候補同時重複、④ `Skill+0x1C8` の大小・同値・負値、⑤ `Skill+0x178` 0/非0、⑥ 全体フラグ `0x65CD54`、⑦ `+0x3B1/+0x4A/+0x2B9`とRNG消費、⑧ コールバック順、候補順、弾/表示生成数、ID、HP/MP、状態遷移を同一EXE・DAT・SAVE・MAP・入力で採取する。原作実測なし：Golden PASS=0、strict MATCH=0。
- L78 **次回P0**：`0x515470` caller全体と `0x4E6D10` 候補treeの生成/並び順を把握して候補返却の決定性を検証。`0x54DB60`→`0x580280`へ渡す生成元と `0x552E60`→`0x547FC0`のHP/状態影響を遡る。T013の全スキル最終対象選択`0x514D60`等とは統合せず比較。T024/T028の未解明P0は維持する。
- L80 **判定**：`OFFLINE-UNSYNCED / STATIC-ASM / INFERRED / VERIFY / NOT READY`、正式B READY=0、E統合=0、原作Golden PASS=0、strict MATCH=0。PC正本の最新checkpoint・担当所有・重複・READY・拒否回収はPC復帰時に一度だけ確認する。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
