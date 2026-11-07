# 迫真戦記 Strict互換 → 改良 開発計画（2026-10-10）

## 最終目的と原則

原作ver0.67同梱のPE32 x86 `Vahren.exe` と同じ挙動を持つ、独立の新エンジンを構築する。
完全再現後は、旧挙動を保持する `strict-067` と修正・改善用 `enhanced` を分離する。
最初の互換対象は迫真戦記ver0.67。Vahren701は別世代の比較資料であり、仕様を混ぜない。
ライセンス/公開は後回しでもよい。ゲーム素材の再配布は別途権利整理が必要。

## 検証の4段階（混同禁止）

1. **BYTE**: 元データを同じバイト列に戻せる。map/metadataのroundtripや各ファイルSHA-256。
2. **STATIC**: 既存EXEの逆アセンブル・疑似コード・原作script・既存台帳と整合する。
3. **TARGET OBSERVED**: 旧EXEの合法なfixture実行で入力・乱数・状態・出力を観測し記録した。
4. **REIMPLEMENT MATCH**: 同じfixtureで新エンジンの出力がTARGET OBSERVEDと一致する。

現時点の成功はBYTE/STATICが中心。T018の旧EXE実機golden PASS数は0のまま。

## 開発の作業区画

- `dev_lab/` は新実装・テスト・報告書だけを書き込み、研究正本は読取専用。
- `rea_lab/` は解析成果の参照のみ（安全拒否済み抽出処理・EXE領域へ手を出さない）。
- 解析レーンA〜Dの仕様追加、レーンEのMASTER/T018統合は既存の権限規則に従う。
- 初期のPython実装は仕様の自動検証・純粋データ層。最終ゲームランタイム言語/描画基盤の選定は後日。

## M0 — ファイル読込基盤（現在進捗: 静的回帰PASS）

- map: 151/151 SHA-256一致、EOF完全消費、byte-exact roundtrip。
- atlas: BMP+metadata 2組、合計513レコード、矩形bounds・メタデータroundtrip。
- context: CP932、204代入、203キー、T009と行・値一致。重複battle_fast=onを保持。
- 1v1 RTS: 140×55 / 初期2ユニット、2v2 RTS: 120×70 / 初期4ユニット。
- native RNG subset: seeded LCG・範囲抽選・<=32767要素のshuffle。追加で0x479A30の28byte物理stride/24byte swap・32767超のdraw連結をバイト列限定の別モデルに実装。全seed境界・末尾4byteの意味はVERIFY。
- 独立単体テスト254件成功（2026-10-11時点）、T012数値/ダメージ/linked命中分岐35件＋mode6固定値8件＋距離減衰厳密平方根10件＋後段status分岐21件を追加。保存済みGhidra5点証拠の検証ソース化39件（初期別保存2件を含む）。旧EXE実機と新エンジンの動的互換比較は未実施。

## M1 — 宣言・スクリプト完全ロード（進行中：CP932/lossless lexerの入口を実装）

- [Ghidra疑似ソースBOOK作成済] `dev_lab/recovered_source/INDEX.md`。通常run37＋初期 `rea_lab/results/VALIDATED_EVIDENCE_20261010.json`対象2の計39関数を、ソース本文ハッシュ・5種証拠ID・caller/callee・Taskとともに `ghidra_c_pseudocode/*.c`へ保存。これはGhidra非可逆のC風疑似コードであり**原作者C++復元でも完全ビルド可能なゲームでもない**。`recovered_source_snapshot_20261010.zip`は以前のsourcebook snapshotとして保管。T012型付きモデルと追加35件試験を含む更新版は`recovered_source_snapshot_20261011.zip`として別名で作成。

