# B-20261030-19H-T013-EQUAL-RANGE-ERASE-01 — B historical targeting source intake

- research_id: `B-20261030-19H-T013-EQUAL-RANGE-ERASE-01`
- owner: B
- tasks: T013 (T024 AI and T028 references, no ownership transfer)
- observed_at: 2026-10-30 19H JST
- source_relative_path: `data/T013_MODE2_EQUAL_RANGE_ERASE_NATIVE_20261030_19H.md`
- source_sha256: `034eebc1521c16f9eb77f500e9579ccf4c7db3744f82bf478a1f858e41b705e8` (authorized PC Markdown SHA256/byte size independently measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target, not a fresh EXE hash in this intake)
- evidence_va_call_offsets: `0x579AA0,0x579AA2,0x579AB6/0x579AB8/0x579AF3,0x579B07/0x579B0D/0x579B0F/0x579B13 RET8,0x44C3D2/0x44C3D6,0x44C550/0x44C554,0x510850→0x44D0D0 or 0x510C20`
- prior_ids_and_corrections: B-20261030-17H shuffle and 18H range insertion existing; this study CORRECTS any interpretation of 0x579AA0 as a candidate-registration writer
- evidence_kind: historical STATIC native/callgraph / INFERRED, VERIFY for ABI/runtime/result; original DYNAMIC 0
- golden_status: original Gameplay PASS0, strict MATCH0
- ready_status: new READY0; E MASTER formal promotion0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; not CURATED

## Reusable source-grounded findings

Old original-PE ASM identifies `0x579AA0` as a **read-only equal-key tree-range finder**, not the tree registration procedure mistakenly suggested by older abstract labels. It searches a key comparable with `node+0x0C` using unsigned comparisons, and returns two iterator-like values through an output pair at `0x579B0D` and `0x579B0F` before `RET 8`. The two caller sites `0x44C3D6` and `0x44C554` each pass a payload key pointer from temporary distance-tree node `+0x18`, not an arbitrary pointer to a Unit. Later range erase `0x510850` may choose full-range or partial deletion by actual returned boundaries. **A separate T028 postretreat 09H caller has a proven full-range branch; this T013 caller does NOT inherit that proof**. Key ordering/duplicates, actual selected target and runtime ownership remain VERIFY.

## Next verification and safety constraints

Review 20H conditional refill on empty result, verify native EAX hidden key pointer and range lifetime, preserve 09H caller-specific proof separately. Curator must independently check permitted original V9 ASM/DAT and prior B/other owner corrections before REF/typed dictionary/develop semantic adoption; no raw EXE/DAT/SAVE/ZIP, generated DB, private path or refused material is included. A B intake summary is not a gameplay Golden or G4 battle-result writeback proof.
