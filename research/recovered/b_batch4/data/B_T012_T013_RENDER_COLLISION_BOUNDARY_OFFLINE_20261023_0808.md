# 迫真戦記 ver0.67｜B担当 T012/T013 空間候補列挙の用途分離（2026-10-23 08:08 JST）

**研究ID** `B-OFFLINE-20261023-0808-T012-T013-RENDER-COLLISION-BOUNDARY-01`  
**owner** B / T012・T013（T011参照、T024/T028新規解析なし）  
**状態** `OFFLINE-UNSYNCED / STATIC-EXE-ASM / STATIC-SQLITE / STATIC-PSEUDOC / STATIC-DERIVED / VERIFY / NOT READY`  
**前回研究ID** `B-OFFLINE-20261023-0716-T012-T013-SPATIAL-CELL-MIGRATION-01`

## 1. 接続・回収・禁止領域

Desktop Commander Local Compactによる `MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、`LANE_B_HANDOFF.md` ほかの同時読取は `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。これは CONNECTION（安全拒否とは別）。PC正本/最新checkpoints/READYは未確認。既存拒否範囲 `0x5710C0..0x571500`、既拒否 `0x4C5CC0` と関連拒否操作は再試行しない。

代わりにLibraryルートの `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（19,646,444バイト）および `Vahren.exe`（2,910,720バイト）を正規に取得。ZIP 34件CRC成功、SQLite `PRAGMA quick_check=ok`。原本ZIP/EXE/DBは読み取り専用、原作実行・変更・公開なし。検索DBおよび擬似Cの抽出済み資料だけを活用し、Ghidra/REAの再解析は実施していない。

- ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`
- EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（指定値に一致）
- SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（manifestに一致）

## 2. 新規分析：`0x004BC4F0` のセル列挙は**描画向け**、最終攻撃対象決定とは未接続

07時台の次候補 `0x004BC4F0` を原作ASM・SQLite・Ghidra擬似Cで調べた。直接呼出元はSQLiteでは **1 site**：`0x004C4142`（`0x004C3EB0`）。この上位関数には `D3DXMatrixTranslation` / `D3DXMatrixMultiply`、Direct3D状態設定、`0x004C41A0 → 0x004C4850` の描画バッチ生成が存在する。`0x004C4850` はオブジェクト仮想関数 `+0x48 / +0x1C` を用いて頂点データを生成し、グラフィックスバッファへ送る処理に相当する（STATIC-PSEUDOC、個々のDirect3D API名は解析資料に依存）。

`0x004BC4F0` 内部で直接確認した条件・CALL：

| 位置 | 振る舞い | 根拠 |
|---|---|---|
| `0x004BC531..0x004BC542` | 7個・16byte/個の管理vectorを静的領域 `0x00B036B8` に構築 | ASM |
| `0x004BC5EB → 0x004BC3C0` | セルを取得し、セル内ポインタvectorを走査 | ASM＋擬似C |
| `0x004BC635` | 候補オブジェクト `+0x64` と任意フィルタ callback を検査 | ASM＋擬似C |
| `0x004BC64D..0x004BC676` | 候補矩形 `+0x40/+0x44/+0x48/+0x4C` と描画矩形のAABB交差 | ASM |
| `0x004BC67C..0x004BC68B` | 仮想スロット `+0x40` の戻り値に3を加え、vectorの振り分け先と特別処理を選択 | ASM |
| `0x004BC691..0x004BC6A6` | 戻り値0の特別分岐では仮想スロット `+0x38/+0x3C` の値を `object+0x04/+0x08` に保存 | ASM |
| `0x004BC8DE` | 比較関数 `0x004BBC60` のポインタをpush | ASM |
| `0x004BC8E9 → 0x0047BB50` | **特別なvector `0x00B036E8` だけ**を並び替える | ASM＋擬似C |

`0x004BBC60` は2つのオブジェクトの`+0x04`を**符号付き比較**し、一致なら`+0x08`を**符号付き比較**する辞書順の比較器。命令 `0x004BBC6F CMP EAX,ECX`、`0x004BBC7C SETL AL`、`0x004BBC84 SETL AL`で確認。いずれも等しい場合は両方向とも偽になるが、**同値オブジェクトの安定順序はまだ証明できない**。また、この関数に明示的なsortがあるのは特別なvectorのみ。他bucketにも同じsortを適用しているとは言えない。

