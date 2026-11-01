# E-AUDIT-20261031-06H-T020-T011-TRAINING-COUNT-GATE-01

- owner: E
- tasks: T020（T018/T019 acceptance crosswalk）
- source_snapshot: 20261031-06H; source readback 2026-11-01 22時台 JST
- source_relative_path: `tests/T020_E_T011_TRAINING_BRANCH_ACCEPTANCE_20261031_06H.md`
- source_sha256: `491E31D65336E274BFF3216D17228BD8438F33C35D6889A986B26051F5283773`（今回PCで実バイト再計算）
- linked_original_owner_research: `B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01`（B/T011又はB/T013、READY未達）
- linked_source_relative_path: `data/T011_TRAINING_COUNT_PROVENANCE_NATIVE_20261031_06H.md`
- linked_source_sha256: `78FFB6534F0B999C734DA7FB5E4040F0C4C8AE7CE1A74232B94B89D623B20D8A`（今回PC read-only実バイト再計算、一致）
- evidence_kind: STATIC SOURCE / HISTORICAL_SYNTHETIC / VERIFY（本文の個別記載を優先）
- golden_status: ORIGINAL_NOT_OBSERVED; actual_PASS=0; strict_MATCH=0
- ready_status: NOT_READY / 正式MASTER統合0
- intake_status: PUBLISHED_INTAKE候補、NOT_CURATED（GitHub readback成功後に成立）

**研究区分:** E/T020（T018/T019比較受入）、2026-10-31 06Hの旧研究を2026-11-01 22時台にPCから再取得。STATIC（B元資料照合）＋実行済みSYNTHETIC（過去記録）/VERIFY/NOT READY。

**E固有の受入知見:** `power+0xD8` が非0のときpower値、0のときscenario値を選ぶ局所count候補。負値は0に、0値は1へ正規化し、その後に別の候補加算経路があり得る。起動条件不成立なら正規化値だけで訓練効果を予測できない。VA 0x472081→0x595320、0x4722D3/0x47238E/0x4723A0、候補node+0x10、Skill+0x2B0。元DAT有効値・実Lv/EXP・符号溢れはVERIFY。

**比較fixture:** E既存runner `tests/t020_e_t011_training_count_branch_gate_20261031_06H.py` が216ユニークな条件付き合成ケースを記録（108 early-skip、108 candidate-count経路）。本入庫時にrunnerは再実行していない。旧原作Gameplay 216PASSとは主張しない。

**訂正関係:** 次の E-AUDIT-20261031-07H-T020-T011-LEADER-CACHE-CROSSWALK-01 が「DIRECTとTRAININGは2種類の訓練能力」ではないと明示訂正。旧06H合成モデルのpath区分を実nativeの二重bonusとして用いてはならない。既存dev_lab 10/11研究のtraining_up fallbackは再発見に加算しない。

**次の検証:** B元証拠のreachable/実使用と合法旧原作のtrainer条件、原本DAT未改変SHA、同POWER/turn/leader/memberと可視EXP/Lvの旧新差分のみ実受入可能。

## 共通受入境界
T018 C-NB02は、未改変原作の合法UIで G0 戦闘開始、同一戦闘の G1 戦闘直前SAVE実バイト/SHA・入力/時刻、G2 実MAP SHA・攻守援3陣営・順序付き出撃Unit/Troop を一次証拠で結ぶまでは未受入。必要なG3/G4の旧原作結果、同一入力に対する新実装結果も未取得。原作 DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。MASTER新規READY=0。T019はGameClear DAT13件/TXT2件の検索範囲差のみRESOLVED、script2優先・実ロード・flag・gwrite復帰はVERIFY。新規確定原作矛盾=0。安全拒否済み境界の再試行・代替経路調査なし。

## KB_CANDIDATE と採録制限
この文書はE担当による原文に基づくサニタイズ済み研究保全であり、他ownerの原報告の複写、公式READY、実機Golden、共有symbols/structs/REF_*の採録ではない。原作PEの識別SHAとして既存記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を参照したが、**今回原本PEの全バイト再ハッシュ・実行は行っていない**。正式な知識採録は専任curatorが出典/訂正/重複/権限を確認する。
