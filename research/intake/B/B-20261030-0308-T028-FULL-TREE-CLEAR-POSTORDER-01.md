# B-20261030-0308-T028-FULL-TREE-CLEAR-POSTORDER-01 — B/T028 historical retreat evidence intake

- research_id: `B-20261030-0308-T028-FULL-TREE-CLEAR-POSTORDER-01`
- owner: B
- tasks: T028 (T011/T013/T024 related, no owner takeover)
- observed_at: 2026-10-30 03H JST
- source_relative_path: `data/T028_SPOT_FULL_TREE_CLEAR_RECURSIVE_DESTRUCTOR_NATIVE_20261030_03H.md`
- source_sha256: `2ce7a4f828c2d749e30e63e7b78a46a8a5b3dec06e535f5a79f1db2fb201ab52` (authorized PC original Markdown byte SHA256/length measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historic source target; executable not newly hashed in this intake)
- native_va_call_offsets: `0x415CF0 full-range gate→0x415D0A→0x416870;0x41687E..0x4168BF;0x416889 recursive call;0x41688E/0x416899→0x5B6BBB;0x4168B0→0x5B6BBB;0x415D0F..0x415D23`
- prior_ids_and_corrections: B-20261030-0113-T028-SPOT-INDEX-EQUALRANGE-ERASE-01 (full gate); B-20261030-0215-T028-SPOT-TREE-ERASE-STRING-RELEASE-01 (partial-node destroy distinct)
- evidence_kind: historical STATIC original x86/Ghidra, INFERRED/VERIFY on high-level state; no original DYNAMIC
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; NOT_CURATED

## Reusable source-grounded findings

Historical original-PE static check follows `0x415CF0` full-range branch `0x415D0A→0x416870` into a **tree-wide destruction routine**. Nil/sentinel node stops at `0x41687E/0x416881`; valid nodes recurse down one branch via `0x416889→0x416870` and traverse the other iteratively, conditionally freeing a heap string on node capacity>=16 then freeing node pointer at `0x4168B0`. The wrapper restores all header links to the head sentinel and sets total count to 0 at `0x415D23`, rather than decrementing the tree count for every node. The 02H partial-node eraser `0x416220` is NOT the helper directly invoked on this full-range path. This cleanup alone has no observed `Spot+0xB8` decrement: Spot reservation release occurs elsewhere. All allocated-object aliasing, malformed trees and full visible retreat behavior are VERIFY.

## Validation and G4 restrictions

Check original native pointers/allocator lifecycle in permitted scope and future afterbattle Spot counter state; do not infer successful external battle result settlement. This preserves a safe summary with source ID/hash, not a newly verified end-to-end battle settlement. Original EXE, DAT, SAVE, MAP, large V9 index, identity and previously refused content are not published. Dedicated curator must recheck permitted V9 and native/old REF/corrections before adding canonical semantics; static CALL and cleanup path are not game Golden proof.

## 2026-11-04 B owner → curator curation-status reconciliation

The **historical owner-intake status above is a time-stamped state**. The current private `develop/REF_BATTLE_AI_MORALE.md` (Git blob `e104daced8f6ec69c1f3ee9e291a00234ddbdbb5`, GitHub readback 2026-11-04 JST) independently lists this **same existing study ID** as `CURATED_STATIC` for strictly bounded original-x86 evidence, with source-report SHA-256 `2CE7A4F828C2D749E30E63E7B78A46A8A5B3DEC06E535F5A79F1DB2FB201AB52` matching this historical owner's recorded report SHA. [Curated semantic entry](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/develop/REF_BATTLE_AI_MORALE.md) is authoritative for exact native receipts and any corrections; this owner note is a historical source, not a second adopted finding.

**Precisely scoped link:** `0x416870` is the independently checked **full-tree** recursion/iteration teardown reached from a full-range branch. The wrapper restores sentinel links and clears the container count in bulk; this is distinct from 02H partial-node erase and proves no `Spot+0xB8` reservation decrement.

**Current stages:** `PUBLISHED_INTAKE` already existed; `CURATED_STATIC` is a **curator's pre-existing adoption**, not newly achieved by this B-owner update. No new ID, new PUBLISHED_INTAKE, new CURATED, original-game Golden PASS, strict MATCH, or new formal READY is claimed here (all **0** for this B-owner update). Runtime effects, complete native ABI, G4 external-result commitment, and original gameplay remain VERIFY/NOT PASSED. Curator's independently checked source/native hashes are cited from its report; original research PC remeasurement was **unavailable** to B owner in this run (`Session terminated`). Previously denied index, `B_AI_ENTRY.md`, and protected operations remain BLOCKED, untouched; no alternate-route retry.
