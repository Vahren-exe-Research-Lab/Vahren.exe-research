# 迫真戦記 ver0.67｜REA独立研究：ScriptBattle→FUN_00564160の引数ABIと状態引渡し

- 記録ID：`REA-OFFLINE-20261023-1233-P0-SCRIPTBATTLE-564160-ABI-STATIC-01`
- 実施：2026-10-23 12時台 JST
- 区分：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。正式REAの`VERIFIED`ではない。
- 研究対象：`0x00492890`内の2つの直接CALL site `0x00492AA9`, `0x00492D4E` → `0x00564160`。今回の差分は**呼出規約、分岐別の5引数・callee正常復帰・早期グローバル副作用を原作機械語で独立照合したこと**。両CALL自体・NewGameModel逆参照登録は前回11時台までに既出につき新規件数に加算しない。
- 原作EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- SQLite SHA256：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
- オフラインZIP SHA256：`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`

## 1. 原本・環境・重複の先行確認

Desktop Commander Local Compactで現行MASTER・プロトコル・README/QUEUE/PROGRESS・検索DBの読み取りを試みたが、7読取とも `McpServerError: MCP SSE probe returned 429 from openai.org`。これは**接続/レート制限**であり、安全拒否とは異なる。PCの電源状態・online性・CPU/RAM負荷・owner・active.lockは不明。PC正本への書込みや同期はしていない。

