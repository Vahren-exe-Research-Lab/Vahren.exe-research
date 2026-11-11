# 確認用の外伝シナリオ（テストDAT）の作り方とつまずき

2026-11-12、Claude。戦闘差し替えの確認用シナリオを作ったときに、作り直しが 4 回必要になった。その原因と、最初から守るべきことをまとめる。対象は ver0.67。

## 1. 最初から守ること（チェックリスト）

- [ ] **`power_order = test` を scenario に書く。** 書かないと既定の `normal`（`context.dat`）になり、「最初の１ターン目は戦争できません」と表示されて 1 ターン目に攻め込めない。本編の動乱（`scenario1.dat`）や他の確認用シナリオも `test`。原作では `0x5A4660` 付近で `power_order` が `normal` かつ初ターンのとき、この表示を出す。
- [ ] **攻め込む先の拠点は中立にする**（どの `power` の `member` にも入れない）。勢力に属する拠点にすると、
  - 敵の主（master）を拠点に置かないと、その勢力がすぐ滅亡する。
  - 主の `yabo`／`kosen` を 0 にしても、配置したボスなど野望の高い人物がいると攻めてくる。

  中立なら攻めてこず、主がいなくても滅亡しない。
- [ ] **プレイヤー勢力の主を本拠地の `member` に入れる。** `master = unit_st` と書くだけでは拠点にいない扱いになり、戦闘に勝っても戦闘後に「主がいない」と判断されて滅亡した。
- [ ] **プレイヤーを十分に強くする。** `class = a000` のレベルを上げるだけでは足りなかった。ユニットに `hp`・`attack`・`defense` などを直接書く（本編のボスのユニット定義と同じ書き方）。敵の拠点は確認対象の人物と少しの兵だけにする。
- [ ] **簡易戦闘で使う fight イベントに `battle{}` を書かない。** 原作の不具合で落ちることがある（[REF_BATTLE_SWAP_HEADLESS.md](../REF_BATTLE_SWAP_HEADLESS.md) §5.2）。戦闘中の条件を確かめたいときは、「この戦闘を見ますか？」に「はい」（画面ありの戦闘）で試す。
- [ ] **fight イベントの文は、すべて `if` の中に入れる。** 本編の `fev1` の書き方（`if (isEvent() || isEvent() == 0) { … }`）に合わせる。
- [ ] **本物のボスや人物を試したいときは、ユニット定義を写さずに名前で置く。** script フォルダの DAT はシナリオに関係なくすべて読まれるので、`member = nisedrgn` のように本編のユニット名を書けば、そのユニットの `break`・`dead_event` などもそのまま使える。
- [ ] **ファイルは CP932・CRLF で保存する。** 新しいフォルダ `script/6xxx_名前/` に置けば、外伝シナリオ一覧に出る（`sortkey` で並び順）。
- [ ] **コメントやシナリオの説明文に `{` `}` を書かない。** 構文の区切りと紛らわしいので避ける。

## 2. 雛形

戦闘差し替えの確認用（`script/6006_戦闘差し替えテスト/battleswap_test.dat`）を短くしたもの。

```
spot sp_t_home:spc
{
name = 本拠地
map = s1919
image = _town3
x = 450
y = 450
member = unit_st,t_hero1,t_hero2,a000*4      // 主（unit_st）を必ず入れる
}

spot sp_t_target:spc                           // 中立（どの power にも入れない）
{
name = 確認対象
map = s1919
image = _town3
x = 200
y = 200
member = t_target,a000*2
}

unit t_hero1
{
name = 味方主力1
class = a000
level = 80
talent = on
member = @
hp = 60000
mp = 1000
attack = 900
magic = 600
defense = 500
speed = 120
}
unit t_hero2 : t_hero1
{
name = 味方主力2
}

unit t_target
{
name = 確認対象の人物
class = a000
level = 1
talent = on
member = @
dead_event = t_dead_ev                         // 倒れたときのイベント
}

event t_dead_ev
{
msg(【戦死イベント】確認対象の人物が倒れた)
}

event t_fight
{
if (isEvent() || isEvent() == 0)
	{
	storeBattleSpot(@t_spot)
	}
if (@t_spot == sp_t_target)
	{
	msg(【開戦イベント】fight イベントが動いた)
	}
if (isEvent() || isEvent() == 0)
	{
	clear(@t_spot)
	}
}

power po_t:p_t
{
	name = 確認(操作)
	flag = flag7
	master = unit_st
	diff = ☆
	head = 説明
	text =
	;
	member = sp_t_home
}

scenario sci_t
{
enable_talent = off
offset = 探索
nozone = on
power_order = test                             // 1ターン目から攻め込める
	name = 確認シナリオ
	text =
	説明文（波かっこを書かない）
	;
	sortkey = 996
	world = we_st
	fight = t_fight
	end_text1 = テスト終了
	end_text2 = テスト終了
	end_text3 = テスト終了
	end_text4 = テスト終了
	end_text5 = テスト終了
	end_text6 = テスト終了
	power = po_t
	;
	spot = sp_t_home,sp_t_target
	;
	roam =
	;
showspot(sp_t_home)
showspot(sp_t_target)
linkSpot(sp_t_home,sp_t_target)
}
```

## 3. 作り直しの記録（何が起きたか）

| 回 | 症状 | 原因 |
|---|---|---|
| 1 | 味方がすぐ全滅、敵が攻めてくる、敵勢力が戦闘に関係なく滅亡 | 味方が弱い。敵の主が好戦的。敵の主を拠点に置いていない |
| 2 | 簡易戦闘の途中でゲームが強制終了（`0x4479DF`） | fight イベントで `battle{}` を設置した（原作の不具合） |
| 3 | 1 ターン目に攻め込めない。ボスが攻めてくる。勝てない | `power_order` 未指定。勢力付きの拠点にボス（野望 100）。味方の能力不足 |
| 4 | 勝ったのに自分の勢力が滅亡 | プレイヤーの主（unit_st）を本拠地に置いていない |
| 5 | 期待どおり（dead_event・fight のメッセージ、勝利、滅亡なし） | — |
