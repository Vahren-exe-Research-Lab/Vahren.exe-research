# B研究既存IDのGitHub保存｜B-20261023-2317-T013-TROOP-MODE-SOURCE-CASE8-01

- **research_id**: `B-20261023-2317-T013-TROOP-MODE-SOURCE-CASE8-01`
- **owner/tasks**: B / T013
- **元研究日**: 2026-10-23 23:17 JST
- **状態**: `PUBLISHED_INTAKE / NOT_CURATED`、既存原資料の静的研究・推論を保全（新発見・新READYへの加算なし）
- **出典**: `data/T013_TROOP_MODE_SOURCE_CASE8_NATIVE_20261023_2317.md`（1–17行）
- **元研究本文 SHA256（2026-11-02研究PC現物照合）**: `8F600308B375B7221A1493BB396EB961421C2418D2B69E90452AEBE5F5B1383A`
- **対象原作EXE SHA256（同日読取専用照合）**: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- **VA / CALL / offset**: 0x4B5976→0x49CCA0, 0x4B597E/0x4B5981, 0x4B59FD→0x4B5A00→0x569530, 0x4F9837→0x569530, 0x4FA043→0x569530, Troop+0x30
- **先行ID / 重複・訂正**: B-20261023-22H-T013-TROOP-FORM-MODE-SETTER-01

## 根拠の区分

元原作ASM限定窓0x4B5957 len0xDD SHA256 4D38429E4ADC259DD5BC53AED6CE486037D4B59C5425DC8FF8980A222E712A62。2026-11-02 V9 read-only 0x569530擬似C有、caller3件(0x4B5A00/0x4F9837/0x4FA043)。

## 研究として再利用できる結論（STATIC/INFERRED）

0x4B4710のcase8相当経路で、0x49CCA0の戻り値をlocalへ保存し、signed >2のときsetterへ行かない。候補配列中、NULLと局所のidentity mismatchを除外した場合に限って保存した値を0x569530へ渡し、Troop+0x30へ伝播する。別callerの0x4F9837は明示的なmode0入力。これは『実modeは0/1/2しか存在しない』証明ではなく、負値・実DAT command・runtime到達は不明。

## 未確定・実機Golden

戻値producer/identity pointerの実型、局所flag+0x1F/+0x20意味、別呼出とのalias、最終AI行動はVERIFY。旧22H setterを新発見として再計上しない。

**必要な次の照合**: 原作合法DAT入力からsource戻値 -1/0/1/2/3、候補NULL/同一性一致・不一致でsetter到達と+0x30差分を比較。

ゲーム原作の実機Golden PASS=0、strict MATCH=0。DYNAMIC確証なし。旧B所有資料中の「READY」は成立した局所静的証拠の境界であり、ゲーム全体の互換READYではない。単一関数の擬似CからABI/意味/副作用を断定しない。禁じられた操作・既拒否元資料の取得/再出版は行わない。curatorはこの摘要と元資料のSHA・相互訂正を確認し、正式REF/辞書採録を個別判断する。
