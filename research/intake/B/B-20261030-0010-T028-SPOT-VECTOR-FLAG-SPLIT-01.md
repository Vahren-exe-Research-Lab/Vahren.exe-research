# B-20261030-0010-T028-SPOT-VECTOR-FLAG-SPLIT-01 — B/T028 historical retreat evidence intake

- research_id: `B-20261030-0010-T028-SPOT-VECTOR-FLAG-SPLIT-01`
- owner: B
- tasks: T028 (T011/T013/T024 related, no owner takeover)
- observed_at: 2026-10-30 00H JST
- source_relative_path: `data/T028_SPOT_VECTOR_HELPER_FLAG_SPLIT_NATIVE_20261030_00H.md`
- source_sha256: `6f972cfb462306b9df4620768e3c212e391a4153d6110f5f5f6eec30dd53c9c6` (authorized PC original Markdown byte SHA256/length measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historic source target; executable not newly hashed in this intake)
- native_va_call_offsets: `0x495544→0x598450(flag0),0x495079→0x598450(flag0),0x5AC5E7→0x598450(flag1),0x5984DF/0x598591,0x5984C7→0x416080,0x5984DA→0x415CF0,0x495578/0x495580,Spot+0xB8`
- prior_ids_and_corrections: B-20261029-2315-T028-RETREAT-SPOT-RESERVATION-RELEASE-01 Spot +0xB8 decrement known; later B-20261030-0113-T028-SPOT-INDEX-EQUALRANGE-ERASE-01 proves flag0 still erases trees
- evidence_kind: historical STATIC original x86/Ghidra, INFERRED/VERIFY on high-level state; no original DYNAMIC
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; NOT_CURATED

## Reusable source-grounded findings

Historical original x86 shows retreat-side caller `0x495544→0x598450` passes flag0, while a separate postretreat mode1 caller `0x5AC5E7` passes flag1. The callee `0x598450` reads a vector of 0x1C-byte entries and always performs `0x5984C7→0x416080` plus `0x5984DA→0x415CF0` pair for element-related indexing **before the flag branch**. With flag0, additional per-entry resolver/destructor candidate `0x598534/0x598543/0x598555→0x463590` and an end-of-list `0x5985A5→0x463590` may be skipped; flag1 allows them conditionally. Therefore flag0 is NOT "no-op." In upstream retreat path, `0x495578` compares linked reference to Spot identity before `0x495580` decrements `Spot+0xB8`; this counter was already known and is not counted again. Does not establish logical move, persistence or original game state.

## Validation and G4 restrictions

Inspect 01H index-erase effect and later mode1 destructor corrections, verify each Spot capacity INC/DEC pair separately before G4 semantics. This preserves a safe summary with source ID/hash, not a newly verified end-to-end battle settlement. Original EXE, DAT, SAVE, MAP, large V9 index, identity and previously refused content are not published. Dedicated curator must recheck permitted V9 and native/old REF/corrections before adding canonical semantics; static CALL and cleanup path are not game Golden proof.

## 2026-11-04 B owner → curator curation-status reconciliation

This is **not a new research finding or an owner-side formal promotion**. The earlier `NOT_CURATED` label above describes the historical owner publication time. Private current `develop/REF_BATTLE_AI_MORALE.md` (Git blob `e104daced8f6ec69c1f3ee9e291a00234ddbdbb5`, read back 2026-11-04 JST) now independently accepts this **same existing ID** as `CURATED_STATIC` for bounded original-x86 facts, with curator-reported original source SHA256 `6F972CFB462306B9DF4620768E3C212E391A4153D6110F5F5F6EEC30DD53C9C6` matching this note's historical owner receipt. [Curated authoritative entry](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/develop/REF_BATTLE_AI_MORALE.md) holds the independently validated native bytes, CALL sites, correction lineage and exact limits.

**Disambiguation for AI reuse:** The original retreat helper's flag0 path does not suppress earlier preliminary/per-entry range-erase calls. The mode=1 flag1 path has separate conditional resolver/destructor handling. This is a bounded byte-level distinction; other callers, resource semantics and external results remain VERIFY.

**Status crosswalk:** pre-existing `PUBLISHED_INTAKE` plus pre-existing curator `CURATED_STATIC` (native-only). This B note does not newly promote any research ID, source publication, CURATED status, READY, gameplay Golden PASS or strict MATCH (all **0 new**). Original-game DYNAMIC, complete ABI, side effects and G4 external settlement still VERIFY/NOT PASSED. Research PC was unavailable during this B owner run (`Session terminated`), so the historical source PE/DAT/V9 SHA values are not freshly remeasured by B. The earlier refused catalog/VA lookup and `B_AI_ENTRY.md` writes, prohibited addresses and other owners were not accessed or retried via any alternative route.
