# READBACK PASS / REA-LOCAL-20261024-06H-P0-F9E0-SOURCE-ABI-STATIC-01
2026-10-24 06時台 JST / REA owner / STATIC / VERIFY / NOT READY
- REA_20261024_06H_P0_F9E0_SOURCE_ABI_STATIC.md: 5514 bytes / SHA256 946CC0AC3BB7BCE6D62B91AC91F6FE36E48D9C8DF0A4E8F111E5610E3FCB6DCA
- REA_20261024_06H_P0_F9E0_SOURCE_ABI_EVIDENCE.json: 3854 bytes / SHA256 79107E1B43CE877B59B7541FAEA89395599A47E8CAF329C3C32B84C691770C24
- REA_20261024_06H_RANGE_OWNER_AUDIT.py: 3215 bytes / SHA256 16E68E4C3EAA12F5874218205CADB3FE2FD0D907D30FED1363939FD75FEB3090
- 別PowerShellプロセスで3成果物をread-only取得し各SHA256を再計算。JSON構文・研究IDとMarkdown ID一致・callers=5・Python SHA一致を確認。
- 独立した後続PythonプロセスでターゲットPE SHA、search.sqlite SHA、実バイト35/35、直接E8の転送先11/11を再照合し全PASS。ゲーム/REA/Ghidraは実行していない。
- 旧Wave1-5=64/64 VERIFIEDは保存済み同期ログの参照値。今回新規VERIFIED0、REAの新規5種証拠完成0、正式TODO/VERIFY/BLOCKED差分0/0/0。
- 原作ゲームGolden PASS0、strict MATCH0、完全複製率未測定。CPU負荷不明、調査全体の所要時間未計測。
- エラー: Markdown最初の書込を組み立てるJavaScriptにSyntaxError。該当ツール呼出前に修正し、後続の書込/readbackが成功。安全拒否なし、既存成果破損なし。
- 保持した未確認点: 各callerの第2引数コンテナの非空保証、F720フィルタを通過する候補の存在、NULL実機発生、出力コンテナとの別名・オブジェクト寿命。
- 原本・MASTER・他owner・既存run・QUEUE・PROGRESS・Git・スケジュールは不変更。
- 次の関数: 0x4751C0/0x47D770の入力コンテナ構築と0x48F720の絞込条件。正式統合はowner Eへ別途。
