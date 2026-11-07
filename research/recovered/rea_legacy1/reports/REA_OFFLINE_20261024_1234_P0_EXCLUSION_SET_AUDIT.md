# 迫真戦記 ver0.67｜REA独立 P0：候補除外ツリーの引数伝播と誤認しやすい挿入呼出の分離

- 研究ID：`REA-OFFLINE-20261024-1234-P0-EXCLUSION-SET-PROVENANCE-STATIC-01`
- 時刻：2026-10-24 12時台 JST（オフライン研究）
- 分類：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 対象：`0x0048F720`, `0x0048F9E0`, `0x00490180`, `0x00493630`, `0x00498EE0`, `0x004868D0`, `0x00488290`, `0x00489630`, `0x00489DB0`

## 0. 事前確認と証拠の限界

Desktop Commander Local Compactで Windows 正本の MASTER、レーン規約、REA README/QUEUE/PROGRESS、検索基盤 README/BUILD_MANIFEST の計7ファイルを `read_multiple_files` で読み取ろうとしたが `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated` で接続失敗。これは接続障害（CONNECTION）であり安全拒否ではない。Windows PC の稼働状態・CPU/RAM・active.lock・最新所有者・最新run・正本との競合は不明。Remote、Work、その他迂回は行っていない。

Library で現物確認した `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe` を、解析コンテナのコピーとして読み取り専用で使用。EXEは起動も変更もせず、旧SQLiteは ZIP からメモリ内へ `sqlite3.deserialize` で開いた。ZIP CRC 34/34、SQLite `PRAGMA integrity_check=ok`、EXE・ZIP・DB・BUILD_MANIFESTのSHA256が一致した。Ghidra/REA/ゲームは起動していない。

ソースSHA256：EXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、ZIP `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP内旧SQLite `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。

**重要：参照したのは内部10,268関数の旧スナップショット。** Libraryの `HAKUSHIN067_CURRENT_GHIDRA_HANDOFF_20261021.md` に記載されたPC正本は内部10,274関数の `HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`（記載SHA256 `282924553309C4778FF6C5D5346CCF5C2BCB1B6FD17E46DBBAE9031547453F8D`）であり、**本runでは未入手・未照合**。今後の正本同期時に再検証する。

## 1. 新規増分A：除外用コンテナは複数の上位ヘルパーに別引数で渡される

従来の `0x0048F720` について、`0x48F73C MOV EDI,[EBP+0x1EED34]` は比較用木構造のヘッダを参照し、`0x48F752 CMP [EAX+0x0C],ESI` → `0x48F755 JAE` で符号なしキー比較、`0x48F786 CMP [EAX],EDI` でメンバーシップ判定が確認できる。これは既知の比較ロジックであり新規発見として再加算しない。

今回の新規追跡は、その**比較用コンテナ構造体のアドレス `context+0x1EED30` がどの上位呼出へ渡されるか**にある。

| 経路 | 根拠の PE VA | 静的に言えること |
|---|---|---|
| `0x0048F9E0 → 0x004868D0` | `0x49010D LEA ESI,[EBP+0x1EED30]` → `0x490113 PUSH ESI`、`0x490114 LEA EDI,[EBP+0x1EED20]` → `0x49011A PUSH EDI`、`0x490122 CALL 0x4868D0` | 除外用マップと外側候補マップが**別々のスタック引数**で渡される。戻り値ALは`0x490127 TEST AL,AL`で判定。 |
| `0x00490180 → 0x00488290` | `0x4901EA MOV EAX,[ESP+0x18]` → `0x4901EE CMP EAX,EBX` / `0x4901F0 JE`、`0x49020B LEA ECX,[ESI+0x1EED30]` → `0x490211 PUSH ECX`、`0x490212 PUSH EBP`、`0x49021A CALL 0x488290` | 選択したオブジェクトの非NULL判定を行い、比較用マップと候補マップを別引数でヘルパーへ渡す。ここでの `EBP` は先行 `LEA [ESI+0x1EED20]` に由来する。 |
| `0x00488290 → 0x00489630 → 0x00489DB0` | `0x488C44 CALL 0x489630`、`0x48977F CALL 0x489DB0` | 補助処理へ継続する CALL は確認できたが、**比較用マップ自体への書込ではない**。引数再配列とエイリアスの追跡が残る。 |

**新しい点**：単に `context+0x1EED34` の読み手を列挙するのではなく、候補集合・除外集合が2つの主要ヘルパーの呼出境界を超えて渡されることを実命令で確認した。関数名は機械生成名であり、具体的なゲーム上の役割を過剰に命名しない。

## 2. 新規増分B：`0x00493630 → 0x00498EE0` の2箇所はグローバル除外木への書込みとは判定できない

`0x00493630` は比較用木構造を参照するため、周辺にある木への挿入関数 `0x00498EE0` を「`context+0x1EED30`の書込元」と誤認しやすい。しかし呼出直前のPE機械語で EAX を追跡すると以下が成立する。

