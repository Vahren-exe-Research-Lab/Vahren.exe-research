# 迫真戦記 新E｜T020 dialog 登録・文字列既定値の分岐境界（独立調査）

**研究ID** `E-OFFLINE-20261028-1745-T020-DIALOG-REGISTRY-FALLBACK-GATE-01`  
**調査** 2026-10-28 17:45 JST / E（T018・T019・T020）  
**分類** `OFFLINE-UNSYNCED / STATIC INDEX VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY / GAME NOT RUN`

## 0. 一次資料と接続・保存境界

Desktop Commander Local Compact の研究ルート `list_directory` は `INVALID_ARGUMENT / McpServerError: Session terminated` で失敗。これは **CONNECTION** であり安全拒否ではない。PCの電源・オンライン状態は未確認。復旧ID: `E-RC-20261028-1745-LOCAL-SESSION-TERMINATED-01`。前回16:45の同種接続失敗とは別試行である。

代替として、ChatGPT Libraryのルート直下に存在する実ファイル `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（元ファイルIDは記録上 `file_000000006ad08209a897b82c4ebf281a`）を今回新規に読み出し、内容を一時作業領域に**派生コピー**した。ZIP原本の変更はなし。ZIP SHA256 **`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`**。`search.sqlite` SHA256 **`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`**、マニフェスト記録値と一致、SQLite `quick_check=ok`。`search.py` で関数とcaller/calleeを限定取得。Ghidra/Java再解析なし。研究規約は同ZIPの2026-10-21スナップショットを読み、E以外の成果を変更していない。

原作EXEの**マニフェスト識別値** SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。今回は原作EXE現物のハッシュ計算や実ゲーム起動をしていない。旧検索DBは2026-10-21スナップショットであり、PC上の最新研究成果を保証しない。

## 1. 新しいE担当の静的照合成果

前回16:45は「放浪・傭兵化メッセージが `0x0052CF50` を経て `0x0043F470` のdialog系に到達する直接CALL」を調べた。今回、その **`0x0043F470` 内部の文字列・登録・コールバック分岐**と、登録に使われる2関数を別々に調査した。

### (a) `decide11` は呼び出しごとに必ず固定選択されるわけではない

旧Ghidra擬似C `0x0043F470` の `in_stack_00000038 == 0` の場合は `FUN_00402800("decide11",8)`、非0の場合は引数側の文字列相当値から `FUN_004420a0(&stack0x00000028)` へ分岐する。したがって、**「dialog登録に到達したら常にdecide11で選択する」という互換実装は静的証拠と一致しない**。

別の `in_stack_00000054 == 0` の分岐では、二つの空文字列相当リテラル（`DAT_00625076`/`DAT_00625077`、呼出長0）を構築する。非0では `FUN_004420a0(local_2c)` と別の0長文字列構築へ進む。ゼロ長の文字列構築呼び出し自体は確認できるが、UI上のボタンや選択肢の最終的な表示状態は未検証。

前回のB14が報告した `0x00497BB0` 側の `decide3 / decide11` 選択と数値 `500 / 10 / 25` は、別の引数・別の条件分岐（候補`+0x74`と関連オブジェクト`+0x1D`）にある。**同じ`decide11`文字列が登場するだけで引数値・同じダイアログ個体・ゲーム効果が同一だとは認定しない**。T019は矛盾確定でなく `VERIFY`。

### (b) dialog索引へのノード構築・登録と「コールバック条件」を分ける

`0x0043F470` は登録前に `local_78 = *(int *)(iVar2 + 0x20)` を読み、その後 `local_74 = "dialog"` を設定し、直接CALL `0x0043F72F → 0x00416E80` と `0x0043F73F → 0x00416B90` を実行する。さらに後段で**`local_78 == 0`** の条件のときのみ `iVar2 + 0x10` 由来のvtableオフセット `+0x1C` を介した間接CALLを記述している。

`0x00416E80` は `0x2C` バイトの割当と文字列相当のコピーを行い、失敗時には `std::bad_alloc` 経路もある。`0x00416B90` は木構造を走査してノードを挿入する経路と、一致・比較の結果によって構築済みノードを解放して**結果フラグ0**を設定する経路を持つ。結果フラグ1も存在する。

**重要な受入境界:** (1) 登録関数に到達すること、(2) 登録結果フラグが1になること、(3) `local_78 == 0` による間接CALL分岐に入ること、(4) 原作で画面表示・ユーザー選択・World更新が発生することは、それぞれ別の事象である。擬似C中の`local_78`は登録前のメモリ読み出しに由来し、登録結果フラグそのものとは示されていない。`iVar2+0x20` の意味（個数等）とvtable呼出し先は現時点で未確定。

### (c) 五つの直接呼出元を照合

`0x0043F470` の直接callerは旧DB上 **5関数・計5 CALL**。`0x0052CCF0` (`0x0052CDDE`)、`0x0052CE50` (`0x0052CF23`)、`0x0052CF50` (`0x0052D047`)、`0x0052D2E0` (`0x0052D3B4`)、`0x0052D3D0` (`0x0052D4C3`)。前回の`0x0052CF50`だけを専用呼出元と誤認する実装を避ける。

局所ソース出典: `functions.code`のUTF-8 SHA256：

| VA | コードSHA256 | 備考 |
|---|---|---|
| `0x0043F470` | `07C974DFCD0D8191E6A7D7B2486BF726AF44472B87873A96A51EA0DB9928F52E` | 既定文字列分岐・dialog登録・間接CALL |
| `0x00416E80` | `92C51433B1115528D85014134072BE025F537865997EBD0862EC2E73B4B0E8DA` | ノード構築 |
| `0x00416B90` | `F01F950DF0218A661A0DC081EC56A359FAA7FF71D0D2035BB890EF1594019232` | 比較・挿入・不一致時の後処理 |
| `0x00497BB0` | `067CF0B7C5E4F2E71CF342337DF87C50DCD6FD211B291D63E2FFB86CD28EC953` | B14側の数値生成との対照 |

これらは解析DBからのコード文字列ハッシュであり、**原作機械語の新規ハッシュではない**。引数のスタック名はGhidraの推定なので、実際の呼び出し時の値・同一インスタンス性は別途検証が必要。

## 2. T020比較fixtureとテスト

- `T020_DIALOG_REGISTRY_BRANCH_CASES_20261028_1745.json`：直接CALL**14件**、誤結線負例**5件**、分岐合成ケース**8件**、Golden不適格負例**7件**。
- `t020_dialog_registry_branch_gate_20261028_1745.py`：旧SQLiteを`mode=ro&immutable=1`かつ`PRAGMA query_only=ON`で参照し、上記の直接CALL・逆接続負例、擬似C内の条件順序、挿入結果2通り、Golden受入ゲートを検証。
- **新規46/46 PASS、終了コード0。前回16:45の28件を同じDBに対して独立再実行して28/28 PASS。今回実行した合計74/74 PASS。** 2026-10-28 13時台の安全拒否によりNOT RUNとなった14件は、今回の実行件数へ含めない。
- 結果は `STATIC INDEX / SYNTHETIC EXECUTED / VERIFY / NOT READY`。原作ゲームの実動作、登録されたdialogの表示、実際の操作選択、ゲーム内での傭兵化・放浪成功を**証明しない**。

## 3. T018 Golden / T019 / 正本の状態

T018合法原作のG0=通常UIで開戦、G1=同一戦闘直前の未改変SAVE生バイト・SHAと入力記録、G2=同一戦闘の実MAP生バイト・SHA、攻撃/防御/支援3陣営、ordered Troop/Unitと配置が必要。G3=戦闘結果、G4=戦略World差分も同じrunに対応させる。文字列・ダイアログ登録の静的経路や合成fixtureをその代替に使用しない。

**今回新規 DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0。G0/G1/G2 NOT RUN。**

T019の新規確定矛盾0件。`decide11`同名文字列の用途・数値分岐との同一性は`VERIFY`。GameClear DAT13箇所/TXT2箇所の字句検索範囲差は既存RESOLVED、`script2`同名定義優先順位・phase flag・TXT実読込・`gwrite`復帰は既存VERIFYを継承（今回T019最新ファイルは未読）。

MASTERの最終既知正式値は**2026-10-28 12時台の旧確認値** `checkpoint196 / READY596 (A115/B229/C136/D116) / 34 Task (DONE9, IN_PROGRESS21, VERIFY4, ID重複0)`。PC正本の今回再確認なし。**正式READY新規統合0件、統合IDなし**。A～D/REAの最新HANDOFFおよび今のowner/既統合/READY/重複・競合は未検証。MASTERへ書き込んでいない。

## 4. 接続障害・安全拒否の引継ぎ

新規接続障害 `E-RC-20261028-1745-LOCAL-SESSION-TERMINATED-01`: 17:45 JST、Local Compactの研究ルート一覧リクエストでSession terminated。最後の成功: 前回16:45 Libraryオフライン成果（28/28）と本runのローカル派生調査（46/46、前回再実行28/28）。PC未保存: 本runのE資料/正本統合、現行owner/READY確認。保存先: 本runの会話添付とLibrary `/迫真戦記/E_OFFLINE_UNSYNCED/` の独立資料（アップロード・再取得結果は別途確認）。再開位置: 今回研究IDを重複判定したうえ、最新E T020およびA～D/REA HANDOFFを参照できるときだけ正式照合。安全拒否の再試行は禁止。

既存の安全拒否 `E-RC-20261028-1353-READONLY-PS-SAFETY-01`, `E-RC-20261028-13H-E13-REPORT-APPEND-SAFETY-02` は引き続きBLOCKED。拒否された13時台MASTER複合照合・報告追記を再試行していない。T018表境界・session-join、T019拒否済みXREF、C T026/T032、D T030 TSV、`0x5710C0`もBLOCKED継続。2026-10-25 OFFLINE-UNSYNCEDと他レーン成果の完全意味重複照合も未完了。Git/push、他レーン、原本EXE/ZIP/SAVE、dev_lab、Work、設定、スケジュールへの変更なし。

## 5. 次の優先手

E/T020：`0x0043F470`の呼出引数の対応を原作ASMなどの合法静的証拠で限定確認して、`decide11` の既定値とB14の数値分岐の**同一インスタンス性が不明**な状態を維持したまま追加比較する。`0x00416B90` 結果フラグと `local_78` 間接CALL条件を別項目として実装受入試験に固定する。

E/T018：同一戦闘のG0→G1→G2の合法原作一次証拠が最優先。原作観測がない限りactual Golden PASSとstrict MATCHを0とする。PC復帰時には安全拒否箇所を避け、現行MASTERの所有権・READY・重複の許可された照合ができる場合だけ、未同期資料を二重反映せず正式統合する。
