# 迫真戦記ver0.67 REA｜T014 Player→GameWindow→GameManager→速度UIの所有者経路

- 研究ID：`REA-OFFLINE-20261023-0836-T014-PLAYER-GAMEWINDOW-OWNERCHAIN-STATIC-01`
- 調査開始：2026-10-23 08:36 JST／状態：**OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**
- 対象P0：従前未解決の`[owner+0x188]`の生成元、`0x0051EF80`の仮想呼出し経路、および`0x00513C60`が経由する受信者の所有関係。
- この文書は新規独立静的証拠。既存成果を破棄・新規REA VERIFIEDに二重計上しない。原作EXE、ZIP、SAVE、A〜E、MASTER、T018、Git、既存スケジュールには変更なし。

## 1. 有効性・入力・接続状況

Desktop Commander Local Compactで研究PCの最新MASTER、規約、REA README/QUEUE/PROGRESS等の一括読取を試行したが`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`。**接続系429であり安全拒否ではない**。PCオンライン状態、CPU/RAM、active.lock、PC正本の最新RUN・所有権・重複状況は未確認。Remote等の別経路による拒否の迂回は行っていない。

実在が確認できたChatGPT Libraryのオフラインパック、原作Vahren.exe、旧decomp_task.zipから作業用コピーを取得。検索基盤README/BUILD_MANIFEST/SQLite、旧QUEUE/PROGRESS/既存成果と前回07:36報告を先読。原作ゲーム・Ghidra・REAを実行せず、**作業用コピーのPE命令とDBのread-only検索**のみ。

