# DAT明示呼出・3候補の往復実証 Implementation Plan

> For agentic workers: use superpowers:subagent-driven-development or superpowers:executing-plans task by task. User approved the minimal spike and agents; no repeated approval for this scope.

**Goal:** 作業コピーのDATが3候補と独自数値列を渡し、既存UIで検索・ソート・選択し、結果をDATへ1回だけ返す。
**Architecture:** Core管理の明示要求入口と原作非依存の表UIを分離。DATが候補と独自値を所有、UIは表示と選択のみ。入口ABI・待機方式はTask1の根拠を通過条件に確定する。
**Tech Stack:** 32bit Windows C/DLL、既存Core、Win32 ListView、DAT、Zig。
**Spec:** DAT_GENERIC_UI_DESIGN_REVIEW_20261026.md。2026-10-26ユーザーが最小実証を承認。

## Global Constraints
- 原作EXE/原本DAT/save変更なし。試験はstartup_clean_20261025作業コピー。Git操作なし。既存成果保持。
- 旧拒否対象3ファイルの変更・同じ拒否操作の別経路迂回は禁止。該当時は明示する。
- 教育/アイテム効果は実行しない。別イベント/ロード/終了後の返却は禁止。未確認ABIでnative callを作らない。
## Review Focus
- 同定義の別個体、空/重複候補、取消不可、plugin欠落/不正引数、二重確定/古い要求への返却。
### Task1: 接続根拠
- [ ] tests/work_dat_ui_dispatch_evidence_20261026.json（hover_dispatch_thunk）：入口ABI、pc/yield、Core競合を照合。未解決は実機接続を止める。
- [ ] tests/work_dat_ui_result_evidence_20261026.json（adapter_review）：choice返却と変数所有権を照合。既存8件ページ変換を汎用結果へ流用しない。
### Task2: 独自列UI
- [x] src/work_selector_panel.hに独自数値列の入力を追加。元順/昇降順/同値安定/欠損末尾/検索後source_index一致をfixtureでRED→GREEN。root PID3264 exit0、既存表回帰PID4372 exit0。
- [x] request単位の列配列を渡す。global unit bonusは作らない。既存教育APIは保持。hidden Win32結合PID12200 exit0。ただしDATの実機受渡しはTask3で未完。
### Task3: コピー限定の往復
- [ ] Task1で入口/待機/結果契約を確定してからCore adapterを実装。3候補/独自列1件/前後カウンタDATを作業コピーに追加。
- [ ] 表示中の後続未実行、確定後1回再開、候補一致、取消、連続2回、plugin無効、不正引数を確認。結果変数は先に初期化。
### Task4: 記録
- [ ] build/fixture/liveを区別し、キュー/handoff/indexへ記録・読戻。往復完了まで教育へ移行しない。

## 2026-10-26 実装契約の補足（最小実証限定）
- ユーザー再確認：補正・予想結果はDATが渡す。新経路のDLLに教育種別推測/教育DAT再解析/教育式を追加しない。
- Task1の静的根拠2件保存済み。入口433B62→4A1250は候補であり実機接続未検証。ALによる単発yieldをUI待機と混同しない。
- 最小DAT fixture: data/recruit_sort_v4/tests/work_dat_ui_spike_v1.dat（未配置）。数値はsetで作り、setv/addvには数値変数名を渡す。リスト内文字列を数値文字列として解釈しない。
- 数値参照は既存キーの完全一致・件数一致・読取可能性を検証しコピー。未存在を0扱いしない。検証でfind-or-create関数463CA0を呼ばない。
- 確定0..2、取消は3のみ、それ以外ERROR。OKだけDAT indexでIDへ変換。backend=0は原作choiceへのfallbackでありDLL経由成功ではない。
- fixture静的parseと構造検査PASS、SHA256=57cf3d5aebea79cfa8a22b9e70c0bfae7fbda9eecffd9dbc000045ec9d7efe20。原作実行とDLL往復は未検証。
- Task2汎用数値列を別agentが実装中。別agentは3候補の要求寿命/一度だけ返却をnative非依存の小さな契約として検証。共用ファイル編集なし。

## 2026-10-27 再開時点の実態（上記2026-10-26の未配置記述を更新）
- 読取probeは作業コピーで接続済み。DAT候補/値/列の読取、原作fallback KMR確定・Cancelの各1回再開を確認済み。新表からの実機返却は未完。
- request/snapshot/binding/session/独自列UIの結合fixture PID32040 exit0。native操作は模擬であり実機完了ではない。
- core/dat_ui_selector_plugin.c/.def/build_dat_ui_selector.ps1を回収。root -Test PID32232 exit0。入力コピー/不正phase失効まで実装。initは常に拒否し、hook/表/返却未接続・未配置。このDLLを利用者へ配布しない。
- 次の実装根拠: tests/work_dat_ui_lifetime_evidence_20261027.json。7 scene reset CALL、通常load、title確認、choice close/hideを列挙。閉じるslotのみではqueue resetを捕捉できない。opening epochと別のlifetime epochを導入する方針。残るdirect hide/teardown経路と部分install失敗の保持条件を確認後に組み込む。

