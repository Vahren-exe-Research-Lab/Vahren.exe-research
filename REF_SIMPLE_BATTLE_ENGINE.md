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
    W.units.insert(end, W+0x258..0x25C)               # 0x4FAA60：この反復で生まれたユニット（召喚など）を末尾に足す
    for m in W+0x248（飛び道具の集合、std::set の順）: m.vf+4    # §11
    for m in W+0x278（終わった飛び道具）: W+0x248 から外す      # 0x579AA0 で探して 0x510850 で消す
    W+0x248 に W+0x268..0x26C（この反復で作られた飛び道具）を入れる   # 0x498EE0
    W+0x258・W+0x268・W+0x278 を空にする
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
first = False                                                # 接敵したての先制
if steps(+0x1868C) > 0:
    if +0x1A4 == 0: first = (latch != 0)
    elif +0x134 and R(0,100) < +0x18600: first = (latch != 0)   # rand 1 回
if Charge(u): return                                         # §5.2 突撃（+0x130 の技能）
if gauge < bdr:
    if latch == 0: IdleMove(u)                               # §4.1
    elif first: MeleeNow(u)                                   # 0x57BBA0：近接の技能（func 1、special なし）をゲージと関係なく出す
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
（実機：**移動中のユニットは乱数を使わない、止まっているユニットは 1 回**。スナップショットの次の反復の乱数の回数と照合して、移動中 23 件はすべて 0 回、停止中 85 件はすべて 1 回。移動中はゲージが閾値を超えても行動しない）

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
- `gauge2 ≥ bdr` でなければ何もしない。届いたら gauge2 = 0。
- 待ち +0x1E538 > 0、または +0xD0 < 0（状態異常と見られる）なら使わない。+0x1AC = 0。
- **近接の優先**：+0x1A4 ≠ 0 かつ +0x134 が立ち、隣の敵（+0x1E570）がいるとき、`R(0,100) < +0x18600` なら、技能の一覧を先頭から見て、special（+0x4C）> 0 なら 0x57BC10 で使えるか確かめ、func = 1（sword）なら vf+0x7C で近接を出す。
- **ふつうの選び方**：技能の一覧（+0x18650、std::list、並びは作るときの順）を先頭から見る。陣営の種類（[+0x1D4]+0xC）が 2 なら +0xA0C、それ以外は +0xA10 の値を使い、0x80000065 より大きいもの（使える技能）だけを試す。special > 0 なら 0x57BC10 も通す。func で分ける（ジャンプ表 0x5465D4）:
  - 1 sword → vf+0x7C（0x546C90）
  - 2 missile → `Skill_ExecuteMissile`（0x546F70、§5.5）
  - 3 heal → 隣の敵がいて range_min ≠ 0 なら使わない。allfunc なら `Skill_ExecuteHealAllTargets`（0x547AF0）。そうでなければ支援の対象の一覧（+0x1E584..）から選ぶ（0x54ADA0・0x54A170・0x54A5F0・0x54A1C0・0x54A7B0）。
  - 4 summon → 0x546466 側（未解析）
- **最初に成功した 1 つだけ**使う。成功したら：
  - 減速 `+0x1E54C = slow_time`（+0x208）、`+0x1E550 = slow_per`（+0x200）。今の残りより長いときだけ。
  - delay（+0x20C）> 0 なら待ち `+0x1E538 = delay + 1`。
  - gun_delay（+0x210）> 0 なら、技能ごとの待ちの表（+0x1E53C、キー = +0x214 の名前）に gun_delay + 1 を入れる（§2 の「+0x1E540 の一覧の残り時間を 1 減らす」はこの表）。

### 5.2 突撃 0x546A30
- 突撃の技能 +0x130 があり、目標があり、連続の歩数 +0x1868C ≥ 技能の +0x2B4、向きが目標の方向と 2 以内なら、その場でダメージ（0x550E70）。歩数を減らす。

### 5.3 近接 0x546C90
- 向きを目標へ。MP −= mp。幻覚（+0xCC < 0）なら `R(0,100) < unit_illusion_miss` で外れ。
- rush 回（0 なら 1）：damage ≥ 0 かつ str ≠ 0 なら 0x550E70 でダメージ。next 系の技能を続けて出す（0x547FC0）。

### 5.5 射撃 0x546F70（func 2）
- 隣の敵がいて range_min（+0x298）≠ 0 なら使わない。allfunc なら `Skill_ExecuteMissileAllTargets`（0x547DB0）。
- 目標（+0x1E574）が要る。状態異常 +0xC0 < 0 で mp = 0 の技能、+0xC4 < 0 で mp ≠ 0 の技能は使えない。MP が足りなければ使えない。技能の待ち（+0x1E53C の表）が残っていれば使えない。
- 距離（当たり判定の矩形の中心どうし）が `range_min < 距離 ≤ check`（+0x294）のときだけ。
- 向きを目標へ（0x447180）。技能の +0x2D0 == 7 なら向きは変えない。
- 味方が射線にいないか `Skill_CheckMissileRangeGate`（0x4E7ED0）で調べる。結果はその反復のあいだ +0x1E560 に残す（1 = 撃てる、2 = だめ）。+0x1FC が立つ技能などは調べない。
- MP −= mp。offset（+0x254）があれば撃つ位置をずらす（vf+0x80）。rush（+0x74）回、`SimpleUnit_CastSkill`（0x547FC0）で飛び道具を作る（§11）。

