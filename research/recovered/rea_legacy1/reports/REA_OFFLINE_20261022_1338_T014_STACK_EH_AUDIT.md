# 迫真戦記 ver0.67｜REA独立T014：スタック所有オブジェクトの読込失敗時EH破棄経路

**独立ID**：`REA-OFFLINE-20261022-1338-T014-STACK-EH-LOCAL-LIFETIME-STATIC-01`  
**分類**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**時刻**：2026-10-22 13時台 JST。**所有担当**：REA/T014。**原本・製品コード・他レーン・MASTER・QUEUE・PROGRESS・Git・スケジュール変更なし**。

## 1. 証拠と先行研究との非重複

- Desktop Commander Local CompactでMASTER等7ファイルを先読みしようとしたが `INVALID_ARGUMENT: McpServerError: Session terminated`。接続障害（安全拒否ではない）で、PCの電源状態、最新版owner/active.lock/MASTER/QUEUE/PROGRESS、RAM/CPUは未確認。復旧記録ID：`REA-RC-20261022-1338-LOCAL-SESSION-TERMINATED-01`。
- 代替としてLibraryに実在する `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe` を材料化。ZIP CRC **34/34 PASS**。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、EXE実測 SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、SQLite実測 SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。DBハッシュは旧 `BUILD_MANIFEST.json` と一致、`PRAGMA integrity_check=ok`。
- 12:30の前回証拠 `REA-OFFLINE-20261022-1230-T014-MSVC-EH-FUNCINFO-HEAP-GATE-STATIC-01` は**旧成果**。前回再検証スクリプトを同一SHAのEXE/ZIP/SQLiteで再実行し、実命令22箇所・制御移動13件・EH状態30・TryBlock2件が **PASS**（約1.227秒）。同じ発見を再加算しない。
- E/T020の12:51報告 `E-OFFLINE-20261022-1251-T020-EH-PHYSICAL-OWNER-GATE-01` は旧Ghidra caller誤帰属とヒープ例外ゲートを既に整理している。今回はそれらを二重計上せず、**スタック側親関数のEHテーブル／読込中の具体的unwind／破棄ABI**だけを新たに追跡した。
- 保存済み擬似Cと直接CALL索引は探索のためにのみ使用。最新PC V3の検索DBは未確認であり、古いオフラインSQLiteと混同しない。REA/Ghidraの新規実行は0回。

## 2. 新しい一次証拠：スタック側 `0x45E1E0` のMSVC EH

`0x45E1E0` は先頭 `55 8B EC 83 E4 F8` で実フレームを作る。`0x45E1E8` でEH thunk `0x5FD6A3`を登録し、thunk内 `0x5FD6C7` がFuncInfo VA **`0x0065508C`**を設定して `0x5B8B1E`にジャンプする。原本PEセクションに基づくVA→raw offset変換でMSVC x86 FuncInfoを直接読んだ。

| 項目 | スタック所有 `0x45E1E0` | 比較用ヒープ `0x45E7F0`（前回既知） |
|---|---|---|
| EH FuncInfo | `0x65508C` | `0x655030` |
| magic | `0x19930522` | `0x19930522` |
| state数 | **7** | 30 |
| UnwindMap | `0x655054` | `0x654EF8` |
| TryBlock数 | **0** | 2 |
| reader CALL | `0x45E52F → 0x5964C0` | `0x45F6A1 → 0x5964C0` |
| reader到達時の状態 | **4**（下記実命令） | 9（前回既知） |

`0x45E2F8` の機械語は `mov byte ptr [esp+0x498],4`。この後 `0x45E52F`までの確認範囲には、対象EH状態位置への後続書換えは検出されなかった。reader呼出直前 `0x45E528` は `lea ecx,[esp+0x174]`、次のCALLが `0x5964C0`。`0x45E284` で構築したスタック上オブジェクトをreaderに渡す構造と整合する。

## 3. 新しい一次証拠：reader失敗時のunwindと対象デストラクタ

読込中に例外が外へ伝播して通常のMSVCアンワインドが実行される場合、状態4からのMapは **`4→3→2→1→0→-1`**。各actionは独立した実命令／rel32転送先と照合した。

