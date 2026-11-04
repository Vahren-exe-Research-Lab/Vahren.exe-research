# 迫真戦記 ver0.67｜B/T011・T024：group+0x34 の二系統集計と適格Unit判定（2026-11-01 11H JST）

**研究ID**：`B-OFFLINE-20261101-11H-T011-T024-GROUP34-DUAL-BUCKET-GATE-01`。**owner** B／**tasks** T011, T024。**状態** `OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。原作実機Golden PASS=0、strict MATCH=0、DYNAMIC=0、新規正式READY=0。T013最終対象・T028士気・敗走への影響はVERIFYに留める。

## 1. 証拠源・接続・未同期の回収

最初に許可済み `Desktop Commander Local Compact` で PC正本 `MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、`LANE_B_HANDOFF.md`、`knowledge/README.md`、`SYNC_STATUS.md` の読取を試行したが、`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。**接続のレート制限**であり安全拒否ではない。最新PC正本、担当範囲の新しい変更、03H書込の実在・SHAは未確認。

ChatGPT Libraryの `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256=`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`（34件CRC正常）、`HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3.zip` SHA256=`059B91381C1B58214353769006E0F4049FCDE393A6B7970F4513602878A2B2C9`（136件CRC正常）、`Vahren.exe` SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` を独立確認。pack内 `search.sqlite` SHA256=`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（readonly quick_check=ok）。**原作EXEは起動せず、再Ghidra解析せず、保全元ZIP/SQLite/原本に書き込んでいない**。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` はGitHub接続上で読取成功、先端SHA=`0225b2e1cd5c710137a3d921f593d158df06624a`。先行 `symbols.tsv`（blob SHA `3fcf2d436c21f3fc91791a91e75c9a800167ca4d`）、`structs.tsv`（`d79f03b1dbac67012882b0cb691d6af479610a01`）、`REF_BATTLE_AI_MORALE.md`、`GHIDRA_V9_B_REVIEW_TOP150.tsv`、`KNOWLEDGE_CURATION_PROTOCOL.md` を照合し、対象関数名の承認済み辞書登録は確認されなかった。PC最新研究全文の重複否定は不能。前回10Hで指摘された `0x528DB0` 二つのsinkを今回検証したので、10H発見の `0x569360` 近接式は再計上しない。

保全の現状：03H PC書込み結果 **UNKNOWN**、04H成果はこの会話のファイルとして存在、05〜10HのHANDOFF差分等24/24件は保存済みSHA台帳とこの作業環境の再読取で一致。07Hの4件はマップ型台帳として検査。**04〜11Hの研究PC同期未実施**。既存SAFE134は過去スナップショットであって現行全件再検証済みではない。安全保留21件は維持し、新規拒否と混同しない。10HのLibrary保存済資料5件は継承。

## 2. 新規STATIC：グループの適格判定 `0x569610`

Ghidra原文 `functions/0056/00569610.c`（SHA256 `80F9A75DC7C6C2121A5FB6CCD8C6667BF35E703B96B01CDBC4A305E06C318CFE`；該当擬似C 24〜39行付近）と原作x86命令を照合。入口 `0x569610` は `group+0xC/+0x10` のUnitポインタ配列を走査し、以下の**5条件すべて**を満たすUnitが1体でも存在すれば `AL=1`（`0x56966D`）、なければ `AL=0`（`0x56965F`）で復帰する。

| 位置 | 原作命令VA | 条件（静的証拠） |
|---|---|---|
| Unit+0x1867C | `0x56962A` | byte == 0 |
| Unit+0xD0 | `0x569633` | signed dword >= 0 |
| Unit+0xC0 | `0x56963C` | signed dword >= 0 |
| Unit+0xC8 | `0x569645` | signed dword >= 0 |
| Unit+0x1867E | `0x56964E` | byte == 0 |

**10Hの `0x569360` の近接判定は `+0x1867C/+0x1867E` の2条件であり、11Hの `0x569610` はさらに符号付き3フィールドを要求する。** 両者を同じeligible集合として実装しない。これらのフィールドの正式ゲーム内名称、0件・不整合vectorでの詳細挙動はVERIFY。原作の `0x52906D -> 0x569610` 直接E8を検証した。

## 3. 新規STATIC：`0x528DB0` は group+0x34 を2つの異なる集計器へ振り分ける

対象関数入口 `VA 0x528DB0`、Ghidra `functions/0052/00528DB0.c` SHA256=`A2444391476AF79BF31F64465B3D344C30EA3E499E9D722D5D01F11D639CBEBC`（擬似C **167〜220行**相当）。この集計部は外側の `param_2+0x34C != 0` かつモードフィールド `param_2+0x474` が0・4でない経路にある。グループ候補は `0x52906D -> 0x569610` のAL真が必要（`0x529072/0x529074` でALをテスト）。

分岐を決めるのは、先頭Unitに関連するデータ `Unit+0x1C8` が指す領域の `+0xE8` と、`0x529043` の整数変換結果を96 (`0x60`) と比較する `0x52904C/0x529057` のフラグである。

- **第1集計系**：`0x52908A` で関連 `+0xE8 == 0`、かつ `0x529093` でローカル比較フラグ==0のとき、`0x5290A2 -> 0x5299E0` の補助処理後、`0x5290A7: mov eax,[esi+0x34]` と `0x5290AA: add [esp+0x18],eax` で合計Aに加算。`0x5290B2` は第2系を飛び越す。
- **第2集計系**：上記のどちらかが成立しない場合、`0x5290BE -> 0x4C52D0` によるリスト登録経路を通り、成功経路 `0x5290DD: mov edx,[esi+0x34]` と `0x5290E0: add [esp+0x20],edx` で合計Bに加算。リスト追加上限チェック・例外経路あり。
- **平均のゼロ件ガード**：`0x529100/0x529104` はBの件数が0なら合計Bを0へ、非0なら `0x529114..0x52911B` で**符号付きIDIV**を実行。Aについても `0x52911F/0x529125` が件数0なら合計Aを0、非0なら `0x52912B..0x529134` で符号付きIDIV。これらは**独立の整数平均**であって合計を一緒に割る処理ではない。

**訂正**：10Hでは `0x5290A7` と `0x5290DD` を「group+0x34の別用途」とだけ記録。11Hでは**同一関数の二分岐に排他的に投入される別々の合計A/Bと各自の件数ガード付き整数除算**に確証を絞った。隊列・移動・戦闘AIへの最終的な意味、ソート/登録の前提、符号付き加算オーバーフロー、FPU丸め、後続レイアウトの座標はVERIFY。

## 4. 10H近接判定の後続：薄いアダプタと間接推論の限界

前回からの未解明 `0x56ADE9 -> 0x569700` に続き、今回 `0x56971A -> 0x569730` の原作E8を検証した。`0x569700`（Ghidra `functions/0056/00569700.c` SHA256=`84DDC661A52B3644CE16B0CD420369288FBD0A4961BB954B2A52019ABACFA688`）はパラメータを並べ替え、`push 0` を追加して `0x569730` へ転送する**小さなアダプタ**。`0x569730`（SHA256=`00AA3D5B6B120CBCCEA02A483BD1E423D30DBEB3C98B84E7F34026E2ABF41EB2`）は群のUnitを走査し、Unit+0x1867Cを検査して処理するが、実ゲームの移動完了や攻撃対象確定はここからは証明できない。

## 5. 検証・Golden仕様・KB_CANDIDATE

検査スクリプト `data/B_20261101_11H_GROUP34_DUAL_BUCKET_READONLY_VERIFY.py` は**特定41命令窓・5件のE8サイト・4つの擬似C SHA一致・SQLite quick_check・ZIP CRC**等を検査し、**60/60項目PASS**（合成/静的検査であり実機Goldenではない）。証拠JSON `data/B_OFFLINE_20261101_11H_GROUP34_DUAL_BUCKET_EVIDENCE.json` は各VAのnative bytes/SHA、各CALL、擬似C相対path/SHA、原作SHA、未検証を保持。今回も禁止VA `0x5710C0..0x571500` と過去拒否操作を調べたり迂回したりしていない。

Goldenの前提：同一原作EXE、DAT/MAP/SAVE、同一Unit/Group構成・先頭Unit、3つのsignedフィールド、group+0x34の正負/境界値、`0x529043` の整数変換結果（95/96境界）、UnitDef+0xE8の0/非0、両リスト件数0/1/2、オーバーフロー/負のIDIV境界、`0x569610` のAL、二つのリスト生成結果・最終行動・呼出順/乱数を実機で採取し、新規実装と厳密に比較。未実測なのでGolden0／strict MATCH0／READY0。

**KB_CANDIDATE（統合専任の判断待ち、非自動確定）**：owner B/T011,T024、研究ID上記、VA `0x569610`, `0x528DB0`, `0x569700`, `0x569730`、CALL `0x52906D -> 0x569610`, `0x5290A2 -> 0x5299E0`, `0x5290BE -> 0x4C52D0`, `0x56ADE9 -> 0x569700`, `0x56971A -> 0x569730`、group `+0x34`、Unit `+0x1867C/+0x1867E/+0xD0/+0xC0/+0xC8/+0x1C8`、先頭Unit定義 `+0xE8`。**STATIC**=機械語・SHA・CFG・符号付き除算、**INFERRED**=2系統の配置評価という機能仮説、**VERIFY**=後続副作用・実機丸め・保存条件・対象選択、**NOT READY**。候補は共有KBやGitへ担当Bから直接書かない。

**次の再開**：PCが復帰したら最優先でMASTER/PROTOCOL/HANDOFF/安全保留の現物照合、03Hファイル有無/実SHA、04〜11Hの未同期資料の重複・競合・元SHAを確認し、B許可資料に一度だけ取り込んで独立readback。PCが不通なら `0x5299E0` によるA側件数の成立、`0x52911F` 以降の平均値消費先、`0x569730` の派生Unit行動とT013最終対象選択を追う。T011召喚・経験値、T012ダメージ・回復・状態、T024戦闘AI全体、T028士気・敗走のP0は未解明のまま維持。
