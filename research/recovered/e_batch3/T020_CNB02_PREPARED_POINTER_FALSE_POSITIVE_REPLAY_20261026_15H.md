# E-AUDIT-20261026-15H-T018-T020-PREPARED-PTR-FALSEPOS-01
Owner E / Task T018,T020; 2026-10-26 15時台 JST。STATIC archived-native replay / SYNTHETIC/ASSERTIONS EXECUTED / VERIFY / NOT READY / original gameplay NOT RUN。

## Evidence and new quantified delta
- Existing Watch-1: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl; 234 JSONL rows; real SHA256 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7.
- Existing Watch-2: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl; 85 JSONL rows; real SHA256 1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46.
- New E-only per-row replay: tests/t020_cnb02_prepared_pointer_false_positive_replay_20261026_15H.py; SHA256 6893047A33218D2EAA068827C8559619CC159638B5FC44D4F748899631B63A61.
- Watch-1: state-bearing log rows205; battlefield_ptr !=0 rows175; **mode1/active0 AND ptr!=0 rows146**; mode1/active0 AND attack_count>0 rows146; PREPARED_WAR_MAP label among strategic rows146; mode2/active1 and ptr!=0 rows25.
- Watch-2: state-bearing rows56; ptr!=0 rows56; **mode1/active0 AND ptr!=0 rows18**; mode1/active0 AND attack_count>0 rows18; PREPARED_WAR_MAP label among strategic rows16; mode2/active1 and ptr!=0 rows35.
- Numerator/denominator count *recorded rows*, not independent units/ticks/battles. Different sampling periods and duplicate source snapshots (e.g. SCENE_EXIT_CANDIDATE) mean these are NOT event frequencies/probabilities. Watch-1+2 are separate real original observation windows; do not cross-join.
- Both archived traces explicitly report captures_saved=0; per-row packet-complete predicate found0 in each. Previous E 2026-10-22 06H had already described the nonzero PREPARED pointer *qualitatively*; new increment is the source-SHA-locked quantitative two-trace false-positive coverage and executable assertion.

## T018 / T020 acceptance refinement
- **Unsafe heuristic:** battlefield_ptr !=0 OR attack_count>0 OR label=PREPARED_WAR_MAP is sufficient for deployed G2. The archived logs contain many strategic-mode counterexamples.
- **Necessary but not sufficient:** mode=2 AND active=1 must be an explicitly time-bounded, same-source observation to consider G2 capture time for further review. Even active/ptr!=0 says nothing about actual real MAP bytes, three side membership, ordered Unit/Troop, SAVE/input, frame atomicity or original UI legality.
- WATCH snapshot metadata is not a Golden result. Same PID/source EXE/READY label collision described in previous 14H audit remains separate; the new runner reads each trace independently and performs NO cross-session/G0/SAVE join.
- Current C-NB02 legal old UI G0, same-battle G1 prestart SAVE bytes+input, and G2 actual MAP/3 sides/deployed Unit/Troop remain NOT QUALIFIED; G3/G4 also NOT QUALIFIED. E new gameplay DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0.
- New test: Windows `python -B -X utf8` 5/5 PASS; old 2026-10-25 21H dual-watch test independently rerun 8/8 PASS; 13/13 total, new only5. Original EXE and Ghidra not started.

## MASTER / T019 / safety / integration
- MASTER read-only final formal checkpoint196, official READY596=A115/B229/C136/D116 (per last existing formal record; every READY ID was NOT recounted). 34 Task DONE9 / IN_PROGRESS21 / VERIFY4 from prior 2026-10-26 13H checked count, NOT independently recounted in this run.
- Official new READY integration0; B 2026-10-26 13H/14H T028 information is STATIC/VERIFY/NOT READY (no proxy integration). The previously reported 13H/14H OFFLINE-UNSYNCED E artifacts remain unintegrated.
- T019 new confirmed Wiki/DAT/EXE contradiction0. Prior GameClear DAT13/TXT2 source-lexical scope difference RESOLVED; script2 duplicate selection/phase flags, TXT runtime load and post-clear gwrite still VERIFY; none retested in this run.
- Prior safety refusals T018 table boundary, E rejected session-join/DAT writes, C T026/T032, D T030 TSV and 0x5710C0 remain BLOCKED, with no replay/bypass. No new safety refusals. Initial one-off Python `-c` command had PowerShell/quoting SyntaxError (OTHER; no output accepted), recovered by independently authored E-only runner. This is not a safety refusal.
- Scope: new E-owned runner and this E-owned note ONLY. MASTER, T018/T019, A-D, REA, dev_lab, original EXE/DAT/SAVE/ZIP, Git/Work, settings and automation unchanged. Sources read-only; all counts are observation-log row counts, not new game results.
- NEXT: prioritize lawful unmodified same-run C-NB02 G0 UI + source/target Spot proof, G1 prestart SAVE raw-byte SHA/input and clock-bound capture, G2 actual MAP SHA + all sides + ordered deployed Unit/Troop; pointer-only prepared-state labels never substitute for those receipts.
