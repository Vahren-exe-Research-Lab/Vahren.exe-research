# Unit / experience / summon: current evidence summary (T011/T012)

Scope: ver0.67 original PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
Evidence basis: existing B owner reports and independent EXP research on the authorized PC.
All points below are STATIC or INFERRED unless stated otherwise. Original gameplay Golden PASS=0, strict MATCH=0.

## 1. UnitData experience writer
- Native 0x551E50 is linked to battle EXP addition, including direct CALL sites 0x547A8C, 0x551167, 0x551C6A and 0x57F4E9.
- The identified accumulation target is a linked UnitData field at +0x16C; the exact end-to-end caller types, rounding and lifetime are not yet fully verified.
- Do not equate an inline summon cache with permanent UnitData experience.
- References: data/T011_T012_EXP_TRAINING_DEATH_CROSSWALK_NATIVE_20261029.md; exp_research_20261021/EXP_RESEARCH_PROGRESS_20261022.md.

## 2. Training and death
- Training function 0x471E80 uses UnitData+0x170 for a threshold and writes experience to UnitData+0x16C at 0x4723D8; 0x4723DE calls 0x58A650 for level update.
- The native death path references property dead_penalty at 0x588D77, calls getter 0x46F4C0 from 0x588D7C, and writes the experience result at 0x588DE0.
- The bundled context.dat has dead_penalty=95; under the normal nonnegative path this is a 95% retention factor, not an unconditional formula for every boundary value.
- References: data/T011_T012_EXP_TRAINING_DEATH_CROSSWALK_NATIVE_20261029.md; data/T011_DATA_MODEL.md.

## 3. Summon holder and group: different relationships
- The observed static holder flow is source S+0xC -> SummonFlash+0xC -> child Unit+0xC.
- Relevant native sites include 0x54ED70, 0x54ED8A, 0x54F074, 0x54F07A and 0x56F720.
- This proves a propagated holder reference, NOT a unique summon parent ID or experience refund destination.
- Child membership through 0x568710 and the source pointer used by callers are separate relationships.
- Four summon-related caller contexts include 0x54DF4B, 0x550219, 0x57F484 and 0x57F492.
- References: data/T011_SUMMONFLASH_HOLDER_CHAIN_NATIVE_20261027_14H.md; data/T011_SUMMON_CALLER_GROUP_PROVENANCE_NATIVE_20261027_15H.md; data/T011_SUMMON_CALLER_SOURCE_TRIAD_SENTINEL_NATIVE_20261027_16H.md.

## 4. P0 remaining, no inferred READY
- Verify whether an inline summon EXP store is transferred to persistent UnitData before battle result cleanup.
- Trace normal and simple-battle EXP paths to the result, save and load boundaries.
- Compare original unmodified game with a controlled SAVE/MAP/DAT/input/RNG capture before accepting strict compatibility.
- This document is a curated entrypoint, not a replacement for the original source reports.

