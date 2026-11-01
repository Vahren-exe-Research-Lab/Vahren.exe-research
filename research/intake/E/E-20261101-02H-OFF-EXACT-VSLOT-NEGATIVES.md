# E-AUDIT-20261101-02H-T020-T013-OFF-EXACT-VSLOT-BRANCH-01

- owner: E
- tasks: T020（T018/T019 acceptance crosswalk）
- source_snapshot: 20261101-02H; source readback 2026-11-01 22時台 JST
- source_relative_path: `tests/T020_E_T013_OFF_EXACT_VSLOT_ACCEPTANCE_20261101_02H.md`
- source_sha256: `E1E5B9646175A9BB0A4578F19BC8F8BC21BE77ED8CCC9D9B77B5601593F18F6B`（今回PCで実バイト再計算）
- linked_original_owner_research: `B-20261101-02H-T013-VIEW-OFF-COMPARE-VSLOT5C-01`（B/T011又はB/T013、READY未達）
- linked_source_relative_path: `data/T013_VIEW_OFF_COMPARE_VSLOT5C_NATIVE_20261101_02H.md`
- linked_source_sha256: `389341F1F321CF412D6930B743807941476C97F4E15F63CACF0EAA552146F61A`（今回PC read-only実バイト再計算、一致）
- evidence_kind: STATIC SOURCE / HISTORICAL_SYNTHETIC / VERIFY（本文の個別記載を優先）
- golden_status: ORIGINAL_NOT_OBSERVED; actual_PASS=0; strict_MATCH=0
- ready_status: NOT_READY / 正式MASTER統合0
- intake_status: PUBLISHED_INTAKE候補、NOT_CURATED（GitHub readback成功後に成立）

**研究区分:** E/T020の01Hモデル精密化、STATIC BYTE VERIFIED（元報告で実施）＋過去実行SYNTHETIC/VERIFY/NOT READY。実原作実行0。

**固有の訂正:** quota_viewとquarter_viewの戻り文字列が、比較局所でASCII小文字の3-byte `off` と**長さも含めて完全一致**したときだけOFF扱い。`offx`、`off `、`of`、`OFF`、空文字を勝手にoffへ正規化しない。quota非offはquarter評価を短絡する。global[0x65BD9E]のloader局所フラグとconsumer0x4C1690の関係はSTATIC、DAT raw値の既定値/実読込はVERIFY。

**vtable条件:** 0x57D994 CALL0x4C1860 の後、PtInRect AL!=0なら後段virtualをskip。AL==0でも別ESI!=0ならskip。**AL==0かつESI==0**の時だけ0x57D9A9 FF D0経由でvtable+0x5Cに達する可能性。これは間接呼出先・最終ターゲット・退却動作を確定しない。関係VA 0x45A26F/0x45A296/0x45A2C6/0x42F860/0x57D994/0x57D99B/0x57D99F/0x57D9A9、context+0xE4。元E報告は4 native window SHA、E8 2 site、FF D0 1 siteを独立監査済み（今回再実行なし）。

**T020負例:** 7 quota戻り値×7 quarter戻り値×2 context+E4×2 PtInRect AL×2 ESI=392ケース、元報告のunittest6/6とfixture392 unique、すべてモデル入力であり合法原作での到達性は未観測。`actual_target=null`、`vcall_identity=null`、native Game result=NOT_RUN。E 01H簡略モデルを訂正するが、原作の不具合認定ではない。

**次の検証:** 元DAT設定バイトSHAと原作合法UIで読める実設定/可視結果、改変のないMAP/表示/入力をそろえる。ABI/FF D0 actual calleeは未確定のためKB確定関数名にしない。

## 共通受入境界
T018 C-NB02は、未改変原作の合法UIで G0 戦闘開始、同一戦闘の G1 戦闘直前SAVE実バイト/SHA・入力/時刻、G2 実MAP SHA・攻守援3陣営・順序付き出撃Unit/Troop を一次証拠で結ぶまでは未受入。必要なG3/G4の旧原作結果、同一入力に対する新実装結果も未取得。原作 DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。MASTER新規READY=0。T019はGameClear DAT13件/TXT2件の検索範囲差のみRESOLVED、script2優先・実ロード・flag・gwrite復帰はVERIFY。新規確定原作矛盾=0。安全拒否済み境界の再試行・代替経路調査なし。

## KB_CANDIDATE と採録制限
この文書はE担当による原文に基づくサニタイズ済み研究保全であり、他ownerの原報告の複写、公式READY、実機Golden、共有symbols/structs/REF_*の採録ではない。原作PEの識別SHAとして既存記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を参照したが、**今回原本PEの全バイト再ハッシュ・実行は行っていない**。正式な知識採録は専任curatorが出典/訂正/重複/権限を確認する。
