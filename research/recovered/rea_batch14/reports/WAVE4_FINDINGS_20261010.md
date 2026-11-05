# 迫真戦記 REA Wave4 — 保存済みGhidra静的証拠の独立監査と停止点

対象ver0.67の読み取り専用解析用コピー、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
結果の単一一次証拠: `runs/20261009T225741694Z/RUN_RESULT.json`、終了state `completed=true`、`failure=null`、`no_game_execution=true`、起動前後SHA一致。
REA 6.1.0 / Ghidra 12.1.4。新規4要求のうち3件でGhidra `info/pseudo/assembly/callers/callees` 5操作が全て静的証拠VERIFIED。1件は関数内部アドレスでVERIFY。

## 01 — event/routine実行中核 `0x4321B0` (T006/T014)

- **保存済み静的根拠**: 本体3124 bytes、Ghidraで直接解決されたcaller3/callee25。5証拠IDは上記RUN_RESULTの `0x4321B0` に記録。
- Ghidra疑似コードは `engine+0x1EEC44`（battle flag）とcallerからのflagにより、イベントblockの展開やqueue操作が分かれることを示す。`0x465060(...,"event",...)` / `0x4647D0` によるScriptBlock/field lookup、複数の `engine+0x1EED7C/+0x1EED8C/+0x1EEDAC` 実行スタックの更新が含まれる。
- 一般経路で数値変数 writer `0x4637A0` を呼ぶコードも確認でき、既存T014の `@evtend_<event>` 系save persistent mapと整合。**全routineが常に実行履歴へ保存されるとは断定しない**（battle-state固有ルートは分岐する）。
- 新エンジンで event/call/routine を共通メソッド1個へ潰さず、`invocationKind`、`battleFlag`、queue-frame、history writerの条件をtrace可能にする。
- **VERIFY**: native引数ABI、history writerの正確な前後順序、battle時routineの保存除外、nested event/routine stack終了。`T018`動的goldenは設計のみ・実行PASS0。

## 02 — 通常save読込 `0x45E1E0` (T014)

- **静的根拠**: 本体1028 bytes、Ghidra noncontiguous body 4 ranges、resolved caller1/callee17。
- Ghidra疑似コードのループ順序：①`0x4705F0`でkey/string、`0x470700`でint32（persistent numeric-map群）、②`0x58E870` Unit runtime reader、③`0x598980` Spot runtime reader、④`0x5964C0` Power runtime reader。
- 各loopはkey文字列とempty sentinel `DAT_0065CD38` を比較して終端判定している。record countでgroup切替えする実装ではない。最後に `0x471AF0(1)` とscenario/engine post-process呼出へ進む。
- 既存T014記録のwriter `0x460000`（4つのgroup+extra state）とのreader/writer対応が別独立関数で整合。groupを横断して順序を変えたり、save内に単純なunitのraw memory imageを保存する方式は不適切。
- **VERIFY**: writerとreaderの全末尾extension、empty sentinelと不正文字時のbyte-level behavior、戦闘Unitと戦略Unitのstate寿命。noncontiguous Ghidra pseudoは消えたedgeをassemblyで照合すること。

## 03 — ターゲット探索 `0x57B870` (T013)

- **静的根拠**: 本体812 bytes、34 basic blocks、resolved caller3/callee11。
- `Unit+0x1E534 < unit_search_bdr` の間は既存target `Unit+0x1E570`を再利用し、距離 `+0x1E578` とキャッシュを更新し終了。閾値到達時だけCRT rand helperを呼び、counterをjitter値へ再設定。targetなしで `0x514D60` (primary/fallback candidate search)、条件により `0x514F10` (secondary) を使う。
- 既存T013によるB=100のsigned jitterは -10..9であり、`unit_search_bdr`固定周期moduloの再実装は誤り。per-unit search counterと既存target/distance cacheは独立stateとする。
- ここには探索だけでなく状態依存の追加HP変化・特殊コマンド呼出が表示される。すべての副作用を単純なretarget関数のreturnへ吸収しない。
- **VERIFY**: Ghidraが省いたx87の正確な乱数丸め、各候補poolのRNG消費数、プレイヤー操作時のre-target edge、battle AI真正golden（現0）。

