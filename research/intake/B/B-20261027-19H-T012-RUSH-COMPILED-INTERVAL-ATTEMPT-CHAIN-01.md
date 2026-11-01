# B-20261027-19H-T012-RUSH-COMPILED-INTERVAL-ATTEMPT-CHAIN-01 — source-preserved B research

- research_id: `B-20261027-19H-T012-RUSH-COMPILED-INTERVAL-ATTEMPT-CHAIN-01`
- owner: B
- tasks: T012 (T011 crossref)
- observed_at: 2026-10-27 19H JST
- source_relative_path: `data/T012_RUSH_COMPILED_INTERVAL_ATTEMPT_LINK_NATIVE_20261027_19H.md`
- source_sha256: `94b1496217b2336458137a03ca89e15c197e5529219ed0bfafd9953320861adf` (actual authorized research-PC Markdown byte SHA-256 rechecked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no fresh PE hash in this intake)
- original_source_kind: saved original-PE ASM / V9 or historical index / normalized DAT, as attributed below; current independent runtime = VERIFY
- evidence_va_call_offsets: `0x59C889,0x59C89E,0x5501A0,0x5501D4,0x550219,0x55037F,0x55038F,0x5503BE,0x5503D0, Skill+0x74/+0x78/+0x1D0, Rush+0x1F0/+0x1F8`
- prior_ids_and_errata: B-20261013-1930-01 (rush_interval compiler); B-20261027-18H-T012-RUSH-SKILL-INTERVAL-FIRST-TICK-01 (initial counter)
- supersedes: only expressly mentioned source corrections; other older interpretations remain linked
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: newly READY 0 / formal E MASTER update 0
- intake_stage: OWNER_STAGED; only a successful exact GitHub readback establishes PUBLISHED_INTAKE; not CURATED

## Reusable research evidence

The source joins the parser's raw `rush_interval` normalization at `0x59C889..0x59C89E` to the Rush update loop near `0x5501A0` (timer and attempt counter `Rush+0x1F0`; Skill quota `+0x74`). Raw interval -1 yields compiled 0; raw 0 yields compiled 5 **in this parser path**, so raw 0 and -1 are not equivalent. The historical unmodified DAT example `F21_...dat` lines 83-90 (relative path in source) has rush=4 and rush_interval=-1; this is a static configuration/example, NOT a measured four-spawn event. Original ASM `0x5503BE` increments attempts and `0x5503D0/0x5503D3` applies the quota test AFTER an attempt; a zero or negative quota need not imply zero attempts along a reachable route. `Skill+0x1D0` plus `Rush+0x1F8` controls optional result-link fields `result+0x194/old+0x198`; the summon kind4 branch can retain null result local. Do not infer child EXP refund, actual execution timing, successful spawn count, or G4 afterbattle effects.

## Limits and next validation

Limited V9-native control-flow proof and permitted DAT/Skill compiler values; explicit attempt/success/result link separation, legal original-game tick/RNG baseline before Golden. The old owner source and cited sites are the verification authority; this text is a sanitized reusable research note, NOT a new native experiment, complete game-engine contract, or G4 result transaction proof. Independent curator must check original SHA, permitted V9 ASM/DAT, earlier REF/dictionary confidence and correction lineage before adopting semantic facts. No raw executable, original game assets, absolute private paths, token/logs, denied-operation content or large database is published.
