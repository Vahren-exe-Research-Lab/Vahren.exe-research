# 迫真戦記 ver0.67 — 戦闘技能の型・能力フラグ、保存nativeによる限定契約（DEV 2026-10-11）

## 証拠と安全範囲
- ユーザーは正しいゲームルールを説明して推測実装させるのではなく、原本EXEの既存逆コンパイル・逆アセンブル証拠に基づき原作仕様を抽出することを要求。
- 研究B/T011・T013の所有資料を読取専用で利用：exe/T013_FIELD137_CONTEXT.txt（VA0x5739E4..0x573A48）、exe/T013_SKILL_KIND_ENUM.txt（VA0x577827..0x577997）、data/T011_DATA_MODEL.md §13。元命令TXTのSHA256はreports/NATIVE_SKILL_CAPABILITY_SUBSET_20261011.json。
- 原ゲームEXE実行や新たな逆解析process起動、原本DAT/セーブ変更、A〜E他レーン/REA正本変更、Remote、Git stage/commit/pushなし。以前の安全拒否を別経路で再実行していない。

## 保存済み逆アセンブルで確認できる1技能分のフラグ書込
- Skill+0x40がkind1 → Unit+0x134=1（VA0x5739E4..FA）。
- kind2 → Skill+0x278==0ならUnit+0x135=1、非zeroならUnit+0x136=1（VA0x5739FC..0x573A1C）。
- kind3 → Unit+0x137=1（0x573A1E..2D）。kind4 → Unit+0x138=1（0x573A2F..38）。
- 上記通常枝ではSkill+0x4Cがsigned32で正ならUnit+0x139=1（0x573A3E..48）。フィールドの論理用途や実skillの成否は未確定。
- kind5は先行0x573975..0x57398DのUnit+0x130ポインタ保持処理へ、kind6は0x57396Fから別経路へ分岐する。kind5/6・その他を簡易flag計算へ無条件流さずUNKNOWNで停止する。

## 保存済みネイティブ上のaction分類成功枝
- VA0x577827でSkill+0x40==8、VA0x577830でSkill+0x120!=0を確認する入口に限定。
- 該当Unit能力byte非zeroの時だけ、action名とglobal kind/subtypeの局所対応を確定：
  sword +0x134 → (1,0) ／ bow +0x135 → (2,0) ／ magic +0x136 → (2,1) ／ heal +0x137 → (3,0) ／ care +0x137 → (3,1) ／ powerup +0x137 → (3,2) ／ summon +0x138 → (4,0)。
- Unit+0x137はheal/care/powerup共通のsupport能力確認であり、3アクションが同じ意味になるとは言えない。
- Unit側flag欠如の場合の0x577999以降や未知action、実命令実行、MP/RNG/攻撃結果はこの部分の証拠だけでは不明。絶対に使用不能という結論にしない。

## 制作DEVに追加したコード
- src/hakushin_compat/native_skill_capability_subset.py：native保存分岐の成功時だけLocalCapabilityWrite/LocalActionDispatchを返す。未取得・未立証経路はNativeSkillContractUnknownでfail-closed。
- tests/test_native_skill_capability_subset.py：通常type1..4とfield278/field4c境界、7行動のkind/subtype、共有support、type5/6拒否、ガード不一致や型誤り拒否、実機動作保証FALSEを検査。専用12/12 PASS。
- reports/NATIVE_SKILL_CAPABILITY_SUBSET_20261011.json：出典txtのsha256とVA、局所結果の合成サンプル、未解決事項をJSON保存。
- 今回確認したのは「元命令のこの分岐結果」と「新Pythonの合成unit test」。原作旧EXE Gameplay Golden0、新strict MATCH0のまま。試遊EXEの創作攻撃・回復へは接続していない。

## 次の重要課題
1. B/T011＋A/T005：本当のUnit/Class parent優先・継承値とEffectiveSkill合成/学習/削除によるcache更新を証拠に基づき確定。
2. B/T013：type5/6、0x577999フォールバック、actionの最終実行、原作MP/RNG/AI決定のreader/caller traceを独立検証。
3. E/T018：実機合法UIでの同条件skill/HP/MP/行動結果をGoldenとして計測し、静的分岐・推測・合成fixtureと区別。
