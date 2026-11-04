# GitHub受付・所在メタデータの照合

取得完了: **2026-11-04 20:02:24 UTC（2026-11-05 05:02:24 JST）**。GitHubの`develop`とローカル比較基準はいずれも`14b3cbc83c2188680a29eb7fcae8d859072c62ba`。固定HEADを順次検査したスナップショットであり、その後の更新を含まない。

これは発見用の所在目録である。GitHubでの保存、正本とのバイト一致、研究知見としての選択採用は別々に扱う。PRタイトル・パス名・件数から意味や妥当性を判定しない。

- [受付一覧](GITHUB_QUEUE.tsv): open PR **13件（#7–#19）**、open Issue **6件**。番号・タイトル・状態・更新時刻・URL・PR固定HEADのみ取得した。既存の`body_sha256`列は保持し、今回の値は`NOT_FETCHED_METADATA_ONLY`とした。これはハッシュではなく未取得状態の明示値である。本文を取得していないため、過去の本文ハッシュを現在の値として再利用しない。以前の値はGit履歴にある。
- [PR研究ファイル目録](GITHUB_SOURCE_CATALOG.tsv): 各固定HEADの`research/`配下 **1,682 blob所在レコード／1,132種類のblob SHA1**。同一内容が複数PRにある場合も所在ごとに保持する。PRの全研究ツリーであり、そのPRが追加したファイルだけではない。
- [回収済み原本との完全一致](GITHUB_EXACT_BODY_LINKS.tsv): **21対応**。回収台帳の保存先をローカル固定コミットのGit object IDに結び、PRのblob SHA1と一致する所在を記録した。原本・回収本文は開いていない。対応数は新しい発見数ではない。
- [developとの差分・発見キュー](GITHUB_DISCOVERY_DIFF.tsv): 上記1,682所在を`develop`全ツリーと比較する。完全一致の既存所在、同名の別内容、PRにのみあるバイト列を分け、ローカル固定コミット・回収台帳・原本目録へのメタデータ対応を併記する。

| 発見状態 | PR内の所在数 | 意味 |
|---|---:|---|
| `EXACT_ALREADY_DEVELOP` | 667 | 同じblob SHA1がdevelopのいずれかのパスに存在する。別名も照合した。 |
| `SAME_PATH_CHANGED` | 35 | 同じパスがdevelopにあるがSHA1が異なり、同一blobはdevelopの他パスにも見つからない。 |
| `AVAILABLE_QUEUE_ONLY` | 980 | 同じパスも同一blobもdevelopに見つからない。GitHub内で所在が確認できる候補である。 |

同じblobの複数所在を含む。`EXACT_ALREADY_DEVELOP`は意味の検証済み・キュレーション済みを意味しない。残る1,015所在も新規知見・採用可能・公開許可の判定ではない。原本目録との文字通りのパス一致は`catalog_same_literal_path`で区別し、完全一致とは扱わない。

## 前回目録からの更新

| PR | 前回HEAD | 今回HEAD |
|---|---|---|
| [#16](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/16) | `4dff901123c35df0d5c164cf57e23e8f52306571` | `897d2ae43be06512820536c212c9de29a7f77843` |
| [#17](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/17) | `86781bc5c83558706c3c6504b7fa563f303b2cff` | `a2ae9a28386bcf6bec03c55cd06aa31ab5994057` |
| [#18](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/18) | `938532ae3b345d5a3612bfadbc65ce5938fb6cb4` | `6acb3d7277df30b4d380fe473b93007d2a33c95d` |

研究所在は前回1,680件から1,682件へ増加。同じPR・同じパスをキーに、追加2、SHA1変更6、同一1,674、削除0。各行の`previous_pr_blob_sha1`と`change_since_previous_catalog`で確認できる。ここでの変更は前回PR目録との比較であり、developとの差分とは異なる。

新規パスはPR16の`research/intake/REA/REA_20261105_04H_T013_T014_OLD_OWNER_SEMANTIC_CURATION_CROSSWALK.md`とPR17の`research/intake/E/repro/t020_e_t028_retreat_strict_type_admission_20261105.py`。名前の所在のみを記録し、内容の検査・実行・意味の採用はしていない。

## 検査方法と境界

GitHub CLI `gh 2.100.0`からGraphQLでopen PR/Issueの必要なメタデータ項目だけを取得し、両接続の`hasNextPage=false`を確認した。本文フィールドは要求していない。REST `GET /repos/ButaMonky/Hakushin067-Research-Knowledge/git/trees/{固定SHA}?recursive=1`でdevelopおよび13 PRの完全ツリーを取得し、全14応答の`truncated=false`を確認した。各PRのHEADは受付一覧と各所在行に記録する。

ローカルでは`git ls-tree -r --full-tree 14b3cbc83c2188680a29eb7fcae8d859072c62ba`によるパス・object IDと、[回収台帳](RECOVERY_LEDGER.tsv)、[原本目録](../../RESEARCH_SOURCE_CATALOG.tsv)のメタデータのみを使った。Git blob SHA1同士で完全一致を判定し、原本の`source_sha256`をGit blob SHA1と比較していない。GitHub blob/raw/download APIは使用していない。PR/Issue本文、ローカル原本、ゲームファイル、保留証拠、コード・再現物の本文は表示・保存・内容検査・実行していない。初期HEAD確認の1回だけRESTのPR一覧をghの--jqで番号・HEAD・タイトルに絞った。このREST応答は本文欄を含み得るため、本文フィールドの非受信までは主張しない。実際の目録更新は本文欄を要求しないGraphQLへ切り替えた。

この目録は保留解除や新たな本文閲覧を認めない。[既存のE受入スコープ監査](e_reports/SCOPE_AUDIT.md)を含む従来の除外・保留条件は維持する。今回の所在名の列挙は、その資料の内容や結論を採用する根拠ではない。採用済みの説明は[回収本文の入口](README.md)と[受付統合履歴](../intake/README.md)で確認する。
