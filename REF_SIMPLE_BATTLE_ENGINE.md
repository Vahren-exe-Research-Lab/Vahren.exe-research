# 簡易戦闘（画面なしの戦闘）の仕様（解析中）

2026-11-12〜、Claude。原作 ver0.67（SHA256 `E8DAC301…767187`）の逆アセンブルと、観測モード（HakushinBattleSwap `mode=observe`）の実機記録から書く。
外部の戦闘で原作と同じ計算をするための仕様。差し替えの入口と出口は [REF_BATTLE_SWAP_HEADLESS.md](REF_BATTLE_SWAP_HEADLESS.md)。確かさは各項に書く（静的＝逆アセンブルのみ、実機＝記録と照合済み）。

## 0. 前提

- 浮動小数点：x87 の精度が 24 ビット（単精度）。中間値は float32 に丸めて計算する（実機：距離が float32 の値と一致）。
- 乱数：CRT rand。`s = s × 0x343FD + 0x269EC3 (mod 2^32)`、値 `(s >> 16) & 0x7FFF`。
  - `R(lo, hi) = lo + ftol(rand × 2^-15 × (hi − lo))`（0x40ED80）。ftol は 0 方向への切り捨て。
  - `P() = ftol(rand × 2^-15 × 100)`（0〜99、百分率の判定に使う形）。
- 定数は context.dat から読む（読み込み処理 `0x45A000..0x45C800` から作った表。研究者の手元）。このゲームの主な値：unit_action_bdr 4000、unit_search_bdr 100、unit_retreat_speed 300、unit_illusion_miss 66、unit_confusion_miss 25、btl_limit 1300、btl_min_damage 1。
- 戦場はマス目（32 px）。context `unit_battle_cram = on` で 1 マスに 1 体（地図の +0x3C が立つ）。

## 1. 1 フレーム（0x40E2F0）

```
for iter in 0..499:
    if iter % 50 == 0: 勝敗の判定（§1.1）
    if Event_ProcessBattleTick(E, 1): break        # 0x492D80
    防衛側・攻撃側の陣営 [side+0x90].vf+4          # 陣営の更新（未解析）
    for u in W.units (W+0x238 の順): u.vf+4          # §2 ユニットの更新
    0x4FAA60                                          # 後処理（未解析）
    W+0x248 の効果の更新、W+0x278 の新しい効果の登録、0x498EE0
    残り時間 W+0x288 -= 1                            # 実機：1 反復に 1
```

### 1.1 勝敗の判定（50 反復ごと）
- 攻撃側が残っていない（0x514C80）かつ W+0x28C ≤ 0 → 2（防衛側の勝ち）。
- 防衛側が残っていない かつ W+0x28C ≤ 0 → 1（攻撃側の勝ち）。
- 残り時間 ≤ 0 → 防衛側 vf+0x18 ≠ 4 なら 2、攻撃側 vf+0x18 == 4 なら 2、それ以外 1。
- 残り時間の初期値は btl_limit × 10（実機 13000、推定）。

## 2. ユニットの更新（SimpleUnit vf+4 = 0x545740）

```
if dead: return
gauge  += speed(+0xA8); gauge2 += speed; search += 1
if +0x1E55C > 0: +0x1E55C -= 1
+0x1E560 = 0
if moving(+0x186D4 != NONE): 移動を進める（§4.3）; return
if knock(+0x1E4E0 != 0): ノックバック（§4.4）; return
if not routed and +0xD4 >= 0: latch = TargetLatch(map, u)   # §3.1、毎反復 rand 1 回（cram のとき）
if Charge(u): return                                         # §5.2 突撃（+0x130 の技能）
if gauge < bdr:
    if latch == 0: IdleMove(u)                               # §4.1
    elif 条件: 0x57BBA0                                       # 未解析
    return
gauge = R(-bdr/10, 0)                                       # rand 1 回
+0x1E538, +0x1E54C, +0x1E558 を 1 減らす（+0x1E54C が 0 なら倍率 +0x1E550 = 1.0）
+0x1E540 の効果の一覧の残り時間を 1 減らす
SearchTarget(u)                                              # §3.2
if RouteCheck(u): return                                     # §6
… 移動の目標を決める（§4.2）
SkillDispatch(u, gauge2 >= bdr)                              # §5
if not moving: 0x57DD10; IdleMove(u)
if acted: NaturalRecovery(u)                                 # 0x57DF90
```
（実機：ゲージと探索カウンタの規則はスナップショットで全ユニット矛盾なし）

