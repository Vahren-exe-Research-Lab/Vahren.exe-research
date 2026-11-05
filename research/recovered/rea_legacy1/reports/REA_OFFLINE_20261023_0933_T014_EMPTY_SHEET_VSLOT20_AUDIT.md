# 迫真戦記 ver0.67｜REA独立静的解析：保留シート整理からGameManager仮想スロット+0x20への到達

研究ID：`REA-OFFLINE-20261023-0933-T014-EMPTY-SHEET-DEFERRED-VSLOT20-STATIC-01`  
観測時刻：2026-10-23 09:33 JST（解析回の開始時点）  
区分：**OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**  
対象：T014 / P0 / GameManager状態遷移・シートマップ後始末・未解決間接CALL  
スコープ：原作EXEと2026-10-21 Ghidra検索DBの読み取り専用独立照合。正式REA再実行なし。

## 1. 入力の実在性、既存成果、PC接続

- Desktop Commander **Local Compact**で研究PCの`MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、REA `README.md` / `QUEUE.json` / `PROGRESS.md`、検索DB `README.md` / `BUILD_MANIFEST.json`の一括読取を先行試行した。結果：`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`。**接続・レート制限障害であり安全拒否ではない**。PCの電源、CPU/RAM、最新owner、active.lock、最新のMASTER/QUEUE/PROGRESS/既存runは確認不能。
- 実在をLibraryで確認した旧`MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、`decomp_task.zip`、原作`Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`を取得して先読した。Library資料はPC正本の最新版とは限らない。**旧PROGRESSは旧スナップショットであり現在の正式進捗として上書きしない**。
- 全関数のGhidra再解析・全疑似C再抽出はしない。ZIP内`search.sqlite`、`search.py`、`BUILD_MANIFEST.json`の作業用コピーを読み、対象VAのみ照合。DBはSQLite `mode=ro`、PEはメモリ上で解析。

| 入力・検証 | 結果 |
|---|---|
| 原作`Vahren.exe` SHA256 | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` PASS |
| オフラインパック SHA256 | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` PASS |
| パック全CRC | **34/34 PASS** |
| `search.sqlite` SHA256 | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、BUILD_MANIFEST一致 |
| SQLite `PRAGMA integrity_check` | **ok** |
| 新規REA / Ghidra / 原作ゲーム実行 | **0 / 0 / 0** |

## 2. 新発見：未特定だったGameManager仮想スロット`+0x20`の**実際のCALL site**

既存06:47報告によりGameManager vtableの`+0x20`が`0x004B9DC0`、GameMngBaseでは`0x004BBBD0`を指すことは判明済みだった。ただしどこから仮想CALLされるかが未解決だった。

今回、原作EXEの**`0x004C26BB CALL EAX`**を同定した。所属関数は`0x004C24B0`。この命令は検索DBの`indirect_calls`にも`caller_va=0x004C24B0 / site_va=0x004C26BB / CALL EAX / pcode_callind=1`として登録される。ただしDBは実際のcalleeを解決していない。下記のレジスタ・ポインタ代入とvtable生データの結合が今回の独立静的証拠である。

```asm
0x004C26AB  mov [ebp+0x24], ebx   ; pending map要素数を0へ
0x004C26AE  cmp [ebp+0x14], ebx   ; primary map要素数と比較
0x004C26B1  jne 0x004C26BD       ; 非空なら仮想CALLをスキップ
0x004C26B3  mov ecx,[ebp+0x04]  ; 受信者ポインタ
0x004C26B6  mov edx,[ecx]       ; vptr
0x004C26B8  mov eax,[edx+0x20]  ; vslot +0x20
0x004C26BB  call eax            ; **今回同定した間接CALL**
```

PEの機械語`0x004C26BB=FF D0`とSQLiteの間接CALL索引の双方で裏付け。**もし**構築済みのGameManagerが初期値`[G+0x10]=G`およびvptr`0x00638DF0`を維持するなら、呼出先は`0x004B9DC0`。基底vptr`0x00638E1C`であれば同じスロットは`0x004BBBD0`を指す。全実行状態のvptrが固定という証明ではない。

## 3. 呼出元とレイアウト、発火ゲート

今回照合した呼出連鎖：

