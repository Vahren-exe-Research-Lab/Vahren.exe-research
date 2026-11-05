# 迫真戦記 ver0.67｜REA P0独立静的研究（2026-10-25 13時台）

**研究ID** `REA-OFFLINE-20261025-1333-P0-CALLOC-OVERFLOW-CALLERS-STATIC-01`  
**状態** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**所有** REA独立証拠（他レーン・MASTER・QUEUE・PROGRESS・Gitは変更しない）  
**復旧ID** `REA-RC-20261025-1333-LOCAL-SESSION-TERMINATED-01`

## 1. 基盤・保全

- Windows PCの `MASTER_LEDGER.md` / `evidence/ANALYSIS_LANES_PROTOCOL.md` / REA README・QUEUE・PROGRESS および検索基盤の確認を Desktop Commander Local Compact で試みたが、操作は `INVALID_ARGUMENT: McpServerError: Session terminated`。これは接続エラーであり、安全拒否ではない。PCが実際に起動中か、最新版owner/active.lock/既存run、CPU/RAMは**未確認**。
- 代替資料：ChatGPT Libraryに実在する `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `/Vahren.exe` を読み取り専用で使用。原本の改変・起動なし。
- ZIP SHA256：`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34エントリ・CRC全件PASS。
- EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回実測）。
- ZIP中の旧SQLite SHA256：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（今回実測、manifest一致）。SQLite quick_check=ok。一時コピーのみを `mode=ro&immutable=1` で読み、再解析・Ghidra/REA起動はしていない。
- 旧2026-10-21の検索基盤は2026-10-22の更新済みcanonical V3より古い。現行PC検索DBに同期済みとは扱わない。
- ZIP内の `research_snapshot/MASTER_LEDGER.md` と `ANALYSIS_LANES_PROTOCOL.md` を参照。旧 `PROGRESS.md` は2026-10-09現在の15/16であり、PC最新のREA正本でも過去報告のWave1～5 64件の代用品でもない。ZIPにREA `QUEUE.json`・`README.md` および現行run/evidenceは収録されていない。

## 2. P0解析対象と非重複

対象：`0x005C303C` `__calloc_impl`、`0x005BAFF3` `__calloc_crt`、`0x005D1C71` `_calloc`、補助 `0x005BBA77` `__callnewh`。前回12時台の `_realloc` 巨大サイズとerrno解析は既知成果として参照のみ。今回は **callocの乗算ガード・errno経路の呼出元差分・CRT wrapperでの再試行**を新しく結合し、その機械語の分岐先と呼出索引を検証した。09時台に安全拒否された別監査ファイルの追記や同操作の迂回は行っていない。

### 2.1 乗算オーバーフローではnew-handlerへ入らない

原作EXE機械語：

```asm
0x005C3041 MOV ECX,[EBP+8]              ; count
0x005C3044 TEST ECX,ECX
0x005C3046 JE  0x005C3063               ; count=0
0x005C3048 PUSH 0xFFFFFFE0
0x005C304D DIV ECX                       ; unsigned limit/count
0x005C304F CMP EAX,[EBP+0x0C]          ; size
0x005C3052 JAE 0x005C3063              ; fits
0x005C3054 CALL 0x005BCBB7             ; __errno
0x005C3059 MOV [EAX],0x0C               ; ENOMEM
0x005C305F XOR EAX,EAX
0x005C3062 RET
```

`count>0 && size>floor(0xFFFFFFE0/count)` なら早期に `errno=12` を直接設定してNULL返却。`HeapAlloc`、`new-mode`検査、`__callnewh`、オプションの `errno_out` 引数より**前**の独立経路である。`count=0` では乗算結果0が1バイトへ正規化される。通常積がガードを通過した場合は必ず `product<=0xFFFFFFE0` なので、後段 `0x005C3074 JA 0x005C3089` は一般の符号なし32bit入力から到達しない（当該条件下の算術的証明であり、汎用コード全体の到達不能証明ではない）。

`0x005C307F CALL [0x00609134]` はHeapAllocのインポートポインタ経由**間接CALL**。引数 `flags=8` は `HEAP_ZERO_MEMORY`。失敗時は `0x005C3089` のnew-mode判定で、設定が非0かつ `__callnewh(確保バイト数)` が非0なら再試行、そうでなければ `errno_out` が非NULLのときだけ `*errno_out=12` を書きNULLを返す。**乗算ガードの早期失敗と区別すること。**

### 2.2 同じ内部関数を呼ぶ二つのwrapperのerrno差分

| 経路 | CALL site | errno_out | 通常の確保失敗 | 乗算ガード失敗 |
|---|---|---|---|---|
| `__calloc_crt` (`0x005BAFF3`) | `0x005BB004` | **NULL** (`PUSH 0` at `0x005BAFFC`) | `__calloc_impl`ではerrnoへ直接書かずNULL返却 → CRT wrapperのSleep/再試行判定 | **内部関数から直接 `__errno()`、errno=12** |
| `_calloc` (`0x005D1C71`) | `0x005D1C86` | **&local_errno** (`0x005D1C7C`) | `local_errno=12` → NULLかつ非0なら `__errno()` でerrnoへ転記（`0x005D1C99`/`0x005D1CA2`） | 内部関数がerrno=12を直接書くため、local_errno経由の二重転記不要 |

**留意**：HeapAllocや呼び出し側の副作用を含む「errnoが絶対変化しない」の証明ではなく、上記関数内の**明示的なerrno書込み**を追跡したもの。

