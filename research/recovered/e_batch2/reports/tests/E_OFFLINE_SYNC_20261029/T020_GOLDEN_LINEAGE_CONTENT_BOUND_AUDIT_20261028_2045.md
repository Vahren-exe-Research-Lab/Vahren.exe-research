# 迫真戦記 新E｜T018/T020 Golden受入証拠の実バイト結合・順序ゲート監査

- ID: `E-OFFLINE-20261028-2045-T018-T020-GOLDEN-LINEAGE-CONTENT-BOUND-01`
- 時点: 2026-10-28 20:45 JST。所有者 E（T018/T019/T020 のみ）。
- 結果分類: `OFFLINE-UNSYNCED / STATIC-OLD-INDEX / SYNTHETIC EXECUTED / VERIFY / NOT READY / NATIVE NOT RUN`。
- 今回の成果: 19時台T018合成Golden `schema_ready` が、**実データとSHAの不一致や型不正でも形式上trueを返す24ケース**を作成し、既存ファイルを編集せず、追加の独立T020ゲートで24/24を拒否することを確認。

## 入手経路と根拠の限定

- 開始時に Desktop Commander Local Compact `read_multiple_files` で最新PC MASTER/規約/検索索引READMEの読取を試みたが、`MCP SSE probe returned 429 from openai.org`。`CONNECTION/RATE_LIMIT`であり、安全拒否ではない。復旧ID `E-RC-20261028-2045-LOCAL-SSE-429-01`。PC通電・最新owner・正本更新状況は未確認。
- 正規のLibraryの実ファイル `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` (`file_000000006ad08209a897b82c4ebf281a`) を新規materializeし、原本非改変の派生コピーから検索SQLiteと10月21日規約を読取。
- ZIP実測SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、SQLite実測SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。SQLite `PRAGMA quick_check=ok`。検索DB接続は `mode=ro&immutable=1` + `PRAGMA query_only=ON`。
- 原作EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は旧マニフェストの**記録値**、現物EXEの本回ハッシュではない。原作ゲームやGhidra/Javaは起動せず。
- 既存のE19:49 `t020_dialog_wrapper_fingerprint_golden_lineage_gate_20261028_1949.py` とJSON fixtureの実ファイルを監査。旧コードは変更していない。

## 今回独立して証明したT018合成ゲートの穴

19:49の`s​​chema_ready`相当ロジックは、同一run/scenario/EXE/DAT SHAの書式、capture_shaの64桁形式、時刻順序、MAP/SAVE/入力SHA形式、三陣営、配備名簿連続性を検証する。これは当時の**合成schema readiness**として妥当だが、次の穴が残る。

1. `digest()`は64桁HEX形式のみの検査。**G0/G1/G2 capture、SAVE、入力、MAPの生バイトからSHAを再計算しない。** 同一runと形式だけ満たして実バイトを変更しても、旧ゲートはtrueになり得る。
2. `isinstance(True,int)`はPythonでtrue。**x/y座標やorderにboolを混入できる。**
3. `g1['at'] <= g0['at'] <= g2['at']` は型・時刻形式を指定せず、**辞書式文字列・負の数・浮動小数でも通過**する。実観測で時計粒度が粗いことを想定して、同一時刻自体は新ゲートでも禁止せず、別の単調増加event_seqを必須にした。
4. `run_id/scenario/side_id/troop/unit` の空白だけの文字列が通る。証拠同一性として有効とは扱えない。
5. `run_id`一致だけでは、**異なるファイルを混入させることを防ぐ親receiptハッシュの連鎖**がない。

これらは**新戦闘エンジンや原作のバグではなく、E所有の合成fixture受入ロジックのfalse-positive要因**。`actual_golden()`は旧版でも常にfalseなので、actual Golden誤計上は発生していない。T019確定矛盾には追加しない。

## T020新規の対策とテスト

