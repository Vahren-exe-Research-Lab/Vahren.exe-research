# B-20261028-14H-T028-DECIDE-SELECTOR-FLAG-WEIGHT-01 — historical B/T028 source intake

- research_id: `B-20261028-14H-T028-DECIDE-SELECTOR-FLAG-WEIGHT-01`
- owner: B
- tasks: T028 (battle object/roster and candidate routing)
- observed_at: 2026-10-28; research PC original report
- source_relative_path: `data/T028_DECIDE_SELECTOR_FLAG_WEIGHT_NATIVE_20261028_14H.md`
- source_sha256: `0c7954ec4979f19e2d74ee80bf9e0dce7b189d00beaae32ccbec5a21acdbf046` (actual PC Markdown bytes and size verified against source metadata 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's static source target; not rehashed as PE this intake)
- native_evidence_va_call_offsets: `0x497C41→0x5846A0,0x497C4D/0x497C57/0x497C59/0x497C63/0x497C6A/0x497C74,0x497C7B/0x497C82/0x497C84,0x497CAF→0x402800, literals 0x632838 decide3,0x632840 decide11;candidate+0x74/+0x75/+0x77`
- prior_ids_and_corrections: B-20261028-13H-T028-NULL-ECX-CALLSITE-MATRIX-01 and earlier 11H/12H flag routing; `decide3` string already mentioned in other old B report (different site)
- evidence_kind: historical original ASM STATIC / INFERRED / runtime VERIFY
- original_golden_status: PASS 0 / strict MATCH 0 / DYNAMIC 0
- formal_ready_status: new B READY0; MASTER formal update0
- intake_stage: PUBLISHED_INTAKE only on exact GitHub readback; NOT_CURATED

## Historical source-grounded facts and proof limits

On the **nonempty candidate-state** branch of `0x497BB0` (the alternative to the both-zero `+0x75/+0x77` null/vector route), native `0x497C4D` reads candidate flag `+0x74`. When nonzero it selects string `decide3` and local integer 500; when zero it selects string `decide11` and computes 10 if another parameter's byte `+0x1D==0`, else 25 via conditional arithmetic at `0x497C6E..0x497C74`. The label is passed to a string operation at `0x497CAF→0x402800`. Numeric values are not automatically morale/death counters or timers; final consuming site was unresolved. Older `decide3` text appears elsewhere, so the independent finding is its native branch coupling at `0x497BB0`, not invention of the literal. Reachability, game-visible effect and other caller ABI remain VERIFY.

## Next validation / G4 caveat

Trace safe downstream consumer of local numeric, validate original DAT/legal candidate flags, avoid universal selector/death meaning and prove second-set usage separately. This is a sanitized re-usable B-owned study with actual original report SHA, not new independent original-game test, ABI closure or external battle result post-commit proof. Dedicated curator alone may admit verified semantic facts into develop REF/dictionary. No game EXE/DAT/SAVE/ZIP, generated DB, private paths or refused content uploaded.