## 3. 目標

### 3.1 TargetLatch 0x4E53B0（隣の敵）
- cram のとき：`dir_order = rand×2^-15×2`（0 か 1）で、隣の 8 マスを調べる順番の表（0x65C03C / 0x65C05C、向き +0x18688 からの相対）を選ぶ。最初に見つかった「敵の種類の陣営」のユニット（+0x65 が立っている）を返す。
- 混乱（+0xC8 < 0）のときは先に `P() < unit_confusion_miss` で敵味方の判定を反転。
- cram でないとき：空間の区画で、`距離 < hand_range(+0x194) + 相手の半径 + 自分の半径` の敵を探す（乱数なし）。

### 3.2 SearchTarget 0x57B870
- `search < unit_search_bdr` なら、今の目標 +0x1E570 との距離だけ更新して終わり。
- 届いたら `search = R(-sbdr/10, sbdr/10)`。目標が無ければ `Ai_SelectNearestTarget`（0x514D60）で敵の陣営から最も近いユニット（stealth は `P() < stealth` のとき外す）。混乱なら確率で味方から。
- 結果を +0x1E574・+0x1E580（目標）、+0x1E578（距離、float32）に入れる。
- `max(attack_range, escape_range) ≥ 距離` なら +0x1A8 = 1。毒（+0xBC < 0）なら HP 減少。

## 4. 移動

### 4.1 IdleMove 0x57C600
- 行き先（+0x186C0/C4、+0x186C8/CC、追う相手 +0x186BC）か、経路の一覧（+0x186B0、+0x186B4 件）をたどる。
- 1 マスの向きを vf+0x78（0x5465F0、rand を使う）で決め、vf+0x74（0x544E10）で動く。
- +0x1868C は連続して動けた歩数（突撃の助走に使う）。

### 4.2 移動の目標 0x57D1D0（静的、要点）
- 目標が無い：ランダムな方向へ歩く（0x4208A0 で角度）。
- satellite（+0x1E594）：親との距離 +0x1E598 を保つ。
- free_move（+0x18618）：目標が attack_range より遠いとき、確率でランダムに動く。
- 目標が attack_range 以内：止まる（0x543DE0）。遠い：目標（または部隊の先頭の目標）を追う。

### 4.3 1 マスの移動 0x544E10
- 地形の値 v = vf+0x64()（0 なら動けない）。
- `s = clamp(v × 0.2 × move(+0xB0) × 倍率, 50, 2000) × 0.01`（px/反復）。
- 所要反復 `+0x186D8 = clamp(ftol(距離/s + 0.5), 1, 198)`。位置は移動の始めに行き先へ書き換える。
- 実機：主力は 1 マス 12 反復。

### 4.4 ノックバック
- 残り距離 +0x1E4E0、向き +0x1E4E8、8 方向の表 0x62A288 で 1 マスずつ押す。|残り| ≤ 16 で終わり。

## 5. 行動

### 5.1 SkillDispatch 0x545CC0
- `gauge2 ≥ bdr` で、gauge2 = 0。技能の一覧（+0x18650、std::list）から使えるものを選び、func（スキル +0x40）で分ける：1 近接（vf+0x7C = 0x546C90）、2 射撃（0x546F70）、3 回復（0x547AF0 ほか）、4 召喚。

### 5.2 突撃 0x546A30
- 突撃の技能 +0x130 があり、目標があり、連続の歩数 +0x1868C ≥ 技能の +0x2B4、向きが目標の方向と 2 以内なら、その場でダメージ（0x550E70）。歩数を減らす。

### 5.3 近接 0x546C90
- 向きを目標へ。MP −= mp。幻覚（+0xCC < 0）なら `R(0,100) < unit_illusion_miss` で外れ。
- rush 回（0 なら 1）：damage ≥ 0 かつ str ≠ 0 なら 0x550E70 でダメージ。next 系の技能を続けて出す（0x547FC0）。

