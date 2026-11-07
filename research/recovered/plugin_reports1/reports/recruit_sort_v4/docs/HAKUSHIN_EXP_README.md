# HakushinExp v1.1 説明書 ― DAT から経験値と召喚の親子関係を扱う

作成: Claude（2026-11-03）
対象: 新約迫真戦記―ほのぼの神話 ver0.67 豪華版（Vahren.exe SHA-256 `E8DAC301…767187`）

この説明書は、**DAT を書く人**（人でも AI でも）がこれだけで正しく書けることを目標にしています。
§11 の「DAT を書くときのチェックリスト」は、書き終えたら必ず確認してください。

---

## 0. ひとことで言うと

戦闘中に、DAT から次のことができるようになります。

| 分類 | できること | 例 |
|---|---|---|
| 経験値の操作 | すぐに足す・引く・設定・倍率 | 田所に +100、歩兵を半分に |
| 経験値の参照 | 今の値・戦闘開始時・戦闘で稼いだ量・この仕組みで変えた量 | 「この戦闘で 500 以上稼いだらボーナス」 |
| ルール | 経験値を得た瞬間に自動で働く（戦闘の間ずっと） | 取得経験値 1.3 倍、車が稼いだ分を JOKER へ、召喚獣が稼いだ分を召喚した本人へ |
| 部隊なし召喚獣 | 原作では経験値 0 の召喚獣にも、原作の式で経験値を得させる | 召喚獣の稼ぎを召喚術師に還元 |
| 親子関係 | 子の数、召喚されたか、何代目か、親が生きているか | 「召喚獣が 5 体以上いたら…」 |
| 召喚スキル | どのスキルで召喚したか | 「s_inyume で召喚した子の数」 |
| スキル → 召喚ユニット | あるスキルで召喚されたユニットを数える・消す・経験値を一括で変える | 「スキルを奪ったら、そのスキルの召喚獣が全滅」 |
| きっかけルール | ダメージを与えた・受けた、補助スキルを使った・受けた瞬間に働く | 反撃・カウンター、被ダメージで成長、士気向上（経験値）、デバフ攻撃 |
| 時間制限付きの効果 | ○秒間だけ取得経験値 +○% | 士気向上を受けたら 30 秒間 1.1 倍、呪いで 20 秒間半分 |

**ゲーム内で確認済み**（2026-11-03〜04）: 通常戦闘・簡易戦闘（CPU 同士）の両方。§5 の各節に、何をどこまで確認したかを書いています。

### 0.1 やりたいこと → 使う関数（早引き）

| やりたいこと | 使う関数 | 例 |
|---|---|---|
| ある人の経験値を今すぐ増やす・減らす | `hk_exp_add` | 例 1・2 |
| 経験値を決まった値にする・倍にする | `hk_exp_set`、`hk_exp_scale` | 例 3 |
| 範囲内の全員を一度に | `storeRectUnit` → `hk_exp_add` | 例 4 |
| この戦闘で稼いだ量で分岐 | `hk_exp_get_earned` | 例 7 |
| ボスが倒れたら全員の経験値を減らす | `dead_event` → `hk_exp_add` | 例 9 |
| 取得経験値を ○ 倍にする（戦闘の間ずっと） | `hk_exp_rule_to_self` | 例 11〜15 |
| 変身・召喚獣が稼いだ分を本人へ | `hk_exp_rule_to_root` / `hk_exp_rule_to_parent` | 例 16〜21 |
| 部隊なしの召喚獣にも経験値を | `hk_exp_troopless` | 例 18・19 |
| 固有キャラ同士で経験値を分ける（師弟） | `hk_exp_rule_to_name` | 例 22・23 |
| 召喚獣の数・何代目か・親が生きているか | `hk_exp_count_children` など | 例 25〜28 |
| どのスキルで召喚されたか | `hk_exp_count_by_skill`、`hk_exp_summoned_by_skill` | 例 29・30 |
| スキルを奪ったら、そのスキルの召喚獣を消す | `hk_exp_vanish_by_skill` / `hk_exp_vanish_skill_all` | 例 31・32 |
| あるスキルの召喚獣にまとめて経験値 | `hk_exp_add_by_skill` / `hk_exp_add_skill_all` | 例 34 |
| あるスキルの召喚獣だけに効くルール | ルール＋flags 4096 | 例 35・36 |
| ダメージを受けたら経験値（反撃・カウンター） | `hk_exp_on_damaged` | 例 37〜39 |
| ダメージを与えたら経験値／相手の経験値を減らす | `hk_exp_on_dealt` | 例 40・42 |
| 補助スキル（士気向上など）を受けたら経験値 | `hk_exp_on_buffed` | 例 41 |
| 補助スキルを使った人に経験値 | `hk_exp_on_cast` | 例 44 |
| ○秒間だけ取得経験値 +○% | `hk_exp_timed`、きっかけルール＋flags 32768 | 例 45〜47 |

---

## 1. 導入と削除

### 必要なもの
- 新約迫真戦記―ほのぼの神話 ver0.67 豪華版（Vahren.exe が上の SHA-256 のもの）

### 導入
1. 配布フォルダ `HakushinExp_v1.0` を、ゲームのフォルダ（`Vahren.exe` がある所）の中に置く。
2. ゲームを終了した状態で `install.bat` を実行する。
3. 置き換えるファイルがあると確認されるので、`y` を入力する。元のファイルは配布フォルダ内の `backup_日時` に保存されます。

入るもの:

| ファイル | 役割 |
|---|---|
| `plugins\HakushinExp.dll` | 本体 |
| `plugins\HakushinDatUiSelector.dll` | 汎用一覧＋**DAT からの呼び出しを DLL に伝える通知基盤**（v1.0 から置き換え） |
| `dinput8.dll`、`HakushinCore.dll`、`plugins\HakushinRecruitPlugin.dll` | 共通基盤（HakushinUI v1.0 と同じもの） |
| `hakushin_plugins.conf` | プラグインの読み込み許可 |
| `HakushinExp.ini` | 設定（ログの有無） |
| `a_default\script\6002_HakushinExp\HakushinExp_v1.dat` | **DAT から使う共通イベント（この説明書の関数）** |

### 削除
`uninstall.bat` を実行すると、導入前の状態に戻ります（追加したファイルはバックアップ内へ移動）。

### 一時的に止める
`hakushin_plugins.conf` の `hakushin.exp|…` の行の 3 項目目を `1` から `0` にして、ゲームを再起動します。

---

## 2. しくみ（必ず読む）

### 2.1 呼び方は「変数に入れて routine で呼ぶ」
原作の `routine()` には引数も戻り値もありません。そこで、
1. **入力を変数に入れる**（`setv(@hk_exp_target,…)`、`set(hk_exp_value,…)` など）
2. **共通イベントを `routine(…)` で呼ぶ**
3. **結果を変数から読む**（`hk_exp_result`、`hk_exp_out`）

という形になります。

```
setv(@hk_exp_target,tadokoro)     // ① 対象
set(hk_exp_value,100)             // ① 値
routine(hk_exp_add)               // ② 呼ぶ
if (hk_exp_result > 0)            // ③ 結果
	{
	msg(経験値を増やしました)
	}
```

