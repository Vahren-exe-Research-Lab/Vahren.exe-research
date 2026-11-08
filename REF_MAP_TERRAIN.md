# 戦闘マップ：地形チップ・オブジェクト・通行判定・移動速度（MAP-T001）

対象: ver0.67 Vahren.exe SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（ImageBase 0x400000、VAはそのまま）。
研究ID: `CLAUDE-MAP-T001-20261109`。担当: Claude（2026-11-09）。
確度の書き方: **静的確認**＝原EXEの命令列で確認／**推定**＝静的根拠はあるが実機未確認／**未確認**。実機Golden 0件。
実装・設計・検証手順は製品リポジトリ `ButaMonky/Vahren.exe-MapGimmick`（Private）に置く。生の逆アセンブル出力はそちらの `research/raw/`。

## 0. 要点

1. 地形（field）とオブジェクト（object）の定義は **0x4EEA00** が全件パースし、マップ管理（`NewGameStage`、vtable 0x63A6EC）の **+0xFC（field）/ +0xEC（object）** の `std::map` に格納する。［静的確認］
2. 「通れない」は3系統ある。［静的確認］
   - **field の `type = coll / wall / wall2`** … そのマスを通行不可グリッドに1を立て、同じマスに見えない当たり判定オブジェクト（Block）を作る。
   - **object の `type = coll / wall / wall2`** … Block を作る。`type` 無指定（木など）と `floor` は**当たり判定なし**（見た目だけ）。
   - **object の `type = break / break2 / gate`** … 壊せる壁・門。通常の Block ではなく専用の生成経路（0x4F3290 経由）で作られる。
3. **移動の速さ・可否は movetype × 地形の attr**。ユニットの仮想関数 **Unit::vf25（0x576DC0）** が、いる座標のセルの `attr` 文字列でユニットの movetype 表を引き、`consti` の値を返す（無ければ既定 **5**）。`ship` の `grass*0` のように **0 のとき「その移動タイプでは進めない」** になる（0 の扱い＝速度0 の消費側は未確認）。［vf25 は静的確認、0＝不可は推定］
4. セル（`FieldData`、0x11C バイト）は描画オブジェクトで、テクスチャ座標（チップ画像の位置）を **+0x6C〜+0x80** に持つ。毎フレーム、表示範囲のセルを列挙（NewGameStage::vf03）→ 各セルの FieldData::vf07 が +0x6C の値から頂点を作る。よって **この6値を書き換えれば次の描画からチップの見た目が変わる**（アニメーション・途中変更の土台）。［静的確認、実機の即時反映は未確認］
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

FieldData::vf07（0x456380）は +0x6C〜+0x78 をUV、+0x8C〜+0xA8 を位置として6頂点（2三角形）を書く。NewGameStage::vf03（0x4FBF40）は表示矩形内のセルを列挙する（0x4C1BE0）。［静的確認］

### 2.2 Block（地形・オブジェクトの当たり判定と表示、vtable 0x6392BC）

0x4DF200 が ObjectDef 相当から生成。`+0x5C` alpha、`+0x114/+0x118` 位置、`+0x11C` radius、`+0x120〜+0x12C` 当たり矩形、`+0x130` floor、`+0x134` land_base、`+0x138` no_wall2、`+0x13C` no_arc_hit、`+0xFC〜+0x110` UV。
type による旗: 1→`+0x130`、2→`+0x67`、3→`+0x67,+0x68`、4→`+0x67,+0x68,+0x69`。type0 は旗なし。画像の大きさが0で `+0x67` も無ければ生成を取りやめる。Block::vf20(1)＝no_arc_hit、vf20(それ以外)＝no_wall2。［静的確認］

**飛び道具との判定**（0x4E5860／0x4E6110、Missile::vf01・SimpleMissile::vf01 から呼ばれる）: `+0x68`（wall）が立つ Block は矩形内で飛び道具を止める。`+0x69`（wall2）の場合は、飛び道具側の条件が成り立つとき乱数と no_wall2 を比べ、乱数が no_wall2 以上なら止める（＝no_wall2 は**すり抜け確率**に相当）。［静的確認。乱数の範囲と飛び道具側条件の意味は未確認］

### 2.3 通行グリッド（`grid`）

grid は `g_GameManager+0x90`（GameManager+0x88 にある小オブジェクトの+8）。

