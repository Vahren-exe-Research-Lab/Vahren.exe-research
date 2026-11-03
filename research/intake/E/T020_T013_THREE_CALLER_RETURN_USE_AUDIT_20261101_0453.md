> **PRIVATE E intake | sanitized Library-source preservation, 2026-11-03.** Existing research ID `E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01`. Original Library Markdown (not present in current authorized-PC `tests/`): measured original raw-file SHA-256 `a14162ddc2cb73d9782638d19c1e4fff87598972332658da892934273215e70a`. Any protected/refused address literal in the *historical safety-HOLD metadata only* has been redacted; this GitHub copy is **NOT original-byte identical**, and its earlier offline original-game, source-runtime or snapshot claims were **not independently reverified on the research PC**. Evidence stays legacy `STATIC/SYNTHETIC/VERIFY`, `PUBLISHED_INTAKE_SANITIZED_LIBRARY_SOURCE / NOT_CURATED / NOT_READY`. Prior refusals and Golden constraints remain unchanged.

# 迫真戦記 E｜T020/T013 0x004E53B0 3 callerの戻り値利用差分（04時台・OFFLINE）

- 研究ID：`E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01`
- 担当：E/T020、T018のGolden識別子とT019の矛盾管理に渡す補助証拠。
- 調査時刻：2026-11-01 04:53 JST。対象snapshot：2026-10-21。
- 状態：`OFFLINE-UNSYNCED / STATIC Ghidra snapshot / SYNTHETIC 24/24 PASS / VERIFY / NOT RUN / NOT READY`。
- 原作実ゲーム DYNAMIC OBSERVED **0**、actual Golden PASS **0**、strict MATCH **0**。新規READY正式統合 **0**。

## 取得出典と信頼境界

