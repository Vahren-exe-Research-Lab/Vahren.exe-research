# T025/T016: dream勝利guardのcleardazo単独参照とed1再入差（C-20261015-0425-01）

- ID / owner / status: C-20261015-0425-01 / C / READY = ver0.67原作SCRIPT限定。旧EXEの変数値・実発火・GameplayはVERIFY / NOT READY。
- PRIMARY original relative: a_default/script/3000_淫ドリームマッチ/ev_dream.dat:618-655、event_world.dat:285-307、7000_その他シナリオ/free_ev_world.dat:120-141、5000_ランダムシナリオ/ev_rnd.dat:568-603。
- SOURCE Dream通常勝利gate: `if((isComTurn()||isNewTurn())&& clearflag && cleardazo)` → `set(ed1,1)` → `wait(25)` → `setGameClear()` → BGM/画像/後続dialog。
- SOURCE Dream観戦勝利gate: 別の後続ifで `countPower()<2 && isWatching() && (isComTurn()||isNewTurn())&&ed1<1` → `set(ed1,1)`、`set(clearflag,1)`、GameClear等。
- SCENARIO contrast: sci1/sc_freeの通常勝利は `clearflag && ed1<1 && yet(po23_ed_A)`、rscは `clearflag && ed1<1`、dream通常勝利だけこの比較範囲で `ed1<1` がなく、代わりに `cleardazo` を要求する。4WorldのGameClearを同一guardへ正規化禁止。
- Literal census: Desktop Commander Local Compactのliteral content searchで normalized ver0.67 `a_default/script/**/*.dat` の `cleardazo` は `3000_淫ドリームマッチ/ev_dream.dat:620` ただ1件（検索内ほか0件）。当該SCRIPT集合に同literalの直接set/add/sub/clear writerを発見せず。
- CONFIRMED-SCRIPT: 上記の比較、`cleardazo`唯一の字面参照、通常勝利gateの`ed1`検査欠落、独立観戦gateの存在だけが確定。
- VERIFY / UNOBSERVED: `cleardazo`のnative初期値・旧SAVE由来・動的参照・別script範囲/EXEの内部writer、実際のnormal勝利到達、GameClear Yield後のframe終了/再入、二重画面描画・原作不具合は未証明。literal参照1件を全実行経路のwriter不存在と拡張しない。
- CONDITIONAL: `cleardazo` が真で `clearflag` が維持され、後続のCOM/NewTurnで同gateが再評価されるなら、`ed1=1` のままでもSOURCE通常勝利ifに進む入力式。一方、旧EXEのGameClearによるscene終了・再入不成立・cleardazo偽なら実二重演出は結論不可。
- SAVED NATIVE cross-check: A所有 `exe/T006_TARGET_DISPATCH.md` / `exe/T006_GAMECLEAR_ARG_PROBE.txt` にある0引数setGameClearのshort helper/Yieldは既知。今回の新native解析ではなくDream独自guardの源コード比較が新増分（旧C-20261015-0322-01はsci1/freeへの既存native接続）。
- REIMPLEMENT: per-scenario World victory predicateを分離し、dreamでは`cleardazo`の未知値を勝手に0/1固定しない。既知`ed1`をdream通常勝利gateへ自動追加しない。normal/observer分岐・0arg GameClear/Yield・後続演出・VM再入を別traceに保存。
- GOLDEN DESIGNED / NOT RUN: 合法dream原作UI/SAVEでclearflag前後、初回COM/NewTurn→次COM/NewTurn、観戦/通常、ed1の可能な変化、可視GameClear・dialog・BGM・保存時scene/Power/Spotを同SAVE SHAと操作列でold/new比較。cleardazo値や合法trueケースが見えない/作れない場合は当該内部分岐をINELIGIBLE。旧原作Gameplay actual Golden PASS0、新旧strict MATCH0。
- DEDUP: 既存T025§47/§98/§99/§96、C-20261015-0225-01、C-20261015-0322-01を再計上せず。新規性はdream固有guardの字面参照1件とed1検査欠落の組合せ。旧原作BUG確定0、Task DONE増0。
- OTHER P0: T025 boss_dead setv/clear/erasePower native、WorldWar po/poo self/inactive union、sc_free queue、T029城壁5回・50000、T026先生生徒一時値、T027財布/在庫、T033旧ID到達性はVERIFY継続。
- RECOVERY: 旧C-RC-20261014-1824-01・旧C/T026/T032等の安全拒否はBLOCKED維持し元payloadの別shell/tool/path/Remote/分割再提出をしない。E cp152統合拒否もE所有BLOCKED、本IDのMASTER正式統合は未実施。
- OWNER/RUN: C所有新規evidenceとLANE_C_HANDOFFのみ更新対象。原本ZIP/EXE/シナリオ、MASTER/T018/他レーン、rea_lab/dev_lab/Work、Git/push/MCP/automationを変更しない。PID21336入力待ち非介入・PC CPU率n/a・重量解析run0。