```asm
0x004B996B  lea edi,[esi+0x0C]   ; S = GameManager + 0x0C
0x004B99DF  push edi
0x004B99E0  call 0x004C24B0     ; 直接CALL、DBとも一致
0x004C24B7  mov ebp,[esp+0x34]  ; 引数Sを取得
```

`G=GameManager`、`S=G+0x0C`を仮定すると、検証した相対配置は次の通り。あくまでもこの構築済みG経路の静的な位置対応。

| S基準 | G基準 | 役割（暫定名称） |
|---|---|---|
| `S+0x04` | `G+0x10` | 仮想関数の受信者ポインタ（通常の初期化ではG） |
| `S+0x0C` | `G+0x18` | primary sheet map本体 |
| `S+0x14` | `G+0x20` | primary map要素数 |
| `S+0x20` | `G+0x2C` | pending mapの先頭/番兵参照 |
| `S+0x24` | `G+0x30` | pending map要素数 |

`0x004C24B0`はpending mapを処理するが、**次の2条件**を通過しない限り`0x004C26BB`には進まない。

1. `0x004C2642 CMP [EBP+0x24],EBX` → `0x004C2645 JE 0x004C26BD`。pending要素数が0なら末尾のCALLはスキップ。
2. pendingに要素があれば`0x004C2661 CALL 0x00416080`、`0x004C2674 CALL 0x00415CF0`、`0x004C267D CALL 0x00415B90`、`0x004C2695 CALL 0x00416870`等の探索・削除・整理経路を通る。その後`0x004C26AB`でpending要素数をゼロにし、`0x004C26AE`で**primary要素数が0なら**末尾のvslot+0x20 CALLへ進む。primaryが非空ならスキップ。

したがって、**保留処理が存在し、その処理の結果primary sheet mapが空になった場合の通知/更新候補**として説明できる。ただし、pendingの正確なゲーム上の意味、処理順序、削除対象数、例外経路、全実行状態での同一Gは未確定。『必ず最後のシートを削除すると発火する』とは断定しない。

## 4. 既存の先頭登録側との対応（新発見の二重計上は禁止）

前回まで確認済みの登録経路は`0x005433D0`である。

```asm
0x005433F6  mov ebx,[esi+0x20]    ; 登録前のprimary map要素数
0x005433FD  lea edi,[esi+0x18]    ; primary map
0x00543417  call 0x00416B90      ; 挿入
0x0054341C  test ebx,ebx
0x0054341E  jne 0x0054342A       ; 登録前に非空ならskip
0x00543420  mov ecx,[esi+0x10]
0x00543425  mov eax,[edx+0x1C]
0x00543428  call eax              ; vslot +0x1C
```

2本を比較すると、**初回登録経路では`G+0x20`の登録前0を判定してスロット`+0x1C`、保留整理経路では整理後`G+0x20`の0を判定してスロット`+0x20`**という相補的な呼出配置である。なお厳密な「初回」「最後」のユーザー可視イベントとの同一性は原作実機で未確認。`+0x1C`の候補`0x004B9D70`、`+0x20`の候補`0x004B9DC0`は過去特定済みなので**今回の新規成果は後者の実CALL siteおよびゲート条件の同定のみ**。

`0x004B9DC0`自体にも`0x004B9DCB`に`[ECX+0x1EF148]`を判定する命令と`0x004B9DD1 JE 0x004B9E4B`がある。したがってvslot+0x20が実行されても、フラグ値によって書込を伴う更新は回避され得る。`+0x1EF148`の書込元は引き続きP0/VERIFYであり、既存の速度設定処理の仕様をここで新規確定しない。

## 5. 機械的検証と正式進捗

付属`verify_rea_t014_empty_sheet_vslot20_20261023.py`はPE32セクション表を用いてVA→実ファイル位置を計算し、原作機械語・相対CALL先・vtableエントリ・分岐先・SQLite索引・Ghidra疑似Cハッシュを検証する。**原作実行や新Ghidra解析、REAの再問い合わせは一切しない**。

