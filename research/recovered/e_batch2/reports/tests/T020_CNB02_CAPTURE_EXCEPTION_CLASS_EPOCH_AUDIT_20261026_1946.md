# E-AUDIT-20261026-1946-T018-T020-CAPTURE-EXCEPTION-CLASS-EPOCH-01
Owner E / 2026-10-26 19:46 JST / T018-T020. T019 read-only. STATIC ARCHIVED-ORIGINAL REPLAY + SYNTHETIC BYTE-NEGATIVE EXECUTED / VERIFY / NOT READY / ORIGINAL GAME NOT RUN.
## Provenance
- Local Compact connected. Read MASTER, ANALYSIS_LANES_PROTOCOL, evidence/LANE_A-D_HANDOFF, REA decomp_task/PROGRESS, dev_lab/docs/IMPLEMENTATION_PLAN, E T018/T019, search_index README and BUILD_MANIFEST, prior E 18:49 evidence. No Ghidra reload, no original-game execution.
- Watch1 original archived search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl pinned SHA256 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7 / 234 JSONL lines.
- Watch2 original archived search_index/BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl pinned SHA256 1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46 / 85 JSONL lines.
- EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 is inherited from prior manifest, NOT independently rehashed here. Prior 18:49 already proved 28 attempts/watch and divergent reason strings; do not double count.
## Distinct new audit delta
- Error fingerprints must contain BOTH exception class and reason. Watch1 28/28 SnapshotError | unexpected nil tree node; Watch2 28/28 ValueError | Unbounded memory request. Collapsing both into generic capture_failure erases the branch-specific diagnostic; root causes are UNKNOWN.
- Attempt indices each strictly 1..28; attempt timestamps strictly monotonic. Watch1 first-to-last attempt 12.371595s within observed 116.560475s ACTIVE-to-first-inactive bracket = 10.6139%. Watch2 11.445319s within 163.920358s bracket = 6.9822%.
- Post-last-attempt to first observed inactive: Watch1 104.187638s; Watch2 152.472975s. Bracket is based on sampled states, NOT exact gameplay battle duration, and attempt-window ratio is NOT a demonstrated snapshot success/failure probability.
- T018/T020 must distinguish OBSERVED_ERROR_CLASS, OBSERVED_REASON, FAILED_ATTEMPT_WINDOW and LATE_ACTIVE_UNPROBED_WINDOW. No future late snapshot failure/success inferred; cause and recorder retry policy require B/REA owner review.
## Regression execution and limits
- E-only Python tests/t020_cnb02_capture_exception_class_epoch_20261026_1946.py: 5/5 unittest PASS, including source SHA+row pins; exact class/reason and 1..28 indices; monotonic clock; bounded attempt ratio; synthetic byte-mutation provenance rejection. Original/new engine strict comparison NOT RUN.
- Same PID 23272 does NOT collapse these two timestamp epochs or imply the same original battle. No G0+G1+G2 receipt join is qualified.
- E_G0 lawful original UI action+Spot, E_G1 same-run prebattle SAVE bytes/SHA+input, E_G2 real MAP+three sides+ordered deployed Unit/Troop, E_G3 result, E_G4 strategic World delta: all NOT QUALIFIED. New original E DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0.
- T019 new confirmed contradictions 0. GameClear DAT13/TXT2 lexical-source scope RESOLVED; script2 precedence, phase flag, TXT runtime load, post-gwrite return VERIFY.
- MASTER checkpoint196 / READY596 (A115 B229 C136 D116) and 34 Task DONE9/IN_PROGRESS21/VERIFY4 inherited previous verified state; no full READY-ID audit or Task reclassification now. New formally integrated READY=0. B-20261026-1913-T028 STATIC/VERIFY/NOT READY.
- Historical refused T018 table operation, C T026/T032, D T030 TSV, banned 0x5710C0, and refused E payloads BLOCKED; not retried/rerouted. Historical OFFLINE-UNSYNCED unintegrated.
- Changed only new E-owned Python test and this E-owned report; no MASTER, A-D, REA, dev_lab, original EXE/DAT/ZIP/SAVE, Git, Work, settings or automation changes.
## Next authorized action
- Obtain lawful C-NB02 same-battle G0 UI, G1 SAVE+input and G2 MAP+three-side roster original receipts. Do not turn exception taxonomy into native root-cause proof. Recorder engineering follow-up on class/retry budget belongs to B/REA, not E.
## Recovery
- E-RC-20261026-1946-REPORT-TEMPLATE-OTHER-01: initial JS orchestration of this report failed before invoking a write (unescaped delimiter), OTHER/RECOVERED by composing a distinct valid text string. No safety refusal; original failed output discarded.
