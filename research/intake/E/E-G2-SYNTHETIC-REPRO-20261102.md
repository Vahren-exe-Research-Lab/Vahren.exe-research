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

## 2026-11-02 follow-on: 12:53 support relation + 13:50 placeholder guards (existing IDs)

These are **two already indexed E owner studies**, not two new research IDs or native discoveries. The full research reports remain PC-only; their 193-ID index entries and batch02 crosswalk already preserve their provenance. This follow-on preserves their previously missing **runnable E-owned source code** in the same open PR. All measurements below were taken from the authorized PC in this recovery run (not extrapolated from earlier tests).

| Existing E research ID / owner | Original report (PC-relative path; SHA-256 rehashed) | Original Python source (PC-relative path; SHA-256 rehashed) | Current synthetic tests |
| --- | --- | --- | --- |
| `E-AUDIT-20261026-1253-T018-T020-SUPPORT-PRESENCE-DEPL-REVIEW-01` / E T018,T020 | `tests/T020_CNB02_G2_SUPPORT_PARTICIPATION_DEPLOYMENT_REVIEW_20261026_1253.md`; `34df7d4731a184ee4e2bfd9d9962c0810a36d178c7b501b00a20a960ccdfdd3c` | `tests/t020_cnb02_g2_support_presence_deployment_review_20261026_1253.py`; `0320a180906cbff14ec943011fb24bda1835d2c53669ef7c99724513a01f1f4a` | 12 |
| `E-AUDIT-20261026-1350-T018-T020-G2-PLACEHOLDER-IDENTITY-01` / E T018,T020 | `tests/T020_CNB02_G2_PLACEHOLDER_IDENTITY_REVIEW_20261026_13H.md`; `23f1c78f6bba3b705d695522f57771b8b252d2258f4c010818018bd6dc90ffc4` | `tests/t020_cnb02_g2_placeholder_identity_review_20261026_13H.py`; `3a1b5f0a10a5f29657fb2ca93d5a4f5ecc755bae5b35a207a1087d30b5db92b4` | 13 |

**Source-grounded semantic difference (T020 SYNTHETIC/VERIFY, VA/CALL/offset: null):** the 12:53 guard adds review flags for disagreement between declared support participants and visible support-deployed roster rows, without claiming that each participant necessarily deploys a troop. The 13:50 guard identifies exact placeholder strings in visible Unit/Troop/Power labels while not rejecting a legitimate compound name merely containing such a word. Source evidence: the two owner reports above, respectively lines 3–12 and 3–12; later overlay code is not a native witness. Correction lineage is 08H shape → 09H defense coverage → 10H parity → 11H unhashable fail-closed → 11:58 cross-role alias → **12:53 support** → **13:50 placeholder**. Both additions extend earlier synthetic reviews; do not overwrite the prior study records or infer native engine bugs from their diagnostics.

From `research/intake/E/repro/`, run:

```sh
python -B -m unittest -q t020_cnb02_g2_support_presence_deployment_review_20261026_1253 t020_cnb02_g2_placeholder_identity_review_20261026_13H
```

**PC execution this run:** 25/25 synthetic cases PASS, process exit 0; both PC source-report digests and both PC Python digests verified; GitHub newly published Python texts independently fetched and matched submitted content after LF normalization (2/2). Historical 89/89 or 102/102 aggregates from older reports were **not rerun as aggregate here**. Published files: `repro/t020_cnb02_g2_support_presence_deployment_review_20261026_1253.py` and `repro/t020_cnb02_g2_placeholder_identity_review_20261026_13H.py`. GitHub text readback is not a replay against the original game.

**State and acceptance:** `PUBLISHED_INTAKE / NOT_CURATED / SYNTHETIC / VERIFY / NOT_READY`. These diagnostics have no actual original-game Golden evidence or VA proof; original gameplay Golden PASS 0, old/new strict MATCH 0, new formal READY 0, and confirmed new T019 contradiction 0. This owner recovery changes no MASTER, `develop`, curated REF, dictionary, game file, or other owner research. **Next cursor:** curator should inspect 12:53/13:50 report conditions and this exact code against prior errata; the original old-game same-run G0 lawful UI/Spot, G1 immediate SAVE+input and G2 real MAP/three sides/ordered deployed Unit/Troop remain unqualified and must be independently observed before Golden or READY.

## 2026-11-02 08H E historical phase-boundary source recovery (no new IDs)

