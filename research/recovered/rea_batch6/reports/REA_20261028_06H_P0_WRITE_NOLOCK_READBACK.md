# REA 06H｜P0 __write_nolock 保存後独立読み戻し
研究ID: `REA-LOCAL-20261028-06H-P0-WRITE-NOLOCK-ERROR-RETURN-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**（2026-10-28 JST）。
別Pythonプロセスで保存済み監査を **40/40 PASS、失敗0、約1.108秒** と再実行。原作EXE・初期DB・V9 SHA一致、両SQLite quick_check=ok、active.lock不在。
- `REA_20261028_06H_P0_WRITE_NOLOCK_AUDIT.py`: size 4852, SHA256 `3B91B84A103172254B172521AF78B28FFF374B0BE5F5D1C11181E181AFB960DB`
- `REA_20261028_06H_P0_WRITE_NOLOCK_EVIDENCE.json`: size 3814, SHA256 `B2F92543352471BC068DA16822E44747CBC10DC3452A991B738244412A4720FE`
- `REA_20261028_06H_P0_WRITE_NOLOCK_ERROR_RETURN_STATIC.md`: size 4703, SHA256 `BB7B3ED53F0E5A25E742776F2DB3A9C7F21815AB090818C5AFB8C19F8A2F6320`
証拠JSON読戻し: ID一致、40/40、failed=[]、formal_added=0、golden_pass=0。日本語報告書の研究IDも一致。
非重複: 05H 34/34証拠・20261011同期64/64を監査に含め、今回の新規REA正式VERIFIED=0。5種正式証拠未取得。ゲームGolden実測0。
調査中の一時的な障害: 初回read-only probeのUnicodeパスがPowerShell→Python pipeで文字化けし、PythonがWinError 123。実ファイルを変更せず、作業ディレクトリからの相対参照によって正常に検証。安全拒否ではない。
CPU負荷・研究総所要時間は未測定。始業時空き物理RAM 12,405,144 KiB（約11.83GiB）。新規REA/Ghidra/ゲーム/Work 0回。
原本ZIP/EXE/SAVE、MASTER、QUEUE、PROGRESS、既存RUN、他owner、Git、公開先、スケジュール変更0。
次: `0x005D2FC9` 第二呼出元と `0x005CA4E5` のconsole/Unicode partial-writeカウントを独立検証。