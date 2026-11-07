# 迫真戦記 ver0.67 原作セーブ完全バイト再構築 — DEVLAB独立成果（2026-10-11）

## 正しさの範囲・作業制約

- 対象はユーザーが作成した原作save1.sav、auto.sav、save2.sav。これらのEXEと元データは編集しない。解析コピーをdev_lab/_workにSHA256一致で保全済み。
- この報告での「完全」は原作セーブ3件の**全構成フィールドと全オブジェクトを独立デコード→再シリアライズ→元保存鍵で再暗号化してバイト完全一致**した意味。旧ゲームの実機LOAD成功、メモリオブジェクト生成、イベント・AI・UI・戦闘の1対1互換は証明しない。
- 原作EXEの新規実行、Ghidra/REAの新解析起動なし。以前の安全拒否操作を別経路で迂回せず、Local Compact以外のPC接続ツールやRemoteを使わず。Git/公開/他AI所有コード/原本への書込なし。
- 研究正本MASTER_LEDGER.mdを読んだ時点でcheckpoint83、190正式研究ID、DONE9/34。DEV成果を公式READY/DONEや旧ゲームGolden PASSへ加算しない。研究A/T014・B/T012・E/T018の所有ファイルは触らない。

## 実セーブの修正済み基本構造

- 3件すべて envelope先頭32bytes（4byte魔法値・28byte鍵）の暗号化＋原作と等しい復号平文を取得。
- 元の数値群は空文字ではなく文字列 ---------- とNUL終端（計11byte）が区切り。numeric/Unit/Spot/Powerの各mapが同じ区切りで終了する。
- 過去の ACTUAL_SAVE_BYTE_GOLDEN_20261011.json の numeric 1960/2593 は**誤集計**。そのレポートを監査履歴として残し、ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json に訂正を保存。
- 訂正したnumeric save1 1958レコード、auto/save2 2591レコード、後者ユニークキー2587。同名キーで異なるauxの4件追加重複あり。キーのみの追加629と (key,aux)の追加633は指標の違い。
- RAM上は1byteのUnit+0x74..0x7A/+0xE8、Power+0x1C/+0x1D、Diplomacy+0x09/+0x0A、graph各Spot/Path+0x88は、保存時には0x4708A0で各4byteゼロ拡張のuint32LEになる。以前の単純packed-byteモデルは原作実saveには不適。
- save1 = 4,660,064 encoded bytes、auto/save2各5,558,753 encoded bytes。autoとsave2は暗号文が異なるが復号平文5,558,721bytesでSHA256一致。

## 解析済みレコードと一致実績

| 構成 | save1 | auto/save2 | 原作に対応する保存ルーチン |
|---|---:|---:|---|
| numeric | 1,958 | 2,591 | 0x460000 |
| Unit | 7,355 | 8,763 | 0x58EFD0 |
| Spot | 138 | 138 | 0x598CE0 |
| Power | 29 | 29 | 0x596AA0 |
| Diplomacy | 29件のPower参照 | 同左 | 0x471D20 |
| graph SpotElm | 121 | 121 | 0x435C10 / 0x5A93F0 |
| graph SpotPath | 160 | 160 | 0x435C10 / 0x5B0600 |
| graph SpotEscapePath | 11 | 11 | 0x435C10 / 0x5B0600 |

- Unit合計24,881実レコード（7,355+8,763+8,763）、Spot414、Power87、graph876は全件decode→packバイト完全一致。各外交セクション153byte、各graph9,656byteも完全一致。
- dev_lab/src/hakushin_compat/normal_save_complete_wire.py は旧unparsed_suffixを採用せず、header/numeric/全Unit/全Spot/全Power/Diplomacy/graphを新規に組み立てる。元28byte鍵を適用して3原本の全暗号化bytesが一致。synthetic変更入力が別暗号文になるテストを含む。
- 別経路の既存 normal_save_all_wire.py も3件全暗号文の一致を確認、専用6テストPASS。両者は下位レコードパーサを一部共有するため完全に独立した実装ではない。


## マップのオブジェクト照合と安全な限界

- 原作セーブのSpot138種類に対して、graph SpotElm121、通常経路160、特殊経路11の両端参照を照合。未解決の端点0、重複した同向・同種route0、自己参照ルート0。
- 方向未確定のため、構造調査用にのみ無向投影を作ると大きさ109の連結成分が1つ、孤立29地点がある。原作の実際の方向制約・通行許可・経路探索アルゴリズムはVERIFY。
- reports/WORLD_GRAPH_REFERENCE_CROSSWALK_20261011.json に保存名・keyとendpoint・raw flags・仮隣接表を記録。これを原作動的移動仕様と混同しない。

## ターン1→2の構造差分

- reports/NATIVE_SAVE_TURN1_TO_TURN2_DIFF_20261011.json に実save1→save2のfield単位差分を保存。
- numeric composite key=(key,aux) の追加633・削除0・変更67。キーのみで比較したときの追加629との差は4件の別aux項目。
- Unit名追加1412・削除4・共通名の内容変更1362。Unit総数7355→8763。書込slot+0xBCは共通名1353個で値が変化し、tail+0x168/0x16C等は1116個だが、ゲーム内HPや毒や経験値の作用とは未対応。
- Spot総数138維持、うち40個が書込tree_key_namesフィールド変化。Power総数29維持、29個のdword+0x5Cフィールドが変化。変数の人間向け意味はまだ確定させない。
- 外交の未ラベルu32+0x14が0→1。world graph全9,656byteは一致。これらは保存状態の観測であり、その変化を生じさせたイベントはまだ未証明。