| オフセット | 内容 |
|---|---|
| +0x60 | 行ポインタ表（byte）。1=通れない |
| +0x64 | 行ポインタ表（int）。経路用の領域番号、初期値 0x80000008 |
| +0x68 | 行ポインタ表（pointer）。領域ノード |
| +0x6C / +0x70 | 幅 / 高さ（マス） |
| +0x74 / +0x78 / +0x7C | 粗グリッド（半分の解像度）の幅・高さ・行表 |

- 0x4E9470: 初期化、0x4E9A20: 1マスを通行不可にする（細・粗両方）。
- 0x4EA2E0 → 0x4E9A60: 通れるマスを長方形の領域に分け、経路探索のグラフを作る（読み込みの最後に呼ばれる）。
- 0x4EAA70: 2点間を8方向に歩いて通行不可マスに当たるか調べる（直進可否）。
- 0x4EC1E0: 経路照会（辞書の既存名 `RouteCache_ConditionalHitPromotion`、B レーン T028 の経路キャッシュと同一関数）。内部で 0x4EAC30（領域ノード +0x68 の参照）と 0x4EAA70 を呼ぶ。呼出元は Unit_ProcessKnockbackMotion（0x5769B0）と 0x5767B0（ユニット移動）。［静的確認］

## 3. 移動タイプと地形の速さ

- Unit::vf25（0x576DC0）: `Unit+0x1F0` と `UnitDef(+0x1C8)+0x14C` が有効なら、`Unit+0x1E4`（stage）の vf02 で現在座標（`Unit+0x214/+0x218`）のセルを取り、セル `+0xD4`（attr）でユニットの movetype 表（`Unit+0x1E8` 系の木、終端 `+0x1EC`）を探し、見つかれば値、無ければ **5** を返す。［静的確認］
- movetype.dat の `consti = attr*値` が値の出所（既存 DEVLAB_TERRAIN_MOVETYPE 参照。33種）。0 と未記述の区別は消費側で未確認（未記述なら既定5 は上記で確認）。
- vf25 の戻り値を速度へ掛ける式・0 のときの扱いは**未確認**（x32dbg 検証項目 V2）。

## 4. 原作でできること・できないこと

| 目的 | 原作の機能 | 備考 |
|---|---|---|
| 地形で移動不可 | field `type=coll/wall/wall2`、object `type=coll/wall/wall2` | 読み込み時に確定 |
| 移動タイプで不可・遅い | movetype の consti（0 や小さい値） | 例 ship は陸 0 |
| 壊せる壁・門 | object `type=break/break2/gate` | 専用経路。門は break2 と同値 |
| 飛び道具を止める | `wall`（必ず）、`wall2`（確率） | 2.2 |
| ダメージ床・毒床 | **無し** | DAT の `doskill(skill,x,y,向き,off)` を定期実行すれば代用可 |
| 戦闘中のチップ変更・アニメーション | **無し** | DLL で FieldData +0x6C を書換え（推定で可能） |
| 季節でマップを変える | `changeMap`（Spot のマップ名、世界画面） | 戦闘用マップの差し替えは DAT だけで可能 |

## 5. 未確認（x32dbg 検証項目）

- V1: 戦闘中に FieldData::vf07（0x456380）が毎フレーム呼ばれるか、+0x6C 書換えが次フレームで反映されるか。
- V2: Unit::vf25 の呼出元と、戻り値（consti）から移動速度への式、0 の扱い。
- V3: 戦闘中に 0x4E9A20 で通行不可を追加し 0x4EA2E0 を再実行してよいか（旧領域の解放、移動中ユニットが持つ領域ポインタの寿命）。
- V4: Block を戦闘中に追加・削除してよいか（空間グリッド `+0x4C` 系への登録・解除）。
- V5: `joint`/`edge` の境界チップは別オブジェクトとして作られるか（基礎チップだけ替えたときの継ぎ目）。

検証用スクリプトは製品リポジトリの `tools/x32dbg/`。

## 6. 主な関数・データ（symbols.tsv に追加）

0x4EEA00 定義パーサー / 0x4EE470 ObjectDef構築 / 0x4EE560 FieldDef構築 / 0x4F0BE0 戦闘マップ読み込み / 0x4562D0 セル設定 / 0x456380 FieldData::vf07 / 0x4DF200 Block生成 / 0x4E5860・0x4E6110 飛び道具とBlock / 0x4E9470・0x4E9A20・0x4E9A60・0x4EA2E0・0x4EAA70・0x4EC1E0 通行グリッドと経路 / 0x4C1B70 座標→セル / 0x4FBE80 NewGameStage::vf02 / 0x4FBF40 NewGameStage::vf03 / 0x576DC0 Unit::vf25 / 0x423E80 チップ名→アトラス矩形。
