# E/T018–T020: dialog pre-dispatch string selection and Golden run-ID synthetic gate (sanitized historical research)

- research_id: `E-OFFLINE-20261028-1849-T020-PREDIALOG-EXPR-GOLDEN-RUN-ID-GATE-01`
- owner: E; tasks: T020, T018; T019 has no newly confirmed contradiction
- source_relative_path: `tests/E_OFFLINE_SYNC_20261029/T020_DIALOG_PREDISPATCH_GOLDEN_RUN_ID_AUDIT_20261028_1849.md`
- source_sha256: `B80A9B6397A54ECFEA304B2E63B6E9859076C37B978FEC223DCD9B5A7F9E1507` (8,462 bytes; authorized-PC file independently rehashed 2026-11-02 JST)
- original_observed_at: 2026-10-28 18:49 JST; static_source_epoch: 2026-10-21 offline Ghidra SQLite (historical, NOT live V9 remeasurement)
- evidence_kind: `STATIC-OLD-INDEX / SYNTHETIC / VERIFY`; original_native_dynamic: `NOT_RUN`; actual_golden_pass: `0`; strict_match: `0`; new_formal_ready: `0`; native_T019_new_contradictions: `0`
- prior_ids: E's 2026-10-28 17:45 dialog registry gate, with B native source reported only as read-only provenance; see also [source excerpt crosswalk](E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART1-20261102.md).
- correction_relation: distinct pre-dispatch input selection and same-run evidence requirements; later 19:49 / 20:45 / 21:49 synthetic admission gates **strengthen** rather than validate original-game output.

## Historic bounded static E analysis

The original E report states a direct-call chain in the **old** index: `0x0052CF50` call site `0x0052D047 → 0x0043F470`; in `0x0043F470`, call sites `0x0043F5A4 → 0x0049C450`, `0x0043F72F → 0x00416E80`, and `0x0043F73F → 0x00416B90`. The input string selection helper `0x0049C450` was reported with **8 different direct callers and 144 call edges** in that historical database; it is **not** demonstrated to belong exclusively to wandering/mercenary UI. The older pseudocode placed the helper before the branch labeled `decide11` and before dialog node registration. Three possible upstream string input branches were modeled using the helper's `param_1 + 0x14`, `+0x28/+0x2C` and alternate pointer checks; no live game activation path was observed. Original report sections “今回新規に確定した静的呼出し” and “T020比較fixture・T018同一run拘束”, approximately lines 11–37, under the pinned source SHA. Independently verify native CALL bytes/ABI against the current authorized V9 before elevating beyond historical `STATIC-OLD-INDEX`.

## Synthetic gate, limitations and next steps

The historical owner fixture checked seven direct-call aspects, four negative mislinks, seven conditional input cases and eight same-battle correspondence cases, with **36/36 historical synthetic/static checks PASS** and **110/110 cumulative archived checks**. These are NOT new rerun results. Golden G0/G1/G2 requires **actual** original game evidence bound to the same independent battle ID (not merely a self-asserted `same_battle_key`): G0 lawful UI, immediate G1 unmodified SAVE/input, G2 actual MAP/three-sided ordered Unit/Troop with provenance. This report confirms no gameplay, UI display, ABI, attack, or World effect; G0/G1/G2 lawful same-run evidence remains absent. No blocked source or private user path is included. Further corrections: [19:49 wrapper source](E-OFFLINE-20261028-1949-T020-DIALOG-WRAPPER-FINGERPRINT-AND-GOLDEN-LINEAGE-01.md), [20:45 hash-binding](E-OFFLINE-20261028-2045-T018-T020-GOLDEN-LINEAGE-CONTENT-BOUND-01.md), [21:49 semantic-binding](E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01.md).
