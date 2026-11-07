# HakushinExp v1.0 説明書 ― DAT から経験値と召喚の親子関係を扱う

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

**ゲーム内で確認済み**: 通常戦闘（2026-11-03、JOKER姉貴の変身・帝国照術師の召喚で確認）。
**未確認**: 簡易戦闘（CPU 同士の戦闘）。召喚スキルの記録は、今は通常戦闘の召喚だけです（§10）。

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

### 2.3 「すぐ反映」と「ルール」の違い
| | すぐ反映（操作） | ルール |
|---|---|---|
| いつ効く | 呼んだその瞬間に 1 回 | 戦闘中、経験値を得るたびに自動で |
| 対象 | そのとき戦場にいるユニット | 名前・条件で指定。**あとから出てきた召喚獣にも効く** |
| 例 | 「+100」 | 「得た経験値を 1.3 倍」 |
| 消えるとき | — | 戦闘が終わると自動で消える |

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
| `hk_exp_value` | 数値 | 入力 | 値（意味は関数ごと） |
| `hk_exp_flags` | 数値 | 入力 | オプション（§6）。使い終わったら 0 に戻す |
| `hk_exp_result` | 数値 | 出力 | 処理した数。マイナスはエラー（§7） |
| `hk_exp_out` | 数値 | 出力 | 調べた答え、または増減の合計 |
| `hk_exp_op`、`hk_exp_to` | 数値 | 内部用 | 共通イベントが自動で設定する。触らない |

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

## 5. 関数リファレンス（共通イベント 25 個）

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
- 記録されるのは、DLL を入れてからその戦闘で行われた召喚だけです。

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

早見表:

| やりたいこと | flags |
|---|---|
| 召喚された誰でも | 768（256＋512） |
| 召喚された誰でも、倒れた親には渡さない | 769（1＋256＋512） |
| 召喚された誰でも、固定値 | 1792（256＋512＋1024） |
| 誰でも、固定値 | 1280（256＋1024） |
| 名前で指定、減ったときも連動 | 2048 |

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

---

## 9. 負担について
- ルールは**経験値を得た瞬間だけ**動きます（実測: 1 回平均 0.018 ミリ秒）。
- DAT からの呼び出しは 1 回 0.6 ミリ秒前後です。**毎フレーム呼ばない**でください。テンプレート A のように「最初に 1 回登録」が基本です。テンプレート B（定期）は必要なときだけ、間隔を長めに。
- 詳細ログ（`HakushinExp.ini` の `[log] verbose=1`）は、試験のときだけオンにしてください。

## 10. 制限・今後
| 項目 | 状態 |
|---|---|
| 戦闘の外（戦略画面） | 使えない |
| DAT の skill ブロックから直接呼ぶ | できない（原作の仕様）。戦闘開始・定期・死亡時のイベントから使う |
| 簡易戦闘 | 未確認（次に確認予定） |
| 召喚スキルの記録 | 通常戦闘の召喚のみ。簡易戦闘の召喚は次に対応予定 |
| スキル → そのスキルで召喚したユニット（一覧・消滅など） | 次に作る予定（新しい関数として追加） |
| 名前の一覧を返す | 未対応（DLL から DAT の配列を書く安全な方法を調査中） |
| 「味方全員」「このスキルを持つユニット」の指定 | 予定（今は名前・storeRectUnit で代用） |

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

## 12. 困ったとき
- **何も起きない**: `HakushinExp.ini` の `[log]` を `verbose=1` にして起動し、ゲームフォルダの `HakushinExp.<番号>.log` を見る。`routine_hk_exp_v1` の行の `result=` がエラー番号。
- **起動直後にゲームが消える（終了コード 0）**: DAT ファイルを別のプログラムが開いたままになっていないか確認（実例あり。DLL・DAT の内容が原因ではなかった）。
- **構文エラー**: Shift_JIS・CRLF で保存されているか確認。
- **止めたい**: `hakushin_plugins.conf` の `hakushin.exp` の行の 3 項目目を 0。

## 13. 技術情報（開発者向け）
- DLL の入口は `routine(hk_exp_v1)` 1 つ。hk_exp_op: 0 足す／1 設定／2 倍率／10〜13 参照／20〜22 個別効果／30 ルール登録（hk_exp_to: 0 名前・1 自分・2 親・3 一番上）／31 ルール全消去／32 部隊なし召喚獣／40〜44 親子関係／45・47 召喚スキル。
- 詳細: `docs/EXP_PLUGIN.md`、通知基盤 `docs/DAT_ROUTINE_BUS.md`、研究記録: 知識ベース `REF_UNIT_EXP_SUMMON.md` §9・§10。
