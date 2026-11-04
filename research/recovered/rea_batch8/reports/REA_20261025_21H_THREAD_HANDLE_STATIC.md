# 迫真戦記 ver0.67｜REA P0 CRT/Ogg worker生成とHANDLE寿命（21時台）
研究ID: REA-LOCAL-20261025-2134-P0-CRT-THREAD-HANDLE-CLOSE-RACE-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。旧実機Golden 0、正式VERIFIED新規0。
出典: 原作研究専用 EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
検索DB SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
解析: 既存Ghidra索引の限定function/related/indirectを先に参照し、別系統でPE/Capstone実機械語を照合。

## 開始時の正式状態/非重複
- MASTER_LEDGER、レーン規約、REA README/QUEUE/PROGRESS、2026-10-11 progress_sync、旧runs一覧、前回20時台研究IDを先読した。
- 2026-10-11同期ログ validated=64/64、Wave1～5=16+10+10+12+16。QUEUE/PROGRESSの古い表示はEPERM由来であり上書きしない。
- 前回研究 REA-LOCAL-20261025-2034-P0-OGG-TEARDOWN-THREAD-WAIT-STATIC-01 の100ms反復待機と二段階decoder cleanupは既知成果として維持、新規計上しない。
- 今回の新規証拠はCRT側「終了時のCloseHandle」と生成失敗の伝播、および関数ポインタ経由のworker到達の独立照合である。

## 新しい静的証拠 A：__beginthread 失敗の返却値と未検査成功状態
- 0x005022FB PUSH 0x005023E0、0x00502300 CALL 0x005B7D14(__beginthread)。
- 0x005B7D7A: CreateThread(IAT)、0x005B7D8A: ResumeThread(IAT)、0x005B7D90: CMP EAX,-1、0x005B7DAF: OR EAX,0xFFFFFFFF（失敗戻り値）。
- 0x005B7D82: [ptd+4]にHANDLEを書き込み、正常時0x005B7DB4でEAXへ返す。
- 0x00502308: [stream+0x48]=EAX。直後0x0050230BでAL=1、0x0050230Eで[stream+0x44]=1。
- callerは__beginthread失敗の -1 を検査せず、0x005022F2の「既存HANDLEが0か」だけを再生成ゲートにする。
- よって失敗時に+0x48=0xFFFFFFFF、+0x44=1となる静的経路があり、再生成時に非ゼロとしてスキップされ得る。実機発生頻度・環境は未測定。

## 新しい静的証拠 B：終了経路がHANDLEを閉じる
- 0x005B7D72で[ptd+0x54]=worker開始関数、0x005B7D77で[ptd+0x58]=引数を設定（Ghidra型復元と原作ASM一致）。
- 0x005B7C92: CALL [EAX+0x54]。このOgg読込経路ではworker 0x005023E0 が間接呼出先。
- 0x005B7C96 CALL 0x005B7C4D(__endthread)。0x005B7C5B: MOV EAX,[ESI+4]、0x005B7C5E: CMP EAX,-1。
- 0x005B7C64: CALL [0x00609088] (CloseHandle)、0x005B7C6B: __freeptd、0x005B7C73: ExitThread(0)。
- worker通常復帰に伴う__endthreadが、親stream+0x48と共通originのHANDLEをCRT側で先にCloseHandleする経路が確認できる。
## 新しい静的証拠 C：WaitForSingleObjectは無効HANDLEを終了扱い
- 0x005021E3終了要求フラグ+0x4C=1、0x005021F3から+0x48を読み0x005021F9でWaitForSingleObject(handle,100)。
- 0x005021FB: CMP EAX,0 / 0x005021FD: JE 0x502204（WAIT_OBJECT_0）。
- 0x005021FF: CMP EAX,-1 / 0x00502202: JNE 0x5021F3（WAIT_FAILEDならループ脱出）。
- 0x00502208でHANDLEを0にするが、CloseHandleはしない。__endthreadで先にCloseHandleしたHANDLEを待つ時間的競合に注意。
- 生成失敗sentinel -1をHANDLEとして渡した場合は、Win32 WaitForSingleObjectが失敗する可能性が高い。ただし実際のGetLastError等は未観測。
- CloseHandle済みHANDLEを並行して待つ操作の結果・資源アクセス競合は動的未検証。ここから確定UAF/リークとは判定しない。
- 追加VERIFY: ResumeThread失敗後のCreateThread HANDLEについて、CRT __beginthread失敗後cleanupには直接CloseHandleが見えない。実条件・外部救済は未確認。

## 静的監査/正式REA境界
- 独立監査ファイル REA_20261025_21H_THREAD_HANDLE_AUDIT.py は原作PE実バイト/Capstone、SQLite read-only、SHA256と整合性を確認。
- 独立静的テスト 62/62 PASS（EXE/DB SHA、ImageBase、機械語39箇所、DB関数7、直接CALL4、間接CALL7、workerアドレス参照1、SQLite quick_check）。
- info/pseudo/assembly/callers/callees は部分索引＋新ASMを使用。新規5種関数別REA正式完全充足0、正式VERIFIED増分0。
- 正式TODO/VERIFY/BLOCKED書込差分0/0/0。過去64件を再計上しない。原作Golden実測0、strict MATCH未実測、完全複製率未測定。

## Golden条件案（DESIGNED / NOT RUN）
1. __beginthreadが-1を返す失敗を注入し、stream+0x48の値・+0x44フラグ・再初期化判定が原作と一致するか確認。
2. 正常worker即終了・stop中終了・長時間停止の各場合でWaitForSingleObjectの実戻値、CloseHandle順序、+0x48の遷移を記録。
3. ResumeThread失敗を切り分け、生成済HANDLE/CRT ptiddataと後処理を測定。
4. 反復Sleep(100)/Wait(100)と無期限待機の関係を分離して検証。
5. 注入テストは研究コピー上のみ、ゲーム本番セーブや原本EXEには触れない。

## 安全/保存/次VA
- PC Localに接続成功、21:38の確認でactive.lock=False、専用REA/Ghidra競合検出なし、空きRAM約7.68GiB（REAを新規起動する条件を満たさない）。
- 新規REA/Ghidra/原作ゲーム実行0回。CPU負荷は37%（単発の観測値）、研究全体の実行時間は不明（監査個別時間はEVIDENCE.jsonへ記録）。
- 作業対象はREA所有の21H新規4ファイルと読み戻し記録のみ。MASTER、QUEUE、PROGRESS、runs、A～E、T018、原本、Git、公開先、Work、スケジュールを変更しない。
- 13/14時台のLibraryオフライン成果は引き続きPC正本への正式同期未完了。安全拒否済Wave6/0x5710C0..0x571500や拒否済ファイル操作は迂回しない。
- 次回P0は 0x005B7C4D(__endthread)の例外ケースおよび0x005B7C7A(__callthreadstart)のSEH捕捉、0x005B7D14のResumeThread失敗時のHANDLE所有と、0x005022C4 のCOM vtable呼出先を優先。