## 2026-10-27 現行実装と実機再開条件（以前の未接続記述を置換する追記）
- Task1: dispatcher/evaluator/context根拠と原作fallbackのKMR確定・明示Cancelは確認済み。独自DLLからの返却成功とは区別する。
- Task3 adapter: 9 CALL + 3 pointerの有限lifetime監視、別opening/lifetime世代、owned snapshot/binding、一度だけordinal/backend保存、原作close接続まで実装済み。init常時拒否という前記は旧段階。独立レビューで発見したACTIVE opening変更後の残留パネルを修正済み。
- build_dat_ui_selector.ps1 -Test root session96338 exit0。DLL SHAab6ac8cfe9c02fe63c4cd97548ad3e5e60ee199900b01530070c18cce6930f28、現行receiptに反映済み。未配置・未arm・DAT再開未検証。3候補の固定実証であり汎用API完成ではない。
- 実機ゲート: (1)診断用コピーの手操作Continueが有効か確認、(2)旧selector/recruit/probeと同時接続しない設定でgeneric DLLのみ検証、(3)タイトルで手動arm、(4)DAT UI Spike v1の表で値30/55/10とBonus、待機中after0確認、(5)ソート後KMR確定でindex1/backend1/status1/selectedkmr/before1/after1、(6)取消は原作fallbackへ戻り、古い要求を再実行しない、(7)連続要求・title/loadで旧表の返却を拒否。各操作前後のidentityとログを保存する。
- 現在は自動入力が原作のみでもContinueに作用せず、手操作比較をユーザーへ通知済み。DLLの不具合と断定せず、同じ起動/テストを繰り返さない。現行診断ゲームは終了、loader/recruit/hover-selector設定は復元済み。原本やセーブ変更なし。

### 2026-10-27 generic native lifecycle and display checkpoint
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Stop VA 0041E7E3/0041E6D0; next native visible panel and DAT result verification. User renewed all game operations; no duplicate launches.
- PID28480 first native trial copied values but title input polling advanced lifecycle on every poll (lifetime53525). Fixed title gate to preserve native post-refresh predicate, invalidate only real title/exit request. Full native prefix/epilogue and reservation checked. O0/O2 lifecycle RED then GREEN, 1000 idle polls, independent review no blocking findings. Added bounded once-per-serial invalidation diagnostics.
- Full build_dat_ui_selector.ps1 -Test exit0. DLL SHA912f1141009e0c4e133c1f54f61eafb40e3d80bf9e959b5284db3e6114d96d4d copied/hash-matched to diagnostic-only plugins. Only generic selector enabled. Legacy manifest backup WORK_PRE_GENERIC_MANIFEST_20261027.conf remains available.
- Native PID23992 HWND15599450 manually armed once at observed initial title (start134375392050132559); patch_active code0. Easy -> DAT UI Spike -> operation faction reached. request_copied serial1 lifetime6 values30,55,10 and panel_active. Accessibility confirms Names/Bonus and AKYS30,KMR55,TNOK10 controls, but screenshot shows only native four choices. panel_active is NOT visible-render acceptance. Native result/DAT resumption not tested; Golden/MATCH remain0.
- Display difference: new panel is direct GDI child of main game; existing working preview uses owned popup surface. Likely drawing conflict, not established solely from log. Agent generic_choice_binding implementing minimal owned-surface change with regression tests in core/dat_ui_selector_runtime.h and core/test_dat_ui_selector_native.c only; no protected src edits.
- Root closed diagnostic PID23992 with normal Alt+F4; process enumeration confirms zero Vahren. Original EXE/DAT/saves unchanged, no deletion. Source/test success distinct from runtime result. Next build/review/deploy new display fix, then observable selection and actual DAT return.

### 2026-10-27 generic native selection SUCCESS; cancellation test pending
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Minimum fixed-three selection path now native verified, not full generic production API. Stop VA0041E7E3/0041E6D0. Owned popup fix and actual WM_ENABLE(TRUE/FALSE) successor-request regression passed RED/GREEN; independent rereview no blocker. Full build_dat_ui_selector.ps1 -Test session23520 exit0 (O0/O2).
- Current diagnostic DLL SHA3d2779cffde4ccd9d9c0ab7b1f8d04327a50d9393e86d1428c96158ad224c43c; only generic enabled. Source runtime bb2415ed95a1d9d7e02c297aef666db1e415c52b2d3fcbb4fd89655f7120466e, nativefixture c3f75331ca39a16bf52bdd2c4a909cbe4ba29fba062986530938cfe700c26db0.
- sky.launch_app produced PID33708 with no HWND/no plugin log; bounded checks unchanged. After exact-path/no-window identity confirmation, stopped that process and verified zero Vahren; Explorer launch succeeded. Prefer Explorer launch for this game; no duplicate processes.
- Native PID23792 HWND18679496 start134375447920166696, manual initial-title arm cookie4b70853d2d32587f -> patch_active0. Easy/DAT UI Spike/operation faction: visible generic popup AKYS30/KMR55/TNOK10. Bonus header click sorted ascending TNOK10/AKYS30/KMR55. Selected third visible row KMR; confirm closed popup and native choice. Screenshot of original DAT message: Result=kmr; Status=1; Before=1 After=1; Backend=1. Native_result log one entry. This proves fixed-three sorted identity return and one DAT resumption in this trial; no general lifecycle/fullscreen coverage or Golden/MATCH claim.
- Minor usability issue: confirmation returned foreground to Explorer; activating original game revealed result. Owner foreground restoration should be reviewed later.
- Advanced result to strategy turn1, sent Escape to return title for cancellation trial. Next capture reported physical Escape user stop. No further Computer Use calls made. Game may remain running PID23792; enumerate and inspect before any input/restart. Need explicit renewed automatic-input permission under tool stop rule. Cancel/native fallback, repeated requests, title/load stale validation remain pending.
- Copied native log to _work/claude_loader_patches_20261026/WORK_GENERIC_NATIVE_23792.log. Original EXE/DAT/saves unchanged by agent; no save operation/deletion. Diagnostic scenario may perform its own normal runtime behavior.

