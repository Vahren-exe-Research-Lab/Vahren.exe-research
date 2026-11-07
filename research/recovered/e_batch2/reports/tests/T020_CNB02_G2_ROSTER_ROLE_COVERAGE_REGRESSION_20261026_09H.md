# E-AUDIT-20261026-09H-T018-T020-G2-ROSTER-PRESENCE-REGRESSION-01
Owner E / T018,T020; T019 reference. 2026-10-26 09H JST. PC-LOCAL / STATIC CODE CROSS-VERSION / SYNTHETIC EXECUTED / VERIFY / NOT READY; native original gameplay NOT RUN.

## Sources and independently reproduced delta
Local Compact read-only: MASTER_LEDGER.md (34 Task queue independently recounted this run); evidence/ANALYSIS_LANES_PROTOCOL.md, A-D HANDOFF; REA decomp_task/PROGRESS.md; dev_lab/docs/IMPLEMENTATION_PLAN.md; tests/T018_GOLDEN_CORPUS.md; wiki/T019_CONTRADICTIONS.md; E prior 11H semantic and 08H shape reports/code.
11H source tests/t020_cnb02_g2_semantic_review_20261025_11H.py PC actual SHA A76D5499B1751443705649B02687DEA5D6FCBDEBDA5323A209695DC9F5736E66; explicitly flags NO_DEFENSE_ROSTER_RECEIPT if no defense row.
08H source tests/t020_cnb02_g2_roster_shape_diagnostic_20261026_08H.py PC actual SHA 36F12B3B71C249A8FD56F7F65E13D3A513333F3F4538AB5BC95C82291E30A032; its test baseline contains only one attack roster row while attack and defense side lists are nonempty, and the baseline returns issues=[].
**Regression in diagnostics, not a native game defect:** 08H dropped the 11H absence-of-defender-roster warning. Neither 08H nor 11H produces Golden PASS; 08H verdict remained VERIFY_NOT_GOLDEN. This is not actual roster loss or an assertion that side lists equal deployed Unit IDs.
Parent receipt source unchanged, actual SHA 34BC469C50471A1BCE58D2815D6E5D9A4CF45D6CD2232898312FDE69A15E349D. Original target EXE reference SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 is from historical manifest, not rehashed or executed here.

## Implemented E-only guarded overlay and checks
New code tests/t020_cnb02_g2_roster_role_coverage_overlay_20261026_09H.py, actual PC SHA256 3D81E8435DFE9CA2EA6F3207476789393A67973A67B622A1EB79CDD7AC65634F. Does NOT edit 08H/11H, old E provenance gate, REA or runtime engine.
Overlay preserves 08H issues and adds NO_ATTACK_ROSTER_RECEIPT / NO_DEFENSE_ROSTER_RECEIPT if no correctly typed row for that role. This is a conservative presence requirement for **proof completeness**, not native membership verification. Cannot infer troop uniqueness or equate side participant labels (possibly Power IDs) to Unit/Troop IDs. support=[] remains permitted.
PC Windows python -B independent new tests 12/12 PASS, errors/failures 0; separately re-ran 08H 14 and 11H 15 = existing 29/29 PASS. New tests include 11H pre-existing warning reproduction, 08H attack-only shape, absent attack/defense, numeric invalid roster, unknown role, support=[], fake hashes, duplicate labels, malformed input, and synthetic no-Golden contract. NOT an actual-game test.
Verdict always VERIFY_NOT_GOLDEN, actual_golden_pass=false, strict_match=false. Positive shape or mock SHA cannot prove real map bytes, ordered deployed Unit/Troop, attack/defense Power identities, temporal consistency, or same-run G0/G1; not production acceptance.

## Golden / T019 / formal checkpoint / isolation
C-NB02 G0 lawful original UI actual attack commit+same-battle witness: NOT QUALIFIED. G1 immediate prebattle SAVE+input real bytes, SHA, clock and battle link: NOT QUALIFIED. G2 native loaded MAP SHA, 3 role identities, ordered deployed Unit/Troop, G2 within active window: NOT QUALIFIED. G3 visible result/G4 World and shared Record delta: NOT QUALIFIED.
New E DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0. Prior REA native partial captures remain separate evidence; no new original process run.
T019 newly confirmed Wiki/DAT/EXE contradiction=0. GameClear DAT13 vs TXT2 lexical search scope RESOLVED. script2 duplicate winner/phase flag, TXT runtime loader and post-GameClear gwrite still VERIFY; original-game check NOT RUN.
PC MASTER Task queue independently recounted: 34 unique IDs, DONE9 / IN_PROGRESS21 / VERIFY4. Last formal checkpoint196, READY596=A115/B229/C136/D116 inherited from PC MASTER; all 596 READY IDs not re-enumerated. New formal READY integrated IDs=none. B-20261026-09H-T028-SPATIAL-GRID-DUAL-ERASE-01 has owner readback but NOT READY; no proxy integration.
13H/14H OFFLINE-UNSYNCED evidence and prior blocked T018 table/session-join, Stage15 denied note, C T026/T032, D T030 TSV, 0x5710C0 remain unmerged/BLOCKED. New safety refusal=0, connection failure=0; denied actions not retried via shell/path/tool/Remote/ZIP.
Only new E-owned T020 Python and this report are written. Original EXE/DAT/SAVE/ZIP, MASTER, A-D, REA, dev_lab, Git/push, Work, settings and schedule unchanged.
Next: Preserve both E code generations as historical; consider E-only official acceptance after genuine same-battle G0+G1+G2 receipts with per-role roster evidence and native deployment identity. Do not promote this synthetic overlay into strict Golden or READY.