## 同時実装した戦闘処理・評価

- main_decomp_status_special_subset.py は保存0x578B70のsuck/magsuck/drain/death 4種のローカル更新を実装。31/31 dedicated Python unit tests PASS。deathの仮想関数や未知乱数処理は明示barrier。
- main_decomp_prestatus_counter.py は0x576F10のUnit+0x185F8のu32周期カウンタを実装。9/9 PASS。0x4DFBB0以降の可視エフェクト/状態変化は未実装。
- 新規・訂正した原セーブ単体テスト群：test_real_save_frontmatter 13/13、test_real_save_section_index 6/6、test_unit_native_wire_prefix 10/10、test_unit_native_full_wire 15/15、test_spot_power_native_full_wire 16/16、test_normal_save_native_sections 13/13、test_world_graph_native_wire 10/10、test_world_graph_reference_index 7/7、test_normal_save_complete_wire 10/10、test_normal_save_all_wire 6/6、test_native_save_state_delta 6/6。すべて対象ファイルを別々に実行しPASS。
- 上記は**今回の保存形式を含む局所試験**。run_checks.ps1全体回帰の新規PASSは宣言しない。以前のPEER script corpusの長時間テストは別問題として負荷/担当の修正を要する。

## 次にすべき具体的タスク

1. 旧reader 0x45E1E0→Unit 0x58E870/Spot 0x598980/Power 0x5964C0/Diplomacy 0x471AF0/world graph 0x435550 の保存済み命令・疑似Cから、**ロード時の参照名→メモリポインタ復元、constructorと例外処理、オブジェクト割当順**を別ファイルで再構築する。byte-exact保存とは別課題。
2. RTS・戦略のシーン上で、原作から得たSpot/Power/Unit/Routeを新ゲームstateへ読み込み、世界マップ描画/入力/ターン/イベント/AIの互換処理を独立検証する。無向隣接の仮投影から実際の移動アルゴリズムを作らない。
3. T012 ownerへ戦闘status特殊効果と0x4DFD80/0x4E13F0の副作用・RNG・仮想死亡callbackの証拠を引き継ぐ。新ゲームstateへの本統合は個別testと差分比較の後。
4. T018 ownerへ旧実機UIで観測可能なターン2の資金・勢力・拠点・Unitと保存slotが対応するgoldenを提案。内部フィールドだけの比較はBYTE証拠、旧ゲーム実機の動作PASSとは別扱い。
5. 完成判定は「原作と同じ画面・音・戦闘・AI・イベント・セーブロードを再実装し、合法実機入力に対して厳密同一結果を検証」するまで留保。C++原文復旧やGhidra pseudo 10,257関数の取得だけで完成と扱わない。


## 追加進捗：旧readerの読込順と新エンジン用IDレジストリ

- 保存済Ghidra 0x45E1E0の疑似Cを再読。実体の正常 .sav loadではUnit準備0x582AA0→Power準備0x5971A0→Spot準備0x590560→0x470550 preamble→numeric→Unit(0x58E870)→Spot(0x598980)→Power(0x5964C0)→Diplomacy(0x471AF0)→WorldGraph(0x435550)→cleanupと呼ぶ。関数に付いた Save_GlobalEnvelope という自動名は特定の global.sav だけを意味しない。
- src/hakushin_compat/normal_save_runtime_registry.py を追加。実saveから作成した型付きレコードを名前で参照できる構造へ投影し、Unit/Spot/Power各一意ID、数値変数の(key,aux)多重値、外交Power名、SpotElm名、通常・特殊経路の両端参照を検証。read-only mappingで個別オブジェクトを取得するための準備を完了。
- save1実データではUnit7355・Spot138・Power29・外交Power名29・graph SpotElm121・Path160・Escape11の全参照が解決。activePower=po2、scenario=sci1。new-game runtime loaderがnative constructorやC++メモリpointerを再現したとは主張しない。
- 直接保存されたorigin/destinationの順序と、無向グラフ投影は別物。sp1の元path origin側ではsp18/sp67のみだが、無向グラフには逆順でsp68bとのリンクもある。原作の一方通行性は未確定。
- tests/test_normal_save_runtime_registry.py：8/8 PASS。初回のテストでは無向投影を直接端点順序と取り違えたため期待値を訂正後に再実施し8/8 PASS。元native画面からの可視Golden0、ゲームengine LOAD side-effectの検証0。
- 原既存セーブhelper群の回帰も test_save_envelope/test_save_probe/test_unit_runtime_prefix/test_spot_runtime_writer_fragment/test_power_runtime_writer_tail/test_native_stream_strings の25/25 PASS（今回）。
- NEXT: 名前で照合したIDレジストリを、実runtime entity生成/所有関係と結び付けるためUnit/Spot/Power constructorと0x435550によるreference resolutionをさらに調査。scoped native実行結果なくルート方向や移動コストを推定しない。

