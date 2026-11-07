# 迫真戦記 ver0.67｜REA P0 CRTスレッド生成失敗・FLS初期化異常経路（22時台）
研究ID: REA-LOCAL-20261025-2234-P0-CRT-START-FAILURE-OWNERSHIP-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY
対象: 研究コピー hakushin067_Vahren.exe、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
DB: 2026-10-21 Ghidra検索基盤 search.sqlite、SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 開始時・過去成果の扱い
- MASTER/ANALYSIS_LANES_PROTOCOL/REA README/QUEUE/PROGRESS、Wave1～5同期ログ、21時台の証拠を読み取り。64/64 VERIFIEDは過去記録であり今回計上しない。
- QUEUE/PROGRESSの古い状態表示はEPERMに伴うstaleであり、2026-10-11T15:39:58Zのprogress_sync validated64/64を優先。
- 21時台には beginthread -1戻り値と worker正常終了の CloseHandle が既知。今回の追加対象は ResumeThread 失敗後のHANDLE扱いとFLS初期化失敗の早期ExitThread。
- 既存19～21時台の調査ファイルは保存・重複ID照合のみ。安全拒否済みWave6、指定VAや拒否済み旧操作に接触しない。

## 新規静的証拠A：ResumeThread失敗時のHANDLE解放が見えない
- 0x005B7D67 PUSH 4 (CREATE_SUSPENDED)、0x005B7D6A PUSH 0x005B7CBB（thread entry）。
- 0x005B7D7A CALL [0x006090A4] はPE IATから KERNEL32!CreateThread と確認。
- 0x005B7D82 は取得HANDLEをPTD+4へ格納、0x005B7D8A CALL [0x0060914C] はResumeThread。
- 0x005B7D90 CMP EAX,-1、0x005B7D93 JNE 0x005B7DB4。失敗側は0x005B7D95 GetLastError→0x005B7D9E _free(PTD)→0x005B7DAF EAX=-1。
- 0x005B7D14関数内に直接のCloseHandle呼出命令なし。成功側(0x005B7DB4)ではCreateThreadのHANDLEを返す。
- **新規VERIFY:** CreateThread成功→ResumeThread失敗では、この関数の局所経路にHANDLEを閉じる処理がない。実際のHANDLEリーク・停止スレッドの生存期間は動的未実測で、確定バグとしない。

## 新規静的証拠B：スレッド開始FLS設定失敗の早期終了
- 0x005B7CBB (__threadstart@4) がFLS状態を取得し、必要なら0x005B7CDD の FLS set helper を呼ぶ。
- 0x005B7CE2 TEST EAX,EAX、0x005B7CE4 JNE 0x005B7D0E。設定失敗は0x005B7CE6 GetLastError→0x005B7CED KERNEL32!ExitThreadへ直接進む。
- 通常経路0x005B7D0Eの __callthreadstart(0x005B7C7A)は、その後0x005B7C96で__endthread(0x005B7C4D)に入り、0x005B7C64でKERNEL32!CloseHandleを呼ぶ。
- **新規VERIFY:** FLS設定失敗の早期ExitThread経路では上記__endthreadが呼ばれない。CRTによる同一HANDLE自動クローズの保証はこの経路からは得られない。
- どちらも機械語による到達可能経路の静的判定であり、実環境で例外発生・リークを再現したわけではない。
- __callthreadstartの0x005B7CA7例外フィルタ枝はSEH復元依存のため通常復帰とは区別。今回の範囲で例外伝播先まで確定しない。

## 検証基準と結果
- 保存済み検索CLIから対象関数と直接/間接CALLを照会し、Capstone独立逆アセンブルとPEインポートテーブルで再照合。
- Python監査は原作/DB SHA、PE ImageBase、IAT5、関数完全逆アセンブル5、ASM分岐等31、IATクローズ呼出不在2、SQLite・関数索引・CALL・data refを検証。
- 独立静的監査 62/62 PASS。新規正式REA5種関数別証拠充足0件、新規正式VERIFIED0件。
- 正式QUEUE/PROGRESS/MASTERに書込なし、TODO/VERIFY/BLOCKED正式差分0/0/0。旧64件は維持。
- 原作ゲームGolden実測PASS 0件、strict MATCH未測定、完全複製率未測定。
- ゲームの通常プレイ結果とCRT異常系を混同しない。Golden条件はDESIGNED/NOT RUN。

## Golden条件（設計のみ）
1. 研究コピー環境でCreateThread成功/ResumeThread失敗を模擬し、戻り値、最後のエラー、PTD寿命、HANDLE数とスレッド状態を観測。
2. スレッドのFLS設定だけ失敗させ、ExitThread経由か__endthread経由か、HANDLEの寿命を測定。
3. 正常終了、wait中終了、WAIT_FAILED分岐、同一stream再利用時の+0x48/+0x44状態を別々に比較。
4. 注入条件なしで通常ゲーム中に発生するかは別指標として観測。いずれも未実行。

## 安全・再開位置
- Windows研究PCは接続成功。開始時active.lockなし、専用REA/Ghidra/Java競合なし、空きRAM約10.94GiB。CPU負荷未測定。
- 新規REA/Ghidra/原作ゲーム起動0回。調査は保存済みGhidra DB・研究用EXEのread-only解析のみ。
- 13/14時台のオフライン成果は正式PC同期未完了（前回から変更なし）。原本、MASTER、A～E、T018、QUEUE、PROGRESS、既存runs、Git、Work、定期実行設定は変更しない。
- 次回: 0x005B7CEDの早期ExitThreadに達するFLS helper 0x005BC522の戻値詳細、および0x005022C4のCOM vtableの具体的IFaceを解析。安全な範囲のみ、既存証拠と非重複確認後に継続。

