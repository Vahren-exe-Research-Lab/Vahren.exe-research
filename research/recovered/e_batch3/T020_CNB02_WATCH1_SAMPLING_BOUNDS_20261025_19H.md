# E-AUDIT-20261025-19H-T018-T020-WATCH1-SAMPLING-BOUNDS-01
Owner E / T018,T020. 2026-10-25 19H JST. LOCAL ORIGINAL-LOG READ-ONLY / STATIC VERIFIED / VERIFY / NOT READY / ORIGINAL GAME NOT RUN.
## Provenance and delta
Primary original watch (existing 2026-10-21 capture): rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl.
Source SHA256 independently rechecked: 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7. 234 JSONL records, 204 state/initial observations in this read, PID23272 per prior source report.
Earlier 18H study computed the gaps between FIRST OBSERVED new states: MODE2→ACTIVE=1 2.814309s; ACTIVE=0→MODE1 1.607820s. This is NOT the exact duration of engine-internal transitions.
## Four first-change observation brackets (UTC, prior old observation < actual edge <= first new observation, subject to single-edge/no-hidden-toggle assumption)
1 MODE 1→2: last old 14:31:32.740234; first new 14:31:34.951083; uncertainty span 2.210849s.
2 ACTIVE 0→1: last old 14:31:37.664712; first new 14:31:37.765392; uncertainty span 0.100680s.
3 ACTIVE 1→0: last old 14:33:33.521048; first new 14:33:34.325867; uncertainty span 0.804819s.
4 MODE 2→1: last old 14:33:34.325867; first new 14:33:35.933687; uncertainty span 1.607820s.
Conditional lag envelopes: 2.713629s < true MODE2→ACTIVE lag < 5.025158s; 0s < true ACTIVE=0→MODE1 lag < 2.412639s. Exact engine switch times NOT observed. No claim of continuous observability or wall-clock precision guarantees.
## T020 regression acceptance design (DESIGNED / NOT RUN)
B01 capture inside MODE-transition bracket is PHASE_BOUNDARY_VERIFY, not proven before/after MODE2.
B02 capture between first observed MODE2 and last observed ACTIVE=0 is PREACTIVE_REVIEW_ONLY, never final deployed roster without same-run atomic G2 evidence.
B03 capture inside ACTIVE-enter bracket is PHASE_BOUNDARY_VERIFY, not automatically ACTIVE_G2_ELIGIBLE.
B04 capture inside ACTIVE-exit bracket is PHASE_BOUNDARY_VERIFY, not automatically ACTIVE_G2_ELIGIBLE.
B05 capture after confirmed ACTIVE=0 while MODE2 may persist is NOT_DEPLOYED_G2.
B06 distinguish source UTC six-digit timestamps from rounded secondary seconds fields; never assert microsecond-exact engine time from any log entry.
Parsing/assert audit: 234 JSONL rows, four transition edges, 6/6 internal structural numeric assertions PASS; no new reusable test script and no native gameplay run. Fixture JSON saved separately by E for independent future runner.
## G0/G1/G2 and exclusions
G0 old legal sci1 po2 sp2→sp16 UI+attack not qualified. G1 same battle pre-start SAVE bytes/SHA plus input not qualified. G2 real loaded MAP, attack/defense/help identity, ordered deployed Unit/Troop and coherent capture not qualified. G3/G4 not qualified. Actual E DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0.
T019 new Wiki/DAT/EXE contradiction=0; GameClear DAT13/TXT2 lexical source scope RESOLVED; script2 winner/phase flag/TXT runtime load/post-GameClear gwrite VERIFY (not retested). No new READY integration.
MASTER checkpoint196/READY596=A115/B229/C136/D116 inherited; TASK QUEUE independently read: 34 unique (DONE9 / IN_PROGRESS21 / VERIFY4). All READY IDs NOT recounted.
Prior safety refusals, T018 table boundary, C T026/T032, D T030, 0x5710C0 remain BLOCKED with zero reattempt; 13H/14H OFFLINE-UNSYNCED unintegrated. Source/other owner/EXE/DAT/SAVE/ZIP, MASTER, Git, Work, automation/settings unchanged.
NEXT: acquire legal same-run original G0 UI and G1 SAVE+input and an actual timed G2 capture with MAP/3 sides/ordered deployed roster; record before/after phase guards and clock calibrations. Treat bracket overlap as VERIFY rather than disqualifying all preactive evidence or incorrectly promoting active samples.