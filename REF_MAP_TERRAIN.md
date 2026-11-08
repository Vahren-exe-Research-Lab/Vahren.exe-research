# 戦闘マップ：地形チップ・オブジェクト・通行判定・移動速度（MAP-T001）

対象: ver0.67 Vahren.exe SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（ImageBase 0x400000、VAはそのまま）。
研究ID: `CLAUDE-MAP-T001-20261109`。担当: Claude（2026-11-09）。
確度の書き方: **静的確認**＝原EXEの命令列で確認／**推定**＝静的根拠はあるが実機未確認／**未確認**。実機確認: V1（チップ見た目の書換え）・V2（地形値と移動）を 2026-11-09 に実施。
実装・設計・検証手順は製品リポジトリ `ButaMonky/Vahren.exe-MapGimmick`（Private）に置く。生の逆アセンブル出力はそちらの `research/raw/`。

## 0. 要点

1. 地形（field）とオブジェクト（object）の定義は **0x4EEA00** が全件パースし、マップ管理（`NewGameStage`、vtable 0x63A6EC）の **+0xFC（field）/ +0xEC（object）** の `std::map` に格納する。［静的確認］
2. 「通れない」は3系統ある。［静的確認］
   - **field の `type = coll / wall / wall2`** … そのマスを通行不可グリッドに1を立て、同じマスに見えない当たり判定オブジェクト（Block）を作る。
   - **object の `type = coll / wall / wall2`** … Block を作る。`type` 無指定（木など）と `floor` は**当たり判定なし**（見た目だけ）。
   - **object の `type = break / break2 / gate`** … 壊せる壁・門。通常の Block ではなく専用の生成経路（0x4F3290 経由）で作られる。
3. **移動の速さ・可否は movetype × 地形の attr**。ユニットの仮想関数 **Unit::vf25（0x576DC0）** が、いる座標のセルの `attr` 文字列でユニットの movetype 表を引き、`consti` の値を返す（無ければ既定 **5**）。`ship` の `grass*0` のように **0 のとき「その移動タイプでは進めない」** になる。［vf25 と消費側 0x57902C は静的確認。2026-11-09 V2 の既存結果により0で移動不可を確認、§3参照］
4. セル（`FieldData`、0x11C バイト）は描画オブジェクトで、テクスチャ座標（チップ画像の位置）を **+0x6C〜+0x80** に持つ。FieldData::vf07はセル値から頂点を作るが、**毎描画必ず呼ばれるとは限らない**。mode 1には描画コンテキストの地形頂点キャッシュ経路があり、画像変更の表示反映は再構築条件に依存する（§15）。この6値はアニメーション・途中変更の土台だが、書換えだけで次描画へ無条件に反映するとは一般化しない。［**実機確認 2026-11-09**: 戦闘中に x32dbg で 7×7 マスの +0x6C〜+0x80 を別セルの値に書き換えると、草原が水の絵に即座に変わった。attr・通行判定は変えず見た目だけ変わる］
5. 原作の DAT 命令にはマップチップを戦闘中に変える命令は**無い**（`changeMap` は世界画面の Spot が使うマップ名の変更）。途中変更・アニメーション・ダメージ床は DLL 拡張で作る。

## 1. 定義パーサー 0x4EEA00

`this`＝マップ管理（NewGameStage）。冒頭で `this+0xE8 = &g_GameManager(0x8BE2F0)`。field 定義の列挙は 0x4EE940、object 定義の列挙は 0x4EE8A0（いずれも Prop 表から種類名で列挙）。

### 1.1 object の属性とObjectDef（0x4EE470で構築、map: this+0xEC）

| 属性 | 意味・既定 | ObjectDef |
|---|---|---|
| `type` | 無指定=0、`floor`=1、`coll`=2、`wall`=3、`wall2`=4、`break`=5、`break2`=6、`gate`=6（break2 と同値）、`goal`=7、`start`=8、`box`=9 | +0x00 |
| `blk` | `on` で真 | +0x04（byte） |
| `width`/`w` | 幅 | +0x08 |
| `height`/`h` | 高さ | +0x0C |
| `alpha`/`a` | 既定 255 | +0x10 |
| `radius` | 既定 16 | +0x14 |
| `land_base` | `on`→0、数値ならその値、無指定→番兵 0x80000008 | +0x18 |
| `image` | 画像名 | +0x1C（std::string） |
| `member` | ランダム選択候補 | +0x38（vector<string>） |
| `no_stop` | 既定は `type != 6` のとき真。`off` で偽、`on` で真 | +0x48（byte） |
| `no_arc_hit` | `on` で真 | +0x49（byte） |
| `no_wall2` | 数値 | +0x4C |

文字列比較はすべて 0x4EF5E9〜0x4EF7EE（type）、0x4EF828（blk）、0x4EF8CE（land_base）、0x4EFA08/0x4EFAB0（no_stop）、0x4EFB58（no_arc_hit）、0x4EFBFB（no_wall2）。［静的確認］

### 1.2 field の属性とFieldDef（0x4EE560で構築、map: this+0xFC）

| 属性 | 意味・既定 | FieldDef |
|---|---|---|
| `type` | 無指定=0、`coll`=2、`wall`=3、`wall2`=4（object と同じ値） | +0x40 |
| `alt` / `alt_max` | 高さ（alt_max があれば alt〜alt_max の乱数） | +0x44 / +0x48 |
| `edge` | `on` で真 | +0x4C（byte） |
| `smooth` | 既定 on=1。`off`→0、`step`→0 かつ step=1 | +0x4D / +0x4E（byte） |
| `attr` | 地形属性（movetype の consti の鍵） | +0x50（std::string） |
| `id` | 無指定ならfield名 | +0x6C（std::string） |
| `joint` | 1件なら文字列 +0x88、複数なら木 +0xA8 | +0x88 / +0xA8 |
| `image` | 無指定ならfield名 | +0x00（std::string） |
| `member` | 上に置く object の候補 | +0x1C（vector） |
| `add2` | 画像の差分候補 | +0x2C（vector） |
| `color` | ミニマップ色（R,G,B を8bitずつ詰める） | +0x3C |

parent（`field a : b`）の継承は Prop 表の親探索（0x465060 等）で行われる。［静的確認］

## 2. マップ読み込み 0x4F0BE0 と実行時の層

`.map` の形式は既存 `T007_MAP_FORMAT`（1バイト幅・高さ、各セル `type,name,0xFE` の並び、0xFF でセル終端）。読み込み時:

- セル配列: `stage+0xA8`（FieldData×幅×高さ、各0x11C）、幅 `+0xAC`、高さ `+0xB0`。座標→セルは 0x4C1B70（ピクセル >>5、つまり **1マス32px**）、NewGameStage::vf02（vtable+8、斜め表示モード対応）。
- field エントリ（type0）: FieldDef を引き、0x4562D0 でセルに設定（下記）。`FieldDef.type != 0` なら 0x4DF200 で Block を作り `stage+0x148` の vector に追加し、**通行グリッド +0x60 と粗グリッド +0x7C に 1** を立てる（0x4F1A0B 付近）。`member` があれば乱数で object を追加生成。
- object エントリ（type1）: ObjectDef を引き、`type` 5/6 は専用経路、その他は 0x4DF200 で Block。
- type>=2 はユニット配置。

### 2.1 FieldData（セル、0x11C、vtable 0x638C54）

| オフセット | 内容 | 根拠 |
|---|---|---|
| +0x6C〜+0x80 | チップ画像のアトラス矩形6値（0x423E80 でチップ名から取得） | 0x4562E0〜0x456314 |
| +0x8C〜+0xA8 | 四隅の画面座標（NewGameStage::vf01 が設定） | FieldData::vf07 |
| +0xAC | byte（隠れ判定等で立つ） | NewGameStage::vf00 |
| +0xB0 / +0xB4 | セル x / y | 0x4F185C |
| +0xB8 | std::string（第1文字列引数） | 0x4562D0 |
| +0xD4 | std::string **attr** | 0x456328、Unit::vf25 |
| +0xF0 | std::string id | 0x456342 |
| +0x10C / +0x110 | 高さ（+0x10C は vf00 で平滑化後の値） | 0x4562D0、vf00 |
| +0x114 | smooth 区分（0/1/2） | 0x4F181B |
| +0x118 | step（byte） | 0x4562D0 |