### 2026-10-27 resumed native cancellation verification
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL; stop VA0041E7E3/0041E6D0. User renewed autonomous PC permission after pause. No duplicate launch; diagnostic PID31876 HWND4392170 start134375491753844200 armed once at observed initial title, cookie f88ec6c091250894. Current DLL SHA3d2779cffde4ccd9d9c0ab7b1f8d04327a50d9393e86d1428c96158ad224c43c; generic plugin only.
- Easy -> DAT UI Spike -> operation faction displayed AKYS30/KMR55/TNOK10. Right-click within popup closed overlay; after reactivating game, original four choices remained waiting. Native Cancel left-click produced actual DAT screen Result=(empty), Status=2, Before=1 After=1, Backend=0. No plugin native_result entry in this run. This verifies fallback cancellation without plugin selection commit and single DAT resumption; not a direct plugin-returned cancellation API.
- Foreground-to-Explorer issue reproduced on popup cancellation, matching prior confirmation run. generic_choice_binding owns runtime/header + native fixture for bounded cleanup-order investigation/fix; root owns deployment/records/game. No protected src edits, original EXE/DAT/save modifications or file deletion.
- Native evidence copied to ../_work/claude_loader_patches_20261026/WORK_GENERIC_NATIVE_31876.log. Remaining: foreground cleanup repair acceptance, repeated requests/stale actual-game validation, disabled/malformed request behavior, full generic candidate API and education/item integration. Do not claim full completion or Golden/MATCH.

### 2026-10-27 generic selector native acceptance and foreground repair
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Stop VA0041E7E3/0041E6D0. Fixed-three minimum path accepted; full general API and education/item integration remain unfinished. This supersedes earlier native-only BLOCKED/pending entries.
- Cleanup repair: re-enable originally-enabled owner BEFORE destroying popup; detach globals first for reentry. No forced foreground call. Agent RED exit1 then GREEN O0/O2 actual WM_ENABLE/WM_DESTROY assertions; root build_dat_ui_selector.ps1 -Test session23538 exit0; independent exact-source review found no blocker.
- Current DLL SHA cdc4554cf9ab4f542c0360a52b92b4d975a415418eb5bbb3d286322ab0a67438. Runtime SHA4140d098c43d0dc7d4d44b4888340568a8a67c7e68523c1b6c3731e7238354d4; native fixture SHAf814179425e2561af6bb5010d41aed7896ac94f38996414ba5e49c8cb46b6e38.
- PID20596: right-click closed only custom panel, kept game foreground and native choice waiting. Native TNOK gave Result=tnok Status1 Before1 After1 Backend0. Same process title-return/reopen reused evaluator/VM addresses but created serial2/lifetime13 (prior serial1/lifetime6). Bonus ascending sort then first visible TNOK returned Result=tnok Status1 Before1 After1 Backend1; exactly one native_result entry; foreground retained.
- PID34556 plugin-disabled control: no Hakushin module, empty-plan log; native AKYS returned Result=akys Status1 Before1 After1 Backend0. No custom table, normal event continued.
- PID32404 malformed-input control: diagnostic DAT referenced missing numeric variable instead of value1. Plugin armed/patch_active but rejected request, native four choices remained. Native Cancel produced empty Result, Status2 Before1 After1 Backend0. Log reason is generic request_rejected, not a dedicated missing-variable diagnosis.
- Original diagnostic DAT restored byte-for-byte SHA c9a96d9c6f83d21ef674b87f893219d4f58945bf174b24ecbdf000027cf4aef2 after normal game closure. Zero Vahren processes verified. Generic-only diagnostic manifest enabled; manual initial-title arming still required. Original game EXE/DAT/save not edited; no file deletion or explicit save operation.
- Evidence: ../_work/claude_loader_patches_20261026/WORK_GENERIC_ACCEPTANCE_20261027.json; WORK_GENERIC_NATIVE_20596.log, WORK_GENERIC_NATIVE_32404.log, earlier WORK_GENERIC_NATIVE_31876.log. Updated ../../data/recruit_sort_v4/core/dat_ui_selector_build_receipt_20261027.json reconciles current hashes and native evidence.
- Recommendation: DAT owns candidates/calculations, DLL owns table and selection. Next bounded proof: opt-in 2/4 candidate cases with one custom numeric column; preserve fixed-three baseline/native fallback. Do not assume choice(v,@labels) expands dynamically without evidence. Full-screen, live stale-load coverage, production automatic install, education integration and native skill hover remain pending; Golden/MATCH unchanged0. No formal broad goal rewrite performed.

