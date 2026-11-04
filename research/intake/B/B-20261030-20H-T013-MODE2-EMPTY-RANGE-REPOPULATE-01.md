# B-20261030-20H-T013-MODE2-EMPTY-RANGE-REPOPULATE-01 — B historical targeting source intake

- research_id: `B-20261030-20H-T013-MODE2-EMPTY-RANGE-REPOPULATE-01`
- owner: B
- tasks: T013 (T024 AI and T028 references, no ownership transfer)
- observed_at: 2026-10-30 20H JST
- source_relative_path: `data/T013_MODE2_EMPTY_RANGE_REPOPULATE_NATIVE_20261030_20H.md`
- source_sha256: `cef83db32b3f4812cb6e8f195d35e9f33de4342bcdf211078c37e865db08539f` (authorized PC Markdown SHA256/byte size independently measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target, not a fresh EXE hash in this intake)
- evidence_va_call_offsets: `0x44C570..0x44C588,0x44C577/0x44C57B/0x44C57D/0x44C57E/0x44C57F/0x44C583→0x56F130;0x56F135/0x56F14E→0x44D2A0;0x56F153..0x56F1A6,0x44D2A0`
- prior_ids_and_corrections: B-20261030-19H-T013-EQUAL-RANGE-ERASE-01 (candidate delete), later 21H continues dispatch after refill
- evidence_kind: historical STATIC native/callgraph / INFERRED, VERIFY for ABI/runtime/result; original DYNAMIC 0
- golden_status: original Gameplay PASS0, strict MATCH0
- ready_status: new READY0; E MASTER formal promotion0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; not CURATED

## Reusable source-grounded findings

Historic original ASM demonstrates an **empty-tree fallback** after the selected equal-range deletion: when the working tree count becomes zero, `0x44C577..0x44C583` passes another source tree's begin/end into `0x56F130`, and nonempty cases skip directly to `0x44C588`. Callee `0x56F130` returns immediately for an empty source range; otherwise it visits successive source nodes, passing key/payload to `0x44D2A0` insertion candidate. Thus a depleted working candidate tree can be repopulated from a retained source range. This neither proves the source and destination represent distinct runtime objects nor that a unique final target is chosen. Original source contains a decompiler hidden-register warning and a `RET8` calling boundary; do not trust a guessed three-argument C signature.

## Next verification and safety constraints

Validate 19H key-range result and 21H post-refill cleanup/dispatch against V9, determine whether actual source records can be recycled without double-ownership. Curator must independently check permitted original V9 ASM/DAT and prior B/other owner corrections before REF/typed dictionary/develop semantic adoption; no raw EXE/DAT/SAVE/ZIP, generated DB, private path or refused material is included. A B intake summary is not a gameplay Golden or G4 battle-result writeback proof.