FieldData::vf07（0x456380）は +0x6C〜+0x78 をUV、+0x8C〜+0xA8 を位置として6頂点（2三角形）を書く。NewGameStage::vf03（0x4FBF40）は表示矩形内のセルを列挙する（0x4C1BE0）。［静的確認］ただしmode 1の0x4C4420にはセル値から直接頂点を作って保存するキャッシュ経路もある。毎frameのvf07呼出保証ではない（§15）。

### 2.2 Block（地形・オブジェクトの当たり判定と表示、vtable 0x6392BC）

0x4DF200 が ObjectDef 相当から生成。`+0x5C` alpha、`+0x114/+0x118` 位置、`+0x11C` radius、`+0x120〜+0x12C` 当たり矩形、`+0x130` floor、`+0x134` land_base、`+0x138` no_wall2、`+0x13C` no_arc_hit、`+0xFC〜+0x110` UV。
type による旗: 1→`+0x130`、2→`+0x67`、3→`+0x67,+0x68`、4→`+0x67,+0x68,+0x69`。type0 は旗なし。画像の大きさが0で `+0x67` も無ければ生成を取りやめる。Block::vf20(1)＝no_arc_hit、vf20(それ以外)＝no_wall2。［静的確認］

**飛び道具との判定**（0x4E5860／0x4E6110、Missile::vf01・SimpleMissile::vf01 から呼ばれる）: `+0x68`（wall）が立つ Block は矩形内で飛び道具を止める。`+0x69`（wall2）の場合は、飛び道具側の条件が成り立つとき乱数と no_wall2 を比べ、乱数が no_wall2 以上なら止める（＝no_wall2 は**すり抜け確率**に相当）。［静的確認。乱数の範囲と飛び道具側条件の意味は未確認］

### 2.3 通行グリッド（`grid`）

`G = module + (0x8BE2F0 - 0x400000)` はGameManagerの実体アドレスであり、`[G]`はvtable。gridポインタは **`[G+0x90]`**（G+0x88に埋め込まれた小オブジェクトの+8）から読む。G自身を一度dereferenceしてから+0x90へ進むのは誤り。根拠は§16。

| オフセット | 内容 |
|---|---|
| +0x60 | 行ポインタ表（byte）。1=通れない |
| +0x64 | 行ポインタ表（int）。経路用の領域番号、初期値 0x80000008 |
| +0x68 | 行ポインタ表（pointer）。領域ノード |
| +0x6C / +0x70 | 幅 / 高さ（マス） |
| +0x74 / +0x78 / +0x7C | 粗グリッド（半分の解像度）の幅・高さ・行表 |

- 0x4E9470: 旧領域・grid行・経路cacheを解放して再確保する初期化。戦闘中に呼んで安全とは未証明（§16）。0x4E9A20: 1マスを通行不可にする（細・粗両方）。
- 0x4EA2E0 → 0x4E9A60: 通れるマスを長方形の領域に分け、経路探索のグラフを作る。引数は grid 1個（スタック渡し、呼出側 `push grid; call`）。読込関数内の呼出は 0x4F1439 と 0x4F320B の**2か所だが分岐の別経路で、1回の読込で呼ばれるのは1回**。［静的確認］
- **戦闘中の再構築（V3）の静的評価**: 0x4EA2E0 は新しい領域を作って通れるマスの `+0x64`（領域番号）と `+0x68`（領域ノード）を上書きするだけで、**前の領域ノードは解放しない**（一時木だけ解放）。この関数単独が旧nodeを解放しないという局所事実であり、再実行全体の安全性を保証しない。旧領域のリークを許容した製品設計にはできず、経路cacheの番号再利用による誤hitにも注意する（§16）。通行不可になったマスの `+0x64/+0x68` は古い値のまま残るため、新しい表は `+0x64=0x80000008`、`+0x68=0` から構築する必要がある。ただし旧+0x68はcleanupがnodeを収集する根拠でもあり、解放前にゼロ化すると旧nodeを追跡できなくなる。これらの値だけをリセットする手順を完成した再構築処理とは扱わない。経路キャッシュ（0x4EC1E0 側）が古い領域の組を保持し続ける可能性があり、塞いだ道を通ろうとする恐れは残る → 実機確認は DLL の段階 M6 で行う。［静的確認／実機未確認］
- 0x4EAA70: 2点間を8方向に歩いて通行不可マスに当たるか調べる（直進可否）。
- 0x4EC1E0: 経路照会（辞書の既存名 `RouteCache_ConditionalHitPromotion`、B レーン T028 の経路キャッシュと同一関数）。内部で 0x4EAC30（領域ノード +0x68 の参照）と 0x4EAA70 を呼ぶ。呼出元は Unit_ProcessKnockbackMotion（0x5769B0）と 0x5767B0（ユニット移動）。［静的確認］

## 3. 移動タイプと地形の速さ

- Unit::vf25（0x576DC0）: `Unit+0x1F0` と `UnitDef(+0x1C8)+0x14C` が有効なら、`Unit+0x1E4`（stage）の vf02 で現在座標（`Unit+0x214/+0x218`）のセルを取り、セル `+0xD4`（attr）でユニットの movetype 表（`Unit+0x1E8` 系の木、終端 `+0x1EC`）を探し、見つかれば値、無ければ **5** を返す。［静的確認］
- movetype.dat の `consti = attr*値` が値の出所（既存 DEVLAB_TERRAIN_MOVETYPE 参照。33種）。0 は消費側 0x57902C で移動せず false を返す。未記述は既定5（下記の既存V2結果・静的確認を参照）。
- vf25 の呼出元は 0x578FD0（移動1歩の計算、vtable+0x64 経由の CALL、戻り 0x579010）。［実機確認 2026-11-09: 呼出元は全件 0x579010、草=6・岩=3 を観測（normal の movetype どおり）］
  - 値 v が **0 なら移動せず false を返す**（0x57902C）。＝ consti 0 は「その移動タイプでは進めない」。［静的確認］
  - 速さ = clamp(v × 0.2 × `Unit+0xB0`（mov 系の値）×（`Unit+0x1E54C`>0 なら `Unit+0x1E550` 倍）× [0x65BD50]（既定1.0）, 50, 2000) × 0.01。v=5 で 1.0 倍。［静的確認、定数は .rdata 実値］
  - v≥8 で `Unit+0x1868C` を加算、v≤3 で0に戻す（地形による何らかの継続カウンタ。用途は未確認）。
- 実機の注意: この版は**斜め見下ろし表示**で動いており、ユニット座標（px）÷32 はマスに一致しない。座標→マスは必ず NewGameStage::vf02 を使う。

## 4. 原作でできること・できないこと

| 目的 | 原作の機能 | 備考 |
|---|---|---|
| 地形で移動不可 | field `type=coll/wall/wall2`、object `type=coll/wall/wall2` | 読み込み時に確定 |
| 移動タイプで不可・遅い | movetype の consti（0 や小さい値） | 例 ship は陸 0 |
| 壊せる壁・門 | object `type=break/break2/gate` | 専用経路。門は break2 と同値 |
| 飛び道具を止める | `wall`（必ず）、`wall2`（確率） | 2.2 |
| ダメージ床・毒床 | **無し** | DAT の `doskill(skill,x,y,向き,off)` を定期実行すれば代用可 |
| 戦闘中のチップ変更・アニメーション | **無し** | DLL で FieldData +0x6C〜+0x80 を書換え（既存V1で実機確認済み） |
| 季節でマップを変える | `changeMap`（Spot のマップ名、世界画面） | 戦闘用マップの差し替えは DAT だけで可能 |

## 5. 未確認（x32dbg 検証項目）

- ~~V1~~: **確認済み**（2026-11-09、OGGテストのコピー、スクリプト map_v1b.txt）。この試験条件では書換えの即時反映を観測した。「vf07が毎描画必ず呼ばれる」への一般化は§15のキャッシュ経路により撤回する。
- ~~V2~~: **確認済み**（§3）。
- V2 補足: 呼出元・式・0 の扱いは §3 に確認済みとして記録（今回のM1作業での再試験ではない）。
- V3: 戦闘中に 0x4E9A20 で通行不可を追加し 0x4EA2E0 を再実行してよいか（旧領域の解放、移動中ユニットが持つ領域ポインタの寿命）。
- V4: Block を戦闘中に追加・削除してよいか（空間グリッド `+0x4C` 系への登録・解除）。
- V5: `joint`/`edge` の境界チップは別オブジェクトとして作られるか（基礎チップだけ替えたときの継ぎ目）。

