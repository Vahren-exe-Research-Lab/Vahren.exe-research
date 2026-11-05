# REA / Ghidra 逆コンパイル定期タスク

目的: 迫真戦記 ver0.67 bundled PE32 x86 Vahren.exe と同一SHA256の**専用コピー**を使用して、重要関数を少数ずつ静的逆コンパイルする。
原本ZIP/EXE・5レーン・MASTER_LEDGER・Codex設定は更新しない。RENEW/INSTALL/MCP登録、Git/push/公開を行わない。

## 現在のタスク構成

- `QUEUE.json`: Wave1=16関数（保存済みrun照合で全16 STATIC VERIFIED）、Wave2=10候補。`wave`省略はWave1、`wave:2`はWave2。Windowsの既存ファイルrename EPERM時はstatus表示が古い場合があるため、RUN_RESULT＋5種証拠と最新syncログを優先。
- `WAVES.md`: wave別の凍結分母・候補アドレス・障害と再開位置。
- `PROGRESS.md`: 人が読む進捗。ただしWindows Node renameのEPERMが続いており古い場合がある。`logs/progress_sync_*.json`中の`waveProgress`・`queueUpdate`・`humanReadableProgress`を必ず参照。
- `run_decompile.ps1`: Desktop Commander Localのみで起動。メモリ8GB以上/Java重複なし/原本ハッシュ一致の場合のみ実行。
- `run_batch.mjs`: REA pinned 6.4.0を単一MCPセッションで起動。1回最大4関数（ソフト上限6）を解析。QUEUEが更新できなくても保存済みsource SHA/verified RUN_RESULT/5方法の証拠ファイルを見て同じ関数を再解析しない。
- `sync_progress.mjs`: 保存済みRUN_RESULTと5種類のGhidra静的証拠を検証。既存QUEUE/PROGRESSのrenameがEPERMならACLを変更せず、固有tmp snapshotと`logs/progress_sync_*`へ`PARTIAL`状態を正確に残し、同じ拒否を繰り返さない。
- `runs/<runId>/`: runごとのMCP生JSONとチェックポイント。既存ファイルを上書きしない。
- `logs/`: 自動集約実行ログ。誤更新や実行停止の原因調査用。

## 運用方法

1. `../../MASTER_LEDGER.md` と `../../evidence/ANALYSIS_LANES_PROTOCOL.md` を先にread-onlyで確認（`decomp_task/`からの相対path）。
2. `QUEUE.json` と `PROGRESS.md` を読む。`active.lock`の有無、Get-Process Java/Ghidra、利用可能メモリを確認。
3. Desktop Commander Local経由で、環境/構文チェック済みなら `& '<このフォルダの絶対パス>\run_decompile.ps1'` を開始。
4. 出力を追跡し、既存プロセスを妨害せず完了/timeout/安全拒否まで観察。
5. `QUEUE.json`、`PROGRESS.md` と `RUN_RESULT.json` の一致・新規数を読み戻して確認し、日本語で進捗報告。

旧A〜Eタスクは停止のまま保持され、別途新A〜Eの再作成が行われた。本REAタスクと所有範囲を分離し、A〜E/REAの実行状態・スケジュール変更をこのラボから行わない。
既往安全拒否 `0x5710C0..0x571500` は初回キューへ入れない。`extract_verified.mjs`の未完成/拒否済み保存処理も再試行しない。
REAはGhidra初期解析に数分かかる。重い解析の並列起動、同じ関数の根拠ない再取得、無限再試行、GUI/ゲーム実行はしない。
異常終了で`active.lock`が残った場合は勝手に破棄せず、所有プロセス・部分RUN_RESULTを調べ安全確認する。

## 判定の区別

- `TODO`：未取得。`VERIFIED`：Ghidra疑似コード/ASM/関数境界/呼出関係の証拠を保存し、同一EXEハッシュ/証拠IDに整合。
- `VERIFY`：関数境界など一部未確定。`BLOCKED`：安全拒否など。`SKIPPED`：競合・空きメモリ不足。
- キューの分母16件は初回優先範囲。**全EXEの逆コンパイル率でもゲーム全体の完成率でもない**。
- 旧EXE実ゲームgoldenテストPASS=0のまま。完全互換性は独立テストで初めて判定する。

## 担当境界

本専用タスクは`rea_lab/decomp_task/`にのみ新規ファイルを書き、既存成果は参照するだけ。
新しい発見はアドレスとevidence IDで記録し、A/B/C/Dの所有Taskに照合してもらう。正本への正式統合はEだけが行う。
本タスクの実行が失敗しても自動化自体は勝手に停止・削除しない。次回の安全なチェックポイントを報告する。
