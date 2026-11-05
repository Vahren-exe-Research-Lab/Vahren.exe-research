# 迫真戦記 ver0.67｜REA独立静的研究 T014（2026-10-23 10時台）

**研究ID:** `REA-OFFLINE-20261023-1033-T014-SCRIPTBATTLE-PLAYER-VSLOT0C-STATIC-01`  
**分類:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**優先課題:** T014/P0・Player仮想関数 `0x0051EF80` の実呼出箇所と、ScriptBattle開始処理との接続。  
**保全:** PC正本への保存なし、原本/MASTER/QUEUE/PROGRESS/他レーン/Git/既存スケジュールの変更なし。新規Ghidra/REA/ゲーム実行なし。

## 1. ソース・既存成果の再確認

Desktop Commander Local CompactでMASTER、ANALYSIS_LANES_PROTOCOL、REA管理文書の一括read-only読取を試行したが、`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`で失敗。接続制限であって安全拒否ではない。PC電源、所有者の最新ファイル、active.lock、プロセス、CPU・RAM使用量は不明。

ChatGPT Library既存の `Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`decomp_task.zip` を正規の権限で取得し、次を読み取り専用で検証した。

| 項目 | 検証結果 |
|---|---|
| 原作Vahren.exe SHA256 | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` PASS |
| オフラインパック SHA256 | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` PASS |
| search.sqlite SHA256 | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` BUILD_MANIFEST一致 |
| オフラインパック CRC | 34/34 PASS |
| 旧decomp_task.zip CRC | 656/656 PASS |
| SQLite PRAGMA integrity_check | `ok` |
| 旧PROGRESS.md | 2026-10-09時点15/16（古い記録） |
| 既往Wave1～5 64/64 | 過去の報告値。今回再認定していない |

全関数の再解析は実行せず、`search.py function / callers / related` と既存SQLiteから対象と周辺を抽出した。Ghidra疑似Cは仮説補助、最終的な命令・分岐・vtableは原作PE32の実バイトで照合。

## 2. 新規発見①：ScriptBattle RTTI の真分岐から戦闘処理関数を呼ぶ

**呼出元 `FUN_004338D0`、CALL site `0x00433E58`。** 機械語：

```asm
0x00433B27  PUSH 0
0x00433B29  PUSH 0x0068C29C ; ScriptBattle RTTI識別情報側
0x00433B2E  PUSH 0x0068C24C ; ScriptElement RTTI識別情報側
0x00433B33  PUSH 0
0x00433B35  PUSH EDI
0x00433B36  CALL 0x005E72E5 ; RTTI動的キャスト相当
0x00433B3E  TEST EAX,EAX
0x00433B40  JNE 0x00433E4A ; 成功時、相対分岐先を再計算して一致

0x00433E4A  MOV ECX,[ESI+0x1E8630] ; Playerオブジェクト
0x00433E50  PUSH 1
0x00433E52  CALL 0x0052BFF0 ; 前処理（意味は未完全解析）
0x00433E57  PUSH EDI        ; 元のScriptBattle要素ポインタ
0x00433E58  CALL 0x00492890 ; T014今回のディスパッチ主体
```

`FUN_004338D0`の抽出済みGhidra疑似Cにも`ScriptBattle::RTTI_Type_Descriptor`および`FUN_00492890`への条件付き分岐が存在し、実命令・SQLite直接CALL索引と一致。関数の受信者やRTTI判定に失敗する経路、スクリプトカーソルの進行条件は別途VERIFY。

## 3. 新規発見②：`FUN_00492890`は3オブジェクトの同じ仮想スロットを順番に呼ぶ

原作機械語、Ghidra疑似C、SQLiteの**間接CALL索引3件**を照合。

```asm
0x00492A2F  MOV [ESI+0x1EEDEC],EBX
0x00492A35  CMP BYTE PTR [ESI+0x1EED40],BL
0x00492A3B  JE 0x00492A43
0x00492A3D  PUSH ESI
0x00492A3E  CALL 0x0049D6A0 ; 条件成立時だけ実行

0x00492A43  MOV ECX,[ESI+0x1E8630] ; Player*
0x00492A49  MOV EDX,[ECX]          ; vptr
0x00492A4B  MOV EAX,[EDX+0x0C]
0x00492A4E  CALL EAX                ; ① Player仮想関数

0x00492A50  MOV ECX,[ESI+0x1E8634] ; Enemy(引数2で初期化)*
0x00492A56  MOV EDX,[ECX]
0x00492A58  MOV EAX,[EDX+0x0C]
0x00492A5B  CALL EAX                ; ② Enemy仮想関数

0x00492A5D  MOV ECX,[ESI+0x1E8638] ; Enemy(引数4で初期化)*
0x00492A63  MOV EDX,[ECX]
0x00492A65  MOV EAX,[EDX+0x0C]
0x00492A68  CALL EAX                ; ③ Enemy仮想関数
0x00492A6A  MOV ECX,[ESI+8]        ; 呼出し後に続く初期化
```

注意：3つの`CALL EAX`は同じ命令形式だが、**受信者は別オブジェクト**。実行前に`0x0049D6A0`が実行される条件があり、その副作用は完全には分かっていない。`[ESI+0x1E8630/34/38]`の実行時非NULLやvptr不変性は未実測。

