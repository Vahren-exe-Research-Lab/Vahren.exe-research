# 迫真戦記 ver0.67｜REA独立T014 P0：「ガード」の正体はキー登録木の件数（2026-10-22 19時台）

**研究ID:** `REA-OFFLINE-20261022-1946-T014-MAP-COUNT-FIRST-INSERT-STATIC-01`  
**状態:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**対象:** `0x543428`（間接CALL）、`0x5433D0`（呼出元）、`0x416B90`（map登録）、`0x4165B0`（mapノード挿入）。独立した比較対象：`0x4322E7`（event側間接CALL）。

## 1. 正本・旧run・検索基盤の有効性

まずDesktop Commander Local Compactの`read_multiple_files`を試行したが、`INVALID_ARGUMENT / McpServerError: Session terminated`で失敗した。これは**接続障害**。安全拒否とは区別し、PCの電源・CPU/RAM・現行owner/lock・最新QUEUE/PROGRESS/MASTER・V3/V4の状態は**不明**とする。

他方、ChatGPT Library上に実在する`/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`と`/Vahren(2).exe`を新たに検索・materializeして現物SHA256を測定し、ZIP CRC=34/34 PASS・ZIP内SQLiteと抽出SQLiteのバイト同一・manifest SHA一致・SQLite `PRAGMA integrity_check=ok`を確認した。Ghidra/REA/ゲームの実行はゼロ。旧スナップショット`PROGRESS.md`は2026-10-09時点の初期**15/16**を記録する。別時点のWave1〜5 **64/64**は過去報告値で今回再確認できないため、合算しない。

