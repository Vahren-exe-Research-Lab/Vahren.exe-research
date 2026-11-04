# 迫真戦記 REA｜2026-10-30 00H Ogg初期PCM充填→worker起動の復号負値伝播境界
研究ID：`REA-LOCAL-20261030-00H-P0-OGG-PREFILL-ERROR-START-CROSSWALK-STATIC-01`。
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。正式REA新規VERIFIED=0、実ゲームGolden PASS=0。
## 現状・出典
MASTER/ANALYSIS_LANES_PROTOCOL/REA README・QUEUE・PROGRESS、10/29 23H監査/証拠/読み戻し、10/26 03H初期fill・04H worker・05H EOF consumer、旧runのログを先読。最新V9は独立索引 `HAKUSHIN067_UNIFIED_V9_20261023.sqlite`（既存CLIは `search_unified_v9_20261023.py`）。既定の旧 `search.sqlite` は10/29整理済。
原作同一SHA隔離EXE：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
V9 DB SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。本回SHA実計算一致、SQLite quick_check=ok、既存23H 52/52とreadback 12/12照合。V9は複合索引であり単一Ghidraプロジェクトの完全統合ではない。
## P0独立追加：0x00502330の復号失敗と0x00502220起動判定を接続
従来10/26 03Hが「初期fillはp1/len1だけ渡し、実読込bytes/EOFはNULL、Decoder戻りを見ない」と把握済み。10/29 22Hは復号負値-3が`0xFFFFFFFD`のcountになる条件、23Hはworker EOFゲートを把握済み。これらを今回の新規発見として再計上しない。
**今回追加した上位到達照合：** `0x005022E9 CALL 0x00502330`、`0x005022EE TEST AL,AL`、`0x005022F0 JE 0x0050231B`。AL非0ならスレッドハンドル `[ESI+0x48]` がゼロのとき `0x005022FB PUSH 0x005023E0` → `0x00502300 CALL 0x005B7D14`（__beginthread相当）、`0x00502308`でハンドルを保持する。既存スレッドがあれば再起動せず `0x0050230B/0E` で `AL=1` / `stream+0x44=1` として成功復帰する。
`0x00502330` はLock `0x00502387` 後、HRESULTが負なら `0x0050238B` でcleanup `0x00502160`→AL=0。一方Lock成功なら `0x00502398/99` でEOF/bytes出力先にNULLを渡して `0x005023A0` がDecoderのvtable+4を呼ぶ。その返りALをTESTせず `0x005023BF` のUnlockへ進み、`0x005023C2` で**無条件AL=1**。Unlock HRESULTも確認されない。
これを22H既知の下位復号 `-3` 経路と合わせると、`0x00501F5D` でPCM要求領域を0埋め後、`0x00501F91` の-3が `0x00501FC2/0x00501FC6` の符号なし加算・分岐に流れ、`0x00501FEA` でDecoder自体もAL=1で戻る。**Lock成功・有効vptr・下位-3の仮定下では、初期PCMがゼロ埋めであっても初期fill成功となり、上位はworker開始/ready更新へ進み得る。** この「初期fill→起動側の到達接続」が今回の差分であり、復号エラー・音声不具合の実測証明ではない。
二つ目の直接caller `0x004BF31C CALL 0x00502330` は `0x004BF321` から `0x00502160` cleanupへ進み、初期fillのALを使わない別の停止・解放経路。通常のworker起動callerとは区別する。
## 判定・試験設計
新規独立検査 `REA_20261030_00H_P0_OGG_PREFILL_START_AUDIT.py`：**50/50 PASS / 1.010秒**（SHA/SQLite/既存証拠/関数・E8索引/局所原作ASM）。証拠JSON `REA_20261030_00H_P0_OGG_PREFILL_START_EVIDENCE.json` を新規専用名でexclusive保存。局所探査に `...INIT_EOF_PROBE.py`、`...START_CALLER_PROBE.py` を使用。
REA5種：info=V9 INDEX、pseudo=V9 INDEX、assembly=隔離同SHAの局所Capstone、callers=V9 INDEX、callees=V9 INDEX。新規関数別正式5種完備=0、正式VERIFIED+0。既存Wave1～5 64/64は `logs/progress_sync_20261011T153958076Z.json` の旧成功記録で維持し再計上しない。QUEUE/PROGRESSの15/16表示はrename EPERM由来の旧値。正式TODO/VERIFY/BLOCKED書込差分=0/0/0。個別VERIFYは「初期fillの実Lock結果と-3同時成立」「PCM実再生とworker回復」「EOFフラグ未出力時の停止」「スレッドハンドル失敗処理」。
原作Golden実測PASS=0、完全複製率=未測定。合成Golden候補：正常OGG、初期パケット破損で-3、途中破損、短い非loop、空loop、Lock失敗、__beginthread失敗を分離して、初期buffer bytes・ready flag・EOF状態・worker継続を記録。テストは未実行。
PC online、開始時FreePhysicalMemory=12,964,608 KiB（約12.36 GiB）、active.lock無し、Java/Ghidraプロセス検出無し。CPU負荷と調査全体の時間は不明。新REA/Ghidra/原作実行無し。既存安全拒否VA/Wave6/REA exportには触れず。
原本ZIP/EXE/SAVE、MASTER、A～E、T018、dev_lab、Git、公開、スケジュール、QUEUE/PROGRESS/既存runsは無変更。13/14時台等のOFFLINE-UNSYNCED研究は今回統合せず。保存後の独立readbackでファイル実在/SHA/研究ID/正式指標を照合する。
## 次回
P0 `0x00502220` の `0x00502300` (__beginthread) の失敗をどう扱うか、ready `+0x44` とworker handle `+0x48` の寿命/停止処理を調査。成功に見える初期fillとスレッド失敗を区別し、初期fillのゼロ埋めが即音声再生となるとは断定しない。