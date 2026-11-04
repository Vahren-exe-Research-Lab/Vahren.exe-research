# B-20261030-0113-T028-SPOT-INDEX-EQUALRANGE-ERASE-01 — B/T028 historical retreat evidence intake

- research_id: `B-20261030-0113-T028-SPOT-INDEX-EQUALRANGE-ERASE-01`
- owner: B
- tasks: T028 (T011/T013/T024 related, no owner takeover)
- observed_at: 2026-10-30 01H JST
- source_relative_path: `data/T028_SPOT_INDEX_EQUAL_RANGE_ERASE_NATIVE_20261030_01H.md`
- source_sha256: `98c6a37bf0ffdb2306ec939e3e262b7ae4a8091a6e71c4ea400e709244251b7e` (authorized PC original Markdown byte SHA256/length measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historic source target; executable not newly hashed in this intake)
- native_va_call_offsets: `0x598469/0x5984C7→0x416080;0x59847C/0x5984DA→0x415CF0;0x416080/0x4160A7/0x4160AB;0x415D0A→0x416870,0x415D8F→0x416220;0x5984DF`
- prior_ids_and_corrections: B-20261030-0010-T028-SPOT-VECTOR-FLAG-SPLIT-01; 02H and 03H detail partial/full range destroy
- evidence_kind: historical STATIC original x86/Ghidra, INFERRED/VERIFY on high-level state; no original DYNAMIC
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; NOT_CURATED

## Reusable source-grounded findings

Historical native caller/callee study shows `0x598450` performs an **initial equal-key lookup / erase-range pair** `0x598469→0x416080`, `0x59847C→0x415CF0` before even reading vector bounds. It repeats the lookup/erase pair per 0x1C-byte vector entry. Flag branch `0x5984DF` occurs AFTER those calls, so flag0 on retreat does not suppress these tree mutations, including with zero vector length (initial pair remains). `0x416080` returns two iterator-like boundaries (old native/string comparator study) and `0x415CF0` removes an actual tree range: when first/head and last/head align it calls full-delete `0x416870`, otherwise iterative partial-node deletion reaches `0x416220`. This is real STATIC mutation, not mere lookup; exact key type, duplicate handling, owner pointer identity and actual state consequences remain VERIFY.

## Validation and G4 restrictions

Link 02H partial key SSO disposal and 03H full-tree recursion, then lawful Spot count/retreat correctness observation. This preserves a safe summary with source ID/hash, not a newly verified end-to-end battle settlement. Original EXE, DAT, SAVE, MAP, large V9 index, identity and previously refused content are not published. Dedicated curator must recheck permitted V9 and native/old REF/corrections before adding canonical semantics; static CALL and cleanup path are not game Golden proof.

## 2026-11-04 B owner → curator curation-status reconciliation

This is **not a new research finding or an owner-side formal promotion**. The earlier `NOT_CURATED` label above describes the historical owner publication time. Private current `develop/REF_BATTLE_AI_MORALE.md` (Git blob `e104daced8f6ec69c1f3ee9e291a00234ddbdbb5`, read back 2026-11-04 JST) now independently accepts this **same existing ID** as `CURATED_STATIC` for bounded original-x86 facts, with curator-reported original source SHA256 `98C6A37BF0FFDB2306EC939E3E262B7AE4A8091A6E71C4EA400E709244251B7E` matching this note's historical owner receipt. [Curated authoritative entry](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/develop/REF_BATTLE_AI_MORALE.md) holds the independently validated native bytes, CALL sites, correction lineage and exact limits.

**Disambiguation for AI reuse:** The preliminary equal-range/erase pair executes before a vector-length check, and a comparable pair occurs per vector entry before the mode flag gate. The callee's full versus partial cleanup branches were separately refined by the already curated 02H/03H studies; flag0 does not imply a read-only/no-op index.

**Status crosswalk:** pre-existing `PUBLISHED_INTAKE` plus pre-existing curator `CURATED_STATIC` (native-only). This B note does not newly promote any research ID, source publication, CURATED status, READY, gameplay Golden PASS or strict MATCH (all **0 new**). Original-game DYNAMIC, complete ABI, side effects and G4 external settlement still VERIFY/NOT PASSED. Research PC was unavailable during this B owner run (`Session terminated`), so the historical source PE/DAT/V9 SHA values are not freshly remeasured by B. The earlier refused catalog/VA lookup and `B_AI_ENTRY.md` writes, prohibited addresses and other owners were not accessed or retried via any alternative route.
