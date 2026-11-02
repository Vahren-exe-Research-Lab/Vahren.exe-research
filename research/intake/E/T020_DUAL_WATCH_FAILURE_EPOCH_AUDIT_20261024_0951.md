# E-AUDIT-20261024-0951-T018-T020-DUAL-WATCH-FAILURE-EPOCH-01｜原作2戦闘window取得失敗の型・時相の独立監査
- Owner E / T018,T019,T020。JST 2026-10-24 09時台。PC-SAVEDを目指す新規E記録。原作実行NOT RUN、STATIC REPLAY OF SAVED ORIGINAL WATCH、READYではない。
- 先読: MASTER_LEDGER.md checkpoint196、ANALYSIS_LANES_PROTOCOL.md、A-D HANDOFF、REA PROGRESS/08H/09H、DEV実装計画、E T018/T019/T020、既保存watch1/watch2と過去07H監査。既存Eの09H V9索引fixture（別ID）には触れず重複登録しない。
## 保存済み原作一次ログの独立バイト再照合
- watch1: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl；SHA256=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7。234 JSONL records。
- watch2: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl；SHA256=1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46。85 JSONL records。
- PID23272は同じだが、watch1 active開始=2026-10-21T14:31:37.765392Z／mode2 active終了=14:33:34.325867Z、watch2開始=15:14:40.580007Z／終了=15:17:24.500365Zで**別戦闘**。同一PID、attack_count、battlefield_ptrだけでG0/G1/G2を結合してはならない。
- watch1 active 116.560秒。packet取得試行28/28はactive開始後0.001〜12.373秒で、全て `SnapshotError/unexpected nil tree node`。
- watch2 active 163.920秒。packet取得試行28/28はactive開始後0.002〜11.447秒で、全て `ValueError/Unbounded memory request`。watch1とは失敗理由が違う。
- watch1試行期間12.372秒、watch2は11.445秒。**両watchともactive開始後15秒以降のcapture試行0**。両原作戦闘自体はそれぞれ100秒以上継続した。
- 両JSONLには成功packetの記録0。watch2のWATCH_COMPLETE_AFTER_SCENE_EXITもcaptures_saved=0、native_finish_commit_verified=false。watch1はWATCH_TIMEOUT。保存JSONL外の成果物の存在・不存在まで主張しない。
## T018/T020 acceptance delta
- error typeを`NATIVE_CRASH`と誤分類しない。どちらも採取器側の例外であって、原作ゲームのクラッシュ・メモリ破損・EXEのバグは未証明。
- 28×2を独立した56件の完了packet失敗として一括計算したり、同じ原因としてまとめたりしない。旧BATTLE_USER構造観測3run/RAW8等とも混算しない。
- 「採取器が戦闘全体の長さにわたり失敗し続けた」や「15秒後なら必ず成功する」はどちらも未観測。後半での合法診断を採るならC/REA ownerへ新規独立試験条件として依頼、Eが採取器/ゲーム原本を改造しない。
- G0は両watchでnative戦闘activeが歴史的にOBSERVED。ただし合法旧UI攻撃元/対象Spot IDの完全receipt不足。G1同run直前SAVE bytes/SHA+操作/設定不足、G2実MAP+三陣営+順序付き出撃Unit/Troop不足。G3勝敗/G4戦略World差分も不足。
- 合法Golden受入時は`watch_filename+watch_SHA+active_start_UTC+PID`で戦闘を一意に束ね、旧EXE/DAT/SAVE/input/実出撃/新buildの各SHAを独立照合する。失敗した採取器ログは補助証拠に限定。
## T020 independent replay results
- 検証器: tests/t020_dual_watch_failure_epoch_gate_20261024_0951.py SHA256=2F8B6C41AB6E6BAF50DADA5B15C38B2419698FF67CC723AAACC24F73431982DB。
- fixture: tests/T020_DUAL_WATCH_FAILURE_EPOCH_CASES_20261024_0951.json SHA256=842D2A91A9830455FE05177DA2F18BB34B3B5B2FF0BAB5C2A71E595E569995F2。
- Local Compact PowerShellからpython -Bで独立実行済: source byte SHA 2/2、JSONL 234+85/319、attempt番号1..28各run、型・時相・active順照合2/2 PASS、合成fixture 11/11 PASS。旧原作ゲーム新規実行0、新規E Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019の新しい確定Wiki/DAT/EXE仕様矛盾0。watchの例外型差は採取器v1/v2系の観測差であり原作仕様不整合ではない。GameClear DAT13/TXT2字句範囲差RESOLVED、script2優先/phase flag/TXT実読込/gwrite復帰はVERIFY継承。
- MASTER最新実読 checkpoint196／公式READY596（A115/B229/C136/D116）、34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値で全件再計数なし。新規READY正式統合0。REA09H新規VERIFIED0、B09H T028 owner NOT READYは昇格しない。
- 旧OFFLINE-UNSYNCED暫定26件はID照合未了で未統合。旧安全拒否 T018表境界、C T026/T032、D T030 TSV、REA 0x5710C0、E旧拒否はBLOCKEDで、再試行・迂回なし。新規安全拒否0。
- 書込権限: 本E-own tests新規3成果物のみ。MASTER、原本EXE/DAT/SAVE/ZIP、他レーン、REA、dev_lab、Git、Work、スケジュール・設定を変更しない。
- NEXT: C-NB02合法UIの同run直前SAVE+入力+実MAP+3side+Unit/Troop確定receiptを優先。採取器ownerには2例外の別対処とactive開始後15/45秒等の安全な追加観測を条件提案（未実施）、Eは採取器修正しない。
