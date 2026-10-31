# Legacy scenario names and load reachability — curated C/T033, A/T005/T014

Scope: original ver0.67 DAT scenario declarations STATIC-SCRIPT and saved x86 loader path STATIC; actual legacy-save load to World VERIFY. Original-game Golden PASS=0, strict MATCH=0. Do not remove legacy branches as dead without loader proof.
Sources: data/T033_LEGACY_SCENARIO_IDS.md, evidence/T033_LEGACY_SCENARIO_IDS.json, data/T005_FORMAL_GRAMMAR.md and data/T014_GLOBAL_SAVE.md; C owner research C-20261013-0025-01. This is not a new owner READY.

## 1. Declared vs referenced scenarios
- Nine currently declared IDs: sci1, tutorial, dream, sci_aow, rsc, sci_mt, sci_st, sc_free, rts. Legacy rsc2/rsc3/rsc4/rsc5 have ZERO declarations but 154 / 77 / 77 / 81 references respectively (T033 inventory), including scenario-qualified overrides.
- Normal save persists @scenario and loader restores its string to runtime scenario field +0x34; this does NOT prove that undeclared IDs pass registry validation, instantiate Power/Spot or enter World.
- Conditional rsc2 changes initial power count, diplomacy/boss and victory thresholds; rsc5 can skip some setup and COM hiring. These are source conditions only, not confirmed legal runtime paths in current new game.

## 2. Explicit-null inheritance
- Original unit base has qualified member@rsc and member@rsc2..rsc5 set to explicit @. Ordinary member definitions on child mur/kbtit are different from child-specific overrides on yatai_k1.
- Generic native property lookup prefers scenario-qualified child→ancestor keys before ordinary child→ancestor fallback, and an explicit @ field can block fallback. Whether the specialized member list consumer follows that exact lookup is VERIFY. Do not infer every mur/kbtit roster is empty.
- Verified source SHA256: normalized sc_rnd.dat EF14C2EB56731D95DABBB29A59BEB85592FB57A62C2D09035195B9B8C6191EDA; normalized 00_base.dat D853C4803D38D6439FC0FD76DD3590A43FFE9C9455798D4F5095B36CBB7C8F07.

## 3. Normal-load Power gate and acceptance
- C-20261013-0025-01 links A-owned x86: Power+0xDC sentinel 0x80000008 triggers scenario-qualified base_level lookup through 0x4647D0 before Power registration; non-sentinel skips this particular lookup. Thus @scenario string restoration is not the final acceptance gate.
- Unverified: undeclared scenario lookup result/ABI, old-save availability, Power+0xDC sentinel cases, registry/UI validation, member-list read semantics, and actual game World return. Keep these as VERIFY; do not synthesize an old save and call it Golden.