| state | 次state | unwind action | 対象ローカル／制御移動 |
|---|---:|---|---|
| 4 | 3 | `0x5FD682` | `[EBP-0x46C]` → `JMP 0x4026B0`（短い文字列様バッファ） |
| **3** | **2** | **`0x5FD675`** | **`[EBP-0x328]` → `CALL 0x45DF70`（読込対象オブジェクト）** |
| 2 | 1 | `0x5FD668` | `[EBP-0x3F8]` → `CALL 0x432DF0` |
| 1 | 0 | `0x5FD65B` | `[EBP-0x1F0]` → `CALL 0x4591F0` |
| 0 | -1 | `0x5FD650` | `[EBP-0x434]` → `JMP 0x50FE60` |

**重要な対応**：正常終了時の `0x45E569` も `lea eax,[esp+0x174]`、`0x45E58B` は `CALL 0x45DF70`。例外時 state3 actionが参照する `[EBP-0x328]` は、同じ局所オブジェクトに対応するGhidra復元と整合する。`0x45DF70`の擬似Cには複数のコンテナ・文字列破棄／解放呼出が存在する。ただし、動的な破棄実行回数と全副作用は別途要検証。

**ABI新規確認**：`0x45DF70`の実命令 `0x45E1D8` は **`RET 4`**。state3 action `0x5FD67B` は引数をPUSHし `0x5FD67C` で `CALL 0x45DF70`、呼出元に `ADD ESP,4` はない。したがって、この経路は**呼出先が4バイトのスタック引数を回収するABI**と一致する。`void FUN(param)`というGhidra宣言のみで呼出規約を判断しないこと。

**結論の境界**：スタック側では読込対象オブジェクトの専用破棄がEH経路に登録され、ヒープ側の前回 `state9→6` とは異なる。**ただし「セーブ読込が完全に原子的で全フィールドが巻き戻る」「上位状態は不変」は導けない**。破棄前の外部副作用、再送出先、例外中のデストラクタ例外や所有権移転は未検証。またスタック関数に**ローカルTryBlockが0件**という事実は、より上位にcatchがないという意味ではない。

## 4. 独立機械検証と正式進捗

`verify_rea_t014_stack_eh_20261022.py` は原本実行なしで、PE32参照、ソースSHA、旧SQLite `mode=ro&immutable=1`、対象擬似CのSHA、実機械語**23箇所PASS**、相対CALL/JMP **11箇所PASS**、EH state **7/7**、unwind経路、既存ヒープEHとの境界を再検査した（約1.17秒）。追加したGhidra保存コード確認：`0x45E1E0`、`0x45E7F0`、`0x5964C0`、`0x45DF70`、`0x590560` の5関数。完全なREA5種証拠を新たに満たしたという意味ではない。

| 指標 | 今回の値 |
|---|---|
| Wave1～5 VERIFIED | 64/64は**過去報告値**。PC現行台帳で再確認できず |
| REA新規正式VERIFIED／5種完備 | **0／0** |
| 正式TODO/VERIFY/BLOCKED差分 | **0／0／0**（QUEUE未変更。正式台帳の現物差分検査は不能） |
| Wave6正式登録 | **0/16（過去報告値）**。既拒否対象には触れない |
| 原作Golden PASS／strict MATCH | **0／0**。ゲーム起動なし |
| 完全複製率 | 不明。5種の証拠達成率とは別 |
| 今回の新規REA/Ghidra実行 | 0／0 |
| 研究PC CPU/RAM／調査全体所要時間 | 不明／未計測 |

## 5. 保存・次回再開

本MD、機械可読 `REA_OFFLINE_20261022_1338_T014_STACK_EH_EVIDENCE.json`、独立再検証 `verify_rea_t014_stack_eh_20261022.py` を**モデル側の作業領域に保存**。ChatGPT Library `迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED` へ別ファイルとして保存・読み戻しする。PC正本への正式同期はまだ行わない。

**次のP0**：ヒープ経路 `0x45F6A1`正常復帰後の `0x45F72C` 前後（所有権移転開始点）と `0x436560/0x436680/0x463280` の実動作、またはスタックreader例外を受ける `0x45E1E0` の直接上位callerとそのcatchの所在を追跡する。既存保存DBから関数・xrefsを先に取得し、必要な局所ASMのみ確かめる。`0x42ECF0`（64bit ABI）と`0x470AE3`（間接CALL）もVERIFY継続。

PC復帰時：MASTER/規約/最新QUEUE/PROGRESS/旧runs/既存Evidence/owner/active.lock/ID/SHAを先読み。12:30・13:38の独立ID、E/T020の12:51 IDと競合を確認し、REA所有範囲へ差分だけ一度同期。安全拒否済みVA `0x5710C0..0x571500`、Wave6やREAエクスポートの再試行・別経路での迂回をしない。Work不使用。スケジュール変更なし。
