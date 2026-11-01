# B-OFFLINE-20261022-1210-T012-T024-VOICE-EXPIRY-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-1210-T012-T024-VOICE-EXPIRY-01`
- owner/tasks: B / T012, T024
- source_relative_path: `data/B_T012_T024_VOICE_EXPIRY_ROUTING_OFFLINE_20261022_1210.md`
- source_sha256: `cdcf17cb64eb648b8bf56597e98f3f0a2a8c2baf94b1bd05deb267bf55082606` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 7949
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 ver0.67｜新B T012/T024：Unitカウンタ満了先は `voice` ScriptBlock を参照する
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X1E4F8`, `0X0057AB22`, `0X0057B380`, `0X0057B453`, `0X00469A20`, `0X00469ABF`, `0X1867E`, `0X18684`, `0X1867D`, `0X0057B467`, `0X1E524`, `0X0057B4CE`, `0X0057B559`, `0X1E51C`, `0X1E520`, `0X0049EB50`, `0X1ED1CC`, `0X0057B800`, `0X57B380`, `0X0057B838`, `0X0057B6FC`, `0X0057B779`, `0X0057B7D8`, `0X469A20`, `0X49EB50`, `0X57AB22`, `0X57B453`, `0X57B467`, `0X57B4CE`, `0X57B6FC`, `0X57B800`, `0X57B838`, `0X1E518`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01`, `B-OFFLINE-20261022-1112-T024-T012-ACTION-TIMER-01`, `B-20261010-2117-03`
- evidence_kind: STATIC source (historical saved Ghidra/REA); INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L11 ## 新規静的証拠と実装上の訂正点
- L13 1. **満了入口**：既存T012の `FUN_0057AA00` は `Unit+0x1E4F8` が正の場合だけ1減算し、1→0の際に `0x0057AB22 → FUN_0057B380` をCALLする（既存 `B-20261010-2117-03` の引用、新発見として再計上しない）。
- L14 2. **重要な新しい接続**：`FUN_0057B380`（VA `0x0057B380`, Ghidra size 1248）は `Unit+0x1DC` を参照し、`0x0057B453 → FUN_00469A20` を呼ぶ。`FUN_00469A20`（VA `0x00469A20`, size 2458）は `0x00469ABF` 付近で文字列 **`voice`** を構築・検索し、内部で **`voice_type` / `class` / `delskill` / `female` / `power`** などの属性を参照し、`ScriptBlock::vftable` のオブジェクトを生成する。よって `+0x1E4F8` 満了時のcallbackには **声・音声または発声スクリプトの選択・配送に関係する静的経路** がある。実際に音を再生する末端までは未証明。
- L15 3. `FUN_0057B380` の外側の入場条件は単純な無条件実行ではない。少なくとも `Unit+0x1867E == 0`、32-bit符号付き `Unit+0xC0 >=0`、`Unit+0xD0 >=0` が必要で、さらに `+0x8C!=0`、`+0x1F8==0`、`+0x1F9!=0`、`+0x18684==2`、`+0x1D0==0`、または `*(Unit+0x1D0+0x1E)==0 && +0x1867D==0` のいずれかを満たす複合ORゲートがある。`+0x1D0` の間接参照は直前のゼロ判定で短絡される。これはGhidra擬似Cに基づくSTATIC、ASM独立照合はVERIFY。
- L16 4. スクリプト由来の候補vectorを準備する `0x0057B467 → FUN_0046D180` について、callee擬似Cは `begin/end` から4バイト要素を複製する。`local_bc != local_b8` を満たす場合のみ候補処理へ進む。候補ゼロ時は行動開始を仮定しない。
- L17 5. 分岐キー `Unit+0x1E524` が **0** の経路は、`0x0057B4CE → FUN_0049EB50`、`0x0057B559 → FUN_00463280` などを使用し、`Unit+0x1E51C` 周辺に追加処理がある。キーが **非0** の別経路では `Unit+0x1E520` を参照し、比較・候補選択・レコード更新を実行する。両分岐は無条件に同じ動作とはいえない。`0x0049EB50` 擬似Cは `0x1ED1CC` 起点・stride `0xB4`・最大 `0x18` 件の内部slotを探索するが、これを原作ゲーム内の『音声キュー24個』と命名するのはまだINFERRED。
- L18 6. 非0の経路では `Unit+0x1E520` が示す連結レコードの `node+0x28` を減算し、結果 `<1` なら `0x0057B800 → FUN_00510030` を呼ぶ。`FUN_00510030` はmap/set系ノードのeraseと更新済みiterator返却に相当するポインタ付け替え・free・要素数減算を含む。これは **Unitタイマー満了後にも別レコードの寿命管理が進む** 静的証拠。`0x57B380` のイベント単位・レコード意味・音声出力保証はVERIFY。
- L19 7. `0x0057B838 → FUN_004BA280` はvectorの保持メモリ解放・3ポインタの0化を行う。候補なし・満了条件不成立・map erase時のリソース状態を勝手に「無害なreturn」と置換しない。
- L20 8. `0x0057B6FC → FUN_0049EB50`、`0x0057B779` と `0x0057B7D8 → FUN_00463280` も同callbackの別条件枝。`FUN_0040ED80` を経由する候補選択があるが RNG消費回数は未確定。全枝のGolden/RNG順は未検証。
- L22 ## 既存の解釈に対する修正
- L24 11時台の『AIが `Unit+0x1E4F8` を設定 → 0到達時 `0x57B380` へ』はSTATICとして維持する。一方、それだけで **AIの攻撃・移動・待機の実行イベント** だと判断してはならない。今回、callback内に `voice` ScriptBlockを読み出す具体経路が見つかったため、少なくとも発声イベント/スクリプト配送が混在する。`Unit+0x1E4F8` は「AIアクション実行タイマー」ではなく **Unitの文字列付き通知/発声に関連するカウントダウン候補** と暫定ラベル変更するのが妥当。発声以外の副作用が全くないとする断定も禁止。
- L26 ## 非重複・次回のP0調査
- L28 - 10/21オフラインB HANDOFF/T012/T024/MASTER snapshotに `0x469A20`, `voice_type`, `+0x1E524`, `+0x1E520`, `0x49EB50` の同定記録を発見できず。最新10/22正本未接続のため、非重複判定は暫定。
- L29 - PC接続復帰時：MASTER最新cp/Task Queue/READYと復旧索引を最初に読み、今回IDと既存ID/owner/競合/READYを照合してBが所有する資料へ **一度だけ** 取り込む。EのMASTERは変更しない。現行V3でE8 `0x57AB22`, `0x57B453`, `0x57B467`, `0x57B4CE`, `0x57B6FC`, `0x57B800`, `0x57B838` をJMP/RefTypeと独立に照合。
- L31 - Golden（**計画のみ・NOT RUN**）：無改変EXE/DAT/SAVE/MAP、同一入力・RNG・Unit/Skill/AIモードで `+0x1E4F8=0/1/2`, `+0x1E518=0/75`, voice候補空/あり, `+0x1E524=0/非0`, `+0x1E520` node TTL `0/1/2/10000`, 外側ガード各偽/真、発声イベント有無・AI実行行動・MP/RNG順を区別して観測。実測なしならGolden PASS=0、strict MATCH=0。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
