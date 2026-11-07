# 迫真戦記 REA｜2026-10-30 03H：Ogg DirectSoundBuffer8の実IID・共有COM所有先・再充填時カーソルリセット
研究ID：`REA-LOCAL-20261030-03H-P0-DSBUFFER-ALIAS-CURSOR-RESET-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED 0、原作Golden実測0。
## 事前照合・出典
共有MASTER/レーン規約/REA README・QUEUE・旧PROGRESS、2026-10-30 02H 既存証拠・37/37監査・11/11 readback、最新保存済み `logs/progress_sync_20261011T153958076Z.json` を先読した。旧Wave1–5の正式静的証拠64/64は不変。旧QUEUE/PROGRESSの15/16はEPERMによる陳腐化のため編集しない。旧runsの全再実行は不要。
同一SHA256隔離EXE：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。統合V9 DB：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。SQLite quick_check=ok。旧README/search.sqliteは10/29整理で不在、V9別名で検索・read-only。
## 新規P0静的証拠1：QueryInterface対象の実GUIDを固定
`0x005022D3 PUSH 0x0060971C`→`0x005022D9 CALL EDX`。PEのVA `0x0060971C` の16byteは `49A425682475824D920F50E36AB3AB1E`（GUID Windows little-endian）で、`6825A449-7524-4D82-920F-50E36AB3AB1E` と一致する。これは **IID_IDirectSoundBuffer8** の公開定義と一致。`0x00502286 LEA EDI,[ESI+8]` と `0x005022D2 PUSH EDI` は、問い合わせの出力先が `stream+0x08` であることを支持する。IID照合は今回追加、QueryInterface失敗時の検査不足自体は10/26既知。
## 新規P0静的証拠2：Play/Stop/Lock/Unlockが同一stream+8フィールドを参照
親の `0x004BEAE9 MOV ESI,[EBP+0xA0]` → `0x004BEAEF CALL 0x00502220`、その後 `0x004BEAF4` で同じ所有フィールドからESIを再取得。`0x004BEB15 MOV EAX,[ESI+8]` → vtable+0x30のPlayを呼ぶ。
初期化側 `0x005022E7 MOV EAX,ESI` → `0x005022E9 CALL 0x00502330`、被呼出側 `0x00502334 MOV ESI,EAX`。その同一オブジェクトの `+0x08` を、SetCurrentPosition(+0x34, site `0x00502354`)、Lock(+0x2C, `0x00502387`)、Unlock(+0x4C, `0x005023BF`) に使用。cleanupは `0x004BF2F5 MOV EDI,[ESI+0xA0]` → `0x004BF308 MOV EAX,[EDI+8]` → Stop(+0x48, `0x004BF318`)を実行。現存する静的経路では共通の `stream+0x08` が再生COMインターフェース。
## 新規P0静的証拠3：停止後の再充填が再生カーソルを0へ戻す
cleanupの `0x004BF318` Stop後、`0x004BF31C CALL 0x00502330` に入る。再充填関数で `0x00502339 XOR EDI,EDI` → `0x00502352 PUSH EDI` → `0x00502354 CALL EDX` は vtable+0x34 の **SetCurrentPosition(0)** と一致。続いて `0x00502359 PUSH 2` を含む vtable+0x2C Lock（**DSBLOCK_ENTIREBUFFER=2**）へ進む。Play側は vtable+0x30 に **DSBPLAY_LOOPING=1** を渡すが、これはバッファ循環であり楽曲のリピートとは別。Stop・Lock・Unlockなどの関数存在自体は以前の研究で既出。今回の差分は **IIDの実値、親→初期化→解放のstream+8所有参照連結、Stop直後再充填時のSetCurrentPosition(0)とLock全領域フラグの確認**。
参考定義：Wine dsound.h（IID_IDirectSoundBuffer8、DSBLOCK_ENTIREBUFFER、vtable）https://sources.debian.org/src/wine-development/2.0-3/include/dsound.h/ ; Microsoft Learn（Play/SetCurrentPosition）https://learn.microsoft.com/en-us/previous-versions/windows/desktop/mt708933(v=vs.85) 、https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee418076(v=vs.85)
## 検証と未確定
独立監査 `REA_20261030_03H_P0_DSBUFFER_ALIAS_AUDIT.py` は原作SHA、V9 SHA、SQLite、4関数・3直接CALL・局所x86レジスタ/フィールド/ABIを **53/53 PASS（0.896秒）**。追加IID監査 `REA_20261030_03H_P0_DS8_IID_AUDIT.py` は **5/5 PASS**。対応JSON 2件、read-onlyプローブ2件、監査2件と本報告はREA所有領域へ新規保存。正式REA5方法は info=V9索引、pseudo=V9索引、assembly=専用PE局所Capstone、callers=V9索引、callees=V9索引で、**新規正式5種完備0・新規正式VERIFIED0**。正式TODO/VERIFY/BLOCKED書込差分0/0/0、Golden実ゲームPASS0、完全複製率未計測。
静的同一性は、該当streamが途中で差し替わらず、QueryInterfaceが成功し、他スレッドがCOMポインタを破棄しないことを条件とする。実行時の実vptr、HRESULT、buffer cursor、Stop後の再生、破損PCM、race・クラッシュは未観測。エラーをゲーム不具合として確定しない。
PC接続正常、active.lock無し、Java/Ghidra競合なし。空きRAM約11.67GiB（11,949.5MiB）。CPU負荷と研究全体所要時間は不明。原本、MASTER、A～E、QUEUE/PROGRESS、既存runs、Git、公開、Work、スケジュールは無変更。過去オフライン成果は未同期のまま。新REA/Ghidra実行および原作ゲーム実行0回。
一時 `python -c` 引用/日本語パスの解釈ミスでSyntaxErrorが発生（OTHER、`REA-RECOVERY-20261030-03H-QUOTING-01`）。安全拒否ではない。専用read-only Pythonプローブに置き換えて正常解析、元対象に変更なし、RECOVERED。
## Golden条件案・再開位置（DESIGNED / NOT RUN）
QI成功/失敗、実際のIIDと+8出力ポインタ、SetCurrentPosition(0)前後のカーソル、Lockの領域長/2区間、Unlock HRESULT、Stop後の再充填、別スレッドからのCOM参照を同一時系列で記録。次は `0x00502330` のLock返却2領域ポインタ/バイト数とUnlockの4引数対応を確認し、二領域時の使用量とエラー時の処理を絞る。ownerはREA、音声Task T015への共有は独立証拠として保留。
