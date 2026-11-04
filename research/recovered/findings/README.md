# 主要解析記録と辞書の出典

[主要解析記録の部分版](PEER_SCRIPT01_FINDINGS_20261011.md) は、既存辞書の `F§…` や `C(§…)` が指していたClaudeの解析記録を、節ごとに参照できるようにしたもの。

関数・フィールドのページには、原本の略記と実際の節へのリンクを併記する。出典のSHA256と節アンカーを検査するため、本文の差し替えや存在しない節へのリンクは生成時に検出できる。

## 収録範囲

原本4,683行のうち4,124行を保持した。個人パスを含む段落、保留対象への言及を含む段落、未確認の付録は、原文の行範囲を示すプレースホルダーに置き換えた。詳細は [除外範囲と原本・保存版SHA](SCREENING.json) に記録する。原本は研究PCに保持している。

これは自動スクリーニング済みの部分版。ファイル全体の手動による意味・プライバシー確認は継続課題。元の `CONFIRMED` などは当時の確認方法を表す表記であり、今回新しく実機確認したことを示さない。

目録の原本SHAと現在の原本SHAは異なる。収録状況は `SOURCE_REVISION_DIFFERS` とし、古い目録版の全文を回収済みとは扱わない。[総合回収台帳](../RECOVERY_LEDGER.tsv) と [全目録の照合](../COVERAGE.md) から対応を追跡できる。

## よく使う入口

- [Unit能力値の生成・第22節](PEER_SCRIPT01_FINDINGS_20261011.md#f-22)
- [親定義の解決・第21節](PEER_SCRIPT01_FINDINGS_20261011.md#f-21)
- [friend集合・第30節](PEER_SCRIPT01_FINDINGS_20261011.md#f-30)
- [レベルアップ・第31節](PEER_SCRIPT01_FINDINGS_20261011.md#f-31)
- [勢力・領地・第58節](PEER_SCRIPT01_FINDINGS_20261011.md#f-58)
- [通常セーブに関係する状態・第79節](PEER_SCRIPT01_FINDINGS_20261011.md#f-79)
- [詳細パネルの条件・第93節](PEER_SCRIPT01_FINDINGS_20261011.md#f-93)
- [詳細パネルのボタン処理・第95節](PEER_SCRIPT01_FINDINGS_20261011.md#f-95)

## GitHub取得コピーでの確認

[収録コミット683d5f8](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/commit/683d5f8b40a044d37ac63d3a8bc2509d8073d9f8)を別クローンへ取得し、737項目のマニフェスト一致、原本SHA一致、除外範囲以外の4,124行から保存版を再構成できることを確認した。189項目の出典リンクと、TempStatusWndの解雇フィールドからC(§93)の実在する節へ到達することを検証済み。検索18試験、収録範囲11試験は成功。[PR #23](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/23)に変更範囲を記録している。全体の手動確認と、除外部分の扱いは継続課題。