## 2026-10-27 bounded count extension experiment (not a production migration)
Ruling: continue the approved isolated feasibility spike with opt-in v2 for exactly 2 or 4 candidates. Preserve the measured v1 fixed3 contract and existing deployments. This tests whether list counts can vary without committing to the unapproved broad redesign. No original game/DAT/save or protected files; no Git operations. Existing diagnostic copy is the isolated workspace.
1. Extend request/snapshot/choice/session/literal/runtime under an explicit v2 profile. Storage max4; v1 remains exactly3. V2 count inferred only from validated exact candidate/reference lengths; values are existing numeric variable references, no evaluation or allocation. N candidates must match N+1 native labels, with Cancel at N. Reject duplicate IDs/refs, aliasing output/value cells, wrong counts, stale serial/lifetime and unknown profile.
2. Keep one signed numeric column, stable source-index mapping, consume-before-write/no retry, existing owner cleanup and required native fallback. No arbitrary command dispatch, new education parsing or binary analysis.
3. Add actual private-memory adapter tests for 2 and4 including ordinal3 valid for4, negative/tied sort values, malformed count and aliases; preserve all v1 regression tests. Capture RED then GREEN in existing patch evidence folder; build alone is not game acceptance.
4. Root creates copy-only DAT 2/4 literal choice branches, then independent source review and Windows regression before diagnostic deployment. Native 2/4 acceptance only after exact source/build/manifest hashes and zero existing Vahren processes. Otherwise leave candidate undeployed with precise resume state.
5. Record owner/status/test evidence in shared queue and fixed handoff; do not mark full generic API complete. Existing app goal text is stale; current selector/loader goal remains governing.
### 2026-10-27 bounded v2 candidate built, native gate pending
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / stop VA0041E7E3/0041E6D0. Progress this turn: isolated opt-in2/4 candidate implementation, tests/review, diagnostic fixture preparation. This is still feasibility work, not formal broad migration.
- v1 remains fixed3; v2 exact2/4 profiles akys/kmr[/tnok/rma], one signed numeric column; source ordinal3 is valid for4 and native Cancel=N. Separate bounded numeric lookups preserve alias rejection across values/output cells; owner cleanup and lifetime/consume-before-store guards retained.
- Independent agent review matched all9 reported source hashes with no code blocker. Actual adapter RED then GREEN O0/O2; 16 legacy suite runs passed. Root build_dat_ui_selector.ps1 -Test -OutputDirectory bounded_v2 PID29904 exit0, log bounded_v2/ROOT_GREEN.log. Standalone dispatch test was canceled by Windows before a test result; NOT PASS, no bypass.
- Candidate DLL SHA3a17cd64a07a8e1b2c19ed107776702aaf21762c353a211d1c32e09a3dd57ead copied/hash-matched to diagnostic plugins with manifest update. Default fixed3 artifact cdc4554c... remains unchanged. Prior diagnostic manifest: WORK_PRE_V2_MANIFEST_20261027.conf.
- Root source fixtures: tests/work_dat_ui_spike_v2.dat and work_dat_ui_spike_entry_v2.dat. One event sequentially requests2 then4, negative/tied values30,-5,-5,55. Native literal choice branches preserve fallback; no assumed list expansion.
- First startup reported entry_v2.dat line18 numeric newline syntax error before DLL arm. Working v1 has CRLF; new v2 had LF only. Normalized both source and diagnostic v2 files to CRLF and verified text equality after CP932 encoding. Source DAT SHAa86c9c2f97b3a145222055b83fd2a1414c44f68e90a6921ffd0419c7eaf9bbd3; source entry SHAbadd555c511ea59cec1628e7a4801b49acc02f7c45da0f96ba6834be6bd76355; deployed entry SHA0ba81323cf019f4d55ea0edf30a6b1a11fe43e76f424386bf115008f904fce5a. Corrected startup NOT yet accepted.
- GUI recovery: Explorer element activation reported geometry unavailable. A coordinate attempt opened readme_4 in Notepad (no editing); subsequent input calls repeatedly reported user input, then minimized window. No further UI input pending user availability question. No new Vahren process exists; do not infer an in-flight test or start duplicate game. No original files/saves modified, no deletion, no Git.
- Resume: user availability -> exact diagnostic Explorer launch once -> title/identity/log/manual arm -> DAT UI Spike v2 -> N2 sorted KMR(-5) return -> N4 sorted RMA(original ordinal3) return; inspect Result/Status/Before/After/Backend and native logs. Then cancellation and v1 regression as needed. Do not label native2/4 successful before observed.
- References: ../_work/claude_loader_patches_20261026/WORK_GENERIC_V2_IMPLEMENTATION_20261027.md; bounded_v2/{RED,GREEN,REGRESSION_FINAL,ROOT_GREEN}.log; core/dat_ui_selector_build_receipt_20261027.json bounded_v2_candidate. Full education integration, arbitrary IDs/instances/counts, full-screen, native skill-hover and production automatic arming remain unfinished.

