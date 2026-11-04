# B-20261028-0410-T028-TEMP-SET-INSERT-ABI-01 — B historical T028 battle state intake

- research_id: `B-20261028-0410-T028-TEMP-SET-INSERT-ABI-01`
- owner: B
- tasks: T028 (battle side, candidate/event prerequisites)
- observed_at: 2026-10-28 04H JST
- source_relative_path: `data/T028_TEMP_SET_INSERT_ABI_NATIVE_20261028_04H.md`
- source_sha256: `ab31afd5b811219e62525f053f0aa08b100b6935db776551eea297adceede76c` (authorized-PC report actual SHA256 and byte size measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target only; no fresh executable hash)
- native_evidence_va_call_offsets: `0x498EE0/0x498EE7/0x498F70..0x498F7F,0x498F00/0x498F24/0x498F47→0x565780,0x498F11/0x498F35/0x498F58→0x40EBE0,0x498F65→0x5AF0F0,node+0x0C,size+0x08`
- prior_ids_and_corrections: B-20261028-0317-T028-TREEFLAG-DUAL-CONTAINER-GATE-01 (2 callsites) and older generic RB tree operations; no duplicate known insert helper facts
- evidence_kind: historical original x86 STATIC / V9 saved pseudo-C / INFERRED, VERIFY for full runtime meaning
- golden_status: original Gameplay PASS0 / strict MATCH0 / dynamic0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE when exact readback, NOT_CURATED

## Source-grounded findings

Historical original native identifies `0x498EE0` as **integer-key range insertion into a temporary RB-tree-like set**. It consumes uint32 key begin/end pointers, returns for empty range, iterates 4-byte entries and uses this-like set pointer in EAX. `0x565780` allocates 0x14-byte node with key copied into node `+0x0C`, `0x40EBE0` links node and increments container count `+0x08`; if tree is nonempty it attempts fast insertion at bounds or general `0x5AF0F0` duplicate-sensitive insertion, with an outparam result node+flag. The count increase is **set member count**, not death count, morale or experience. The 03H caller supplies two different temporary set objects based on N from tree flags, but which gameplay values they represent is VERIFY.

## Next validation

Track the producers and consumers of two temporary sets, exact duplicate key effects, permitted V9 x86 and legal original-game side selection. Owner B source is the referenced relative path and SHA; the sanitized note is not a new executable/dynamic game test or G4 settlement contract. Curator must independently inspect permitted V9 source, DAT, prior versions and ownership before updating REF/symbols/structs/develop. No original assets, private paths, massive DB or previously denied payloads have been uploaded.