### 07時台からの修正・注意

07時台は「空間セル列挙から接触最終対象決定へ追う」として `0x004BC4F0` を優先した。しかし今回の直接CALLと描画経路の検証により、この関数を**当たり判定の本体とみなすことはできない**。この限定をBの新証拠として残す。以前のセル越境swap-with-lastによる **セル配列順序変化** のSTATIC結果は維持するが、それを**命中順序の変化**に直結させない。

一方、以前からのミサイル接触候補探索 `0x00515470 → 0x004E6D10` は `0x00515477` で `Skill+0x134` を検査し、`0x00515489` で `0x004E6D10` を呼び出す**別の入口**。SQLite直接CALLでは `0x004BC4F0` の直接callerは `0x004C4142` のみ、`0x004E6D10` は `0x00515489` のみ。**直接CALL上の経路が別**なのはSTATIC-SQLITE＋STATIC-ASMだが、共有オブジェクトや間接参照を経て連携する可能性を排除できるわけではない（VERIFY）。

## 3. 検証

独立検証用Pythonは標準ライブラリでPEヘッダとsection/RVAを読取り、実EXEから期待バイトを抽出し、`E8 rel32`の呼出先を復号。SQLiteは `mode=ro` で読む。対象5関数の擬似CをDB収録ハッシュと再照合した。

- 原作EXE SHA一致、検索DB SHA一致、SQLite quick_check `ok`。
- 24箇所のopcode anchor **24/24 PASS**。
- 直接CALLサイトの原作E8復号とSQLite索引 **6/6 PASS**。
- Ghidra擬似Cの再ハッシュ **5/5 PASS**。
- 間接vtable先の完全復元、画面描画順と実際の攻撃対象順との一致：**未検証**。
- 原作Golden PASS **0**、strict MATCH **0**、READY **0**、DONE増加 **0**。

## 4. 未同期・未保存回収

07時台までの B 新研究は最新PC正本への未同期のまま。`B-RC-20261023-0213-LIBRARY-OVERWRITE-CONTAINER-01`、`B-RC-20261023-0417-LIBRARY-CORRECTION-STILL-UNSYNCED-01` は重複統合しない。02時台訂正版2本について、Library実体を本回再取得し、SHAが従来初回版（`FF33D37B...`／`AC237A16...`）のままと確認。ローカル訂正版は`8FF22164...`／`FABE16F2...`。本回、コピー/マテリアライズが正常化した状態を確認してB所有2件だけ同名上書きを一度試したが、**ともに `container_session_unavailable: No active container session was found for container_path.` で失敗**。同操作をさらに反復せず、既存未反映案件のまま維持。対応RECOVERY-IDは別記録 `B-RC-20261023-0808-LIBRARY-CORRECTION-STILL-FAILED-01`。

本研究のファイル保存先・Libraryへの実アップロード/readback結果は別保存レシート、または当回報告で実績のみ記載する。PCのB HANDOFF、MASTERは未変更であり、Eの正式統合はしていない。

## 5. 次の未解明P0 / 再開点

1. **T013**：`0x00515470 → 0x004E6D10` のmanagerが保持する候補treeのノード登録元と順序を、空間セルvectorとは独立に辿る。候補の反復順（tree order / 登録順 / 早期return）をASMで検証。`0x004BC4F0`は直接の命中候補入口ではないので再調査を繰り返さない。
2. **T012**：ヒットが確定してからHP/MP/状態効果・死亡へ到達する実際のCALL/間接先、RNG消費の境界。`0x5710C0..0x571500`の既拒否場所への迂回解析はしない。
3. **T011**：`object+0x54` stampのreader群と `grid+0x28`マスク初期化、Skill `+0x134/+0x1FD`のwriter範囲。
4. **T024/T028**：戦闘AIの最終対象選択、士気・敗走は今回未着手のP0維持。

**Golden NOT RUN条件**：同一原作EXE/DAT/MAP/SAVE/tick/入力/RNGで、同セル複数オブジェクト、key(+4,+8)同点/相違、描画矩形と命中対象矩形を区別。旧セルswap-back後の描画バケット順と、`0x004E6D10`候補treeの反復順、実際の攻撃対象、HP/RNGを別々に記録する。フレーム描画のソートと戦闘命中を取り違えない。
