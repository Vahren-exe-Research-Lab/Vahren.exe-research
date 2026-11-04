# 迫真戦記 新B｜T013 二経路キャッシュ出自とT012 virtual+80分岐のオフライン照合

- **オフライン研究ID**：`B-OFFLINE-20261019-1516-06`（正式B証拠IDではない）。対象T013主・T012副。原作ver0.67同梱Vahren.exeについての保存済み証拠の**静的再照合と新しい複合fixture設計**であり、新規原作実機観測ではない。
- **現在の状態**：`STATIC SAVED-REA × PREVIOUS-B-PROBE JOIN / DESIGN-SYNTHETIC / OFFLINE-UNSYNCED / NOT READY`。最新PC MASTER/B HANDOFF/所有資料の再読は接続障害で未達。新しい機械語命令の発見を主張しない。
- **既知対象SHA256**：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（保存REA記載値、原本再hashなし）。
- **入力1**：ChatGPT Library `/decomp_task.zip`、更新 `2026-10-18T17:01:26Z`、本ZIP SHA256 `e1ecf0b9c9a315df3eae39bc88399b54150ed0622baee813d945d31f7d2442cb`。`runs/20261009T225741694Z/57B870_procedure_{info,assembly,pseudo_code,callers,callees}.json` の5件`checked.ok=true`。ASMの既保存証拠ID `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`。
- **入力2**：B先行 `B-20261019-1317-01`（0x57DA1Fゲート、B保存native `exe/T013_UNIT_OWNER_PROBE.txt`/`T013_POOL_SEMANTICS_PROBE.txt`をPC接続中に読んだ研究メモ）。今回は**元のnativeファイルを再読できていない**。先行の`B-OFFLINE-20261019-1414-05`と2026-10-11の既正式B`B-20261011-0115-01`、`B-20261015-0110-01`を重複登録しない。
- **入力3**：上記ZIP内のREA所有既存メモ `REA_20261017_1440_V80_OPTIONAL_ARG_BRANCH_CROSSCALL.md`（静的分析済み説明）。本メモが引用する0x57E3xxのnativeテキストを今回独立入手・再hashできていないため、こちらは**既証拠の再利用に基づくモデルテスト**とする。

## A｜T013：同じUnit+1E580でも「値の出自」は異なる

**保存REAからの直接確認（既知命令を再照合）**：`0x57B87F`が`Unit+0x1E534 < global[0x65BCAC]`で低counterへ分岐。低counterかつ`+0x1E570=null`は`0x57B88F→0x57BB94`へ進み、局所的に`+0x1E574/+0x1E580`を明示clearせずret。低counterで`+0x1E570!=null`なら`0x57B8A1/+0x57B8CE`がそのpointerを**両cacheへ直接代入**し、`0x514D60`を呼ばない。閾値到達側でも`+0x1E570!=null`なら`0x57B9C7/0x57B9EE`で両cacheを同pointerへ更新、`0x57B983`のselectorを通らない。閾値到達かつ`+0x1E570=null`の場合は`0x57B983 CALL 0x514D60`を経由して`0x57B9AD→selected`と`0x57B9B3→aux`へ別ポインタを書ける。

**前回の別caller証拠からの条件付き交差照合**：`0x57D9F5..0x57DA1F`は`context+0x1EED64 <=100`（符号付き）かつ旧`Unit+0x1E580=null`の場合だけ`0x514D60`を呼ぶ。`0x57DA2C/0x57DA36/0x57DA3C`で戻りの距離・selected・auxを書き込む。呼出後cacheのnullnessの一致は前回研究`B-OFFLINE-20261019-1414-05`が指摘した**当該呼出の局所不変条件**に限られ、全writer・全tickに昇格できない。

### 新しい検証・実装上の増分（既命令のクロス経路からの導出）

1. `Unit+1E580 != null`は**`0x514D60`の実行証拠ではない**。`0x57B870`の`+0x1E570`直コピーだけでも非nullになる。再実装receiptを`aux_value`だけでなく`source_callsite` (`57B870-low-copy` / `57B870-full-copy` / `57B870-selector` / `57DA1F-selector` / `OTHER_ORIGIN`)に分けるべき。
2. 低counterかつ`+0x1E570=null`の枝は、その関数内では古い`+1E580`を消さない。この後に別caller`0x57DA1F`へ到達し`ctx<=100`だった場合でも**古いauxが非nullなら再探索を省略し得る**。これは*二callerがその順序で呼ばれること・他writer/消失処理がないことを前提にした合成状態遷移*であり、原作stale-targetバグの確認ではない。
3. 閾値到達時で`+1E570=null`なら`0x57B870`からselectorが呼ばれ、選択結果の2つのpointerは異なり得る。もしその後`0x57DA1F`に進み旧auxが非nullなら、**別callerの探索を省略**する可能性がある。逆にselectorが空の両nullを返した場合、当該gateは再探索可能。関数実行順・target寿命・直後の別writerはVERIFY。
4. `0x57B870`のrefresh境界と、`0x57DA1F`の`ctx+0x1EED64 <= 100`は**独立の条件**であり、片方のタイマがもう片方の必須refreshを暗黙に駆動すると仮定しない。`0x65BCAC`のunit_search_bdrと`ctx+1EED64`の用途同一性も未確定。

