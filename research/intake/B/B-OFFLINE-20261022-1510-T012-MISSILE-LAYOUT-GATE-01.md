# B-OFFLINE-20261022-1510-T012-MISSILE-LAYOUT-GATE-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-1510-T012-MISSILE-LAYOUT-GATE-01`
- owner/tasks: B / T012, T011
- source_relative_path: `data/B_T012_MISSILE_LAYOUT_GATES_OFFLINE_20261022_1510.md`
- source_sha256: `fc20088da5a25161689d83198d9c875be39a54c7d5e39fbe92287a60cfa56b11` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 6994
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 ver0.67｜B担当 T012/T011：Missile生成時の入力・出力レイアウト分離と3段ゲート監査
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X580412`, `0X58041C`, `0X58043F`, `0X58044C`, `0X580A30`, `0X582240`, `0X582001`, `0X4BC920`, `0X582040`, `0X40E670`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261022-1410-T012-MISSILE-MODE4A-01`, `B-OFFLINE-20261021-0200-01`
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L10 ## A. 新しい交差検証：入力ポインタと生成後のMissile候補を同一構造体として扱ってはいけない
- L12 - 先行ASMでは `0x580412/0x58041C/0x58043F/0x58044C` の分岐が `[EBX+0x48/+0x4A]` 等を読み、`[EBX+0x290]` (4バイト候補)、`[EBX+0x2A0]` (double候補)、`[EBX+0x2B9]` (1バイト)を参照。
- L13 - 先行検索擬似Cでは、`0x580A30 -> 0x582240` の直接CALL先に `Missile::vftable` と `FUN_005b6c2b(0x1C8)` 確保候補がある。14時台の保存ASM転記ではCALLの E8機械語 `E8 0B 18 00 00` と、戻りEAXからEBPへの保持を記録。
- L14 - 0x1C8 = **456 bytes**。これに対し EBX側の `+0x290` の末尾は `0x293`、`+0x2A0` double末尾は `0x2A7`、`+0x2B9` byte末尾は `0x2B9`。**456バイトのMissile候補 allocation の内側に収まらない**。
- L15 - 一方、生成後 EBP側の `+0x40..+0x4C` 各4バイト（最大末尾0x4F）、`+0x64` (末尾0x67)、`+0xAC` (末尾0xAF)、`+0x170` double（末尾0x177）は全て0x1C8範囲内。読み書きの整合性から **少なくとも入力側の大きいレコードと生成後の456バイトMissile候補は、別レイアウトとして型モデル化する必要がある**。
- L16 - 注意: EBXが独立した Skill オブジェクトのbase pointerか、別の大きな複合構造のsubobject pointerかは未確定。EBPもfactory再利用経路があるため常に新規allocationされたと断定できない。以上は**型・オフセット衝突防止の静的制約**でありメモリ実測ではない。
- L18 ## B. 前回ASMから導いた3ゲート（新しい組合せ関係）
- L20 - `G1 / mode`: `mode0 iff (flag48=0 AND flag4A=0 AND (flag46!=0 OR flag49!=0 OR double2A0!=0))`。それ以外はmode1。これは前回の有限数値モデルを再利用。
- L21 - `G2 / local geometry input`: `flag4A!=0 -> 0`、`flag4A==0 -> [EBX+0x290]`。mode1そのものを理由に0になるわけではない。
- L22 - `G3 / postfactory shape`: **到達可能な後続ブロック内で** `flag4A!=0` のときに限り `flag2B9` を検査し、0/非0で `EBP+0x170` または `EBP+0x40..+0x4C` の別経路へ進む。別の全域で `2B9` が無関係だと断定しない。
- L23 - G1〜G3の入力6bit (48,4A,46,49,2A0が零か,2B9) を純粋なBooleanモデルで **64/64列挙**。構成数は `(mode0,+290,shown pathでは2B9未検査)=14`、`(mode1,+290,shown pathでは2B9未検査)=18`、`(mode1,0,2B9=0)=16`、`(mode1,0,2B9!=0)=16`。mode0は14/64、mode1は50/64。
- L24 - 新しい設計上の帰結：`mode1` 内に **G2が0になる32ケース**と **G2が+0x290になる18ケース**が混在する。「mode1なら生成位置入力0」と単純化してはいけない。また `2B9` が後段幾何分岐を変えるのは（現在の保存ASMで観測した範囲では）`4A!=0` の場合だけ。
- L25 - 合成列挙は命令再実行ではなく、**保存済み条件式の検算**。NaN/非有限double、先行ガード、未到達ブロックやRNGは対象外。実原作Goldenには計上しない。
- L27 ## C. 最小のGolden設計と未解決P0
- L29 1. `48=0,4A=0,46=1`: mode0、localは+290。`2B9=0/1` で**示された後続分岐**に差が生じないか観測。
- L30 2. `48=1,4A=0,46=1`: mode1だが localは+290。`48=0,4A=1,46=1`: mode1でlocalは0。mode固定・geometry sourceだけ変更する対照群。
- L31 3. `48=0,4A=1,46=1,2B9=0/1`: mode/localを固定して後段幾何分岐のみ対照。加えて`45=0/1`、`+290=0/非0`、浮動小数+2A0の +0/-0/非0/NaNを区別。
- L32 4. T011: `[EBX+0x2B9]` の writer／DATプロパティと、`0x582240` factory返値の本当のABIを原作ASMで確認。T012: `0x580A30` → 0x582240 → `0x582001` (0x4BC920) / `0x582040` (0x40E670) の双方の object-owner/登録後を追跡。T013: 当たり判定・最終対象決定の入口と時間/RNG順の関係は別P0。
- L33 5. 原作同一SHA EXE・無改変DAT・SAVE・MAP・同じ入力とseedが揃った合法Goldenで、生成物のバイト列/矩形、動き、接触、HP/MP、RNG countを観測する。未測定。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
