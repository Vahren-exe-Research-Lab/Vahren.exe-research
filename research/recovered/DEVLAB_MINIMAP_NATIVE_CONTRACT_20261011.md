# DEV 独立解析：原作 MiniMapWnd の静的レンダリング・入力契約（2026-10-11）

## 選定・競合防止
- ユーザー要望は「他AIの調査と重複せず、原作画像を模写せず、解析証拠で再開発」。Desktop Commander Localで MASTER_LEDGER.md checkpoint83・5レーン規約・A/B/C/D handoff・DEV WBS/dirty Gitを参照。開始時 Local sessions0、process全体CPU情報n/a（PC低負荷と断定しない）。
- 別AIは Unit能力値 0x573BD0/0x58B7F0・Unit/Class親優先・Skill capability と terrain/movetype、BはT012/T013のdamage/AI、DはRTS・音声・入力を継続中。上記source、WBS、Git index、他レーンownerを一切編集しない。
- D/T015の旧資料には MiniMapWnd の erase/cleanup 登場が2か所確認されるが、MiniMapWnd 固有の背景色grid、入力、動的更新の根拠付きプロトコルは記録が薄い。**DEV専用の非重複な局所分析**として作業し、D公式T015のREADY/DONEは更新しない。
- 対象の一次静的証拠：**既存** `recovered_source/peer_script01_ghidra_named_decomp_20261011.zip`。Ghidra疑似Cであり原C++ソースでも正確なx86型・実引数ではない。旧Vahren.exe実行・新規Ghidra/REA・デバッガ起動0。原データ、実セーブ、公開Wiki画像はいずれも解析用改変なし。

## 保存済みGhidraで確認した静的call chain
1. **戦闘シーンsetup** `0x48D6A0` (`decomp_0048xxxx.c`) は `0x4F0BE0` を呼び（stage/map構築側）、その後 `0x4DD8C0` を呼ぶ。ゲーム描画の縮小コピーではなく別処理を呼ぶ構造を確認。2呼出の全副作用・到達条件はVERIFY。
2. **マップ読込/初期化** `0x4F0BE0` (`decomp_004Fxxxx.c`) は `0x4DCDC0` を呼ぶ分岐を含む。後者はMiniMapWnd相当のレイアウト・各描画バッファ、比率・初期化に関わるが、x87 operandはGhidraで消失した部分があり画面上の正確な矩形はまだ不明。
3. **MiniMapWnd::vf02** `0x4DE920` (`decomp_004Dxxxx.c`) は複数のstatic/dynamic vertex配列を組み立てて描画装置virtual methodへ渡す。頂点byte幅0x18のcopyが見え、2D色矩形だけで完結せず画像/mark layer候補を持つ。実UI draw order・render state・image identityはVERIFY。
4. **原座標・入力** `0x4DE410` は `PtInRect` でwindow+0x178の矩形に入力点があるか判定し、分岐後に `FUN_00520800` (viewport移動core) や `FUN_00528870` へ接続。`0x4DCB70/0x4DCCB0` はモード次第で `D3DXVec3TransformCoord` を使う。Ghidraが一部 `_ftol2_sse` の引数を落としており、ミニマップclick→カメラ座標は未確定で実装しない。
5. **drag reset** `MiniMapWnd::vf16` = `0x4DE690` は window+0x168 と +0x16C の2DWORDを **0x80000008** に設定して0を返す。+0x170のhover/press関連値とは同一視しない。

## 0x4DD8C0: カラーグリッドの独立描画
- `engine = *(DAT_0087F798+4)` 候補の `engine+0x1EF6B4` からvector-of-vector様のDWORD値グリッドを取り出し、外側が行、内側が列として周回。`pCVar6` を `SetDCBrushColor` に渡し、`FillRect` でセル色矩形を塗る。
- 配置画面の幅候補は `abs(DAT_0087F890 - DAT_0087F888)`、高さ候補は `abs(DAT_0087F894 - DAT_0087F88C)`。グリッドの列数、行数でそれぞれ割った値を `FUN_005B6ED0` (既存A/Claude側でceil確認)に渡し、`_ftol2_sse` 結果をセル幅/高さとしている。
- **未確定**：source map種別/色（terrain attribute, world state, diplomacy等）の実producer。色配列を単なるraw `.map`タグや元画面pixelの縮小から生成すると決めつけない。セル位置決定は `0x4DCCB0` の矩形変換にも依存するため、単純row*ceil/col*ceilが全モードの実画面位置一致とは断言しない。
- 単独のGhidra ZIP全文検索では `0x1ef6b4` リテラル参照がこの `0x4DD8C0` にのみ出現する。別の動的offset/プロキシを介した書込は有り得る。「producerなし」とは言わない。

