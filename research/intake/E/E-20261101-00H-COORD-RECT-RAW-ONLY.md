# E-AUDIT-20261101-00H-T020-T013-COORD-GATE-RECT-01

- owner: E
- tasks: T020（T018/T019 acceptance crosswalk）
- source_snapshot: 20261101-00H; source readback 2026-11-01 22時台 JST
- source_relative_path: `tests/T020_E_T013_COORD_GATE_RECT_ACCEPTANCE_20261101_00H.md`
- source_sha256: `93E90360A4D70632782915540020430806B9E11A1813598AD3472A96E57AB250`（今回PCで実バイト再計算）
- linked_original_owner_research: `B-20261101-00H-T013-COORD-TRANSFORM-GATE-OUTPUT-ABI-01`（B/T011又はB/T013、READY未達）
- linked_source_relative_path: `data/T013_COORD_TRANSFORM_GATE_OUTPUT_ABI_NATIVE_20261101_00H.md`
- linked_source_sha256: `022EFBC353968A50C1C6B91473279042BA9E139BB759C9D21417CC7DE8C4951C`（今回PC read-only実バイト再計算、一致）
- evidence_kind: STATIC SOURCE / HISTORICAL_SYNTHETIC / VERIFY（本文の個別記載を優先）
- golden_status: ORIGINAL_NOT_OBSERVED; actual_PASS=0; strict_MATCH=0
- ready_status: NOT_READY / 正式MASTER統合0
- intake_status: PUBLISHED_INTAKE候補、NOT_CURATED（GitHub readback成功後に成立）

**研究区分:** E/T020の原作条件/Win32矩形比較設計、STATIC BYTE（元報告）＋条件付きSYNTHETIC/VERIFY/NOT READY。2026-11-01 00HのE報告を22時台再SHA確認。

**受入根拠:** 0x4C1880→0x4C1690 direct E8。0x4C16AF JE・0x4C16BC JNEから0x4C1749 raw-copyへ到達可能、[EDI]=ECX,[EDI+4]=EAX、0x4C1755 EAX=EDI、0x4C175F RET4。0x65BD9E global とcontext+0xE4の組合せがRAWとD3DX経路を分ける。これらは局所静的境界で、全体ABIや画面pixelの正確さは未確定。

**比較fixture:** 2×2×4 margin×10点=160ユニークな合成ケース。RAW_PASSTHROUGH120/120について実Win32 InflateRect/PtInRectのhalf-open矩形（left/top含むright/bottom除く）と合成raw分岐の一貫性を検査。残り40/40 D3DX_REQUIREDは expected_point=null/TRANSFORM_NOT_RUN。D3DX matrix・rounding・Unit field・実ゲーム画面座標を発明しない。原ゲームの受入結果160PASSではない。

**prior:** A-20261013-1100-04、B00 callerの元意味論をE新発見として二重計上しない。次の01H writer→consumerモデル、および02H exact off/value/vslot条件へ連結する。

**次の検証:** 合法旧原作の設定値DAT原本SHA、同MAP/UI display mode/入力/フレームを固定し、可視クリック対象をold/new対比。原作画面で取れない内部flag値はUNKNOWN。

## 共通受入境界
T018 C-NB02は、未改変原作の合法UIで G0 戦闘開始、同一戦闘の G1 戦闘直前SAVE実バイト/SHA・入力/時刻、G2 実MAP SHA・攻守援3陣営・順序付き出撃Unit/Troop を一次証拠で結ぶまでは未受入。必要なG3/G4の旧原作結果、同一入力に対する新実装結果も未取得。原作 DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。MASTER新規READY=0。T019はGameClear DAT13件/TXT2件の検索範囲差のみRESOLVED、script2優先・実ロード・flag・gwrite復帰はVERIFY。新規確定原作矛盾=0。安全拒否済み境界の再試行・代替経路調査なし。

## KB_CANDIDATE と採録制限
この文書はE担当による原文に基づくサニタイズ済み研究保全であり、他ownerの原報告の複写、公式READY、実機Golden、共有symbols/structs/REF_*の採録ではない。原作PEの識別SHAとして既存記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を参照したが、**今回原本PEの全バイト再ハッシュ・実行は行っていない**。正式な知識採録は専任curatorが出典/訂正/重複/権限を確認する。
