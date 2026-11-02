# E/T018・T020｜10月25～27日研究資料のPC現物SHA台帳・Golden受入境界
研究ID: E-AUDIT-20261029-05H-T020-PC-SOURCE-INVENTORY-01
Owner E。2026-10-29 05時台 JST。状態 PC LOCAL / STATIC BYTE INVENTORY / VERIFY / NOT READY。
## 一次出典・限定範囲
- Windows `_REDEV_RESEARCH/tests/` の直下のみ。E所有候補 T018_/T020_/t020_ かつファイル名に20261025・20261026・20261027の日付を含む現物をread-only取得。
- 正本 `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、A～D HANDOFF、REA `rea_lab/decomp_task/PROGRESS.md`、DEV計画、T018、T019をread-only参照。
- ChatGPT Library `/迫真戦記/E_OFFLINE_UNSYNCED` の83件をメタデータ確認。日付付き20261025～27は0件、20261028は23件、20261024は57件、日付不明3件。
## 新成果：10/25～27に保存されたE資料のbyte inventory
- E/T018・T020日付名ファイルは133件：20261025=33、20261026=46、20261027=54。各現物のバイト数とSHA256を記録。
- 133件内のJSONはすべて正常にparseできた（構文異常0）。これは資料内容の真偽・本来存在すべき資料の網羅性は保証しない。
- PC一次bytes台帳 `tests/T020_E_PC_20261025_27_BYTE_INVENTORY_20261029_05H.json`、30,274B、SHA256=29DF7E435A3C63C0A33F7A2F38D83C2EA604E1791F669BAED5A38CF8BDC0DFE1。新規専用Pythonで生成・readback同bytes確認。
- 再実行可能スクリプト `tests/t020_e_20261025_27_inventory_20261029_05H.py` はE所有・軽量・旧原作/gameplay/Ghidra実行無し。既存台帳が違えば書換せず停止。
## 前回21時台Library原本保全の再検証
- 2026-10-28のLibrary source manifest23件を現存stagingと再ハッシュ：同名22/23一致、残1件は `T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json` の短縮不完全コピー。
- 同1件のLibrary実原本は別名 `T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149_LIBPIN_7D574F25.json` にあり、SHA256=7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA一致。
- 同名の短縮コピーをT018比較runnerに渡さない。別名原本も内容・出典・owner・現行runner schema照合まで正式採用しない。
## 判定・復旧境界
- 13時台の14合成ケースはPC保存済みだが旧安全拒否に従ってNOT RUN。今回対象は研究資料のハッシュ/JSON解析であり拒否された14ケースの再実行・代替試行ではない。
- T018 G0旧合法UI開戦、G1同run未改変SAVE+入力、G2 MAP現物/三陣営/ordered Unit/Troop、G3結果、G4World差分の一次証拠は未充足。DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2 scope RESOLVED、script2優先順位・phase/TXT実load・gwrite・decide11用途VERIFY（継承値）。
- 新規READY正式統合0、MASTER旧cp196/READY596(A115/B229/C136/D116)、34 Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値で今回全件再集計NOT RUN。
- BLOCKED: 旧T018表境界、T019拒否済XREF、C T026/T032、D T030 TSV、0x5710C0、10/28 13H拒否2件。今回新安全拒否0・迂回0。
- OFFLINE-UNSYNCED全期間や日時を名前に含めない資料、過去拒否による未保存本文まで網羅したとは主張しない。
- 次: 133件の根拠リストを現行E runner入力に突き合わせ、Source Hash・owner・誤コピーを検査して非破壊的な受入条件を作る。旧原作一次証拠の取得は最優先。

## 保存済台帳に対する独立回帰
- `tests/t020_e_archive_inventory_regression_20261029_05H.py` を新設。Python -B unittest 実行5/5 PASS、失敗0（0.037秒）。
- 検証範囲: 133ファイルの件数・日付内訳・一意性、全133件のbyte長/SHA256再計算、対象JSON構文、21H LIBPINの36ケース/原本SHA、短縮同名コピーの不一致とJSON不正。
- 新規原作実機試験0、過去安全拒否13Hの14ケース試験0。新規READY正式統合0、未同期の正式解決認定0。