## 2026-10-28 bounded generic5 and optional auto-arm implementation
Scope: incremental diagnostic spike requested by user; no broad production migration. Preserve v1/v2 controls and live PID9080/x32dbg session until a reviewed candidate is ready.
1. Profile3 recognizes exact hk_ui_select_g (14 chars), supports N1..5 unique candidate tokens, DAT display-label list and one signed numeric column. Validate count/list lengths, output/value/count cell aliases, raw native placeholder labels and final Cancel=N. Labels must be prepared before selection; no runtime DAT formula inference.
2. Root prepares CP932/CRLF K5 wrapper and fixture, initializing all label slots and output state each request. Two sequential requests test 5 then1 with changed labels. No49 claim, arbitrary native function invocation, native hover or education effects.
3. Reuse current table, use captured DAT display labels for profile3. Existing exact profile1/2 display remains unchanged. Test ordinal identity after sort/search; cancellation keeps native fallback.
4. Claude auto-arm patch reviewed separately, source SHA/mtime verified; default flagoff unchanged. Explicit build switch enables AUTO. Replace proposed stale-log deletion with unique test log paths, preserving user-requested recoverability and existing logs.
5. Agents have separate file ownership; root integrates after RED/GREEN and independent exact-source reviews. Default/AUTO Windows fixture runs occur after source freeze. Synthetic PASS does not establish game startup safety.
6. Native gate: user closes current diagnostic game normally; never double-launch or hotreplace loaded DLL. Verify AUTO title log order with xp.txt absent then present, preserving prior xp file. Reattach debugger for panel tests. K5 label expansion/return/fallback then singleton/repeat. Capture any C0000005 before continuing.
7. Failure keeps request PARTIAL; original EXE/DAT/save unchanged. Record actual commands/results/hashes, native confirmations and unverified items in queue/handoff/index. BGM and 10th lifetime gate remain unimplemented pending evidence.

### 2026-10-28 Claude v3 runtime integration checkpoint
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. §89 / README_APPLY §7 replaces §6 runtime steps1-3 and the preceding generic5 plan. No duplicate implementation: generic5 header edits restored; preliminary evidence retained, not deployed.
- Claude runtime/reader/grid/test sources copied with exact base checks and CRLF-preserving patches. Receipt: _work/claude_loader_patches_20261026/v3integration/applied_sources.json. Runtime integration header SHA a3ddea32e4c3cc35de9697cb7be2f99c721d629db432a2a76347fba946511627. Literal SHA ce0175edb30b9084f901d30040eba62239730871b02dfd3488168070f3b854e3.
- Package synthetic build_dat_ui_v3_test.ps1 on Windows: PID1892 exit0, O0 85/85 and O2 85/85. This tests delivered package headers; installed-header and runtime/regression suites still pending. Native ACTUAL remains0; Golden/MATCH0.
- Independent review found partial list insertion could corrupt displayed-row mapping, and failed predecessor v3_show could revoke a successor request. Assigned separate files/tests to agents for narrow RED/GREEN fixes; do not deploy until verified.
- Optional AUTO arm patch applied with exact expected SHA432f033a...; existing build default remains off. Native diagnostic logs now use CREATE_NEW unique names, preserving previous logs. Narrow tests recorded in auto_arm/WORK_AUTO_ARM_INTEGRATION_20261028.md; full default/AUTO suites pending.
- §87 lifetime audit is STATIC only; no new gate or BGM patch. Stop VA0041E7E3/0041E6D0, crash VA005DA9F8 still reproduction pending. Current game/debugger and deployed DLL/manifest unchanged.
- Next: freeze reviewed sources, run Windows v3 runtime default/AUTO and legacy suites, then diagnostic-copy label expansion/return/cancel/fullscreen/IME. V3 grid currently names/numeric columns only; chip/detail/hover reuse and education/item migration remain unfinished.

