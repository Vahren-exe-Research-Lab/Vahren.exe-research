> E owner 01H historic report. Original `tests/T020_E23_TYPED_PROJECTION_JSON_CONFORMANCE_AUDIT_20261029_01H.md`, verified PC SHA-256 `3B7F2E63FB67BDCE349E8BB4C92FF723EDBAC935C93A961C08066D5F453674B0`, 2026-11-02 JST. Safety-sanitized, not byte-identical; prior synthetic test totals are *not rerun now*, original-game Golden PASS 0, strict MATCH 0, new READY 0, NOT_CURATED.

# 迫真戦記 新E｜E23投影の型一致・非標準JSON境界（2026-10-29 01H）
研究ID: E-AUDIT-20261029-01H-T018-T020-TYPED-PROJECTION-JSON-CONFORMANCE-01
分類: PC LOCAL / STATIC CODE CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作ゲーム実行なし。

## 入力・所有権
- E-owned tests/t020_e23_source_projection_binding_gate_20261029_00H.py（継続基盤、read-only）。
- E-owned tests/t020_e21_source_attestation_gate_20261028_23H.py と tests/T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json（旧合成receipt、read-only）。
- E-owned tests/t020_cnb02_g2_cross_generation_parity_guard_20261026_10H.py（G2診断のみ、read-only）。
- evidence/ANALYSIS_LANES_PROTOCOL.md、A-D HANDOFF、rea_lab/decomp_task/PROGRESS.md、dev_lab/docs/IMPLEMENTATION_PLAN.md、tests/T018_GOLDEN_CORPUS.md、wiki/T019_CONTRADICTIONS.md（参照のみ）。
- 旧E21実bytesは今回はWindows PCへ未同期。2026-10-21 EXE manifest SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187を継承（現物再ハッシュなし）。

## 独立した新規欠陥・改善
- 00Hのbind()はPython dict/listの通常 == 比較を利用する。Pythonでは False == 0、True == 1、1 == 1.0 が成立し、元source byte/SHAが不変でも投影receiptのネストした型変更が一致扱いになり得る。
- 合成実例: receipt.native_receipt_verified=False→整数0、deployed[0].order=整数0→False に変更しても、旧bindは SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE を返した。
- 新しいstrict_bindは先に旧source SHA/research ID/schema/run linkage検査を通した上で、辞書/配列/値に対する再帰的・型同一比較を行う。上述の型混入を SOURCE_TO_RECEIPT_TYPED_MISMATCH として拒否する。
- 旧source JSON decoderはPython標準の既定動作により NaN / Infinity / -Infinity を許す。sourceの未使用属性にNaNを付けても旧projectionは成功した。新gateではparse_constantで非標準JSON数値を拒否。
- 合成G2の最低限の型契約（map_sha 64桁hex、side role/id文字列、出撃order/x/yが正確に整数、Unit/Troop/side_idが非空文字列）もソース側で確認する。
- 前記は「合成bytes→抽出receipt整合性」の拡張だけであり、原作MAP/三陣営/出撃Unit真正性、old gameplayやstrict一致を証明しない。E21/22のdefend/defense alias、実defense roster不在、実map_id/active window欠落は従来VERIFY。

## 検証・根拠
- 今回新規 tests/t020_e23_typed_projection_gate_20261029_01H.py 28/28 PASS（Local Windows Python -B unittest）。
- Previously refused or protected sources are SAFETY_HOLD; not accessed or retransmitted.
- 合成specimenのみで負例を再現。旧E21 rawをPC再ハッシュした、旧原作を起動した、T018既存runnerへ正式結線した、という主張はしない。
- T018 G0=通常UI合法開戦、G1=同一run直前未改変SAVE+入力証跡、G2=実MAP ID/bytes・三陣営とordered Unit/Troop及びactive windowの独立一次証拠。G3戦闘結果/G4 World差分も未取得。DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
- T019新規確定原作矛盾0。GameClear DAT13+TXT2字句scope差RESOLVED、script2優先/phase flag/TXT実読込/gwrite復帰/decide11用途VERIFYを継承。

## 統合境界・安全・再開
- 旧確認checkpoint196 / READY596=A115 B229 C136 D116、34Task DONE9/IN_PROGRESS21/VERIFY4 は2026-10-28 12時台の既知値（最新全件再集計NOT RUN）。01H B新成果B-20261029-0113-T028-RESULT-18CALLER-INDEX3-NULL-SINK-01はB HANDOFFでSTATIC/VERIFY/NOT READY。E代理READY0。
- Previously refused or protected sources are SAFETY_HOLD; not accessed or retransmitted.
- 10/25以降OFFLINE-UNSYNCED全件の同ID/owner/合意/READY/競合照合は未完了。MASTER正式統合0、最新checkpoint未更新。新規E専用script/report/receipt以外の既存資料を変更しない。
- NEXT: E21のソース実bytesを許可された正規経路でWindows側へ確認可能になった場合のみ strict_bindで投影を再照合（合成証拠ゆえGolden昇格なし）。C-NB02の合法旧原作G0/G1/G2一次観測と既存T018 runnerの非破壊的接続が最優先。
