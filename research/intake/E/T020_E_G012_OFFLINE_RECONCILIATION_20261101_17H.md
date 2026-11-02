> Archived E-owned original research report; sanitized PRIVATE intake, not byte-identical. Original PC `tests/T020_E_G012_OFFLINE_RECONCILIATION_20261101_17H.md` remeasured SHA-256 `F3014188EC9729B8786569CC1CD8A03585E601C46B3A14F9B594976E4A9637CA` at 2026-11-02 JST. STATIC/SYNTHETIC/VERIFY as the historic report states; **new native run 0, Golden PASS 0, strict MATCH 0, new READY 0, NOT_CURATED**. 39 historical offline-source file receipts and their old test counts are provenance metadata only: raw offline bundles are **not** mirrored here and cannot substitute for G0–G2.

# 研究E｜C-NB02 G0-G2旧証拠と11/1オフライン差分のPC復帰照合（2026-11-01 17H JST）
研究ID: E-PC-20261101-17H-T018-T019-T020-G012-SOURCE-LINK-RECONCILIATION-01
owner: E / T018,T019,T020。区分: PC LOCAL / STATIC SOURCE BYTE VERIFIED / VERIFY / NOT READY。新規VA/CALL: なし（既存出典の照合）。
## 参照と正本
- MASTER_LEDGER.md 4642行 SHA256 E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3。最後の正式checkpoint 196 / READY596=A115,B229,C136,D116。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧値（今回全件再判定なし）。
- evidence/ANALYSIS_LANES_PROTOCOL.md、A～D HANDOFF（Bに11/1 17Hの旧オフライン研究10件のNOT READY復元あり）、rea_lab/decomp_task/PROGRESS.mdおよび保存RUN、dev_lab/docs/IMPLEMENTATION_PLAN.md、E所有tests/T018_GOLDEN_CORPUS.md、wiki/T019_CONTRADICTIONS.md、既存tests/T020_E_NATIVE_CNB02_JOIN_PREFLIGHT_20261029_09H.mdをread-only確認。
- PC T018 1669行 SHA256 CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120。11/1 16HオフラインZIPからの旧T018照合報告と完全一致。PC T019 SHA256 102AFAB94359902D5E74E4B8C55D06CD46269B85DB1B7D0A426FCDE2ED6FC25B。
- PC既存T020 10/29 join資料 SHA256 EC23B00CD61DE2EEF28C15593E370EA224B36083CA4B508EFF0511C7260CE331。16H提案の観測不足22欄/候補11欄は旧T018の10/15合法受入票・10/17手動票と重複再審査が必要。新規11欄の全てを独立新発見として計数しない。
## 原作一次証拠の境界
- rea_lab/headless_analysis/search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json 実SHA256 87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C。2026-10-21 UTC14:31:37～14:33:35 の原作PID23272/旧mode2→mode1は限定原作実行構造の証拠。gate_status PASSは攻撃Spot/対象Spotのnative実ID、完全戦闘packet、Eの同一run G0合法画面証拠を証明しない（いずれもfalse/不足）。
- WATCH1 READY.json 実SHA256 0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C、WATCH2 READY.json 実SHA256 936FBBA2961A46128CD4D4DFD4E93134A8663B127E1625A3C3F721ACD4ABC71B。双方のnative_gameplay_G0_confirmed=false / G1_complete=false。単一PIDでも14:31と15:14は別戦闘時間窓。ARMED/READYというファイル名をEのGolden READYへ変換しない。
- G0: 未改変原作の合法UIでsci1/po2/sp2→sp16を選択した同一戦闘の実画面・開始時刻・一意run/battle識別が必須。G1: その戦闘直前SAVEの実bytes/SHAおよび操作押下/解放と入力SHA・時間順が必要。G2: 実選択MAP bytes/SHA・攻守支援3陣営・順序付き出撃Troop/Unit/位置の実観測が必要。s16.mapとsave1/2の保存Spot数はSTATIC候補でありactual実戦名簿ではない。
- 実ゲームE DYNAMIC OBSERVED=0 / actual Golden PASS=0 / new-old strict MATCH=0。T020原作者変更5系列6条件NOT RUN。旧観測が原子的に結合できなければVERIFY/NOT RUN/INELIGIBLE、合成PASSから昇格させない。
## V9・T019・未同期
- PC search_index/CURRENT_ACTIVE_RESEARCH_STATE_LATEST.jsonと00_START_HERE_ACTIVE_RESEARCH.mdは10/29現在V9指定。V9 SQLite予定SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（この回DB全バイト再計算なし）。旧MASTER末尾のV3現行説明は2026-10-22時点の履歴記述であり、現在のV9指定に優先しない。GitHub非公開KB developのGHIDRA_V9_COVERAGE_REPORT.md/KNOWLEDGE_CURATION_PROTOCOL.mdをread-only参照。
- T019 GameClear DAT13/TXT2の字句source範囲差は既存RESOLVED。script2の同名勝者、phase flag、TXT runtime読込、gwrite後続はVERIFY。新規確定矛盾0、原作BUG確定0。
- 以前の拒否済み操作・資料・保護範囲は SAFETY_HOLD として維持。内容取得・再試行・迂回は行わない。
- KB_CANDIDATE: 同一研究ID / E/T018,T019,T020 / 出典・source SHAは上記 / STATIC=原文/manifest/既存受入の読取、VERIFY=同一runのG0/G1/G2と比較適格性 / Golden0 / READY0。専任curatorへ候補のみ、knowledge・Gitの改変なし。
## 保存と再開
- 以前の拒否済み操作・資料・保護範囲は SAFETY_HOLD として維持。内容取得・再試行・迂回は行わない。
- 次回は独立run G0→G1→G2の合法一次receiptを優先。OFFLINE39ファイルは同SHA/旧E T018/10-29 T020との意味重複・owner・未完了・安全境界を確認した後にのみ許可E資料へ一度だけ取り込み、readbackし、正式READYには動的証拠を要求する。