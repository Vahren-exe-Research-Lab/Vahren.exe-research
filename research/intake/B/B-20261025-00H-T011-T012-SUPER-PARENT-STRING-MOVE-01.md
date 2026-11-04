# B-20261025-00H-T011-T012-SUPER-PARENT-STRING-MOVE-01 — B owner historical evidence intake

- research_id: `B-20261025-00H-T011-T012-SUPER-PARENT-STRING-MOVE-01`
- owner: B
- tasks: T011/T012
- observed_at: 2026-10-25 00H JST
- source_relative_path: `data/T011_T012_SUPER_PARENT_STRING_OUTPARAM_MOVE_NATIVE_20261025_00H.md`
- source_sha256: `ea4a2d934d1aa422103b3dcae2e34e8f04d1eccfe7e34498aa0427fe225e4a79` (authorized PC Markdown bytes independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original PE; not rehashed on current intake)
- static_evidence_va_call_offsets: `0x502DD0,0x502E0B,0x503420,0x503440,0x505064,0x505099,0x5050A4,0x5050AB,0x405300, ScriptData+0x04/+0x14`
- prior_ids_and_remarks: B-20261024-22H-T011-T012-SUPER-PARSER-PRODUCER-01; B-20261024-2318-T011-T012-SUPER-COLON-CTOR-01; 21H super empty-name consumer
- evidence_kind: historical STATIC (Ghidra/original ASM where expressly attributed), INFERRED and VERIFY; no new dynamic gameplay
- golden_status: original game PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new READY0 / formal E MASTER0
- intake_status: OWNER_INTAKE; PUBLISHED_INTAKE requires exact GitHub readback; NOT CURATED

## Reusable owner findings

Historical original ASM shows `0x505099→0x502DD0` obtains a parent token through a **string output parameter** passed as ECX, with its pointer returned in EAX (`0x503420 MOV EAX,EBX`, `0x503440 RET`). The prior Ghidra `void` presentation of this parser misses that return protocol. `0x5050A1/0x5050A4/0x5050AB→0x405300` then transfers/copies the token string into a newly constructed ScriptData object's `+0x04` string container, with character length at `ScriptData+0x14`. That layout connects the older getter's empty-`super` name condition to a potential producer, not a proven exact instance/parent chain. Subsequent `0x5050FF` obtains a NEW token after registration; do not treat that as the same parent name. Original game effects/exception/alias remain VERIFY.

## Validation boundary

Validate native return/outparam and the destination ScriptData type against V9 plus accepted DAT; do not infer class inheritance/EXP automatically. Historical source details are retained by the owner at the relative path and SHA above. This summary does not itself independently prove a native ABI, original-game compatibility, G4 external-result settlement or Unit ownership semantics. Dedicated curator must reconcile old IDs, source/native evidence, DAT and corrections before any REF/dictionary/develop admission. No raw game assets, private user path, large DB or previously refused operation output are included.
