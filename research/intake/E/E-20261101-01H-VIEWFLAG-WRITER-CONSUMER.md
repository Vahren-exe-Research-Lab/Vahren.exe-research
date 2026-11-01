# E-AUDIT-20261101-01H-T020-T013-VIEWFLAG-PRODUCER-CONSUMER-01

- owner: E
- tasks: T020（T018/T019 acceptance crosswalk）
- source_snapshot: 20261101-01H; source readback 2026-11-01 22時台 JST
- source_relative_path: `tests/T020_E_T013_VIEWFLAG_CHAIN_ACCEPTANCE_20261101_01H.md`
- source_sha256: `20895EEE1230762FDA5938A80A235ED5FBAEB50CD9E26AFE3744547C89664862`（今回PCで実バイト再計算）
- linked_original_owner_research: `B-20261101-01H-T013-QUOTA-QUARTER-FLAG-WRITERS-01`（B/T011又はB/T013、READY未達）
- linked_source_relative_path: `data/T013_GLOBAL65BD9E_QUOTA_QUARTER_WRITERS_NATIVE_20261101_01H.md`
- linked_source_sha256: `35BABF2BE5C00B052BDCDC907431A96398349A15163C03629AAD008819E81B8E`（今回PC read-only実バイト再計算、一致）
- evidence_kind: STATIC SOURCE / HISTORICAL_SYNTHETIC / VERIFY（本文の個別記載を優先）
- golden_status: ORIGINAL_NOT_OBSERVED; actual_PASS=0; strict_MATCH=0
- ready_status: NOT_READY / 正式MASTER統合0
- intake_status: PUBLISHED_INTAKE候補、NOT_CURATED（GitHub readback成功後に成立）

**研究区分:** E/T020 source-to-fixture crosswalk、STATIC＋過去実行SYNTHETIC/VERIFY/NOT READY、報告01H JST、PCソースSHA再確認22時台。

**条件モデル:** global byte[0x65BD9E] は0x45A22Cでクリア、局所quota条件を判定し、0x45A343で条件成立時に1を書き込む。0x4C16A4 downstream consumerはflag=0またはcontext+0xE4!=0ならRAW_PASSTHROUGH、そうでないとD3DX_REQUIREDという**経路選択モデル**。VA0x45A296、0x45A298..0x45A2D2 quarter分岐。preexisting flagは当該loader分岐で上書き、quota短絡時quarter helperは評価不要。

**T020再利用性:** 2 quota×2 hypothetical helper AL×2 context+E4×2 old flag×2 sentinel=32ユニークな**モデル入力**。過去Python unittest4/4 PASS、RAW20/D3DX_REQUIRED12。DATに書いてある設定文字列と実helper ALの写像は、この01H時点ではUNKNOWN。出力は経路markerのみで、D3DX matrix実値・PtInRect target・AI最終行動・ゲーム互換を証明しない。

**訂正関係:** E-AUDIT-20261101-02H-T020-T013-OFF-EXACT-VSLOT-BRANCH-01 により、quota/quarterの返り値について**ASCII厳密off比較**が補強された。01Hのboolean簡略モデルを実DAT keyの直接意味論として採録しない。

**Golden条件:** 合法旧UI・実設定保存hash・MAP/表示条件/経過tickの旧新一致。不可視flag注入はINELIGIBLE。

## 共通受入境界
T018 C-NB02は、未改変原作の合法UIで G0 戦闘開始、同一戦闘の G1 戦闘直前SAVE実バイト/SHA・入力/時刻、G2 実MAP SHA・攻守援3陣営・順序付き出撃Unit/Troop を一次証拠で結ぶまでは未受入。必要なG3/G4の旧原作結果、同一入力に対する新実装結果も未取得。原作 DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。MASTER新規READY=0。T019はGameClear DAT13件/TXT2件の検索範囲差のみRESOLVED、script2優先・実ロード・flag・gwrite復帰はVERIFY。新規確定原作矛盾=0。安全拒否済み境界の再試行・代替経路調査なし。

## KB_CANDIDATE と採録制限
この文書はE担当による原文に基づくサニタイズ済み研究保全であり、他ownerの原報告の複写、公式READY、実機Golden、共有symbols/structs/REF_*の採録ではない。原作PEの識別SHAとして既存記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を参照したが、**今回原本PEの全バイト再ハッシュ・実行は行っていない**。正式な知識採録は専任curatorが出典/訂正/重複/権限を確認する。
