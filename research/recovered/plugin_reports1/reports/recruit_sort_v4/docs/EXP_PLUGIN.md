# HakushinExp（経験値の操作）プラグイン

作成: Claude（2026-11-03）。状態: DAT 命令 `routine(hk_exp_v1)` の全操作（0・1・2・10〜13・20〜22）と、戦闘の最初に 1 回登録するルール（30）を通常戦闘でゲーム内確認済み（2026-11-03。2 戦連続で台帳・ルールの作り直しも確認。経験値の変化 1 回あたり平均 18µs）。未確認: 簡易戦闘、同名モブが複数いる実機、flags。完成前の版。

## DAT から使う（`routine(hk_exp_v1)`、通知基盤 docs/DAT_ROUTINE_BUS.md 経由）

- 事前に数値変数 `hk_exp_op`／`hk_exp_value`／`hk_exp_flags`／`hk_exp_result`／`hk_exp_out` を set し、配列変数 `@hk_exp_target`（op 21 では `@hk_exp_dest` も）を setv/addv しておく。空の `event hk_exp_v1 { }` を定義しておく。
- ルール（op 30、共通イベント hk_exp_rule_to_name/self/parent/root、op 31 で全消去）: 戦闘の最初に 1 回登録すると、その戦闘中に経験値を得た瞬間に働く（あとから出た召喚獣にも効く）。親・一番上の親は名前ではなくその個体の親子関係でたどる。flags 256 誰でも／512 召喚されたユニットだけ／1024 固定値／2048 減ったときも。
- op: 0 足す／1 設定／2 千分率で掛ける、10 今の値／11 戦闘開始時の値／12 戦闘で得た量／13 手で変えた量（最初の対象、答えは hk_exp_out）、20 倍率（この戦闘）、21 転送（この戦闘、`@hk_exp_dest` の最初の名前へ、value は千分率）、22 20・21 の解除。
- hk_exp_result: 処理した数、または負（-10 変数なし、-11 戦闘外、-12 op 不正、-13 転送先なし、-14 対象なし）。
- 名前は原作の戦闘中ユニットの名前表（評価器＝context+0x504 の +0x1EEBEC）を読み取りで引く。同名なら生存を優先（原作 0x49E780 と同じ）。
- 台帳は経験値の記録ごと。新しい戦闘で自動的に空になる。
- 例（試験 DAT）: 30 フレームごとに op 21 で jocar,joker_re → hs_joker 1000‰。
根拠: 研究 findings §96（`dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md`）、知識ベース `REF_UNIT_EXP_SUMMON.md` §9。

## 関数（DLL の書き出し）

ゲームのスレッドから、戦闘中のユニットに対して呼ぶこと。

| 関数 | 内容 |
|---|---|
| `int32 HakushinExp_Apply(void *battleUnit, int32 op, int32 value, uint32 flags, int32 *changed)` | 戦闘中のユニットの経験値を操作 |
| `int32 HakushinExp_ApplyToUnitData(void *unitData, int32 op, int32 value, uint32 flags, int32 *changed)` | ユニットの記録（UnitData）を直接操作 |
| `void *HakushinExp_FindUnitByTag(void *nearUnit, const char *tag)` | 同じ陣営で、タグ（DAT のユニット名）が一致するユニット。生きている方を優先、いなければ倒れたユニット |
| `void *HakushinExp_FindSummonParent(void *child)` / `HakushinExp_FindSummonRoot(void *child, uint32 flags)` | 召喚の親／一番上の親（参考。今は重点を置かない） |

- op: `0` 足す（value が負なら引く）、`1` 設定する、`2` 千分率で掛ける（500 = 半分）。
- 経験値は 0〜0xFFFFFFFF に収める。レベルは下がらない（原作にレベルダウンがないため）。
- 戻り値: 0 = 実行、負 = しなかった（-1 引数、-2 記録なし、-3 倒れている、-4 原作の条件、-5 op 不正）。`changed` に実際の増減（符号付き）。
- flags: `0x1` 倒れていたら何もしない、`0x2` 原作と同じ条件（部隊あり・経験値禁止なし）のときだけ、`0x4` 通常戦闘でもすぐレベルアップ判定、`0x8` レベルアップ判定をしない。
- 増えたとき、簡易戦闘のユニットはすぐレベルアップ判定（原作 0x58A650）。通常戦闘は戦闘終了時の原作の判定（0x575110）に任せる。

## ルール（`HakushinExp.ini`、Vahren.exe と同じフォルダ）

原作の経験値処理（0x551E50）で、あるユニットの経験値が変化した瞬間に動く。変化量は符号付き。`[rule1]`〜`[rule16]`。

```ini
[rule1]
source=jocar,joker_re   ; 変化したユニットのタグ（カンマ区切り）。空なら全員
when=gain               ; gain=増えたとき / loss=減ったとき / both
target=joker            ; self / parent / root / ユニットのタグ
mode=delta              ; delta=変化量×value/1000 / fixed=value をそのまま
value=1000              ; 負の数も可（例 -1000 で同じ量を引く、fixed=100 で毎回 100）
give_to_dead=1          ; 倒れている受け手にも渡す
take_from_source=0      ; 1 なら渡した分を変化したユニットから引く（移動）
enabled=1

[log]
verbose=1               ; 完成前の版は既定 1
```

例:
- JOKER姉貴の変身: 上の rule1。車と戻った JOKER が得た分が、倒れていても JOKER姉貴に入る。
- 経験値取得ごとに固定 100 を追加: `source=xxx target=self mode=fixed value=100`
- 召喚獣の取得を無効にする: `source=召喚獣のタグ target=self mode=delta value=-1000`

ルールで足した分はルールの引き金にならない（連鎖しない）。死亡時の減少（dead_penalty）や吸収など、0x551E50 以外の変化はまだ捕まえない。

## ログ（`HakushinExp.<プロセス番号>.log`）

`config`/`rule` 設定、`active` 差し替え完了、`gain` 変化のたび（量・ユニット・経験値・閾値・レベル・部隊・倒れているか・親）、`rule_applied`/`rule_skipped` ルールの結果、`api_apply` 関数の呼び出し。最大 8 MB。

## 導入・ビルド・試験

- `plugins/HakushinExp.dll`、`hakushin_plugins.conf` に `hakushin.exp|HakushinExp.dll|1|30|1||<SHA-256>`。
- 差し替えは原作の 0x551E50 呼び出し 4 か所（0x547A8C、0x551167、0x551C6A、0x57F4E9）。起動時の読み込みが終わった後、UI スレッドで入れる。外すには再起動。ルールなし・ログなしなら差し替えない。
- ビルド: `core/build_exp_plugin.ps1 -Test`（`-Quiet` で既定ログなし）。
- 試験: `test_exp_logic.c`（操作・上限・タグ検索・ルール全種）、`test_exp_plugin.c`（偽の原作関数で呼び出し規約の中継・レジスタ保存・符号付き変化・ルール）。-O0/-O2 合格。ゲーム内は未確認。