### 5.4 ダメージ 0x550E70
- 既存研究 T012（`data/T012_BATTLE_CALC.md` §3・§4）を正とする。攻撃側 = 能力値（str のモード）× damage_consti[耐性] × 乱数（damage_min..max）、防御側 = 防御 × 別の乱数（damage_min2..max2）。差を取り、距離の補正、耐性 0/10 の特別扱い、btl_min_damage。

## 6. 潰走 0x57DBB0
- `HP/maxHP ≤ +0x18608` で潰走（+0x1867E = 1、移動の速さ ×unit_retreat_speed/100）。潰走中は `> +0x18608 × 1.2` で立ち直る。

## 7. 戦死 0x544790
- `HP −= ダメージ`、0 以下で：撃破の報酬、break（死亡時スキル）、生存判定 0x588470、vf+0x58（除去）、dead_event（その場で実行。あとから呼んだものが先に動く、実機）。

## 8. ユニットのフィールド（主なもの）
| オフセット | 内容 | 確かさ |
|---|---|---|
| +0x90/+0x94 | HP / MP | 実機 |
| +0x98/+0x9C/+0xA0 | 攻撃 / 防御 / 魔力（の順と見られる） | 実機（値） |
| +0xA8 | 速さ（行動ゲージの増分） | 実機 |
| +0xB0 / +0x1B0 | 移動（現在 / 基本） | 静的 |
| +0xBC..+0xD4 | 7 つの状態ゲージ（毒・麻痺・沈黙などと見られる） | 静的（T012 §6） |
| +0xDC/+0xE0 | 最大HP / 最大MP | 実機 |
| +0x130 | 突撃の技能 | 静的 |
| +0x188/+0x18C/+0x194 | attack_range / escape_range / hand_range | 静的（定義の対応表） |
| +0x214/+0x218 | 位置（マスの中心） | 実機 |
| +0x228 | 半径 | 静的 |
| +0x18608 | 潰走の HP 割合（double） | 静的 |
| +0x18650 | 技能の一覧（std::list） | 静的 |
| +0x1867C/+0x1867E/+0x18680 | 死亡 / 潰走 / 撤退 | 静的・実機 |
| +0x18688 | 向き（0..7） | 静的 |
| +0x1868C | 連続の歩数 | 静的 |
| +0x186D4/+0x186D8 | 移動の進み / 所要反復 | 実機 |
| +0x1E52C/+0x1E530 | 行動ゲージ（2 本） | 実機 |
| +0x1E534 | 探索カウンタ | 実機 |
| +0x1E570/+0x1E574/+0x1E580 | 隣の敵 / 目標 | 実機 |
| +0x1E578 | 目標までの距離（float32） | 実機 |

## 9. ダメージの詳細（0x550E70、静的、2026-11-12 読み直し）
```
res = 相手の consti（+0x13C の map）からスキルの attr（+0x110）の値、0..10 に丸め。attr 無し・見つからない → 5
c1  = damage_min + rand×2^-15 × (damage_max − damage_min)          # rand 1 回。このゲームは 0.8..1.2
atk = ftol(Strength(攻撃者, スキル) × consti[res] × c1 + 0.5)
def = str のモード 1/4 → 相手 +0x9C、2/5 → 相手 +0xA4、3 → (+0x9C + +0xA4)/2、6・その他 → 0
c2  = damage_min + rand×2^-15 × (damage_max − damage_min)          # rand 1 回。**damage_min2/max2 ではない**
dmg = atk − ftol(c2 × def + 0.5)
mode 6（fix）: dmg = ftol(scale × 100 + 0.5)
damage_range_adjust（+0x250）≠ 0: f = clamp((range − 距離)/(range − adjust), 0, 1)、dmg = ftol(f × dmg + 0.5)
res 10 → ダメージを与えない
scale（+0x280）== 0 → 0 を与える
mode 6 → dmg（最低値なし）
res 0 → 1000000
相手が潰走中 → dmg = ftol(dmg × unit_retreat_damage/100)
dmg = max(dmg, btl_min_damage)
相手.vf+0x70(dmg, 攻撃者, スキル, 旗) → Hit_LinkedAward 0x551E50 → flash → 状態異常（add_per +0x230 の確率、damage_min2/max2 はここで使う）
```
- Strength 0x550D80（スキル +0x27C のモード、+0x280 = str の値 × 0.01、+0x288 = str_ratio × 0.01）:
  - 1 attack: ftol(攻撃 +0x98 × scale + 0.5)、2 magic: 魔力 +0xA0、3 attack_magic: (攻撃×ratio + 魔力×(1−ratio)) × scale、4 attack_dext: (攻撃×ratio + 技 +0xAC×(1−ratio))、5 magic_dext: (魔力×ratio + 技×(1−ratio))、6 fix。
