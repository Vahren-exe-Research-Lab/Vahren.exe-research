# B-20261027-2013-T011-T012-FOLLOW-PARSER-RESULT-LINK-01 — source-preserved B research

- research_id: `B-20261027-2013-T011-T012-FOLLOW-PARSER-RESULT-LINK-01`
- owner: B
- tasks: T011, T012
- observed_at: 2026-10-27 20H JST
- source_relative_path: `data/T011_FOLLOW_COMPILER_RUSH_RESULT_LINK_NATIVE_20261027_20H.md`
- source_sha256: `f2b968ef7b5e15583af0883196eefc314bacf9c09233dcd61ba98930abfadcd8` (actual authorized research-PC Markdown byte SHA-256 rechecked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no fresh PE hash in this intake)
- original_source_kind: saved original-PE ASM / V9 or historical index / normalized DAT, as attributed below; current independent runtime = VERIFY
- evidence_va_call_offsets: `0x59B91A,0x59B928,0x59B94D,0x59B967,0x59B969,0x59B999,0x55038F,0x5503A6,0x5503B2,0x5503B8, Skill+0x1D0, result+0x194/+0x198`
- prior_ids_and_errata: B-20261027-19H-T012-RUSH-COMPILED-INTERVAL-ATTEMPT-CHAIN-01; linked-result fields known earlier; do not count twice
- supersedes: only expressly mentioned source corrections; other older interpretations remain linked
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: newly READY 0 / formal E MASTER update 0
- intake_stage: OWNER_STAGED; only a successful exact GitHub readback establishes PUBLISHED_INTAKE; not CURATED

## Reusable research evidence

Historical native static evidence connects the `follow` Skill property parser at `0x59B91A..0x59B999` to compiled `Skill+0x1D0`: the `follow=on` text comparison path stores 1; other input routes use integer property getter `0x4647D0` and store its result, not a constant Boolean. The report compared `.rdata` string targets and a previous B native record without treating adjacent protected strings as a new source. On Rush update, `0x55038F` checks compiled `Skill+0x1D0`; nonzero enables OPTIONAL result chain linking when result and old pointer both exist, writing `+0x194/+0x198`, and `Rush+0x1F8` later becomes result. The type4 summon path may leave the local result null. The rule is a branch gate, not confirmed summon parenthood, permanent Unit identity, or EXP transfer; follow magnitude use by other consumers remains VERIFY.

## Limits and next validation

Verify source compiler and Rush consumer in current V9 with normalized DAT values, then inspect allowed result lifecycle before claiming afterbattle identity and G4. The old owner source and cited sites are the verification authority; this text is a sanitized reusable research note, NOT a new native experiment, complete game-engine contract, or G4 result transaction proof. Independent curator must check original SHA, permitted V9 ASM/DAT, earlier REF/dictionary confidence and correction lineage before adopting semantic facts. No raw executable, original game assets, absolute private paths, token/logs, denied-operation content or large database is published.