### 2026-10-29 Work v4 integration resumed
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Current scope: DAT-driven generic unit selector and common plugin loader. README_APPLY sections8/9, v4/DAT_UI_V4_SPEC and FINDINGS sections90-92 supersede the preceding generic5/v3-only checkpoint.
- Claude/human ACTUAL evidence reports v4 chips, native details, 17/234 candidate selection and one education flow; latest V5 fixes remain synthetic-only until Work verification. Do not count the 12 education types as completed. Golden/MATCH remain0.
- Windows Work regression: lifetime O0/O2 PASS; v3 runtime default 55/55 twice; AUTO 55/55 twice; successor 12/12 twice. All four build processes exit0. Evidence: _work/claude_loader_patches_20261026/v4/WORK_RUNTIME_REGRESSION.json and WORK_*.stdout.log. These are synthetic tests, not game execution.
- After interruption, agent states were checked: two interrupted and one pending. Build owner and readonly review owner explicitly resumed. Root owns records and diagnostic-copy preparation; auto_arm_integration owns build/fixture files; generic5_adapter owns readonly v4/location/custom-column review; generic_wrapper_review owns readonly DirectInput design. No concurrent grid edits authorized.
- Build pending: v4 O0/O2/AUTO, edge, updated87-check v3 component fixture, full default/AUTO selector suites and formal Zig0.14.1 DLL SHA. Preserve diagnostic test logs using unique CREATE_NEW paths; expected values unchanged.
- Remaining: education12 teacher/student/cancel/execution on full diagnostic copy; location display-name resolver; explicit DAT numeric columns; DirectInput overlap/fullscreen/IME; old diagnostic additions cleanup. Native right-click result remains unverified. Crash VA005DA9F8 remains reproduction pending; no speculative BGM patch.
- Location review: existing adapter returns spot tag, old human-readable names came from DAT dictionary/SPN1. Direct inclusion is insufficient. Manifest documentation correction needed: enabled is field3, immediately after DLL name, not field4.
- Original EXE/DAT/MAP/saves/ZIP remain readonly. No Git mutation or game deployment this checkpoint. Stop VAs0041E7E3/0041E6D0 are evidence references, not permission to expand analysis.
### 2026-10-29 DirectInput capture design review (Work; NOT IMPLEMENTED)
- Scope: readonly review of current proxy/Core APIs, FINDINGS sections91-93 and saved T015 evidence; no new EXE analysis, game operation, deployment or input hook. Root requested this record. Prior plan SHA256 4833C7F831D47BEB07B2C602B4174B65B4D7CE934269F0A52F81E62933471440, UTC mtime 2026-10-28T16:14:18.7681304Z rechecked before append.
- Current core/dinput8_proxy.c (SHA C7A6A16C25D943242CDF447CA3814BB14E6A0B285CDD5DD819C5653E415ECF34) forwards DirectInput8Create to the system DLL unchanged. Core extensions1-4 provide reservations/events/CALL_PATCH/PTR_PATCH, not an input capture API. Existing PTR_PATCH ownership does not itself solve COM object/interface lifetime.
- Saved exe/T015_INPUT_POLL_DISASM.txt: mouse call 0x4BCFBB and keyboard call 0x4BD0D5 use vtable+0x28 (GetDeviceData), cbObjectData=0x14, flags=0, maximum255/64 events respectively. GetDeviceState is not shown in this saved polling path. Do not claim runtime tracing of these exact calls from this review.
- Critical saved behavior: 0x4BCFC6..0x4BCFD6 processes mouse events even on a negative HRESULT if returned count is nonzero. 0x4BD0DB..0x4BD0E7 does the same for keyboard. Capture must never pass uninitialized/stale event data on failure; preserve the actual failure HRESULT, do not pretend reacquisition succeeded.
- Held state is persistent: mouse press/release at 0x4BD037..0x4BD0A5 updates bytes +0x24/+0x26/+0x28; poll clears edge bytes but does not clear all held bytes. Returning zero events alone can leave an already-delivered button held. Track what the game received, neutralize its pending held state through a verified release/reset contract, and quarantine overlay closing clicks until physical release and neutral state are established.
- Focus flush hazard: saved exe/T015_FOCUS_FLUSH_PROBE.txt 0x4BD170..0x4BD1B2 calls mouse then keyboard GetDeviceData with NULL output, flags0, the same in/out count local; 0x2710 is set only before the mouse call. Changing the mouse flush result to count0 also changes the keyboard request to0. Preserve this native NULL-output call's behavior; separate capture-internal draining from it. Focus loss does not guarantee a complete keyboard flush.
- Recommended new Core service: instance/request-generation/owner-HWND-bound exclusive capture token. A stale request cannot release its successor. Proxy owns the mouse device broker; callbacks perform no DAT/native UI calls and do not hold Core locks across COM calls or SendMessage. UI request transitions own creation failure, cancellation, destruction, replacement and plugin-stop cleanup. Do not simply expire a token and expose a still-visible overlay's clicks to the game.
- Restrict interception to identified SysMouse devices and verified data formats; keyboard/other devices remain unchanged. Avoid globally rewriting a shared COM vtable. QueryInterface aliases, AddRef/Release, recreation, active callbacks and cloned-vtable lifetime require tests. Unsupported formats/interfaces mean refuse capture and fall back to native selection, not silently claim safe capture.
- GetDeviceState support, if needed, must preserve failures and neutralize only successful output of an established format/size. GetDeviceData needs distinct handling for normal reads, DIGDD_PEEK, NULL output, zero count and DI_BUFFEROVERFLOW. Do not leave suppressed events queued for replay after closing, or silently turn PEEK into consuming reads. Drain and rearm transitions must be serialized with device reads.
- Detail mode1 (read-only preview/hover): suppress native clicks and wheel while the table is active; provide hover coordinates through the separately verified read-only detail route. Do not whitelist the entire detail rectangle: FINDINGS93 confirms that own-faction panels can contain hire/dismiss buttons and are rebuilt repeatedly. Hover during events is an extension, not original behavior to reproduce.
- Detail mode2 (interactive buttons): separate explicit capability/permission and lifecycle design is required before implementation. The existing broad PC-operation authorization does not turn a generic preview into an automatic hire/dismiss action. Any permitted native action can change candidate identity/lifetime and must invalidate/rebuild the selection request. No mode2 behavior is implemented or approved by this review.
- Fullscreen: beside-window placement from section91 is only a workaround where space exists. DirectInput capture cannot guarantee native Win32 table visibility in exclusive D3D fullscreen. Validate windowed/fullscreen, DPI, focus loss, minimize/restore and cursor routing independently; do not change cooperative level or acquire/unacquire policy as an unverified shortcut.
- Minimum fixtures before game deployment: disabled-capture exact forwarding; mouse versus keyboard/device isolation; held-before-open and held-after-close; right-click/double-click/wheel; NULL/PEEK/count0/overflow/failure; request successor and UI-creation failure; device recreation and COM lifetime; no hire/dismiss/backing-choice click-through. Then diagnostic-copy focus/fullscreen and hover-only checks. A mouse-only fix must not be represented as keyboard/IME isolation.
- Evidence distinction: section91.3 ACTUAL reports click-through despite disabled/inactive owner; T015 offsets above are saved static evidence. Implementation, synthetic tests and new Windows/game acceptance for this design are all NOT RUN. Largest risks: stale held state, close-click replay, buffered queue leakage and COM lifetime. No source change follows from this record.