## 0x4DE330: 動的overlayセル更新（局所確定）
- UI/window様entityの +0x2397C（横セル数）、+0x23980（縦セル数）、+0x23978（頂点pointer配列）、+0x23988（alpha byte）を使用。
- 入力座標は呼出元で既に変換され、x/yを **符号付き整数のゼロ方向除算8** (x86のsign bias算式) でgrid indexへ写して `0..dimension-1` にclamp。index = `column + columns*row`。
- `param3!=0` ならcolor DWORD **0**、そうでなければ `alpha_byte << 24` を、同一cellの2つのvertex色DWORDへ格納する。描画される結果色・alpha blend状態はこの部分では確定しない。
- 呼出元 `0x5B3F90` は領域処理、`Blind::vf01` = `0x5B4360` はtimer/cell-list付きの反対側更新として同helperを呼ぶ。FoW/探索/目隠しというゲーム上の意味は**現段階で仮説**、class名 Blindだけから確定しない。
- `0x4DD8C0` 自身にも overlay grid vertex作成分岐がある。この背景色/rasterと動的overlayを同一配列へ潰す設計は避ける。

## 安全なDEVローカル実装（他AIへ未接続）
- `src/hakushin_compat/native_minimap_static_subset.py`：カラーgridを**外部から提供された直接RGB COLORREF**として扱う。表示extent÷グリッド寸法のceil、行列保持、ローカル軸揃えの相対矩形、既に変換された座標の/8 clamp、0/alpha<<24の2頂点書込、drag reset sentinelの**限定算術**を関数化。
- **意図的な停止境界**：カラーパレット以外のCOLORREF種別、source grid producer、source map→色決定、D3DX/ftol後の絶対座標、実スクリーン描画、Fog状態、遊べるEXE本体への接続は実装しない。APIの `coordinate_transform_reconstructed=False` と `fog_or_visibility_gameplay_meaning_verified=False` を維持。
- `tests/test_native_minimap_static_subset.py` では不均一な画面サイズ（ceilでセル端が画面範囲を超えることも保持）、COLORREFのBGR変換、負のspan、/8端点、配列衝突/不正形式拒否、保存Ghidra C内の原VA命令文字列を検査。実ゲームでのminimap動作goldenテストとは区別。
- 新しいファイルはdev_lab既存`src`/`tests`/`docs`のみ（新フォルダ0）。既存のbattle_window/playtest_game、Claude peer_script01、5レーンdata/exe/MASTER、Git indexは変更せず。

## 次に限定して調べるべき点（他AIと調整）
1. **色グリッドproducer**：map初期化 0x4F0BE0 側の engine+0x1EF6B4 所有者、spot/field/raw paletteとの接続をnative writer+calleeの局所証拠から確認。これはD/T015へリンクする依頼候補であり他レーン資料は編集不可。
2. **入力変換のx87 operand**：0x4DE410→0x4DCB70→0x520800 callでscreen/minimap/world座標を一次x86で固定できるまで、クリック移動のstrict版は保留。
3. **動的unit表示**：0x4DDE70/0x4DE0D0が別描画vertexへ入れる対象class、flagによる色差、Blind更新ループの実効visibilityを追跡。一般ゲームのfog知識だけから命名しない。
4. **E/T018合法UIのgolden**：ミニマップ上をclick/dragしてカメラがどの位置へ移動するか、固定景観/水域/味方/敵/未探索で色がどう変わるかを原作実機で独立観測。旧gameplay actual Golden0、新strict MATCH0維持。

## 完了判定
これは DEV BF-05/BT-09/QA-01 に貢献する**保存native由来の局所API研究**。MiniMapWnd全体・戦闘UI・ゲーム機能自体は未完成。研究A〜E公式DONE/READYは変更しない。テスト成功もSTATIC/MODEL_TESTED以上へ格上げしない。

## 実行・証拠の最終結果
- `python -m unittest discover -s tests -p test_native_minimap_static_subset.py -v`: **16 / 16 PASS**, `MINIMAP_NATIVE_FINAL_EXIT=0`。内訳：色grid/ceil・矩形順序・8pixel alpha-grid・Win32 BGR・sentinel・不正index/不正palette拒否・保存Ghidra関数文字列照合。
- 保存Ghidra ZIP SHA256：`c167dc8b09e8cae6abaa14e23bac94e675585ae432595a1608fdbc1cc8249b9a`。12関数のローカル疑似C SHA256とクロスcall照合結果は `reports/MINIMAP_NATIVE_STATIC_AUDIT_20261011.json` に記録。
- `git diff --check` exit0。別AIのdirty変更には触れず、この調査で新規追加したのは上記native_minimap静的モデル・専用テスト・本書・監査JSONのみ。PCのWindows旧/新ゲームEXEは起動せず、新デコンパイラ/REA/Java process起動なし。
- **判定**：色グリッドの producer、座標変換、Unitマーカーの描画元は未解明。したがって元ゲーム描画の完成 / UI実機成功 / 原作ゴールデン合格への昇格0。今回の16件はあくまで静的仮想関数のbounded MODEL_TESTED。
 

