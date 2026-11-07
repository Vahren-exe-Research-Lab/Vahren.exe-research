# 迫真戦記 ver0.67｜REA独立 P0：戦闘候補・除外集合のイベント待避経路を特定

**研究ID**：`REA-OFFLINE-20261024-1530-P0-DIPLO-HELP-DEFERRED-HANDOFF-STATIC-01`  
**観測日**：2026-10-24・15時台 JST  
**状態**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。原作実機Golden、REA正式VERIFIED、PC正本同期を主張しない。  
**所有権**：REA独立解析のみ。原本・SAVE・ZIP・A〜E・MASTER・T018・QUEUE・PROGRESS・既存run・Git・スケジュール非変更。

## 0. 先読み・前回との非重複・ソース

Desktop Commander Local CompactでWindows正本のMASTER、レーン規約、REA README・QUEUE・PROGRESSを先読みする操作を試みたが、`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`で失敗。**CONNECTION/RATE_LIMIT**であり、安全拒否ではない。研究PCの通電状態、現行owner/lock・最新run・CPU/RAMは不明。Remote/Work/別接続経路による迂回は実施していない。

ChatGPT Libraryで実在確認した既存`/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`と`/Vahren(2).exe`を今回の解析コンテナに正規取得し、原ファイルに書き込まず確認。ZIP内のMASTER/レーン規約/旧PROGRESS/索引README・manifestを先読。過去の2026-10-24 13:34、14:35の研究報告・JSON・監査スクリプトを照合済み。**前回14:35は0x48D6A0→0x4F6540の候補・除外引数、および0x4F6540の除外集合「照会」とローカル集合「挿入」の識別。** 今回は別の制御経路 `0x488290→0x490180→0x52E9E0` と、同名イベントを検出する`0x521D90`を調べた。以前のCALL数を新規として再加算しない。

