# E/T018・T020｜原本SHA連動の静的資料受入ゲート（2026-10-29 06H JST）
研究ID: E-AUDIT-20261029-06H-T020-SOURCE-PIN-ADMISSION-01
Owner: E/T018/T020、T019参照。状態: PC LOCAL / STATIC SOURCE ATTESTATION / SYNTHETIC EXECUTED / VERIFY / NOT READY。

## 参照と新しい差分
- Desktop Commander Local CompactでMASTER最終末尾、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、rea_lab/decomp_task/PROGRESS.md、dev_lab/docs/IMPLEMENTATION_PLAN.md、E T018/T019、検索索引README/BUILD_MANIFESTをread-only確認。
- 2026-10-29 05H作成のPC E資料133件のbyte inventoryと、04HのLibrary原本23件source manifestが受入候補。新しい解析EXEやGhidraは起動しない。
- 両台帳の実バイト固定: PC manifest SHA256 29DF7E435A3C63C0A33F7A2F38D83C2EA604E1791F669BAED5A38CF8BDC0DFE1、Library manifest SHA256 10AB86C458598FEF0C81AEF2CC7118485950ACC57972D0B5C1B8031E637A37AC（本回PCで直接取得）。
- 新規 tests/t020_e_source_pin_admission_20261029_06H.py は両manifestの原本hash、133/23件数、指定名の唯一性、許可フォルダ限定、実file byte数とSHA256を一致させるE単独の静的検証ツール。
- 21H T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json は、Library pin元から作った別名 LIBPIN_7D574F25.json に明示マッピングする。古い同名短縮コピーを採用しない。
- 判定は SOURCE_PINNED_STATIC_ONLY_NOT_NATIVE のみであり、実旧原作の証拠、実出撃、Golden PASS、READYとは一切別。source manifest自体が信頼できる研究スナップショットかどうかはSHAだけでは保証できない。
## 実行したT020回帰
- 新規Python -B unittest 8/8 PASS、exit0（manifest pin/133・23件数、PC実バイト、Library21H原本36合成ケース、同名短縮コピー拒否、未登録名拒否、パストラバーサル拒否、不明なsource拒否、非native判定）。
- 前回05H 133件source inventory用5/5 PASS、04H Library21H原本pin用3/3 PASSを同一PCで再実行、いずれもexit0。今回実行の独立合計16/16 PASS。旧原作ゲーム、13H安全拒否14ケース、過去21H249ケースはNOT RUN。
## Golden / T019 / MASTER境界
- G0合法UI戦闘開始、G1同run未改変SAVEと入力、G2実MAP/三陣営/ordered deployed Unit/Troop、G3結果、G4戦略World差分の一続きの一次原作証拠は未充足。DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019原作確定矛盾新規0。GameClear DAT13/TXT2のsource-scope差は従来RESOLVED、script2同名優先/phase flag/TXT runtime load/gwrite/decide11用途はVERIFY（継承）。
- MASTER正式checkpoint196、READY596(A115/B229/C136/D116)を末尾で確認。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値、今回最新全件再集計NOT RUN。新規正式READY統合IDなし。
- 既存T018表境界・T019 XREF・C T026/T032・D T030 TSV・0x5710C0・10/28 13H安全拒否はBLOCKED継続し再試行しない。今回新拒否0、他owner/原本/REA/dev/Git/Work/automation変更なし。
- OFFLINE-UNSYNCED全期間の完全な元資料照合、旧T018比較runnerの正式接続、schema意味照合、原作実G0-G2取得は未完了。
- 次: 正規比較runnerの実入力schemaとE保全資料のsource pin状態をread-onlyで対照。raw-bytes hashだけでnative観測は認定しない。