- `T020_GOLDEN_LINEAGE_CONTENT_BOUND_CASES_20261028_2045.json`（合成fixture 30ケース：旧ゲートtrue/新ゲートfalse **24件**、旧ゲートもfalse **3件**、両ゲートtrue **3件**）。
- `t020_golden_lineage_content_bound_gate_20261028_2045.py`（旧コード実物を読み込み検証する独立ゲート）。
- 追加条件: `capture_b64/save_b64/input_b64/map_b64`をstrict base64復号してSHA256再計算、`G1.capture_sha→G0.previous_capture_sha→G2.previous_capture_sha`の明示的な結合、非空白ID、時刻・event_seqの厳密intと非負条件、event_seqの単調増加、座標と順序の厳密int判定。
- ただし、リンクとハッシュが合っても**合成データの内容・真正性しか確認しない**。第三者が一式を捏造できる。原作の合法UIでの観測、原作EXE/DAT現物との対応、native provenanceによる実Golden認定はこの独立ゲートでは行えない。マップ座標範囲やゲーム固有のUnit/Troop同一性も未確定のため仮定しない。
- 新規ユニットテスト **36/36 PASS**（30個別case + 旧ソース/fixture SHA + SQLite SHA/quick_check + 合成正例 + native=0境界）。
- 旧E 16:45 **28/28 PASS**、17:45 **46/46 PASS**、18:49 **36/36 PASS**、19:49 **58/58 PASS** を同一旧DBで再実行。総実行 **204/204 PASS**。13時台の安全拒否による未実行14ケースは除外。
- テストの成功は `STATIC INDEX + SYNTHETIC EXECUTED` のみ。原作実機動作・Golden comparision/strict MATCHは **NOT RUN**。

## T018 Golden と T019

- G0: 旧合法UIによる実際の戦闘開始。G1: **同一戦闘**の直前SAVE生バイト・実行環境・入力記録。G2: **同一戦闘**の原作MAP生バイト・攻防支援三陣営・ordered出撃Troop/Unitと配置。G3: 戦闘結果、G4: World差分。まだ原作合法一次観測はない。
- 今回原作 `DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0`。schema-only PASSはこれらへ加算しない。
- T019今回の新規確定矛盾 **0件**。既存GameClear DAT13/TXT2の字句検索範囲差 RESOLVED、`script2`優先順位/phase flag/TXT実読込/`gwrite`復帰 VERIFY、`decide11`用途同一性 VERIFYを**前回値として継承**。最新T019正本未読。

## 正本・拒否・再開位置

- MASTER PC最新版は **未読**。最終既知（2026-10-28 12時台までの旧確認値） `checkpoint196 / READY596 (A115/B229/C136/D116) / Task34 (DONE9, IN_PROGRESS21, VERIFY4, 重複ID0)`。**今回確認した最新値ではない**。今回正式READY統合 **0件、IDなし**。READY全数・owner・合意・他レーン最新と既統合照合不能のためMASTER書込は行わない。
- 13時台拒否 `E-RC-20261028-1353-READONLY-PS-SAFETY-01`、`E-RC-20261028-13H-E13-REPORT-APPEND-SAFETY-02` は継続 BLOCKED。旧T018表境界/session-join、T019拒否済みXREF、C T026/T032、D T030 TSV、`0x5710C0`の拒否もBLOCKED。別shell/tool/path/Remote/ZIPで拒否操作を再試行していない。
- 今回429は新規 `CONNECTION/RATE_LIMIT` で `SAFETY_REFUSAL` ではない。Windows正本への書込・読み戻しは**未実施**。既知の10月25日以降OFFLINE-UNSYNCEDの重複・競合照合も未完。
- 次回: 自然復旧したPC接続で**許可された範囲の**最新E資料、owner/READY/既統合/競合/他レーンHANDOFFを独立照合し、未統合かつREADYのもののみ正式統合。拒否済み操作は対象外。T018のG0/G1/G2生バイト証拠を合法旧UIの同一runから収集することが全体最優先。
- 無変更対象: Windows MASTER、他owner A～D/REA、dev_lab、原作EXE/DAT/ZIP/SAVE、Git/push、Work、設定、スケジュール。
