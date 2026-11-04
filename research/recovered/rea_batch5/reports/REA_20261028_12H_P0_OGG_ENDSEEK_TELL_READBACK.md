# REA 2026-10-28 12H｜独立保存・読戻し
研究ID: `REA-LOCAL-20261028-12H-P0-OGG-ENDSEEK-TELL64-STATIC-01`
状態: PC-SAVED / STATIC / VERIFY / NOT READY。
対象は隔離コピーPE32。11H前回48/48および既存Wave1–5の正式64/64を非重複照合。正式VERIFIED追加0、Goldenゲーム実測0、strict MATCH NOT RUN。
初回監査50/50 PASS。証拠JSON保存時50/50 PASS。別PowerShell/Pythonプロセスで独立監査50/50 PASS、failed=[]、exit=0、監査時間約5.154秒（初回は約1.14秒）。
別PowerShellで証拠JSONを再読込しpassed=50/total=50、failed.length=0を確認。
PCで取得したSHA256:
- REA_20261028_12H_P0_OGG_ENDSEEK_TELL_AUDIT.py: 792181B4B250A1F6207DFDA8DDD248EF2973EF61FAF14E7F5DDE7B1B7747A5EA
- REA_20261028_12H_P0_OGG_ENDSEEK_TELL_EVIDENCE.json: 88E4E03933CDA6711E1CA7CA6F17AAA04A9CA57807F26AA7451A65B04A0C5C30
- REA_20261028_12H_P0_OGG_ENDSEEK_TELL_STATIC.md: C045F04343F778DEDF38854D93BF6DD167A79C59F317BE7BECAB65BD4F0EF05E
PC接続成功、active.lock=False、開始時空きRAM約15.59GiB、Java/Ghidraなし、CPU負荷不明。研究全体の実行時間不明。
主発見: 0x005D1310でCALLIND 0x005D136Aはseek(ds,0,SEEK_END)→0x005D1375はtell(ds)。seekの戻り値を直接検査せずtellを呼び、tell32bit結果をCDQで64bitへ符号拡張。tell=-1なら-131で早期復帰。
初期DBは両CALLINDを各1件、V9は各0件（方式差のため欠落断定しない）。双方の直接caller 0x005D1689は1件。両DBのquick_check=ok。
正式TODO/VERIFY/BLOCKED差分0/0/0。5証拠はINDEX_ONLY+TARGETED_PE_NATIVEであり正式5パッケージではない。
操作経過: 最初のread-only一時プローブでPowerShell→Pythonへの日本語フルパスが文字化けしWinError123。許可された同一PCのカレントディレクトリ相対参照で正常解消。安全拒否ではない。原本や他owner、MASTER、QUEUE、PROGRESS、Git、検索DB、スケジュールは未変更。
次回P0: 0x005CEE10のCALLIND 0x005CEE80、64bit offsetのseek callbackへの伝播・異常分岐。Unicode/console __write_nolockは別VERIFY。
