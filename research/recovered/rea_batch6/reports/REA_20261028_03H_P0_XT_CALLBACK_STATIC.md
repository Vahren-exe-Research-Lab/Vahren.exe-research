# REA 2026-10-28 03時台｜P0 CRT終了時single callbackスロット初期値と実行到達条件
研究ID: `REA-LOCAL-20261028-03H-P0-XT-NULL-SLOT-NATIVE-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作ゲームGolden実測0、新規REA正式VERIFIED 0。
原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 先読・差分
MASTER/5レーン規約、REA README/QUEUE/PROGRESS、最終progress_sync(64/64)、2026-10-21検索DB manifest、2026-10-28 02H `doexit` 原作ABI監査41/41を参照。既存の「quick=1でも0x0060967C..0x00609680のcallbackループは残る」という**構造**と、実配布PEの**登録値**を今回初めて切り分けた。既存02H/以前のCRT研究を新規成果として再計上しない。

## STATIC A｜CRT配列の実初期値とPE属性
原作PE `.rdata` の特性フラグは `0x40000040`（`IMAGE_SCN_MEM_WRITE` なし）。PE内4-byte DWORDを直接読み取り次を確認：
| VA | 元PE DWORD | 意味 |
|---|---|---|
| `0x0060966C` | `0x00000000` | 通常コールバック範囲の左端 |
| `0x00609670` | `0x005CCD70` | 通常時の非NULL callback 1 |
| `0x00609674` | `0x005BDAB1` | 通常時の非NULL callback 2 |
| `0x00609678` | `0x00000000` | 通常範囲右端 |
| `0x0060967C` | **`0x00000000`** | quick時にも検査される唯一のcallbackスロット |
| `0x00609680` | `0x00000000` | 右端（排他的） |

## STATIC B｜実native分岐とcallsite
`0x005BB5AD` はループ先頭ポインタを `0x0060967C` に設定。`0x005BB5B4` は `0x00609680` と比較。`0x005BB5C0 MOV EAX,[EAX]` → `0x005BB5C2 TEST EAX,EAX` → `0x005BB5C4 JE 0x005BB5C8` → `0x005BB5C6 CALL EAX` という分岐。元PEスロットが0のため、**未改変のロードイメージであれば`0x005BB5C6`のCALLはスキップ**される。`0x005BB5C8`で+4し範囲外へ。`quick=1`は`0x005BB503/507`から通常コールバック部分を飛ばす。通常部分に登録された非NULL2件は`0x005CCD70`（内部でCloseHandle IATへ到達）と`0x005BDAB1`（`0x005BD9F7`呼出し）。これらはquick=1では実行対象にならない。
初期Ghidra DBの`0x0060967C`参照は`0x005BB5AD`（DATA）・`0x005BB5C0`（READ）の2件で、直接WRITE参照0。native `.text`にスロットのリテラル4byteは`0x005BB5B0`の1箇所のみ。**間接ポインタ書込み、OS/プラグイン等による変更は否定しない**。動的な例外伝搬・ExitProcess到達も未実測。

## STATIC C｜原作互換条件
前回02H報告の「quickでも1スロット分のcallback検査がある」は正しいが、**このEXEの静的初期値ではその先の間接CALLは実行されない**。callbackを登録したと推定して通常終了時2件まで省略してしまう説明は不正確。Golden条件は通常終了（2件の非NULL候補）/quick終了（0件）/終了済みguard/明示ランタイム書換え仮説を区別。すべてDESIGNED / NOT RUN。元EXE/ゲームにパッチや実行なし。

## 整合性・進捗・障害
原作/旧DB/V9 SHA照合、両SQLite quick_check=ok、旧02H静的監査41/41確認、REA既存Wave1～5の保存済sync=64/64。今回の独立原作native監査 **38/38 PASS**、新規正式5種完備0・正式VERIFIED追加0・TODO/VERIFY/BLOCKED記録差分0/0/0。5種証拠はinfo/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。原作Golden PASS=0、strict MATCH NOT RUN、完全複製率未測定。
前段PowerShellコマンドの二重引用符処理で構文エラーが1件（OTHER）。変数展開を避けた直接コマンドに変更してpreflight成功。最初の探索プローブで命令途中から逆アセンブルした表示は採用せず、命令境界`0x005BB5AD`を基準に独立監査済み。安全拒否・接続断ではない。
PC preflight: active.lockなし、Java/Ghidra検出なし、空きRAM約9.91GiB、CPU負荷不明。保存前監査2.852秒、保存時2.556秒。研究全体の所要時間不明。新規REA/Ghidra/原作ゲーム/Work実行0。原本、MASTER、QUEUE、PROGRESS、既存runs、他レーン、Git、公開先、スケジュール不変更。
次P0: `0x005BD9F7`通常終了callbackの役割と`0x005B861A`→`0x005BB625`のexitCode由来、終了時guard優先順位の追加静的確認。実ゲーム観測は別の合法な検証工程へ分離する。