### 2.2 使えるのは戦闘中だけ
- 戦闘の外で呼ぶと `hk_exp_result` が **-11** になり、何も起きません。
- 書く場所は「戦闘中に動くイベント」です（§4）。

### 2.3 「すぐ反映」「経験値ルール」「きっかけルール」「時間制限付き」の違い
| | すぐ反映（操作） | 経験値ルール（§5.5） | きっかけルール（§5.10） | 時間制限付き（§5.11） |
|---|---|---|---|---|
| いつ効く | 呼んだその瞬間に 1 回 | 経験値を得るたびに自動で | ダメージ・補助スキルが 1 体に当たるたびに自動で | 付けてから ○秒間、経験値を得るたびに |
| 対象 | そのとき戦場にいるユニット | 名前・条件で指定。**あとから出てきた召喚獣にも効く** | 同左（与えた側・受けた側などを選ぶ） | 付けたユニット |
| 例 | 「+100」 | 「得た経験値を 1.3 倍」 | 「受けたダメージ×レベル×1/2」 | 「30 秒間 +10%」 |
| 登録 | 毎回呼ぶ | 戦闘の最初に 1 回 | 戦闘の最初に 1 回 | 呼ぶか、きっかけルールで自動 |
| 消えるとき | — | 戦闘終了、`hk_exp_rule_clear` | 同左 | 時間切れ、`hk_exp_clear`、戦闘終了 |

### 2.4 ユニットの指定は「名前」と「関係」
- **名前**: DAT のユニット名（`unit xxx` の xxx）。召喚獣は召喚スキルの `add` に書いた名前（例 `jocar`、`inyume`）。
  - 同じ名前が何体もいると、**生きているものを優先して 1 体だけ** 選ばれます（原作の `isAlive` などと同じ選び方）。
- **関係**: 「得たユニット自身」「召喚した本人（親）」「召喚をさかのぼった一番上」。ルールでだけ使えます。
  - **名前ではなく個体の親子関係でたどる**ので、同名のモブ召喚術師が何十体いても、各召喚獣の分は自分を召喚した個体に届きます。

### 2.5 経験値とレベル
- 経験値は 0 未満にも上限以上にもなりません。
- レベルは下がりません（原作にレベルダウンがないため）。
- レベルアップの判定は原作と同じ時点です。通常戦闘は**戦闘終了時**、簡易戦闘は**その場で**判定されます。
- **倒れたユニットにも経験値は入り**、戦闘終了時のレベル判定も受けます（実機確認済み）。

---

## 3. 変数

`hk_exp_setup` を呼ぶと、すべて作られます。**値はすべて整数**です。

| 変数 | 種類 | 入力/出力 | 意味 |
|---|---|---|---|
| `@hk_exp_target` | 文字列の配列 | 入力 | 対象のユニット名（複数可） |
| `@hk_exp_dest` | 文字列の配列 | 入力 | 渡し先の名前、またはスキル名（最初の 1 つだけ使う） |
| `@hk_exp_list` | 文字列の配列 | 出力 | 名前の一覧の書き込み先（§5.12）。関数を呼ぶたびに中身が置き換わる |
| `@hk_exp_skill` | 文字列の配列 | 入力 | ルールの条件「このスキルで召喚されたユニットだけ」（flags 4096）のスキル名（最初の 1 つ） |
| `hk_exp_value` | 数値 | 入力 | 値（意味は関数ごと） |
| `hk_exp_flags` | 数値 | 入力 | オプション（§6）。使い終わったら 0 に戻す |
| `hk_exp_result` | 数値 | 出力 | 処理した数。マイナスはエラー（§7） |
| `hk_exp_out` | 数値 | 出力 | 調べた答え、または増減の合計 |
| `hk_exp_pending` | 数値 | 出力 | 当たった記録の件数（§5.13）。DLL が自動で書く |
| `hk_exp_seconds` | 数値 | 入力 | 時間制限付きの効果の秒数（§5.11） |
| `hk_exp_receiver` | 数値 | 入力 | きっかけルールの渡し先（§5.10）。0 名前／1 本人／2 本人の親／3 本人の一番上の親／4 相手 |
| `hk_exp_op`、`hk_exp_to`、`hk_exp_trigger` | 数値 | 内部用 | 共通イベントが自動で設定する。触らない |

### 配列への入れ方
```
setv(@hk_exp_target,tadokoro)       // 1 つにする（前の中身は消える）
addv(@hk_exp_target,miura)          // 1 つ足す
storeRectUnit(red,0,0,9999,9999,@hk_exp_target)   // 戦場の四角の中のユニットをまとめて入れる
```
- `setv(@hk_exp_target,hk_none)` は「誰もいない」の意味で使えます（`hk_exp_setup` はこれで初期化します）。

---

## 4. 書く場所（テンプレート）

### テンプレート A：戦闘の最初に 1 回だけ（ルールの登録など）
戦闘が始まった直後は、まだ名前の表ができていないので -11 が返ることがあります。**返らなくなるまで毎フレーム試し、成功したら止める**形にします。

```
// 拠点・シナリオの戦闘イベント（fight = my_fight）
event my_fight
{
set(my_exp_ready,0)
battleEvent(my_exp_start)
}

event my_exp_start
{
rif (my_exp_ready == 0)
	{
	routine(hk_exp_setup)
	// ↓ ここにルールの登録などを書く（例は §8）

	// ↑ ここまで
	if (hk_exp_result != -11)
		{
		set(my_exp_ready,1)
		}
	}
}
```
- `my_exp_ready` は自分で決めた変数名です（他と重ならない名前に）。
- 登録を何度もやり直す可能性がある書き方（失敗したら次のフレームでもう一度、など）にする場合は、`routine(hk_exp_setup)` の直後に `routine(hk_exp_rule_clear)` を入れて、途中まで登録されたルールを消してから登録し直してください（重複登録や 32 個の上限を防ぐ）。
- 最後に呼んだ関数の `hk_exp_result` が -11 でなければ「戦闘中に実行できた」という意味です。

### テンプレート B：戦闘中に一定間隔で
```
event my_exp_tick
{
rif (isInterval(300))     // 約 5 秒（60 フレーム＝1 秒）
	{
	// ここに書く
	}
}
```
（`battleEvent(my_exp_tick)` で登録。§9 のとおり、定期的な呼び出しは必要なときだけにしてください。）

### テンプレート C：ユニットが倒れたとき
```
unit some_boss
{
	...
	dead_event = boss_dead_exp
}

event boss_dead_exp
{
// ここに書く（倒れたその場で実行される）
}
```
- `dead_event` は戦闘後ではなく、**倒れた瞬間**に実行されます（実機確認済み）。
- `hk_exp_setup` を戦闘の最初に呼んでいない場合は、ここでも呼んでください（何度呼んでも問題ありません）。

---

## 5. 関数リファレンス（共通イベント 44 個）

表記: **入力** → **出力**。`target` は `@hk_exp_target`、`dest` は `@hk_exp_dest`、`value` は `hk_exp_value`。

### 5.1 準備
#### `hk_exp_setup`
- 変数を作り、初期化する。戦闘の最初に 1 回。何度呼んでもよい。
- 入力: なし → 出力: なし（`hk_exp_value`・`hk_exp_flags`・結果が 0 になる）

