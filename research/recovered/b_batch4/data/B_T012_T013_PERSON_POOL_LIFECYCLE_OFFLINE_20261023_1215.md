# 迫真戦記 ver0.67｜新B T012/T013：Person候補vectorの初期化・リセット・破棄と死亡時候補変化の照合

- 研究ID：`B-OFFLINE-20261023-1215-T012-T013-PERSON-POOL-LIFECYCLE-JOIN-01`
- 実施：2026-10-23 12:15 JST開始／担当：新B（T012・T013）／状態：**OFFLINE-UNSYNCED / STATIC-GHIDRA / STATIC-SQLITE / VERIFY / NOT READY**
- Bの許可された研究資料のみ作成。原本EXE・DAT・SAVE・Git・設定・MASTER・他レーンには書き込みなし。
- Local CompactによるPC MASTER読取：`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。接続障害であり、安全拒否ではない。最新版MASTER、LANE_B_HANDOFF、PC保存済み復旧索引は未確認。
- ソース：ChatGPT Libraryに存在する `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` のread-onlyスナップショット（34件のZIP CRC検査PASS）。Bundle SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。同梱 `headless_analysis/search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（integrity_check=ok）。期待EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。**今回EXE自体を取得・読取検証していないため原作ASM直接検証ではない。**
- 検証プログラム：`B_T012_T013_PERSON_POOL_LIFECYCLE_VERIFY_20261023_1215.py`、証拠：`B_T012_T013_PERSON_POOL_LIFECYCLE_EVIDENCE_20261023_1215.json`。

## 1. 今回の問い

11時台の`B-OFFLINE-20261023-1109-T012-T013-UNIT-VSLOT70-LIVEVECTOR-01`では、全対象処理 `0x00547DB0` が各候補の処理後に候補vectorのbegin/endを再取得し、数値インデックスだけを進めることを確認した。死亡時に候補vectorが即時変更されるのかを知るため、**候補vector自体の寿命管理**と**死亡時の別管理リスト**を区別する。

## 2. Person候補vector +0x48 の3種類の寿命処理

| EXE VA（検索DB上の関数開始） | 検証したGhidra擬似Cの事実 | 位置づけ |
|---|---|---|
| `0x00514740` | `Person::vftable`設定、`param_1[0x12] / [0x13] / [0x14] = 0`。各要素4バイトなので `+0x48 / +0x4C / +0x50` がbegin/end/capacity候補 | **初期化：STATIC-GHIDRA** |
| `0x005149C0` | `*(void **)(param_1+0x4C) = *(void **)(param_1+0x48)`、類似操作は`+0x38`群、`+0x58`群にも存在 | **一括論理クリア：STATIC-GHIDRA**。要素毎の仮想デストラクタ呼出しはこの関数内に見えない。呼出site `0x0051E729 → 0x005149C0` |
| `0x00514AA0` | `+0x48..+0x4C`に格納された非NULL各ポインタに `(*(code *)**(undefined4 **)*piVar5)(1)` を実行してからendをbeginへ。`+0x58`群と`+0x38`群にも類似のループ | **要素に対する仮想解放系：STATIC-GHIDRA**。正確なABIと物理解放の副作用はVERIFY |
| `0x005148A0` | `Person::vftable`設定、`0x514AA0`を呼出し、後続で`param_1[0x12]`メモリ領域を`0x5B6BBB`に渡し、`param_1[0x12..0x14]`を0化 | **コンテナ破棄系：STATIC-GHIDRA**。site `0x005148DB → 0x00514AA0`。擬似Cの引数表現に疑義がありASM/呼出規約はVERIFY |

`0x00514F10`も`+0x48..+0x4C`を読み、各候補の`+0x1867C==0`等で選別する。`0x00547DB0`は、`Unit+0x1D4`から辿る一方の管理者（またはその`+0x1C`の参照先）の`+0x48/+0x4C`を走査し、候補の`+0x1867C`を判定し、`0x00547F60 → 0x00550E70`へ処理を配送する。

**新たな横断的結論：** 候補`+0x48`系列には、「初期化」「一括論理長リセット」「個別要素に仮想処理を行う破棄」という**異なる呼出経路**がある。したがって死亡時に候補vectorのendが即時詰められると一律に実装してはならない。`Unit+0x1D4`の参照先が、ここで初期化される`Person`実体であることはレイアウト上整合するが、型・ポインタ所有関係はまだ**INFERRED / VERIFY**。

