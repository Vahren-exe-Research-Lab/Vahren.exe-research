# P0 NOOP worker・合成試験
研究ID: P0_TAKEOVER_20261024_01 / K-L補助実験 / 2026-10-24。
分類: THROWAWAY SPIKE / SYNTHETIC HOST TESTED / NOT NATIVE G3 PASS。
EXE source SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 SHA（親verify）: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
元命令の接続候補: Start 00492890正常復帰→Task 004C2935。workerは元PE/プロセス/メモリ/VM/Unitへアクセスしない。
親のrun_observer.py/observe.jsは一切変更していない。

## 起動・wire
P0NoopWorker.exeは.NET Framework 4 x86。通常は引数なしで先行起動する。
UTF-8 stdin/stdout/stderr、JSON Lines。1プロセスは1requestで終了する。
stdinを渡す前にstderrの {"type":"worker_ready","protocol":"P0_NOOP_V1","source_sha256":"..."} を受領する。
readyはrequest受理ではなく、起動処理後の入力待ち状態。親の500ms game waitにworker cold startを含めない。
request必須: protocol、source_sha256、req_id、battle_id、start_digest、event_name、payload。
protocolはP0_NOOP_V1、source_sha256は上記大文字固定SHAと完全一致。
req_idは非zero UUID D形式。battle_idはASCII [A-Za-z0-9_.:-]{1,128}。
start_digestは64桁hex。payloadはJSON object。入力は最大1MiB、JSON nesting最大32。
event_nameは Local\P0Battle.<非zero UUID D形式>.<1..999999999> のみ。Global、任意名、seq0、suffix等は拒否。
stdout ACKはtype=noop_ack、status=echo_only、native_result_applied=falseに全必須識別子とpayloadをechoする。
stdout ACKをflushしてからOpenEvent(EVENT_MODIFY_STATE,false,event_name)→SetEvent→CloseHandle。
signal結果はstderr type=signal_result、signaled、Win32 error、outcome=event_signaled_onlyまたはunknown。
exit0=SetEvent成功、20=request拒否、22=OpenEvent/SetEvent失敗。ACKは通知成功・native再開・結果commitの証明ではない。
source SHAの照合は宣言値の検証であり、原作現物のattestationではない。親が現物SHAとsnapshotを結び付ける。

## hostの受理規約
hostは元snapshotからexpected envelopeを確定し、protocol/source/req/battle/digest/event/payloadの一致を確認する。
ACK受理は同req_idについて一回だけ。duplicateは無害化し、前battleのACK、識別子不一致、期限後のACKは採用しない。
eventはrequestごとに新規名でCreateEventし、ERROR_ALREADY_EXISTSなら古いsignaled状態の可能性を拒否する。名前を再利用しない。
SetEventはwakeupにすぎない。wrong battle ACKでもeventがsignaledになり得ることを合成試験で確認した。
timeout、worker早期終了、ACK後signal前終了、signal成否不明はoutcome_unknown。勝敗、生存、native resultを補完しない。
今回native resultは常に適用ゼロ。idempotencyは合成host Receiverの受理モデルで検査した。実native hostへの組込み完了を主張しない。
worker内には永続dedupe DBはなく、複数workerを同req/eventで起動しない責任はhostが持つ。
親のgame waitは最大500ms、元4C2935 continuationを一回進める。timeoutでもVM PC/active/finishを書き換えない。
親のnative callback中にstdout/stderr同期読み待ち、UI message pumping、worker起動待ちを追加しない。

## synthetic negative modes
--synthetic-mode timeout|crash|delayed|duplicate|wrong_battle|after_ack_crash。
negative modeはpayload.synthetic_only=true必須。原作probeでは引数なしのnormalのみ使用する。
crashはACK前exit91、after_ack_crashはACK後signal前exit93による早期終了模擬。OS例外/SEH crashの再現ではない。
timeoutは800ms遅延後ACK/signalなしでexit92。delayedは750ms遅延後ACK/signal。duplicateはACK2行、signal1回。
wrong_battleはACKだけbattle_idを変更しsignalする。この負例によりeventだけで結果を受理してはいけないことを検査する。

## 合成検証結果
test_noop_synthetic.py: 15試験PASS、原作プロセスアクセス0。詳細はSYNTHETIC_TEST_RESULTS.json。
正常、重複ACK一回受理、wrong battle拒否、crash/timeout/delayed/ACK後crash、protocol/source/digest/event名3種の拒否、stale ACK、既存signaled event名の拒否。
正常試料はreadyまで782ms、依頼からeventまで250ms。duplicate試料はready907ms、依頼からevent218ms。これは計測例であり性能保証ではない。
初回readyなし試験は500msでTIMEOUT、後からACK+SetEvent成功を観測。late ACKを拒否した。起動と処理を分離したready handshakeで再試験PASS。
late delayed試験は100ms timeout後に実際にeventがsignaledになったが受理0。ACK後終了もACKが存在するだけで成功へ昇格させなかった。
成果JSONはPython UTF-8読戻し同値確認済み。PowerShellの既定ANSI読取では日本語payloadが誤読されるため、Get-Contentは-Encoding UTF8を明示する。
再開地点: 親がworker_readyを待ち、専有native copyのC1 gate tokenをrequestへ対応付け、bounded NOOPの元continuationを観測。合成15PASSをG3/G2/戦略Goldenへ加算しない。

