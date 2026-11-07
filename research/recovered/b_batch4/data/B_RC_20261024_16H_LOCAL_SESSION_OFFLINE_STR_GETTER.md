# B復旧記録｜2026-10-24 16時台

- **RECOVERY-ID**: `B-RC-20261024-16H-LOCAL-SESSION-01`
- **関連研究ID**: `B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01`
- **対象/Owner**: B／T012、Skill strのABIとScriptData親探索
- **最初の試行**: Desktop Commander Local Compact `read_multiple_files` によるPCの `MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、`LANE_B_HANDOFF.md` 取得
- **実エラー**: `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`
- **分類**: CONNECTION。新規SAFETY_REFUSAL 0件。旧拒否対象の新規解析・経路変更による再試行なし。
- **結果**: PC正本を参照できず、現行checkpoint/予約/重複/READY、未同期回収22ファイル対後続10研究のID対応、既拒否・部分JSON案件を確認できない。PC書込/readbackは0。正式READY/MASTER統合/Golden PASS/strict MATCHは0。
- **代替証拠**: Libraryの`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34/34 CRC）、原作Vahren.exe（SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）。原本は実行・変更せず。SQLite read-only quick_check=ok。
- **オフライン増分**: `0x59CCC6`の`str` raw bytes/引数/出力`+0x20`の原作ASMによるクロス確認、`0x464B46..0x464B49`の `super` 最大50検索境界。旧成果（既知のstrパーサ・コピー・ratio）を再計上しない。
- **未保存/未同期**: PC B資料・`LANE_B_HANDOFF.md` への反映なし。Library側の成果保全はこの記録の後続アップロード成否で別管理。PC復帰時に既存ID・owner・拒否・重複・READYを照合してB所有資料だけへ一度取り込む。
- **次の許可された一手**: PC復帰時に旧安全拒否と未同期索引から確認し、本研究を差分照合。独立研究は非拒否領域に限定し、`0x00464290`の存在判定、合法DATに50階層が存在するか、実機Golden条件を静的に整理する。
- **不変更**: 原本EXE/DAT/SAVE/ZIP、Git、MASTER、他lane、REA/dev_lab、Work、設定、スケジュール。