正規のChatGPT Libraryに存在した `Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`decomp_task.zip`、`decomp_task_offline_rule_20261019.zip` を今回の解析環境へ読取コピー。原作EXE/SQLite/ZIPの上記SHA256一致、オフラインZIP `34/34` CRC、SQLite `PRAGMA integrity_check=ok`。DBは内部10268＋外部188関数、直接CALL47550、間接CALL候補5109、データ参照107934、文字列4298。Ghidra/REA/原作ゲームの新規実行は0回。

旧 `decomp_task.zip` の `QUEUE.json` はWave1～4が凍結済み16＋10＋10＋12＝48、Wave5が`IN_PROGRESS`。その時点の`function_queue`では16 VERIFIED / 48 TODO、`PROGRESS.md`は古い15/16表示。これらは更新タイミングの異なる記録であり、**過去チャットの「64/64 VERIFIED」をこの旧パックだけから確定しない**。今回の対象 `0x00564160`/`0x00492890`等は旧`function_queue`に存在しない。現行正本との重複照合は未実施であり正式追加・正式キュー変更を保留する。

## 2. 主な発見①：FUN_00564160はECX・EDX＋スタック3引数

Ghidra 12.1.4の既存疑似Cは `void __fastcall FUN_00564160(uint param_1, int param_2, undefined4 param_3, int param_4, int param_5)`。これは推測に基づく機械生成署名なので、原作ASMで独立確認した。

- `0x0056419B`：スタック第5引数（ESP相対、プロローグ後）を取得。
- `0x005641A2`：スタック第4引数を取得。
- `0x005641D7`：スタック第3引数を取得。
- `0x005641D1`：ECX（第1引数）をグローバルへ記録。
- `0x005641E9`：EDX（第2引数）をグローバルへ記録。
- **正常復帰 `0x00564C9A: RET 0x0C`**：呼出先がスタックの3引数12バイトを解放する。ESI/EDI/EBX/EBPはこの通常復帰経路でPOPされる。`0x00564C9D`以降は例外・異常経路側の可能性があり、通常RETと混同しない。

したがって、**呼出先の「5引数」は全てpushによる5個のスタック引数ではない**。ECX,EDX＋右から左へpushする3引数である。フック時にcdecl 5引数等へ読み替えるとレジスタ・スタックを誤る。

## 3. 主な発見②：`Engine+0x1EED18`非ゼロ経路、完全な引数源

`0x00492A73`の比較に続く`0x00492A79: JE 0x00492C75`を通らない側では：

```asm
0x00492A7F  MOV ECX,[ESI+0x1EEE14]
0x00492A85  CMP ECX,EBX
0x00492A87  JG  0x00492A8E
0x00492A89  MOV ECX,0x80000008
0x00492A8E  MOV EDX,[ESI+0x1EED48]
0x00492A94  MOV EAX,[ESI+0x1EED1C]
0x00492A9A  LEA EDI,[ESI+0x1EEDF4]
0x00492AA0  PUSH EDI
0x00492AA1  PUSH EDX
0x00492AA2  MOV EDX,[ESI+0x1EED44]
0x00492AA8  PUSH EAX
0x00492AA9  CALL 0x00564160
```

ここでは`EBX=0`が`0x00492A2A XOR EBX,EBX`から受け継がれる経路を前提にする。ESIは呼出側のEngineを指すという従来の静的追跡を前提とし、介在するCALLEE/非標準ABI経路での破壊がないことは要動的検証。

| `FUN_00564160`仮引数 | レジスタ/スタック | この分岐での値 |
|---|---|---|
| `param_1` | ECX | `Engine+0x1EEE14`の値（signed >0の場合）、それ以外 `0x80000008` |
| `param_2` | EDX | `[Engine+0x1EED44]` |
| `param_3` | スタック第1 | `[Engine+0x1EED1C]` |
| `param_4` | スタック第2 | `[Engine+0x1EED48]` |
| `param_5` | スタック第3 | `Engine+0x1EEDF4`の**アドレス** |

ここで`param_5`はフィールド内容のロードではなく`LEA`で作るポインタ。この違いは差し替え時の重要な境界。

## 4. 主な発見③：`Engine+0x1EED18`ゼロ経路、内部にさらに2分岐

`0x00492C75`：`CMP [ESI+0x1EED28],EBX`により次の選択がある。

**(A) `Engine+0x1EED28==0`：** `0x00492C7D`で`Engine+0x1EECFC`を取得し、`0x00492CA4`の`FUN_004647D0`（データ名`"event"`に対応する既存疑似C）を経由、戻り値の`+0x20`をEDIへ格納する。`0x00492CBF`以降で3スタック引数をpush、`0x00492CCE: JMP 0x00492D46`へ合流。

**(B) `Engine+0x1EED28!=0`：** `0x00492CDF`の`FUN_00597A20`の戻り値`+0x20`からEDI取得。EDI==0なら`0x00492D30: CALL 0x0046F4C0`により別途値を取得する経路がある。`0x00492D37`以降で共通の3引数pushへ。

両経路の合流点では、

```asm
0x00492D43  PUSH EBX  ; EBX=0
0x00492D44  PUSH EAX  ; [Engine+0x1EED48]
0x00492D45  PUSH ECX  ; [Engine+0x1EED1C]
0x00492D46  MOV EDX,[ESI+0x1EED44]
0x00492D4C  MOV ECX,EDI
0x00492D4E  CALL 0x00564160
```

(A)は`0x00492CCB`から直接同じ3引数をpushして`0x00492D46`へ合流する。`0x00492D43`の命令を(A)で**重ねて実行するわけではない**。

| `FUN_00564160`仮引数 | 0x00492D4E側の値 |
|---|---|
| `param_1` ECX | EDI：`event`/`FUN_00597A20`/必要時`FUN_0046F4C0`から解決した値 |
| `param_2` EDX | `[Engine+0x1EED44]` |
| `param_3` stack | `[Engine+0x1EED1C]` |
| `param_4` stack | `[Engine+0x1EED48]` |
| `param_5` stack | **0** |

**両CALL siteの違いは第1引数と第5引数。第2～4引数のフィールド源は一致する。** 入力値の意味・生存期間・ヌル許容性は未確定。

## 5. 主な発見④：callee開始直後のグローバル引渡し契約

`0x00564160`の開始直後に、以下の直接書込みが確認できる。

| CALL入力の対応 | グローバル | 実命令 |
|---|---|---|
| `param_1`生値 | `0x0067B938` | `0x005641D1` |
| `param_1`、ただし`0x80000008`なら0 | `0x0067B93C` | `0x005641DE` |
| `param_3` | `0x0067B944` | `0x005641E3` |
| `param_2` | `0x0067B948` | `0x005641E9` |
| `param_4` | `0x0067B94C` | `0x005641EF` |
| 下位状態から派生したフラグ | `0x0067B940` | `0x0056422F` |

`param_1`のセンチネル変換は`0x005641C5 / 0x005641CB / 0x005641CD / 0x005641CF`の演算とGhidra疑似Cの双方で検証。`0x80000008`の場合、`0x0067B938`には**元の0x80000008が保存される一方**、`0x0067B93C`には**0**が入る。ここを混同すると、置き換え前後の状態比較が誤る。

Ghidra疑似Cでは`param_4+0x14`と`param_2+0x14`を逆参照する。したがって少なくともこれらの引数を整数識別子と断定するのは危険であり、適切な参照先を持つポインタである可能性が高い。例外的入力への挙動・Goldenは未実測。

**注意：関連グローバルは他関数からも書き換えられるものがあり、「このCALLのみが唯一のwriter」とは断定しない**。DBのwrite_access付きxrefs一覧は検証結果JSONに保存した。

## 6. 境界の評価（フック・別実装向け）

この呼出境界は、戦闘開始時の特定の引数・グローバル状態を追跡する**重要な観測点**。しかし関数先頭でウィンドウ・リスト等を操作し、その後も大量の副作用があるため、**ここを置き換えるだけで戦闘モード差し替えが可能**とはまだ証明できない。`0x00492890`以前のEngine/Player/Enemy準備、NewGameModelの逆参照、`0x00564160`以後の消費先・終了復帰値の両方を検証する必要がある。

現時点の安全なGolden観測設計：`0x00492A73`の判定値、`0x00492AA9`・`0x00492D4E`のECX/EDX/ESP+4,+8,+C、`0x005641D1`～`0x005641EF`のグローバル更新直後、`0x00564C9A`正常復帰直前のESP/戻り先と、上記グローバルの最終値。これらは**未測定**であり実測PASS=0。

## 7. 検証・実行と正式状態

付属のread-only検証器：`verify_rea_20261023_1233_battle_handoff_abi.py`。原作EXE/SQLite/ZIPにSHA固定検証をかけ、PEセクション境界を解釈して指定64機械語サイトを独立照合。CALL 5件、相対分岐5件、グローバル書込み6件、対象calleeのSQLite直接caller全2箇所、擬似C5関数の個別SHAを照合。SQLite整合性PASS・ZIP CRC 34/34 PASS。

```bash
python verify_rea_20261023_1233_battle_handoff_abi.py \
 --exe /path/to/Vahren.exe \
 --sqlite /path/to/search.sqlite \
 --pack /path/to/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip \
 --out result.json