- [済/字句層] CP932の全590 script DAT（14,591,845 bytes）をbyte-exact再構成し、42,912個のraw spanに分ける。コメント集計20334/392/2058がT005と一致。debug行の意味適用は未着手。
- [実装済/宣言ヘッダー] 30,695件すべての種別・親宣言をT005と照合。本文が括弧不一致の5宣言は不完全ノードとして記録し、勝手に補完しない。
- [実装済/候補グラフ] T011対象30,634宣言、親21,214参照、未発見56、曖昧1,292を独立照合。候補の優先順位・実際の値継承は未実装。
- [実装済/sci1静的輪郭] 29 power/129 spot/26 roamおよびworld=wev1/fight=fev1/politics=ev_poliを抽出。実行・可視状態は未検証。
- [限定実装] `generic_properties.py`: native確認済みのscenario `map` など、明示allowlist指定されたgeneric keyに限り、先勝ち・qualified variant・explicit null・control block内のparse-time回収を再現。特殊handler、multi-line値は未対応。
- [限定実装] `script_body_subset.py`: if/rif/while/battle/else・単一行代入/関数呼出を元ソースspan付きの構文木として保存。原作3ファイル16宣言サンプルでrecognized2,896/opaque26、parser error0。追加した`event_ast_corpus_audit.py`で590 DATからevent507＋scenario9、計516本文をサンプリングし、recognized71,346/opaque172、span mismatch0、解析error0（不完全宣言4件は選択対象外）。特殊item・多行文字列、全30,695宣言ASTは未達。
- [未実装] 宣言内部のassignment/call/if/rif/whileを完全ASTへ展開する。
- 継承・scenario variant・明示 `@`・list/duplicate構文を元データを失わない形で保持。
- declaration graphの名前・件数を `T005_DECL_INVENTORY` と独立照合する。
- キー上書きは共通last-winsにしない。generic first-winsとspecial parserを別実装。
- **合格条件**: 全現役script corpusで型・名前・継承が漏れず回収され、失敗は未実装として記録。

## M2 — 決定論的スクリプトVM/状態管理

- [限定実装] `battle_root.py`: root `if` true後除去 / root `rif` true後も保持 / root ELSE無視の契約シミュレーション。条件評価と各種command実行は外部依存で未実装。
- [限定実装] `search_cadence.py`: T013/0x57B870から探索閾値到達のper-unit counter、B=100時の[-10,9] jitterによる91..110更新間隔を純粋計算モデルとして固定。候補探索・RNGの他consumerは未実装。
- [限定実装] `expression_subset.py`: int32数式と短絡`&&/||`・副作用call/unknown拒否。`micro_vm_subset.py`: synthetic numeric set/add、if/while、next Yield、break/continue、再開ステップ。`event_vm_subset.py`: 別の合成event registryでevent/callはYield、routineはContinue、returnはcall境界unwind、waitはpassごとのカウンタを保持。nativeのarg1/2・battle wait特殊path・全commandは未実装。
- event/call/routineのstack、if/rif/while/return/next/break/continue、numeric/string変数。
- 旧エンジン固有のYield/Continueとターン・戦闘フェーズの評価順序。
- seeded RNGとstartup/reset/load/map-local/map-exitの再seedをログ付きで分離。
- [合成fixture PASS] `save_envelope.py` でT014/T031共通envelopeの32byte header/28draw鍵/絶対byte indexの暗号化と復号、`global.sav` key/aux/int32/末尾marker、gwriteのaux上書きを再現。既存 `T014_GLOBAL_CODEC_GOLDEN.json` 暗号文SHA256一致。実save byteは未提供なのでMATCHとはしない。
- [静的writer/reader照合+限定byte fixture PASS] `native_stream_strings.py`: 0x470830は全文検査し不正byteならNULのみ、0x20..0x7Fを許容。`unit_runtime_prefix.py`: Unitの5string/10dword/flags7+1/4vector終端とE4/E8の中間順序をreader/writer両者から確認。`spot_runtime_writer_fragment.py`と`power_runtime_writer_tail.py`: 保存済みwriterだけに基づくcapacity等のtag、home_spot2連続empty sentinelをsynthetic inverseで確認。後半本家reader・実savは依然VERIFY。
- [限定実装] `battle_clock.py` はabsolute tick、resettable getTime、isIntervalの10量子化、10tick単位のlimit更新を分離。native int overflow/zero intervalなどは未実装。
- [保存Ghidra静的証拠＋合成テスト] `event_view_branch.py`: event general/special early branch、初期判定＋2参照判定のlazy順、(flag54,55)=(1,0)/(0,1)/(0,0)による2ポインタ再配線を6件検証。`0x464290` qualified key presence判定の50-pass guardも保存assemblyで独立確認（既存`0x4647D0`値取得側の50-passと別）。native full event状態復元はVERIFY。
- [保存native caller契約] `eb40_caller_contract.py`: 未解析0x57EB40を2箇所から mode0/1で呼ぶ。行動分岐callsiteではAL非zeroでnatural recovery+postcall skip、別反復callsiteではALを見ずにindex++。caller-onlyでありcallee semantics未解析。
- [保存静的証拠+合成試験] `script_rng_quirks.py` は `index(list,N)`→末尾、`pushRand2` 出力の下位16bit偏り、pre-draw `raw==count`受理を保持。`confusion_refresh_subset.py` はT013 search coreの直接3段階CRT消費をモデル化し、selector/callee内drawを推測で合算しない。
- native command registryを参照し、実装済み命令と未知命令を明示。
- **合格条件**: VM microfixtures、戻り値、乱数消費、イベント実行順を再現可能。

