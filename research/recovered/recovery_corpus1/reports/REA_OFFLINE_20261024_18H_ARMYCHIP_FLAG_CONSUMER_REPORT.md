# 迫真戦記 ver0.67｜REA P0 独立静的研究（2026-10-24 18時台）

**研究ID** `REA-OFFLINE-20261024-1836-P0-ARMYCHIP-FLAG-CONSUMER-VTABLE-STATIC-01`  
**分類** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**今回の焦点**：既知の遅延外交支援・除外集合に格納する `node+0x14` フラグが実際に読み出される箇所と、その処理に関与する `ArmyChipBuilder` 仮想テーブルの静的同定。既存成果の再計上はしない。

## 1. 作業前の根拠・復旧

優先する Desktop Commander Local Compact により、Windows正本 `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、REA `README.md`/`QUEUE.json`/`PROGRESS.md` を読み取る試行を行った。しかし接続段階で **`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`**。これは接続/レート制限のエラーであり、安全拒否ではない。実PCオンライン状態、CPU/RAM、active.lock、最新のowner/QUEUE/PROGRESS/現行SQLiteは確認不能。別shell/Remote等で迂回せず、Ghidra/REA/原作実行は一切しない。

代替としてアクセス権を持つ ChatGPT Library の原作 `Vahren(2).exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、旧 `decomp_task.zip`、プロトコルのコピーを取得した。ZIPに入っている旧MASTER/README/PROGRESS/BUILD_MANIFESTを先読した。原本EXE・ZIPは変更せず、別の作業コピーのSQLiteを**読み取り専用**で照合。旧REAアーカイブの記録 `progress_sync_20261011T153958076Z.json` は Wave1–5 64/64 を示すが最新正式状態の代用とはしない。旧PROGRESS/QUEUEには過去の EPERM/STALE 不整合がある。旧Ghidra DBは内部10,268関数（2026-10-21版）。現行と報告されたV3 10,274関数/V4 11,226関数は本実行ではアクセスできず比較未了。

ソースハッシュ（本実行で読み込んで検証）：

