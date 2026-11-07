# 迫真戦記 REA｜2026-10-31 00H｜Ogg最終cleanup callbackの設定元とclose責任（P0）
研究ID：`REA-LOCAL-20261031-00H-P0-OGG-FILE-CLOSE-CALLBACK-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。前回23Hで発見済みの間接CALL自体、22Hの3種内部dispatchは二重計上しない。
## 新規静的証拠
- `0x005D16C0` は `0x005D16CF` でファイルを開き、成功時 `0x005D1701 mov esi,0x005B7A4E` と `0x005D170B mov [eax+8],esi` でCRT `_fclose` を第7引数として `0x005D1712 call 0x005D1630` に渡す。隣接するread=`0x005B77CB`、seek=`0x005CFDD0`、tell=`0x005B797C` は別slot。
- `0x005D1630` の `0x005D1645 mov ecx,[ebp+0x20]` → `0x005D164E mov [eax+8],ecx` → `0x005D165F call 0x005D1490` によって第7引数を次の生成関数へ中継。
- `0x005D1490` の `0x005D14D7 mov ecx,[ebp+0x18]` → `0x005D14EE mov [esi+0x2C8],ecx` でclose callbackをオブジェクトに保存。これにより前回23Hの未同定 `outer+0x2C8` 設定元を標準ファイル読込経路に限り解決した。
- `0x005CFE00` は `0x005CFEDF/0x005CFEE1` で `outer[0]!=0`、`0x005CFEE3/0x005CFEEB` でclose callback非NULLを確認し、`0x005CFEEE call eax` で `outer[0]`（FILE*）を引数に渡す。標準ファイル経路のCALL先は `0x005B7A4E`（V9のMSVC 2010 CRT `_fclose`）。
- 失敗時は `0x005D1587` または `0x005D1695` が `outer[0]=0` にしてから `0x005CFE00` を呼び、callbackを抑止する。一方、標準ファイルwrapper `0x005D171C/0x005D171E/0x005D1721` は戻り値非0なら `0x005B7A4E` を直接呼ぶ。正常解放と失敗解放の責務を分岐させる構造。
## 解釈の制約
- この具体的な `_fclose` への対応は `0x005D16C0→0x005D1630→0x005D1490` の標準ファイル経路についての静的結論。別のcaller、別設定、FILE*無効化、再入、他スレッド、実行時のclose回数は未確定。
- `0x005D3DE0` のtag読取先 `0x005D3E2B / 0x005D3E5D / 0x005D3E96` のwriterや範囲保証は未解決。今回のclose callbackと混同しない。ABIの正式確定も行わない。
- 以前の同一領域での不正シーク位置仮説は重複計上なし。ゲームGolden 0・完全複製率未測定。
## 検証・保存
- 原作研究コピー SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。統合V9 DB SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、独立V9 verify PASS、SQLite quick_check=ok。
- V9 function/callers/callees/pseudo と研究コピーの局所Capstone ASMで確認。監査 **29/29 PASS（0.8943秒）**。この監査はformal REA 5種証拠の新規完備を意味しない。
- 初回監査27/29は作成した照合scriptにある2個の命令開始VAの誤記（`0x005D170E`→`0x005D170F`、`0x005CFEE0`→`0x005CFEE1`）。修正後29/29 PASS、対象EXE/既存証拠は未変更。RECOVERY-ID `REA-RECOVERY-20261031-00H-AUDIT-OFFSET-01`、分類OTHER、未保存発見なし。
- 正式既存STATIC VERIFIED **64/64**（`logs/progress_sync_20261011T153958076Z.json`を再読）。新規正式VERIFIED0・新規5種証拠一式0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- PCオンライン・開始時active.lockなし、空き物理RAM **12290920KiB（約11.72GiB）**。Java/Ghidra競合プロセスのリスト表示なし。CPU負荷/総作業時間不明。追加REA/Ghidra/ゲーム実行なし。
- REA専用フォルダの新規独立IDのみ書込。MASTER/QUEUE/PROGRESS/既存RUN/原本/A-E/dev_lab/Git/スケジュールを変更しない。
## 次回
- `0x005D3E2B / 0x005D3E5D / 0x005D3E96` で読むtag群のwriter・値域とallocation初期化からの到達を追う。callbackについては別caller/再入の可能性だけVERIFYで保持する。
- Golden案：正常open→close1回、初期化失敗→wrapper close1回、再入・異常FILE*・tag境界を分離（**すべて未実測**）。