1. 認可PCの `Desktop Commander Local Compact.read_file` で現行 `MASTER_LEDGER.md` 取得を試行したが `McpServerError: Session terminated`。これは接続障害であり安全拒否ではない。別経路で認可PCの旧拒否を迂回しない。
2. ChatGPT Libraryのユーザー提供 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（2026-10-21 snapshot）を**今回実ファイルとして取得**。zip size **19,646,444 bytes**、実測SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。`search.sqlite` はZIP内コピーだけを `mode=ro` + `PRAGMA query_only=ON` で使用。EXE・SAVE・ゲーム・Ghidraの再実行なし。原作EXEの前回記録済み期待SHA256は `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回実PEを再照合していない）。
3. 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` `develop` read-only。今回確認したGitHub HEAD `0225b2e1cd5c710137a3d921f593d158df06624a`、`symbols.tsv` blob `3fcf2d436c21f3fc91791a91e75c9a800167ca4d`、`REF_BATTLE_AI_MORALE.md` blob `83fb9b91a84e8190042802ed7af5666ca51f7f8c`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`。GitHub HEADとPC `develop` の一致は未確認。
4. 03時台既存研究 `E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01` をベースラインとして区別し、同一発見・同一fixtureを再追加しない。

## 新規増分：3つの直接CALLにおける戻り値の使われ方

以下は旧Ghidra擬似Cおよび索引上の直接CALL情報。実行時にどの経路を通るかは未確定。`param_1` がUnit基底である想定もオリジナルABIで独立確定したわけではない。

| index内CALL site | caller entry / 旧関数code_SHA256 | 擬似C上の必要な条件（**十分条件ではない**） | このcallerでの値利用 |
|---|---|---|---|
| `0x00545A02 -> 0x004E53B0` | `0x00545740` / `4BD1B725B04BA8B7EE47829A7026AE9B23D8840EF747B3BDB24CE4CC4D4890D1` | `(char)Unit+0x1867E == 0` かつ `param_1[0x35] >= 0` ほか | `iVar10`へ戻り値取得、`param_1[0x795c]`（byte offset `+0x1E570`）へ格納。格納後の先行値比較は別途VERIFY。 |
| `0x0057AD8C -> 0x004E53B0` | `0x0057AA00` / `5827D0DF895C261CB6CFB81ABCCC730BC7F31EC977FFA0411BDF466C51E978B7` | `(char)Unit+0x1867E == 0` かつ `param_1[0x35] >= 0` と `param_1[0x61ab] == 0` ほか | `iVar7`へ戻り値取得、同じ `param_1[0x795c]`へ格納。後段の`extraout_ECX`はGhidraレジスタ推定であり、その値を戻り値と同一と仮定しない。 |
| `0x0057D982 -> 0x004E53B0` | `0x0057D8B0` / `2E0612C1CFC8295826E75095FCF6D2C37763EA867434D9E10E5667CFD0970A89` | `Unit+0x1867E != 0` かつ座標非負・先行優先経路未成立・`(char)param_1[0x23]==0` ほか | `iVar5`に取得。**この関数体では** `+0x1E570`への格納が見えず、`0x004C1860`の戻り値 `cVar4==0` かつ `iVar5==0` の場合にのみ `vtable+0x5C` 間接CALLへ到達し得る。 |

呼出対象 `0x004E53B0` の旧Ghidra code SHA256 は `1B74D266BE034E2984E3C4456EBE5CF5DAEBDCA07C8674A934EB34EF3F5CE1E1`。戻り値として候補ポインタ様の値または0を返す複数経路が静的に存在。**3 callerの同じ戻り値を「常に `Unit+0x1E570` に保存」「常に最終攻撃対象へ昇格」と一括定義しない。**

**新規な差分（03時台との差）**は、`Unit+0x1867E`に対する`==0`の2つのcallerで結果を保存する一方、`!=0`側の別callerでは戻り値を真偽gateとして使う、という**callerの局所文脈**を3者対照したこと。これらの条件は該当局所箇所において相反するが、実際のプレイで必ず交互に実行されるという意味ではない。

## T020 受入fixture・不変条件

- 旧Ghidra `search.sqlite` で関数4件の保存されたcode SHAを照合：**4/4 PASS**。
- `0x004E53B0`への索引上の直接CALL 3箇所を列挙照合：**3/3 PASS**。これはnative PE E8 bytesの今回再確認ではない。
- 3つのcallerにおける擬似C guard / store / 仮想呼出条件を確認：**3/3 PASS**。
- sourceテキストの意図的な偽改変4件（2つの格納先の書換、flag逆転、矩形関数呼出欠落）を検証器が拒否：**4/4 NEGATIVE REJECTED**。
- caller3種×フラグ2種×仮定の戻り値ゼロ/非ゼロ2種×**他の局所前提充足か否か**2種＝**24/24 SYNTHETIC PASS**。いずれもモデルの内部整合であり、原作動的実行に対するPASSではない。特に`scan_zero_rect_pending`は矩形結果のゼロが未確定で、仮想CALLが実行されたことを意味しない。
- 前回の03時台T020 128件fixtureを同じ旧SQLiteから別途再実行：**128/128 synthetic PASS**。前回成果の再確認であり、新規128件とは数えない。

### T019の解釈矛盾管理

- GitHub既存辞書 `0x4E53B0 = Unit_RefreshTargetLatch` は、特定callerで `+0x1E570`へ格納する既存文脈に基づく名前。今回の`0x57D982`局所gate用途とは両立可能。**Wiki/DAT/EXEの新規確定矛盾とはしない**。
- 既存GameClear（DAT13/TXT2）の探索範囲差は旧RESOLVED、実loader順序はVERIFY。今回新たなWiki/DAT/EXE原文の取得・直接照合は行っていない。
- 候補研究は `KB_CANDIDATE`。ID=`E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01`、owner=E/T020、VA/CALL 3 siteを上表に固定。**辞書の既存名前を勝手に更新しない**。専任KB curatorの審査待ち。

### T018 Goldenとの比較境界

`research_snapshot/tests/T018_GOLDEN_CORPUS.md` 旧1473〜1478行を今回ZIPから直接再読：C-NB02のsci1 po2/sp2→sp16は**静的な候補**。実ゲームの合法未改変UIで G0 開戦を観測できたときのみ DYNAMIC OBSERVED。G1はその同一戦闘の直前SAVE実byte SHA256・EXE・操作・時刻・turn/phase。G2は実選択MAPとSHA、三陣営A/B/supportのPower、ordered Unit/Troop、隊長・配置・向き、開始frame。保存Spot構成・s16.map候補から実戦配備を捏造しない。既存の旧拒否T018表境界への再試行・迂回なし。

本T020 fixtureは実SAVE/入力/映像と結合しておらず、source rankが `STATIC SNAPSHOT` であるため、Golden受入票へPASSとして代入不可。**G0/G1/G2いずれもNOT RUN、DYNAMIC OBSERVED 0、actual Golden PASS 0、strict MATCH 0**。

## 正本・保留・再開

- MASTERの現行値はLocal接続障害により未取得。**旧最後の確認値** checkpoint196 / READY596（A115・B229・C136・D116）、34 Task DONE9 / IN_PROGRESS21 / VERIFY4。今回は再集計していない。
- 今回の新規正式READY IDなし（0件）。既存のowner/READY/source SHA/時刻/合意/重複/競合をMASTER最新版と突合できないため、**正式統合のみ `BLOCKED(CONNECTION)`**。今回の独立研究はOFFLINE-UNSYNCEDで保留。
- 旧安全拒否：T018表境界、C T026/T032、D T030 TSV、`[PROTECTED_RANGE_REDACTED]`等を継承。旧B HOLD21・10/25未回収資料・過去OFFLINE-UNSYNCEDも未解決。新規の安全拒否は**0件**。接続障害と安全拒否を区別。
- 許可外変更：PC原本EXE/ZIP/SAVE、MASTER、A-D/REA/dev_lab、共有knowledge、Git/push/merge、Work、設定、他タスク **0件**。
- 再開：①Local復旧後の最新MASTER/規約/全owner HANDOFF・REA保存RUN・E資料・KB SYNC_STATUS確認→②現行owner/READY/競合/同ID・source SHA/時刻/拒否履歴との重複照合→③本IDを一度だけE所有T020へ反映可能か判定（自動READY化しない）→④許可済み原作G0/G1/G2一次証拠取得と新実装との同条件可視比較へ進む。CPU負荷が高い場合は軽量read-onlyのみ。

**保存とreadback:** 下記独立SHA台帳を用いて、新規報告・検証器・fixtureと台帳自身を保存先から読み戻す。ライブラリに保存できてもPC正本は未同期である。
