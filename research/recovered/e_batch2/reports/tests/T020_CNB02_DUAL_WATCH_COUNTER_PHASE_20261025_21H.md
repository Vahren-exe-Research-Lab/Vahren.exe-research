# E-AUDIT-20261025-21H-T018-T020-DUAL-WATCH-COUNTER-PHASE-01
Owner E / T018,T020 / 2026-10-25 21H JST. Evidence: archived original native watcher replay; STATIC/VERIFY/NOT READY. No new gameplay execution.
## Read-only source evidence
- Watch1: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl; 234 JSONL records; SHA256 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7.
- Watch2: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl; 85 JSONL records; SHA256 1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46.
- Both hashes independently rechecked on PC with read-only Get-FileHash; same PID23272 does NOT mean the two logs describe the same battle.
## New bounded delta; observation timestamps are not engine transition instants
- In Watch1, attack_count fluctuates at least 10 times before first observed mode1->mode2, including DECREASES and repeated values. It is NOT a monotonic battle ID or one-to-one proof of G0.
- Watch2 attack_count 1->2 is bracketed (15:14:31.628166, 15:14:35.148607] UTC while mode remains 1 and active remains 0. Earliest next mode1->mode2 bound is after 15:14:36.656388 UTC, a minimum gap exceeding 1.507781 seconds; so count increment alone must not be promoted to battle start.
- Watch2 mode1->mode2 bracket (15:14:36.656388, 15:14:37.460907] width 0.804519s; active0->1 bracket (15:14:37.863199, 15:14:40.580007] width 2.716808s.
- Under explicit no-hidden-transition/observer-clock assumptions, Watch2 mode2->active1 actual interval is >0.402292s and <3.923619s (Watch1 previously >2.713629s and <5.025158s). Fixed phase duration cannot be inferred.
- Watch2 active1->0 bracket (15:17:22.790812, 15:17:24.500365] width 1.709553s; mode2->mode1 bracket (15:17:24.500365, 15:17:26.311948] width 1.811583s. world_mode toggles 0->1->0 at entry and exit in BOTH logs; not a persistent G2 identity flag.
- Both logs each contain 28 CAPTURE_VERIFY_GAP entries, with no completed battle packet. They are stored original observations but NOT real G2 MAP/three-side/ordered deployed roster receipts.
## Executable T020 archive replay
- New E-only runner: tests/t020_cnb02_dual_watch_counter_phase_gate_20261025_21H.py; SHA256 B2C27CB98B739401917E47F4D2D952BDC948CD02137F452170ECB1FF945C39B4.
- Python -B replay: 8/8 tests PASS, 0 FAIL; pins both source hashes and row counts, checks session separation, attack_count reversal/pre-mode change, four mode/active edges per watch, exact Watch2 interval bounds, world_mode transient toggles, and absence of completed packets.
- Tests replay pre-existing raw log data; this is not a new native execution, golden Gameplay PASS, or strict old/new MATCH. Neither prior 19H/20H verifier nor source logs were altered.
## Acceptance / integration / safety
- G0 lawful sci1/po2/sp2->sp16 UI+input, G1 same-run prestart SAVE bytes/SHA and input, G2 actual MAP+attack/defense/support IDs and ordered deployed Unit/Troop, G3 result and G4 World diff all remain NOT QUALIFIED.
- Original E Gameplay DYNAMIC OBSERVED added 0; actual Golden PASS 0; strict MATCH 0. Synthetic/regression PASS must not count as Golden.
- T019: no new confirmed Wiki/DAT/EXE contradiction. GameClear DAT13/TXT2 lexical-scope difference RESOLVED; script2 duplicate precedence/phase flag, TXT runtime read, post-clear gwrite still VERIFY, not retested.
- MASTER latest formal cp196/READY596=A115/B229/C136/D116 (all READY IDs not recounted). TASK QUEUE directly recounted: 34 unique, DONE9/IN_PROGRESS21/VERIFY4. New READY integration 0; new B-20261025-2117-T024 is STATIC/VERIFY/NOT READY.
- Existing safety refusals (T018 table boundary, E legacy, C T026/T032, D T030 TSV, 0x5710C0 etc.) remain BLOCKED without retrial or workaround. 13H/14H OFFLINE-UNSYNCED E artifacts not promoted. E-owned new runner and this note only; MASTER, A-D, REA, dev_lab, originals, Git/Work, settings/schedule unmodified.
- Next: acquire lawful same-run G0 UI and G1 SAVE/input plus G2 actual live MAP/three-side/deployed Unit/Troop with source byte hashes and timestamps; never join Watch1 and Watch2 by PID, attack_count, pointer, or filename alone.

