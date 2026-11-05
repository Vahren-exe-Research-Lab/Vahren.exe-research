# 迫真戦記 ver0.67｜REA独立T014：MSVC例外アンワインド／ヒープ読込失敗の局所証拠

**独立ID**：`REA-OFFLINE-20261022-1230-T014-MSVC-EH-FUNCINFO-HEAP-GATE-STATIC-01`  
**分類**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**解析日**：2026-10-22 12時台（JST）  
**対象**：原作EXE `0x45E7F0`、Ghidra分割位置`0x45EAC0`、ヒープ読込CALL `0x45F6A1→0x5964C0`、MSVC EHメタデータ`0x655030`、catch `0x45F933`。REA/Ghidraの再実行なし。

## 1. 接続・証拠状態と旧runの確認

Desktop Commander Local CompactでPC正本のMASTER先頭を読み取ろうとしたが、`INVALID_ARGUMENT / McpServerError: Session terminated`。これは**接続不能**であり、安全拒否の判定ではない。PCの起動状態、最新MASTER/QUEUE/PROGRESS/runs/owner/lock、CPU/RAMは**未確認**。新規PC書込み・正式同期なし。接続復旧記録ID：`REA-RC-20261022-1230-LOCAL-SESSION-TERMINATED-01`。Work不使用。

前回 `REA-OFFLINE-20261022-1134-T014-PARTIAL-READ-OWNER-GATE-STATIC-01` の検証スクリプトを同一の読取専用ソースへ再実行し、命令30/30、直接CALL11/11、SQLite CALL索引4/4がPASS（約1.192秒）。過去の成果を破棄・再計上していない。

- Library正本ZIP `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`：CRC 34件PASS、SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。
- 原作 `Vahren(2).exe` 現物：SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- ZIP内 `search.sqlite`：SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、BUILD_MANIFEST一致、SQLite `integrity_check=ok`。
- `search.py`で対象 `0x45E1E0`/`0x45E7F0`/`0x45EAC0`/`0x45F933`/`0x5964C0` の既存Ghidra本文・索引を限定抽出。追加の実アセンブリは同SHAのEXEから指定VAに限定して独立バイト検査。既存REA5証拠が揃ったとみなしていない。

## 2. 新発見A：`0x45EAC0`は独立した関数入口として扱えない

従来の検索索引は `0x45F6A1→0x5964C0` の `caller_va` を `0x45EAC0` と報告していた。しかし、原作機械語の制御フローは次のとおり。

| VA | 原作機械語の意味 |
|---|---|
| `0x45E7F0` | `push ebp`で新しい呼出フレームを開始。関数冒頭で`0x5FD61C`をEHハンドラとして設定 |
| `0x45EABC` | `mov esi,[eax]` |
| `0x45EABE` | `mov edi,edi`（2バイトNOP相当） |
| `0x45EAC0` | `mov ecx,[ebp-0x14]`。直前から**普通にフォールスルー**しており、新しいスタックフレームを作らない |
| `0x45EF03` | 条件分岐 `JE 0x45F66E` |
| `0x45F66B` | 既存の通常経路で `RET 8`。直後の `0x45F66E` は上記条件分岐で到達する別の基本ブロック |
| `0x45F6A1` | `CALL 0x5964C0`（`0x138`バイトのオブジェクト確保・構築後） |

`0x45EAC0`への短距離逆行分岐も3件確認した（`0x45EAE5`、`0x45EAFA`、`0x45EB39`）。Ghidra自身の `FUN_0045e7f0` 擬似C本文にも `FUN_0045eac0:` が**内部ラベル**として出現する。同じコード領域の「別機械出力関数」への分割であって、実行時に独立CALLできる入口とは認定できない。

**既存報告の訂正**：`0x45E52F`（スタック上オブジェクト、実関数入口 `0x45E1E0`）と `0x45F6A1`（ヒープ上オブジェクト、実フレーム入口 `0x45E7F0`）の**2つのCALL siteがある**ことは変わらない。ただし後者の呼出元を`0x45EAC0`独立関数として扱った点は危険。将来のフックでその位置を普通の関数入口として利用しない。索引の関数数を機械的に「独立に呼出可能な関数の数」と見なさない。

## 3. 新発見B：MSVC EH FuncInfo／状態遷移を現物で復元

`0x45E7F0`のEHハンドラ `0x5FD61C` は、原作機械語 `0x5FD63D` で `0x655030` を渡す。PE節のVA→raw offset変換を検証後、MSVC x86 `FuncInfo`を直接読み取った。

| FuncInfoフィールド | 現物値 |
|---|---|
| magicNumber | `0x19930522` |
| maxState | **30** |
| pUnwindMap | `0x654EF8` |
| nTryBlocks | **2** |
| pTryBlockMap | `0x655008` |

対象の重要なUnwindMap要素は次のとおり。

| EH state | 次のstate | unwind action | 観測した役割 |
|---|---:|---|---|
| **15** | **9** | `0x5FD5DB` | `[EBP-0x20]`のポインタを `0x5B6BBB` に渡して解放。**コンストラクタ途中の生メモリ**向け |
| **9** | **6** | `0x5FD56E` | `[EBP+0x80]`を `0x4026B0` に渡す。局所文字列・一時領域の後処理 |
| 16 | 9 | `0x5FD5E6` | 別の局所一時領域の終了処理。今回は補助情報のみ |