### 5.2 操作（すぐ反映。target の全員に）
#### `hk_exp_add`
- 入力: target、value（負なら引く）、flags（任意）
- 出力: result＝処理した人数、out＝実際に増減した合計
#### `hk_exp_set`
- 入力: target、value（その値にする。負は 0）
- 出力: 同上
#### `hk_exp_scale`
- 入力: target、value（千分率。500＝半分、2000＝2 倍）
- 出力: 同上

### 5.3 参照（target の最初の 1 人。答えは out）
| 関数 | out |
|---|---|
| `hk_exp_get_now` | 今の経験値 |
| `hk_exp_get_start` | この戦闘で最初に関わったとき（その記録の最初の変化か、最初に触ったとき）の経験値 |
| `hk_exp_get_earned` | この戦闘で原作の処理（攻撃・回復・召喚）で得た量（減った分は引く） |
| `hk_exp_get_manual` | この戦闘でこの仕組み（操作・倍率・転送・ルール）で変えた量 |
- result は 1（成功）か、マイナス（エラー）。

### 5.4 個別の継続効果（そのとき戦場にいる target だけ。この戦闘の間）
| 関数 | 入力 | 働き |
|---|---|---|
| `hk_exp_mul` | target、value（千分率） | 得た量×value÷1000 になるよう上乗せ（1300＝1.3 倍） |
| `hk_exp_transfer` | target、dest、value（千分率）、flags | 得た量×value÷1000 を dest の最初のユニットへ足す |
| `hk_exp_clear` | target | 上の 2 つを解除 |
- **あとから出てくるユニットには効きません**。そういう場合はルール（5.5）を使います。

### 5.5 ルール（おすすめ。戦闘の最初に 1 回登録）
誰が（**source**）経験値を得たときに、誰に（**渡し先**）、どれだけ（**量**）を足すか、を登録します。

- **source**: target の名前（複数可）。flags 256 なら「誰でも」。flags 512 を足すと「召喚されたユニットだけ」。
- **量**: 得た量×value÷1000（負も可）。flags 1024 なら value そのもの（固定値）。
- 普段は経験値が**増えたとき**だけ働きます。flags 2048 で減ったときも働きます。
- 1 戦闘 32 個まで。戦闘が終わると消えます。

| 関数 | 渡し先 |
|---|---|
| `hk_exp_rule_to_name` | dest の最初の名前のユニット（固有キャラ向け。倒れていても届く） |
| `hk_exp_rule_to_self` | 得たユニット自身（倍率に使う） |
| `hk_exp_rule_to_parent` | 召喚した本人（個体ごとに正確） |
| `hk_exp_rule_to_root` | 召喚をさかのぼった一番上（召喚獣の召喚獣でも本人へ） |
| `hk_exp_rule_clear` | この戦闘のルールを全部消す |
- 出力: result＝登録後のルールの数（成功）、マイナス（エラー）。
- ルールで足した分は、別のルールの引き金になりません（連鎖しない）。

### 5.6 部隊なしの召喚獣
#### `hk_exp_troopless`
- 原作では、部隊に属さない召喚獣（yorozu に troop 指定がない召喚、簡易戦闘の召喚）は経験値を 1 も得ません。
- この関数を使うと、その召喚獣も**原作の計算式そのまま**で経験値を得るようになります。この戦闘の間だけ。
- value: `0` 原作どおり／`1` 召喚獣自身も得る／`2` 召喚獣には残さず、ルールでの受け渡しにだけ使う
- 対象は「召喚されたユニット（親がいる）」だけです。
- 実機確認: 召喚獣 12 体の 2,216 回分（計 207 万）を、ルールで召喚術師へ渡せた。

### 5.7 親子関係（target の最初の 1 人。答えは out）
| 関数 | out |
|---|---|
| `hk_exp_count_children` | 生きている子（そのユニットが召喚したユニット）の数 |
| `hk_exp_count_children_all` | 倒れた子も含めた数（原作の召喚数の上限は、こちらで数えていると推定） |
| `hk_exp_is_summoned` | 召喚されたユニットなら 1、違えば 0 |
| `hk_exp_generation` | 何代目か（0 召喚されていない／1 子／2 孫…） |
| `hk_exp_parent_alive` | 親が生きていれば 1、倒れていれば 0、親がいなければ -1 |

### 5.8 召喚に使ったスキル（target の最初の 1 人。答えは out）
| 関数 | 入力 | out |
|---|---|---|
| `hk_exp_count_by_skill` | target（召喚した本人）、dest（スキル名。`hk_none` なら全部） | そのスキルで召喚した、生きている子の数 |
| `hk_exp_summoned_by_skill` | target（調べるユニット）、dest（スキル名） | そのスキルで召喚されたなら 1、別のスキルなら 0、記録がなければ -1 |
- スキル名は DAT の `skill xxx` の xxx（召喚を実際に行うスキル。JOKER の車なら `sp_jocar_nt2`）。
- 記録されるのは、DLL を入れてからその戦闘で行われた召喚だけです。通常戦闘・簡易戦闘の両方で記録されます（2026-11-04 確認）。
- 記録されるスキル名は「実際に召喚を行ったスキル」です。ミサイルの連鎖の先で召喚する場合は、そのミサイル側のスキル名になります（例 `abesan_yari1_pr1b`）。

### 5.9 スキル → そのスキルで召喚したユニット
dest（`@hk_exp_dest` の最初の名前）がスキル名です。`hk_none` なら全スキル。**生きている**ユニットだけが対象です。

| 関数 | 入力 | 働き・出力 |
|---|---|---|
| `hk_exp_vanish_by_skill` | target（召喚した本人。複数可）、dest | その本人たちが dest のスキルで召喚した子を全員消す（倒れた扱い）。result＝消した数 |
| `hk_exp_vanish_skill_all` | dest | 召喚した本人を問わず、dest のスキルで召喚されたユニットを全員消す。result＝消した数 |
| `hk_exp_count_skill_all` | dest | 召喚した本人を問わず、dest のスキルで召喚された生きているユニットの数（out） |
| `hk_exp_add_by_skill` | target、dest、value、flags | その本人たちが dest のスキルで召喚した子全員の経験値に value を足す。result＝人数、out＝増減の合計 |
| `hk_exp_add_skill_all` | dest、value、flags | 召喚した本人を問わず、dest のスキルで召喚されたユニット全員に value を足す |

- 「消す」は、原作が親の死亡時に `element_lost` の子を消すときや、命令 `removeTroop` と同じ処理（ユニットの消滅処理）を使います。消えたユニットは**倒れた扱い**で、そのユニットの `dead_event` や `break`（死亡時スキル）も原作どおり動きます。
- 消えた子が `element_lost = on` の子を持っていれば、その孫も原作どおり消えます。
- 消されたユニットの `dead_event` の中から呼んだ hk_exp の関数は無視されます（入れ子の呼び出しを防ぐため）。
- ルールの条件にも使えます: flags **4096** と `setv(@hk_exp_skill,スキル名)` で「そのスキルで召喚されたユニットが経験値を得たときだけ」。
- 状態: 通常戦闘・簡易戦闘でゲーム内確認済み（2026-11-04。消去 計 105 体、一括加算 計 75 体、スキル指定のルールが該当スキルの召喚ユニットだけに働くことを確認。落ちる・止まるなし）。

