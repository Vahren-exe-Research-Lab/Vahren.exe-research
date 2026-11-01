# Historical B/T012: RushMissile first permitted update and zero-interval burst candidate
- research_id: `B-20261027-18H-T012-RUSH-SKILL-INTERVAL-FIRST-TICK-01`
- owner/tasks: B/T012 primary; T013 linked
- historical_observed_at: 2026-10-27 18H JST; source+original PE SHA checked on authorized PC 2026-11-02 05H JST
- source_relative_path: `data/T012_RUSH_SKILL_INTERVAL_FIRST_TICK_BURST_NATIVE_20261027_18H.md`
- source_sha256: `931ADC0C142968AD5DBBE70DC5E3851BD47D4C1E1F254E26C820CD61E2562CA6` (5,827 B; current PC source)
- original_PE_SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (read-only checked)
- V9_composite_SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (current read-only tool report; DB not fully rehashed)
- evidence_kind: historical STATIC_ASM / INFERRED signed and timing consequences, current V9 CALL graph; runtime VERIFY
- original_gameplay_golden_PASS: 0; strict_MATCH: 0; DYNAMIC: 0; new_READY: 0
- curation_status: PUBLISHED_INTAKE; source cited in existing develop `REF_BATTLE_AI_MORALE.md`; curatorial status of *specific semantics* must be determined by KB curator.

## Bounded source evidence
- Source §NEW ASM/SEED: `0x54F9AC` writes `Rush+0x1D4=Skill`; `0x54F9D1` loads `Skill+0x78`; `0x54F9D4` seeds `Rush+0x1F4` with this value, not necessarily zero. `Rush+0x1F0` initialized zero.
- Source §NEW ASM/TICK: `0x5501AE` increments `Rush+0x1F4`; `0x5501C1/0x5501C4` compare it with `Skill+0x78` using a signed `JL`; on threshold `0x5501CA` resets counter to zero and executes effect branch. An *update invocation* is not automatically an elapsed rendered frame.
- Source §NEW ASM/REPEAT: `0x5503BE` increments `Rush+0x1F0`, `0x5503D0` compares with `Skill+0x74` upper count, `0x5503D5` compares interval with zero, `0x5503D9 JE 0x5501D4` loops effect within the **same update invocation** when the interval is zero and count remains. Finishing follows `0x5503F9 -> 0x4C22B0` and `Rush+0x1D0=0`.
- Source §CONDITIONAL CONSEQUENCE: for stable, legal, nonoverflowing Skill values, seeded interval `N` may make the *first permitted* update fire immediately; interval zero with positive count K may cause up to K effect repetitions in a single permitted update. The source does **not** show that every legal Skill reaches this case, or that one update corresponds to one visible frame.
- Source §ORIGINAL ASM BYTE WINDOWS retains three historical hashes: `0x54F990..0x54FA27` = `C809726B588758A3D6915BD66BD8EE2CBA552561D813622CA68A3CA5B63C5F3D`; `0x5501A0..0x5501DF` = `6C9FF24E5297BA47863C248C95493177765F2AFA82997DC7EB355FF8159DD524`; `0x550375..0x55040F` = `AB399B4FCC0B1E1F39EB0F44CD92F61F2CB0C456A7D4DD893E77BD84D63CE57F` (last is arbitrary byte window, **not** aligned instruction start). **Not rehashed here**.
- Current V9 `--inspect 0x5501A0` confirms function indexed and E8 `0x5503F9 -> 0x4C22B0`, `0x550219 -> 0x54E7B0`; old source E8 count 3/3 refers to past PE inspection, not a new current 3/3 run.

## Corrections, unverified scope, next
- prior_ids: `B-20261027-17H-T012-RUSH-GAMETASK-VIRTUAL-GATE-JOIN-01` (Task gate prerequisite), `B-20261021-1714-01` (older Rush fields) and T012 historical § intervals. The earlier Task gate is not superseded; it constrains when this update may run.
- erratum: do not implement uniformly as “one effect per frame” or “counter always starts at zero”. Neither is justified by the native conditional paths.
- G4 relevance: zero-interval burst could change Unit/HP/EXP/death-related inputs before native battle termination, but no complete side-effect contract, external result or Golden outcome was demonstrated.
- limitations: legal DAT actual Skill+0x74/+0x78 values, signed overflows, exceptional exits, Skill mutation mid-loop, manager predicates, RNG, HP/MP, child summons, scene time and persistence all VERIFY.
- next_validation: safe independent local ASM check + unmodified-game fixtures with interval 0/1/3 and count 1/2/3, matching original EXE/DAT/MAP/SAVE/inputs/RNG; do not attempt refused code paths.
