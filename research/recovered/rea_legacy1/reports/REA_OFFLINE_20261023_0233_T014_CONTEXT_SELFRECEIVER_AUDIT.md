# 迫真戦記ver0.67 REA独立静的監査 — GameManager初期化と仮想CALLの具体的候補

- 記録ID: `REA-OFFLINE-20261023-0233-T014-CONTEXT-SELFRECEIVER-WRITER-STATIC-01`
- 日時: 2026-10-23 02:33 JST 定期実行枠（実際の所要時間は全体未計測）
- 管理状態: **OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**
- 対象: `0x543428`（親関数`0x5433D0`）、初期化・vtable参照チェーン（`0x4B78C0`, `0x48A5B0`, `0x553A90`, `0x553B20`, `0x4B9D70`）
- 目的: 既存成果で未解決だった`context+0x10`の格納元とvtableスロット実体を、**現在保存済みのEXEとSQLiteを使って独立照合**する。

## 前提・接続・既存成果

Desktop Commander Local Compactの`MASTER_LEDGER.md`読取は`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`で失敗。**CONNECTION/RATE_LIMIT、SAFETY_REFUSALではない**。PC稼働、CPU/RAM、active.lock、最新MASTER/QUEUE/PROGRESS/runsは未確認。別ツール経由でこの拒否を回避したわけではなく、ユーザー承認済みの**別媒体に事前保存済みの解析スナップショット**を独立静的研究に用いた。REA/Ghidraの新規実行はゼロ。

