# REA 2026-10-26 18時台｜独立保存・読み戻し
研究ID: REA-LOCAL-20261026-18H-P0-CRT-SEH-ORPHAN-E8-XREF-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY
PC: SAITO / Local Compact 接続成功。作業観測JST 18:32〜18:42。
原作SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
現行V3検索DB SHA256: 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25

## 保存結果・独立読戻し
- REA_20261026_18H_P0_CRT_ORPHAN_E8_AUDIT.py SHA256 7DBF87EE4A574CFA0939212670BA74B24E5267D1D562795E5602C56504E5FB16
- REA_20261026_18H_P0_CRT_ORPHAN_E8_EVIDENCE.json SHA256 2CCEF122498AE5B067202B6D2AE24B49266787915CFB0A9A1BE9638F8B2E49CD
- REA_20261026_18H_P0_CRT_ORPHAN_E8_STATIC.md SHA256 434A0A6EF681794D3F2D1293896F6693D7EC7F19AD715DB15E0A37B2025212B6
- 独立PowerShellプロセスで監査スクリプトを再実行: 20/20 PASS、0.9159秒、INDEPENDENT_READBACK_PASS。
- PowerShell ConvertFrom-Jsonで証拠JSONの研究ID、20/20、未索引E8三件、Golden=0を独立読戻し。上記3ファイルのSHA256を再計算。
- V3 guard: PASS_ACTIVE_V3_STATIC、guard対象14ファイル一致、E8索引44889・JMP索引6324を確認。
- 旧REAの2026-10-11保存同期ログ64/64維持。今回の正式VERIFIED増分0、公式TODO/VERIFY/BLOCKED書込差分0/0/0。Golden実測PASS0。

## 安全・実行環境
開始時メモリ空き13.62GiB、18:38時点のCPU全体単発負荷9%、研究全体の厳密な所要時間は未測定。新規REA/Ghidra/旧ゲーム起動0回、Work0回。
active.lockは開始・終了とも存在しない。PC書込はREA所有の新規監査・証拠・報告・このreadbackのみ。その他の原本、他レーン、MASTER、QUEUE、PROGRESS、Ghidra検索正本、既存runs、Git、スケジュールを変更していない。旧OFFLINE-UNSYNCEDは未同期。
安全拒否0。調査中の通常エラーは (1) stdin経由の日本語パス文字化けでWinError123（ASCIIの限定的なパス発見に変更）、(2) V3 CLIではrelated非対応（callers/calleesへ切替）、(3) SQLカラム名誤指定（実schemaを読み直し）、(4) 報告書JSのバッククォート構文エラー（書込前に修正）。いずれも安全拒否ではなく、原本変更なし。
旧FLS/Wave6/禁止VA/REAエクスポート等の拒否済み操作は再試行せず、迂回していない。

## 再開位置
次のP0候補: 0x004BE480のDirectMusic管理配列+0x70について、初期化途中の例外時に後始末する全ownerを限定照合。今回の未索引サイト 0x005B8612/2A/2F はV3検索DBへの修正依頼候補として独立保全し、現行DBやGhidraをこのタスクでは修正しない。
