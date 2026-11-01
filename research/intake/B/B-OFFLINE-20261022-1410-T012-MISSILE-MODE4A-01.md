# B-OFFLINE-20261022-1410-T012-MISSILE-MODE4A-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-1410-T012-MISSILE-MODE4A-01`
- owner/tasks: B / T012
- source_relative_path: `data/B_T012_MISSILE_MODE4A_2B9_OFFLINE_20261022_1410.md`
- source_sha256: `7144e6ba6a09e768ef2fc180ef49e274a0c4ba62424ad4166eee4ee11ea1f17c` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 7258
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 ver0.67｜新B T012：ミサイル生成 0x580280 の +0x4A モードと +0x2B9 幾何分岐
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X580412`, `0X58041C`, `0X580422`, `0X580428`, `0X58042E`, `0X58043D`, `0X58043F`, `0X58044C`, `0X580457`, `0X580467`, `0X58046C`, `0X5805DD`, `0X580603`, `0X5807ED`, `0X5807F7`, `0X580801`, `0X580827`, `0X580A30`, `0X582240`, `0X580A3A`, `0X580A3E`, `0X5815EA`, `0X5815F4`, `0X5815FD`, `0X581649`, `0X58164B`, `0X581663`, `0X58166B`, `0X581687`, `0X581E3F`, `0X580280`
- prior_ids / possible errata / crossrefs: not separately enumerated; consult original
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L12 ## 今回の独立増分A：+0x4A は射出方式候補とスケール入力に二重に影響
- L14 - 原作ASM `0x580412 cmp byte [ebx+0x48],0; 0x58041C cmp byte [ebx+0x4A],0`。
- L15 - `0x580422` / `0x580428` が `[ebx+0x46]`, `[ebx+0x49]` を調べ、`0x58042E..0x58043D` で `[ebx+0x2A0]` の double と0をx87比較。
- L16 - `0x58043F` では `[esp+0x80]=0`、`0x58044C` では `[esp+0x80]=1`。通常の有限実数を前提に、局所選択mode0は **48==0 && 4A==0 && (46!=0 || 49!=0 || 2A0!=0)** の場合。これ以外はmode1。NaN/非正規浮動小数、差分パッチによる挙動は別VERIFY。
- L17 - `0x580457..0x580467`: 4A!=0なら `EAX=0`、4A==0なら `[EBX+0x290]` を読み、`0x58046C` で局所 `[ESP+0x84]` へ格納。**4A!=0はmode1への強制だけでなく、+0x290から来る局所値を0へ置換する**。これは独立した二つの帰結。
- L18 - 32組のboolean合成表: 48/4A/46/49/2A0ゼロ非ゼロを全組合せ → mode0=7、mode1=25。4A非0の16組はすべてmode1かつ局所入力0。合成モデルの条件式との一致のみで、原作Gameplayの動的実測ではない。
- L20 ## 今回の独立増分B：+0x45 の幾何効果はmodeで異なる
- L22 - 原作ASM `0x5805DD cmp byte [ebx+0x45],0`、`0x580603 cmp dword [esp+0x80],0`。45!=0かつmode0で、Unit候補の `[edi+0x40..0x4C]` 座標から中心相当を再計算し、局所作図用座標へ保存する経路。上流のポインタ/候補位置の同一性はVERIFY。
- L23 - 別分岐 `0x5807ED cmp byte [ebx+0x45],0` と `0x5807F7 cmp dword [esp+0x80],1`。45!=0かつmode1で局所アンカー候補 `[esp+0x24/0x28/0x74/0x78]` へoffset加算（`0x580801..0x580827`）。このブロックには別の先行条件があるため、mode1なら必ず実行とは言わない。
- L24 - よって「4A!=0だから45の効果は完全に無効」という単純化は誤り。**45の効果はmode0とmode1で異なり得る**。
- L26 ## 今回の独立増分C：+0x4A と +0x2B9 は生成後の幾何更新に再登場
- L28 - `0x580A30 CALL 0x582240`（旧Ghidra CALL索引と原作EXEの `E8 0B 18 00 00` が一致）。戻りEAXをEBPへ移し、直後 `0x580A3A [ebp+0x64]=1`、`0x580A3E [ebp+0xAC]=0`。生成先はオブジェクト候補だが正式型の全復元は未了。
- L29 - 後続 `0x5815EA cmp byte [ebx+0x4A],0`、`0x5815F4 cmp byte [ebx+0x2B9],0`。**この後続ブロックに到達した場合**、4A!=0でさらに2B9のゼロ非ゼロ分岐を通る。
- L30 - `4A!=0 && 2B9!=0`: `0x5815FD..0x581649` に `[ebp+0x170]` への0設定と、生成物候補 `[ebp+0x40/+0x44/+0x48/+0x4C]` の範囲値再書込みあり。位置/幅の変形候補だが当該矩形が実コリジョンhitboxかはVERIFY。
- L31 - `4A!=0 && 2B9==0`: `0x58164B..0x581663` で `[ebp+0x4C]-[ebp+0x44]` の符号処理と半減算の後、double `[ebp+0x170]` へ格納。`+0x170` のゲーム上の正式意味は不明。
- L32 - `0x58166B..0x581687`: 特定フラグ `[esp+0x19]!=0` で生成物候補 `[ebp+0xE8]` のdoubleの符号を反転。2B9分岐後にも続く。発射角・向きとの同定はVERIFY。
- L33 - 両branchともこの局所処理は `0x581E3F` 側へ合流するが、これを**すべてのミサイル生成の共通終端**だと断定しない。
- L35 ## 先行成果との非重複と限界
- L37 - 旧B T012は `0x580280` がMissile RTTIを参照すること、kind/MP/processed、factory→結果receiptのギャップ、Skill+0x290などを既に調査。これらは新規採番しない。
- L38 - ZIP snapshotの `T012_BATTLE_CALC.md` と `LANE_B_HANDOFF.md` で `+0x4A` およびmode変数 `local_94` の上記複合分岐の詳細記録を検索した範囲では見つからなかった。**PC最新正本は未参照なので重複未確定**。今回の純増は上記3節の条件・生成後幾何変形を**原作ASM**で束ねたこと。
- L39 - 2B9のproducer / EBXのruntime object / 0x582240のメモリ所有者 / 生成後実コリジョン / RNG消費と順序 / 最終攻撃対象・HP/MPが未確定。`0x580280` のpseudoは型誤認があり、保存Cコードを直接新エンジンへ転記しない。
- L42 ## Goldenに必要な境界と次の合法検索
- L44 - 原作無改変SHA一致EXE・DAT・SAVE・MAP・入力・seedと同一runで、Skill候補 `+0x48/0x4A/0x46/0x49/0x2A0/+0x45/+0x2B9` の原文プロパティと実runtime値を確認。
- L45 - 例: 48=4A=0かつ46=1（mode0）、48=0/4A=1/46=1（mode1, local入力0）、48=1/4A=0/46=1（mode1, +290入力）、および2B9=0/1、45=0/1、特殊float、+84の有無。各条件で `0x580A30` の生成物byte列、位置・大きさ、実弾・接触/HP/MP・RNG call数を比較。
- L46 - 次はB T011側の`+0x4A/+0x2B9` writer/元Skill DAT宣言と、`0x582240` の生成物所有者・登録先を合法範囲で追う。T013最終target、T012ダメージ決着、T028士気、T024通常AIは引続きP0。
- L47 - 原作Gameplay Golden PASS=0、new/old strict MATCH=0。新B READY=0、MASTER正式統合=0、Task DONE増=0。PC保存0で `OFFLINE-UNSYNCED / NOT READY`。
- L48 - 保存・readback: この独立資料をB所有Library data/へアップロード後に本文の研究ID/VA/SHAと内容一致を別操作で読み戻す。アップロード失敗時はPC・Library未保存と明示し、チャットに再開点を残す。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