## 5. T011 training count and leader-keyed bonus memo (2026-10-31 06H/07H)
- Original PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` was independently read back. Native E8 at `0x472081` calls `0x595320`; the helper takes a nonzero `Power+0xD8` training count or falls back to scenario `training_up`, with a zero-to-one and negative-to-zero normalization path. Its general role was **already reported** by `dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md` §§61/62.1: newly documented here is the exact producer-to-turn-loop call chain, not an independent discovery of `training_up`.
- Native `0x47229E` calls already-named/inferred leader resolver `0x583DC0`. A null leader takes the base count; otherwise `0x4722BE` searches a stack-local tree through `0x4F8A80`. On a hit, node `+0x10` is added to the base count (`0x4722D0..0x4722D3`). This mapped integer is **not a second independently identified training skill**.
- On a cache miss, the native branch scans the leader's skill array, tests kind `+0x40 == 6` and name `training`, reads its integer `+0x2B0` into bonus `B`, and computes `base + B` at `0x47238E`. Native `0x4723A8` calls `0x4ED3B0` to allocate and populate a 24-byte node from `(leader pointer, B)`; `0x4723BC` calls `0x474A80` for tree insertion. This leader-pointer-keyed memoization is the **new 07H crosswalk**, not a change to the previously recorded training formula.
- Original-PE byte-window SHA256 readback: `0x595320..0x5953AD` = `0BA98130D2DF8A06275B558B27BF23AD0305A6C07D73AD13ED54E1935AB2C5E0`; `0x47230D..0x4723C1` = `C06DD1963E59B0B27A75E784BDFA6A1571E04221F57636F2CE5AC1191ECB0328`; `0x4ED3B0..0x4ED3EF` = `1395CDD21F4E7E00E49A578913A87DF123874310B5581FA95EB6F0BEC44C0C80`. Capstone independently confirmed the key E8 sites, field loads and +0x2B0 access.
- Source IDs: `B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01` (`data/T011_TRAINING_COUNT_PROVENANCE_NATIVE_20261031_06H.md`) and correction `B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01` (`data/T011_TRAINING_LEADER_BONUS_MEMO_NATIVE_20261031_07H.md`); owner `B/T011`. The 07H correction takes precedence over any 06H suggestion that node `+0x10` and Skill `+0x2B0` are semantically different effects.
- State: original x86 **STATIC**; stack-local memo lifetime, duplicate-leader behavior, negative bonuses, overflow and realized in-game training remain **INFERRED/VERIFY**. Original-game Golden PASS **0**, strict MATCH **0**, no owner READY or MASTER promotion. The authorized 20x-modified DAT snapshot must never substitute for an unmodified original-DAT Golden fixture.

## 6. T011 訓練時の一時leader-bonus tree：生成・削除境界（B 08H–11H）
- 既存07Hの「leader pointer → training bonus B」のメモ化と区別する。08H原作x86 0x472091→0x49ED90 はstack-local tree header用の24-byte sentinelを初期化し、0x4726C1→0x4DEF40で後始末した後、0x4726D9→0x5B6BBBでsentinelを解放。永続UnitData経験値格納先ではない。
- 08H 0x474A80下位では同一keyの挿入不成立時にincoming nodeを破棄、caller 0x4723C1は挿入flagではなく既計算base+Bを利用する。後続Unitで同じleaderを共有した際の再計算と値の一貫性はVERIFY。
- 09H 0x4DEF40はbeginがheadの先頭nodeかつendがheadのとき0x4DEF57→0x4ED030を呼び、0x49F6A0のsubtree clearを使う全区間経路を持つ。条件不一致のとき0x4DEFCF→0x4DEC70のpartial eraseへ進む。通常訓練が必ずpartial pathを通るとは断定しない。
- 10H 0x4DEC70はnode+0x15をチェックし無効iterator報告候補を分岐、0x4DEEBBでnode解放、tree count+0x8の条件減算・出力iterator store。木型と例外経路はINFERRED/VERIFY。
- 11H 0x4DEF74で削除対象currentを退避し、right-subtree最左端またはparent上昇で次iteratorを削除前に保存（0x4DEF9A/0x4DEFC4）。0x4DEFCFで削除後、0x4DEFD4..DCのループに戻る。解放済みcurrentを再利用しない設計意図はINFERRED。
- 独立原作PE-window SHA256: 0x4DEF40..0x4DEFE8 = 22CE973C898A0C136230C929A1AD2E7435E5C605FA3E25A8037DA398E6A142ED; 0x4DEC70..0x4DEEE2 = 45928E56A9E419403F375690D648172D59516995AC973E98922E95C9F909FF27; 0x4DEF6A..0x4DEFE5 = 7296E8670C2B6255ECBB977E8BE4811E29C62C9B191CD767F444E95AF6151080。
- Owner/IDs: B/T011、B-20261031-08H-T011-TRAINING-CACHE-LIFECYCLE-01、B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01、B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01、B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01。
- 一次報告: data/T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md; data/T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md; data/T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md; data/T011_TRAINING_PARTIAL_RANGE_SUCCESSOR_PRESERVE_NATIVE_20261031_11H.md。
- 確度: 原PE命令/E8はSTATIC、実際の全経路到達と例外はVERIFY。原作Gameplay Golden PASS=0 / strict MATCH=0 / B READY増分0。召喚親への恒久EXP移管の証明には流用しない。
