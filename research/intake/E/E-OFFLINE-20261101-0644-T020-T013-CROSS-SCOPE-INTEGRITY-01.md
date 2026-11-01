# E-owned intake: cross-scope consistency of 03H–05H models

research_id: E-OFFLINE-20261101-0644-T020-T013-CROSS-SCOPE-INTEGRITY-01
owner: E
tasks: T020 (T018/T019 boundary only)
snapshot_at: 2026-11-01 06:44 JST
source: ChatGPT Library /迫真戦記/E_OFFLINE_UNSYNCED/T020_CROSS_SCOPE_EVIDENCE_INTEGRITY_AUDIT_20261101_0644.md
source_sha256: DB7CD06EA1E2D67FBB105701A78F9FA6CE4332A3B53163F795F7306742FB49E4
source_bytes: 5506
source_verification: original Library file materialized and byte SHA-256 independently verified 2026-11-02 JST; same digest in prior Library readback receipt. Current authorized-PC copy was NOT verified.
classification: prior STATIC / conditional SYNTHETIC / INFERRED / VERIFY / NOT READY
original_game_dynamic_observed: 0
actual_golden_pass: 0
strict_match: 0
new_ready: 0

## Useful non-duplicate E acceptance evidence
Previously existing 03H, 04H and 05H synthetic fixture sets (128 + 24 + 128 cases) were cross-compared without creating new source-native discoveries: the archived audit reports 280/280 expected model results, 12 comparable 03H→04H conditions, 48 comparable 04H→05H conditions and 11/11 intentional mutants rejected. The other cases differ in entry predicates and must not be silently treated as comparable. A 04H not-at-call-site branch is not the same event as a 05H post-gate local else-clear. Neither is a confirmed original-game contradiction.

Relevant prior-only VAs: 0x00545740, 0x0057AA00, 0x0057D8B0, 0x004E53B0. E8 call sites 0x00545A02, 0x0057AD8C, 0x0057D982, and 0x0057D994; indirect 0x0057D9A9 unresolved. Offset +0x1867E, +0x1E570. Source report covers the previously archived models, NOT a new native-V9 or original-EXE test.

## Dedup / corrections / reproduction
Prior IDs: E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01 (same E PR #17), E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01 (same E PR #17), and 05H dual-caller-latch source linked from E PR #8. This is a new **cross-scope consistency test**, not three new studies and not the owner-B native research. Reproduce from the authorized archived 03/04/05 fixtures and their independent model preconditions; scripts and results exist in Library, historical execution NOT rerun in this intake.

Status: PUBLISHED_INTAKE only after GitHub readback; NOT CURATED. KB_CANDIDATE for curator's per-caller semantics, with dynamic behavior, exact vcall target and legacy Golden G0/G1/G2 unresolved. Original game, SAVE, MAP, other owner reports, MASTER, shared KB and protected operations untouched.