### 2026-10-30 入力分離の実装計画
目的：一覧の操作が背後へ届く問題を解消する。UI判断として、一覧中はマウスボタンとホイールを隔離し、説明表示用の移動は維持する。
構成：デバイスごとの純粋な状態処理、DirectInputの型付き転送、Coreの所有権API、一覧の寿命への接続の順に実装する。現在の横置きだけでは完成扱いにしない。
- [x] core/hakushin_mouse_gate.c/.h と test_mouse_gate.c：通常・準備・遮断・解放待ち・次要求待ちを試験。押下済み・取消・連続要求・失敗・欠落・参照読取・NULL消去を扱う。WindowsのO0/O2各135/135成功（テストのみ）。
- [ ] dinput8_proxy.c：確認できたマウスと形式に限定して転送層へ接続。COM別名・参照寿命・再生成を試験し、未対応時は一覧を出さない。
- [ ] Core拡張とdat_ui_v3_runtime.h：世代トークンで開始／準備完了／終了を接続。一覧表示直前に候補と寿命を再検証し、遅延取消が後続要求へ届かないようにする。
- [ ] 合成検証後に診断コピーへ配置。背後の選択・雇用・解雇の無作用と説明表示、取消、連続表示、失焦をまとめて確認。全画面・日本語入力も別途確認する。
読取はデバイスロック下で開始から結果反映まで直列化する。実イベントの空読取と物理解放が揃うまで準備・解放を完了しない。失敗や時間経過を解放の代用にしない。
初期化は原作の押下状態が不明として開始する。hkmg_native_baselineには原作入力consumerの押下状態を実際に読んだ値だけを渡す。新規デバイスや物理マウスの解放は原作内部状態の証拠にしない。不明なら一覧を出さず原作へ戻す。
取消後はOSのダブルクリック間隔も隔離する。時間だけで解除せず、物理解放・空の消費読取を必須にする。消費したボタン／ホイール、内容不明のNULL消去、欠落・読取失敗で静穏期間を開始し直す。後続要求も隔離を引き継ぐ。
通常時は元の戻り値・イベント・NULL消去件数を保持する。遮断時も戻り値は保持し、失敗バッファはゲームへ渡さない。参照読取は消費・準備完了の証拠に使わない。
API仕様根拠：https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee417894(v=vs.85) 。保存済み原作経路は上節T015を参照。

### 2026-10-30 実装区切り（テストのみ）
- 入力分離の状態処理・単体試験・専用ビルド手順を追加。proxy/Core/一覧には未接続で、ゲームへの配置なし。
- レビューで新規デバイスの中立誤認、取消ダブルクリック、内容不明の消去／欠落の3点を修正。失敗を再現してから修正した。
- Windows x86で最適化なし・あり各135/135成功。証拠：_work/mouse_input_gate_20261030/final、失敗再現は同フォルダ配下review_red・double_click_behavior_red・flush_red。
- エージェントの入力設計・実装レビュー結果は回収し本節へ反映。現行ゲームと既存DLLは変更していない。
- 次：型付きDirectInput転送、consumer押下状態の読取証拠、Core所有権と一覧寿命への接続。通常処理・失焦・連続表示を試験してから診断コピーへ配置する。
- API references: https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee417894(v=vs.85) (GetDeviceData flags/count/overflow); https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee417897(v=vs.85) (GetDeviceState format and HRESULT).