| 資料 | SHA256 |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインパック | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| 旧 `search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP 34件CRC、SQLite `PRAGMA integrity_check=ok`、PE32 ImageBase `0x00400000`。既存旧DB全関数は再解析せず、局所的に検索・疑似Cと原作機械語を相互照合した。

## 2. 新規 P0-A：除外ノードのフラグに実際の読み手が存在

**発見**：`0x00491870` は `context+0x1EED30` の木構造からキーを検索し、成功時にノードの `+0x14` バイトを読み込む。これは17時台の「モード1/3/4で挿入ノードへ1、その他で0が保存される」という書込側の発見を、**独立した読取箇所**へ接続するものである。

| 機械語VA | 元EXEの動作 | 分類 |
|---|---|---|
| `0x004918EB` | `LEA ECX,[EBP+0x1EED30]` | 除外集合を検索先に設定 |
| `0x00491901` | `MOV byte ptr [ESP+0x1A],0` | キー未発見時のフラグ初期値0 |
| `0x00491906` | `CALL 0x004F8AE0` | 木構造内のキー検索 |
| `0x0049190F` | `CMP ECX,[EBP+0x1EED34]` | ヘッダ/終端比較 |
| `0x00491915` | `JE 0x00491929` | キー未発見なら0のまま |
| `0x0049191A` | `MOV BL,[ECX+0x14]` | **既存ノードのフラグ読出し** |
| `0x00491921` | `MOV [ESP+0x1A],BL` | そのフラグを局所退避 |
| `0x00491A04` / `0x00491B33` | `TEST BL,BL` | **二つの分岐で再利用** |

フラグ非0の経路は `context+0x1EED4C` を読み、0の経路は `context+0x1EED50` を読み、各経路で `0x005911D0` に渡すCALLが存在する。主要なCALL siteは `0x00491A11`/`0x00491A42`、後段 `0x00491B42`/`0x00491B66`。**このフラグは未使用の記録ビットではなく、後続処理の参照データを切り替える。** ただし `+0x1EED4C/+0x1EED50` のゲーム意味（支援種別、部隊アイコン、文字列など）は確定できない。

先行する17時台の静的証拠 `0x0052ECB2`（一時的フラグ代入）と `0x0048A4E5`（ノード保存）を今回も整合確認したが、これらは**再計上しない既知事実**。キーが不一致なら局所フラグは0だが、関数全体の到達条件、コンテナの所有権、実ゲームの応答は未確認。

## 3. 新規 P0-B：読み手につながる `ArmyChipBuilder` クラス仮想テーブルの原本RTTI

旧Ghidraの直接CALLでは `0x00491870` の呼出元として **`0x005B0A50`（CALL site `0x005B0B15`）** が確認される。さらに原作 `.rdata` のMSVC RTTIとコンストラクタを独立検査した。

| VA | 原本値と解釈 |
|---|---|
| `0x0063AE50` | vftable前の Complete Object Locatorポインタ = `0x00640004` |
| `0x0063AE54` | vftableの先頭関数アドレス `0x005B0980` |
| `0x0063AE58` | **vftable +4 の関数アドレス `0x005B0A50`** |
| `0x00640010` | COLのTypeDescriptorポインタ `0x0068DA8C` |
| `0x0068DA94` | C++装飾クラス名 `.?AVArmyChipBuilder@@` |
| `0x005B08AF` | コンストラクタが `MOV [ESI],0x0063AE54` でvptrをセット |
| `0x005B06C6` | `0x005B0680` からコンストラクタ `0x005B0880` をCALL |

**判定**：`0x005B0A50` を *ArmyChipBuilder の vtable slot +0x04 の関数* として原本と旧SQLiteから結び付けた。ただし、どのオブジェクトが実行時にその仮想呼出し先へ入るか、実際の `CALL [vptr+4]` site、関数の正式C++名・仮想型までは未確定。`0x00491870` の内部から `0x005B0680` に向かう CALL site `0x00491E99` と、別経路の `0x00490590 -> 0x005B0680`（`0x004917B3`）も元EXE/旧索引で照合したが、実際のライフサイクルの保証は未実測。

## 4. 独立再現性・進捗を分離

| 対象 | 今回の値 |
|---|---|
| 原作PE/ZIP/SQLite・manifest等の元検証 | **7/7 PASS** |
| 原本RTTIと旧DB型シンボル | **7/7 PASS** |
| 指定機械語 | **38/38 PASS**（うち2箇所は17時台既知） |
| DB整合性/旧関数数 | **2/2 PASS** |
| 原本直接CALL先 | **9/9 PASS** |
| 旧DB登録CALL site | **9/9 PASS** |
| 旧Ghidra擬似Cマーカー照合 | **7/7 PASS** |
| 局所の分岐先 | **4/4 PASS** |
| **独立静的検査合計** | **83/83 PASS** |
| 過去報告のWave1–5 VERIFIED | 64/64（古い同期ファイル・今回正式再認定なし） |
| 新規REA VERIFIED | **0件** |
| 正式5種 `info/pseudo/assembly/callers/callees` 新規完全充足 | **0関数** |
| 正式TODO / VERIFY / BLOCKED 台帳の書込差分 | **0 / 0 / 0** |
| 新規独立VERIFY研究記録 | 1件（**未同期**） |
| 原作Golden実測PASS / strict MATCH | **0 / 0** |
| 完全複製率 | 未測定 |
| 新規REA / Ghidra / ゲーム起動 | **0 / 0 / 0** |

**83は対象を限定した比較チェック数であり、83関数を逆コンパイルした数でもゲーム互換性の百分率でもない。** 部分ASM、Ghidra機械疑似Cと直接/間接参照を照合したが、正式REAの5種全セットは未完成。過去Waveと重複しないことは一部の旧証拠と照合できたのみで、最新PC正本との全ID比較は未了。

監査スクリプト単体の時間 **1.085秒（この実行のみ）**。作業全体の所要時間は未計測。PCのCPU/RAM・電源稼働状態は不明。安全拒否済みVA `0x5710C0..0x571500`、Wave6、REA Exportには触れず、原本ZIP/EXE/SAVE、MASTER、A～E、Git、QUEUE、PROGRESS、スケジュールは変更なし。

## 5. 未解決・Golden条件・次のP0

1. `0x005B0A50`（ArmyChipBuilder vslot+4）の**実際の間接CALL siteと呼出条件**、および `0x00491870` へ到達する状態を確定する（今回はvtable*配置*までであり動的到達は未証明）。
2. `context+0x1EED4C` と `+0x1EED50` の値の生成元・実用上の違いをDBの局所 `callers/callees/related` と原本ASMで追跡する。
3. 同一キーをモード1/4の順に再登録したときの旧フラグ保持、未登録キー、モード0、空の除外ツリー、遅延イベント復帰をゲームGoldenの独立ケースとして設計する。**すべて未実測**。
4. PC復帰後は最新MASTER/owner/lock/QUEUE/PROGRESS、V3/V4状態、source SHAと既存研究IDを確認し、過去の未同期記録との競合/重複を除外したうえでREA担当範囲へ一度だけ同期する。

## 6. 再開記録

**RECOVERY-ID:** `REA-RC-20261024-18H-LOCAL429-OFFLINE-01` / **研究ID:** `REA-OFFLINE-20261024-1836-P0-ARMYCHIP-FLAG-CONSUMER-VTABLE-STATIC-01`。ローカル接続の実エラーは `429 from openai.org`（接続・制限、拒否ではない）。未達：PC正本の最新確認と正式同期、現行DBとの差分、Golden実測、実際の間接CALL siteと `+0x1EED4C/+0x1EED50` 意味論。再開地点：`0x005B0A50` vslot+4 を起点とする仮想CALLサイトと `0x00491870` のフィールド2つの所有関係。**Libraryへ独立保存したとしても PC-SAVED/正式 VERIFIED の表現を使用しない。**
