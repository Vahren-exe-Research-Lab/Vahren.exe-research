# 迫真戦記 ver0.67｜REA T014独立静的研究：速度UIのOwner/Gate別名書込

- 研究ID：`REA-OFFLINE-20261023-0736-T014-UIOWNER-GATE-ALIAS-STATIC-01`
- 日付：2026-10-23 JST・7時台
- ステータス：**OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**
- 対象：`0x0051EF80 → 0x00513A80 → 0x00453800`、結果の消費者 `0x00513C60 / 0x00526A40 / 0x004B9DC0`。
- 所有範囲：REAの独立証拠。MASTER、既存QUEUE/PROGRESS、A～E、T018、原本、Git、スケジュールは変更しない。Work/REA/Ghidra/ゲーム実行なし。

## 1. 先行資料・環境の再確認

最初にDesktop Commander Local CompactでWindows研究PCのMASTER/規約/REA README・QUEUE・PROGRESSを`read_multiple_files`で読み取ろうとしたが、**`UNAVAILABLE: MCP SSE probe returned 429 from openai.org`** で失敗した。安全拒否ではない。研究PCの実稼働、CPU/RAM、active.lock、最新MASTER/QUEUE/PROGRESS/runsは不明。異なるshell/Remoteを用いた再試行はしていない。

ChatGPT Libraryで実在を確認した`/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`/Vahren.exe`、`/decomp_task.zip`、規約ファイルを使用した。ZIPとEXEはオフラインの作業領域へコピーして読み取り専用で解析し、**ユーザー原本は変更していない**。オフラインZIP内の検索README/BUILD_MANIFEST/旧MASTER/旧PROGRESS、REA ZIPのREADME/QUEUE/PROGRESS、前回06:47研究を照合。

| 対象 | SHA256・状態 |
|---|---|
| 原作 `Vahren.exe` | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| 2026-10-21オフラインパック | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` / 34/34 CRC PASS |
| 既存SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` / `integrity_check=ok` |
| 既存REAアーカイブ | ZIP CRC PASS・旧QUEUEを閲覧。PC正本への適用可否・最新性は未確認 |

既存06:47成果では`[0x0067B328]`と`0x0067B313`の使用は確認済み。**今回はそれらへの具体的な代入起点と所有関係を特定した点だけが新規差分**であり、速度計算・仮想関数アドレスは再計上しない。オフライン旧MASTERおよび既存T014独立監査に今回の命令サイト`0x453851 / 0x513A95 / 0x51F035`の一致記録は見つからなかった。PCの最新正本との重複照合は未了。

## 2. 新規発見A：`0x67B328`の正体は静的Windowオブジェクトの `+0x98`

前回の速度変更関数は`0x513C6A MOV EDX,[0x0067B328]`により得たポインタの`+4`を参照していたが、**`0x67B328`自身の書込元は未解決**だった。

今回、原作EXEの機械語で以下の2段の直接CALLを検証した。

```asm
0x51EF8D  MOV EDI,ECX                ; owner
0x51F02E  MOV ECX,[EDI+0x188]        ; inner = owner+0x188 の指すオブジェクト
0x51F034  PUSH EDI                   ; 引数 owner
0x51F035  CALL 0x513A80

