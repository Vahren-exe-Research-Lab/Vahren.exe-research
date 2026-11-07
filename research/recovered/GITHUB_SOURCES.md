# GitHubの受付・本文所在の照合

2026年11月5日に取得した、未統合の担当PRとIssueのスナップショット。本文の意味や確度を判定する一覧とは区別する。

- [受付一覧](GITHUB_QUEUE.tsv) は取得時点の13PR・6Issueを記録する。本文は転記せずSHA256を記録し、後の改版を照合できる。
- [担当PRの研究ファイル目録](GITHUB_SOURCE_CATALOG.tsv) は、固定HEADごとのresearch/配下の1680 blobレコードを記録する。同じ本文が複数のPRに存在する場合も別の所在として保持する。
- [原本一致の対応](GITHUB_EXACT_BODY_LINKS.tsv) は、回収本文のGit blob SHA1とPR内blob SHA1の完全一致で対応付けた。ファイル名が違っていても同じ本文を拾う。

これは元報告や証拠本体の回収とは別の検査。PR内にファイル名・研究IDがないことだけで、知見の不在や欠落とは判定しない。blob一致は同じバイト列の所在を示し、独立した発見や原作動作の追加証明ではない。

このGitHub目録作成では保留対象の本文を取得していない。この目録にある名前は所在メタデータであり、保留の解除・本文公開許可にはしない。新しい受付や改版は、最新HEAD・本文SHA・既存の訂正を再照合する。

主な担当受付は [BのPR18](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/18)、[EのPR17](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/17)、[REAのPR16](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/16)。正本へ反映済みの資料は [回収本文の入口](README.md) と [受付統合履歴](../intake/README.md) を参照する。

## 検査方法

GitHub APIで各PRの固定HEADの完全ツリーを取得し、truncatedが偽であることを確認した。元のnative出力・保留本文のblobは開かず、path・blob SHA1・サイズ・modeを使う。原本一致の対応は、回収本文のbytesにGitのblobヘッダーを付けたSHA1を比較した。21対応は複数PRの所在を含み、21件の新しい発見を示さない。
