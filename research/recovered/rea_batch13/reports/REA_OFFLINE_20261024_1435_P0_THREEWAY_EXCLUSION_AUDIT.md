# 迫真戦記 ver0.67｜REA P0：戦闘初期化三分岐・除外集合引数ABIの独立監査

- 研究ID：`REA-OFFLINE-20261024-1435-P0-THREEWAY-BATTLE-EXCLUSION-ABI-STATIC-01`
- 日付：2026-10-24 14時台 JST
- 状態：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 所有：REA独立静的証拠。Windows正本のQUEUE/PROGRESS/MASTER・他レーン・原本・Git・予定には非書込。
- 前回13時台との**非重複差分**：前回は`0x4868D0/0x488290/0x489630`の候補集合挿入を確認。今回は**別の関数**`0x48D6A0`がゲーム開始処理で`0x4F6430/0x4F6540/0x4F84B0`を選択する条件、`0x4F6540`へ渡す6実引数、`0x4F6540`内部での除外集合**照会**とスタックローカル集合**挿入**を原作PEで区別した。登録済みCALLを新規数に足さない。

## 0．接続・ソースの先読み

Desktop Commander Local CompactからWindows正本の`MASTER_LEDGER.md`先読みを1回試みたが、`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`。これは429による接続/レート制限であり安全拒否ではない。Windows正本の最新MASTER、レーン所有権、REA README/QUEUE/PROGRESS/既存runs、`active.lock`、現行検索DBの実在・ハッシュ・競合・PC電源・CPU/RAMはこのrunでは確認できなかった。

代替としてChatGPT Libraryの**実在確認済み**`/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`と`/Vahren(2).exe`を容器内へ取得し、読み取り専用で使用。ZIP内の`research_snapshot/MASTER_LEDGER.md`、`research_snapshot/evidence/ANALYSIS_LANES_PROTOCOL.md`、`research_snapshot/rea_lab/decomp_task/PROGRESS.md`、旧検索README/manifest/SQLiteを検査。スナップショットのREA PROGRESSは**10月9日時点15/16**であり、10月24日までに報告されたWave1～5の64/64の値の代用品とはしない。どちらの数字も今回正式に更新していない。

