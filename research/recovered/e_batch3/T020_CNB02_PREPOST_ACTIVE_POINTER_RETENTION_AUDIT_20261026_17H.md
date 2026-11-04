# E-AUDIT-20261026-17H-T018-T020-POSTACTIVE-PTR-RETENTION-01
Owner E / Task T018,T020 (T019 read-only) / 2026-10-26 17時台 JST / PC Local Compact / archived native log STATIC replay + synthetic negative tests / VERIFY / NOT READY / original game NOT RUN.

## Primary source and exact replay
- Watch-1: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl (234 lines), verified SHA256 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7.
- Watch-2: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl (85 lines), verified SHA256 1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46.
- Each file is analyzed separately: first/last samples satisfying mode=2 && active=1 define only OBSERVED phase bounds, not actual switch time. Count state-bearing rows with mode=1 && active=0, nonzero battlefield_ptr, before first active sample or after last active sample.
- Watch-1: BEFORE active strategic rows 72 / nonzero ptr 42 / attack_count>0 42; AFTER last active strategic rows 104 / nonzero ptr 104 / attack_count>0 104. First postactive mode1 sample 2026-10-21T14:33:35.933687Z.
- Watch-2: BEFORE active strategic rows 14 / nonzero ptr 14 / attack_count>0 14; AFTER last active strategic rows 4 / nonzero ptr 4 / attack_count>0 4. First postactive mode1 sample 2026-10-21T15:17:26.311948Z.
- **New E disaggregation:** previously counted 164 strategic-mode nonzero-pointer rows = **56 before first active** (42+14) + **108 after last active** (104+4), 0 inside observed-active span for strategic rows. These are recorded rows, not independent battles/ticks or rates. The timestamps are one observer's archived UTC stamps, not atomic native transition proof.
- Source labels PREPARED_WAR_MAP are not guaranteed in every retained-ptr row (Watch-2 13/14 before, 3/4 after). Therefore label alone cannot recover all pointer-retention cases.
- Watch-1/2 share PID23272 but represent distinct archived battles; the shared READY id was already flagged in E 14H and this study neither merges G0 reports nor cross-joins SAVE/RAW from other PIDs.

## T018/T020 acceptance consequence
- Existing 15H E result established that ptr!=0 and attack_count>0 do not prove deployed G2 while mode1. New concrete separation demonstrates the **same insufficient fields persist in mode1 AFTER the observed battle** (108 state rows). Do not use them as G3 end commit, G4 completed strategic delta, or evidence of a new battle starting.
- Suggested classification: AFTER_LAST_ACTIVE_MODE1_WITH_PTR = POSTACTIVE_RETAINED_PTR_REVIEW; BEFORE_FIRST_ACTIVE_MODE1_WITH_PTR = PREACTIVE_PREPARED_PTR_REVIEW; neither claims why old engine retains pointers nor changes source meaning.
- G3 needs native result/visible outcome and chronological source receipt; G4 needs attributable strategy World/Spot/Power/Unit state diff tied to same original battle. A retained pointer or positive attack_count is NOT a result or World diff.
- E-owned replay tests/t020_cnb02_watch_prepost_pointer_lifecycle_20261026_17H.py SHA256 8D917457CAF6AD56ED43DFB39A79016A57199E46F5FFB09FA4B0BA632F2897FA; **3/3 tests PASS**, including mismatched source hash and row-count negatives. Existing 15H predecessor independently rerun **5/5 PASS** (total 8/8). No new Ghidra/Java/game process; no source or prior E test edits.
- All code assertions remain archived-log verification / synthetic negatives: never actual Golden PASS, new gameplay DYNAMIC OBSERVED, or strict MATCH.

## Status, boundaries, continuity
- C-NB02 G0 legal original UI attack/Spot identity, G1 same-battle prestart SAVE actual bytes/SHA+input, G2 actual MAP SHA/attack-defense-support roles and ordered deployed Unit/Troop remain NOT QUALIFIED; G3/G4 unqualified. New E DYNAMIC OBSERVED 0, actual Golden PASS 0, strict MATCH 0.
- T019 newly proven Wiki/DAT/EXE contradiction 0; GameClear DAT13/TXT2 lexical-scope difference RESOLVED; script2 same-name precedence/phase flag, TXT runtime load, post-clear gwrite VERIFY (not retested).
- Formal READY newly integrated 0. MASTER most recently established cp196, READY596=A115/B229/C136/D116; last independently recounted TASK QUEUE 34 DONE9/IN_PROGRESS21/VERIFY4 (13H, inherited here), full READY ID recount NOT RUN. B 17H T028 study is STATIC/VERIFY/NOT READY; E does not proxy-integrate.
- Old safety refusals (T018 table boundary, E session-join and prior refused outputs, C T026/T032, D T030 TSV, 0x5710C0) remain BLOCKED, without retry/bypass. Prior 13/14H OFFLINE-UNSYNCED artifacts remain not formally integrated. New safety refusal 0; PC connection failure 0.
- Scope: new E-owned test + this E-owned note only. MASTER, A-D, REA, dev_lab, source EXE/DAT/SAVE/ZIP, Git/push, Work, settings and scheduling unchanged. NEXT: prioritize **same actual legal original run** UI G0 + G1 prestart SAVE bytes/input + active window+MAP/3side/ordered roster G2, then independent G3 resultCode/G4 World diff without stale-pointer substitution.
