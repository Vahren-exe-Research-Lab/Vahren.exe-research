# 迫真戦記 REA｜2026-10-30 01H：スレッド生成失敗→上位再生状態→解放経路の接続
研究ID：`REA-LOCAL-20261030-01H-P0-OGG-THREADFAIL-PLAY-GATE-CROSSWALK-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、原作Golden実測PASS=0。
## 既存証拠・二重計上防止
MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、RUN一覧、最新progress_sync、統合V9入口、10/25 19H/20H/21H、10/26 03H/04H、10/30 00Hをread-only確認。旧sync `20261011T153958076Z` はWave1–5合計64/64、QUEUE/PROGRESSの旧15/16表示はrename EPERMによる。今回64へ加算しない。
原作専用EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`（SQLite quick_check=ok）。旧search.sqliteは10/29整理済みであり、索引はV9別名を使用。
10/25の19H/21Hは、`0x005B7D14`（__beginthread相当）の失敗返却-1と`0x00502220`での未検査格納・ready=1、CRT側ハンドル閉鎖まで既に確認済み。10/30 00Hは初回PCM fillの下位エラー未検査を確認済み。これらの単独事実は新規発見として計上しない。
## 今回の追加P0：上位の再生開始と失敗後の後片付けを一続きで検証
1. `0x005B7D90 CMP EAX,-1` →失敗時`0x005B7DAF OR EAX,0xFFFFFFFF`。直接CALL `0x00502300→0x005B7D14` の返値は `0x00502308` で `[stream+0x48]` に格納され、`0x0050230B/0E` で戻りAL=1と `[stream+0x44]=1`。失敗時にもこの区間にはEAX=-1検査がない。ここまでは既存事実。
2. **追加接続**：上位 `0x004BE820` の `0x004BEAEF CALL 0x00502220` 後は戻りALを判定せず、`0x004BEAFA CMP BYTE [ESI+0x44],0` のみで `0x004BEB00` のcleanup分岐を決める。よって__beginthread=-1の前提では成功側へ到達し得る。
3. **追加確認**：成功側 `0x004BEB1A` でCOM相当vtable+0x30を取り `0x004BEB22 CALL EDX`。直後 `0x004BEB24 MOV [ESI+0x50],1` で、呼出結果EAX/HRESULTを調べない。条件成立時は**workerが未生成でも、上位が再生開始の関数を呼び、stream状態+0x50を1にする**静的経路が成立する。+0x30の実vptrと音声API成功は実測していない。
4. **追加接続**：後日の `0x004BF2B0` cleanupで、`0x004BF303/306` がready(+0x44)非0ならCOM相当vtable+0x48を呼び、`0x004BF31C CALL 0x00502330` の初期fillをもう一度実行した後、`0x004BF327 CALL 0x00502160` に進む。ready=falseであれば、この追加fillは飛ばす。失敗時ready=trueと結合すると、worker不在でも追加fill側を経由し得る。
5. `0x00502160→0x005021E0` ではstop(+0x4C)=1、+0x48に残った-1を `WaitForSingleObject(handle,100)` に渡し、戻りがWAIT_FAILED(-1)なら待機ループを抜ける経路がある。その後+0x48=0、+0x44=0へリセットする。WAIT_FAILED実測値・他スレッド競合は未観測。
## 範囲・重要な留保
今回の独立した差分は**CRT失敗sentinel→上位のCOM再生呼び出しと+0x50=1→cleanup追加fill/待機**の到達連結であり、個々のCRT失敗検出・PCMゼロ埋め・vtable位置は既往研究成果。原作で__beginthread失敗が再現した証拠はない。音が出る、クラッシュする、ハンドルリークする等は断定しない。
正式REA5方法：info=V9 INDEX、pseudo=V9 INDEX、assembly=同一SHA隔離EXEの局所Capstone、callers=V9 INDEX、callees=V9 INDEX。新規関数別REA正式5種完備=0、VERIFIED=0。正式TODO/VERIFY/BLOCKED書込差分=0/0/0。ゲームGolden実測PASS=0、strict MATCH/完全複製率=未測定。
限定検査 `REA_20261030_01H_P0_OGG_THREADFAIL_PLAY_AUDIT.py`：**47/47 PASS・1.5211秒**。原作SHA/V9 SHA/SQLite、関数7件・直接CALL7件・局所命令24件等を照合。根拠JSON `REA_20261030_01H_P0_OGG_THREADFAIL_PLAY_EVIDENCE.json` はexclusive新規作成。
CPU負荷・研究全体所要時間は不明。直近計測の空き物理RAM=10,771,192 KiB（約10.27GiB）、Java/Ghidra検出0、active.lock無し。新規REA/Ghidra/ゲーム実行なし。最初の一時PowerShellコマンドに引用・変数展開ミス（OTHER、ファイル変更なし）があったが、EncodedCommand形式へ修正しread-onlyで成功。安全拒否ではない。
保存範囲はREA ownerの本回probe/audit/evidence/report/readbackのみ。MASTER、QUEUE、PROGRESS、既存runs、原本ZIP/EXE/SAVE、A–E、T018、dev_lab、Git、公開、Work、スケジュールは無変更。13/14時台OFFLINE成果の正式同期は未実施。
## Golden条件案（DESIGNED / NOT RUN）と次回
正常__beginthreadと失敗-1を分離し、`+0x48/+0x44/+0x50`、上位vtable+0x30呼出回数/戻値、worker実起動、cleanup時の追加fill回数、Wait戻値、再初期化の有無を原作研究コピーで比較。再現前に実ゲームの不具合と判定しない。
次のP0は `0x004BEB22` の実際のDirectSound vptr/Play成否・`0x004BF318` stop経路と `0x005B7D14` ResumeThread失敗直後のハンドル所有をさらに検証し、例外時に「+0x50=1・実worker無し」がどこまで保持されるかを確かめる。
