# 元EXEをソースへ戻すための現実的な設計図

**方針**：まず原作ver0.67のstrict互換の挙動とデータ構造を取り戻し、画面・入力・音声をあとから接続する。enhancedモードはstrict完成後に分離する。

## いま手元にある2種類のソース

1. **Ghidra疑似C：39関数** `ghidra_c_pseudocode/FUN_XXXXXXXX.c`。証拠5点と実行前後同一ハッシュを確認して保存したC風の中間表現。変数名/型/グローバル名はGhidraによる推定で、元作者のソースではなく、単体ではコンパイル不可。
2. **実行可能な互換試作ソース：Python** `../src/hakushin_compat/*.py` と `../tests/test_*.py`。こちらは当プロジェクトが新規に書いた再開発コード。map・image・context・脚本AST・戦闘時刻・イベントVM・状態異常・保存形式を部分的に実装。ただし全ゲームはプレイできない。

原EXEの元ソース全体に変換するボタンや、自動修正だけで動く段階ではない。実装済みの各コードは固有の機能*断片*であり、元関数全体の置換/完全互換を主張しない。

## Ghidra関数→再開発コードへの対応（限定）

| 関数 | 既存Pythonの該当処理 | 状態／残る作業 |
|---|---|---|
| `0x5B6E99` / `0x5B6EAB` | `legacy_rng.py` | MSVC seed・rand15の数値モデル。実ゲームのseedタイミングは別途VERIFY |
| `0x40ED80` | `legacy_rng.py` | 限定した乱数範囲処理。Ghidraのx87丸めと整数化helperは完全未保証 |
| `0x479A30` | `native_vector_shuffle_subset.py` | 28byte stride/24byte swap・乱数拡張の物理モデル。残り4byteは未同定 |
| `0x470830` | `native_stream_strings.py` | byte 0x20..0x7Fの全件検査・不適格ならNULのみ |
| `0x57DF90` | `status_recovery_subset.py` | HP/MP/7 gauge更新の純粋算術モデル。death side effect/呼出timing未知 |
| `0x576E30` | `negative_heal_flow_subset.py` | 5既定値、0..10 clampの抵抗値取出し断片。関数ABIや全callsite未実装 |
| `0x551490` | `negative_heal_flow_subset.py` | 負amount向けchance/r²/dext 2段階gate・RNG直接draw。本体のstat変更/全属性未実装 |
| `0x546F70` | `missile_latch_subset.py` | 中間+latch=0/1/2、空間判定、MP debit前早期return。技能実行全体は未実装 |
| `0x4E7ED0` | `spatial_presence_subset.py` | 単一方向セルと周辺探索のfilterだけ。実方向テーブル/trig/candidate全走査未実装 |
| `0x57B870` | `search_cadence.py`, `confusion_refresh_subset.py` | timer/cached target・3種のdirect rand。完全AI動作は未実装 |
| `0x4321B0` | `event_view_branch.py`, `event_vm_subset.py` | 参照先の条件分岐・合成event呼出。yet保存履歴と実callstackは未実装 |
| `0x505210`, `0x504400`, `0x463280` | `generic_properties.py`, `declaration_ast.py` | generic field先勝ち・宣言syntax subset。special callback登録と完全読み込み未実装 |
| `0x4693F0`, `0x464290`, `0x4647D0`, `0x465060` | `generic_properties.py` | qualified→base→parent・明示@停止の限定モデル。50回guardと複雑な継承実ケースは要再検証 |
| `0x58EFD0`, `0x58E870` | `unit_runtime_prefix.py` | Unit直列化の先頭部分のみ。tree/後半/全ロードは未実装 |
| `0x45E1E0`, `0x460000` | `save_envelope.py`, `save_probe.py` | global・通常save先頭のlimited corpus probe。全群の保存復元は未実装 |
| `0x550D80` | `typed_damage_fragments.py` | 技能モード1〜5のstat混合式とmode外0、x87 converter前の数学値を明示。native default丸めはVERIFY |
| `0x550E70` | `typed_damage_fragments.py`, `damage_two_draws_subset.py`, `damage_distance_gate_subset.py`, `damage_final_branch_subset.py`, `damage_status_dispatch_subset.py`, `damage_status_candidate_subset.py` | 防御+0x9C/+0xA4、独立2 rand、mode6の100×scale+0.5、完全平方根距離0..1倍率、r10/scale0/mode6/r0/min、後段状態異常のsource/chance/候補ごとの抵抗r²＋独立2 randを局所復元。x87/HP virtual/0x578B70実副作用は未完 |
| `0x5D1B80` | `typed_damage_fragments.py` | global非zero時のCVTTSD2SI局所のみ検証済み。global0側の0x5D1BB6以降FISTP/FILD/補正分岐前半は既存`exe/T010_RUNTIME_PROBE.txt`で確認。後段不足のためnative通常丸めは未確定 |
| `0x551E50` | `hit_linked_award_subset.py` | hit context一回flag、linked+0x16C更新、ratio/skill固定倍率、unsigned thresholdをvirtual level helper前まで分離。経験値の実効果・level-upは未検証 |

今回のdamage/hit関連Pythonモジュールは**数学的な演算式と分岐順を型付きで記述した部分的な再実装**であり、x87の80-bit中間丸め、別関数の副作用、全ゲームとの同seed実測結果は未実装。関連する一次命令・VERIFYは`../../rea_lab/decomp_task/SOURCE_RECOVERY_TYPED_DAMAGE_20261011.md`を参照。

一覧にないGhidra関数についてもC風疑似コードは出力済みだが、**全機能の移植は済んでいない**。特に関数の識別子`FUN_...`を実際のAPI名に読み替えるにはstack/register引数とcallerを交差検証する。

## 完成へ向けた必須の段階

### 第1段階：非描画ヘッドレスコア

- スクリプト全宣言の読み込み・継承/派生解決・特殊parser・有効シナリオ実体化。
- ターン・イベント・戦闘tick・制限時間・VM stack/call/return・RNG draw順の整合。
- Unit/Skill/Power/Spotの実際の更新および演算、Unit生成・削除・AI選択・移動・命中・死亡・士気を再現。
- Unit/Spot/Powerの全save/loadと異常入力時のfail-closed動作を解明。

### 第2段階：原作観測（セーブファイルはユーザーが共有できるまで保留）

- ユーザーが通常操作で得た画面、戦闘数値、同seedの保存/ロード結果をgoldenの対象にする。
- T018レーンが観測条件・関数単位の期待値を独立採取し、strict再実装に差分テストを行う。
- **現時点では原作実機TARGET OBSERVED=0、新エンジンstrict MATCH=0。** Pythonテストの件数をそのまま互換性に換算しない。

### 第3段階：UI・描画・操作・音声の移植

- 解像度、UI入力タイミング、マップ層、アニメーション、BGM/SE、未使用assetの参照規則などを必要に応じて分離。
- strict完成後、音量0ループや高解像度UIなどの独立したenhanced改良モードを検討。

## 開発プロセスで避けること

- 元作者が持っていた変数名・コメント・元C++ファイル階層を『完全復元できた』と表現しない。
- Ghidra疑似コードの`undefined4`/register引数の意味を推測で固定しない。x87/FPUはアセンブリ側を優先。
- 保存済み断片の意味を新たなGhidra実行成功と混同しない。既往の安全拒否操作を迂回しない。
- 原本/他レーン研究/MASTER/T018や定期タスクの書込には手を出さない。