Two **existing** E-owned T018/T020 studies from the 193-ID provenance index had full Python code missing from PRIVATE GitHub. Their PC report files and code were read directly, code SHA-256 checked against the preexisting 337-asset receipt, and the existing owner Draft PR #17 was reused. No new PR, study ID, original-game claim, or curated dictionary edit.

| Existing ID | E PC report, SHA-256 rechecked | PC code, SHA-256 rechecked | GitHub isolated code | Synthetic tests |
| --- | --- | --- | --- | ---: |
| `E-AUDIT-20261025-17H-T018-T020-G2-ACTIVE-WINDOW-OVERLAY-01` | `tests/T020_CNB02_G2_ACTIVE_WINDOW_SCHEMA_REVIEW_20261025_17H.md` — `6b23bcc7b934baaff834c40b7919337cb062f6a20fa26b6c3237b834026d301c` | `tests/t020_cnb02_g2_active_window_review_20261025_17H.py` — `1035b5420ae40d4d45a45e685f38014f3dee824de361143f32fe65c29c486359` | [17H phase source](repro/t020_cnb02_g2_active_window_review_20261025_17H.py) | 22/22 |
| `E-AUDIT-20261025-18H-T018-T020-MODE2-PREACTIVE-PHASE-BOUNDARY-01` | `tests/T020_CNB02_MODE2_PREACTIVE_PHASE_BOUNDARY_20261025_18H.md` — `5d8de36ca113fb8948c9ce669f90bdbe3f69e73206cfad643a20e189352e3c20` | `tests/t020_cnb02_mode2_preactive_phase_review_20261025_18H.py` — `f0a4122b4568906af1753a7fb7cfe1497172d30ceddf1df5138feb8001e72e7a` | [18H phase source](repro/t020_cnb02_mode2_preactive_phase_review_20261025_18H.py) | 6/6 |

**Owner-source semantic difference and corrections (SYNTHETIC / VERIFY; VA, CALL and offsets: null):** 17H shows an explicit preexisting 16H synthetic gate gap: a candidate G2 timestamp *after* `active_exit` can pass the former source-shape check with no issue flag. The 17H overlay checks exit bounds, same clock/run/battle/PID, mode=2 + active=1 guards and a nonempty coherence-witness field. The 18H overlay then separates MODE2 preactive, ACTIVE review, ACTIVE=0 exit tail, and MODE1 postbattle. A historical watch's 2.814309-second preactive interval is cited from the E original report; the raw watcher log was **not independently rehashed or replayed this run** and its complete bytes are not in this PR. These are schema/observation-taxonomy corrections, **not an engine bug finding** or a new G2 native roster witness. Both code files and reports are owner E; source line anchors: 17H report `## Newly demonstrated bounded admission gap` through `## New E-owned isolated executable reviewer`; 18H report `## Newly isolated T020 contract nuance` through `## Independent, isolated executable reviewer`.

Reproduce with Python stdlib only from `research/intake/E/repro/`:

```sh
python -B -m unittest -q t020_cnb02_g1_phase_contract_matrix_20261025_16H t020_cnb02_g2_active_window_review_20261025_17H t020_cnb02_mode2_preactive_phase_review_20261025_18H
```

On the authorized PC, **46/46 synthetic unittest methods PASS, exit 0** (18 preexisting G1 tests + 22 restored 17H tests + 6 restored 18H tests). This does **not** mean 46 new tests, original-game verification, or code execution on the fetched GitHub copy. Both GitHub UTF-8 source texts were fetched back and compared character-for-character to staged text (2/2); PC SHA-256 measures original PC bytes and is not a Git blob SHA-1. Source receipt status was updated in the existing E TSV; no raw watch logs, original EXE/DAT/MAP/SAVE, tokens, passwords or user absolute paths were uploaded.

**Status / next review:** `PUBLISHED_INTAKE / NOT_CURATED / SYNTHETIC + VERIFY`; new IDs 0; MASTER change 0; original DYNAMIC OBSERVED 0, actual gameplay Golden PASS 0, strict MATCH 0, new formal READY 0. Original same-run lawful G0 UI/Spot, G1 immediate SAVE/input and G2 loaded MAP/three sides/ordered deployed Unit-Troop are still not joined. Curator should review the 16H→17H→18H change in **G2 phase eligibility** against native primary evidence, after deduplicating same IDs across develop and older owner PRs; independent original Golden capture remains pending. Earlier refused observations remain BLOCKED and have not been retried.
