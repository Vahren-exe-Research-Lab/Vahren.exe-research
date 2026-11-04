> Recovery annotation (2026-11-05): privacy-sanitized derivative. One personal absolute research-root prefix is replaced with `<research-root>`; the full authored technical body, historical status and corrections are otherwise preserved.

# 迫真戦記 ver0.67｜新B 04:17 独立研究：BattleWnd active tree `+0x248` の登録元特定

- ID：`B-OFFLINE-20261023-0417-T012-T013-ACTIVE-TREE-QUEUE-INSERT-01`
- 対象：T012（Missile/SimpleMissile管理）、T013（衝突候補管理との区別）、参照T011（Skillゲート）
- 日時：2026-10-23 04:17 JST開始。所有者：B。状態：**OFFLINE-UNSYNCED / STATIC-EXE-ASM / STATIC-SQLITE / VERIFY / NOT READY**。
- 原作ゲーム実行・Golden PASS **0**、strict MATCH **0**、新規READY **0**、MASTER更新 **0**。

## 1. 原本・接続・安全・復旧

Desktop Commander Local Compactで `<research-root>\MASTER_LEDGER.md` を最初に読み取り試行し、次のエラーで接続に失敗：`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。**接続/レート制限**であり既存の安全拒否ではない。別Remote/shell/toolによる対象PCへの再試行なし。

復旧ID：`B-RC-20261023-0417-LOCAL-SSE429-01`。未確認＝最新checkpoint、Task Queue、READY、重複、最新Protocol/B HANDOFF、安全拒否台帳、未同期最新一覧。PCへの今回の保存と同期は**未実施**。前回 `B-RC-20261023-0316-LIBRARY-CORRECTION-SESSION-01` の訂正未反映問題は、別IDのまま扱う。旧安全拒否アドレス `0x5710C0..0x571500` は解析対象から外し、拒否された証拠・操作への再試行なし。

ChatGPT Libraryで `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` および `/Vahren.exe` の原本を見つけ、正規file IDから作業コンテナへコピーして**読み取り専用**で解析した。

| 証拠 | SHA256（今回の実測） |
|---|---|
| ver0.67 `Vahren.exe` | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインパック | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内 `search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP 34件のCRC PASS、SQLite `PRAGMA quick_check=ok`、SQLite SHAは BUILD_MANIFEST.json と一致。Ghidra再解析・REA・原作EXEの実行/改変なし。静的索引の直接CALL索引を**原作EXEのPE32実バイト**と独立照合した。以下の要点以外の分岐・型は全て意味論未確定とする。

## 2. 今回のP0解決部分：`BattleWnd +0x248`の登録元

前回03:16時点のP0「`0x0040E2F0`で検索・削除する`manager+0x248`の**登録元が分からない**」を、今回初めて静的に追跡した。

原作の `BattleWnd` シングルトンは `0x008B8C90`。`0x0051D260` は同オブジェクトの構築に関わり、`+0x24C`のtreeヘッダを初期化する。2種類の生成関数はそれぞれ生成物の `+0xA8` に `0x008B8C90` を設定する命令を持つ。

- `0x00580F24: MOV [EBP+0xA8],0x008B8C90`（原作ASM直接照合）
- `0x00548DBD: MOV [EBX+0xA8],0x008B8C90`（同）

### 2.1 生成時の二段階登録：owner側とglobal側は別の入口条件

従来Bが確認したowner索引（既知・**再計上しない**）は、生成時 `Skill+0x1FD != 0` の条件下で `owner → +0x1D4 → manager +0x68` へ登録：`0x00581FA6→0x565780`, `0x00581FB0→0x5158E0`、別の生成経路は `0x00549EAD`, `0x00549EB7`。

今回の独立増分は、その**後の分岐**にあるglobal索引への登録予約。

