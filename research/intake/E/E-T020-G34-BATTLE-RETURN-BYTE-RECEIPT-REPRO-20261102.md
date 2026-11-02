# E/T020 existing-ID recovery: G3/G4 single-commit and byte-receipt gates (2026-11-02 JST)

**Status:** PUBLISHED_INTAKE / NOT_CURATED / SYNTHETIC + STATIC-source-context / VERIFY. **No new research ID or native observation.**

## Owner source identity and witnessed SHA256

- Primary existing research ID: `E-AUDIT-20261021-2147-BATTLE-RETURN-COMMIT-GATE-01` (owner E, T018/T020, study 2026-10-21). Authorized-PC report `tests/T020_BATTLE_RETURN_COMMIT_GATE_20261021_2147.md`; PC SHA256 rechecked 2026-11-02: `2417E9BDEB47C7BF8B5602A41CDE8BB214724528E34CC5E5B46BE3B0E3CA24F3`. Existing source-index row and batch01 are antecedents, not duplicated here.
- Recoverable Python source: `tests/t020_battle_return_commit_gate_20261021_2147.py` (owner E, existing study's E/T020 synthetic helper); authorized-PC original SHA256 `9A12BA734B89E4FCB2D8DB86A0C2485D6F41208256B413F24F55BE95334F79B8`, rechecked 2026-11-02. Preserved runnable text: [G3/G4 source](repro/t020_battle_return_commit_gate_20261021_2147.py), from owner commit `d7db0f057d80dee1348e4d3dc2cc2645df5e5c52`; GitHub full-text readback matched.
- Additional PC-only E/T020 receipt helper (not independently assigned a new study ID): `tests/t020_cnb02_byte_binding_20261022_0046.py`, authorized-PC SHA256 `B1382005D55780166DE46F8FB20AA5F214FF105101EA84241B5E5DC9278151AB`, rechecked 2026-11-02. Preserved [byte-binding source](repro/t020_cnb02_byte_binding_20261022_0046.py) in owner commit `b8d5b5a0c1983d9585eedff0626e7a2a4bef2ce7`; GitHub full-text readback matched.
- Related *separate* existing E research ID `E-AUDIT-20261022-0450-AUTOSAVE-BYTE-IDENTITY-01`, source `tests/T020_AUTO_SAVE_BYTE_IDENTITY_CROSSWALK_20261022_0450.md`, PC SHA256 `05CB31A1819DCDB2876A9BDB4BF43E34DBC5DE6402C86A8792DB54477902E9DE` rechecked 2026-11-02. This report demonstrates that same filename and length are not SAVE byte identity; it is **not** relabeled as the byte-binding script's original authoring report.
- VA/CALLsite/offset for these newly preserved **schema validators: null**. Older A/B/C native descriptions and historical references in the 21 Oct E report are read-only provenance; this recovery does not independently validate any native function, ABI, route, or World write.

## Reproducible bounded behavior

Run from `research/intake/E/`:

```sh
python -B repro/t020_battle_return_commit_gate_20261021_2147.py
python -B repro/t020_cnb02_byte_binding_20261022_0046.py
```

The authorized PC re-executed these unchanged synthetic stdlib tests on 2026-11-02 JST: **8/8 passed** for the first script (exit 0); **13 discovered, 12 passed, 1 skipped** for the second (symlink test unavailable on this Windows permission configuration; exit 0). No genuine old-game fixture was executed.

- G3/G4 schema: reject missing original observation, missing G0–G4 single-run identity, missing listed old hash fields, or simultaneous native/new-API commit paths; leave unobserved route and missing captures VERIFY; insufficient new build/capture yields NO_STRICT_COMPARISON. This is a **presence/shape predicate**. The 8-case synthetic test uses literal placeholders like `present`, so even its `SYNTHETIC_SCHEMA_READY` is not a true byte-verified original receipt.
- Byte gate: validate 12 expected receipt roles, SHA256 field syntax, role-specific file bytes against claimed hash, reject duplicate/absolute/parent-escaping/symlink paths and missing files in a bounded caller-supplied root. Tests create temporary artificial files and clean them up. `BYTE_BOUND_SYNTHETIC` and `BYTE_BOUND_NOT_GOLDEN` are not proof of actual legal C-NB02 capture, origin, clock, battle identity, semantics, or native single-commit behavior. The EXE digest constant is a reported identifier, not a fresh original EXE read.
- **Important independence requirement:** a schema-only G3/G4 `READY_FOR_COMPARISON` string or a byte-binding success alone must NEVER be promoted to curator READY, actual Golden PASS, strict MATCH, or successful World commit. Same-run genuine source capture and independently established semantic mapping are additional gates.

## Duplicate/errata/curation boundary

Existing 193-ID E source index already links the 21 Oct report and 22 Oct SAVE-identity report; this addition **preserves previously metadata-only Python evidence**, with **new IDs 0**. Do not import the companion as a new finding or claim E ownership of A/B/C's native reverse-engineering findings. No supersedes or errata against native code is asserted; this documents the *schema-versus-byte-versus-meaning* separation and the independent older auto.sav size/SHA mismatch. State `PUBLISHED_INTAKE` only upon GitHub source+note readback; `CURATED` remains curator-only. Reproduction contains no original EXE/DAT/MAP/SAVE, raw logs, private paths, or blocked evidence.

**Golden and formal acceptance:** E original same-run legal G0 UI/Spot + G1 immediate SAVE/input + G2 actual MAP/three sides/ordered Unit/Troop are not joined; G3/G4 genuine exit/World checks therefore also lack a qualified original run. DYNAMIC OBSERVED 0; original Golden PASS 0; strict MATCH 0; new formal READY 0; new MASTER decision 0. Synthetic pass does not change them.

**Next cursor:** prioritize the 2026-10-29 08H–09H `tests/t020_e_native_runner_evidence_boundary_20261029_08H.py` and `tests/t020_e_native_cnb02_join_preflight_20261029_09H.py` as **metadata-only, source/ownership/safety/errata review pending**; do not automatically execute native interactions or publish original input. Curator separately reconciles latest `develop`, older correction chains and E study IDs.
