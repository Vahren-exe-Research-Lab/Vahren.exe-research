# E/T018–T020 G2 synthetic diagnostic reproducibility chain (2026-11-02)

**Owner E, existing research IDs only. PUBLISHED_INTAKE / SYNTHETIC + VERIFY / NOT_CURATED / NOT_READY.** This note indexes verified E-owned code; it makes no new native Vahren claim. No original-game Golden or strict-match result.

## Why these files matter

The earlier 08H G2 shape checker did not require an actual defense roster row. The 09H overlay restored attack/defense row-presence warnings; 10H restored typed side-participant and placeholder MAP warnings; 11H fail-closed code protects list/object `side` from a `TypeError` in earlier overlays; the 11:58 overlay flags same visible Unit/Troop labels across roles for **review**, without equating them to native instance identity. None treats synthetic names, SHA-looking strings, or static side slots as proof of deployed native entities.

## Source/ID and runner map

| E source research ID (already indexed) | GitHub runner in `repro/` | PC original runner SHA-256 (actual bytes rehashed 2026-11-02) | Tests now |
| --- | --- | --- | ---: |
| `E-AUDIT-20261021-2345-CNB02-RECEIPT-PROVENANCE-GATE-01` | `t020_cnb02_receipt_provenance_gate_20261021_2345.py` (previously staged) | `34bc469c50471a1bce58d2815d6e5d9a4cf45d6cd2232898312fde69a15e349d` (earlier verified receipt) | 17 |
| `E-AUDIT-20261026-08H-T018-T020-G2-ROSTER-SHAPE-NEGATIVE-EXEC-01` | `t020_cnb02_g2_roster_shape_diagnostic_20261026_08H.py` (previously staged) | `36f12b3b71c249a8fd56f7f65e13d3a513333f3f4538ab5bc95c82291e30a032` (earlier verified receipt) | 14 |
| `E-AUDIT-20261025-11H-T018-T020-G2-SEMANTIC-REVIEW-RUNNER-01` | `t020_cnb02_g2_semantic_review_20261025_11H.py` | `a76d5499b1751443705649b02687dea5d6fcbdebda5323a209695dc9f5736e66` | 15 |
| `E-AUDIT-20261026-09H-T018-T020-G2-ROSTER-PRESENCE-REGRESSION-01` | `t020_cnb02_g2_roster_role_coverage_overlay_20261026_09H.py` | `3d81e8435dfe9ca2ea6f3207476789393a67973a67b622a1eb79cdd7ac65634f` | 12 |
| `E-AUDIT-20261026-10H-T018-T020-G2-SEMANTIC-PARITY-01` | `t020_cnb02_g2_cross_generation_parity_guard_20261026_10H.py` | `e2f206f30f3d66de9bd91d4a0c62ddc081fadf8403f69250c5594f42c2317cff` | 14 |
| Supplementary 11H implementation referenced in the 11:58 original E report; **no independent research ID created** | `t020_cnb02_g2_unhashable_role_failclosed_20261026_11H.py` | `2ab5810741a6e4b42f67d356ad65adab3084b60cdb7d00ede394adba6e35d47d` | 11 |
| `E-AUDIT-20261026-1158-T018-T020-CROSSROLE-IDENTITY-ALIAS-01` | `t020_cnb02_g2_cross_role_visible_alias_guard_20261026_1158.py` | `9ebb19f73f284d119fa536308af9da9694db8181a0e5e0da2189c0fa2b2f6ac8` | 11 |

