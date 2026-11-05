# 起動直後終了の再発とファイルロック修復（2026-11-04）

## 原因と過去研究
- 2026-11-03の既知事例: `STARTUP_LOCK_ROOT_CAUSE_20261103.md`。
- 当時はDesktop Commander LocalのNodeプロセスがDATを開いたままで、Vahren.exeがDATを排他オープンできず終了コード0で約1.2秒後に終了。原作/EXE/DLL破損ではなかった。
- 今回の起動失敗時も、ゲームの`a_default/script`配下で同じ種類のファイルロックを検出。

## 今回の観測と作業
- Windows Restart Managerで対象5ファイルのロック所有者をすべてPID 8884（Node.js / Desktop Commander Local）と特定。
- Sysinternals Handleで、PID 8884内のファイルハンドルを6個検出。
- 対象: `event_world.dat`（0x75C）、`100_イベント汎用/event_battle.dat`（0x7CC）、`2000_勢力ストーリー/po11_event.dat`（0x448、0x4C8）、`6000_スキルテスト/0maptest.dat`（0x6C8）、`6000_スキルテスト/skilltest.dat`（0x718）。
- 過去の `release_verified_handle.py` を参照し、新規の `release_verified_dat_locks_20261104.py` で対象プロセス内の各ハンドルの実ファイルパスをWin32 APIで2回ずつ照合してから、確認済み6個だけを `DuplicateHandle(DUPLICATE_CLOSE_SOURCE)` で解放。結果: 6/6成功。
- 結果JSON: `release_verified_dat_locks_result_20261104.json`。
- 解放直後にDAT全595件の`FileShare.None`による排他オープン検査: **595/595成功、ロック0件**。
- 解放直後のHandleツール再照合: PID 8884に対象 `a_default/script` のハンドルなし。
- 原作EXE、DLL、既存`HS_Summon_Test.dat`、新規`HS_Simple_Battle_Test_20261104.dat` のSHA-256が作業前の期待値と一致。ファイル内容変更なし。

## 変更禁止・再発防止
- **ゲームDAT、EXE、DLLは一切書き換えていない**。今回の修復対象は残留ファイルハンドルのみ。
- 今回のPID 8884およびハンドル番号は一度限り。以後の再発で**再利用禁止**。
- 今後ゲームDATの調査はDesktop Commander Localの`read_file`で長期ハンドルが残らないよう、必要なテキストは短命Python/PowerShellプロセス内で読み込んで即終了する。
- ハンドル強制解放は例外的な修復操作であり、他の実行中の読み書き処理を壊す危険があるため一般化しない。
- **ユーザー希望に従い、今回の修復後にVahren.exeの起動テストは行っていない**。ゲームの起動可否は本人の実機操作で最終確認する。
