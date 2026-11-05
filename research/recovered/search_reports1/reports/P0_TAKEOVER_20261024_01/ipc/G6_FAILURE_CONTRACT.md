# G6失敗契約・negative native試験の独立レビュー
研究ID: P0_TAKEOVER_20261024_01。2026-10-24。read-only source review + 設計。
元EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
合成worker15件とhelper8件の保存結果を再利用。再実行0、原作操作0、worker/helper/controller/JS変更0。
機械可読正本: G6_FAILURE_CONTRACT.json。全source SHA、phase別fallback、failure matrix、commonDLL向けabort enumを収録。
親報告のnative C1観測（pass1349,index0,count405,unitSinceStart0、後続Unit/次pass tick）は前提資料。今回のG6失敗試験成功とは扱わない。

## 既存workerの正確な起動条件
| 目的 | argv | ready | request後の動作 |
|---|---|---|---|
| ACK前終了 | --synthetic-mode crash | 出る | 正常検証後exit91。ACK/SetEventなし |
| ACK後終了 | --synthetic-mode after_ack_crash | 出る | ACK flush後、OpenEvent前exit93 |
| 遅延 | --synthetic-mode delayed | 出る | 750ms待機後ACK/SetEvent |
| 応答なし | --synthetic-mode timeout | 出る | 800ms待機後exit92。ACK/SetEventなし |
--modeは無効。全negative modeはpayload.synthetic_only=trueを要求する。欠落時はrequest_rejected/exit20で、crash試験にならない。
crashはworker早期終了の模擬であり、アクセス違反・SEH例外・OSクラッシュではない。
readyはmode引数検証直後、request読込前に出る。したがってnegative modeでもprewarmは成立する。
helperは500ms応答期限で自身のchildをkillできるため、delayed/timeoutの自然exit0/92を前提にしない。
現run_noop.pyはworker_argsを指定せず、payloadはsnapshot_jsonだけ。無変更の現scriptではnegative選択不可。
native負例を親が別controllerで準備する場合は、故障注入が合成であることとsnapshotが原作実測であることを別フィールドで記録する。

## fallbackの意味とphase
| phase | 原作結果commit | 許容される処置 |
|---|---|---|
| prewarm失敗 | 未開始 | attach/armしない。原作を独立して継続 |
| Start実行中 | 未開始 | 原作初期化の自然returnを待つ。途中処理を飛ばさない |
| C1待機前 | 未開始 | 同contextでobserverから元4C2935へ一回戻る |
| Wait実行中 | 未開始 | signalまたは500ms timeoutの自然return。workerのみ独立終了可 |
| ACK後・signal前 | 未開始 | ACKだけで成功扱いせず、native wait結果を待つ |
| Wait return後 | 未開始 | 同thread/同contextで一回continuation。状態一致と後続実行を確認 |
| native結果commit開始後（将来） | 開始/部分適用 | 原作戦闘へ自動fallbackやfinish再実行をしない |
| commit完了（将来） | 適用済 | 一致するcommit証拠を確認してVMを一回再開 |
| commit有無不明（将来） | 不明 | 結果を補完せず照合・復旧が必要 |
現在のNOOPはnative result適用0。ACK・SetEventはcommitではない。入力snapshotの一致も結果反映の証明ではない。
将来のfinishは複数副作用を持つため、commit開始後に通信が切れた場合「ACKなし＝未適用」と推定できない。
partial commit/unknownのrollbackと再試行は未実装。今回のbounded fallback候補と別のG6課題として残る。

## 失敗時の分類
worker startup失敗はNOT_SUBMITTED。native待機に入っていなければtimeout-resumeの成功にはならない。
worker ACK前/ACK後終了、期限切れ、signal失敗、controller切断はIPC OUTCOME_UNKNOWN。nativeの状態は別途観測する。
wrong battle/digest/payload等はMISMATCH、receipt受理0。eventが既にsignaledでも結果を受理しない。
重複ACKは一回receiptとし、追加resumeをしない。期限後・前battleのACKは破棄しevent名を再利用しない。
WAIT_TIMEOUT=258は終了理由として記録し、後続の原作継続を別証拠で確認する。WAIT_FAILED=0xFFFFFFFFは失敗であり、GetLastErrorを必要とする。[Microsoft仕様](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
helper成功はnative_resume_verified=Falseのまま。helper側期限開始とnative側Wait開始は厳密同期していない。

## 現controllerの限定事項
observe_noop.js cleanup()はholdEventを閉じる。Wait中にSTOP/unload/cleanupを実行しないこと。待機中handleを閉じた際の動作は未定義である。[Microsoft仕様](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
CreateEventW直後のERROR_ALREADY_EXISTS確認は現在JSにない。runごとのUUIDで衝突可能性を下げているが、古いsignaled eventを実際に拒否した証明ではない。既存objectの場合、初期状態指定は無視される。[Microsoft仕様](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createeventw)
現在JSはWAIT_FAILEDのGetLastErrorを記録しない。失敗値が出た場合、正常timeoutと一緒に集計しない。
unitWatchは最初のUnit更新でdetachする。unitSinceStartは最初の更新検出であり、全後続更新の完全なカウンターではない。
FS0はinstrumentation callback内の値、元SEH/flagsは未証明。sampled digest一致は全engine状態・全thread writerの不存在証明ではない。
500msはAPIに渡すtimeoutであり、スケジューリング等を含む厳密な実時間上限とは扱わない。

## 次のnative worker早期終了試験の合格条件
親専任で、正常NOOP往復を先に確認した後の別試験とする。故障mode/marker/source分類をログに固定する。
prewarm ready→同thread/同battleのeligible C1→worker exit91（ACK/SetEventなし）→native wait_result258→元continuation、を一連で確認する。
exit20 request拒否、hostによる強制kill、WAIT_FAILEDはworker exit91の代用にしない。
待機前後sampled state/roster/Task counter digestが一致し、待機中の観測Unit/tick進行がないことを確認する。
元の次slot/最初Unitと次pass tickを確認し、Start/finish/VM PCを再実行・巻戻ししていないことを記録する。
終了処置はwait return後。合格分類はLIMITED_WORKER_EARLY_EXIT_TIMEOUT_NATIVE_CONTINUATIONのみ。full G6・クラッシュ復旧・部分commit回復へ昇格しない。

## commonDLLへ渡す設計API
JSONのapi_design.abort_reason_enumに31値を保持。実装済みABI/APIではなく設計契約。
phase、abort_reason、commit_state、ipc_status、native_wait_result/native_last_error、resume_observed、continuation_countを独立に記録する。
識別子はrun/session/seq/req/battle/digest/source/thread/gateを結ぶ。abort通知自体はPC/active/finishを書き換えない。
再開地点: 親がnegative専用controllerの条件とcleanup phaseを定め、ユーザー協力の一戦を実施。子は原作試験を行わない。