取得先: ChatGPT Libraryの既存非公開ファイル`/Vahren.exe`、`/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`/MASTER_LEDGER.md`、`/ANALYSIS_LANES_PROTOCOL.md`、`/decomp_task.zip`。LibraryコピーのMASTER最終更新は2026-10-09、旧REAのPROGRESSは15/16の旧スナップショット。以前のWave1–5 64/64の値も過去報告値のため**合算・再認定しない**。REA所有外のAレーンT014資料を編集しない。読み取れる過去のREAオフライン記録`...20261023-0141-T014-SPOTFIRE-TAILJMP...`との差分を採用し、既知の11間接CALL+1 tail JMPは二重計上しない。

ソース追跡:

- `Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、2,910,720 bytes。
- アーカイブ SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP 34/34 CRC PASS。
- `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、BUILD_MANIFESTと一致、SQLite `integrity_check=ok`。
- 検査は元EXEのPE32セクションのファイル位置から実命令を抽出し、対象8関数に限定した既存SQLite擬似Cハッシュ・xrefsと突合した。全関数の再逆コンパイルは行っていない。

## 増分発見A: 未解決の`context+0x10`初期値の直接書込が見つかった

1. `0x004B7971` (`0x004B78C0`内) の実機械語は `C7 05 00 E3 8B 00 F0 E2 8B 00`、すなわち **`mov DWORD PTR [0x008BE300],0x008BE2F0`**。データ参照索引の`0x008BE300`に対する直接WRITEもこの1箇所のみ（*間接書込がない証明ではない*）。
2. 同じ初期化経路で`0x004B79D1: mov EDI,0x008BE7F4`、`0x004B79D6: call 0x0048A5B0`。呼出先`0x0048A5F4: mov DWORD PTR [EDI+4],0x008BE2F0`により、**engine+4**はこの経路では`context=0x008BE2F0`。
3. 別の既存経路`0x00433E80`では`0x00434175: mov EBX,[EBX+4]`→`PUSH EBX`→`0x0043419D: call 0x00543A30`。`0x00543A63`はFadeSheetの`[ESI+4]`へ受け取ったcontextを保存する。`0x005433F3`でこの値を再取得する。
4. FadeSheet登録`0x005433D0`の`0x00543420: mov ECX,[ESI+0x10]`が受信者を読む。前記初期化経路の`ESI=context=0x008BE2F0`なら、**受信者ポインタを格納する実アドレスが`0x008BE300`で、その初期内容は`0x008BE2F0`（GameManager自身を指す自己参照）**である。map基点は`0x008BE308`、登録前mapカウンタは`0x008BE310`。

**範囲制約:** 上記は保存済み原作PE32に存在する初期化経路とフィールド対応の静的証拠。別の起動経路・後続書込・オブジェクト破棄・並行処理での値の維持は実機未検証。`0x00543A30`はFadeSheetを構築するが、構築した全インスタンスが必ず`0x005433D0`を通ることを証明するものではない。

## 増分発見B: vptr設定と`vtable+0x1C`の具体的関数VAが解決候補に

`0x00553B20`（`GameMngBase`コンストラクタ相当）では`0x00553B4F`で`[0x008BE2F0]=0x00638E1C`と書く。その後`0x00553A90`（`GameManager`上位コンストラクタ相当）では`0x00553ACB`で**`[0x008BE2F0]=0x00638DF0`**と再設定する。SQLite疑似Cは最終値を`GameManager::vftable`と命名しているが、判断は実機械語および読み取った`.rdata`に基づく。

`.rdata`のPE実データを独立読取した結果:

| 項目 | 静的アドレス/値 | 根拠 |
|---|---|---|
| 最終GameManager vptr | `0x00638DF0` | `0x00553ACB`のDWORD書込 |
| 仮想スロット`+0x1C` | `0x00638E0C` | `0x638DF0 + 0x1C` |
| **スロットの実データ** | **`0x004B9D70`** | `.rdata[0x638E0C]`のDWORD |
| 基底クラス構築途中vptr | `0x00638E1C` | `0x00553B4F` |
| 基底クラス同スロット | `0x004BBBD0` | `.rdata[0x638E38]`のDWORD |

`0x00543423`は`mov EDX,[ECX]`、`0x00543425`は`mov EAX,[EDX+0x1C]`、`0x00543428`は`call EAX`。したがって**GameManagerの最終vptrと自己参照が保持される実行条件では、`0x543428`の間接CALLターゲットは`0x004B9D70`**。これは旧報告で未確定だった実装先の**具体的な静的解決候補**であり、動的Golden確定ではない。

特に`GameMngBase`構築途中に同じ間接CALLが行われる場合（その到達性は未確認）は、別スロット`0x004BBBD0`に解決され得る。ポインタ・vptrの変更や条件ガードにも依存するため、単一実装先をあらゆる状態で確定したとは言わない。

## 増分発見C: 候補`0x004B9D70`の動作（部分）

`0x004B9D70`はECXをオブジェクトポインタとして使う。`0x004B9D78`で`[ECX+0x1EF148]`の1バイトを判定し、ゼロなら`RET`側へ進む。非ゼロなら`[ECX+0x80]=0x19`、`[ECX+0x84]=0x28`とし、`P=[ECX+0x98]`の指す領域のバイトオフセット`0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2D,0x34`をゼロ化する。その後`RET`。Ghidraの名前なし関数と機械語が一致する。各フィールドの意味（入力状態・描画制御等）は**未確定**。

これは単純な「必ず再描画する関数」という過去の仮説を裏付けない。影響範囲として、この受信者/スロットへのフックを再実装するときは`0x1EF148`条件とECX ABIの保持を検討する。

## 読取専用の独立検証と進捗

- ZIP CRC: **34/34 PASS**。EXE/SQLite SHA: **一致**、SQLite integrity: **PASS**。
- PE32機械語指定箇所: **25/25 PASS**。
- 直接CALLサイトとSQLite対応: **2/2 PASS** (`0x004B79D6`, `0x0043419D`)。
- SQLite対象関数疑似Cと保存ハッシュ: **8/8 PASS**（関数ごと、正式REA検証への昇格ではない）。
- 仮想スロット実バイト: **GameManager / GameMngBase 両方PASS**。
- `0x00543428`の間接CALL索引: **1/1 PASS**。
- Python検証器実行時間: **約0.55秒**。全調査時間: **未計測**。研究PC CPU/RAM負荷: **不明**。
- 今回の**新規REA正式VERIFIED: 0件**。正式5種類証拠新規完成: **0件**。正式TODO/VERIFY/BLOCKED差分: **0/0/0**（PC最新台帳は未取得）。原作実機Golden PASS: **0件**。strict MATCH: **0件**。完全複製率: **未測定**。
- 5種証拠(`info/pseudo/assembly/callers/callees`)は既存Ghidra関数行・擬似Cと今回の局所ASM、選別済みdirect/indirect参照があるが、REA正式の各関数5点セット・最新RUN_RESULTの完備を今回検査できず**未完成/VERIFY**。新規REA実行・Ghidra実行ともに0回。

## 未解決・復旧

- P0/VERIFY: `0x543428`が正常ゲーム進行の全経路で確かに`0x4B9D70`へ解決するか。直接/別名参照/後続代入の影響を調べる。初期状態は`GameManager`、構築途中では`GameMngBase` vptrが異なる。
- P0/VERIFY: `0x4B9D70`の状態ビット`ECX+0x1EF148`のセット・クリア元と、`[ECX+0x98]`が指すデータ構造の所有権/有効期間を追跡。`0x4BBBD0`との差も比較する。
- VERIFY: `0x5AA7F5`（spot_fireのtail JMP）が同じ`context+0x10`の構造を使う場合の動的受信者は未確定。既知12経路は集計変更なし。
- CONNECTION: REA研究PC Local初回読取429。PC最新正本への同期と最新RUN/lock/ownerは未検査。安全拒否新規なし。

**復旧ID**: `REA-RC-20261023-0233-LOCAL-429-01`。PC復旧後は最新MASTER、解析所有権、QUEUE/PROGRESS、RUN_RESULT、5種証拠、他owner競合と過去研究IDを突合後、安全なREA所有領域に単発同期する。原本EXE/ZIP/SAVE、MASTER、A～E、T018、dev_lab、Git/公開/スケジュールは変更しない。Work未使用。

**保存方針**: 独立オフライン記録とread-only再検証器をChatGPT Libraryの`迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED`へ保存し、個別の独立読み戻しSHA一致を確認してから保存済と記載。PC正本同期は別問題であり未実施。