| ソース | 実測SHA256 |
|---|---|
| ユーザー承認済み原作EXEと同内容のコピー | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP収録の**旧**`search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP CRC・manifest・SQLite `PRAGMA integrity_check=ok`、内部**10,268**関数を照合。**現行**PC正本は2026-10-21引継ぎ資料上、内部**10,274**関数の`HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`。現物未入手・SHA未再測定につき、今回の旧DB解析は**現行正本とのVERIFYが必要**。旧ZIPのPROGRESSは10月9日時点 **15/16**、後日のWave1〜5 **64/64**は過去報告で今回再照合なし。両方を合算しない。

## 1. 増分A：0x00488290は一定条件で「後続を切り替える戻り値1」を生成する

原作PE32の直列命令を確認：

```asm
0x488BFB CMP EAX,[ECX+8]         ; しきい値比較
0x488BFE JG  0x488C4D            ; 超過時はこのフラグ設定をスキップ
0x488C00 MOV EAX,[ESP+0x1A8]     ; param_5の候補ポインタ
0x488C07 CMP BYTE PTR [EAX+0x1D],BL
0x488C0A JE  0x488C13
0x488C0C MOV BYTE PTR [ESP+0x5B],1
...
0x48952D MOV AL,[ESP+0x5B]       ; 戻り値バイト
0x48954A RET 0x18
```

旧疑似Cでは`local_139 = 0`で初期化され、`if ((int)pcVar8 <= local_108[2])`内の`if (*(char *)(param_5+0x1d)!='\0') local_139=1`に対応、`return local_139`で復帰する。従って**条件付きで0/1を返す実分岐**。これを「除外集合に直接書き込むフラグ」と解釈してはいけない。なお各レジスタの全例外経路は未追跡。

呼出元`0x00490180`は、`0x4901DB TEST EAX,EAX`などで事前条件を検査してから`0x49021A CALL 0x00488290`を呼び、`0x49021F MOV [ESP+0x17],AL`でこの結果を保持する。入口ガードには`0x00597A50()>0`、`[context+0x1EED4C]+0x10 != 0`、候補選択結果 !=NULL、`[候補+0x94]==0`が含まれる。**ガード成立後に0x00488290を呼ぶ可能経路**であり、無条件呼出と主張しない。

## 2. 増分B：戻り値1側は候補・除外ツリーを状態オブジェクトへ「待避」する

`0x490542 CMP BYTE PTR [ESP+0x17],BL`→`0x490546 JE 0x490569`で、結果0側は`0x49056A CALL 0x00490590`、非0側は次のように分岐する：

```asm
0x49054E LEA EDX,[ESI+0x1EED30]   ; 除外集合のアドレス
0x490554 LEA EAX,[ESI+0x1EED20]   ; 候補集合のアドレス
0x49055A MOV ESI,[ESI+0x1E8630]   ; 別の状態オブジェクト
0x490560 PUSH EDX                   ; 第2スタック引数（除外）
0x490561 PUSH EAX                   ; 第1スタック引数（候補）
0x490562 CALL 0x0052E9E0
```

`0x0052E9E0`自身も機械語から調査：

```asm
0x52EA09 MOV DWORD PTR [ESI+0x4A8],4  ; 状態種別
0x52EA18 MOV ECX,[ESP+0x24]           ; 第2引数＝除外
0x52EA1C MOV EAX,[ESP+0x20]           ; 第1引数＝候補
0x52EA23 MOV [ESI+0x4B0],ECX           ; 除外集合へのポインタ値
0x52EA31 MOV [ESI+0x4AC],EAX           ; 候補集合へのポインタ値
...
0x52EB0F RET 8
```

**新しく確認した性質は、2集合の内容を複製しているのではなく、2集合のアドレスを別オブジェクトのフィールドへ格納すること。** これは参照の待避であり、ただちに各集合への挿入・削除とはならない。戻り値0側では上記の状態待避を経ず、直接`0x00490590`へ進む。`0x0052E9E0`内の直接CALLには`0x00476720`/`0x004F9000`の木挿入ヘルパーは含まれない（**当該関数の限定的否定証拠**）。間接更新や下流の更新元を否定していない。

## 3. 増分C：`diplo_help_test`という同名イベントの登録・照会・再開候補を接続

`0x0052E9E0`は、原作PEの文字列VA **`0x0062B048`**（NUL終端`diplo_help_test`）を`0x52EAE4 PUSH 0x62B048`で登録処理へ渡し、`0x52EAFA CALL 0x0052CCF0`で後続処理を呼ぶ。別の`0x00521D90`には**別アドレス`0x0062B584`だが同内容**の`diplo_help_test`文字列を判定する経路がある：

```asm
0x522830 PUSH 0x62B584        ; 'diplo_help_test'
0x52283A CALL 0x0043F330     ; この文字列の判定に続く処理
0x52283F CMP AL,BL
0x522841 JE  0x522867        ; 不一致相当は次の分岐
0x522843 CMP DWORD PTR [0x87F6F0],1
0x52284A JE  0x5222DD
0x522850 MOV EAX,[EBP+0x194]
0x522857 MOV [EBP+0x4A8],EBX  ; 旧疑似Cは0へ戻す
0x52285D CALL 0x00490590
```

これにより**待避／名前付きイベント要求／名前付きイベント検査／条件付きの通常経路呼出し**という静的接続候補を得た。`0x00521D90`側の条件は文字列判定成立と`DAT_0087F6F0 != 1`。Ghidra疑似Cでも`*(param_1+0x4a8)=0; FUN_00490590();`を確認した。両文字列VAの実バイトは独立一致。ただし、**`0x0052E9E0`のESI受信オブジェクトと`0x00521D90`のEBPオブジェクトが同じ実体か、イベントが実際に配達されるか、集合ポインタの有効寿命までは未証明**。この経路をGolden PASSや確定した戦闘遷移仕様には昇格しない。

## 4. 実装への影響と次の研究

候補・除外集合をバイナリ境界で受渡しするだけでなく、**呼出時の所有状態と生存期間**も調査する必要がある。今回見つけた`context+0x1E8630`の受信オブジェクト、`state+0x4AC/0x4B0`の利用先、`0x0052CCF0`のイベント起動処理、`0x00521D90`の「同一インスタンスか」、`0x00490590`の候補選択`0x0048F720`の非NULL条件が優先VERIFY。コピーではないなら、待避中に木構造を破棄する実装は危険になり得るが、これは**安全性設計上の仮説**であり実発生は未実測。除外集合`context+0x1EED30`の本当の追加・削除writerも依然未特定。

## 5. 独立監査・REA5種証拠・Golden

監査：`REA_OFFLINE_20261024_1530_P0_DIPLO_HELP_HANDOFF_AUDIT.py`（Python標準ライブラリのみ、実ゲーム/REA/Ghidra不実行）。PEセクションからVAを写像して原作バイト、E8 rel32、条件分岐先を検査。保存済み旧SQLiteのdirect `calls`、擬似C SHA、意味マーカーを二次資料として照合。ソースハッシュ・ZIP CRC・manifest・SQLite integrityを先行検証。**77/77件の選定監査をPASS**（機械語34、CALL＋DB 9、short branch 4、疑似C SHA4、意味マーカー15、文字列2、そのほかソース検証9）。**77は関数完成数ではない**。

| 指標 | 今回 |
|---|---|
| 既存Wave1～5正式VERIFIED | 過去報告64/64。**PC正本を再読できず再認定なし**。旧ZIP 15/16と合算しない |
| 新規正式VERIFIED | **0** |
| 新規REA正式5種類`info/pseudo/assembly/callers/callees`完全充足 | **0関数**（旧DB機械出力＋指定ASMのみ） |
| 正式TODO/VERIFY/BLOCKED書込差分 | **0/0/0**（未編集、現行値は不明） |
| 新規独立VERIFY | **1研究ID**（正式キューへ未反映） |
| 原作Golden PASS / strict MATCH | **0 / 0**（未実測） |
| 完全複製率 | **未測定** |
| REA/Ghidra/ゲーム実行 | **0/0/0** |
| CPU負荷・空きRAM・PC active.lock | **不明** |
| スクリプト単体所要時間 | JSON内`audit_elapsed_seconds`（約1.3秒）。調査全体は未計測 |

**復旧ID**：`REA-RC-20261024-1530-LOCAL-SSE429-01`。時刻15時台、試行Local Compact `read_multiple_files`（MASTER・規約・README・QUEUE・PROGRESS）、実際の理由`UNAVAILABLE / MCP SSE probe 429`、分類CONNECTION/RATE_LIMIT。未保存発見はWindows正本への今回の差分、現行10,274 DBとの照合、所有者・ロック・正式進捗の確認。許可された次手はPC復帰時にread-only正本照合後、重複・ID・ownerを確認してREA独立成果だけ一度同期。拒否済みVA、Wave6、REAエクスポートへの再実行や迂回なし。自動化状態は変更しない。