### 5.4 ダメージ 0x550E70
- 既存研究 T012（`data/T012_BATTLE_CALC.md` §3・§4）を正とする。攻撃側 = 能力値（str のモード）× damage_consti[耐性] × 乱数（damage_min..max）、防御側 = 防御 × 別の乱数（damage_min2..max2）。差を取り、距離の補正、耐性 0/10 の特別扱い、btl_min_damage。

## 5.6 行動のあとの回復 0x57DF90
- HP += hprec（+0xB4）。ただし毒（+0xBC < 0）で hprec ≥ 0 のとき、HP が最大を超えていて hprec ≥ 0 のときは足さない。最大HP（+0xDC）で頭打ち。負になったら vf+0x70 で倒れる。
- MP += mprec（+0xB8）。沈黙（+0xC4 < 0）で mprec ≥ 0 のときは足さない。0..最大MP（+0xE0）。
- 7 つの状態ゲージ（+0xBC・+0xC0・+0xC4・+0xC8・+0xCC・+0xD0・+0xD4）に unit_status_recovery（0x65BD58）を足し、unit_status_hp_limit（0x65BCFC）で頭打ち。負の値が状態異常の残り（毒 +0xBC、移動不可 +0xC0、沈黙 +0xC4、混乱 +0xC8、幻覚 +0xCC、行動不可 +0xD0、目標の固定不可 +0xD4 と見られる。名前は使われ方からの推定）。
- 最後に 0x578EF0。

## 5.7 距離を取る 0x57DD10（cavalry_range）
- cavalry_range（+0x198）があり、目標がいて、隣の敵がいないとき、目標との距離が cavalry_range 未満なら、目標と反対の方向へ escape_run（+0x190）× 2 の位置を行き先にする（弓兵などが離れる動き）。+0x1E55C > 0 の間はしない。

## 6. 潰走 0x57DBB0
- `HP/maxHP ≤ +0x18608` で潰走（+0x1867E = 1、移動の速さ ×unit_retreat_speed/100）。潰走中は `> +0x18608 × 1.2` で立ち直る。

## 7. 戦死 0x544790
- `HP −= ダメージ`。0 より大きければ、ノックバック（攻撃者の knock、相手の no_knock +0x1E4DC と乱数）、被弾時の技能（+0x1B0）などで終わり。
- 0 以下で：
  1. 部隊に入っているユニットを、部隊の主のいる攻撃者が倒したなら、倒されたユニットの UnitData +0x1C4 を、攻撃者の部隊の +0xBC と主の +0x1B4 に足す（撃破の報酬、0x5449C0..）。
  2. break（死亡時スキル）。def の "lost_reserve" の確率で別の技能。W+0x28C（両軍の全滅判定の猶予）を lost_reserve（無ければ 10）にする。
  3. **0x588470（死亡の扱いの判定）**：たまった経験値でレベルを上げきり（unit_level_max まで）、`経験値 ×= dead_penalty/100`、勢力の資金から「価格 × レベル」を引く。シナリオ変数 `@mode_dead2`・`@mode_dead` と、人材なら `rand% ≥ 生存率`（0x585890 の値）で、本当に死ぬかを決める。結果を UnitData +0x1B0 に入れる。
  4. 部隊の主なら、部隊の技能（+0x184）を出す。
  5. vf+0x58（除去）。dead_event（REF_BATTLE_SWAP_HEADLESS.md §5.2：その場で実行、あとから呼んだものが先に動く）。
- 召喚（func 4）は `Summon_ProcessSkillKind4`（0x547490）。既存研究 REF_UNIT_EXP_SUMMON.md を参照。

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
- 既存研究 T012 §3 と一致（防御側の乱数も damage_min..max）。研究日誌（非公開）の以前の記述「damage_min2..max2」は誤り（status 側 0x5513xx・0x5518xx が使う）。
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

## 12. 戦闘のクラスと更新関数（RTTI から、静的）
| クラス | vtable | 更新 vf+4 | 備考 |
|---|---|---|---|
| SimpleUnit | 0x63A4BC | 0x545740 | 簡易戦闘のユニット |
| Unit | 0x63A9E4 | 0x57AA00 | 通常戦闘のユニット |
| SimpleMissile | 0x63A5A4 | 0x552030 | 簡易戦闘の飛び道具 |
| Missile | 0x63A544 | 0x54BA00 | 通常戦闘の飛び道具 |
| RushMissile | 0x63A6B4 | 0x5501A0 | rush の飛び道具 |
| Heal | 0x63A604 | 0x54E420 | 回復の効果 |
| SummonFlash | 0x63A65C | 0x54F490 | 召喚の効果 |
| SimpleStaticUnit | 0x63A8E4 | 0x55AD80 | 簡易戦闘の建物（城・砦など） |
| StaticUnit | 0x63A85C | 0x55AD80 | 通常戦闘の建物 |
| Troop | 0x639A30 | 0x56AB20 | 部隊 |
| Person | 0x6396E0 | 0x5149C0 | 陣営の基底 |
| Enemy | 0x638B60（+0x90 の部分 0x638B84） | +0x90 の vf+4 = **0x4498E0** | AI の陣営。1 反復の手順「陣営の更新」 |
| Player | 0x639B08（+0x90 の部分 0x639B2C） | 0x521A00 | プレイヤーの陣営 |
| DemoPerson | 0x638030（+0x90 の部分 0x638054） | 0x449730 | |
| BattleWnd | 0x638074（+0x28 の部分 0x6380CC） | 0x40E220 | 戦況ウィンドウ |