## 3. 死亡後処理で変更される「別のリスト」との区別

- `0x00575DF0`の直接CALL記録から、`0x00575F6C`および`0x00575F8C → 0x005684B0`を確認。
- `0x005684B0`は、Ghidra擬似C上では`unaff_EDI+0x0C / +0x10` のグループ内vectorを走査し、フラグ`+0x1D`が立つ経路では `Unit+0x1867C != 0` の個体を`memcpy`で詰め、endを4バイト縮める。**対象はグループvector**であって、前節の**Person+0x48候補vectorと同じである証拠はない**。
- `0x00575DF0`の`0x00575E2E → 0x004C22B0`も確認。`0x004C22B0`は、別のmanager側で`+0x2C..+0x30`内の一致要素を0化し、`+0x64..+0x68`のvectorを`memcpy`で前詰めし、条件付きで`+0x54..+0x58`へ後処理予約する。ここも**Person+0x48と別のレイアウト**。擬似CにABI不確定箇所あり。
- 5つの選択関数（`0x550E70`, `0x578370`, `0x544790`, `0x55ABA0`, `0x55B060`）から上記のPerson一括クリア・破棄（`0x5149C0`, `0x514AA0`）への**直接CALLはSQLite記録上0本**。間接CALL・vtable・transitive（多段）経路が無いことを意味しない。

**結論：**「致死→グループvector縮小」から直ちに「`0x547DB0`が読んでいる候補vectorも縮小」と推論するのは誤り。`0x547DB0`の数値indexが飛ぶ可能性は**条件付きの仮説**のまま。逆に、削除が遅延/別vectorの場合はindex飛ばしは起こらない可能性がある。**DYNAMIC未実施。**

## 4. 証拠・検証手順と限界

検証対象Ghidra擬似C 15関数の`code_sha256`をDB上の値と再計算一致、関係する具体フィールド・条件表現の32マーカー確認、指定した6件の直接CALLレコード照合。結果 **15/15、32/32、6/6 PASS**。Bundle 34/34 CRC PASS、SQLite整合性PASS。これらは**抽出済み静的資料の内部整合性**であり、原作EXEへの再照合/Golden一致ではない。

独立増分は「Person候補vectorの3つの寿命経路」と「グループ・manager側の死亡後vectorをPerson候補vectorと同一視しない」という横断契約整理。既存の11時台`0x547DB0`ライブvector走査や既知の`0x5684B0`死亡処理そのものは、新発見に再計上しない。今回ZIP内スナップショットと手元B既存成果で重複を限定照合したが、**PC最新版MASTER/checkpoint/READYとの重複・権限確認は未了**。

## 5. 次回のP0とGolden条件

**優先検索：** `callers/related 0x005149C0, 0x00514AA0`（一括クリアをいつ呼ぶか）、`callers 0x00514F10`、`function 0x00547DB0`の`owner+0x48/+0x4C`全writerと`+0x1D4`参照先のPerson同定、`0x00575DF0`死亡時サブ呼出と間接呼出、候補`Unit+0x1867C`writer。旧拒否範囲`0x5710C0..0x571500`への再アクセス・拒否経路迂回を行わない。T011、T024、T028の未解明P0は別途残す。

**Golden要件：** 同一原作EXE/DAT/MAP/SAVE/入力/RNG、候補 `[A,B,C]` 中でA致死、A状態フラグとPerson候補vector`+0x48/+0x4C`の各tick値、グループ`+0x0C/+0x10`とmanager`+0x64/+0x68`の変化、B/Cへの配送順・回数・経験値/HP変化を並べて測定。未実施につき **原作Gameplay Golden PASS=0、strict MATCH=0、新規READY=0、Task DONE増加=0**。

## 6. 復旧・保存状態

Local PC 正本・MASTER・B HANDOFF未同期。別件`B-RC-20261023-0213-LIBRARY-OVERWRITE-CONTAINER-01`系の過去訂正版未反映は未解決のまま。今回の追加保存・読み戻しは保存結果に基づき別途報告する（このレポート本文は成果の真偽を先取りしない）。再開はまず最新PC MASTER・owner・既存ID・重複・拒否・競合・READY照合、その後B所有文書への一度限りの採録。MASTER正式統合はE担当。