| 生成関数 | 新規条件（局所スタック） | JNE到達先 | CALL site → function | 実際の操作 |
|---|---|---|---|---|
| `0x00580280` | `0x00581FB9: CMP [ESP+0x1B],0` | `0x00582039` | `0x00582040 → 0x0040E670` | `BattleWnd +0x268`の追加待ちvectorへポインタを積む |
| `0x00547FC0` | `0x00549EC3: CMP [ESP+0x5B],0` | `0x00549F49` | `0x00549F50 → 0x0040E670` | 同 |

`0x0040E670`内部は`+0x26C`（終端）、`+0x270`（容量終端）、`+0x268`（先頭）を参照し、ポインタ要素を書き込んで終端を4バイト進める。**この時点ではまだ `+0x248` treeへの直接挿入ではない**。スタックフラグの代入元・意味は未特定。Skill+0x1FDとは異なるゲートであり同一視禁止。

### 2.2 `0x0040E2F0`が「追加待ちvector → tree実挿入」を行う

更新処理 `0x0040E2F0` 内、原作ASMで以下を同一関数内の順序として確認。

| VA | 動作 |
|---|---|
| `0x0040E49A` | `BattleWnd+0x24C`から**既存active tree**ヘッダ取得 |
| `0x0040E4AE` | 既存要素にvtable `+0x04`の間接CALL |
| `0x0040E4FF/0x0040E505` | `+0x278/+0x27C`の**削除待ちvector**参照 |
| `0x0040E528` | `0x00579AA0`で `+0x248` treeをキー検索 |
| `0x0040E53D` | `0x00510850`で一致範囲削除 |
| `0x0040E54B/0x0040E551` | `+0x26C/+0x268`の**追加待ちvector**境界取得 |
| **`0x0040E55F`** | **`0x00498EE0`呼出：+0x248 treeに追加待ち要素を登録** |
| `0x0040E5C0/0x0040E5F1` | 追加/削除vector終端を調整する後処理 |

更新関数は早期終了する分岐を持つので、上記**到達時**の順序であり、すべてのフレーム/ミサイルがこの処理を必ず通ると主張しない。

### 2.3 `0x00498EE0`の実登録処理

`0x00498EE0` は追加vectorの `[begin,end)` を4バイト単位で走査する。

- `0x00498EF6`でtree要素数がゼロか検査する。
- 空／端点適格などの条件では `0x00498F00,0x00498F24,0x00498F47 → 0x00565780`。ノードを確保し、`node+0x0C`へ追加vectorの**ミサイルポインタ値**をキーとして入れる。
- `0x00498F11,0x00498F35,0x00498F58 → 0x0040EBE0`、treeへノード登録し要素数を更新。`0x0040EC03–04`でtree要素数を1増やし保存。
- `0x00498F21`および`0x00498F44`は`JAE`、キー端点判定は**符号なし32bit比較**。既存キーなどでは`0x005AF0F0`側を選ぶ分岐があり、毎回新規挿入とは限らない。
- `0x00498F74`でvector入力カーソルを+4し次の要素へ。

**結論（STATIC-ASM）**：前回不明の**global active tree `BattleWnd+0x248`の生産者／挿入関数が `0x00498EE0`** と特定できた。旧owner tree `+0x68`とは別の経路である。`0x565780`が複数treeで共通のノード割当を担っていても、実際の挿入器は異なる。

### 2.4 追加待ちと削除待ちは二つのvector

`0x0040E670`（直接callerは今回調査範囲の二つ）が参照するのは `+0x268/+0x26C/+0x270`の**追加待ち**。一方、前回Bが見つけた`0x00552092 → 0x0040E700`は `+0x278/+0x27C/+0x280`の**削除待ち**。後者は今までどおり原作実行の死滅/メモリfree確定ではない。

**到達した1回の`0x40E2F0`内部では**既存要素のvcall、削除待ちの処理、追加待ちの処理の順となる。これは**同じ処理パスで追加されたばかりのオブジェクトが、先行した既存tree反復に参加しない**ことを示す。ただし、いつ生成され、どの更新passへ反映されるか、途中早期return、同一ポインタの追加・削除同時キュー、重複・メモリアドレス再利用、厳密なtick順序はすべてVERIFY。

