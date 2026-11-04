# B-OFFLINE-20261022-1609-T012-MISSILE-POSTREGISTER-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-1609-T012-MISSILE-POSTREGISTER-01`
- owner/tasks: B / T012, T011
- source_relative_path: `data/B_T012_MISSILE_POSTREGISTER_OFFLINE_20261022_1609.md`
- source_sha256: `3629c7d2d8f8612add944d0dd3b657911beab59d082715cafd7ac12c53a1a935` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 8337
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T012/T011 弾生成後の二重登録境界・Skill+2B8後段経路（2026-10-22 16時台 JST）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X580280`, `0X00582001`, `0X004BC920`, `0X00582040`, `0X0040E670`, `0X00582022`, `0X004B9F70`, `0X00582032`, `0X0054DA10`, `0X54DA10`, `0X40E670`, `0X00547FC0`, `0X00549F50`, `0X00580280`, `0X54DA66`, `0X4FACA0`, `0X54DABC`, `0X4C5EF0`, `0X54DAD2`, `0X4C60F0`, `0X4BC920`, `0X4C624D`, `0X4C60B7`, `0X4C5FA5`, `0X582032`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261021-0200-01`, `B-20261019-0408-01`, `B-20261019-0520-01`, `B-OFFLINE-20261022-1410-T012-MISSILE-MODE4A-01`, `B-OFFLINE-20261022-1510-T012-MISSILE-LAYOUT-GATE-01`
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L8 ## 増分A：0x580280で生成物候補へ入力レコードポインタをコピーする書込み
- L10 保存済みGhidra擬似C（`FUN_00580280`）で `piVar12[0x2c] = (int)param_3;` を確認した。32bit整数配列解釈なら出力候補の `+0xB0` へのポインタ相当の書込みに対応する。また当関数内では複数箇所で `param_3+0x2B8` と `param_3+0x2B9` を読む。従って `param_3` はSkill相当の入力レコード**候補**。関数ヘッダは `float param_3` と推定されており型復元が矛盾するため、厳密な Skill* と断定しない。
- L12 同関数末尾には、通常側 `0x00582001 -> 0x004BC920` と特殊側 `0x00582040 -> 0x0040E670` の直接CALLが記録される。これは既存 `B-OFFLINE-20261021-0200-01` で指摘済みであり、CALL存在そのものを新規再計上しない。今回の増分は登録**先の状態変更の差**と、通常側に続く条件付き後段。
- L14 ## 増分B：通常登録後だけに現れる Skill候補+0x9F5 後段ゲート
- L16 `0x580280`擬似C末尾の通常経路は以下（説明用の条件整理であり原ソースではない）。
- L18 ```c
- L19 if (special_route_flag == 0) {
- L20 FUN_004bc920(manager_candidate, missile_candidate);
- L21 if (input_skill_candidate->field_0x30 != input_skill_candidate->field_0x34 &&
- L22 input_skill_candidate->field_0x23C == 0) {
- L23 FUN_004b9f70(...); // separate gated side effect
- L24 }
- L25 if (input_skill_candidate->field_0x9F5 != 0) {
- L26 FUN_0054da10();
- L27 }
- L28 } else {
- L29 FUN_0040e670();
- L30 }
- L31 ```
- L33 `0x00582022 -> 0x004B9F70`、`0x00582032 -> 0x0054DA10` をGhidra CALL索引で確認。`0x54DA10`の既存B研究 `B-20261019-0408-01` はSkill+0x2B8による座標・二helperの差を既に解明しているため、その既知分岐を新規成果として数えない。今回の未記録候補は**0x580280の通常登録後の +0x9F5 gate と先行+0xB0 writer による接続仮説**。`special_route_flag` はGhidraの `uStack_fc._3_1_` の再命名で、真の入力と寿命・値域はVERIFY。
- L35 ## 増分C：登録ヘルパの更新効果は同一でない
- L37 - `0x004BC920`（146 bytes）は `FUN_004BC3C0(manager,1)`で得るvector候補のendを4バイト増加し、manager候補 `+0x8` の連番を+1して `missile_candidate+0x54` へ格納する。整列・再確保の異常系があり、常に正常完了する保証はない。
- L38 - `0x0040E670`（137 bytes）は**隠れEAX参照**の `+0x268/+0x26C/+0x270` の3ポインタを使用して4バイト要素を追記する。観測した当関数擬似C内部には `+0x54` の通番付与が存在しない。`0x40E670`直CALL callerは `0x00547FC0` site `0x00549F50` と `0x00580280` site `0x00582040` の2つ。両者を同じ登録完了・表示中・命中登録と解釈しない。
- L39 - `0x004B9F70`（162 bytes）は候補vector非空時にindexを選び、vtable `+0x24` 経由の処理を呼び出す。表示・音・効果の人間名はVERIFY。
- L41 ## 増分D：下流の子要素再登録候補と順序への影響
- L43 既知 `0x54DA10` は `in_EAX+0xB0` で取得したレコードから `+0x2B8` を読み、座標計算 `site 0x54DA66 -> 0x4FACA0`、候補出力 `in_EAX+0xE0/+0xE4`、virtual slot+8 の後、`+2B8!=0` では `site 0x54DABC -> 0x4C5EF0`、`+2B8==0` では `site 0x54DAD2 -> 0x4C60F0`へ分岐する（B-20261019-0408-01を再利用）。
- L45 今回下流擬似Cを新規照合すると、`0x4C60F0` も `0x4C5EF0` も仮想slot `+0x4C` が成立する場合に**内部vector子要素**を走査し、既存vectorから要素を外す候補処理・矩形 `+0x40/+0x44/+0x48/+0x4C` の座標を更新し、`0x4BC920`を呼んで再登録する経路を持つ（CALL sites `0x4C624D`、`0x4C60B7`）。
- L47 `0x4C5EF0` にも別の `0x4C5FA5 -> 0x4BC920` があるが、Ghidra擬似Cでは当該経路は `param_4==0` 時の**親要素用**。`0x54DA10` は `0x4C5EF0(...,1)` として呼ぶため、この接続が正しければ親用直登録は通らず、子要素走査側のみが候補となる。ABI復元が不完全であることから実命令による引数1の確認はVERIFY。
- L49 ここから **親の通常登録1回と、条件付き子要素登録の複数回を混同すると生成数・管理連番・RNG時系列を誤算するリスク** が分かる。ただしどの旧原作戦闘でもそれが実行されると確定したわけではない。`0x54DA10` の隠れ `in_EAX` が 0x580280生成した同じ `Missile` ポインタか、caller `0x580280` のレジスタ保存・復元を実ASMで確認する必要がある。
- L51 ## 根拠の検証
- L53 - SQLite `PRAGMA quick_check = ok`。
- L54 - 上記9関数の保存擬似C存在を確認。保存擬似Cの指定12文字列パターン存在も確認。追加された11個の直接CALL組 `(caller VA, site VA, callee VA)` が全件DB内で1件ずつ一致。**旧10/21索引由来であり現行V3の原作E8機械語検証ではない。**
- L55 - 2個の登録ルート候補×`+0x9F5`二値×`+0x2B8`二値＝8件の**合成分岐モデル**をJSONへ保存。これは直接CALL成否・原作の到達性・値の合法性を保証しない。
- L56 - 保存済みGhidra関数のSHAとCALL現物は別添構造化JSONへ記録。原作ゲーム新規実行0、Golden PASS0、strict MATCH0。
- L58 ## 非重複・安全・次のP0
- L60 既知分を再計数しない: `B-20261019-0408-01`（0x54DA10 Skill+2B8枝）、`B-20261019-0520-01`（2B8 writer）、`B-OFFLINE-20261021-0200-01`（0x580280→pool→2登録CALL）、`B-OFFLINE-20261022-1410-T012-MISSILE-MODE4A-01`、`B-OFFLINE-20261022-1510-T012-MISSILE-LAYOUT-GATE-01`（後者の実IDと完全一致要PC再照合）。新規候補の局所scopeは「0x580280末尾Skill+9F5 gateと＋B0 producer」「下流子要素再登録の静的条件」「通常/代替vecの状態副作用の違い」。PC最新版未照合につき非重複確定不可。
- L62 次の重点検索は安全なB範囲の `0x580280` site `0x582032` 直前・ `0x54DA10` 入口におけるEAX/ESI実物同定（最新PCに許可された保存ASMが存在する場合のみ）、`Skill+0x9F5` writer／原文DAT key、`0x4C60F0`子要素virtual+0x4Cの戻り値と旧新座標・管理連番の整合。必要な Golden は同一正規EXE SHA、無改変DAT、SAVE、MAP、入力/seed、直前直後のMissile ID・子要素数・位置・HP/MP・RNG順序。**ゲームプレイ Golden 0、strict MATCH 0、DYNAMIC 0、Task DONE増0**。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