### 5.10 きっかけルール（ダメージ・補助スキル）
戦闘の最初に 1 回登録すると、その戦闘の間、**ダメージや補助スキルが 1 体に当たるたびに**働きます。範囲攻撃なら、当たった全員について 1 回ずつ働きます。

| 関数 | きっかけ | 「本人」 | 「相手」 |
|---|---|---|---|
| `hk_exp_on_dealt` | ダメージを与えた | 攻撃した側 | 攻撃を受けた側 |
| `hk_exp_on_damaged` | ダメージを受けた（反撃・カウンター） | 攻撃を受けた側 | 攻撃した側 |
| `hk_exp_on_cast` | 補助スキルを使った | 使った側 | 受けた側 |
| `hk_exp_on_buffed` | 補助スキルを受けた（士気向上・デバフ） | 受けた側 | 使った側 |

- 入力:
  - target（本人の名前。flags 256 なら誰でも）
  - `hk_exp_receiver`（渡し先）: 0 名前（dest）／1 本人／2 本人の親／3 本人の一番上の親／4 相手
  - value と flags
- 量: 「ダメージ（補助スキルなら効果量）× value ÷ 1000」。
  - flags 1024 なら value そのもの（固定値）。
  - flags 16384 なら、さらに**受け取る側のレベル**を掛ける。
- flags 8192 と `setv(@hk_exp_skill,スキル名)` で、**そのスキルが当たったときだけ**働きます。
- flags 512（召喚されたユニットだけ）、4096（召喚スキル指定）、1（倒れた相手には渡さない）も使えます。
- 経験値ルール（§5.5）とは別に数えます（両方を合わせて 1 戦闘 32 個まで）。
- ダメージ量は、原作が経験値の計算に使う値です（距離による減衰を含む）。ボス補正や最低ダメージの補正の前の値なので、実際の HP の減り方と少し違うことがあります。
- 「補助スキル」は、ステータスを与えるスキル（原作の処理 0x551490 を通るもの。士気向上・歌唱など）です。ダメージを与える攻撃・回復は「ダメージ」の側に入ります。
- 状態: 通常戦闘・簡易戦闘でゲーム内確認済み（2026-11-04。士気向上（攻撃）は本体のスキル名 `sp_attack` で届き +100、整列・歌唱・デバフなどの補助スキルも届いた。被ダメージ×レベル×1/2 も動作）。召喚獣の被ダメージ（例 43）も敵の攻撃で確認（2026-11-04 06:13）。
### 5.11 時間制限付きの効果（取得経験値 +○% を ○秒間）
| 関数・指定 | 働き |
|---|---|
| `hk_exp_timed` | target 全員に、今から `hk_exp_seconds` 秒間、取得経験値 +value‰（100＝+10%、-500＝半分）を付ける |
| きっかけルール＋flags **32768** | 経験値を足す代わりに、渡し先へ「`hk_exp_seconds` 秒間 +value‰」を付ける（士気向上で 30 秒間 1.1 倍など） |
| `hk_exp_clear` | 倍率・転送と一緒に、時間制限付きの効果も消す |
- 同じユニットに付け直すと、その時点から時間を数え直します（重ねがけで倍率は増えません）。
- 時間は実際の時間（秒）です。ゲームの早送りでは短くなりません。戦闘が終わると消えます。
- `hk_exp_mul`（倍率）や経験値ルールの倍率とは別に足されます。
- 状態: 通常戦闘でゲーム内確認済み（2026-11-04。士気向上を受けた 5 体に +10% が付き、時間が過ぎると止まった）。

### 5.12 名前の一覧を受け取る（DLL → DAT）
`@hk_exp_list`（`hk_exp_setup` が作る）に、ユニットの名前を書き込みます。前の中身は消えます。result と out は書き込んだ数です。

| 関数 | 入力 | 書き込む名前 |
|---|---|---|
| `hk_exp_list_children` | target、value（1 で倒れた子も） | 最初の対象の子 |
| `hk_exp_list_skill_all` | dest（スキル名、hk_none で全部） | そのスキルで召喚された生きているユニット（召喚した本人を問わない） |
| `hk_exp_list_by_skill` | target、dest | 最初の対象がそのスキルで召喚した生きている子 |
| `hk_exp_list_parent` | target | 最初の対象の親（召喚した本人） |
| `hk_exp_list_root` | target | 最初の対象の一番上の親 |

- 書き込んだ配列は、原作の `countVar(@hk_exp_list)`（数）や `storeIndexVar(@hk_exp_list,番号,@受け取り)`（N 番目、0 から）でそのまま使えます。他の関数の対象にするときは、`@hk_exp_target` へ写してください（例 49）。
- 名前は DAT のユニット名です。同じ名前のモブは同じ名前が並びます（どの個体かまでは区別できません）。
- 書き込みは原作の `setv`／`addv` と同じ関数（文字列の配列を空にする・1 つ足す）で行うので、メモリの扱いは原作と同じです。
- 状態: 通常戦闘でゲーム内確認済み（2026-11-04。書き込み 85 回すべて読み直しと一致、DAT の countVar／storeIndexVar で取り出した名前で別の関数を呼べた。落ちる・固まるなし）。

### 5.13 当たった記録（DAT で「当たったとき」に原作の命令を使う）
ダメージ処理の最中に DAT を直接動かすのは危険なので、DLL が「当たった記録」をため、DAT が戦闘中のイベントで 1 件ずつ取り出して処理します。

1. 戦闘の最初に、きっかけルールを flags **65536** 付きで登録する（どの攻撃・補助スキルを記録するかは、ふつうのきっかけルールと同じく source とスキル指定で決める。量や渡し先は使わない）。
2. DLL は当たるたびに記録を積み、件数を `hk_exp_pending` に書く（最大 256 件。あふれた分は捨てる）。
3. DAT は battleEvent で `if (hk_exp_pending > 0)` を見て、`hk_exp_hit_pop` で 1 件取り出す。

| 関数 | 働き |
|---|---|
| `hk_exp_hit_pop` | 1 件取り出す。`@hk_exp_list` に [攻撃した側の名前, 受けた側の名前, スキル名]、`hk_exp_out` に量（ダメージ・効果量）、`hk_exp_result` は 1（空なら 0） |
| `hk_exp_hit_count` | 記録の件数（out） |
| `hk_exp_hit_clear` | 記録を全部捨てる |
| `hk_exp_hit_vanish` | 直前に取り出した記録の受けた側（value 1 なら攻撃した側）の**個体**が、dest のスキルで召喚した生きている子を消す |

- 名前は同名のモブでは区別できませんが、`hk_exp_hit_vanish` は記録した個体そのものを使うので、同名のモブでも正確です。
- 記録は戦闘が終わると消えます。
- 状態: 通常戦闘でゲーム内確認済み（2026-11-04。攻撃が召喚術師に当たる → 記録 → 取り出し → 受けた個体の召喚獣を消す、の流れで召喚獣が画面から消えた）。
- 試験のこつ: DAT でユニットの能力やスキルを変えたら、セーブを読み込まずに新しく始めること（セーブを読むとセーブ側の値が使われる）。クラスを持つユニットのスキルは、クラス側の skill も変えること。

