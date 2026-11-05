# ON-AI-001｜迫真戦記ver0.67 戦闘AI構成／DATとEXEの責任分界（2026-10-25）

作成日：2026-10-25 JST。所有：ONDISKストーリー研究。STATIC SOURCE/KNOWN NATIVE。原作実機での行動再現・Golden = NOT RUN。
原作製品DAT/EXE、研究B・T013、dev_lab既存エンジンのコード/他担当資料は読み取りのみ。新しく逆コンパイルやEXEの再インポートはしていない。

## 要点／ユーザーの用途
迫真戦記のCPU戦闘AIは「一つのDATではない」。原作EXEに備わる (a)ユニット単位の近傍探索/標的更新/移動/技能選択/戦闘処理、DATに記述した (b)context/unit/class/skillによるパラメータと技能構成、(c)「Ai戦闘制御_*」の上位指揮イベントと動的スキル差替え、(d)勢力/専用ボスイベントが重なる。
新規スタンドAIは新規AIシステムを自作するより、戦闘開始自動召喚、satellite、専用技能、ボスイベントを優先利用する。厳密な絶対射程/共有HPは別。

## 1. 迫真戦記 context.dat の原本値
現物：`a_default/script/context.dat` L145-173/179-206。
- `unit_action_bdr=4000`、`unit_search_bdr=100`
- `unit_attack_range=600`、`unit_escape_range=350`、`unit_escape_run=100`、`unit_hand_range=16`、`unit_view_range=16`
- `unit_specialuse_per=80`、`unit_use_coe=90`、`unit_keep_form=on`
- `unit_retreat_damage=50`、`unit_retreat_speed=300`、`unit_confusion_miss=25`
- `unit_element_heal=on`、`unit_summon_min=0`、`btl_min_damage=1`、`btl_unitmax=810`
- `btl_attackmode=100`, `btl_chargemode=80`, `btl_standby=25`, `btl_counter=80`, `btl_intercept=50` 等もあるが全ての人間向け効果と内部消費を確定していない。
- Wiki `unit` では speed の蓄積が `unit_action_bdr` に達すると行動、とされる（推定表現あり）；時刻秒との一対一は保証しない。

## 2. 原作EXEの通常AIループ（既存T013保存研究）
正本：`_REDEV_RESEARCH/data/T013_AI.md`、`data/T013_WORK_NORMAL_AI_CONTRACT_20261012.md`（研究B所有・read-only）。デコンパイル統合V9 DB：`_REDEV_RESEARCH/rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`（read-only）。
既存dev_labの部分実装：`src/hakushin_compat/native_unit_ai.py` と `native_unit_movement.py`（今回不変更）。これらは部分的な境界一致であり全通常AI/実機等価ではない。

| 関数/entry | 保存命令で確認した役割 | 確度/留保 |
|---|---|---|
| `0x57AD56`付近 | Unit更新ループから、近傍探索→技能試行→副技能試行への分岐 | 局所CFG確定、全calleeは未確定 |
| `0x4E53B0` | 衝突グリッド／空間bucketから付近候補を先着判定で取得 | 実際の探索が必ず最短とは限らない。候補の有効性/陣営条件 |
| `0x57B870` | 探索カウンタ、広域標的再探索、attack/support cache構築 | 近傍探索とは別。RNG/通常経路確認済、全分岐未解決 |
| `0x514D60` | primary SimpleUnitとfallback SimpleStaticUnitの距離候補を走査 | 単一全リスト最短選択とは異なる。nearest tieは先着 |
| `0x514F10` | 回復・補助用の別候補vectorを構築 | 攻撃標的と混同禁止 |
| `0x57E4E0` | Unit+0x18638から選択技能、種類/状態/探索/発動を判定 | 技能の完全優先順位、実効果の全詳細はVERIFY |
| `0x57E1D0` | Unit+0x130側の別技能候補、標的・距離等のgate | 主技能候補と混同禁止 |
| `0x57C600` | 通常移動指示・追尾対象位置を取得し経路/方向処理へ | 経路生成・地形/壁の全動作はVERIFY |
| `0x57D1D0` | satelliteで設定した親/術者への追従移動の処理候補 | 静的参照確定、ハードな最大射程ではない |

