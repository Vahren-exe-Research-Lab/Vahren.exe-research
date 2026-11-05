# E-AUDIT-20261027-0345-T020-T028-HASH-ORDER-CONDITIONAL-DIVERGENCE-01
Owner E / T020, linked T018; 2026-10-27 03H JST; PC-SAVED / STATIC SOURCE REVIEW + CONDITIONAL SYNTHETIC TESTS / VERIFY / NOT READY / ORIGINAL GAME NOT RUN.
## 出典・増分
Desktop Commander Local CompactでMASTER TASK QUEUE、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA PROGRESS、dev_lab IMPLEMENTATION_PLAN、E T018/T019と02H T020、旧search_index README/BUILD_MANIFESTを参照。
B-owned 03H source: data/T028_CACHE_DUPLICATE_INSERT_ROLLBACK_NATIVE_20261027_03H.md actual byte SHA256 532489082933B1E06408886DB6346B5CCF3100CA8F5D34CBF5AE4AAF0C22D04A。
B-owned 01H source: data/T028_ROUTE_CACHE_THRESHOLD_PROMOTION_NATIVE_20261027_01H.md actual SHA256 948B343D87621DEB9960E119A827DBBAA515ABD0F4BC67B05B415972FA5F8E36。
Bundled EXE baseline hash E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 is inherited B original-PE witness; E has not rehashed/launched EXE in this run.
## 分離すべき2種類の構造
B original PE source states 0x4EC4BD→0x4ED350→0x4FC710: same-key insert returns prior hash node, inserted=0 and releases new temporary node via 0x4FC7E9→0x4FC920. The hash node count is rolled back.
Separate 0x4EC4CC→0x4EC640 order-list append is seen after 0x4EC4BD on miss path; the 03H B report does NOT prove a legal original-game duplicate can reach this path, nor all caller invariants.
CONDITIONAL COUNTEREXAMPLE ONLY: if a key already in hash reaches that insertion path and the order append still occurs, hash keys [7] / order keys [7] become [7] / [7,7] after rejected insert. Evicting head once then yields hash [] / order [7] in the deliberately simplified model.
Thus hash-key uniqueness cannot BY ITSELF certify matching hash/order counts, safe eviction or payload lifetime. This is not a confirmed original-game bug, not a confirmed reachable original condition, and not a reason to patch owner-B code.
## 新規T020実行結果と受入条件
Created tests/t020_t028_hash_order_duplicate_window_20261027_03H.py; actual SHA256 454F82C21119288A136A04C94C0AEF6591A6AEA0DAF4FB0F5D210C9FD8D5E0BC.
Windows python -B -X utf8: 6/6 synthetic unittest PASS, 0 failure. New-key balance, duplicate with conditional append, suppressed append alternative, head eviction orphan example, distinct key case, gameplay false-status checks.
Strict capture requirement for future: actual original insertion key, lookup outcome, returned inserted flag, hash and order counts PRE/POST, evicted head identity, original EXE/DAT/SAVE/MAP/input hashes, run/session/battle/clock coherence, Unit+0x186B0 effect; missing field must remain VERIFY/NOT QUALIFIED.
No binary/actual gameplay execution. Synthetic 6/6 is NOT original Golden PASS and NOT strict MATCH; hash/order divergence is entirely conditional and cannot be called gameplay-observed.
## MASTER / Golden / T019 / safety
MASTER 34 TASK QUEUE lines independently read/recounted: 34 unique IDs, DONE9, IN_PROGRESS21, VERIFY4. Latest official checkpoint196 / READY596=A115/B229/C136/D116 inherited, no all-READY reenumeration. Newly accepted READY IDs none. Latest B 03H is STATIC / VERIFY / NOT READY.
C-NB02 old lawful G0 UI+Spot, G1 same-battle immediate prebattle SAVE bytes+input, G2 real loaded MAP+three sides+ordered deployed Unit/Troop, G3/G4 all NOT QUALIFIED. E new gameplay DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0.
T019 newly confirmed Wiki/DAT/EXE contradiction=0; GameClear DAT13/TXT2 lexical-scope RESOLVED; script2 same-name winner/phase flag/TXT runtime/gwrite return all VERIFY.
Prior safety refusals T018 table/session-join, C T026/T032, D T030 TSV, 0x5710C0 and other owner records remain BLOCKED, no reattempt/alternate route. Old OFFLINE-UNSYNCED not integrated. New refusal/connection error none.
Writes limited to independent E-owned new test and report. No MASTER/A-D/REA/dev_lab/original EXE/ZIP/SAVE/DAT/Git/push/Work/settings/automation mutation. Original P0 path remains missing real same-battle G0/G1/G2 receipts; next priority is obtaining those legally, not adding synthetic cache tests endlessly.
