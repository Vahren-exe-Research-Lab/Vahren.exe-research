# E/T018–T020: Golden lineage content-binding gate (historical owner report, sanitized)

- research_id: `E-OFFLINE-20261028-2045-T018-T020-GOLDEN-LINEAGE-CONTENT-BOUND-01`
- owner: E; tasks: T018, T020 (T019 classification only)
- source_relative_path: `tests/E_OFFLINE_SYNC_20261029/T020_GOLDEN_LINEAGE_CONTENT_BOUND_AUDIT_20261028_2045.md`
- original_source_sha256: `5EB696F60F9255DC3E08F630011754B02571EC10C3FBAFF95723F67E8DF44A2B` (7,296 bytes; original authorized research PC rehashed 2026-11-02 JST)
- observed_at: 2026-10-28 20:45 JST; source_epoch: 2026-10-21 offline SQLite (historical report, not the current unified V9)
- evidence_kind: `STATIC-OLD-INDEX / SYNTHETIC / VERIFY`; original_game_dynamic: `NOT_RUN`; golden_pass: `0`; strict_match: `0`; new_formal_ready: `0`; newly_confirmed_T019_native_contradictions: `0`
- VA/CALLsite/offset: null; this finding concerns an E-owned synthetic admission predicate, **not** a newly checked engine address or executable behavior.
- prior_ids: `E-OFFLINE-20261028-1949-T020-DIALOG-WRAPPER-FINGERPRINT-AND-GOLDEN-LINEAGE-01`
- correction_relation: adds independent false-positive checks to the older 19:49 `schema_ready` fixture gate; does **not** supersede native evidence or establish a game bug.
- provenance_crosswalk: `research/intake/E/E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART1-20261102.md` (same ID already excerpt-indexed; this is additional sanitized meaning, **not a new research ID**).

## E-owner finding and bounded evidence

The prior schema-only fixture predicate accepted 24 constructed cases with mismatched raw bytes/digests or invalid structured values. Its 64-character digest format check did not rehash raw G0/G1/G2 captures, immediate SAVE, inputs or MAP; Python's `bool`-as-`int` and loose timestamp/ID checks also allowed malformed synthetic witnesses. Matching `run_id` and hash-like strings alone cannot establish parent receipt lineage. These are **false-positive risks in the E fixture acceptance code**, not observed engine bugs. The older `actual_golden()` check remained false; no real Golden was miscounted.

Historical independent synthetic gate required strict Base64 decode and SHA-256 of bytes, explicit G1 capture → G0 previous capture → G2 previous capture links, nonblank IDs, strict nonnegative integer time/event sequence, strictly increasing `event_seq`, and integer coordinates/roster order. Its recorded fixture partition was 30 cases: 24 previous-pass/new-fail, 3 control rejects and 3 valid reconstructed synthetic controls. The owner recorded 36/36 own checks and 204/204 cumulative historical offline checks (not rerun in this recovery). Source evidence: original E report sections “今回独立して証明したT018合成ゲートの穴” and “T020新規の対策とテスト”, approximately lines 17–39; inspect original under the recorded SHA before citing exact line numbers.

## Limits, errata and next verification

Hash-bound synthetic data is still forgeable in its entirety. The gate **does not** prove authenticity of original-game screenshots/UI, genuine SAVE/MAP or deployed units. No T019 original-engine contradiction was established. Do not promote `schema_ready` or these synthetic PASS counts to native Golden, strict MATCH or formal READY.

Next: compare the 20:45 gate against its 21:49 semantic-binding correction (separate ID, linked below); verify the actual original game's lawful **same-run** G0 UI, immediate pre-battle G1 SAVE/input, and G2 MAP/three-side ordered Unit/Troop witnesses, with externally bound timestamps and source digests. No denied or protected native material is included here.
