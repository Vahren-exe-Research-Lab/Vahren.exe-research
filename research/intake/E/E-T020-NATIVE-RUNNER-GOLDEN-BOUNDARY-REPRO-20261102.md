# E/T018–T020 historical source recovery: resolved DEV runner is not original Golden (2026-11-02)

**Stage:** PUBLISHED_INTAKE / STATIC_SOURCE + SYNTHETIC / VERIFY / NOT_CURATED / NOT_READY. Both studies already exist in the E 193-ID catalogue; **new research IDs = 0**. This preserves E-side independent negative-acceptance tests, not owner B/REA/DEV research.

## Original study/source provenance, independently checked at authorized PC

| Original E research ID and study (2026-10-29 JST) | PC original report (SHA256 rechecked 2026-11-02) | E-owned Python source (SHA256 rechecked 2026-11-02) | Newly preserved source |
| --- | --- | --- | --- |
| `E-AUDIT-20261029-08H-T018-T020-NATIVE-RUNNER-EVIDENCE-BOUNDARY-01` | `tests/T020_E_NATIVE_RUNNER_EVIDENCE_BOUNDARY_20261029_08H.md`; `30BF6CC7D5CE982FAE79FED12ED0BE95768ADB1316929C45725F1B44BBDA7EB5` | `tests/t020_e_native_runner_evidence_boundary_20261029_08H.py`; `35DDC47A7C17520F95349F9758F1701B9CFA8BE61A7153370324F3410F0AAB59` | [source](repro/t020_e_native_runner_evidence_boundary_20261029_08H.py) |
| `E-AUDIT-20261029-09H-T018-T020-NATIVE-CNB02-JOIN-PREFLIGHT-01` | `tests/T020_E_NATIVE_CNB02_JOIN_PREFLIGHT_20261029_09H.md`; `EC23B00CD61DE2EEF28C15593E370EA224B36083CA4B508EFF0511C7260CE331` | `tests/t020_e_native_cnb02_join_preflight_20261029_09H.py`; `C5DF46AC81E92F1DEC024A7528E2BE322F3B75241D925B53DA4BEB1F9915D538` | [source](repro/t020_e_native_cnb02_join_preflight_20261029_09H.py) |

Both reports were already searchable in `E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART1-20261102.md`, and neither code source was previously preserved by this E PR. Original PC SHA256 checked 4/4; GitHub source readback 2/2. SHA256 refers to PC source bytes; GitHub text may normalize line endings. Owner E/T018,T020; T019 contradiction records are read-only background. Newly established native VA/CALLsite/offset: **null**. Any references to an actual ABI or mechanism in upstream DEV/B/REA are not independently promoted by this E publication.

### Scope and observed synthetic reproduction

Both unchanged E scripts **parse, but do not execute,** the DEV source `dev_lab/src/hakushin_compat/native_battle_runner.py` to check an AST source contract, and use simulated dictionaries for negative cases. That DEV file was read-only and SHA256 rechecked at authorized PC on 2026-11-02: `2F1BBFDA6A3C935564AEF5A9FAD6DA10085A1C87B5C093BED4CAAF551250A5F9`. Other owner source code is not copied or edited.

Original-PC commands (run from the research root with its authorized, unchanged DEV source in place):

```sh
python -B tests/t020_e_native_runner_evidence_boundary_20261029_08H.py
python -B tests/t020_e_native_cnb02_join_preflight_20261029_09H.py
```

Fresh synthetic/AST `unittest` replay **19/19 PASS and 22/22 PASS**, each exit 0 (41/41 total; source hash verified). No original EXE, SAVE, MAP, DAT, game runtime, or DEV `run_fixture` was executed. The GitHub `repro/` copies are *source preservation*, **not standalone** executable replicas: their AST source pin expects the authorized original `dev_lab/` adjacent to `tests/`, which is deliberately not included. Running them inside GitHub alone cannot prove the tests pass or that native functions were run.

The 08H guard separates the DEV synthetic provenance marker `DAT_DERIVED_WITH_SYNTHETIC_RESOLVED_RUNTIME`, `playable=False`, `original_gameplay_golden=0`, `strict_match=0` from any legally witnessed old engine battle. CLI exit 0 or a MAP SHA calculated over DEV input does not imply original map selection or native finish/World commit.

The 09H independent G0–G4 preflight checks equality of asserted run labels, real-looking SHA *syntax* for G1 inputs and MAP, 3-side role labels, roster presence, explicit Unit/Troop instance mapping, participant pointers and claimed G3/G4 receipts. Even with every mock field populated the result is `CROSSWALK_DESIGNED_NOT_STRICT`. A matching display name, pointer, or map digest is not by itself an observed old Unit/Troop identity or legal original map selection.

### New bounded 2026-11-02 erratum: malformed negative inputs are not always classified

A **separate synthetic, read-only probe** invoked unchanged 09H `diagnose()` with two intentionally malformed mock inputs. Both raised **`TypeError`**, rather than a named `INVALID_*` verdict: (a) G2 `roles=[["attack"],"defend","support"]` is unhashable at `set(roles)`; (b) DEV `request.participants=None` is not iterable while building the pointer set. Probe wrapper caught the exceptions and returned exit 0. No original assets or DEV engine runtime were used.

This is a **limited parser/negative-coverage gap**, not a proven original game bug, native mismatch, or evidence of unsafe external execution. Do **not** call the 09H helper universally fail-closed for arbitrary untrusted shapes. A future E-owned synthetic regression may enforce deterministic `INVALID_*` results for both cases, after source-version and downstream contract review; keep original recovered code byte-for-byte identifiable and use `errata` rather than rewriting the published provenance. The 22/22 ordinary mock tests were not sufficient to detect these two malformed-shape cases.

### Curation decision gate

These are two already catalogued historical **IDs**, not two newly discovered native functions. Compare current owner report SHA and later correction chains before optional curator REF references. Neither script is a substitute for independently captured, same-run lawful G0 original UI/Spot, G1 immediate SAVE/input bytes, G2 actual selected MAP/three roles/ordered Unit-Troop array, G3 old battle end, and G4 World consequence. **Original DYNAMIC OBSERVED 0, Golden PASS 0, strict MATCH 0, new formal READY 0, new MASTER change 0, T019 new confirmed contradictions 0**. Unrelated denied operations and protected evidence are not opened or reconstructed.

**Next E source cursor:** existing metadata-only `tests/t020_e_source_pin_admission_20261029_06H.py` and `tests/t020_e_comparator_kind_boundary_20261029_07H.py` require ownership, SHA, source dependencies, errata and safety checks. Curator separately handles semantic consolidation and any `develop`/REF/lexicon modifications.