| 検証 | 結果 |
|---|---:|
| 原作EXEの機械語命令VA | **42/42 PASS** |
| 相対直接CALL先の再計算とSQLite照合 | **6/6 PASS** |
| 間接CALL索引（今回`0x004C26BB`、既存`0x00543428`） | **2/2 PASS** |
| 条件分岐の生バイトからの到達先再計算 | **4/4 PASS** |
| 派生・基底のvtable `+0x1C/+0x20` | **4/4 PASS** |
| 対象13関数のGhidra疑似C SHA256 | **13/13 PASS** |
| ZIP CRC / SQLite整合性 | **34/34 PASS / ok** |

Ghidra検索DB内の疑似CハッシュやCALL索引は**機械抽出証拠**でありREA正式の5種一式（`info/pseudo/assembly/callers/callees`）の再取得・検証に該当しない。今回各種の参照は確認したが、**新規5種完成は0関数、REA VERIFIEDは0件**。以前のWave1〜5 **64/64**は過去報告値であり今回独立認定しておらず、古い`PROGRESS.md`の15/16とも加算しない。

| 項目 | 結果 |
|---|---:|
| 公式TODO/VERIFY/BLOCKED書込差分 | **0/0/0**（正本現況は未確認） |
| 独立した未解決P0 | `GameManager+0x1EF148` writer / 呼出時受信者生存性、依然**VERIFY** |
| 原作実機Golden PASS | **0** |
| strict MATCH | **0** |
| 完全複製率 | 未測定 |
| 新規安全拒否 | **0** |
| 独立検証スクリプト実行時間 | 初回約**3.8763秒**（JSON参照） |
| 調査全体の時間・研究PC CPU/RAM | 不明 |

## 6. 未実施Goldenの観測設計（PASSではない）

確認すべき実行時条件を明示する。

- ケースA：`[G+0x30]==0`、`0x004C2645`から整理/仮想CALLをスキップすること。
- ケースB：pendingが非空でも整理後`[G+0x20]!=0`、`0x004C26B1`から仮想CALLをスキップすること。
- ケースC：pending非空からprimaryが空へ変化した時、`0x004C26BB`直前に`ECX==[G+0x10]`、`[ECX]`が期待するvptrであることをスナップショット取得。
- ケースD：GameManager派生/基底のvptr違い、`+0x1EF148`が0/非0の場合の`0x004B9DC0`の副作用、返却時の状態・間隔等を個別観測。

現在これらを**測定していない**。原作正常returnの偽装やGolden PASSの捏造を禁止。

## 7. 重複・権限・再開位置

**先行との差分**：06:47には`vtable+0x20→0x004B9DC0`が既知、08:36にはPlayer→GameWindow→GameManagerの参照関係が既知。今回初めて具体的な仮想CALL site `0x004C26BB`、pending/primaryの二段ゲート、`0x004B9930→0x004C24B0`の直結、登録側`0x00543428`との対応が1つの静的証拠として確認された。PC最新正本および他AIの未同期IDとの完全な重複照合はまだできないため、正式採番・MASTERへの反映は未実施。

接続障害ID：`REA-RC-20261023-0933-LOCAL-SSE429-01`。対象：PC正本参照。試行：Local Compact一括読取1回。実際の理由：MCP SSE probe HTTP 429。影響：PC最新run/owner/lock/競合/同期の確認不能、REA起動条件未充足。未保存発見：**今回の静的追加証拠は当初PC未保存**（独立成果として保存し、Library読み戻し成否は外部確認後だけ記載）。許可された次手：PC復旧時に`MASTER`・レーン規約・最新`QUEUE/PROGRESS`・最新runs/evidence・owner・`active.lock`・source SHA・同IDを先読し、変更衝突・重複を確認したのちREA担当所有域の必要最小部分へ一度だけ同期。Remote・異なるシェル・ZIP等で既拒否Wave6/0x5710C0..0x571500/REAエクスポートを迂回しない。

**次のP0**：`GameManager+0x1EF148`の別名経由writerとメモリ初期化・ロード時の書換え経路。副次調査は`Player`仮想スロット`+0x0C（0x0051EF80）`の具体的CALL site。今回解決した`0x004C26BB`を未解決として再計上しない。製品EXE、原本ZIP/SAVE、A〜E、MASTER、T018、dev_lab、Git、既存スケジュールは変更しない。