## 3. 機械的検査と根拠の階層

- **元EXE実バイト＋SQLite一致の直接CALL：18/18 PASS**（既知owner登録やremoveルートも参照関係確認用に含む。18件すべて新発見という意味ではない）。
- **原作EXEの固定VAに対するASM命令バイト：30/30 PASS**。
- **関連7関数の保存Ghidra擬似C SHA再計算：7/7 PASS**（検索基盤内部一致、意味論・実機検証ではない）。
- **CALL rel32変異の負例：6/6検出**（合成）。
- ZIP内SQLite `quick_check=ok`／ZIP CRC34件 PASS／manifest SHA一致。
- 原作GamePlay、SAVE Golden、strict MATCH は0。静的推論を実行実測と表記しない。

証拠：`B_T012_T013_ACTIVE_TREE_QUEUE_EVIDENCE_20261023_0417.json`、検証器：`B_T012_T013_ACTIVE_TREE_QUEUE_VERIFY_20261023_0417.py`。検証器はEXE/ZIP/SQLiteを**読み込むだけ**、単独のB JSON出力ファイル以外に書き込まない。DLL・ゲーム・Git・Ghidra・REAは実行しない。

## 4. 旧IDとの非重複・統合制限

- 今回IDは既存の `B-OFFLINE-20261023-0316-T012-T013-CROSS-DOC-CALL-AUDIT-01` の**未解決 `+0x248` 登録元**を新たに解いた。前回の49 CALL横断照合を新規の発見として再計上しない。
- `B-OFFLINE-20261023-0114-T012-T013-MISSILE-INDEX-LIFECYCLE-01` のowner tree登録や削除vector発見は既存成果扱い。
- ZIPの `MASTER_LEDGER.md / LANE_B_HANDOFF.md / T012_BATTLE_CALC.md` は今回の新規VA `0x00498EE0 / 0x0040E670 / 0x0040EBE0`を説明しておらず、過去B報告と現在参照可能な資料に同一研究IDは見つからなかった。ただし**最新Windows MASTER/他レーンとの衝突・READY照合は未実施**。既存解決済みP0との誤重複を防ぐため `VERIFY` のまま。
- 原作の戦闘遷移入口/出口ハックへの互換契約に転用するなら、Eが独立して判断する。E MASTER、他レーン、Git、開発コードへ書かない。

## 5. 次のB未解明P0

1. **今回固有のVERIFY:** `0x00581FB9 [esp+0x1B]` と `0x00549EC3 [esp+0x5B]` が立つ生成条件を、呼出引数と初期化元から遡及。`Skill+0x1FD`との異同を確認。
2. **同じmanager実体:** `[missile+0xA8] = 0x008B8C90` の不変範囲と、`0x40E2F0`の `in_EAX` を実行時に比較。aliasと寿命はVERIFY。
3. **実戦に直接重要:** `0x0040E4AE` active treeのオブジェクト側vtable `+0x04`の具体的な派生ターゲット、接触`0x515470 → 0x4E6D10`からHP・状態/RNGに到る真の後続。
4. T013通常攻撃の最終対象選択、T024戦闘AI、T028士気・敗走は未解明P0。新規解析なしと明記。

**Golden要求**：完全同一ver0.67のEXE SHA、DAT、MAP、SAVE、戦闘直前状態、tick、RNG、各ミサイル識別子、ownerとBattleWndのポインタ、スキル2ゲート、追加待ち `+0x268`、active tree `+0x248`、削除待ち `+0x278`の観測列を1runに紐付けること。原作一次実測なしでは互換PASS/strict MATCHに昇格させない。

**最終判定：** `STATIC-EXE-ASM/STATIC-SQLITE`の範囲で**global tree登録元を特定**。dynamic alias・queue処理到達・本来の戦闘結果と接続は`VERIFY`。**NOT READY / OFFLINE-UNSYNCED**、PC正本更新なし、master統合なし、original Golden PASS=0 / strict MATCH=0。