## M3 — 世界・内政・戦闘のヘッドレス縦断実装

- scenario sci1の最小ロードから勢力・spot・unit・player・ターン0を構築。
- World/Fight/Politicsのphaseを駆動し、具体的なデータモデルとsave/loadを接続。
- 最初の試運転対象は、1v1 RTSの初期マップ→初期ユニット→1 tick→結果ログ。
- [時計のみ縦断PASS] `headless_clock_scene.py` は実1v1/2v2の地形・静止ユニットを読み、BattleClockと合成root if/rifを20tick実行してJSON出力できた。原作スクリプト実行、Unit移動、ダメージ、AIは未実装。
- [限定実装] `synthetic_vm_scene.py`: 実マップ＋合成数値VM＋clockを31tick駆動しdeterministic traceを保存。Native event実行ではない。
- [限定実装] `targeting_subset.py`: SimpleUnit primaryとSimpleStaticUnit fallback、stealth primary-only RNG、strict nearest/tie、primary射程外でもbestを保持する二段階距離比較、best/auxiliaryの2 pointerを区別。上位AI行動は未実装。
- [合成縦断PASS] `synthetic_invocation_scene.py` 1v1/2v2 実stage上でevent→child wait(2)→return→親再開を8 pass trace。`synthetic_ai_scene.py` は仮team/全SimpleUnit割当で120tickを試験。閾値到達とprimary selector呼出を分け、1v1=refresh4/selector2、2v2=refresh8/selector4。cached targetがあってもjitterは消費する。ユニット移動/攻撃/本家AI判定は未実装。
- [純粋数値試験PASS] `status_recovery_subset.py` はT012のpoi/sil正回復skip、負HP早期virtual要求、MP下限0、7ゲージ上限capを限定実装。death-like vfunc副作用とaction cadence全callerはVERIFY。
- [保存native文脈＋合成RNG抽選] `negative_heal_flow_subset.py`: core入口chanceの発動回数1、amount>=0負値gate bypass、r=default5/clamp0..10、r²により全候補処理の早期終了、r²通過時2追加rand+contest差<=10では次候補へ、damage_consti table最大11のnonzero overrideをモデル化。x87 integer conversion/skill mutationは外部注入／未実装。
- [保存Ghidra+native callsite] `spatial_presence_subset.py`: 0x4E7ED0の非0 mode方向1-cellと0 mode radius sweep、signed trunc/32、候補の共通4フラグ、strict distance < reach、およびsource sweep reach+32の局所契約を6試験。trig/direction data/実際の距離値は外部VERIFY。
- [保存native callsite] `missile_latch_subset.py`: 0x546F70のUnit+0x1E560=0/1/2 state machine、空間判定後のlatch=1/2、Skill+0x278 MP debit前の早期retを6試験。前段skill可否と後段damageは未実装。
- [保存Ghidra/アセンブリ+合成試験] `typed_damage_fragments.py`(10)：0x550D80 mode1..5の攻撃式、0x550E70防御+0x9C/+0xA4とnegative odd/signed overflow時のmode3 0方向平均、0x5D1B80非default SSE局所。x87 native通常丸めは明示的に未実装。
- [保存Ghidra/アセンブリ+合成試験] `damage_two_draws_subset.py`(8)：攻撃/防御それぞれ独立rand15×2、通常3回・mode6独立3回のnative変換、damage_consti乗算とsigned32差、mode6は後段0x551020で固定値100×scale+0.5に上書き（mode6新規8件）。`damage_final_branch_subset.py`(8)：r10/scale0/mode6/r0/ordinary-minの分岐優先順とdamage virtual呼出の有無。HP実変更は未実装。
- [保存Ghidra/アセンブリ+合成試験] `hit_linked_award_subset.py`(9)：0x551E50 context-once、参照Unit+0x1C8の+0x16C加算、Skill+0x2A8 sentinel / ratio mode3,4,5 / threshold unsignedでlevel helper要求まで。レベルアップ・通知実効未実装。
- [新規合成10件] `damage_distance_gate_subset.py`: 0x55103D..0x5510D7の射程開始+0x250=0ならskip、非zeroではMath factor=clamp((max−sqrt(signed32 dx²+dy²))/(max−min),0,1)とN(damage×factor+0.5)を、非負の完全平方距離に限定して再現。x87 sqrt・control word・非平方距離・native default丸めは未実装。
- [保存Ghidra + 新規21合成] `damage_status_dispatch_subset.py`(11)と`damage_status_candidate_subset.py`(10)：0x550E70末尾optional補助call/早期Unit8D/候補source/共通発動chance RNG/Skill14C mapping・vector234全件/1件選択、各recordのr²阻止は**次recordへ**、通過時だけ2追加rand＋dext差>10でstatus helperを要請。負値healのr²阻止＝全中断とは異なる。native丸めとvirtual副作用は未実装。
- 戦闘計算0x550E70、状態処理0x576E30、targeting、skill、tick順を独立モジュール化。
- **合格条件**: 同一seed・同一入力でゲーム状態遷移の再現性があり、goldenを実行可能。

