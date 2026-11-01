# E-AUDIT-20261031-07H-T020-T011-LEADER-CACHE-CROSSWALK-01

- owner: E
- tasks: T020（T018/T019 acceptance crosswalk）
- source_snapshot: 20261031-07H; source readback 2026-11-01 22時台 JST
- source_relative_path: `tests/T020_E_T011_LEADER_CACHE_ACCEPTANCE_20261031_07H.md`
- source_sha256: `04C7D9040C9EF633D9D027F696795691ECD4A5AF394CE5D04C1C5EEDD9128452`（今回PCで実バイト再計算）
- linked_original_owner_research: `B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01`（B/T011又はB/T013、READY未達）
- linked_source_relative_path: `data/T011_TRAINING_LEADER_BONUS_MEMO_NATIVE_20261031_07H.md`
- linked_source_sha256: `FA2E1295E2C93A15482F6DB4A3B4AF3F03935054EF5959E6F3D1D2AB2167499C`（今回PC read-only実バイト再計算、一致）
- evidence_kind: STATIC SOURCE / HISTORICAL_SYNTHETIC / VERIFY（本文の個別記載を優先）
- golden_status: ORIGINAL_NOT_OBSERVED; actual_PASS=0; strict_MATCH=0
- ready_status: NOT_READY / 正式MASTER統合0
- intake_status: PUBLISHED_INTAKE候補、NOT_CURATED（GitHub readback成功後に成立）

**研究区分:** E/T020受入訂正、STATIC SOURCE＋過去実行済みSYNTHETIC/VERIFY/NOT READY。2026-10-31 07H、PC現物SHA再照合は2026-11-01 22時台。

**E固有の訂正:** 06Hのpath名称は2種類の独立した加算能力を意味しない。node+0xCにはleader pointer、node+0x10にはSkill+0x2B0由来のleader-training bonus Bの**キャッシュ値**が入る。既ヒット経路は現在unitのbase count+Bを算出する。別leader pointerは別mapキー、NULL leaderはbaseのみ。VA 0x47229E→0x583DC0、0x4722BE→0x4F8A80、0x4723A8→0x4ED3B0、0x4723BC→0x474A80。キャッシュの時間境界とallocator失敗はVERIFY。

**T020比較fixture:** E既存テストは432個の3操作合成シーケンス（合計1296モデルイベント）、初回insert仮定・hit・不一致・scopeリセットを区別。原作実機の正常ユニット成長や中途Skill変更可能性を証明していない。source code `tests/t020_e_t011_leader_bonus_cache_gate_20261031_07H.py`。このrunでは再実行しない。

**prior/errata:** E-AUDIT-20261031-06H-T020-T011-TRAINING-COUNT-GATE-01 を訂正。既10/11 dev_labのtraining Skill+0x2B0記載を新E-native発見として二重計上しない。

**Golden条件:** 同turn・Power/leader・配下員・訓練状態の旧新可視EXP/Lv変化だけが比較対象。内部ポインタ/キャッシュヒットは旧合法UIから不可視ならINELIGIBLE。

## 共通受入境界
T018 C-NB02は、未改変原作の合法UIで G0 戦闘開始、同一戦闘の G1 戦闘直前SAVE実バイト/SHA・入力/時刻、G2 実MAP SHA・攻守援3陣営・順序付き出撃Unit/Troop を一次証拠で結ぶまでは未受入。必要なG3/G4の旧原作結果、同一入力に対する新実装結果も未取得。原作 DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。MASTER新規READY=0。T019はGameClear DAT13件/TXT2件の検索範囲差のみRESOLVED、script2優先・実ロード・flag・gwrite復帰はVERIFY。新規確定原作矛盾=0。安全拒否済み境界の再試行・代替経路調査なし。

## KB_CANDIDATE と採録制限
この文書はE担当による原文に基づくサニタイズ済み研究保全であり、他ownerの原報告の複写、公式READY、実機Golden、共有symbols/structs/REF_*の採録ではない。原作PEの識別SHAとして既存記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を参照したが、**今回原本PEの全バイト再ハッシュ・実行は行っていない**。正式な知識採録は専任curatorが出典/訂正/重複/権限を確認する。