ヒープ読込経路は `0x45F67E` で state=15、`0x45F687` で `0x590560` のオブジェクト初期化を実行し、**初期化から復帰した後** `0x45F692` で state=9、`0x45F69E` でオブジェクトポインタを `[EBP-0x18]` に保存、`0x45F6A1` で `0x5964C0` を呼ぶ。したがって**読込中の例外に対しては state=9 のunwind経路が対象**であり、state15の `[EBP-0x20]` 生メモリ解放アクションを当然に適用できるわけではない。

ここが前回までの推測を前進させた、**実機械語とEHデータを独立に突き合わせた静的証拠**である。

## 4. 新発見C：catch-all登録と二次的LoadException送出

2件目のTryBlockMap：`tryLow=6`、`tryHigh=16`、`catchHigh=17`、`nHandlers=1`。HandlerTypeレコード`0x654FF8`は、型ポインタ`0`（catch-all）、フラグ`0x40`、handler VA **`0x45F933`** を保持する。この対応は通常の直接CALL索引に現れないため、C++ EHマップを独立参照する意義がある。

`0x45F933`の実機械語は `[EBP-0x1C]` を `0x5B71DD` に渡し、`0x5B6522`で例外オブジェクトを構築し、`LoadException`のvtable値`0x63852C`を設定、`0x5B864E`へ例外を送出する。`[EBP-0x1C]` は`0x45E8F5`で読み込んだファイルバッファを格納している。**このcatch内で直接解放されるのはファイルバッファであり、`[EBP-0x18]`にある構築済みヒープオブジェクトとは別である。**

**VERIFYの境界**：確認したstate9→6アクションとcatch `0x45F933`の局所命令には、`[EBP-0x18]`の完成オブジェクトに対する専用デストラクタ／deleteがない。これは**例外時リソース解放漏れ候補**になるが、上位での所有権移転、別経路の破棄、ランタイムの例外挙動までは未検証。原作の恒久的メモリリークや部分更新オブジェクトのゲーム上残存を断定しない。

## 5. 増分・指標・再開可能性

| 指標 | この回の状態 |
|---|---|
| オフラインパック／旧11:34検証 | ZIP CRC PASS／SQLite PASS／旧スクリプト再検証PASS |
| 新規独立静的確認 | 実命令22箇所、CALL・分岐13箇所、EH state30件、TryBlock2件（今回の機械的チェック） |
| 新規REA正式 VERIFIED | **0件** |
| 新規REA `info/pseudo/assembly/callers/callees` 5種類一式 | **0関数**。個別の既存REA証拠充足はPC不通で不明 |
| Wave1～5 | **64/64**は前回報告の歴史値で、今回正本と独立照合はしていない |
| 正式TODO/VERIFY/BLOCKED差分 | **0/0/0**（QUEUE未変更） |
| 原作Golden PASS／strict MATCH | **0/0**（原作起動なし、完全複製率不明） |
| 新規Ghidra/REA実行 | **0/0**。旧例外処理・疑似C・EXE読取りだけ |
| Python検証 | 前回分1.192秒／今回分約1.229秒（全調査所要時間は未計測） |
| PC負荷 | CPU/RAM不明。接続不能によるもので安全拒否ではない |
| 原本/他レーン/MASTER/Git/スケジュール | **変更なし** |
| 保存状態 | 本MD＋機械可読JSON＋再検証Pythonを独立保存。PC正本への正式同期はまだ行っていない |

**関連証拠**：`REA_OFFLINE_20261022_1230_T014_MSVC_EH_EVIDENCE.json`は原作/ZIP/SQLiteのSHA、対象関数5件の擬似C SHA、22箇所の原本命令、制御フロー、MSVC 30-state unwind map、2 TryBlock/handlerレコードを収録。`verify_rea_t014_eh_20261022.py` は保存済みパック・EXEのみを読み取り、別のJSONへ独立再出力できる。Ghidraの新しい一括抽出は不要。

**次回P0**：`0x45E1E0`のスタック上オブジェクトのEH mapと `0x45E7F0`のヒープオブジェクトの対比を行い、`0x45F933`から例外が上位へ届くときのcleanup範囲をさらに分類する。特に`0x45F6A1`失敗時にどの地点までオブジェクトが公開され得るか、`0x436560/0x436680/0x463280`が所有権移転を担うかを確認する。別件`0x42ECF0`（64bit ABI）、`0x470AE3`（仮想CALL）はVERIFY据置。

**同期ガード**：研究PCへ接続が復帰したらMASTER、解析規約、最新QUEUE/PROGRESS、run/evidence、owner/active.lock、旧報告ID・ハッシュ・競合を再照合し、既存証拠への二重登録を避けてREA所有の許可範囲へ1回のみ統合する。接続不可を理由に研究全体は停止しない。過去の安全拒否済みVAやWave6/REA exportを別経路で再試行しない。
