# 迫真戦記 新E｜E21合成G2とPC既存G2診断契約の差分（22時台）

研究ID: E-AUDIT-20261028-22H-T018-T020-E21-PC-G2-CONTRACT-CROSSWALK-01
担当: E / T018・T020（T019参照）。分類: PC-LOCAL / SYNTHETIC EXECUTED / STATIC CODE CROSSWALK / VERIFY / NOT READY。
新規原作DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。新規正式READY=0。

## 入力・所有権・独立性
- PCへDesktop Commander Local Compact接続成功。evidence/ANALYSIS_LANES_PROTOCOL.md、A～D HANDOFF末尾、REA decomp_task/PROGRESS.md、dev_lab/docs/IMPLEMENTATION_PLAN.md、search_index/README.md、E所有tests/T018_CNB02_BRIDGE_STAGE_CROSSWALK、2026-10-25/26 G2診断コード・報告、wiki/T019_CONTRADICTIONS.md末尾をread-only参照。
- E21の合成JSON元資料: 会話添付 E_20261028_2149/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json。ChatGPTコンテナで再ハッシュした元資料SHA256=7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA。PC内で元資料そのものを再ハッシュしたわけではない。
- E21から必要な *合成* G2側ID/deployed/map_shaとsource_classのみ新規JSONへ写し、PC既存tests/t020_cnb02_g2_cross_generation_parity_guard_20261026_10H.py の診断に投影。E21親ゲート(2045/2149)の実行を今回PCで再演したのではない。
- 新規E所有のfixture・Python・本報告書だけを書込。元T018表境界/拒否済みXREF・他owner/REA/dev_lab/原本EXE/DAT/ZIP/SAVE・Git/Work/設定/automation変更なし。旧安全拒否操作の別tool/shell/path迂回無し。

## 新しい一対一照合成果
- E21のG2は sides=[{role:attack,id:A},{role:defend,id:D},{role:support,id:S}] と deployed=[(A,u1,t1,order0),(S,u5,t3,order1)]。3種side *宣言* は存在するが、defense相当の出撃Unit/Troopはゼロ。現行PCのE 09H/10H診断へ写すと NO_DEFENSE_ROSTER_RECEIPT を出す。
- E21のfield名は「defend」、PC 09H/10Hの正規化roleは「defense」。名称対応を検証専用変換で明示し、DEFEND_TO_DEFENSE_ALIAS_VERIFYを必ず維持。原作のside意味やPower同一性を自動確定しない。
- E21にはMAP bytesの合成hashはあるが、PC G2 schemaのmap_idに対応する一次証拠が無い。MAP_ID_UNVERIFIEDとなる。任意map_idを後付けしてもMAP_ID_NOT_SOURCE_ATTESTEDを解除しない。
- さらにE21合成captureにはG2のactive-enter/exit二重bracket・同じ戦闘の外部一次receiptがない。同期run_id・自作SHA/JSONが一致しても旧原作の同一戦闘、配置完了、合法UI、未改変SAVEを証明しない。
- 21時台E合成semantic bindingを既存PC T018 runnerにそのまま「認証済みGolden」として取り込むことは不適切。これは実ゲーム側の矛盾ではなく、Eの2系統schemaの相互運用・証拠階級の不足である。

## T020 合成回帰
- 新規tests/t020_e21_g2_schema_bridge_gate_20261028_22H.py：24/24 PASS。新規JSONから診断モデルへ投影、欠落defense、未証明MAP、role alias、誤side ID、役割/side ID重複、非hashable role/side ID・非object入力のfail-closed、bool order、非連続順序、名前欠落、重複roster、後付けmap_id/自己申告nativeの負例を実行。
- 既存09H role overlayを今回独立再実行12/12 PASS、10H cross-generation guardを独立再実行14/14 PASS。今回PC実行合計50/50 PASS、失敗0。これは合成fixture・診断コードの結果であり旧EXE gameplayテストではない。
- 13時台に安全拒否された未実行14件と、21時台旧SQLite依存249件は今回の50件に含めず、前回履歴を新規PASSに再加算しない。
- 新規成果の分類: SYNTHETIC EXECUTED / STATIC CROSSWALK / VERIFY / NOT READY。Bの実戦分岐、Ghidra間接先、原作実可視出撃の確定はしない。

## T018 GoldenとT019
- 合法C-NB02のG0: 元の通常UIでの戦闘開始の一次動画/入力/実時刻。G1: 同じ戦闘の直前未改変SAVE実bytes+SHA/操作順序。G2: 原作実MAP bytes+ID、攻防支援の可視side、順序付き実Troop/Unitとactive window。G3戦闘結果・G4戦略World差分も同一runで別途必要。
- 「三陣営が存在」≠「攻防両陣営が出撃した一次証拠」。出撃実数とside宣言を分けて受入。不明ならVERIFY、actual Golden PASS禁止。
- T019新規確定Wiki/DAT/EXE矛盾0。GameClear DAT13/TXT2字句scope差はRESOLVED、script2同名優先、phase flag、TXT読込、gwrite復帰、decide11用途はVERIFY継承。今回原作のバグ認定0。

## MASTER・復旧・再開
- MASTER TASK QUEUEの旧13時台安全拒否を尊重して同じ再照合は未実施。最終確認旧値=2026-10-28 12時台 checkpoint196 / READY596（A115/B229/C136/D116）、34 Task（DONE9/IN_PROGRESS21/VERIFY4、当時ID重複0）。この回の最新値として扱わない。
- 新規正式READY採録IDなし。E21はOFFLINE-UNSYNCED、10/25以降の完全重複・owner・合意・既統合照合は未完了。今回のPC保存はE22独立検証成果のみでE21原本の正式同期・READY昇格ではない。
- 旧E安全拒否 E-RC-20261028-1353-READONLY-PS-SAFETY-01 と E-RC-20261028-13H-E13-REPORT-APPEND-SAFETY-02、T018表境界/session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0ほかはBLOCKED維持。今回新規安全拒否0/PC接続障害0。
- 次のE優先: E21合成schemaとPC T018正式比較runnerの**受入レイヤーを分離した非破壊統合設計**（source capture と map_id/roster観測receiptを独立保持）。合法旧UI同一戦闘のG0/G1/G2一次証拠を取得するまではstrict MATCH=0、READY=0を維持する。