### 探索カウンタ
`unit_search_bdr` は原本100。通常更新で Unit+0x1E534を増加し、しきい値到達時にreset-jitter（おおむね-10..9）と再探索を行う。概ね91..110回の該当Unit更新ごとであり、**91..110フレーム／秒ではない**。特殊技能による強制更新も存在する。
近傍探索`4E53B0`は最初に条件合格した対象を返す経路を持ち、全体 selector`514D60`はprimaryとfallbackの距離比較。**どちらも単純な毎frame「全敵の最短1体」ではない。**

### 標的優先／ステルス／混乱
- `0x514D60` primary（SimpleUnit、owner+0x48 vector）とfallback（SimpleStaticUnit、owner+0x58 vector）を別に走査。距離が同じなら通常は先に列挙された候補を保持。
- primary候補に `stealth` 乱数除外。例`stealth=80`で約80%のprimary除外。fallbackは同じ除外を持たない。完全不可視とは断定しない。
- 混乱の状態・`unit_confusion_miss`に応じ、通常の敵ターゲットpoolと補助用味方poolが確率で反転する分岐が存在。現原本の閾値は25。
- `unit_element_heal=on`の支援候補処理は、召喚Unitも回復候補にできるようfilterを変える。スタンドが回復可能になる可能性があるが、親子HP共有の二重回復に注意。

### 回復・技能
- heal/care/powerupは攻撃候補とは別の候補リストを使う。MP・射程・状態などによるフィルタあり。
- T013保存nativeのSkill+0xA18/0xA1Cコールバック：HP/MPの回復候補は現在／最大比率の小さい順で、同率は距離順。能力上昇は現在値の大きい順・同値は距離順。状態治療は状態に応じ除外し、距離で比較。特定経路では先頭4候補のshuffleがある。全ての回復技能へ無条件に適用してはいけない。
- `skill`/ `skill2`/ `delskill`/ `learn` が実際の所持技能を決める。`special`, `mp`, `range`, `check`, `far`, `gun_delay`, `delay`が発動条件を制約。技能アイコンの`sortkey`は原則UI表示順、全行動AIの優先スコアではない。
- Skill連鎖`next`/`next2`/`next3`/`pair_next`などは一技能の攻撃処理であり、これを戦闘AIの意思決定と同一視しない。
- 選択済みSkillと副候補でUnitの異なるフィールド（+18638と+130）を参照する。下位callee未解明なので完全な発動優先順位はUNKNOWN。

## 3. CPU編隊制御の本編DAT
`a_default/script/Ai戦闘制御_軍楽隊なし版.dat` 全3707行。大きな`story change_form`／`story change_form_battle`（307行）／`event form_inbattle`（2143行）から成る。CPU/シナリオ/難易度・ボス等条件で全機能ON・簡易版に分岐。
- 戦闘開始：`storeRectUnit(red/blue)`で両軍取得、`shuffle`、勢力/リーダー区分、CPU赤青判定、指揮官を前衛・騎兵・砲兵と左右中央のグループへ分類。
- `Ai戦闘制御_追加部分.dat`：冒頭コメントは戦闘イベント関数を使える人物リーダーに限定する問題のため、一般兵リーダーの擬似入替／管理を説明。必ずしも戦闘中の判断コードではない。
- `Ai戦闘制御_速度・待機スキル.dat` 155行：`form_slow90..10`、`form_dash`、`a_wait1000_*` は歩調を揃える減速・待機と、終盤のガン逃げ防止加速。
- `Ai戦闘制御_入れ替え必殺技.dat` 895行：CPUにスキルを出し惜しみさせる`wait_*`と距離・冷却調整済み`com_*`。本編AI側で`removeSkill`→`addSkill`等の差替えを行う。
- **ONDISKの固有例**：軍楽隊なし版 L1155-1161で `sp_ondisk` を`wait_ondisk`/`com_ondisk`に置換する。定義は入替必殺技DAT L284-290（`gun_delay=sp_ondisk*9`待機→`sp_ondisk*1`本技能）。`sp_world_ondisk`や新スタンドには自動適用しない。
- `form_inbattle` は時間>=30で左右中央の戦力全滅を検査し、`rif(isInterval(285/345))`で経過時間に応じ定期再編。`smoveTroop()`が207行にあり指揮官への直線移動指示。通常の地形回避とは異なるので障害物と衝突のおそれ。
- 残り時間<500、攻撃側cpu_red条件で`form_gannnigeboushi`：`form_dash`加速技能を付加し待機/鈍足技能を外す。時間切れ攻撃遅延に対するルール。
- `scenario1.dat` L29は`fight=fev1`、`100_イベント汎用/event_battle.dat`は戦闘全般の定型イベント。`story fight=on`を持つ独立拡張も存在。
- CPU指揮DATの処理は状況依存であり、全戦闘で一律発動するわけではない。人材、ボス、プレイヤー操作、ゲームモードの分岐と競合に注意。

