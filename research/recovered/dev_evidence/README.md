# ミニマップ・技能能力の再現用資料

ローカルに残っていた作者作成の限定モデル、専用テスト、監査JSONを、元ファイルと同じバイト列で回収しました。
対応する研究本文は [ミニマップの解析](../DEVLAB_MINIMAP_NATIVE_CONTRACT_20261011.md) と [技能能力の解析](../DEVLAB_NATIVE_SKILL_CAPABILITY_20261011.md) です。

## 内容

| 研究 | 実装 | テスト | 監査記録 |
|---|---|---|---|
| ミニマップのセル算術・頂点配列 | [Pythonモデル](src/hakushin_compat/native_minimap_static_subset.py) | [専用テスト](tests/test_native_minimap_static_subset.py) | [JSON](reports/MINIMAP_NATIVE_STATIC_AUDIT_20261011.json) |
| 技能種別と能力バイトの局所分岐 | [Pythonモデル](src/hakushin_compat/native_skill_capability_subset.py) | [専用テスト](tests/test_native_skill_capability_subset.py) | [JSON](reports/NATIVE_SKILL_CAPABILITY_SUBSET_20261011.json) |

元資料と回収先のSHA-256、照合範囲は [回収台帳](DEV_EVIDENCE_LEDGER.tsv) にあります。
回収時には正本と13件のオープンPRの先端ツリーでファイル名を検索し、該当ファイルが存在しないことを確認しました。

## ゲームを使わない再現

Python 3.12で、リポジトリのルートから次を実行します。外部パッケージは不要です。

```powershell
$env:PYTHONPATH = (Resolve-Path research/recovered/dev_evidence/src).Path
python -B -m unittest discover -s research/recovered/dev_evidence/tests -p test_native_skill_capability_subset.py -v
python -B -m unittest discover -s research/recovered/dev_evidence/tests -p test_native_minimap_static_subset.py -v
```

2026年11月5日の回収先での再実行は、技能能力が12件成功、ミニマップが22件成功・3件スキップでした。
ミニマップの3件は保存済み逆コンパイルZIPに依存する照合で、そのZIPは同梱していません。
監査JSON内の過去の25件成功は当時の記録として保持しています。現在の配布資料だけでその3件を検証したことにはなりません。
ミニマップJSONに記されたモデルとテストのSHA-256は、今回回収した2ファイルと一致しました。

これらは局所的な算術・分岐の合成テストです。原作実機の動作、最終的な技能集合、霧の意味、実画面の座標変換、ゲーム全体の互換性は別の検証項目です。