## 4. 新規発見③：コンストラクタ追跡とvtableから3件の候補先を具体化

`FUN_0048A5B0`が以下のインスタンスを生成・格納することを実命令で確認。

| オブジェクト保管 | コンストラクタ呼出 | 保存命令 | 初期化済みvptr | `vptr+0x0C` の実ポインタ |
|---|---|---|---|---|
| `engine+0x1E8630` | `0x0048A93D CALL 0x0051E100` Player | `0x0048A952` | `0x00639B08` | **`0x0051EF80`** |
| `engine+0x1E8634` | `0x0048A977 CALL 0x00447280` （引数2） | `0x0048A989` | `0x00638B60` | **`0x00447810`** |
| `engine+0x1E8638` | `0x0048A9AA CALL 0x00447280` （引数4） | `0x0048A9B8` | `0x00638B60` | **`0x00447810`** |

元のvptr代入の証拠：`0x0051E13E MOV DWORD PTR [EDI],0x00639B08`（Player派生側）、`0x004472CB MOV DWORD PTR [ESI],0x00638B60`（Enemy基底側）。vtableデータをEXE `.rdata`から独立抽出し、Playerスロット`0x00639B14`は`0x0051EF80`、Enemyスロット`0x00638B6C`は`0x00447810`を保持していると確認。

これは**確認した初期化状態に依存した静的解決先**であり、実行中の全経路に適用できると断定しない。

## 5. 既存研究との接続（重複を除外）

前回までに判明していたPlayer仮想関数の実装`0x0051EF80`について、**今回判明した新規呼出元は `0x00492A4E`**。Player仮想関数の中では`0x0051EF8F CALL 0x00447810`によってEnemyの実装関数をまず直接実行し、その後、`0x0051F035 CALL 0x00513A80`へ進む。後者は前回研究した速度UIの初期化処理。両CALL先の存在・過去のPlayer vtable内容自体は既存成果として扱い、新規件数には加算しない。

このように、**ScriptBattle RTTI→`0x00492890`→Player/Enemy 3オブジェクトの仮想初期化**という明確な制御関係が新たに接続された。これを「戦闘開始から終了までのI/O互換が完成」とはしない。

## 6. 再現性・独立検証

再検証用Pythonは原作EXEおよびオフラインパック内既存SQLiteを**読み取るのみ**。PE32セクションの生バイト、相対CALL/JNE/JE先の再計算、vtable生ポインタ、SQLite CALL/間接CALL/xrefs、既存Ghidra疑似CテキストSHAを確認する。

| 検証 | PASS |
|---|---:|
| 実命令バイト照合 | **52 / 52** |
| 機械語CALL宛先＋DB直接参照索引 | **9 / 9** |
| 間接CALL site＋DBレコード | **3 / 3** |
| JNE/JE分岐先再計算 | **2 / 2** |
| vtable生ポインタ | **4 / 4** |
| Ghidra疑似CのSHA256 | **10 / 10** |
| SQLite整合性 | PASS |
| オフラインZIP CRC | **34 / 34** |
| 旧REAアーカイブ CRC | **656 / 656** |

検証器初回実行時間：約**0.79秒**。研究作業全体の実行時間は計測していない。PC負荷不明。

REAの5種 `info/pseudo/assembly/callers/callees` の追加完全セットは**0関数**。新規正式REA VERIFIED **0件**。Wave1～5 64/64は過去報告値で今回未再認定。旧PROGRESS 15/16は2026-10-09時点の古い値であり足し算・置換しない。正式TODO/VERIFY/BLOCKEDへの書込 **0/0/0**（最新現在値未取得）。原作ゲームGolden PASS **0**、strict MATCH **0**、完全複製率**未測定**。

## 7. 未解決と次の再開位置

**P0 / VERIFY**: 呼出元`0x00492890`の後半で`[engine+8]+8+0x38`の代入が何を結び付けるのかを調べ、`0x00564160`等に渡す戦闘移行情報と、実際の戦闘実行ハンドオフを追跡する。同時に、`0x00433B40`真分岐到達条件（RTTI以外のスクリプトキュー条件）と`0x0049D6A0`がPlayer/Enemyのvptrに影響するかを確認する。`0x0051EF80`及び`0x00447810`での**メモリ差分・正常return条件**をGolden設計の観測点として整理する。`GameManager+0x1EF148`への書込元も未解決。動的GoldenをPASS扱いしない。

**接続障害ID**: `REA-RC-20261023-1033-LOCAL-SSE429-01`。試行：正本5ファイルのLocal read-only一括読取、失敗理由：SSE 429。影響：最新owner/QUEUE/PROGRESS/lock確認とPC正本への同期が不可。許可された対応：ユーザー所有Libraryのオフラインパックのみを利用し、独立成果として保存、復帰時に競合・重複・source SHA・ownerを確認し1回だけ適正同期。**安全拒否対象Wave6 / VA 0x5710C0..0x571500 / 過去拒否済みエクスポートへの迂回再試行なし。**

**保存状況**: 本レポート＋機械可読証拠JSON＋Python検証器を別IDのオフライン成果として作成。Library保存・独立読戻しの成否は別途保存レシートで検証。**PCのMASTER/QUEUE/PROGRESSには反映していない**。