### 2026-10-30 型付き入力転送の区切り
- したこと：型付き入力転送を追加し、独立レビューの結果を回収。古い要求の再利用・物理押下の見落とし・即時状態との混同を修正。
- テストのみ：転送O0/O2各108/108、状態処理O0/O2各135/135成功。証拠は_work/mouse_input_gate_20261030/transport_final・gate_final。
- 推定：既存逆アセンブル資料では原作の保持ボタンは3個。物理入力の解除確認は全ボタンで行う設計とした。
- 次：デバイスの参照・別名・破棄の管理と非破壊の物理入力確認を接続。その後に共通基盤・一覧へ組み込む。ゲーム未配置・実機未確認。

### 2026-10-30 デバイス管理・専用読取の区切り
- したこと：Device8 A/Wの共通寿命・転送・設定拒否を実装。独立エージェントの専用マウス読取とレビューを回収し、別名経由・複数デバイス・解放後の試験を追加。
- テストのみ：Windows最適化なし／あり各58/58、専用読取各607/607、転送回帰各108/108成功。証拠は_work/mouse_input_gate_20261030のdevice_final・probe_final・transport_after_device。
- 設計判断：未対応の旧インターフェースを素通しせず拒否。元デバイスの相対移動を消費しないよう別の非排他デバイスから全8ボタンを読み、失敗時に再取得・再利用しない。実機での非干渉は未確認。
- 次：起動時の生成経路全体とCoreの参照保持、一覧の開閉へ接続する。ゲーム未配置、クリック重なりの改善は実機未確認。

### 2026-10-30 生成経路と原作押下状態の区切り
- したこと：入力生成側の共通管理と原作マウス状態の読取部品を追加。独立レビューで見つかったコールバック中の最終参照解放を修正し、試験を追加。
- テストのみ：Windows最適化なし／ありで生成側各111/111、原作状態読取各134/134成功。証拠は_work/mouse_input_gate_20261030のfactory_final・baseline。
- 設計判断：ConfigureDevicesの通知は描画面なのでそのまま転送。設定変更中の捕捉を拒否し、終了時にデバイスの再確認を管理側へ要求する契約とした。
- 次：同じデバイスの別名をまとめる管理、Coreの参照保持、信頼できるUI読取境界へ接続。原作が保持するポインタはラッパー導入後に変わるため、実デバイスとの対応を別途照合する。ゲーム未配置・実機未確認。

### 2026-10-30 共通管理の結合試験
- したこと：結合時の異常終了を再現し、生成側とデバイス側の同名内部テンプレートの衝突を無名名前空間で解消した。通知中の最終参照解放の試験も追加。
- テストのみ：Windows最適化なし／ありで結合各147/147、デバイス各75/75、生成側各111/111、終了0。証拠は_work/mouse_input_gate_20261030/{broker_combined,mouse_device_after_broker,input_factory_after_broker}。
- 独立レビュー2件を回収。参照寿命に追加指摘なし。UIメッセージ取得地点だけでは原作入力更新の完了順序を確定できない。
- 次：入力更新境界を確定して起動経路・共通基盤・一覧に接続する。ゲーム未配置、入力重なり改善は実機未確認。

### 2026-10-30 起動ローダー入力接続
- したこと：登録前は捕捉を拒否する入力管理サービスを実装し、明示ビルド指定時だけ起動ローダーへ接続。提供側の寿命はプロセス終了まで保持する設計とした。
- テストのみ：Windows O0/O2各38/38。未実装と失敗時参照漏れの失敗を先に確認し修正。通常版・入力管理版の標準入力DLL転送も終了0、証拠_work/mouse_input_gate_20261030/{proxy_input_review_red,proxy_input_review_green,proxy_candidate}。
- 独立成果を回収：入力更新完了境界の部品はO0/O2各153/153。保存資料の0x4B9AB1→NewGameMouseの表+4を根拠とするが、ゲーム接続は未実施。
- 次：Core提供側・一覧開閉へ接続し、別DLLの提供側寿命とA/W経路の追加試験を行う。候補DLLは作業領域のみ、ゲーム未配置・実機未確認。

### 2026-10-30 一覧入力結合と起動比較
- したこと：入力更新完了境界・一覧開閉を接続し、期限切れ再確認と終了再試行を修正。独立レビューは回収済み、待機時転送に具体的な欠陥なし。
- テストのみ：提供側寿命32/32、一覧制御343/343、結合160/160をWindows O0/O2で確認。自動準備版の既存回帰も終了0。証拠は_work/mouse_input_gate_20261030。
- 実機確認：候補はタイトルへ到達しinput_provider_readyまで記録。候補と変更前の双方で同じ自動クリックがEasyに反映されず、一覧の入力捕捉確認には到達していない。専用読取の非干渉は未確認。
- 配置：比較後にゲームを通常終了し、バックアップ・前後ハッシュを照合して候補へ戻した。deployment.jsonとcomparison_before_*/receipt.jsonに保存。原作フォルダは未変更。
- 次：手作業で一覧を開ける時に、押下漏れ・確定・取消・入力復帰を一括確認。自動クリック不成立を入力対策の不具合とも成功とも断定しない。