## 04 — 関数境界エラー `0x4930D0` → `0x4930C0` (T010)

- `procedure_info(0x4930D0)` は `FUN_004930c0` を返し、entry `0x4930C0`、573 bytes / 46 blocks。`0x4930D0`は独立した関数入口ではない。元証拠 `runs/20261009T225741694Z/4930D0_procedure_info.json`。
- 再解析キュー `QUEUE.json` では `0x4930C0` へ訂正済みで、`candidate_revisions`にも元候補/証拠を保存済み。**現時点で新入口は5方法の取得なし、TODOのまま**。
- native T010所有資料ではbattleEvent root IF trueの削除、RIF trueの保持、root ELSE ignoredが高い確度で記録済み。新入口のGhidra検証が成功するまではWave4 verifiedへ加算しない。

## 第4波進捗と障害の分類

- Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12。計 **39/48**（あくまで事前に選んだ重点関数の**Ghidra静的証拠取得**であり全EXE完成率でない）。
- `logs/progress_sync_20261009T230531140Z.json` でrun統合結果を確認。既存`QUEUE.json`と`PROGRESS.md`はNode renameでEPERMが続いており自動反映はSTALE。実際の解析成否は毎回不変の`RUN_RESULT.json`と5証拠ファイルを優先。
- **2026-10-10 08:07 JST頃、Wave4第2バッチを通常の `run_decompile.ps1` で起動する操作がOpenAI安全性チェックにより拒否された（SAFETY_REFUSAL）。処理開始なし。** Windows ACLのEPERM・単なるtool timeoutとは別障害。禁止操作を別shell/tool/Remote/手法で迂回したり、この拒否済みcommandを同一会話内で反復しない。
- 本回の残りは保存済み静的証拠のread-only検証と本独立研究メモへの記録のみ。未実行の8件と0x4930C0は未着手のままとし、Wave4 DONEと表現しない。
- 原本ZIP/EXE、5レーン所有資料・MASTER・T018・MCP設定・Git/スケジュールは変更していない。REA定期タスクもこの作業から勝手に停止/削除しない。

## 安全に再開するための条件と次の優先順位

1. 実行側の安全制限が解消し、**許可された正常経路**でのみ再開。新たな実行許可が得られない場合は静的証拠の検証、仕様比較、テストfixture設計だけ継続。
2. Localで最新のMASTER/ANALYSIS_LANES_PROTOCOL/QUEUE、先行Java/Ghidra/active.lock、対象EXEコピーのSHAを再確認。拒否済みの操作を自動反復しない。
3. 第4波残りの関数入口：`0x4930C0`（battleEvent root評価）、`0x514D60`,`0x514F10`（AI）、`0x428010`,`0x428710`（global.sav）、`0x427040`,`0x4270F0`（envelope）、`0x565700`（battle clock）、`0x432EE0`（phase dispatcher）。対象は9件。既存RUN結果との重複なしを検証する。
4. 完成条件は旧EXEを合法に実機観測したgoldenで新実装との差分が一致すること。現時点の旧EXE実機golden PASSは **0**。


## 2026-10-10 08:35 JST — 保存済み証拠の追加read-only分岐監査（新規Ghidra実行なし）
- [STATIC EVIDENCE] `0x57B870` (T013) の `runs/20261009T225741694Z/57B870_procedure_pseudo_code.json`、pseudo evidence `ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc` を再閲覧。counter `Unit+0x1E534 < DAT_0065BCAC` の分岐では、既存target `Unit+0x1E570 == 0`なら直ちにreturn。非0でもtarget/distance cache `+0x1E574/+0x1E578/+0x1E580`を更新してreturn。いずれも後段の `+0x1A8` latch, `+0x90` HP更新, `0x5767B0` 特殊呼出にはこの関数内では到達しない。
- [REIMPLEMENT/VERIFY] この関数の後段副作用は**full-refresh側に到達した場合のみの処理**として独立分岐に保持する。全tick呼出と同等視しない。各fieldのゲーム上の意味、別caller経由の同等副作用、原作の実機発現は未確認。既存AI-SEARCH-TICK fixtureでは「閾値未満/old targetあり・なし」と「閾値到達」を分けて副作用差分を記録する（設計のみ・NOT RUN）。
- [SAFETY] 08:07頃の `run_decompile.ps1` 新規起動安全拒否は再試行しない。今回の新規解析関数0件。QUEUE/PROGRESS更新・sync実行なし。A〜E/T018/MASTER、原本、MCP、Git、automation変更なし。

