# 迫真戦記 ver0.67 — 独立互換エンジン開発ラボ

目的: **原作同梱EXEの挙動をStrict互換で再現し、その後に改良モードを発展させる。**

ここは新規コードと回帰テスト専用。`../MASTER_LEDGER.md`、A〜Eレーン資料、原本ZIP/EXEは読み取り専用。既存Git/MCP設定やスケジュールは変更しない。

## 実装状況（2026-10-10）

- `map_codec.py`: 迫真151 mapすべてbyte-exact再エンコード、全SHA-256照合。
- `image_codec.py`: BMP32+atlas metadata 2組・513レコードを解析/再エンコード。
- `context_codec.py`: CP932 context.dat 204代入・203キーと原証拠一致、先勝ち重複規則を採用。
- `battle_initial.py`: 1v1/2v2 RTSマップの地形・ユニット配置を不変データへ変換。
- `legacy_rng.py`: native MSVC LCG、限定range、forward shuffle、明示的なreseed境界。
- `script_source.py`: 現役590 DATをCP932でbyte-exact復元し、コメントをlossless spanとして保持。14,591,845 bytes、42,912 spans照合。
- `declaration_ast.py`: 590スクリプトで30,695宣言ヘッダーがT005一致。本文終端未確定5件を明示して隔離。
- `parent_graph.py`: 30,634対象宣言・21,214親参照をT011と一致照合。56参照は候補なし、1,292参照は複数候補。
- `scenario_surface.py`: sci1の29勢力・129拠点・26放浪ユニット宣言と関連イベントを非実行で抽出。
- `generic_properties.py`: native保存証拠T005による一般プロパティの先勝ち登録・qualified variant・explicit `@`・if内でのparse-time回収の限定モデル。特殊fieldや完全ASTは未実装。
- `battle_root.py`: T010のbattleEvent root if（一度成立すると削除）/rif（反復）の純粋なtick単位契約モデル。イベント命令実行は未実装。
- `search_cadence.py`: T013のB=100などのper-Unit探索カウンタと±10%相当のreset jitterを限定再現。ターゲット選択自体は未実装。
- `save_envelope.py`: 32byte header＋28byte additive key／global.sav key・aux・int32とupsertを静的根拠に基づき実装。T014既存合成fixtureの暗号文SHA256が完全一致。実ゲーム保存fileは未観測。
- `battle_clock.py`: reset可能getTimeと絶対tickを区別、isIntervalを10刻みに量子化、limitを10tickごとに更新する限定純粋モデル。
- `headless_clock_scene.py`: 1v1/2v2実stage配置を読み、合成if/rifと戦闘clockを20tick駆動してJSON化。Unit移動・戦闘・本家VMは未実装。
- `expression_subset.py`: 整数数式・比較・関数呼出・`&&/||`短絡評価の限定AST。右辺の乱数消費をnative同順序でskip可能。unknown token/overflowは停止。
- `script_body_subset.py`: if/rif/while/battle・assignment/callの元文字位置保持AST。未解析構文はopaqueのまま保持。全grammar実装は未達。
- `micro_vm_subset.py`: synthetic numeric `set/add`、if/else、while、next(Yield)、break/continueの有限ステップVM。実イベントのsave/wait/command網羅なし。
- `event_vm_subset.py`: 合成event registryを利用し、event/callのYield、routineのContinue、returnフレームunwind、waitカウンターの再訪問を限定的に再現。optional args・完全native stack・battle特殊pathは未確定。
- `synthetic_vm_scene.py`: 原作RTS 1v1/2v2 stage配置＋合成VMと戦闘時計を31tick連動、10/20/30tickで数値更新するJSON trace。
- `synthetic_invocation_scene.py`: 実1v1/2v2マップ配置＋合成 event/routine/wait/return を8 VM pass追跡。イベント呼出順序と中断位置はJSON化するが旧EXE実行ではない。
- `targeting_subset.py`: SimpleUnit/StaticUnitの2pool、ステルスgate、strict近距離比較に加え、primary射程外でも現在の最短値を保持してfallbackと比較するhelper契約を実装。native出力2ポインタを`uid`と`auxiliary_uid`に分離。後段AI行動との対応は未確定。
- `synthetic_ai_scene.py`: stage上の静止ユニットに**仮チーム**を割り当て、120tickのカウンター満了`refresh_checks`と実selector呼出を分離。1v1 refresh4/selector2、2v2 refresh8/selector4。native実陣営/移動/戦闘は未実装。
- `status_recovery_subset.py`: HP/MP自然回復のpoi/sil gate、7ゲージupper cap、HP負値早期virtual経路を純粋数値試験。nativeの死因副作用とaction tick到達は未検証。
- `native_vector_shuffle_subset.py`: 保存Ghidra 0x479A30を物理28byte stride・先頭24byte swap・unsigned 15bit拡張rand indexまで別モデル化。残4byteの意味はVERIFY。
- `script_rng_quirks.py`: native string `index`の範囲外clamp、pre-drawのcount等号受入、`pushRand2`の15bit格子出力を合成契約化。
- `confusion_refresh_subset.py`: 0x57B870の直接CRT rand (jitter/primary混乱/support混乱)を独立3箇所として計測。callee内部の追加drawは含めない。
- `spatial_presence_subset.py`: 保存済みGhidra 0x4E7ED0の2分岐（方向セル1件／周辺探索）、signed座標÷32、4つの候補フラグ、厳密な距離比較、source scan+32を独立して部分再現。方向表・距離演算・全cell walk未実装。
- `missile_latch_subset.py`: 保存native 0x54714E..0x5471A6の+0x1E560 cache0/1/2、空間判定callの有無、MP減算前の早期retを局所契約化。
- `event_view_branch.py`: Ghidra 0x4321B0のspecial battle入口とgeneral event view選択（3つの0x40B200 callsite、54/55 flag、44/48参照先の3通り）を純粋テスト化。event履歴の永続化は未確定。
- `eb40_caller_contract.py`: 保存nativeの0x57EB40呼出元2種類（0x57E5D3: mode0でALにより自然回復へ; 0x4B61AD: mode1の反復でAL非参照）をcaller-only trace。callee内部は未解析。
- `negative_heal_flow_subset.py`: 負値heal/status coreの発動chance（1回/コア）、抵抗r²成功で全候補中断／dext差<=10で次候補skip、直接CRT rand消費1/3、11個damage_consti overrideを証拠限定の合成モデルで再現。x87数値・実stat mutationは未実装。
- `typed_damage_fragments.py`: Ghidra疑似コードで省略された0x550D80の5攻撃式、0x550E70の防御+0x9C/+0xA4とmode3 signed32平均、**mode6の100×scale+0.5固定ダメージ式**、0x5D1B80非default CVTTSD2SI局所を型付き数学モデルで復元。x87 default roundingのsaved 0x5D1BB6..DD前半は別メモで保存、末尾未取得のため未解析。
- `damage_two_draws_subset.py`: 0x550E70の攻撃・防御別rand15×2、attackBase/耐性係数/各native conversion callback、32bit差分とmode6時のextra converter＋固定値上書きまで追跡。距離・HP・native正規x87丸めは未実装。
- `damage_final_branch_subset.py`: r10 damage-virtual迂回、scale0引数0、mode6最低値補正迂回、r0の1000000、通常のmin clampとUnit flagを限定モデル化。virtual実作用なし。
- `damage_distance_gate_subset.py`: native 0x55103D..0x5510D7のSkill+0x250=0 skip、sqrt距離による0..1倍率clamp、damage×倍率+0.5を**厳密な整数平方根のケースに限定**して検証。非平方距離のx87計算と正常native丸めはfail-closed。
- `damage_status_dispatch_subset.py`: 0x550E70末尾の補助callee→Unit8D早期return、状態異常source存在→chance1 draw→contextD、Skill14C mapping/234 copy-all/1件selectorの処理順を独立trace。未解析builder・x87丸めは注入/未実装。
- `damage_status_candidate_subset.py`: 28byte属性候補ごとのr² gateは**その候補だけskip**（負healとは異なる）。通過時2 rand/dext差>10で0x578B70要請、局所damage強度=max(10,raw)。native mutationは未実装。
- `hit_linked_award_subset.py`: 0x551E50のcontext+0xC一度きり、ratio／skill別上限、Unit+0x1C8のlinked値+0x16C更新とunsigned thresholdまで。level helper/UI実効果なし。
- `native_stream_strings.py`: 保存Ghidra 0x470830の文字列全体検査。無効byteならNULのみ、0x7Fは許可。`save_envelope.py`のDEL過剰拒否を訂正。
- `unit_runtime_prefix.py`: 0x58EFD0 writer/0x58E870 reader双方で確認したUnit先頭の文字列5・raw dword10・flags7+1・4string vectorと+E4/+E8挿入の限定byte codec。後半は未対応。
- `spot_runtime_writer_fragment.py`: Spot 0x598CE0 writerの名前tree→capacity/castlebattle/fightvalue/dunname tagged sectionを純粋合成モデル化。native reader未検証。
- `power_runtime_writer_tail.py`: Power 0x596AA0 writerのfixtype/train_max/train_up/base_level/home_spot vectorとempty sentinel 2回を純粋合成モデル化。native reader未検証。
- `script_body_audit.py`: 原作3ファイル16宣言サンプルで2,896文を分類、opaque26・parser error0。全文法PASSではない。
- `event_ast_corpus_audit.py`: 590 DAT全ファイルからevent最大2＋scenario最大1宣言/ファイルを抽出し、516本文・recognized71,346/opaque172の原文span一致を独立検証。全30,695宣言の完全ASTではない。
- `save_probe.py`: ユーザーが提供したsavのヘッダーとglobal全records/通常save先頭numeric groupを読み取り専用で診断。未知のUnit以下は解析完了としない。
- `generic_property_audit.py`: 元590 DAT中のscenario9宣言、single-line map代入1件を静的走査、エラー0。
- `saved_ghidra_sourcebook.py`: Ghidraの以前の保存成果14runでVERIFIED37件と初期`rea_lab/results`の5点検証済2件をSHA/証拠IDで照合し、`recovered_source/ghidra_c_pseudocode`に合計39関数のC風疑似コードを分割。コンパイル可能な元C++復元ではない。
- `package_source_snapshot.py`: 39疑似C＋本ラボの実行可能Python互換実装＋専用テスト/索引を2026-10-11版ローカルZIPに収録。並列AIは`docs/PARALLEL_AI_SCRIPT_ASSISTANT_20261011.md`に従い、既存フォルダ内の担当ID付き新規ファイルだけ書込。前回10日版ZIPはそのまま保管。原本EXE・ゲーム画像/音楽/シナリオ/実saveは含めない。C/C++のビルド/旧EXE goldenは未確認。
- `tests/`: 合計254件合格（2026-10-11・静的/合成/保存済みGhidra証拠検証テスト）。旧EXE実機golden PASSとは別集計。`reports/`: 原データ照合を再実行できる結果JSON。