### 2.3 新発見：CRT専用wrapperの再試行・Sleep境界

`__calloc_crt`は `__calloc_impl` がNULLを返すと、`DAT_0068DC80`（timeout閾値）を見て、閾値が0なら即NULL返却。非0なら `0x005BB01B CALL [0x00609160]`（Sleepインポート関数ポインタ）で待ち、遅延値を1,000ms増加させたうえで閾値と比較し、超えていなければ再度 `__calloc_impl` を呼ぶ。

静的命令：`0x005BB012` (timeout読取)、`0x005BB01B` (Sleep間接CALL)、`0x005BB021` (加算1000)、`0x005BB027` (閾値比較)、`0x005BB037` (retry→`0x005BAFFC`)。過大な積による失敗もwrapperではNULLとして扱われるので、**閾値が非0に変更されれば再試行しても成功しない同じオーバーフローを繰り返す可能性**がある。全て静的制御フロー上の可能性であり原作実行未観測。

`DAT_0068DC80` とnew-mode `DAT_0068E8C0` はPE `.data` のファイル未初期化・仮想確保領域（BSS相当）にあり、通常ロード直後は両者0。旧Ghidra `data_refs` では前者6件、後者3件の**直接READのみ**でWRITE0。間接書込/ランタイム変更を除外できないため通常起動後も永久に0と断定しない。ロード直後の標準設定ではCRT wrapperは最初の失敗で再試行しない。

### 2.4 純粋モデルの境界条件（原作実機を動かしたテストではない）

- `calloc(0,0xFFFFFFFF)` / `(0,0)` → 乗算結果0を1バイトに正規化しHeapAlloc経路。
- `(1,0xFFFFFFE0)` / `(2,0x7FFFFFF0)` → 積が最大値に等しく**早期ガードは通過**（巨大確保が成功する意味ではない）。
- `(1,0xFFFFFFE1)` / `(2,0x7FFFFFF1)` / `(0xFFFFFFFF,1)` → 早期オーバーフローでerrno=12、CALL newhandler/HeapAllocなし。
- `__calloc_crt` で `__calloc_impl` が常にNULLと仮定した純粋分岐モデル：閾値0で1回・Sleepなし、500で1回・Sleep(0)、1000で2回・Sleep(0),Sleep(1000)、1500で2回、2000で3回。これはメモリ不足を発生させた結果でも実機Sleep実測でもない。

## 3. 機械語・DBの独立検証

`REA_OFFLINE_20261025_13H_CALLOC_AUDIT.py` を作成。固定SHA照合、ZIP CRC、SQLite quick_check、PE32セクション範囲、原EXEの対象命令バイト、E8符号付き相対CALLの着地点、短距離条件分岐の着地点、Ghidra `calls`/`indirect_calls`/`data_refs`、BSS、境界値の算術モデルを照合。**112/112項目PASS**（112関数ではない）。独立再実行で同数PASS。対象の大規模再逆コンパイル・疑似C全件再抽出はなし。

REA正式証拠の状態：対象関数の旧DB `info相当 / pseudo / callers / callees` と原作EXEの**抜粋ASM**は調査材料として存在するが、REA所有形式の `info / pseudo / assembly / callers / callees` 5点**関数別完備パッケージ**の新規構築・正式登録・5点の内容保証は未実施。**新規REA VERIFIED=0**。Ghidraの機械出力をそのまま正式VERIFIEDへ昇格させていない。

旧過去記録のWave1～5 `64/64` は今回のPCで検証できないため「過去の申告値」として別枠に置き、増算しない。旧ZIPスナップショットの `15/16` との単純合算もしない。正式QUEUE/PROGRESS未変更なのでTODO/VERIFY/BLOCKED**書込差分0/0/0**。ゲームGolden PASS **0（実機未測定）**、strict MATCH 0（実測なし）、完全複製率未測定。

## 4. 次の候補・Golden設計

P0 `0x005BAFF3` 内の `DAT_0068DC80` 間接更新経路と、`_calloc` (`0x005D1C71`) の `errno` 退避/転記がGhidra推定を超えて実ABIとして一致するかを継続調査する。加えて `0x005D1490` など呼出側の入力値生成を調査し、ゲーム固有データ経路へ接続する。実機Goldenを行う場合は原作の巨大確保を直接強制せず、**隔離したスタブ/モック環境**で `HeapAlloc`・Sleep・new-handlerを制御し、呼出回数、errno、返値、遅延系列を比較すること。実機未実施のためGolden PASSは0。

## 5. 障害・保存境界

- `REA-RC-20261025-1333-LOCAL-SESSION-TERMINATED-01`: Local Compactでの先読一括試行が `INVALID_ARGUMENT / McpServerError: Session terminated`。**CONNECTION**に分類。試行3件とも同一終了エラー。許された次手はPC接続回復時のread-only正本確認・owner/lock・最新ID競合照合後の重複排除同期。安全拒否済みWave6/VA・09時台の監査追記は触れない。
- 原本、ZIP、PCのMASTER/QUEUE/PROGRESS、既存runs、A～E、T018、Git、Work、公開先、自動化設定は未変更。新規Ghidra・REA・ゲーム起動0回。
- CPU負荷・RAM・PC総所要時間：**不明**。独立監査Python単体の実行時間は証拠JSON記録値を参照。
- 今回の出力は本実行環境の `/mnt/data`、および（アップロードできれば）Libraryの専用 `REA_OFFLINE_UNSYNCED` のみ。**PC正本へ保存成功とは記録しない**。PCでのreadbackと正式昇格は未完了。
