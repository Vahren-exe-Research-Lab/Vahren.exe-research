# 迫真戦記 REA｜2026-10-29 12H Ogg codebook復号コールバックの間接CALL候補を解決
研究ID：`REA-LOCAL-20261029-12H-P0-OGG-CALLBACK-DISPATCH-STATIC-01`。
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規REA正式VERIFIED=0、Golden=NOT RUN。

## 着手時の独立確認
- Local PCオンライン。最初にMASTER、5レーン規約、共通操作ルール、REA README/QUEUE/PROGRESSと11H報告・証拠、検索索引README/BUILD_MANIFESTを確認。
- 対象隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` を実測一致。SQLite quick_check=ok。
- 最新有効sync `logs/progress_sync_20261011T153958076Z.json`：Wave1～5=64/64 STATIC VERIFIED。QUEUE/PROGRESSはEPERM由来の旧表示であるため更新・集計に使わない。11H=47/47 PASSを保持。
- 開始時 `active.lock`なし、Java/Ghidra先行プロセスなし、空きRAM約14.31GiB。既存12H同名成果なし。未同期10/28資料は正本へ統合しない。

## 今回の新規P0静的成果：間接CALL `0x005E0837`
- 機械語 `0x005E0B5B PUSH 0x005DAD60` → `0x005E0B67 CALL 0x005E06C0`：wrapper `0x005E0B20` は第5引数としてコードブック浮動小数ベクトル加算関数 `0x005DAD60` のポインタを渡す。
- `0x005E06C0` 内の `0x005E0837 CALL DWORD PTR [EBP+0x18]` がその第5引数のコールバックを実行。`0x005E083A ADD ESP,0x10` により、コールバック4引数の呼び出し側stack cleanupを独立確認。
- 対照経路 `0x005E08A0` は `0x005E08DB PUSH 0x005DAA90` → `0x005E08E7 CALL 0x005E06C0`。同一間接CALL siteはwrapperによって `0x005DAD60` または `0x005DAA90` に解決する。
- これらはGhidra `calls` 上で `0x005DAD60/0x005DAA90` の直接callerが0件でも、コールバックとして使用する**独立の静的証拠**。一方、wrapperの実ゲーム到達性・すべての実行可能ターゲットは未確認。
- SQLite `pointer_refs` とEXE 4-byteデータが一致：`0x0061AE7C -> 0x005E08A0`、`0x0061AE9C -> 0x005E0B20`、`0x0061AEBC -> 0x005E0DC0`。3つの4番目オフセット・スロットに相当する表候補だが、vptr代入・runtime dispatchはVERIFY。

## -1エラー処理と返却契約
- `0x005E06C0` は `0x005E0776 CALL 0x005DAA60` 後、`0x005E077E CMP EAX,-1` / `0x005E0781 JE 0x005E0891` で拒否する。通常の上限比較 `0x005E078D JGE` も同じ経路へ進む。
- `0x005E0837` のコールバック返却後は `0x005E083D CMP EAX,-1` / `0x005E0840 JE 0x005E0891` で失敗扱い。`0x005E0891 XOR EAX,EAX` は上位への戻り値を0にする。
- `0x005E0DC0` も `0x005E0E81 CALL 0x005DAA60` の結果-1なら `0x005E0F48`へ遷移して0を返す。`0x005E2A80` では-1でNULLを返す経路を既存疑似Cに確認。戻り値0とNULLはここでは数値として同じだが、各callerの成功/失敗意味論は**未確定**。
- `0x005E08A0/0x005E0B20` は各0 active-channel経路でEAXを0にし、非0なら共通coreのEAXをそのまま返す。元symbol値をarray indexに使用する前の負値全般のvalidationは別途VERIFY。

## 検証と保全
- 旧索引のinfo/pseudo/callers/calleesと、隔離EXE局所Capstone assembly、6 direct CALL site、1 indirect CALL site、3データpointer、22 native命令、8関数存在を照合。監査 **53/53 PASS**、0.746秒、exit0。
- **REA正式5種セットの新規取得0件、正式VERIFIED追加0件**。Wave1～5は64/64、正式TODO/VERIFY/BLOCKED差分0/0/0。原作Golden PASS0、完全複製率不明。
- 新規REA/Ghidra解析とゲーム実行なし。CPU使用率・研究全体の所要時間は未測定。原本・MASTER・QUEUE/PROGRESS・旧RUN・他owner・Git・検索DB・自動化は未変更。
- 保存先はREA所有 `rea_lab/decomp_task/` の新規PROBE/AUDIT/EVIDENCE/STATIC/READBACKのみ。独立読み戻しでのSHA256照合を最終的に実施。
- 次回のP0：`0x0061AE7C/9C/BC` に対応する表のvptr代入・仮想CALL siteをread-onlyで探索し、`0x005E0B20` / `0x005E0DC0` のruntime到達を区別する。ゲームGoldenは実測可能な別担当へ条件設計として渡すだけ。
