# B-20261025-0312-T011-TOKEN-POSTBRACE-AT-DISPATCH-01 — B owner historical evidence intake

- research_id: `B-20261025-0312-T011-TOKEN-POSTBRACE-AT-DISPATCH-01`
- owner: B
- tasks: T011/T012
- observed_at: 2026-10-25 03H JST
- source_relative_path: `data/T011_PARENT_BRACE_NEXT_TOKEN_AT_BRANCH_NATIVE_20261025_03H.md`
- source_sha256: `b17fb5c04b66517e327da58e9f58157d6d1ae8a939a5ba70e16cb1d97e47d0f0` (authorized PC Markdown bytes independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original PE; not rehashed on current intake)
- static_evidence_va_call_offsets: `0x50B8E6,0x50BA65,0x50BAC7,0x50BAD4,0x50BAE9,0x50BAF0,0x50B4C0,0x50B4FB,0x50B508,0x62CF54`
- prior_ids_and_remarks: B-20261025-0210-T011-SUPER-BRACE-RETURN-ABI-01; 01H brace error gate was already known
- evidence_kind: historical STATIC (Ghidra/original ASM where expressly attributed), INFERRED and VERIFY; no new dynamic gameplay
- golden_status: original game PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new READY0 / formal E MASTER0
- intake_status: OWNER_INTAKE; PUBLISHED_INTAKE requires exact GitHub readback; NOT CURATED

## Reusable owner findings

Historical original ASM follows the successful `0x5049E0` result to an upper parser token read `0x50BAD4→0x502DD0`, followed by `0x50BAE9` testing token-string length. Empty token length leads to cleanup and `EAX=0` return; nonempty dispatches to `0x50B4C0` general token processing. There, `0x50B4FB→0x426490` is supplied the literal `"@"` (source raw bytes `40 00` at `0x62CF54`), with result compared against -1 near `0x50B508`. The report **does not prove** all semantics of the search, EOF, nested parent syntax, or actual Skill load. It specifically distinguishes this 03H continuation from the earlier brace validation/return ABI and defers generic parser internals to the proper owner.

## Validation boundary

Verify bounded V9 parser CALL and allowed DAT token grammar, cross-link with earlier 01H/02H, never infer real summon/EXP behavior from parser branch alone. Historical source details are retained by the owner at the relative path and SHA above. This summary does not itself independently prove a native ABI, original-game compatibility, G4 external-result settlement or Unit ownership semantics. Dedicated curator must reconcile old IDs, source/native evidence, DAT and corrections before any REF/dictionary/develop admission. No raw game assets, private user path, large DB or previously refused operation output are included.
