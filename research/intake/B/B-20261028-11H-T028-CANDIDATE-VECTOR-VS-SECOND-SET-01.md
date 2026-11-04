# B-20261028-11H-T028-CANDIDATE-VECTOR-VS-SECOND-SET-01 — historical B/T028 source intake

- research_id: `B-20261028-11H-T028-CANDIDATE-VECTOR-VS-SECOND-SET-01`
- owner: B
- tasks: T028 (battle object/roster and candidate routing)
- observed_at: 2026-10-28; research PC original report
- source_relative_path: `data/T028_CANDIDATE_VECTOR_VS_SECOND_SET_NATIVE_20261028_11H.md`
- source_sha256: `999b59cbd7ea8c833bec209d9242cadcbfcafdf987425e4b4f36585c3acae166` (actual PC Markdown bytes and size verified against source metadata 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's static source target; not rehashed as PE this intake)
- native_evidence_va_call_offsets: `0x49460A..0x494618→0x497BB0,0x49515C..0x49516A→0x497BB0,0x497C0D/0x497C12/0x497C17,0x497C21→0x463590,0x497C31→0x4C1290,0x4984AB/0x498D78→0x460E90`
- prior_ids_and_corrections: B-20261028-10H-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01; 12H details the null-vector candidate destruction, 13H classifies caller ECX producer
- evidence_kind: historical original ASM STATIC / INFERRED / runtime VERIFY
- original_golden_status: PASS 0 / strict MATCH 0 / DYNAMIC 0
- formal_ready_status: new B READY0; MASTER formal update0
- intake_stage: PUBLISHED_INTAKE only on exact GitHub readback; NOT_CURATED

## Historical source-grounded facts and proof limits

Historical x86 proves apparent `[ESP+0x98]` at `0x49460F` and `0x495161` is calculated **after four PUSH instructions** and thus points to a different temporary pointer slot relative to the earlier two-set stack base. These are candidate **vector** arguments and not established consumers of the second RB set. Callee `0x497BB0` checks flags candidate `+0x77/+0x75`; if BOTH zero it distinguishes ECX nonnull →`0x497C31→0x4C1290` 4-byte vector append, versus ECX null →`0x497C21→0x463590` ownership cleanup route. If either flag nonzero, it uses other handling `0x5846A0`, with downstream `0x460E90` resetting multiple candidate fields only on permitted branches. Actual second-set consumer remains **UNIDENTIFIED**; don't count stack-address resemblance as proof or assume unconditional destruction from a null caller.

## Next validation / G4 caveat

Read 12H actual object cleanup and 13H null/non-null caller matrix, locate independent second-set reader within legitimate owner source. This is a sanitized re-usable B-owned study with actual original report SHA, not new independent original-game test, ABI closure or external battle result post-commit proof. Dedicated curator alone may admit verified semantic facts into develop REF/dictionary. No game EXE/DAT/SAVE/ZIP, generated DB, private paths or refused content uploaded.
