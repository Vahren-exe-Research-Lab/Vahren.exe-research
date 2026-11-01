# E/T018-T019-T020 — C-NB02 Golden evidence admission and T019 historical correction

- research_id: E-OFFLINE-20261101-16H-T018-T019-T020-CNB02-SOURCE-G012-ADMISSION-01
- owner: E; tasks: T018,T019,T020.
- observed_at: 2026-11-01 16H JST; snapshot: user-supplied 2026-10-21 offline pack + E 15H candidate schema, **not** current target gameplay.
- source_relative_path: Library/T018_T019_T020_CNB02_SOURCE_ADMISSION_AUDIT_20261101_16h.md
- source_sha256: 5131D85237594DBCBD051A53D8A096301CCE1729A92A7DEB62EB1C11BC967109 (materialized raw Library bytes, remeasured 2026-11-01).
- source_snapshot_zip_sha256: 911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2 (verified by the source research run, not downloaded again here).
- source_snapshot_T018_sha256: CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120 (2026-10-21 snapshot, do not identify as latest PC T018).
- prior_ids: E-OFFLINE-20261101-15H-T018-T020-SIX-GATE-COVERAGE-ADMISSION-01; T018-E-REP-BATTLE-20261013.
- new VA/call/offset: none. Candidate s16.map and sci1/po2/sp2->sp16 are SCRIPT/SNAPSHOT CANDIDATES ONLY, not dynamic G2.
- evidence_kind: STATIC source excerpt + SYNTHETIC negative test + VERIFY; no native original actual; ready_status NOT READY; Golden DYNAMIC0 / actual PASS0 / strict MATCH0.
- kb_candidate: E/T018-T019-T020-CNB02-SOURCE-G012-ADMISSION-GAP-16H.

## Audit result
The 15H candidate JSON for C-NB02 lacked **22 measured values**: G1 six, G0 four, G2 eight, comparison four. A historical T018 schema crosswalk showed **11 additional fields absent from this candidate schema** (proposed fields, not proven legally obtainable UI measurements). In the independent 16H check, 19/19 newly injected synthetic negative cases correctly rejected/withheld evidence promotion; prior six-gate 381/381 was **not rerun** or recountable as new target success. The 22/11 counts are schema completeness diagnostics, not number of proven actual-game defects.

In particular sp16 is not po16, a candidate s16.map is not the active MAP file, stored Unit lists/Spot counts do not establish deployed Troop order or the three enemy/ally/support Side owners. Verify G0 legal user-visible attack, G1 same-run prebattle SAVE byte SHA plus inputs/timestamps, G2 actual map+runtime layout, three powers and ordered Unit/Troop, and independent original/reimplementation evidence. Uncaptured evidence stays VERIFY/INELIGIBLE.

## T019 provenance correction
Older MASTER T019 C-007 GameClear conflicting note was already corrected: the earlier short/full ending mapping for zero-argument vs argument-present setGameClear() had been inverted. Do not revive that historical alleged Wiki contradiction. **This is an old erratum**, not a new native re-evaluation or newly confirmed bug. GameClear DAT13/TXT2 search-scope mismatch was resolved as a search-domain difference, not a runtime guarantee. script2 priority/flag and TXT loader remain VERIFY. Newly confirmed T019 contradictions: 0.

## Status and follow-on
This offline research had connection failure while reading MASTER (not a safety refusal); this run independently read authorized PC MASTER, owner HANDOFF starts and current E docs, but 34-task/full READY was not recomputed. Last authoritative official checkpoint196 and READY596 (A115/B229/C136/D116), 34-task DONE9/IN_PROGRESS21/VERIFY4 are prior values only; owner E formally accepted no new READY. Existing unsafe/refused source operations remain BLOCKED and are neither retried nor published. Next: locate complete legal same-battle G0+G1+G2 source receipts, decide missing 11 fields as required/optional/INELIGIBLE, and only then build original-vs-new strict runner inputs.