- `0x493AB6 CMP [ESP+0x20],1` → `0x493ACD LEA EAX,[ESP+0x7C]` → **`0x493AD1 CALL 0x00498EE0`**。
- `0x493AD6 CMP [ESP+0x20],2` → `0x493AED LEA EAX,[ESP+0xA0]` → **`0x493AF4 CALL 0x00498EE0`**。

いずれも EAX は **この関数のスタック上の一時領域を指す**。`0x00498EE0` 側が暗黙の EAX に格納されたコンテナを更新する形式と整合する。よってこれら2箇所だけを `context+0x1EED30` の直接 writer と記録するのは誤り。スタック一時領域と比較木が間接的に同一実体を参照するかは未証明であり、全データフローの完全否定までは主張しない。

また `0x00489DB0` 内の `0x489E08 LEA EBX,[EDI+0x88]` → `0x489E1B CALL 0x005158E0` と、`0x489E24 LEA EBX,[EDI+0x98]` → `0x489E37 CALL 0x005158E0` は**オブジェクト相対の2つの内包マップ**への挿入候補である。`EDI` が `context` と同一か、比較集合に別途エイリアスするかが未確認なので、これらも `context+0x1EED30` への直接 writer として昇格しない。

これが今回の偽陽性排除（negative static evidence）である。書込元の確定は未解決 VERIFY。

## 3. 独立再検証（選定した点検のみ）

独立監査 `verify_rea_20261024_12h_exclusion_set_provenance.py` を作成し、ZIP内SQLiteをRAMで開き、EXEのPE32セクションテーブルからVAを実バイトに写像、指定命令・E8 rel32 CALL・SQLite登録CALL・疑似Cハッシュを再照合した。

- EXE/ZIP/DB/manifestとZIP CRC：**6/6 PASS**
- 指定PE命令：**30/30 PASS**
- E8直接CALL先：**8/8 PASS**
- SQLite整合性：**1/1 PASS**
- 対象9関数の疑似Cハッシュ：**9/9 PASS**
- SQLite直接CALL索引：**8/8 PASS**
- **計62/62 PASS**。これは62関数完了という意味でも、原作実測Goldenでもない。

監査対象E8 CALL site は `0x490122→0x4868D0`, `0x49021A→0x488290`, `0x493AD1→0x498EE0`, `0x493AF4→0x498EE0`, `0x488C44→0x489630`, `0x48977F→0x489DB0`, `0x489E1B→0x5158E0`, `0x489E37→0x5158E0`。間接CALL先の正式同定、関数境界全域、例外return、完全なABI、現行10,274関数DB差分は今回未完了。

## 4. REA正式・未解決・Golden

正式5種 `info/pseudo/assembly/callers/callees`：旧SQLiteは9関数のinfo/機械生成pseudo、CALL参照の索引を含むが、assembly は今回**指定箇所のみ**。正式REAの独立5種エクスポート一式をこのrunで完成した関数は**0件**。新規 `VERIFIED=0`、既存Wave1～5 `64/64` は過去報告であり**PC正本で未再確認**、加算しない。ZIP同梱の旧10月9日 `15/16` とは時点と分母が違う。正式QUEUE/PROGRESSへの変更はなし、`TODO/VERIFY/BLOCKED` **書込差分0/0/0**、オフラインVERIFY論点は継続。原作Golden実機 PASS **0件**、strict MATCH **0件**、完全複製率**未測定**。

新規Ghidra実行0、REA実行0、ゲーム起動0、Work0。監査単体実行時間は機械可読JSON参照。研究全体の所要時間とPC CPU/RAMは不明。

## 5. PC復旧時の安全な再開位置

1. 最新MASTER/レーン規約/REA README・QUEUE・PROGRESS・runs/evidence・owner・lockを先に読み、今回IDと前回10/11時台IDの重複・競合を確認する。
2. PC現行 `HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite` と `search_current.py` をread-onlyで開き、本報告の9関数と8 CALL site・ABI/例外分岐を差分検証する。旧DBを正本と誤認しない。
3. `0x004868D0` および `0x00488290` で`context+0x1EED30`と`+0x1EED20`がどの引数へ再配置されるか、実際の書込元があるかを追跡する。特に `0x00489630` / `0x00489DB0` の所有オブジェクトと集合間エイリアスを検証する。
4. 比較木のキーの追加・削除条件を得たら、`0x0048F720` の「すべての候補が除外される」到達条件、正常・例外returnを検証し、将来のGolden試験ケースにする。静的検査をGolden PASSと混同しない。

**接続障害ID**：`REA-RC-20261024-1234-LOCAL-SESSION-TERMINATED-01`。対象は先読み7ファイルとWindows正本同期。理由は Local MCP session terminated。未保存なのは今回のWindows正本統合・最新競合照合。許された次手は正本接続後のread-only照合→REA所有範囲のみ重複なく一度同期。安全拒否ではない。今回のオフライン成果は独立ファイルで保存するが**Windows正本未同期**とする。