- **注意: 即死級のスキル（固定 999,999 ダメージなど）では、ダメージ量がそのまま使われます。** 例 38 の形だと JOKER の変身（sp_jocar_dmg）で 1,250 万の経験値が入りました。自滅・即死スキルを除外したいときは、flags 8192 で対象のスキルに絞るか、value を小さくしてください。

---

## 6. flags（hk_exp_flags）— 足し算で組み合わせる

| 値 | 意味 | 使える関数 |
|---|---|---|
| 1 | 倒れているユニットには渡さない／操作しない | 操作・転送・ルール |
| 2 | 原作と同じ条件（部隊あり・経験値禁止なし）のユニットだけ | 操作・転送・ルール |
| 4 | 通常戦闘でもすぐレベルアップ判定する | 操作・転送・ルール |
| 8 | レベルアップ判定をしない | 操作・転送・ルール |
| 256 | 誰が得ても（target を見ない） | ルール |
| 512 | 召喚されたユニットが得たときだけ | ルール |
| 1024 | 固定値（得た量に関係なく value） | ルール |
| 2048 | 経験値が減ったときも働く | ルール |
| 4096 | `@hk_exp_skill` のスキルで召喚されたユニットが得たときだけ | ルール |
| 8192 | そのとき当たったスキルが `@hk_exp_skill` のときだけ | きっかけルール |
| 16384 | 量に受け取る側のレベルも掛ける | きっかけルール |
| 32768 | 経験値を足す代わりに、時間制限付きの効果を付ける（§5.11） | きっかけルール |
| 65536 | 経験値を足す代わりに、当たった記録を積む（§5.13） | きっかけルール |

早見表:

| やりたいこと | flags |
|---|---|
| 召喚された誰でも | 768（256＋512） |
| 召喚された誰でも、倒れた親には渡さない | 769（1＋256＋512） |
| 召喚された誰でも、固定値 | 1792（256＋512＋1024） |
| 誰でも、固定値 | 1280（256＋1024） |
| 名前で指定、減ったときも連動 | 2048 |
| あるスキルで召喚されたユニットだけ（誰でも） | 4864（256＋512＋4096） |
| あるスキルが当たったときだけ、誰でも、固定値（きっかけルール） | 9472（256＋1024＋8192） |
| 受け取る側のレベルを掛ける（きっかけルール） | 16384 |
| あるスキルが当たったら、誰でも、時間制限付きの効果（きっかけルール） | 41216（256＋8192＋32768） |
| 倒れた相手には渡さない、を足したいとき | 上の値＋1 |

**ルールや操作の後は `set(hk_exp_flags,0)` に戻す**こと（次の呼び出しに残ります）。

---

## 7. エラー（hk_exp_result がマイナス）

| 値 | 意味 | よくある原因と対処 |
|---|---|---|
| -10 | 変数がない | `hk_exp_setup` を呼んでいない |
| -11 | 戦闘中でない | 戦闘の前・後に呼んだ。テンプレート A のように、成功するまで繰り返す |
| -12 | 番号・値が不正 | `hk_exp_troopless` の value が 0〜2 以外など |
| -13 | 渡し先がいない | dest の名前のユニットが戦場にいない／dest が空 |
| -14 | 対象がいない | target の名前のユニットが戦場にいない（召喚獣がまだ出ていない等） |
| -15 | ルールが多すぎる | 1 戦闘 32 個まで |

---

## 8. 具体例（30 例）

特に断りがない限り、テンプレート A の「ここに書く」の中、または戦闘中のイベントに書きます。

### A. 経験値をすぐ変える

**例 1：田所に経験値 +100**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_value,100)
routine(hk_exp_add)
```

**例 2：田所と三浦に経験値 -50（0 未満にはならない）**
```
setv(@hk_exp_target,tadokoro)
addv(@hk_exp_target,miura)
set(hk_exp_value,-50)
routine(hk_exp_add)
```

**例 3：経験値を 1000 にしてから半分にする**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_value,1000)
routine(hk_exp_set)
set(hk_exp_value,500)
routine(hk_exp_scale)
```

**例 4：戦場の四角の中の全員に -30**
```
storeRectUnit(blue,0,0,9999,9999,@hk_exp_target)
set(hk_exp_value,-30)
routine(hk_exp_add)
```
（red・blue のどちらが味方かは原作の storeRectUnit の仕様に従います。）

**例 5：倒れているユニットは除いて +200**
```
setv(@hk_exp_target,tadokoro)
addv(@hk_exp_target,miura)
set(hk_exp_flags,1)
set(hk_exp_value,200)
routine(hk_exp_add)
set(hk_exp_flags,0)
```

**例 6：すぐにレベルアップ判定まで行う（通常戦闘でも）**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_flags,4)
set(hk_exp_value,5000)
routine(hk_exp_add)
set(hk_exp_flags,0)
```

### B. 経験値を調べる

**例 7：この戦闘で稼いだ量が 500 以上ならボーナス +200**
```
setv(@hk_exp_target,tadokoro)
routine(hk_exp_get_earned)
if (hk_exp_out >= 500)
	{
	set(hk_exp_value,200)
	routine(hk_exp_add)
	}
```

**例 8：戦闘開始時より経験値が減っていたら補てん**
```
setv(@hk_exp_target,tadokoro)
routine(hk_exp_get_start)
set(my_start,hk_exp_out)
routine(hk_exp_get_now)
if (hk_exp_out < my_start)
	{
	set(hk_exp_value,100)
	routine(hk_exp_add)
	}
```
（変数から変数への `set` の書き方は原作 DAT の仕様に従ってください。）

### C. 倒れたとき

**例 9：ボスが倒れたら、相手側全員の経験値 -100（呪い）**
```
unit kinshi_boss
{
	...
	dead_event = boss_curse
}

event boss_curse
{
routine(hk_exp_setup)
storeRectUnit(red,0,0,9999,9999,@hk_exp_target)
set(hk_exp_value,-100)
routine(hk_exp_add)
}
```

**例 10：仲間が倒れたら、その分の悲しみで隊長に +300**
```
unit nakama
{
	...
	dead_event = nakama_dead_exp
}

