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
