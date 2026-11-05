# controlled worker exit91 復帰試験: 独立read-onlyレビュー
研究ID P0_TAKEOVER_20261024_01 / 2026-10-24 / exit_hij。
判定: 指定の複製ゲーム・最初の通常戦闘・共有記録書換なし・worker ACK前制御終了に限定し、実行を止めるblocking issueなし。未実行コードレビューであり復帰PASSではない。
EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（親verify継承、今回DB問合せなし）。
読み取ったファイルはruntime/observe_recovery.js、runtime/run_recovery.py、ipc/p0_noop_host.py、ipc/P0NoopWorker.cs、ipc/IPC_INTEGRITY.json。コード変更・実行・attach・プロセス操作なし。

## 審査対象の現物SHA256
- observe_recovery.js: 002E9EC75F57775FDC9CC0098F749A8D20204AF96E826EDCBB8A19C465A178C1
- run_recovery.py: 94D98434BD1283317A976F95F8DA31528612CE06F6D42DC283D1E288A6A6FE7C
- p0_noop_host.py: 89A515E1EA979147B4811BE86122BF22243B7A5EF004675A97E47192C9B5C0AA
- P0NoopWorker.cs: B7279FF4DDCCC9CDD095E10B44A818F80DB280E6E1B0F4F0C4F63FE304727330
- P0NoopWorker.exe: 31FDD845E8EF121C6A8A91BABF6C71B16998029B5129DEFE806E67E29A778C2C
worker source/exeはIPC_INTEGRITYの既存保存hashと一致。現在のsourceを独立再buildしたという意味ではない。run時injected.jsのhashも別途記録する。

## コード経路で確認した点
1. run_recoveryはgame_copy EXE hash/pathとia32、対象hookのPE bytes（relocation mask付き）を検査する。--attachはQueryFullProcessImageNameWでcopy以外を拒否する。元ゲームを選択する経路はない。
2. workerをgate前にprewarmし、worker_args=['--synthetic-mode','crash']を渡す。request payloadにsynthetic_only:trueが入り、worker側はこのboolを検証する。
3. workerのcrashモードはrequest検証後、synthetic_crash/phase=before_ackをstderrに出しreturn91。ACK構築、OpenEvent、SetEventより前である。OS障害・アクセス違反・game crashを起こす試験ではない。
4. named eventはunique UUID、auto-reset、initial nonsignaled。CreateEvent failure/ERROR_ALREADY_EXISTSを拒否する。worker制御終了ではeventをsignalするコードへ到達しない。
5. handoff_requestはstart digest照合後P0NoopHost.submitへ。submitはdaemon writer/readerへ処理を分け、game threadでpipe待機を行わない。host receipt期限0.5秒はgameのWaitForSingleObject(500)と独立。
6. gateは同ゲームthread、最初のbattle、元task owner/E、同pass、Unit初回更新前、GameEvent/Scene深度とvmCallerを照合する。holdDoneで再実行を防ぐ。候補siteは004C2935。
7. waitInProgressをNativeFunction waitの前でtrue、finallyでfalse。cleanup RPCはpendingならeventを閉じずwait_pendingを返し、controllerは待ってからunloadする。待機中CloseHandleを避ける意図に整合。
8. WaitForSingleObject戻り値によらず元hookへreturnして通常dispatcher巡回へ復帰する。native finish呼出、E/Unit/Power/Spot書込、PC/return偽装なし。
9. timeout後にbefore/after sample、tick/Unit count、elapsed、game contextを記録する。eventを閉じる。自然493630入口/出口、4335E0のworld stateを後続観測する。
10. hostはworkerのEOF/ACK欠如をoutcome_unknownとして記録し、native_resume_verified=false/native_result_applied=falseを維持する。host側完了を原作復帰成功へ変換しない。

## 実測の受入条件
- run identity/exe/source hashes一致、observer_ready、eligible gate一回、handoff_request一回、submit accepted=true。
- workerログsynthetic_crash phase=before_ack、ACK count0、accepted_receipts0、signalなし。exit_code_at_receipt=91が得られれば制御終了codeも実測確認となる。
- hostはEOFとprocess pollの時間差によりexit_code_at_receipt=nullになり得る。この場合「91実測」と書かず、sourceのreturn91経路とbefore_ackログに限定する。OS crash実証にはいずれもならない。
- handoff_resume wait_result=258(0x102 WAIT_TIMEOUT)、wait_last_error0、native_result_applied=false。wait0やWAIT_FAILEDはこの故障注入ケースの合格ではない。
- pre_digest==post_digest、sampled_state_equal=true、ticksBefore==ticksAfter、unitsBefore==unitsAfter。これは採取sampleのみの不変であり、全heap/thread/乱数/VM全体のatomic凍結ではない。
- elapsed_msを保存し500ms近傍であることを確認する。OS schedulingで上振れ得る。gate_elapsed_to_postcapture_msにはsnapshot/IPC emit等の前後費用が入り、gate全体のhard500ms保証とはしない。
- 解除後にUnit初回更新→通常battle_tick→自然finish一回→mode1/active0/world_return_taskを同seq/threadで確認する。待機復帰のみでは自然戦闘完了を証明しない。
- Frida error/controller_error、異常detach、read unavailable、sample欠落の場合は該当証拠をUNKNOWN/INCOMPLETEにし、暗黙PASSしない。

## 範囲上の限界（今回の実行blocking issueではない）
- before/after makeState、emit、CloseHandleには全体finallyがなく、読取等で例外が出るとhandoff_resumeやevent cleanup記録を欠く可能性がある。例外時にゲーム状態を書き戻す経路はなく、この試験の成功証拠としては不合格にする。
- cleanup guardは現在のwait pendingを守る。STOP/unloadは試験のresumeと後続観測を受け取ってから行う運用とし、準備途中の強制中断まで一般保証したとは扱わない。
- workerの停止だけを試す。host/controller障害、ACK後crash、遅延signal、永久停止、結果apply中障害、native finish例外からのrollbackを含まない。
- IPC外部echo成功run20261024T005426_10cf1dfbの親通知を背景とするが、このレビューはそのraw独立再監査ではない。今回のrecovery rawと混合してPASSにしない。
- G4 settlement未成立は前文書のまま。bounded timeout→通常continueで原作が自然決着することと、外部戦闘結果を書き戻すことは別の実験。
再開地点: 親が作るrecovery runのinjected.js/identity/eventsを本hashと照合し、上記受入条件を同battleで集計する。コード修正が入った場合は現物hashを再確認する。
