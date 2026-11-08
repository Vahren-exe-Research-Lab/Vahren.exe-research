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
4. セル（`FieldData`、0x11C バイト）は描画オブジェクトで、テクスチャ座標（チップ画像の位置）を **+0x6C〜+0x80** に持つ。毎フレーム、表示範囲のセルを列挙（NewGameStage::vf03）→ 各セルの FieldData::vf07 が +0x6C の値から頂点を作る。よって **この6値を書き換えれば次の描画からチップの見た目が変わる**（アニメーション・途中変更の土台）。［**実機確認 2026-11-09**: 戦闘中に x32dbg で 7×7 マスの +0x6C〜+0x80 を別セルの値に書き換えると、草原が水の絵に即座に変わった。attr・通行判定は変えず見た目だけ変わる］
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
- 0x4EA2E0 → 0x4E9A60: 通れるマスを長方形の領域に分け、経路探索のグラフを作る。引数は grid 1個（スタック渡し、呼出側 `push grid; call`）。読込関数内の呼出は 0x4F1439 と 0x4F320B の**2か所だが分岐の別経路で、1回の読込で呼ばれるのは1回**。［静的確認］
- **戦闘中の再構築（V3）の静的評価**: 0x4EA2E0 は新しい領域を作って通れるマスの `+0x64`（領域番号）と `+0x68`（領域ノード）を上書きするだけで、**前の領域ノードは解放しない**（一時木だけ解放）。よって再実行しても古いポインタがぶら下がる（解放済みを指す）ことは無いが、メモリは少し漏れる。通行不可になったマスの `+0x64/+0x68` は古い値のまま残るため、再構築前に全マスを `+0x64=0x80000008`、`+0x68=0` に戻す（0x4E9470 の初期化と同じ値、`+0x60` は保つ）必要がある。経路キャッシュ（0x4EC1E0 側）が古い領域の組を保持し続ける可能性があり、塞いだ道を通ろうとする恐れは残る → 実機確認は DLL の段階 M6 で行う。［静的確認／実機未確認］
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

- ~~V1~~: **確認済み**（2026-11-09、OGGテストのコピー、スクリプト map_v1b.txt）。vf07 は描画のたびに表示中のセルについて呼ばれ、書換えは即時反映。
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
