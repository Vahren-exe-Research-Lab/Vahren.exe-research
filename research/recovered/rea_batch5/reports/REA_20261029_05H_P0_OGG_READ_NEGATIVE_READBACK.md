# REA 2026-10-29 05H 独立保存・読み戻し照合
研究ID: `REA-LOCAL-20261029-05H-P0-OGG-NEGATIVE-READ-STATE-STATIC-01`
状態: PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-29 05H JST）。
- Desktop Commander Local接続: 成功。source EXE/DB SHA256一致・DB quick_check=ok。active.lock無し。
- 旧保存RUN・Wave合計: 2026-10-11 progress_sync `64/64 STATIC VERIFIED`維持（新規0）。
- 前回04H研究証拠: 71/71、failed=[]を別途検証。前回研究と問題二重計上無し。
- 今回監査: `REA_20261029_05H_P0_OGG_READ_NEGATIVE_AUDIT.py` 実行 `80/80 PASS`、失敗0、0.508秒。
- PowerShell別プロセスでEVIDENCE.jsonを再parseし `research_id`、80/80、failed=0、Golden=0、newVerified=0確認。
- 独立PowerShell SHA256/size:
  - `REA_20261029_05H_P0_OGG_READ_NEGATIVE_AUDIT.py`: 5450 bytes / `7B7B0D2F33D018BBE929D22DD434DD5CBF0E729F82CBF3A3193CD7BEA708A9EC`
  - `REA_20261029_05H_P0_OGG_READ_NEGATIVE_EVIDENCE.json`: 3758 bytes / `0D96692398DF92B134D1ACD1C45E8B75C66430E9BC2E7ECEED402EFE93531B32`
  - `REA_20261029_05H_P0_OGG_READ_NEGATIVE_STATIC.md`: 7534 bytes / `43E7E6895FED5CEDFA1A17B78479502A2665F0810E0E9CBC0CBD4EC92A39A481`
- 解析資料の対象3関数VA `0x005D12E0`/`0x005CF970`/`0x00501F10` のreport記載を再検査し、すべてTRUE。
- 作業中、新規REA/Ghidra/ゲーム実行なし、原本・他owner・MASTER・QUEUE/PROGRESS・既存RUN・Git・スケジュールの書換なし。10/28 17～22H Library成果はOFFLINE-UNSYNCEDで保留。
- P0再開: `0x005D57C0` return非0の条件、`0x005D1076` 間接CALLとread負値生成条件。別レーンへのREADY配布なし。
- CPU使用率・研究全体実行時間は測定なし。開始時RAM空き約16.44GiB、PCはオンライン。
## QCリカバリー記録
`REA-LOCAL-20261029-05H-QC-POWERSHELL-QUOTING-01`（分類 OTHER / NOT BLOCKED）。対象: read-only SQLiteスキーマ表示の `python -c` 一行コマンド。原因: PowerShellのネスト引用符が崩れ、`entry_va` をコマンド名と誤解釈。DB/EXE/既存資料への書込・未保存差分は0。許可された再開: shell文字列を再利用せず、作成済み所有audit.pyをPythonファイル実行して独立静的参照を行い、80/80 PASSで取得目的を達成。これは接続障害・安全拒否ではない。
