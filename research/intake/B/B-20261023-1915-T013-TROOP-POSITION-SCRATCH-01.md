# 迫真戦記 新B・既存研究の再利用用保全｜B-20261023-1915-T013-TROOP-POSITION-SCRATCH-01

- **research_id**: `B-20261023-1915-T013-TROOP-POSITION-SCRATCH-01`; **owner/tasks**: B/T013
- **元研究日**: 2026-10-23 19:15 JST
- **入庫状態**: `PUBLISHED_INTAKE / NOT_CURATED`（過去研究の保存、独立新発見なし）
- **一次owner出典**: `data/T013_TROOP_POSITION_SCRATCH_MODE_V3_20261023_1915.md` (1–18)
- **元研究本文 SHA256 (研究PC 2026-11-02実測)**: `1E6970599923ED6962EC760AEA6550A1A3EF6D0CB3655E3712084B8F8F2CEECF`
- **原作EXE SHA256 (研究PCでread-only照合)**: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- **VA / CALL site / offset**: 0x5699C0, 0x5697B1→0x5699C0, 0x569904→0x5699C0, Troop+0x0C/+0x10/+0x28/+0x30/+0x38, Unit+0x1867C/+0x1F9, 8B scratch 0xB040EC/+4/+8
- **先行成果/訂正関係**: B-20261023-18H-T013-TROOP-DISPATCH-ROUTE-01、B-20261023-1708-T013-TROOP-RTTI-RATIO-GATE-01

## 静的根拠と検証範囲

既存V3保存資料で2つのE8呼出しを静的検証。2026-11-02 V9 read-only 0x5699C0擬似C有、直接CALL元2件、出先25件、辞書未登録。過去ASM窓とGhidraの誤ABIを区別し原資料訂正関係を保持。

## 再実装へ再利用できる既存知見

配置候補producerの0x5699C0はTroop+0x30 modeで生成経路を分け、+0x38を一部経路の候補上限に利用し、+0x28を角度候補として参照/設定する。条件適格なUnitを基にした座標pairを8-byte strideの共有scratch配列へ積み、入口でendをbeginへ戻す論理クリアの経路がある。回転用D3DXを呼ぶ枝も存在。正確な型/座標系や最終Unit移動・スレッド/再入安全を静的だけで保証しない。

## VERIFY / 今後の検証

角度/座標変換のFPU・ABI、scratchの消費順序、modeによる最終配置、原作実機入力と結果はVERIFY。今回、過去に拒否された別のcallee内部・XREFにはアクセスも転載もしていない。

mode=1/2/others、+0x38=0/1/3、Unit不適格flag、入力角度とscratch pairを無改変原作で比較。

**境界**：実ゲームGolden PASS=0 / strict MATCH=0。新規READY=0。原資料のREADYは限定されたx86窓やcrossjoinについてであり、実機互換の達成ではない。元ASM/DATを新しく取得し直したものではなく、既存owner資料と現行V9検索索引を照合した要約。元研究内の拒否操作・保護VA・不明な下位実装は転載せず、別経路で確認しない。正式REF/辞書への採録と訂正は専任knowledge curatorのみ。