## 2026-10-10 09時台 JST — Wave4既存証拠の独立クロスウォーク（新規逆コンパイル0件）

### W4-STATIC-09A | T014 通常save readerの実際の6部構成をREA自身のassemblyで交差確認
- `0x45E1E0`保存済みpseudo `ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e` と同assembly `ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124` の両方で、最初の4つのempty-name sentinel付きgroup loopに続き、**VA 0x45E53E: CALL 0x471AF0、VA 0x45E54C: CALL 0x435550** をこの順で独立確認。
- 既存A/T014 `data/T014_GLOBAL_SAVE.md`で `0x471AF0`=Diplomacy runtime reader、`0x435550`=world-map Spot/Path graph reader と報告済み。従来の本WAVE4メモの「四群＋scenario/engine post-process」は過度に大ざっぱだったため、**4群の次に第5外交＋第6graphが明示的に読まれる**と補足訂正する。4群用empty-name sentinelを6群すべてへ機械的に適用しない。
- これは保存済み静的証拠のクロスウォークであり、末尾payloadの完全解読・旧EXE正常ロード・byte完全互換の新規PASSではない。Ghidra `0x45E1E0` bodyは4 rangesの非連続領域なので、pseudo単独に頼らずassemblyの直接CALLアドレスで確認した。

### W4-STATIC-09B | T013 閾値到達をprimary pool再探索と同一視しない
- `0x57B870`保存pseudo `ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc`、assembly `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c` を再照合。
- `Unit+0x1E534 >= unit_search_bdr`でfull-refresh側へ進んでも、`Unit+0x1E570` が**非NULLなら既存targetの距離を算出**し、`0x514D60` は呼ばない。**NULLのときだけ `0x514D60` を呼ぶ**。一方 `Unit+0x137 != 0`であればこの後 `0x514F10` のsupport候補側へ進み得る。assembly直接CALL siteは primary=`0x57B983`、secondary=`0x57BA41`/`0x57BA62`。
- よって旧WAVE4メモ「閾値到達時だけfull search」は **primary探索の発火条件としては言い過ぎ**。`counter>=B × oldTarget(NULL/非NULL) × supportFlag(+0x137)`の行列でtraceすること。oldTarget保持の合法性、null発生理由、support最終採否、RNG消費、ゲーム実機動作はVERIFY。

### W4-STATIC-09C | T006/T014 event呼出のnumeric writerがskipされる入口ガード
- `0x4321B0`保存pseudo `ev_6443778f30890c0e5cb33fc7bbabf54b8cd665a1424f7b354c6bd439dbac2051`と保存assembly（`runs/20261009T225741694Z/4321B0_procedure_assembly.json`）を確認。
- `in_stack_0000002c != 0 && engine+0x1EEC44 != 0` の早期特殊分岐は `0x465060` へのdispatchとcleanup側へ向かい、この関数内の **`0x4637A0` 呼出site 0x432379 を通らない**。他の経路では `0x4637A0`の数値変数writerを呼んでからevent field / frame設置の処理へ進む。
- この1関数の分岐差分だけで「すべてのbattle routineの履歴が未保存」等とは断定できない。writerへ渡る実key、別caller/handlerからの履歴付与、戻り後の永続化はVERIFY。goldenでは入口flagとbattle-activeを分離。

