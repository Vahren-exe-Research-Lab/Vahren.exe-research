# B-20261028-10H-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01 — historical B/T028 source intake

- research_id: `B-20261028-10H-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01`
- owner: B
- tasks: T028 (battle object/roster and candidate routing)
- observed_at: 2026-10-28; research PC original report
- source_relative_path: `data/T028_ROSTER_VECTOR_DUAL_SET_PRODUCER_NATIVE_20261028_10H.md`
- source_sha256: `d13eda3a41dfc3f0ba40b59a039c407b0aae263768e3ae5f26bc2565839fcc37` (actual PC Markdown bytes and size verified against source metadata 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's static source target; not rehashed as PE this intake)
- native_evidence_va_call_offsets: `0x493A59→0x44D730,0x493A7B→0x47BB50,0x493A8B/0x493A92,0x493A9E→0x5882F0,0x493AB6/0x493AD1→0x498EE0,0x493AD6/0x493AF4→0x498EE0,0x493AF9..0x493B2D`
- prior_ids_and_corrections: B-20261028-03H-T028-TREEFLAG-DUAL-CONTAINER-GATE-01 and 04H set insertion, 07H roster self seed; this is a producer/consumer join, not rediscovery
- evidence_kind: historical original ASM STATIC / INFERRED / runtime VERIFY
- original_golden_status: PASS 0 / strict MATCH 0 / DYNAMIC 0
- formal_ready_status: new B READY0; MASTER formal update0
- intake_stage: PUBLISHED_INTAKE only on exact GitHub readback; NOT_CURATED

## Historical source-grounded facts and proof limits

Old original-ASM traces the **actual 4-byte pointer-key vector producer** feeding two conditionally populated temporary integer-key sets. After `0x493A59→0x44D730` and `0x493A7B→0x47BB50`, it obtains an original object pointer, invokes `0x493A9E→0x5882F0`, and receives a vector seeded by that object and extended by successfully resolved names from the object's `+0xD4/+0xD8` 0x1C-stride records. For N>=1, it inserts this same vector range through `0x493AD1→0x498EE0` to first set; for N==2, `0x493AF4` additionally inserts it into a **different** set. N0 inserts neither. The shared input vector buffer is freed and its begin/end/cap slots zeroed after insertion; set nodes retain copied 32-bit KEY VALUES, not addresses into freed vector storage. This establishes one producer of pointer-valued keys, not all writers or final loyalty/retreat results. Miss in `0x467DE0` does NOT imply the different `0x5916E0` shared fallback succeeds, as they are distinct resolvers.

## Next validation / G4 caveat

Inspect 11H potential second-set consumer interpretation, preserve actual stack-offset delta and source pointer identity; compare native V9/old owner and source SHA before official curation. This is a sanitized re-usable B-owned study with actual original report SHA, not new independent original-game test, ABI closure or external battle result post-commit proof. Dedicated curator alone may admit verified semantic facts into develop REF/dictionary. No game EXE/DAT/SAVE/ZIP, generated DB, private paths or refused content uploaded.