## 継続解析：0x4DD8C0 動的メッシュの生成分岐と色grid producer探索（2026-10-11）

### 保存済み疑似Cの広域直接参照を追加監査
- 対象は既存 `recovered_source/peer_script01_ghidra_named_decomp_20261011.zip` の48 ZIP entry中、全35 `.c` group。文字列 `0x1ef6b4` は **1件**、`0x4DD8C0` reader側のみ。`0x4F0BE0` stage loaderにもこのliteralは出現しない。`exe/` の保存済み `.txt` 338件・計約12.2 MiBを照合しても、当該 literal/0x87F798/0x4DD8C0 の直接一致は0だった。
- **これは「原作にwriterがない」という証明ではない**。間接ポインタ・別名の構造参照・暗黙caller・抽出対象外のnative instruction・decompilerが失ったEAX/ESIの副作用によるwriter経路が残る。今後はproducerを見つけるまで地形tag→COLORREFの生成規則を実装しない。
- 同ZIPの `0x1eeee0` 直接参照は **2件**：`0x4DD8C0` と `0x407300`（別のcharacter/stats表示系）。`0x1eee4c` は `0x4DD8C0` の1件で、そこからengine内subobjectのアドレスが`DAT_008A3070`にセットされる。これらのフィールドの**論理名・副作用は未確定**。
- `0x48D6A0` battle/stage setupは`0x4F0BE0` stage readerの後に`0x4DD8C0`を呼ぶ保存静的順序。だが前者が直接engine+0x1EF6B4を生成するわけではなく、各calleeのポインタ引数/副作用はVERIFY。原作の通常battleだけでなく他scene modeのcall順も要確認。

### 動的メッシュの限定トポロジー（SAVED-GHIDRA-STATIC）
- `0x4DD8C0` 内の追加条件は `*(engine+0x1EEEE0) != 0`。偽の場合は**この関数のメッシュ新規生成分岐をskip**。既存の別オーナーにあるoverlayを削除/消去したとまで断定しない。
- 陽性分岐で、源color gridの行数を`H`、1行目のDWORD要素数を`W`としたとき、grid列`C = floor(W/8)+1`、行`R = floor(H/8)+1`、レコード数`2*C*R`が`DAT_008A307C`／`+80`／`+84`へ入る。単純な`ceil(W/8)`では**W=8や16ちょうどの端点を誤る**。
- 2個の頂点レコードを1組として、各レコードは`0x18=24`bytes。行`r`と列`c`の最初のvertex slotは、偶数行`2*(C*r+c)`、奇数行`2*(C*r+(C−1−c))`。次のslotが`+1`。これは保存疑似Cの`uStack_28=uVar5&1`と奇数行の`iStack_30*-2-2+piStack_24`から限定導出。**GPUのprimitive方式・render order・画面座標・fog視認効果までは未復元**。
- `DAT_008A3070`は`engine+0x1EEE4C`へのポインタ候補。実world/terrain/visibility samplerとは未同定。
- 実マップの110×110とは独立に、**もしCOLORREF入力グリッドが110×110なら**C=14,R=14,レコード数392という合成例。現行`DirectRgbColorGrid`は自前の規格外/不正値を安全に拒否するが、原作EXEの不正入出力動作を再現したわけではない。

### 独立コード・テストと残件
- ChatGPT所有の既存`native_minimap_static_subset.py`末尾へ`NativeOverlayMeshTopology`、`native_overlay_mesh_topology_from_grid_shape`、`native_overlay_vertex_slot_pair`を追加（既存試遊EXE/本番rendererへは未接続）。
- 専用`test_native_minimap_static_subset.py`へ9件追加：8境界/サイズ、行交互reverse、disabled flag、型・範囲・layout偽装拒否、原Ghidra substrings、ZIP全体直接xref件数。**25/25 PASS**（旧16＋新9、exit0）。
- 元バイナリのEXE起動・新Ghidra/REA・git stage/commit/push・原作データ変更なし。STATICと合成MODEL_TESTEDであり、原作実機Gameplay Golden0／strict MATCH0のまま。
- **NEXT**：①`0x4F0BE0` caller/calleeのpointer aliasを保存済み逆コンパイルで辿り、`engine+0x1EF6B4` producerを探す ②flag`+0x1EEEE0` writer/初期状態を別保存命令で調査 ③`engine+0x1EEE4C` subobjectと`0x5B3F90`/Blind::vf01の関係を確認 ④限定実機Goldenを得るまで初期地形色/霧を固定しない。正式D/T015やMASTERは他AI ownerに照合を依頼するだけで変更しない。
