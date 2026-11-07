# 迫真戦記 REA｜2026-10-29 20H Ogg wrapperの非0戻り値とresidue復号の失敗扱い
研究ID：`REA-LOCAL-20261029-20H-P0-OGG-UPPER-ERROR-RETRY-RESIDUE-ZERO-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作実機Golden未実測、正式REA5方法証拠の新規取得なし。
## 入口・非重複照合
MASTER、evidence/ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、19H報告/evidenceと既存同期ログを読取。QUEUE/PROGRESSは既知のEPERM stale、既存正式Wave1-5=64/64を保持する。19Hのmapping inverse正常return0と下位EAXの上書きは再計上しない。
現行正本は統合V9（古いsearch.sqliteでなく`HAKUSHIN067_UNIFIED_V9_20261023.sqlite`）。隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。V9 CLI `function 0x005CFA10` および3種のresidue逆復号関数と共通処理を限定参照。
## P0 新規静的証拠：上位 `0x005CFA10` はwrapperエラーを次パケット探索へ変える
CALL site `0x005CFACF` → `0x005D45E0`。戻り直後 `0x005CFAD7 TEST EAX,EAX`、`0x005CFAD9 JNE 0x005CFA90`。非0（wrapper固有の-135/-136を含む）は**直ちに同じ値を上位へ返さず、パケット取得ループへ戻る**。0時は `0x005CFAE4 CALL 0x005D5730` に進む。
次の読込 `0x005CFA9F CALL 0x005D3BC0` が-1なら `0x005CFAAE CMP EAX,-1`→`0x005CFAB1 JE 0x005CFC6C`、`0x005CFC6E MOV EAX,0xFFFFFFFD`により **-3** を返す。継続時の状態遷移とEOF到達条件はVERIFYで、すべての非0が必ず-3になるとは言わない。
復号成功後 `0x005CFAEC TEST EAX,EAX` が非0なら `0x005CFAF6 MOV EAX,0xFFFFFF7F` の **-129**。これは別の境界で、wrapperの-135/-136を直接伝播したものではない。
## P0 新規静的証拠：residueモードの戻り値は失敗検出の指標にならない
mode0 `0x005E08A0` とmode1 `0x005E0B20` は、それぞれ `0x005E08E7` / `0x005E0B67` で共通 `0x005E06C0` を直接CALL。共通処理は `0x005E0776` でcodebookを復号し、-1時 `0x005E0781 JE 0x005E0891`。コールバック `0x005E0837 CALL [EBP+0x18]` 後に-1なら `0x005E0840 JE 0x005E0891`。`0x005E0891 XOR EAX,EAX` で0として終了する。
mode2 `0x005E0DC0` も `0x005E0E81 CALL 0x005DAA60` の-1時 `0x005E0E8C JE 0x005E0F48`、`0x005E0F0C CALL 0x005DB120` の-1時 `0x005E0F17 JE 0x005E0F48`。出口 `0x005E0F4A XOR EAX,EAX` / `0x005E0F50 RET`。したがって3モードの確認済み経路では内部の復号失敗が戻り値0に折り畳まれる。バッファ変更・副作用や実ゲームの音声欠損は未実測で、成功と同一効果だとは断言しない。
## 検証、障害、再開
REA所有の独立監査 `REA_20261029_20H_P0_OGG_UPPER_ERROR_ROUTE_AUDIT.py`：**38/38 PASS、1.120秒**。機械語、既存19H証拠、旧RUN同期数、対象VA、隔離EXE/V9ハッシュの照合結果：`REA_20261029_20H_P0_OGG_UPPER_ERROR_ROUTE_EVIDENCE.json`。5方法の新規正式束0、新規VERIFIED0、公式TODO/VERIFY/BLOCKED差分0/0/0、既存64/64。Golden PASS0、完全複製率未測定。PC接続正常、開始時空きRAM約11.56GiB、active.lockなし、先行Java/Ghidra検出なし、CPU負荷と全作業時間は不明。REA/Ghidra再実行なし。
復旧ID `REA-LOCAL-20261029-20H-RECOVERY-CLI-QUOTING-01`：最初のPowerShell経由Python -cで引用符解釈が崩れSyntaxError（OTHER/COMMAND_SYNTAX）。安全拒否ではなく原本未変更。REA所有の通常の.pyプローブへ切替し成功、未保存解析結果なし。
原本、既存RUN、他レーン、MASTER、QUEUE、PROGRESS、Git、V9、スケジュールは変更していない。前回成果との重複計上なし。既存オフライン未同期成果は未統合。
**次回**：`0x005CFA10`の上位caller、失敗パケット連続時のexit状態・`0x005D3BC0`のEOF分岐を重点調査。実機での音声破綻/無限ループの有無はVERIFY、Golden設計のみ可。