- 陣営の更新 0x4498E0（Enemy）：0x140 反復ごとに `Ai_RebuildLiveUnitScoreMap`（0x5151D0）と `ModeScoreRank_Process`（0x448E90）で作戦のモードを選び直す。主将の kosen、context の btl_mode_coe・btl_attackmode・btl_chargemode を使う。既存研究 REF_BATTLE_AI_MORALE.md（T013・T024・T028）がこの部分にあたる。

## 13. 戦闘開始時の準備と配置（0x40F320 → 0x410420、静的）
- 0x40F320（SimpleBattle の準備）:
  1. 前の戦闘の陣営と表を片付ける（0x40F000、0x48ABF0）。
  2. 両陣営の部隊（Troop、0x567EE0）と SimpleUnit（`Battle_CreateSimpleUnit` 0x544290）を作る。人材は `UnitData_FindPersistentRecord`（0x467DE0）。
  3. **全ユニットの一覧 W+0x238 を random_shuffle（0x501CA0）で混ぜる**（rand を使う。1 反復でユニットを更新する順番はこの並び）。
  4. 戦場の地図を読む（0x4F0BE0、E+0x1EF570。地図名は目標の拠点の +0x2C）。戦場の矩形を E+0x1EF164..0x1EF170 に写す。
  5. マス目の占有表を作る（0x4E4B30）。地図の物（+0x65 か +0x67 が立つもの）を 0x4E4DC0 で置く。
  6. **配置 0x410420**。
  7. `Event_InitializeBattleClock`（0x492710）の値 × 10 を W+0x288（残り時間）に入れる。W+0x28C = 0。
  8. 両陣営の vf+0xC（陣営の準備）。
- **0x410420（配置）**:
  - 戦場の中心 (cx, cy) と、半幅 `t = ftol(|幅|/2 × 0.75 + 0.5)`、半高 `ftol(|高さ|/2 × 0.75 + 0.5)`、その比 r。
  - **攻め込んだ側**は、出発した拠点ごとにまとまる（W+0x20C の木）。出発の拠点と目標の拠点の戦略地図での座標（`x`・`y`）の差から、atan2 で 8 方向 d を決める（同じ位置なら `rand×2^-15×8`）。
    - 角度 `(d+2)×45°`（×0.017453293）の方向へ、中心から `x = cx + ftol(cos×t + 0.5)`、`y = cy + ftol(ftol(−sin×t + 0.5) × r + 0.5)` の位置に、その拠点の部隊を全部置く。部隊の向きは `(d+4) & 7`（中心を向く）。
  - **守る側**は、地図の守りの位置の一覧（地図 +0x180）が無ければ、向きを `rand×2^-15×8`（攻め込んだ側の向きがあればそれ）にして、全部隊を中心に置く。一覧があれば別の手順（未解析）。
  - 部隊ごとの置き方は `Troop_Place`（0x56A790、部隊・x・y・角度）:
    - 隊列の種類 troop+0x30（1 = 横一列で幅 troop+0x38、2・その他 = 人数の平方根の切り上げ列）。
    - 隊列の位置を **D3DX の `D3DXMatrixRotationZ`・`D3DXVec3TransformCoord`**（d3dx9_35.dll）で回す。
    - 各ユニットを 0x56A0B0 で置く（占有表 0x4E5040 で空いているマスを探す）。列の間隔は cram のとき 32、そうでなければ半径 +0x228 の 2 倍。
  - 外部の計算での注意：回転に d3dx9_35.dll の関数を使っているので、同じ DLL を使うか、その数値の出方をまねる必要がある（ゲームに同梱）。定数 π は float32 の値（0x62A190 = 3.1415927410125732）。

## 14. 1 マスの向き vf+0x78（SimpleUnit 0x5465F0、静的、途中）
- +0x18698 > 0 なら 1 減らして待つ。
- 行き先への atan2 から 8 方向 d を決め、そのマス（表 0x62A288 × 32）が空いていれば（0x4E5040 == 1）その向きに進む（+0x18690 = 0、向き +0x18688 = d）。
- 空いていなければ 2 回まで待つ（+0x18690）。それでもだめなら、今の向きのマス、さらに周りの向き（+0x18694 の横よけの形）を試す。
