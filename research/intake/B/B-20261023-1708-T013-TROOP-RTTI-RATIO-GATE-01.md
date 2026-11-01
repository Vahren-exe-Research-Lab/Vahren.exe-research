# B研究既存IDのGitHub保存｜B-20261023-1708-T013-TROOP-RTTI-RATIO-GATE-01

- **research_id**: `B-20261023-1708-T013-TROOP-RTTI-RATIO-GATE-01`
- **owner/tasks**: B / T013 (T024参照)
- **元研究日**: 2026-10-23 17H JST
- **状態**: `PUBLISHED_INTAKE / NOT_CURATED`、既存原資料の静的研究・推論を保全（新発見・新READYへの加算なし）
- **出典**: `data/T013_TROOP_RTTI_HALF_RATIO_GATE_V9_20261023_1708.md`（1–26行）
- **元研究本文 SHA256（2026-11-02研究PC現物照合）**: `63F911CC923FF36F836D78AEB08ECB223C24C8E57666034D8A8D8C5720EC5537`
- **対象原作EXE SHA256（同日読取専用照合）**: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- **VA / CALL / offset**: Troop RTTI 0x00639A2C/0x0063F40C; vtable 0x00639A30 slot+4→0x0056AB20; 0x569360; Troop+0x34/+0x3C/+0x44; Unit+0x1867C/+0x1867E
- **先行ID / 重複・訂正**: B-20261023-1519-T013-GROUP-AGGREGATE-LIFECYCLE-01、B-20261023-1618-T013-GROUP-SPACING-CONSUMER-01

## 根拠の区分

原作MSVC RTTI TypeDescriptorに .?AVTroop@@、0x639A34指す仮想slot+4に0x56AB20。保存ASMの近接比較では0x569453→0x5E3B70。2026-11-02 V9 read-only 0x569360の擬似C有・E8 callers2、E8 outgoing2。

## 研究として再利用できる結論（STATIC/INFERRED）

Troop周期条件（+0x1Cおよびengineフラグ等）により+0x3Cのカウンタを更新する。約100周期の条件付き処理で0x569360へ到達する静的経路がある。対象構成員の最初の適格Unitをアンカーに、その他の適格N名と距離条件を満たすM名を数え、通常の有限値・N>0の比較はM/N>=0.5で真の戻り値に相当する。N=0の局所枝は真を返す。ただし『士気値』や『敗走』と命名しない。

## 未確定・実機Golden

本番での仮想call実到達、FPU特殊値/NaN、全writer、0x44の意味、配置・攻撃動作との関連はVERIFY。原作Golden0・strict MATCH0、新READY0。

**必要な次の照合**: 0/1/2/3/4構成員と距離境界、カウンタ99/100/101、+0x44変化を同一SAVE/MAP/seedで観測。

ゲーム原作の実機Golden PASS=0、strict MATCH=0。DYNAMIC確証なし。旧B所有資料中の「READY」は成立した局所静的証拠の境界であり、ゲーム全体の互換READYではない。単一関数の擬似CからABI/意味/副作用を断定しない。禁じられた操作・既拒否元資料の取得/再出版は行わない。curatorはこの摘要と元資料のSHA・相互訂正を確認し、正式REF/辞書採録を個別判断する。
