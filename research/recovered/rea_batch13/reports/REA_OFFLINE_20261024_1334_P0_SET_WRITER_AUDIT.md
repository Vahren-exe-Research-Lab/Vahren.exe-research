# 迫真戦記 ver0.67｜REA独立P0：戦闘候補集合・除外集合の書込先を分離

- 研究ID：`REA-OFFLINE-20261024-1334-P0-SET-CANDIDATE-EXCLUSION-WRITERS-STATIC-01`
- 実施時刻：2026-10-24 13時台 JST
- 状態：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 研究所有範囲：REA独立の静的証拠。製品コード、原本、MASTER、QUEUE、PROGRESS、A～E、Git、スケジュールは変更なし。
- **新規性**：前回12時台の「2集合が別引数で伝播」から進め、候補集合への直接挿入CALL 3箇所と除外集合の読み取り用途、挿入の非空ゲート、および4関数の正常復帰スタック清掃量を原作PEバイト＋旧Ghidra索引で区別した。旧CALL件数を新規発見として再加算しない。

## 0. 先読み・接続・資料の状態

`Desktop Commander Local Compact` で Windows正本の `rea_lab/decomp_task/PROGRESS.md` を先読みしようとしたが `INVALID_ARGUMENT / McpServerError: Session terminated`。接続障害であり、**安全拒否ではない**。Windows MASTER/規約/REA QUEUE・PROGRESS/直近run/owner/lock・現行SQLiteの最新状態は未取得。研究PC電源状態、CPU、RAM、active.lockの状態は不明。Remote・Workを使っていない。

代替としてChatGPT Libraryの既存ルート `/` に実在した`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`と`Vahren(2).exe`を読み取り専用で取得した。前回12時台の報告・JSON・検証スクリプトも会話の実ファイルから確認。ZIP内 `research_snapshot/rea_lab/decomp_task/PROGRESS.md` は**2026-10-09時点の15/16**であり、最新の正式状態ではない。過去報告のWave1～5 `64/64` を本runで再認定しない。前回12時台監査は独立再実行で62/62 PASS（再計上なし）。

**ソース識別**：