検証用スクリプトは製品リポジトリの `tools/x32dbg/`。

## 6. 主な関数・データ（symbols.tsv に追加）

0x4EEA00 定義パーサー / 0x4EE470 ObjectDef構築 / 0x4EE560 FieldDef構築 / 0x4F0BE0 戦闘マップ読み込み / 0x4562D0 セル設定 / 0x456380 FieldData::vf07 / 0x4DF200 Block生成 / 0x4E5860・0x4E6110 飛び道具とBlock / 0x4E9470・0x4E9A20・0x4E9A60・0x4EA2E0・0x4EAA70・0x4EC1E0 通行グリッドと経路 / 0x4C1B70 座標→セル / 0x4FBE80 NewGameStage::vf02 / 0x4FBF40 NewGameStage::vf03 / 0x576DC0 Unit::vf25 / 0x423E80 チップ名→アトラス矩形。

## 7. M1 実装のための ABI・読取り契約（2026-11-09 Codex）

研究ID: `CODEX-MAP-M1-ABI-20261109`。対象EXE SHA256は本書冒頭と一致（今回実測）。OGGテスト配下コピーを pefile + Capstone で**静的に読んだだけ**で、ゲーム起動・注入・メモリ変更・実機試験は行っていない。VA は基準0x400000で、呼出先は `module+(VA-0x400000)` に補正する。

### 7.1 NewGameStage::vf02 — vtable+8 / 0x4FBE80

- ABIは `FieldData* __thiscall(Stage* self, int32_t px, int32_t py)`。ECX=stage、スタック第1引数=px、第2引数=py、戻り値EAX=セル、callee が8バイトを除去する。［STATIC］
- 根拠: Unit::vf25 の 0x576DE4〜0x576DFE は Unit+0x218 を push、Unit+0x214 を push、ECX=Unit+0x1E4 として `call [vtable+8]`。callee 0x4FBEA3/0x4FBEA6 は [EBP+0xC]/[EBP+8] を読み、0x4FBF19/0x4FBF30 は `ret 8`。
- 整数型の根拠: 斜め座標変換 0x4C1690 内 0x4C16CE〜0x4C16F1 は入力を32ビットで保存して `fild dword` する。float のビット列を渡す契約ではない。
- 斜め表示分岐は 0x4FBE89 の global 0x65BD9E と stage+0xE4 に依存する。helper 0x4C1690 は stage+0xDC/+0xE0、+0x18/+0x20、+0x68、+0xD4/+0xD8 を参照する。非斜め分岐は 0x4FBF26 から 0x4C1B70 へ進む。
- 斜め分岐は変換後のマス座標を 0〜width-1 / 0〜height-1 に丸める（0x4FBEB7〜0x4FBF03）。したがって返却ポインタだけで「入力座標がもともとマップ内だった」とは判定できない。M1では幅高さの正値、積とアドレス加算のoverflow、配列可読範囲を確認し、返却セルが配列内かつ0x11C境界であることを検証して `index=(cell-cells)/0x11C; x=index%width; y=index/width` を得る。
- M1実装前の時点ではvf02をDLLのHKDR購読callbackから呼ぶ実機試験は未実施だった。既存V1は原作自身の vf25→vf02 が返したセルの観察でありDLL呼出の受入れを代替しない。**その後のM1実機確認は§10**に記録する。

### 7.2 Battle_FindUnitByName — 0x49E780

- ABIは `BattleUnit* __fastcall(const char* name, Evaluator* evaluator)`、ECX=終端付き名前、EDX=vm_context+0x504、戻り値EAX。stack引数なし（0x49E8A7 は `ret`）。既存辞書・REF_UNIT_EXP_SUMMON §10 の契約を今回静的に再確認した。［STATIC再確認、新規実機確認ではない］
- 根拠: 0x49E7B6 は名前をECXからEAXへ、0x49E7B8 は評価器をEDXからESIへ保存。0x49E7CF〜0x49E7D9 は名前長を走査。0x49E7F0 は評価器+0x1EEBEC の名前multimapを使用。0x49E826 はnode+0x28のUnit*、0x49E82D/0x49E836 はUnit+0x1867Cのgone byteを読む。生存優先、なければ最初のgone unitを返す。
- 名前表は vm_context+0x504+0x1EEBEC。MSVC map の +4=head、+8=size、node+0/+4/+8=left/parent/right、+0xC=key string、+0x28=Unit*、+0x2D=nil。引数なしsetupの候補は、空表を拒否し、上限付きで検証した表のキーを使いUnitを解決し、Unit+0x1E4のstageを取得すること。これは**実装方針**であり新しい原作関数の発見ではない。stage vtable、配列・幅高さを再検証し、戦闘外・stage変更時に旧記録を捨てる。
- 原作関数は一時std::stringを構築/解放する（0x49E7E1→0x402800、0x49E810→0x5B6BBB）。ゲーム地形やユニットを変更する処理ではないが、完全な「プロセスメモリ書込みなし」の関数ではない。
- **実績の区別**: Extensions commit `1ba7e4c46d7e783f353d3eae9f42b1def24553d5` の `plugins/exp/src/hakushin_exp_dat.h` 225〜238行は名前表を読み取る `hxd_find_unit` 再実装。原作0x49E780を直接呼ぶものではない。同commitの `docs/DAT_ROUTINE_BUS.md` 77〜80・121〜126行はcallback内native直接呼出を未実機確認としている。EXPの戦闘動作実績を、MapGimmickからのnative直接呼出実績に読み替えない。**今回別途確認したMapGimmick M1の実績は§10**。

### 7.3 既存結果との整合と未確認

§0/§3/§4/§5に残っていた「V1推定」「V2の0は未確認」は、同文書の2026-11-09既存V1/V2結果に合わせて訂正した。過去の静的段階のintake本文は当時の記録として維持する。今回新たに実機確認したのではない。この記録時点ではV3〜V5、native lookup/vf02のHKDR callback内呼出、setupの戦闘開始/終了/再戦時の寿命は未確認だった。後日のM1開始・読取り経路の実機確認と、なお未確認の終了/再戦を§10で区別する。静的ABIの一致や合成テストを実機受入れへ格上げしない。

## 8. 試験シナリオの敵勢力設定（2026-11-09 ユーザー実機報告）