**これらは静的形式/契約の検証結果です。本家ゲームの実行golden PASSではなく、現時点でプレイ可能なエンジンでもありません。**

## Windowsでの実行

PowerShellでこのフォルダへ移動し、以下を実行します。

```powershell
.\run_checks.ps1
```

`.ps1`がブロックされた場合もWindows全体の実行ポリシーは変更せず、次のコマンドを個別に実行します。

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
python -m unittest discover -s tests -p 'test_*.py' -v
python -m hakushin_compat.audit
python -m hakushin_compat.context_audit
python -m hakushin_compat.script_source_audit
python -m hakushin_compat.parent_graph_audit
python -m hakushin_compat.scenario_audit
python -m hakushin_compat.generic_property_audit
python -m hakushin_compat.script_body_audit
python -m hakushin_compat.event_ast_corpus_audit
python -m hakushin_compat.scene_cli 1v1rts1.map
python -m hakushin_compat.scene_cli 2v2rts1.map
python -m hakushin_compat.headless_clock_scene 1v1rts1.map --ticks 20
python -m hakushin_compat.headless_clock_scene 2v2rts1.map --ticks 20
python -m hakushin_compat.synthetic_vm_scene 1v1rts1.map --ticks 31
python -m hakushin_compat.synthetic_vm_scene 2v2rts1.map --ticks 31
python -m hakushin_compat.synthetic_invocation_scene 1v1rts1.map --ticks 8
python -m hakushin_compat.synthetic_invocation_scene 2v2rts1.map --ticks 8
python -m hakushin_compat.synthetic_ai_scene 1v1rts1.map --ticks 120
python -m hakushin_compat.synthetic_ai_scene 2v2rts1.map --ticks 120
# 保存済みGhidra証拠を再検証して39関数のC風疑似コードへ整理（元EXEやGhidraは実行しない）
python -m hakushin_compat.saved_ghidra_sourcebook
# すでに生成した疑似Cと実行可能Python部分をローカルZIPとして保存
python -m hakushin_compat.package_source_snapshot
```

テストレポートは `reports/` 内へ新しい名前で保存し、既存結果を上書きしません。

## 解析正本との関係

- 読取元: `../data/source_snapshot/hakushin067_core/`（元ZIPではなく読み取り専用snapshot）。
- 根拠: `../evidence/T007_MAP_ROUNDTRIP.json`、`T008_IMAGE_FORMAT.json`、`T009_CONTEXT_INVENTORY.json`。
- 仕様: `../data/T005_FORMAL_GRAMMAR.md`、`T007_MAP_FORMAT.md`、`T008_IMAGE_FORMAT.md`、`T009_CONTEXT_MODEL.md`、`T031_RANDOM_EVENT_SCHEDULER.md`。
- 動的テストの正本: `../tests/T018_GOLDEN_CORPUS.md`。Eレーンのみ編集します。
- REA/Ghidraの独立証拠: `../rea_lab/results/`。推定した型/関数名は製品へ自動適用しません。

## Strict互換を最優先

原作のバグ・初期値・乱数消費・イベント順序も必要に応じ再現します。新しい便利機能は別profileで明示的に有効化する設計とします。
未知の動作を推測で固定せず `VERIFY` として扱い、native static証拠と実ゲーム観測を区別します。
公開やライセンス決定は現段階の実装要件に含めません。

次の成果物・合格条件と優先順位は `docs/IMPLEMENTATION_PLAN.md` を参照。手作業は現在すべて保留とし、後日まとめる一覧は `docs/USER_MANUAL_TASKS_DEFERRED.md` を参照。セーブデータなしで原作の観測に協力する場合は`docs/MANUAL_OBSERVATION_WITHOUT_SAVE_20261010.md`を利用。原作の実機観測をユーザーにお願いする際は `docs/MANUAL_TARGET_OBSERVATION.md` と `docs/OBSERVATION_RECORD_TEMPLATE.md` を利用。