## 4. 移動・追従・スタンド
- `class/unit satellite=数値`は自動追従。原作に32個の宣言例（召喚スキル `s_monaka`→`mona0071 satellite=30` と `achamo=50`など）。
- V9保存擬似Cで文字列`satellite`参照3つは`FUN_00571B70`、Unit+0x1E594が追従対象候補、+0x1E598距離設定。消費`FUN_0057D1D0`。追従ロジックがDATではなく原作EXE側にあることを示す。
- `moveTroop()`は追尾しつつ攻撃可、`moveTroopFix()`は攻撃をせず強行移動、`smoveTroop()`は直線移動。これらは「無限距離を超えない移動禁止」を保証しない。
- スタンド通常移動には`satellite`を基本に選ぶ。ただし`yorozu=troop3`のプレイヤー直接操作との優先関係、術者移動/壁/敵追跡時の最大距離、AI命令によるoverrideはLIVE NEED。
- 「スタンドは普通の人間の物理攻撃無効、スタンド自身は物理攻撃可能、敵スタンドにも有効」はユーザー確定。専用`standhit`属性＋ghost型物理耐性のSTATIC試作済み。共有HPと最大射程のハード拘束はDAT単独未実証。
- さらにCPUは`unit_element_heal=on`のため、召喚体への回復判定を行う。スタンドと本体のHP共有実装で重複回復が起きないか検証すべき。

## 5. スタンドAIへの実装提案（変更未実施）
優先度1. DAT単独：開幕強制召喚／standhit専用攻撃／`satellite=50..80`／`element_lost=on`／必要ならCPU専用wait/comスキルで必殺技を温存。元本体`starchira`を無断変更しない。
優先度2. DATの独立`story fight=on` + `battleEvent`でボス固有の強制スキル・段階・奪取演出。CPU全軍陣形DATへ横断追加するより干渉が少ない。
優先度3. 独立試験で、CPU術者の停滞/移動、召喚1/2体、半径R境界、ボスがスタンドを奪った時のenemy-side追従対象・復活、手動操作と衛星追従の競合を実測。
優先度4. もし厳密な「半径Rを越す移動は禁止」「親子正本HP共有」を実現できないなら、最小DLL hookまたは新戦闘側adapterに移す（owner identity、毎frame移動、damage/recovery、death）。DATで似せただけを完成扱いしない。

## 確定事項と未解決
CONFIRMED ORIGINAL DAT: 上記ファイル・行/数値、`form`、スキル差替え、`satellite`実使用。
CONFIRMED SAVED NATIVE (STATIC): 0x4E53B0/57B870/514D60/514F10/57E4E0/57E1D0/57C600、T013のキャッシュ・乱数・標的候補・状態反転。
VERIFY: CPU上位DATの全シナリオ条件効果、各AI Skill完全発動優先順位、敵の位置予測・経路探索の全枝、satelliteプレイヤー命令競合、超過制限、`unit_action_bdr`の原本全step対応、実機HP/MP/RNG/行動一致。
GAMEPLAY OBSERVATION/Golden: 今回 0。新AIコード変更0、通常戦闘の原本再起動0。

## 技術資料リンク（public docs、閲覧用）
- https://w.atwiki.jp/vahren_ency/pages/389.html : class とAI設定（brave、line、satellite、attack/escape_range）
- https://w.atwiki.jp/vahren_ency/pages/379.html : unit、speed/action閾値、summon等
- https://w.atwiki.jp/vahren_ency/pages/378.html : skillと攻撃の発動条件
- https://w.atwiki.jp/vahren_ency/pages/402.html : 連鎖skill
- https://w.atwiki.jp/vahren_ency/pages/944.html : battleEvent、moveTroop、smoveTroop、skillTroop