0x513A8E  MOV EAX,[ESP+0x18]        ; 引数 owner を復元
0x513A92  PUSH ESI                   ; 旧ESIを保存
0x513A93  PUSH EAX                   ; owner
0x513A94  PUSH ECX                   ; inner
0x513A95  MOV ESI,0x0067B290        ; 静的Windowオブジェクト
0x513A9A  CALL 0x453800
```

`0x453800`内での引数取得は、この関数がEBX/EDIをpushした後に行われる。このため`[ESP+0x0C]`は直前の`PUSH ECX`、`[ESP+0x10]`は直前の`PUSH EAX`に対応する。

```asm
0x453800  MOV BYTE PTR [ESI+0x83],1
...
0x453841  MOV EAX,[ESP+0x0C]       ; inner
0x45384A  MOV ECX,[ESP+0x10]       ; owner
0x453851  MOV [ESI+0x98],EAX
0x45385E  MOV [ESI+0x9C],ECX
...
0x4538FF  RET 0x08
```

`ESI=0x0067B290`を代入すると、初期化時の**到達可能な実行経路**で次が成立する。

| アドレス | 静的別名 | 代入される値 |
|---|---|---|
| **`0x0067B313`** | `Window+0x83` | `1`（有効フラグ） |
| **`0x0067B328`** | `Window+0x98` | **`[owner+0x188]`（innerポインタ）** |
| **`0x0067B32C`** | `Window+0x9C` | **`owner`ポインタ** |

これは **Ghidra擬似Cだけからの推測ではなく、原作x86機械語のレジスタ・スタックデータフローと固定アドレスの演算**で導いた構造。該当helperは、2個のスタック引数を`RET 8`で回収する。

## 3. 新規発見B：`0x67B313`の書込元も同じ初期化処理

前回は速度変更を許可する`DAT_0067B313`の読み出しを確認していた。今回、`0x0067B290+0x83=0x0067B313`と一致することを確認した。つまり上記`0x453800`先頭の`MOV BYTE PTR [ESI+0x83],1`が、**このグローバル許可フラグを1へ初期化する具体的な正の書込証拠**となる。

読み出し側の原作命令は、`0x513C61 CMP BYTE [0x67B313],0`、`0x526AFB CMP BYTE [0x67B313],0`、`0x4B9DD8 CMP BYTE [0x67B313],DL`。いずれも2026-10-21検索DBの`data_refs`にREADとして登録されている。

`0x67B313`は原作PEの初期化済み`.data`像では0であり、対象helperを経由した後に1となる。したがって静的には、**初期化前のゼロ→Window初期化による有効化**という経路を立証できた。しかし他の書込み、破棄、後続リセットが存在しないことは未確認であり、実機到達順はまだ未実測である。

## 4. `inner+4`とGameManagerの関係：解明範囲と未確定事項

既知の速度変更処理は、`0x513C6A MOV EDX,[0x67B328]`→`0x513C70 MOV EAX,[EDX+4]`を経て、`GameManager候補+0x1EF148`、`+0x20`、`+0x1EF150`の条件を検査し、`0x513CB2 MOV ECX,[EDX+4]`に続いてECXへ0x0Cを加算して既知の`0x4C21F0`を呼ぶ。

今回、上記`EDX`がこの初期化経路では`[owner+0x188]`に由来することを確定できた。ゆえに対象候補は**`receiver = [[owner+0x188]+4]`**と具体化できる。`0x526B15/0x526B1B`にも同型の読み出しが存在する。

一方、以前別のコンストラクタで確認済みの`0x008BE7F4+4 = 0x008BE2F0`（GameManagerグローバル）という経路が、このownerの`[owner+0x188]`へ必ず代入されるかは**まだ繋がっていない**。今回の静的証拠だけで`receiver == 0x008BE2F0`とは断定しない。受信者を固定アドレスに決め打ちしてフックすることも禁止。

## 5. なぜ従来のdata_refsから書込元を見つけられなかったのか

読み出し命令は絶対アドレス`[0x0067B328]`を直接参照するため、Ghidraの`data_refs`には直接READとして現れる。しかし書込命令は`MOV [ESI+0x98],EAX`で、**ESI=0x0067B290を別関数の呼出元が用意する**。この間接化により、単純な`target_va = 0x67B328`のデータ参照索引だけでは書込サイトを発見できない。

この件は今後の`GameManager+0x1EF148`のwriter探索にも教訓を与える。ただし前者がこの手法で発見できた事実は後者の書込存在や場所を証明しない。

## 6. 独立検証、5種証拠、残課題

独立検証器`verify_rea_t014_ui_owner_gate_alias_20261023.py`は、**24個の機械語位置、直接CALL 2件の相対飛越先とSQLite索引、READ site 5件、6関数の既存Ghidra擬似C SHA256、アドレス別名3件**を原作EXE/SQLiteで照合してPASS。SQLite integrity_check、ZIP 34/34 CRC、原作/DB/ZIP SHA256もPASS。

- 正式REA `info/pseudo/assembly/callers/callees` 5点セットの今回新規完成：**0関数**。対象関数について既存デコンパイル本文だけでVERIFIED昇格させない。
- 正式REA VERIFIED増分：**0**。過去Wave1～5の64/64は別時点の報告値であり、今回加算・再認定しない。取得できた古いQUEUE自体は状態が旧版のため、最新正本を優先する。
- 正式QUEUE/PROGRESSへのTODO/VERIFY/BLOCKED書込差分：**0/0/0**。PC正本の現状数は未知。
- 原作実機Golden PASS=**0**、strict MATCH=**0**、完全複製率=**未測定**。
- 原作ゲーム/REA/Ghidra実行：**0回**。全調査時間：未計測。検証器時間：証拠JSON `verifier_seconds`に記載。PC CPU・RAM使用量：不明。

次のP0として、`[owner+0x188]`がどの条件で`0x008BE7F4`を指すかを`0x48A5B0`の登録元/`0x51EF80`の受信者作成経路から調べ、次いで`+0x1EF148`の別名writerを探索する。別件の`vtable+0x20`実行時CALL siteもVERIFYとして継続。全関数再抽出や既拒否Wave6/VAの操作はしない。

### Golden観測条件（設計のみ・未実行）

Window初期化直前/直後に`[0x67B313]`、`[0x67B328]`、`[0x67B32C]`、`[owner+0x188]`、`[[owner+0x188]+4]`を読取り比較する。さらに候補受信者と`0x008BE2F0`の一致有無を実測し、`+0x1EF148`/`+0x1EF150`/`+0x20`、入力h=25/100の速度更新を採録する。NULLや破棄中オブジェクトは別ケースにし、正常復帰を推測で偽装しない。

## 7. 書込・復帰記録

- 接続障害ID：`REA-RC-20261023-0736-LOCAL-SSE429-01`。
- 未取得：現在のPC正本MASTER/QUEUE/PROGRESS/runs、所有権・active.lock・CPU/RAM・競合状況。安全拒否は新たに発生していない。
- 成果の本体：このMD、機械可読JSON、独立検証用Pythonを新規独立IDで保存。PC正本は**未同期**。
- 復帰点：PCがつながったときに最新のOwner・QUEUE/PROGRESS/MASTER・既存研究ID/ソースSHAを確認し、重複や競合が無いことを確認できた場合のみREA所有範囲へ差分を一度同期する。他レーンやMASTERは変更しない。
- Libraryの保存/独立読み戻し：実際のアップロードと再取得が成功した場合にのみ成功と宣言する。
