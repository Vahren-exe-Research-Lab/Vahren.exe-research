# B-OFFLINE-20261024-14H-T012-SCALE-INIT-PARSER-COPY-X87-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261024-14H-T012-SCALE-INIT-PARSER-COPY-X87-01`
- owner/tasks: B / T012
- source_relative_path: `data/B_T012_SCALE_INIT_PARSER_COPY_OFFLINE_20261024_14H.md`
- source_sha256: `367a19af2a8bed7bee23419940956f33a3b6db6b9ca244d6df09c6735e71a438` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 6191
- original research date: 20261024; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T012 Skill倍率の生成・初期化・コピーの連結検証（2026-10-24 14時台）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X00599600`, `0X00599860`, `0X00599900`, `0X3FF00000`, `0X00599BD0`, `0X0059CDA3`, `0X0059CDBC`, `0X005510FF`, `0X00551102`, `0X0046FB00`, `0X0046FC13`, `0X0046FCE0`, `0X0046FC3E`, `0X0051E6F0`
- prior_ids / possible errata / crossrefs: not separately enumerated; consult original
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L13 ## 新規増分A：生成時の初期値は `0.0`、`str_ratio` 初期値は `1.0`
- L15 2026-10-21 Ghidra擬似Cと直接CALL索引で `0x00599600` → CALL site **`0x00599860`** → `0x00599900` を照合。`0x00599900`内部の対象オブジェクト書込みは以下。
- L17 ```cpp
- L18 *(undefined4 *)(unaff_ESI + 0x27c) = 0;
- L19 *(undefined8 *)(unaff_ESI + 0x280) = 0;
- L20 *(undefined8 *)(unaff_ESI + 0x288) = 0x3ff0000000000000;
- L21 ```
- L23 この初期化経路に限れば、倍率 `+0x280` はIEEE doubleの **+0.0**、比率 `+0x288` は **1.0**。既往T012 §32の「`str_ratio`省略時1.0」と整合するが、**その同じ初期値を作る関数と生成側CALL siteを新たに接続**した。Ghidra擬似Cベースであり、実機で必ずこの初期化関数を経由するという網羅的証明ではない。
- L25 ## 新規増分B：生成後の解析器は整数→doubleへの倍率上書きを行う
- L27 既存T012 §32では、`0x00599BD0`関数内、VA `0x0059CDA3`付近の `FILD [ESP+0x320]` → 0.01倍 → `0x0059CDBC`で `Skill+0x280` 格納まで確認済み（**この旧証拠そのものは再計上しない**）。今回、Ghidraの完全擬似Cで次を独立照合。
- L29 ```cpp
- L30 *(double *)(param_3 + 0x280) = (double)iStack_1608 * _DAT_0063b070;
- L31 ```
- L33 `iStack_1608`は擬似C上の**符号付き32bit整数**。0.01という定数値は過去の原作ASM記録に依存する（このZIPには定数の原作生バイトがない）。この前提で、いずれの32bit整数についても結果は有限で、**0になるのは元の整数が0の場合のみ**。負数は非ゼロ側。`INT_MIN/INT_MAX`を含む7点の算術fixtureは付属JSON参照。NaNや±∞は**この整数→0.01倍の経路単体から生成できない**。合法DATの全文到達・別writer・外部メモリ破損・FPU制御ワードまでは含まない。
- L35 この結論は13時台のx87 `0x005510FF TEST AH,0x44` → `0x00551102 JP`がNaNでも真になるというISA解析を否定しない。**NaN分岐は命令上存在するが、この解析器経由の通常スケール入力から直接到達する証拠はない**と範囲を絞る。
- L37 ## 新規増分C：既存Skillのコピーがパーサ実行より先にある
- L39 `0x0046FB00`の直接CALL site **`0x0046FC13` → `0x0046FCE0`**、次いで **`0x0046FC3E` → `0x00599BD0`** の順序をSQLiteで確認。`0x0046FCE0`の擬似Cには、次のビット幅を保つコピーがある。
- L41 ```cpp
- L42 *(undefined8 *)(param_1 + 0x280) = *(undefined8 *)(param_2 + 0x280);
- L43 *(undefined8 *)(param_1 + 0x288) = *(undefined8 *)(param_2 + 0x288);
- L44 ```
- L46 したがって、**この継承／再構築候補ループでは「コピー→設定解析」の順序**が静的に確定する。解析器の対象経路に到達すれば `+0x280` は再度格納されるため、単純な「コピーした値を常に最後までそのまま利用」ではない。ただし解析器が参照する有効プロパティに親設定が含まれるか、ExplicitNull/欠損時にどの値が `iStack_1608` に渡るかは未解決であり、親の数値継承が失われると断定しない。
- L48 別の `0x0051E6F0` にも `+0x280` 書込みが見つかるが、これを同一Skill型と認定できる証拠がないため今回のSkill初期化へ混同せず **TYPE-VERIFY/EXCLUDED** とした。正本で他のwriter・aliasを追う必要がある。
- L50 ## 既存との非重複・限界・次P0
- L52 既存成果：T012 §32のparser倍率、T012 §76の最低ダメージ、13時台のx87フラグ真理値、旧T011の構造体調査。今回の新規対象は **`0x00599860`で初期化を連結、`0x0046FC13`→`0x0046FC3E`のコピー→再解析順、signed-int経路のfinite到達条件**。研究IDの最新版MASTER/HANDOFFとの横断重複照合はPC停止のためVERIFY。
- L54 次はB担当の許可済み範囲で、`0x00599BD0`へ入る `iStack_1608` のdef-useとDAT raw `str`/継承/省略の読み取りを、既保存ASMと照合する。`+0x280`の別writerと `0x0046FB00` の再構築実際到達も確認する。Goldenは無改変原作EXE/旧DAT/SAVE/MAP同一入力・RNG条件で、raw str=省略/0/正数/負数、派生skillによる親上書き、resist index=0/1..9/10、HP/MP/死亡イベント/next tick比較。NaN/∞は合法入力未実証のためGolden-ELIGIBILITY VERIFY。原作Gameplay Golden PASS **0**、strict MATCH **0**、DONE増加 **0**。
- L56 今回のコンテナ保存とreadbackはJSON/MDとも検証。PC `LANE_B_HANDOFF.md`・MASTER・他lane・原本・Git・Work・設定・毎時スケジュールは無変更。次回PC接続後、研究ID/owner/既存拒否/重複/READYを確認して一度だけB所有資料へ同期する。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
