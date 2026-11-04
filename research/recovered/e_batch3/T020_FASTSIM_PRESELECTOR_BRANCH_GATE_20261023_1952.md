# E T018/T020｜簡略戦闘の計算前selector・早期分岐を分離（STATIC）
研究ID: E-AUDIT-20261023-1952-T020-FASTSIM-SELECTOR-PRIORITY-01
日時: 2026-10-23 19:52 JST / owner E / STATUS STATIC・VERIFY・NOT READY / Gameplay NOT RUN
対象EXE識別SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（V9索引の記録。今回EXE現物再hashは未実施）
証拠版: search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite（既検証DB SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE）。
参照: V9 CLI function 0x0040E220・0x00431FB0・0x0040D220・0x00452FF0。前回E T020_FASTSIM_RETURN0_PRIMARY_VTABLE_DRAW_GATE_20261023_1850.mdとの差分のみ。
## 非重複の新知見
0x40E220（secondary側this候補）は、冒頭で+0x78と+0x7Cがそれぞれ0x80000008かを比較。いずれか不一致なら0x40E2DF CALL 0x452FF0へ。ここを簡略戦闘実行と数えない。
両mode一致でもsecondary+0x19Cのbyteが0なら何も実行せずreturn（擬似C分岐）。return0の描画制御byte primary+0x84とは別フィールド。
secondary+0x19C!=0のとき0x40E25E CALL 0x431FB0。返値非zeroなら0x40E26D CALL 0x4338D0(1,0)に進み、その回は0x40E2F0を呼ばない。
返値zeroのとき初めて0x40E27F CALL 0x40E2F0。返値0→0x40E28E CALL 0x40D220(1)、返値1/2→0x40E2B9 CALL 0x493630（bool値区別）→0x40E2BE CALL 0x40F000→0x40E2C3 CALL 0x48ABF0。
0x431FB0（ABI未認証）の擬似Cでは in_EAX+0x1EED78 == +0x1EED7C と、各index=0x80000008 または vector-count<=index という二条件をすべて満たすと0、満たさなければ1を返す。これはGhidra未認証の暗黙EAX基点であり、vector実型・Task意味・引数ABI・実際の呼出条件はVERIFY。
0x40E220の直接CALL site 0x40E25E/0x40E26D/0x40E27F/0x40E28E/0x40E2B9/0x40E2BE/0x40E2C3/0x40E2DF はV9のE8 native opcode_kindとして返された。間接virtualの解決・実機到達は未証明。
## T018 Goldenへの影響
G0開始・G1同一run直前SAVE+入力・G2実MAP/三陣営/ordered Unit-Troop・G3結果・G4戦略復帰は依然E受入未充足。DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
合法な同一実行のtraceでは「mode pair→secondary+19C→0x431FB0返値→0x40E2F0到達/未到達→return code→draw/VM/finish→戦略commit」を時点ごとに別receiptにする。早期return・VM分岐・UI drawをG3完了と扱わない。PID/戦闘世代・SAVE/入力各bytesとSHAも必要。
## T020の独立回帰・範囲
同IDのE所有JSON fixture18例とPython gateを新規生成。未観測値VERIFY、実行されない経路にretを混ぜた場合CONFLICT_NONEXEC_RESULT。これらは静的分岐模擬のみで原作Gameplayの合否ではない。
前18:50版のprimary vtable +0x0C/0x452D90、+0xA4/+0x84判定は既知として加算せず、今回追加したのはそれ以前の3段階ゲート（mode・+19C・0x431FB0）である。
T019の確定新矛盾0。GameClear DAT13/TXT2字句範囲差RESOLVEDのみ、script2同名優先/flags/TXT実load/gwrite復帰はVERIFY。
## 継承・統合前ゲート
MASTER最終正式checkpoint196・READY596=A115/B229/C136/D116、34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値、今回全ID・Task再集計なし。新規正式READY0。OFFLINE-UNSYNCED暫定26研究は未照合。
旧安全拒否T018表境界、12時台T020ノート/MASTER復旧、C T026/T032、D T030 TSV、禁止0x5710C0ほかをBLOCKED維持し迂回しない。今回の独立fixture・新研究のみ書込。
NEXT: 条件分岐と実行中のsecondary +0x19C/selector/描画ゲートを一次記録で結び、G3/G4と切り分ける。同一runのG0-G2の合法旧UI証拠取得が最優先。