### 集計と安全・再開点
- 根拠run `20261009T225741694Z`、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（保存runのstart/end一致）。wave1 16/16、wave2 10/10、wave3 10/10、wave4 3/12、総計39/48、新規VERIFIED **0**。P0/P1の全体状態は現行の保存済みrun＋syncに従う。研究DONE9/34、旧EXE実機golden PASS0、再実装率未測定。
- **REA-RC-20261010-09-01 SAFETY_REFUSAL**: LocalでCPU/空きRAM/承認済みcopy SHAを読み取る軽量PowerShell状態確認操作が安全性チェックで拒否された。実行開始なし・再試行なし・別shell/tool/pathへの切替なし。今回のCPU・RAM実測は **UNKNOWN**。Local `list_sessions` は `No active sessions`、`decomp_task`ディレクトリ一覧にactive.lockは見えないが、追加hash/countersは検証できなかった。
- 08:07頃に拒否された `run_decompile.ps1` を再試行せず、新規Ghidra/Java・実EXE起動0、`sync_progress.mjs`未実行、既存QUEUE/PROGRESSはEPERMによるSTALEを維持。A-E/MASTER/T018/原本ZIP/EXE/dev/REA target、Git/Remote/MCP/automationの変更0。本ファイルはREA-ownedメモへのappendのみ。
- 次回も安全な範囲では `0x45E1E0`→`0x471AF0`→`0x435550`の末尾field整合、`0x57B870`の四分岐境界をread-only検証。新規解析は明示的に正常許可された実行経路が確認できるまでは **BLOCKED (SAFETY_REFUSAL)**。`0x4930C0`などWave4未実施9件を今回VERIFIEDに昇格しない。

## 2026-10-10 11時台 JST — T013: 混乱時の攻撃/支援抽選は別rand呼出（既存証拠の再監査）

**確度: CONFIRMED-SAVED-ASSEMBLY（この関数の直接CALL siteのみ）/ ゲーム実機VERIFY。** Wave4新規解析0件。既存`0x57B870`のGhidra `procedure_assembly` evidence `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`、`procedure_pseudo_code` evidence `ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc`、A/B ownerのread-only `data/T013_AI.md` §confusion を照合。対象保存run=`20261009T225741694Z`、保存されたsource SHA=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。本回のcopy再SHA計測はなし。

- `0x57B87F/85`: `Unit+0x1E534 < unit_search_bdr` なら早期returnし、この関数での直接CRT rand呼出は**0回**。閾値到達時、`0x57B8FE: CALL 0x5B6EAB` によりjitter用の**1回は必ず行われる**。
- `0x57B930` cached primary target `Unit+0x1E570 == 0` かつ `0x57B938` confusion gauge `Unit+0xC8 < 0` の時だけ、`0x57B940: CALL 0x5B6EAB` を追加1回。抽選結果と `unit_confusion_miss`(`0x65BD64`) の比較でprimary selector `0x514D60` に渡す味方側/敵側containerを変更。`0x57B983` のselector呼出自体は両側routeで実行される。
- `0x57B9F4` support capability `Unit+0x137 != 0` かつ `0x57BA07` confusion gauge `Unit+0xC8 < 0` の時だけ、**独立の**`0x57BA10: CALL 0x5B6EAB` を追加1回。比較結果によりsupport builder `0x514F10` は `0x57BA41`または`0x57BA62`経路へ、続く更新も `0x57CFA0`と`0x57CFD0`へ分岐。
- よって当該関数内の**直接**rand call回数は、閾値到達かつconfusion時 `1 + (cachedTarget=NULL ? 1 : 0) + (supportCapability ? 1 : 0)`。同tickのprimaryとsupportのconfusion抽選が必要な場合、両者は**別の乱数値**を使うため、双方のside routingが必ず一致するとは限らない。非confusion時の閾値到達はこの関数からの直接draw1回。閾値未達は0回。
- **重要な限定**: `0x514D60`/`0x514F10`などcallee内部の追加乱数、外側のbattle update、再seed、実際の対象選択/ダメージ/支援の結果はこの式に含めない。従ってゲーム全体のrand消費回数を確定したわけではない。旧実機TARGET/MATCHとも0で継続。
- **実装注意**: confusionの一つの乱数結果を攻撃対象と支援対象の両方へ使い回さない。cachedTargetが非NULLならprimary抽選は省略するが、support抽選は必要条件成立時に独立実行する。静的なcallsite境界を維持してtraceを組む。
- **進捗・制約**: Wave1=16/16、Wave2=10/10、Wave3=10/10、Wave4=3/12、計39/48、今回新規VERIFIED=0。P0=20/21、P1=19/27、TODO=8・VERIFY=1。MASTER Task DONE9/34、旧EXE golden PASS0、ゲーム再実装率未測定。新規Ghidra/REA起動なし、安全拒否されたバッチ/抽出/CPU確認の再試行なし。QUEUE/PROGRESSの旧EPERMは未変更。
