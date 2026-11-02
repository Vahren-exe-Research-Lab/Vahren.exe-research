> E-owner archived 00H study; original PC `tests/T020_E23_SOURCE_PROJECTION_BINDING_AUDIT_20261029_00H.md`, SHA-256 `13C682425FC7115899C7B0D1E5F1B480B3248F1CDBFE34FFAE147F92915BB9C0` measured 2026-11-02 JST. This report is safety-sanitized, *not* raw-byte-identical. Historical synthetic tests were **not rerun this pass**; original-game Golden PASS 0, strict MATCH 0, newly accepted READY 0, NOT_CURATED.

# E T018/T020｜E23 source byte pin と E22 投影receipt の結合監査（2026-10-29 00H）
研究ID: E-AUDIT-20261029-00H-T018-T020-E23-SOURCE-PROJECTION-BINDING-01
状態: PC LOCAL / STATIC + SYNTHETIC EXECUTED / VERIFY / NOT READY。原作ゲーム未実行。
## 入力・出典・差分
- E22 PC fixture: tests/T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json, SHA256 F2E509FE99AA91A9466FA40533B392B61AEBB0B34DBE582699AB2586D34DFCE7。
- E23 PC gate: tests/t020_e21_source_attestation_gate_20261028_23H.py, SHA256 EF4A7767688E633A189632CEEDF1224D41C37865A75F17B01A9FF40E87AFE83B。
- E21元 fixture: 会話添付 E_20261028_2149/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json。ChatGPT container実bytes SHA256 7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA。
- 同E21 base.g2から {map_sha,sides,deployed} と run_id/base.capture_source/base.native_receipt_verified を選択した正規JSON SHA256 = 47DBFC9455DD9FC478B02F498A17848458EA610BD246494C0E21A38B303A58B1。これはChatGPT containerで計算した投影digestでありWindows上でE21全bytesを独立再照合したものではない。
- PC側E22 captureの正規JSON SHA256も上記と一致（新規 test_02）。この確認はE21→E22の選択フィールドの値を強化するが、G0/G1証拠や原作真正性ではない。
## 新たに確認した受入欠陥
- E23のsource_pin(expected,raw)は元artifact bytesのSHA一致を判定するが、audit(receipt,raw)のreceipt内容とrawを結び付ける判定は存在しない。
- 合成元bytesが同じでも、受け渡すreceipt.g2.deployed[0].unitを別の有効文字列へ書換えた場合、旧auditは両者とも source_attestation='SYNTHETIC_ARTIFACT_BYTE_IDENTITY_ONLY' を返す（test_04で再現）。旧auditはstrict MATCHを認めないため誤Golden化バグの直接証明ではなく、「source pinをreceipt同一性と誤用できる」診断上の隙。
- 新E専用gateはexpected SHA→生bytes JSON→research ID/schema/capture class→G0/G1/G2 run ID一致→厳密projected receiptを再構築し、投影と受領したE22 receiptを完全比較する。
- 別Unit・MAP digest・side ID・run_id・余剰field、source bytes欠落、SHA不一致、研究ID違い、schema違い、G0/G2 run不一致、JSON重複キーなどは適切な拒否結果へ分岐する。成功時も SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE のみ。
## 実施したテスト
- 新規 tests/t020_e23_source_projection_binding_gate_20261029_00H.py: 20/20 PASS。
- 同PCでE23先行20件とE22先行24件を合わせて再実行: 今回64/64 PASS（この64件に新規20件を含む）。既存試験は新規成果として二重計上しない。
- 新規コード PC SHA256 6557F0F57BD782EBA4C342D1ADBFF88F4EFFAA22738DB325CDBE171B2D246709。原作EXE新規ハッシュなし。Ghidra再実行・ゲーム実機観測なし。
## Golden・T019・MASTER・安全
- G0合法旧UI起動、G1同一戦闘直前未改変SAVE/input、G2実MAP bytes/ID・三陣営・ordered Unit/Troopを別々の一次receiptで満たす必要。現E21/E22の合成2者だけでは不適格。G3結果/G4 World差分も未採取。
- DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。T019新規確定原作矛盾0。GameClear DAT13+TXT2範囲差RESOLVED、script2/phase flag/TXT runtime/gwrite/decide11 VERIFY継承。
- Prior safety refusal / protected evidence remain SAFETY_HOLD; no retry or workaround.
- B 2026-10-29 00H 最新HANDOFF B-20261029-0015-T028-FIVE-ELEMENT-RECORD-PRODUCER-CORRECTION-01 は STATIC/VERIFY/NOT READY、E代理統合なし。
- Prior safety refusal / protected evidence remain SAFETY_HOLD; no retry or workaround.
- 10/25以降 OFFLINE-UNSYNCED成果はPC正本との同ID/owner/READY/重複/競合の完全照合未完了。E21源ファイルをWindowsへ正式同期・MASTER統合していない。T018/T019既存資料、他owner、REA、dev_lab、原本/Git/Work/設定/スケジュール変更なし。
## 再開
- E21元生bytesを正式参照可能な経路で取得し、PC上でexpected SHAと投影の再計算が成立した場合だけ本gateでE22とのバイト由来一致を正式照合（合成なのでGolden昇格なし）。
- Prior safety refusal / protected evidence remain SAFETY_HOLD; no retry or workaround.