**Source report provenance** (PC-relative original reports; full content remains on authorized PC): 25 Oct 11H `tests/T020_CNB02_G2_SEMANTIC_REVIEW_RUNNER_20261025_11H.md` SHA `a8b9430b2a852cf05b679963df1cc06b635eb57f20b720cff465b7b4fe0bb744`; 26 Oct 09H `tests/T020_CNB02_G2_ROSTER_ROLE_COVERAGE_REGRESSION_20261026_09H.md` SHA `759606ba516928c21a623fe3c2a3f8ceb9da73a8ccd872c417c89bbb6a4dad91`; 10H `tests/T020_CNB02_G2_CROSS_GENERATION_PARITY_GATE_20261026_10H.md` SHA `0584365a103610a04acaa08923af2cc864acb6537ee3f677f31ed78107bfc4bb`; 11:58 `tests/T020_CNB02_G2_CROSS_ROLE_VISIBLE_ALIAS_DIAGNOSTIC_20261026_1158.md` SHA `3ce52e96fb8f2542682065c0f4ecdde7b00f234a13cfa54b7c3aabf9e5112aa1`. Report ID, source line and linked 193-index paths are available in [E source index](E-SOURCE-RECEIPT-INDEX-193-20261102.tsv) and historical [crosswalk batch 1](E-LEGACY-20261020-31-CROSSWALK-BATCH01-20261102.md) / [batch 2](E-LEGACY-20261020-31-CROSSWALK-BATCH02-20261102.md).

## Reproduce

Use Python 3 stdlib only. From `research/intake/E/repro` on a separately checked-out copy of this E branch:

```sh
python -B -m unittest -q t020_cnb02_receipt_provenance_gate_20261021_2345 t020_cnb02_g2_roster_shape_diagnostic_20261026_08H t020_cnb02_g2_semantic_review_20261025_11H t020_cnb02_g2_roster_role_coverage_overlay_20261026_09H t020_cnb02_g2_cross_generation_parity_guard_20261026_10H t020_cnb02_g2_unhashable_role_failclosed_20261026_11H t020_cnb02_g2_cross_role_visible_alias_guard_20261026_1158
```

**Observed on authorized PC (2026-11-02): 94/94 synthetic unittest PASS, exit code 0.** Five newly staged runner original PC byte SHA-256 values were rehashed; all matched previous E report/receipt values. The five GitHub runner full UTF-8 texts were fetched back and matched the PC tool's text after LF normalization (5/5). Git blob SHA-1 and PC original-byte SHA-256 are different types of digest; no raw Windows newline identity is implied. The newly fetched GitHub copy itself was not separately executed; its source text was checked.

Run order is not an implied acceptance priority. Dependency chain: receipt provenance → 25 Oct semantic preflight; independent 08H shape → 09H role presence → 10H parity → 11H list/object fail-closed → 11:58 cross-role alias. Older generations are preserved to replay **regression counterexamples**, not recommended as final standalone G2 admission gates.

## Current evidence boundary / curator action

- **No original-game G0/G1/G2 same-battle chain**: lawful G0 UI/Spot and commit, immediate G1 original pre-battle SAVE/input with bytes and clock, loaded runtime MAP with 3 sides and ordered deployed Unit/Troop (G2) are not jointly evidenced. No G3/G4 original strict parity either.
- E original-game dynamic observation newly made 0; actual Golden PASS 0; strict MATCH 0; new formal READY 0; no MASTER change. T019 GameClear DAT13/TXT2 lexical-scope note stays RESOLVED; actual script2/TXT runtime precedence/phase/gwrite VERIFY.
- The 08H checker has a missing-defense-row warning gap; 10H can raise TypeError for list/object roster roles; the later overlays restore conservative diagnostics without modifying earlier historical source. Even the 11:58 overlay compares visible text labels only: same label may refer to different original objects or lifecycle epochs.
- Curator should review existing E original report source lines/hashes, correction order and any overlapping `develop` content, and select a *single canonical diagnostic policy* if useful. E does not update `REF_*`, `symbols.tsv`, `structs.tsv` or `develop`; do not merge this diverged draft blindly or count the five scripts as five research IDs.
- Original EXE/DAT/MAP/SAVE/ZIP, personal logs and prohibited VA/operations were not accessed or uploaded by this code-preservation action; earlier safety blocks remain in effect.

**Next E cursor:** source-check additional allowed G2 12:53 support and 13H placeholder-ID overlays for genuinely missing behavior (dedup first), then gather lawful atomic original G0–G2 receipts when obtainable. No synthetic PASS implies Golden qualification.
