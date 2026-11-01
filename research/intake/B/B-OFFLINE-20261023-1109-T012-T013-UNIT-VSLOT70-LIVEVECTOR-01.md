# Virtual slot +0x70 dispatch by Unit type and live-vector traversal

- research_id: `B-OFFLINE-20261023-1109-T012-T013-UNIT-VSLOT70-LIVEVECTOR-01`
- tasks: T012 / T013
- source_relative_path: `data/B_T012_T013_VSLOT70_LIVE_VECTOR_OFFLINE_20261023_1109.md`
- source_sha256: `f5e50129239f25d03e263be4c357a06ca2fd5e134f414aea78f353308d7285de` (actual authorized PC text hash, matched recovered source manifest)
- prior_ids_and_relationships: B-OFFLINE-20261023-0909-T012-T013-DUAL-POOL-RANGE-FANOUT-01; B-OFFLINE-20261023-1017-T012-T013-ALLFUNC-HITCTX-EXP-REARM-01; no unverified prior correction is overridden
- supersedes: none asserted; existing conflicting findings require curator errata review
- owner: B
- observed_source_status: historical owner study, STATIC / INFERRED / VERIFY; no new source discovery in this intake
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous verified source identification, not a new PE rehash in this run)
- verified_at: 2026-11-02 JST; original report SHA-256 recalculated from authorized PC text bytes and matched the safe recovery manifest
- golden_status: original game PASS 0; strict MATCH 0; DYNAMIC 0
- ready_status: newly confirmed READY 0; E MASTER formal promotion 0
- intake_status: PUBLISHED_INTAKE only after GitHub exact-text readback; NOT automatically CURATED
- safety: excluded pre-existing denied evidence and protected ranges; no prohibited payload, raw game assets or private paths
- limitations: This is a sanitized re-usable summary of an old source report. It does not prove live gameplay, exact ABI, object lifetime or G4 postbattle writeback. Curator must compare the current develop REF/dictionaries, source correction lineage and original ASM before admitting any new semantics.

## Preserved source findings
- Historical original-byte report identified `0x551146/0x551148/0x551154` as an indirect call through `[vptr+0x70]` inside `0x550E70`. Do **not** rewrite as a unique direct E8 call.
- Historical RTTI/vtable matches: Unit `vptr=0x63A9E4` → `0x578370`; SimpleUnit `0x63A4BC` → `0x544790`; StaticUnit `0x63A85C` → `0x55ABA0`; SimpleStaticUnit `0x63A8E4` → `0x55B060`, all at virtual offset `+0x70`.
- The source discusses HP field `+0x90` and distinct death/owner cleanup paths, but these four legal static alternatives are not exhaustive runtime dispatch proof. Target type, live vector mutation, event order and later EXP or battle settlement remain VERIFY.

## Minimal reproduction/check
Using source report and current authorized V9/native ASM, check the indirect instruction and each RTTI/vtable slot, then trace each callee's conditional writes/readers without invoking disallowed ranges. Compare legal original-game Unit/SimpleUnit/StaticUnit cases for dynamic claims. G4 death and cleanup boundary is NOT established.
