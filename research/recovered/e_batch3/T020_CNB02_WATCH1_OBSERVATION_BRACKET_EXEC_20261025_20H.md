# E-AUDIT-20261025-20H-T018-T020-WATCH1-OBSERVATION-BRACKET-EXEC-01
Owner E / T018,T020. 2026-10-25 20H JST. STATIC stored-original-log timing / SYNTHETIC regression / VERIFY / NOT READY; original gameplay NOT RUN.
## Primary evidence and hashes
Original existing watcher: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl, 234 JSONL rows, PID23272 by prior native report.
Local read-only Get-FileHash current source SHA256=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7; matches prior 19H receipt.
Input 19H fixture: tests/T020_CNB02_WATCH1_SAMPLING_BOUNDS_20261025_19H.json; SHA256=E5AEA5AA06EDC33AE2CED416AD1BAB7754EB01213BE98E80DBF3A7232A06475E; no modification.
Base original EXE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (existing manifest, not rehashed this run).
New E-owned runner: tests/t020_cnb02_watch1_observation_bracket_gate_20261025_20H.py; final SHA256=F2F152A6A7B0F1B6E92E4AB1E492D560F1EE4F2FB52C107A1F1C5D0F7A545805.
## New executable crosswalk and resolved regression mismatch
Converted the 19H B01-B05 timestamp cases into runnable assertions without changing 17H/18H validators or 19H JSON.
First run: 6 test methods, B05 subcase FAIL: naive mode-return uncertainty classifier emitted PHASE_BOUNDARY_VERIFY for 14:33:35 UTC, while 19H expected NOT_DEPLOYED_G2.
Independent logic check: 14:33:34.325867 UTC already confirms ACTIVE=0 in saved watcher; MODE2->MODE1 is bracketed through 14:33:35.933687. Subject to single-edge/no-hidden-toggle and common observer clock, deployed-active G2 is excluded in this interval despite uncertainty about return-to-mode1 time.
Corrected only this new E file: B05 status NOT_DEPLOYED_G2 plus independent mode_return_uncertain=true. No change to archived source/19H fixture. The initial failure is a new regression-model bug, not a native-game bug or safety refusal.
Final python -B run: 6/6 methods PASS including B01-B05 subcases, B06 no actual G2 timestamp, known-active review only, mode return uncertainty, uncalibrated/naive clock, source-hash and corrupted-bracket negatives.
Existing 18H phase classifier independently rerun python -B: 6/6 PASS. Total final 12/12 unittest methods, new 6; no actual Golden assertions.
New classifier never emits original_gameplay true, actual_golden_pass true, strict_match true, or engine_transition_time_known true. It uses the 19H source-hash receipt + bracket timestamps, not fresh memory reads.
## Golden acceptance, T019, MASTER, and safety
G0 legal old UI sci1 po2 sp2->sp16, G1 same-battle prestart SAVE bytes/SHA plus UI input, G2 observed real MAP + 3 sides + ordered deployed Unit/Troop remain NOT QUALIFIED. G3/G4 also unqualified.
Source watcher timing is historical original observation only; no actual G2 capture is present. New E DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0.
T019 newly confirmed Wiki/DAT/EXE contradictions=0; GameClear DAT13/TXT2 lexical scope RESOLVED, script2 precedence/phase flag/TXT runtime load/post-clear gwrite remain VERIFY, not re-proven here.
MASTER final checkpoint196 / READY596=A115/B229/C136/D116 inherited (READY IDs not recounted). TASK QUEUE freshly parsed: 34 unique; DONE9, IN_PROGRESS21, VERIFY4; T018/T019/T020 remain IN_PROGRESS.
New READY formal integration=0. B-20261025-2008-T024 is STATIC/VERIFY/NOT READY; other owners not modified or proxy-integrated.
Existing refusals T018 table boundary, C T026/T032, D T030 TSV, 0x5710C0, and E legacy blocked operations remain BLOCKED; zero reattempt or alternate route. 13H/14H OFFLINE-UNSYNCED remains not formally integrated.
Only new E-owned T020 Python and this note written; source watcher, JSON, MASTER, T018, T019, A-D, REA, dev_lab, EXE/DAT/SAVE/ZIP, Git, Work, settings, schedule untouched.
NEXT: original legal same-run G0 UI, prestart G1 SAVE bytes+input, time-calibrated G2 MAP/three side/ordered deployed Unit+Troop with before/after guards. If true timestamp falls inside watcher bracket, keep VERIFY without inferring internal engine switch time.
