# E-AUDIT-20261031-08H-T020-T011-CACHE-DUPLICATE-CLEANUP-01

- owner: E
- tasks: T020（T018/T019 acceptance crosswalk）
- source_snapshot: 20261031-08H; source readback 2026-11-01 22時台 JST
- source_relative_path: `tests/T020_E_T011_CACHE_LIFECYCLE_ACCEPTANCE_20261031_08H.md`
- source_sha256: `3CF55EDEDA35499D02FF09FA8CD75CBE2CBED9E014861665B0A1777DDBA2EC22`（今回PCで実バイト再計算）
- linked_original_owner_research: `B-20261031-08H-T011-TRAINING-CACHE-LIFECYCLE-01`（B/T011又はB/T013、READY未達）
- linked_source_relative_path: `data/T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md`
- linked_source_sha256: `B79044AE9C8AE40FE3F59E06DD056E0D73DAABEC3D98B784C628737A2EACE1EF`（今回PC read-only実バイト再計算、一致）
- evidence_kind: STATIC SOURCE / HISTORICAL_SYNTHETIC / VERIFY（本文の個別記載を優先）
- golden_status: ORIGINAL_NOT_OBSERVED; actual_PASS=0; strict_MATCH=0
- ready_status: NOT_READY / 正式MASTER統合0
- intake_status: PUBLISHED_INTAKE候補、NOT_CURATED（GitHub readback成功後に成立）

**研究区分:** E/T020条件付き受入、STATIC CROSSCHECK＋既合成検査/VERIFY/NOT READY。2026-10-31 08H報告、2026-11-01 22時台実SHA読取。

**E固有の境界:** 0x472091→0x49ED90でsentinel初期化、0x4726C1→0x4DEF40 erase要求、0x4726D9→0x5B6BBB解放。低レベル0x474B09の**重複キー挿入**はincoming nodeを破棄してflag0を返す候補だが、通常callerは事前にmap検索するため、同じleaderの通常プレイ二重insertに到達する証拠はない。0x4723C1は既計算base+Bを使い、挿入成否と現在unitの計算値を混同しない。node+0xC/+0x10、insert flag+0x4。

**T020負例:** 以前の合成実行144/144（72強制duplicate injection、72別pointer）で「cacheに残る過去bonus」「現在unitに使用されるbonus」「解放順」を分離。強制duplicateは **LOW_LEVEL_INJECTION_ONLY** で原作合法Goldenには流用不可。正常枝の概念的順序 INIT_SENTINEL→PROCESS_UNIT→REQUEST_RANGE_ERASE→FREE_SENTINEL。例外・allocator failure・pointer recycle・実解放完了はNOT RUN。E runnerは `tests/t020_e_t011_cache_duplicate_cleanup_gate_20261031_08H.py`、今回再実行0。

**prior:** E06H count→E07H leader cache→E08H duplicate/cleanupを段階研究としてリンクし、新native解釈の発見件数をB ownerと二重計数しない。

**比較受入:** 原作EXP/Lv/可視結果を同条件で比較し、不可視pointer・強制重複のsynthetic結果をDYNAMIC/Goldenへ昇格しない。

## 共通受入境界
T018 C-NB02は、未改変原作の合法UIで G0 戦闘開始、同一戦闘の G1 戦闘直前SAVE実バイト/SHA・入力/時刻、G2 実MAP SHA・攻守援3陣営・順序付き出撃Unit/Troop を一次証拠で結ぶまでは未受入。必要なG3/G4の旧原作結果、同一入力に対する新実装結果も未取得。原作 DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。MASTER新規READY=0。T019はGameClear DAT13件/TXT2件の検索範囲差のみRESOLVED、script2優先・実ロード・flag・gwrite復帰はVERIFY。新規確定原作矛盾=0。安全拒否済み境界の再試行・代替経路調査なし。

## KB_CANDIDATE と採録制限
この文書はE担当による原文に基づくサニタイズ済み研究保全であり、他ownerの原報告の複写、公式READY、実機Golden、共有symbols/structs/REF_*の採録ではない。原作PEの識別SHAとして既存記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を参照したが、**今回原本PEの全バイト再ハッシュ・実行は行っていない**。正式な知識採録は専任curatorが出典/訂正/重複/権限を確認する。
