# N 独立NOOP native receipt監査
研究ID P0_TAKEOVER_20261024_01 / run 20261024T005426_10cf1dfb / PID39496 / seq1。
EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 DB SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
判定: G3_NOOP往復の限定実測成功。独立30条件すべて一致。完全G1/G2/G4/G5/G6の達成ではない。元ログ変更なし・N担当の実機操作なし。
固定prefix27event SHA4FEE362C97CAB46780CF5C695A9F375BD0ED4DB3DCDDA8308081C904EE634FB2。
終了後full29event SHA A0DACD6B9D3D9FBD832A1E40811E76A18D7C2BC74736978FF2074EBEE0F613E6。2回読取一致後にreviewへコピー。
実行source bytes SHA69489CA15B7EEE9347C46E291A0655CD639DF349AA9F3099F1889CC8E71118E1はattach receiptのsource_sha256と一致。今回改行変換の補正不要。

## 照合結果
- 行7–9: Start→C1、tid38988/pass14616、VM return preferred433620、C1 preferred4C2935/index0/count244、owner/EBX=E一致、Unit未更新・GameEvent外。eligibleは1回だけ。
- 行10–13: request→submit→worker receipt→native resume。request/submit/receipt/resume各1件、seq1、固有UUID event、同battle/request/digest、ACK1/duplicate0/signal1。要求JSONとecho JSONは文字列として完全一致。
- packet 206 Unit（84/122/0）はStartLeave名簿のHP/MP/max/XY/tokenと全件一致。全項目available、token重複なし。generationはunverifiedのまま。
- 開始snapshot digest A450D9AFF731862E6E87EBB585C9E2AC2B831AF3CDE25BF6BE8897A75A6EC24Eを独立再計算。pre state+task_counter+rosterからBF4BC51C9E7B12177FA300699B7F33B539221F3DED2D795A4AD69E8869B30D61も独立再構成一致。
- WaitForSingleObject result0、観測98ms（worker receipt109msは別時計区間）。pre/postdigest同値、sampled_state_equal=true、ticks0→0/units0→0。C1/resume contextは保存全項目一致。
- 行21同passにUnit57AA00、行22次passにbattle tick。再開後は原作戦闘が進む。行25/26自然finish preferred493630、return49303F、tick1400、active1→0。行27後のGameEvent returnでmode1/active0。
- 最終29eventではworld後にapplication-requested detach、controller_exit/user_process_killed=false。Frida/controller/unload/reject errorなし。OSプロセスexit code自体はこのreceiptにないため独立証明しない。

## 限界と再開地点
署名とはSHAおよびechoされた識別fieldの照合であり、暗号学的な電子署名/認証ではない。post raw stateは保存されず、post同値は検証済みsourceの計測receiptを根拠とする。
98msはwait開始からの区間で、事前全名簿captureと後処理を含むcallback全体の上限ではない。全writer/MAP/VM/RNG停止、原作SEH/EFLAGS、caller slot、全slot relocation、生成identityは未確定。
外部結果applyは全receiptでfalse。世界mode1復帰は観測したが永続SAVE/全戦略effectの完全commitを証明しない。cleanup待機競合候補はこのrunではworld後detachにつき未発現であり一般解消ではない。
再開: verify_noop_native.pyを固定証拠と照合し、N_NOOP_NATIVE_VERIFICATION.jsonの30条件とscopeを維持する。full G2や結果適用の研究は別revision/別receiptで実施。
保存資料: NOOP_NATIVE_20261024T005426_PREFIX.jsonl、同FINAL.jsonl、同SOURCE.js.txt、N_NOOP_NATIVE_VERIFICATION.json、verify_noop_native.py。
