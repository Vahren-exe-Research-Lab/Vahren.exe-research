# E/T018–T020: synthetic capture semantic-binding regression (historical owner report, sanitized)

- research_id: `E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01`
- owner: E; tasks: T018, T020 (T019 classification only)
- source_relative_path: `tests/E_OFFLINE_SYNC_20261029/T020_GOLDEN_CAPTURE_SEMANTIC_BINDING_AUDIT_20261028_2149.md`
- original_source_sha256: `D46C9DEF81CA661559717EE274D3782B97D16403D1F8B02F00C22B1225D5A56B` (8,480 bytes; original authorized research PC rehashed 2026-11-02 JST)
- observed_at: 2026-10-28 21:49 JST; source_epoch: 2026-10-21 offline SQLite (historical, not fresh V9)
- evidence_kind: `STATIC-OLD-INDEX / SYNTHETIC / VERIFY`; original_game_dynamic: `NOT_RUN`; golden_pass: `0`; strict_match: `0`; new_formal_ready: `0`; newly_confirmed_T019_native_contradictions: `0`
- VA/CALLsite/offset: null; this is an E-owned synthetic verification predicate, not new proof of native engine calls.
- prior_ids: `E-OFFLINE-20261028-2045-T018-T020-GOLDEN-LINEAGE-CONTENT-BOUND-01`, `E-OFFLINE-20261028-1949-T020-DIALOG-WRAPPER-FINGERPRINT-AND-GOLDEN-LINEAGE-01`
- correction_relation: extends the prior digest+parent-hash gate to bind **structured fields to their captured bytes**. The 20:45 check is a necessary but insufficient synthetic predicate; do not replace it or claim real-game curation.
- provenance_crosswalk: `research/intake/E/E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART1-20261102.md` (same ID already excerpt-indexed; full safe meaning preserved here without minting another ID).

## E-owner finding and bounded evidence

The earlier 20:45 `hardened_synthetic_ready()` verified decoded capture bytes, digest and G1→G0→G2 parent hashes, but did **not** prove that `capture_b64` actually serialized visible fields: scenario/EXE/DAT digest, timestamp/event order, three-side roster identities, Unit/Troop placement/order or SAVE/input/MAP association. Keeping capture bytes and hashes fixed while changing the visible metadata could still return true in synthetic cases. No such discrepancy was observed in the original game.

The owner introduced a **fixture-only** virtual `hakushin-synthetic-capture/v1` format: canonical UTF-8 JSON with sorted keys, no extra whitespace or nonfinite numbers; acceptance requires exact byte equality between reserialized structured fields and decoded capture bytes. `capture_sha` and `capture_b64` are excluded from the self-referential content; previous-capture links remain inside the content. Unexpected schema additions are rejected unless versioned. The earlier digest/lineage gate remains required. **This virtual JSON is not the game's capture format**; both the bytes and metadata can still be forged together.

The original E owner recorded 36 synthetic fixtures (31 earlier-pass/new-reject, 2 control rejects, 3 rebuilt valid synthetic controls), 45/45 new regression checks and 249/249 cumulative historical offline checks (including the prior 204). Earlier intermediate TypeError during development was repaired before the recorded final test; these checks have **not** been rerun in this recovery. Evidence: original E report sections “今回の具体的な発見”, “新設したE所有の合成検証ゲート” and “T020 合成回帰結果”, approximately lines 18–40, under the listed original SHA.

## Limits, errata and next verification

This is a regression in E's **admission test semantics**, not a native T019 contradiction or formal READY. The 31 negative cases do not prove a game-engine bug. A real Golden needs independently captured lawful original same-battle G0 UI, immediate pre-battle G1 SAVE/input and G2 MAP/ordered three-side Unit/Troop with auditable external provenance. Review E's current accepted runner against this historical synthetic gate without touching refused evidence, and ask the curator to consider the explicit fixture/capture distinction in the knowledge reference. Do not upgrade synthetic PASS to original Golden.
