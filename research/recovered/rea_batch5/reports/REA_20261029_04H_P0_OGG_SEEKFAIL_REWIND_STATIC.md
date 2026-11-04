# 迫真戦記 REA｜2026-10-29 04H Ogg seek失敗コードとループ復帰の接続
研究ID: `REA-LOCAL-20261029-04H-P0-OGG-SEEKFAIL-REWIND-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden実測0、正式新規REA VERIFIED0。

## 初期照合・重複防止
- Desktop Commander Local接続成功。MASTER/ANALYSIS_LANES_PROTOCOL/REA README・QUEUE・PROGRESS・保存済runと2026-10-21検索DB README/BUILD_MANIFEST、03H証拠、および10/26 04Hの既存EOF研究を先読。
- 旧同期ログ `logs/progress_sync_20261011T153958076Z.json` はWave1〜5の64/64 STATIC VERIFIED。QUEUE/PROGRESSはrename EPERMにより古い数値を含むため更新・再計上しない。
- 既存10/26 04Hは「loopフラグ1、read0を繰返すと脱出不明」を既報告。03Hは `0x005D0020` のGhidra `void` 誤型と負return伝播を既報告。本04Hはseek失敗コードの分岐別扱いと、loop復帰での戻り値の破棄を接続。既知現象を新規独立故障として二重計上しない。
- 隔離ターゲットEXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` は現run再計算一致。DB quick_check=ok。

## STATIC-A｜0x005CEB30 seekコールバックのエラー階層・引数ABI
- `0x005CEB38 TEST ECX,ECX`→`0x005CEB3A JE 0x005CEB80`：datasource `decoder[0]` がNULLなら `0x005CEB80 MOV EAX,0xFFFFFF7F`、戻り値 **-129**。
- コールバック `decoder+0x2C4` がNULL、または間接CALL `0x005CEB53 CALL EAX` の返値が **-1** なら `0x005CEB78 MOV EAX,0xFFFFFF80`、戻り値 **-128**。`0x005CEB4E/50/51/52` は `0, high32, low32, datasource` を順にpushし、呼出し後 `ADD ESP,0x10`。x86 cdecl相当の `seek(datasource,offset64,SEEK_SET)` 形式。
- -1以外が返れば `0x005CEB5D/60` にlow/high32位置を保存、`0x005CEB67 CALL 0x005D39F0`で内部バッファ初期化、`0x005CEB71 XOR EAX,EAX`で0成功。登録済みのFILE* seek wrapper `0x005CFDD0` がoffset high32を落とす件は10/28 11H/13Hに既報告であり今回再計上しない。

## STATIC-B｜同じseek障害でも上位APIが返すコードが異なる
- `0x005D0020` は `0x005D00EC CALL 0x005CEB30`→`0x005D00F4 TEST EAX,EAX` で非0ならcleanup `0x005CF9E0`を経て `0x005D0117`で **-137** へ変換。前回03Hの-137条件を下位の-129/-128と突合した。
- `0x005D04E0` は `0x005D0888`/`0x005D08E7`/`0x005D09DB`で同helperを呼ぶ。特に `0x005D08E7`直後、`0x005D08F3 MOV [EBP-0x10],EAX`、非0で `0x005D0B18` cleanupに進み、`0x005D0B39 MOV EAX,[EBP-0x10]` で下位エラー **-129/-128をそのまま返す**。cleanupでdecodeバッファを解放し `decoder+0x58=2` とする。全経路の戻り値型を厳密に復元したとは主張しない。
- 呼出し連鎖 `0x005D0B7A CALL 0x005D04E0`（caller `0x005D0B60`）→`0x005D0B82 TEST EAX,EAX`→`0x005D0B84 JS 0x005D0E7E` は負returnを維持して帰る。上位 `0x005D0F5F CALL 0x005D0B60`（caller `0x005D0E90`）も通常epilogueでEAXを変えずにreturn。これらのCALLとnative命令を旧DBと照合。

## STATIC-C｜loop復帰側はseek失敗を受け取っても捨てる
- OggDecoder fill `0x00501F10` は `0x00501F91 CALL 0x005D12E0` のread戻りをESIへ取り、`0x00501F9B TEST ESI,ESI` でread0判定。ループフラグ `object+4==1` なら `0x00501FB7 CALL 0x005D0E90`（時間0への復帰）へ進む。
- 復帰CALLの直後は `0x00501FBC ADD ESP,0xC` → `0x00501FBF MOV EAX,[EBP+0xC]` で要求サイズをロードし、戻りEAXの負エラーは **比較・伝播されず破棄**。`0x00501FC2 ADD EDI,ESI` なのでread0時に読了バイト数は進まず、要求サイズが残れば `0x00501FCF/0x00501FD3` で再読込へ戻る。
- **条件付きVERIFY**: seek callbackが無い/失敗し、再readも継続的に0、かつloopフラグ有効・要求byte数>0なら、制御が無進捗で再試行を繰返す可能性。10/26 04Hの既存loop空入力疑いを「seek失敗エラー破棄」という追加経路で補強したもので、原作ゲームでのハング発生や無限実行を実測した事実はない。別API `0x00502000` も `0x00502015` 復帰CALLのEAXを無視するが、単独でループとは断定しない。

## 証拠・分類・継続
- 出典：10/21 `search.py function` 0x005CEB30/0x005D0020/0x005D04E0/0x005D0B60/0x005D0E90/0x00501F10/0x00502000、`callers 0x005D04E0`、`callees 0x005CEB30`、`related 0x005CEB30 --depth 2 --limit 30`、read-only SQLite direct/indirect CALLと対象PE32 Capstone。監査 `REA_20261029_04H_P0_OGG_SEEKFAIL_REWIND_AUDIT.py` **71/71 PASS、0.571秒**（検査数であり解析関数数ではない）。
- REA5種: info=SEARCH INDEX、pseudo=SEARCH INDEX+PE対照、assembly=TARGETED PE native、callers=SEARCH INDEX+native site、callees=SEARCH INDEX+native site。新規正式5種完全パッケージ=0、新規正式VERIFIED=0、既存正式64/64維持。正式TODO/VERIFY/BLOCKED変更=0/0/0。独立VERIFYは既存Ogg seek/loop問題の精密化として1群、READY化しない。
- GoldenはDESIGN / NOT RUN：datasource NULL→-129、seek callback NULLまたは-1→-128、`0x005D0020` での-137変換、`0x005D04E0` の-128/-129保持、ループ属性とread0/seek失敗の組合せで呼出し回数・完了/無進捗を原作と比較。原作Golden PASS=0、strict MATCH=NOT RUN、完全複製率=未計測。
- PC接続あり、開始時active.lock無し/Java-Ghidra先行0、空きRAM約16723MiB、CPU使用率サンプル0%。独立監査0.571秒、研究全体所要時間と常時CPU負荷は不明。新規REA/Ghidra/原作ゲーム/Work起動なし。原本ZIP/EXE/SAVE、MASTER、A〜E、T018、QUEUE/PROGRESS、既存runs、検索DB、Git/公開/スケジュール変更無し。
- 10/28 17〜22HのLibraryオフライン成果は未同期のまま保全。今回保存はREA owner内の新規AUDIT.py/EVIDENCE.json/STATIC.md/READBACK.mdのみ、既存資料の上書きなし。
- **再開位置:** `0x005D12E0` のread=0/負値別契約と `0x005CF970` のseek直後parse失敗分岐、さらに0x00501F10のloop時進捗カウンタ/異常復帰。Goldenは実測可能環境・許可の下で別途。
