# B-20261028-1217-T028-NULL-VECTOR-CANDIDATE-DESTRUCTION-01 — historical B/T028 source intake

- research_id: `B-20261028-1217-T028-NULL-VECTOR-CANDIDATE-DESTRUCTION-01`
- owner: B
- tasks: T028 (battle object/roster and candidate routing)
- observed_at: 2026-10-28; research PC original report
- source_relative_path: `data/T028_NULL_VECTOR_CANDIDATE_DESTRUCTION_NATIVE_20261028_12H.md`
- source_sha256: `890db7a710ba6747b9b29f7a0a6485081a062c7dcac99d3c8747a8e05772d13b` (actual PC Markdown bytes and size verified against source metadata 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's static source target; not rehashed as PE this intake)
- native_evidence_va_call_offsets: `0x497C1B/0x497C21→0x463590,0x4635A0→0x49F410,0x4635BA→0x4BF820,0x4635DE→0x402710,0x4635E4→0x460F10,0x46103E→0x510C20,0x4635EE→0x4591F0,0x4635F4→0x5B6BBB`
- prior_ids_and_corrections: B-20261028-11H-T028-CANDIDATE-VECTOR-VS-SECOND-SET-01; 13H isolates ECX=NULL caller sites, but reachability retains +0x75/+0x77 prerequisites
- evidence_kind: historical original ASM STATIC / INFERRED / runtime VERIFY
- original_golden_status: PASS 0 / strict MATCH 0 / DYNAMIC 0
- formal_ready_status: new B READY0; MASTER formal update0
- intake_stage: PUBLISHED_INTAKE only on exact GitHub readback; NOT_CURATED

## Historical source-grounded facts and proof limits

Original static CALL chain identifies the `0x497BB0` ECX-null branch for candidate whose flags `+0x77/+0x75` are both zero: `0x497C1B` extracts owner pointer and `0x497C21→0x463590` starts an actual cleanup route rather than no-op. `0x463590` accesses owner `+0x2FC` keyed tree through `0x49F410` and `0x4BF820` range erase, then `0x4635E4→0x460F10` looks up owner `+0x330` keyed tree and may remove nodes through `0x510C20` while resetting record `+0x94` and string `+0x84`. A nonnull candidate pointer can then pass destructor `0x4591F0` and deallocator `0x5B6BBB`. No proof of guaranteed live destruction, no owner alias safety or linkage to final morale/death/EXP; all those remain VERIFY.

## Next validation / G4 caveat

Check 13H caller ECX producers and candidate flag state, validate input ownership and legal original-game trigger before recording G4 cleanup semantics. This is a sanitized re-usable B-owned study with actual original report SHA, not new independent original-game test, ABI closure or external battle result post-commit proof. Dedicated curator alone may admit verified semantic facts into develop REF/dictionary. No game EXE/DAT/SAVE/ZIP, generated DB, private paths or refused content uploaded.
