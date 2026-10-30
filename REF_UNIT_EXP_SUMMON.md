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