event nakama_dead_exp
{
routine(hk_exp_setup)
setv(@hk_exp_target,taichou)
set(hk_exp_value,300)
routine(hk_exp_add)
}
```

### D. 倍率（ルール）

**例 11：召喚術師の取得経験値を 1.3 倍**
```
setv(@hk_exp_target,hs_summoner)
set(hk_exp_value,300)            // +30%
routine(hk_exp_rule_to_self)
```
- 1.1 倍＝100、2 倍＝1000、半分＝-500、得られなくする＝-1000。
- 実機確認: 召喚 1 回 +10 に +3 が付いた。

**例 12：味方（名前で列挙）全員の取得経験値を 1.1 倍（「士気向上」的なスキル）**
```
setv(@hk_exp_target,tadokoro)
addv(@hk_exp_target,miura)
addv(@hk_exp_target,kimura)
set(hk_exp_value,100)
routine(hk_exp_rule_to_self)
```
- 名前で書いたユニットは、あとから出撃・召喚されても効きます。

**例 13：戦場にいる味方全員の取得経験値を 1.1 倍（名前を書かずに）**
```
storeRectUnit(blue,0,0,9999,9999,@hk_exp_target)
set(hk_exp_value,100)
routine(hk_exp_rule_to_self)
```
- 呼んだ時点でいるユニットの**名前**で登録されます。同名のユニット（同じモブなど）にはまとめて効きます。

**例 14：敵の取得経験値を半分に（妨害）**
```
storeRectUnit(red,0,0,9999,9999,@hk_exp_target)
set(hk_exp_value,-500)
routine(hk_exp_rule_to_self)
```

**例 15：経験値を得るたびに固定で +5（成長補正）**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_flags,1024)
set(hk_exp_value,5)
routine(hk_exp_rule_to_self)
set(hk_exp_flags,0)
```

### E. 変身・召喚獣の稼ぎを本人へ（ルール）

**例 16：JOKER の変身（車・戻った JOKER が稼いだ分を JOKER 本人へ）**
```
setv(@hk_exp_target,jocar)
addv(@hk_exp_target,joker_re)
set(hk_exp_value,1000)           // 全額
routine(hk_exp_rule_to_root)
```
- 車が出る前に登録してよい。本人が倒れていても届く。
- 実機確認: 2 戦で計 87 万を JOKER へ。

**例 17：召喚された誰が稼いでも、召喚をさかのぼった一番上へ全額（汎用）**
```
set(hk_exp_flags,768)            // 誰でも＋召喚されたユニットだけ
set(hk_exp_value,1000)
routine(hk_exp_rule_to_root)
set(hk_exp_flags,0)
```
- 1 つのルールで、召喚術師の召喚獣も JOKER の車も、それぞれの本人へ届く（実機確認済み）。

**例 18：部隊なしの召喚獣も含めて、稼ぎを召喚した本人へ（召喚獣には残さない）**
```
set(hk_exp_value,2)
routine(hk_exp_troopless)
set(hk_exp_flags,768)
set(hk_exp_value,1000)
routine(hk_exp_rule_to_parent)
set(hk_exp_flags,0)
```
- 実機確認: 召喚獣 12 体の稼ぎ 207 万を召喚術師へ。

**例 19：召喚獣の稼ぎの半分を本人へ、残り半分は召喚獣自身に残す**
```
set(hk_exp_value,1)              // 召喚獣も経験値を得る
routine(hk_exp_troopless)
set(hk_exp_flags,768)
set(hk_exp_value,500)
routine(hk_exp_rule_to_parent)
set(hk_exp_flags,0)
```

**例 20：同名のモブ召喚術師が何十体いても、それぞれの召喚獣の稼ぎをそれぞれの召喚術師へ**
例 18 と同じ書き方で大丈夫です。名前ではなく個体の親子関係でたどります。

**例 21：召喚獣が経験値を得るたび、本人に固定 +5（倒れた本人には渡さない）**
```
set(hk_exp_flags,1793)           // 1＋256＋512＋1024
set(hk_exp_value,5)
routine(hk_exp_rule_to_parent)
set(hk_exp_flags,0)
```

**例 22：固有キャラ A の稼ぎの 2 割を固有キャラ B へ（師弟）**
```
setv(@hk_exp_target,deshi)
setv(@hk_exp_dest,shishou)
set(hk_exp_value,200)
routine(hk_exp_rule_to_name)
```

**例 23：弟子の稼ぎを師匠へ全額移す（弟子は増えない）**
```
setv(@hk_exp_target,deshi)
setv(@hk_exp_dest,shishou)
set(hk_exp_value,1000)
routine(hk_exp_rule_to_name)
setv(@hk_exp_target,deshi)
set(hk_exp_value,-1000)
routine(hk_exp_rule_to_self)
```

**例 24：ルールを途中でやめる**
```
routine(hk_exp_rule_clear)
```

### F. 親子関係・召喚スキルで分岐する

**例 25：召喚獣が 5 体以上いたら、召喚術師に +100**
```
setv(@hk_exp_target,hs_summoner)
routine(hk_exp_count_children)
if (hk_exp_out >= 5)
	{
	set(hk_exp_value,100)
	routine(hk_exp_add)
	}
```

**例 26：あるユニットが召喚獣なら何もしない、そうでなければ +50**
```
setv(@hk_exp_target,someone)
routine(hk_exp_is_summoned)
if (hk_exp_out == 0)
	{
	set(hk_exp_value,50)
	routine(hk_exp_add)
	}
```

**例 27：孫（召喚獣の召喚獣）なら特別扱い**
```
setv(@hk_exp_target,grandchild_name)
routine(hk_exp_generation)
if (hk_exp_out >= 2)
	{
	// 孫以降のときの処理
	}
```

**例 28：親が倒れている召喚獣かどうか**
```
setv(@hk_exp_target,jocar)
routine(hk_exp_parent_alive)
if (hk_exp_out == 0)
	{
	// 親（JOKER）が倒れている
	}
```

**例 29：召喚術師が s_inyume で召喚した子の数が 12 になったら**
```
setv(@hk_exp_target,hs_summoner)
setv(@hk_exp_dest,s_inyume)
routine(hk_exp_count_by_skill)
if (hk_exp_out >= 12)
	{
	// 上限に達したときの処理
	}
```

**例 30：このユニットは sp_jocar_nt2 で召喚されたか**
```
setv(@hk_exp_target,jocar)
setv(@hk_exp_dest,sp_jocar_nt2)
routine(hk_exp_summoned_by_skill)
if (hk_exp_out == 1)
	{
	// JOKER の変身スキルで出た車
	}
```

### G. スキルを奪う・召喚ユニットを消す

**例 31：スキルを奪ったら、そのスキルで召喚されたユニットを全滅させる**
```
// 攻撃側のイベントで、相手（victim）から召喚スキル s_inyume を奪い、味方（thief）に渡す
eraseSkill(victim,s_inyume)          // 原作の命令（書き方は原作の仕様に従う）
addSkill2(thief,s_inyume)            // 原作の命令（同上）
// 奪われたスキルで victim が召喚していたユニットを消す
setv(@hk_exp_target,victim)
setv(@hk_exp_dest,s_inyume)
routine(hk_exp_vanish_by_skill)
```
- 同名のモブから奪う場合は、生きているものが 1 体選ばれます。モブ全員分を消すなら例 32。

**例 32：誰が召喚したかに関係なく、s_inyume で出たユニットを全部消す**
```
setv(@hk_exp_dest,s_inyume)
routine(hk_exp_vanish_skill_all)
```

**例 33：s_inyume で出たユニットが戦場に 10 体以上いたら**
```
setv(@hk_exp_dest,s_inyume)
routine(hk_exp_count_skill_all)
if (hk_exp_out >= 10)
	{
	msg(召喚獣が多すぎます)
	}
```

**例 34：召喚術師が s_inyume で出した子全員に経験値 +500**
```
setv(@hk_exp_target,hs_summoner)
setv(@hk_exp_dest,s_inyume)
set(hk_exp_value,500)
routine(hk_exp_add_by_skill)
```

