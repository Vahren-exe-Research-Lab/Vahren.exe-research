# 迫真戦記 新B｜T012 Skill倍率の生成・初期化・コピーの連結検証（2026-10-24 14時台）

- 研究ID：`B-OFFLINE-20261024-14H-T012-SCALE-INIT-PARSER-COPY-X87-01`
- 復旧ID：`B-RC-20261024-14H-LOCAL-SESSION-UNSYNCED-01`
- 状態：**OFFLINE-UNSYNCED / STATIC-GHIDRA / VERIFY / NOT READY**。PC正本同期なし／実機Golden PASS 0／strict MATCH 0／新READY 0。

## 実証できた証拠源と接続状況

最初にDesktop Commander Local Compactを試行したが、`INVALID_ARGUMENT: McpServerError: Session terminated`で失敗。分類 **CONNECTION**（安全拒否ではない）。PC最新MASTER、Task Queue、B HANDOFF、22ファイルと未同期10研究、Library訂正版2件の差分は未照合。過去安全拒否領域`0x005710C0..0x00571500`および`0x0058021E..0x00580340`は新規解析対象から除外した。

Libraryの`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（非正本）を取得。SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、計34件のZIP CRCすべてPASS。SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` はBUILD_MANIFESTと一致、`PRAGMA quick_check=ok`。原作EXEの指定SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` はZIP manifest上の記録であり、**ZIPにEXE本体が入っていないため現物再計算ではない**。禁止対象に対する別経路検索は行っていない。

## 新規増分A：生成時の初期値は `0.0`、`str_ratio` 初期値は `1.0`

2026-10-21 Ghidra擬似Cと直接CALL索引で `0x00599600` → CALL site **`0x00599860`** → `0x00599900` を照合。`0x00599900`内部の対象オブジェクト書込みは以下。

```cpp
*(undefined4 *)(unaff_ESI + 0x27c) = 0;
*(undefined8 *)(unaff_ESI + 0x280) = 0;
*(undefined8 *)(unaff_ESI + 0x288) = 0x3ff0000000000000;
```

この初期化経路に限れば、倍率 `+0x280` はIEEE doubleの **+0.0**、比率 `+0x288` は **1.0**。既往T012 §32の「`str_ratio`省略時1.0」と整合するが、**その同じ初期値を作る関数と生成側CALL siteを新たに接続**した。Ghidra擬似Cベースであり、実機で必ずこの初期化関数を経由するという網羅的証明ではない。

## 新規増分B：生成後の解析器は整数→doubleへの倍率上書きを行う

既存T012 §32では、`0x00599BD0`関数内、VA `0x0059CDA3`付近の `FILD [ESP+0x320]` → 0.01倍 → `0x0059CDBC`で `Skill+0x280` 格納まで確認済み（**この旧証拠そのものは再計上しない**）。今回、Ghidraの完全擬似Cで次を独立照合。

```cpp
*(double *)(param_3 + 0x280) = (double)iStack_1608 * _DAT_0063b070;
```

`iStack_1608`は擬似C上の**符号付き32bit整数**。0.01という定数値は過去の原作ASM記録に依存する（このZIPには定数の原作生バイトがない）。この前提で、いずれの32bit整数についても結果は有限で、**0になるのは元の整数が0の場合のみ**。負数は非ゼロ側。`INT_MIN/INT_MAX`を含む7点の算術fixtureは付属JSON参照。NaNや±∞は**この整数→0.01倍の経路単体から生成できない**。合法DATの全文到達・別writer・外部メモリ破損・FPU制御ワードまでは含まない。

この結論は13時台のx87 `0x005510FF TEST AH,0x44` → `0x00551102 JP`がNaNでも真になるというISA解析を否定しない。**NaN分岐は命令上存在するが、この解析器経由の通常スケール入力から直接到達する証拠はない**と範囲を絞る。

## 新規増分C：既存Skillのコピーがパーサ実行より先にある

`0x0046FB00`の直接CALL site **`0x0046FC13` → `0x0046FCE0`**、次いで **`0x0046FC3E` → `0x00599BD0`** の順序をSQLiteで確認。`0x0046FCE0`の擬似Cには、次のビット幅を保つコピーがある。

```cpp
*(undefined8 *)(param_1 + 0x280) = *(undefined8 *)(param_2 + 0x280);
*(undefined8 *)(param_1 + 0x288) = *(undefined8 *)(param_2 + 0x288);
```

したがって、**この継承／再構築候補ループでは「コピー→設定解析」の順序**が静的に確定する。解析器の対象経路に到達すれば `+0x280` は再度格納されるため、単純な「コピーした値を常に最後までそのまま利用」ではない。ただし解析器が参照する有効プロパティに親設定が含まれるか、ExplicitNull/欠損時にどの値が `iStack_1608` に渡るかは未解決であり、親の数値継承が失われると断定しない。

別の `0x0051E6F0` にも `+0x280` 書込みが見つかるが、これを同一Skill型と認定できる証拠がないため今回のSkill初期化へ混同せず **TYPE-VERIFY/EXCLUDED** とした。正本で他のwriter・aliasを追う必要がある。

## 既存との非重複・限界・次P0

既存成果：T012 §32のparser倍率、T012 §76の最低ダメージ、13時台のx87フラグ真理値、旧T011の構造体調査。今回の新規対象は **`0x00599860`で初期化を連結、`0x0046FC13`→`0x0046FC3E`のコピー→再解析順、signed-int経路のfinite到達条件**。研究IDの最新版MASTER/HANDOFFとの横断重複照合はPC停止のためVERIFY。

次はB担当の許可済み範囲で、`0x00599BD0`へ入る `iStack_1608` のdef-useとDAT raw `str`/継承/省略の読み取りを、既保存ASMと照合する。`+0x280`の別writerと `0x0046FB00` の再構築実際到達も確認する。Goldenは無改変原作EXE/旧DAT/SAVE/MAP同一入力・RNG条件で、raw str=省略/0/正数/負数、派生skillによる親上書き、resist index=0/1..9/10、HP/MP/死亡イベント/next tick比較。NaN/∞は合法入力未実証のためGolden-ELIGIBILITY VERIFY。原作Gameplay Golden PASS **0**、strict MATCH **0**、DONE増加 **0**。

今回のコンテナ保存とreadbackはJSON/MDとも検証。PC `LANE_B_HANDOFF.md`・MASTER・他lane・原本・Git・Work・設定・毎時スケジュールは無変更。次回PC接続後、研究ID/owner/既存拒否/重複/READYを確認して一度だけB所有資料へ同期する。
