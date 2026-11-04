# B-20261030-1615-T013-MODE2-PAIRWISE-DISTANCE-TREE-01 — B/T013 historical mode selection evidence

- research_id: `B-20261030-1615-T013-MODE2-PAIRWISE-DISTANCE-TREE-01`
- owner: B
- tasks: T013 (T024 AI and T028 side effects as references only)
- observed_at: 2026-10-30 16H JST
- source_relative_path: `data/T013_MODE2_PAIRWISE_DISTANCE_TREE_NATIVE_20261030_16H.md`
- source_sha256: `af6fd09492bfbf89084ad2daa49fe80ce89fd2abbb67606507d5345000dee282` (research-PC original Markdown SHA256/byte count checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target, no fresh EXE hash now)
- evidence_va_call_offsets: `0x44C068/0x44C0FE;0x44C114..0x44C169;0x44C16F/0x44C173/0x44C178;0x44C185→0x5E3B70;0x44C1AD→0x44D630;0x44C1BC→0x44D1C0;0x44C1C8/0x44C1D5/0x44C1EA;node+0x10(double)/+0x18(payload)`
- prior_ids_and_errata: B-20261030-15H-T013-MODE2-ALT-DUALFLAG-MODE3-01 subpath; 17H follows candidate-tree output with shuffling
- evidence_kind: historical native STATIC / Ghidra-indexed CALL, INFERRED where identified; gameplay and ABI VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0; no E MASTER update
- intake_status: owner-only PUBLISHED_INTAKE after exact GitHub readback, NOT_CURATED

## Reusable source finding

Original x86 source observes a nonzero candidate-scratch branch `0x44C068→0x44C0FE` traversing **two temporary trees** and pairs of selected group Unit pointers. For each pair it computes signed32 coordinate deltas at offsets `+0x220/+0x224`, squares and sums them in 32-bit integer arithmetic, converts through FILD and calls `0x5E3B70` before storing a double-like tree key. The source warns this CALL **does not alone prove sqrt semantics**. Node allocation `0x44C1AD→0x44D630` places a double key at `node+0x10` and pointer payload at `+0x18`; `0x44C1BC→0x44D1C0` inserts with double comparator, and an equal-key branch can destroy a node, so same-distance pairs are not necessarily all preserved. An additional insert is gated by manager `+0xA7` and two Unit `+0x1A4` values. Overflow, aliasing, identity, final target and live distance meaning VERIFY.

## Limits and next verification

Review 17H vector conversion/shuffle and 19H equal-range erase; do not identify the temporary distance key as a guaranteed shortest-target selection. Native V9/allowed DAT, original owner SHA, earlier revisions, and other lanes must be reviewed by dedicated KB curator before any semantic REF/typed dictionary/develop promotion. This is a sanitized historical B-owner summary rather than a new original-game test or G4 result commit. Original executable, scripts, saves, identity, huge DB and refused payloads remain excluded.
