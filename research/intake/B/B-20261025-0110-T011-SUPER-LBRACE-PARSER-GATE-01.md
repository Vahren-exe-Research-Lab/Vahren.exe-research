# B-20261025-0110-T011-SUPER-LBRACE-PARSER-GATE-01 — B owner historical evidence intake

- research_id: `B-20261025-0110-T011-SUPER-LBRACE-PARSER-GATE-01`
- owner: B
- tasks: T011/T012
- observed_at: 2026-10-25 01H JST
- source_relative_path: `data/T011_SUPER_LBRACE_GRAMMAR_GATE_NATIVE_20261025_01H.md`
- source_sha256: `f3f37bac36b005d8aadbf880f07ff5d3bf6460449f0d679960e2374e6c7f15a3` (authorized PC Markdown bytes independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original PE; not rehashed on current intake)
- static_evidence_va_call_offsets: `0x6020D0,0x62C430,0x65DB28,0x5050FF,0x505107,0x505113,0x505137,0x505139,0x50517D,0x50519B`
- prior_ids_and_remarks: 22H super parser, 23H ':' token constructor, 00H parent token; later 02H return ABI corrects status propagation
- evidence_kind: historical STATIC (Ghidra/original ASM where expressly attributed), INFERRED and VERIFY; no new dynamic gameplay
- golden_status: original game PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new READY0 / formal E MASTER0
- intake_status: OWNER_INTAKE; PUBLISHED_INTAKE requires exact GitHub readback; NOT CURATED

## Reusable owner findings

Old original-PE byte report shows a static constructor `0x6020D0` assigning raw `"{"` (byte `7B 00` at `0x62C430`) to a string object `0x65DB28`. After the already-known colon/parent ScriptData creation, parser `0x5050FF` reads the next token, `0x505113` calls a token comparison, and `0x505137/0x505139` branches on the comparison result. One branch `0x50517D..0x50519B` constructs an error-reporting object associated with missing `"{"` syntax. Exact callee comparison polarity and end-to-end legal grammar are **not proven** by the owner study; it only supports a bounded post-parent brace check and error path. Later 02H study resolves the caller-visible return path. No forbidden callee interior inspected here.

## Validation boundary

Cross-check permitted V9 CALL and brace lexical producer; take 02H success/error-return correction as higher authority and inspect DAT grammar only if safe. Historical source details are retained by the owner at the relative path and SHA above. This summary does not itself independently prove a native ABI, original-game compatibility, G4 external-result settlement or Unit ownership semantics. Dedicated curator must reconcile old IDs, source/native evidence, DAT and corrections before any REF/dictionary/develop admission. No raw game assets, private user path, large DB or previously refused operation output are included.
