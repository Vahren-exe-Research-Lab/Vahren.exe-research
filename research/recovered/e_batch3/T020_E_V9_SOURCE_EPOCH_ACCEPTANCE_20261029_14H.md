# 研究E｜V9解析索引への正式切替に伴うT019/T020 source-epochゲート（2026-10-29 14H）
ID: E-AUDIT-20261029-14H-T019-T020-V9-CANONICAL-PROVENANCE-GATE-01
Owner E/T019,T020; STATIC / BYTE VERIFIED / SYNTHETIC TESTED / VERIFY / NOT READY.

## 新規確認した出典条件（PC LOCAL、実バイトをread-only照合）
- 2026-10-29更新の rea_lab/headless_analysis/00_START_HERE_ACTIVE_RESEARCH.md と同ディレクトリ CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json は、ユーザー指定の統合V9を現行と記す。従来V3の使用指定は旧情報。
- 現行V9 DB: search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite、141033472 byte、実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
- 現行V9 CLI: search_index/search_unified_v9_20261023.py、実SHA256 6B3333571CD3E2E97BB6E6DBFD85D751EA869903998C93E49E70FB3461547896。
- 上記2SHAは原出典UNIFIED_V9_INTEGRITY_20261023.jsonの登録値と一致。利用者選択CURRENT_ACTIVEポインタのDB_SHAとも一致。
- read-onlyのCLI statsは関数11950（内部11762/外部188）、Ghidra refs243678、native E8 CALL 44890、E9/EB JMP 6324、合計native索引51214、unresolved control5145と報告した。
- 2026-10-23版V9案内とCLI stats内の『PC default remains V3』は当時の記載で、2026-10-29更新の明示ポインタとは記載時点が異なる。全種のショートカット/GUIがV9へ切替済みとまでは断定しない。
- 旧検索先の search_index/README.md、BUILD_MANIFEST.json は現在その位置に存在しない（ENOENT）。既知過去ソースSHAや関数対応を消去せず、今後の新規静的証拠は現行V9 DB/CLIのSHAとEXE SHAを別個にpinする。
- 原作EXE識別SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 は両V9 metadataに記載。今回はEXEの現物を再ハッシュしていない。
- E8 CALL 44890 と古い直接CALL 47550は索引世代・集計方法が異なるため差分数を欠損や修復率としない。間接callや原作実Gameplayを確定しない。

## T018/T019/T020 受入とテスト
- G0通常UI戦闘開始、G1同一戦闘の直前未改変SAVE/input、G2実MAP/攻防援軍3side/順序付き出撃Unit/Troop、G3終端、G4復帰後World差分は引き続き同一runの一次receipt未充足。
- 13H発見の2watch同じREADY IDだが異なるtrace SHA/戦闘時間窓を引き続き区別。V9索引昇格・関数数増加・過去RAW8はG0-G2の原作Golden資格を補わない。
- T019原作確定矛盾新規0。GameClear DAT13/TXT2検索範囲差はsource-scope RESOLVED、script2同名勝者/phase flag/TXT runtime読込/gwrite復帰/decide11用途はVERIFY。
- 新規 tests/t020_e_v9_source_epoch_gate_20261029_14H.py に実SHA/登録manifest/ポインタ/件数の正例・旧V3や改変SHA/EXEの負例を実装。python -Bで10/10 PASS、FAIL0。これはsource selection保護でありGolden互換検査でない。
- 原作DYNAMIC OBSERVED 0 / actual Gameplay Golden PASS 0 / strict MATCH 0。新規正式READY ID 0、checkpoint196・READY596=A115/B229/C136/D116（既確認値）、34Task DONE9/IN_PROGRESS21/VERIFY4（旧値、再集計なし）。

## 安全・所有権・再開
- 旧T018表境界、E session-join拒否、T019 XREF、C T026/T032、D T030 TSV、禁止VA0x5710C0、10/28 13H安全拒否14件は各BLOCKED。別tool/path/shell/Remote/ZIP経由の再試行なし。今回安全拒否0。
- 旧OFFLINE-UNSYNCED/意味的重複全照合は未完。B 14H T013はVERIFY/NOT READY、E代理統合なし。原本EXE/DAT/SAVE/ZIP、他owner、REA、dev_lab、Git/Work/設定/スケジュール変更0。
- 保存対象は本E-owned資料と新E-owned検証コードのみ。追加原作テスト/新Ghidra解析なし。次は合法G0/G1/G2同一戦闘一次receiptを探索し、別runの資料混同を避ける。新規VA照合はV9のSOURCE SHA/EXE SHAとCALL vs JMPを区別する。
