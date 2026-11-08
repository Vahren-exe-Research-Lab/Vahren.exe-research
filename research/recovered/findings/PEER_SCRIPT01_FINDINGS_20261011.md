<!-- SCREENED PARTIAL HISTORICAL RESEARCH. See RECOVERY_LEDGER.tsv and SCREENING.json. -->
# 主要解析記録の部分回収版

原本の個人パスを含む段落、保留対象への言及を含む段落、未確認の付録を除外した。本文の確認区分は著者の当時の記述であり、今回原作を再検証した結果ではない。ファイル全体に自動スクリーニングを実施したが、全478KBの意味とプライバシーの手動確認は未完了。省略範囲は同じフォルダーのSCREENING.jsonを参照する。 2026-11-05に、既存保留範囲に重なる旧保存版3182行を追加除外した。原本は保持する。

# PEER_SCRIPT01 解析記録 — イベントVM・フロー制御・戦闘イベント (2026-10-11)

<!-- CLAUDE-INDEX: Codex/他AI向け。Claude所有。最新の成果はこの表から辿る -->
## 最初に読む：Claude 成果の索引（2026-10-26 更新）
この findings は Claude 所有。Codex / Work / 他レーンは**読み取り専用で参照**し、この表から必要な節へ進む。各節に、STATIC / DAT_DERIVED / ACTUAL / SYNTHETIC の区別と VERIFY を書いてある。原作との Golden / MATCH は特記がない限り 0。

| 話題 | 節 | 状態 | 主な根拠ファイル |
|---|---|---|---|
| 戦略⇄戦闘の場面境界、**基準アドレス G=0x8BE2F0 と E=G+0x504** | §82（実測は §82.5 / §82.6、入口・出口の網羅と訂正は §82.7） | STATIC ＋ **ACTUAL**（画面あり1回、簡易戦闘1回） | `_work/claude_live_boundary_scene_20261026.jsonl`、`_work/claude_live_boundary_simple_20261026.jsonl` |
| プラグインローダーのレビュー、**EXEのスレッド構成とDirectInput8Createの呼び出しスレッド**、修正パッチ | §83 | STATIC ＋ Wine上の単体・結合テスト（実機Windows・ゲーム実行は0） | `_work/claude_loader_patches_20261026/README_APPLY.md` |
| 汎用UI 実証中のクラッシュ 0x5DA9F8（Vorbis デコード）、**BGM ストリームのスレッド構成と原作の二重デコード競合** | §84 | STATIC（実測はまだ。観測用 x32dbg スクリプトあり） | `_work/claude_x32dbg_bgm_race_capture.txt` |
| 汎用UI の候補数: **原作 choice は一覧を展開できない（件数は DAT の解析時に固定）。ラベルは &変数& 展開あり** | §85 | STATIC | `_work/claude_gen_choice_wrapper.py`、`_work/claude_choice_wrapper_k49_proposal.dat` |
| 田所 sw_karate0 の一回分の攻撃（技能連鎖・命中・時刻） | §80 | STATIC | — |
| 原作の読み取り専用の実機観測（ツール、手順、ログ） | §81、§81.6、§81.7 | **ACTUAL**（攻撃者は unit_mt） | `_work/claude_live_obs_karate_02.jsonl`、`_work/claude_live_obs_karate_02_summary.json` |
| 戦争開始〜戦闘終了〜戦略復帰（0x48F9E0 / 0x4922A0 / 0x493630） | §68、§72〜§74、§79 | STATIC、実装あり | `peer_script01_war_start.py`、`peer_script01_battle_end.py` |
| 定義、技能リスト、能力値（def 生成） | §14〜§38 | STATIC、実装あり | `peer_script01_native_definitions.py` |
| スクリプト VM とイベントフック | §18、§79 | STATIC、実装あり | `peer_script01_strategy_events.py` |

使い方:
- コードは `dev_lab/src/hakushin_compat/peer_script01_*.py`、テストは `dev_lab/tests/test_peer_script01_*.py`（`PYTHONPATH=src python -m unittest`）。
- 観測ツールは原作に**読み取り専用で接続するだけ**（書込み・停止・注入はしない）。


担当ID: **PEER_SCRIPT01**（スクリプト文法・イベントVM・実行順序）。
旧EXE実機golden観測 **0件**、strict MATCH **0件**のまま。以下の合成テスト成功は互換の証明ではない。

<a id="f-0"></a>
## 0. 証拠の取り方
- 原本ZIP `新約迫真戦記―ほのぼの神話ver0.67 豪華版(画像・音声削除版).zip` から `Vahren.exe` を**読み取り専用で取り出し**、SHA-256 `E8DAC301…767187`（`exe/HAKUSHIN_EXE_RELATION.md` の記録値）と一致することを確認。そのコピーをクラウド側で capstone 5.x / pefile により逆アセンブルした（新規Ghidra / REA runner は未使用）。原本ZIP・EXEは無変更。
- 既存の保存証拠 `exe/T006_FLOW_CONTROL_PROBE.txt`, `T006_OPCODE_HANDLERS.tsv`, `T006_REGISTRY_RECOVERED.tsv`, `T006_HANDLER_RETURN_CFG.tsv`、疑似C `FUN_004321B0.c` と突き合わせた。
- 実スクリプト590 DAT（`data/source_snapshot/hakushin067_core/a_default/script`）を既存パーサ（declaration_ast / script_body_subset）で静的走査。
- 作業用コピー置き場として `dev_lab/_work/`（Vahren.exeコピー、src/testsのZIP、script corpusのZIP）を作成済み。**この並列作業ルールが届く前に作成したため、競合として報告する。** 不要なら削除してよい。

<a id="f-1"></a>
## 1. 確定事項（CONFIRMED: 命令VAで確認）
### 1.1 主インタプリタ 0x4338D0
- 4本の並列スタック: body `+0x1EED78`、pc `+0x1EED88`、mode(aux) `+0x1EED98`、marker `+0x1EEDA8`。
- marker値は .rdata の定数: `0x637DF8=0`(CALL)、`0x637DFC=1`(IF)、`0x637E00=2`(LOOP)。
- ノード型はRTTIで判別（0x5E72E5 = dynamic_cast）:
  `ScriptFunc`(0x68C268) / `ScriptIF`(0x68C284) / `ScriptBattle`(0x68C29C) / `ScriptWhile`(0x68C2B8) / `ScriptBlock`(0x68C2D4)。基底は `ScriptElement`(0x68C24C)。
- **ScriptIF** (0x433BA3..0x433C51): 条件を評価し、then(+0xC) か else(+0x1C) の**どちらかを必ずpush**する（空のelseでもpushする）。marker=IF。主ループは rif フラグ(+4)を読まないので、**通常イベント中の `rif` は `if` と同じ**。
- **ScriptWhile** (0x433C56..0x433D04): 偽なら何もしない。真なら body(+8) を marker=LOOP でpush。
- **ScriptBlock**（裸の `{}`、0x433D09..0x433DA2）: body(+4) を **marker=CALL** でpush（イベント呼出と同じmarker）。
- **ScriptBattle** → 0x492890 を呼んでパスを終了。
- **ScriptFunc** → dispatcher 0x4A1250。AL≠0ならパス終了（Yield）、AL=0なら同じパスを継続。
- **フレーム終端** (pc==len, 0x4339F9..0x433AFB): 4本をpop。markerがLOOPなら親のpcを1戻す（whileノードを再実行して条件を再判定）し、同じパスを継続。それ以外では、modeスタックが空なら script end (0x433DA7)。親のmodeが異なれば FadeOutSheet（vtable 0x6388D4）によるシーン遷移でパス終了。同じなら継続（**イベント終端自体はyieldしない**）。
- ループ先頭 (0x4339DE) で、現在の mode `+0x1EEC3C` = 最上位フレームの mode。

### 1.2 呼出系
| 命令 | handler | 内容 |
|---|---|---|
| event / call (op0) | 0x4A1317 | arg0=イベント名。**arg1/arg2だけを読む**（`edi<3`, 0x4A1360）。4個目以降は読まない。core 0x4321B0 を flag=0 で呼び、AL=1 (Yield) |
| routine (op1) | 0x4A1430 | **追加引数は渡さない**（push 0,0）。flag=1、AL=0 (Continue, 0x4A1486) |
| core | 0x4321B0 | frameを body/pc/marker=CALL でpush。modeは**通常: 現mode**(0x432715..0x432721)、**scene path: 定数0x636168=2**(0x4327BE)。※Ghidra疑似Cはこのmode pushを落としている |
| core (戦闘中routine) | 0x4321F4..0x4322AD | flag=1 かつ `+0x1EEC44`(戦闘中) → 本体を**戦闘bodyスタック** `+0x1EEDC4/+0x1EEDD4` にpush（主スタックには積まない） |
- 引数なしの event()/routine() は arg index0 の取得で例外（0x415750）。
- scene path（イベント宣言の特定プロパティ2つが非空）では、arg1/arg2 が `+0x1EED4C/+0x1EED50` に入る（0なら `[+0xC]+0x58`）。どのプロパティが条件になるかは VERIFY。

### 1.3 return / break / continue / next
- **return** (0x4A148D): 戦闘中(`+0x1EEC44`≠0)なら `next` と同じ（**巻き戻しなしでyield**）。それ以外は、markerがCALLでないフレームをpopしていき、最初のCALLフレームは**popせずに pc=len に設定**してAL=1。CALLフレームが見つからなければ全部pop後にyield。→ **裸の `{}` の中で return すると、そのブロックだけを抜ける**。
- **break** (0x4A1549): LOOP以外のフレームを**CALLフレームも含めて**popし、LOOPフレームを見つけたらそれもpopしてAL=0。**routine境界を越えて呼出元のwhileを抜ける**。見つからなければ全部pop後に C++ throw (0x4A1669, type 0x6419CC)。
- **continue** (0x4A166E): LOOPフレームの pc=len（終端処理で条件を再判定）、AL=0。途中のフレームはpop。見つからなければ throw (0x4A1745)。
- **next** (op8, 0x4A1429): `mov al,1` だけ。**引数は評価もチェックもしない**。

### 1.4 wait (op9, 0x4A17D8)
- カウンタは**グローバル1スロット** `+0x1EED58`。待機していない状態は sentinel `0x80000008`。
- `wait(n)` 初回: カウンタ=n（arg0のみ、0x4528A0で数値化）にして pc を戻し、yield。以後、毎パス −1。結果>0なら pc を戻してyield。≤0なら sentinelに戻してyield（pcは進んだまま）。
  - ⇒ `wait(n)` は **n+1回のyield**（n≥1）。`wait(0)` と負の値は `wait(1)` と同じ2回。`wait(-2147483640)`（=sentinel値）は毎回読み直しになり**永久に終わらない**。`wait(INT_MIN)` は1回減らすと0x7FFFFFFFになる。
- `wait()`（引数なし）: UI処理中かどうかを判定する（mode==2かつ非戦闘なら4オブジェクト、それ以外は `+0x1E8630` の1オブジェクト）。処理中なら pc を戻してyield、終わっていればそのままyield。
- 戻すpcは、戦闘中なら戦闘pcスタック `+0x1EEDD8`、それ以外は主pcスタック `+0x1EED8C`。

### 1.5 戦闘イベント (`battle { … }`)
- インストーラ 0x492890: `+0x1EED64/+0x1EED60/+0x1EED68` を0にする。root list(`+0x1EEDB8`, count `+0x1EEDBC`)が**空のときだけ**、battleブロック直下の **ScriptIF だけ**を順に追加する（**if/rif以外のrootは捨てる**）。mode=2、`+0x1EEC44`=1、戦闘bodyスタックと発火済みsetをクリア。
- 毎フレームのdriver 0x492D80（通常path 0x492EB8〜）: 戦闘bodyスタックが空でなければ 0x493300 で再開して終了（**body実行中はroot評価もフレームカウンタも止まる**）。空なら `+0x1EED64++`, `+0x1EED60++`。`%10 != 0` なら終了。`%10 == 0` のときだけ root scan (0x4930C0)。`%20 == 0` で 0x49D5B0（未解析）。
- root scan 0x4930C0: rootを**登録順に**、発火済みset（RB-tree `+0x1EEDE4`）に入っていればskip。条件が真なら、`if` は発火済みsetに入れる（`rif` は入れない）→ then-body(+0xC)をpush → **すぐ0x493300で実行**。そこでyieldしたら、**残りのrootはそのフレームでは評価しない**。root の else(+0x1C) は使われない。
- body runner 0x493300: **ScriptIF と ScriptFunc だけ**を実行する。ScriptIF は then/else を必ずpush（入れ子の rif は if と同じ）。**ScriptWhile/ScriptBlock/ScriptBattle は無視して読み飛ばす**。body 終了で 0x52BFF0(1) とメッセージをqueueに入れる。
- 戦闘中の routine は戦闘bodyスタックで**その場で実行**される（1.2参照）。break/continue は戦闘中でも**主スタック**を操作する（戦闘bodyには効かない）。

<a id="f-2"></a>
## 2. 既存Python実装との差分（取り込み時の注意）
| 項目 | 既存 (event_vm_subset / micro_vm_subset / battle_root) | native |
|---|---|---|
| break/continue | 呼出境界を越えると MicroVMError | **越えて**呼出元のwhileを抜ける |
| break/continue（whileなし） | MicroVMError | 全フレームをpopしてから throw |
| return | 境界のフレームを即削除してyield | CALLフレームは pc=len で残し、次のパスでpop（観測上は同じ）。**裸ブロックもCALL** |
| next(args) | 引数があるとエラー | 引数は無視 |
| wait(n) | 1..10000以外はエラー | 0/負=2回、sentinel値=永久、int32で折り返す |
| wait() | 未対応 | UI処理中判定（hostのコールバック） |
| event 追加引数 | 1引数だけ受け付ける | arg1/arg2を読む（4個目以降は無視）、scene pathあり |
| routine 追加引数 | 1引数だけ受け付ける | 無視する |
| 戦闘中routine | — | 戦闘bodyスタックでその場で実行 |
| battle root | 全rootを毎tick評価し、ifを除去 | 10フレームごと、順番どおり、bodyがyieldしたら中断、実行中は時計停止、if/rif以外は捨てる |
| 戦闘body内の while/block | — | 無視 |
| rif（通常イベント） | if と同じ | if と同じ（一致） |

既存モジュールは**変更していない**。新モジュール `peer_script01_native_flow_vm.py` は独立して存在する。統合はメインAIの判断に任せる。

<a id="f-3"></a>
## 3. 実スクリプトでの使用状況（590 DAT / 3,227 event）
- `event(…)`: 1引数 1,773回、**3引数2回**（`4000_AoW/event_aow_100.dat` `event(bt_aow_100,po_aow_100c,po_aow_100b)`、`event_aow_264.dat`）。scene path を通る候補。
- `routine(…)`: 1引数 2,555回。追加引数を付けた例は0。
- `wait(数値>0)` 15,796回、`wait()` 1,165回、`wait(0以下)` 0回、wait(式) 0回。
- return 37回（裸ブロック内0、戦闘body内0）。break 41 / continue 19（いずれも同じイベント内のwhile内）。裸ブロック 5回。
- `battle{}` ブロック10個、root if 91 / rif 1,146。**if/rif以外のroot 2件が捨てられる**: `2023_イベント_リュージ騎士団/event_23_RPG.dat` の `po23_adventure_shrine` L2369-2370 `moveTroopFix(trt1_s4,hnsk1)` / `moveTroopFix(trt2_s4,hnsk2)`。原作では**実行されない**（作者バグ候補。T019/T020へ登録を推奨）。
- 戦闘body内: wait(n) 346回、wait() 58回、next 13回、routine 6回（RTS: `routine(rtsSelect1v1)` など）、入れ子のrif 10回、while/block 0回。

<a id="f-4"></a>
## 4. 実装・テスト
- `dev_lab/src/hakushin_compat/peer_script01_native_flow_vm.py`: `NativeFlowVM`（主パス `run_pass`、戦闘フレーム `battle_frame`）。式評価・UI処理中判定・その他コマンドは host のコールバックを必須にし、無ければ `FlowModelGap` で止める（fail-closed）。native の throw は `NativeScriptThrow`、パス内の無限ループは `NativeHangGuard`。
- `dev_lab/tests/test_peer_script01_native_flow_vm.py`: **36件**（正常系・境界値・異常系の合成35件 + 実スクリプトの静的検査1件）。クラウド側で36/36 PASS。実スクリプト検査は、PC上の snapshot がある場合だけ実行し、ないときはskipする。

- **PC上（Desktop Commander）での全体回帰（2026-10-11 06時台）**: 実行前に他のAIの回帰が動いていないことを確認した。`python -m unittest discover` は **Ran 298 tests OK（exit 0）**。内訳は既存233件、PEER_SCRIPT01の36件、他AIが並行して追加したらしい新規テスト（test_damage_status_* など）。実スクリプトを使う検査 `TestRealCorpusBattleInstall` も、PC上では skip されずに実行されて OK。run_checks.ps1 の残り18ステップ（map/atlas/context/DAT/親参照/scenario/generic/AST audit、scene_cli、clock/VM/invocation/AI の合成シーン）も**すべて exit 0**。
  - 注: `run_checks.ps1` をそのまま実行しようとしたが、`-ExecutionPolicy Bypass` 付きの起動はツールの安全判定で拒否された。そのため、スクリプトの中身と同じ Python コマンドを1つずつ直接実行した。`DEV_LAB_ALL_CHECKS_PASSED` の文字列は ps1 自体を実行しないと出ないため、この行は出ていない。

<a id="f-5"></a>
## 5. 未解明（VERIFY）
- ~~scene path の判定に使う `event` プロパティ名~~ → **解決**: Prop_LookupString（0x4647D0）はプロパティ名を EDX で受け取る。0x4323AB で `map`、0x432441 で `bcg`、0x4324E5 で `bg` を渡している（§9.1 の実装と一致）。FadeOutSheet / 0x52BFF0 の画面効果は未解明のまま。
- ~~event名が解決できないときの挙動~~ → **解決**（§16）: 空の ScriptBlock になり、何も起きない。
- ~~`wait()` が判定するUIオブジェクトの意味~~ → **解決**: 引数なしの wait は、次のものが終わるまで待つ。(a) 0x520280: メイン画面（engine+0x1E8630）でスクロールや移動の要求が残っている（+0x438 ≠ 0x80000008、または +0x468 ≠ +0x46C）。(b) scene mode（mode 2 で戦闘中でない）のときは、さらに 0x515490: 2つのマップ（+0x1E8634 / +0x1E8630）上で、移動中のユニットがいる（各ユニットの +0x1867C == 0 かつ、+0x186B4 ≠ 0 または +0x186C0 / +0x186C8 ≠ 0x80000008）。つまり「カメラのスクロールとユニットの移動が終わるまで待つ」。ランナーは何も動いていない前提で、即座に通過する。
- ~~戦闘bodyが event/call を呼んだとき（主スタックにpushしてyield）の、その後の実行タイミング~~ → **解決**: Script_ModeDriver（0x4335E0）は、mode 2 で battleActive が立っている間、`BattleEvent_FrameDriver(0)` を呼んだ後も battleActive が立ったままなら **RunPass を呼ばずに戻る**。そのため、戦闘中に主スタックへ積まれたイベントは、**戦闘が終わって battleActive が落ちた後**の最初の RunPass で、スタックの一番上から実行される。その後に `battle{}` の次の文へ戻る。+0x1EED18 が立っている特殊な戦闘（0x49B280、ダンジョン等と推定）では別の経路を通る。mode 6 は 0x433E80（StretchBlt を使う画像表示）で、スクリプトは実行しない。
- 0x4338D0 先頭のゲート → **一部解決**。
  - **+0x1EEC4C**（gate A）: MsgWnd_ShowMessage（0x52B600）が、メッセージを表示すると1にする。RunPass はこれが立っている間は何もせずに戻る。つまり「メッセージを表示している間はスクリプトが止まる」。
    - クリア: world や scene を切り替える 0x48B4A0 / 0x48BF60 / 0x48C880 / 0x48D6A0 が、dword 書込みで +0x1EEC4C..4F を一緒に0にする。Player::vf01（入力処理）はこの値を参照する。メッセージウィンドウを閉じたときに個別にクリアする経路は未特定。
  - **+0x1EEC4D**（gate B）: Script_InvokeEventCore の scene path が1にする（scene の初期化待ち）。
  - そのほかのゲート: global 0x87F650、0x87F5D0 && 0x87F6F0（モーダル系と推定）、pModel+0x20（開いているウィンドウ数。param_2 が真なら無視する）。BattleEvent_FrameDriver ではさらに 0x8BB75C を見る。
  - ランナーでは「yield = ユーザーの操作を待つ」として扱っており、この構造と一致する。
- **0x492D80 の戦闘終了判定**（戦闘レーンへの引き継ぎ用メモ）: 10フレームごとに次を行う。
  1. 0x5656A0（AI の tick と推定）を呼ぶ。
  2. ルートを走査する（root の list が空でなければ）。
  3. 20フレームごとに 0x49D5B0 を呼ぶ。
  4. +0x1EED28 が0でなければ、両陣営の判定をする。主体（+0x1EED44）の vf+0x18 == 4 かつ相手（+0x1EED48）の vf+0x18 ≠ 4 か、0x514C80（残っているユニットの判定）で勝ちなら `0x493630(engine, 1)`、それ以外は `(engine, 0)` で戦闘を終える。
  - 0x493630 は、§18 の world フックを発火させる呼出し元の1つ。
- ~~battleEvent() と battle{} root の関係~~ → **解決**（§19b）: 同じリストの末尾に、ScriptIF だけを追加する。
- ~~0x4321B0 が使う文字列プロパティの具体名~~ → **解決**: map / bcg / bg（上記）。

<a id="f-6"></a>
## 6. 担当外の発見（Bレーン T012 / メインAIへの引き継ぎ）
この並列作業ルールが届く前に調べた内容。**既存ファイルは修正していない。**
1. **`0x550D80` の mode3〜5 の定数 `0x63B0B0` は binary64 の 2.0**（raw `0000000000000040`）。式は `(A*R + B*(2-R))*S + 0.5`。既存 `typed_damage_fragments.py` は `(1-R)` で計算しており誤り。保存済みの定数probeには0x63B0B0が無かったため、推測に頼っていた部分。テスト `test_typed_damage_fragments.py` の mode3〜5 の期待値と、`test_damage_two_draws_subset.py` の mode3 の期待値（attack_base 80 → 190）も直す必要がある。`0x63B080 = 2^-15` も確認した。
2. **`0x5D1B80` は MSVC CRT の `_ftol2_sse`、`0x5D1BB6` は `_ftol2`**（全命令を取得済み）。SSE path は FSTP qword → CVTTSD2SI（0方向へ切り捨て、NaNや範囲外は0x80000000）。x87 path も0方向へ切り捨てるが、int64の下位32bitを返し、NaNなどでは0を返す。
3. `DAT_00B14A40 = IsProcessorFeaturePresent(10)`（SSE2判定、0x5BB349。.rdata 0x609654 の初期化テーブルから登録）。SSE2のあるCPUでは常にSSE path。
4. **Direct3D9 の `CreateDevice` を BehaviorFlags=0x20 で呼んでいる**（0x559741..0x559774。D3DCREATE_FPU_PRESERVEなし）。Direct3D9の仕様どおりなら、作成したスレッドのx87は**単精度(PC=24)**になる。sqrt helper 0x5E3B70 はPCビットを保ったまま実行する。戦闘計算が同じスレッドで動くかは VERIFY。精度で結果が変わる例: mode1で A=45, S=0.7 のとき PC53 では31、PC24 では32。
5. `0x550E70` の距離減衰: 分母は **int32の減算（折り返しあり）**（0x551096）。clamp 0x5510A6..C6 は r>1→1、r<0→0、**NaNはそのまま通す**。そのため分母0のときは、0/0=NaNならSSEで0x80000000、±∞なら1か0になる。
6. 2本目の乱数による防御係数はスタックに残ったまま（攻撃側はbinary64として保存される）。mode6の固定値は、残った0.5に加算される（既存の記述どおり）。
付録Aに、この内容のドラフト実装（未統合）を載せた。

<a id="f-7"></a>
## 7. 次にやれること

> 原本141〜142行は部分回収の対象外（held_native_paragraph）。



<a id="f-8"></a>
## 8. 追加作業（2026-10-11 06時台後半）: EXE全体のデコンパイルと、式・命令系の完全回収
### 8.1 EXE全体の擬似Cソース（Ghidra 11.4.2）
- 公式 Ghidra 11.4.2 をクラウド側に導入した（ZIPのSHA-256 `795a0207…e037a6` は公式リリースページの値と一致）。検証済みの Vahren.exe コピーをheadlessで自動解析し、**10,257関数すべての擬似Cを出力**した（失敗0。コード約2.0MB、.text の約94%）。
- そのうえで2回目のパスとして名前を付けた。RTTIのvtableメソッドと手動解析した関数で**626個**の名前、全dispatcherのcase位置に**209個**の命令名コメントを付けた（結果として名前付き関数は計1,129個）。
- 成果物: `dev_lab/recovered_source/peer_script01_ghidra_named_decomp_20261011.zip`（1.8MB。展開すると12MB。再現用スクリプトとmetaデータ同梱）。**元作者のソースではなく、そのままではコンパイルできない擬似C**。構造体のフィールド名はまだ付いていない。
- 以前の「SAFETY_REFUSAL」範囲について: ユーザーの明示的な許可を受け、中身が自作ゲームEXEの互換解析目的の読み取り専用逆コンパイルであることを確認したうえで実施した。ツールの権限確認ダイアログの拒否を回避したわけではない。

### 8.2 RTTIによる元のクラス名（`PEER_SCRIPT01_RTTI_CLASSES_20261011.md`）
- 194個の型記述子（**元のC++クラス名**）を回収した。vftableが分かったのは180クラス・232行。継承関係とスロット数も取得した。
- `ScriptElement`←`ScriptFunc/IF/While/Block/Battle/Set/Data`、`ExpresElement`←`ExpresNum/String/Bin/Func`、`BreakError`/`ContinueError`、`Unit`/`Spot`/`Troop`/`GameModel` など。

### 8.3 命令レジストリを全部回収（`peer_script01_command_registry.py`）
| 系統 | エンジン上のmap | dispatcher | jump table | opcode数 |
|---|---|---|---|---:|
| GENERAL | +0x1EEF50 | 0x4A1250 | 0x4A635C | 79 |
| WORLD | +0x1EEF60 | 0x4A7A90 | 0x4ACD58 | 52 |
| VARIABLE | +0x1EEF70 | 0x4AE0F0 | 0x4B37EC | 84 |
| BATTLE | +0x1EEF80 | 0x4B4710 | 0x4B658C | 17 |
| PB | +0x1EEF90 | 0x4B6710 | 0x4B7820 | 5 (pb1..pb44, 未使用) |
- 名前は登録時（0x44D920）とScriptFunc生成時（__strlwr）の両方で小文字化されるため、**命令名の大文字小文字は区別されない**（`PlaySE`/`playse`/`backscroll` は正常に動く）。
- 未登録の名前は GENERAL→WORLD→VARIABLE→BATTLE→PB の順に既定処理へ落ちていく。
- **実スクリプトの命令呼出し184,060回のうち、未登録は7回だけ**: `chat3`×4（po22_event.dat L532/534、po22_kaiso.dat L494）、`fafeout`×2（po25_event.dat L3341、po25_kaiso.dat L3150。fadeoutの誤記）、`eras`×1（randomev71-80.dat L551。eraseの誤記）。作者バグ候補。最後の既定処理（0x4B6710の後）の挙動はVERIFY。
- 式で使える組込関数は**80個（ID付き）**を回収した（map 0x87A368）。例: `rand`=6, `yet`=5, `count/countVar`=500, `has/inVar`=501, `getTime`=602, `isInterval`=604。
- その他: `isInterval(n)` は「エンジン側のカウンタ % (ceil(n/10)*10)」で、既存の battle_clock.interval_quantum と一致した（0x45191F..0x451948。どのカウンタを使うかは既存のT010記録どおり絶対tickだが、今回は再確認していない）。

### 8.4 式パーサの仕様（`peer_script01_native_expression.py`）
- **優先順位**（map 0x87A568。表 0x62C6EC と、`(`=10 を 0x50D888 で追加）: `* / %`=0, `+ -`=1, `== != >= <= < >`=2（**等値と比較が同じ順位**）, `&&`=3, `||`=4, `)`=9, `(`=10。左結合。**単項演算子は無い**。
- **括弧の癖**: `)` は対応する `(` まで演算子を取り出したあと、**自分自身もスタックに積む**（優先順位9）。そのため括弧グループは閉じきらず、`)` の後ろの演算子が括弧内の最後の値と結合する（`2*(a)+c` は `2*(a+c)` になる）。
- **関数呼出しの癖**: 出力スタックの一番上が変数名のときに `(` が来ると、その変数が関数呼出しになる（`a || b && (c)` は `b(c)` と解釈され、解析失敗）。関数の引数はリテラルか名前だけで、入れ子にできない。関数名は小文字化される。
- 数値リテラルは `[0-9+-]` だけでできたトークンを atoi したもの。atoiの結果が `0x80000008` になる値は数値ではなく変数名として扱われる。
- **実スクリプトの条件16,632個**: ネイティブでの解析失敗は0。ネイティブと標準的な解釈で構造が違うものが89個、そのうち**結果まで変わり得るものが5個**:
  1. `randomev_tyakai.dat` shimokitano_tyakai_function2 L2471 / `_com` L2551: `A==0 && (…) || (…) || …` はネイティブでは `A==0 && (… || … || …)` になる。茶会ボーナスの全分岐に「先生≠akys」の条件がかかる。
  2. `po10_event.dat` L29、`po11_event.dat` L37、`po1_event.dat` L9: 入れ子の括弧と `&& clearflag==0` の結合が変わる。
  いずれも静的モデルからの予測で、実機確認は0件。
- **評価**（ExpresBin 0x44DCE0）: `+ - *` はint32で折り返す。`/` はIDIV（0除算やINT_MIN/-1でゲームがクラッシュ）。**`%` は剰余ではなく `trunc(a*b*0.01+0.5)`**（パーセント）。**`<`と`<=` は右辺から評価**、`>`と`>=` は左辺から。`&&`/`||` は短絡評価で、結果は0か1。未知の演算子は0を返す。`==`/`!=` は、どちらも`@`名なら文字列比較、どちらも違えば整数比較。片方だけ`@`名のときは変換関数0x44DA60を通るためVERIFY。
- 変数の読み取り（ExpresString::evalInt）は**find-or-create**なので、条件式で未定義の変数を読むだけで値0の変数が作られる。短絡評価で評価されなかった変数は作られない。

### 8.5 変数命令（VARIABLE 0x4AE0F0）
- `set`: 引数を評価してから代入。`add/sub/mul`: **対象の変数をfind-or-createしてから**引数を評価し、int32で折り返す。`div`: IDIV（クラッシュの条件は上と同じ）。`mod`: Cの剰余（符号は被除数に従う）。`per(v,p)`: `trunc(p*0.01*v+0.5)`（x87の FILD, FMUL, FIMUL, FADD のあとftol）。
- 命令の整数引数（0x49CCA0）に渡せるのは**数値リテラルか変数名だけ**。`set(x, a+1)` のような式を渡すとネイティブでは例外になる（実スクリプトでの使用は0）。
- 実スクリプトでの使用回数: set 6,488 / add 1,802 / mul 460 / sub 428 / div 225 / per 62 / mod 14。

### 8.6 テスト（今回追加分）
- `tests/test_peer_script01_native_expression.py`: 26件（実スクリプト16,632条件を使う検査1件を含む）
- `tests/test_peer_script01_command_registry.py`: 7件（実スクリプト184,060呼出しを使う検査1件を含む）
- 既存の `test_peer_script01_native_flow_vm.py`: 36件

### 8.7 次の課題
- 構造体の復元: エンジン本体（`in_ECX + 0x1EED78` などのフィールド）、Unit、Skill、SpotのフィールドにGhidraで型を付け、擬似Cのフィールド名を意味のある名前にする。
- ~~字句解析器 0x502DD0 の `+`/`-` 符号の扱いを確定させる~~ → §13 で確定。
- 0x44DA60 の変換関数（文字列と数値を混ぜた比較）。
- ExpresFunc の80関数の本体を、ID順に互換実装する。
- 改良版（enhancedモード）を作るときの土台として、strictの挙動はこのモジュール群を正とし、括弧の癖などは「互換オプション」として切り替えられるようにする方針を提案する。


<a id="f-9"></a>
## 9. 実スクリプトを実際に動かす（`peer_script01_script_runner.py`）
### 9.1 新たに確定した仕様
- **イベント属性**: 本体の先頭にある `bcg = …`、`map`、`bgm`、`handle`、`title`、`volume` などは文ではなく宣言プロパティ（実スクリプトで591イベント、そのうち `bcg` が545）。共通処理 0x4321B0 は `map` と `bcg`（空なら `bg`）を読み（0x432398..0x4324E0）、どちらかが空でなければ**scene path（mode 2のフレーム、FadeOutSheet）**に入る。該当するイベントは**540個**。
- **`@evtend_<名前>`**: event/call/routine を呼ぶたびに、フレームを積む前に整数変数 `"@evtend_"+名前` を1にする（0x432323 → 0x4637A0。戦闘中のroutineでは行わない）。**`yet(x)` = (`@evtend_x` == 0)**（0x44F5C6..0x44F626。find-or-createなので未定義でも作られる）。
- **文字列の解決（0x49C450）**: `@名前` は文字列リスト変数（engine+0x1E863C）の先頭要素。存在しない、または空なら `""` で、変数は作られない。`@`で始まらない名前はその文字列自体。
- **`==`/`!=` で片方だけ文字列の場合**: `@`側に変換0x44DA60（`find('+')` して `substr(0, idx)`、つまり最初の `+` より前）をかけてから比較する。数値リテラルの文字列表現は `""`。`!=` は `==` と同じ構造とみなしている（VERIFY）。
- **組込関数名が未登録の場合**: 0x4C1200 で見つからないとidが `0x80000008` になり、どのcaseにも一致しない（戻り値は未確認でVERIFY。ランナーではMODEL_GAPとして止める）。
- **各命令がパスを終えるかどうか（AL）を自動で導出**: GENERALでYieldするのは op2,5–11,14,15,17,20,21,62–64,70（保存済みCFGと一致）。title/title2 は 0x4A6B30 の戻り値（VERIFY。Yieldとして扱う）。WORLD/VARIABLE/BATTLE の命令はすべてAL=0（継続）。
### 9.2 全イベント（3,213個）を個別に実行した結果
外部関数は0、UI命令は記録のみ、という簡易条件で実行した。
| 結果 | 件数 |
|---|---:|
| SCRIPT_END（正常に終了） | 2,634 |
| PASS_LIMIT（500パス以内に終わらない。待機ループなど） | 482 |
| SCENE_TRANSITION（scene イベントから戻った） | 49 |
| BATTLE_START（`battle{}` に到達） | 12 |
| MODEL_GAP（未回収の経路で停止） | 25 |
| NATIVE_HANG（yieldしないループ） | 8 |
| NATIVE_CRASH（0除算） | 3 |
- 改善前（属性・`@evtend_`・文字列比較が未対応だった時点）はMODEL_GAPが694件だった。
- NATIVE_HANG と NATIVE_CRASH は、関数をすべて0に固定したことによる見かけ上のもので、実機でも起きるとは限らない。
### 9.3 作者バグ候補（静的に確認。実機では未確認）
- **存在しないイベントの呼出し**: `setEraseListOfStudent`（item_chara_choice系の4イベント＋randomev55）、`randomev67_b`、`e18_po22a`、`ev_chara_sichosha2`（po25_majime）、`randomev69_b`、`randomev70_b`。
- **波括弧の対応が取れていない宣言**（宣言が完結しない）: `4000_AoW/event_aow_264.dat` L417（bt_aow_264）、`40_内政/CC_inu_hakuro.dat` L24（ev_chara_hakuro）、`40_内政/politic_sakenomi.dat` L255（sk_gyakutai2）。ネイティブの字句解析器がこれをどう扱うかはVERIFY。
- **未登録の関数 `sfriend()`**（isFriendの誤記と思われる）: po5_event.dat、randomev66系。
- 既出: `battle{}` の直下にある `moveTroopFix` ×2 は実行されない。`chat3`/`fafeout`/`eras` は未登録の命令。
### 9.4 テスト
- `tests/test_peer_script01_script_runner.py`: 7件。実スクリプトのテストは、当初3,213イベントを全件実行していた（約100秒）。現在は8個に1個を抜き出した402イベントで実行している（§12）。


<a id="f-10"></a>
## 10. スクリプト状態だけに依存する組込関数と、リスト変数の命令
### 10.1 組込関数（ネイティブ実装を `native_builtin` に追加）
| id | 名前 | 仕様（VA） |
|---:|---|---|
| 5 | yet(x) | 整数変数 `@evtend_x` が0か（0x44F5C6..0x44F626。find-or-create） |
| 500 | count/countVar(L) | リスト `L` の要素数。`@` は付けても付けなくてもよい（0x49CB10 が取り除く） |
| 501 | has/inVar(L, a, …) | **すべての引数のすべての要素が** `{T(e) for e in L}` に含まれれば1（0x451369..0x45153E）。各引数は0x49C950で解決（`@x` ならリスト、それ以外は1要素のリスト）。T = 最初の `+` より前 |
| 502 | amount/conVar/reckon(L, b) | `T(b_i)` が `T(L)` の中に何回現れるかの合計（0x451564..0x4516D5） |
| 503 | equal/eqVar(L, x) | `T(L[0]) == T(resolve_string(x))`（0x4516F8..0x451791） |
### 10.2 リスト変数の命令（VARIABLE op36–41、0x4AFFDB..0x4B07A6）
- `setv(x, src)`: x を src の解決結果のコピーで置き換える。`addv`: 末尾に追加（重複も残る）。`subv`: src のどれかと完全一致する要素を全部消す（ここでは T を使わない）。`clear`: 変数そのものを map から消す。`shuffle`: Native_VectorShuffle（0x479740、乱数を使う。既存の native_vector_shuffle_subset と接続できる）。`index(L, n, d)`: `d = [L[n]]`、L が空なら `d = []`。範囲外の n の挙動はVERIFY。
- ~~ランナーでは shuffle を「並べ替えない」スタブにしている~~ → §14 で本来の乱数シャッフルにつないだ。
### 10.3 改善と回帰
- 全イベントの実行: SCRIPT_END 2,636、MODEL_GAP 23（500パス上限）。
- PC上の全体回帰（このチャットの書き戻し後）: **Ran 374 tests OK（exit 0、570秒）**。PEER_SCRIPT01の実スクリプト調査テストが重かったため、上限を40パスに下げ、イベント登録表を作り直す処理を省いて高速化した。


<a id="f-11"></a>
## 11. 構造体を型付けした擬似C（ソースバンドル typed/）
- Ghidra上で `Engine` 構造体を定義した。フィールドは curMode / battleActive / waitCounter / battleFrame / bodyStack / pcStack / modeStack / markerStack / battleRoots / battleBodyStack / battlePcStack / battleFiredSet / cmdGeneral〜cmdPB / strListVars など。これを `this` として `Engine::Script_RunPass`、`Script_ModeDriver`、4つの命令dispatcherに適用した。結果、`this->markerStack.last` のように読める擬似Cになった（`typed/typed_engine.c`）。
- `ExpresBin`（op/left/right）、`ExpresFunc`（name/args）、`ExpresNum`（value）、`ExpresString`（text）の構造体を、それぞれの評価メソッドに適用した（`typed/typed_expr.c`）。
- 戻り値の型、ScriptIF/ScriptWhile/ScriptBlock の vector 配置（0x10間隔）、ScriptFunc の名前と引数の位置は未確定で、今後の課題。
- `battleEvent`（op10, 0x4A18B1）: Prop_LookupParentChain("event") で本体を取得してコピーし、要素を 0x436530 で判定、合格したものを 0x5299E0 で登録、最後に 0x4BA280、AL=1。RTSのバトルイベント（2箇所）が使う。登録先の詳細はD/Cレーンと共有したい（VERIFY）。

---
<a id="f-12"></a>
## 12. choice/select の結果書込みとテキストモード再生（`--play`）
- **choice(v, A, B, …)**（GENERAL op15）: 選択肢は最大50個（0x4A1E4C で `eh_vector_constructor(…, 0x1C, 0x32, …)`、std::string 50個分）。決定時に選んだ項目の**0始まりの番号**を整数変数 v に書く（0x41EBE0）。引数が空だと vector の0番目にアクセスして throw する。AL=1（Yield）。
- **select(v, text)**（GENERAL op14）: ダイアログの +0x298 が1のとき、v に1（決定・1番目のボタン）、それ以外で0（キャンセル）を書く。AL=1。
- 画面に文章を出す命令（op11/17/19/78: msg系、dialog/dialogF、title/title2、choiceTitle）は、UIホストに文章を渡す。
- ランナーの UI ホスト:
  - `HeadlessUi`（既定）: 文章を transcript に記録するだけ。choice は0、select は決定（1）を返す。
  - `ConsoleUi`（`--play`）: 文章をコンソールに出し、choice/select を input() で聞く。**原作のスクリプトをテキストだけで遊べる**最初の形になった（描画・音・戦闘はまだない）。
  - 使い方（dev_lab で `PYTHONPATH=src`）: `python -m hakushin_compat.peer_script01_script_runner <イベント名> --play [--scripts <scriptフォルダ>] [--func-default N] [--max-passes N] [--seed N]`。イベント名を省略すると全イベントを調査する。
- select の既定値を0から1に変えたので、分岐の先が長くなった。そのため実スクリプト調査テスト（402イベントの標本）の上限を150パスにし、SCRIPT_END の下限を60%にした。実測: SCRIPT_END 251 / PASS_LIMIT 141 / SCENE_TRANSITION 4 / BATTLE_START 2 / MODEL_GAP 3 / NATIVE_CRASH 1（1.7秒）。
- PEER_SCRIPT01 のテストは合計 **83件**（クラウドで全件PASS）。いずれも合成テスト・静的検査であり、golden（原作実機の観測）は0件のまま。
- VERIFY: choice で選択肢を51個以上指定したとき、51個目以降が捨てられるのか、それとも別の処理になるのか（0x4A1E4C 周辺の詳細は未読）。title/title2 の AL。

<a id="f-13"></a>
## 13. 字句解析器 Lexer_NextToken（0x502DD0）の mode 0 を確定（§7・§8 の VERIFY を解消）
式を読む箇所（0x50360A ほか、計7箇所の呼出し）は、すべて mode 0（第2引数0）で呼んでいる。
1. 生の行を、空白集合 `" \t\r\n"`（0x62C420）で区切って**セグメント**に分ける（`_mbsspnp`/`_mbspbrk`、0x502CB0/0x502BA0）。**トークンが空白をまたぐことはない**。
2. セグメントの中で、現在位置から区切り文字集合 `{}(),;:=!<>&|*/+-%`（0x62C3CC）の最初の文字までを1トークンにする。0x502BA0 は絶対位置を返し、見つからなければ文字列の長さを返す。
3. 現在位置が区切り文字の場合は、演算子表（0x65BF98 の char* 25個を 0x50D6D0 で vector 0x87A508 にコピーしたもの）を**表の順に**照合し、最初に一致したものを採用する: `== != >= <= && || < > { } ( ) = , ; : // /* */ /+ + - * / %`。
4. **`+`/`-` は表で一致しても採用されない**（0x50332A..0x503359: `op=="+"||op=="-"` のとき `len < pos+1` を満たした場合だけ採用するが、一致している以上これは常に偽）。そのため 0x50339D に進み、pos+1 から次の区切り文字までを1トークンにする。
   - `x<-100` → `x` `<` `-100`、`x - 1` → `x` `-` `1`。
   - **`x-1` → `x` `-1`**（被演算子が2つ並ぶため、0x5042FB でネイティブ構文エラーになる）。`a+b*c` → `a` `+b` `*` `c`。
   - 単独の `!`、`&`、`|` は表にないので、同じく次の区切り文字までが1トークンになる（`!x`）。
5. 照合の補助関数: 0x40B200 = `std::string == const char*`（sete）、0x41DED0 = `std::string != std::string`（setne）。
6. 数値リテラル（0x503460）: トークンが `[0-9+-]` だけでできていれば atoi、そうでなければ名前として扱う（既に実装済み）。
- **実スクリプト16,632条件で、旧トークナイザとトークン列が完全一致した**（差分0件）。原作のスクリプトはすべて空白で区切って書かれている。ただし**改造で `if (x-1 > 0)` のように空白なしで書くと、原作では構文エラーになる**。改造時の注意点として重要。
- 条件式の中に `{ } = ; : // /* */ /+` が来たときのパーサーの経路は未回収（VERIFY）。実装では ExpressionModelGap で止める。
- 文字列は復号済みの文字として扱っている。`_mbs*` 系はCRTのANSIコードページ（日本語Windowsではcp932）でマルチバイトを認識する。別ロケールのWindowsで動かした場合の挙動はVERIFY。
- 実装: `peer_script01_native_expression.tokenize` をこの規則に置き換えた。テストを4件追加した（旧1件は置き換え）。

<a id="f-14"></a>
## 14. shuffle/shuffleVar を本来の乱数シャッフルにつないだ
- VARIABLE op40 → 0x479740(first, last): 範囲が空でなければ 0x479A30 を呼ぶ。これは **`std::random_shuffle`**（i = 1..n-1 について、`j = native_shuffle_index(i+1)` を求めて i と j を入れ替える）。
- 0x479A30 は28バイトの要素のうち先頭24バイトだけを入れ替える（既存の `native_vector_shuffle_subset` が記録済み）。VS2010 の std::string（0x1C）の構成は `_Bx[16]`、`_Mysize`、`_Myres`、`_Alval`（状態を持たないアロケータ、+0x18）。つまり**入れ替わらない4バイトはアロケータで、文字列の値は丸ごと入れ替わる**。
- 実装: `peer_script01_script_runner.native_random_shuffle(items, rng)`。既存の `native_shuffle_index` と `LegacyRng` を、読取りだけで再利用している。ランナーは `rng=` 引数で LegacyRng を受け取る（既定はシード0。CLIでは `--seed`）。これで「並べ替えない」スタブを廃止した。
- VERIFY: 原作でいつ `srand` が呼ばれるか（乱数レーンの担当）。シードが一致しないかぎり、原作と同じ並び順にはならない。
- テスト: 独立に再導出した期待値との一致、乱数を引く回数（n-1回、n≦1なら0回）、スクリプト経由の `setv`+`shuffle`。1件追加した。

<a id="f-15"></a>
## 15. スクリプト読込器（0x50B220系）を機械語から再構成した（`peer_script01_native_script_parser.py`）
DATファイルを読み込む処理を、他AIの汎用パーサ（declaration_ast / script_body_subset）とは独立に、機械語の順序どおり移植した。

**ファイル単位の処理（0x50B220）**
- CreateFileA でファイルを読み、istringstream にして、Lexer_NextToken(mode 0) を空トークン（EOF）まで繰り返す。
- 先頭トークンによる振り分けは次のとおり。

| 先頭トークン・状態 | 処理 |
|---|---|
| `//` | mode 2 で行の残りを捨てる |
| `/*` | 0x50B0C0 で `*/` トークンまで捨てる |
| `/+` | `a_system/xp.txt` に `switch` がなければ行コメント。あれば無視して続きを読む（0x879819） |
| 宣言の外 | Decl_Parse（0x504400） |
| 本体が始まる前 | 0x5049E0 |
| `}` | 0x50ACA0（ブロックを閉じる、else 連鎖の処理） |
| 宣言種別が context/workspace/detail/attribute | 専用ビルダー |
| キーワード表に一致 | 各ビルダー |
| 上記以外 | Decl_GenericPropertyParse（0x505210） |

- **ハンドラがエラーを返すと、0x50C9A0 → 0x50BBF0 でエラーを表示し、`_CxxThrowException` で読込全体を中断する**。一方、**EOFの時点で宣言が開いたままでもエラーにならない**（ブロックスタックを検査しない）。

**字句解析（§13の続き）**
- 行は getline で読む。直後にストリームの状態を見て、eof|fail|bad なら終了する（0x502EF0）。そのため**改行で終わらない最終行は、行ごと捨てられる**。
  - 実データでは271ファイルが該当し、内訳は `}` 202、コメント66、空行3。文が失われるファイルは0件。
- 押し戻しは1枠（0x65DA9C）。
- gap（0x65DAB8）は、空白の長さだけ空白文字を入れたもの（0x42AFE0 = `assign(n,' ')`）。タブも1文字の空白になり、行頭では空。

**文の書式（0x505210）**
- `名前 = 値…`（ScriptData）:
  - 行番号カウンタ 0x8797E4 が増えるまで、つまり**同じ行の終わりまで**を値とする。
  - 整数の後ろに同じ行でトークンが続くと「データ文が不正です。数値の後が改行になってません」になる。
  - **ScriptData は宣言のプロパティ map に InsertIfAbsent で入る**。if や while の中に書いてあっても、最初に出たものが有効で、文の列には入らない。
- `名前(引数…)`（ScriptFunc）:
  - 名前は `_strlwr` で小文字にする（ASCIIだけ。**全角の `ｍｓｇ` はそのまま**残るので、命令として見つからない）。
  - 各引数は、先頭トークンが 0x503460 で数値と判定されれば ExpresNum。そうでなければ、先頭トークンに「gap+トークン」を `,` か `)` まで連結した ExpresString。
    - そのため**改行をまたぐ本文は区切りなしで連結される**（`$` が改行の代わり）。
    - `f()` と末尾の `,` は引数を作らない。先頭の `,` は「関数の引数が空文になってます」。
  - 本文中の `(` は文字列の一部として扱う（`chat(a,b,(テキスト）)` は通る）。
- **キーワード表 0x50D650（57件）** は、トークンの `@` より前で引く（0x50B4EE、`member@rsc5` → member）。std::map なので**大文字小文字を区別する**。
  - if/rif → 0x50A5E0、while → 0x50A850、battle → 0x50AE70、text → 0x507110。
  - それ以外は skill 系 → 0x507730、member 系 → 0x508AA0、friend 系 → 0x509E10、icon/consti/cutin 系 → 0x507F60、change 系 → 0x506AD0、power/spot/roam → 0x509520。
  - **`cutin` は GENERAL op74 と同じ名前だが、文としてはキーワード表が先に取る**。イベント内で `cutin(...)` と書いても、命令としては実行されない（実データでは未使用）。
- 0x509520（power/spot/roam）: **`;` で終わるリスト**で、改行は関係ない。各項目は `,` か `;` までのトークンを gap で連結したもの。
  - 他のリスト系ビルダーは「行末の `,` か、次の行頭の `,` で続く」とモデル化した。内部構造は未回収（VERIFY）。

**ブロック**
- if/rif は条件式を読んだ後に `{` が必須（ないと「if文の始めで { を書き忘れてます」）。ScriptIF の +4 は rif フラグ。
- IF の then ブロックを閉じる `}` の後は、1トークンを読む。
  - `else` なら、次は `{` か `if` だけを受け付ける（**`else rif` は「else文の次が不正です」**）。
  - それ以外のトークンは押し戻す。
  - else if は親の else リストに入る。閉じるときは 0x50ACA0 の再帰で、暗黙の else も一緒に閉じる。
- **宣言種別の別名**: `world` と `fight` は `event` になる（0x504468）。実データでは wev_dream / wev_rsc / rts / rtsf の4件。
- 同じタグ名は、`xp.txt` に `old` がなければ「構造体のタグ名が重複しています」になる（0x87981A）。
- `script/unicode.txt` があると UTF-16 として読む（0x8797F6）。さらにその中に `foreign` とあれば、msg/talk/chat/msg2/talk2/chat2/dialog/dialogf/select の9命令を別のパーサ 0x5060A0 で読む（0x8797F7）。どちらも実データには該当ファイルがない。

**実データでの検証（オラクル）**: 「出荷されたデータはエラーなしで読み込める」を基準にした。
- **590ファイルすべてがエラー0件**で読めた。
- 宣言が開いたままEOFに達したファイルが205件ある。これは、最終行の `}` に改行がないため。
- イベント数は **3,237**（旧ローダーより20件多い）。旧パーサが読めなかった15件、world/fight の4件、yuh_is_not_dead_dr を含む。
- 旧ローダーと共通の3,217イベントのうち、**3,165件は構造が完全に一致**した。差が出た52件は、いずれも逆コンパイルで確定した次のネイティブ仕様によるもの: 末尾の空引数を落とす、改行を除去する、タブを空白にする、ブロック内の `=` をプロパティ map に入れる。
- 旧版で「作者バグ候補」とした `}` 不足の宣言（event_aow_264 / CC_inu_hakuro / politic_sakenomi ほか）は、**いずれも改行のない最終行の `}` が捨てられることによるもの**。ネイティブでは、宣言がEOFまで開いたままになるだけで、エラーにはならず、動作にも影響しない。siege_system.dat の余分な `}` も同じ理由で捨てられ、問題にならない。

<a id="f-16"></a>
## 16. 未知の命令・未知のイベント名・未登録の関数（いずれも機械語で確定）
- **未知の命令**:
  - 呼び出しは GENERAL の default → WORLD（0x4A7A90）→ VARIABLE → BATTLE → PB（0x4B6710）と順に渡る。最後の default は、`a_system/debug_paper.txt`（ルート直下でも可）に有効な行があるとき（0x87981C）だけ GameException を throw する。
  - それ以外は 0x4B77A3 の `xor al,al` で、**何もせずにパスを続ける**。GENERAL は WORLD の戻り値をそのまま返す（epilogue で EAX を変更しない）。
- **未知のイベント名**:
  - 先に `@evtend_<名前>` を1にする。
  - その後、Prop_LookupParentChain（0x465060）が**空の ScriptBlock** を返す。フレームは積まれるが、次のステップで pop される。エラーにはならない。
  - 名前は**最初の `+` より前**で引く（0x465195）。
  - 自分の "event" プロパティがない宣言では、`super` チェーンを最大50段たどる。イベントの継承は実データで未使用のため、モデル化していない。
  - event/call/routine の第1引数は、0x49C450 で解決する（`@var` なら、その変数の先頭要素）。
- **未登録の式関数**: id は 0x80000008 になる。default（0x452523）では、debug モードなら throw、それ以外は 0x44F8DC の `xor eax,eax` で **0** を返す（Ghidra の擬似Cは iterator 値を返すように見えるが、誤り）。`sfriend()` は常に0になる。
- これを受けて、§9.3 の「作者バグ候補」の実際の影響は次のとおり。
  - 存在しないイベントの呼出し（setEraseListOfStudent ほか）は、**何も起きない**。
  - `chat3`/`fafeout`/`eras` は**無視される**。
  - `sfriend()` は**0**。
  - 全角の `ｍｓｇ(...)` は**何も表示しない**（po22系10箇所）。
  - serihu.dat の spot リストは、**カンマ抜けの2行が1項目に連結される**（L4365 `…人種 @hsi_hold_2` と L4366 `さあ来い！…` で1項目）。
- ランナーへの反映:
  - 既定の挙動をネイティブと同じにした。
  - `--strict`（debug_paper.txt 相当）で throw に切り替えられる。
  - 全3,237イベントの実行結果（500パス上限）: SCRIPT_END 2,222 / PASS_LIMIT 771 / SCENE_TRANSITION 216 / BATTLE_START 18 / NATIVE_HANG 7 / NATIVE_CRASH 3 / **MODEL_GAP 0**（旧ローダーでは23）。NATIVE_HANG と NATIVE_CRASH は、関数を0に固定したための見かけ上のもの。
- テスト:
  - `test_peer_script01_native_script_parser.py` 20件（実データの オラクル1件を含む）。
  - 既存テストのうち仕様が変わったもの（未知イベント・未登録関数）を置き換え、実データの件数を更新した（EOFで開いたままの宣言を含めたため）。
  - PEER_SCRIPT01 のテストは合計 **110件**、クラウドで全件PASS。golden は0件のまま。

<a id="f-17"></a>
## 17. 文章系命令の細部（機械語で確定）
- **title/title2 の AL**（§9.1 の VERIFY を解消）: 0x4A2256..0x4A2260 で `AL = 0x4A6B30("title", 命令名)` となる。つまり **`title(...)` はパスを終え（Yield）、`title2(...)` は終えずに続ける**。ランナーに反映した。
- **choice の上限**: 0x4A1E4C でスタック上に std::string[50]（0x1C×0x32）を確保する。選択肢をコピーするループ（0x4A1E51..）には**上限の検査がない**ため、51個以上指定するとネイティブではスタックが溢れる（未定義動作）。ランナーでは、51個以上は推測で動かさず NativeScriptThrow にした。
- **msg/msg2/talk/talk2/chat/chat2**（op11, 0x4A1978）:
  - 引数が1個なら本文、2個なら（第1引数, 本文）、3個なら（第1引数, 第2引数, 本文）として 0x52B600 に渡す。途中で 0x49C450 による文字列解決が入る。
  - 命令名が `2` で終わる版では、フラグ 0x8BA1A8 = 1 になる。
- **文字の折り返し**（0x4DB230）: `@`、`$`、`\n` で行を区切り、`。`（0x81 0x42）は特別に扱う。`@` と `$` が画面上でどう違うか（改ページ・クリック待ちなど）は VERIFY。
  - `--play` では `$` を改行、`@` を改ページ（Enter待ち）として表示している（表示上の仮決め）。
- **0x436BC0**: `$$$`、`###`、`%%%`（数値）、`&&&` を引数で置き換えるテンプレート展開。システムメッセージ用で、イベントの msg とは別物。
- テスト: 1件追加（title/title2、choice の51個、本文の分割表示）。

<a id="f-18"></a>
## 18. ゲーム側からイベントを起動する仕組み（world/fight/politics フック、0x432EE0）
- **0x432EE0（ScenarioHook_Run）**: EDX でフック種別（`world`、`fight`、`politics`）を受け取る。
  1. `Prop_LookupString(現在のシナリオ, out, "scenario")` を呼ぶ。この関数は**プロパティ名を EDX で受け取る**ので、引いているのは「現在のシナリオ宣言の `world`（または `fight`、`politics`）プロパティ」になる。
  2. その値（例: tutorial なら `world = wev1`、`fight = fev1`、`politics = ev_poli`）を Prop_LookupParentChain("event", 名前) に渡し、本体を取得する。
  3. その本体をフレームとして積む（marker CALL、mode = 第1引数）。
  - `politics` のときだけ、先頭に合成の ScriptFunc `ppl1`（GENERAL op70）を差し込む。
  - 第3引数が0でなければ、0x46E250 のリスト（==2 で別の種類）を本体に連結する（詳細は VERIFY）。
- 実データでは9シナリオすべてが world/fight を持ち、7シナリオが politics を持つ。world と fight を宣言種別にしたもの（world wev_dream など）は、§15 の別名で event として登録される。
- **呼出し元**（つまりフックが発火する場面。近くの文字列から推定したもので、タイミングは VERIFY）:

| 呼出し元 | 推定される場面 |
|---|---|
| 0x4342A0 | `fight`（戦闘シーン） |
| 0x434EB0 | decide2 の後に `world` |
| 0x471E80 | ×3: decide3 / 出奔（「$$$が出奔しました」）、外交の拒否（diplo_frd/sup_turndown）、ターン処理（no_autosave/kosen/raid_bdr） |
| 0x48C880 | `world` |
| 0x4922A0 | 簡易戦闘（`@battlefield`/`@battleattack`/`@battledefense` 変数）の後に `fight` |
| 0x493630 | ×2: 防衛に成功（「$$$は###を防衛しました」）、報酬の受け取り |
| MercenaryWnd::vf16 | 雇用の後に `politics` |
| 0x51F3B0 | 上士の説明の後に `world` |

  - フック以外でイベントを積むもの: Unit::vf28 / SimpleUnit::vf28（ユニット側からの Script_InvokeEventCore）、BattleWnd/GameCtrl/0x52BFF0 などから 0x431FB0、0x45B850/0x48AD30/0x521D90 から 0x432010。
- ランナーへの反映は今後の課題。ゲームループ（ターン進行）を再現しないと、フックを発火させる順序は決められない。そのため、現状は `--play <シナリオのworldイベント名>` で手動で起動する。

<a id="f-19"></a>
## 19. スクリプトの状態だけで決まる push 系命令（VARIABLE op12/14/15）
- **Rng_RangeInclusive（0x40ED80）**: EAX = 上限、EDI = 下限。`下限 + ftol(rand() × 2^-15 × (上限−下限))` を返す。
  - 名前に反して、上限は含まない（0..上限−1）。定数 2^-15 は .rdata 0x63B080 にある。
- **pushRand(v)**: v = Rng(100, 0)、つまり **0..99**（0x4AEDF8）。
- **pushRand2(v)**: v = Rng(0x7FFFFFFF, 0)（0x4AEE3D）。
  - 積は46ビットあるので、FPU を24ビット精度で動かすと結果が変わる（例: draw = 12345 なら、53ビットで 809041919、24ビットで 809041920）。どちらの精度で動いているかは、他レーンの FPU 精度仮説に依存する（VERIFY）。
- **式関数 rand()**（id 6, 0x44F62B）: `Rng_RangeInclusive(100, 0)` なので **0..99**。引数は無視される（`rand(5)` でも0..99）。実データでの使用は136箇所。
  - 同じ switch で、id 7 isNewTurn は engine+0x1EF4C1 のバイト、id 8 isWorldMusicStop は (engine+0x1EF175 == 0) を返す。どちらもエンジンの状態なので未実装。
- **pushv(L, n)**: n = リスト L の要素数（0x49CB10 で先頭の `@` を取り除く）。存在しないリストは0。
  - 引数が3個の形（0x4AEC46..）は、T(L[i]) と解決した値の一致を数える。実データでは使われていないため、未対応（model gap）とした。
- **addstr(@X, s)**（op81, 0x4B04C2..0x4B05E8）: 次の順に処理する。
  1. 先頭 = 0x49C5C0(X)
  2. 末尾 = 0x49C450(s)
  3. 先頭 += 末尾（0x40B360）
  4. 変数 [0x44DAB0(X)：先頭の `@` を除いた名前] = [先頭]（0x49F7D0 で map に挿入）
  - 結果は**1要素のリストに置き換わる**。実データの用例: 顔画像名に `_joy` などの接尾辞を付ける。
  - 要素が複数あるリストに 0x49C5C0 を使ったときの挙動は VERIFY（先頭要素として実装した）。
- **index(L, n, d) で n が範囲外のとき**（§10.2 の VERIFY を解消）: 要素アクセス 0x40AFB0 は符号なしで `size > n` を判定し、満たさなければ `_Xout_of_range("invalid vector<T> subscript")` を呼ぶ。つまり **std::out_of_range が throw される**（負の n も同じ）。ランナーでは NativeThrow にした。
- pushTurn など、world の状態が必要なものは担当外。
- ランナーでは `rng`（LegacyRng）の rand15 を使う。§14 の shuffle と同じ乱数列になる。
- **PC上の全体回帰**（このチャットで§15〜18を書き戻した後）: **Ran 648 tests OK（674秒）**。他のAIの python.exe が動いていないことを確認してから実行した。
> **訂正（2026-11-09）:** battleEvent全体は既存root listをclearした後、選択したeventのScriptIFを再登録する。以下の「常に追加する」という一般化は撤回する。5299E0単体のappendとdispatcher全体を混同していた。根拠・未確認範囲は[現行REFの訂正](../../../REF_SCRIPT_VM_CONTEXT.md#4-battleevent-replace-all-correction)を参照。以下の歴史本文は原文を保持する。
<a id="f-19b"></a>
## 19b. battleEvent（GENERAL op10）を確定（§11 の VERIFY を解消）
- 処理は次の順に進む。
  1. Prop_LookupParentChain("event", 名前) で本体を取得してコピーする。
  2. 先頭レベルの各要素について、0x436530 で `__RTDynamicCast(ScriptElement → ScriptIF)` を試す。キャストできたもの**だけ**を 0x5299E0 で **std::list（engine+0x1EEDB8 = battle{} のルートと同じリスト）の末尾に追加**する。
  3. 最後に 0x4BA280 を呼ぶ。これはコピーした vector を解放する（operator delete で first/last/end を0にする）だけで、意味的な処理はない。
  4. AL = 1。
- battle{} の 0x492890 は**リストが空のときだけ**ルートを登録する。battleEvent は**常に追加する**。そのため、戦闘前に battleEvent を呼ぶと、後の battle{} のルートは登録されない（仕様上の帰結。実機での確認はしていない）。
- if 以外の要素（命令文など）は無視される。存在しないイベント名なら空ブロックになり、何も登録されない。
- VM に `_battle_event` を実装した。テストを1件追加した。

<a id="f-20"></a>
## 20. 遊び方（テキストモード）と改造時の注意
**起動例**（dev_lab で `set PYTHONPATH=src`。スクリプトフォルダは既定で data/source_snapshot/.../script を使う）:
- `python -m hakushin_compat.peer_script01_script_runner --scenario tutorial --hook world --play`
  - シナリオの world イベント（tutorial なら wev1）をテキストで遊ぶ。`--hook politics` なら内政イベントになる（先頭に ppl1 が入る）。
- `python -m hakushin_compat.peer_script01_script_runner ev_chara_hakuro --play --func-default 1`
  - イベントを名前で指定して起動する。ゲームの状態に関する関数（isMaster など）は、未実装なので `--func-default` の値（既定0）を返す。
- `--seed N`: shuffle と pushRand の乱数シード。`--strict`: debug_paper.txt 相当（未知の命令や関数で停止する）。`--legacy-loader`: 旧パーサを使う。
- 表示: `【話者】本文`。`$` で改行し、`@` で改ページ（Enter待ち）。choice は番号、select は y/n で入力する。

**改造でスクリプトを書くときに引っかかりやすい点**（すべて原作どおりの挙動。§13〜§16）:
1. 条件式の `-` と `+` は、**前後に空白を入れる**。`if (x-1 > 0)` は x と -1 の2トークンになり、条件式エラーで**読込全体が止まる**。
2. `else rif` は書けない（else の後は `{` か `if` だけ）。
3. 全角の `ｍｓｇ(` は命令として認識されず、黙って無視される。
4. 存在しないイベントや命令を呼んでも、エラーにならず**何も起きない**（debug_paper.txt を置くとエラーになる）。
5. `name = 値` は、if の中に書いても宣言のプロパティになり、最初に書いたものが有効になる。
6. ファイル末尾の行が改行で終わっていないと、その行は読まれない（`}` だけなら問題ない）。
7. `cutin(...)` はキーワード表に取られるので、イベントの中では命令として使えない。
8. `choice` の選択肢は50個まで（51個以上は原作ではスタックが溢れる）。
9. spot/power/roam のリストは `;` で終わる。カンマを忘れると、前後の行が1項目に連結される。

**まだできないこと**: マップ・戦闘・ユニット・勢力・内政の実際の処理（他レーンの担当）、ゲームループ（ターン進行やフックの自動発火）、セーブ。ここにあるのは**スクリプトVMとイベントの流れをテキストで再現したもの**で、原作実機との一致検証（golden）は0件のまま。

<a id="f-21"></a>
## 21. 【最重要課題】unit:base と class:base の親解決 — 原作は「同じ種別の中だけ」で探す（CONFIRMED）
**結論**: 親参照（`宣言種別 タグ : 親`）は、**呼出元が指定した種別のレジストリの中だけ**で解決される。種別をまたいで探すことはない。そのため、`unit:base` と `class:base` が両方あっても、原作の中では曖昧さは生じない。
- `unit tnok → base2 → base1 → base` の最後の `base` は **unit:base**。`class defbase : base` は **class:base**（→ base_kn）。
- 先行調査で CROSS_KIND_COLLISION と分類した6,041件は、「unit と class を1つの名前空間として扱った構文上の分類」で、原作の挙動ではない。

**根拠（すべて x86 命令で照合済み）**
1. **種別ごとに独立したレジストリ**（Script_InitKeywordMap 0x50D650）: 各種別について、`operator new`（0x5B6C2B）と map ヘッダの初期化（0x4634A0）で新しい map を作り、0x463280 で「種別名 → map」を種別表に挿入している。
   - unit: new 0x50E385 → insert 0x50E42E。class: new 0x50E55D → insert 0x50E606。
   - workspace〜skillset のどの種別も同じ形で、ポインタを共有している種別はない。
   - world/fight は Decl_Parse（0x504468..0x5044AE）で event に書き換えられる。
2. **`super` を書くのは1箇所だけ**: 0x5049E0（ヘッダの `: 親` → ScriptData "super"、文字列 0x62C918）。
   - **読むのは4関数だけ**（"super" 文字列 0x634090/0x6340A0/0x6340B0/0x6340C0 を参照するコードはこの4関数しかない）。
   - どの関数も、最初に `種別表[種別]`（0x462B30 = std::map::operator[]）でレジストリを取り出してスタックに保存し、**親を1段たどるたびに、その同じレジストリで親タグを探す**。

| 関数 | 保存先 | 親タグの検索 | 段数の上限 |
|---|---|---|---|
| 0x464290 Prop_HasKey | [esp+0x18]（0x464327） | 0x464531 | 0x464559 |
| 0x4647D0 Prop_LookupString | [esp+0x18] | 0x464B1E | 0x464B46 |
| 0x465060 Prop_LookupBlock | [esp+0x1C]（0x46516B） | 0x4653E7 | 0x46540F |
| 0x465770 ScriptSet 系 | [esp+0x20]（0x4658DA） | 0x465AEC | 0x465B14 |

   - 4関数に共通する処理: タグを最初の `+` で切る（0x4643A3 / 0x464949 / 0x4651D7 / 0x465986）。std::map は大文字小文字を区別する（0x4C1200）。まず自分のプロパティを見て、なければ `super` に進む。`super` は空でない ScriptData（+0x14 ≠ 0）でなければならない。上限は 0x32 段（自身＋祖先49段。循環していてもここで止まる）。
3. **Unit 定義の生成（0x582D90）**:
   - 名前を `+` で切る（0x582E36）。
   - `Prop_HasKey("unit", タグ, NULL)`（0x582EB4。キーが NULL ならタグが存在するかだけを返す: 0x46442A..0x46443B）が真なら、def+0x1C = タグ、**def+0x54（クラス名）= `Prop_LookupString("unit", タグ, "class")`**（0x582EF7。class 指定そのものも unit の継承連鎖から取る）、def+0x38 = unit 連鎖の race。
   - 偽なら、名前をそのままクラスタグとして使う（def+0x1C = def+0x54 = タグ、race は class 連鎖から取る）。
4. **Unit のフィールド取得（0x585AD0、呼出し158箇所。*_max 系・level・face・picture・exp* などすべて）**: 次の順に探し、最初に見つかったものを返す。
   - `key2 = key + "@" + シナリオ名`（0x406D50。シナリオ名 = ctx+0x34。0x432F14..0x432F39 で `Prop_LookupString(kind="scenario")` のタグとして渡しているのと同じフィールド）。
   1. unit 連鎖の key2（0x585B24 → 0x585B45）
   2. unit 連鎖の key（0x585B90 → 0x585BB3）
   3. class 連鎖の key2（0x585BFE → 0x585C1F。class は def+0x54）
   4. class 連鎖の key（0x585C6A。見つからなければ空の ScriptData）
   - つまり、**unit の祖先のどれかが定義していれば、class 側の値は使われない**。`@シナリオ` の版が優先されるのは、同じ連鎖の中だけ。
   - 実データの `@` 接尾辞は rsc / sci1 / dream / sc_free / sci_st などで、シナリオ名と一致する。
5. **attack_max などの使われ方**（0x5747A1..0x574817）: `ftol(int(attack_max) × attack(+0x98) × 0.01 + 0.5)` で計算する（整数の積を先に作る。x87_percent_expr と同じ演算）。0 なら attack をそのまま使う。**attack_max は攻撃力に対するパーセント値**。heal_max も同じ形（0x574714..）。

**実データ（unit 4,586 / class 4,080 宣言）に当てはめた結果**
- 8,461件は、同じ種別の中で根まで解決できる。
- 181件は、親タグが**別の種別にしか存在しない**（unit 176件。例: `unit amhsich : amhsi4` の amhsi4 は class にしかない。class 5件。例: `class c_ncncbase : base1`）。原作では、ここで継承が止まる（親が見つからない扱い）。
  - amhsich の場合、unit 連鎖は自分自身だけになり、残りのフィールドは class=c_amhsich の連鎖（c_amhsich→amhsi4→amhsi3→amhsi→base→base_kn）から取られる。
- 24件は、親タグがどちらの種別にもない。大文字小文字だけが違う参照は0件。
- **tnok**: unit 連鎖 [tnok, base2, base1, base]、class = c_tnok（連鎖 [c_tnok, a072, base, base_kn]）。attack_max = **130（unit:base）** で、class:base_kn の180は使われない。hp = 28930、attack = 730 はどちらも unit 連鎖から取られる。

**実装**（新規）: `src/hakushin_compat/peer_script01_native_definitions.py`
- NativeRegistries: 種別ごとのレジストリ。InsertIfAbsent で、`super` もヘッダから設定する。
- 上記の関数に対応するもの: has_key（0x464290）、lookup（0x4647D0）、unit_definition（0x582D90 の一部）、unit_field（0x585AD0）、percent_of（0x5747BF..）。
- テスト: `tests/test_peer_script01_native_definitions.py` **9件 PASS**（合成7件、実データ2件。実データ側では tnok の値と、同じ種別での解決件数 8461/181/24 を固定している）。
- 構文解析器の重複タグ判定でも、world/fight を event として扱うよう修正した（テストを1件追加）。

**未確定（VERIFY）・次の対象**
- キーワード系のリスト（skill / member / friend など。0x507730 / 0x508AA0 / 0x509E10 …）が宣言の map にどう格納されるか（generic の `=` は InsertIfAbsent であることを確認済み）。リストの継承は 0x465060 の mode 2（0x4FAA60 で連結）を使う可能性がある。どの呼出元が mode 2 を使うかは未調査。
- 同じ種別に同じタグが2回あるとき: Decl_Parse は既存の宣言を再利用して InsertIfAbsent で合併する。重複エラー集合 0x87A4E8 がいつクリアされるかは未調査。実データでは unit/class/skill に重複タグはない。
- DAT の読込順（0x50BF60 / 比較関数 0x50BF00）。上記の合併でしか効かないため、実データでは結果に影響しない。
- HP/攻撃などの基本能力値（0x585AD0 ではなく、0x585960 などの別の getter の可能性）、level と成長率、skill / skill2 / delskill / learn の合成。周辺の getter 群（0x583F40〜0x586AB0）も unit を先に見て class にフォールバックする形に見えるが、1つずつは検証していない。
- **次に解析すべき関数**: 0x573BD0（Unit の能力値初期化本体。attack_max などはここから 0x585AD0 を呼ぶ）、0x585960（unit と class を両方調べる getter）、0x584970（同）、0x465060 を mode 2 で呼んでいる箇所（リストの継承）。

<a id="f-22"></a>
## 22. Unit 能力値の生成 — DAT の hp/attack… から Unit+0x90.. と *_max まで（0x58B7F0 → 0x573BD0）
**結論**: 能力値は2段階で作られる。(1) 定義レコード（0x582D90 の def）に、0x58B7F0 が「基本値＋成長×(レベル−1)、上限 `〜Max` で頭打ち」を書く。(2) 0x573BD0 がそれを Unit オブジェクト（+0x90..）にコピーし、条件付き補正（未移植）の後、`*_max`（パーセント）と「2×基本−max」の派生値を作る。**DAT の宣言値はそのまま戦闘の能力値ではない**（tnok の attack は 730 → def 878 → max 1141）。

分類: **C** = CONFIRMED（x86 命令で確認）、**S** = STATIC-HIGH、**V** = VERIFY（未解析・未移植）、**B** = BLOCKED。

### 22.1 呼出し関係とフェーズ
- **C** 0x582D90（def 生成）: 0x58328A で 0x58C0E0(def,0)（skill/skill2 のみ。能力値には触れない）→ 0x58329E で `lv = 0x585AD0(def,"level")`、0 なら 0x80000008（0x5832C3）→ 0x5832CF で **0x58B7F0(ECX=[esp+0x38], EDX=def, lv)**。
- **C** 0x573BD0（引数 [esp+0xF4] = Unit。+0x1C8 = def、+0x1CC = 第2 def、+0x1D0 = フラグ、+0x1DC = ctx）。呼出元は 0x55A455（0x55A130）、0x55AF18（0x55ADD0）、0x573AE7（0x571B70）。
  1. コピー 0x573C19..0x573CAF
  2. +0x1D0 と +0x1CC が両方非0のときだけ: notalent 補正 0x573CC8..0x573D7A ＋ ボーナス3周ループ 0x573D80..0x574705（どちらかが0なら 0x57470E へ直行。0x573CB5 / 0x573CC2）
  3. `*_max` と派生値 0x57470E..0x574CFD（常に実行）
- **S** 0x573BD0 の Unit はレベルアップ処理 0x575110（Unit::vf 群の隣、def+0x168..0x170 を更新）と同じオブジェクト。戦略側／戦闘側どちらの Unit かは **V**。

### 22.2 名前・格納先の対応（**C**）
名前表 .data 0x68D858（0x58B7F0 用。[0..10] 名前、[11..21] `名前Up`、[22..32] `名前Max`）と 0x68D770（0x573BD0 用）は同じ順。

| DAT キー | def | Unit 現在値 | max キー → Unit | 派生（2×基本−max） |
|---|---|---|---|---|
| hp | +0x178 | +0x90 | heal_max → +0xD8（+0xDC = hp） | — |
| mp | +0x17C | +0x94 | —（+0xE0 = mp） | — |
| attack | +0x180 | +0x98 | attack_max → +0xE4 | +0x10C（<0 → 0） |
| defense | +0x184 | +0x9C | defense_max → +0xE8 | +0x110（<0 → 0） |
| magic | +0x188 | +0xA0 | magic_max → +0xEC | +0x114（<0 → 0） |
| magdef | +0x18C | +0xA4 | magdef_max → +0xF0 | +0x118（<0 → 0） |
| speed | **+0x194** | +0xA8 | speed_max → +0xF4 | +0x11C（下限10 → 上限 speed） |
| dext | **+0x190** | +0xAC | dext_max → +0xF8 | +0x120（<0 → 0） |
| move | **+0x1A0** | +0xB0 | move_max → +0xFC | +0x124（下限10 → 上限 move）、+0x1B0 = move |
| hprec | **+0x198** | +0xB4 | hprec_max → +0x100 | +0x128（<0 → 0） |
| mprec | **+0x19C** | +0xB8 | mprec_max → +0x104 | +0x12C（<0 → 0） |

- def 側の並びが名前順でないこと（speed/dext、move/hprec/mprec）は、3箇所が独立に一致することで確認した: 0x58B83C..0x58B8B1、0x4AC0B3..0x4AC130（スクリプト命令の加算/代入）、0x573C19..0x573CAF（コピー）。
- +0xBC..+0xD4 と +0x108 = 大域 [0x65BCFC]。**S**: 0x45AD63..0x45AD80 で `0x46F4C0("unit_status_hp", 100)` の結果を1回だけ書く（書込みはこの1箇所のみ。読みは 0x5747B4 / 0x574CD4 / 0x57E0B5）。0x46F4C0 の既定値の扱いは未検証のため、移植コードでは既定値を仮定しない（引数必須）。

### 22.3 def の能力値（0x58B7F0、**C**）
1. **レベル**（def+0x168）: 引数が 0x80000008 なら `Prop_LookupString(class, def+0x54, "level")`（class 連鎖のみ）。ECX == 0xAB42F8 なら scenario の `base_level` を加算、ECX が他の非NULLなら [ECX+0xDC] を加算、NULL なら加算なし。最後に 1 未満を 1 に（0x58B97C..0x58B98C、符号付き）。**V**: 0x582D90 が ECX に何を渡すか（[esp+0x38]）。
2. **multi 表**（0x58B9A1..0x58BC11）: `Prop_LookupBlock("multi")` を unit（def+0x1C）→ class（def+0x54）の順に読む（第4引数 = 0）。リストごとに係数を 0.0 から始め（FLDZ 0x58BAAA / 0x58BB64）、整数値（+0x20）が非0の要素で `係数 = 値×0.01`、0の要素で `(名前 → 係数)` を map に挿入する（0x58FE60）。**S**: std::map の insert なので先勝ち（unit のリストが優先）。mode 0 は同じ種別の連鎖で最も近い宣言、と推定。
3. **各能力値 i**（0x58BC20..0x58C01A、11回）:
   - 基本 = unit 連鎖に名前があれば unit、なければ class 連鎖、どちらにもなければ 0（0x58BC3A..0x58BCC7。**`@シナリオ` 版は見ない**。0x585AD0 とは別の検索）。
   - 成長 = 同じ規則で `名前Up`。どちらにもなければ `ftol(ceil(multi[名前] × 基本))`。名前が map になければ係数 0.0（FLD qword / FIMUL 基本 → **0x5B6ED0 = ceil**（SSE2 経路 0x5B6F10: 正は切り捨て＋端数があれば +1、負は切り捨てのみ）→ 0x5D1B80）。
   - 値 = 成長 × (レベル−1) + 基本（IMUL / ADD、int32）。
   - `名前Max` が unit/class のどちらかにあれば `値 = min(値, Max)`（符号付き JLE）。なければ頭打ちしない（0 の Max も「ある」扱いで 0 に頭打ちになる）。
4. その後の 0x58A540 / 0x58A400 は exp / exp_mul / exp_max だけを計算し、能力値には触れない（命令を確認済み）。

### 22.4 Unit への展開（0x573BD0）
- **C** コピー: Unit 現在値 = def の値（22.2 の表どおり）。
- **C**（演算部分）notalent: 係数 f = `0x46F4C0("notalent_down",100)×0.01`。f ≠ 1 で、def+0x78 == 0、def+0x94 == 0、かつ 0x585CA0 が両 def で偽のとき、attack/defense/magic/magdef/dext = `ftol(v×f + 0.5)`。**V**: `@mode_sdown`（0x463CA0）の意味、0x585CA0、def+0x78 / +0x94 の意味。
- **V**（**S** の部分あり）ボーナス3周ループ 0x573D80..0x574705: 何らかのリスト要素（+0x3B0 フラグ、値 [esp+0x1C]）について、名前が 0x68D770 の能力値名と一致すれば、フラグが立っていれば `stat += 値`、そうでなければ `stat += ftol(stat × (値×0.01) + 0.5)`（0x574509..0x57452A。**整数積を作らず、係数を先に掛ける**）。名前が training / skill / type / summon_max / movetype の場合は別処理。リストの出所（+0x1CC の +0xD4/+0xD8、要素サイズ 0x1C、map 0xB0A18C）は未解析。**この結果に依存するため、下記の max は「ループが実行されない場合（+0x1D0 か +0x1CC が NULL）」以外では入力が未確定。**
- **C** max と派生値（0x57470E..0x574CFD）:
  - `max = ftol(int(0x585AD0(key)) × 現在値 × 0.01 + 0.5)`（IMUL で整数積を先に作る）。結果が 0 なら現在値（キーが無いときも 0 → 現在値）。
  - 派生 `d = 2×現在値 − max`（ADD/SUB、int32）。attack/defense/magic/magdef/dext/hprec/mprec は SETS/DEC/AND で負を 0 に。speed/move は `d = max(d, 10)`（CMP 0xA / JGE）→ `d = min(d, 現在値)`（0x574C57 JG / 0x574C88 JLE）。現在値が 10 未満なら d = 現在値。
  - 意味（乱数幅の下限など）は **V**。名前は付けず、オフセットで返す。

### 22.5 補正の適用順（確定分と未確定分）
`level`（0x585AD0 → 0 なら class "level"）→ ＋レベル補正（ECX 依存、**V**）→ 下限1 → 基本＋成長×(Lv−1)（Up または ceil(multi×基本)）→ `〜Max` で頭打ち →〔Unit へコピー〕→ notalent（**V** のゲート）→ ボーナス3周ループ（**V**）→ `*_max`（%）と派生値。
- 未確定: race による補正は、この経路では見つからなかった（race は def+0x38 にあるだけ）。ボーナスループの出所、scenario 依存の補正（`@シナリオ` は *_max と level の 0x585AD0 だけが見る）、戦略 Unit と戦闘 Unit の区別。

### 22.6 0x585960 / 0x584970（限定解析）
- **C** 0x585960(out, key)、EDI = def: タグが **unit として存在すれば**（Prop_HasKey(unit, tag, NULL)、0x5859B4）unit 連鎖だけを `key@シナリオ` → `key` の順に探し、**class には戻らない**。存在しなければ class 連鎖で同じ順。結果は ScriptData（out に書く）。能力値初期化からは呼ばれない（呼出元は 0x4771F0 / 0x4780D0 / 0x478F50 / 0x47CE80 / 0x4D4A50 / 0x519490 / 0x560CA0 StatusWnd / 0x562850）。
- **C** 0x584970 は `sub_image@シナリオ` → `sub_image` の画像系 getter。能力値とは無関係のため、ここで打ち切った。
- 0x465060 のリスト継承は multi の読み出しで使われるが、mode 0 なので mode 2（0x4FAA60）は今回も対象外。

### 22.7 実装（既存ファイルへの追加）
`src/hakushin_compat/peer_script01_native_definitions.py`（新規ファイルなし）
- `STAT_NAMES` / `DEF_STAT_OFFSET` / `UNIT_STAT_OFFSET` / `UNIT_MAX_FIELDS`（**C**）
- `definition_level(regs, udef, level_bonus)`: level_bonus は呼出側が明示（**V** 部分は既定値で埋めない）
- `multi_factors`（**C**、map の先勝ちは **S**）、`definition_stats`（**C**）、`unit_copy_stats`（**C**）
- `notalent_scale(stats, percent)`（演算 **C**、ゲートは呼出側。**V**）
- `unit_max_and_low(regs, udef, stats, unit_status_hp)`（**C**。unit_status_hp は引数必須）
- `unit_only_or_class_field`（0x585960、**C**）
- x87 の丸めは既存の `_round_sig` / `_ftol_sse` / `x87_percent_expr` を使う（倍精度 53bit）。
- キーワード文（`multi = …`）を `NativeDecl.lists` に保持し、`lookup_list` を追加した（重複文の扱いは **V**。先の文を保持）。

**tnok（実データ・静的予測。原作実機の観測ではない）**
- level 5（unit tnok）。multi は unit:base の `5, attack, defense, magic, hp, hprec, 2, dext`。`〜Up` / `〜Max` は連鎖になし。
- def: hp 34718 / mp 100 / attack 878 / defense 638 / magic 542 / magdef 1 / speed 90 / dext 61 / move 230 / hprec 62 / mprec 15（例: attack = 730 + ceil(36.5)=37 × 4）。
- ボーナスループが実行されない場合の Unit: attack_max 1141（130%、unit:base）、派生 +0x10C = 615、magdef_max 5、+0x118 = 0、speed_max 108、+0x11C = 72。

### 22.8 テスト・ビルド
- `tests/test_peer_script01_native_definitions.py`: 9件 → **18件**（合成8件追加: レベルの sentinel と下限、multi の先勝ちと係数リセット、Up 優先・ceil・Max 頭打ち、負値の ceil、*_max のゼロ代替と派生値、notalent、0x585960 の class 非フォールバック。実データ1件追加: tnok）。
- **クラウド**: py_compile OK。peer テスト（test_peer_script01*.py）**135件 OK**。クラウド全体の discover は 368件中 23件 ERROR。いずれも他担当のテストで、クラウドに無い素材（stage/*.map、アーカイブ、source snapshot の一部）による FileNotFoundError 19件など。今回の変更とは無関係。
- **PC**: **BLOCKED**（PC のシェルが使えない。DC は使用禁止のため迂回しない）。git status も BLOCKED。前回の PC 648件は今回の版に含めない。
- **原作実機との比較: 0件**（Golden PASS ではない）。

### 22.9 次の解析を阻んでいる関数
- 0x573D80..0x574705 のボーナスループの出所: +0x1CC（第2 def？）の +0xD4/+0xD8 リスト（要素 0x1C）と map 0xB0A18C。これが分からないと、+0x1D0/+0x1CC が非0の Unit の現在値と *_max が確定しない。
- 0x582D90 の [esp+0x38]（0x58B7F0 の ECX＝レベル補正の出所）。
- 0x46F4C0（context 系の整数 getter と既定値）、0x463CA0（`@mode_sdown`）、0x585CA0。
- 0x58FE30 / 0x58FE60（multi の要素テキストの正規化と map insert）。
- 0x575110（レベルアップ時の再計算。0x68D7D4 表と hpUp… を使う）。

<a id="f-23"></a>
## 23. 能力値ボーナスループ（0x573D80..0x574705）— 部隊・リーダー・status 技能による補正
**結論**: ボーナスループの処理内容は、x86 命令ですべて読み終えた。補正の正体は **`func = status` の技能**で、Unit が**部隊（troop）に属しているときだけ**適用される。技能は「リーダーの技能」→「自分の技能」→「（自分がリーダーなら）配下の技能」の3周で、`type` によって選ばれる。補正量は技能の **`time`**（`yorozu` に対象名があればその値）で、`direct = on` なら固定値の加算、それ以外は % 加算になる。補正は Unit 現在値に入り、**その後で** `*_max` と派生値が計算される（§22.4 の max は補正後の値が入力）。
- 未解明のまま残るのは**入力側**だけ: 各 def の技能リスト def+0xEC を作る 0x58C0E0（skill/skill2・skillset 展開・乱数を含む）、`@mode_sdown`、`notalent_down`、`unit_status_hp`、consti map の初期値、レベル補正の ECX。

分類: **C** = CONFIRMED（x86）、**S** = STATIC-HIGH、**V** = VERIFY、**B** = BLOCKED。

### 23.1 Unit+0x1C8 / +0x1CC / +0x1D0 の正体（**C**、Unit 生成 0x56F880 の 0x56FEAF..0x56FEE3）
- +0x1C8 = 自分の def（EDX）。
- +0x1D0 = 部隊オブジェクト（スタック引数 [esp+0x114]）。NULL のこともある。
- +0x1CC = 部隊の先頭 Unit の def（部隊の vector +0xC/+0x10 の先頭）。部隊が NULL、空、先頭が NULL のときは自分の def。つまり **+0x1CC = リーダーの def**、`+0x1C8 == +0x1CC` は「自分がリーダー」。
- 0x573BD0 は +0x1D0 == NULL ならボーナスループも notalent も実行しない（0x573CB5）。0x55A130 / 0x55ADD0 経由（def を Unit 内 +0x1E624 に埋め込む特殊な生成）は +0x1D0 = EBX。

### 23.2 3周の入力リスト（**C**）
| 周 | リスト | 適用条件（技能の `type` = Prop_LookupString(skill, 名前, "type")、0x574184..0x5741A4） |
|---|---|---|
| 0 | リーダー def の +0xEC（技能名の vector、要素 0x1C） | 自分がリーダーでない、かつ type ∉ {1, 3}（0x574206..0x574224） |
| 1 | 自分の def の +0xEC | type ∉ {0, 3}。type 2 は自分の def が「def+0x78 ≠ 0 または def+0x94 ≠ 0」（0x585CC0 と同じ判定）のときだけ（0x5741E4..0x574204） |
| 2 | 自分がリーダーのときだけ: リーダー def の **member リスト（+0xD4）**の各名前を 0x467DE0 で def に引き、その def の +0xEC を **std::set<string>（大域 0xB0A18C、ノード 0x2C）**に入れる（0x416D60）→ 集合順で vector 0xB0A17C にコピー（0x479830） | type == 3（0x5741C8..0x5741DD） |

- 集合と vector は周ごとに空にする（0x573EA4..0x573F0A）。そのため周2の順序は**文字列昇順で重複なし**（std::less = バイト比較 0x402C40）。周0/1 は def+0xEC の順序。
- def+0xD4 = `member@シナリオ` → `member`（unit 連鎖、なければ class 連鎖。0x5833F8..0x583469）から 0x582D90 で作るリスト（0x58354F。def+0x77 / +0x75 が立っている名前は除外）。

### 23.3 技能ごとの処理（**C**）
技能レコードは 0x4678A0（ctx+0x31C のキャッシュ、レコードは 0x599BD0 が作る）。
- +0x40 ≠ 6（`func ≠ status`、0x59CC1D..0x59CC34）なら飛ばす（0x574106）。
- `attr`（+0x110）が `training` なら飛ばす（0x574145。add2 は見ない）。
- 対象の並び: `add2` リスト（+0x158、0x59E81C..0x59E89D）が空でなければそれ、空なら `[attr]`（0x574247..0x574285）。
- 対象ごとの値: `yorozu`（+0x338 の map、0x59F49F..0x59F558）に対象名があれば、その値（node+0x28）。なければ **`time`（+0x2B0、0x59CF6B..0x59CF98。+0x2B0 の writer は builder 内でこの1箇所＋コピー/初期化だけ）**。※`value` キーではない。
- 対象名で分岐:
  1. `summon_max` → Unit+0x168 += 値（0x57436C..0x574399）
  2. `movetype` → Unit+0x14C = 技能の `add`（+0x13C、0x59A79B..0x59A7C8）（0x5743C9..0x574407）
  3. 11の能力値名（表 0x68D770）→ `direct`（+0x3B0）が立っていれば `stat += 値`。そうでなければ `stat += ftol(stat × (値×0.01) + 0.5)`（FILD stat、FILD 値、FMUL 0.01、FMULP、FADD 0.5、0x5D1B80 は切り捨て。負の % は 0 方向に切り捨て。ADD は int32 で回り込む）（0x574431..0x57452A）
  4. それ以外（耐性名など）→ Unit+0x13C の map<string,int>（0x574493..0x574611）:
     - 名前があれば: 現在値 ≥ 10 かつ 値 ≥ 0 なら変更しない。そうでなければ `新 = direct ? 値 : 現在値 + 値`。
     - 名前がなければ: `新 = direct ? 値 : 値 + 5` で挿入する。
     - どちらも、新 ≥ 100 → 10、≤ −100 → 0、> 9 → 9、< 1 → 1。
- `direct` フラグ（+0x3B0）= (`direct == "on"`) で、さらに `d360 == "on"` または `direct == "roll"`（+0x3B1）なら 0（0x59D44E..0x59D5D3、0x40B200 は大文字小文字を区別する完全一致）。
- **S**: `yorozu` の要素 `attack*50` → (text "attack", int 50)。'*' の分割は字句側で、ネイティブの箇所は未特定（**V**）。map の挿入（0x463280）は先勝ちと推定。

### 23.4 notalent の条件（**C**）と適用順
- 条件: 部隊あり（+0x1D0 ≠ NULL）、`0x463CA0("@mode_sdown")+0x1C == 1`、`percent×0.01 ≠ 1.0`、自分の def の +0x78 == 0 かつ +0x94 == 0、**0x585CA0**（= def+0x77 ≠ 0 または def+0x75 ≠ 0）が自分の def とリーダーの def の両方で偽。
- def+0x75 = `0x585890(def, "talent").text == "on"`（0x5830CB..0x58312F）。def+0x77 は実行時フラグ（0x467535 で 1）。def+0x78（0x460C76 など）と +0x94 の意味は **V**。
- 順序（**C**）: def 生成（0x58B7F0）→ コピー → notalent → 周0 → 周1 → 周2 → `*_max`（%）→ 派生値。補正は現在値に入るため、`*_max` と派生値にも効く。
- 重複・解除・再計算: 同じ技能が周0/1で2回あれば2回適用される（集合を使うのは周2だけ）。解除処理はこの関数にはない。0x573BD0 の呼出し（Unit 生成の3箇所）で毎回 def の値から作り直す。レベルアップ時の再計算（0x575110）は **V**。

### 23.5 レベル補正 ECX（0x582D90 → 0x58B7F0）
- **C**: 0x582D90 は入口の ECX を [esp+0x38] に保存し（0x582DE8）、0x58B7F0 の ECX に渡す（0x5832C8）。member の def 生成（0x583546 → 0x466F60）にも同じ値を渡す（0x58351B）。
- **C**: 呼出元は 0x466090（ECX = 0、一時 def 0xB0ABC8）、0x466B00（ECX = EBX）、0x466F60（ECX = スタック引数 [esp+0xC4]）。
  - 0x466F60 の呼出元は21箇所。例: Script_DispatchWorldCommand 0x4A92B6 は **0xAB42F8** を渡す（→ scenario の `base_level` を加算）。MercenaryWnd 0x4D7C93 は [esp+0x2C] のオブジェクトを渡す（→ obj+0xDC を加算）。
- **V**: 各呼出元のオブジェクトの種類（+0xDC の意味）と、どのスクリプト命令が 0x4A92B6 に当たるか。移植コードでは `level_bonus` を呼出側が明示し、`unverified_inputs` に残す。

### 23.6 実装（既存ファイルへの追加）
`src/hakushin_compat/peer_script01_native_definitions.py`（新規ファイルなし）
- `def_has_talent`（0x585CC0）、`def_is_special`（0x585CA0）、`notalent_applies`（0x573C12..0x573D3B の条件）
- `NativeStatusSkill` / `status_skill(regs, 名前)`: 技能レコードのうちループが読む部分（func, attr, add2, yorozu, time, direct, add, type）
- `UnitBonusState`、`apply_status_bonuses(...)`: 3周・選択・対象・値・4種の分岐（周2の member の技能リストを渡さないと ValueError）
- `UnitStatBlock` / `unit_stat_block(...)`: 新エンジンへの受け渡し用。DAT 値（`dat_values`）、def 値、Unit 現在値、*_max・派生値（オフセット付き）、summon_max、movetype、consti、適用の記録、`unverified_inputs` を分けて持つ。`is_final` は、未検証の入力が1つでもあれば False（現状は常に False）。部隊ありの場合、技能リストと notalent の入力は必須（既定値で埋めない）。

### 23.7 テスト・ビルド
- `tests/test_peer_script01_native_definitions.py`: 18件 → **29件**（合成10件、実データ1件を追加）。
  - 合成: 固定/% 加算と順序、0・負値（−29.5 → −29）、int32 回り込み、add2/yorozu/direct・roll・d360、type による周の選択、周2の重複除去と入力必須、training・非 status・未定義技能・summon_max・movetype・耐性 map の上下限、notalent の条件、レベル1/5/上限、能力値の分離、補正 → *_max → 派生値の順、notalent → 加算の順。
- **tnok（仮の入力・静的予測）**: def+0xEC = DAT の unit `skill` リスト（ファイル順）、リーダー自身、配下なし、consti は空と**仮定**した場合:
  - +0x78/+0x94 なし: 現在値は変わらない（type 2 が適用されない）。
  - あり: hp 38190 / attack 966 / speed 108 / move 290、attack_max 1256。
  - 仮定入力のため確定値ではない（Golden ではない）。
- **クラウド**: py_compile OK。peer テスト **146件 OK**。全体 379件中 23件 ERROR。いずれも他担当のテスト（素材なしの FileNotFoundError など）で、§22 のときと同じ23件。今回の回帰ではない。
- **PC**: テスト実行と git status は **BLOCKED**（PC のシェルがない。迂回しない）。`dev_lab/.git/HEAD` = `refs/heads/main` だけを確認した。
- 原作実機との比較: **0件**。

### 23.8 新エンジンへの接続
- **接続できる**: def の能力値（0x58B7F0）、Unit の現在値・*_max・派生値の計算順、status 技能による補正の規則全体、notalent の条件、部隊を持たない Unit の最終値（`has_troop=False` のときは技能リストが不要。ただし `unit_status_hp` と `level_bonus` は入力）。
- **まだ接続できない**: 部隊に属する Unit の最終値。def+0xEC の技能リスト（0x58C0E0）、consti map の初期値（Unit+0x13C）、`@mode_sdown` / `notalent_down` / `unit_status_hp`（0x46F4C0 / 0x463CA0）が未導出。

### 23.9 次に解析すべき関数（優先順）
1. **0x58C0E0**: def+0xEC の技能リスト（skill / skill2、skillset 展開 0x46A3C0 / 0x46A700、0x4FA9F0 と 0x501CA0 の乱数・並べ替え、0x416D60 の集合化）。部隊 Unit の最終値を決める最後の大きな入力。
2. 0x571B70 などでの Unit+0x13C（consti）と +0x168（summon_max）、+0x14C（movetype）の初期化。
3. 0x46F4C0（context の整数 getter）と 0x463CA0（`@` 変数）→ `unit_status_hp`、`notalent_down`、`@mode_sdown`。
4. 0x466F60 の21個の呼出元のレベル補正オブジェクト（+0xDC）。
5. 0x585890（talent の getter）、def+0x78 / +0x94 の writer の意味、0x575110（レベルアップ時の再計算）。

<a id="f-24"></a>
## 24. def の技能リスト生成（def+0xEC）— 0x58C0E0 / 0x58DA40 / 0x58AFA0 / item
**結論**: 技能リストの生成は x86 命令で最後まで読み終え、移植した。乱数を使うのは **class の `skill2`（無作為選択）だけ**で、std::random_shuffle（0x501CA0、CRT rand()、既存の `LegacyRng.shuffle_forward` と同じ手順）を使う。同じ関数の中で consti（耐性）と movetype も作られ、Unit 生成（0x571B70）がそれを Unit にコピーする。これで、部隊に属する Unit の補正入力（§23）が DAT とシードから計算できるようになった。
- 実データの tnok は乱数を1回も使わない（rand 0回）。技能リスト・consti・movetype・能力値補正まで静的に計算できる（下記 24.6）。

分類: **C** = CONFIRMED（x86）、**S** = STATIC-HIGH、**V** = VERIFY。

### 24.1 呼出し順（**C**、0x582D90 新規 def）
1. 0x58C0E0(def, 0)（0x58328A）: 技能リスト＋consti＋movetype＋class の能力値下限。この下限はこの時点では直後の 0x58B7F0 に上書きされる。
2. 0x58B7F0（能力値、§22）
3. member の def 生成（0x583546 → 0x466F60。member の def も同じ処理で作られ、rand() を使いうる。**V**: この並びでの rand() 消費）
4. 0x58AFA0（class 変更・learn・delskill2）
5. item リスト（0x58358A..0x58376D）

その後、0x571B70 が Unit+0x168 = summon_max、Unit+0x13C = def の consti のコピー（0x4C1340）、Unit+0x14C = def の movetype を設定し、最後に 0x573BD0 を呼ぶ（§22/§23）。

### 24.2 0x58C0E0 の技能部分（**C**）
- 開始時に、それまでの def+0xEC を集合 S に入れてから空にする（0x58C17B..0x58C1C3）。
- `skill_or_set_exists`（0x46A3C0）: skillset か skill のタグがあるか。`expand_skill`（0x46A700）: skillset なら `member` リストの各項目（再帰なし、存在チェックなし）、skill なら自分自身、どちらでもなければ空。
1. class の `skill`（mode 0）と `skill2` を読む。`skill2` の先頭項目の数値 N の符号で順序が変わる。N ≥ 0（または skill2 なし）なら `skill` の展開が先、N < 0 なら後（0x58C2B3 / 0x58C929）。
2. `skill2`: 選ぶ数 = |N|。候補 = 2番目以降の項目。候補が1つ以上あれば **random_shuffle**（rand() を 候補数−1 回。選ぶ数が 0 でも並べ替えはする）。
   - 1巡目: 有効でない候補は捨てる。展開した名前の中に S に無いものがあれば採用して末尾に追加（0x590300 = set_difference、**S**）。
   - 2巡目: 残った候補を並べ替え後の順で、選ぶ数に達するまで追加。
3. unit の `skill`（`@シナリオ` 版を優先、0x469460）を展開して末尾に追加。
4. unit の `skill2` は、i 番目の項目の展開を**位置 i にそれぞれ挿入**する（同じ位置に挿入するので、展開の順は逆になる。i は無効な項目でも進む）。
5. talent フィルタ（def+0x77 も def+0x75 も 0 のとき）: 技能の `talent`（+0x50）が `on` なら削除、それ以外の空でない文字列なら、その名前の技能に置き換える。
6. delskill: unit 連鎖に `delskill@シナリオ` / `delskill` があればそれ、なければ class 連鎖（0x465770 の ScriptSet）。各項目を展開し、各名前の**最初の1つだけ**を削除する。
7. def+0xFC、def+0x10C（item の技能）を末尾に追加 → 0x58DA40。

### 24.3 0x58DA40 の後処理（**C**）
1. 重複削除（最初の1つを残す）。
2. fkey: 技能の `fkey`（`名前*数値`）ごとに、数値が**厳密に最大**のものだけを残す（同値なら先に出たもの）。
3. `sortkey`（+0x6C、符号付き）で並べ替え（比較関数 0x582A70 は元の位置 +0xA14 で同順位を決める）＝安定ソート。

### 24.4 consti / movetype / class の能力値下限（**C**、param_2 == 0 のとき）
- def+0x12C consti = unit（`@シナリオ` 版優先）→ class → race の順に `名前*値` を map に insert（先に入ったものが残る、0x463280）。
- def+0x13C movetype = unit に movetype があれば unit、なければ class、なければ race。
- class の**自分自身の宣言だけ**（親を辿らない 0x4645C0 / 0x464C90）に能力値名があれば、`def 値 = max(def 値, class 値)`（0x58D7E9..0x58D907）。

### 24.5 0x58AFA0（**C**）と item（**C**）
- **class 変更**: class 自身の宣言の `change`（例 `c_tnok2*15`）について、名前が空でなく、レベル ≥ 数値なら、class を変えて 0x58C0E0(def, 0) を呼ぶ。これを繰り返す。能力値は新 class の下限まで上がる。**V**: 0x469390 / 0x586320（def+0x158 の再設定）。
- **learn**: unit の `learn`（`@シナリオ` 版優先）、空なら class の `learn`。
  - 数値の項目が段（初期値 1）を決め、名前の項目は「レベル ≥ |段|」なら map に入れて最高段を更新する。
  - 最高段の名前がすべて既にリストにあれば何もしない。そうでなければ 0x58C0E0(def, 1) で作り直し（S = 現在のリスト）、**最高段の名前だけ**を展開して、段 ≥ 0 なら末尾に追加、段 < 0 なら先頭から順に挿入する。
  - 続いて `delskill2`（展開しない、名前で最初の1つを削除）→ 0x58DA40。
- **item**: unit の `item`（`@シナリオ` / 素の名前）、なければ class。数値の項目でグループが切り替わる（最初は front）。front の項目は def+0x10C と def+0xEC の先頭（1つずつ先頭に入れるので逆順）、back の項目は def+0xFC と末尾。最後に 0x58DA40。
- Unit+0x168 summon_max = 0x585AD0(def, "summon_max")。0 なら `unit_summon_min`（0x46F4C0、既定値 1）、負なら 0（0x5729C0..0x572A28）。
- def+0x75 = unit 連鎖の `talent@シナリオ` / `talent` が `on`（getter 0x585890 は unit 連鎖のみ）。

### 24.6 データ読込みの修正（**C**）
- データ文 `x = @`: 数値でない先頭トークンが `@` なら代入しない → 空文字列（0x505381..0x5053AD、0x42F860 は「≠」）。
- リスト `x = @`（項目が `@` 1つ）: 空リストとして格納し、親の値も遮る（0x507E7B..0x507EA5。builder 0x507730 で確認、他の builder にも同じ `@` 比較がある＝**S**）。
- 宣言のデータとリストは1つの map なので、`has_key` はリストのキーも見るように直した（先に出た方が残る）。§21 の件数テストは変化なし。

### 24.7 実装・テスト
- `peer_script01_native_definitions.py` に追加した関数:
  - `skill_or_set_exists`、`expand_skill`、`build_skill_list`、`postprocess_skill_list`
  - `build_consti_movetype`、`class_stat_floor`、`apply_class_change_and_learn`、`apply_item_list`
  - `definition_skill_state`（0x582D90 の順）、`def_talent_on`、`unit_summon_max`、`unit_initial_from_def`
  - 乱数は既存の `legacy_rng.LegacyRng` を読み取り専用で使う（変更なし）。
- テスト: 29件 → **40件**（合成10件、実データ1件）。
  - 合成: random_shuffle の手順を LCG から独立に計算して照合、1巡目の「新しい技能優先」、skill2 の負数、unit skill2 の逆順挿入、sortkey の安定ソート、talent の削除・置換・`@`、delskill（1回だけ削除）、`skill = @` による遮断、fkey、consti/movetype の優先順、learn の最高段・負の段・delskill2、item のグループ、class 変更と下限（自分の宣言のみ）。
- **tnok（実データ・静的予測、Golden ではない）**: rand 0回。
  - def+0xEC = ch0, charge_new, a_dash, sp_chikorita1, ch1, h_gun, sp_speed, seiretsu, pes_knock, c_cv1, ps_hp, ps_at, ps_df, ps_sp3, ps_mv3, ps_pl, ps_eart, ps_wate, pes_sikihendo。self_a072（class a072 の skill2）は fkey self_summon で pes_sikihendo（2 > 1）に負けて消える。
  - movetype `wheel`、consti は class a072 の値（sw 7, pl 3 …）。
  - tnok は talent = on なので notalent は掛からない。部隊のリーダー自身・配下なしとすると、c_cv1（type 1、direct、yorozu attack*50 / defense*25 / magic*50 / move*10）が効き、attack 928 / defense 663 / magic 592 / move 240、attack_max 1206。type 2 の ps_* は def+0x78 / +0x94 次第（**V**）。
- **クラウド**: py_compile OK、peer テスト **157件 OK**。全体 390件中 23件 ERROR（他担当・素材なし。§22/§23 と同じ23件）。
- **PC**: テスト実行と git status は **BLOCKED**（PC のシェルなし。迂回しない）。原作実機との比較 **0件**。

### 24.8 残りの未確定と次の対象（優先順）
1. **member の def 生成**（0x466F60 の再帰、def+0xD4）: rand() の消費順と、`a072 * 7` のような項目の解釈（builder 0x508AA0 の `*` 処理）。リーダーの周2（配下の技能）の入力。
2. def+0x78 / def+0x94 の意味と writer（0x460C76、0x46FD8A など）: type 2 技能を自分に適用するかどうか。
3. 0x46F4C0（context の整数）: `unit_status_hp`、`notalent_down`、`unit_summon_min`。0x463CA0（`@mode_sdown`）。
4. srand のタイミング（乱数レーン）: skill2 の無作為選択を実機と一致させるために必要。
5. 0x586320 / 0x469390（class 変更時の追加処理）、0x590300 / 0x416D60 などの STL 断片の確認、builder ごとの `*` 分割（0x507F60 / 0x506AD0 / 0x508AA0 / 0x509E10）。

<a id="f-25"></a>
## 25. member の def 再帰生成（0x466F60）と rand() の消費順、context の整数、def+0x78/+0x94、srand
**結論**:
- def を1つ作るたびに、rand() は次の順で消費される: (1) class の `skill2` の並べ替え（候補数−1回）、(2) **`enable` の1回（ほぼ常に）**、(3) member の def（各自が (1)(2)）、(4) class 変更・learn による作り直しの並べ替え。
- member は `名前*N` で **N 体**作られる。
- 乱数のシードは場面ごとに **GetTickCount** で入れ直される。そのため DAT だけでは原作の無作為な結果は再現できない（実機の値はセーブから読むしかない）。

分類: **C** = CONFIRMED（x86）、**S** = STATIC-HIGH、**V** = VERIFY。

### 25.1 0x466F60（**C**）
引数は ECX = ctx、スタック = (名前, レベル補正オブジェクト, member フラグ)。
1. スクリプト変数 `@cln_名前` を読む（0x41DF20 で連結 → 0x463CA0）。値を v とする。
2. v == 0 で、その名前が unit タグとして存在すれば、def 名 = 名前。そうでなければ `名前+v`（_itoa 10進、0x5D1779）。class にしかない名前は最初から `+0` になる。
3. `@cln_名前` = v + 1（0x4637A0）。
4. def（0x1D4 バイト、0x582AA0）を作り、0x582D90(def, def 名, フラグ) を呼ぶ。ECX はレベル補正オブジェクト。
5. 戻ってから、ctx+0x2FC の map に (def 名 → def) を insert する（0x4671B3、上書きしない）。def+0 は def 名そのもの（0x582DFD）。
- 0x467DE0 = ctx+0x2FC を**名前の完全一致**で探す。

### 25.2 0x582D90 での member と rand()（**C**）
- 0x582D90 から呼ばれうる関数を全部たどって rand()（0x5B6EAB）の呼出しを探した。0x466F60 の再帰を除くと、次の3箇所だけだった。
  1. 0x58C0E0 → random_shuffle 0x501CA0（class の skill2）
  2. **0x583344 enable**: def+0xCC = `enable`。`enable_max ≥ enable` なら `enable + ftol(rand()×(1/32768)×(enable_max−enable+1))`（0x58333A..0x58336B）。両方とも未指定（0, 0）でも条件を満たすので、**def 1つにつき必ず1回** rand() を使う。getter は 0x585890（unit 連鎖のみ、`@シナリオ` 版優先）。
  3. 0x58AFA0 → class 変更時の 0x586320（friend の再構築、random_shuffle 0x479A30）。新しい class 自身の宣言に `friend@シナリオ` / `friend` がある場合だけ（0x469390）。**移植していない**: 該当したら例外を出す。
- **member**（引数フラグが立っているとき、0x5833AF..0x583561）:
  - リスト = unit の `member@シナリオ` / `member`（unit 連鎖）。無ければ class の同じキー（0x469460）。
  - 各項目について: 同じ名前の def が既にあって +0x77 か +0x75（talent on）が立っていれば作らない。それ以外は 0x466F60(項目, 同じレベル補正オブジェクト, フラグ 0) で作る。member の member は作られない。
  - def+0xD4 には member の **def 名**（`a072+3` など）が入る。§23 の周2 はこの名前で def を引く。
- **リスト builder 0x508AA0**（member / merce / add2 / next2 / next3 / just_next / monster / sound / item / castle_guard）: `名前 * N` は同じ項目を N 回入れる（N ≤ 0 なら入れない。`*` の後が数値でなければ読込みエラー、0x508D17..0x508E38 / 0x509215）。`*` は字句の文字列 0x65DBEC（0x6021B7 で初期化）。
- `*` は builder によって意味が違う。0x507F60（consti / yorozu / icon など）と 0x506AD0（change / fkey など）では `名前*N` の N を int に入れる（0x508349 / 0x506E8E、**C**）。0x507730（skill / skill2 / learn / multi）と 0x509E10（delskill など）は `*` を特別扱いしない（定数 0x65DBEC を参照しない）。
- rand() の順番は、作る順に深さ優先になる（親の skill2 → 親の enable → member ごとに skill2 → enable → 親の 0x58AFA0）。

### 25.3 context の整数（0x46F4C0、**C**）
- 関数内 static の map（0xB06A18）でキャッシュする。初めて読むキーは `Prop_LookupBlock("context", タグ "context", key, 0)` の**先頭項目の整数**、無ければ既定値。最初に読んだ値をプロセス終了まで使う。
- 実データ（context.dat）: `unit_status_hp = 100`、`notalent_down = 100`、`unit_summon_min = 0`。
  - **notalent_down = 100 なので、この版では notalent 補正は実際には掛からない**（§23.4 の係数 = 1.0）。
  - unit_status_hp は 100 で確定した（§22 の大域 0x65BCFC）。
- 移植コードは context ブロックの「キー = 項目, …」を行単位で読む（**S**: 本来の読込みは builder 0x508AA0、タグ名 "context" も **S**）。

### 25.4 def+0x78 / def+0x94
- **C**: 0x585CC0（+0x78 ≠ 0 または +0x94 ≠ 0）を使うのは addUnit（0x4A8F00 → 0x4A90A6）など。ここで真なら、その def の member リスト（def+0xD4）に Unit を追加する。つまり「**部隊を率いる def**」かどうかの判定。
- **C**: def+0x78 = 1 を書くのは 0x460940（`neutral_max` / `neutral_min` / `neutral_member_*` / `monster_level` を使う中立・モンスター部隊の生成。0x460C76）。
- **V**: def+0x94 の書き手は、コンストラクタ（0 を書く、0x582AFE）以外まだ特定できていない（+0x94 は他の構造体でも頻出する）。
- §23 の type 2 技能は、この判定が真の def（中立部隊のリーダーなど）にだけ自分にも掛かる。tnok を普通に作った場合は偽（type 2 は配下にだけ効く）。

### 25.5 srand の時期（**C**、CRT srand = 0x5B6E99）
- 呼出しは4箇所:
  - 0x4B7907（0x4B78C0 ← 0x555AD0）
  - 0x4C20B7（0x4C1FC0 ← GameManager::vf01 などの場面初期化 0x48AD30 / 0x48B4A0 / 0x48BC70 / 0x48BF60 / 0x48C880 / 0x48D6A0 / 0x48EA60）
  - 0x50139E（0x5001B0、`stage/…map` の読込み）
- 3箇所は `srand(GetTickCount())`。0x500315 だけは、マップの値（+0x30）が 0 でなければそれを種にする。
- このため **def 生成の無作為な結果（skill2 と enable）は、実機の種を記録しない限り一致しない**。互換の方針は次のとおり。
  - 新エンジンでは独自の種で同じ手順を回す。
  - 既存のセーブでは、保存された技能リストや enable を正とする。
- 詳しい消費順は乱数レーン（T031）の資料と突き合わせが必要（**V**）。

### 25.6 実装・テスト
- 追加・修正した関数:
  - `create_definition`（0x466F60 + 0x582D90 の順。map への登録は最後）
  - `NativeDefWorld`（ctx+0x2FC、`@cln_` カウンタ）、`member_skill_lists`
  - `NativeContextInts` / `load_context_lists`
  - リスト builder 0x508AA0 の `*N` 展開
  - class 変更先が自身の宣言に friend を持つ場合は例外
- テスト: 40件 → **47件**（合成6件、実データ1件）。
  - 合成: `*N` と名前の付け方、カウンタの継続、talent 付きの既存 def は作らない、自分自身を member にした場合（登録前なので作られる）、rand() の順番と回数、enable の範囲、周2の入力、context のキャッシュ。
- **tnok（静的予測、Golden ではない）**:
  - class c_tnok の `member = a072*7` で、member は `a072+0` 〜 `a072+6` の7体。
  - rand() は8回（enable×8、並べ替えなし）。
  - 配下の技能に type 3 は無い。
  - 結果（部隊リーダーとして）: attack 928 / attack_max 1206 / summon_max 0（`unit_summon_min = 0`）。
- **クラウド**: py_compile OK、peer テスト **164件 OK**。全体 397件中 23件 ERROR（他担当・素材なし、これまでと同じ23件）。
- **PC**: テスト実行と git status は **BLOCKED**。原作実機との比較 **0件**。

### 25.7 次の対象
1. def+0x94 の書き手（セーブの def 読込みと、スクリプトの部隊系命令から探す）。
2. 実際の呼出し元（シナリオ開始 / addUnit / 雇用 / 中立生成 0x460940）ごとの member フラグとレベル補正オブジェクト。0x460940 は member 数自体も rand() で決める。
3. 0x586320（friend / friend_ex）と 0x479A30 の移植: class 変更時の rand() 消費。
4. 乱数レーンとの照合: 起動から最初の def 生成までの rand() 消費と、種を記録する方法。

<a id="f-26"></a>
## 26. def+0x78 / def+0x94 の正体 — 「独立部隊のリーダー」判定（フェーズ1）
**結論（C）**: def+0x94 は単独のフラグではなかった。**def+0x84 にある std::string（在野・放浪先のスポット名）の長さ**である。根拠はコンストラクタ 0x582AA0（0x582AF8..0x582B04: +0x98 = 容量 0xF、+0x94 = 長さ 0、+0x84 先頭 = 0）。
- 0x585CC0（`+0x78 ≠ 0 || +0x94 ≠ 0`）の意味は「**中立部隊のリーダー、または放浪中（在野）の def**」＝勢力に属さず自分の部隊を率いる def。

| 項目 | 内容（VA） |
|---|---|
| def+0x78（byte） | 中立部隊リーダー。0x460940 が 1（0x460C76）。そのほか 0x435095 / 0x478C3F / 0x494510（0 も書く 0x4945DD）/ 0x4A9609 / 0x4A9ABE / 0x4A9D68 / 0x4AA7E0 / 0x4B49FC / 0x4F98BE / 0x4F9D66 / 0x4FE404 / 0x597627 が 1 を書く（def 取得直後の書込みをデータフローで検出）。セーブ対象（writer 0x58F060）。 |
| def+0x84 / +0x94 | 放浪先スポット名。**書込み**: 0x460E90（放浪させる。0x460ED4 で代入、ctx+0x32C の集合へ追加）、0x461DA0（乱数でスポットを選んで代入 0x4620B9 / 0x4620DD、0x40ED80 を使う）、def のコピー（0x4664F6 / 0x466C84）、0x47D99F。**消去**: 0x460F10（集合から外して空文字列にする）、0x461090。セーブ対象（0x58F097、0x470830）。 |
| 0x460E90 | +0x77..+0x7A を 0 にする（**中立フラグ +0x78 も消える**）。+0xBC = 0、+0xC0 = 100、+0x80 = 0、+0xE4 = 0x18、0x583830（**V**）。 |
| 読み手 | addUnit（0x4A90A6: 対象 def が独立リーダーなら、その def の member リストへ追加。上限は [0x65C118]−1）、eraseUnit（0x4A9505: +0x94 ≠ 0 なら放浪集合から外す）、roamUnit（0x4A9A08）、0x44FE44、0x45EF77、0x47D98A、0x4B18C0、0x55E25A。 |

- §23 の type 2 status 技能が自分にも掛かる条件は、この判定が真の def（中立リーダー・放浪者）のときだけ。勢力所属の通常 Unit には掛からない。
- 実装: `def_leads_independent_troop`、`roam_definition`（0x460E90）、`unroam_definition`（0x460F10）。`NativeDefinition` に `neutral_78`、`roam_spot`（+0x84）、`from_save` を追加し、`NativeDefWorld.roaming`（ctx+0x32C）を追加した。
- 未確定（**V**）: +0x79 / +0x7A の意味、0x583830、0x461DA0 の乱数（0x40ED80 は乱数レーン T031 の範囲）。

<a id="f-27"></a>
## 27. Unit 生成の21入口と中立部隊生成（フェーズ2）
0x466F60 の引数は（名前, レベル補正オブジェクト, member フラグ）で、フラグを先に push する。`UNIT_CREATION_ENTRIES` に全21箇所を収録した。

| VA | 呼出元 | 経路 | フラグ | レベル補正 | 確信度 |
|---|---|---|---|---|---|
| 0x45D295 | 0x45BE10 | シナリオ開始: 放浪 Unit（roam / no_home） | eax | 0xAB42F8（base_level） | S |
| 0x45D6A4 | 0x45BE10 | シナリオ開始: 勢力 Unit（power / member / talent） | 0 | 0xAB42F8 | C |
| 0x460C57 | 0x460940 | 中立部隊リーダー | 0 | 0（後で monster_level） | C |
| 0x460CE0 | 0x460940 | 中立部隊の配下（同名） | 0 | 0（同上） | C |
| 0x466910 | 0x4667B0 | fkey / class 系の生成 | 0 | 0 | S |
| 0x467579 | 0x4673B0 | member 付き生成 | 1 | 0（eax） | V |
| 0x478C34 | 0x4780D0 | 雇用（price） | 0 | obj [esp+0x28] | S |
| 0x4795C1 | 0x478F50 | 傭兵雇用（class / merce / price） | 0 | obj（ecx） | S |
| 0x47D448 | 0x47CE80 | 傭兵（merce / price） | edi | 0xAB42F8 | S |
| 0x4A92B6 | addUnit | スクリプト addUnit | eax（対象あり） | 0xAB42F8 | C |
| 0x4B49E2 | 0x4B4710 | スクリプト var 系 | 1 | 0 | S |
| 0x4D7C93 | MercenaryWnd::vf16 | 傭兵ウィンドウ | 0 | obj [esp+0x2c] | S |
| 0x4F98B3 | 0x4F9510 | castle_guard | 0 | obj（edx） | S |
| 0x4F9CD0 / 0x4F9D01 | 0x4F9510 | castle_guard の組 | ? | 0xAB42F8 / esi | V |
| 0x4FA1F5 / 0x4FA221 | 0x4F9510 | 戦闘の handle / red Unit | eax / ? | 0xAB42F8 / eax | V |
| 0x4FE2E3 / 0x4FE3FB | DItem::vf01 | ダンジョン道具（add_vassal / roam） | 0 | 0 | S |
| 0x583546 | 0x582D90 | def の member（§25） | 0 | 親と同じ | C |
| 0x59761A | 0x5972E0 | ダンジョン / 城の収容 Unit | 1 | 0xAB42F8 | S |

- **base_level 経路**（ECX == 0xAB42F8）は `scenario.base_level` を加算する（0x58B916..0x58B94B）。**obj 経路**は obj+0xDC を加算する。この2つは別物で、obj の型は **V**。
- **中立部隊生成 0x460940（C）**:
  - context: `neutral_max`（既定値 ctx+0xC）、`neutral_min`（0）、`neutral_member_min`（0）、`neutral_member_max`（[0x65C118]−1）。`monster_level` は scenario から読む。
  - スポットごと（ctx+0x2F0 の map 順。対象かどうかは 0x597B00(spot)+0x10 == 0 かつ spot+0x24 == 0 で、呼出側が渡す **V**）:
    - `monster@シナリオ` / `monster` リスト（`*N` で繰り返し）。
    - 部隊数 = min + ftol(rand/32768×(max−min+1))。ctx+0xC を上限とする。
    - 部隊ごと: 名前 = リスト[ftol(rand/32768×n)] → リーダー生成（フラグ 0、補正 0）→ monster_level > 0 なら 0x58B7F0（そのレベルで能力値を再計算）と 0x58AFA0 → +0x78 = 1。
    - 配下数 = 下限 + ftol(rand/32768×幅)。配下は**リーダーと同じ名前**で作り、同じく再レベル化してリーダーの +0xD4 に追加する。
  - **rand() の順**: 部隊数 → [選択 → リーダー生成（skill2, enable）→ 再レベル化の 0x58AFA0 → 配下数 → 配下ごとに（skill2, enable, 0x58AFA0）]×部隊数。
- 実装: `UNIT_CREATION_ENTRIES`、`create_for_entry`（VERIFY の行・入力が足りない行は拒否）、`generate_neutral_troops`、`relevel_definition`、`scenario_base_level`。
- **実データ**: context は `neutral_min = neutral_max = 4`、`neutral_member_min = neutral_member_max = 7`。spot `dr519` で部隊3（ctx+0xC = 3 で上限）、各配下7、rand 31回（seed 42 の合成シード）。

<a id="f-28"></a>
## 28. class 変更・成長（フェーズ3）
- **changeClass（0x4AB55E、C）**: def+0x54 = class → 0x58C0E0(def, 0)。現在の技能リストを S として作り直すので、skill2 は新しい技能を優先して**再抽選**し、rand() を使う。consti / movetype も作り直し、class 自身の宣言の能力値で下限を取る。0x58B7F0（能力値の作り直し）も friend の再構築も**行わない**。changeRace（0x4AB629）も同じ（def+0x38 = race）。
- **レベル到達による class 変更（0x58AFA0、C）**: 同じ 0x58C0E0(def, 0) に加えて、新 class 自身の宣言に `friend@シナリオ` / `friend` があれば 0x586320（friend 集合の再構築、random_shuffle 0x479A30）。**未移植**のため例外を出す（§25 の方針を維持）。
- **レベルアップ（0x575110、Unit の vtable メソッド。Person::vf05 0x514C62 / Player::vf05 0x5200E2 から呼ばれる、C）**:
  - 実行条件: Unit+0x8C == 0、部隊あり（+0x1D0）、Unit+0x18614 == 0。
  - exp ≥ next（符号なし）の間、次を繰り返す。
    - level_max（0x585AD0、0 なら context `unit_level_max`、既定値 100）以上なら終了。
    - level+1。
    - 能力値ごとに「`名前Up`、無ければ ceil(multi×基本値)」を**加算**し、`名前Max` で頭打ち。
    - 0x58AFA0（class 変更・learn・delskill2）→ 0x58A400（exp 計算、**未移植**: exp / next は呼出側が渡す）。
  - 毎回頭打ちするため、負の成長があると作成時の式（§22）と結果が変わる（テストで確認）。**作成時とは別の関数**として実装した。
  - rand() は 0x58AFA0 の作り直しでだけ使う。
  - **V**: Unit の現在値を再計算するか（0x576660 は仮想関数呼出しのみ）。
- 保持の規則: セーブから復元した def（`from_save`）は作り直さない（map への登録は上書きしない）。changeClass やレベルアップはゲーム内の出来事なので適用する。
- 実装: `change_class_script`、`change_race_script`、`level_up_definition`。

<a id="f-29"></a>
## 29. 乱数と統合試験（フェーズ4・5）
- **srand（0x5B6E99、C）の4箇所**（`SRAND_SITES`）:
  - 0x4B7907（0x4B78C0 ← 0x555AD0）: GetTickCount
  - 0x4C20B7（0x4C1FC0 ← GameManager の場面初期化 7関数）: GetTickCount
  - 0x500315（マップ読込み 0x5001B0）: マップの種（+0x30）が 0 でなければそれ
  - 0x50139E（同じマップ読込み）: GetTickCount
  - 乱数レーン（A / T031、IN_PROGRESS）の「起動・中央リセット（ロード含む）・マップ固有の種・マップ終了で入れ直す」と一致する。T031 の資料は読取だけ。
- **同じ種での再現**: def 生成・中立生成・class 変更・レベルアップのすべての rand() 消費を `LegacyRng` 1本でつないだ。同じ種・同じ入力なら同じ結果になる（試験済み）。
- **実機と一致させるのに足りないもの**:
  1. その時点の CRT 乱数状態（GetTickCount 由来の種と、それ以降の他の消費）
  2. 生成の呼出し順（シナリオ開始の Unit 配置順、スポットの順）
  3. 0x461DA0 などの他の乱数消費
  4. ロード後は入れ直されるので、セーブを挟んだ流れは連続しない。
  - 固定の種で再現できることと、原作の実際のプレイを再現できることは**別**。
- **テスト区分**（`test_peer_script01_native_definitions.py`、54件）:
  - SYNTHETIC: 合成 DAT に対する単体試験
  - ACTUAL / STATIC: 原作 DAT から静的に計算
  - GOLDEN / MATCH: **0件**
- **実データの結果（STATIC、Golden ではない）**:
  - **tnok はシナリオで変わる**。unit:base に `member@rsc = @` があるため、シナリオ rsc では member **0体**。前回の「member 7体・rand 8回」は**シナリオ名が空のとき**の結果（前回の条件付き予測）。
  - attack 928 / attack_max 1206 は、member の有無に関係なく変わらない（配下に type 3 技能がないため）。
  - 独立リーダーとして作った tnok（+0x78 が立つ）は、type 2 の ps_* が自分にも掛かり、hp 38190 / attack 1021（(878+50)×1.1）。
  - 無作為な skill2 を持つ class（hayakuchi2、候補4）: rand 3+1 回。選ばれる技能を LCG から独立に計算して照合した。
  - レベルで class が変わる Unit（yatai_k1: Lv15 で a022 → a0222）。
  - 同名 Unit の2体目は `tnok+1`。member の member は作られない（深さ1で止まる）。
- **クラウド**: peer テスト **171件 OK**。全体 404件中 23件 ERROR（他担当・素材なし、これまでと同じ23件）。**PC**: テスト実行と git status は **BLOCKED**。

### 次の対象（優先順）
1. 0x586320 / 0x479A30（friend / friend_ex の再構築）を移植し、レベル到達の class 変更で例外にしないようにする。
2. obj+0xDC の型（雇用・城・傭兵の入口）と、VERIFY の入口4組の引数。
3. 0x58A400 / 0x58A540（exp / next）と、レベルアップ後の Unit 現在値の扱い（0x576660）。
4. 0x45BE10（シナリオ開始の配置順）と 0x461DA0（放浪先の乱数）。乱数レーンとの照合。

<a id="f-30"></a>
## §30 friend / friend_ex（def+0x158）— 0x586320 / 0x469390 / 0x479A30

| VA | 内容 | 分類 |
|---|---|---|
| 0x586320 | friend集合の遅延生成。def+0x160(size)≠0なら複写して返す（乱数0）。空なら毎回再生成 | CONFIRMED |
| 0x586320 手順1 | unit鎖(def+0x1C)に friend@scen/friend があれば unit所有、なければ class(def+0x54) の friend（has判定なし、無ければ空） | CONFIRMED |
| 0x4694E0→0x465770 | key@scen優先→key、最寄り宣言のstd::set（0x509E10ビルダー、重複除去・バイト順） | CONFIRMED（集合化はSTATIC-HIGH） |
| 0x5865A8..0x58685C | friendが空の時のみ friend_ex（unit→class）。数値項目kで区切り、k=0の間の名前は固定、以降は候補集合。候補を集合順でベクタ化→0x479A30→先頭k個→固定と合併。friend_num/appendは読まない | CONFIRMED |
| 0x5867CD..0x5867F6 | k>候補数 または k<0 は 0x415A60 破棄ループが end を越えて開始＝未定義動作 → 実装は拒否（NativeUndefinedBehaviour） | CONFIRMED |
| 0x586872..0x586A1C | friend非空: 所有kindの friend_num（0x4693F0 @scen優先）が 0<num<|S| なら shuffle→先頭num個。friend_append(text)が非空なら追加 | CONFIRMED |
| 0x479A30 | std::random_shuffle（0x1C文字列）。i=1..n-1で rand()%(i+1)、n≤32767で LegacyRng.shuffle_forward と同一。乱数消費 n−1 | CONFIRMED |
| 0x469390 / 0x58B09E | Lv由来のclass変更（0x58AFA0）で、0x58C0E0 の**後**に新classの**自宣言**に friend@scen/friend があれば def+0x158 をクリアして 0x586320 | CONFIRMED |
| changeClass/changeRace (0x4AB55E/0x4AB629) | 0x58C0E0のみ。friend再生成なし（集合保持） | CONFIRMED |
| addFriend/eraseFriend op0x31 (0x4ACA7A..) | 対象ごとに先に0x586320（空なら生成）。eraseFriendで対象のみ→集合クリア（次回再生成）。それ以外は追加/削除 | STATIC-HIGH（擬似C＋call site） |

- 呼出元: 0x58AFA0 / 0x586AB0（雇用・友好判定。UI 0x41C510、MercenaryWnd等）/ 0x589230（CharaWnd等の情報表示）/ 0x4ACB1A。**UIを開くだけで初回生成の rand() が起こり得る**ため、実機の乱数位置はUI操作依存（ACTUAL: VERIFY）。
- 実装: `class_has_own_friend`, `rebuild_friend_set`, `friend_set`（遅延生成・保持）, `friend_script`, `NativeSkillState.friends`。`apply_class_change_and_learn` の NotImplementedError を削除（全条件の根拠あり）。
- 原作DAT（STATIC）: friend_ex / friend_num / friend_append は0件 → 実データの friend 生成は乱数0。tnok friend 23件。own friend を持つ変更先class（c_boss_web_2/3, a2013, a2152, a2153 等）は再生成されるが乱数消費なし。
- テスト: SYNTHETIC 8件＋ACTUAL 1件追加（計63件 OK）。GOLDEN 0 / MATCH 0 のまま。
- 残VERIFY: 0x507730 の数値項目判定の厳密なトークン化、friend_append が複数値の時の text 結合。

<a id="f-31"></a>
## §31 経験値と複数レベルアップ — 0x58A540 / 0x58A400 / 0x58A650 / 0x575110 / 0x576660

| VA | 内容 | 分類 |
|---|---|---|
| 0x582C56..66 | ctor: level=1, exp(+0x16C)=0, next(+0x170)=0 | CONFIRMED |
| 0x58C022/0x58C029 | 0x58B7F0末尾で exp=0x58A540, next=0x58A400（Lv由来class変更より前のclassで計算） | CONFIRMED |
| 0x58A540 | 符号付き: s=0,e=exp; i=1..level-1: s+=e; e=_ftol2(e*mul)（mul=exp_mul*0.01 qword、53bit積、切捨て、範囲外INT32_MIN）; exp_max≠0 かつ e>exp_max(符号付き)→cap | CONFIRMED |
| 0x58A400 | 符号なし: nxt=e, prev=0; (level-1)回: prev+=e; e=low32(FISTP qword chop(u32(e)*mul)); cap(符号なし); nxt+=e（0xFFFFFFFFで飽和）。next=nxt。nxt≤旧next かつ exp>prev なら exp=prev | CONFIRMED |
| 0x58A650 | def単体のLvUpループ（Hit_LinkedAward 0x551FD3、world命令 0x4AB49B、0x4723DE）。while exp≥next(符号なし): level_max判定→level++→成長+Max→0x58AFA0→0x58A400 | CONFIRMED |
| 0x575110 | Unit版。成長部 0x575203..0x575932 と 0x58A72D..0x58AE62 は命令数同一・call/定数列同一（md5一致） | CONFIRMED（同等性はSTATIC-HIGH） |
| 0x575110 ゲート | Unit+0x8C≠0→即return（0x576660なし）。+0x1D0==0 または +0x18614≠0 → ループなしで 0x576660(1)。終了時 +0x186C0/C4/C8/CC=0x80000008, +0x186BC=0 | CONFIRMED |
| 0x576660 | Unitリスト+0x186B0のクリア（引数1=全消去/0=先頭1件）と表示・動作状態(+0x5B0オブジェクト、+0x5F0..+0x5FC)のリセットのみ | CONFIRMED |

- **Unit現在値**: 0x575110/0x576660 は Unit +0x90..+0x12C（能力・最大値）も現在HP/MPも書かない。LvUp後のUnit再導出箇所は未特定 → VERIFY。HP比率維持等の仮実装はしていない。
- 実装: `exp_for_level`, `update_exp_next`, `init_definition_exp`（create/relevel で呼出）, `level_up_loop`（任意段数）, `unit_level_up`（ゲート）, `NativeDefinition.exp/exp_next`。既存 `level_up_definition` は1段分の本体として維持。
- 乱数: LvUpループ自体は rand 0。各段の 0x58AFA0（skill2抽選・friend再生成）だけが消費。
- ACTUAL(STATIC): tnok exp=275/mul=120/max=0 → Lv5 exp 1476 / next 2046、+600で Lv6・next 2730・rand 0。rsc は exp系キー全0 → exp=next=0 で、ループが走れば level_max(既定100)まで上がる静的帰結（実機でrscがループ対象になるかは VERIFY）。
- x87精度: 53bit（_PC_53）前提。Direct3D初期化で精度が24bitに変わる可能性は未検証（VERIFY）。
- テスト: SYNTHETIC 6件＋ACTUAL 1件（計70件 OK）。GOLDEN 0 / MATCH 0。

<a id="f-32"></a>
## §32 残VERIFY生成入口 — 0x467579 / 0x4F9CD0 / 0x4F9D01 / 0x4FA1F5 / 0x4FA221

| 呼出VA | 引数（asm） | 所有者・条件 | 分類 |
|---|---|---|---|
| 0x467579 | flag=1（push 1）、level obj=EAX=0（直前 test eax,eax で0確定） | 0x4673B0（addPower op6 0x4A8B53、シナリオ開始 0x45BE10×2）。Power（ctor 0x590560）+0x24 の名前が 0x467DE0 で見つからない時のみ生成。生成後 Power+0x1C=0、0x593550 | CONFIRMED（+0x24が盟主名である点はSTATIC-HIGH） |
| 0x4F9CD0 | flag=ESI=0（0x4F9BDA xor以後不変）、obj=0xAB42F8 | 0x4F9510 第2スタック引数 L<0 の分岐（0x4F9C9B） | CONFIRMED |
| 0x4F9D01 | flag=0、obj=ESI=NULL | L≥0。生成後 L'=0x585AD0(def,"level")+L（int32）、0x58B7F0(ECX=0,def,L')、0x58AFA0 | CONFIRMED |
| 0x4FA1F5 | flag=EAX=0、obj=0xAB42F8 | 同関数 handle/red 側、L<0（0x4FA1CA） | CONFIRMED |
| 0x4FA221 | flag=0、obj=NULL | L≥0 → 0x4FA226..0x4FA264 で同じ relevel | CONFIRMED |

- 既存defがあり +0x77 または +0x75 の場合は生成せず再利用（0x4F9C59..0x4F9C8B）。
- 0x4F98B3 の level obj は [this(ECX)+0x14]（0x4F95CF）。this の型と寿命は未特定 → STATIC-HIGHのまま、+0xDC の値は呼出側必須引数（黙って既定値にしない）。0x478C34 / 0x4795C1 / 0x4D7C93 も同様に `object_dc` 必須。
- 実装: `create_for_entry(..., level_arg=)`。L必須・分岐の符号不一致は ValueError。relevel 分岐は `relevel_definition`（exp/next も再計算）。
- テスト: SYNTHETIC 3件（計73件 OK）。

<a id="f-33"></a>
## §33 シナリオ開始順と放浪RNG — 0x45BE10 / 0x40ED80 / 0x461DA0

- 生成順（call siteはCONFIRMED、全体順はSTATIC-HIGH）: ①scenario spot ②scenario power 順に 0x4673B0（盟主 0x467579, flag1, 加算なし）③diplo/league/enemy_power ④代替spotベクタ（ctx+0x2F0 map順、0x597A20 no_home / 0x597770 / 0x592260(0x597B00) で除外）⑤scenario roam 順: 既存defはskip、無ければ 0x45D295 生成（flag0, base_level）→初期spot→そのunitのmember群 0x45D6A4（flag0, base_level, arbeit/talent判定）→0x460E90 ⑥0x46E650、0x4673B0 2回目（0x45D7E7）、item_sale。
- **表の訂正**: 0x45D6A4 は「勢力ユニット」ではなく「各roamユニットのmember」。0x45D295 の flag は EAX=0（直前 test eax で0確定）→ CONFIRMED。
- 0x45D2AD..0x45D40C 初期spot（CONFIRMED）: home = 0x469460(unit, def+0x1C, "home")。非空なら 0x501CA0 shuffle（n−1 rand）→ 0x467E90 で解決できる最初の名前。全滅/空なら代替ベクタから ftol(rand/32768*n)（1 rand）。代替も空なら 0x463590 で配置なし。
- 0x40ED80（CONFIRMED）: lo + _ftol2(rand*(1/32768)*(hi−lo))、1 rand。0x461DA0（月次の放浪移動、0x471E80 のみから）では home 判定後 0x467F40 の +0x128 ベクタ（0x1C文字列）から 0x40ED80(n,0) で1個選択（STATIC-HIGH）。0x461DA0 全体の移植は未着手（VERIFY）。
- 乱数共有: CRT rand は単一状態（スレッド毎 ptd+0x14）。雇用・中立生成・放浪・friend・skill2 は全て同じ列を消費（T031 lane A の `LegacyRng` を読取専用で使用、変更なし）。
- 同一seed再現性（SYNTHETIC）は保証。実機は srand(GetTickCount()) (0x4B7907/0x4C20B7/0x50139E) のため ACTUAL の列は実行毎に異なる → 実機一致は未検証（MATCH 0）。
- 実装: `SCENARIO_START_ORDER`, `rand_between_40ed80`, `roam_start_spot`。テスト SYNTHETIC 4件。

<a id="f-34"></a>
## §34 原作DAT統合テスト（今回バッチ）

| 項目 | 結果 | 区分 |
|---|---|---|
| tnok シナリオ"" | member 7 / rand 8（seed 1, 12345 とも）— 変化なし | STATIC |
| rsc | member 0 / rand 1 — 変化なし | STATIC |
| friend遅延生成 | tnok 23件、rand 0（原作DATに friend_ex/num/append 無し） | STATIC |
| friend保持/再生成 | 非空は保持、空（eraseFriend後）は再生成 | SYNTHETIC規則＋ACTUAL入力 |
| 複数LvUp | tnok exp+600 → Lv6 next 2730、seed777で+5000 → 5段、rand 0 | STATIC |
| VERIFY入口 | 0x4F9D01 tnok L=2 → level欄+2 | STATIC |
| 同一seed再現 | 生成→LvUp→skill列が一致 | SYNTHETIC |
| sci1 roam | ikeda → home@sci1 で sp44、rand 0 | STATIC |

- baseline に変化が無い理由: friendは遅延生成で生成時に呼ばれず、exp計算は rand を使わないため。
- 件数: 本テストファイル 82件 OK（前回54→+28）。全体 432件中 23件は従来どおり環境依存エラー（PC未再検証）。
- GOLDEN 0 / MATCH 0（実機比較なし）。セーブ由来defの friend 保存有無は未調査（VERIFY）。

<a id="f-35"></a>
## §35 戦闘中のEXP獲得 — Hit_LinkedAward 0x551E50

観測（OBS、実装根拠にはしない）: 画像A=KMR Lv20 EXP 95371/87716（戦闘中、Lv不変）、画像B=田所 Lv21 EXP 74942/93637（戦略画面）。別ユニットのため前後比較ではない。

| 項目 | 内容 | 分類 |
|---|---|---|
| 呼出元 | Damage_Core 0x551167、Heal_NegativeAmount 0x551C6A、0x547A8C、0x57F4E9 | CONFIRMED |
| 停止条件 | skill+0x2A8 == −123456.0（exp_per=off）、Unit+0x1D0==NULL、Unit+0x18614≠0、record+0xC≠0（付与後1にする） | CONFIRMED |
| skill+0x2A8 | 0x59BD42..0x59BE56: exp_per=off→−123456.0、on→1.0、それ以外 int×0.01（無指定 0.0） | CONFIRMED |
| 係数f | 種別(skill+0x40, 表0x55201C): 3→0.02、4→0.01、5→clamp(r,0.01,0.2)、その他→clamp(r,0.01,0.33)。r=a/b（b=0なら0.0） | CONFIRMED |
| 基本値 | e=_ftol2(ceil(f×target Unit+0x185FC)) | CONFIRMED |
| exp_per≠0 | e=_ftol2(e×exp_per+0.5)（下限なし） | CONFIRMED |
| exp_per=0 | x=e; (+0x44 または +0x4C>0)→10; +0x74>0 かつ 種別≠1 → x/+0x74（idiv）; 10未満→10 | CONFIRMED |
| 保存先 | **def+0x16C**（Unit+0x1C8のdef）。Unitには保持しない | CONFIRMED |
| 直後のLvUp | Unit+0x8C≠0（SimpleUnit/SimpleStaticUnit）かつ exp≥next の時だけ 0x58A650＋"t_levelup"/"levelup" | CONFIRMED |


> 原本1043〜1045行は部分回収の対象外（held_native_paragraph）。


<a id="f-36"></a>
## §36 レベルアップ発火タイミング

| 時点 | 経路 | 分類 |
|---|---|---|
| 戦闘中の命中/撃破 | 0x551E50: EXP加算のみ（SimpleUnitだけ即LvUp） | CONFIRMED |
| 勝敗成立 | BattleEvent_FrameDriver 0x492D80 が 0x514C80 等で判定 → 0x493630(gm,1/0)（0x49303A/0x493082/0x4930A1） | CONFIRMED（条件の意味はSTATIC-HIGH） |
| 戦闘終了処理 | 0x493630: GM+0x1EEC3C==2（戦闘モード、0x492890で設定）なら 3陣営 GM+0x1E8630/+0x1E8634/+0x1E8638 の vf05 をこの順で呼び、その後 0x4C21F0 | CONFIRMED |
| vf05 | Person/Enemy 0x514C50、Player 0x5200A0（先に+0x470=+0x46C）: Unitベクタ +0x48..+0x4C の順に 0x575110 | CONFIRMED |
| 他の終了経路 | BattleWnd::vf01 0x40E2B9、Script_DispatchCommand 0x4A1764 も 0x493630。0x49B5C0（FrameDriverで GM+0x1EED18≠0 の時 0x49B280 経由）はモード判定なしで同じ3呼出 | CONFIRMED |
| 勝ち/負け | 0x493630 の結果フラグは LvUp ブロックを左右しない → 勝敗・退却で同じ | CONFIRMED（退却/時間切れが 0x493630 を通るかは呼出元ごとに STATIC-HIGH） |
| 戦略画面 | world op31 levelup/addLevel（0x4AB3E0..: n回 {exp=next; 0x58A650}）、0x471E80 の訓練（func==6 の技能、0x4723DE 同形） | CONFIRMED / STATIC-HIGH |

- 結論: 通常戦闘Unitのレベルアップは**戦闘終了処理 0x493630 内**で起こる。戦略画面への復帰より前に、def上で完了している。

<a id="f-37"></a>
## §37 LvUp後のUnit同期

- 0x575110 / 0x576660 は Unit 能力値（+0x90..+0x12C）も現在HP/MPも書かない（§31、CONFIRMED）。
- Unit能力値の計算 0x573BD0 の呼出元は Unit初期化 0x571B70（← 0x56F880 戦闘Unit生成、← SimpleUnit ctor 0x544290）と StaticUnit 系 ctor のみ（CONFIRMED）。→ 新しい能力値・技能が Unit に入るのは**次にUnitを生成した時**（STATIC-HIGH: 戦闘開始時の 0x56F880 呼出元 0x4F6540/0x4F84B0/0x4F9510/0x4B4710/0x4A58D4）。
- 技能（learn/skill2/friend）は 0x58AFA0 により def 上で LvUp の各段ごとに即時更新（CONFIRMED）。
- 戦闘Unitの破棄時期、戦闘後の現在HPの def への書戻しの有無: 未調査 → VERIFY（比率維持や全回復は実装していない）。
- 実装: `skill_exp_per`, `HitAwardInput`, `hit_exp_amount`, `BattleUnitState`, `hit_linked_award`, `battle_end_level_ups`, `forced_level_ups`。テスト SYNTHETIC 7件（計89件 OK）。

<a id="f-38"></a>
## §38 周辺課題（フェーズ5）

- **friend集合のセーブ**: 保存側 0x58F5D7..0x58F638 が def+0x158 の各文字列を 0x470830 で書き、区切り 0x68B3A8 / 0x68B9D0 の後に movetype、level、exp、next を書く（CONFIRMED）。読込側（0x58EEBF 付近）の対応は STATIC-HIGH。→ ロード後も非空なら保持され、0x586320 で再抽選されない。
- **x87精度**: CRT初期化で `_controlfp_s(0,0x10000,0x30000)`（_PC_53）。IDirect3D9::CreateDevice（0x559774）の BehaviorFlags=0x20（SOFTWARE_VERTEXPROCESSING）で、D3DCREATE_FPU_PRESERVE(0x2) は**無し**（CONFIRMED）。D3D9 は文書化された仕様として FPU を単精度(24bit)に変更するため、ゲーム中の x87 演算は PC24 の可能性が高い（外部仕様、実機VERIFY）。既定値はまだ53bitのまま（変更すると他レーンの期待値に影響するため、本findingのみ記録）。
- 0x461DA0 全体の移植、0x4F9510 の this 型: 未着手（次回）。

<a id="f-39"></a>
## §39 EXP表示の不一致 — 解消

| 項目 | 内容 | 分類 |
|---|---|---|
| 表示関数 | 戦闘ステータス欄 0x407300（呼出元 0x4071DA）。選択Unit [0x660F70] → def=Unit+0x1C8（0x4073AE/0x4073B3） | CONFIRMED |
| Lv | itoa(def+0x168)（0x407DFD） | CONFIRMED |
| EXP | ultoa(def+0x16C) "/" ultoa(def+0x170)（0x40856D / 0x408583）。符号なし、変換・補正・キャッシュなし、描画ごとに再読込 | CONFIRMED |
| StatusWnd 0x55BC60 | 同じく def+0x16C / +0x170 を ultoa | STATIC-HIGH |
| HP表示 | itoa(Unit+0xDC) と itoa(Unit+0x90)（0x407300 内）→ 現在HP=Unit+0xDC、最大=Unit+0x90 | STATIC-HIGH |

**原因（STATIC、観測とは別区分）**: 以前の不一致は、モデル側の前提が2点違っていたため。
1. 0x58A400 は毎回 **Lv1 から全区間を現在の class の exp_mul で再計算**する。KMR は Lv15 で c_kmr → c_kmr2（exp_mul 120→125）、田所も Lv15 で c_yaju → c_yaju2（125）に変わる。前回の検算は初期 class の120で計算していた。
2. 画面の「田所」の内部 tag は **yaju**（name=田所）で、tdn ではない。

| Unit | 内部tag/class | exp, exp_mul | 計算next | 観測 | 判定 |
|---|---|---|---|---|---|
| KMR Lv20 | kmr / c_kmr2 | 257, 125 | **87716** | 87716 | 完全一致（OBS整合） |
| 田所 Lv21 | yaju / c_yaju2 | 220, 125 | **93837** | 93637 | 1桁差。観測EXP 74942 は Lv21 区間 [74900, 93837) に収まる → 画像読取りの誤記の可能性（VERIFY：画像の再確認を依頼） |

- 生成直後の def は 0x58B7F0（next計算）→ 0x58AFA0（Lv由来のclass変更）の順なので、Lv20 で新規生成した KMR の next は**変更前 class の値（47642）のまま**。次の LvUp で 0x58A400 が125で再計算する（CONFIRMED順序）。
- GOLDEN 0 / MATCH 0（同条件の実機比較ではなく、スクリーンショットとの整合確認）。

<a id="f-40"></a>
## §40 戦闘後のUnit寿命・HP/MP引継ぎ

| 項目 | 内容 | 分類 |
|---|---|---|
| EXP / Lv / next / 技能 / friend | すべて def が所有。戦闘中の付与と戦闘終了時のLvUpは def に直接書く（§35/§36） | CONFIRMED |
| 能力値の Unit 構築 | 0x573BD0 は Unit 初期化 0x571B70（← 戦闘Unit生成 0x56F880、← SimpleUnit ctor 0x544290）と StaticUnit 系 ctor からだけ呼ばれる | CONFIRMED |
| 生成時の現在HP/MP | 0x57479B: Unit+0xDC = hp、0x5747AE: Unit+0xE0 = mp（満タンで開始） | CONFIRMED |
| セーブされる def 項目 | friend集合、level、exp、next、能力値 +0x178..+0x1A0（Unit_Serialize 0x58EFD0、読込側はセーブ版≥6で friend を読む） | CONFIRMED（疑似Cより） |
| 現在HP/MPの保存先 | def にもセーブにも**フィールドが無い** | CONFIRMED（def/セーブについて） |
| 戦闘終了時のHP補正 | 0x493630 と 0x575110 に Unit HP の書込は無い | CONFIRMED（範囲内） |
| Unit 破棄の位置 | 0x493630 内では仮想 dtor 呼出は見つからない。シーン切替側（0x49B5C0 のリスト解放など）が候補 | VERIFY |
| Troop 等、他オブジェクトでのHP保持 | 未調査 | VERIFY |


> 原本1110〜1111行は部分回収の対象外（held_native_paragraph）。


<a id="f-41"></a>
## §41 状態遷移仕様（Work 向け）

| 段階 | 所有者 | 値 | VA | 確信度 |
|---|---|---|---|---|
| 1. 戦闘Unit生成 | Unit←def | 能力値=0x573BD0(def)、HP/MP=満タン、consti/movetype=def のコピー | 0x56F880→0x571B70→0x573BD0 | CONFIRMED |
| 2. EXP獲得 | def | def.exp += e（e は §35 の式）、通常Unit は LvUp なし | 0x551E50 | CONFIRMED |
| 3. 戦闘終了 | def | GM モード2なら3陣営×Unit順に LvUp ループ。各段で成長・class変更・friend・learn・next再計算 | 0x493630→vf05→0x575110 | CONFIRMED |
| 4. Unit の後始末 | Unit | 0x576660(1)、+0x186BC..CC のリセット。能力値・HP は書かない | 0x5759CB.. | CONFIRMED |
| 5. 戦略画面 | def | 表示は def.level/exp/next の生値 | 0x407300 / 0x55BC60 | CONFIRMED / STATIC-HIGH |
| 6. セーブ/ロード | def | friend、Lv、exp、next、能力値。HP は無し | 0x58EFD0 / ローダ | CONFIRMED（疑似C） |
| 7. 次の戦闘 | Unit←def | 1 と同じ（新Lvが反映） | 同上 | STATIC-HIGH |

- 新エンジンの入出力: 入力 = def（level, exp, next, stats, skills, friends）と戦闘結果（EXP付与記録、GMモード、陣営順）。出力 = 更新後の def。Unit は戦闘ごとに def から作り直す。
- 状態異常の寿命: Unit 側にしか無いと考えられるが、保持先は未調査（VERIFY）。

<a id="f-42"></a>
## §42 検証（今回）

- 実装: `exp_display`, `DEF_SAVE_FIELDS`。
- テスト: ACTUAL データ・STATIC 結果 4件（KMR next 87716、田所=yaju と Lv21 next 93837、新規生成時は変更前 class の next、セーブ項目に HP 無し）。
- 次の解析対象: Unit 破棄の呼出位置、Troop 側の HP 保持有無、0x461DA0、0x4F9510 の this 型。

<a id="f-43"></a>
## §43 戦闘Unitの寿命

| 項目 | 内容 | 分類 |
|---|---|---|
| 戦闘Unit生成 | 0x56F880 は **Unit コンストラクタ**（0x56F8DD で vtable 0x63A9E4 を設定）。+0x1C8=def、+0x1D0=troop、+0x1CC=leader def（0x56FEAF..0x56FEE3）→ 0x571B70（0x570226）→ 0x573BD0 | CONFIRMED |
| 生成時HP/MP | 0x56F880 内の 0x571B70 以降に Unit+0xDC / +0xE0 の再設定なし。呼出元 5 範囲（0x4F6540、0x4F84B0、0x4F9510、0x4B4710、0x4A26FE）にも +0xDC/+0xE0 の書込なし → 戦闘Unitは毎回満タンで開始 | CONFIRMED（これらの生成経路について） |
| destructor | vtable slot0 0x570C90 → 本体 0x543E00 → flag&1 なら delete。SimpleUnit も同じ slot0、StaticUnit は 0x55B010 | CONFIRMED |
| dtor の書戻し | 0x543E00..0x544290 に def(+0x1C8)・troop(+0x1D0)・HP(+0xDC) へのアクセスなし → 破棄時に def へ書き戻す値は無い | CONFIRMED |
| 破棄の呼出位置 | 0x493630 / 0x49B5C0 には Unit の仮想 dtor 呼出なし。GameTask ループ 0x4C24B0（vf05 が偽なら dtor）とアプリ終了 0x5539C0 は別対象。実際の Unit 破棄位置は未特定 | VERIFY |
| 戦闘終了時の書戻し | 0x493630→vf05→0x575110/0x576660 は def の Lv/EXP/技能だけを更新（§36）。Unit の HP/MP/状態を def に写す命令は無い | CONFIRMED（確認範囲内） |
| 勝敗・退却 | LvUp ブロックは結果フラグ非依存（§36）。退却・時間切れの専用経路は未分離 | STATIC-HIGH / VERIFY |


> 原本1146〜1146行は部分回収の対象外（held_native_paragraph）。


<a id="f-44"></a>
## §44 HP/MP・状態の保持区分

| 区分 | 内容 | 根拠 | 分類 |
|---|---|---|---|
| 1. 戦闘中だけの Unit 状態 | 現在HP +0xDC、現在MP +0xE0、能力値 +0x90..（構築値）、consti/movetype コピー、行動キュー +0x186B0 等 | 0x573BD0 / 0x576660 | CONFIRMED（所在）|
| 2. 戦略画面へ引き継ぐ状態 | def の Lv・EXP・next・能力値・技能・friend | §35/§36/§40 | CONFIRMED |
| 3. Troop が持つ可能性 | Troop 側の HP 保持は未調査。ただし Unit 生成時に HP を読む命令は無い | §43 | VERIFY（HP 復元経路は見つからない）|
| 4. セーブ/ロード | def: friend・Lv・EXP・next・能力値。HP/MP 無し | §40 | CONFIRMED（疑似C）|
| 5. 次回 Unit 生成で初期化 | HP/MP=満タン、能力値・consti・movetype を def から再構築 | §43 | CONFIRMED |

- 結論（確認できた経路の範囲）: 戦闘で受けたダメージ・状態異常を次の戦闘に持ち越す命令は、Unit 生成・Unit 破棄・戦闘終了・def セーブのどこにも存在しない。「全回復の処理がある」のではなく「HP を保存・復元する経路が見つからない」という形の結論であり、Troop など未調査の構造体については VERIFY を残す。

<a id="f-45"></a>
## §45 0x4F9510 の this と level object（+0xDC）

| 項目 | 内容 | 分類 |
|---|---|---|
| 0x410B2F の呼出 | ECX=[0x8B8E58]（DemoPerson、0x447280 で生成）、EDX=[0x8B8E5C]、L=−1（push −1）→ base_level 分岐 | CONFIRMED |
| this の型 | Person 系の戦闘陣営オブジェクト（Person/Enemy/Player/DemoPerson） | STATIC-HIGH |
| level object | 0x4F95CF で this+0x14 を読む。Person ctor 0x514740 は +0x14 を設定しない（外部で設定） | VERIFY（Power と推定）|
| Power+0xDC | Power 初期化 0x590880（← 0x4673B0 0x46749D）: scenario "base_level"（0x590E9C）＋ power "base_level"（0x5914D0 = 0x4693F0("power", tag, key@scen 優先)、0x590ED3） | CONFIRMED |
| Power+0xD4 / +0xD8 | training_average / training_up | CONFIRMED |

- 実装: `power_level_object_dc(regs, scenario, power_tag)`。`create_for_entry` の `object_dc` 引数に渡せる値。addBaseLevel/setBaseLevel による後からの変更はモデル化していない。

<a id="f-46"></a>
## §46 0x461DA0（月次放浪）— 途中経過

- 0x471E80 からのみ呼ばれる。ゲート: context "roam_avoid"（既定 off）、ユニット +0x74、+0xCC、"fix"（0x585890）、"home"。home 指定ありなら 0x467F40 の +0x128 ベクタから 0x40ED80(n,0) で1つ選ぶ（§33）。全体の移植は未完了（VERIFY）。

<a id="f-47"></a>
## §47 検証（今回）

- 追加テスト: SYNTHETIC 1件（Power+0xDC の合算と scenario 版キー）。専用テスト 94件 OK。
- 次の解析対象: Unit 破棄の実際の呼出位置（シーン切替・Person の Unit ベクタ解放）、Troop 構造体の HP 保持有無、Person+0x14 の書込元、0x461DA0 の移植。

<a id="f-48"></a>
## §48 Unit 破棄経路の追跡（続き）

| 項目 | 内容 | 分類 |
|---|---|---|
| Unit vtable | Unit 0x63A9E4 / SimpleUnit 0x63A4BC: slot0=0x570C90（削除dtor）、slot5=0x431910（`mov al,1`：常に真）。StaticUnit 0x63A85C: slot0=0x55B010 | CONFIRMED |
| 削除dtor の呼出元 | 直接呼出は無く仮想のみ。疑似C全体で `(**vtbl)(1)` 形の呼出は 16 関数（GameModel::vf02 0x4BBF70、GameTask ループ 0x4C24B0、0x5539C0 ほか） | CONFIRMED（疑似Cの網羅検索） |
| GameModel::vf02 0x4BBF70 | モデルのセル配列（+0xC/+0x10）とリスト（+0x18）の全オブジェクトを、削除済み集合に登録（0x565780→0x5158E0）してから dtor(1)。呼出元は GameModel dtor 0x4BBE20 のみ | CONFIRMED |
| GameModel の寿命 | NewGameModel（vtable 0x639490）は 0x4E4830 ← 0x4B9E50 ← 0x4B78C0 ← 0x555AD0（起動時の初期化）で生成 → 戦闘ごとには破棄されない | STATIC-HIGH |
| GameTask ループ 0x4C24B0 | 各タスクの vf05 が偽なら dtor(1)。Unit の vf05 は常に真なので、仮に Unit がこの一覧に入っていてもここでは消えない | CONFIRMED（vf05 の値）/ 一覧への所属は VERIFY |
| 結論 | 戦闘ごとの Unit 解放位置は未特定。戦闘終了（0x493630）・陣営 vf05・GameModel clear のいずれでもない | VERIFY |

- Troop / Person との関係: Unit は +0x1D0 に Troop、+0x1CC に leader def、陣営（Person）は Unit ベクタ +0x48..+0x4C を持つ（§36）。Troop が HP を保持するかは今回も確認できなかった（VERIFY）。
- 勝敗・退却・時間切れによる破棄の違い: 破棄位置が未特定のため判定不能（VERIFY）。

<a id="f-49"></a>
## §49 0x461DA0 月次放浪（前半を復元、STATIC-HIGH）

ECX = ctx（0x471E80 からのみ呼出）。

1. turn = [ctx+0x2C]+0x1EF4C8（ゲーム側の経過ターン）。
2. context "roam_avoid"（0x46F6F0、既定 "off"）が "on" なら 0x484970(GM+0x1EF4B4) を事前取得。
3. ctx+0x32C の放浪 def 集合（ヘッダ +0x330）を集合順に処理。各 def について:
   - def+0x74 ≠ 0 → 対象外。
   - def+0xCC（enable：出現ターン）> turn → 対象外。
   - 0x585890(def, "fix") が "on" → 対象外。
   - 0x583A80(def) が真、def+0xA0 の文字列が非空、かつ "fix" ≠ "home"（0x42F860 は「不一致なら真」）→ 0x467F40(def+0xA0) の +0x128 ベクタ（0x1C 文字列）から 0x40ED80(n, 0) で1件選び（rand 1回）、spot として解決できれば def+0x84（放浪 spot）に代入。
   - 現在 spot = 0x467E90(def+0x84)。解決できなければ対象外。
   - 0x5AAEC0(out, spot の 0x597BA0, 0, 2, 上の代入フラグ) で候補リストを作る。空なら対象外。
   - 候補の絞り込み: "fix" ≠ "home" なら 0x4630D0、"fix" == "home" なら unit "home"（0x469460, @シナリオ優先）を集合化して照合（0x4622BE 以降）。
4. 0x4622BE 以降（候補の照合、移動先の決定、Troop/def への反映、失敗時の動作）は未読 → 次回の再開位置。

- 乱数: 現時点で確認できたのは "fix" ≠ "home" 側の def+0xA0 抽選での 0x40ED80 1回のみ。後半の抽選は未確認。
- 研究C（T025 等）の資料に 0x461DA0 / 0x471E80 の記述は無い（LANE_C_HANDOFF を read-only で確認）。

<a id="f-50"></a>
## §50 検証（今回）

- コード変更なし（Power+0xDC は §45 の `power_level_object_dc` のまま。hire 系 entry の level object 型が未確定なので、`create_for_entry` への自動接続はしていない）。
- 専用テスト 94件（前回保存版のまま）。
- 次の再開位置: 0x461DA0 の 0x4622BE 以降、0x5AAEC0 の候補生成、Unit 解放位置（シーン切替関数 0x48C880 / 0x48D6A0 側の解放処理）。

<a id="f-51"></a>
## §51 0x5AAEC0 spot探索（CONFIRMED）

`0x5AAEC0(out, start, power, mode, max_dist)`: 幅優先探索。キューに (要素, 距離) を積み、訪問済み集合で重複を防ぐ（開始点は距離0で訪問済み）。

- 取り出した要素の距離が max_dist を超えていれば捨てる（キューが空なら終了）。
- SpotEscapePath（RTTI判定）→ 追加も展開もしない。
- Spot → 開始点以外なら mode に応じて追加（mode 0: 0x597B00 の勢力 == power かつ power+0x10≠0、mode 1: ≠ power、mode 2: 常に追加）、その後 距離+1。
- その他の SpotElm（道）→ 追加しない、距離はそのまま。
- 未訪問の隣接（+0x8C..+0x90 ベクタ順）を現在の距離で積む。
- **出力は std::set<SpotElm*>**（0x14 バイトの木ノード、+0x10/+0x11 フラグ）。反復順は**オブジェクトのアドレス順**で、データだけからは決まらない（VERIFY：ヒープ配置）。

<a id="f-52"></a>
## §52 0x461DA0 月次放浪（完成、CONFIRMED）

§49 の前半に続き、0x4621B5..0x46272B を復元。1体の def につき:

1. 除外: def+0x74≠0、def+0xCC > 現在ターン、fix（0x585890, @シナリオ優先）== "on"。
2. 0x583A80(def) が真、def+0xA0 が非空、fix ≠ "home"（0x42F860 は不一致で真）→ 0x467F40(def+0xA0)+0x128 から 0x40ED80(n,0)（rand 1回）。spot として解決できれば def+0x84 に代入し、探索距離を 1 にする（既定 2、0x461FED / 0x4620C4）。
3. 現在 spot（def+0x84）を解決できなければ終了。S = 0x5AAEC0(spot, 0, mode 2, 距離)。空なら終了。S に現在 spot 自身を追加（0x4621B5）。
4. V = S をアドレス順にベクタ化。fix == "home" なら unit "home"（@シナリオ優先）に含まれる名前だけ残す（0x4622BE..0x4623D6）。fix ≠ "home" なら 0x4630D0 で全件（STATIC-HIGH：全件コピー）。
5. context "roam_avoid" が "on" のとき（0x484970(GM+0x1EF4B4) の +0x64 集合）: 0x583A80(def) が真、または yabo（0x585580、未定義なら 50）> _ftol2(rand/32768×200)（rand は 0x583A80 が偽のときだけ）なら、集合内の spot を V から除く。全部消えたら元の V に戻す（0x46248F..0x46255C）。
6. V が空なら終了。そうでなければ def+0x84 = V[_ftol2(rand/32768 × |V|)]（0x4625FD..0x46263F）。

- 乱数消費: 手順2で最大1、手順5で最大1、手順6で1。
- 反映先は def+0x84（放浪 spot 文字列）だけ。放浪集合 ctx+0x32C、Troop、Person、Power への書込は 0x461DA0 内に無い（CONFIRMED）。移動先が無い場合は def+0x84 が変わらない（手順2で代入済みの場合はその値のまま）。
- 呼出順: ctx+0x32C の集合順（def ポインタのアドレス順、VERIFY）で各 def を1回ずつ処理。同じ月に二重に動かす仕組みは無い（1回のループのみ）。0x461DA0 は 0x471E80（ターン処理）からのみ呼ばれる。
- 0x583A80 の意味（+0x94、+0x7C、+0x74、+0x174、class "price" を読む述語）は未解析 → 呼出側の入力（VERIFY）。def+0xA0 の文字列と 0x467F40 のオブジェクト型も VERIFY。
- 実装: `unit_int_default50`, `SpotElm`, `spots_within`, `RoamInputs`, `monthly_roam_def`。アドレス順は呼出側が `spot_address_rank` で明示的に渡す（既定値なし）。
- 研究Cの資料に 0x461DA0 / 0x471E80 の記述は無く、競合なし（read-only 確認）。

<a id="f-53"></a>
## §53 Unit を所有するコンテナと削除（新発見）

| 項目 | 内容 | 分類 |
|---|---|---|
| 所有者 | 陣営オブジェクト（Person/Enemy/Player/DemoPerson、GM+0x1E8630/+34/+38）の Unit ベクタ +0x48..+0x4C（ほかに +0x58, +0x38 のベクタ） | CONFIRMED |
| 全削除 | Person::vf04 0x514AA0（4つの vtable で共有）が +0x48 / +0x58 / +0x38 の全要素に slot0(1)（削除 dtor）を呼び、+0x6C 集合の要素の +0x6C を 0 にしてからベクタを空にする | CONFIRMED |
| 削除の呼出元 | GM リセット 0x48AA00 が3陣営の vf04（+0x10）を呼ぶ（0x48ABE7..）。0x48AA00 の呼出元は GameManager::vf02 0x4B9A20 のみ。Person の dtor 本体 0x5148A0 も 0x514AA0 を呼ぶ | CONFIRMED |
| 削除しない消去 | Person::vf01 0x5149C0（Player::vf01 0x51E6F0 経由）は同じベクタを**削除せず**空にする | CONFIRMED |
| 戦闘開始 | BattleEvent_InstallBattleBlock 0x492890 は3陣営の vf03（+0xC: Enemy 0x447810 / Player 0x51EF80）を呼ぶ。Unit 削除は含まない | CONFIRMED |
| 戦闘終了 | 0x493630 は vf05（LvUp）だけ。vf04 は呼ばない | CONFIRMED |
| 未解決 | GameManager::vf02（GameModel の全削除も行う）がいつ呼ばれるか（戦闘ごとかアプリ終了時か） | VERIFY |

- 現時点で言えること: 戦闘Unitは陣営が所有し、陣営の vf04 で一括削除される。戦闘終了処理そのものは削除しない。削除がいつ起きるかは GameManager::vf02 の呼出時期で決まる。
- HP については §43 のとおり、次に作られる Unit は満タンで始まる。Unit が再利用される経路は見つかっていない（生成は常に 0x56F880 の new）。

<a id="f-54"></a>
## §54 検証と保存（今回）

- 追加テスト: SYNTHETIC 6件（spot探索、通常抽選、除外条件、fix=home、roam_avoid と復元、def+0xA0 移動と探索距離1）。専用テスト 100件 OK。
- 次の再開位置: GameManager::vf02 の呼出時期、0x583A80 の述語、def+0xA0 の意味、0x4630D0 の確認。

<a id="f-55"></a>
## §55 戦略モード開発の現状分類（2026-10-12、Claude主担当開始）

dev_lab/src/hakushin_compat を読取調査（PC の git status / テスト実行は DC Local の実行が安全拒否 [Sensitive Remote Exec] → BLOCKED、迂回せず）。

| 区分 | 内容 |
|---|---|
| 実装済み・接続済み | def生成・能力値・技能・friend・EXP/LvUp・生成入口21件・中立部隊・放浪初期spot・月次放浪（peer_script01_native_definitions）、スクリプトVM（peer_script01_script_runner / flow_vm / expression / command_registry）、**戦略マップ構築（今回 peer_script01_strategy_world）** |
| 実装済み・未接続 | セーブ読み書き系（normal_save_* / *_native_full_wire / world_graph_native_wire：他AI所有、read-only）、scenario_surface（静的概要） |
| 仕様確定・未実装 | Power+0xDC、戦闘終了LvUp・Unit生成と HP 初期化の規則（§36/§43）、雇用系生成入口（obj 型以外） |
| 仕様未確定・要解析 | WORLD コマンド（addUnit 5474回、setTruce 1572、addSkill…）の状態変更、ターン処理 0x471E80 の全体順序、勢力AI、収入・維持費、戦闘開始の攻防決定、0x583A80、GameManager::vf02 の呼出時期 |
| 他AI担当・待機 | 戦闘内部（Work）、VM 研究（A）、内政・イベント研究（C：T025 等）、GUI 描画 |
| 実機照合待ち | すべて（GOLDEN 0 / MATCH 0） |

縦の実行経路（シナリオ開始→1ターン→移動→接敵→戦闘→結果→次ターン）のうち、今回成立したのは「シナリオ選択→マップ構築」。次は「勢力・spot 所属・人材配置」と「ターン処理 0x471E80 の順序」。

<a id="f-56"></a>
## §56 戦略マップ構築（GENERAL op42..45、STATIC-HIGH）

| op | 処理 | 根拠 |
|---|---|---|
| 42 showSpot | 名前ごとに 0x467E90 で spot を解決（失敗なら無視）。GM+0x1EEBCC の要素マップに無ければ作成（0x5A8110）して表示（vcall +0x54） | 0x4A2F00.. 疑似C |
| 43 hideSpot | 要素があれば非表示（+0x58） | 同上 |
| 44 linkSpot / linkEscape | 両端を 0x49C450 + 0x49E490 で解決、どちらか NULL なら何もしない。キー = 2名を 0x405490 の比較順で "+" 連結（向きは VERIFY、モデルは無順序対）。同じ要素マップに無ければ SpotPath（0x4A0050）/ SpotEscapePath（0x5AF9C0）を作成、ctor 内 0x5AFB30 → 0x5AF920×2 で両端に接続。既存なら再表示のみ。第3引数=経路画像（context "spot_route" / "spot_escape_route" 既定）、第4引数=数値 | 0x4A30F5.. asm / 疑似C |
| 45 hideLink | 既存の経路要素を非表示（+0x58） | 同上 |

- 初期マップはシナリオ宣言本体の文（showSpot / linkSpot …）で作られる。シナリオのスクリプトブロックは 0x4654B0 が返し、利用箇所は 0x53B750（← 0x53F120、シナリオ選択系ウィンドウ）。**実行時期は VERIFY**。
- 非表示の経路が隣接ベクタ（+0x8C）から外れるかは VERIFY → `spot_graph(include_hidden=...)` を呼出側が必ず指定。
- ACTUAL データ（STATIC 結果）: sci1 = spot 129 / 表示 110 / 経路 171（うち逃走路 11）。linkSpot 175 回のうち 4 回はシナリオ spot 一覧に無い spneet / sp85 を含むため作られない。rsc 125/113/171、sc_free 124/110/171、sci_st 72/63/4、sci_mt 9/9/8。全シナリオで未解決の変数引数 0。
- 実装: 新規 Claude 所有 `src/hakushin_compat/peer_script01_strategy_world.py`（`StrategyMap`, `StrategyScriptRunner`, `load_scenario_infos`, `build_scenario_map`）と `tests/test_peer_script01_strategy_world.py`（4件 OK）。スクリプト実行器は継承のみで、既存ファイルは変更していない。
- `StrategyMap.spot_graph()` は月次放浪 `monthly_roam_def` と `spots_within` にそのまま渡せる。

<a id="f-57"></a>
## §57 戦闘との接続契約（現時点の確定分）

| 方向 | 項目 | 内容 | 分類 |
|---|---|---|---|
| 戦略→戦闘 | Unit 生成 | 参戦 def ごとに 0x56F880（Unit ctor）: +0x1C8=def、+0x1D0=troop、+0x1CC=leader def。能力値は def から再構築、HP/MP 満タン | CONFIRMED（§43） |
| 戦略→戦闘 | 所有 | Unit は陣営オブジェクト（GM+0x1E8630/+34/+38）の +0x48 ベクタが所有 | CONFIRMED（§53） |
| 戦闘中 | EXP | 0x551E50 で def+0x16C に加算（通常 Unit は LvUp しない） | CONFIRMED（§35） |
| 戦闘→戦略 | LvUp | 0x493630 で 3 陣営 × Unit 順に 0x575110 | CONFIRMED（§36） |
| 戦闘→戦略 | 引継ぎ値 | def の Lv・EXP・next・能力値・技能・friend。Unit の HP/MP を def に書く命令は無い | CONFIRMED（§40/§43） |
| 未確定 | 攻撃側/防御側の決定、参戦部隊の選択、戦闘MAP選択、勝敗後の spot 所属変更、死亡・損耗の反映 | VERIFY（次工程） |

<a id="f-58"></a>
## §58 シナリオ開始：Spot・Power・放浪者（CONFIRMED、実装済み）

**Spot**（0x467260：ctx+0x2EC マップ、既存なら +0xB0=ctx のみ。new 0xD0 → ctor 0x5971A0 → 初期化 0x5972E0）
- +0x00 名前、+0xB0 ctx、+0xB8=0、+0x80 gain、+0x84 castle、+0x88 capacity（0 なら ctx+0xC、その後 24 で頭打ち 0x5973F9）、+0x2C map、+0x48 dungeon、+0x8C=0、+0x90 value。いずれも 0x4693F0（@シナリオ優先）。
- spot "member"（@シナリオ、0x469460、0x508AA0 ビルダー）を順に: 既存 def が +0x77 か +0x75 なら飛ばす。それ以外は 0x466F60（入口 0x59761A：flag 1＝配下も生成、level obj 0xAB42F8）→ def+0x78=1、def+0xCC=0、spot+0x1C（std::set）へ。def+0xE4 = +0x77 なら 0、+0x75 なら index+10、それ以外 index+24。続けてその def の配下（+0xD4）: 既存なら（+0x77/+0x75 → +0x7A=1）、+0xCC=0、spot+0x1C へ。
- **訂正**: §33 の SCENARIO_START_ORDER 手順1「def 生成なし・rand なし」は誤り。spot member の生成で rand を消費する（ソースの記述を修正）。


> 原本1317〜1322行は部分回収の対象外（personal_path_paragraph）。


**放浪者**（0x45D19A..0x45D78C）
- 代替 spot = ctx+0x2F0 の名前順で、no_home≠on、politics≠on（0x597770）、所有者がイベント勢力でないもの。
- scenario "roam" 順: 既存 def は飛ばす → 0x466F60（0x45D295：flag 0、base_level）→ roam_start_spot → spot が無ければ配置しない（0x463590）。
- 配下: unit member（@シナリオ、無ければ class member）。arbeit（unit、@シナリオ）が on/power/fix でなければ、unit "talent"（通常の Prop_LookupString）が "on" の名前だけ生成。既存で +0x77/+0x75 なら飛ばす。0x466F60（0x45D6A4：flag 0、base_level）→ 新 def が +0x77/+0x75 なら +0x7A=1、+0xC0=100、+0xCC=放浪者の +0xCC、放浪者 +0xD4 へ追加。最後に 0x460E90。

実装: `StrategySpot`, `StrategyPower`, `StrategyWorld`（`owner_of`）, `create_spot`, `create_power`, `start_scenario_world`, `roam_fallback_spots`, `start_roaming_units`。ctx+0xC（既定 capacity）の書込元は VERIFY のため呼出側の必須引数。

ACTUAL データ（STATIC、seed 1）: sci1 = spot 129、勢力 29、def 6985、rand 6977。po1 = master udk、領地 sp1、money 8000。放浪 26 名中 14 名を配置（残りは spot member で既に生成済み）、rand 累計 7011。

<a id="f-59"></a>
## §59 ターン処理 0x471E80（構造のみ、未実装）

- ECX = ターン管理オブジェクト。+0x38 = 段階番号。0 = ターン開始（+8=1、+0x38=1 など）、1 = 段階2へ、2..N+1 = 勢力ベクタ（+0x18..+0x1C）の各勢力を**1 呼出につき1勢力**処理。
- 勢力ごと（+0x1C が真のとき）: 0x595170 / 0x595320 / 0x49ED90、context 値（0x46F4C0）、Power+0xC4（100 上限で加算）、0x593550 で全 Unit を集め、各 Unit について:
  - +0x77 が偽: +0x74 が偽なら +0xBC に加算。0x585670 の値を money(+0x5C) から引き、負なら別集計、正なら 0x585750 の値を money に加える（収支、詳細 VERIFY）。
  - +0x77/+0x75 が偽で条件（+0x168 < 値、+0xC8 < ターン、0x5857E0 偽、訓練値≠0）を満たすと訓練: 技能 func==6 の +0x2B0 で回数を決め、`exp=next; 0x58A650` を回数分（§36 の forced_level_ups と同形）。
  - それ以外で +0xC0 < 閾値かつ +0x80 < 3 → 離脱候補（0x4C1290）。
  - 離脱候補ごと: 0x583CF0 → 所属解除（+0x78 なら 0x598450）、+0xD0 = ターン、0x460E90（放浪化）、"decide3" メッセージ（0x52CF50）。
  - 最後の勢力の後に politics フック（0x432EE0）。0x461DA0（月次放浪）、0x49E300、0x52AE60 などはこの関数の後半の分岐。
- 次回はこの関数を段階ごとに移植する（必要な補助関数 0x585670 / 0x585750 / 0x595170 / 0x595320 / 0x5857E0 / 0x583DC0 / 0x583CF0 / 0x474A80 の解析が先）。

<a id="f-60"></a>
## §60 検証と保存（今回の追加分）

- 戦略テスト 6 件 OK（合成 2・ACTUAL 4）。定義モジュールの変更は SCENARIO_START_ORDER の文言訂正のみ。

<a id="f-61"></a>
## §61 維持費・収入・初期設定・begin_scenario（CONFIRMED、実装済み）

- 維持費系（`peer_script01_strategy_world.py`）:
  - 0x585670 cost: `cost` が 0 以上で talent のとき、rank 1 なら senior_cost%、rank 2 なら executive_cost%。それ以外は素の値。
  - 0x585750 finance: cost < 0 なら −cost、それ以外は `finance`。
  - 0x5857E0: no_training。
  - 0x595170 training 目標: talent か +0x77 の def の平均レベル（いなければ 1.0）× pct × 0.01 + 0.5 を切捨て。pct は power の training_average、0 なら context の値（既定 100）。
  - 0x595320 training_up: power の値、0 なら scenario の値、それも 0 なら 1。負なら 0。
- 0x592E30 収入: `_ftol2(gain_per × 0.01 × Σspot gain + 0.5)`。
- 0x4726FF.. ターン末: +0x1C == 0 の勢力を順序ベクタから除き、それ以外は money += 収入（上限 1,000,000）。
- 0x45C1C3..0x45C5AB 初期設定（7項目）:
  - context の値（既定値あり）を読み、scenario がキーを持てばその値で上書きする。
  - spot_capacity / war_capacity は上限 24、3つの range は下限 1。
  - 結果を `@<key>` 変数に書く。
- `begin_scenario`: 設定 → spot → power → 放浪者 の順。diplo / league は未実装。
- ACTUAL（sci1）: 設定 = {8, 24, 500, 1600, 3, 1, 1}。po1 の収入 7000、rand 7011 回（モデル上の回数で、GOLDEN ではない）。

<a id="f-62"></a>
## §62 勢力の人事（merits・loyal・rank）とターンの勢力処理（CONFIRMED、実装済み）

### 62.1 新しく確定した事実
- **0x593550 は 0x5937BB で終わる。** 0x5937C0 以降は別の関数で、§59 の「残りは VERIFY」は誤りだった。
  - 勢力のユニット一覧 = power+0x64（名前順の set）の各 spot について、spot+0x1C（名前順の set）にある名前の def。
  - spot+0x1C には隊長（+0x78）と、0x5972E0 が入れた部隊員の両方が入っている。
- **def の ctor 値**（0x582C1E..0x582CCA）: +0x74 = 0、+0x80 = 0、+0xBC = 0、+0xC0 = 100、+0xC4 = 100、+0xC8 = −1、+0xD0 = −100。
- **power の ctor 値**: +0x1C/+0x1D = 0（0x590767）、+0x60 = 0x80000008（0x59076E）。
- **event 勢力**: 0x46757E で +0x1C = 0 になる（master が既にいても同じ）。ターン処理はこの勢力を飛ばし（0x472068）、ターン末に順序から除く。
  - 以前のテストは event 勢力 p2 がターン末に残る前提だった。期待値は native に合わせて修正し、テスト内で明示的に有効化する形に変えた。
- **0x4673B0 の後半**（0x467582..0x467815）:
  - base_merits = 0x5914D0("base_merits")、base_loyal = 0x5914D0("base_loyal")（0 なら 100）。
  - 各ユニット:
    - +0x77: merits 0 / loyal 100。
    - +0x75: merits = base、loyal = 0x585D20 が真なら 100、偽なら base。
    - その他: merits = base、loyal = base。
  - power の `merits` / `loyals` リスト（builder 0x507F60、`名前*N`）で個別に上書きする。
  - 最後に 0x5924B0 を呼ぶ。
- **0x585D20**（EBX = power）: 次をすべて満たすと真。
  - +0x77 でない。
  - master 本人でない。
  - `loyal` の def が master である。
  - +0x74 == 0 または power+0x60 == 0x80000008。
- **0x5924B0 rank**:
  - +0x77 → 4。+0x78 の def を集めて L とする。
  - L の talent で master に loyal（条件は上と同じ。ただし本人除外の判定はない）→ 3。
  - L を std::sort（0x47BB50）で並べる。比較 0x582750 の順:
    1. rank の降順
    2. merits の降順
    3. `sortkey` の昇順
    4. class 文字列（memcmp）の昇順
  - ex = `executive_bdr`（既定 10）、se = `senior_bdr`（既定 30）。power にキーがあればそちらを使う。
  - 0x5D1D90 は floor。ne = floor(n·ex%)、ns = floor(n·se%)。
  - rank < 3 のものは、i < ne なら 2、i < ns なら 1。
  - 32件を超えて完全同順位があるときは StrategyModelGap にする（introsort の順序は未移植）。sci1 では発生しない。
- **0x591570**（power の int）:
  - master に +0x77 があり名前が空でなければ、0x585580（unit 連鎖、既定 50）。
  - そうでなく power がキーを持てば、その値。
  - どちらでもなければ 50。
- **ターンの勢力入口** 0x473A68..0x473B34（phase が 2+i になった呼出し）:
  - 0x5924B0。
  - power+0x128 を clear（意味は VERIFY）。
  - `+0x68 = ftol(rand×2^-15×raid_bdr) + ftol(kosen²×0.01+0.5)` を計算する。**勢力ごとに rand 1回。**
  - "world" フック 0x432EE0(1,1,1) を呼ぶ。
- **勢力処理** 0x47202C..0x4726E7（次の呼出し）:
  - 前処理:
    - +0x1C == 0 なら何もしない。
    - しきい値 = −10000 + 100 − master+0xC4。power+0x1D が立ち、`@mode_escape` == 1 のときは −10000 の代わりに `loyal_escape_bdr`（既定 1）。
    - その後 master+0xC4 に trust_up（既定 1）を足す（上限 100）。
  - 各ユニット:
    - +0x77: finance を加算して次へ。
    - +0x74 == 0 なら merits += `merits_bonus`（既定 100）。
    - money −= cost。cost ≥ 0 なら finance を加算する。
    - talent: loyal < しきい値かつ rank < 3 なら出奔候補。
    - talent 以外: 次をすべて満たせば count 回レベルアップ（exp = next; 0x58A650）。
      - level < 目標
      - +0xC8 < turn
      - no_training でない
      - up ≠ 0
      - count = up + 隊長（0x583DC0）の status/training スキルの +0x2B0。0x40B200 は「一致で真」。
  - 出奔（0x47244C..、放浪化と「$$$が出奔しました」）は未移植。候補が出たら StrategyModelGap にする（fail-closed）。
  - power+0x1D が立っていて最後の phase なら "world" フックを呼ぶ。
- **0x583DC0**: 隊長（+0x78 または放浪中）なら本人。それ以外は def map を名前順に見て、member に名前を含む最初の隊長。見つからなければ NULL。
- turn = GM+0x1EF4C8 = ターン処理オブジェクト（GM+0x1EF4B4）の +0x14。0x472714 で +1。

### 62.2 実装（`peer_script01_strategy_world.py`）
- 追加した関数: `power_master_def`, `power_int_591570`, `loyal_to_master`, `init_power_units`（create_power から呼ぶ）, `assign_power_ranks`, `unit_leader_583dc0`, `leader_training_bonus`, `power_phase_entry`, `power_upkeep_step`, `PowerUpkeepReport`。
- `start_scenario_world` / `create_power` は `context` が必須になった。
- definitions の NativeDefinition に +0x74/+0x80/+0xBC/+0xC0/+0xC4/+0xC8 を追加した（ctor 値）。roam_definition でも 0xBC/0xC0/0x80 を戻す。
- `unit_cost` は rank_80 を直接使う（ctor 0 / 0x5924B0）。
- **STATIC_HIGH**:
  - `loyal`（builder 0x506AD0）を Prop_LookupString で読むときは、リストの先頭項目の名前部分として扱う。
  - `merits` / `loyals` 項目の `名前*N` 分割。

### 62.3 VERIFY / BLOCKED
- 未解析の書き手: +0x74、+0x1D（プレイヤー勢力か）、power+0x60。
- 0x5916E0 で master が無いときのダミー record の中身。
- 出奔の実処理（0x598450 / 0x416080 / 0x460E90）。
- phase 0 の 0x583A80 → +0xC8。
- ターン末の 0x46C940 と外交部。
- world フックの中身と、それが消費する rand。
- +0x68 の使い道（AI の行動判定と推定。未確認）。
- std::sort の32件超の同順位。

### 62.4 テスト
- strategy 14件、definitions 100件。合計114件 OK。
- 内訳: SYNTHETIC（rank / 維持費 / 訓練 / 出奔 fail-closed / raid の rand 1回）と ACTUAL（sci1）。
- GOLDEN 0 / MATCH 0。

<a id="f-63"></a>
## §63 変数ストア・外交・ターン末・ゲーム開始・std::sort（CONFIRMED、実装済み）

### 63.1 変数ストア（ctx+0x30C）
- 名前 → レコード `(text, int+0x1C)` の multimap。
  - 0x463CA0 find-or-create: 先頭レコードを返す。無ければ ("",0) を作る。
  - 0x4637A0 Set(name, v, replace): replace のとき 0x58F7E0 で同名を全消去してから ("",v) を追加。
  - 0x463BE0: 同名が存在するか。
  - 0x463610: (text,0) を追加。
  - 0x464050: text 一致のレコード一覧。
  - 0x463900(name, text|NULL): text 一致のレコードを削除。NULL なら全削除。
- 外交はすべてこの変数で持つ（勢力名は byte 比較で小さい方を先に連結、区切りなし）。
  - `@frd_`+min+max: 友好度。
    - 0x46B230: NULL 勢力なら 0x80000008、それ以外は find-or-create。
    - 0x46B3A0: 0x80000008 以外は 0..100 に丸めて Set。
    - 0x46B580: 存在するか。
  - `@leg_`+min+max: 同盟の期限ターン（0x46B720 / 0x46B8D0、同じ勢力同士なら何もしない）。
  - `@trc_`+a+b: **引数の順で連結し、並べ替えない**。
    - 0x46BA40: −1 なら 0x7FFFFFFF、それ以外は max(v−turn, 0)。
    - 0x46BB80: Set。
  - 0x46C200(p,q,v):
    - `@com_p` の (q, max) レコードを更新する。
    - `@com2_p_q` の (p, v) レコードを設定する。
- 中立勢力 = ctx+0x58（名前は空）。0x597B00 の fallback と同じオブジェクト。

### 63.2 シナリオ開始時の外交（0x45CA90..0x45D0B8）
- 全勢力を名前順に処理する（フィルタなし）。
- 中立との友好度 = 75 − yabo/2（0x591570 "yabo"）。
- 自分自身との友好度 = 0x80000008。
- 他の勢力 q との友好度:
  - `diplo` に q を名指しした最初の項目があれば、その値。
  - 無ければ、まだ変数が無いときだけ 50。
  - 名前順で後に処理される勢力の `diplo` 指定が上書きする。
- `league` → 0x46B8D0、`enemy_power` → 0x46C200。
- begin_scenario に組み込んだ（放浪者配置の前）。
- sci1: `@frd_` 464件、`@leg_` 5件。

### 63.3 ターン末 0x4726FF..0x473A31（`turn_wrap`）
- turn+1 したあと、勢力の順序ベクタを走査する。
  - 非活性の勢力は erase。
  - 0x46C940（`@beit_` レコード。存在すれば Gap）。
  - money += 収入（上限 1e6）。
  - 全勢力名との組ごとに:
    - `@leg_` を find-or-create する（**全組の変数が生成される副作用**）。
    - 値 == turn なら同盟期限切れ。0x46BC80 ブロック（`@com_` があれば Gap）と、履歴 0x471110(9)。
- 友好度の自然減:
  - `diplo_frd_turndown`(1) と `diplo_sup_turndown`(1) を使う。
  - i<j の各組で、com 集合に無ければ frd>0 なら max(frd−sup, 1)。
  - さらに、同盟が無く（leg ≤ 0）、0x4807E0 で隣接していれば max(frd−frd_t, 1)。
- **0x4807E0（隣接判定）**: p の各 spot のうち可視（SpotElm+0x88 = vf25）のものについて、0x5AAEC0(mode 0, 距離 1, 勢力 q) が空でなければ真。
- その後の処理（呼出側の仕事）: 0x49E300（再描画）、0x461DA0（月次の放浪）、world フック、エンディング判定、autosave。
  - autosave は scenario `no_autosave` が "on" と**異なる**とき（0x42F860）。

### 63.4 ゲーム開始 0x45B850（`game_start`）とターン初期化 0x4716C0
- **プレイヤー**:
  - power+0x1D = 1（**+0x1D = プレイヤー勢力で確定**）。
  - 君主 def の +0x74 = 1（**+0x74 = プレイヤー操作ユニット**）、+0xCC = 0。
  - 0x583C70 = def を含む最初の spot の所有者（無ければ中立）。
- **actor（+0x76）**:
  - 候補 = +0x74 が立っておらず（+0x77 または +0x75）の def。`actor`=="on" なら先に +0x76 を立てる。
  - std::sort で並べる。比較 0x582640 は yabo **>=**（非厳密）。
  - 件数 = chop(n×actor_per%+0.5)。actor_per は scenario の値、無ければ context。
  - 順に見る:
    - 既に actor → 件数 −1。
    - "off" → 飛ばす。
    - "on" → 立てて件数 −1。
    - それ以外 → chop(rand×2^-15×100) < yabo（君主は ×2）なら立てて件数 −1。
- **中立部隊 0x460940**: 対象は、所有者が中立で、かつ member 集合が空（spot+0x24 = set のサイズ）の spot。[0x65C118]=8。
- **0x4716C0**:
  - turn = 0、phase 0。
  - 順序 = event でない勢力を名前順に並べ、random_shuffle 0x501CA0（n−1 回の rand）。
  - `power_order`（0x468880: scenario の値、無ければ context の値）=="test" でプレイヤー勢力があれば、先頭と**交換**（移動ではない）。
- sci1・po1 選択: rand 28回（シャッフルのみ）、先頭 po1。actor_per = 0。

### 63.5 std::sort の移植（`msvc_sort`）
- 0x47BB50（_Sort: 32件超かつ ideal>0 なら分割、ideal = ideal/2 + ideal/4）を移植した。
  - 0x47BCC0 _Unguarded_partition、0x47BE60 _Median（40件超で9点の中央値）、0x44D6A0 _Insertion_sort は逆アセンブルと照合済み。
  - ヒープソート部（0x4F62C0 / 0x47C070）は MSVC2010 の実装どおり（STATIC_HIGH）。
- rank のソート（§62 の Gap）はこれに置き換えた。

### 63.6 戦争・AI の地図（STATIC、未実装）
- **GameCtrl::vf01 0x474F10**:
  - phase≥2 で現在の勢力がプレイヤー（+0x1D）なら UI へ（0x51FAA0）。
  - AI なら次の順で進める:
    1. 0x4751C0（攻撃判断）
    2. 0x47E3A0
    3. 0x47F670 / 0x47A1A0
    4. 0x47AE50
    5. 0x471E80
- **0x4751C0**: 目標候補（turn+0x40）を、raid 値（turn+0x68）、0x46B230、Rng_RangeInclusive、0x5AB460 で評価する。
  - 0x597D50 で出撃部隊を集め、0x48F9E0（戦争開始）または 0x475B90（移動）へ進む。
- **0x48F9E0 戦争開始**: GM+0x1EED1C=目標 spot、+0x1EED4C=防衛勢力（0x597B00）、+0x1EED50=攻撃勢力。最後に 0x4868D0（援軍）と 0x490180。
- **0x493630 戦争終了**（結果の反映）。処理内容:
  - 友好国を攻めたときの diplo_down / diplo_bestfriend
  - `@battlefield` / `@battleattack` / `@battledefense`
  - 敗北時の loyal_down、勝利・防衛メッセージ、退却 0x4962B0
  - 滅亡 0x4973E0、world フック
  - win_gain、loyal_up/down、占領
  - 従軍報酬（support_gain / arbeit_gain）
  - レベルアップ（§既出）
- 次の工程は 0x493630 の移植（Work 側の戦闘結果を受け取る契約）。

### 63.7 テスト
- strategy 18件、definitions 100件。合計118件 OK。GOLDEN 0 / MATCH 0。

<a id="f-64"></a>
## §64 戦闘の書戻し・AIの評価値・ターンの全体構造（CONFIRMED、実装済み）

### 64.1 ターンの全体構造（GameCtrl::vf01 0x474F10 / 0x471E80 / 0x47C280）
- **phase 0**: 0x471E80 で phase 1 へ進む（0x583A80 の条件を満たせば ctx+0x50 の +0xC8 を設定）。
- **phase 1 = 放浪・人材の行動（0x47C280）**:
  - 呼ばれるたびに次を行う:
    - actor_per は scenario の値、無ければ context の値（0）。
    - 行動者ベクタ（turn+0x28）が空なら作り直す。
      - 対象: def map を名前順に見て、次をすべて満たすもの。
        - 放浪していない、または enable ≤ turn
        - +0x77 または +0x75
        - +0x78 または放浪中
        - +0x77 も +0x74 も立っていない
      - +0x76（actor）ならそのまま追加する。
      - それ以外は、0x583A80 が真なら 0x47CE80 を呼ぶ。続いて **rand（0x40ED80(0,100)）を1回**引き、< actor_per かつ 0x585C80 なら追加する。
      - 最後に random_shuffle する。
    - 0x462740（中立の攻略候補 spot）について、各 spot に 0x47C0E0 を適用し、shuffle したあと std::sort（+0xC0 の降順、0x47C260）。
    - `@mode_steal`==1 でプレイヤー勢力があれば、その spot を shuffle して先頭10件を残し、+0xC0=gain、+0xBC=0x597C90 を入れて sort する。
    - 0x484970（突出勢力）があれば、「その勢力の spot 数 ÷ 可視 spot 数 ≥ raise_most_power(80)%」のとき行動を禁止する。
    - 行動者を +0x3C から1人ずつ処理する:
      - actor かつ資金(+0x174) > 10 なら 0x47C7A0。0x583A80 が真なら 0x47CE80。
      - 行動が許可されていれば 0x47D520 を呼ぶ。行動を起こしたらそこで戻る（戦闘などで中断）。
    - 全員を処理し終えたら 0x471E80 で phase 2（勢力 0 の入口）へ進む。
- **phase ≥2**:
  - プレイヤー勢力（+0x1D）なら UI へ。
  - AI なら 0x4751C0（攻撃判断、目標候補 turn+0x40 と raid 値 turn+0x68）→ 0x47E3A0 → 0x47F670 / 0x47A1A0 → 0x47AE50 → 0x471E80。
- **0x47D520（人材の行動）**:
  - turn == 0 なら何もしない。
  - 所属勢力 = 0x583C70。
  - 放浪していなければ、loyal ≥ loyal_border(50)+100−君主の信頼のとき中止。そうでなければ倍率 = 1+(閾値−loyal)/閾値。放浪中は倍率 2.0。
  - 中止条件:
    - 非プレイヤー勢力で 0x587C10 が偽。
    - 0x583A80 が真かつ +0xB0 が 0 でない。
    - 0x585D20（君主に loyal）。
    - yabo < raise_yabo_bdr。
  - 強さの閾値:
    - a = chop(yabo×倍率+0.5)、b = chop(a×1.5+0.5)。
    - r = 0x40ED80(a/2, b)。
    - v = chop(0x587FA0×r%+0.5)。
  - 候補 spot のうち、v ≥ +0xBC で 0x5AD6C0（経路）があるものに 0x47D770（戦争開始）。プレイヤー勢力の場合は、steal 候補に経路判定なしで同じ処理。

### 64.2 実装した関数
- **`unit_defeated_588470`**（Unit::vf28 → def+0x1B0「死亡」）。処理:
  - talent 以外は Unit+0x18614==0。
  - 残っているレベルアップを処理する（インラインのループは 0x58A650 と同じ本体。定数の番地が一致、STATIC_HIGH）。
  - exp ×dead_penalty(50)%。
  - 治療費 = medical×level。所属勢力の money から払う。
  - `@mode_dead2` / `@mode_dead` と alive_per による死亡判定。君主とプレイヤーユニットは別の分岐。
- **`unit_strength_587cc0`**: context の fv_* 係数（0x459610 で読む。既定値 hp10 mp100 attack100 speed200 move200 hprec200 level10 consti10 summon20）を使い、各積を chop して def+0x1C4 に入れる。
- `spot_strength_597c90`、`power_strength_592f10`。
- `neutral_raise_targets_462740`: no_raise≠"on"、可視、中立の spot。
- `spot_ai_value_47c0e0`: chop((中立の隣接数/隣接数×10+1)×gain+0.5)。
- `dominant_power_484970`:
  - partial_sort（0x484E70）で上位2勢力を取り、比 ≥ diplo_most_power(200)% なら最上位を返す。
  - プレイヤーがいて、最上位がプレイヤー勢力でなければ閾値を2乗する。
- `msvc_partial_sort`。
- 0x587C10 = 配下に +0x7A のものがいる。0x587FA0 = 本人と配下の強さの和。

### 64.3 次の工程
- 0x5AD6C0（spot 経路、510行）、0x47D770（人材による戦争開始、491行）、0x47CE80 / 0x47C7A0（放浪者の雇用・移動）。
- その後 0x4751C0（AI の攻撃）、0x48F9E0 / 0x493630（戦争の開始と終了）。

### 64.4 テスト
- strategy 22件、definitions 100件。合計122件 OK。GOLDEN 0 / MATCH 0。

<a id="f-65"></a>
## §65 phase 1（人材の行動）の実装と、可視判定・経路（CONFIRMED、実装済み）

- **0x597BA0（要素の取得）**: 要素が無い spot には、静的なダミー Spot を返す。ctor 0x5A8110 は 0x5A83C3 で +0x88=0 を書くので、ダミーは**常に不可視**。§63 の 0x4807E0 で Gap にしていた扱いを、不可視に修正した。
- **0x5AD6C0（経路）**: (a, b, flag) を受け取る。
  - a==b なら真（0xFFFFFFFF）。
  - 要素のリンクベクタ上で BFS を行う。訪問済みには enqueue の時点で印を付ける。
  - escape パスには入らない。road は深さを変えずに進む。spot は深さ +1。
  - flag が立っていれば、開始 spot の所有勢力の spot だけを通る。
  - 深さ > 0 で b に着けば真。
- **0x583A80（放浪中で行動できるか）**:
  - 放浪していなければ偽。
  - +0x7C==1:
    - プレイヤーなら資金 > 0。
    - それ以外は、資金 > arbeit_money_mini × class の price。
    - 上の条件に当たらなければ、配下に +0x7A==0 の者がいれば真。
  - +0x7C==2: +0xB0 が 0 でないか、GM+0x1EF140==5（未対応で Gap）。
  - +0x7C==3: 真。
  - ctor は +0x7C=0、+0x174=0 なので、シナリオ開始直後は常に偽。
- 補助関数:
  - 0x583CF0 / 0x585C80（def の spot と、その spot がプレイヤーのものか）。
  - 0x587C10（配下に +0x7A の者がいる）。def に `flag_7a` を追加した。0x5972E0 で 1、0x460E90 で 0 に戻す。
  - 0x587FA0（本人と配下の強さの和）。
- **`actor_phase_47c280` / `actor_action_47d520` / `actor_war_47d770`**:
  - 放浪者の戦争は `WarRequest` として返す（0x48F9E0 は未移植）。
  - 次の場合は Gap にする: 謀反（放浪していない人材の 0x47D770）、0x47CE80、0x47C7A0。
  - turn 0 では 0x47D520 は何もしない。ただし rand は、行動者リストを作るときに引かれる。
- **0x65C114（nozone）**:
  - `@mode_nozone`==1、または ctx+0x33C（zone のリスト）が空なら 1。
  - 実データに zone 宣言は無い（scenario1 は `nozone = on`）。そのため AI は 0x47A1A0 の経路を通る（zone のリストを書く処理は VERIFY）。
- ACTUAL（sci1・po1・turn 0）: phase 1 で rand 334回、行動者 0。モデル上の回数。
- テスト: strategy 25件、definitions 100件。合計125件 OK。GOLDEN 0 / MATCH 0。
- 次の工程:
  1. 勢力 AI のフレーム処理: 0x481260 / 0x476D60 / 0x47E3A0 / 0x47A1A0 / 0x4751C0 / 0x47AE50。
  2. 戦争の開始 0x48F9E0 と終了 0x493630。

<a id="f-66"></a>
## §66 勢力の性格 0x593890 と勢力AIの目標選定 0x47E3A0（CONFIRMED、実装済み）

- **0x593890（性格 power+0x20）**: 勢力の初期化 0x590880 の中で、**member の処理より前**（0x5909C6）に呼ばれ、**rand を1回引く**。
  - これまでのシナリオ開始のモデルには、この rand が抜けていた。修正後、sci1 の開始は 6977 → **7006回**（29勢力 × 1）、begin_scenario 込みは 7011 → **7040回**。テストの期待値は、この根拠で更新した。
  - y = 0x591570(p,"yabo")。この時点では master の +0x77 はまだ立っていない（0x467535 は初期化の後）。そのため、勢力の yabo か 50 が使われる。
  - a=chop(y×0.5+0.5)、b=chop(y+0.5)、v=chop(r×2^-15×(b−a))+a。
  - v<25 → 3、v<50 → 2、v<75 → 1、それ以外 → 0。
  - 3 になり、かつ ctx+0x54（プレイヤー勢力）=0、ctx+0x50（プレイヤー人材）≠0、0x592CE0 が真なら 2 にする。0x592CE0 は「勢力が +0x1D を持つか、勢力の spot の配下に +0x74 の def がいる」。
  - ctor は +0x20 を書かない。中立の勢力 ctx+0x58 は静的な ctx（0x8BE4A8、BSS）の中にあり、0x593890 の呼出元（0x5909C6・0x590F90・0x475C60・0x481260）からは書かれない。よって 0 とした（STATIC_HIGH。ロード後や2戦目以降は VERIFY）。
- **0x591D50（目指す地点）**:
  - H を決める: power+0xC0（`@@@@@` が1件だけなら空）。+0xC0 が空なら、勢力の `home` リストを使う。
  - H の各 spot で、要素が見えるものだけを見る。最初のものを centre として覚える。
    - +0x64 に無い（自勢力の spot でない）→ その中点を返す。
    - 自勢力の spot なら、0x5AAEC0(mode 2, 1) の要素を set 順に見て、+0x64 に無い最初の要素の中点を返す。
  - 最後まで返らなければ、flag（p+0x20≠0）が立っていれば centre、立っていなければ 0x80000008。
- **要素の矩形（ctor 0x5A8110）**:
  - 中心は spot の x / y。大きさは 32×32。
  - big>0 なら縦横とも big。w>0 / h>0 はそれぞれ個別に上書きする。
  - +0x40=x−w/2（C の除算）、+0x48=+0x40+w。y 側も同じ。
  - 中点 = x0+((x1−x0)>>1)。
  - 矩形を後から書く関数（0x5A4D20 / 0x5A71F0 / 0x5A99C0）は VERIFY。
- **0x480370**: 目標ごとに +0xBC=trunc(sqrt(dx²+dy²))。目指す地点が無い（sentinel）なら 0。sqrt は PC53 を前提に isqrt と同じ結果になる（PC24 は §付録の VERIFY）。
- **0x47B740（橋渡しの目標）**: 静的な set を返す。
  - 目標 t に隣接する自 spot（mode 0）が2つ以上あり、自勢力の spot だけを通って互いにつながらない場合が対象。
  - そのとき t+0xBC = 先頭の +0xBC + (件数−i)×100 とし、set に入れる。
  - 到達性は対称なので、set の順には依存しない。
- **0x47E3A0 の本体**（p = 手番の勢力）:
  1. 自 spot（0x593400）の +0xC0=1000000、+0xC4=0、+0xC8=0 にする。ターンの +0x54 と +0x40 を空にする。
  2. 自 spot ごとに、隣接する他勢力の spot（mode 1）を見る。まだ見ていない spot で、leg(p,所有者)<1 かつ trc(p→所有者)<1 なら +0x40 に積む。
  3. 目標が無ければ終わる。あれば random_shuffle（n−1 回の rand）。
  4. 0x591D50 と 0x480370 で距離を出し、0x47E2E0（+0xBC の降順）で sort する。
  5. 1回目の評価: v=max(10, castle/2+gain)。地点があれば、v=chop(((i×twc+1)×v)+0.5)（twc=target_way_coe(50)×0.01）。sort する。
  6. caution=0.1。`@mode_hostil`（find-or-create）==1 なら caution_adjust(30)×0.01。
  7. 敵対集合 H = 0x484970 の最強勢力（p 以外）＋ 0x46BC80(p) のうち frd<50 の勢力。
  8. +0xC4=max(100, 0x597C90) とし、その最大を M とする。k1=1000/M、k2=1000/件数。
  9. 2回目の評価。**所有者の** +0x20 で式が分かれる:
     - 0: (D+2X)+P
     - 1: (D+X)+P
     - 2: (2D+B)+2P
     - その他: (D+B)+2P
     - D=(100−frd(p,所有者))×10、X=(M−c4)×k1、B=c4×k1、P=(件数−i)×k2。
     - +0.5 して chop する。所有者がプレイヤーなら、chop(r×caution+0.5) を加える。
  10. partial_sort(k=1) のあと 0x47B740、そして sort する。
  11. 目標ごとに rand を1回引く。c4=chop(max(1, r×2^-15×(yabo×0.02))×c4+0.5)。
      - power+0x108 の記録で |turn−記録|≤2 なら ×4。
      - 最後に max(100)。
      - 最初に +0xBC/先頭 < 閾値（自勢力の +0x20 が 0 なら 0.33、1 なら 0.66、それ以外は 0.25）になった位置を覚える。
  12. 覚えた位置から後ろは +0xC8=1。自勢力の性格が 1 なら c4×0.75、2 なら c4×0.66（いずれも +0.5 して chop）。
  13. 目標の順に、隣接する自 spot（mode 0）のうち未割当のもの（set_difference 0x480400）を割り当てる。
      - 自 spot に +0xC4・+0xC8 を写し、+0xC0=通し番号とする。
      - 所有者がプレイヤー、所有者が H にいる、または橋渡しの目標なら、+0xCC=目標。
      - その spot を +0x54 に積む。
      - 守備の def（0x597D50: 配下のうち +0x78 の者）に、+0x1C8=0x587FA0、+0x1BC=spot、+0x1D0=番号を書く。
- 追加したフィールド:
  - def: +0x1BC / +0x1C8 / +0x1D0（ctor 0）
  - spot: +0xC4 / +0xC8 / +0xCC（ctor 0）
  - power: +0x20 / +0xC0 / +0x108（書く関数は VERIFY）
  - ターン: +0x40 / +0x54
- **重大 VERIFY / BLOCKED: SpotElm の set 順**:
  - 0x5AAEC0 が返す std::set<SpotElm*> は**オブジェクトのアドレス順**。次の3か所で結果を左右する。
    - 目標の収集順（その後の shuffle の入力）
    - 自 spot の割当番号
    - 0x591D50 の近傍
  - アドレスはヒープの性質で決まる。Windows の LFH はアドレスを無作為化することがあるので、静的には決められず、実行ごとに変わる可能性もある（推定、VERIFY）。
  - 実装は `elem_rank` を明示的に受け取る。受け取らずに順序が結果を左右する場面では、StrategyModelGap にする。
  - ACTUAL（sci1・po1・turn 0）: 28 の AI 勢力のうち **25 が Gap**。目標が1つの po10 は ['sp23'] になる。
  - 進めるには、実行時に順序を取得するか、互換方針（例: 要素の生成順）を明示的に決める必要がある。決めるのはユーザー / Work。
- テスト: strategy 28件、definitions 100件。

<a id="f-67"></a>
## §67 戦闘終了 0x493630 の復元と、Work 向けの戦略側公開 API（STATIC、一部実装）

### 67.1 呼出元と引数（CONFIRMED）
- 0x493630 は ECX = 目標 spot（GM+0x1EED1C）、EDX = 戦争ブロック（GM+0x1EED20）、引数1 = GM、引数2 = 結果フラグ（0/1）で呼ばれ、`ret 8` で戻る。
- 呼出元とフラグ:

| 呼出元 | 条件 | フラグ |
|---|---|---|
| FrameDriver 0x49303A | 片方の陣営（0x514C80）が全滅し、+0x1EED68 ≤ 0 で、GM+0x1EED48 側が残る | 1 |
| 0x4930A1 | 同じ条件で GM+0x1EED48 側も全滅 | 0 |
| 0x493082 | 時間切れ（0x565730 ≤ 0）、A 側の vf18 == 4 かつ B 側 ≠ 4 | 1 |
| 0x4930A1 | 時間切れのその他 | 0 |
| BattleWnd::vf01 0x40E2B9 | 0x40E2F0 の結果 == 1 | その値 |
| Script_DispatchCommand 0x4A1764 | スクリプトの引数 | その値 |

- 結果フラグは勝ち負けとして命名しない。挙動として分かっていることは次のとおり。
  - フラグ 0: 攻撃側の忠誠が下がる。目標は奪われない。攻撃側の power+0x108 に、目標とターンが記録される。
  - フラグ 1: 防衛側が撤退または解散し、攻撃側が目標に入って領有する。
  - 支払いでは、フラグ 1 のとき防衛側の率が `*_lose`、攻撃側の率が `*_gain` になる。

### 67.2 処理の順序（CONFIRMED。GUI の部分は移植しない）
1. "battle" マップの検索と、要素の 0x5AAE50（GUI）。
2. **GM+0x1EEC3C == 2 なら**、3陣営 GM+0x1E8630 / +0x1E8634 / +0x1E8638 の vf05 をこの順で呼ぶ（Unit ベクタ順に 0x575110 → LvUp、§36）。その後 0x4C21F0(app+0xC, 25)。
   - **0x4C21F0 の正体**: フレーム周期の設定。app+0x74 = 25、app+0x78 = chop(1000/25 + 0.5) = 40ms。ゲームの状態には影響しない。
3. 音（0x405A20）。
4. ctx+0x54 == 0 かつ ctx+0x50 ≠ 0 かつ phase ≠ 0 なら、プレイヤー def の +0x79 を 0 にする。
5. GM の戦闘フィールドをクリアする（+0x1EEC44 / +0x1EEC48 / +0x1EED40..42、ベクタ +0x1EEDC4 / +0x1EEDD4、集合 +0x1EEDE4、リスト +0x1EEDB8）。
6. 放浪者の戦争かどうかを判定する（0x48F720 / 0x493819）。条件は、攻撃マップが1件で、その最初の def が放浪中であり、かつ「0x583A80 が偽、または +0xB0 == 0」であること。
7. 一覧を作る。
   - **e0**: 攻撃マップ（GM+0x1EED24、{出発 spot: set<def*>}）のレコードを、出発 spot の +0xC0 の昇順に std::sort（0x499290 / 0x48F700）する。各レコードの def は +0xE4 の昇順（0x530490）。
   - help マップ（GM+0x1EED34、{spot: (power, byte)}）にある出発 spot の def とその配下は、援軍集合1 に入る。byte が 0 なら援軍集合2 にも入る。
   - **d0**: 目標の守備（0x597D50: +0x78 の者）を、0x582750 で並べたもの。
8. 両勢力に名前がある場合:
   - phase ≠ 0 かつ 0x5923F0 なら「友好国に攻め込んだので信用度が下がりました」（GUI）。
   - frd(防衛, 攻撃) > 0 なら、frd − diplo_down(10) を求め、diplo_bestfriend(80) 以上なら 79、1 未満なら 1 にして書く。
   - 防衛側の power+0x118 から攻撃側を消す。
   - 両勢力の power+0x128 に目標の spot 名を追加する。
   - `@war_`+最小+最大 = 1（0x46C710。`"@"+キー+"_"` + 並べた組）。
9. `@battlefield` / `@battleattack` / `@battledefense` を置換で書く（0x463610 の第3引数 1 = 既存を消して (text, 0)）。
10. 戦闘で作られた def（GM+0x1EEC00）を 0x463590 で破棄する（def マップと放浪集合から外して delete）。
11. **死亡処理**（d0、次に e0 の順）:
    - 1周目: 各 def の配下のうち +0x1B0 の者について、spot の集合から外し、0x497BB0(ECX=NULL) で即時に破棄し、+0xD4 から除く。
    - 2周目: +0x1B0 の def について:
      - 配下がいない場合: 一覧の要素を "" にし、spot から外す。
      - 配下がいる場合: 最初に見つかった配下が後継になる。
        - +0xBC = max(後継, 本人)。+0x1B4 は本人の値をコピーする。+0x78 = 1、+0x7A = 0。
        - 後継の配下は、本人の配下のうち後継より後の者にする。
        - 一覧の要素を後継の名前に置き換える。
        - 本人が放浪中でなければ、spot から外す。放浪中で spot 名があれば、後継を 0x460E90 で放浪させる。
      - いずれの場合も、0x497BB0 に ECX = 遅延ベクタを渡す（最後に 0x463590）。
    - **0x497BB0（+0x1B0 の def の場合）**:
      - +0x77 も +0x75 もなければ、破棄（ECX が NULL なら即時、そうでなければ遅延）。
      - そうでなければ「死亡しました」（GUI）を出す。その def が +0x74 なら ctx+0x50 = 0、ctx+0x54 = ctx+0x58。その後で破棄。
    - 生存したまま離脱する def は、別の経路を通る（0x585E00 自決/殉死、0x585890 と rand による +0x7C 傭兵化、0x460E90 放浪）。この経路は VERIFY。
12. 攻撃マップが空（GM+0x1EED28 == 0）なら、0x52BFF0 / "btlevent"、遅延破棄をして戻る。
13. **フラグ 0**:
    - 攻撃側（援軍以外、配下を含む）のうち、+0x75 で、+0x7A と +0x77 がなく、rank < 3 の者について、+0xC0 −= loyal_down(10) + (100 − 攻撃側の盟主の +0xC4) とする。負になったら 0。
      - 盟主がいない場合、0x5916E0 は ctor で作った静的な仮レコード（+0xC4 = 100）を返す。
    - メッセージ（GUI）の後、0x4962B0(0) を呼ぶ。
    - 攻撃側に名前があれば、power+0x108 に [目標] = turn を挿入する（insert-if-absent）。
    - 0x592320 が偽の勢力には 0x4973E0（攻撃側、防衛側の順）。
    - mode 1 なら "world"（GUI）。最後に遅延破棄。
14. **フラグ 1**:
    - **防衛側（d0、援軍以外）**:
      - 撤退先 = def+0x1B4（Spot*）、なければ 0x5AC1A0(目標の要素, 防衛勢力, k>0)。2回目は +0x77 の者だけ試す。
      - 撤退先がある場合: 0x598450 で目標から外し、撤退先の集合に本人と配下を入れる。撤退先が def+0x1B4 だった場合は、spot+0xB8 を −1 する。
      - 撤退先がない場合: 0x598450 で外したうえで、配下に 0x497BB0(ECX=NULL)、本人に 0x497BB0(遅延) を呼ぶ。
    - 目標の集合を空にする（0x416870）。
    - **攻撃側（e0、援軍以外）**: 目標の capacity（+0x88）に達するまで、隊長を数えながら元の spot から移す（配下も一緒に移すが、数には含めない）。
    - 放浪者の戦争なら: 本人が生きていれば 0x434EB0（新しい勢力を作る）。いずれの場合も遅延破棄をして戻る。
    - **占領**:
      - bonus = chop(win_gain(50) × gain × 0.01 + 0.5)。
      - 防衛側の忠誠を、フラグ 0 と同じ式で下げる（盟主は防衛側の勢力）。
      - 攻撃側のうち +0x75 で、+0x77 と +0x7A がない者: +0xC0 += loyal_up(10)（上限 100）、+0x174 += bonus、攻撃側 +0x5C −= bonus。
      - 防衛側の +0x64 から目標を消し、攻撃側の +0x64 に入れる。
      - その後、メッセージ（GUI）、0x4962B0(1)、0x592320 / 0x4973E0、GUI、遅延破棄。
15. **0x5AC1A0（撤退先の探索）**:
    - 防衛勢力に名前がなければ NULL。
    - 要素の BFS を行う。deque を使い、訪問済みには追加の時点で印を付ける。
    - 展開するたびに、要素のリンクベクタのコピーを **random_shuffle** する。
    - 開始以外の Spot 要素で、勢力が一致するものについて:
      - 隊数（0x597A50: +0x78 の者）+ +0xB8 < capacity なら、その spot を返す。
      - そうでなく flag が立っていれば、+0x77 も +0x75 もない最初の隊を 0x598450(…, 1) で解散させ、その spot を返す。
16. **0x4962B0（報酬・謝礼）**:
    - 金額の元は、Unit 登録 GM+0x1EEBDC（0x49E6B0: 名前 → Unit）の **Unit+0x1B4**（部隊の功績。戦闘中に加算される）。def+0x1B4 ではない。
    - support: help の各 spot について、spot の配下が空で要素も不可視の場合は除く。それ以外は、Σ Unit+0x1B4 × 率 + 0.5 を chop した額を、援軍の勢力が受け取り、防衛側（byte ≠ 0）または攻撃側（byte 0）が支払う。
    - arbeit: spot の配下が空で、要素も不可視の spot（傭兵）だけが対象。その set の最初の def の +0x174 に chop(Unit+0x1B4 × 率 + 0.5) を加え、同じ額を勢力が支払う。率が 0 の側は処理しない。
    - 率の既定値: support_gain 10、support_gain_lose 3、arbeit_gain 10、arbeit_gain_lose 0。
17. 0x592320（勢力が存続しているか）:
    - 名前が空なら真。
    - 盟主に +0x77 と名前があれば、0x583C70(盟主) == p かどうか。
    - そうでなく、"master" キーの文字列が空なら、spot が1つ以上あるかどうか。
    - それ以外は偽。

### 67.3 Work 向けの公開 API（`peer_script01_battle_end.py`）
- 呼び出し: `apply_battle_end(world, turn_state, BattleEndInput, rng, context) -> BattleEndReport`
- **Work が渡す入力**:
  - `battle_id`: 重複検出のキー。
  - `result_flag`: 0 か 1（生の値）。
  - `caller_va`: 上の表のどれか。
  - `gm_mode`: GM+0x1EEC3C の値。
  - `war`: `WarState`。目標、防衛・攻撃の勢力、`attack_map`（出発 spot と def 名）、`help_map`（spot, 勢力, byte）、`temp_defs`（GM+0x1EEC00）。
  - `sides`: 3陣営の `BattleUnitState`。def は def マップ上の**同じオブジェクト**でなければならない。
  - `unit_credit_1b4`: 終了時点で登録されている Unit の、名前と +0x1B4 の組。
  - 共有 def 上で Work が書いておくもの: `killed_1b0`（0x588470 の結果。0x57897B が書く）と、必要なら `escape_spot_1b4`（def+0x1B4）。
- **Claude が更新する状態**:
  - def の Lv / EXP（vf05 → 0x575110 は **この API の中でだけ**実行する。Work は LvUp を別に呼ばない）。
  - 忠誠、+0x174、+0xBC。
  - def の破棄と後継。
  - spot の集合、勢力の +0x64 / +0x5C / +0x108 / +0x118 / +0x128。
  - 変数（`@frd_`、`@war_`、`@battle*`）。
  - ctx+0x50 / +0x54。
- **返り値** `BattleEndReport`: 段階の一覧、levels、deleted（0x463590 の順）、promoted、loyalty、payments、ui_events（GUI だけ）、player_def_lost、frame_rate、rng_draws。
- **保証すること**（2026-10-12 更新。詳細は §68.7）:
  - 先に deep copy 上で全体を実行する。対象は world・turn state・入力・rng・**context**（registries だけ共有、読み取り専用）。Gap（VERIFY）などの例外が出たら、world・turn state・rng・**context の初回読み込みキャッシュ**のどれも変えずに例外を返す。Work 側でコピーを作る必要はない。
  - 成功したら、呼出側のオブジェクトをその場で更新する（world / def / spot / power のオブジェクトは差し替えない）。context のキャッシュには、原作が初回読み込みで入れるのと同じキーだけが増える。
  - 同じ `battle_id` を2回渡すと `BattleEndDuplicate`（何も実行しない）。
  - Unit の def が def マップのオブジェクトと違えば拒否する（identity の確認）。
  - LvUp は1回の呼出の中で1回だけ行われる。
- **VERIFY として拒否するもの**（2026-10-12 時点）:
  - ~~0x434EB0~~ → **実装済み**（`found_power_434eb0`。67.3b の記述を §68.8 で更新）。
  - 0x5AC1A0 で、2つ以上のリンクを shuffle する場合（`LINK_ORDER_VERIFIED = False`。リンクベクタ +0x8C の順序が未確認なので、shuffle 結果を決められない）。リンクが1本以下なら実行する。
  - 同じ +0xC0 / +0xE4 による並べ替えの同値。ただし `WarState.map_order == "RANKED"`（攻撃・援軍マップの順を呼出側の rank で決めたもの。COMPAT / SYNTHETIC）なら、+0xC0 の同値はその順で処理し、stages に `ranked-map-order(COMPAT)` を残す。
  - 援軍マップの不整合、ctx+0x58 の勢力のお金。
- テスト（SYNTHETIC）: 6件。
  - フラグ 0。
  - 拒否時に状態が変わらないこと、重複、identity。
  - 盟主が死んで勢力が滅亡する場合の拒否。
  - 援軍への支払い。
  - 中立 spot の占領。
  - 撤退（リンク順を仮定）。

### 67.3b 追加の移植（同日）
- **0x497BB0（生存したまま離脱する def）**: CONFIRMED、実装済み（`unit_leaves_497bb0`）。
  - +0x1B0 がなく 0x585E00 が真の場合、+0x77 は「自決」、+0x75 は「殉死」になり、X（+0x74 の処理、破棄）へ進む。
  - それ以外は離脱する。
    - +0x77 は配下を全員外す。+0x75 は、flag 0 かつ +0x78 なら +0x7A の配下だけを残し、そうでなければ全員外す。
    - +0x74 でなければ "arbeit"（0x585890: text と number）を見る。text が空、または number ≠ 0 なら、+0x7C = (0x40ED80(0,100) < number)。rand を1回使う。
    - 0x460E90(spot) で放浪させる。
    - +0x77 かつ +0x74 なら 0x4692C0（ctx+0x54 の勢力の +0x1D = 0、ctx+0x54 = 0）。
  - **0x585E00**: "loyal" を見る（0x585890。項目リストの先頭 `名前*N`。text の読み方は STATIC_HIGH）。
    - 名前が空、または N == 0 なら偽。
    - +0x77 なら、名前が自分のときだけ抽選する。
    - それ以外は、所属勢力の盟主名が名前と一致しなければ偽。+0x74 で power+0x60 ≠ 0x80000008 なら偽。盟主の def が無いか +0x1B0 なら抽選、そうでなければ偽。
    - 抽選: N > 0x40ED80(0,100)。
  - 補助関数: 0x585CA0 = (+0x77 または +0x75)、0x41DED0 = 文字列が異なる、0x416920 = 文字列が等しい、0x406E30 = 一時文字列の破棄。
- **0x4973E0（勢力の滅亡）**: CONFIRMED、実装済み（`power_destroyed_4973e0`）。
  - 0x46CBD0: `@beit_`+勢力名 の各レコードについて、その def の +0xA0 文字列を空にし（+0xB0 = 0）、変数を消す。
  - プレイヤーの勢力なら、ctx+0x54 を解除する。+0x1C = 0。
  - +0x64 を写してから空にする。各 spot について、0x597F40 の一覧のうち +0x7A でない def に +0x1B0 = 0 とし、0x497BB0(flag 0, ECX NULL) を呼ぶ。その後 spot の集合を空にする。
  - 最後に 0x460940（中立部隊の再配置。rand を使う）。ctx+0xC は入力 `spot_capacity_0c` で受け取る。
  - **0x597F40**: spot の "politics" が on でなければ、0x597D50 の各隊長の後にその配下を並べる。on なら集合の全員。
- **0x434EB0（放浪者が勢力を作る）**: 〔2026-10-12 訂正: その後 0x468A70 / 0x471E00 / 0x587470 も解析し、**実装済み**（`found_power_434eb0`）。範囲は §68.8〕以下は当初の記録。
  - 新しい勢力は ctor 0x590560 で作り、0x590F90 で初期化する。
    - 名前 = 本人の名前 + "@np"。+0x1C = 1、+0x1D = 本人の +0x74、fix = 0。
    - master = 本人。money = 本人の +0x174。+0x64 = {目標}。
    - +0x40 = 0x5917B0。その後 0x593890（性格、rand）。
  - 続いて 0x468A70（登録）、0x471E00（手番へ追加）、0x460F10。
  - 本人: +0x77..+0x7A = 1,1,0,0、+0x174 = 0、+0xC0 = 100、+0xA0 = ""、+0x80 = 0。部隊全員の +0x7A = 0。
  - 本人が +0x74 でなければ、+0x77 / +0x75 の配下を独立させる: +0x78 = 1、+0xC0 = 0x587470、勢力の money += 配下の +0x174 として、本人の +0xD4 から外す。
  - 最後に 0x5924B0。
  - 0x468A70 / 0x471E00 / 0x587470 は未解析。
- テスト（battle_end）: 8件。生存者の放浪、勢力の滅亡、出陣処理の末尾を追加した。

### 67.3c 出陣処理の末尾（0x490590 の 0x491666..0x491816、CONFIRMED、実装済み）
- 戦闘の場面へ移る直前に、次の順で処理する。
  1. 全 spot の +0xB8 を 0 にする。
  2. 攻撃マップを順に見る。
     - 出発 spot が help マップ（GM+0x1EED30）にあれば、GM+0x1EECB4 に積む。
     - そうでなければ、def を +0xE4 順に並べ、0x588170 を呼ぶ（本人と配下の +0xC8 = 現在のターン。§62 の訓練の判定が使う値）。def があれば GM+0x1EED5C を +1 し、0x5B0680 で行軍を表示する（GUI）。
  3. "battle" の場面へ移る。
- 実装: `war_dispatch_491666`。テスト1件。
- 〔2026-10-12 更新〕出陣の前半（0x48F9E0 / 0x4868D0 / 0x490180 / 0x488290 / 0x489630 / 0x489DB0 / 0x490590 の状態部分）は §68 で移植した。メッセージ・ダイアログは UI イベントとして記録するだけ。


> 原本1901〜1908行は部分回収の対象外（held_native_paragraph）。


<a id="f-68"></a>
## §68 戦争開始 0x48F9E0 系の復元、開始〜終了の接続、既存モデルの訂正（STATIC、実装済み）

### 68.1 既存モデルの訂正（CONFIRMED）
- **0x46B720（leg）**: 戻り値は生の値ではない。NULL 勢力なら 0。`@leg_`+min+max を find-or-create し（同じ勢力どうしでも特別扱いしない）、−1 なら 0x7FFFFFFF、それ以外は max(v − turn, 0)（turn = GM+0x1EF4C8、0x46B874..0x46B888）。
  - 旧実装は生の値を返していた。影響: ターン末の友好度の減衰（0x4736DE..）と 0x47E3A0 の目標収集。テストの期待値はこの理由で更新した（leg 12 → turn 0/5/20 で 12/7/0）。
  - ターン末の呼出時点では、ターンはすでに +1 されている（0x472714）。
- **0x46BC80（敵対集合）**: 完全に移植した（`power_com_set(w, p, turn=)`）。
  - 返り値は静的な std::set<Power*>（0xB12400）。アドレス順なので、所属の判定だけに使う。
  - `@com_p` の各レコード r について（k2 = `@com2_p_r.text`）:
    - r.int ≤ turn、または相手勢力がない、または 0x591610 が偽 → r と k2 を全部消す。
    - k2 のレコードのうち、勢力が無いか 0x591610 が偽のものを消す（0x463DF0 の静的ベクタのスナップショットを回すので、消してもずれない。同じ text が2つあると解放済みノードを読むため Gap）。1つでも消したら、r.int = 残りの最大値。それが ≤ turn なら消す。
    - k2 が空なら消す。そうでなければ相手を集合に入れる。
- **0x5AAEC0**: mode 0 / 1 では、**引数の勢力**に名前（+0x10 = 長さ ≠ 0）が必要。ctx+0x58（名前なし）を渡すと何も追加しない（0x5AB1C9 / 0x5AB1F3）。`spots_within` を修正した。
- **0x597D50(spot, out, a, b)**: 集合の名前順に def を引き、+0x78 があるものを残す。a のときは、行動済み（0x588070）の def は「b かつ +0x74」の場合だけ残す。最後に **def+0xE4 で std::sort**（0x47BB50 / 0x530490）。
  - 戦闘終了側の `_spot_defenders_597d50` はこの並べ替えをしていなかったので修正した。+0xE4 が未知なら Gap。
- **0x588070（行動済み）**: def+0xC8 ≥ turn、または隊長（0x583DC0）の +0xC8 ≥ turn、または隊長の配下のだれかの +0xC8 ≥ turn。
- spot+0x8C: ctor と初期化で 0。スクリプト（0x4AC810）が書くが未モデル。`StrategySpot.castle_8c`。

### 68.2 0x48F9E0（戦争開始、ECX = 目標 spot、引数 = GM, 元の攻撃マップ）
1. 城の判定 0x597860: spot+0x8C == 0 なら spot の "castle_battle" == "on"、そうでなければ +0x8C == 1。結果を GM+0x1EED40/41/42 に入れる。城でなければ +42 = "maze_battle" == "on"。
2. GM+0x1EEBAC / +0x1EEBBC のベクタ、+0x1EEC2C の集合、+0x1EED5C、ターン処理の集合 +0x78 / +0x88 / +0x98 / +0xA8 を空にする。
   - 消すのは [scene+0x10] の集合、追加するのは [GM+4]+0x1EF4B4 の集合。両者を同じオブジェクトと見なしている（STATIC_HIGH）。
3. GM+0x1EECC4 = spot の map（+0x2C）。空なら "test"。GM+0x1EED18 = 0、+0x1EED1C = 目標。援軍マップを空にし、攻撃マップ = 元のマップの写し（0x498E60）。
4. actor = 0x48F720: 攻撃マップを順に見て、援軍マップに無く def 集合が空でない最初の項目の、**集合の先頭 def（アドレス順）**。
   - 候補の def の勢力・放浪・+0xB0 が全部一致しない場合は Gap。
5. 防衛勢力 = 0x597B00(目標)、攻撃勢力 = 0x583C70(actor)。UI（カメラ、「$$$へ攻め込みました」）。防衛勢力に名前がなければ +40 = 0。
6. 目標の隊数 > 0 で actor が放浪中でなければ、0x4868D0(…, flag 0)。真ならプレイヤーのダイアログ 0x52DE20 へ進む（ここで止まる）。
7. 偽なら 0x490180（68.4）。

### 68.3 援軍の選定
- **0x4868D0**（同盟国の援軍。turnproc, target, war, help, defP, attP, flag）:
  - N = 0x5AAEC0(目標, defP, mode 1, support_range)。集合の順（VERIFY）を写して random_shuffle。
  - 各 spot c（隊数 > 0、所有者 q に名前、q ≠ attP）について:
    - leg(attP, q) > 0（攻撃側）:
      - leg(defP, q) > 0 なら、attP がプレイヤーのときだけ続ける（両方と同盟）。
      - 距離 d = 経路探索（attP と q の spot と目標だけを通る）。d == 0 か d > support_range なら次へ。
      - defP が 0x46BC80(attP) と 0x46BC80(q) の両方に入っていなければ次へ。
      - attP がプレイヤーで flag 0 → 結果を真にする。両方と同盟、attP がプレイヤー、flag あり → q を +0x88 / +0x98 へ。そうでなく q がプレイヤー → 結果を真。それ以外は 0x489630。
    - そうでなく leg(defP, q) > 0（防衛側）:
      - leg(attP, q) > 0 なら、defP がプレイヤーのときだけ続ける。
      - 経路は defP と q の spot。距離の判定は同じ。
      - defP がプレイヤーで flag 0 → 結果を真にして次へ（参加しない）。両方と同盟、defP がプレイヤー、flag あり → q を +0x88 / +0x98 から外す。q がプレイヤー → 結果を真。それ以外は 0x489630。
  - 最後に（flag 0 なら）0x46C940(attP) の傭兵（`@beit_`）。レコードがあれば Gap。
- **経路探索**（0x4868D0 と 0x488290 で同じ）:
  - 出発 == 目標なら −1。FIFO に (要素, d) を積み、積む時点で訪問済みにする。目標を取り出したら d を返す。キューが尽きたら 0。
  - SpotEscapePath は捨てる。SpotPath は d のまま積む。spot は、許可集合（勢力の +0x64 と目標）にあるとき d+1 で積む。
  - このモデルの地図は spot–道–spot の二部グラフなので、リンクの順序によらず結果が決まる（道どうしのリンクがあれば Gap）。
- **0x488290**（自軍の援軍。turnproc, target, war, help, defP, attP）:
  - N = 0x5AAEC0(目標, defP, mode 0, myhelp_range) を shuffle する。
  - 隊数 > 0 の spot について、defP の spot を通る経路で d を求める（0 か > myhelp_range なら次へ）。
  - defP がプレイヤーなら結果を真にして次へ。そうでなければ 0x489630(q = defP)。
  - 最後に 0x46C940(defP)。
- **0x489630**（q が c から兵を出す。this = attP）:
  - 側 s = (leg(q, defP) > 0 または q == defP)。
  - s かつ q ≠ defP のとき、attP が 0x46BC80(defP) と 0x46BC80(q) の両方にあれば続ける。なければ 0x489DB0 が偽なら終わり。
  - limit = 0x80000008（上限なし）。q == defP なら:
    - A = 目標の防衛隊（0x597D50(目標,0,0)）の 0x587FA0 の和 + 援軍マップで側 ≠ 0 の項目。B = 残りの攻撃マップ。
    - r = rand()。x = chop(r/32768 × (100 − kosen(q)))。limit = chop((x×0.04 + 1) × B + 0.5) − A。負なら終わり。
  - 0x593AC0(q)（勢力の "supportable" ≠ off かつ盟主ユニットの "supportable" ≠ off）が偽なら終わり。
  - cap = 1000。c = war_capacity − (q == defP なら目標の隊数) − (q の援軍項目にある def の数)。c < 1000 なら cap = c。c ≤ 0 なら終わり。
  - G = 0x597D50(c, q == defP, 0) を shuffle する。i < |G| かつ i < cap の間、G[i] を取る。limit があるときは、0x587FA0 の和が limit を超えたところで止める（超えた隊も含む）。
  - 1隊も取れなければ終わり。取れたら c+0xC0 = 1000000。攻撃マップに (c, 集合)、援軍マップに (c, q, s) を入れる（どちらも上書きしない）。
- **0x489DB0**（q が防衛側を助けるか）:
  - leg(q, attP) > 0 なら、defP がプレイヤーのとき q を +0x88 と +0x98 に入れ、偽を返す。
  - A = 目標の防衛隊の和。攻撃マップの項目は、援軍の側 byte が 0 なら B、無いか ≠ 0 なら A に足す。
  - defP がプレイヤーでなければ:
    - k = kosen(defP)。a = chop(k×0.25 + 0.5)。r = rand()。b = chop(k×0.75 + 0.5)。c = chop(r/32768 × (b − a))。
    - y = chop(int32((c + a) × A) × 0.01 + 0.5)。y > B なら偽。
  - C = 0x597D50(c,0,0) の和。s = "diplo_success_sup"（2000）。thr = s/4 + chop(rand()/32768 × (s − s/4))。
  - w1 = (100 − yabo(q))×0.1 + 1。mc = 盟主(defP)+0xC4 × 0.01。h = (frd(defP,q) + 150 − frd(attP,q)) / 2（C の除算）。
  - z = chop((C + A) × w1 + 0.5)。score = chop((h×10 + z/B×1000) × mc + 0.5)。B == 0 なら inf / NaN になり 0x80000000。
  - score ≥ thr なら q を +0x78 に入れて真。
  - そうでなければ、defP がプレイヤーなら q を +0x88 へ。q が +0xA8 に無ければ、f = frd(defP, **defP**) > 0 のとき clamp(f − diplo_frd_down(10)/2, 1, 100) を設定する。
    - 0x48A2CB で EDX = ECX = defP なので自分との友好度になる（通常は番兵値で、何も起きない）。原作どおりに移植した。
  - q を +0xA8 に入れて偽。

### 68.4 0x490180 と 0x490590
- **0x490180**:
  - 目標の隊数 > 0、defP に名前、actor が放浪中でなければ 0x488290。
  - +0x88 にあって +0x78 に無い勢力ごとにメッセージを出す（+0x98 にあれば「同盟中なので援軍を拒否」、なければ「援軍を拒否」）。順序は集合のアドレス順。
  - 0x488290 が真ならダイアログ 0x52E9E0 へ進む（ここで止まる）。そうでなければ 0x490590。
- **0x490590**（0x491666 の手前までの状態部分）:
  - H = (ctx+0x54 も ctx+0x50 も NULL) ? 0x469170（`@hero` を find-or-create して def を引く）: NULL。
  - defP がプレイヤーなら 54。そうでなければ、0x597F40(目標) の各 u について: +0x74 → 54、u == H → 56（どちらも見つけたら止める）。
  - まだ決まらなければ:
    - attP がプレイヤーなら 55。
    - そうでなければ、攻撃マップの各 def とその配下について: +0x74 → (側 ? 54 : 55)、== H → 56。
    - そのあと、援軍マップの勢力がプレイヤーなら (側 ? 54 : 55)。
  - (GM+0x1EED44, +48) = 54 なら (+0x1E8630, +34)、55 なら (+34, +30)、それ以外は (+34, +38)。
  - +0x1EED43（戦闘画面を省略するか）= (54 または 55) ? !"@config@player_battle"（既定 on） : !"@config@enemy_battle"（既定 off）（0x5657F0）。
  - プレイヤーの def P（ctx+0x50）、かつプレイヤー勢力なし（ctx+0x54 NULL）の場合に P+0x79 = 1 になる:
    - 55、P の勢力 == attP、turnproc+0x38 ≠ 0、攻撃マップが1件、0x585FD0(その spot, P)。
    - または 54、P の勢力 == defP、0x585FD0(目標, P)。
    - 0x585FD0: P に +0x77 がなく +0x80 ≥ 1 で、0x597D50 を 0x582750 で並べ替えた先頭が P。
  - そのほかの分岐はメッセージだけ。
  - F54 か F55 なのに ctx+0x50 が NULL だと、原作は 0x583A80(NULL) を呼ぶ。Gap にした。
- 続いて既存の 0x491666 の末尾（§67.3c）。

### 68.5 公開 API（`peer_script01_war_start.py`）
- 呼び出し: `begin_war_48f9e0(world, turn_state, target, attack: tuple[AttackEntry], rng, context, settings, *, player_battle=True, enemy_battle=False, elem_rank=None, spot_rank=None) -> WarStartReport`
  - `attack`: 元の攻撃マップ 0x8BA6F4（AI か UI が作る）。
  - `settings`: `scenario_world_settings` の結果（war_capacity と3つの range）。
  - `elem_rank` / `spot_rank`: SpotElm* / Spot* のアドレス順の代わりに使う順位。渡さなければ、順序に依存しない場合だけ通す。
- `WarStartReport`:
  - `war`（WarState。`map_order` は spot_rank があれば "RANKED"）。
  - `stage`: `DISPATCHED`、`PLAYER_DIALOG_52DE20`、`PLAYER_DIALOG_52E9E0`。
  - そのほか castle/maze、map_name、actor、`involvement`（54/55/56/43/44/48、+0x79）、`dispatch`（0x491666）、ui_events、rng_draws。
- **トランザクション**: world / turn state / rng / context の deep copy で先に実行する。例外が出たら何も変えない。成功したら、呼出側のオブジェクトをその場で更新する。
- ダイアログの段階では、原作がダイアログを開く時点の状態（すでに参加した援軍、使った乱数）を残して止まる。ダイアログ後の続き（0x52DE20 / 0x52E9E0）は未移植（VERIFY）。
- Work への流れ: `begin_war_48f9e0` → `report.war`（と `involvement.auto_43` / 陣営オブジェクト）→ 戦闘 → `BattleEndInput(war=report.war, …)` → `apply_battle_end`。

### 68.6 マップ要素の順序（調査のまとめ）
- 現状:
  - std::set<SpotElm*> と std::map<Spot*, …> は**ヒープアドレス順**。
  - SpotElm は operator new(0x36C)（0x4A2F8D / 0x48C1D2）、Spot は 0xD0。CRT ヒープは HeapCreate(0, 0x1000, 0)（0x5BD052）。LFH を明示しておらず、HeapSetInformation は破損時終了の設定だけ（0x5B84FC）。
  - Windows 7 以降は LFH が自動で有効になり、Windows 8 以降はその割当がランダム化される。そのため、静的なデータからアドレス順は再現できない見込み（推論。実機での観測で VERIFY）。
- RNG と AI への影響:
  - random_shuffle の入力順が変わると、同じ乱数列でも結果が変わる。0x4868D0 / 0x488290 の N、0x47E3A0 の目標、0x461DA0 の放浪がこれに当たる。
  - 攻撃マップの順は、0x493630 での +0xC0 の同値の扱いと、0x491666 の処理順を左右する。
  - 援軍の spot は +0xC0 = 1000000 で同値になるので、援軍が2つ以上あると必ず順序が必要になる。
- 方針:
  - 原作準拠としては固定しない。
  - 互換の方針として、生成順（`compat_creation_order_rank`）を呼出側が明示的に選べるようにする。その結果は COMPAT と表示し、GOLDEN / MATCH には数えない。
  - 新エンジンが論理 ID を使う場合の差: 乱数の消費回数は同じで、選ばれる順だけが異なりうる。
- 必要な観測: 実機で戦争開始の直前と直後のセーブを取り、援軍の決定結果と乱数の状態を突き合わせる。または、デバッガで 0x5AAEC0 の出力集合を記録する。どちらもユーザーが実機で行う必要がある。

### 68.7 apply_battle_end / begin_war_48f9e0 の失敗時の保証（Work からの依頼への回答）
- 以前は、事前検証で context（0x46F4C0 の初回読み込みキャッシュ）を共有していた。現在は **context も deep copy して事前検証する**。
- 例外が出た場合は、context.cache を含めて何も変わらない。成功した本実行の途中で例外が出ることは、同じ入力の事前検証が通っている以上ありえないが、念のため cache を元に戻してから再送出する。
- **Work 側のコピー隔離は不要**（残しても結果は同じ）。
- テスト: `test_gap_is_transactional`（cache 不変）、`test_battle_end_failure_keeps_context`。

### 68.8 0x434EB0 と 0x5AC1A0 の実装範囲（§67 との整合）
- **0x434EB0**: 実装済み（`found_power_434eb0`）。flag 1 で、放浪者の戦争に勝ち、本人が生きている場合に呼ばれる。
  - 新しい勢力（名前 + "@np"、盟主 = 本人、money = +0x174、+0x64 = {目標}、+0x1D = 本人の +0x74）を作る。
  - 0x593890（rand 1回）→ 0x468A70（登録と外交の初期化。同名で生きている勢力がいれば Gap）→ 0x471E00（手番に追加）→ 0x460F10。
  - 本人と配下のフラグ、配下の独立（忠誠 = 0x587470）、0x5924B0。
  - 元の所有者は目標を失う。表示名 +0x40（0x5917B0）とメッセージは未モデル。
  - 未確認: 0x468A70 で、同名の勢力がすでにある場合の扱い。
- **0x5AC1A0**: 実装済み（`escape_spot_5ac1a0`）。ただし、展開する要素のリンクが2本以上あると、shuffle の入力順（リンクベクタ +0x8C の順）が未確認なので Gap（`LINK_ORDER_VERIFIED = False`）。リンクが1本以下なら実行する。
- 攻撃・援軍マップの順: `WarState.map_order`（68.5）。"UNVERIFIED" のときは、順序に依存する場合を Gap にする。

### 68.9 テスト
- 新規 `tests/test_peer_script01_war_start.py`（SYNTHETIC）: 敵対集合の期限切れと滅亡、経路、行動済みの除外、AI どうしの戦争の全体、乱数の回数、Gap 時の不変（cache を含む）、COMPAT 方針、プレイヤーのダイアログ2種、プレイヤー防衛時の判定、プレイヤー def の指揮（+0x79）、放浪者の戦争、支援の判断（0x489DB0）、**戦争開始 → 合成の戦闘結果 → apply_battle_end の統合テスト**。
- これらはすべて SYNTHETIC の静的移植のテストで、原作での一戦の完走ではない。GOLDEN 0 / MATCH 0。

### 68.10 ターン末の友好度減衰の訂正（0x4736DE..0x473884、CONFIRMED）
- sup の減衰（diplo_sup_turndown）は、j が 0x46BC80(i) に**含まれる**ときに行う（0x4737AC: 見つかれば減衰）。旧実装は判定が逆だった。
- 隣接による減衰（diplo_frd_turndown）の条件:
  - leg(i, j) ≤ 0（0x46B720）。
  - i+0x118（和平の期限。§69 の 0x593D50 が書く）に j があり、値 ≥ turn なら減衰しない。
  - 0x4807E0(i, j)。
- テストの期待値 78/49/49 は逆判定から来ていたので、79/50/50 に改めた。和平で減衰が止まることも確認するようにした。

### 68.11 0x46C200 のレジスタ
- EDX = p（`@com_`+p と `@com2_`+p+"_"+q のキー）、ECX = 記録する相手（`@com2_` のレコードの text）。引数は (ctx, q, v)。
- シナリオ開始時は ECX = EDX = p。共闘の承諾（0x482DBC / 0x482DCC）では相手の勢力を ECX に渡す。
- `com_set(w, p, q, v, by=...)` に一般化した。

<a id="f-69"></a>
## §69 勢力 AI の外交 0x481260（STATIC、実装済み）

### 69.1 呼出位置
- GameCtrl::vf01 0x474F10 で、AI 勢力の手番の最初のフレーム（turnproc+0x50 == 0x80000008）に呼ばれる。
- 真を返したら、そのフレームは UI 待ちになる。偽なら 0x47E3A0 → (0x65C114 ? 0x47A1A0 : 0x47F670) → 0x476D60 へ進む。
- 2フレーム目以降は 0x4751C0（攻撃）と 0x47AE50 / 0x471E80（§70 以降）。

### 69.2 0x481260 本体
1. turnproc+0x50 = −1。p = order[phase−2]（範囲外なら NULL で、原作は異常終了するので Gap）。
2. turn % diplo_mode_itv(12) == 0 なら 0x593890（性格の引き直し、rand 1回）。
3. 盟主の +0x74（プレイヤーの人材）または 0x593960 が偽なら終了。
   - 0x593960: 勢力 "diplomacy" ≠ off かつ 盟主ユニット "diplomacy" ≠ off。
4. 予算 = 0x480B20:
   - x = chop(rand/32768 × kosen)。
   - chop(diplo_budget_per(33)×0.01 × money × (100−x)×0.01 + 0.5)。
   - ctx+0x54 が無く ctx+0x50 があり、0x592CE0（プレイヤーに関係する勢力）なら半分にする（C の除算）。
5. 候補 L = 0x4837E0。空なら終了。
6. L の各 q について:
   - p+0xB0[q] ≥ turn ならとばす。
   - cost = 0x593C20(q) = chop(収入(q) × diplo_cost_per(10)×0.01 + 0.5)。予算 < cost ならとばす。予算から引き、0x593C70 で p+0xB0[q] = turn。
   - q がプレイヤーなら、0x480920(q, p) が偽のとき記憶して次へ。
   - frd(p,q) < diplo_bestfriend(80) → 0x480920 が偽なら 0x481F90（親睦）。
   - leg(p,q) ≤ 1 → 同じ条件で 0x481820（同盟）。
   - frd < 95 で（性格 3、または yabo < 0x40ED80(0,100)）→ 同じ条件で親睦。
   - それ以外は性格による共闘依頼（0x4826C0）:
     - 0: E = 0x4847D0(p, 0x484580(p,0), 1.0) の各 x について、0x480D80(q, p, x) なら依頼する。
     - 1: E = 0x4847D0(p, 0x484580(p,1), 1.0) の各 x に依頼する。
     - 2: 0x484580(p,1) の先頭に依頼する。
     - 3: 何もしない。
7. 記憶したプレイヤー勢力があれば、同じ順で1つ処理して真を返す（0x480920 の判定はしない。性格 0/1 は E の最初の1件だけ）。

### 69.3 補助関数（CONFIRMED）
- **0x480BD0**: p 以外の 0x591610 な勢力（名前順）のうち、leg < 0x7FFFFFFF のものがちょうど1つならそれを返す。
- **0x484580(p, adjacent)**: 静的ベクタを返す。
  - 0x480BD0 があればそれ1つ。なければ 0x484970（突出勢力）が p 以外で leg < MAX ならそれ1つ。
  - それ以外は、名前順の候補（adjacent なら 0x4807E0(p,q)、leg ≠ MAX）について +0x104 = 0x592F10 とし、0x484C40 で得点を付け、+0x100 の昇順に std::sort（0x484D80。0x47BB50 と同じテンプレート、STATIC_HIGH）。入力が名前順なので、同点でも順序は決まる。
- **0x484C40（得点、結果は +0x100）**: leg == MAX なら MAX。そうでなければ:
  - A = frd×10、B = 相性(盟主q, 盟主p)×10、C = +0x104 × 1000/max。
  - 性格 2: X = frd×C×0.01、A を2倍。
  - それ以外: X = C（flag 0 かつ性格 3 なら 1000 − C）。性格 0 なら X を2倍、性格 1 なら B を半分。
  - 得点 = chop((X + (B + A)) × d4 + 0.5)。d4 = `@mode_hostil` が 1 なら 1 − caution_adjust(30)×0.01×0.5、そうでなければ 1。
  - max == 0 のときは inf / NaN になり 0x80000000。
- **0x4847D0(p, V, factor)**:
  - s = 0x592F10(p)。性格 0 なら rand 1回で s = chop((x×0.01+1)×s+0.5)。s = chop(s×factor+0.5)。
  - V を前から set に入れ、s から強さを引く。s ≤ 0 か性格 3 なら止める。
  - **結果は std::set<Power*>（アドレス順）**。
- **0x4837E0（外交の相手）**:
  - S1 = 0x484580(p,1)。空なら S1 = S0 = 0x484580(p,0)。S1 が空なら [] を返す。
  - 乱数フラグ = chop(yabo×0.5+0.5) > chop(rand/32768×100)。E1 / E0 = 0x4847D0。
  - 第1部: E1 の各 e（集合の順。共有の訪問済み集合があるので順序依存）で frd(p,e) < bestfriend のものについて、e の spot の外側の隣接 spot の所有者 q を調べる。
    - 性格による除外: 0 は E1 / E0 に無いこと、1・2 は E1 に無いこと。
    - 相性 > compati_bad(0)、frd ≠ 0。
    - 性格と |S1| と乱数フラグに応じて 0x4807E0(p,e) / (p,q) を判定し、通れば候補にする。
  - 第2部: p 自身の spot の外側の隣接 q を同じ条件で加える（性格 0 は |S1| == 1 のときだけ）。
  - 候補集合 → ベクタ → +0x104、0x484C40(flag 1)、+0x100 の降順で sort。
- **0x480920(q, p)**: q の可視 spot に接する p の spot が2つ以上あり、p の領内で互いにつながっていないものがあれば真（p を分断している）。
- **0x480D80(a, b, c)**: b の本拠（0x5937D0）から、b 以外の spot を通るたびに 1 を加える緩和探索を行う。c の spot に a の support_range+1 以内で届けば真。
  - 0x5937D0: event 勢力なら最初の spot。そうでなければ盟主 def の spot（0x583CF0）、無ければ最初の spot。

### 69.4 3つの提案
- **0x481F90（親睦）**:
  - q がプレイヤーなら、ダイアログ（金 = 0x593C20(q)）を出す。保留として返す。
  - AI の場合:
    - thr = s/4 + chop(rand/32768×(s − s/4))。s = diplo_success_frd(2000)。
    - 得点 = chop(((相性×10 + frd×10) + g/sq×500) × 盟主(p)+0xC4×0.01 × k3 + 0.5)。g = chop(強さ(p)×w1+0.5)、w1 = (50 − (盟主qの yabo+kosen)/2)×0.01 + 1、k3 = q の性格 3 なら 1.5。
    - leg > 0 なら得点を2倍。得点 > thr なら、q の性格 3 は承諾、それ以外は「p が 0x4847D0(q, 0x484580(q, 性格≤1)) に無い」ときに承諾。
  - q+0x118[p] ≥ turn（和平中）または承諾:
    - 金を p から q へ。0x593D50 で p+0x118[q] = turn + diplo_frd_peace(2) − 1。
    - frd = min(f + diplo_frd_up(20), 100)。
  - 拒否: frd = max(f − diplo_frd_down(10), 1)。
- **0x481820（同盟）**:
  - s = diplo_success_leg、閾値は s/2 から。条件は frd ≥ max(bestfriend,1)。q の性格 3 は 0x480BD0(q) が NULL のときに承諾する。
  - 承諾: 金を移し、leg ≠ MAX なら leg = turn + diplo_league_up(6)。拒否しても frd は変えない。
- **0x4826C0（共闘、ECX = q、引数 p, x）**:
  - leg(p,x) > 0 なら偽。
  - プレイヤー q: x が 0x46BC80(q) と (p) の両方にある場合は除く。0x480D80(p,q,x) が真ならダイアログを出し、turnproc+0x74 = q。
  - AI q: 条件は leg(p,q) > 0、diplomacy、leg(q,x) ≤ 0、frd(q,x) < bestfriend、上の集合の判定、0x480D80。
    - そのうえで 0x4847D0(q, 0x484580(q,0), 性格3なら1.5 そうでなければ5.0) を呼ぶ。結果は捨てるが、rand は使う。
    - x が 0x484580(q,0) にあれば承諾。
  - 承諾: 金を移し、0x46C200 を (EDX=p, ECX=q) と (EDX=q, ECX=p) で、期限 turn + diplo_sup_up(6) にして呼ぶ。

### 69.5 新しい状態フィールド
- 勢力:
  - +0xB0 `diplo_b0`（相手ごとに最後に外交したターン）。
  - +0x118 `map_118`（和平の期限ターン）。
  - +0x100 `strength_100`（強さまたは得点。0x484970 と 0x484C40 が同じ場所を使う）。
  - +0x104 `strength_104`。
- turnproc: +0x50 `ai_index_50`、+0x64 `ai_flag_64`、+0x74 `common_74`。

### 69.6 順序と保留
- Power* のアドレス順が必要な場所:
  - 0x4847D0 の結果を回すところ（0x481260 の性格 0/1、0x4837E0 の E1）。
  - 0x4837E0 の候補で得点が同じ場合。
- これらは `power_rank` を渡すか（COMPAT: `compat_power_creation_rank`）、Gap にする。
- プレイヤーへのダイアログ（親睦・同盟・共闘とその拒否）は `rep.dialogs` に保留として返す。回答後の処理は未移植（VERIFY）。
- 履歴 0x43FAA0（種類 0x29 / 0x3D / 0x3E / 0x3F）は `rep.log` に記録するだけ。

### 69.7 テスト
- `tests/test_peer_script01_power_diplomacy.py`（SYNTHETIC）13件。
- 内容: 0x480BD0、費用と予算、敵の並べ替え、分断と到達、0x46C200(by)、和平による親睦承諾、拒否による友好度の低下、同盟の承諾、プレイヤーへの保留、共闘、本体（COMPAT 順位）、決定性、手番なしの Gap。
- GOLDEN 0 / MATCH 0。

<a id="f-70"></a>
## §70 勢力 AI の配置換え 0x47A1A0 と def+0xE8（STATIC、実装済み）

### 70.1 フレームの流れ（GameCtrl::vf01 0x474F10、CONFIRMED）
- 現在の勢力 = 0x471DC0。+0x1C が 0 なら 0x471E80（次の勢力へ）。
- **turnproc+0x50 < 0（手番の最初）**:
  - 0x591610 が偽なら次の勢力へ。
  - +0x50 == 0x80000008 なら 0x481260（§69）。真ならそのフレームは終わる。
  - 0x47E3A0 → (0x65C114 ? 0x47A1A0 : 0x47F670) → 0x476D60。
  - 0x476D60 が偽なら +0x50 = 0、+0x64 = 1。
- **2フレーム目以降**:
  - +0x64 が立っていれば、+0x50 = 0 として 0x47E3A0 と 0x47A1A0 / 0x47F670 をやり直す。
  - その後 +0x64 = 0x4751C0()。+0x50 == 0x80000008 になったら 0x47AE50 → 0x471E80。
- 0x65C114 = (`@mode_nozone` == 1) または zone のリスト ctx+0x33C が空（0x45C8A8）。

### 70.2 0x47A1A0（配置換え、nozone の経路）
1. 目標リスト turnproc+0x40 が空なら何もしない。
   - プレイヤーの勢力は turnproc+0xB / +0xC 次第（未モデル、Gap）。fix == 3（hold）なら何もしない。
2. y = yabo(p)。U = 0x593090(p):
   - 自 spot（名前順）の集合（名前順）にいる +0x78 の def を集める。
   - 各 def に +0x1BC = その spot、+0x1C8 = 0x587FA0 を書く。
3. 並べ替え:
   - rel = 0x592CE0(p)。rel かつ性格 > 1 なら random_shuffle。そうでなければ +0x1C8 の降順に std::sort（0x47E300）。
   - rel のとき: k = trunc(|U|/4)。プレイヤーの def（ctx+0x50）が U[k] より後ろにあれば、0x40ED80(0,k) を1回引き（**結果は使わない**）、U[k] と入れ替える。
4. L = A0, B0, A1, B1, …（A = def+0xE8 が立っている def、B = それ以外）。
5. **自 spot の +0x1C 集合を全部空にする。** 可視の spot を V（とその写し V2）にする。lim = ctx+0xC（spot_capacity）。
6. L が空になるまで、目標 t = T[i]（i は巡回）について:
   - V が空なら V = V2、lim = 0x7FFFFFFF。
   - N = t の隣の自 spot（0x5AAEC0 mode 0, 1。集合の順）。
   - 必要量 need:
     - coef = (t の所有者がプレイヤー ? 1.0 : 0.5) + rand/32768 × yabo×0.01。
     - need = chop(0x597C90(t) × coef + 0.5)。
     - p+0x108[t] が2ターン以内なら need = chop(need×4+0.5)。
     - yabo > chop(rand/32768×100) なら need /= max(|N|,1)（C の除算）。
   - N から V に無い spot を除く。空になったら、N = V を spot の gain の降順に sort したもの（0x479F60）。
   - N の各 spot s について（spot ごとに need をはじめから使う）:
     - cnt = 0x597A50(s)。lim ≠ MAX なら lim = s の capacity。
     - cnt < lim の間、次をくり返す:
       - L のうち +0x1BC == s の最初の def。なければ 0x479F90(+0x1BC, s) が真の最初の def（この場合は 0x588170 で +0xC8 = turn）。
       - どちらも無ければやめる。
       - def と配下を s+0x1C に入れ、need −= +0x1C8、cnt += 1。need ≤ 0 ならやめる。
     - cnt < lim でなにか置けたときだけ、s を V に残す。
   - i += 1。
- **0x479F90**: spot 要素のラベルを map にキャッシュする。
  - 両方にラベルがあれば、等しいかどうかを返す。
  - そうでなければ原作は 0x5AD6C0(elem(to), elem(to), 1) を呼ぶ（0x47A012 と 0x47A01E がどちらも to を読む）。これは常に真なので、ラベルのない方に相手のラベル（両方無ければカウンタ値、カウンタ +1）を付けて真を返す。偽の分岐には到達しない。
- 無限ループの見張り: 置けない def が残ると原作は止まらないので、上限を超えたら Gap にする（`max_rounds`）。

### 70.3 def+0xE8（前線フラグ、CONFIRMED）
- ctor では 1（0x582C45）。
- 0x583830 が設定する。呼ばれるのは 0x582D90 の 0x583373（enable の rand のあと、0x58AFA0 の前）と 0x460E90。
  - unit "line"（0x585AD0）が空でなければ "back" 以外のとき 1。
  - 空なら、最初のスキル（+0xEC）のレコード +0x40 == 1（func "sword"、0x59CB4D）のとき 1。スキルが無ければ 0。
  - スキル func → +0x40: sword 1、missile 2、heal 3、summon 4、charge 5、status 6、それ以外 0。
- 実装: `NativeDefinition.line_e8`、`def_line_583830`。
  - 0x460E90（`roam_definition`）は regs を受け取って計算する。+0x79 も 0 にする（以前は漏れていた）。
  - レコードの無いスキルは None（VERIFY）とし、0x47A1A0 で Gap にする。

### 70.4 ACTUAL データでの実行（COMPAT、GOLDEN ではない）
- sci1 の初手、全 AI 28勢力について、0x481260 → 0x47E3A0 → 0x47A1A0 を COMPAT 順位（SpotElm / Power の生成順）で実行した。28勢力すべて Gap なく完了した。
- 外交の候補は全勢力で空だった。開始時点では隣接する他勢力がなく、性格の条件を満たさないため。
- テスト: `tests/test_peer_script01_power_ai.py`（SYNTHETIC）5件。

<a id="f-71"></a>
## §71 勢力 AI の雇用 0x476D60 系（STATIC、実装済み）
実装: `peer_script01_power_hire.py`。テスト: `tests/test_peer_script01_power_hire.py`（SYNTHETIC 14件）。

### 71.1 0x476D60（入口）
- p = order[phase−2]。room = ctx+0x14（max_unit）− 0x592FE0(p)。0x592FE0 は p の各 spot の +0x1C 集合の大きさ（配下も含む）の合計。room ≤ 0 なら偽。
- U = 0x593090(p)。0x4771F0 が真なら真を返す（プレイヤーへの確認ダイアログ）。
- U を 0x476D20 で std::sort（+0x1D0 昇順、同値なら +0x1C8 降順）。
- C = 0x593E90(p) ＋（p の spot の "merce" と "monster" の名前の set、バイト順）。空でなければ random_shuffle。
- 君主（0x5916E0）が U にあれば U[0] と入れ替える。0x478F50(room, U, C) → 0x4780D0(room, C, U) → 偽。
- 0x593E90: 勢力 +0x90 merce を写す。"@@" があれば1つ消して印を付ける。印が無く空でなければそれを返す。そうでなければ君主の unit "merce"（@scen）を足し、class(君主).fkey が空でなく、class(fkey).unique が "on" でなく、class(fkey).race が空か君主と同じなら fkey も足す（以前の要約の「unique == on で追加」は逆だった。訂正）。

### 71.2 0x4771F0（放浪人材の登用・傭兵契約）
- L = U のうち +0x77 か +0x75。各リーダー l について（room > 0 の間）:
  - 領域 = 0x5AC880(elem(0x583CF0(l)), 1, 0) ∪ {l の spot}（set<Spot*>、アドレス順）。
  - 各 spot s で 0x4611E0(ctx, s, mode 1, 1): 放浪集合 ctx+0x32C（Def* 順）から、def+0x84 == s、+0xCC ≤ turn、かつ「0x583A80 かつ +0xB0 ≠ 0」でない def。各候補に +0x1BC = s。
  - 候補 r ごとの判定（不成立なら次の候補）:
    - r+0x74 かつ r+0xC8 ≥ turn → 次。
    - 0x583A80(r) で r+0x74 でない: 外交不可（0x593960 偽）なら 0x461750（立ち去り）。外交可なら rand 2回の判定（chop(rand×100/32768) > yabo(p) → 立ち去り。2回目 < yabo(r) かつ 0x484970 == p → 立ち去り）。
    - aff = 0x5878F0(r, 君主)。r+0x74 で p+0x60 ≠ SENT かつ turn−p+0x60 < leave_period(5) なら 0。aff ≤ compati_bad(0) なら（r+0x74 なら +0xC8 = turn）次。
    - 傭兵でなければ、r+0x1BC の 0x597A50 ≥ capacity なら次。
    - price = 0x585960(r,"price") + chop((100−aff)×0.01 × price × employ_price_coe(100)×0.01 + 0.5)。傭兵なら chop(arbeit_price_coe(33)×price×0.01 + 0.5)。
    - 資金不足で r+0x74 でなければ（傭兵なら立ち去り）次。0x586080(r, l) が偽なら次。
    - r+0x74: +0xC8 = turn、turnproc+0x6C = r、+0x70 = r+0x1BC、ダイアログ "employ_hero" → **真で終了**。
    - 傭兵: 0x46CD30（def+0xA0 = 勢力名、+0xCC = 0、"@beit_"+勢力 に (r, turn+arbeit_turn(3))）、+0x174 += price、+0x80 = 0、資金 −= price。次のリーダーへ（room は減らない）。
    - 登用: 0x460F10、r と配下を r+0x1BC へ、+0x78 = 1、+0x7A = 0、+0xBC = 0、+0xC0 = aff、+0x174 += price、+0x1D0 = spot+0xC0、+0x1C8 = 0x587FA0、+0xC8 = turn、資金 −= price、U に追加、room −= 1。次のリーダーへ。
- 0x5AC880（nozone）: 開始要素から BFS。SpotEscapePath は通らない。SpotPath はその先の要素に置き換える。開始点と同じ所有者（名前あり）の spot だけを進む。nozone では距離が常に 1（上限 1000）なので、結果は「開始 spot から自勢力の spot だけで繋がる成分（開始点を除く）」。zone の経路（0x46F020、0x65C11C/0x65C120）は未移植（Gap）。
- 0x5878F0(r, m): m NULL → 100。r+0x74 → 0x587470。m の名が unit(r).enemy にあれば 0。loyal 文字列 s: 空 → 0x587470。s が r 自身の名 → phase > 1 なら 0x587470、そうでなければ 0。def s が無い → 0x587470。s == m → 100。0x583C70(m) が名無し、または 0x583C70(s) と違う → 0。phase ≤ 1 で 0x583DC0 が違う → 0。それ以外 0x587470。
  - GM+0x1EF4EC は turnproc+0x38（phase）と確定（turnproc = GM+0x1EF4B4）。
- 0x586AB0(l, r)（phase ≥ 2 の分岐を移植。phase 0/1 は Gap）: F = 0x586320(l)。"male"/"female"/"neuter" による性別制限（def+0x70: 0x582D90 で "sex" = male 1 / female 2 / 他 0）。r の名が F にあれば真。r+0x74 かつ 0x5878F0(r,l) ≥ compati_vassal_bdr(50) で真。same_friend ≠ "off" かつ同種族で同クラス（A=class(l).fkey が空でなければ fkey 一致も可）なら真。F が空なら偽。"allrace" / "allclass" の分岐、最後の「クラス（または fkey）が F にあり、種族が同じか F にある」判定（same_friend == "off" なら両方 F で判定）。
- 0x586080(r, l): 0x586AB0(l, r) → 真。傭兵で 0x5878F0(r,l) ≥ 50 → 真。l の same_call == "off" → 偽。種族違い → 偽。同クラス、または fkey 一致 → 真。
- 0x461750（立ち去り）: 傭兵で +0xB0 ≠ 0、または +0x74 → 何もしない。fix == "on" → 何もしない。S = 0x5AAEC0(現在地, 0, mode 2, **4**)。fix == "home" なら home リストで絞る。p の spot を除く。roam_avoid == "on" で 0x484970 があれば chop(rand×100) < yabo(r) のとき突出勢力の spot を除く（戻さない）。V[chop(rand/32768×|V|)] へ移動（集合の順は SpotElm アドレス順 → elem_rank）。

### 71.3 0x478F50（部隊の補充）と 0x4780D0（新リーダー）
- 0x478F50: sc = p+0x1D、または君主が @hero、または "@mode_samecall"（find-or-create）の値が 0。各リーダー d（room > 0 かつ資金 ≥ 10 の間）: free = min(0x65C118 − 配下数 − 1, room)。
  - 0x466090（同種召集の雛形。static 0xB0ABC8 を k+"+tmp" で 0x582D90 → **rand を消費**）と 0x586AB0(d, 雛形) が真なら、n = min(資金/price（price ≤ 0 なら 10000）, free) 回 0x4667B0（0x466F60(k) で生成し、種族を d、クラスを k または d に変えて 0x58B7F0 / 0x58C0E0 / 0x58AFA0）。1体以上なら支払って次へ。
  - そうでなければ T = spot の monster ＋ unit merce（無ければ class merce、0x465060）を shuffle し、C を後ろに足す。0x466B00(t)（t+"+tmp" の一時レコード、**rand を消費**）で 0x586AB0 が真になる最初の t を n 体（0x466F60(t, 勢力, 0)、level object = 勢力 +0xDC）配下にする。
- 0x4780D0: C2 = C のうち、一時レコードが +0x77/+0x75 か、staff 判定（勢力 staff。"@@" か空なら君主 unit staff、それも無ければ君主の種族と fkey）を通る名前。各 d について spot が満員なら 0x5AC880 の領域を shuffle して空きのある spot を探す。C2 を shuffle し、資金の足りる名前を巡回して 0x466F60(t, 勢力, 0)（+0x78 = 1）で新リーダーを置き、それぞれに 0x478F50 で部隊を補充する。
- 0x465C20（同種召集の可否）: same_call ≠ "off"、class(d).fkey_sc（無ければ fkey）が存在、その class が unique でない、種族条件。
- 新規 def の +0xE4 は ctor の 10000（0x582C4C、今回確認）。def+0xE4 を def のフィールド（`NativeDefinition.e4`）にし、spot 側の記録が無いときはそれを使う。0x460E90 は 0x18。

### 71.4 ACTUAL（sci1・COMPAT 順位）
- プレイヤー無しで初手の全28勢力を 0x481260 → 0x47E3A0 → 0x47A1A0 → 0x476D60 まで実行。全勢力が新リーダー 4〜12、部隊 22〜78 を雇用し、3勢力が放浪人材を1人登用した。Gap なし（GOLDEN ではない）。

<a id="f-72"></a>
## §72 ターンの駆動・攻撃判断・イベント接続・セーブ契約（STATIC、実装済み）
実装: `peer_script01_turn_frame.py`、`peer_script01_strategy_events.py`、`peer_script01_strategy_save.py`。テスト: `test_peer_script01_turn_frame.py`（11件）、`test_peer_script01_strategy_events.py`（5件）。

### 72.1 0x4751C0（攻撃判断）
- turn == 0、勢力が死亡、+0x50 ≥ 目標数、fix on/hold → +0x50 = SENT、偽。
- pl = ctx+0x54 NULL かつ ctx+0x50 あり かつ 0x592CE0(p)。H = 0x591B30（勢力 +0xC0、無ければ power "home"）。kosen = max(0x591570(p,"kosen"), 25)。
- 目標を +0x50 から順に（+0x50 += 1）: q = 所有者。!pl かつ平和（0x593E50: p+0x118[q] ≥ turn）→ 次。f = 0x46B230(p,q)（find-or-create）。!pl かつ f ≥ diplo_bestfriend(80) なら thr = chop((125−kosen)×0.01×f+0.5)、0x40ED80(0,100) < thr → 次。fix home で H に無い → 次。!pl なら「q がプレイヤー、0x597910(t)、fix warlike、f < turnproc+0x68」のどれかで評価へ。
- 評価: e = t の集合が空かつ +0x90 == 0。def = 0x597C90(t)。N = 0x5AB460(t, p, 0, my_range)（自 spot で兵がいて、自勢力の spot と t だけを通る経路長が 1..my_range のもの。経路は 0x4868D0 と同じ BFS）。係数 = raid_min(−50)×0.01 + (raid_max(50)×0.01 − min)×rand/32768（0x4208A0）+ raid_coe(15)×0.001×kosen。fix warlike なら 100.0。
- N の spot（+0xCC が NULL か t のもの）から 0x597D50(s,1,1) の def を war_capacity まで集める（e なら1体だけ、プレイヤー def を除く）。攻撃マップ（{s: set<def>}）が空なら偽。1体だけでプレイヤー def が行動済みなら偽。プレイヤー def がいれば合計 ×1.5。!e で chop(合計×係数+0.5) < def なら偽。そうでなければ **0x48F9E0（戦争開始）→ 真**。
- 偽で +0x50 が SENT でない場合、次のフレームは次の目標から続く。真の後は +0x64 が立ち、目標を作り直して +0x50 = 0 から再走査する。

### 72.2 0x47AE50（君主の避難）と 0x471E80 の出奔
- 0x47AE50: 首都（0x5937D0）の自隣接が2以上かつ首都の兵が2以上なら何もしない。首都の自隣接 spot のどれかに「兵のいる敵隣接」がなければ何もしない。候補 = 自 spot（名前順）のうち条件を満たすもの。+0xBC = min(自隣接数 − 2×プレイヤー隣接数, 0)（プレイヤー勢力があるとき）、+0xC0 = 0x597C90。0x479F20（+0xBC ≥、同値なら +0xC0 ≥、非厳密）で sort。先頭が首都でなければ君主を移す（満員なら未行動の def と入れ替え）。
- 0x471E80 の出奔（0x47244C..0x472618）を移植した（従来は Gap）。リーダーは配下ごと spot を離れ、配下はリーダーの配下から外れる。def+0xD0 = turn、0x460E90 で放浪。テストの期待値を変更（理由: 移植したため）。

### 72.3 0x471E80（ターン処理）と 0x46C940
- 構成: phase ≥ n で wrap（turn+1、phase 0、turn_wrap、0x461DA0、world フック）。phase 0→1、1→2（+ 勢力0の入口）、k≥2 は維持処理 → phase+1 → 次の勢力の入口（n に達したらそこで止まり、wrap は次の呼出し）。入口の共通処理: 目標クリア、+0x50 = SENT、+0x54 クリア、+0x64 = 0、+0x68 = 100、0x473A68（+0x68 の rand 1回）、world フック。
- 0x46C940（@beit_ 名簿）を移植: def が無い／傭兵でない／期限切れのレコードを消し、def+0xA0 を空にする。有効な def を返す。turn_wrap は Gap をやめてこれを呼ぶ（テストの期待値を変更）。戦争開始側で有効な傭兵がいる場合（傭兵の参戦 0x486A7C..）は引き続き Gap。
- 0x461DA0 の一巡（`monthly_roam_461da0`）を接続: 放浪集合を Def* 順で、def+0xA0 の勢力の +0x128 を候補にする。

### 72.4 GameCtrl::vf01 0x474F10（1フレーム、`frame_474f10`）
- phase ≥ n → 0x471E80。phase 0: プレイヤーが放浪中（0x468700）なら **PLAYER_UI**、そうでなければ 0x471E80。phase 1: 0x47C280（人材の戦争要求が出たら **ACTOR_WAR_47D770** で停止）。
- phase ≥ 2: 死亡勢力 → 0x471E80。プレイヤー勢力で turnproc+0xB が 0 → **PLAYER_UI_51FAA0**。+0x50 ≥ 0 / < 0 の分岐は §70.1 の通り。戦争が始まれば **BATTLE**（または 0x48F9E0 のダイアログ段階）で停止する。
- フレームは取引単位（deepcopy の予行 → 本実行）。Gap なら状態は変わらない。`run_frames` は停止条件か指定ターンまで回す。
- SYNTHETIC: BATTLE → apply_battle_end → 続行で、1ターンが最後まで回ることを確認（`test_turn_through_battle`）。
- ACTUAL（sci1・プレイヤー無し・COMPAT 順位）: ターン0の全28勢力（外交・目標・配置・雇用）→ ターン末（収入・外交減衰・月次放浪）→ ターン1の phase 0/1 → po31 が sp37 を攻撃して **BATTLE** で停止（64フレーム、約340秒。大半は予行の deepcopy）。

### 72.5 GUI 契約（停止点と再開）
| 停止 | 原作 | 再開に必要なもの |
|---|---|---|
| PLAYER_UI_51FAA0 | プレイヤーの手番 UI | GUI の操作。終了は **§78** `player_turn_end_520040`（0x520040 → 0x471E80） |
| DIALOG_481260 | 外交の申し出（§69） | **§76**: `answer_diplomacy_521d90` → 次のフレーム |
| DIALOG_477E7E | employ_hero（turnproc+0x6C/+0x70 = def / spot） | **§77**: `answer_employ_hero_521d90` → 次のフレーム |
| PLAYER_DIALOG_52DE20 / 52E9E0 | 援軍要請（§68） | **§74**: `answer_war_dialog_521d90` / `commit_sortie_52eb20` |
| BATTLE | 0x491666 の後の戦闘シーン | Work の戦闘 → `apply_battle_end` → 次のフレーム |
| ACTOR_WAR_47D770 | 人材の戦争 | **§75 で解消**: 0x47D770 を実行し、戦争なら BATTLE / ダイアログの stage で停止 |

### 72.6 イベント VM の接続
- 原作では、スクリプトの整数変数（0x463CA0）と戦略側の変数（@frd_ 等）は同じ ctx+0x30C。`WorldIntVars` で `StrategyWorld.vars` をランナーに渡し、一つの保存先にした。文字列リスト変数（GM+0x1E863C）はブリッジが持つ。
- `EventBridge.fire(hook)` が 0x432EE0 と同じくシナリオの world/fight/politics イベントを実行する。ターン処理の3か所（入口 0x473B2F、wrap 0x4738B6、プレイヤー最終の 0x47265D）で発火する。ブリッジが無いときは "SKIPPED" と記録する（状態からイベントの効果が抜けていることを明示）。
- **未移植のゲーム状態を読み書きする命令・関数は Gap（黙って無視しない）**。WORLD / BATTLE / PB 系、未対応の VARIABLE 系、GENERAL の state 系（win/terminate/save/next/battleEvent/erase/doskill/resetZone/doGameEnding/setGameClear/exit/gread/gwrite）、状態を読む式関数。
- ACTUAL: sci1 の wev1 は最初に storePlayerUnit を使うので Gap。全シナリオのフック・イベントで使われる命令の上位は add/clear/index/set/choice（対応済み）、未対応では gread、addSkill、setPM、storePlayerUnit、addUnit、storePowerOfUnit、eraseUnit、pushMoney など。関数は ptest、isEvent、inPower、isPlayer、inBattle、isAlive、isNewTurn など。次の移植対象。

### 72.7 セーブ契約（def レコード 0x58F060、CONFIRMED）
- 書込順: +0x78/+0x79/+0x7A（byte→int）、+0x80、+0x84（文字列）、+0xC8、+0xCC、+0x174、+0xBC、+0xC0、+0xC4、+0xD0、+0xD4 配下（文字列…＋区切り1）、+0xE4、+0xE8（byte）、+0xEC / +0xFC / +0x10C（各ベクタ＋区切り1）、+0x12C（文字列,整数の対）＋区切り2、"arbeit" +0x7C、"arbeit_user" +0xA0、"item_skill" +0x11C＋区切り1、"friend" +0x158＋区切り1＋区切り2、+0x13C、+0x168/+0x16C/+0x170、能力値 hp, mp, attack, defense, magic, magdef, speed(+0x194), dext(+0x190), hprec, mprec, move。
- 区切りは .data 0x68B3A8 / 0x68B9D0 の std::string（内容は起動時に設定、VERIFY）。+0x74..+0x77 と +0x1BC.. は書かれない。
- `def_save_record_58f060` がモデルの値をこの順に並べる（未モデルは None）。バイト形式はセーブ担当の範囲。

### 72.8 残り（VERIFY / 未移植）
- ダイアログの回答処理（481260 / 477E7E / 52DE20 / 52E9E0）、0x47D770 の戦争、傭兵の参戦（0x486A7C..）、zone の経路（0x46F020 / 0x47F670）、0x586AB0 の phase 0/1、0x5923F0（プレイヤー勢力の攻撃判断）。
- イベントのゲーム状態命令・関数。def+0xD0 の ctor 値、+0x11C の項目順の保持、区切り文字列の内容。
- 速度: 予行の deepcopy が支配的。取引の粒度を下げる（失敗し得る関数の前で検査する）改善の余地がある。

<a id="f-73"></a>
## §73 WRQ-20261013-CLAUDE-BRIDGE: 戦略→戦闘→結果反映→戦略復帰の境界契約（STATIC、実装済み）
依頼ID: **WRQ-20261013-CLAUDE-BRIDGE**（Work 共有キュー、P1）。§68.7（context/cache の失敗保護）、§68.8（434EB0/5AC1A0）、§72（ターン駆動）は解決済みなので、ここでは再解析しない。この節では、Work が戦闘の前後で必要とする入出力、責務の分担、再開条件を確定させる。
- 証拠の区分: すべて STATIC（逆アセンブル）と SYNTHETIC テストによる。GOLDEN 0 / MATCH 0。原作の実行はしていない。
- Work の製品コードと共有キューは変更していない（読んだだけ）。

### 73.1 全体の流れ（CONFIRMED_NATIVE）
1. **戦争の開始**: `begin_war_48f9e0` から `WarStartReport` が返る。
   - `stage == DISPATCHED` であること。
   - 次の値がそろう: `war`（WarState）、`involvement`（GM+0x1EED54/55/56/43/44/48）、`dispatch`（0x491666: 行軍数 GM+0x1EED5C、援軍待ち spot GM+0x1EECB4）。
   - フレーム側では `frame_474f10` が `stop == "BATTLE"` を返す（§72.5）。
2. **行軍の到着**: 行軍 1本が着くたびに 0x491870（ArmyChipBuilder::vf01、0x5B0B15 から）が 1回呼ばれる。→ `march_arrived_491870`
   - 行軍数 ≤ 0 なら何もしない（IDLE）。
   - 1 減らして、まだ > 0 なら待つ（WAIT_MARCH）。
   - 援軍待ちが残っていれば、援軍の 1波を出す（HELPER_WAVE、73.2）。
   - 残っていなければ振り分け（73.3）。
3. **戦闘の実行**:
   - 通常は 0x4922A0(GM, skip) から始まる。
   - skip = 0: 戦闘シーン 0x48D6A0。
   - skip ≠ 0: 戦況ウィンドウ上で戦闘画面を出さずに解決する（以下「画面なしの解決」）。
   - どちらの場合も、最後に 0x493630 が 1回だけ呼ばれる。→ `apply_battle_end`
4. **戦略への復帰**: ターン処理（GameCtrl::vf01 0x474F10）が、GUI のゲートが開いたあとで、同じ TurnState のまま次のフレームを実行する（73.6）。

### 73.2 援軍の波（0x4918E3..0x491ED7、`helper_wave_491870`）
- P = 待ち行列の先頭 spot の援軍勢力。help map に無い場合は ctx+0x58（中立）。
- 待ち行列を前から順に見る:
  - help map に無い spot: 消すだけで、行軍しない。
  - 勢力 ≠ P の spot: 残す。
  - すでに 1件取っていて、0x597830(spot) が真の spot: 残す（傭兵の spot は単独で 1波になる）。
  - それ以外: 消して取る。
- 取った spot の処理:
  - 攻撃マップの項目を引く（0x48A3A0）。無ければ何もしない。
  - def を +0xE4 で並べる（表示用）。
  - **P == 防衛側（GM+0x1EED4C）なら、各 def に 0x588170 を呼ぶ**（def+0xC8 = turn。配下も同じ）。攻撃側の援軍には呼ばない。
  - def が 1人以上いれば、行軍数を +1 して行軍 0x5B0680 を始める。
- 0x597830(spot) は、spot+0x24（隊員数）== 0 かつ要素の vf64 が偽（不可視）のとき真。傭兵の仮 spot を表す。
- 波で 1本も行軍が始まらなかった場合、原作では 0x491870 を再び呼ぶものが無く、そこで止まる。これを `STALL` として返す。データ上で起きるかどうかは VERIFY。
- 援軍以外の攻撃元の 0x588170 は、すでに 0x491666 で済んでいる（§68）。

### 73.3 振り分け（0x491EDC..、`march_arrived_491870`）
上から順に判定し、最初に当てはまったものに進む。

| 条件 | 結果 |
|---|---|
| 目標の隊員数（+0x24）== 0 で、かつ「目標の value（+0x90）== 0、または [GM+0x1EED44]+0x48 の Unit ベクタが空」 | **NO_DEFENDER**。<br>・`!43 && (54‖55)` なら「戦場の領地に守備兵がいないので戦闘を…」を表示する。<br>・@battlefield/@battleattack/@battledefense を置き換える。<br>・GM+0x1EEFA0 をクリアし、0x52AD90 を呼ぶ。<br>・0x40D0A0(dl=1) で画面なしの解決へ進む。<br>・`fight` フックは呼ばれない。GM+0x1EED43 は変わらない。 |
| 56 かつ 0x469170(ctx)（`@hero` の find-or-create）≠ NULL かつ player_battle（0x683748） | DIALOG WATCH_HERO「静観中の$$$が参加してるこの戦闘を見ますか？」 |
| 54 も 55 も偽で、enemy_battle（0x683749）が真 | DIALOG WATCH「この戦闘を見ますか？」 |
| 54 も 55 も偽で、enemy_battle が偽 | 0x4922A0(GM, 43)（43 = !enemy_battle = 1。画面なし） |
| 54 または 55 で、「!player_battle、または [GM+0x10]+0xB」 | DIALOG CONTROL「この戦闘を操作しますか？」 |
| 54 または 55 で、それ以外 | 0x4922A0(GM, 43)（43 = !player_battle = 0。戦闘シーン） |

- 0x683748 と 0x683749 は、0x5657F0 が `@config@player_battle` / `@config@enemy_battle` から設定するグローバル値。CONFIRMED。§68.4 の引数と同じもの。
- ダイアログは 0x40D0A0(dl=0) と 0x52CCF0（タグ `simplebattle`）で開く。回答は 0x521D90 の 0x52226A で処理される。→ `answer_simplebattle_521d90`
  - 0x87F6F0 == 1（はい）なら 0x4922A0(GM, 0)。
  - それ以外なら 0x4922A0(GM, 1)。
  - 3種類のダイアログすべてで同じ処理。
- [GM+0x1EED44]+0x48 は戦闘担当の陣営オブジェクト。目標の隊員数が 0 で value ≠ 0 のときだけ読まれ、`side44_units_empty` として Work が渡す（渡されなければ Gap）。
- [GM+0x10]+0xB: TurnState.auto_0b（turnproc+0xB）と同じものと見ている。GM+0x10 == &turnproc かどうかは VERIFY。`ctrl_0b` で明示して渡せる。

### 73.4 0x4922A0(GM, skip) と、解決の 2経路（`launch_4922a0`）
- 共通の処理:
  - GM+0x1EED43 = skip。
  - battle{} のルートリスト GM+0x1EEDB8 を解放する。
  - @battle 変数 3つを置き換える。
  - GM+0x1EEFA0 をクリアする。
- **SCENE_48D6A0**（skip = 0）:
  - FadeOutSheet(2) → GameManager::vf01 → 0x48D6A0。
  - 0x48D6A0 は GM+0x1EEC3C = 2 にし、srand(GetTickCount()) を呼び、0x4342A0 で `fight` を発火する。
  - 戦闘の FrameDriver が 0x493630 を呼ぶ（0x49303A / 0x493082 / 0x4930A1）。
- **HEADLESS_40E2F0**（skip ≠ 0、および NO_DEFENDER）:
  - 0x432EE0 で `fight`(1,1,2) を VM に積む。
  - 0x52AD90 を呼び、0x40D0A0(dl=1) で戦況ウィンドウ 0x8B8C90 を開く。ウィンドウには target / war / help を 0x8B8E48/4C/50 に、dl を 0x8B8E54 に保存する。
  - BattleWnd::vf01 0x40E220 が毎フレーム次を行う:
    - VM が動いていれば 0x4338D0 を実行する（`fight` のスクリプトが先に終わる）。
    - そうでなければ 0x40E2F0 を実行する（内部で 0x492D80(…,1) と 0x514C80 を使う。中身は Work の担当範囲）。
    - 結果が 0 なら続ける。0 以外なら次を順に行う:
      1. ウィンドウを閉じる（vf10）。
      2. **0x493630(target, war, GM, 結果 == 1) を 0x40E2B9 から呼ぶ。**
      3. 0x40F000 と 0x48ABF0 を呼ぶ。
      4. GM+0x1EEC71 == 0 なら 0x48EEE0 で world_bgm を戻す。
  - GM+0x1EEC3C は変わらない。world 上なら 1 のまま。`fight` が battle{}（0x492890）を設置した場合だけ 2 になる。
- **乱数の注意（VERIFY、戦闘担当の範囲）**: 画面なしの経路では、0x4922A0 の中で戦闘ボイスのために CRT rand（0x5B6EAB）を使う。
  - 条件: 0x8797C9、かつ GM+4 の +0x130 ≠ 0.0、かつ 0x8797CC == 0（音の設定）。
  - 処理: 0x40EE80 の一覧で def に +0x77 か +0x75 がある Unit ごとに、rand() を 1回呼んで 0x68C638[ftol(r/32768×5)] を引く。最大 2回まで引き、鳴らせた時点で終わる。
  - 音の設定によって乱数の消費が変わり、その消費は 0x493630 より前に起きる。

### 73.5 結果の受け渡し（`check_battle_end_handoff` → `apply_battle_end`）

| BattleEndInput | 値 | 責任 |
|---|---|---|
| battle_id | 戦争ごとに一意。`w.battle_end_log` で一度だけ受け付ける | Work |
| result_flag | 0/1 の生の値（勝敗の名前は付けない） | Work |
| caller_va | SCENE: 0x49303A / 0x493082 / 0x4930A1。HEADLESS: 0x40E2B9。スクリプト 0x4A1764 はどちらでも可 | Work |
| gm_mode | 呼出時点の GM+0x1EEC3C。SCENE は 2。HEADLESS は 1（battle{} があれば 2） | Work |
| war | `WarStartReport.war` をそのまま渡す（等価であること） | Claude が生成し、Work が渡す |
| sides | gm_mode == 2 なら 3陣営のベクタ（GM+0x1E8630/34/38 の順）。それ以外は空 | Work |
| unit_credit_1b4 | 終了時に GM+0x1EEBDC に登録されている Unit の +0x1B4 | Work |
| spot_capacity_0c | ctx+0xC | 呼出側 |

- def の書込み:
  - def+0x1B0（killed）は、Work が戦闘中（0x57897B）に 1回書く。
  - def+0x1B4（撤退先）も Work が書く。
  - これを読んで消費するのは 0x493630 だけ。
  - 戦争の参加者は `war_participants` で求める: 攻撃マップの def とその配下、目標の隊員とその配下、GM+0x1EEC00。
- **二重適用の禁止**:
  - 死亡・撤退・EXP・LvUp・支払い・占領は、`apply_battle_end` の 1回の呼出しの中ですべて行う。
  - LvUp（vf05 → 0x575110）は gm_mode == 2 のときだけ、apply_battle_end の中で行う。
  - 戦略の戦争では、Work は `finish_resolved` / `battle_end_level_ups` を別に呼ばないこと。Work の `apply_resolved_strategy_end` の docstring「no separate LvUp call」と一致している。
  - 同じ battle_id をもう一度渡すと `BattleEndDuplicate` になる。
- **Work の現行 API との差（Work 向けの情報。Work のコードは変更していない）**:
  - `apply_resolved_strategy_end` は gm_mode = 2 に固定で、caller も FrameDriver の 3つに限っている。SCENE 経路ではこれで正しい。
  - HEADLESS 経路（0x40E2B9、gm_mode 1、sides なし）の入口はまだ無い。
- `check_battle_end_handoff` の判定:
  - 違反があれば Gap（または Duplicate）にする。
  - 戦争外の def に +0x1B4 が残っている場合、陣営に参加者以外の Unit がいる場合（イベントの addUnit 等）、参加者以外に credit がある場合は、VERIFY として返すだけにする。

### 73.6 戦略への復帰（`strategy_resume_after_battle`）
- 0x493630 のあと、戦略側の状態に戦争を指すものは残らない。
- 次に実行するのは `frame_474f10`（同じ TurnState）。
  - 攻撃した勢力の turnproc+0x64（ts.ai_flag_64）は 1 のまま。そのため、同じ勢力が同じターンに目標選定（0x47E3A0）からやり直し、もう一度攻撃することがある。
  - phase と +0x50 は戦争によって変わらない。
- 実行してよいのは、次のゲートがすべて開いてから（0x474F10 の冒頭）:
  - VM が空いている（0x431FB0 偽）。
  - 0x87F650 == 0、かつ !(0x87F5D0 && 0x87F6F0)。
  - 0x67BDA0 == 0x80000008。
  - 0x473BB0 が偽。
  - turnproc+9 == 0。
- SCENE 経路の場合は、さらに world シーンに戻っていること（0x48C880 が GM+0x1EEC3C = 1 にする）。これは Work 側で VERIFY_SCENE_TEARDOWN。
- プレイヤーのダイアログで止まったときの再開:
  - `simplebattle` → `answer_simplebattle_521d90`。
  - 0x521D90 には、ほかに `prewar`（はい → 0x5A4D20）と `war`（はい → 0x48F9E0(GM, 0x8BA6F4) をもう一度呼ぶ）の分岐もある。プレイヤーが仕掛けた戦争の確認に使われる。これらの回答処理の移植は未完（§72.8）。

### 73.7 実装とテスト
- `peer_script01_war_start.py`: `MarchState`、`BattleRoute`、`helper_wave_491870`、`march_arrived_491870`、`launch_4922a0`、`answer_simplebattle_521d90`、`war_participants`、`check_battle_end_handoff`、`StrategyResume`、`strategy_resume_after_battle`、`RESOLVER_CALLERS`。
- `tests/test_peer_script01_war_start.py::TestBridgeWRQ20261013`（4件、SYNTHETIC）:
  - 援軍 2波（防衛側の援軍だけ +0xC8 が付く）→ 画面なしでの開始。
  - 受け渡しの検査（caller と mode の組合せ、sides、撤退先、別の war、二重適用）と復帰。
  - プレイヤーの操作ダイアログと回答 → 戦闘シーン（3陣営が必要）。
  - NO_DEFENDER と陣営入力の要求、WAIT_MARCH、STALL。
- 全体: 218 OK。
- 区分:
  - READY: 73.2〜73.6 の戦略側の判定と検査。
  - VERIFY: [GM+0x10]+0xB、STALL、戦闘ボイスの rand、0x40E2F0/0x492D80(…,1) の内部（Work）、シーンの片付け。
  - NOT RUN: 原作との突き合わせ（GOLDEN/MATCH）。

<a id="f-74"></a>
## §74 WRQ-20261013-CLAUDE-BRIDGE（続き）: 戦争開始ダイアログの回答と再開（STATIC、実装済み）
依頼ID: **WRQ-20261013-CLAUDE-BRIDGE**。§73（WarState、MarchState、BattleRoute、check_battle_end_handoff、strategy_resume_after_battle）はこの節で再解析・再実装していない。
- 証拠の区分: 逆アセンブル（STATIC）と SYNTHETIC テストによる。GOLDEN 0 / MATCH 0。
- Work の製品コードと共有キューは変更していない。

### 74.1 既存移植の訂正: 0x4868D0 攻撃側の分岐（CONFIRMED）
- 0x48722B..0x487248 の処理:
  - attP がプレイヤー（+0x1D）で、flag == 0 なら、AL = 1 にして **0x4879C4（次の候補）へ跳ぶ**。0x489630 は呼ばない。
- 旧移植はここで次の判定に落ちていた。そのため、プレイヤーに尋ねる前に AI の候補が 0x489630 で参戦してしまっていた。
- 防衛側の分岐（defP がプレイヤー）は元から正しかった。
- 回帰テスト: `test_player_attacker_no_ai_join_before_asking`。

### 74.2 ダイアログを開く側（`WarStartReport.dialog` = `PendingWarDialog`）
- 原作でダイアログの回答を待つ間、戦争の状態は GM の戦争ブロックと Player 陣営オブジェクト（GM+0x1E8630）に保持される。
  - Player 陣営オブジェクトのフィールド: +0x4A8 = モード、+0x4AC = war、+0x4B0 = help。
  - `PendingWarDialog` は、このうち再開に必要なものを持つ:
    - tag、種類、モード。
    - 戦争の組立て状態（_Build）。
    - 戦況ウィンドウの青枠 spot（0x8BA710）。
    - begin_war の設定。
- 停止時点の状態はそのまま残る。0x4868D0 / 0x488290 による参戦、乱数の消費、@com_ の期限切れ処理が対象。
- **0x52DE20**（0x490149 から。0x4868D0(flag 0) が真のとき）:

| 条件 | モード | ダイアログ |
|---|---|---|
| defP == ctx+0x54 | 0 | YESNO `diplo_ask_test`「$$$が侵攻されました 同盟国に援軍を要請しますか？」 |
| attP == ctx+0x54 | 0 | YESNO `diplo_ask_test`「$$$に攻め込みます 共闘国に共同軍を要請しますか？」 |
| 第三者で、leg(player, defP) > 0（0x46B720）。attP ∈ 0x46BC80(defP) かつ attP ∈ 0x46BC80(player) | 1 | OK のみの `prewar`「共闘国の$$$から援軍の要請が来ました」 |
| 同上で、上の com 条件を満たさない | 3 | メッセージ「同盟国の$$$が###への援軍を求めて来ました」＋ YESNO `diplo_support_test`「$$$に援軍を出しますか？」 |
| 第三者で、leg ≤ 0 | 2 | OK のみの `prewar`「共闘国の$$$から共同軍の要請が来ました」 |

  - 候補一覧 0x4857C0 は表示専用で、乱数は使わない。読む @leg_ レコードは、直前の 0x4868D0 がすべて作成済み（同じ N と同じ判定順）。
  - 青枠の spot は 0x5A4B20 → 0x5AB460(target, player, q, dmax) で求める。
    - q: モード 1/3 は defP。モード 2 は、攻撃マップのうち help にない最初の項目の spot の所有者（既定はプレイヤー）。
    - dmax: ctx+0 support_range。
  - 0x5AB460 は、q ≠ NULL のとき経路計算に使う勢力を [p, q] に固定する（0x5AB4CF / 0x5AB65E）。
- **0x52E9E0**（0x490562 から。0x488290 が真のとき）:
  - モード 4。
  - 青枠の spot は 0x5AB460(target, player, defP, ctx+8 myhelp_range)。
  - YESNO `diplo_help_test`「$$$が侵攻されました 周辺領地から援軍を出しますか？」。
- ctx+0x54 が NULL なのに +0x1D の勢力があるという矛盾した状態では、ダイアログは作らずに VERIFY を記録する（原作ではこの状態にならない）。

### 74.3 回答（0x521D90、`answer_war_dialog_521d90`）
- Player::vf01 0x521AE1 は、tag（0x87F5C0、長さ 0x87F5D0）と回答（0x87F6F0）がそろうと 0x521D90 を呼ぶ。
- 0x43F330 は tag が一致すると **tag を消して真を返す**。
  - 回答は 1回しか処理されない。2回目は `WarDialogConsumed` になる。
  - 「いいえ」でも tag は消費される。
  - 「はい」は 0x87F6F0 == 1 のこと。それ以外の値（いいえ・閉じる）は「いいえ」と同じ扱い。

| tag | はい | いいえ |
|---|---|---|
| diplo_ask_test | 0x4868D0(flag 1)（N の shuffle をもう一度行い、0x489630 で参戦: 乱数）→ 0x49E3B0 / 0x452F60（GUI）→ **0x490180** | GUI → **0x490180** |
| prewar（OK のみ） | 0x5A4D20: 0x8BB6C4 → 0x8BA6F0 を設定して戦況ウィンドウを開く | 何もしない（再開経路は無い。OK のみなので VERIFY） |
| diplo_support_test | 0x5A4D20 | +0x4A8 = 0。0x48A340 → **0x490180**。メッセージ「援軍の求めを拒否したので…友好度が下がりました」 |
| diplo_help_test | 0x5A4D20 | +0x4A8 = 0 → **0x490590** |

- **0x48A340 の原作の癖（CONFIRMED）**:
  - ECX = EBX = EDI = defP で呼ばれる。そのため、変わるのは frd(defP, defP) で、プレイヤーとの友好度ではない。
  - 処理内容: find-or-create した値が > 0 なら clamp(v − diplo_frd_down(10)/2, 1, 100) を書く。
- 0x490180 は再びダイアログ（0x52E9E0）で止まることがある。そのときは新しい `report.dialog` が返る。

### 74.4 出撃の確定（0x52EB20、`commit_sortie_52eb20`）
- 戦況ウィンドウの確定（WarWnd::vf16）で、次の確認ダイアログが出る:
  - +0x4A8 が 1〜3 なら `send_support`。
  - +0x4A8 が 4 なら `send_help`。
  - +0x4A8 が 0 なら `war`（プレイヤー自身の攻撃）。
- `send_*` で「はい」なら 0x52EB20 を呼び、続いてモード 1〜3 は **0x490180**、モード 4 は **0x490590** に進む。「いいえ」は何もしない（ウィンドウ側の動作は GUI 担当）。
- 0x52EB20 の処理。選択 = 0x8BA6F4 {spot: set<def>}、GUI から渡される:
  1. 各項目について:
     - sent += 0x587FA0(def)、count += 1。
     - spot+0xC0 = 1000000。
     - 攻撃マップに挿入する（0x476700/0x476A50/0x476720、上書きしない）。
     - help マップに (spot, ctx+0x54, side = モード∈{1,3,4}) を挿入する（0x48A4B0/0x4F9000）。
  2. モード ≠ 4 のとき、信用度の減点を計算する:
     - avail = 青枠の各 spot について、0x597D50(s,0,0) の 0x587FA0 を合計したもの（順序に依存しない）。
     - x = chop((1 − ((100 − support_trust_bdr(75))×0.01 + sent/avail)) × trust_down_support(40) + 0.5)。
       - FPU 命令は DE E1 = FSUBRP ST(1),ST(0)。
       - avail == 0 のとき、FIDIV の結果が inf/NaN になり、ftol は 0x80000000 を返すので減点なし。
     - モード 3 なら x/2（0 方向への丸め）。
     - x > 0 かつ count < ctx+0x10（war_capacity）− 2 なら、プレイヤーの盟主の +0xC4 から x を引く。
     - メッセージ: sent == 0 なら「共闘約束を反故にしたので信用度が下がりました」、それ以外は「援軍の出し惜しみをしたと見られ信用度が下がりました」。
  3. +0x4A8 = 0 にし、0x5A4520 でウィンドウを閉じる。
- 選択内容の検査: 青枠以外の spot と、その spot の隊長ではない def は Gap にする。ウィンドウでどの def を選べるかの規則は GUI の範囲なので、検査は失敗側に倒すだけにしている。
- 確定は 1回だけ（`committed`）。ウィンドウが開く前に確定しようとした場合も Gap にする。

### 74.5 プレイヤー自身の攻撃 `war`（0x522303、`player_war_521d90`）
- 「はい」なら 0x48F9E0(ECX = [0x8BA6F0]; GM, 0x8BA6F4) を呼ぶ。これは `begin_war_48f9e0` と同じ入力。
- そのあと 0x468700(ctx) が真（ctx+0x54 が NULL で ctx+0x50 がある = プレイヤーが放浪中）なら、プレイヤー def の +0xC8 = turn にする（def+0x1A4 経由で GM+0x1EF4C8 を読む）。
- 「いいえ」は何もしない。
- 戻り値の report が再びダイアログで止まっている場合は、74.3 の処理に続く。

### 74.6 戦略フレームの再開条件（`FrameGates` / `frame_blockers` / `resume_frame_474f10`、turn_frame）
- 0x474F10 冒頭のガード（CONFIRMED 0x474F21..0x474F77）をそのまま入力にする。GUI 担当・戦闘担当が渡す値で、Claude 側では作らない:
  - turnproc+9。
  - 0x431FB0（VM 実行中）。
  - 0x87F650。
  - 0x87F5D0 && 0x87F6F0。
  - 0x67BDA0 ≠ 0x80000008。
  - 0x473BB0。
  - GM+0x1EEC3C ≠ 1（シーンの片付けが終わっていない）。
- Claude 側で加える整合性の検査:
  - 未回答のダイアログ、または出撃を待っている戦況ウィンドウがある。
  - 出陣済みの戦争に apply_battle_end がまだ適用されていない。
- ガードが閉じているときは None を返し、何も変えない（原作で vf01 が何もせずに戻るのと同じ）。
- battle_id が未適用なら Gap。
- 開いていれば、同じ TurnState のまま `frame_474f10` を 1回実行する。
- シーンの片付け、GUI、画面なしの戦闘は Work の担当範囲で、Claude 側では代わりに実装しない。

### 74.7 Work 向けの公開 API と、未解決の依存
- 公開 API:
  - `begin_war_48f9e0(...).dialog`
  - `answer_war_dialog_521d90(w, ts, dialog, ok, rng, ctx)`
  - `commit_sortie_52eb20(w, ts, dialog, selection, rng, ctx)`
  - `player_war_521d90(...)`
  - `FrameGates` / `frame_blockers` / `resume_frame_474f10`
- いずれもトランザクションになっている。先に deepcopy で予行し、Gap が出たら world / TurnState / ダイアログ / 乱数 / context cache を変えない。
- 結果の `WarDialogStep` は、action（CONTINUED / WARWND_OPEN / NOTHING）、report、信用度の減点、ui_events、rng_draws を持つ。
- **GUI 担当が渡すもの**:
  - ダイアログの回答（はい/いいえ）。
  - 戦況ウィンドウでの選択（spot → 隊長 def）。
  - FrameGates。
- **VERIFY として残したもの**:
  - prewar を OK 以外で閉じた場合（再開経路が無い）。
  - 戦況ウィンドウのキャンセルと選択規則。
  - 青枠 0x8BA710（0x5A4B20 の set<SpotElm*>）の順序。GUI の表示順だけに影響し、合計は順序に依存しない。
  - 0x4857C0 の表示内容。
- **未移植（次の候補）**: 0x47D770（人材の戦争）、外交ダイアログの回答（diplo_friendly / diplo_league / diplo_common と employ_hero 0x475C60）。

<a id="f-75"></a>
## §75 WRQ-20261013-CLAUDE-BRIDGE（続き）: 0x47D770 人材の戦争開始と出奔（STATIC、実装済み）
依頼ID: **WRQ-20261013-CLAUDE-BRIDGE**。
- 0x47D520 による判定（§64、`actor_action_47d520`）は再解析していない。
- 0x47D520 は 0x47D770 を呼んだ直後に AL = 1 を返す（0x47D740 / 0x47D758）。この節では 0x47D770 の中身を扱う。
- 証拠の区分: STATIC。テストは SYNTHETIC。GOLDEN 0 / MATCH 0。

### 75.1 共通部分（CONFIRMED 0x47D7D1..0x47D982）
- 関数内 static の map 0xB136A8 を毎回クリアする。
- home = 0x583CF0(def)、owner = 0x597B00(home)。
- {home: {def}} を、攻撃マップと同じ挿入（0x476700 / 0x476A50 / 0x476720）で入れる。
- home が NULL の場合、原作では NULL キーになる。この場合は Gap にする。

### 75.2 放浪中の人材（def+0x94 ≠ 0）: 戦争（CONFIRMED 0x47D98A..0x47DA01）
1. **def+0x84（放浪先）= target の名前**（0x402710）。これを **0x48F9E0 より前に**行う。
2. 0x48F9E0(ECX = target; GM, &0xB136A8) を呼ぶ。
- 戦争開始の中では、actor（0x48F720）がすでに放浪中という扱いになる。そのため 0x4868D0 と 0x490180 の援軍選定は行われない。
- 0x493630 では放浪者の戦争として扱われ、勝てば 0x434EB0 で新しい勢力ができる（§67）。
- 戦争開始以外の乱数は使わない。

### 75.3 放浪していない人材: 出奔（CONFIRMED 0x47DA04..0x47E13D）
1. HeroFlag の表示（0x5B1A10 / 0x5B1730(GM+0x1E9080, map, def, target) / 0x5B1FA0）。GUI。
2. **owner がプレイヤー勢力（+0x1D）の場合だけ、引き抜きを行う**:
   - thr = loyal_border(50) + 100 − master(owner)+0xC4。
   - v = chop(0x587CC0(def,1) × (yabo × 0.01) + 0.5)。yabo は 0x585580。
   - 対象の spot: 0x5AAEC0(home の要素, owner, mode 0, ctx+0 support_range) に home を加えた集合。set<SpotElm*> の順で回るので、elem_rank が必要。
   - 各 spot s について、0x597D50(s,0,0) の各 dd（≠ def）を見る。dd の配下 m（0x5882F0 の 1番目以降）ごとに次を判定する:
     - m+0xC0 < thr。
     - m+0x77 または +0x75。
     - m+0x7A が立っていない。
     - x = chop(0x587CC0(m,1) × (m+0xC0 / thr) + 0.5)（FIDIV のあと FMULP）。
     - v ≥ x。
   - 条件をすべて満たした m について:
     - m を 0x583DC0(m) の +0xD4 から外す（最初の一致だけ）。
     - m を def+0xD4 の末尾に追加する。
     - m の名前を s の集合から外す（0x416080 / 0x415CF0）。
     - メッセージ「$$$が離反して###に与しました」。
   - thr ≤ 0（0 での FIDIV）と、0x583DC0 が NULL の場合は Gap。
3. 0x598450(home, def, 0) で、def と配下の名前を home から外す。破棄はしない。
4. 0x460E90(ctx, def, target)（`roam_definition`）で target に放浪させる。+0x77..+0x7A の消去、+0xC0 = 100 などもここで行われる。
5. def+0xD4 の各名前について、0x467DE0 で def を引く。+0x77 または +0x75 があれば **+0x7A = 1** にする（0x460E90 の後）。
6. メッセージ「$$$が###を出奔しました」と画面スクロール（0x5202E0、GUI）。
- **この呼出しでは戦争は始まらない。** def は target で放浪状態になり、のちの人材フェーズで改めて判定される。乱数は使わない。

### 75.4 実装と接続
- `strategy_world.actor_war_47d770`:
  - 旧版は出奔を Gap にしていた。
  - 今は分岐名（"war" / "rebellion"）付きの WarRequest を返す。
  - 判定と乱数消費は変えていない。テスト期待値 1件を、理由と日付付きで更新した。
- `war_start.actor_war_start_47d770(w, ts, req, rng, ctx, settings, ...)` → `ActorWarReport`:
  - 結果の種類: WAR（war = WarStartReport）または REBELLION（poached / flagged）。
  - トランザクションになっている（失敗しても状態を変えない）。
- `turn_frame._frame` の phase 1:
  - 旧版は `ACTOR_WAR_47D770` で止めていた。今は 0x47D770 を実行する。
  - 戦争なら、AI の攻撃と同じく `BATTLE` で止まる。ダイアログが出ればダイアログの stage で止まる。
  - 出奔では止まらない（原作どおり、そのフレームで終わる）。
  - `FrameReport.actor` に結果を入れる。
- テスト: `TestActorWarWRQ20261013`（4件）。
  - 放浪中の人材の戦争。
  - プレイヤー以外の勢力での出奔。
  - プレイヤー勢力での出奔と引き抜き。
  - Gap のときに状態が変わらないこと。
- 全体: 234 OK。
- 残りの VERIFY:
  - HeroFlag の 3関数は GUI として扱った。状態を書き換える処理が無いことは、呼出元と文字列から推定した。
  - 引き抜かれた m は、どの spot の集合にも入らない。def は直後に放浪するので、原作どおりの挙動。

<a id="f-76"></a>
## §76 WRQ-20261013-CLAUDE-BRIDGE（続き）: 外交ダイアログの回答とプレイヤーの提案（STATIC、実装済み）
- 証拠の区分: STATIC。テストは SYNTHETIC。GOLDEN 0 / MATCH 0。
- 0x521D90 が扱う tag の一覧（0x43F330 の照合順）: turnend, commission, commission2, retreat_ok, simplebattle, prewar, war, dispose, extract_vassal, diplo_friendly, diplo_league, diplo_common, diplo_friendly_test, diplo_league_test, diplo_common_test, send_support, send_help, diplo_support_test, diplo_ask_test, diplo_help_test, title, employ_hero, roam_hero, roam_hero2, raise_hero, dungeon, gameover, npm_replay, all_auto, gameclear, power_select, person_select, event_select, nopower, takeoff_item, erase_poli。
  - そのうち、戦略の停止点から再開するのに必要なものを §73〜§78 で移植した。
  - 残りはプレイヤーのコマンド（GUI 担当の操作）。

### 76.1 既存移植の訂正: turnproc+0x74（CONFIRMED）
- 0x4826C0 の 0x4828B4 は `mov [turnproc+0x74], edi` を実行する。
- このときの edi は 0x482831 の `[esp+0xD8]` で、スタックの深さ 0x74 を差し引くと **第3引数 x（共闘の相手として攻撃する敵勢力）**。q（依頼を受ける側）ではない。
- 0x4833F0 と DialogWnd::vf01（0x441B29）も、この値を敵勢力として読んでいる。
- 旧移植は `ts.common_74 = q` だったので、`x` に直した。

### 76.2 AI の提案へのプレイヤーの回答（`answer_diplomacy_521d90`）
- 停止点 `DIALOG_481260` の再開。開いているダイアログは `pending_diplomacy_dialog(rep)` で取り出す。0x481260 のプレイヤー分岐は 1回しか呼ばれないので、ダイアログは最大1つ。
- 共通の前提:
  - p = 現在の勢力（turnproc+0x38 − 2。範囲外なら NULL → Gap）、player = ctx+0x54。
  - tag の消費は 1回だけ（`DiplomacyAnswered`）。
  - 乱数は使わない。
  - 回答後は 0x452F60（GUI）。
- 0x4830D0（diplo_friendly_test）:
  - はい:
    1. p の資金を 0x593C20(player) 減らし、同額を player に加える。
    2. 0x593D50(p, player) で p+0x118[player] = turn + diplo_frd_peace(2) − 1。
    3. frd = min(f + diplo_frd_up(20), 100)。
  - いいえ: frd > 0 なら max(f − diplo_frd_down(10), 1)。
- 0x482DF0（diplo_league_test）:
  - はい: 同じ資金移動のあと、leg ≠ 0x7FFFFFFF なら leg = turn + diplo_league_up(6)。
  - いいえ: メッセージのみ。
- 0x4833F0（diplo_common_test）:
  - はい:
    1. 同じ資金移動。
    2. leg(player, p) を読む（結果は使わないが、レコードは作成される）。
    3. until = turn + diplo_sup_up(6)。
    4. 0x46C200 を (p, x, by player)、続いて (player, x, by p) の順で呼ぶ。x = turnproc+0x74。
  - いいえ: メッセージのみ。
- 再開: 0x481260 が turnproc+0x50 = −1 にしているので、次のフレームで外交は二度実行されない。
- p がダイアログ時の勢力と違う場合は Gap にする。

### 76.3 プレイヤーからの提案（`player_proposal_521d90`）
- DiploWnd::vf16 が 0x683AAC / 0x683AB0 を設定する（GUI）。「いいえ」は何もしない。
- diplo_friendly:
  - 0x481F90(turnproc, p = [0x683AAC] = プレイヤー, q = [0x683AB0])。
  - 0x593C70(p, q)（p+0xB0[q] = turn）。
- diplo_league: 0x481820(turnproc, p, q)、0x593C70(p, q)。
- diplo_common:
  - 0x4826C0(ECX = q = [0x683AAC]; turnproc, p = ctx+0x54, x = [0x683AB0])。
  - 0x442D80(ECX = player, EAX = q) → 0x593C70(player, q)。
- 相手の AI は、AI 同士の提案と同じ処理と乱数で判断する。

<a id="f-77"></a>
## §77 WRQ-20261013-CLAUDE-BRIDGE（続き）: employ_hero の回答 0x475C60（STATIC、実装済み）
- 停止点 `DIALOG_477E7E`。0x4771F0 が、放浪中の **プレイヤーの def r（r+0x74）** を現在の勢力 p に仕官させるか尋ねる。r = turnproc+0x6C、spot = turnproc+0x70。
- 「いいえ」:
  - メッセージのみ（0x583A80(ctx+0x50) によって「傭兵契約を拒否」か「仕官を拒否」かが決まる）。
  - turnproc+0x6C / +0x70 は原作どおり残す。
- 「はい」:
  1. price = 0x585AD0(r, "price")。AI の 0x4771F0 が使う 0x585960 ではない。
  2. price += chop((100 − aff)×0.01 × price × employ_price_coe(100)×0.01 + 0.5)。
     - aff は、p+0x60 ≠ SENT かつ turn − p+0x60 < leave_period(5) なら 0、それ以外は 0x5878F0(r, master p)。
  3. 0x583A80 が真なら、price = chop(arbeit_price_coe(33) × price × 0.01 + 0.5)。
  4. **p の資金から price を引く（残高の検査はしない）**。
  5. 0x583A80 が真の場合（傭兵契約）:
     - 0x46CD30(p, r, arbeit_turn(3))。
     - r+0x174 += price、r+0x80 = 0。
  6. それ以外の場合（仕官）:
     - 0x460F10。
     - r+0x174 += price。
     - spot の集合に r と配下の名前を入れる。
     - word +0x78 = 1、+0x7A = 0、+0xBC = 0、**+0xC0 = 100**（AI の 0x4771F0 では aff）、+0x80 = 0。
     - 0x588170。
     - 0x593890(p)（rand を 1回使い、性格を引き直す）。
  7. どちらの場合も:
     - unit の "join" 文字列が空でなければ、0x434CC0(VM, text) でイベントを積む。`join_event` として返し、イベント担当が実行する。
     - 画面スクロール（GUI）。
- ctx+0x54 は変えない。
- トランザクションになっている。トークン = HiringReport（`answered`）。turnproc+0x6C/+0x70 が変わっていたら Gap。

<a id="f-78"></a>
## §78 WRQ-20261013-CLAUDE-BRIDGE（続き）: プレイヤーのターン終了 turnend（STATIC、実装済み）
- tag "turnend" で「はい」（0x521DFA）。
- turnproc+0xA ≠ 0 なら何もしない。書き込む側は VERIFY なので、GUI 担当からの入力 `turnend_locked_0a` として受け取る。
- それ以外なら 0x520040:
  1. ctx+0x54 が NULL で ctx+0x50 があれば、プレイヤー def の +0x79 = 0。
  2. GUI の処理（0x52AD90 / 0x52AE60 / 0x49E300 / 0x49DC80）。
  3. **0x471E80(turnproc)**: AI のフェーズと同じ進行処理。
  4. 結果のメッセージ3件（訓練・維持費・財政）。
- これで `PLAYER_UI_51FAA0` の停止を閉じられる。→ `player_turn_end_520040`
- テスト: §76 は 5件、§77 は 4件、§78 は 2件。全体: 245 OK。

<a id="f-79"></a>
## §79 WRQ-20261013-CLAUDE-BRIDGE（続き）: イベント橋のゲーム状態コマンドと式関数（STATIC、実装済み）
### §79.1 ACTUAL sci1 探索で見つかった誤停止（battle_end 0x48F720）
- 探索: sci1、COMPAT ranks、プレイヤーなし、戦闘結果は SYNTHETIC（flag 1/0 交互）。GOLDEN/MATCH には数えない（原作は実行していない）。
- 停止内容: 攻撃エントリが1件で def が複数ある場合、「set<def*> の先頭 def（アドレス順）」が決まらないとして常に Gap になっていた。
- 修正: 全 def が「流浪中かつ（0x583A80 不可 または +0xB0 == 0）」を満たさない場合、先頭がどれでも cStack_e1 = 0 なので順序は不要とした。1つでも満たす def があれば、従来どおり Gap（ロールバック付き）。
- 回帰テスト2件:
  - `test_multi_def_entry_without_actor_is_order_free`
  - `test_multi_def_entry_with_actor_is_gap_and_rolls_back`
### §79.2 VARIABLE コマンド（Script_DispatchVarCommand 0x4AE0F0）
- 共通形（CONFIRMED）:
  - store 系: リストを作り、GM+0x1E863C[0x44DAB0(dst)] を置換する。
  - src 系の引数は 0x49C950 で解決する（'@x' → リスト x のコピー、それ以外 → [リテラル]）。
  - 単一ソースは 0x49C450 で解決する。
  - push 系: 変数引数の生テキストに VarMap_Set(name, value, replace 1)（0x4637A0）。
- 実装した39コマンド（`STATE_VAR_COMMANDS`）:
  - storePlayerUnit / storePlayerPower（ctx+0x50 / +0x54）
  - storeNonPlayerPower = storeComPower
  - storePowerOfSpot / storePowerOfUnit、storeSpotOfPower / storeSpotOfUnit
  - storeLeaderOfPower（0x593090。+0x1BC/+0x1C8 の書き込みを含む）、storeLeaderOfSpot
  - storeUnitOfPower（0x593550）、storeUnitOfSpot、storeRoamUnitOfSpot（mode 2）
  - storeMemberOfUnit、storeMasterOfPower
  - storeClass / BaseClass / RaceOfUnit、storeSkillOfUnit
  - storeNowPower（[GM+0x10] → 0x471DC0。GM+0x10 = turnproc を確定）
  - storeAllPower / AllSpot / NeutralSpot（0x597950）/ NextSpot / AllTalent
  - pushTurn（turn+1）、pushMoney / Spot / Force / Gain / Castle / Capa / Diplo
  - pushSex / Level / Loyal / Merits / Rank / Trust
- 対象が見つからない場合の動作は、ハンドラごとに原作どおりにした:
  - pushCastle / Capa / Spot / Gain / Diplo は書き込まない。
  - def 系の push は 0 を書く。
  - NULL を参照する場合は StrategyModelGap。
- EventBridge の追加入力: `ts`（turnproc）、`context`、`settings`、`elem_rank`。未接続のまま必要になった場合は Gap。
- テスト: `TestStateVarCommandsWRQ20261013.test_store_and_push`。全体: 248 OK。
### §79.3 式関数（ExpresFunc_EvalInt 0x44F470）: 実装済み
- 引数の取り方（CONFIRMED）:
  - 0x415750(args, i): 範囲外なら throw。
  - 0x452860: ExpresString への検査付き dynamic_cast。ExpresNum の引数は bad_cast で throw。
  - 解決方法は3種類で、関数ごとに決まっている。s1 = 0x49C450、list = 0x49C950、raw = ノードの文字列そのもの（'@' を解決しない）。
  - 検索: 勢力 0x467F40、def 0x467DE0、spot 0x467E90。
- turnproc フラグ（GM+0x1EF4B4。TurnState に追加）:
  - 0x4716C0 で +0x9..+0x10 を 0 にする。
  - 0x471E80 は呼ばれるたびに、最初に +0xB..+0x10 を 0 にする（0x471ED3/0x471ED6）。
  - +0xD: ターン一巡の world フックの直前に 1（0x4738B2）。
  - +0xF: プレイヤー勢力の維持処理で 1（0x472636）。
  - +0xE / +0x10: 勢力フェーズ開始で、プレイヤー勢力なら +0xE、それ以外なら +0x10 を 1 にする（0x473B0D..0x473B19）。world フックより前。
  - +0xA（isGameClear）を 1 にする処理は未発見（VERIFY）。ctor は 0、0x4740A0 は 0 を書く。
- 世界状態の関数:
  - 0 isGameClear = +0xA。
  - 2 isNPM = ctx+0x54 と +0x50 がどちらも NULL。
  - 3 isWorld / 4 isMap・isEvent / 13 isSelect = GM+0x1EF140 が 1 / 2 / 5。
  - 7 / 9 / 10 = +0xD / +0xE / +0xF。
  - 8 = GM+0x1EF175 == 0。
  - 11 isScenario = raw == ctx+0x34。
  - 12 isComTurn: +0x10 が 0 なら 0。引数がなければ「現在勢力があり、プレイヤーでない」。引数があれば「現在勢力の名前 == s1」。
  - 14 = GM+0x1EF152 == 1。
- 人材・勢力の述語:
  - 100 isPlayer(s1):
    - 勢力の場合: +0x1D なら 1。そうでなければ 0x469170（"@hero" を find-or-create）の def と 0x5916E0(勢力) が同一なら 1。
    - def の場合: +0x74 なら 1。そうでなければ hero と同一なら 1。
  - 101 isNPC(list...): 全要素について、プレイヤー勢力でも +0x74 の def でもなければ 1。
  - 102 isAlive(list...): 勢力なら +0x1C。def なら存在すれば真。それ以外は 0。
  - 103 isMaster = +0x77。104 isRoamer = 0x583C70 が無名勢力。106 isLeader = +0x78。
  - 107 isVassal(a[, l]): +0x7A。l があれば、さらに 0x583DC0(a) == l。
  - 108 isRoamLeader = +0x94 ≠ 0（流浪 spot 文字列の長さ）。109 isTalent = 0x585CA0。
  - 110 isEnable = +0xCC ≤ turn。112 isArbeit = 0x583A80。113 isDone = +0xC8 ≥ turn。
  - 105 isEnemy / 114 isFriend（0x44FAFD を共用し、id 0x69 で分岐）:
    - 両方 def の場合: 0x583C70 の勢力を比べる。異なれば isEnemy = 1、同じなら isFriend = 1。それ以外で一方でも名前付き勢力なら 0。両方とも無名なら 0x583DC0 の隊長を比べる。
    - def でない場合: spot どうしで 0x597B00 の所有者を比べる。
- 数値の関数:
  - 200 getTurn = turn + 1。201 countSpot = 勢力 +0x6C（spot 集合の要素数）。
  - 202 countForce = 0x592F10。203 countGain = 0x592E30、または spot +0x80。
  - 204 countMoney = 勢力 +0x5C、または def +0x174。205 getMode = GM+0x1E8。
  - 206 countPower = ctx+0x2E0 のうち +0x1C の数。
- 位置の関数:
  - 300 inPower(p, list...): 勢力が存在し +0x1C であること。各要素について、spot なら所有者 == p、spot でなければ {T(0x593550 の def 名)} に含まれること。引数が0個なら _Xout_of_range。
  - 301 inSpot(s, list...): 各要素が {T(spot+0x1C の名前)} に含まれること。
  - 303 inRoamSpot(s, list...): 各要素が def であり、0x583CF0 == s であること。
  - 400 isJoin(a, b[, f]):
    - 両方勢力の場合: a の各 spot について 0x5AAEC0(b, 0, 1) が空でなければ 1。
    - そうでなければ spot どうしで 0x5AD6C0(a, b, 引数が3個以上か)。
  - 401 isWar = find-or-create "@war_"+min+max > 0（0x46C4E0）。402 isLeague = 0x46B720 > 0。
  - 403 isInvade = "@battleattack" の先頭レコードの文字列 == 勢力名。
  - 405 getClearFloor = "@dun_"+raw。
  - 406 isNext(a, b[, n]): n は 0x49CCA0。b ∈ 0x5AAEC0(a, NULL, 2, n)。
  - 407 isNowSpot = raw == GM+0x1EF220 の名前（NULL なら 0）。
  - 900 ptest(spot(raw), raw) = spot+0x1C を名前順に T() し、raw と一致する個数。引数がなければ 0。
- Gap（安全側で停止）として残したもの:
  - 1 isPeace（0x473DF0）。
  - 111 isSameArmy / 302 inBattle（戦闘中のユニット。戦闘担当の範囲）。
  - 404 isDungeon（GM+0x1EF21C ≠ 0 の場合）。
  - 600..616（戦闘）。
  - GM の値（`EventBridge.gm`）が渡されていない場合。
- テスト（`TestStateFunctionsWRQ20261013`。全体 251 OK）:
  - 関数33件を1つのイベントで確認。
  - GM 入力がない場合は Gap、数値引数は throw になることを確認。
  - turnproc フラグの遷移を確認。
- 既存テストの説明を更新した（2026-10-13 付のコメント）。politics の Gap の理由が、isPlayer から set() の 0x49CCA0 に変わったため。期待値（Gap）は変えていない。

### §79.4 setPM と ACTUAL sci1 フックの探索（STATIC + 実データ）
- setPM（VARIABLE op76 0x4B3494）:
  - k = "_pm_" + s1(arg0)。L = 0x49CB10(arg1)。
  - 0x463900(k, NULL) で k の全レコードを消してから、L の順に 0x463610(k, e, 0) を追加する。
  - → `_v_set_pm`。テスト1件。
- 実データ（sci1）の world フックを橋で実行し、止まった位置（Gap）を確認した。sci1 の初期ワールド、GM 入力は仮値、GOLDEN/MATCH 0。
  - 修正前: VARIABLE:setPM で停止。
  - 修正後: WORLD:addSkill で停止（WORLD コマンドは未移植。次の工程）。
  - fight フックは VARIABLE:storeBattleSpot（戦闘の範囲）、politics フックは WORLD:eraseUnit で停止。
- 長時間探索 run2（sci1、イベントなし、戦闘結果は SYNTHETIC）:
  - 31戦闘目、ターン2で `0x5AC1A0: link vector order before random_shuffle` の Gap。
  - 調査結果:
    - 要素の +0x8C ベクタに追加している箇所は 0x5AF920 だけ。0x5AF920 は push_back(const&) で、エイリアス検査をする。
    - 呼出元は 0x5AFB30 の2回だけで、どちらも経路要素（ebx = this）に対して push している。順序は [第2引数の spot, ecx の spot]（+0x1E8 = 第2引数の名前、+0x204 = ecx の名前）。
    - spot 要素側のベクタを埋める処理は見つからなかった。また linkSpot の引数と ecx / 第2引数の対応も未確定。
  - このため LINK_ORDER_VERIFIED は False のまま（VERIFY）。

### §79.5 WORLD コマンドの開始と UD / PM 変数、save（STATIC、実装済み）
- WORLD のディスパッチャ 0x4A7A90 の引数は GM+0x504。したがって [引数+0x1EEC3C] = GM+0x1EF140（モード）、[引数+0xC] = ctx。ハンドラは AL = 0 で終わる（0x4ACD37）。
- addSkill / addSkill2（op35 0x4AB6F4）:
  - L の各名前について処理する。GM モードが 2 なら、戦闘ユニット（0x49E6B0 / 0x49E780）を先に引く。戦闘担当の範囲なので Gap。
  - def は 0x467DE0 で引く。無ければ次の名前へ。
  - 引数1以降の各スキル名を、展開せずにそのまま追加する:
    - addSkill2（0x4A6B30 で名前を比較）: +0x10C に push_back し、+0xEC の先頭に insert（0x417080）。
    - addSkill: +0xFC と +0xEC に push_back。
  - スキル1件ごとに 0x58DA40 を呼ぶ。
- eraseSkill（op36 0x4AB9DF）:
  - def は 0x467DE0 で引く（戦闘ユニットは引かない）。
  - 引数が1個なら +0xEC だけ全消去（0x41DE00）。
  - それ以外は、+0xEC → +0xFC → +0x10C → +0x11C の順に、一致する要素をすべて消す。0x58DA40 は呼ばない。
- def+0x11C: アイテム名の vector（0x583737..0x583743。前グループ・後グループとも push）。`NativeSkillState.items_11c` として追加し、`apply_item_list` でも積むようにした。
- VARIABLE:
  - setUD（op0 0x4AE198）: v はノードの生の名前（'@' 付きのまま）。0x463900 で全レコードを消し、0x49C950(arg1) の各要素を (e, 0) として追加。
  - storeUD（op1 0x4AE280）: v のレコード文字列を（0x463DF0、挿入順で）文字列リスト L に入れて置換する。
  - storePM（op77 0x4B359F）: "_pm_"+s1 のレコード文字列を L に入れて置換する。
- save（GENERAL op7 0x4A17C8）: 0x45F960(ctx)（セーブ担当: 説明文の作成、GetLocalTime、"@hero" の find-or-create など）を呼んだ後、AL = 1 を返す。
  - 橋は `EventBridge.save_hook` が None なら Gap。callable を渡した場合は、それを呼んでから AL = 1 を返す（セーブ処理自体は担当外）。
- 実データの探索（sci1、橋あり）:
  - 初期状態の world フックが SCRIPT_END まで実行できるようになった。実行回数の多いコマンド: VARIABLE:set 84、WORLD:addSkill 14、setPM 7、addSkill2 4。
  - その後の停止箇所は、storeUD → setUD → save の順に解消した。
- テスト（`TestWorldAndUdCommandsWRQ20261013`、3件）。全体: 標準10モジュールで 254 OK。

### §79.6 WORLD コマンド（続き）と gread/gwrite（STATIC、実装済み）
- addMoney / setMoney（op27 0x4AB06D）:
  - L = 0x49C950(arg0)、n = 0x49CCA0(arg1)。
  - 勢力なら +0x5C、勢力でなく def なら +0x174 に加算（int32）または代入。
  - 処理の後、現在勢力（0x471DC0）がプレイヤー勢力なら 0x4D21E0（GUI の更新）。
- 加算後に下限・上限をかけるコマンド。いずれも v = int32(v + n) を計算し、負なら 0 にする:
  - addLoyal（+0xC0、上限 100）。
  - addMerits（+0xBC、上限なし）。
  - addTrust（+0xC4、上限 100）。
- levelup / addLevel（0x4AB3E2）: n 回 {+0x16C = +0x170; 0x58A650}（`forced_level_ups`）。
- setLevel（0x4AB4BD）: 0x58B7F0(ECX = 0, def, n) だけを呼ぶ。0x58AFA0 は呼ばない。
- changeClass / changeRace（0x4AB55E / 0x4AB629）: 0x49C450 の値を +0x54 / +0x38 に代入し、0x58C0E0(def, 0) を呼ぶ（既存の port）。
- setLeague / resetLeague・setTruce / resetTruce（0x4A7B35 / 0x4A7F03）:
  - リスト形式: set は引数2個以下、reset は1個以下の場合。L の全順序対 (i, j)（i ≠ j）について処理する。
  - ペア形式: それ以外の場合。(a, b) の1回だけ。set の n は a、b の解決より先に読む。
  - 書き込む値: v = n（set）または 0（reset）。v = −1 ならそのまま、それ以外は v + turnproc+0x14。
  - leg は 0x46B8D0（キーは名前順）。trc は 0x46BB80 で、キーは "@trc_"+ECX+EDI（引数順）。リスト形式では両方向、ペア形式では a→b の1方向だけになる。
- addDiplo / setDiplo（0x4A82D1）:
  - 引数2個以下: リスト形式で全順序対。
  - 3個以上: n = 0x49CCA0(arg2) を先に読み、(a, b) の1回だけ。
  - add は 0x46B3A0(a, b, 0x46B230 + n)、set は 0x46B3A0(a, b, n)（0..100 にクランプ）。
- addUnit（op10 0x4A8F00）。詳細は `_w_add_unit` の docstring:
  - 宛先が勢力の場合:
    - 0x591610 が偽なら何もしない。
    - 首都（0x5937D0）が自勢力の spot なら、0x5AD220(首都) を使う。結果が NULL なら首都を使う。
    - そうでなければ +0x64 の先頭の spot。
  - 宛先が spot の場合: その spot。第3引数が "roam" なら放浪させる。
  - 宛先が def の場合:
    - 0x585CC0 のリーダーでなければ何もしない。
    - 部隊が満員（|+0xD4| ≥ [0x65C118] − 1）なら、最初の非人材メンバーを外す（ベクタと spot 集合から外すだけで、def は消さない）。
  - 名前ごとの処理:
    - 既存の人材 def、または名前に '+' を含む既存の def（0x4A6CB0）なら、それを移動する。
    - それ以外は 0x466F60(n, 0xAB42F8, spot ≠ NULL) で作る（entry 0x4A92B6）。作ったものが人材で、名前が n と違えば 0x463590 で削除する。
    - 移動の手順: 放浪中なら 0x460F10。リーダーなら 0x598450(spot, def, 0)。メンバーならリーダーのベクタと spot 集合から外す。
    - その後 +0xCC = 0、+0xC0 = 100 にしてから、次のいずれか:
      - roam: 0x460E90。
      - spot: +0x78 = 1、+0x7A = 0。politics が "on" なら def だけを +0x1C に入れ、そうでなければ 0x598410（def とメンバー全員）。
      - def 宛て: +0x78 = 0、+0x7A = 0x585CA0。リーダーの +0xD4 に push し、リーダーが放浪中でなければ、その spot 集合にも入れる。
- 0x5AD220（空きのある自勢力 spot の探索）:
  - BFS で、push の時点で訪問済みにする。
  - 所有者が P0 の spot で、兵数（0x597A50）が +0x88 未満ならそれを返す。+0xB8 は見ない。
  - 他勢力の spot は展開しない。
  - 展開のたびに random_shuffle する。リンクが2本以上ある場合は §79.4 と同じ理由（リンクの順序が未確定）で Gap。
- eraseUnit（op11 0x4A9478）:
  - 放浪中の場合: s = 0x583CF0 を取ってから 0x460F10。メンバーのうち人材は s で放浪させ（0x460E90）、それ以外は削除する。
  - 放浪中でない場合: メンバーのいるリーダーは、部隊を先頭のメンバーに引き継ぐ（+0x78 = 1、+0x7A = 0、+0xC0 = 100、残りのメンバー）。その後、リーダーのベクタと spot 集合から外す。
  - 最後に 0x463590 で削除する。
- eraseUnitTroop（op12 0x4A96F5）: メンバーを spot から外して削除し、その後にリーダーを外して削除する。
- プレイヤー def（+0x74）を消す場合、ctx+0x50 = NULL、ctx+0x54 = &ctx+0x58（無名勢力オブジェクト）になる。このモデルでは表現できないため、変更する前に Gap にする。
- gread / gwrite（GENERAL op76 0x4A5F53 / op77 0x4A60D1）:
  - グローバルデータファイル（0x428010 / 0x428710）を使う。ゲームの状態の外側。
  - gread(k, v[, L]): VarMap_Set(v は生の名前, rec+0x1C, 1)。3番目の引数は '@' を外さない生のキーで、[rec の文字列] を入れる。
  - gwrite(k, n[, t]): 0x428710(k, t, n)。
  - `EventBridge.global_store`（read / write）が None なら Gap。
- 実データ（sci1）: 初期状態の politics フックも SCRIPT_END まで実行できるようになった（ptest 545 回、eraseUnit 1 回）。
- テスト（`TestWorldAndUdCommandsWRQ20261013`。合計 9件）。全体: 259 OK。
- 既存テストの入力を更新した（2026-10-13 付のコメント）。fight の「未移植コマンドで Gap になる」例を、addUnit から removeSpot に替えた。期待値（Gap）は変えていない。

### §79.7 roamUnit / eraseUnit2 / changeMap 系（STATIC、実装済み）
- roamUnit / roamUnit2（op13 0x4A98FD）:
  - S = 0x467E90(s1(arg1))。引数があるときだけ求める。
  - 放浪中の def: S があれば 0x460E90(def, S)。なければ何もしない。
  - それ以外:
    - sp = S、なければ 0x583CF0(def)。NULL なら次の def へ。
    - roamUnit の場合だけ、リーダーの部隊を先頭メンバーに引き継ぐ（roamUnit2 は部隊ごと動く）。
    - リーダーのベクタから外す。
    - 0x598450(sp, def, 0) を呼ぶ。S が def の実際の spot と違っても、S から外そうとする（native の挙動。元の spot 集合には def が残る）。
    - 0x460E90(def, sp)。
- eraseUnit2（op14 0x4A9B6D）:
  - x が勢力なら 0x593550、spot なら 0x597F40 で対象を取る。どちらでもなければ何もしない。
  - +0x77 でない各ユニットについて、T(s1(arg_i)) == T(名前) となる引数が1つでもあれば、eraseUnit と同じ手順で削除する（部隊の引き継ぎ → リーダーのベクタ → spot 集合 → 0x463590）。
- changeMap（op44、spot+0x2C）/ changeDungeon（op46、+0x48）: 対象の各 spot に s1(arg1) を代入する。
- changeCastle（op45 0x4AC794）: arg1 は ExpresNum でなければならない（0x4528A0 の検査付きキャストで、違えば bad_cast）。spot+0x8C = n。
- 共通: プレイヤー def（+0x74）を消す場合は、変更する前に Gap にする（§79.6）。
- 実データの探索（sci1、橋あり、セーブとグローバルデータは仮の hook）: turn 0 の phase 31 で WORLD:changeMap の Gap → 解消した。
- テスト1件を追加（合計 10件）。

### §79.8 WORLD コマンド（続き 2）（STATIC、実装済み）
- addFriend / eraseFriend（op49 0x4ACA77）: 既存の `friend_script` に接続した。最初に 0x586320 を呼ぶので、空の集合は生成され、rand() を使うことがある。
- add/set 系（L と n を取り、int32 で加算するか代入する）:
  - spot（0x467E90）: addGain +0x80（0x4AC407）、addCastle +0x84（0x4AC4ED）、addCapa +0x88（0x4AC5D3。加算・代入の後に 24 で頭打ち）。
  - 勢力（0x467F40）: addTraining +0xD4（0x4AADB1）、addTrainingUp +0xD8（0x4AAE9D）、addBaseLevel +0xDC（0x4AAF83）。
- setDone（op39 0x4AC1D3）: f は arg1 の生の文字列。"on" なら def+0xC8 = turn、それ以外なら turn − 1。
- addStatus / setStatus（op38 0x4ABFBD）:
  - k = s1(arg1)、n = 0x49CCA0(arg2)。
  - 表 0x68C6E0 の11個の名前（hp, mp, attack, defense, magic, magdef, speed, dext, move, hprec, mprec）と k を比較し、一致したもののフィールドを変える。
  - フィールドは hp +0x178 … mprec +0x19C。speed +0x194、dext +0x190、move +0x1A0 の順序に注意。
- removeSkill（op37 0x4ABE77）: 戦闘ユニット（GM モード 2）だけを対象にする。それ以外のモードでは何もしない。モード 2 は戦闘担当の範囲なので Gap。
- changePowerName（op16 0x4AA0F2）:
  - 勢力 +0x74 = s1(arg1)。
  - 勢力が見つからない場合は NULL+0x1D を読む（0x4AA17E）→ ネイティブはクラッシュする。`NativeCrash` で表す。
  - 現在勢力がプレイヤー勢力なら 0x4D21E0（GUI）。
- changePowerFlag（op17）: +0x40 = t。GM モードが 1 なら 0x4A6CE0（GUI）。勢力が見つからなければ何もしない。
- changePowerFix（op18）: arg1 の生の文字列で決まる。on 1 / home 2 / hold 3 / warlike 4 / それ以外 0。
- setPowerHome（op51 0x4AA42D）: +0xC0 を空にしてから、0x49C950(arg1) の要素を入れる。引数が1個、またはリストが空なら ["@@@@@"]。これが `home_c0` を書く処理（従来 VERIFY だったもの）。
- erasePowerMerce（+0x90 を空に）/ erasePowerStaff（+0xA0 の集合を空に）。
- addPowerMerce[2]: s1(arg_i) を push_back する。2 の形では、"@@" が無ければ追加する。
- addPowerStaff[2]: 集合に insert する。2 の形では "@@" も insert する。
- 勢力に表示用のフィールドを追加した: `StrategyPower.name_74` / `flag_40`（初期値は VERIFY で None）。
- 全体: 263 OK。
- 未移植: changeMaster（0x4AA57A。0x4692C0 / 0x469250 / 0x5924B0 / 0x585890 を使う）、changePlayer（0x468F90）、addPower / erasePower / unionPower、addSpot / removeSpot、setEnemyPower 系、setArbeit。いずれも Gap のまま。

### §79.9 戦闘終了の受領書（receipt）と、0x493630 が積む world フック（STATIC、実装済み）
- Work の共有キューの照合結果（2026-10-13、WORK-WRQ-RECONCILE-20261013-01）に、「戦闘側が必要とする終了 receipt と scene cleanup を、まだ生成していない」とあった。これに対応した。scene の後片付け自体は Work の担当なので、ここでは行わない。
- 0x493630 は world モード（モード値 == 1）のとき、0x432EE0('world', 1, 0, 1) を呼ぶ。呼ぶ場所は2か所:
  - 0x494E4D（flag 0 の経路）
  - 0x496121（flag 1 の経路）
- 0x432EE0 はイベントの本体を VM に**積む**だけ（§18）。本体が実行されるのは 0x493630 が戻った後、つまり遅延削除（0x463590）の後になる。
- 第2引数は 0（ターン処理側は 1）。この場合は 0x432EE0 の [esp+0x90] == 0 の経路を通るが、その意味は VERIFY。
- 実装:
  - `BattleEndReport.queued_hooks` に (フック, 引数, 呼出し VA) を記録する。
  - `battle_end_receipt(w, battle_id)` が、適用済みの戦闘についてだけ、frozen の `BattleEndReceipt` を返す。中身:
    - stages
    - 削除した def（その def を持つ Unit は戦闘側で破棄が必要。ポインタが無効になる）
    - 滅亡した勢力・新しく建った勢力、player_def_lost
    - GUI イベント（native の順）
    - 積まれたフック
    - 再開の条件（FrameGates）: scene_not_world が False、answer_pending が False、フックが積まれた場合は vm_busy_431fb0 が False
  - 未適用の battle_id を渡すと Gap（receipt は作らない）。
- 未回答のダイアログ、未適用の battle_id、scene が world に戻っていない、のいずれかの状態のまま戦略の tick を進めない、という規則は、既存の `frame_blockers` / `resume_frame_474f10` とこの receipt の条件で担保する。
- テスト1件（`test_receipt_reports_queued_world_hook`）。

<a id="f-80"></a>
## §80 WRQ-20261014-CLAUDE-YAJU-ATTACK: 田所(yaju)の sw_karate0 一回分の接続仕様（STATIC＋DAT_DERIVED、ACTUALなし）


> 原本3017〜3025行は部分回収の対象外（held_native_paragraph）。


### 80.1 関係するフィールド（パーサ FUN_00599BD0、STATIC-C）
| キー | Skill の位置 | 変換 | 値（DAT_DERIVED） |
|---|---|---|---|
| func | +0x40 | 未指定=0、sword=1、missile=2、heal=3、summon=4、charge=5、status=6（0x59CAE0..0x59CC34） | root=1。joi、joi2、pr0=0。js 系=2 |
| next / next2 / next3 / next4? / pair_next | +0x8C（長さ +0x9C）/ vec +0xA8 / vec +0xB8 / +0xC8（長さ +0xD8）/ +0xE4（長さ +0xF4） | 文字列 | — |
| rush / rush_degree / rush_random_degree / rush_interval | +0x74 / +0x7C / +0x80 / +0x78 | interval は 0→5、−1→0（B1930） | joi: 2 / 0 / 10 / 4 |
| bom | +0x1C0 | byte | 全て 0 |
| hard | +0x1C4 | on=4、それ以外は数値 | 全て 0 |
| hard2 | +0x1C8 | — | 0 |
| onehit | +0x1CC | — | 0 |
| homing | +0x1D8 | on=180、fix=1810、hold=3610、origin=−180、数値。いずれも ×π/180（[0x65C4C0]=0.0174533） | joi: origin（−π） |
| collision | +0x168（長さ +0x178） | 文字列 | js 系 = "none" |
| offset（相殺） | +0x134 | 0x59C9C7..0x59CA8A、値 on | root、js 系 = on |
| wait_time | +0x23C | — | joi=6、pr2=2 |
| joint_skill | +0x244 | on なら +0x26E=1、+0x24C=−3。center 未宣言なら +0x2B8=1（0x59F6CD..0x59F767） | joi、joi2、pr0 |
| damage | +0x24C | 未宣言は 0 | root=0、js=−3、jsb=0、js2=0、punch_hit=−3 |
| slide / slide_speed / slide_delay / slide_stamp | +0x254 / +0x258（×0.01）/ +0x260 / +0x264 | — | root: 90 / 0.16 / 0 / 0 |
| next_last / next_first / next_order / next_interval | +0x26E / +0x26F / +0x270 / +0x274 | — | root: next_first=on |
| mp | +0x278 | — | 全て 0 |
| str / str_ratio | +0x27C（mode 0..6）/ +0x280 倍率（×0.01）、+0x288 | B §482 | root: attack*0 → mode1、0.0。jsb: mode1、1.00。js2: mode2、0.10 |
| range / check | +0x290 / +0x294 | — | js 系 40 |
| speed | +0x2A0（×0.01、0x59AE85） | — | js 系 900 → 9.0。pr2 1800 → 18.0 |
| exp_per | +0x2A8 | off は番兵値（T012 §78–81） | root=off、js 系=65 |
| time | +0x2B0 | 未宣言は 0 | punch_hit=8、pr=11 |
| center on / end | +0x2B8 / +0x2B9 | — | — |
| d360 / d360_adj | +0x3B1 / +0x3B8 | — | js 系: on / 45 |
| anime / anime_interval | +0x3E8 / +0x3EC | — | punch_hit: 4 / 2 |
| slow_per | +0x200（×0.01） | — | root: 0.8 |

### 80.2 発動の契機と後続技能の生成（STATIC-C）
- **後続生成は Missile::vf22（0x54DCA0）だけ**。仮想関数 +0x58 が vf22 にあたる。
  - 起動条件は、次のいずれかがあること: next、next2、next3、+0xC8 の文字列。
  - 選択の優先順位:
    1. 引数 unit=0 で +0xC8 があれば +0xC8。
    2. next3 が空でなければ、**全要素をベクタ順（index 0..n−1）に1回ずつ生成**する。
    3. それ以外で next があれば next。
    4. それ以外は next2 から1つ。next_order(+0x270)=0 なら rand() を1回使って選ぶ。on なら missile+0x1AC の順番。
  - next_order は next2 にしか効かない。joi の next_order=on は next3 には影響しない。
  - 子の func による分岐:
    - func=4: summon 0x54E7B0 / 0x54F720。
    - func=3: 0x54E0B0。
    - それ以外: 子の rush≠0 なら 0x54F720（Rush）、rush=0 なら **580280（拒否範囲。VERIFY）**。
  - **子の標的**: 子の homing≠0、または親 Skill の +0x1CD、または**親の joint_skill(+0x244)** が立っていれば、親ミサイルの +0xB4（保持している標的）を渡す。どれも立っていなければ、vf22 の引数（命中したユニット、または 0）を渡す。
  - 新旧ミサイルの連結は +0x194 / +0x198 で行う。
- **ミサイル側の vf22 呼び出し（Missile::vf01 0x54BA00）**:
  - 有効になって最初のフレームで、missile[0x60]==0 かつ next_first のとき。
  - next_interval(+0x274)≠0 なら、フレーム数が next_interval の倍数のとき。
  - 終了時（time 超過や射程到達）に、next_last(+0x26E) が立っていて、まだ終了フラグ missile[0x3E]==0 のとき。
  - 命中時（FUN_0054DAE0）に、next_interval==0 かつ next_first==0 のとき。引数は命中したユニット。
- **ユニット側（剣 func=1）は Unit::vf31_shared3（0x57E650）**:
  - next が空なら next2 を Rng_RangeInclusive で選ぶ（next_order=0 のとき）。
  - **next_first=on**: 子をその場で生成する。
    - 子の rush≠0 なら 0x54F720。rush=0 なら 580280。
    - 親の homing≠0 なら標的ユニットを渡す。0 なら、ユニット中心から標的点までの角度を FUN_00447150 で求めて渡す（Rush 側は +0x1FC=1、+0x200=その角度）。
    - その後 vf32 を、遅延する子なし（param_5=0）で呼ぶ。
  - **next_first=off**: 子を Unit+0x1E49C に預け、突進経路の中間点（FUN_005795E0 で index==全長/2 のとき）に生成する。
- **pair_next（+0xF4≠0）**: vf31 の末尾で、next の処理の後に1回生成する（rush=0 なら 580280、そうでなければ 0x54F720）。その後 0x57BE30 を呼んで AL=1 を返す。
- **joint_skill**:
  - ロード時に damage=−3（命中判定なし）、next_last=on、center=on を強制する。
  - 実行時には、vf22 で子の標的を親ミサイルの標的に固定する。
  - 位置と向きは 580280 内部で決まるため VERIFY。
- **wait_time**: ミサイルごとのカウンタ missile[0x68]。vf01 の先頭で次のように扱う。
  1. missile[0x68] が wait_time 未満なら、+1 して何もせずに戻る。
  2. +1 した結果がちょうど wait_time で、かつ sound リスト（Skill+0x30≠+0x34）があれば、FUN_004b9f70 で効果音を鳴らして戻る。
  したがって、有効フレームは wait_time+1 回目の vf01 から始まる。**親（root）にも Rush にも作用しない**。Rush の間隔は Rush 側の +0x1F4 カウンタである（B1218、Work の native_rush_missile と既存の RuntimeActions）。

### 80.3 一回の攻撃の時系列
T0 は Unit::vf31 が sw_karate0 で 1 を返すユニット tick とする。
相対 tick は「各オブジェクトの vf01 が呼ばれた回数」で表す。生成されたフレームのうちに最初の vf01 が呼ばれるかどうか（以下 e∈{0,1}）は **VERIFY**。

| 段階 | 時点 | 入力 / 条件 | 状態変化 / 出力 | 乱数 | 根拠 |
|---|---|---|---|---|---|
| R0 受付 | T0 | Unit+0xC0≥0。mp≠0 なら MP≥mp。標的 Unit+0x1E570 が非null | 失敗なら 0 を返し、何もしない | — | vf31 0x57E650 先頭 |
| R1 向きと MP | T0 | 標的の中心 x と下端 y | Unit+0x18688 = 8方向（&7）。MP −= 0。Unit+0x1868C = 0。rush>1 の連撃予約はなし（root の rush=0） | — | vf31 |
| R2 混乱による外れ | T0 | Unit+0xCC<0 のときだけ | 判定値 < DAT_0065bd60 なら標的点を乱数でずらし、R3 を飛ばす | Rng_RangeInclusive 1回。外れたらさらに rand() 1回 | vf31 0x57E79D/0x57E7FF。フィールド名は VERIFY |
| **R3 root のダメージ** | T0 | damage(0)≥0 かつ str mode1≠0 | **Damage_Core_0x550E70(context=Unit+0x7C, 標的) を倍率 0.0 で呼ぶ**。exp_per=off なので EXP は早期 return | core 内の rand（Work の compute_resolved_damage では2回） | vf31 0x57E7E5、B T012 §292・§971 |
| R4 効果音 | T0 | root に sound リストがあるとき | FUN_004b9f70。inputs にはリストがないので鳴らない | — | vf31 0x57E89F |
| R5 連撃の生成 | T0 | next_first=on、子 joi の rush=2、root の homing=0 | 0x54F720(joi, 0, &角度)。Rush+0x1F4 = 4（interval） | — | vf31 0x57EA48..5D、0x54F990 |
| 既存保留範囲のため非収録（旧保存版3182行） | | | | | |
| R7 pair_next | T0 | karate_pr0、rush=0 | 580280 で生成（**VERIFY**） | 580280 内部は VERIFY | vf31 末尾 |
| R8 後処理 | T0 | — | 0x57BE30 を呼び、1 を返す | VERIFY | vf31 |
| S0 / S1 連撃 | Rush の tick 1 と tick 5（+e） | rush_degree=0、rush_random_degree≠0 | 弾ごとに rand() 1回 → 580280(joi, …, 序数)。2発目で 0x4C22B0 を呼んで非活性化 | **弾ごとに CRT rand 1回**（Work の resume_rush_direction 0x55022A→0x55037F） | RushMissile::vf01 0x5501A0、B1218 |
| J 待機 | joi の vf01 1〜6回目 | wait 6、sound なし | 何もしない | — | 0x54BA00 先頭 |
| J 有効 | joi 7回目 | speed 0、homing origin(−π) | 位置は発動者の中心に追従（center 強制）。step 0→1。damage −3 なので命中判定なし | — | 0x54BA00 の speed==0 分岐 |
| J 終了 | joi 8回目 | time 0 < step 1、next_last 強制 on | vf22 → joi2 を1回生成（標的は joi+0xB4）→ 消滅 | 580280 内部は VERIFY | 同上 |
| K | joi2 の 1回目 / 2回目 | joint のみ | 2回目に vf22 → **js、jsb、js2 をこの順に生成**（標的は joi2+0xB4）→ 消滅 | 同上 | vf22 の next3 ループ |
| P | pr0 の 1回目 / 2回目 | 同じ型 | 2回目に karate_pr、karate_pr2 を生成（どちらも damage −3 で演出のみ） | 同上 | 同上 |
| C 飛翔 | 子の 1回目〜 | speed 9.0（パース時の値。1フレームあたりの速度は 580280 で設定するため VERIFY）、range 40 | 80.4 の順で処理 | 80.4 | 0x54BA00 |
| H 後続 | jsb が命中した tick | — | vf22(命中ユニット) → punch_hit を生成。damage −3、time 8 なので約 9〜10 tick で消える | 580280 内部は VERIFY | 0x54DAE0 |

1発（S_k）あたり、子が最初に命中判定できるのは「joi 生成 + 6(待機) + 2(joi) + 2(joi2) + 1」= **生成後およそ 11 tick 目**（+e の累積は VERIFY）。
1回の攻撃で効果を出す子は **2発 ×（jsb 1回 + js2 1回）**。DOC の「[攻撃×100％]（2回）[魔力×10％]（2回）」と一致する。

### 80.4 子ミサイル（js / jsb / js2）の1フレーム（Missile::vf01、STATIC-C）
1. フレームカウンタを進める。旧値 f = missile[0x60]、その後 +1。hard=0 のとき、この時点で cStack_81=0。
2. 移動弾（speed≠0、arc/drop/circle なし）は cStack_81=1。
   未終了なら次を行う。
   - 移動累計 d = ftol(missile+0x100)。
   - **range ≤ d なら**、next_last があれば vf22（js 系にはない）。その後、終了フラグ missile[0x3E]=1。
   - d += |速度[0x3A]|。
3. 終了していれば step を +1 する。**time(0) ≤ step なら消滅**（FUN_00515420）。
4. next_interval による生成（js 系は 0）。
5. 命中判定を許すかどうか: hard=0 なら毎フレーム。ただし **f < damage の間は禁止**（damage が正なら命中の遅延フレーム数として働く）。
6. 弾の矩形があり、missile[0x71]==0 のときだけ以下を行う。
   - **offset=on かつ未終了**: FUN_00515470 で重なっている相手側の弾を探す。見つかれば相手と自分の vf21 を互いに呼ぶ。
     - vf21 0x54DB60 では、自分の hard2 ≤ 相手の hard2 なら自分を終了させ、衝突演出を出す。
     - 演出: collision 宣言がある（"none" を含む）なら、名前で引いて 580280。宣言がなければ、全体設定 0x65CD54 または "MissileFlash"。
     - **collision は相殺の演出指定であり、ユニットへの命中判定とは無関係**（STATIC-C）。"none" を引いた結果（null か）と 580280 の扱いは VERIFY。
   - **命中判定**: 未終了、bom=0、**damage > −2**、cStack_81 のとき。
     - FUN_004E5860（単体）でユニットを探す。
       - 走査順: 弾の AABB（+0x40..+0x4C）を格子余白だけ広げ、y→x の 16px 格子セル順に、セル内はベクタ順。
       - ユニットの判定矩形は Unit+0x40..+0x4C。Unit+0x230≠0 なら、その半径の正方形（下端基準）。
       - 陣営: ユニット側の勢力種別（1/4）を、発動者側 XOR 弾+0x19C と比べる。+0x19D（味方も対象）、+0x19E（発動者のみ）、+0x19F の各フラグは 580280 で設定されるため VERIFY。発動者は除外する。
       - 発動者+0xC8<0 のとき rand 1回。
       - d360 は、弾の縦横比が 2 以上のときだけ回転方向に分割する。28×28 は単一矩形。
     - 見つかった対象の +0x66≠0 なら、ダメージなしで終了（VERIFY: 盾などか）。
     - それ以外は **FUN_0054DAE0**。
       - damage≥0 かつ str≠0 なら、Damage_Core(弾+0x78 の context, 対象)。
       - next_interval==0 かつ next_first==0 なら vf22(対象)。
       - onehit なら step=1000000。
       - **hard==0 なら終了（貫通しない）**。
   - bom≠0 の場合は FUN_004E6110 で全対象を順に処理する（今回は該当しない）。
7. 移動。
8. 結論:
   - **js（damage −3）は命中判定を一度もしない**。演出だけで、sound defense を持つ。
   - **jsb と js2 はそれぞれ最大1回、最初に重なった敵ユニット1体にだけ効果を与える**。同じ対象に2回当たることも、複数の対象に当たることもない。
   - 命中した次の tick で消滅する。
   - 命中しなければ、range に届いた tick で消滅する（1フレーム 9px なら 6 tick 目。命中判定ができるのは 1〜5 tick 目。VERIFY）。
   - damage −1 / −2 は、命中しても core を呼ばずに後続と終了だけを行う（今回は該当しない）。

### 80.5 既存のダメージ計算へ渡す入力（Work: native_dat_damage_adapter / compute_resolved_damage）
| 段 | source | target | mode | scale | ratio | resistance の鍵 | EXP | MP |
|---|---|---|---|---|---|---|---|---|
| root（R3） | 田所 | Unit+0x1E570 | 1 | 0.0 | +0x288（未宣言） | b"sw"（root の attr。+0x110 の生の値） | off（番兵） | 0 |
| jsb の命中 | 発動者（弾の context） | 命中ユニット | 1 | 1.00 | 未宣言 | b"sw" | exp_per 0.65 | 0 |
| js2 の命中 | 同上 | 同上 | 2 | 0.10 | 未宣言 | b"msw" | 0.65 | 0 |

- str は "attack * 100" のように空白を含む。トークン分割は Work の既存ローダーに従い、ここでは数式を再定義しない。
- **DELTA**: root は「str0 なのでダメージなし」ではない。STATIC 上は倍率 0 で core を呼んでいる（B §292、§971 の scale0 分岐）。最終的な値は既存の select_final_damage_handler_branch に任せ、短絡させないこと。乱数の消費もここで起きる。

### 80.6 Work が今すぐ接続できるもの / まだできないもの
- **できる**（決定的な意味として扱える）:
  - R0〜R8 の順序。
  - root の core 呼び出し（倍率 0）。
  - next_first による Rush の即時生成（既存の RuntimeActions.start_rush に (2,4)）。
  - 突進 14 経路フレーム。
  - joi の待機 6 → 7回目で有効 → 8回目で joi2 → その2回目で next3 の3体をベクタ順に生成。
  - 子の標的を親ミサイルから受け継ぐこと（joint）。
  - 子の処理順（射程 → 消滅 → 相殺 → 命中）。
  - 単体ヒット・非貫通・命中後の消滅、punch_hit の生成時点。
  - 80.5 の入力。
  - Work の validate_resolved_skill_path（root→next→next3[1]）に命中したユニットを渡せば、既存の HP/EXP 処理へつながる。
- **できない**（580280 が拒否範囲のため）:
  - 子・pair・punch_hit の初期位置、角度、1フレームあたりの速度。
  - start_random_degree=8 の乱数を使う時点と式。
  - 弾の矩形が w/h そのままかどうか。
  - +0x19C..+0x19F の陣営フラグ。
  - wait_time=0 の弾の効果音の時点。
  - collision="none" の解決。
- **できない**（その他）:
  - 生成されたフレームのうちに tick するか（e）。
  - オブジェクト間の tick 順と乱数の交差順。
  - Unit+0xCC / +0xC8 の正式名と閾値 DAT_0065bd60 / 0065bd64。
  - slow_per の消費先（vf31、vf32、0x57E1D0、0x5795E0 にはない）。
  - 0x57BE30 の作用。
  - 対象+0x66 の意味。
- 範囲外: AI が発動を判断する条件と射程（「接敵時」）。Work の既存の発動受付を使う。

### 80.7 最小テスト（Work 向け、合成 + DAT_DERIVED。原作との一致を主張しない）
1. 標的が null なら vf31 相当は何もしない（MP、乱数、生成すべて変化 0）。
2. root で core を倍率 0・mode1 で1回呼び、exp_per=off なので EXP は増えない。
3. next_first により T0 で Rush(2,4) を生成し、Rush の tick 1 と 5 に弾を出す。弾ごとに rand 1回。
4. joi は vf01 の 1〜6回目で無作用、7回目で有効、8回目で joi2 を1体生成して消える。
5. joi2 は2回目に js、jsb、js2 をこの順で生成し、子の標的は親の標的になる。
6. js（damage −3）は命中探索を呼ばない。
7. jsb が1回目の tick で敵と重なれば、core を mode1・倍率1.0・b"sw"・EXP 0.65 で**1回**呼び、punch_hit を命中ユニット標的で1体生成し、次の tick で消える。重なり続けても2回目はない。
8. js2 は mode2・倍率0.1・b"msw"。後続は生成しない。
9. 敵がいなければ、射程に届いた tick に消滅する。ダメージも punch_hit もない。
10. 味方とだけ重なる場合は命中しない（+0x19D=0 と仮定。VERIFY として明示）。
11. 静止した敵1体に対して全体で、root core 1回 + jsb 2回 + js2 2回 + punch_hit 2体 + pr 系演出。
12. 突進の経路長が 14 で、中間点で子を生成しない。

### 80.8 残る不足と、必要な資料・観測
1. **580280 本体（拒否範囲）**。子と pair の位置・角度・速度・矩形・陣営フラグ・start_random_degree・効果音を決めている。代替手段は次のどちらか。
   - 許可された保存抜粋の提供（再取得ではなく、ユーザーの承認が要る）。
   - 原作観測: 田所の通常攻撃1回を1フレームずつ録画し、拳画像の出現位置と軌跡を田所・標的との相対で読む（乱数そのものは観測できない）。
2. 新しいオブジェクトの同フレーム tick（e）と、オブジェクト間の tick 順。B/REA の保存済み task 反復（0x4C2240 の追加と、その巡回元）、または上のフレーム録画が必要。
3. collision="none" の結果。敵の弾と拳が相殺した場面の録画で、閃光の有無を見る。
4. slow_per の消費先。保存済み B の速度計算資料、または移動中に発動した場面の観測が必要。
5. Unit+0xCC / +0xC8、DAT_0065bd60 / 64、0x57BE30、対象+0x66。いずれも保存済み B / REA の該当 VA が必要。

<a id="f-81"></a>
## §81 WRQ-20261014-CLAUDE-YAJU-ATTACK（続き）: 原作マップテストでの読み取り専用観測の準備（観測準備のみ、ACTUAL 0）

[2026-10-14 / Claude] **状態: 準備まで完了。原作プロセスでの実測は未実施**。
- 原作は起動しておらず、実測値は 0 件。Golden 0、MATCH 0。
- §80 で確定した事項は変更しない（root の core 呼出、damage −3 と 0 の違い、collision、next3 の順序）。
- 拒否範囲（580280、4C28D0 ほか）は今回も読んでいない。
  - 例外が1件ある。0x4C24B0 のフレーム印を探すために decomp ファイル全体を grep したとき、1行だけ 4C28D0 本体内の行がヒットした。この行の内容は使わず、それ以上も読んでいない。
  - フレーム印には、拒否範囲外の 0x4C24B0 が書く M+0x40 だけを使う。

### 81.1 観測手段（確認結果）
1. **このセッションから使える手段**
   - PC 上のシェルはない。Desktop Commander は使用禁止なので使わない。
   - PC 上のファイルの読み書きと、画面操作は使える。
   - したがって、**原作プロセスへ接続できるのはユーザーの PC 上で実行されるスクリプトだけ**。
   - 既存の観測ツールを探したが、該当するものはなかった。
     - REA は静的解析専用で、原作の実行は組み込まれていない。
     - `MANUAL_TARGET_OBSERVATION.md` は手動のスクリーンショット観測の手順。
2. **新規ツール**: `dev_lab/src/hakushin_compat/peer_script01_live_observer.py`（Claude 所有）。
   - 使う API は `OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_LIMITED_INFORMATION)` と `ReadProcessMemory` だけ。
   - 書込み・コード注入・フック・ブレークポイント・スレッド停止・コードバイトの読取りは**しない**。
   - EXE の同一性は、実行中プロセスの実体ファイルの SHA256 を `E8DAC301…` と照合して確かめる。一致しなければ記録しない。
3. **ASLR 対応**: DllCharacteristics=0x8140 で DYNAMIC_BASE が立っている。
   - 毎回の起動で、Toolhelp を使って Vahren.exe の基底アドレスを取得し、VA を再配置する。
   - 起点が合っているかは、GameManager の vtable 一致と、タスク管理の M+4 が GM を指すことの2点で検証する。
   - どちらかが一致しなければ `ObserverGap` で停止し、推測で補わない。
4. **起点**（STATIC-C。保存済み decompile を read-only で読んだもの）

| 起点 | 位置 | 根拠 |
|---|---|---|
| GM | 静的 VA 0x8BE2F0 | 0x5524xx の静的初期化が GameManager::vftable 0x638DF0 を書き込む |
| タスク管理 M | GM+0xC | GameManager::vf01 → 0x4C24B0 |
| active ベクタ | M+0x2C / +0x30 | 0x4C22B0 |
| pending ベクタ | M+0x64 / +0x68 | 0x4C22B0。0x54F720 の GM+0x70 と一致 |
| フレーム時刻 | M+0x40（timeGetTime） | 0x4C24B0 |
| 間隔 | M+0x78（ms） | 0x4C24B0 |
| 陣営と Unit ベクタ | GM+0x1E8630 / +34 / +38、陣営+0x48 / +0x4C | §53 |
| Rush プール | VA 0x8BE278 / 0x8BE27C | 0x54F720 |
| vtable | RTTI の値 | — |
| Skill のタグ | Skill+0（std::string） | 0x599C3C |
| Unit の定義とタグ | [Unit+0x1C8] → def、def+0x1C のタグ | T011、§14 |
| EXP | def+0x16C（次レベルの値は +0x170） | T011 |

5. **識別方法**
   - Unit は、def のタグ（既定は `yaju` と `unit_mt`）で選ぶ。
   - その Unit の標的 +0x1E570 も記録する。
   - 弾（Missile / SimpleMissile / Heal）と Rush は、次のどちらかに当てはまれば記録する。
     - Skill のタグが対象の11種（8技能に sw_karate1、karate_pr、karate_pr2 を加えたもの）のどれか。
     - 発動者（弾は +0x78、Rush は +0x1D8）が監視対象の Unit。
6. **記録する値**
   - Unit: §80 の既知フィールド（矩形、HP、MP、+0x214 の座標、向き、+0x130 / +0x1E4A0 の技能タグ、突進の状態と経路、標的）と EXP。
   - 弾: 既知フィールド（+0x180 フレーム、+0x1A0 待機カウンタ、+0x1A4 step、+0xE8 速度、+0x100 移動累計、+0x118 角度、+0xF8 終了フラグ、+0xB4 標的、前後リンク）に加え、**先頭 0x200 バイトの生データ**。
   - Rush: 既知フィールドと 0x218 バイトの生データ。
   - 意味が確定していない領域は生データのままにし、名前を付けない。
7. **限界**
   - 状態を止めずに読むので、**同じフレーム内で複数オブジェクトが一貫している保証はない**。
     - 各サンプルには、M+0x40 の前値と後値、読取時刻を付ける。
     - 時刻の対応付けには、弾自身の更新カウンタ（+0x180、+0x1A0、+0x1A4）を優先する。
     - 複数の時点の値を1フレームとして合成しない。
   - ポーリングは約 1ms 間隔で、フレーム間隔（M+0x78。実測で確認する）より十分短い。
     - 最短寿命の子弾（§80 の推定で約6フレーム）が丸ごと見えない可能性は低いが、0 ではない。
     - 最初に観測した時点を、生成された時点とは断定しない。生成は「最初に観測した時点以前」、消滅は「最後に観測した時点より後」として扱う。
   - 弾やエフェクトがタスクベクタに登録されているかは 580280 の内部にあたるため **VERIFY**。
     - 実測で Missile 系の vtable が1件も現れなければ、その事実を Gap として報告し、全メモリの探索には広げない。
   - フレーム印 M+0x40 はフレームループの先頭で書かれる。タスク処理の途中に読んだ場合は、同じ印のもとで更新前と更新後が混在しうる。
8. **自己テスト**（合成メモリ、`tests/test_peer_script01_live_observer.py`、6件 PASS）
   - ASLR 基底の誤りを Gap として扱う。
   - 監視 Unit とその標的の抽出。
   - 弾をタグか発動者で絞り込む。std::string の inline 形式と heap 形式の両方を読む。
   - Rush プールの読取りと突進経路の読取り。
   - 異常なベクタを Gap として扱う。
   - 書込み API がないこと。
   - **これは原作での実測ではない。**

### 81.2 マップテストの条件（DAT_DERIVED と Claude の def 生成モデル。実機確認ではない）
- 入口: 起動 → 難易度選択 → 外伝「マップテスト」sci_mt → 勢力 po_mt（名前は「空手部・スキルテストの裏技」）。
  - po_mt の master は `unit_mt`。
  - 敵は po_mt2 で、master は hideshine、中央の sp_mt にいる。
  - 6000_スキルテスト/0maptest.dat の 76〜166 行。
- **`unit_mt` は田所（yaju）ではない。**
  - 継承は `unit_mt : unit_st : yaju`。unit_st は名前が「テスト先輩」で、hp 889464、dext 114、hprec 114514 に変えてある。unit_mt では `skill=boat_gun`。
  - Claude の def 生成（0x58C0E0 の移植）で技能リストを計算した結果:
    - unit_mt: `sw_karate0, ch_karate, buchipa, a_dash, boat_gun, sw_karate1, self_a020, seiretsu, c_as1`
    - yaju: `sw_karate0, ch_karate, buchipa, a_dash, sw_karate1, sp_tea, …`
  - どちらもクラス c_yaju（a020）の skillset `sw_karate` = {sw_karate0（接敵時）, sw_karate1（射程60、`just_next=sw_karate_js_joi`、rush 1）} を持つ。
  - したがって、**標準のマップテストでも sw_karate0 の弾の位置・速度・時刻は観測できる見込み**。
  - ただし、能力値に依存する値（ダメージ、EXP）は田所の値ではない。
  - unit_mt は boat_gun や sw_karate1 も使いうる。ログでは Rush と root の技能タグで区別し、sw_karate0 の回だけを採用する。
- 1ターン目は戦争ができない（DAT のコメントとスクリプトによる）。ターンを終えてから出撃する必要がある。
- 戦闘イベント be_st は siege_system などを呼ぶ。防衛兵器が出現して雑音になる可能性がある。
- **田所本人で観測したい場合は試験用コピー案を使う（未作成）**。
  - 原本フォルダは変更しない。
  - 観測用に別フォルダへ展開したコピーの `6000_スキルテスト/0maptest.dat` で、`power po_mt` の `master = unit_mt` を `master = yaju` にする1行だけを変える。
  - 注意: we_st2（`event_test.dat` の 126〜137 行）は最初のターンに yaju を roamUnit / addUnit し、batman と a0203×7 を配下に加える。そのため、yaju の所属と部隊編成が変わりうる。実際の結果は VERIFY。
  - 作成するかどうかはユーザーが判断する。


> 原本3313〜3328行は部分回収の対象外（personal_path_paragraph）。


### 81.4 観測後に埋める対応表（いまは全て未測定）
| 項目 | §80 の静的推定 | 実測 |
|---|---|---|
| joi、joi2、js 系、pr の初期位置と、攻撃者・標的との関係 | 580280 の内部なので VERIFY | 未 |
| jsb、js2 の1フレームあたりの移動量と向き | 9px/フレーム（パース値。VERIFY） | 未 |
| 親が子を生成してから、子が最初に更新されるまで（e） | VERIFY | 未 |
| wait_time=6 と待機カウンタ +0x1A0 の対応 | 1〜6回目は何もせず、7回目で有効 | 未 |
| Rush 2発の間隔と、各子の出現・命中・消滅 | Rush の tick 1 と 5、子は生成から約11 tick 目 | 未 |
| 突進 14 フレームと子生成の関係 | next_first なので T0 に生成。中間点での生成なし | 未 |
| Unit の vtable（Unit か SimpleUnit か） | §80 は Unit::vf31/vf32 を前提にした。SimpleUnit なら vf31 は 0x546C90、vf32 は 0x544F80 で、別の実装 | 未 |

### 81.5 Work への報告
- **READY にできる範囲**: 観測の準備（ツール、自己テスト、手順）のみ。実測値はないので、Work の実装はまだ変えないこと。
- 次の最小観測: 81.3 を1回行う。結果が一貫しない場合だけ、開始距離か向きを1つ変えてもう1回。

### 81.6 実機ログ01（2026-10-14 01:36〜、ACTUAL・粗い）
**記録の条件と結果**
- ログ: `dev_lab/_work/claude_live_obs_karate_01.jsonl`（25,871,892 バイト）。
- EXE: SHA256 一致、PID 34216、基底 0x440000。
- 起点の検証: GM の vtable と M+4 は一致した。
- フレーム間隔 M+0x78: probe 時は 40ms、diag 時は 10ms。戦闘中か、速度設定によるかは VERIFY。
- **欠陥1**: GM+0x1E8630/34/38 は 3つとも 0 だった。§53 の陣営スロットは、この GM の位置では成立しない。
  - 一方、Player と Enemy の Actionable 部分オブジェクト（RTTI vtable 0x639B2C / 0x638B84、+0x90）はタスクベクタの中にあった。
  - そのため **Unit は 0 件として記録された**。攻撃者のタグは不明のままで、発動者ポインタは 0x4507D008 の1体だけだった。
- **欠陥2**: 毎回のスナップショットで、全タスク（996件）の vtable と Rush プール（48件）を読み直していたため、1回の取得に約 175ms かかった。
  - フレーム時刻 M+0x40 の差の最頻値は 173〜178ms で、**数フレームおきの粗い標本**になった。
  - 時刻印1つあたりの標本数は大半が1回。一時停止中と思われる区間では、同じ印のまま 2104 回取得していた。
- 対策（同日、自己テスト 9件 PASS）:
  - タスクの種類はポインタごとにキャッシュし、新しく入ったものだけを読む。
  - Rush はタスクベクタから拾う。
  - 弾は対象 11 技能だけを記録し、その発動者を自動で監視対象に加える。
  - 陣営は Player / Enemy オブジェクトの +0x48 ベクタから付ける。
  - 弾の生データは 0x1D8 バイト。ログ01で、次のオブジェクトの vtable が +0x1D8 に見えたため。

**粗いながら一致した点（§80 の静的推定 → 実測。攻撃者が田所かどうかは未確定）**

| 項目 | 実測（ログ01） | §80 との関係 |
|---|---|---|
| Rush の間隔カウンタ +0x1F4 | 4 → 発射数 +0x1F0 は 1 → 間隔 1,3 → 発射数 2 で active=0 | tick 1 と tick 5、1回の攻撃で 2発。一致 |
| Rush の角度 +0x200 | 生成時に固定（例 4.8521 rad）。joi 側の +0x118 は ±数 rad/100 ずれる（例 4.9157、4.8129） | 乱数で角度をずらす。式は VERIFY |
| joi | 0×0 の点オブジェクト。待機カウンタ +0x1A0 は 1→6 のあいだ位置が固定。その後フレーム +0x180 は 1→2、step 1 で、位置が発動者に追従 | 待機 6 → 有効 → 次で終了。一致 |
| joi2、pr0 | 0×0。フレームは最大 2、step は最大 1 | 2回目の vf01 で子を生成して終了。一致 |
| js 系の大きさ | 28×28 | w/h のまま |
| js 系の速度 +0xE8 | **9.0/フレーム**。移動累計 +0x100 は 9 ずつ増える | speed 900×0.01。一致 |
| js（damage −3） | 移動累計 54 で終了（射程 40 を 45 で超えた後、さらに +9）。最大フレーム 6 | 射程に届いたときだけ終了。一致 |
| jsb、js2 | 移動累計 9 か 27 で終了（射程未満）。最大フレーム 4 | 命中して終了し、貫通しない。命中の直接証拠（相手 HP）は Unit 未取得のため VERIFY |
| punch_hit | 32×32、最大フレーム 10、step 9 | time 8 → 9〜10 tick。一致 |
| karate_pr | 120×80、速度 0、step 最大 12 | time 11。一致 |
| karate_pr2 | 60×60、速度 **18.0**、待機 2、移動累計 144 で終了 | speed 1800×0.01、range 120。一致 |
| 標的 +0xB4 | js 系は発動者自身（0x4507D008）、pr 系と punch_hit は敵（0x44F69BF8） | joint の標的引継ぎ。js 系の起点は発動者という意味で VERIFY |
| 発動者 | 弾 +0x78 と Rush +0x1D8 が同じポインタ | フィールドの意味を実測で確定 |

**まだ確定しないこと**: 標本が粗いため次の4点は決まらない。ログ02（高速化版）で測る。
- 初回更新までのずれ e。
- 子と親が同じフレームに存在するかどうか。
- Rush の各発と子の相対フレーム。
- 突進との関係。

### 81.7 実機ログ02（2026-10-14 01:55〜01:59、ACTUAL・フレーム単位）
**記録の条件**
- ログ: `dev_lab/_work/claude_live_obs_karate_02.jsonl`
  - サイズ 67,203,509 バイト。SHA256 `7cba0e01…de9e`。
  - 11,517 スナップショット。
- 要約: `dev_lab/_work/claude_live_obs_karate_02_summary.json`
- EXE: SHA256 一致、PID 34216。
- 取得の速さ: 1回の取得の中央値は 7.4ms。フレーム印の差は 23〜35ms（M+0x78 は大半が 40ms、一部 10ms）。1フレームあたり 2〜4 回取得でき、**全フレームを捕捉した**。
- 攻撃者:
  - probe で、タスクから得たユニット 92体の中に `unit_mt`（テスト先輩、Unit vtable、Player 側）が1体いることを確認した。
  - 弾の +0x78 と Rush の +0x1D8 が指すのはこのユニットである。
  - **田所（yaju）ではない**。位置・時刻・角度の規則にだけ使い、ダメージ量や EXP は田所の値として扱わない。
- 検出した攻撃: 31回（Rush が shots=0、カウンタ=4 の状態で現れた回数）。
  - そのすべてで、突進の長さ +0x186D8 = 14 だった。
  - root が sw_karate0 であることは、突進14・pair_next・next_first の挙動から判断した。sw_karate1 である可能性は残るが低いと見る。
  - Unit+0x130 は ch_karate を指していたため、選択中の技能を示すフィールドではない。

**時刻の決め方**
- 同じフレーム印の中に、更新前と更新後の標本が混ざる（印はループの先頭で書かれるため）。
- そこで時刻は、各オブジェクト自身の更新カウンタ（Unit の突進 index、Rush の発射数とカウンタ、弾の待機・フレーム・step）で数えた。
- T0 = 突進 index が 0 になったユニットの更新とする。

**時系列（ACTUAL）**

| 時刻 | 起きたこと |
|---|---|
| T0 | 突進開始（14、index 0）。**Rush を生成**（発射0、カウンタ4）。**karate_pr0 を生成** |
| T0+1 | Rush の1回目の更新で1発目 → joi A を生成（待機0）。pr0 はフレーム1 |
| T0+2 | joi A 待機1。pr0 の2回目の更新で karate_pr と karate_pr2 を生成し、pr0 は消える |
| T0+5 | Rush の2発目 → joi B を生成。Rush は非活性（発射2） |
| T0+8 | joi A 有効（フレーム1、step 1）。位置は発動者の矩形中心に追従 |
| T0+9 | joi A → joi2 A2 を、その時点の発動者の中心に生成。A は消える |
| T0+11 | A2 → **js、jsb、js2 を同じ 28×28 で、A2 の点を中心に生成**。A2 は消える |
| T0+12 | 子が 9px 移動。**jsb と js2 が命中**（大半）。punch_hit を jsb の移動前の中心に生成し、標的は命中したユニット。**同じ更新で敵の HP が減る**（例 6779→6060） |
| T0+13 | jsb と js2 が消える。joi B → B2 |
| T0+14 | 突進終了（フラグ 0） |
| T0+15 | B2 → 子を生成 |
| T0+16 | B の子が命中（HP がもう一段減る。例 5191→4328、4 フレーム後に 4328→3661） |
| T0+17 | js A が射程で終了（移動累計 54、フレーム 6） |

**Work がそのまま使える確定事項（ACTUAL）**
1. **新しく生成されたオブジェクトは、生成された次のフレームに初めて更新される**（e=1）。連鎖のどの段でも同じ。
2. wait_time=6:
   - 1〜6回目の更新で待機カウンタが 1〜6 になる。
   - 7回目の更新で有効になる（frame 1、step 1）。
   - 8回目の更新で next3 を生成して消える。
3. Rush:
   - 生成の次のフレームに1発目、その4更新後に2発目を出す。
   - 角度は T0 の時点で固定する。
   - **θ = atan2(−dx, −dy)**。dx、dy は発動者の矩形中心から標的の矩形中心まで。31回すべてで誤差は 1° 未満。
4. 移動:
   - 1フレームの変位は (−sinθ, −cosθ) × speed×0.01。
   - 位置は整数に丸められる。丸め方は VERIFY。
5. joi の角度 = Rush の角度 + 乱数。
   - 70本の実測で −8.52°〜+6.76°。
   - ±8°（start_random_degree）だけでは説明できず、±10°（rush_random_degree）と矛盾しない。どの乱数を何回使うかは、580280 の内部なので VERIFY のまま。
6. 子の角度 = 親 joi の角度（joi2 経由）。生成位置は joi2 の点。
7. 命中:
   - jsb と js2 は、移動後のフレーム1（69本中43本）かフレーム2で命中し終了する。1回だけで、貫通しない。
   - 命中した次の更新で消える。
   - js（damage −3）は途中で止まらず、射程で終わる。
8. punch_hit は約10更新（step ≤ 9）で消える。
9. karate_pr は step 12 で消える。karate_pr2 は待機2の後、1フレームあたり +18° 回転しながら移動し、移動累計が 120 以上になったら終了する。
10. 突進:
    - 14 経路点。7点で前進し（下端中心を約 4px/フレーム、標的の下端中心へ向かう）、折り返して戻る。頂点は index 6〜7。
    - 振れ幅の上限（§80 の 1.5×Unit+0x228）が実際の制約になっているかは VERIFY。
    - Unit+0x214 は突進中も動かない。表示上の矩形だけが動く。

**まだ確定しないこと / 次の最小観測**
- 田所本人での値（ダメージ・EXP）: マップテストでは観測できない。§81.2 の試験用コピー案か、本編で田所の部隊を使う必要がある。
- 命中と HP 減少の内訳（jsb と js2 のどちらがいくつ減らしたか）: 同じ更新で起きるため、ログ02からは分けられない。
- 位置の丸め規則、関与する乱数の種類と回数。
- Work への連絡: 上の 1〜10 は ACTUAL として接続してよい。ただし新エンジンとの比較はまだなので、Golden / MATCH は 0。

<a id="f-82"></a>
## §82 WRQ-（Claude、2026-10-26）戦略⇄戦闘の場面境界：既存成果の照合と基準アドレスの確定（STATIC、実機観測は準備済み）

[2026-10-26 / Claude] 照合した資料は次の4つ。いずれも読み取りのみ。
- B の `data/T012_STRATEGY_BATTLE_BOUNDARY_INTERFACE_20261021.md`（B-20261021-BOUNDARY-01）
- A の `data/T010_EVENT_SCHEDULER.md`
- D の `data/T015_UI_RENDER_INPUT_AUDIO.md`
- 本 findings の §68 / §73 / §79

新規の解析は、保存済みの Ghidra 出力と逆アセンブルの限定的な読取りだけで、拒否範囲は使っていない。原作 Golden 0、MATCH 0。

### 82.1 新しく確定したこと：基準アドレスは2つある（STATIC-C）

| 名前 | アドレス | ここを基準にするもの | 根拠 |
|---|---|---|---|
| **G = GameManager** | 静的 VA 0x8BE2F0 | +8 = タスクループの終了フラグ、**+0x1EF144 = 場面番号**、+0xC = タスク管理 | GameManager::vf01 0x4B9930 の switch。FadeSheet::vf01 0x543B10 が `G+0x1EF144 = 次の番号; G+8 = 1` |
| **E = engine = G+0x504** | VA 0x8BE7F4 | 戦闘・戦略の資料にある「GM / engine + 0x1EEC3C、+0x1EEC44、+0x1E8630 …」の全部 | 静的初期化 `0x553F60(&0x8BE7F4)`。Unit 初期化で `Unit+0x1E0 = G+0x504`（Unit+0x1DC = G+0x1B8、Unit+0x1E4 = G+0x1EF570）。0x4B99C7 が戦闘場面 0x48D6A0 を `ECX = G+0x504` で呼ぶ |

- **注意**: G+0x1EF144 は E+0x1EEC40 と同じ dword である（0x1EF144 − 0x504）。つまり、モード E+0x1EEC3C のすぐ隣に場面番号がある。
- **§81.6 で陣営スロットが 0 だった理由**: §81.6 は G+0x1E8630 を読んでいた。正しくは E+0x1E8630（= 0x8BE7F4+0x1E8630）。§53 / §73 の「GM+…」はすべて E 基準として読む。
- Work の native モデル（`native_unit_tick` の engine = Unit+0x1E0）とは一致している。

### 82.2 場面の切替機構（STATIC-C と D/T015 の照合）
1. GameManager::vf01 は `while (G+8 != 2)` のループを回す。
   - 毎回 G+0x1EF144 で分岐する。0→0x48AD30、1→0x48C880(world)、2→0x48D6A0(戦闘、ECX=E)、4→0x48B4A0、5→0x48BF60、6→0x48BC70、7→0x48EA60(ECX=E)。
   - その後 `0x4C24B0(G+0xC)`（タスクループ）に入る。
2. タスクループは、G+8 が 0 以外になると抜ける。抜けたら場面番号を読み直す。
3. 場面を変えるのは FadeSheet 系（FadeOutSheet の vtable は 0x6388D4）。
   - フェードの最終段で、次の番号 < 10000 なら G+0x1EF144 を書き、G+8 = 1 にする（0x543B10）。
   - タイトルへ戻る確認で YES のときは、G+0x1EF144 = 0、G+8 = 1（D/T015 393行）。
4. **プラグインで「場面が変わった」を取るなら、置き場所の候補は2つ**。
   - GameManager::vf01 の switch の直前（場面番号を読む位置）。
   - FadeSheet が G+0x1EF144 を書く位置。
   - 通知を「戦闘」と名付けてよいのは、場面番号が 2 のときだけ。画面なしの戦闘は場面が変わらない（82.3）。

### 82.3 開戦から終了まで（B・A・Claude の資料はおおむね一致）

| 段 | 内容 | 資料ごとの一致 / 差 |
|---|---|---|
| 入口 | **0x4922A0(E, skip)** だけが入口。直接の呼出元は 0x4921CD（0x491870 内）、0x522297、0x5222AA（0x521D90 内）。E+0x1EED43 = skip。E+0x1EEDB8 の root を解放する。@battlefield / @battleattack / @battledefense を 0x463610 で共有 map に公開する | B と §73 で一致。B は 0x463610 による公開と、終了時の再公開を追加した |
| skip=0 | FadeOutSheet(2) → G+0x1EF144=2 → 0x48D6A0(ECX=E)：モード 2、`srand(GetTickCount())`、`fight` を発火 | §73。B は「後続の非同期復帰は VERIFY」 |
| skip≠0 | 0x432EE0 で fight を VM に積む → 0x52AD90 → 0x40D0A0(BattleWnd)。**場面は変わらず**、モードは 1 のまま | 一致 |
| 別の初期化 | **0x492710**（呼出元は 0x4103B1、関数 0x40F320）：E+0x1EED44/48、時計、+0x1EEC44/48 などを初期化 | B が新たに見つけた。Claude の資料にはない。どの経路で呼ばれるかは VERIFY |
| battle{} の設置 | 0x492890（VM の 0x433E58 から）：ScriptIF root、モード 2、active 1、3陣営の vf+0xC | §79 と B で一致。0x48D6A0 と 0x492890 のどちらがモード 2 を先に書くかは VERIFY |
| 終了 | **0x493630** だけが出口（FrameDriver の 0x49303A / 0x493082 / 0x4930A1、BattleWnd の 0x40E2B9、script の 0x4A1764）。モード 2 なら 3陣営の vf+0x14 → 0x4C21F0。0x493746 で +0x1EEC44 / 48 と +0x1EED40..42 を消す。@battle 変数3つを再公開する | 一致（A の保存 ASM と §73） |
| 復帰 | 0x48C880 がモードを 1 にする。0x474F10 の冒頭のゲートが開いた後で戦略が再開する | §73.6。B は「World 再入は VERIFY」 |

- **0x4922A0、0x492710、0x492890 が毎回同じ順で呼ばれるかは、どの資料でも確認されていない**。82.4 の実機観測で順序の一部を確かめる。
- 外部 EXE に戦闘を渡す場合の入出力パケット案は、B §IV にある（提案のみ。実装と実証はなし）。

### 82.4 実機観測の準備（ツール拡張、自己テスト 11件 PASS、実測はまだ）
- `peer_script01_live_observer.py --boundary`
  - 読む値: G の +8 と +0x1EF144、E の +0x1EEC3C/40/44/48、+0x1EED18〜60、+0x1EEDB8、陣営スロットとその Unit 数、タスクの種類別の数、`Unit+0x1E0 == E` かどうか。
  - 値が変わったときだけ1行書く（約2秒ごとに生存確認の1行も書く）。
- 確認すること:
  1. E = G+0x504 であること（`unit_engine_ptr_ok`）。
  2. 戦略 → 戦闘 → 戦略で、各値がどの順に変わるか。
  3. 画面なしの戦闘では場面番号が変わらないこと。

### 82.5 実機ログ（ACTUAL、2026-10-26 18:4x、戦略 → 戦闘画面 → 戦略 を1回）
**記録の条件**
- ログ: `dev_lab/_work/claude_live_boundary_scene_20261026.jsonl`（旧名 `_01`。82.6 の注意を参照）
  - 2,761,756 バイト。SHA256 `b427d037…926e`。3272 行。
- EXE: SHA256 一致。
- ASLR: 今回の基底は 0x2C0000 で、G は 0x6BE2F0 に再配置されていた。それでも起点の検証（GM の vtable、M+4 == G）は通った。
- 画面なしの簡易戦闘は、今回は記録していない。

**E = G+0x504 を実機で確定**
- 戦闘中、`Unit+0x1E0 == G+0x504` が True だった。
- E+0x1E8630 / +34 の陣営スロットにある Unit ベクタは 0 → 138 / 187 → 終了時 260 / 247 と変化した。3つ目のスロットは 0 のまま。
- 82.1 の訂正は正しい。

**時系列**（t は記録開始からの秒。st はフレーム印。値が変わった時点だけを抜き出した）

| t | 変化 | 解釈 |
|---|---|---|
| 0 | 場面 1、モード 1、active 0、E+0x1EED54..56 = [0,0,0] | 戦略（world）画面 |
| 17.335 | E+0x1EED55 = 1、行軍数 E+0x1EED5C = 2 | 開戦（0x48F9E0）。関与フラグと行軍2本 |
| 18.169 / 18.567 | 行軍数 1 → 0。**FadeOutSheet（vtable 0x6388D4）がタスクに現れる** | 0x491870 の到着が2回 → 0x4922A0(skip=0) → FadeOutSheet。E+0x1EED43 = 0 |
| 18.795 | **G+0x1EF144 = 2、G+8 = 1**（同じ印のうちに） | フェード完了でタスクループを抜ける |
| 18.812 | **モード 2**。タスクが 2 件に減る | 0x48D6A0 がモード 2 を書く。この時点で戦略側のタスクは片付いている |
| 18.97〜19.15 | 陣営 0 の Unit が 1→138、陣営 1 が 0→187。Unit タスクが 325 件。Player 1件、Enemy 2件 | 場面の初期化（印 65188723 の1フレーム、約 350ms のあいだ） |
| 19.147 | G+8 = 0 | タスクループの再開 |
| 21.07〜21.27 | E+0x1EEC48 が 1→2→3→4。root E+0x1EEDB8 の数 = 17。その後 **active E+0x1EEC44 = 1**、+0x1EEC48 = 0 | battle{} の設置（0x492890）。active はモード 2 より **約 2.5 秒あと**に立つ |
| 21.3〜60 | Missile / Rush が増減する | 戦闘中 |
| 60.224 | **active = 0、root の数 = 0** | 0x493630 の後半（0x493746）で消える |
| 61.924 | **G+0x1EF144 = 1、G+8 = 1**。FadeOutSheet が現れる | world へ戻るフェードが完了 |
| 61.96〜62.01 | タスク 0、陣営ベクタが空になる、**モード 1** | 0x48C880 の world 初期化 |
| 62.032 | G+8 = 0。タスク 323 件 | 戦略が再開 |

**プラグインの「戦闘開始・終了」通知に使える ACTUAL 事実**
1. 戦闘画面への切替は、次の順で見える。
   1. FadeOutSheet の出現
   2. G+0x1EF144 = 2 と G+8 = 1
   3. モード（E+0x1EEC3C）= 2
   4. Unit の生成
   5. 約 2.5 秒後に active（E+0x1EEC44）= 1
   - 「戦闘中のユニットがそろった」を知りたいなら、active = 1 を待つ。「場面が変わった」を知りたいなら、場面番号 = 2 を見る。
2. 終了は、まず active = 0 になる（root も消える）。約 1.7 秒後に場面番号が 1 になり、タスク・陣営が片付き、モードが 1 になる。
   - 終了処理 0x493630 は active = 0 の直前に走る。結果の取得は、active が 1 → 0 になる前後で行う。
3. **場面が切り替わる瞬間には、タスクがいったん 0〜3 件まで減る**。切替の前に取ったポインタ（Unit、陣営、タスク）は、切替の後では使えない。
4. 時間の多くは、フレーム印 1つ分の中（場面の初期化中の約 350ms）に収まっている。フレーム単位のフックで同期処理をすると、その間は呼ばれない。

**未確認**
- 画面なしの簡易戦闘（場面番号は変わらない見込み）。
- 0x492710 が呼ばれるかどうか（直接見える値はない）。
- 撤退、時間切れ、プレイヤーが攻めた側の場合。
- 今回は E+0x1EED55 = 1（関与の種類）だったが、攻めたのか攻められたのかの区別は VERIFY。

### 82.6 実機ログ（ACTUAL、2026-10-26 18:52、画面なしの簡易戦闘を1回）
**ログ**
- `dev_lab/_work/claude_live_boundary_simple_20261026.jsonl`
  - SHA256 `d075ee79…1a91`。90 行。
  - 中身は `_work/claude_live_boundary_01.jsonl`（現在の PC 版）と同じ。
- **注意: 82.5 のログはファイル名の重複で上書きされた**。Claude が保持していた写しを `_work/claude_live_boundary_scene_20261026.jsonl` として戻した（SHA256 `b427d037…926e`、82.5 と同じ）。

**時系列**

| t | 変化 |
|---|---|
| 9.25 | 開戦: 標的 spot E+0x1EED1C、防衛勢力 +0x1EED4C、攻撃勢力 +0x1EED50 が書き換わる。**E+0x1EED43（skip）= 1**、行軍数 = 2 |
| 10.08 / 10.47 | 行軍数 1 → 0（行軍チップ ArmyChip / ArmyChipBuilder の出入り） |
| 10.47〜31 | **場面番号は 1、モードは 1、active は 0 のまま。FadeOutSheet は出ず、Unit は 1体も生成されず、陣営ベクタも空のまま** |
| 30.9 | DialogWnd がタスクに現れる（結果表示と見られる） |

**結論（ACTUAL）**
- 簡易戦闘は、**場面番号・モード・active のどれも変えない**。
- 見分けられる値は E+0x1EED43 = 1（0x4922A0 の skip）と、行軍数が 0 になることだけ。
- 終了を示す状態値は、今回読んだ範囲には現れなかった。
- したがって、**簡易戦闘の開始・終了をプラグインで確実に取るには、0x4922A0（入口）と 0x493630（出口）の呼出し自体に掛けるしかない**。場面番号の監視だけでは取りこぼす（§82.2 の予想を実機で確認）。
- E+0x1EED43 は、前回の画面あり戦闘のあとも 0 のままだった。今回の簡易戦闘のあとも 1 のまま残った。この値は「最後に起動した戦闘の種別」を示すだけで、「戦闘中」を示すものではない。
- 未確認: 簡易戦闘の結果がいつ適用されるか（0x40E2B9 → 0x493630 の時刻）は、状態値からは決められない。


> 原本3594〜3599行は部分回収の対象外（held_native_paragraph）。


| 関数 | 参照の全件（除外範囲の外） | 含意 |
|---|---|---|
| 0x4922A0（戦闘起動） | 0x4921CD（0x491870）、0x522297 / 0x5222AA（0x521D90）。データ参照 0件 | 3件で閉じている |
| 0x493630（終了処理） | 0x49303A / 0x493082 / 0x4930A1（BattleEvent_FrameDriver）、0x40E2B9（BattleWnd::vf01）、0x4A1764（Script_DispatchCommand） | 5件で閉じている |
| 0x492890（battle{} の設置） | 0x433E58（Script_RunPass）のみ | — |
| 0x492710 | 0x4103B1（0x40F320）のみ。0x40F320 は 0x40D0C6（**0x40D0A0 = 戦況ウィンドウを開く処理**）からだけ呼ばれる | **0x492710 は戦況ウィンドウ（画面なし）用の初期化**。0x40F320 が作る仮の陣営2つ（0x8B8E58/5C）を E+0x1EED44/48 に入れ、戻り値×10 をウィンドウのタイマー 0x8B8F18 にする |
| 0x40D0A0 | 0x491FFB / 0x49204F / 0x492143 / 0x4921F7（0x491870）、0x492473（0x4922A0 の skip≠0 側） | — |
| 0x48F9E0（開戦） | 0x475AD0（AI ターン）、0x47D9B6（0x47D770 人材）、0x4CD931（0x4CD7C0：raise_hero の回答）、0x522322（0x521D90 の war の回答）、0x5B1F57（HeroFlagObj::vf01） | — |
| 0x491870（行軍の到着） | 0x5B0B15（ArmyChipBuilder::vf01）のみ | — |
| FadeOutSheet（vtable 0x6388D4）を**場面番号 2 で**作る箇所 | 0x49241C（0x4922A0）、**0x432C14 / 0x432C64（Script_InvokeEventCore）**、**0x49B1DB（0x49AF10）**。番号が変数のものは 0x431F9A（Script_DispatchCommand 0x4A22B1 から）と 0x433AF3 | 下の訂正を参照 |

**§82.3 の訂正（重要）**
1. **「すべての戦闘が 0x4922A0 を通る」は誤り**。
   - 守備兵がいない場合（NO_DEFENDER、0x491FFB）は、0x491870 から直接 0x40D0A0（画面なし）へ進み、0x4922A0 を通らない（§73.3 の記述どおり。fight フックも呼ばれない）。
   - 「この戦闘を見ますか / 操作しますか」の3種類のダイアログでも、**回答の前に**戦況ウィンドウ（0x40D0A0 → 0x492710）が開く。0x4922A0 は回答のあとで呼ばれる。
2. **ダンジョン戦は別の入口と出口を持つ**。
   - 入口は 0x49AF10。呼出元は、0x521D90 の `dungeon` の回答と、0x49B5C0 の「次のフロアへ進みます」。中で 'army' を使い、E+0x1EED18 に局所ポインタを入れ、E+0x1EED44/48 を初期化し（A-20261013-1100-03）、FadeOutSheet(2) を作る。
   - 戦闘中は、E+0x1EED18 ≠ 0 のため FrameDriver が 0x49B280 → **0x49B5C0** に進む（A-20261013-0938-02）。**0x493630 は直接呼ばれない**。
   - したがって「出口は 0x493630 だけ」は、ダンジョン以外の戦闘に限られる。
3. **場面番号 2 は戦闘とは限らない**。
   - Script_InvokeEventCore が FadeOutSheet(2) を作る（§18 の scene path：`map` / `bcg` を持つイベント、540件）。
   - map を表示するイベントも戦闘場面（0x48D6A0）を使う、と読める。場面番号 2 を「戦闘」と名付けると、イベント場面を誤って数える。実機での確認は VERIFY。

**プラグインのフック位置の推奨（STATIC）**

| 目的 | 掛ける場所 |
|---|---|
| 戦闘の開始（全種類） | 0x4922A0（skip の値で画面あり / なしを区別）＋ 0x40D0A0（NO_DEFENDER と、ダイアログ前の戦況ウィンドウ）＋ 0x49AF10（ダンジョン） |
| 戦闘の終了 | 0x493630（ダンジョン以外）＋ 0x49B5C0（ダンジョン） |
| 場面の切替 | GameManager::vf01 の switch。ただし番号 2 は戦闘とイベント場面の両方に使われる |
| 戦闘が動いているか | E+0x1EEC44（active）。画面ありの戦闘と、battle{} を設置したイベントの間だけ 1 になる |

**次の実機観測（最小）**
- (a) map を表示するイベント（会話イベントなど）の前後で `--boundary` を記録する。場面番号 2 になるのに、開戦の値（+0x1EED1C/4C/50、行軍数）が変わらないことを確かめる。
- (b) 守備兵がいない領地への侵攻。
- (c) 撤退や時間切れで終わる戦闘。
- (d) ダンジョンがあるシナリオなら、ダンジョン戦。

<a id="f-83"></a>
## §83 Claude（2026-10-26）: プラグインローダーのレビューとスレッド構成（STATIC、パッチはWine検証のみ）

**対象**: `data/recruit_sort_v4/core/` HK ABI v1 ローダー（Work 所有、未編集）。修正案と取り込み手順は `_work/claude_loader_patches_20261026/README_APPLY.md`。Golden/MATCH 0。

### §83.1 EXE のスレッド（Vahren.exe SHA256 e8dac301…、全 CreateThread / _beginthread の xref）
| スレッド | 生成箇所 | 開始関数 | 内容 |
|---|---|---|---|
| メイン | — | — | WinMain → Graphics_InitDirect3D 0x555500 → 0x555CD0 |
| 起動ローダー | 0x555D98 `CreateThread` | 0x555AD0 | 「スクリプトの読み込み中です」「イメージの読み込み中です」。終了まで、メインは PeekMessage ループ（0x555F31）で GetExitCodeThread==0x103 を待つ。終了後、メインは 0x555E3D で GameManager::vf01 0x4B9930 に入る |
| BGM | 0x502300 `_beginthread`（CRT 0x5B7D14） | 0x5023E0 | 0x502220←0x4BE820←0x4BDE40。DirectSoundBuffer vtbl+0x10/+0x2C/+0x4C とデコーダ vf1 のみ |

- 同期モード: `a_system/xp.txt` があると 0x87981B=1 になり、0x555D7E で 0x555AD0 をメインスレッドで直接呼ぶ。
- **DirectInput8Create の呼び出しは 0x4BCE3B の 1 箇所で、ローダースレッド上**にある: 0x555AD0→0x4B78C0→0x4B9E50→0x4EE0C0→0x4BCDD0。したがって dinput8 プロキシの HK_StartupTry とプラグイン init はローダースレッドで実行される（同期モードを除く）。
- 直接呼び出しグラフ（E8/E9）: ローダーから到達する 710 関数（うち間接呼び出しを含むもの 197）にも、BGM スレッドにも、パッチ対象の関数は含まれない。対象は 0x4D45B0（RVA 0xD462B）、MercenaryWnd::vf16 0x4D79C0（0xD84FA/0xD8611/0xD861D/0xD8BDA/0xD8BE6）、Script_DispatchCommand 0x4A1250 の片 0x4A26FE（0xA5B28/0xA5B54）、0x41E710（0x1E7E3）。間接呼び出しが残るため、到達しないことの証明ではない。
- 結論: 現行の WH_GETMESSAGE によるインストールは、ローダー実行中のメッセージループで発火し得る。対策は「init スレッドのハンドルを保持し、その終了を待ってからインストールする」こと（`hakushin_loader_wait.h`）。

### §83.2 パッチ箇所の照合（STATIC）
- 募集用の 8 箇所はすべて .text 内の E8 で、呼び先は 0x4D4A50。ページ境界をまたぐ箇所はない。
- 0x1E7E3 は `E8 28 01 00 00` で、呼び先は 0x41E910。
- 0x238238 は .rdata の vtable スロット（vtable 0x638234 の +4、値 0x405820）。selector が HKH で予約し、Work の `work_choice_render_pointer.h` が CAS で書き換える。Core の CALL 管理の対象外。

### §83.3 レビューの要点と対応
1. ポインタ書き換えを Core で管理する仕組みがない → PTR_PATCH 拡張（id 4）を新設。
2. 他スレッドが実行中でないことの保証がない → §83.1 と loader_wait。
3. 戻り値 7 の重複 → `HakushinCore_LastCallGateBusy`。
4. 停止フラグが戻らない → ログに plugin id を追加（方針は Work が決める）。
5. DLL ハッシュ未確認 → manifest v2 と、書込共有なしのハンドルを読込まで保持する方式。
6〜9. 文書化案は README_APPLY §2 に記載。

### §83.4 検証（Zig 0.14.1 x86 + Wine 9.0 + Xvfb、実機 Windows ではない）
- 新規テスト: ptr 82/82、ptr 結合 17/17（RED 2/5）、manifest_sha 16/16、hash 結合 9/9、loader_wait 5/5。
- Codex 既存スイートを移植して実行: 元のソース 30/30、パッチ後 30/30。
- 未実行: `../src` を伴う本番ビルド、production host、startup の 12 ケース、proxy。

### §83.5 第2弾（2026-10-27）: 間接呼び出しの解決（STATIC）
- 方法: パッチ対象 5 関数の祖先集合（直接呼び出しを逆にたどる。29 関数）を作り、その中で間接呼び出しの入口になり得るもの（RTTI の vtable に載るか、データ・即値でアドレスを取られているもの）を数える。12 個: HeroMenuWnd / MenuWnd / MercenaryWnd / PersonsInfoWnd / PoliWnd / StatusWnd の vf16、PersonsInfoWnd の vf17、BattleWnd / GameManager / Player / GameEvent(Script_ModeDriver) の vf01、Catch@0x48E965。
- ローダー（直接到達 713 関数）の仮想呼び出しの変位と照合した。
  - +0x40（slot 16）: なし。
  - +0x44（slot 17）: 0x559666 の 1 箇所だけ。D3D デバイスの vtbl+0x44（Present）。
  - +4（slot 1）: 0x42E74E / 0x43A3DD / 0x4709D0 の 3 箇所。いずれも iostream の sentry で、`[[obj]+4]+obj+0x38` の streambuf の vf1 を呼んでいる。
- ローダー内でアドレスを取られている関数 14 個から直接到達できる 146 関数も、祖先と重ならない。CreateWindowEx / SendMessage / DispatchMessage など窓・メッセージ系の API はローダー内にない。BGM スレッドの間接呼び出し 3 箇所は DirectSound とデコーダ。
- 結論: 過大近似のモデルでも到達しない（強い静的根拠）。未解決は、値が関数先頭より前で決まるレジスタ呼び出し約 30 件（主に CRT の DecodePointer と GDI API を保持したレジスタ）。loader_wait は保険として維持する。
- 第2弾の成果物（`_work/claude_loader_patches_20261026/`、27 ファイル）:
  - `build_scripts_ps1.diff`（ps1 13 本）、`docs_md.diff`（md 9 本）、`build_claude_loader_patch_test.ps1`。
  - `src_*.diff`: 0x238238 を Core の PTR_PATCH に移す。ビルドフラグ `WORK_SELECTOR_PTR_MANAGED` で選択し、bridge の HK_OK と衝突しないよう同じレイアウトの型で受ける。
  - `test_render_pointer_managed.c`。
- 第2弾の検証（Wine）: startup 12 ＋ logger ＋ proxy 3 は元・パッチ後とも 16/16、v2 追加 3 ケースも PASS。本番ビルド 4 種と managed 版のビルドは成功。unsupported-host 3 種＋ hover 2 種は 5/5。render_pointer_managed は 10/10。既存 30 スイートは再度 30/30。

### §83.6 第3弾（2026-10-27）: 実ゲームのログによる裏付け（ACTUAL、読み取りのみ）と、間接呼び出しの残りの解決（STATIC）
**ACTUAL**: Work の診断用コピー `_work/startup_clean_20261025/新約迫真戦記―ほのぼの神話ver0.67 豪華版/` のログ（HakushinSelectorPlugin.log、HakushinRecruitPlugin.log、HakushinDatUiProbe.26632.log）を読んだ。
- 記録のあるすべての起動で、`init_tid` と `target_ui_tid` が異なる。例: pid 20976 で init 17548 / UI 26960、pid 24116 で 4276 / 25020、pid 25740 で 25732 / 9500。プラグインの init が UI（メイン）スレッド以外、つまり §83.1 の起動ローダースレッドで走っていることの実測による裏付けである。
- このコピーの `a_system` には `xp.txt` がない（非同期ロード）。
- `installer_begin` は窓探索の 3〜5 回目（約 0.3〜0.5 秒後）に来ている。ログに時刻がないので断定はできないが、ロード中にインストールしている可能性が高い。loader_wait を適用すべき根拠が強まった。
- Work の DatUiProbe は「タイトル画面で手動 arm」という運用でこの問題を避けている（`loading=0 corroboration only; not all-thread proof`）。loader_wait はこれを自動化するもの。
- ログ上、EXE は 0x820000 に配置されていた（DYNAMICBASE、DllCharacteristics 0x8140）。本節の VA は既定ベース 0x400000 の値なので、RVA＝VA−0x400000 として読むこと（例: probe の site 0x853B62 は RVA 0x33B62）。

**STATIC**: §83.5 で未解決だったレジスタ呼び出しを全部たどった。
- 0x423C91 は SelectObject（`mov ebp,[0x609048]`）、0x438391 は FindNextFileA（`[0x609170]`）。
- 0x511A50 / 0x511F00 は std::sort の比較関数。呼び出し元 0x50BF60（ローダー到達）と 0x50D350 は、どちらも `push 0x50BF00` を渡している。0x50BF00 は 0x402C40（葉関数）だけを呼ぶ。
- CRT の分:
  - `___crtMessageBoxW` は GetProcAddress で解決した user32 を呼ぶ。`__getptd_noexit` は Fls 系 API。
  - `__callnewh`: EXE には `_set_new_handler` の呼び出しがないので null。
  - `___libm_error_support`: 既定の 0x5B8FAA だけ（即値の参照は 1 箇所）。
  - `doexit` と `___crtCorExitProcess` はプロセス終了時のみ。
- 結論: ローダースレッドの間接呼び出しはすべて、API、COM（D3D・DirectSound）、iostream の streambuf、CRT 内部、比較関数のいずれかに解決できた。パッチ対象 5 関数の祖先（29 関数・入口 12 個）に到達するものはない。静的解析で言える範囲では「到達しない」が確定した。残る前提は COM / OS からのコールバック（EXE のコードを呼ばない）と、静的には見えないコード生成がないことの 2 点。Work 側でゲーム上の確認（loader_wait 適用後のログで `route_init_thread_exited` が `installer_begin` より前に出ること）を行えば閉じる。

<a id="f-84"></a>
## §84 Claude（2026-10-28）: クラッシュ 0x5DA9F8 と BGM ストリームのスレッド構成（STATIC、ACTUAL 0）
対象は WORK-DAT-GENERIC-UI-SPIKE の未解決クラッシュ（WER: Vahren.exe、c0000005、offset 0x1DA9F8）。VA は既定ベース 0x400000 の値（実行時は ASLR で再配置される）。原因はまだ確定していない。以下は静的根拠と観測手順。

### §84.1 落ちた命令
- 0x5DA930 は libvorbis `decode_packed_entry_number`（codebook.c）と同形。引数 book=[ebp+8]、oggpack_buffer=[ebp+0xC]。
- codebook のオフセット: +8 used_entries、+0x14 codelist、+0x1C dec_codelengths、+0x20 dec_firsttable、+0x24 dec_firsttablen、+0x28 dec_maxlength。
- 0x5DA9F8 `cmp eax,[ebx+ecx*4]` は二分探索の `book->codelist[lo+p]` の読み取り。ebx=codelist、ecx=lo+p、esi=lo、edi=hi。
- lo と hi は used_entries と firsttable から決まる。ビットストリームの中身だけで codelist の範囲外へ出ることはない。したがって AV になるのは、codebook / codelist そのものが壊れているか解放済みか、book ポインタが不正な場合（UAF、二重デコードによる状態破壊、ヒープ破壊のいずれか）。

### §84.2 どのスレッドがデコードするか
- OggDecoder（vtbl 0x6395CC）を生成するのは 0x501E20 だけで、呼び出し元は BGM 再生 0x4BE820 だけ。効果音は Ogg を通らない。
- 0x5DA930 に到達するのは ov_read 相当の 0x5D12E0 だけで、0x5D12E0 を呼ぶのは OggDecoder::vf01（0x501F10）だけ。
- vf01 を呼ぶ場所は 2 つある。
  1. **BGM スレッド** 0x5023E0（`_beginthread`、0x502220 から）。`stop`（+0x4C）が立つまでループし、state（+0x50）==1 のとき GetCurrentPosition → Lock → vf01（0x50249E / 0x50252E）→ Unlock → Sleep(100)。
  2. **main** の 0x502330（vf02 で先頭へ seek → SetCurrentPosition(0) → Lock → vf01（0x5023A0）→ Unlock）。呼び出し元は開始の 0x502220 と、停止の 0x4BF2B0（0x4BF31C）。
- ストリームオブジェクト（0x5C バイト、0x4BE480 で生成し、サウンド管理の +0xA0 に置く）: [0] デコーダ、[1] IDirectSound、[2] バッファ、+0x44 再生中、+0x48 スレッドハンドル、+0x4C 停止フラグ、+0x50 状態（1=再生、3=停止中）。

### §84.3 原作の競合（STATIC、実害は未確認）
- 0x4BF2B0 の停止経路は、`+0x44` が立っていれば次の順で処理する: `state=3` → IDirectSoundBuffer::Stop（vtbl+0x48）→ **0x502330（main が seek と vf01 デコードを実行）** → 0x502160（ここで初めて停止フラグを立て、0x5021E0 で BGM スレッドの終了を待つ）。
- BGM スレッドが state を確認するのはループの先頭だけで、ロックも完了待ちもない。そのため BGM スレッドが vf01 の途中にいると、**同じ OggVorbis_File を 2 スレッドが同時に seek・デコードする**。
- 起きる確率は「デコード時間 ÷ 100 ms」程度で、低くて間欠的。
- 0x4BF2B0 の呼び出し元: 0x4BE1C0（GameManager::vf02 ほか）、0x4BE220（タスクループ 0x4C24B0 から 32 フレームに 1 回。曲の終端でプレイリストの次曲へ切り替える）、0x4BE6B0（終了処理）、0x4BE820（曲の切り替え）。
- 窓が非アクティブの間、main ループは Sleep(10) で止まる（0x4C の PeekMessage ループで、WM_ACTIVATE が 0x879822 を落とす）。BGM スレッドは止まらない。再アクティブ化の直後に 0x4BE220 が曲の終端を処理すると、この競合の窓に入る。フォアグラウンド切り替えでのクラッシュと時期は合うが、因果関係は**未証明**。
- 15964 の DAT（hk_ui_spike_v1）には BGM 命令がない。panel_active の待機中に落ちており、この時点で main がストリームに触れたかどうかは不明。ヒープ破壊（plugin 由来を含む）の仮説もまだ排除できない。

### §84.4 判別するための観測（Work と人に依頼）
- `_work/claude_x32dbg_bgm_race_capture.txt`: 止めずにログだけ取るブレークポイント 11 個（BGM のデコード前後、main の停止・再充填・終了待ち・開始、スレッド開始）。
- 判定: ある tid の BGM_FILL_BEGIN と BGM_FILL_END のあいだに、別 tid の MAIN_REFILL_DECODE が出れば、競合が実際に起きた（クラッシュしなくても判定できる）。
- AV が起きたら: 落ちたスレッドの tid（BGM か main か）、レジスタ、book の各フィールド、`mem.valid` の結果、minidump、main スレッドのコールスタック（+0x102330 / +0xBF2B0 が載っているか）を保存する。
- x32dbg が F9 のたびに止まるのは、plugin DLL の TLS コールバック（スレッドが attach するたびに走る）が原因。Preferences の Events で TLS Callbacks / DLL Entry / Thread Entry のチェックを外す。
- 競合が確定した場合の対策案（実装は Work。原作は書き換えない）: 停止経路で、0x502330 の前に BGM スレッドを止めて待つ（0x5021E0 を先に呼ぶのと同等）よう、0x4BF31C の CALL を Core 管理の CALL パッチで差し替える。ただし手を入れる前に、ACTUAL の確認が必須。

### §84.5 ACTUAL（2026-10-28、PID 9080、x32dbg のログ専用ブレークポイント、人の操作）
- ログ: `_work/claude_x32dbg_bgm_race_log_9080_20261028.txt`（5471 行）。実行時のベースは 0x820000、main の tid は 13424。
- 回数: MAIN_STOP（0x4BF2B0）581 回、main 側のデコード（0x5023A0）598 回、BGM スレッドの起動 299 回。**重なり（BGM_FILL_BEGIN から END までの間に、別スレッドの SEEK / DECODE が入ること）は 0 回**。C0000005 も起きなかった。
- 確認できたこと（ACTUAL）: §84.3 の順序（main が SEEK → DECODE → DONE を行い、そのあとで WAIT_THREAD、そこで BGM スレッドが終了）は実際の動作どおり。BGM スレッドが生きている間に main がデコードする構造は事実。
- 言えないこと: 今回の条件では実際の重なりは観測されなかった。ブレークポイントの通知で各スレッドの実行間隔が変わるため、「起きない」ことの証明にはならない。ただし、0x5DA9F8 のクラッシュの主因としての優先度は下げる。
- 次の候補: plugin のパネル表示中にフォアグラウンドを切り替える元の再現手順で、FILL のログ用ブレークポイントを外し、例外だけを捕捉する設定で再試行する。それでも 0x1DA9F8 で落ちたら、§84.4 の採取（tid、book、コールスタック、minidump）を行う。ヒープ破壊の仮説はまだ有効。

<a id="f-85"></a>
## §85 Claude（2026-10-28）: 原作 choice の引数と、候補数を変えられる汎用 UI の DAT 側の形（STATIC）
対象は WORK-DAT-GENERIC-UI-SPIKE の残課題「choice(v,@labels) が動的に展開されるか」。VA は既定ベースの値。

### §85.1 choice の実体
- GENERAL op15（Script_DispatchCommand 0x4A1250、case 0xF、0x4A1E2x 付近）。arg0 が結果変数名。arg1 以降は、**引数のトークン 1 個がラベル 1 個**。
- 各ラベルは `ScriptArg_AsStringElement`（0x452860）で取り出す。中身は解析時に作られた文字列要素への dynamic_cast だけで、変数の評価も一覧の展開もしない（文字列要素でなければ throw する）。
- ラベルはスタック上の std::string[50]（0x1C×0x32）にコピーされ、上限の検査はない（§12 既出）。**ラベル数は DAT の解析時に固定され、上限は 50（候補 49 ＋ Cancel）**。`@一覧` を渡しても、"@一覧" という 1 個のラベルになるだけで展開はされない。
- 0x41E710 が件数を 0x8BB848、文字列を 0x8BBBA4 以降（0x1C 刻み）に保存する。描画は 0x41E910。

### §85.2 ラベルは描画時に &名前& を展開する
- 0x41E910 のラベル描画ループ（0x41EA00..0x41EA33）は、ラベルの文字列ごとに **0x4303E0 を呼ぶ**（ECX=ラベル、0x41EA11）。0x4303E0 は msg と同じ `&name&` 展開器（`cmp byte [ecx],0x26` が 0x430506 にある）で、結果を 0x455520 で描く。
- したがって、ラベルの**文字列**は `&@変数&` で変数から差し込める。件数だけは固定。
- 注意: 0x4303E0 は名前が見つからないと VarMap_FindOrCreate にたどり着き、変数を作ってしまう。choice の前に、すべてのラベル変数へ値を入れておくこと。

### §85.3 汎用 UI への帰結（提案）
- 「件数ごとに choice を 1 つ」用意する形が、原作だけで成り立つ唯一の書き方。件数 N=1..K（K≤49）の分岐を持つラッパーイベントを DAT に置き、ラベルは `&@hk_ui_labelI&` で差し込む。そうすれば、plugin がない（あるいは失敗した）ときの原作 fallback も正しい表示名で動く。
- 生成器: `_work/claude_gen_choice_wrapper.py`（CP932・CRLF を出力し、K は 1..49）。K=49 の出力例は `_work/claude_choice_wrapper_k49_proposal.dat`（未配置、未実行）。入力は hk_ui_count と @hk_ui_labels、出力は v2 と同じ hk_ui_index と hk_ui_status（1=確定、2=Cancel、3=エラー）。
- plugin 側の注意（`src/work_dat_ui_literal.h`）: 認識に使うのは `routine(<15 文字以下の予約名>)` の 1 引数だけ（`wdul_string` は length>15 を拒否する）。生成器のイベント名 `hk_ui_select_g` は 14 文字。v2 の予約名に加えて認識させる場合は、名前、件数（native の 0x8BB848＝N+1 と、候補一覧の長さ N の一致）、Cancel=N の検証を同じ方針で行う。
- 未確認（ACTUAL が必要）: 字句解析器が choice の引数中の `&` をそのまま文字列要素に残すか（msg では残る）、`index(@一覧,数値変数,@出力)` が 49 件まで正しく動くか、ネストしていない連続 if の中での choice の yield と再開。原作での実測は 0。

<a id="f-86"></a>
## §86 Claude（2026-10-28）: DAT 汎用 UI selector の自動 arm（手動の arm 操作をなくす条件）（STATIC、Wine fixture のみ、ACTUAL 0）
対象は `core/dat_ui_selector_plugin.c`（Work 所有、base mtime 1793032353209、SHA256 6e30fe0d…）。Claude は core を直接編集していない。差分は `_work/claude_loader_patches_20261026/dat_ui_selector_auto_arm.diff`。

### §86.1 自動 arm の静的な根拠（RVA、ベースは実行時に加算）
- **ローダー終了**: base+0x47983C は、起動ローダー（スレッド 0x555AD0。`a_system/xp.txt` があれば main で同期実行）を始める前に 0x555D69 で 1 になり（CS base+0x479628 の中）、ローダーが終わった後（GetExitCodeThread≠STILL_ACTIVE）に 0x555E15 で 0 に戻る。plugin の init はローダー内（DirectInput8Create 0x4BCE3B）で走るので、init 後に 0 を観測すれば、ローダースレッドはもうゲームのコードを実行していない。残るのは main と BGM スレッド 0x5023E0 だけで、BGM スレッドはディスパッチャ 0x4A1250 に到達しない（§83.5／§83.6）。
- **タイトル画面**: base+0x6AD434（GameManager+0x1EF144）は場面番号。0＝タイトル（0x48AD30、'title_name'）、1＝ワールド、2＝戦闘・マップイベント、4＝シナリオ選択、5＝シナリオ開始、6＝ロード、7＝マップテスト。
- **呼ばれる場所**: 判定は WH_GETMESSAGE フック（UI スレッド、タスクループのメッセージ取得）で行う。つまりタスクとタスクの間で、スクリプト VM がこのスレッドでコマンドの途中にいることはない。
- **安定条件**: loading=0 かつ scene=0 が、連続 30 回以上・500 ms 以上続いたら arm して install する。途中で一度でも崩れたらカウントをやり直す。

### §86.2 パッチの中身（`WORK_DAT_UI_AUTO_ARM` を定義したときだけ有効。既定ビルドは不変）
- `probe_scene_title()` と `probe_try_auto_arm()` を追加。PENDING のときだけ動く。arm 済みで state が PENDING に戻っていたら（Core が HKX_BUSY を返した場合）、CAS で INSTALLING にしてから install を再試行する。
- `probe_image()` で SizeOfImage>0x6AD438 も確認する（実際は 0x750000）。
- 手動の arm メッセージ（`probe_process_arm`）は、上書き用としてそのまま残す。
- worker は `manual_arm_wait` の代わりに `auto_arm_wait` を出し、arm 前は 20 ms ごとに WM_NULL を post してフックを回す。PostMessageW が失敗したら `post_failed` で FAILED_RETAINED にする。
- 既定ビルドの同等性は、フラグなしでプリプロセス（`-E -P`）した結果を元のソースと比べて確認した。違いは `probe_process_arm(...)` を `{ }` で囲んだ 1 箇所だけ（コンパイラの出力は同じビルドでも毎回違うので、バイナリ比較は使っていない）。

### §86.3 Wine での検証（Zig 0.14.1、x86-windows-gnu、`-Wall -Wextra -Werror`）
- ビルド: 既定（元のソース・パッチ後）と AUTO（-O0／-O2）、DLL・fixture・native fixture すべて成功。
- `build_dat_ui_selector.ps1` 内の fixture: 3 種とも GUARD PASS。
- `test_dat_ui_selector_native.c`（-O0／-O2）: 元のソース、パッチ後の既定、AUTO の 3 種とも PASS。ただし、これらは自動 arm の経路そのもの（場面番号の読み取り・安定判定）を通らない。
- **既存 fixture の不安定さ（パッチと無関係）**: `bounded_request_failure_diagnostics` が `adapter_failure_diag.<PID>.log` に追記するが、事前に消していない。Wine では PID が再利用されるので、前の実行のログが残って `diagnostic_records()` が多く数え、`FAIL: missing or repeated bounded diagnostic` になる（元のソースで 6/12 失敗）。ログを消してから実行すると 3 種とも 0/12。修正案は `_work/claude_loader_patches_20261026/test_native_stale_log.diff`（DeleteFileW を 1 行。期待値は変えていない）。Windows でも PID の再利用はあるので、同じことが起こりうる。

### §86.4 未確認（ACTUAL が必要）
- 実機で、操作なしにタイトルで `auto_arm_wait` → `auto_arm_accepted` → `patch_active` の順にログが出ること。
- `xp.txt` あり（同期ロード）でも同じ順になること。
- 自動 arm の判定は起動直後の PENDING の間だけ働く。ゲームからタイトルに戻ったときの扱い（古いロード状態の寿命）は §86 の範囲外で、別途レビューが必要。
- 原作での実測は 0。Golden/MATCH は 0 のまま。

<a id="f-87"></a>
## §87 Claude（2026-10-28）: DAT 汎用 UI selector の寿命ゲートの網羅性（タイトル復帰・ロード・場面切り替え）（STATIC、ACTUAL 0）
対象は Work の `core/dat_ui_lifetime.c` と `core/dat_ui_selector_runtime.h`（読むだけで、変更なし）。VA は既定ベースの値。

### §87.1 selector が使う native 状態
- context は G=0x8BE2F0（GameManager。live 記録の 0xCDE2F0−0x820000+0x400000 と一致）。数値変数マップは G+0x4C4、文字列マップは G+0x1E8B40。値の書き先は「ノード+0x28 → レコード → +0x1C」。choice は静的オブジェクト 0x8BB6D8（vtable 0x638234）。
- 確定の直前に `selector_fresh()` が同じ UI スレッド上で snapshot を取り直し、捕捉時と memcmp で比べ、その直後に書く。間に native のコードは走らない。そのため、解放済みメモリへの書き込みは epoch ではなく、この取り直しが防いでいる。epoch が防ぐのは「別の choice のインスタンスなのに中身が同じ」という場合（ABA）。

### §87.2 ゲートの網羅性（直接 call・jmp・ポインタ参照を全走査）
| native 操作 | 入口 | Work のゲート | 判定 |
|---|---|---|---|
| 場面に入るときの初期化 0x4C1FC0（ESI=G+0xC） | 呼び出し元は 7 箇所だけ（0x48AF13 title、0x48B658 scene4、0x48BCB9 scene6、0x48BFEC scene5、0x48C92E scene1、0x48D810 scene2、0x48EABC scene7） | reset gate 7/7 | 網羅。0x4B99FC のジャンプ表では scene3 に処理がない。どの呼び出しも各場面処理のループの外にあり、場面に入るたびに 1 回だけ |
| LoadWnd の読み込み 0x45E5F0 | 0x4D0D8A だけ | load gate | 網羅 |
| choice を開く 0x41E910 | 0x41E7E3 だけ | open gate | 網羅 |
| choice を閉じる ChoiceWnd::vf21 0x41E6D0 | vtable 0x638288 だけ（直接呼び出しはない）。native の確定 0x41EC93 も vtable 経由 | close gate | 網羅 |
| 隠す 0x453AC0 | vtable 0x638244。直接呼び出しは 200 件以上あるが、choice を this にしているのは vf21 内の 0x41E6D8 だけ（0x8BB6D8 を参照する命令をすべて確認） | hide gate（ECX==choice のとき） | 網羅 |
| タイトルへ戻る要求 | GameManager vf03 0x4B9AA0（0x638DFC） | title gate。その後の scene0 の reset とあわせて二重 | 網羅 |
| 変数マップを全部消す 0x45BE10、セーブから読む 0x45E7F0 | どちらも 0x433E80 からだけ呼ばれる。0x433E80 は Script_ModeDriver 0x4335E0（vtable 0x63A6D4）で mode==6 のときだけ jmp される。mode 6 を書くのは scene6 の処理 0x48BCAF だけで、その直後の 0x48BCB9 で reset gate が通る。Script_RunPass 0x4339DE は保存した mode を戻すだけ | reset gate（scene6）が必ず先に通る | 網羅（順序は静的に確認） |
| choice の状態リセット 0x41E510（件数 0x8BB848=0） | Player::vf01 0x51EE83（mode 1＝ワールドの初期化）だけ | **ゲートなし** | scene1 に入るとき（0x48C92E）の後に走るはずだが、順序は未確認。choice は静的オブジェクトで、変数マップには触れないので、メモリの安全性には影響しない |

- 個々の変数の置き換え: VarMap_Set 0x4637A0 は、既存のノードを消して（0x58F7E0）新しいレコードを作る。そのためレコードのアドレスは変わりうる。ただし確定時は名前からノードとレコードをたどり直すので、書き先は常にその時点で生きているレコードになる。同じアドレスが再利用された場合（ABA）も、書き先は正しい。
- 結論: 静的に見える経路では、Work のゲートの集合に抜けは見つからなかった。ゲートがないのは 0x41E510 だけで、これは場面の切り替えの後にしか走らないはず（ACTUAL で確認）。

### §87.3 ACTUAL 確認の手順（準備のみ、未実行）
- `_work/claude_x32dbg_dat_ui_lifetime_order.txt`: ログだけを取るブレークポイントを 14 個置く（open、native の確定、reset 7 つ、LoadWnd、変数の全消去、セーブからの読み込み、0x41E510、タイトル要求）。各行に tid と scene を出す。plugin なしの原作で動かす。
- 判定: 最後の CHOICE_OPEN の後に、RESET・LOADWND_LOAD・TITLE_REQUEST のどれもないまま VARS_CLEAR・VARS_LOAD・CHOICE_STATE_RESET が出たら、ゲートのない寿命の経路があるということ。
- 試す操作: 新規ゲーム→choice→回答、ワールド⇄戦闘、メニューからのセーブとロード、タイトルからのロード、タイトルへの復帰。
- 未確認: 戦闘中など、choice を待っている間に別のスクリプト（同じ VM の別イベント）が変数を書き換えるか。原作での実測は 0。Golden/MATCH は 0 のまま。

<a id="f-88"></a>
## §88 Claude（2026-10-28）: DAT 汎用 UI v3（候補 1〜49 件・数値列 0〜4 列）の部品一式（STATIC＋合成テスト、ACTUAL 0）
置き場所は `_work/claude_loader_patches_20261026/`（README_APPLY.md §6）。DAT 側の仕様は `dat_ui_v3_SPEC.md`。Work のファイルは変更していない（予約名の追加だけを diff で渡す）。

### §88.1 設計
- v1/v2 で実機確認済みの命令（setv、addv、set、add、clear、routine、if、choice）と変数名をそのまま使う。固定 ID・固定ラベル・最大 4 件という制限だけをなくした。
- 件数: 原作の choice は解析時にラベル数が決まり、最大 50 個（§85）。そこで wrapper `hk_ui_select_v3` に、件数 1..49 の choice 分岐を生成器で並べる。ラベルは `&@hk_ui_label<i>&` で、plugin がない場合も同じ名前が出る。
- 列: `@hk_ui_columns`（0〜4）と `@hk_ui_values`（数値変数名を行優先で N×列数）。
- plugin の書き込みは、v1/v2 と同じく `hk_ui_index`＝行と `hk_ui_backend`＝1 だけ。status は wrapper が計算する。
- `wdu3_map`: 1 回の走査で最大 200 個超のキーを集められる std::map の読み取り（キーを並べ替えて二分探索）。v1/v2 の `wdus_map` と同じ構造チェック（ノード数、isnil、循環と共有子の拒否、最後に読み直し）を行う。

### §88.2 検証
- 合成テスト 74/74 PASS（-O0／-O1／-O2／-Os、Wine）。項目は README_APPLY.md §6。
- 作成中に見つけた不具合: 1 要素ベクタを読む一時領域の、NUL より後ろが未初期化で、2 回の読み取りの memcmp が -O2 だけでたまに不一致になった。修正済み。Work の v1/v2 の読み取りは `={{0}}` で初期化しているので、同じ問題はない。

### §88.3 未確認（ACTUAL）
- choice の引数の `&@hk_ui_label<i>&` が、`&` を残したまま保存され、描画時に展開されるか。違っていれば、`wdu3_native_label()` と生成器のラベルの形だけを直す。
- runtime への組み込み（README_APPLY.md §6 の手順 1〜3）は Work が行う。ゲーム上の確認は手順 4。原作での実測は 0。Golden/MATCH は 0 のまま。

<a id="f-89"></a>
## §89 Claude（2026-10-28）: v3 の runtime（本体への組み込み）・結合テスト・独立レビュー（Wine の合成テストのみ、ACTUAL 0）
置き場所と手順は README_APPLY.md §7。Work の `dat_ui_selector_runtime.h` は、diff（6 か所、追加 11 行、うち 2 行は既存行の置き換え）だけで配線する。

### §89.1 状態遷移（`dat_ui_v3_runtime.h`）
- 状態は IDLE → PENDING → ACTIVE → CONSUMED、途中で RETIRED。serial が尽きたら DEAD。surface・serial・pending 以外の状態は v1/v2 と共有しない。
- observe（ネイティブのディスパッチャ内）: すべての入口が古い v1/v2/v3 の要求を置き換える。v3 は `wduc_resolve` → `wdu3_capture` → `wdu3_phase_ready` を通ったら PENDING にする。UI には触れない。
- tick: 最初に、置き換えられた v3 の overlay を片付ける（v1/v2 が owner の状態を読む前）。最後に v3 本体を処理する。開いた choice が baseline のときは待つ。baseline+1 のときは、取り直した snapshot がコピーと一致し、所有 close の確認（前後 2 回）と `wdu3_bind` が通ったら ACTIVE にして表示する。それ以外は RETIRED。ACTIVE の間は、200 ms ごとに同じ確認で早めに回収する。
- 決定: パネルの結果は投函（PostMessage）で後から届く。serial と状態を確認 → surface を閉じる → もう一度確認 → すべてを取り直して確認 → 書き込み計画と書き込み可否 → CONSUMED → index → backend → 寿命ゲート経由で close を 1 回。書き込みに失敗したら使い切りのままにして、close も再試行もしない。
- キャンセル・外からの close・反応しなくなったパネル: overlay だけを閉じて RETIRED にする。原作の choice は待ったまま。

### §89.2 検証
- 結合テスト 55/55（-O0／-O2、自動 arm パッチなし・あり）、部品テスト 85/85（4 段階）。ミューテーション 10 種のうち 7 種を検出し、残る 3 種は二重の確認によって書き込みには至らない。Work の既存スイートは配線後もすべて PASS（`test_dat_ui_lifetime.c` の line50 だけは、Work の元のファイルでも Wine では失敗する環境差）。詳細は README_APPLY.md §7。

### §89.3 独立レビューで直した点（別の AI エージェント、2 回）
1. 見出しで並べ替えると、選択が別の候補に移っていた（並べ替えた後の順で古い選択位置を引いていた）。そのまま Enter で別の候補が決定されうる。→ 並べ替え・絞り込みの前に選んでいる行を記録し、同じ行を選び直す。回帰テストを追加し、古い動きに戻すとテストが落ちることを確認した。
2. ダブルクリック・右クリックの通知の中で grid を破棄していた。→ 結果を記録して投函し、自前のメッセージの中で callback を呼ぶ。投函の前に grid が破棄されたら callback はない。
3. v3 から v1 に切り替わるとき、v1 の overlay の下で owner が有効のまま残りうる。→ tick の最初で古い v3 の overlay を片付ける。
4. v1/v2 の後片付けが、v3 が生きている間も pending フラグを 0 にしていた。→ `!v3_live()` のときだけ 0 にする。
5. bind のアドレス上限が v1 の 5 ラベル分のままだった。→ 50 ラベル分（`UINT32_MAX-0x4bc120`）。
6. テストのコメントと中身の不一致（「callback が親を破棄する」と書いて外から破棄していた）。→ 実際に callback から破棄するテストを追加。
7. 検索欄で Enter／Esc が効かなかった。→ 検索欄にも同じキー処理を入れる。
8. （2 回目）投函に失敗すると、パネルが反応しないまま ACTIVE に残る。→ `wdug_inert()` で tick が回収する。
9. （2 回目）テスト 14b が、serial がたまたま 0 のときだけ意図した経路を通っていた。→ 明示的に揃える。
- ほかに、コピーを構造体代入から memcpy にした（パディングも含めて memcmp で比べるため）。
- 2 回目のレビューの結論: 再検証せずに書き込む経路、二重の書き込み・close、古い serial で動く経路は見つからない。新しい確定的な不具合もない。

### §89.4 未確認（ACTUAL）
- §88.3 と同じ（`&@hk_ui_labelN&` の展開）。ほかに、ゲーム内での投函→tick→決定の順序、フルスクリーン、IME 入力中の検索欄。原作での実測は 0。Golden/MATCH は 0 のまま。

<a id="f-90"></a>
## §90 Claude（2026-10-28）: v3 の実機確認・自動 arm の不具合と修正・Codex 統合版への反映

### §90.1 実機確認（ACTUAL、Work の診断用コピー、PID 10356）
- 字句解析は `choice` の引数の `&` を残し、ゲーム本来の選択肢は `&@hk_ui_label0&` を文字列変数の値に展開する（「ただ一人」と表示）。
- Case1: 一覧で並べ替えてから選択 → Index=2 Result=tnok Status=1 Backend=1。
- Case2: 一覧で Cancel → ゲームの選択肢で選択 → Index=0 Result=only Backend=0（DLL は何も書かない）。
- Case3: 49 件×4 列、検索と並べ替えのあと選択 → Index=43 Result=c43 Backend=1。

### §90.2 自動 arm の不具合と修正
- ACTUAL（PID 20812/10356）: 読み込みフラグ（0x87983C）と scene がどちらも 0 の「読み込み前」の時点で arm した（§86 の静的な想定は誤り）。
- 修正: フラグが 1 になったのを一度見て、0 に戻ってから arm する（`probe_auto_seen_loading`）。test_dat_ui_auto_arm_edge.c で確認。
- Codex の指摘 2 件（一覧の再構築失敗時の対応付け、先に表示した要求が後の要求を取り消す問題）は、Codex の修正を残して統合した。一覧の再構築に失敗したときは「破損」状態にして、キャンセルだけを受け付ける。

<a id="f-91"></a>
## §91 Claude（2026-10-28）: DAT 汎用ユニット一覧 v4（実機確認済み）

### §91.1 構成
- 予約名 `hk_ui_select_v4`。DAT はユニット ID のリスト（`@hk_ui_candidates`）と列指定（`@hk_ui_columns` = `見出し=能力名`、最大 8 列）を渡す。題名（`@hk_ui_title`）と最初の並び（`@hk_ui_sort`）は任意。
- 能力値は DLL がユニット定義表から直接読む。定義表の場所: map は ctx=G+0x1B8 の +0x2FC、先頭ノードは +0x300、件数は +0x304。値は def+0x168。def+0x1A4 が ctx と一致するものだけを使う。
- 名前はゲーム本来の 0x5846A0 を呼んで得る（fastcall: ECX=def、EDX=出力 std::string）。heap のバッファは 0x5B6BBB で解放する。関数の先頭バイトが想定と違えば呼ばずに ID を表示する。
- ゲーム側の選択肢は 2 つだけ: `choice(hk_ui_anchor,一覧から選ぶ,Cancel)`。そのため 50 件の上限がない（DLL は 512 件まで）。DLL がないときは「一覧から選ぶ」で 8 人ずつのページ選択になる。
- 書き込む順番は index → anchor → backend。backend=1 を最後にするのは、これを DAT が「確定」の印として使うため。
- ファイル: src/work_dat_ui_v4.h、core/dat_ui_v3_runtime.h（v4 の部分）、src/work_dat_ui_grid.h（並べ替えの指定、512 行・8 列、3 回目のクリックで元の順）。DAT 生成: _work/claude_loader_patches_20261026/v4/claude_gen_unit_table_v4.py。

### §91.2 検証
- Wine の合成テスト: v4 結合 43/43（-O0、-O2、AUTO）、v3 部品 87/87、パネル破損 73/73、v3 結合 55/55、次の要求 12/12、native、自動 arm の境界 10/10。
- 独立レビュー（別の AI エージェント）で、名前関数の呼び出し規約と文字列の扱いを Vahren.exe の逆アセンブルと照合した。指摘のうち 5 件を直した:
  - 書き込みの順番
  - 開いている間の確認を軽くした（毎回の全件読み直しをやめた）
  - 定義表と結び付いていないユニットは受け付けない
  - DAT 側の入力が次の呼び出しに残らないようにした
  - 同じ名前が並ぶときは ID を付ける

### §91.3 実機確認（ACTUAL、PID 3596 / 26868 / V4d）
- DLL なし: 17 人をページ選択で選べた（Index=2）。234 人は 30 ページ（Index=0）。0 人なら Status=3 で選択肢を出さない。水練の講師を「ひで」に選べた。
- DLL あり:
  - 17 人の一覧（名前・Lv・HP・攻撃・魔防、Lv 降順）が出た。
  - 234 人から選ぶと Index=2 Backend=1 Anchor=0 で、ゲームの選択肢が閉じてイベントが続いた。
  - 水練講師の一覧（講師補正・HP・Lv）から選べた。
  - 横に出す版で、HP 見出しで並べ替えてからダブルクリックすると Index=12、Backend=1（DAT の順と一致）。
- 一般兵の ID（例: `a030+0`）も定義表のキーで、名前と能力値が読めた。
- `pushv(@list,n)` で人数が入る。`index()` で範囲外を指定すると最後の要素が入る（空き枠は「－」で埋める）。前の `choiceTitle` は残るので、ゲームの選択肢の前に題名を出し直す。
- 自動 arm: 監視フックが読み込み後に付く場合があり（PID 3596/19552）、その場合はフラグ 1 を一度も見ない。読み込みを一度も見ていないときは「フラグ 0 かつタイトル画面」が 10 秒続いたら arm する（PID 26868 で `auto_arm_late_title` → `patch_active`）。
- 入力の重なり: ゲームは DirectInput でマウスを読むため、ゲーム窓を無効化しても、一覧の上のクリックが下のゲームの選択肢に届いた（lifetime_epoch で取り消し → ページ選択。誤った書き込みはなし）。そのため、画面に余裕があれば一覧をゲーム窓の横に出すようにした（V4d で確認）。

### §91.4 未確認
- ゲームの選択肢を右クリックしたときの戻り値。
- 全画面のとき（一覧が中央に重なる）のマウス操作。キーボード操作を推奨。
- 顔・チップ画像の表示（未実装）。

<a id="f-92"></a>
## §92 Claude（2026-10-28）: キャラチップ・ゲーム本来のステータスパネル・教育のキャラ選択（v4 の拡張、実機確認済み）

### §92.1 キャラチップ
- チップ名は、ゲーム本来の決定処理 0x584970 で決める。
  - 呼び方は thiscall（ECX=def、スタックに std::string* out と flag、`ret 8`）。ゲーム側の呼び出し元はどれも flag=1。
  - image / sub_image（レベル別）/ tkool を見て、ゲームが描くのと同じ名前を返す。
  - ファイルは読まない（独立レビューで逆アセンブルを確認）。0x423e80 は検索だけで、挿入はしない。
- 画像は `a_default\chip` → `chip2` の `<名前>[.png]` を WIC で読み、32×32 に収める。
  - Work の work_selector_icons.h（ImageList）を使う。
  - 名前は UTF-16 で検査し、区切り・`:`・`..`・デバイス名を拒否する。CP932 の 2 バイト目の 0x5C は許可する。
- ACTUAL: 自勢力 17 人・234 人・水練の講師の一覧で、チップが表示された。

### §92.2 ゲーム本来のステータスパネル
- Work の work_selector_native_detail.h（開く 0x55BAB0、閉じる 0x55B590）をそのまま使う。
- 行が選ばれたら、投函したメッセージの中でパネルを開く。
- 閉じるのは次の場面。
  - 決定（結果を書き込む前。閉じられなければ書き込まない）
  - キャンセル
  - 次の要求が来たとき（その場で閉じる）
  - 一覧を閉じたとき
- 閉じるのに失敗したら、毎回の tick で閉じ直す。
- ACTUAL:
  - ANNYUI姉貴 ⇔ ひで の切り替え、決定時に閉じることを確認した。
  - 一般兵（a030+0 など）も、ユーザーが手で操作して問題なし。
  - 自動操作の試験中に一覧が反応しなかったのは、操作用アプリの画面が一覧の上に重なっていたため。ゲーム側の不具合ではなかった。

### §92.3 教育のキャラ選択
- claude_lecture_v4.dat の `choiceUnitFromList_v4` が、lecture.dat の 8 人ずつのページ選択の代わりになる。
  - 入出力は元と同じ（@chara_list → @eranda_chara、取りやめなら yappa_yameru=1。入口で 0 に戻す）。
  - 列は 補正(magdef)・Lv・HP・攻撃・防御・魔力・技術・速さ。
- lecture.dat はコピーを書き換えて使う（claude_patch_lecture_v4.py）。元のイベントは choiceUnitFromList_orig として残す。
- ACTUAL: 診断用コピーで講師・生徒の選択から教育の実行まで、ユーザーが操作して問題の報告なし。

### §92.4 その他
- 一覧の題名の高さを、固定 20 ピクセルから実際のフォントの高さに変えた（高 DPI で文字がはみ出していた。ユーザーの指摘）。
- 独立レビュー（2 回目）の指摘 8 件のうち 7 件を直した。
  - 閉じ失敗の再試行
  - 次の要求で即座に閉じる
  - パネルを開く前の世代確認
  - yappa_yameru の初期化
  - 名前の検査
  - 終了中は閉じる処理を呼ばない
  - テストが自分で画像を用意する
- 残りの 1 件は、ゲームが選択肢に自分で答えたときにパネルが最大 1 tick 残ること。C 側で捕まえる場所がないので記録だけにした。
- 検証:
  - v4 結合テスト 68/68（-O0、-O2、AUTO）
  - v3 部品テスト 87/87、パネル破損テスト 73/73、v3 結合テスト 55/55、次の要求のテスト 12/12、native テスト、自動 arm の境界テスト 10/10
- 最終ビルドの SHA は b56aae9a…。題名とレビューの修正は合成テストのみで、ゲーム上ではまだ確認していない（ユーザーに依頼中）。

<a id="f-93"></a>
## §93 Claude（2026-10-29）: 詳細パネル（StatusWnd）の雇用・解雇ボタンが出る条件（ユーザーの x32dbg で実機確認）

- 調べ方: ユーザーが x32dbg で診断用コピーを起動し、ブレークポイントで通過した場所と値を記録した。
  - その回の起動では、Vahren.exe の先頭アドレスは 0x00A30000 だった（起動ごとに変わる）。
  - アドレスは本書のほかの節と同じく、元の VA（0x400000 基準）で書く。
- 静的解析（Claude）と実機（ユーザー）で、確認の種類を分けて書く。

### §93.1 ボタンを作る処理の場所
- ACTUAL: パネルを組み立てる処理 0x55BC60 の引数（[esp+4]）は、自勢力のユニットでも 0 だった。ボタンの有無は、呼び出し側の引数では決まらない。
- ACTUAL: ボタンは 0x55D7FF から始まる処理で作られる。
  - 0x55D712 から始まる 1 組目の処理（雇用 0x6292C4 / 0x6292BC、解雇 0x6292CC）は、自勢力でも他勢力でも通らなかった。
- ACTUAL: 詳細を 1 回開くあいだに、入口 0x55D8F6 を 10 回前後通った。パネルは表示中に繰り返し組み立て直される。

### §93.2 3 つの判定（入口 0x55D8F6 の後）
3 つとも満たしたときだけボタンを作る。

1. eax=ユニットで 0x583CF0 を呼ぶ。戻り値が 0 なら 0x55D9FC（ボタン処理の終わり）へ飛ぶ。
   - STATIC: 0x583CF0 は、ユニットの +0x84 の文字列と +0x1A4（ctx）を 0x467E90 に渡して、何かを引く。
   - ACTUAL: 同じ勢力でもユニットごとに戻り値が違った。
     - 自勢力: 41397640 / 413979A0 / 41395DC8
     - 他勢力: 41398120 / 41395EA0
   - 推定: 勢力ではなく、ユニットの所属先（領地など）。名前の確認はしていない。
2. 1 の戻り値で 0x597B00 を呼び、その戻り値の byte +0x1D が 0 なら飛ぶ。
   - ACTUAL: 戻り値は勢力ごとに一定で、+0x1D は次のとおりだった。

     | 勢力 | 0x597B00 の戻り値 | +0x1D |
     |---|---|---|
     | 自勢力 | 15086448 | 1 |
     | 他勢力 | 15085DE0 | 0 |
     | 他勢力 | 15086D40 | 0 |
     | 同盟勢力 | 15086070 | 0 |

   - ACTUAL: 他勢力では、0x55D905 を通った直後に 0x55D9FC へ飛んだ。
   - 結論: +0x1D は「プレイヤーの勢力」を示すフラグ。ボタンは「ユニットの所属先の勢力がプレイヤーか」で決まる。同盟勢力にも出ない。
3. [0x8BA5DC]==0x80000008 かつ byte[0x8BA5BC]!=0 なら飛ぶ。
   - STATIC: 0x8BA538 は起動時に 0x5A4100 で作られる画面の部品で、名前 'war' を持つ（+0xBC = 0x8BA5F4）。
     - +0x84（=0x8BA5BC）が表示中の印、+0xA4（=0x8BA5DC）が状態。
     - 同じ形の判定がゲーム内に約 30 か所ある（0x418E88、0x41B512、0x52377D、0x52D649、ボタン押下の処理（StatusWnd::vf15 = 0x560650）の中の 0x5606A2 など。2026-10-29 訂正: 以前「ホバー処理」と書いたのは誤り）。
     - 0x8BA5BC に直接書く命令は、初期化の 0x5A41B5 だけ。表示と非表示は、画面の部品のメソッドがポインタ経由で書いていると推定。
   - ACTUAL: [0x8BA5DC] は通常時からずっと 0x80000008 だった（特別な表示モードではない）。
   - ACTUAL: 0x8BA5BC を書込監視したところ、戦闘時の「出撃するユニットを選んでください」の画面を出すとき（と閉じるとき）に書き込まれた。
   - ACTUAL: その画面の間に自勢力ユニットの詳細を開くと、0x8BA5BC=1 で、雇用・解雇ボタンは出なかった（ユーザーが目で確認）。
   - 結論: 出撃するユニットを選んでいる間は、ボタンを出さない。

### §93.3 作られるボタン（STATIC）
- 表の「ユニット」は、パネルの +0x1B8 から取ったもの（0x55D7FF）。
| ボタン | 命令の位置 | 文字 | 作ったときに立つ印 | 条件 |
|---|---|---|---|---|
| 雇用 | 0x55D93A | 0x629318 | +0x1C4 | ユニットの +0x7A==0 かつ [esp+0x1A]!=0 |
| 召上げ | 0x55D95F | 0x629320 | +0x1C5 | ユニットの +0x7A!=0 |
| 解雇 | 0x55D99C | 0x629328 | +0x1C6 | [esp+0x19]!=0 かつ ユニットの +0x74==0 かつ [esp+0x18]!=0 |
| アイテム | 0x55D9DD | 0x629330 | +0x1C7 | [esp+0x1B]!=0 かつ [0x68B590]-[0x68B588] が 0 でない かつ [esp+0x18]!=0 |

- 各ボタンは 0x436870 で文字を用意し、0x455520 で作る。
- [esp+0x18]〜[esp+0x1B] は 0x55D80B〜0x55D8F1 で決まる。
  - 0x585AD0 にキー（0x6292E4、0x6292F8、0x629308）を渡して調べた結果を、0x42F860 で判定している。
  - キーは `noremove_unit`（0x6292E4）、`noitem_unit`（0x6292F8）、`noemploy_unit`（0x629308）。値を "on"（0x6292E0 ほか）と比べている。
    - それぞれ [esp+0x19]（解雇）、[esp+0x1B]（アイテム）、[esp+0x1A]（雇用）に入る。
    - 0x585AD0 は、ユニットの文字列（+0x1C）と ctx+0x34 から引く。スクリプトのユニット・クラス設定の値と推定。
    - 比較の向きは未確認。「on なら、そのボタンを出さない」と推定（名前から）。
- ACTUAL: 自勢力のユニットでは、雇用と解雇の 2 つだけが作られた（0x55D93A → 0x55D99C → 0x55D9BB → 0x55D9FC）。
- ACTUAL（ユーザーの観察とスクリーンショット、2026-10-29）: 「召上げ」は**陪臣**の詳細に出る。
  - 陪臣は、特定の人材の部下から動かせない。
  - 召上げを押すと軍資金を払って普通の人材になり、ほかの人材の部下にも配置できるようになる（ユーザーの説明）。
  - 画面の例: ポッチャマ（陪臣、忠誠 100）の詳細では、ボタンは召上げだけで、解雇はなかった。
  - ユニットの +0x7A を「陪臣」の印と判断してよい（召上げの条件 +0x7A!=0 と一致）。
- STATIC: [esp+0x18] は、+0x7A==0 なら 1。陪臣（+0x7A!=0）のときは、0x583DC0 の戻り値の +0x74 が 0 でなければ 1、0 なら 0。
  - 0x583DC0 はユニット定義の一覧（ctx+0x300）をたどる。陪臣の主の人材を探していると推定（未確認）。
  - 陪臣に解雇が出ないのは、この印（+0x74）によると推定（未確認）。
- ACTUAL（ユーザーのスクリーンショット、2026-10-29）: [マスター] の人材（田所）の詳細では、ボタンは雇用だけで、解雇はなかった。
  - 解雇の条件のうち、マスターで成り立たないのは「ユニットの +0x74==0」か「noremove_unit」のどちらか。
  - ACTUAL（x32dbg、0x55D98F で記録、2026-10-29）: [esp+0x19]・+0x74・+0x7A は次のとおりだった。

    | ユニット | 解雇可否 [esp+0x19] | +0x74 | +0x7A |
    |---|---|---|---|
    | マスター | 1 | 1 | 0 |
    | 人材 | 1 | 0 | 0 |
    | 一般ユニット | 1 | 0 | 0 |
    | 陪臣 | 1 | 0 | 1 |

  - 結論: ユニットの +0x74 は「マスター」の印。マスターに解雇が出ないのは +0x74 による。
  - 4 種類とも [esp+0x19]=1 だった（noremove_unit は付いていなかった）。
- 未確認: アイテムのボタンが出る条件。

### §93.4 イベント中のステータスパネル（ユーザーの観察、2026-10-29）
- 元のゲームでは、イベント中にステータスパネルの説明表示（マウスを重ねるとスキルの説明が出る）は出ない。
- 教育などのイベントの途中では、ステータスパネル自体を見ることができない（ユーザーいわく、不便）。
- そのため、DLL の一覧からパネルを開き、そこで説明表示を出すことは、元のゲームにない**機能追加**になる。
  - 再現すべき「元の動き」は存在しない。
  - 有効・無効を選べるようにし、ゲームの規則（イベントの進行など）には触れないこと。

### §93.5 DLL（v4 のステータスパネル）への影響
- 他勢力のユニットは、今の DLL のままでボタンなしになる（正しい）。
- 自勢力のユニットは、一覧で選んでいる間も雇用・解雇ボタンが出る。
- 自勢力をボタンなしで出すには、組み立て直されるたびに、作られたボタンを DLL 側で隠すか無効にする必要がある（+0x1C4〜+0x1C7 が目印）。
- 使わない方法:
  - 0x8BA5BC を立てる（約 30 か所の動きが変わる）
  - 勢力の +0x1D を書き換える（ゲームの状態を変える）
- 未調査: ボタンの持ち方と、隠す・無効にする関数。静的解析で確かめてから実装すること。

<a id="f-94"></a>
## §94 Claude（2026-10-29）: 研究知識ベース（knowledge）への移行

- 「今わかっていること」を、作業日誌とは別に `_REDEV_RESEARCH\knowledge\` にまとめた。入口は `_REDEV_RESEARCH\00_START_HERE.md`。
  - アドレス事典（手書き 118 件＋自動 656 件）、構造体事典（40 項目）、DAT の挙動、UI の仕組み。
  - 検索 `knowledge\kb.py`（統合 V9 の疑似コードに名前を重ねて表示）、Ghidra への反映 `ApplyKnowledge.java`（Ghidra 11.4.2 の headless で試験済み）、x32dbg の名前付けスクリプト。
- 今後、この findings に新しい節を書くときは、knowledge の該当行も書き直す（手順は knowledge\README.md）。
- 訂正（§93.2）: 0x5606A2 は説明表示（ホバー）の処理ではなく、ボタン押下の処理 StatusWnd::vf15（0x560650）の中。
- 訂正（本セッションの過去の説明）: 0x521A00 は Player の主の仮想関数表ではなく、+144 にある Actionable 側の表の 1 番（Player::b144_vf01）。2026-10-11 の名前 Player::vf01 は主表と副表を区別していなかった。
- 静的に新しく確認したこと: グローバルのウィンドウ実体 55 個（vtable の書込み位置から）。0x8BA538 は WarWnd、0x8BCD48 は StatusWnd→TempStatusWnd、0x8BB6D8 は ChoiceWnd、0x8BE2F0 は GameManager。

<a id="f-95"></a>
## §95 Claude（2026-10-29）: 詳細パネルのボタンの仕組みと、v4 でボタンなしにする設計（STATIC）

- ボタンは組み立て時にパネルの画像へ描くだけ（0x455520、EAX=ウィンドウ、ESI=矩形、ret 8。呼び出し 6 か所: 0x55D77F / 0x55D7C6 / 0x55D951 / 0x55D976 / 0x55D9AF / 0x55D9F0）。描いたら印 +0x1C4〜+0x1C7 を立てる。
- 矩形は全パネル共通: 0x68B578（雇用/召上げ）、0x68B568（解雇）、0x68B588（アイテム）、ポインタ表 0x65BEA8。
- 押下 0x560650（仮想関数 15）は、+0x1BC が「なし」（0x80000008）で、印が立っているボタンにだけ +0x1BC を設定する。印が全部 0 なら何もしない。
- 離す 0x560CA0（16）は、+0x1BC が「なし」なら何もしない。番号があれば印を確認し直さずに動作する。
- TempStatusWnd の表 0x639CD4 の +0x3C / +0x40 は押下 / 離す、+0x44（説明表示）は空の関数 0x406E20。StatusWnd の表 0x639C5C とは別なので、TempStatusWnd だけを変えられる。
- 設計（ボタンなし）: 6 か所の CALL を「TempStatusWnd かつ DLL 使用中なら描かない」関数へ向け直し、TempStatusWnd の表の押下・離すを「使用中なら印を 0、+0x1BC をなしにしてから元を呼ぶ」関数に差し替える。詳細と試験項目は dev_lab\docs\DAT_UI_V4_STATUS_PANEL.md。実装・実機確認はまだ。

<a id="f-96"></a>
## §96 Claude（2026-11-03）: 召喚の親子関係と経験値の流れ（任意ユニットへの経験値付与・親への分配スキルの下準備）

- 確かさ: すべて STATIC（原本 x86 を capstone で直接読んだもの）と既存研究の再確認。実機は未確認（§96.5 の記録用スクリプトを用意）。
- 対象: Vahren.exe SHA256 E8DAC301…767187。ImageBase 0x400000、DYNAMIC_BASE あり（実行時は先頭アドレス＋RVA）。
- 道具と擬似 C: `dev_lab/_work/summon_exp_20261103/`（vdis.py＝逆アセンブル、dispscan.py＝あるオフセットを使う命令の全探索、vtab.py、rawbytes.py）。
- 「BattleUnit」は戦闘中のユニット（通常型 vtable 0x63A9E4、簡易戦闘型 0x63A4BC）。「UnitData」は knowledge の UnitDef（+0x168 level、+0x16C 経験値、+0x170 次の閾値）。


> 原本4091〜4106行は部分回収の対象外（held_native_paragraph）。


### §96.2 経験値の流れ（既報の確認と整理）
- 加算の本体: 0x551E50（EAX=context、stdcall 12）の **0x551FB2 `add [edi+0x16C], edx`**（6 バイト `01 97 6C 01 00 00`）。
  - EDI＝加算先 UnitData（＝actor+0x1C8）、EDX＝加算量、ESI＝context（[esi]＝actor の BattleUnit）。
- 0x551E50 が加算しない条件（先頭）: 技能の exp_per=off（Skill+0x2A8 が −123456.0）、actor+0x1D0（部隊）＝0、actor+0x18614≠0、context+0xC≠0（同じ攻撃で加算済み）。
- 召喚された子:
  - 子の攻撃の経験値は子の +0x1C8＝R（親の BattleUnit の木にある一時的な記録）に入る。親の UnitData には入らない。
  - 子に部隊がないと加算されない。部隊が付くのは yorozu に troop/troop2/troop3 がある召喚だけ。簡易戦闘の召喚は常に部隊なし（既報 `exp_research_20261021/EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md` CP01/CP02）。
  - R は戦闘の後片付けで親の BattleUnit と一緒に捨てられる。戦闘終了時に親へ移す処理は見つかっていない（既報。未確定のまま）。
- 召喚した親自身: 召喚の発動で親の UnitData に加算される（0x57F190 の 0x551E50 呼び出し。簡易戦闘は 0x547A8C）。
- レベルアップ:
  - 0x58A650（ECX=UnitData、スタック引数なし）。経験値≧閾値（+0x170）のあいだ、level_max までレベルを上げ続ける。
  - 簡易戦闘のユニット（actor+0x8C≠0）は、加算の直後に判定する（0x551FBA → 0x551FD3）。
  - 通常戦闘のユニット（+0x8C=0）は、戦闘終了時に 0x575110 でまとめて判定する。条件は +0x1D0≠0、+0x18614=0、経験値≧閾値。呼び出し元（0x514C50、0x5200A0）は陣営 +0x48 の一覧を全部回り、+0x1867C（倒れた印）は見ない。倒れたユニットや召喚獣がこの一覧に残っているかは未確認。
  - 戦略画面の訓練（0x4723D0〜0x4723DE）: 経験値に閾値をそのまま書いてから 0x58A650 を呼ぶ。

### §96.3 「任意のユニットに任意の経験値を渡す」関数の契約（設計。実装はまだ）
- 戦闘中（BattleUnit が分かるとき）:
  1. ud = unit+0x1C8。0 なら何もしない。
  2. ud+0x16C += n。原作の 0x551FB2 には桁あふれの処理がない。DLL では 0xFFFFFFFF で止めることを推奨。
  3. unit+0x8C≠0（簡易戦闘）なら、ud+0x16C ≧ ud+0x170 のとき 0x58A650(ECX=ud) を呼ぶ。
  4. 通常戦闘（+0x8C=0）なら何もしない。戦闘終了時に 0x575110 が判定する（原作と同じ時点）。
  - 原作の加算と同じ扱いにするなら、+0x1D0=0 や +0x18614≠0 のユニットには渡さない（戦闘終了時の判定もされないため）。
  - 0x551E50 そのものは呼ばない。context、技能の倍率、最低 10、重複防止が絡むため。
- 戦略画面（UnitData だけのとき）: ud+0x16C += n。閾値以上なら 0x58A650(ECX=ud)。訓練と同じ呼び方。
  - 未確認: 戦略画面での表示の更新や、ステータスの再計算が別に要るか。

### §96.4 「子が得た経験値の一部を親に渡す」スキルの設計メモ
- フック位置は 0x551FB2（加算の直前）。actor（[esi]）を子→親の表で引き、親が見つかれば floor(EDX×割合) を §96.3 の方法で親に渡す。元の加算はそのまま実行する。
  - 「子の分を減らして親に移す」か「子にもそのまま入れて、親にも足す」かは仕様として決める。
- 注意点:
  1. 部隊のない子は 0x551E50 の先頭で返るので、0x551FB2 まで来ない。部隊のない召喚獣でも親に渡したいなら、0x551E50 の入口で加算量を別に計算する必要がある（原作の式を再現し、+0x1D0 の条件だけを外す）。
  2. 親が倒れている（+0x1867C≠0）ときに渡すか。倒れた親が戦闘終了のレベル判定を受けるかは未確認（§96.2）。受けない場合、経験値は次にレベル判定されるまで持ち越される。
  3. 孫（召喚獣が召喚した召喚獣）の場合、親の +0x1C8 も R なので、そのまま渡すと親の R に入る。人材まで届けたいなら表を上へたどる。
  4. 子→親の表は戦闘ごとに空にする。戦闘中の BattleUnit は解放されず、倒れても印が立つだけと読める（解放は戦闘の後片付けの vtable[0]＝0x570C90）。→ 要実機確認。
  5. スキルを持っているかの判定（DAT の独自キーなど）は別途設計する。

### §96.5 実機での確認（x32dbg、記録だけ）
- スクリプト: `dev_lab/_work/summon_exp_20261103/x32dbg_summon_exp_trace_20261103.txt`
- 記録点（すべて bpcond 0 の止まらないブレークポイント、メモリは書き換えない）:
  - LINK＝0x5774A0、EXPTRY＝0x551E72、EXPADD＝0x551FB2、GONE＝0x575A60、SETTLE＝0x575110
- 確かめること:
  1. 召喚のたびに LINK が 1 回出て、parent が召喚したユニットであること。
  2. 部隊のない召喚獣の攻撃では EXPTRY troop=0 のあとに EXPADD が出ないこと。yorozu=troop の召喚獣では、EXPADD の ud が子の R であること。
  3. 子が消えても、親の children の数が減らないこと。
  4. 戦闘終了時の SETTLE に、召喚獣と、戦闘中に倒れたユニットが含まれるかどうか。

### §96.6 実機の記録（2026-11-03 09:31、ユーザーのプレイ、x32dbg の記録だけ）
- ログ: `dev_lab/_work/summon_exp_20261103/trace_20261103_0931.log`（SHA256 450024098776B52EB994D015153DCDFF367105680F9E553D61D9AB90AB2AF944）。この回の Vahren.exe の先頭は 0x00DA0000。
- 場面: 召喚者 1 体（parent=45B00028、lv1、部隊あり）が同じ召喚を 12 回使った通常戦闘（+0x8C=0）。
- ACTUAL:
  1. LINK は召喚 1 回につき 1 回。parent は毎回同じ召喚者で、n_before は 0→11 と 1 ずつ増えた。この回は子が 1 体も消えていないので、「消えても一覧が減らない」ことは未確認のまま。
  2. 12 体の子はすべて child_troop=0（部隊なし）、follow（+0x1E594）=0。追従先の欄は親を指していない（satellite なし）。
  3. **12 体の子が同じ記録 R（child_ud=207FBC78）を使っていた。** 同じ親・同じ召喚先なら R を使い回す（既報 CP10/CP11 の静的解析）を実機で確認。
  4. 子の攻撃による EXPTRY は 1,459 回、すべて troop=0。EXPADD は 0 回。**部隊のない召喚獣は経験値を 1 も得ない**（§96.2 を実機で確認）。
  5. EXPADD は 12 回だけで、すべて召喚者自身（召喚の発動 1 回ごとに +10。最低値 10）。召喚者の経験値は 0→120。
  6. 戦闘終了時の SETTLE は、召喚者・子 12 体・GONE が出た 11 体すべてに来た。**召喚獣も陣営の一覧に残り、終了時のレベル判定 0x575110 の対象になる。**【2026-11-03 訂正: この 11 体（lv10）の GONE は 3 回の記録すべてで戦闘の最初、攻撃より前に出ており、戦闘中に倒れたのではない（出撃しないユニットの片付けなどと推定、未確認）。倒れたユニットが SETTLE に来ることは、§96.7 の敵（lv5、攻撃後に GONE）と §96.8 の JOKER で確認した。】子は troop=0 なので 0x575110 の条件で何もしない。§96.2・§96.4 の「未確認」はこれで解消。
  7. 召喚者の UnitData は lv1 で次の閾値（+0x170）が 0 だった。別のユニット（lv99）は閾値 0xFFFFFFFF（既報 CP18 の上限固定）。閾値 0 の意味は未確認。
- 付記: 記録の前に、BGM 再生スレッド（0x5023E0）だけが Suspended のまま残り、メインスレッドが 0x5021E0 で終了待ちを続けてゲームが固まった。x32dbg の `resumethread 27A8`（TID 10152）で復旧。誰が止めたかは不明。x32dbg のコマンドは数を 16 進で読むので、TID は 16 進で渡すこと（10 進の 10152 を渡すと「無効なスレッド 65874」になる）。
- 設計への影響: この召喚では「子が得た経験値」が常に 0 なので、親へ分けるスキルは 0x551FB2 では何も起きない。部隊のない召喚獣にも効かせるなら、0x551E50 の入口で原作の式による「本来の量」を計算する方式が必要（§96.4 注意 1）。

### §96.7 実機の記録 2 回目（2026-11-03 09:46、ユーザーのプレイ、x32dbg の記録だけ）
- ログ: `dev_lab/_work/summon_exp_20261103/trace_20261103_0946.log`（SHA256 634437A189849B4E8862FF8E25D4B7F55B292D71CE31ADA451E6A7E7304652A5）。2 回目の戦闘は 2950 行目以降。
- ACTUAL:
  1. 召喚者（48F24008、lv1）が 12 回召喚。12 体とも部隊なし・同じ R（1FE8AD58）・追従先 0。1 回目と同じ。
  2. 2 回とも召喚はちょうど 12 回で止まった。召喚数の上限（親 +0x168）が 12 の可能性がある。→ 未確認（親 +0x168 を読んでいない）。
  3. 子 2 体（494E1008、4910B4F0）が倒れた（GONE）。どちらも最後の召喚の後なので、倒れた後に子一覧が減るかはまだ分からない。倒れた子も終了時の SETTLE に来た。
  4. 子の攻撃 805 回はすべて部隊なしで加算 0。1 回目と同じ。
  5. 別の味方（48F425B0、lv5、部隊あり、子なし）は普通に攻撃で経験値を得た（184 回、1 回 10〜18、合計 2275）。この UnitData も次の閾値 +0x170 が 0。
  6. **そのユニットは戦闘中に倒れ（GONE）、終了時の SETTLE の入口では lv100・経験値 0 になっていた**（倒れる前は lv5・2275）。倒れてから SETTLE までのどこかで、レベル上限まで上がり経験値が 0 になった。閾値が 0 だとレベルアップのループ（0x58A650 型）が上限まで回ると読める。1 回目の lv99・閾値 0xFFFFFFFF のユニットも同じ現象の結果と推定。どの処理で起きたか（死亡処理 0x588D77 付近の経験値の書込みか）は未確認。
- 原因（ユーザー確認、2026-11-03 09:56）: 検証用 DAT で召喚者 hs_summoner と敵 hs_target に `exp = 0` を書いていた。DAT の exp は「必要経験値の基礎値」なので、閾値 +0x170 が 0 になった。原作の DAT の現象ではない。修正と経緯は `dev_lab/_work/summon_exp_20261103/SUMMON_EXP_LV100_ROOT_CAUSE_20261103.md`。48F425B0 は用意した敵（帝国歩兵 Lv5）、召喚上限 12 はこの検証用ユニットの設定。
- 補足（ログから）: 敵は 0x575110 の入口で既に lv100 だったので、上限まで上がったのは「倒れてから戦闘終了の判定まで」の間（死亡時の処理側）。召喚者は 0x575110 の入口ではまだ lv1・経験値 120・閾値 0 だったので、こちらは 0x575110 で上限まで上がったと読める。

### §96.8 実機の記録 3 回目: JOKER姉貴の「JOCAR発進！！」（変身型・部隊ありの召喚、2026-11-03 10:13）
- ログ: `dev_lab/_work/summon_exp_20261103/trace_20261103_1013.log`（SHA256 E6212581D32CD264A86AAB57EF8F0E250B3D7254B72A18542E13FF167B6DBAAE）、5535 行目以降。DAT は F20_summon.dat の sp_jocar → sp_jocar_dmg（attack_us=7、fix*999999）→ … → sp_jocar_nt2（func=summon、add=jocar、summon_level=100、yorozu=troop3）。jocar は break=jocar_break（倒れると joker_resummon で joker_re を troop3 で召喚）、element_lost=off。
- ACTUAL（順番どおり）:
  1. JOKER（4476A010、lv25、UnitData 1E27C6E0）が普通の攻撃で 990×24 回を得る（85506→107286）。
  2. LINK parent=JOKER、parent_dead=0、child=車（44ACC008）、**child_troop≠0**、child_ud=203610B8（JOKER とは別の R）。召喚は JOKER が倒れる前。
  3. 車の R は lv25・経験値 85506・閾値 102816 から始まった（召喚レベル 100% で JOKER の lv25 を写した値と読める。経験値は lv25 の下限か、戦闘開始時の JOKER の値のどちらかで、未確定）。
  4. 車の攻撃は 648 回すべて加算された（1 回 495 か 990、合計 400,950）。**入り先はすべて車の R（203610B8）で、JOKER の UnitData には 1 も入っていない。**部隊ありの召喚獣は経験値を得るが、子自身の記録に入る（§96.2 を実機で確認）。
  5. JOKER の GONE（children=1）。直後の JOKER の加算で、JOKER は **lv26・経験値 101,922** になっていた（倒れる前は lv25・107,286）。107,286×0.95＝101,921.7 なので、倒れたときに dead_penalty（95%）が掛かり、同時に閾値 102,816 を超えていた分で lv26 に上がったと読める（死亡処理 0x588D77 付近、既報の経験値の書込み。レベルアップの位置は未確認）。
  6. **倒れた後の JOKER にも +8,250 が入った**（sp_jocar_dmg などの攻撃が倒れた JOKER の手柄として数えられたと推定）。0x551E50 の条件に「倒れていない」は無いので矛盾しない。
  7. 車は倒れなかったので、joker_re の召喚（2 段目の親子）は起きなかった。
  8. SETTLE: JOKER（倒れた）lv26・110,172・閾値 667,014（上がらない）。車の R は lv25・486,456 で閾値以上なので 0x575110 で上がるが、R は戦闘後に捨てられる。
- まとめ: 変身中に車が稼いだ 400,950 はすべて車の R に入り、戦闘後に失われる。本物の JOKER に残るのは、変身前の分・倒れた後の手柄・dead_penalty の後の値だけ（予想: 戦闘後 lv26・110,172、ユーザーの画面で確認待ち）。
- スキル設計への影響: 「子の経験値を親へ」は 0x551FB2 のフックで実現できる（部隊ありなので加算が起きる）。joker_re のように孫まで続く場合は親を上へたどり、最終的に R ではない本物の UnitData（親子の表で最上位の親）に渡すのがよい。親が倒れていても渡すかは仕様で決める（原作は倒れた JOKER にも加算している）。


> 原本4194〜4683行は部分回収の対象外（unreviewed_appendix）。