| ソース | SHA256 |
|---|---|
| 承認済み原作EXE内容をもつ`Vahren(2).exe` | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内**旧**`search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP旧DBは**内部10,268関数**。他の報告にある**10,274関数の現行DB**本体はこのrunでは取得・照合できなかった。古い結果を現行正本と混同しない。

## 1．P0新証拠：`0x0048D6A0`の3つの呼び分け

**重要：次の3分岐は当該命令位置における静的制御フロー。実ゲームでどの分岐を踏むかのGoldenは未実測。**

| 条件（EBX＝状態コンテキスト） | CALL site | callee | PE32の根拠 |
|---|---|---|---|
| `[EBX+0x1EED28]==0` | `0x0048E49A` | `0x004F6430` | `0x48E481 CMP ...0`、`0x48E488 JNE`で非ゼロ経路と分離 |
| `[EBX+0x1EED28]!=0`かつ`[EBX+0x1EECD4]!=0` | `0x0048E4CC` | `0x004F6540` | `0x48E4A1 CMP ...0`、`0x48E4AE JE 0x48E4D3`を通らない経路 |
| `[EBX+0x1EED28]!=0`かつ`[EBX+0x1EECD4]==0` | `0x0048E4EA` | `0x004F84B0` | `0x48E4AE JE 0x48E4D3` |

`0x48E4CC`を唯一の「除外集合を明示的に渡す」呼出しとして今回確認。このCALLの**旧DBの直接callerは1件**で、E8バイト・rel32・SQLite呼出記録で一致。これだけから間接caller全てを否定しない。

## 2．`0x004F6540`の実引数と正常復帰の部分ABI

`0x48E4B6`で`LEA EDX,[EBX+0x1EED30]`、`0x48E4BC PUSH EDX`。その後`0x48E4A8`で求めた候補コンテナアドレスを`0x48E4C3 PUSH EAX`、`[EBX+0x1EED1C]`を`0x48E4C4 PUSH ECX`、`EDI`を`0x48E4CB PUSH EDI`、最後に`0x48E4CC CALL 0x4F6540`。

| callee入力 | 直前の生成元 | 注記 |
|---|---|---|
| ECX（fastcallの第1引数相当） | `[EBX+0x1EED44]` | `0x48E4C5` |
| EDX（第2引数相当） | `[EBX+0x1EED48]` | `0x48E4BD` |
| スタック引数1 | `EDI` | `PUSH EDI` |
| スタック引数2 | `[EBX+0x1EED1C]` | `PUSH ECX` |
| スタック引数3 | `EBX+0x1EED20` **候補集合** | `PUSH EAX` |
| スタック引数4 | `EBX+0x1EED30` **除外集合** | `PUSH EDX` |

calleeプロローグ`0x4F657B/0x4F6589/0x4F6590/0x4F6597`でスタック4引数を個別取得。正常エピローグ`0x004F66CE`は**`RET 0x10`**。4スタック引数計16バイトのcallee清掃と一致。例外脱出の完全ABI・vptr・関数全境界までは未証明。

## 3．除外集合の「照会」とローカル集合の「挿入」を誤認しない

`0x004F6540`の旧Ghidra疑似Cでは、第6引数`param_6`（上記除外集合）を`local_104`に保持。`local_104+4`からRB木ヘッダを参照し、例えば`0x4F6C??`近辺からの巡回・条件判定に使用。`0x004F8AE0`はキーを符号なし比較してノードを探し、戻りノードを書込先ポインタ`EAX`へ格納する**検索関数**であり、入力コンテナのノードを挿入する関数ではない。`0x4F6D86`、`0x4F77EE`の2 CALLを機械語＋旧DBで照合。

反対に、`0x004F9000`（重複判定付き挿入ヘルパー）は`0x4F70BA`と`0x4F7127`で呼ばれるが、両site直前の`EBX`はそれぞれ**`LEA EBX,[ESP+0xF0]`**と**`LEA EBX,[ESP+0x100]`**であり、**スタック上の一時コンテナ**を指している。したがってこの2件を**`context+0x1EED30`除外集合の直接writer**と誤認してはいけない。`0x004F91A0`は本物のノード挿入（`[unaff_EDI+8]`件数加算）の補助だが、ここで扱うローカル集合への挿入は別物。

**未解決**：除外集合の永続的な追加・削除writerは現時点で未特定。`0x004F6540`の全関数/すべての間接callを追跡しない限り「除外集合は書き換えられない」とまでは断定できない。`0x00553F60`での空木初期化、`0x004B8920`での破棄は別のライフサイクル証拠だが、このrunで独立検証したwriterとは扱わない。

## 4．独立再現監査（実ゲーム非起動）

監査ファイル：`verify_rea_20261024_14h_threeway_exclusion.py`。Python標準ライブラリのみ使用。PEのIMAGE_SECTION_HEADERからVAを原本のバイトへ写像、E8 `rel32`を独立計算、3つの条件分岐のshort displacementを検証、旧SQLiteの`calls`、5関数のGhidra擬似C本文SHA、および選定した意味上の照合点を確認。SQLiteはオフラインZIPからメモリにdeserializeし、原本への書込みなし。入力SHA、ZIP CRC、manifest hash、SQLite integrityを先に確認する。

| チェック | PASS |
|---|---:|
| EXE/ZIP/DB SHA256 | 3/3 |
| ZIP CRC・manifest hash・SQLite integrity・旧DB内部数・PE base | 6/6 |
| VA別のPE機械語 | 42/42 |
| E8 CALL先計算＋SQLite一致 | 10/10 |
| short分岐先 | 3/3 |
| 関数ごとの擬似C SHA | 5/5 |
| 意味照合マーカー（補助） | 7/7 |
| **選定監査合計** | **76/76** |

**76件は選定静的照合項目であり、関数完成数や複製率ではない**。ベースの10,268件Ghidra擬似CはREA正式5種証拠ではない。

## 5．正式REA・Golden・次に必要なこと

| 項目 | 値 |
|---|---|
| 今回新規REA VERIFIED | **0** |
| `info/pseudo/assembly/callers/callees`正式新規5種完全充足 | **0関数**。旧DB機械生成info/pseudo/callsと限定ASM照合のみ |
| 既存Wave1～5 VERIFIED | 前回までの報告64/64。**今回PC正式証拠は再読不可**のため確定再認定なし、二重計上なし |
| 正式TODO / VERIFY / BLOCKED書込差分 | **0 / 0 / 0**（未編集） |
| 新規独立論点 | 本研究IDのVERIFY 1件（正式キュー未登録） |
| 原作ゲームGolden PASS / strict MATCH | **0 / 0**（今回未実測） |
| 完全複製率 | 未測定 |
| 新規REA・Ghidra・ゲーム実行 | **0 / 0 / 0** |
| 監査単体実行時間 | JSONの`elapsed_seconds_approx`参照（約1秒） |
| 調査全工程所要時間・PC負荷 | **不明** |

**優先次関数**：`0x004F6540`内部の除外集合のエイリアス伝播、および`0x0048F720`の除外判定と`0x0048D6A0`の三分岐接続。将来PC正本復旧時には先にMASTER/レーン規約/REA QUEUE・PROGRESS・既存run/owner/lockと現行10,274検索DBの実体・SHA・重複IDを確認。必要な関数だけ最新DBで検証し、owner権限が確保できたときだけREA所有領域に一度同期。原本・MASTER・他レーン・Gitを更新しない。

## 6．復旧ID

- `REA-RC-20261024-1435-LOCAL-SSE429-01`：2026-10-24 14時台、試行 Local Compact `read_file(MASTER_LEDGER.md)`、実エラー`UNAVAILABLE / SSE probe 429`、種別 CONNECTION/RATE_LIMIT（安全拒否ではない）。最後の成功はオフラインZIP・EXEと監査76件。未達は最新PC owner/lock/run/DBの照合・正式同期。継続場所は本研究IDのオフライン成果および独立監査スクリプト。
- 拒否済みVA`0x5710C0..0x571500`・Wave6・REAエクスポートには触れていない。Remote/Work使用なし。自動化設定変更なし。