| 対象 | SHA256 |
|---|---|
| 原作同一内容の承認済EXEコピー | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内**旧**`search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

旧DBは内部**10,268**関数。Libraryの引継ぎ文書`HAKUSHIN067_CURRENT_GHIDRA_HANDOFF_20261021.md`によれば、PC正本は内部**10,274**関数、現行DB SHA256 `282924553309C4778FF6C5D5346CCF5C2BCB1B6FD17E46DBBAE9031547453F8D`。その**現行DB本体は今回未入手・未照合**。旧DB結果を最新正本と誤認しない。

## 1. 独立して新たに結び付けた書込先

### 1.1 `0x0048F9E0 → 0x004868D0`（CALL `0x00490122`）

`0x49010D LEA ESI,[EBP+0x1EED30]` → `0x490113 PUSH ESI`で**除外集合**のコンテナを渡す。その直後の`0x490114 LEA EDI,[EBP+0x1EED20]` → `0x49011A PUSH EDI`で**候補集合**を渡す。ほかの引数を加えて`0x490122 CALL 0x4868D0`へ接続する。したがって両者を1つの木として扱うべきでない。

`0x004868D0`の旧Ghidra擬似Cには`FUN_00476720(param_3);` があり、そのE8呼出site **`0x004880AF`**はPE機械語およびSQLite `calls` ともに`0x00476720`へ一致する。`param_3`はこの呼出経路での候補集合側であり、`param_4`側（除外集合）への同型直接挿入は確認されない。これは**候補集合への書込経路**であって、除外集合への書込ではない。実際の挿入成立は周辺条件・例外に依存する。

### 1.2 `0x00490180 → 0x00488290`（CALL `0x0049021A`）

`0x49020B LEA ECX,[ESI+0x1EED30]` → `0x490211 PUSH ECX`で除外集合を、`0x490212 PUSH EBP`で候補集合を別引数として渡す。直前のEBPの所有者については既存報告の追跡を引用し、今回の局所PEチェックのみでその全生存期間を新規証明したとは扱わない。

`0x00488290`の旧Ghidra擬似Cにも`FUN_00476720(param_3);`があり、実際のCALL site **`0x004893E7`**を原作PE＋SQLite両方で確認した。これも`param_3`（候補集合）側へ挿入し、`param_4`（除外集合）への同型直接挿入ではない。

### 1.3 共通ヘルパー `0x00489630`（CALL `0x004879BF` / `0x00488C44`）

両経路が`0x00489630`へ入ることを2つのE8 CALL siteで確認した。旧擬似Cでは候補集合に対応する`param_6`に対し`FUN_00476720(param_6);`がある。CALL siteは**`0x00489CC5`**、直前`0x489CBE PUSH ESI`を含むバイトも照合した。

一方、除外集合に対応する`param_7`は`*(undefined4 **)(param_7 + 4)`等から木のノードを参照し、候補の照会・集計に利用する。`FUN_00476720(param_7)`という同型直接挿入は、今回の旧擬似Cにはない。`0x00489630 → 0x00489DB0` のCALL **`0x0048977F`**も確認。`0x00489DB0`の旧擬似Cには`*(undefined4 **)(param_8 + 4)`による集合参照があり、除外集合がさらに下流でも参照され得る。ただし、**間接エイリアス書込の完全否定や全関数の完全なwriter列挙ではない**。

**これら3つの`0x00476720`への直接CALLは既存SQLite登録済み**。今回の新証拠は、2つのコンテナのどちらが書込み対象かを対応付けたデータフローである。

## 2. 新しい条件：`0x00489630`の挿入には局所コンテナの非空ゲート

- `0x00489C07 CALL 0x005158E0`：局所内側マップへの挿入経路。
- `0x00489C3F CMP DWORD PTR [ESP+0x4C],0`。
- `0x00489C44 JNE 0x00489C81`：比較値が非ゼロの場合に候補外側マップへの追加側へ進む。
- `0x00489CC5 CALL 0x00476720`：条件を通過した先で候補集合への挿入。

旧Ghidra擬似Cも`if (iStack_3c == 0) { cleanup } else { ... FUN_00476720(param_6); ... }`と一致する。したがって、**共通ヘルパーは毎回無条件に候補を追加するわけではない**。ただし、この局所カウントが実ゲーム中のどの条件で0になるのか、原作のGolden条件は未実測。このゲートを除外集合自身の空/非空と同一視しない。

## 3. 呼出規約についての部分独立証拠

PE上の正常returnサイトで以下のスタック清掃命令を直接確認した。

| 関数 | 正常return site | 機械語 | 清掃バイト数 |
|---|---|---|---:|
| `0x004868D0` | `0x00488256` | `C2 1C 00` | 28（7スタック引数相当） |
| `0x00488290` | `0x0048954A` | `C2 18 00` | 24（6スタック引数相当） |
| `0x00489630` | `0x004899F2` | `C2 1C 00` | 28（7スタック引数相当・ECX受渡しを別途検討） |
| `0x00489DB0` | `0x0048A339` | `C2 20 00` | 32（8スタック引数相当） |

これらは**少なくとも1正常復帰経路**の後片付け量であり、関数境界全域、SEH/C++例外脱出、vptr、間接CALL解決、完全ABIを証明するものではない。特に`0x00489630`にはCALL直前のECXロードがあるため、7つのstack引数に加えてECX引数を考慮する必要がある。

## 4. 独立検証・否定証拠の限界

Python標準ライブラリでPE32のセクション表からVA→生バイトを写像し、E8 rel32を計算。旧SQLiteはRAMへ `deserialize` して読み取り専用で検査。外部実行を含む原作ゲーム、REA、Ghidraを起動しない。

| 項目 | PASS |
|---|---:|
| EXE/ZIP/DBハッシュ・ZIP CRC・manifest・SQLite integrity・旧関数数・PE基底等 | 9/9 |
| PE指定命令（LEA/PUSH、条件分岐、RETを含む） | 24/24 |
| E8 CALL先の独立相対アドレス計算 | 13/13 |
| SQLiteの対応直接CALL参照 | 13/13 |
| 旧擬似Cハッシュ・対象表現の選択的照合 | 18/18 |
| 反例：今回追跡した3関数で除外集合を直接`0x476720`へ渡す同型コードはない | 3/3 |
| **今回の選定した検査合計** | **80/80 PASS** |

これは**80関数の逆コンパイル完了**ではなく、選択した静的チェック80件の一致。反例3件はGhidra旧擬似C内の文字列不在という**限定的な否定証拠**。間接経路や異なるwriter関数を排除しない。前回12時台62/62は監査スクリプト独立再実行で再確認したが、今回80/80には加算していない。

## 5. REA正式指標・保存差分

| 指標 | 値・範囲 |
|---|---|
| `info / pseudo / assembly / callers / callees` | 対象関数の機械生成info/pseudoとCALL indexは照合。assemblyは選定部分のみ。正式REA 5種の新規完全充足 **0関数** |
| 新規REA VERIFIED | **0件** |
| 既存 Wave1〜5 VERIFIED | 過去報告 **64/64**。PC正本を今回独立再照合できず、加算なし |
| 正式QUEUE/PROGRESS TODO/VERIFY/BLOCKED書込差分 | **0/0/0**（未編集） |
| 新規オフライン論点 | 1件 `VERIFY`（条件付き集合書込先・同一性・alias検証、正式QUEUE未反映） |
| 実ゲームGolden PASS / strict MATCH | **0 / 0**（実機起動なし） |
| 完全複製率 | **未測定** |
| 新規REA/Ghidra実行 | **0/0** |
| Work・Remote・ゲーム実行 | **0** |
| 監査スクリプト単体実行時間 | 約 **0.87秒**（他工程・独立再実行を含まない） |
| PC負荷・解析全所要時間 | **不明** |

## 6. PC復旧時にすべきこと

1. **先に**PC正本のMASTER、レーン規約、REA README/QUEUE/PROGRESS、既存run/evidence、owner、active.lock、安全拒否とEPERMの記録を確認。今回研究IDと既存成果が競合しないかを照合。
2. `HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`（10,274内部関数）の正本指定・manifest/hashをread-only検証。今回の`0x004868D0`, `0x00488290`, `0x00489630`, `0x00489DB0`と`0x00476720`のCALL-site・関数区間・vptr/ABI/例外returnを現行側に再照合。現行ZIPを新規アップロードすればPC不通でも同じ確認が可能。
3. `context+0x1EED30`に**実際に挿入/消去するwriter**の呼出siteとコンテナ引数別名関係を追加調査。今回見つけた3 CALLは`context+0x1EED20`側のwriter候補であり、除外集合writerに誤計上しない。
4. `0x00489630`の`0x489C3F`局所カウントが0となる条件を、`0x0048F720`の候補除外と接続。非空/空・全候補除外・ポインタ寿命・正常return/例外returnを別々にGolden条件化（現時点実測0）。
5. 所有者・ロック・既存ID・ソース差分に問題がないときだけ、REA所有領域へ**1度だけ同期**。旧成果・原本・MASTER・他レーンを置換しない。拒否済み操作の迂回なし。

接続障害記録：`REA-RC-20261024-1334-LOCAL-SESSION-TERMINATED-01`。時刻2026-10-24 13時台 JST、対象`PROGRESS.md`先読み、試行 Local Compact `read_file`、応答`McpServerError: Session terminated`、影響はPC正本同期・最新重複・owner/lock未確認。許可された次手は正本再接続時の読み取り照合。安全拒否ではない。成果はOFFLINE-UNSYNCEDとして残す。