## B｜T012：`0x580280`を攻撃成功として扱わない枝別fixture

既存REAメモは`0x57E381`の`Skill byte+0x26F`で、(a) ゼロなら`0x57E38C PUSH ESI`→`0x57E3D9`、(b) 非ゼロで`ESI+0x74==0`なら`0x57E3BC CALL 0x580280`→`ADD ESP,0x18`→`0x57E3D7 PUSH 0`、(c) 非ゼロで`ESI+0x74!=0`なら`0x57E3CF CALL 0x54F720`→`ADD ESP,0xC`→`0x57E3D7 PUSH 0`という**局所経路**を記録している。共通後段`0x57E3F9`は仮想slot+0x80を呼び、正常bindingが`0x579290`なら24byte cleanupと整合する。`0x57E3D9`のscaleはcaller側stack由来で、別caller `0x546C6E`の既確認リテラル0.9を流用してよいとは言えない。

ここから得られる**設計上の明確な分離点**：`0x580280`を呼んだかどうか、`0x54F720`か、virtual+0x80への最終オプションDWORDが`ESI`か`0`か、scale/pointsの出所、subtype vptrと正常帰還、HP/MP/効果を別々のreceiptへする。`0x580280`の実作用・RNG/命中結果・`0x54F720`の影響は依然**VERIFY**。本回の合成モデルにcalleeの戻りや攻撃効果を代入していない。

## C｜検証条件と限界

- `test_T012_T013_DUAL_CACHE_ORIGIN_AND_V80_PATHS_20261019.py`は、ZIP hash、57B870の既存REA5/5メタデータ、保存ASM10アンカーと局所モデル/枝別fixtureを読み取り専用で検査する。**合成15/15 PASS・FAIL0**。元の`B-OFFLINE-20261019-1414-05`の14件等を新規に足して公式検証件数としない。
- **結果の分類**：既存x86アンカーの再確認 `STATIC-RECHECK`、二callerの実行順に関する条件付き表 `MODEL/VERIFY`、virtual80の枝別contract `DESIGN-SYNTHETIC`。新関数の5種REA evidence IDは0。新規原作実機Gameplay Golden PASS **0**、新旧strict MATCH **0**。
- **P0の次の観測設計**：対象可視・HP/MP・再探索発動/消滅の原作UI観測を、合法旧ゲーム使用かつ同EXE/DAT/SAVE/map/input/capture・SHA記録が可能な場合だけE/T018へfixture候補として引き渡す。内部`+1E580`や`ctx+1EED64`は旧UIから見えないなら`UNKNOWN/INELIGIBLE`とし、推定target pointerと画面射撃を安易にMATCHへ昇格しない。`0x580280`側は既保存xrefとcalleeを許可範囲で追加確認する必要がある。
- **重複防止**：`B-20261011-0115-01`（57B870 support・counter枝）、`B-20261015-0110-01`（derived pointer cache）、`B-OFFLINE-20261019-1217-03/1414-05`（selectorと57DA1Fとの局所結合）、`REA-20261017-1440-V80-OPTIONAL-ARG-PATH-01`（virtual+80 caller）を再成果採番せず、**新規事項は『出自別二caller receiptを試す合成モデル』と『T012枝別fixtureの非同一性検査』の設計・検証に限定**。

## D｜保存・復旧

- Local試行結果：`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。**接続障害**であって安全拒否ではない。Remote試行なし。PC CPU/RAM・最新MASTER/B HANDOFFは読めない。
- 利用できた過去の最後のPC正本観測は`checkpoint189 / 正式586=A115+B219+C136+D116 / DONE9・IN_PROGRESS21・VERIFY4`。今回直接の最新版証明はなし。Library `MASTER_LEDGER.md`は2026-10-18 16:59Z更新でcheckpoint187の旧コピー。最新MASTERに基づく正式READYや累計加算は**0**。
- 未処理過去ID `B-20261019-0725-01` HANDOFF safety refusal、`E-RC-20261019-0850-B0814-MASTER-SAFETY-01` はBLOCKEDのまま。拒否内容の再提出・分割/別toolによる迂回なし。
- **再開ID**：`B-RC-OFFLINE-20261019-1516-06`。PC復帰または同等に同期済み正本が利用可能になったら、MASTER・規約・LANE_B_HANDOFF・B所有T011/T012/T013/T024/T028の最新版から本IDと既存証拠の重複/担当/予約を照合し、`B-20261019-...`正式採番を必要な新STATIC根拠に限って検討する。sourceが補強設計だけならREADYを立てず監査に留める。
- PCの`data/T012_BATTLE_CALC.md`、`data/T013_AI.md`、`evidence/LANE_B_HANDOFF.md`、MASTER、REA/他レーン/dev_lab/Git/スケジュールには**一切書込なし**。原本EXE/ZIP/SAVEの実行・変更0。ChatGPT LibraryのB用`data/`へ今回の新規メモとテストだけ保存可能な場合は、版を区別して保管する。
