# E-owned intake: byte-bound G0/G1/G2 receipt and frame-epoch integrity

research_id: E-OFFLINE-20261101-11H-T018-T020-G012-ARTIFACT-ATOM-01
owner: E
tasks: T018, T020
snapshot_at: 2026-11-01 11H JST
source: ChatGPT Library /迫真戦記/E_OFFLINE_UNSYNCED/T018_T020_G012_ARTIFACT_ATOM_AUDIT_20261101_11h.md
source_sha256: F811809B90D4719320EE7BF0DE0E5A964FA0FB8202DA1149CF878E148A3D1AED
source_bytes: 6771
source_verification: original Library source materialized and independently SHA-256 rehashed 2026-11-02 JST; agrees with previous Library readback receipt. Not verified as currently present in authorized PC tests folder.
classification: archival SYNTHETIC / INFERRED acceptance-gap / VERIFY / NOT READY
original_game_dynamic_observed: 0
actual_golden_pass: 0
strict_match: 0
new_ready: 0

## Narrow delta, not a new engine claim
Existing 09H T018/T020 roster bijection/order and 10H definition-versus-runtime provenance gates mainly checked fixture shapes and self-declared digests. The 11H independent gate additionally requires matching **actual bytes** of artifacts, same run/session/battle and G2 snapshot/epoch/barrier, and tests mismatch despite matching claimed hashes. Archive result: 3 model runs × 24 variants = 72/72 expected classifications; only 3 baselines passed local byte integrity, and 69 variants were expected malformed/insufficient receipts. It does not prove atomic capture in original gameplay; native VM/RNG captured neither.

Preserve distinction between immutable, legitimately shared old/new replay INPUT SAVE/MAP bytes and independently collected old/new OBSERVATION OUTPUT (erratum from E 2026-11-01 18H). Unconditional file-path inequality for all artifacts is invalid. This erratum is a correction to the acceptance rule, not a 2026-11-01 native discovery.

## Golden admission and dedup
An actual eligible case requires legal original-game battle UI (G0), same-battle immediate prebattle SAVE byte SHA and input trace (G1), and actual selected MAP, three powers, ordered deployed Units and Troops with stable identity and stage/frame (G2). All artifacts must have true bytes/digests and causally join to the same run; if unavailable remain VERIFY/INELIGIBLE, never synthesize from DAT or a candidate MAP. A replacement comparison also requires separate new-build and actual new observation, not matching fixture values alone.

Prior related E IDs: 09H roster bijection/order (already E PR #17), 10H definition-runtime provenance (E PR #8), and 12H cross-run alias admission with 18H correction (E PR #17). 11H adds byte binding and mixed-epoch negative cases, not a new G0/G1/G2 PASS. Historical 72 synthetic tests were not rerun during publication.

KB_CANDIDATE: Golden admission provenance only; no new VA/E8 site verified in this 11H source. Historical upstream mapping in REF_BATTLE_TAKEOVER belongs to original owner. GameClear DAT13/TXT2 only lexical-scope RESOLVED; script2 actual precedence/TXT runtime/gwrite remain VERIFY. PUBLISHED_INTAKE / NOT CURATED only after branch readback. MASTER/READY/GOLDEN unchanged.