- 対象: OGGテスト配下のゲームで、外伝「マップギミックテスト」を**新規開始**した試験。敵勢力 `po_hkmapt2` に `fix = on`、`yabo = 0`、`kosen = 0` を同時に設定した状態で、ユーザーから「敵は攻めてこない」との報告を受けた。確度は**ユーザー実機報告（この設定の組合せ・この試験シナリオに限定）**。
- 変更前は敵に先に攻め込まれて滅亡したため、この3設定を追加して再導入した経緯がある。設定と変更前の状況の出典: [MapGimmick commit 0ca4ddea の試験DAT](https://github.com/ButaMonky/Vahren.exe-MapGimmick/blob/0ca4ddea4f4b0c26aa3c58faff475fe0e90c3201/dat/mapgimmick_test.dat#L72)、同版 `CODEX_HANDOFF.md` §0・§4。結果の出典は本作業チャットのユーザー返答（2026-11-09）。Codexによる独立した画面観察・再試験は行っていない。
- **未分離**: fix / yabo / kosen 各設定の個別効果と必要十分性。他シナリオ・継続セーブ・長時間経過・全難易度で同じ挙動になるかは未確認。DATの既存コメントにある「fix = onで侵攻しない」を単独効果の確定根拠にはしない。
- この報告が確認したのは敵の先行侵攻が見られなかったことだけ。「城壁と門」「海の戦場」へ攻め込めること、M1のDLL読取り結果、M2チップ変更などは本報告の確認範囲に含めない。

## 9. M2 チップ矩形取得の静的契約（2026-11-09 Codex）

研究ID: `CODEX-MAP-M2-CHIP-ABI-20261109`。対象は本書冒頭と同じver0.67 SHA256。OGGテスト配下EXEを静的に読んだ実装担当の出力を確認した。根拠は製品リポジトリ `ButaMonky/Vahren.exe-MapGimmick` の `research/raw/m2_chip_abi.txt`（596行、SHA256 `157b5489bf929c732ea8295e83d2d7ecc70a08df3a869cbed54378727b3eafd2`）。本節で使う命令範囲は以下に限定し、同ファイルの命令途中から始まる0x55A640付近は根拠に使わない。原作バイナリは収録しない。

### 9.1 0x423E80 の引数・戻り値と書込み

- **custom ABI**: EDX=終端付きチップ名 `char*`、ESI=呼出側が用意した24バイト出力、EAX=その出力先、stack引数なし。標準のfastcallだけではESI引数を渡せない。［STATIC］
- 名前は0x423EE8〜0x423F11でEDXから一時std::stringへ変換する。戻りは0x423FFFの `mov eax,esi`、0x42401Cの `ret`。原作FieldData設定側は0x4562DCでESIへstack出力先を入れ、0x4562E0で呼び、0x4562E5〜0x456314で6 dwordをセル+0x6C〜+0x80へ転記する。
- 空名は0x423F1E〜0x423F5A、未登録名は0x423F7F〜0x423FEDで既定矩形をコピーする。既定値は0xB05140〜0xB05154の6 floatで、0x423EAF〜0x423EE2が0xB05158のbit0を使って初回に6個の0.0へ初期化する。つまり取得関数自体にもこのlazy初期化と一時文字列の生成/解放があり、「完全にメモリ書込みをしない関数」ではない。
- 6値の最後2個はfloatのサイズ値。Block側は0x4DF409〜0x4DF415で出力+0x10/+0x14をBlock+0x10C/+0x110へコピーし、0x4DF41D〜0x4DF43Fで `fld dword` と0.0比較を行う。Blockのcoll印が無い経路ではゼロサイズで生成を取りやめる。有限値かつ末尾2値>0を要求するM2の検証は**製品側の安全条件**であり、原作がすべての非有限値/負値を拒否するとの主張ではない。

### 9.2 チップ矩形の名前表

- 0x423F76→0x426360→0x4266B0で名前を検索する。headポインタ格納位置はVA 0x87A230（ASLR時はmodule+0x47A230）。head+4=root、node+0/+4/+8=left/parent/right、node+0xC=std::string key、node+0x28=6 dwordの矩形値、node+0x41=nil byte。［STATIC］
- 根拠: 0x4266B0/0x4266BBがhead/rootを取得、0x4266BE/0x42671Aがnilを検査。0x4266D4でkeyを選び、0x42670F/0x426718でright/leftへ進むlower_bound経路を使う。0x426360は候補のキー比較で一致を確かめ、0x423F7Fはheadとの一致で未登録を判定。0x423F8C〜0x423FACがnode+0x28〜+0x3Cを出力へコピーする。
- これはT040で既出の `g_ChipAtlasMap`（0x879E68、4整数の矩形、node nil+0x39）とは位置・値の幅・nil位置が異なる。本節のnative取得経路で0x879E68の表構造を流用しない。両表の生成・相互変換の全経路は本節では未調査。
- M2実装は名前の検索経路を上限付きで検証してからnative呼出し、出力を検証する。これは実装方針であり、任意の破損状態や同時変更に対するnative関数の安全性を保証する研究結果ではない。

### 9.3 確認範囲

この節はM2実機試験前の静的根拠の記録。後日のHKDR callback内native呼出し・表示変更・復元の実機結果は§11に記録し、静的根拠とは区別する。再戦時の寿命・V5境界飾りは引き続き未検証。既存V1のデバッガによる書換え成功だけをM2製品経路の成功には読み替えない。

## 10. M1 読取り経路の実機確認（2026-11-09 03:24 JST）

研究ID: `CODEX-MAP-M1-LIVE-20261109`。OGGテスト配下で外伝「マップギミックテスト」の「地形読み取り」をユーザーが実行し、Codexがゲーム側 `HakushinMapGimmick.log` を読み取った。対象は本書冒頭のver0.67、詳細ログ版DLLのSHA256は `3d11f1340cbb0a5e27fc6bb523c048ba478b509bdd57b3d003e0415b82ad4d20`（導入先DLLで実測）。原作素材・個人ログの原文は収録せず、確認した値を以下に要約する。

| 時刻（JST、2026-11-09） | 呼出と観測結果 |
|---|---|
| 03:24:04.061 | `hk_map_setup result=0`、width=45、height=45、outputs_valid=1 |
| 03:24:13.818〜.826 | `hk_map_cell_of result=0`、unit=`hk_mapt_hero`、x=20,y=38。続く`hk_map_get result=0`でattr=`grass`、field=`pasture` |
| 03:24:22.066〜03:24:34.972 | cell_of/getとも0、x=24,y=37、attr=`rock`、field=`mt`を複数回 |
| 03:24:44.783〜03:24:52.065 | cell_of/getとも0、x=19,y=37、attr=`grass`、field=`pasture`を複数回 |

同一ゲーム実行（PID 12656）の同一DAT呼出スレッドで、各成功行はoutputs_valid=1だった。これにより今回のM1製品経路について、初期化・HKDR通知からのsetup、原作名前lookup、stage vf02による座標取得、attr/idのDAT文字列配列出力が戦闘中に動いたことを**実機確認**とする。座標と地形の変化もログで確認した。任意のDLL・別版・全呼出状況の安全性まで一般化しない。

### 10.1 先行する -13 と試験配置の修正

03:19:41〜03:20:08の先行試験ではsetup/getは0だが、`hk_map_cell_of(hk_mapt_hero)` は -13（名前未解決）。この時点のhome memberは `a000*6` のみで、master名を設定しただけでは試験対象が明示配置されていなかった。homeへ `hk_mapt_hero` を明示配置したDATで新しく試験し、上表のcell_of=0を確認した。先行試験のgetが返したx=0,y=0のmud/mudは、cell_ofの成功を意味しない。

### 10.2 残る確認

戦闘終了→再戦時のstage寿命、ログOFF、M2のチップ変更/復元、V3〜V5はこのM1実機受入れ範囲に含めない。後日のM2実機結果は§11に分離する。§7の「未実機」は調査当時の履歴として残し、現在の確認範囲は本節による。M2の静的契約（§9）をM1の成功から実機確認へ格上げしない。

## 11. M2 チップ変更・復元の実機確認（2026-11-09 03:30 JST）

研究ID: `CODEX-MAP-M2-LIVE-20261109`。OGGテスト配下の外伝「マップギミックテスト」で、ユーザーから**「見た目が変わり、元に戻った」**と報告があった。Codexは同じ実行の `HakushinMapGimmick.log` を読み取り、下表と照合した。導入先DLL SHA256は `816ed8a5c668029623234b3de4a8ce59d25b7d9c464411ebc212a893a9abb069`（実測）。対象は本書冒頭のver0.67。個人ログ原文・ゲーム素材は収録しない。

| 時刻（JST、2026-11-09） | 呼出と観測結果 |
|---|---|
| 03:30:18.976 | setup=0、45×45、battle=1 |
| 03:30:27.055 | cell_of=0、`hk_mapt_hero` はx=14,y=19 |
| 03:30:27.096 | `hk_map_chip_rect=0`、範囲(12,17)〜(16,21)、chip=`seag` |
| 03:30:32.115 | get=0、x=14,y=19、attr=`sand`、field=`sand` |
| 03:30:44.474 | `hk_map_restore_rect=0`、同じ範囲(12,17)〜(16,21) |
| 03:30:46.928 | get=0、同じx=14,y=19、attr=`sand`、field=`sand` |

同一実行PID 25416・同一DAT呼出スレッド・battle=1の成功行でoutputs_valid=1。inclusive範囲は5×5セル。**ユーザーの画面観察とDLL成功ログを組み合わせ、この試験条件でM2のチップ画像変更と復元が動いたことを実機確認**とする。画面変化はユーザー報告であり、Codexによる独立した画面観察ではない。

### 11.1 試験名 seag の静的確認

M2実装担当と記録担当は試験コピーの `a_default/image/imagedata.dat` を[既存T008形式](research/recovered/plugin_reports1/reports/T008_IMAGE_FORMAT.md)でそれぞれEOFまで読み、502レコード、atlas 2048×6500、全矩形が範囲内であることを確認した。幅高さは先頭2個のu32LE、offset12からNUL終端名＋4個のu32LE矩形を読み、終端名`________`の直後がEOF（12128バイト）であることも確認。metadata SHA256 `06643ee734acb36d1f0b82402791c99479d4b97717fc06e329a2a1e9ac63a95a` は両担当で一致した。画像本体 `image.dat` はBMPで、名前と矩形の対応表は `imagedata.dat`。［静的データ確認］

- `seag`: record byte offset 5114、LTRB=(96,165,128,197)、32×32。
- 参考 `sea0`: offset 4871、LTRB=(1792,133,1824,165)。`grass`: offset 2406、LTRB=(704,101,736,133)。
- このメタデータ確認単独ではnativeロード成功を証明しない。M2製品経路の成功は上記の別の実機観測による。

### 11.2 残る確認と解釈の限界

変更前のgetログが無いため、上表の変更中・復元後がともにsand/sandだったことを「変更前からattr/idが不変だった」とする実機証明には使わない。再戦時のsnapshot寿命、境界飾りの継ぎ目（V5）、ログOFF、異常時rollbackの実機挙動は未検証。任意の画像・範囲・別版の成功へ一般化しない。M3以降の受入れは含まない。


### 11.3 再起動後の再現（03:36 JST）

ユーザーの追加報告「問題なく終わりました」をログと照合した。PID 25008では03:36:08.027にsetup=0、45×45、battle=1、03:36:15.166にchip_rect=0（中心x=3,y=16、範囲(1,14)〜(5,18)、seag）、03:36:24.353に同範囲のrestore_rect=0を確認した。先のPID 25416とは異なる新規プロセスであり、**再起動後の再現成功**に限定する。同一プロセスで戦闘終了→再戦した場合の寿命確認ではない。

### 11.4 同一プロセスで撤退→再戦（03:44〜03:47 JST）

追加試験ではユーザーから「撤退後も維持されました」と報告があり、勢力の存続と再戦を確認した。試験DATはmasterをwallmemberへ明示配置したM2コミット`f47f25f`。それ以前の勢力滅亡の原因をこの変更だけで確定しない。記録担当が読み直したDLLログは次のとおり。

| 時刻 | PID 28996 の結果（すべてresult=0、outputs_valid=1） |
|---|---|
| 03:44:46.918 | setup、45×45、battle=1、stage=012dd860、cells=19a16024 |
| 03:44:55.116 | chip_rect、seag、(1,11)〜(5,15) |
| 03:45:05.642 | restore_rect、同範囲 |
| 03:47:32.191 | setup、45×45、battle=2、stage=012dd860、cells=1888c024 |
| 03:47:42.003 | chip_rect、seag、(0,0)〜(3,3) |
| 03:47:51.511 | restore_rect、同範囲 |

同じプロセスでbattle世代1→2、stageアドレス再利用・cell配列変更後の変更と復元が成功した。2戦目は端でclipされた4×4=16セル。これを同プロセス再戦の受入れ確認とし、§11.2の再戦未検証は先行試験時点の記録とする。cell配列まで完全同一アドレスを再利用する条件、境界飾りの継ぎ目（V5）、ログOFF、異常時rollbackは依然未確認。毒床の実機成功も含まない。

## 12. M4用 DAT 呼出契約の静的調査（2026-11-09）

研究ID: `CODEX-MAP-M4-DAT-20261109`。対象EXE SHA256は `e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187`。結論は静的確認に限定し、毒床・敵のみへの毒付与の実機成功を意味しない。

### 12.1 doskill の第5引数 off は座標モード

`Script_DispatchCommand`（0x4A1250）のcase 0x38、0x4A5740以降を確認した。x/yは0x49CCA0で数値引数として評価される。0x4A5774で第5引数を取得し、0x4A578Aの比較文字列VA 0x6319B8は`on`（対象EXEのPE sectionを直接読み確認）。0x4A579Cで0x4A6B30による文字列比較後、非一致は0x4A580Dへ分岐する。`on`または既定経路では0x4A57AE/0x4A57E1で画面幅・高さ（0x65BEEC/0x65BEF0）によるスケールとカメラ座標加算を行うが、`off`を含む非`on`経路は入力座標をそのまま使う。［STATIC］

従って`off`を敵味方指定と解釈しない。専用発射者のグローバル0xAC08FC/0xAC0900の初期化経路はあるが、その所属・命中対象フィルタは未追跡。Unit+0x1D4の所属識別からred/blueとの対応まで推定しない。また、この版のマス→描画座標を単純なcell×32で求める根拠はない。§7のvf02はpixel→cellであり、逆変換は別途確認が必要。

### 12.2 storeIndexVar は文字列配列の要素を文字列出力

`Script_DispatchVarCommand`（0x4AE0F0）のcase 0x29、0x4B05F8〜0x4B07A6を確認した。入力は文字列配列、添字は0x4B0631から0x49CCA0で評価、出力先は第3引数。0x415530で文字列vectorを構成し、`Ai_InsertKeyedVectorRecord`へ渡す。文字列要素を数値変数へ自動変換して出力する契約ではない。既存HakushinExpの配列出力例とも整合する（[README](research/recovered/plugin_reports1/reports/recruit_sort_v4/docs/HAKUSHIN_EXP_README.md)、countVar/storeIndexVarの説明）。［STATIC］

0x49CCA0（既存Ghidra名`ScriptArg_EvalIntLiteralOrVar`、189 bytes）はinteger literalへのdynamic_cast成功時に+4の整数を返し、numeric variableの場合は`Variable_GetOrCreateNumeric`によるレコード+0x1Cを読む。不適合型は例外経路へ進む。この評価経路には文字列の数値変換がない。ただし、別の明示変換命令が全命令集合に存在しないことまでは確認していない。［STATIC］

### 12.3 毒識別子 poi と耐性スキルの区別

OGGテストの原作DATを読み取り、`a_default/script/30_スキル/F12_charge.dat:1642–1663`の`dsncharge`に`func=charge`、`add=poi`（1661行）、`add_per=50`（1662行）を確認した。毒付与の既存識別子はこの定義では`poi`であり、`poison`という綴りを未検証のまま代入しない。一方、`Status_10_部隊.dat:332–343`の`ps_poi`は`func=status`、`attr=poi`による耐性用定義であり、毒付与の動作例には使えない。原作定義の存在と、doskill経由で敵だけに毒を付けられることは別の主張である。最小毒床の実機試験・発射者所属・耐性による影響は未確認。素材本文は収録しない。［静的データ確認］

### 12.4 根拠と再確認方法

解析担当は`dev_lab/HakushinMapGimmick/tools/ghidra/run_query.py`から、project `dev_lab/_work/kb_ghidra_validation_20261030/Hakushin067_ResidualCodeRepair_20261022`、program `hakushin067_Vahren.exe`を`-noanalysis -readOnly`で照会し、3件ともexit 0。記録担当も該当出力を読み、上記分岐・型評価と照合した。出力はローカルTEMPの解析結果であり、正本収録物ではない。再確認は上記VAで行える。

| ローカル解析出力 | SHA256 | 確認範囲 |
|---|---|---|
| `%TEMP%/m4_dat_query2_out.txt` | `f0def70da51d819c12b1b15a0d02ed851dd2a86b61f9df1dbd5db9778b3a1b29` | doskill 2293–2378行、storeIndexVar 4661–4732行 |
| `%TEMP%/m4_dat_query3_out.txt` | `ed40f1ca2076bc2aba066c69b3b993f4432a4a4fc256e42d5103b19fc6fa1546` | 0x4A5740以降の110命令、0x4A6B30 |
| `%TEMP%/m4_dat_query4_out.txt` | `d36b8871210d44527e1631853383fe7650f98afaae4b1cb08f7b2905a9070519` | 0x49CCA0 |


## 13. M3 アニメーション試験と時間単位の訂正（2026-11-09）

研究ID: `CODEX-MAP-M3-LIVE-20261109`。対象はOGGテストの同じver0.67。導入DLL SHA256は `026ff7879eaca7bf4d2bc973a94866a5ca482b393816179d3dab5bb1b332a663`（plugins配下を実測）。以下はログの成功、画面についてのユーザー報告、静的な時間契約を分離した記録であり、M3の全面受入れではない。画像・個人ログ原文は収録しない。

### 13.1 grass画像列と初回試験

§11.1と同一SHA・T008形式の`imagedata.dat`で、M3実装担当が全502レコード・EOF・boundsを検証した際に次を確認した。［静的データ確認］

| 名前 | record byte offset | LTRB |
|---|---:|---|
| grass | 2406 | (704,101,736,133) |
| grass1 | 2428 | (736,101,768,133) |
| grass2 | 2451 | (768,101,800,133) |

初回PID 24040では03:56:11.488のanim_def=0、03:56:11.490のanim_rect=0、範囲(4,8)〜(8,12)、active=25、interval=20。03:57:16.221までtick=0が継続し、restore呼出は無かった。ユーザー報告は「止まらなかったように見える、重くない」。これは登録/tickの成功と体感負荷の報告であり、目視の切替・停止が成功した証明ではない。

### 13.2 DLLtickと内部時計の取り違え

初回DATは1200回の`hk_map_tick`呼出を20秒として扱っていた。しかし1 DLLtickはDATからの呼出1回で、内部シミュレーションtickや描画frameとは別である。既存A72の保存根拠`exe/T010_BATTLE_FRAME_ORDER.md`§4/§6および`exe/T010_CLOCK_UPDATE_PROBE.txt`では、通常0x492D80(arg0)の0x492FA1 `jne 4930A6`によりabsolute%10!=0時はreturnし、0x4930C0 root scanも10内部tick境界の内側にある。正本内にも[T030のA72訂正](research/recovered/principal_models1/reports/data/T030_RTS_MODE.md)488行に保存されている。旧[T010](research/recovered/script_topics/T010_EVENT_SCHEDULER.md)132行の初回counter=1/毎tick root評価はこの通常経路に適用しない。［既存STATICの再照合］

初回ログの60 DLL呼出ごとの成功要約は概ね10秒間隔で、通常内部60tick/sを仮定するとDLL呼出は約6/s、1200回は約200秒になる。これは固定実時間保証ではなく、速度・pause・gate・別arg1経路によって変わる。restore未到達をDLL停止機能の不具合と結論しない。試験DATだけをinterval=2、`isInterval(600)`の2周期でrestoreする形へ訂正し、DLLは変更していない。

### 13.3 修正試験と一時停止中の表示

記録担当が直接読んだPID 13528の結果は次のとおり。［実機ログ確認］

| 時刻（JST） | 観測 |
|---|---|
| 04:05:41.063 / .070 | anim_def=0 / anim_rect=0、interval=2、範囲(4,8)〜(8,12)、active=25 |
| 04:05:57.383 | tick=0、active=25、区間集計anim_changed=750 / transitions=30 |
| 04:06:05.466 | restore_rect=0、同範囲、active=0 |
| 04:06:07.595 | get=0、active=0 |
| 04:06:09.642 | tick=0、active=0、区間集計anim_changed=700 / transitions=28 |

最後の700/28は直前60呼出区間の累積であり、復元後に700セルを書き直したという意味ではない。製品`src/hakushin_map_plugin.c:151–170,202–203`のtickログ集計を照合した。

ユーザーは最初に「一部戻るが草が残る」、続いて「画面移動したら残っていた草は消えた、ゲーム閉じた」と報告し、試験時は「一時停止していた」と確認した。ログでは復元・active=0が成立し、報告された一部の残像はカメラ移動後に解消した。この観測だけでキャッシュ原因を確定しない。T010§5にはpause中もUI/renderの別経路があるため「pauseですべての描画が停止する」とも断定しない。

**未確認:** 通常進行・カメラ固定時の即時復元、意図した3画像の目視切替、長時間負荷、M3の同プロセス再戦。M3全面受入れは保留。

## 14. M4 所属aliasと命中対象の追加静的調査

研究IDは§12の`CODEX-MAP-M4-DAT-20261109`を継続する。同じEXE・読み取り専用Ghidra projectでの追加照会（exit 0）によるSTATIC。§12.1/§12.3の所属・命中経路未追跡はその時点の履歴であり、以下の局所契約まで追跡した。毒床の実機確認とはしない。

### 14.1 色aliasとdoskill専用発射者

- Enemy ctor 0x447280はparam3をowner+0x0Cへ保存。初期化0x48A973/0x48A9A6はmask 2/4で生成してE+0x1E8634/+0x1E8638へ置き、0x51E100経由のE+0x1E8630はmask 1。
- storeRectUnitの0x4B3227以降では`red`（VA 0x630D38）がE+0x1EED48、`blue`（0x630D3C）がE+0x1EED44を参照し、そのowner+0x0Cを使う。
- 0x432AEB〜0x432AFDはflags E+0x1EED54/+0x1EED55が両方0の場合にred=slot+0x1E8634、blue=slot+0x1E8638を設定する。他状態の0x432B0E〜0x432B34はslot+0x1E8630/+0x1E8634へ切り替える。0x492726/+2Cにも呼出側pointerによるalias設定がある。従って色とmaskを固定対応させない。
- doskillの0xAC08FC専用ownerはmask 2で作られる。0x4A58BA〜0x4A58D4でUnit ctor 0x56F880のparam5へこのownerを渡し、ctorはUnit+0x1D4へ保存する。`off`による座標選択と、この所属maskは独立である。

### 14.2 attack_usと局所命中filter

既存`exe/T012_SKILL_PARSER_FIELD_DUMP.txt:35–48`の0x59A4AF→0x59A4D8はSkill+0x70への設定。解析担当が対象PEを直接読み、比較文字列VA 0x624898=`attack_us`（隣接0x6248A4=`skill`）を確認した。0x580280ではSkill+0x70のbit 1/2/4をそれぞれMissile+0x19C/+0x19D/+0x19Eへ写し、値7では+0x19Fを立てる。

0x4E5860/0x4E6110はowner maskが1または4かのboolを作り、混乱Unit+0xC8<0時の乱数反転を経て+0x19CとXORする。候補側にもmask 1/4判定を行い、不一致を通常対象とし、+0x19Dは両側、+0x19Eは自己を許可、+0x19Fは通常の他者経路を抑止する。0x54BA00からこれらの衝突判定後に0x54DAE0の適用へ進む。

従って混乱等の別条件がない通常のdoskill専用mask 2発射者では、attack_us=0はmask 1/4側、attack_us=1はmask 2側を対象にする局所filterと読める。ただし色alias・実際の配置・衝突条件は別途必要であり、任意の「敵だけ」への毒成功を保証しない。毒確率・耐性・同group複数巻込み・最小skill全体と実機成立は未確認。

### 14.3 追加出力の出所

根拠はローカル`%TEMP%`の解析出力で、原作素材ではなく非収録の照会結果。§12.4と同じproject/target、下記SHAは記録担当も照合。VAと局所範囲を上記に残し、再確認可能にした。

| 出力 | SHA256 | 主な範囲 |
|---|---|---|
| m4_sides_out.txt | `58946e2425df4780bdac4f32f1340a5527bba4d1de44cce6efd684d74e599b57` | Enemy ctor、doskill owner/Unit構築 |
| m4_sides2_out.txt | `55392bab7db18d8d8644899814c97ffd6cdaacbc7d0f678335ea37a48e6569b1` | storeRectUnit色alias |
| m4_sides3_out.txt | `747997cbcff7dc7812b66df90cc9f91f605d0bbbdfa489a16c7ac051a7b18d2b` | 3 slot初期化 |
| m4_dummy_out.txt | `6c3a490c140f07fc71c469bd1377571d076ef5b0898392d61c9eb6e52f0d5999` | 563行 Unit+0x1D4=param5 |
| m4_alias_out.txt | `55d1cfc779cb2365139aa9a6dc7ae3d09642f94b494eae8290b444d9a4d3fdb1` | 0x432AEB/0x492726 |
| m4_projectile_out.txt | `208598738b795f3f76a1b6d3b6202bc949ce67a921890ffb3456d7c24e58d405` | 507–529行、Skill+0x70 |
| m4_hitfilter_out.txt | `aaba31bb4627771a3d0089418cb059862f27de2ae3b7e2056a6ff01f920538b1` | 59–74、300–318、359–375、733–748、839–850行 |
| m4_collision_out.txt | `5ca0cf1100b894e85553c287c76e86d79006744d0a0f048dedbcbb65cc3bb384` | 504–527行、衝突後の適用 |


## 15. 地形頂点キャッシュと表示反映の条件

研究ID: `CODEX-MAP-M3-RENDER-CACHE-20261109`。§13の残像観測を受けた追加STATIC。新たなゲームattach・liveメモリ観測は行っていない。§0/§2.1/§5の「毎描画vf07・次描画へ必ず反映」は広すぎたため訂正し、V1で実際に観測した即時反映自体は保持する。

- 0x4C271F/0x4C2722はG+0x94から描画コンテキストRを取得して0x4C2728で描画へ進む。
- 0x4C4420内の0x4C45F3でmode 1を判定し、0x4C45FCでR+0x3C8Cが非ゼロなら0x4C4603からreturn。ゼロの場合のみR+0x38のstageを取り（0x4C461C）、vf03でセルを列挙（0x4C4641）し、セル+0x6C〜+0x78から6頂点を直接作る。0x4C47F2でR+0x3C8C=1としてvertex bufferへuploadする。［STATIC］
- カメラsetter 0x4C3C20はR+0x4C/+0x50の座標を設定し、0x4C3C5AでR+0x3C8C=0にして行列を再計算する。0x520800からこのsetterを呼ぶ経路を確認した。［STATIC］
- 0x4C3EB0の描画先頭にはtargetを黒へClearする経路がある。通常のalphaによる前frame残留を原因とする根拠にはならない。

**解釈の限界:** M3の「画面移動で草の残像が消えた」はカメラ変更によるキャッシュ再構築と整合する［INFERRED］。しかし当該実機のR/mode/flagは観測しておらず、原因を実機確定とはしない。画像変更後の適切な無効化方法、別mode、一時停止と通常進行の差、継ぎ目は別途検証する。この静的調査時点ではR+0x3C8Cの書換え実機成功はまだない。後日のcache対応版による固定カメラでの変更/復元成功は§18に分離し、当該実行のR/mode/flagの直接観測とは区別する。

根拠は§12.4と同じreadOnly Ghidra project・対象EXE、全照会exit 0。ローカル`%TEMP%`解析出力のSHA256（本文・素材の転載なし）:

| 出力 | SHA256 | 確認範囲 |
|---|---|---|
| m3_render_out.txt | `16b3cfc093bc7dd236102b043b8aaba1ce0ffe8511c10c5bd75ee13f2dff6178` | 描画関連関数 |
| m3_render2_out.txt | `74afb5a21f9a652e47df669700d1a07bf9fc75d27a275abd023e394d3e78b99d` | 61行Clear、244–332行cache/build |
| m3_dirty_out.txt | `044a1ee4b3d88e76eb425a01c9d0f9f992c4b7529b9265deb8fed68060ca1285` | flag 0/1の保存位置 |
| m3_dirtywriters_out.txt | `628ecf3e85b1aa1297e337752700783fdf582a822d4cb044be733bab9e3ae97f` | 388–434行カメラsetter |
| m3_camera_out.txt | `697b20012817e173b24f539bee58796ce9fae5518d1b2e6b761d6a6daa384055` | R取得、mode/flag分岐、stage取得 |


## 16. M5/M6準備: gridの所有権と再構築境界

研究ID: `CODEX-MAP-M6-GRID-OWNERSHIP-20261109`。既存証拠の再照合と同じver0.67へのreadOnly静的照会。M6の危険な仮実装・OGG変更・新規実機試験は行っていない。

### 16.1 Gとgridの参照、field/objectの区別

`G=module+(0x8BE2F0-0x400000)`はGameManagerの実体（symbolsのkind=object）で、`[G]`はそのvtable。製品保存ASM `research/raw/dis_4f0be0.txt` の0x4F0D8Bはstage+0xE8からGを取得、0x4F0D91はLEA G+0x88、0x4F0D9BはMOV [G+0x90]でgridポインタを取得する。正本の旧「gridはG+0x90」という省略はdereference位置が曖昧だったため、§2.3を`grid=[G+0x90]`へ明確化した。［STATIC］

「field collは全MAPで未使用」と一般化しない。[既存全MAP調査](research/recovered/DEVLAB_TERRAIN_MOVETYPE_20261011.md)12–14行は、highland_128_collを24,382セル、highland_128_coll_wを1,312セルと記録し、前者のtype=collは有効、後者はコメントであると区別している。これは過去の全量データ調査であり、今回の試験MAPにcollが存在するかの新しい実測ではない。また同文書の当時「native未取得」は履歴として保持し、後日の§1/§2のnative証拠と混同しない。

objectのcoll/wall/wall2によるBlockと、break/break2/gate(type 5/6)の専用生成は異なる。field attr変更、通行grid変更、Blockの生成/削除は別操作であり、gridを開通させても既存Blockが消えるとは限らない。M5のattrで変わるmovetype判定と、M6の経路グラフ・V4のBlock管理を一つの成否にまとめない。

### 16.2 4EA2E0単独の再実行とcache

製品保存`research/raw/q14_out.txt:634–692`では4EA2E0が新nodeをgrid+0x68へ上書きし、一時木を解放する。旧領域nodeの解放処理ではない。同784–806行の4EC1E0はgrid+0x64の2つの領域番号から`((src & 0x7fff)<<16) | (dst & 0xffff)`を作り、grid+0x80系cacheのhit時に保存済pathを返す。新領域で番号が再利用される場合、旧cacheのままでは旧pathを返す危険がある。旧nodeを残して解放済参照を避けるだけでは、正しさもリーク回避も満たさない。［STATICからの設計上の帰結］

### 16.3 4E9470の解放と再確保

新しい保存照会`m6_grid_ownership_out.txt:34–181`で、4E9470は旧幅/高さが非ゼロの場合に次を行うことを確認した。［STATIC］

1. 旧grid+0x68全セルの非ゼロnodeを一時木へ集約し、その木を走査する。
2. 各nodeの+0x2Cの隣接木、+0x18のvector、node本体を解放する。
3. gridの細3表と粗表の行・行表を解放する。
4. grid+0x84のcache値vectorを解放し、0x4F4140を呼び、+0xACの順序listを解放して+0xB0=0へ戻す。
5. 182–256行で幅/高さと表を再確保し、+0x60=0、+0x64=0x80000008、+0x68=0、+0x7C=0で初期化する。

同262–288行の4E9980も隣接木/vector/node本体を解放するnode destructorである。旧+0x68を先にゼロ化すると4E9470が旧nodeを収集する手掛かりを失うため、sentinelリセットとcleanupの順序を取り違えない。4E9470は通行byteも初期化するので、既存障害物を保持したまま単に呼び直すAPIではない。

正規xrefはmap loader内0x4F0F06の1件。callerはEDI=grid、`push height; push width; call 4E9470`。callee先頭もEDIをgridとして読み、正常epilogue 0x4E9948は`RET 8`（`m6_path_copy_out.txt`）。従ってEDIの暗黙引数＋stack width/height＋callee cleanupであり、単純なcdecl/thiscall宣言に置換しない。値の返却はこの呼出から有用な契約を確定していない。［STATIC ABI］

**未確認:** 戦闘中の正規cleanup呼出条件、Unit/AIが保持する旧経路の寿命全体、再確保例外後の復旧、変更前の細/粗障害物の安全な保存復元。正規map-load経路の存在は戦闘中の再初期化が安全という証明ではない。M6/V3はまだ未実機であり、この調査だけで有効化しない。

### 16.4 根拠の所在

新規照会は§12.4の既知Ghidra project/EXEを`-noanalysis -readOnly`で読み、全件exit 0。ローカルTEMP出力のSHA256を記録し、ゲーム資産・個人ログは収録しない。

| 出力 | SHA256 | 範囲 |
|---|---|---|
| m6_grid_ownership_out.txt | `1b3cb699d12cfdb57eb4586caa2056aa19c9d6b27a1a5ef9f258fc48995a325b` | 4E9470/4E9980、loader caller |
| m6_path_lifetime_out.txt | `594d8c82eba87197d7aa1aa2cb5579c81d0d8ea9fba37367298ee8668f666806` | 5767B0/5769B0、4E9470 prologueとxref |
| m6_path_copy_out.txt | `33de387f3835518b99856233818dab40c9ded95a31fc1edf261c553f07c0bc94` | 57A690/4EDFE0、4E9948 RET8 |
| m6_path_values_out.txt | `a665a00a6dc58f3fa0dfb002138be21b468042d1f8f548e241e4988d1f865c7a` | 57A910、両callerのUnit+0x186B0宛先 |
| m6_path_values_asm_out.txt | `a581a1aec0254aacbd87397a619e8bec7170e582d52e78b99f253b3445a18688` | 57A910の範囲反復・ESI引数 |

### 16.5 直接callerのpath値コピーと残る寿命問題

0x4EC1E0の既知直接callerは0x5767B0と0x5769B0。前者0x5767FC〜0x57680E、後者0x576AB1〜0x576AC3は返されたvectorのbegin/endを取り、ESI=`Unit+0x186B0`として0x57A690へ渡す。0x57A690は旧list nodeをdeleteしてから0x57A910へ範囲挿入する。0x57A910の0x57A93E/0x57A950/0x57A98CはESIを入力beginからendまで8 bytesずつ進め、0x57A960で0x4EDFE0を呼ぶ。0x4EDFE0は新しい0x10-byte list nodeを確保し、+8/+0xCへESIが指す2DWORDをコピーする。［STATIC、decompileとASMを照合］

従ってこの2経路では、返されたvectorの保存領域をそのままUnitが借用し続けるのではなく、8-byte要素をUnit側listへ値コピーする。**これを全AI経路の無参照保証へ一般化しない。** コピーされた要素の意味と下流の全consumer、node等のpointer値が要素に含まれないことの全体証明、cache破棄と同時進行する処理の排他は未確認。さらに値コピーが独立していても、既にUnitへ渡した旧経路を再計算しなければ新しい障害物へ向かい続ける問題が残る。

次の最小確認は、Unit+0x186B0のconsumerと移動中の再経路探索条件を既存B/T028記録へ接続し、合法な停止点で旧経路を無効化できるかを確定すること。M6の実機はそれ以降とし、新規移動命令、移動途中、解除、同プロセス再戦、反復時のメモリ量を別々に観測する。


## 17. M5 attr代入の文字列ABIと容量内経路

研究ID: `CODEX-MAP-M5-STRING-ASSIGN-20261109`。M5設計準備のSTATICであり、attr変更/復元の実機成功ではない。原作0x402710はC文字列代入ではなく、**文字列オブジェクトから部分文字列を代入する関数**である。

| 項目 | 確認した契約 |
|---|---|
| ABI | ECX=宛先object、stack=(source object pointer, position, count)、RET 0xC、EAX=宛先 |
| metadata | object+0x10=length、+0x14=capacity。capacity<16はinline、>=16はobject先頭のpointerをdataとして読む |
| コピー長 | min(source.length-position,count)。宛先lengthを更新して末尾NULを書き込む |
| 範囲外position | 0x402721の比較後0x40272A→0x5B5BBA、std::out_of_range |
| 過大長 | 0x40275C〜0x402766→0x5B5B6D、std::length_error |
| 容量不足 | 0x40276B〜0x402777でcapacity<コピー長なら0x402A40へ進む |
| 容量内縮小/空代入 | heap pointerとcapacityを保持し、空でもheapを解放しない |
| 自己代入 | source==destは0x4028F0を使う別経路 |
| 成否 | bool戻り値はなく、正常復帰後のmetadataとbytesの再読照合が必要 |

0x402A40はoperator_newを使う容量拡張経路とbad_allocのthrow経路を持つ。成長時例外の全所有権・strong exception guaranteeは未確定であり、Zig/C側で原作MSVC C++例外を通常の失敗戻り値のように扱わない。［STATIC／未確定境界］

M5初版の**提案**は、原作宛先のcapacity内だけを許し、sourceを別object、position=0、count=検証済lengthとして既知の範囲外・成長経路を避ける方式。従来DESIGNの「元のattrと同じ長さ以下」という案に対し、native分岐が比較するのは元lengthではなくcapacityである。ただし「capacity内なら全て安全」という一般保証ではなく、metadata・SSO/heapのdata領域・NUL・書込み可能範囲・stage寿命の検証は必要。自己代入経路は初版対象外とする提案。

復元用にはDLL所有の元bytesとlengthを保存する。原作string構造体のheap pointerを複製して後から戻す方式は所有権を壊すため使わない。短縮後もcapacityは保持されるため、その容量内で元bytesを戻す経路を構成できる［設計上の帰結、実機未検証］。再確保を伴う復元・例外後復旧は未解決。複数セルの全件事前検証、途中失敗時のrollback、画像とattrの独立した元値保存は製品側の実装/合成テストで別途検証する。

M5はセル+0xD4のattrのみを対象とし、field id・FieldDef・通行grid・Blockの変更を同時成功とみなさない。既存hk_map_getの出力残値で意図せずattr変更しないよう明示指定が必要という製品設計案も、native契約とは区別する。

根拠は§12.4と同じ対象EXE・readOnly Ghidra、照会2件exit 0。記録担当も出力とSHAを照合した。ローカル解析出力は非収録:

- `%TEMP%/m5_string_out.txt`: SHA256 `1ea763a2b7785da1b3ad4325d200645d34c3c03cf522d0d4ecf5ca734e65507c`（0x402710 decompile＋ASM）。
- `%TEMP%/m5_growth_out.txt`: SHA256 `5052f060f6211f2a937f8056b27707a04d88719ef3f59a7b59a508c7344827bf`（0x402A40とthrow helper）。

### 17.1 M6へ越境しない座標上の注意

既存`research/raw/q14_out.txt`の4EC1E0は座標を>>5してgrid照会へ進む一方、M1のFieldData取得は斜め表示対応のstage.vf02を使う。DATのcell x/yをそのまま通行gridのx/yへ書く対応は今回未証明である。M5のattr対象セルが正しく取れたことをM6の通行grid座標対応の証明に流用しない。これは既存経路間の接続上のVERIFY項目であり、新しい実機観測ではない。


## 18. M3 cache対応版の固定カメラ試験（2026-11-09 05:08 JST）

研究IDは`CODEX-MAP-M3-LIVE-20261109`を継続。OGGテストの自動event戦闘で、親実装担当が画面を操作・観察し、記録担当が同実行のDLLログと配置ファイルSHAを独立に照合した。通常侵攻ではなく、単一戦闘での確認である。

- DLL: M3 cache対応コミット`3abbf33`、SHA256 `ce81ff368a482b24e4f54749f294366f9b0886f1bac94f5088cdda78445b6ed3`。OGG配下の唯一のVahren.exeの親/plugins/HakushinMapGimmick.dllを選び実測し、backup内の旧DLLを除外した。
- 試験DAT: `edb620d`、`mapgimmick_test.dat` SHA256 `6c27206a2c3a06a4bdc817dab0436d23ebbaff51d3d93cee501aac8b17339afa`。原作root listを置換するbattleEvent呼出を避けた試験構成。素材・DAT本文・画面画像・個人ログ原文は収録しない。
- 実行PID 26792、同一thread 31780、battle=1。ctx=010ee2f0、stage=012dd860、cells=01758024、45×45。ctxはログのDATコンテキスト値であり、§16のGameManager実体Gと混同しない。

| 時刻（JST） | ログ観測（全行result=0、outputs_valid=1） |
|---|---|
| 05:08:07.233 | setup、45×45、battle=1 |
| 05:08:13.894 | anim_def、grass_demo、interval=2 |
| 05:08:13.903 | anim_rect、範囲(29,19)〜(33,23)、active=25 |
| 05:08:43.055 | tick、active=25、区間集計changed=750/transitions=30 |
| 05:08:58.180 | restore_rect、同範囲、active=0 |
| 05:09:04.784 / 05:09:26.276 | get、active=0、x=31,y=21、attr=grass、field=pasture |
| 05:09:11.606 | tick、active=0、区間集計changed=725/transitions=29 |

最後の725/29は前の集計以降に発生した変更の累積であり、復元後の新たな725セル書込みを意味しない（§13.3と同じログ仕様）。変更中05:08:36.004にもgrass/pastureだったが、変更開始前のgetが無いためこれだけで変更前からの不変を証明しない。

親担当の画面観測では、カメラ移動を行わず、緑色の変更パッチ出現→restore後に黄色い元地形へ全体復元→復元状態の維持→自動監視によるworld帰還を確認した。記録担当自身による画面の独立観察ではなく、操作担当の直接観察とログを組み合わせた受入れ証拠である。**この自動event戦闘・固定カメラ条件で、cache対応版の変更と復元が成立した**とする。§13のカメラ移動後だけ解消した先行観測とは別試験として保持する。

同DATでHKDR setupに到達したことは観測済み。ただし[スクリプトREF §4](REF_SCRIPT_VM_CONTEXT.md#4-battleevent-replace-all-correction)のreplace-all静的訂正に対する万能な因果実証とはせず、登録構成修正後に到達した実機結果として記録する。

**未確認:** 通常侵攻で同じ結果になること、pause状態が実際に成立していたこと、M3同プロセス再戦、長時間負荷、3画像それぞれの目視識別。M4毒床・M5attr・M6通行再構築の実機成功は含めない。§15のR/mode/flag自体のlive値は今回も記録しておらず、元の残像原因を遡って確定しない。
