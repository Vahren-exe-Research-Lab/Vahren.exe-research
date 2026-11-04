# 迫真戦記 新B｜T012/T013 空間セル移動・候補列挙順の新規静的解析（2026-10-23 07時台）

**研究ID** `B-OFFLINE-20261023-0716-T012-T013-SPATIAL-CELL-MIGRATION-01`  
**接続復旧ID** `B-RC-20261023-0716-LOCAL429-01`  
**owner** B / T012（当たり判定に先行する空間管理）・T013（候補集合の順序）。T011のフィールド解釈に依存。T024/T028の新規研究は今回なし。  
**区分** `OFFLINE-UNSYNCED / STATIC-EXE-ASM / STATIC-SQLITE / STATIC-PSEUDOC / STATIC-DERIVED / VERIFY / NOT READY`

## 1. 起点・復旧優先・証拠源

- 最初にDesktop Commander Local CompactでPCの `MASTER_LEDGER.md`・`ANALYSIS_LANES_PROTOCOL.md`・`LANE_B_HANDOFF.md` の読取を試みたが、実エラー `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。分類は **CONNECTION** であり、安全拒否ではない。Remote・別シェル等で拒否済み操作を迂回せず、PC書込なし。
- B回収索引 `T011_T012_T013_T024_T028_UNSYNCED_RECOVERY_REGISTER_20261020.md`、Bの06:08研究、根拠JSONおよびB既存成果を照合。既存 `B-RC-20261023-0213-LIBRARY-OVERWRITE-CONTAINER-01` の02:13訂正版上書きは **未解決**、同じ失敗操作の再試行をしなかった。既知安全拒否の対象（`0x5710C0..0x571500`、`0x4C5CC0`等）は再調査しない。
- Library根にある `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren.exe` を取得。ZIP34ファイルのCRC PASS、同梱 `search.sqlite` の quick_check `ok`。SHA256はEXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、SQLite `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` で既知manifestに一致。Ghidra/REA再解析や原作実行はしない。
- Library単体MASTERは既知 checkpoint187 の古い複製、ZIP研究snapshotは記載上 checkpoint195。**PC上の現行MASTERは未確認**。そのためREADYや重複の最終照合・正式同期はしない。

## 2. 新発見：`0x004BCA30` は「現在のセル」と「移動先のセル」を比較し、異なる場合だけ移籍させる

前回06:08の `0x004BC920` は矩形中心を用いた空間セルへの初回登録と `object+0x54` の値保存を確認済み。今回は **未登録の別関数 `0x004BCA30`** の機械語を原作EXEから直接確認した。

| VA | 原作ASMで検証した操作 | 状態 |
|---|---|---|
| `0x004BCA37` | `MOV EDX,[EBP+0x28]`：空間コンテナのマスク値 | STATIC-ASM |
| `0x004BCA40..0x004BCA56` | object `+0x40/+0x48/+0x44/+0x4C` の矩形中心を計算（算術右シフト） | STATIC-ASM |
| `0x004BCA58..0x004BCA6A` | 現在中心座標と渡された移動先座標に同じマスクを適用 | STATIC-ASM |
| `0x004BCA6E` / `0x004BCA72` / `0x004BCA74` | x・yの両方が一致なら `JE 0x4BCB22` へ抜ける | STATIC-ASM |
| `0x004BCA7D → 0x004BC3C0` | **現在セル**を `create=0` で取得し、該当objectがあれば除去 | STATIC-ASM＋引数解釈STATIC-DERIVED |
| `0x004BCAC4 → 0x004BC3C0` | **移動先セル**を `create=1` で取得して登録 | STATIC-ASM＋引数解釈STATIC-DERIVED |
| `0x004BCB14` | 移動先のポインタ配列の終端を4バイト前進 | STATIC-ASM |
| `0x004BCB18..0x004BCB1F` | コンテナ `+0x08` を増加し、同じ値を `object+0x54` に記録 | STATIC-ASM |

この関数は単なる「座標が変わるたびに全登録を作り直す関数」ではない。**マスクをかけたセル座標が変わらなければ、セル配列にも `object+0x54` にも変更しない**。マスクの実行時値とセルサイズの確定はVERIFY。

## 3. 旧セルからの削除は swap-with-last：候補順序は安定しない

`0x004BCA98..0x004BCAB4` は、旧セルのvector内から対象ポインタを線形検索する。該当する場合、`0x004BCAA4` で末尾ポインタを読み、`0x004BCAA7` で見つかった位置を**末尾ポインタで上書き**した後、`0x004BCAB1..0x004BCAB4` で終端を4バイト戻す。元の順序を維持する配列シフトは行わない。

この削除の構造は既存 `0x004BC9C0` の処理とも整合する。ただし `0x004BC9C0` 単体の発見は既存B成果（2026-10-13）に含まれるため **今回の新発見には計上しない**。今回の独立した増分は、**`0x004BCA30` がセル越境時にこの不安定順序の削除と新セル登録を結合していること**。

例えば1セルの順序 `[A, B, C]` で A が別セルへ移動すると、残る順序は `[C, B]` になり得る。これが接触時の最終採用候補を変えるかは、後段の候補収集・ソート/選択の有無が未確認のため **VERIFY**。前回の「tree中順走査」の順序を、このvector順と同一視してはいけない。

## 4. 移動関数の呼出元も照合：旧矩形更新より前にセル移籍が走る

SQLiteの直接CALL索引と原作E8 rel32の照合で `0x004BCA30` への呼出を **5 site** 確認した：

- `0x004C5D7E`（caller `0x004C5D50`）
- `0x004C5F12`（caller `0x004C5EF0`）
- `0x004C6117`（caller `0x004C60F0`）
- `0x004C62C5` と `0x004C635E`（caller `0x004C6290`）

うち `0x004C5D50` は `0x004C5D7E` で移動先の矩形中心を渡して **セル移籍を先行**し、`0x004C5D96 / 0x004C5DA2 / 0x004C5DA5 / 0x004C5DA8` で矩形境界（`+0x48/+0x4C/+0x40/+0x44`）を更新する。同様に `0x004C6290` の `0x004C62C5` は、物体の矩形を次位置へ更新する前に呼ばれる。

したがって `0x004BCA30` では、現時点の旧矩形から **旧セル**を決定し、引数に渡された次位置から **新セル**を決定する順序と読める。擬似C単独では暗黙レジスタ引数の型が失われるため、E8・レジスタ/スタック・分岐を原作ASMで照合した。`0x004C5CC0` など過去に安全拒否のあった別領域は触れていない。

## 5. `object+0x54` は不変の個体IDではない（T011/T012に重要）

既存10/13 B資料は `0x004C3DC0` と `0x004BC920` が同一オブジェクト `+0x54` を上書きし得ることを記録済み（既存成果）。今回は更に、**セル越境のたび `0x004BCA30` がコンテナ `+0x08` の増分値を同フィールドへ書き戻す**経路を直接確認した。

その一方、同じセル内の移動では早期ジャンプして書き戻さない。よって `object+0x54` を「不変の個体ID」「座標更新ごとのカウンタ」「画面フレーム番号」と固定して再実装する根拠はない。局所的には**登録時またはセル越境時に更新されるstamp**と呼ぶのが安全。実際の全writer、比較reader、スコア書込との優先関係はVERIFY。

## 6. 検証・重複・Golden設計

- 本回の追加検証コードでは、原作EXEの重要ASM **21/21 byte anchor一致**、E8から計算した呼出先とSQLite索引 **7/7一致**、該当Ghidra擬似Cの再計算SHA **4/4一致**、SQLite quick_check `ok`。BINとSQLiteのSHAも一致。対象は `0x004BCA30,0x004BC9C0,0x004C5D50,0x004C6290` などの許可範囲のみ。
- セルマスクを **仮の** `0xFFFFFFE0` とした合成6例（同セル2、x/y越境2、負座標越境1、swap-back除去1）PASS。これは想定値の条件モデルであり、原作でこのマスクが使われると証明したものではない。
- 既存確認：06:08研究は `0x004BC920` 初回登録とキュー境界を中心に扱った。2026-10-13以前のB資料には`0x004BC9C0`と`+0x54`多重writerが既出。今回の**新規増分**は`0x004BCA30`の「マスク一致時スキップ／旧セルswap-back削除／新セル登録・stamp更新」および5つの呼出元。B HANDOFFスナップショットで関数VAの記述を照合したが、最新PC正本への完全な重複照合はできない。
- 実機Golden 0、strict MATCH 0、正式READY 0、Task DONE増加0。原作を実行していない。

**Golden設計（NOT RUN）**：同一EXE、DAT、MAP、SAVE、tick、RNG、入力で、単体移動が「同セル」「セル境界越え」「負座標境界越え」に分かれる配置を作る。セルごとのobjectポインタ列の順序、`grid+0x08`、`object+0x54`、最終接触候補、命中対象、HP・状態・RNGを同じ内部ステップで観測する。3体以上同セルで先頭/中間/末尾の移動除去を区別し、swap-back後の候補選択が後段で並び替えられるか確認する。

## 7. 次の許可された一手・保存状態

- **P0次回**：`0x004BC4F0` の空間セル列挙から、`0x004E6D10` など実際のミサイル接触候補探索との接続を限定的に調査する。`grid+0x28`の初期化と `object+0x54` readerを調べ、セル順序が本当に最終対象へ作用するかVERIFY。T024/T028はP0維持。0x5710C0..0x571500その他既拒否コマンドには触れない。
- **安全・権限**：原本EXE、ZIP、SQLite、SAVE、他lane、REA queue、Git、MASTER、スケジュールは読取専用または不操作。B所有の研究本文・証拠JSON・検証Pythonのみ別名作成し、Library B `data/` に書ける場合だけ保存する。PC側のB HANDOFFへの同期はLocal復帰後に owner/ID/重複/競合/READY の再照合後、一度だけ実施する。MASTER反映はE担当。
- **現時点の保存・readback**：本文・JSON・検証コードを作成。Library保存/readbackの最終実績は別途実際に操作・SHA確認した場合にのみ報告する。過去02:13のLibrary訂正版は未解決のまま引き継ぐ。
