# E-AUDIT-20261025-11H-T018-T020-G2-SEMANTIC-REVIEW-RUNNER-01
Owner: E / T018,T020. 2026-10-25 11H JST. STATIC CODE REVIEW + NEW SYNTHETIC TESTS / NOT READY / OLD GAMEPLAY NOT RUN.
## 対象と差分
PC Local Compact: MASTER_LEDGER.md、evidence/ANALYSIS_LANES_PROTOCOL.md、A-D HANDOFF、REA decomp_task/PROGRESS.md、dev_lab/docs/IMPLEMENTATION_PLAN.md、E既存T018/T019/T020を読取。MASTER最終正式checkpoint196/READY596は変更しない。
10HのE監査で発見したG2形状ゲートの意味的穴を、既存コードの変更なしにE所有の独立review runnerで検査可能にした。
新コード: tests/t020_cnb02_g2_semantic_review_20261025_11H.py、SHA256 A76D5499B1751443705649B02687DEA5D6FCBDEBDA5323A209695DC9F5736E66。
元コードSHA256 34BC469C50471A1BCE58D2815D6E5D9A4CF45D6CD2232898312FDE69A15E349D (read-only再計算一致)。
10H設計書SHA256 39DBE2D6F9688F93253D59E31EC28AE5C3F654E7F62F5C9CCEC0105D39185602 (read-only再計算一致)。
## 実行結果
python -B -m unittest -v t020_cnb02_g2_semantic_review_20261025_11H：**新規15/15 PASS、0 failure、終了正常**。
初回実行は旧17件がimport経由で自動再発見され32 PASS。E新コードのimportを修正し、再実行では新規15件だけが走ることを確認。旧17件を新規加算しない。
検査：未知/numeric roster side、攻防side空、同じ可視ラベル対の重複、未確認MAP、Unit/Troop numeric、side参加者numeric、防御roster欠落、support空の合法shape、support項目欠落、map digest見かけ、old_observed=false、synthetic=falseでもMATCH非認定。
結果は元gateのparent verdict + flags + actual_golden_pass=False + strict_match=Falseのみ。原作MAPバイト・本物の出撃Unit/Troop・陣営Power/所属を証明するものではない。
**重複した名前は別Unitの場合があるため即拒否せずREVIEW。sideリストとroster IDの一致は意味不確定につき推測せず、support=[]は合法候補。**
## 正本・Golden・矛盾と安全
EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187は旧マニフェスト識別値。今回旧EXE/DAT/SAVE/MAP実バイト再検証なし。
C-NB02 G0合法UI sp2→sp16、G1同run直前SAVE+入力、G2 native MAP/3side/ordered Unit-Troop、G3結果、G4 World差分は依然NOT QUALIFIED。E DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
T019新規確定Wiki/DAT/EXE矛盾0。旧GameClear字句範囲差RESOLVED、script2優先/phase flag/TXT loader/gwrite復帰VERIFY。
公式新規READY統合IDなし。cp196/READY596=A115/B229/C136/D116は最後の正式値。34 Task DONE9/IN_PROGRESS21/VERIFY4は10H全件再集計の旧確認値で、11H再計数なし。E T018/T019/T020 IN_PROGRESS。
OFFLINE-UNSYNCED正式未統合、過去T018境界/E join/code、C T026/T032、D T030 TSV、0x5710C0等の安全拒否はBLOCKED維持。再提出・別tool/path/shell/Remote/ZIP迂回なし。新規安全拒否0、接続障害0。
MASTER、原本EXE/ZIP/DAT/SAVE、A-D/REA/dev_lab、Git/push、Work、他タスク/設定/スケジュールは不変更。新規書込は本E所有ノートと新E所有コードのみ。
NEXT: 合法旧UI C-NB02で同一戦闘のG0/G1/G2実バイト証拠を採取し、MAP同定・陣営Power・Troop/Unit実体との一対一結合を独立監査。現runnerは合成レビュー専用で正式受入器への昇格は保留。
