# B-20261030-0215-T028-SPOT-TREE-ERASE-STRING-RELEASE-01 — B/T028 historical retreat evidence intake

- research_id: `B-20261030-0215-T028-SPOT-TREE-ERASE-STRING-RELEASE-01`
- owner: B
- tasks: T028 (T011/T013/T024 related, no owner takeover)
- observed_at: 2026-10-30 02H JST
- source_relative_path: `data/T028_SPOT_TREE_ERASE_STRING_RELEASE_NATIVE_20261030_02H.md`
- source_sha256: `1c95d49a632f3c27b800c774e6ca738a4cf58116d96709587fdc8823225f5aaf` (authorized PC original Markdown byte SHA256/length measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historic source target; executable not newly hashed in this intake)
- native_va_call_offsets: `0x4160F4/0x416150/0x4161D9→0x402C40;node+0x1C/+0x20 (length/capacity);0x416220/0x416224..0x41622F,0x41646A..0x41648F,0x4164A2..0x4164A7`
- prior_ids_and_corrections: B-20261030-0113-T028-SPOT-INDEX-EQUALRANGE-ERASE-01; 03H separate full-tree destructor
- evidence_kind: historical STATIC original x86/Ghidra, INFERRED/VERIFY on high-level state; no original DYNAMIC
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; NOT_CURATED

## Reusable source-grounded findings

Old original-PE byte report connects the Spot-like tree equal-key search with a **small-string-optimized key comparator**. At `0x4160F4,0x416150,0x4161D9` it calls an earlier-known bytewise comparator `0x402C40`; node string length `+0x1C` and capacity `+0x20` decide inline vs heap storage (capacity threshold `0x10`). Partial erase helper `0x416220` checks a nil/invalid iterator candidate at `0x416224`; for valid nodes it frees a separate string heap buffer at `0x416474` only when capacity>=16, resets capacity/length/inline data and frees the node at `0x41648F`. It decrements tree count near `0x4164A6` only under a nonzero test. This is a STATIC per-node destruction contract; key encoding, validity, exception behavior and live state are VERIFY. Earlier `0x402C40` byte comparator body is not a new finding here.

## Validation and G4 restrictions

Use 03H separately proven full-tree postorder recursion; check same-container ownership and whether Spot reservation count is managed independently. This preserves a safe summary with source ID/hash, not a newly verified end-to-end battle settlement. Original EXE, DAT, SAVE, MAP, large V9 index, identity and previously refused content are not published. Dedicated curator must recheck permitted V9 and native/old REF/corrections before adding canonical semantics; static CALL and cleanup path are not game Golden proof.