**例 35：s_iwana_nt で出たユニットが稼いだ分だけ、召喚した本人へ全額（他の召喚は対象外）**
```
setv(@hk_exp_skill,s_iwana_nt)
set(hk_exp_flags,4864)               // 256 誰でも + 512 召喚されたユニット + 4096 スキル指定
set(hk_exp_value,1000)
routine(hk_exp_rule_to_parent)
set(hk_exp_flags,0)
```

**例 36：s_inyume で出たユニットだけ取得 1.5 倍**
```
setv(@hk_exp_skill,s_inyume)
set(hk_exp_flags,4864)
set(hk_exp_value,500)
routine(hk_exp_rule_to_self)
set(hk_exp_flags,0)
```

### H. ダメージ・補助スキルで経験値（きっかけルール）

**例 37：ダメージを受けたら経験値 +50（固定）**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_receiver,1)               // 本人へ
set(hk_exp_flags,1024)               // 固定値
set(hk_exp_value,50)
routine(hk_exp_on_damaged)
set(hk_exp_flags,0)
```

**例 38：受けたダメージ × 自身のレベル × 1/2 を経験値に**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_receiver,1)
set(hk_exp_flags,16384)              // ×レベル
set(hk_exp_value,500)                // ×1/2
routine(hk_exp_on_damaged)
set(hk_exp_flags,0)
```

**例 39：カウンター — 攻撃してきた相手の経験値を、受けたダメージの 2 割だけ減らす**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_receiver,4)               // 相手（攻撃してきた側）
set(hk_exp_value,-200)
routine(hk_exp_on_damaged)
```

**例 40：誰でも、与えたダメージの 1 割を経験値に（全体の成長を早める）**
```
set(hk_exp_flags,256)
set(hk_exp_receiver,1)
set(hk_exp_value,100)
routine(hk_exp_on_dealt)
set(hk_exp_flags,0)
```

**例 41：士気向上（経験値）— 士気向上(攻撃)を受けた味方に経験値 +100**
```
setv(@hk_exp_skill,shiki_up_atk)     // 士気向上(攻撃) の DAT 上のスキル名にする
set(hk_exp_flags,9472)               // 256 誰でも + 1024 固定値 + 8192 スキル指定
set(hk_exp_receiver,1)               // 受けた本人へ
set(hk_exp_value,100)
routine(hk_exp_on_buffed)
set(hk_exp_flags,0)
```

**例 42：デバフ攻撃（経験値減少）— 特定の攻撃スキルが当たった相手の経験値 -30**
```
setv(@hk_exp_skill,debuff_skill)     // そのスキルの DAT 上の名前
set(hk_exp_flags,9472)               // 誰でも + 固定値 + スキル指定
set(hk_exp_receiver,4)               // 相手（攻撃を受けた側）
set(hk_exp_value,-30)
routine(hk_exp_on_dealt)
set(hk_exp_flags,0)
```

**例 43：召喚獣がダメージを受けたら、その痛みの半分を召喚した本人の経験値に**
```
set(hk_exp_flags,768)                // 誰でも + 召喚されたユニットだけ
set(hk_exp_receiver,2)               // 本人の親
set(hk_exp_value,500)
routine(hk_exp_on_damaged)
set(hk_exp_flags,0)
```

**例 44：補助スキルを使うたびに、使った本人に +20（支援役の成長）**
```
set(hk_exp_flags,1280)               // 誰でも + 固定値
set(hk_exp_receiver,1)
set(hk_exp_value,20)
routine(hk_exp_on_cast)
set(hk_exp_flags,0)
```

**例 45：士気向上（攻撃）を受けた味方は、30 秒間 取得経験値 1.1 倍**
```
setv(@hk_exp_skill,sp_attack)
set(hk_exp_flags,41216)              // 256 誰でも + 8192 スキル指定 + 32768 時間制限付き
set(hk_exp_receiver,1)               // 受けた本人
set(hk_exp_value,100)                // +10%
set(hk_exp_seconds,30)
routine(hk_exp_on_buffed)
set(hk_exp_flags,0)
```

**例 46：呪い — 攻撃を受けた相手は 20 秒間 取得経験値が半分**
```
setv(@hk_exp_skill,curse_skill)      // 呪いのスキル名
set(hk_exp_flags,41216)
set(hk_exp_receiver,4)               // 相手（攻撃を受けた側）
set(hk_exp_value,-500)
set(hk_exp_seconds,20)
routine(hk_exp_on_dealt)
set(hk_exp_flags,0)
```

**例 47：イベントで、田所に今から 60 秒間 取得経験値 2 倍**
```
setv(@hk_exp_target,tadokoro)
set(hk_exp_value,1000)
set(hk_exp_seconds,60)
routine(hk_exp_timed)
```

### I. 名前の一覧を使う

**例 48：召喚術師の召喚獣が 5 体以上いたら、召喚術師に +100（名前の一覧で数える）**
```
setv(@hk_exp_target,hs_summoner)
routine(hk_exp_list_children)
if (countVar(@hk_exp_list) >= 5)
	{
	set(hk_exp_value,100)
	routine(hk_exp_add)
	}
```

**例 49：s_inyume で出たユニットの 1 体目を、別の関数の対象にする**
```
setv(@hk_exp_dest,s_inyume)
routine(hk_exp_list_skill_all)
if (hk_exp_result > 0)
	{
	storeIndexVar(@hk_exp_list,0,@hk_exp_target)    // 1 体目の名前を対象に写す
	set(hk_exp_value,50)
	routine(hk_exp_add)
	}
```

**例 50：召喚獣の親（召喚した本人）の名前を取り出して、原作の命令に使う**
```
setv(@hk_exp_target,inyume)
routine(hk_exp_list_parent)
if (hk_exp_result == 1)
	{
	storeIndexVar(@hk_exp_list,0,@my_parent)       // 自分の配列変数へ
	// @my_parent を原作の命令（addStatus など、配列を受け取れるもの）に渡す
	}
```

### J. スキルを奪う攻撃（当たった記録を使う）

**例 51：攻撃スキル steal_atk が当たったら、相手の召喚スキル s_inyume を奪って攻撃した本人に渡し、相手の s_inyume の召喚獣を消す**
```
// 戦闘の最初（テンプレート A）: steal_atk が当たったら記録する
setv(@hk_exp_skill,steal_atk)
set(hk_exp_flags,73984)              // 256 誰でも + 8192 スキル指定 + 65536 記録
set(hk_exp_receiver,1)
routine(hk_exp_on_dealt)
set(hk_exp_flags,0)

// battleEvent（毎フレーム）: 記録があれば 1 件ずつ処理
rif (hk_exp_pending > 0)
	{
	routine(hk_exp_hit_pop)
	if (hk_exp_result == 1)
		{
		storeIndexVar(@hk_exp_list,0,@thief)     // 攻撃した側
		storeIndexVar(@hk_exp_list,1,@victim)    // 受けた側
		eraseSkill(@victim,s_inyume)             // 原作の命令（下の注意を参照）
		addSkill2(@thief,s_inyume)               // 原作の命令（同上）
		setv(@hk_exp_dest,s_inyume)
		set(hk_exp_value,0)
		routine(hk_exp_hit_vanish)               // 受けた側の個体の s_inyume の召喚獣を消す
		}
	}