```

- 検証器の初回実行：`PASS`、約0.79秒（調査全体の時間ではない）。
- 追加Ghidra/REA 0回、原作実機Golden PASS **0**、strict MATCH **0**、完全複製率未測定。
- 今回の正式REA `info / pseudo / assembly / callers / callees`新規完全セット **0関数**。SQLite擬似CのSHA一致は正式VERIFIEDに昇格しない。**新規REA VERIFIED 0**。
- 現行TODO/VERIFY/BLOCKEDへの**正式書込差分 0/0/0**。未解決研究上の対象はP0/VERIFYに維持。最新キューの実際のカウントはPC接続できず不明。
- CPU/RAM実機負荷：不明。実機PCの接続状態：不明（Local 429）。安全拒否発生なし。

## 8. 同期・次回再開

本レポート・JSON・検証器は独立出力。原本EXE、SQLite、旧ZIP、原本ZIP/SAVE、MASTER、他レーン、Git、T018、既存スケジュールに変更なし。PC正本への書込み・正式同期は**未実施**。Libraryへの保存が行われた場合もPC正本への同期とは別扱い。

接続障害記録：`REA-RC-20261023-1233-LOCAL-SSE429-01`（現行MASTER/QUEUE/PROGRESS/active.lock/CPU不明、静的解析のみ継続、正本同期は復旧後に差分・所有者・競合・SHA・既存IDを照合して一度だけ）。

次回P0の優先順：① `0x00564160`から書かれる`0x0067B938`～`0x0067B94C`の**消費先と後続上書き**、② 分岐ゼロ側EDI（`event`/`FUN_00597A20`/フォールバック）の実体と`param_1`センチネル条件、③ NewGameModel+0x38のreaderと解放時の無効化、④ `GameManager+0x1EF148`の間接writer。未確認の動的挙動は推測でPASSとしない。
