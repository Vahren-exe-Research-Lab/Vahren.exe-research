# B-20261031-22H-T013-ALT-LIST-DRAIN-RESET-ORDER-01 — B historic T013 source intake

- research_id: `B-20261031-22H-T013-ALT-LIST-DRAIN-RESET-ORDER-01`
- owner: B
- tasks: T013 (Unit candidate lists / target-selection prerequisites)
- observed_at: 2026-10-31 22H JST
- source_relative_path: `data/T013_22H_DOUBLE_RESET_CHAIN_NATIVE_20261031.md`
- source_sha256: `5f449d9340f19a8f2a67b154cdc207b499eb2e402301e7695d2825c560dbf464` (2026-11-02 JST authorized PC original Markdown SHA256/byte-length verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no new executable hash during intake)
- evidence_va_call_offsets: `0x57DE95→0x4C1860,0x57DEBF/0x57DEC5;0x57DECB→0x576660,0x576661/673/67E/693,Unit+0x186B0/+0x186B4,0x57DED8 E9→0x543DE0,Unit+0x186BC/+0x186C0/+0x186C4`
- prior_ids_and_corrections: B-20261031-21H-T013-FIRST-NODE-SENTINEL-TO-COORD-01; old separate list reset sources, 23H resolves 0x4C1860 BOOL. Crucial: E9 tail JMP, not CALL.
- evidence_kind: historical source STATIC original ASM / V9 CALL and INFERRED, VERIFY for interpretation; original game DYNAMIC=0
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / no E MASTER formal update
- intake_status: PUBLISHED_INTAKE on exact GitHub readback; NOT_CURATED until independent KB review

## Reusable historical evidence

Old bounded x86 after a true `0x57DE95→0x4C1860` conditional sets `Unit+0x186C8/+0x186CC` then passes PUSH1 to `0x576660` at `0x57DECB`; the subsequent `0x57DED8` is an **E9 tail JMP to `0x543DE0`**, NOT a call. In the list routine, input flag 1 clears **separate** linked list head `Unit+0x186B0` and count `Unit+0x186B4`, freeing all old nodes, while flag 0 removes only the first node and decrements the count. These `+0x186B0/B4` fields are distinct from the prior candidate-list `+0x18650/+0x18654`. A post-clear optional path checks `+0x8C,+0x1F8,+0x186B4,+0x5F0` and invokes further virtual callbacks/field updates, not guaranteed in all cases. Tail `0x543DE0` resets independent `+0x186C0/+0x186C4` to `0x80000008` and `+0x186BC` to 0; it does NOT itself reset the earlier `+0x186C8/+0x186CC`. Native list effects and final target remain VERIFY.

## Provenance and next verification

Reconcile separate list identities and permitted vtable side effects, evaluate 23H rect gate, and verify source/consumer of +0x186C8/CC before formal structure names. This owner-created sanitized summary references the real B source by relative path and measured SHA. It does not constitute new full decompilation, original-game execution, G4 external battle-result settlement or verified final target. Dedicated curator alone may interpret REF/typed dictionary/develop based on independent native/DAT and errata audit; original game files, large index, private paths and refused payloads are excluded.