| 出典 | 現物SHA256 |
|---|---|
| 原作PE32 EXE（読取専用） | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP（読取専用） | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP収録`search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

## 2. 新発見：`context+0x20`は任意の「状態フラグ」ではなくmapの件数

先行15:33～18:36報告は`0x5433F6`で`context+0x20`を先取りして、ゼロなら`0x543428`を呼ぶことまで確認済みだった。しかし`+0x20`の**意味**は未解決だった。今回はその直前のmap登録の実アセンブリと、下位登録関数内の件数増分までつなげた。

原作機械語（VAとオペランドを実測照合）：

```asm
0x5433F3 mov esi,[esi+0x04]  ; ESI = context
0x5433F6 mov ebx,[esi+0x20]  ; 登録前の map 件数をスナップショット
0x5433FD lea edi,[esi+0x18]  ; map オブジェクトの基点
...
0x543417 call 0x416B90      ; この map へ "sheet" キーを登録/既存キー照合
0x54341C test ebx,ebx       ; 登録後の最新件数でなく、登録前の件数
0x54341E jne  0x54342A
0x543420 mov ecx,[esi+0x10] ; 別オブジェクトをthisとして取得
0x543425 mov eax,[edx+0x1C]
0x543428 call eax            ; 登録前件数が0のときのみ実行
```

`0x416B90`内部は受け取ったmapの`+0x04`からRB-treeのヘッダを読み、キー比較・既存キー検索・挿入を行う。挿入経路から`0x4165B0`を`0x416C3C`または`0x416C86`でCALLする。`0x416C3A mov edi,ecx`は前者で**EDI=map基点**を確立する。

```asm
0x4165B0 mov ecx,[edi+0x08]  ; mapの要素数を読み取る
...
0x4165F7 inc ecx             ; 成功する新規挿入で1増加
0x4165F8 mov [edi+0x08],ecx  ; mapの要素数を書き戻す
```

`map = context+0x18`なので、`map+8 = context+0x20`。これは機械語上の位置とmapの実際の挿入処理が連動する、**直接的なフィールド同定**である。「map/set<T> too long」分岐、ヘッダ・左右の木ポインタ・色フラグ等もRB-tree解釈と整合する。

| 基準アドレス | フィールド | 判定 |
|---|---|---|
| `context + 0x18` | キー登録用mapオブジェクトの先頭 | 機械語+疑似C確認 |
| `context + 0x1C` | mapヘッダ/番兵ポインタ（map+4） | `0x416B97`等に確認 |
| `context + 0x20` | **map要素数**（map+8） | `0x4165B0`の件数増分に確認 |
| `context + 0x10` | 二次オブジェクトへのポインタ | 正体・vptrは未確定 |

**局所的な結論：`0x543428`の間接CALLは、`"sheet"`の挿入による「初回のみ」を直接検査しているのではなく、**登録を始める前の**共有キー登録mapが空（要素数0）だったかで判断している。**別キーが事前に存在するなら`sheet`キーが新規でも呼出しをスキップ**する。正常なmapで登録前0件なら、挿入成功経路は0→1件となる一方、条件判定は保存済みEBX=0に依存する。

このため以前の「`context+0x20`はガード値」「途中関数が値を変更するか未確認」という記述は、今回**件数フィールドであることと、map挿入で増加し得ることを確認した**内容で更新する。ただし、動的に必ず成功する、例外時も実行される、全11サイトが同一mapを共有する、呼出先が再描画通知である、などは断定しない。

## 3. 独立裏付け：event側も同じmap件数を先取り

別経路 `0x4321B0` の実命令：

```asm
0x4322B2 mov ebp,[ebp+0x04]   ; context
0x4322B5 mov edi,[ebp+0x20]   ; 登録前のmap件数
0x4322BC lea esi,[ebp+0x18]   ; 同mapの先頭
0x4322D6 call 0x416B90        ; "event" キー登録
0x4322DB test edi,edi
0x4322DD jne  0x4322E9
0x4322DF mov ecx,[ebp+0x10]   ; 二次オブジェクト
0x4322E7 call edx             ; vtable+0x1Cから取得
```

この経路でも`map=count`の関係が成立する。16:33や17:35報告の「別キーの11同型サイト」は**今回の追加件数としては計上しない**。今回は`sheet`と`event`の二経路について**条件フィールドの意味を新規解明**したのであり、11経路全部の実行時型やmapインスタンス同一性を証明したものではない。

## 4. 保守・互換性への影響

今後のDLLフックで`0x5433D0`を一度呼び出したあとにもう一度呼んでも、二回目はmap件数が非ゼロなら`0x543428`の間接CALLをスキップし得る。すなわち、以前報告した複数データ構造への重複登録に加え、**登録前map件数に応じて間接CALLの有無も変わる**。部分処理を差し替えるなら「元の件数」「実際に追加したキー」「既存登録の副作用」を区別する必要がある。

ただし`0x543428`の実装VAおよび`context+0x10`の代入元/クラス/ABI全体は依然**VERIFY**。`context+0x10`がNULLではないことを`+0x20`条件だけで保証できない点も次の静的検査対象。通常の呼出し規約、別の初期化・例外経路、gameplay Goldenは追加証拠待ち。

## 5. 今回の独立検証・正式進捗

| 指標 | 結果 |
|---|---|
| PE固定位置命令バイト | **29/29 PASS** |
| E8 rel32直接CALL＋SQLite索引 | **4/4 PASS** |
| 間接CALL索引 | **2/2 PASS** |
| Ghidra疑似C本文SHA | **4/4 PASS** |
| SQLite整合性 / ZIP CRC | **PASS / 34/34 PASS** |
| 今回新規REA5種類完全証拠 | **0関数** |
| 今回の新規REA正式VERIFIED | **0件** |
| 正式TODO/VERIFY/BLOCKED差分 | **0 / 0 / 0**（PC正本未変更） |
| 原作実機Golden PASS / strict MATCH | **0 / 0** |
| PC CPU・RAM / 全調査所要時間 | **不明 / 未計測** |
| 専用静的検証器の実行時間 | 約**1.93秒** |

5種類の証拠区分：`info`/`pseudo`は旧Ghidra検索DB、`assembly`は原作PEの独立バイト照合、`callers`/`callees`は旧SQLite索引。**REA6.1.0が個々の関数について5種類を正式保存したことを今回は確認できず、0件昇格**。原作実行なし。過去の64/64 VERIFIEDは過去報告値のまま。

## 6. 未解決と復帰手順

P0次回：`context+0x10`のwriter、生成関数、vptr設置・動的型分岐を旧DBから優先抽出し、`0x543428`の実際の候補VAを絞り込む。並行して`0x433E80`の親入口`context+0x20`チェックを「map件数での早期終了」として照合する。`0x5AA6E0`のジャンプテーブル警告・Wave6拒否済みの対象を別枠で保持し、拒否操作を迂回・再実行しない。

新規独立証拠は`REA_OFFLINE_20261022_1946_T014_MAP_COUNT_FIRST_INSERT_EVIDENCE.json`、再検証コードは`verify_rea_t014_map_count_gate_20261022.py`。研究PC正本・原本・MASTER/QUEUE/PROGRESS・A～E・Git・スケジュールは変更しない。接続障害ログID：`REA-RC-20261022-1946-LOCAL-SESSION-TERMINATED-01`。接続復帰時は最新所有権/lock/既存ID/現行DBのsource SHA/V3-V4と競合照合したうえで、REA担当領域に一度だけ同期する。

**保存状態はLibrary upload/readbackの実測結果に基づいて別途更新する。PC正本は未同期。**
