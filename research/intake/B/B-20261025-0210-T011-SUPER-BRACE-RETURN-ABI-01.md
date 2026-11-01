# B-20261025-0210-T011-SUPER-BRACE-RETURN-ABI-01 — B owner historical evidence intake

- research_id: `B-20261025-0210-T011-SUPER-BRACE-RETURN-ABI-01`
- owner: B
- tasks: T011/T012
- observed_at: 2026-10-25 02H JST
- source_relative_path: `data/T011_SUPER_BRACE_STATUS_RETURN_ABI_NATIVE_20261025_02H.md`
- source_sha256: `f427da40bc490c0dda1076c31ca8ccad959e20aa9ad3728a7f11218c141a2100` (authorized PC Markdown bytes independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original PE; not rehashed on current intake)
- static_evidence_va_call_offsets: `0x505137,0x505139,0x50513B..0x505179,0x50517D..0x5051E2,0x505200,0x50B8E6,0x50BA65,0x50BA69,0x50BB40`
- prior_ids_and_remarks: B-20261025-0110-T011-SUPER-LBRACE-PARSER-GATE-01; later B-20261025-0312-T011-TOKEN-POSTBRACE-AT-DISPATCH-01
- evidence_kind: historical STATIC (Ghidra/original ASM where expressly attributed), INFERRED and VERIFY; no new dynamic gameplay
- golden_status: original game PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new READY0 / formal E MASTER0
- intake_status: OWNER_INTAKE; PUBLISHED_INTAKE requires exact GitHub readback; NOT CURATED

## Reusable owner findings

Historical bounded original ASM refines the brace-gate's status ABI: on the observed nonzero comparison branch, parser `0x5049E0` performs temporary string cleanup and returns `EAX=0` through common `0x505200 RET`; on the error branch beginning `0x50517D`, an error/message object candidate is allocated, and `0x5051E0 MOV EAX,EDI` returns a potential non-null pointer. Its owner `0x50B220` calls `0x5049E0` at `0x50B8E6`, tests result at `0x50BA65..0x50BA69`, and on nonzero may cleanup and return early rather than continuing token processing. Success returns to the upper parser loop, not a proof that `0x5049E0` itself parses the full block. Exception, actual comparison polarity, all callers and real DAT inputs remain VERIFY.

## Validation boundary

Check current permitted V9 entry/exit CALL sites and status propagation; compare with 03H continuation without assuming runtime error handling is exhaustive. Historical source details are retained by the owner at the relative path and SHA above. This summary does not itself independently prove a native ABI, original-game compatibility, G4 external-result settlement or Unit ownership semantics. Dedicated curator must reconcile old IDs, source/native evidence, DAT and corrections before any REF/dictionary/develop admission. No raw game assets, private user path, large DB or previously refused operation output are included.