## M4 — 画面・入力・描画・音声・保存

- 描画はルール判定から分離。元map/atlas+loose chip優先規則、UIや音量0など既知癖にも対応。
- 正規ゲーム操作、セーブ/ロード、イベントダイアログ、RTS・通常戦略の各モードへ拡張。
- **合格条件**: ゲーム開始・戦闘・終了・再ロードまで通しプレイできる。

## M5 — 原作互換の確立と改良モード

- T018 goldenの旧EXE実測条件を満たす部分から、差分を機械比較。
- 残るP0/P1 UNKNOWN/VERIFYを解消し、未観測の挙動を『一致』と呼ばない。
- 厳密互換が成立した要素のみEnhancedの改善を追加。strict側への意図しない影響は回帰テストで防ぐ。
- **完成判定**: 原作の主要ゲーム導線/スクリプト/戦闘/セーブを観測済みgoldenで照合でき、未確定事項を明示。

## 具体的な次回タスク（正本T-IDとは別の開発用タスク）

| 順位 | 開発ID | 成果物 | 完了条件 |
|---|---|---|---|
| 1 | DEVLAB-001 | DAT lexer / comment scanner | script 590件をCP932 decodeし、不明tokenを報告 |
| 2 | DEVLAB-002 | 宣言AST＋シナリオロード | T005宣言inventoryと整合 |
| 3 | DEVLAB-003 | Unit/Skill/Spot定義resolve | 継承＋ExplicitNull＋scenario overlayの区別 |
| 4 | DEVLAB-004 | VM小ステップ処理 | Yield/Continue、if/rif/whileの合成fixture |
| 5 | DEVLAB-005 | 1v1 RTS初期シーン駆動 | 入力→1tick→状態を再実行可能JSON化 |
| 6 | DEVLAB-006 | old-vs-new比較runner | 原作観測が入れば数値/順序/出力差分を検出 |

**注意**: DEVLAB番号は独立実装用であり `MASTER_LEDGER.md` のT番号やA〜Eレーン担当を変更しない。

## 安全・非重複

- 原本ZIP/EXE・研究正本を編集しない。Git操作、配布、プラグイン/MCP設定も別途明示許可なしには実施しない。
- 過去に安全拒否されたUnit constructor逆解析やREA証拠text extractionを別tool/routeで再試行しない。
- 他の5レーンの実行中は重いGhidra解析を並列起動しない。このラボの軽量テストは独立実行。
- テスト成果は入力SHA-256・手順・成功/失敗・未確認を保存し、Eレーンが必要な時に読み取れる形を維持。
- 真の原作動作を試験する前に`TARGET OBSERVED`と書かない。レポートは追記型・既存上書き禁止。
