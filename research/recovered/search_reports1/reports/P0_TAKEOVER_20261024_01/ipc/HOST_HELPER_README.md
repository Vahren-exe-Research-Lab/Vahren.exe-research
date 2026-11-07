# P0 NOOP host helper
研究ID P0_TAKEOVER_20261024_01。合成host補助のみ。親のnative observerを変更しない。
p0_noop_host.py: importable P0NoopHost。1 instance = 1 worker = 1 request。
使い方（必ずprewarmをnative gate外で呼ぶ）:
```python
from p0_noop_host import P0NoopHost
host = P0NoopHost(worker_path, callback, startup_timeout=5.0, response_timeout=0.5)
assert host.prewarm()["status"] == "ready"
# native message handler内。pipe I/O、response待機はbackground thread。
accepted = host.submit(request)
# teardown時。自身Popen childのみ終了。PID検索や原作アクセスなし。
host.close()
```
submitはrequestをdeepcopyしてthreadを起動するだけ。2回目/未ready/closedはFalse、追加callbackなし。
callback(result)は背景threadから終端一回。callback自身の例外はcallback_errorに保持する。
status: noop_ack_signaled / mismatch / request_rejected / outcome_unknown。
noop_ack_signaledは一致ACKとSetEvent成功ログの受領。全結果native_resume_verified=False/native_result_applied=False。
親はJSのWait結果・pre/post snapshot・正確continuationと別に照合する。helperだけではnative成功にならない。
response_timeoutはhelper側submit処理からの期限。native側500msの開始点とは厳密同期していないため、helper成功でもnative timeoutはあり得る。
req/battle/digest/event/source/protocol/payloadを一致照合。payloadはcanonical JSON比較でboolとintegerを区別。
同一reqのACK重複はcallback/receiptを増やさない。全stdout/stderrはEOFまで期限付きで読取り、mismatchを検出する。
timeout、終了途中、pipe例外、host closeはoutcome_unknown。期限切れchildは自身Popen参照でのみ終了。
wait_resultは合成試験/管理用。native message handlerやgame gateから呼ばない。
test_host_helper.py: 既存worker実行の8試験PASS。正常、duplicate、wrongbattle、ACK後終了、遅延、source拒否、起動期限切れ、pending close。
成果: HOST_HELPER_TEST_RESULTS.json、HOST_HELPER_INTEGRITY.json。合成PASSをG2/G3やnative NOOP往復のPASSへ加算しない。
