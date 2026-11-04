# 迫真戦記 ver0.67｜REA独立静的調査：ArmyChipBuilder子配列の生成・破棄境界
研究ID: `REA-LOCAL-20261024-2238-P0-ARMYCHIP-VECTOR-LIFETIME-STATIC-01`
日時: 2026-10-24 22時台 JST。分類: **PC-SAVED / STATIC / VERIFY / NOT READY**。
対象原作SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（実ファイル再計算済）。
検索DB: `HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`（実ファイル再計算済）。

## 既存との非重複・参照
MASTER_LEDGER / ANALYSIS_LANES_PROTOCOL / REA README・QUEUE・PROGRESS / 既存同期ログ / 20261024 20H・2035・2137証拠 / 旧search README・BUILD_MANIFEST / V9整合性・検索CLIを先読。
同期ログ `progress_sync_20261011T153958076Z.json` はWave1～5で64/64、レビュー済run21件。旧PROGRESSの15/16表示とQUEUEの旧TODOはEPERM由来で陳腐化。正式数の増減・キュー更新なし。
前回2137研究は子 `ArmyChip` のRTTI、+0x34/+0x08/+0x48/+0x44の実ターゲット、条件分岐を既に確定。今回は**親コンテナの初期化・解放境界および探索範囲を明示した別実証**を追加。

## 新しい静的証拠A：親/子の型とメソッド境界
- 親 `ArmyChipBuilder` vtable=`0x0063AE54`、COLポインタ=`0x00640004`。slot `+0x00` は `0x005B0980`、`+0x04` は従来の主処理 `0x005B0A50`。
- 子 `ArmyChipBuilder::ArmyChip` vtable=`0x0063AE74`、COLポインタ=`0x0063FFB4`。slot `+0x00` は `0x005B1310`、`+0x04` は `0x005B13D0`。
- 親生成 `0x005B0880` の命令 `0x005B08BE/0x005B08C1/0x005B08C4` は `builder+0x14/+0x18/+0x1C` をそれぞれゼロ初期化。これらは子ポインタvectorのbegin/end/capacityに相当する。
- 親 `0x005B0A50` 内で `0x005B0C83` →子生成 `0x005B0EA0`、`0x005B0CC3` にて `builder+0x14`、`0x005B0CCD` →汎用vector挿入 `0x004C1290`。既存2137の生成・追加経路を別途限定再照合。

## 新しい静的証拠B：親デストラクタは配列領域を解放するが、要素破棄は未同定
- 親vtable `+0x00` の `0x005B0980` は `0x005B0983` で `0x005B09A0` を呼び、`0x005B099B` は `RET 4`。
- `0x005B09A0` は2つの内部木構造を片付けた後、`0x005B0A0E` で `[ESI+0x14]`（vector先頭格納領域）を取得。非NULLなら `0x005B0A19` で `0x005B6BBB`（free系）へ渡す。
- 続いて `0x005B0A21/24/27` で `+0x14/+0x18/+0x1C` をすべてゼロ化し、`0x005B0A44` で基底Actionableのvptrへ戻す。
- このデストラクタ本体 `0x005B09A0～0x005B0A4B` には、直接CALLが6本（すべて `0x005B6BBB`）のみ。独立したx86命令逆アセンブルでも間接CALLを認めず、子destructor `0x005B1310/0x005B1330` の呼出しは**この関数内には存在しない**。
- したがって「親デストラクタは子オブジェクト全件を個別に破棄する」という実装仮定は採用できない。ただし、別の所有者/経路が子を解放する可能性があり**リーク確定ではない**。

## 検索範囲を限定した存在・不存在の証拠
- 元PE .text内の親vtableポインタ `0x0063AE54` リテラル参照は `0x005B08B1` の1箇所、子vtableポインタ `0x0063AE74` は `0x005B0F45` の1箇所。
- V9内の `0x005B0EA0` へのE8直接CALLは `0x005B0C83` の1箇所（発信元 `0x005B0A50`）。
- 汎用vector挿入 `0x004C1290` はV9全域で147直接CALL。そのうち `0x005B0800～0x005B1600` 範囲では `0x005B0CCD` の1箇所。
- **証明範囲の限界:** 直接E8・.text絶対リテラル・クラス周辺アドレスのみに対する結果。別関数からの親オブジェクトへの書込、間接CALL、別の派生型混入、vptr動的更新を否定する結果ではない。生成・vector登録・削除の完全列挙と扱わない。

## 独立検証と進捗
監査: `REA_20261024_22H_P0_ARMYCHIP_VECTOR_LIFETIME_AUDIT.py`。原作PE実バイト・E8相対CALL・vtable・限定.textスキャン・V9(SQLite read-only, quick_check)・擬似C部分照合・デストラクタCALL完全列挙を独立検査。
初回 **40/40 PASS**。保存済み証拠JSONと再計算結果の独立論理比較を加えた検証 **41/41 PASS**。監査所要時間は初回1.858秒、最終再検証1.406秒。全調査時間未計測。
正式REA info/pseudo/assembly/callers/calleesの**新規完全5種類セット=0関数**、新規VERIFIED=0。対象新規6関数の部分証拠はREA VERIFIEDに自動昇格しない。正式TODO/VERIFY/BLOCKED差分=0/0/0。
Golden原作実機PASS=0、strict MATCH=0、完全複製率未測定。新規Ghidra・REA・ゲーム実行0、PC全体CPU負荷と空きRAMは今回未測定。
PCオンライン、Local正常接続。21時台既存成果との衝突なし。REA active.lockなし、Java/Ghidraプロセス未検出。
不具合記録: `REA-LOCAL-20261024-22H-JSON-TUPLE-01`。初回の読み戻し比較でPython tupleと保存JSON listをそのまま比較して1件FAIL。正規化して修正後41/41 PASS。安全拒否ではなく元証拠・原本変更なし。探索用旧プローブのRTTI表示でNUL区切り文字の誤りによるUnicodeDecodeErrorも検出（記録ID `REA-LOCAL-20261024-22H-RTTI-PRINT-01`）。正式監査のRTTI証明には使用せず、親子vtable実バイトで評価。
安全拒否済み `0x004BC9C0` の検索CLI、0x5710C0..0x571500、Wave6/REA exportは再試行・迂回なし。原本・MASTER・QUEUE・PROGRESS・既存run・A～E・Git・Work・スケジュール無変更。

## 次に調べること
P0: 子の解放責任が `0x005B1310` 等の別処理・イベント/共有所有者にあるのかを、許可範囲で静的証拠により同定する。親vtable+0x04を実際に呼ぶ箇所の親型証明、子配列へ外部経路から登録される型、vptr変更/要素数変動もVERIFY。
Golden設計（NOT RUN）：子0/1/複数件、生成・vector登録・各反復・親破棄の順序を観測し、vector領域と子オブジェクトの寿命を別々に記録する。再実装では根拠なしに親が子を一括destroyする仕様を固定しない。

