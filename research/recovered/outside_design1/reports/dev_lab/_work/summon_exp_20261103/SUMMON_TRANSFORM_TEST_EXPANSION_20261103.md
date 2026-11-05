# 召喚・変身EXPテスト拡張（2026-11-03）

## 適用先
- DAT: `[USER_HOME]\Documents\迫真戦記\新約迫真戦記―ほのぼの神話ver0.67 豪華版\a_default\script\6001_召喚研究テスト\HS_Summon_Test.dat`
- バックアップ: `[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\_work\summon_exp_20261103\HS_Summon_Test_before_JOKER_dummy_20261103.dat`
- 変更後 SHA256: `BC5EDD389AE258864468F812F0766E85458871875B53368CA375802A0F413853`

## テストの構成
- 味方領地 `hs_summon_home`: `hs_summoner`（帝国照術師Lv1、召喚 `s_inyume`）＋`hs_joker`（原作 `joker` 派生、Lv25、原作の学習仕様維持）
- 敵領地A `hs_summon_enemy`: `hs_target`（帝国歩兵Lv5、移動0、攻撃スキル `a_zan,c_as1`）
- 敵領地B `hs_summon_dummy_home`: `hs_dummy`（Lv99、移動0、攻撃スキルなし、HP500000）
- 両敵領地とも `hs_summon_home` にリンク接続。敵は別勢力。
- 意図せぬLv100バグを避けるため、`exp = 0` と `training_up` の特殊指定は追加していない。

## 原作技能との対応
- `unit joker` は `learn = 25,sp_jocar`。
- `sp_jocar` 「JOCAR発進！！」は車になる技能。内部の `sp_jocar_nt2` に `summon_level = 100` があるため、車 `jocar` がLv100で出るのは原作設定。
- `sp_jocar_dmg` には `str = fix*999999` の攻撃処理があり、変身時に敵へ大ダメージを与える可能性がある。EXP比較は召喚と変身を分けて行う。
- `unit hs_joker : joker` はテスト専用のクローンであり、原作 `joker` 自体は変更していない。

## 検証状態
- CP932書き込み・読み戻し、既存2領地保持、3領地の接続、Lv指定、無抵抗技能解除、参照ID重複なし、各技能の原作存在：静的確認済み。
- ゲーム実機起動、JOKER姉貴のLv25学習技能表示、変身成功、戦闘後経験値：**未検証**。
- 既存セーブに反映されないため、新規シナリオ開始が必要。