| 入力 | SHA256 / 検査 |
|---|---|
| 原作Vahren.exe | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`／一致 |
| オフラインパック | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`／CRC **34/34 PASS** |
| 検索DB | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`／manifest一致、`integrity_check=ok` |
| 旧decomp_task.zip | CRC PASS。ただし最新PC正本ではない |

## 2. **新発見A：前回のownerはPlayerとして静的に解決できる**

`0x0051EF80`の呼出元は既存SQLite直接CALL表では0件。ただし原作PEの`.rdata`にある**Player仮想関数テーブル**を調べると、`0x00639B08`を起点とするスロット`+0x0C`（VA`0x00639B14`）には関数ポインタ`0x0051EF80`が入っている。`0x0051E13E`の機械語`C7 07 08 9B 63 00`がPlayerオブジェクトのvptrを`0x00639B08`にする。テーブル手前の`0x00639B04`はRTTI Complete Object Locator `0x0063F2F4`を指す。**直接CALLが無いことは未使用を意味せず、Playerの仮想スロット経由で参照される**（具体的な呼出命令側の実行時到達は未実測）。

GameManager/Player生成の既知の経路を追加照合すると：

1. `0x004B78C0`内`0x004B79B8 CALL 0x004B9E50`の後、同関数`0x004B79D6 CALL 0x0048A5B0`。
2. `0x0048A5B0`は`0x0048A5F4`で`[engine+4]=0x008BE2F0`（GameManager）、`0x0048A5FB`で`[engine+8]=0x008BE378`（後述のGameWindow）を設定。
3. `0x0048A938 MOV ECX,[EDI+4]`→`0x0048A93B PUSH ECX`→`0x0048A93C PUSH EAX`→`0x0048A93D CALL 0x0051E100`。割当が成功した場合に`Player`コンストラクタへGameManagerポインタを渡す。失敗分岐は別扱い。
4. `Player`コンストラクタ`0x0051E100`は基底`0x00447280`、さらに`0x00514740`を呼ぶ。この基底処理の`0x00514808 MOV [ESI+4],ECX`により`[Player+4]=GameManager`。
5. `0x0051E388 MOV EAX,[EDI+4]`→`0x0051E38B LEA ECX,[EAX+0x88]`→**`0x0051E39E MOV [EDI+0x188],ECX`**。よって確認した正常構築経路で**`[Player+0x188]=GameManager+0x88`**。

この事実は前回07:36の`[owner+0x188]`が不明だった箇所を一段解決する。前回のWindow+0x98/+0x9C代入そのものは既知であり、新規実績に加算しない。

## 3. **新発見B：GameWindow+4にGameManager自身を代入する前段処理を解明**

`0x008BE2F0 + 0x88 = 0x008BE378`。この位置にはGameManager内に埋め込まれた`GameWindow`サブオブジェクトがある。`0x00553B20`の原作命令で、`0x00553B64 MOV [0x008BE378],0x00638E78`によりGameWindow vptrを設定し、`0x00553B5E XOR ESI,ESI`に続く`0x00553B6E MOV [0x008BE37C],ESI`でその`+4`を**0**にする。

これに対し、GameManagerのゲーム初期化側`0x004B9E50`には、**`0x004B9F36 MOV DWORD PTR [0x008BE37C],0x008BE2F0`**が存在する。つまり：

```
G = 0x008BE2F0                     GameManager
W = G + 0x88 = 0x008BE378          embedded GameWindow
初期構築: *(W + 4) = 0
0x004B9E50完了後: *(W + 4) = G
Player成功構築後: *(Player + 0x188) = W
```

`0x004B79B8`と`0x004B79D6`のCALL順は同じ関数内で証明可能であり、**通常の非例外初期化順ではGameWindow+4の設定がPlayer構築に先行する**。ここから任意の時点で不変と断言することはできない。

## 4. **新発見C：速度設定UIからGameManagerまでポインタ経路が閉じた**

`Player`の仮想メソッド`0x0051EF80`は、`0x0051EF8D MOV EDI,ECX`で受信者を保持し、`0x0051F02E MOV ECX,[EDI+0x188]`→`0x0051F034 PUSH EDI`→`0x0051F035 CALL 0x00513A80`を実行。

`0x00513A80`は引数を整えて`0x00513A95 MOV ESI,0x0067B290`→`0x00513A9A CALL 0x00453800`へ渡す。前回に確認済みのhelperは静的な**UIWindow**`0x0067B290`に、`[UIWindow+0x83]=1`、`[UIWindow+0x98]=GameWindow`、`[UIWindow+0x9C]=Player`を書き込む。**ここでのUIWindowとGameManager埋込GameWindowは別オブジェクト**。

よってUI初期化後の条件付き連鎖は以下になる。

```
*[0x0067B328]                   = GameWindow (W)
*(*[0x0067B328] + 4)           = *[W+4] = GameManager (G)
0x00513C60: EDX = [0x0067B328]; EAX = [EDX+4]
0x00513C60: ECX = [EDX+4]; ECX += 0x0C
0x00513CB8: CALL 0x004C21F0   (receiver=G+0x0C)
0x004C21F0: [receiver+0x74] / [receiver+0x78] に速度・間隔を格納
結果: [G+0x80] / [G+0x84] を更新
```

**前回は`[[owner+0x188]+4]`がGameManagerであるか未確定だったが、今回の初期化経路上ではGameManagerと静的に結び付いた。** ただし、イベント中のポインタ交換、破棄順、複数Playerインスタンス、後続書込の完全被覆は未検証なので、実機Goldenなしで全状態に一般化しない。

速度変更は無条件ではない。`0x00513C61`のUI有効フラグ、GameManager`+0x1EF148`、`+0x20`、`+0x1EF150`等の条件判定を通った場合のみ`0x00513CB8`に達する。`+0x1EF148`への実際のwriterは依然P0/VERIFY。

## 5. 既存成果との差分／検査

07:36までに`0x0051EF80→0x00513A80→0x00453800`、速度UIの`+0x83/+0x98/+0x9C`、0x00513C60の読出し、0x004C21F0の出力先は確認済み。今回は**Player vtableスロットの同定、`Player+0x188`を生成する命令、GameWindowの埋込構造、GameWindow+4のゼロ→GameManager初期化、初期化時の直接CALL順を結び付けた点**のみ新規。

旧MASTERスナップショットとこのチャットの07:36までのオフライン成果から今回の新規命令位置`0x0051E39E`、`0x004B9F36`、`0x00639B14`の同一証明は見つからなかった。**PC正本を確認できていないので全レーンに対する非重複は未保証**。

検証スクリプト`verify_rea_t014_player_gamewindow_ownerchain_20261023.py`は原作PE32から命令を直接読み、検索SQLiteは`mode=ro`で利用。検証内容は機械語**38命令位置**、直接CALLの相対オフセットとDB索引**8件**、データ参照と索引**8件**、保存済みGhidra疑似CテキストのSHA256**12関数**、Player vtableの実ポインタ、オブジェクトオフセット計算、ZIP CRC、SQLite整合性。

| 項目 | 今回 |
|---|---:|
| 機械語／CALL／参照／疑似Cハッシュ | **38/38、8/8、8/8、12/12 PASS** |
| 新Ghidra・REA・ゲーム実行 | **0 / 0 / 0** |
| 新規REA正式5種完成 | **0関数** |
| 新規REA VERIFIED | **0件** |
| 既存Wave1〜5の64/64 | **過去の別時点報告、今回再認定せず** |
| 正式QUEUE/PROGRESSに書込んだTODO/VERIFY/BLOCKED差分 | **0/0/0** |
| 原作実機Golden PASS／strict MATCH | **0 / 0** |
| 完全複製率 | **未測定** |
| 研究PC CPU/RAM・総調査時間 | **不明** |
| 独立検証器実行時間 | **証拠JSONを参照** |

今回の12関数は**Ghidra機械生成pseudoのハッシュ照合**であり、REAの`info/pseudo/assembly/callers/callees`の正式5点証拠完成ではない。

## 6. 黄金比較（未実施・観測設計）と次のP0

実機の安全な観測点は、(A)`0x00553B6E`直後の`[W+4]==0`、(B)`0x004B9F36`直後の`[W+4]==G`、(C)`0x0051E39E`直後の`[Player+0x188]==W`、(D)`0x00513A9A`後の`[0x67B328]==W`および`[0x67B32C]==Player`、(E)速度UI操作前の各ゲート、`0x00513CB8`到達時の`ECX==G+0x0C`。NULL/例外/破棄中は異常系として別観測し、正常returnを偽装しない。

次のP0：`GameManager+0x1EF148`へのポインタ別名による書込元探索、その後`GameManager` vtable`+0x20`の実行時ディスパッチCALL site、およびPlayer仮想メソッド`0x0051EF80`の具体的な呼出元のXREF/ABI検証。既拒否Wave6・`0x5710C0..0x571500`・REAエクスポートを別shell/経路で再試行しない。

## 7. 保存・復帰条件

- 接続障害ID：`REA-RC-20261023-0836-LOCAL-SSE429-01`。新規安全拒否0件。PC不通は**研究全体BLOCKEDを意味しない**。
- 作業用成果：この報告書、機械可読JSON、再検証用Python。ファイル保存と独立読み戻しは実際に試行して成功した段階だけ確定する。
- 研究PC正本：**未同期**。最新MASTER/規約/owner/QUEUE/PROGRESS/active.lock/既存run/既存ID/ソースSHAを復帰時に照合したうえ、重複・競合が無ければREA担当所有範囲だけ一度同期する。未解決時は`VERIFY`のまま保持する。