- 既存研究 T012 §3 と一致（防御側の乱数も damage_min..max）。研究日誌（非公開）§97.25 の「damage_min2..max2」は誤り（status 側 0x5513xx・0x5518xx が使う）。
- 外部の計算での実装は研究者の手元にある（未照合。多種ユニットの記録で照合する）。

## 10. スキルの連鎖と飛び道具（静的、途中）
- skillset（`skillset a_zan { member = zan0,zan1 }` など、48 個）はスキル名の束。クラスの skill に書かれ、メンバーに展開される。
- 一般兵の近接 a_zan = zan0（func sword、str attack*0、next = zan0_joi）＋ zan1（func missile、range 80、rush 2、str attack*0、next2 = zan1_nt0,zan0_joi2）。実際のダメージは next 側のスキルが出す。
- `SimpleUnit_CastSkill` 0x547FC0（0x2188 バイト）は "class SimpleMissile" のオブジェクトを作る。簡易戦闘にも飛び道具のオブジェクトがあり、1 反復の手順 5（W+0x248 の木の vf+4）で更新される。

## 11. 飛び道具 SimpleMissile（静的、途中）
- RTTI から vtable を特定した（`.?AVSimpleMissile@@` → COL 0x63F76C → vtable **0x63A5A4**）。更新 vf+4 = **0x552030**（0xE25 バイト）。通常戦闘の Missile は vtable 0x63A544、更新 0x54BA00。
  - 同じ方法で SimpleUnit 0x63A4BC（更新 0x545740）、Unit 0x63A9E4（更新 0x57AA00）も確かめた。
- 作られ方：`SimpleUnit_CastSkill`（0x547FC0）が、簡易戦闘のとき（型名で判定）`0x40E670` で戦況ウィンドウの W+0x268（新しい飛び道具の一覧）に積む。1 反復の手順 7 の `0x498EE0(W+0x248, [W+0x268], [W+0x26C])` が、それを W+0x248（動いている飛び道具の集合）に入れる。
- 主なフィールド：+0x78 撃ったユニット、+0xB0 スキル、+0xA8 W、+0x180・+0x1A4 経過反復、+0x1A0 待ち（スキルの wait_time +0x23C まで待つ）、+0xF8 終わり（立つと次の反復で `0x40E700` が W+0x278 の削除の一覧に積む）。
- 1 反復（0x552030）の流れ：
  1. 終わっていれば、削除の一覧へ（offset_on のときは陣営の一覧からも外す）。
  2. wait_time まで待つ。
  3. resize 系（大きさの変化。当たり判定の矩形 +0x40〜+0x4C も変わる）。
  4. 移動（homing +0x1D8 などで向きを変え、0x4C5A40 で進める）。
  5. 経過 +0x1A4 がスキルの time（+0x2B0）を超えたら終わり（next_last なら次のスキル）。next_interval（+0x274）ごとに次のスキル（vf+0x58）。
  6. **当たり**：hard（+0x1C4）が 0 でなければ「経過 % hard == 0」のとき、0 なら経過 == damage(+0x24C)+1 のときだけ判定する。
     - bom でない：`0x4E5860` で最初に当たったユニット。+0x66 が立っていれば（壁など）止まる。そうでなければ **`0x54DAE0`**（ダメージを与える。既存研究 T012 の DAMAGE_CALLER_54DAE0）。
     - bom：`0x4E6110` で範囲内の全ユニットに `0x54DAE0`。
  7. 終わりの演出・乱数での散らばり（Rng_RangeInclusive 3 か所、0x4208A0）など。
- 一般兵の近接 a_zan の zan1 は func missile（range 80、rush 2、damage −3、next2）なので、**近接攻撃の多くもこの飛び道具の経路を通る**。