```
- **注意:** `eraseSkill`／`addSkill2` は原作の命令で、ユニットの記録（セーブに残る）を書き換えます。**戦闘中に使ったときの原作の動き（すぐ使えなくなるか、戦闘後か）は未確認**です。試すときはセーブのバックアップを取ってください。
- 同名のモブから奪う場合、`eraseSkill(@victim,…)` は名前で指定する原作の命令なので、どの個体（または全員）から消えるかは原作の仕様次第です。召喚獣を消す部分（`hk_exp_hit_vanish`）は個体ごとに正確です。

**例 52：補助スキルを受けた記録で、受けた側の名前を調べる（いろいろな「当たったとき」処理の土台）**
```
setv(@hk_exp_skill,sp_attack)
set(hk_exp_flags,73984)
set(hk_exp_receiver,1)
routine(hk_exp_on_buffed)
set(hk_exp_flags,0)
// battleEvent で hk_exp_hit_pop → storeIndexVar(@hk_exp_list,1,@buffed) で受けた側の名前
```

---

## 9. 負担について
- ルールは**経験値を得た瞬間だけ**動きます（実測: 1 回平均 0.018 ミリ秒）。
- DAT からの呼び出しは 1 回 0.6 ミリ秒前後です。**毎フレーム呼ばない**でください。テンプレート A のように「最初に 1 回登録」が基本です。テンプレート B（定期）は必要なときだけ、間隔を長めに。
- 詳細ログ（`HakushinExp.ini` の `[log] verbose=1`）は、試験のときだけオンにしてください。

## 10. 制限・今後
| 項目 | 状態 |
|---|---|
| 戦闘の外（戦略画面） | 使えない |
| DAT の skill ブロックから直接呼ぶ | できない（原作の仕様）。代わりに、きっかけルール（§5.10）を戦闘の最初に登録すると、「あるスキルが当たったとき」に働く形でスキルと連動できる |
| 簡易戦闘 | 対応（battleEvent が動く。2026-11-04 確認） |
| 召喚スキルの記録 | 通常戦闘・簡易戦闘の召喚の両方に対応 |
| スキル → そのスキルで召喚したユニット | 数える・消す・経験値の一括操作・ルールの条件（§5.9、ゲーム内確認済み） |
| きっかけルール | ダメージを与えた・受けた、補助スキルを使った・受けた（§5.10、ゲーム内確認済み） |
| 時間制限付きの効果 | 「○秒間 +○%」（§5.11、ゲーム内確認済み） |
| 名前の一覧を返す | §5.12（原作の setv／addv と同じ関数で書き込む） |
| 「味方全員」「敵全員」「このスキルを持つユニット」をルールの対象にする | 予定（今は名前・storeRectUnit・flags 256 で代用） |

## 11. DAT を書くときのチェックリスト（AI・人向け）
1. ファイルは **Shift_JIS・改行 CRLF** で保存した（LF だと起動時に構文エラー）。
2. 戦闘の最初（または呼ぶイベントの先頭）で `routine(hk_exp_setup)` を呼んでいる。
3. **戦闘中に動くイベント**（battleEvent・dead_event）の中で呼んでいる。戦闘前のイベントで呼ぶと -11。
4. ルールの登録はテンプレート A の「成功するまで 1 回」の形にした（毎フレーム登録すると 32 個で -15）。
5. flags を使ったら、すぐ `set(hk_exp_flags,0)` に戻した。
6. value の単位を確認した（倍率・転送・ルールは**千分率**。+30% は 300、1.3 倍の「上乗せ分」として 300）。
7. `@hk_exp_dest` は、渡し先の名前またはスキル名を **setv で 1 つ目に**入れた。
8. 名前は DAT のユニット名（unit の名前、召喚獣は add の名前）、スキル名は skill の名前。
9. 同名のモブを 1 体だけ狙うことはできない（生きているものが 1 体選ばれる）。モブ全体には、ルールの関係指定（parent・root）を使う。
10. 共通イベントの名前は `hk_exp_` で始まる。自分のイベントや変数には `hk_` で始まる名前を使わない（通知基盤が予約）。
11. ゲームを起動したまま、別のプログラムで DAT ファイルを開いたままにしない（起動直後に終了する原因になる）。
12. target に入れる名前は、**戦場に実際に出ているユニットの DAT 上の名前**。定義しただけのユニットや、別の名前で出撃しているユニットは見つからない（-14）。迷ったら詳細ログの `gain` 行の `actor=…[名前]` で実際の名前を確かめる。
13. きっかけルール（§5.10）では `hk_exp_receiver`（渡し先）を、時間制限付き（§5.11）では `hk_exp_seconds`（秒数）を、**呼ぶ前に毎回 set する**（前の値が残る）。
14. スキルで絞るとき（flags 4096・8192）は、`@hk_exp_skill` にスキル名を setv する。`@hk_exp_dest` ではない。スキル名は「実際にその効果を出すスキル」（召喚ならミサイル側のスキル名になることがある）。分からなければ、まずスキル指定なしで登録し、詳細ログの `event_applied … skill=[名前]` や `summon_link … key=[名前]` で確かめる。
15. ダメージ量を使う量の計算（例 38 など）は、即死級・自滅系のスキル（固定 999,999 など）でとても大きくなる。必要なら flags 8192 で対象のスキルに絞る。
16. 消す関数（§5.9）で消えたユニットは「倒れた扱い」。そのユニットの dead_event や break が動く。その dead_event の中から呼んだ hk_exp の関数は無視される。

## 12. 困ったとき
- **何も起きない**: `HakushinExp.ini` の `[log]` を `verbose=1` にして起動し、ゲームフォルダの `HakushinExp.<番号>.log` を見る。`routine_hk_exp_v1` の行の `result=` がエラー番号。
- **起動直後にゲームが消える（終了コード 0）**: DAT ファイルを別のプログラムが開いたままになっていないか確認（実例あり。DLL・DAT の内容が原因ではなかった）。
- **構文エラー**: Shift_JIS・CRLF で保存されているか確認。
- **止めたい**: `hakushin_plugins.conf` の `hakushin.exp` の行の 3 項目目を 0。

## 13. 技術情報（開発者向け）
- DLL の入口は `routine(hk_exp_v1)` 1 つ。hk_exp_op: 0 足す／1 設定／2 倍率／10〜13 参照／20〜22 個別効果／30 ルール登録（hk_exp_to: 0 名前・1 自分・2 親・3 一番上）／31 ルール全消去／32 部隊なし召喚獣／40〜44 親子関係／45・47 召喚スキル／46・48〜51 スキル → 召喚ユニット／33 きっかけルール／23 時間制限付きの効果／60〜64 名前の一覧／70〜73 当たった記録（きっかけルール flags 65536）。
- 詳細: `docs/EXP_PLUGIN.md`、通知基盤 `docs/DAT_ROUTINE_BUS.md`、研究記録: 知識ベース `REF_UNIT_EXP_SUMMON.md` §9・§10。
