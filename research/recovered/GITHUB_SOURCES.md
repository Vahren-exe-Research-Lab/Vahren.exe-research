# GitHub受付・所在メタデータの照合

取得完了: **2026-11-04 22:25:34 UTC（2026-11-05 07:25:34 JST）**。GitHubの`develop`とローカル比較基準は`c8b9686a136763b678495afafb4cd13b9b9fde8a`。固定コミットの順次検査であり、その後の更新や今回の追加回収を含む将来の先端は自動的に反映しない。

これは所在・保存版同一性の目録である。GitHubでの保存、正本とのバイト一致、研究知識としての採録は区別する。題名・パス・件数から意味の妥当性や公開可否を判定しない。

- [受付一覧](GITHUB_QUEUE.tsv): open PR **13件（#7–#19）**とopen Issue **6件**。番号・題名・状態・更新時刻・URL・PR固定HEADだけを取得した。本文は取得せず、`body_sha256` は `NOT_FETCHED_METADATA_ONLY` のままとする。これはハッシュではない。
- [PR研究ファイル目録](GITHUB_SOURCE_CATALOG.tsv): 固定HEADの`research/`配下 **1,693 blob所在／1,143種類のblob SHA1**。PRの研究ツリー全体であり、各PRが追加した差分だけではない。同じバイト列の複数所在も保持する。
- [回収保存版とのGit blob一致](GITHUB_EXACT_BODY_LINKS.tsv): **96対応**。基準コミットの回収台帳899行にある保存先とPR内blob SHA1を結ぶ。原本全文との一致は、別途[回収台帳](RECOVERY_LEDGER.tsv)の原本SHA・保存版SHA・回収状態で確認する。部分回収や個人情報整形版が原本全文と同じとは扱わない。
- [正本との差分・発見キュー](GITHUB_DISCOVERY_DIFF.tsv): 全1,693所在を基準developの全ツリーと比較し、同一blobの別名・同名の別内容・PRだけの所在を区別する。元カタログと回収台帳への対応も、文字通りのパス一致と本文同一性を分ける。

| 状態 | PR内の所在数 | 意味 |
|---|---:|---|
| `EXACT_ALREADY_DEVELOP` | 706 | 同じGit blob SHA1が正本のいずれかのパスにある。意味の採録済みとは限らない。 |
| `SAME_PATH_CHANGED` | 35 | 同じパスがあるが内容は異なり、同一blobも正本の他パスにない。 |
| `AVAILABLE_QUEUE_ONLY` | 952 | 同じパスも同一blobも正本に見つからない。追加確認の候補であり、新発見・採用可能の判定ではない。 |

## 前回の所在目録からの変化

前回の比較基準は`14b3cbc83c2188680a29eb7fcae8d859072c62ba`、1,682所在。今回1,693所在となり、同じPR番号・同じパスをキーに追加11、blob変更11、同一1,671、削除0。正本との比較とは異なる。PR HEADの変更は次の3件。

| PR | 前回HEAD | 今回HEAD |
|---|---|---|
| [#16](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/16) | `897d2ae43be06512820536c212c9de29a7f77843` | `35dfcb14b70940ded4a5dcfeca8347ae009694a1` |
| [#17](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/17) | `a2ae9a28386bcf6bec03c55cd06aa31ab5994057` | `c6abc1e0c065280125d7122659a7ee7a4360c12a` |
| [#18](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/18) | `6acb3d7277df30b4d380fe473b93007d2a33c95d` | `144f93f6ebe1adc1c0706d31ac20300fad0b8cbe` |

各所在行の`previous_pr_blob_sha1`と`change_since_previous_catalog`で追跡できる。追加されたパスも本文は取得していない。古い目録はGit履歴に残り、受付の現在値と混同しない。

## 取得方法と検証の境界

GitHub接続ツールには返却本文の項目選択がないため、GitHub CLI経由のGraphQLで必要なメタデータだけ要求した。open PR/Issueとも`hasNextPage=false`を確認し、repository PRIVATEとdefault branch developのSHAを照合した。取得中のPR HEADは受付表へ固定する。

変更されたPR16/17/18だけRESTの`git/trees/{固定SHA}?recursive=1`で更新し、3応答すべて`truncated=false`。残る10件は固定HEADが前回と同じなので、前回完全取得した不変Git treeのメタデータを再利用した。キャッシュ再利用を今回の再ダウンロードとは数えない。source/raw/blob本文API、添付・コード・ログの取得や実行はしていない。

正本は同じ固定SHAの`git ls-tree -r --long`全ツリーを使用し、Git blob SHA1同士で比較した。原本SHA256をGit SHA1と比較しない。原本カタログと回収台帳も基準コミットの版を読み、未コミットの新回収を比較へ混ぜていない。Issue本文・PR本文・ローカル原本・ゲーム・保留対象本文はこの所在照合では開いていない。

この一覧は保留解除・未採用本文の自動取得・削除を認めない。従来の[スコープ監査](e_reports/SCOPE_AUDIT.md)や個別DEFERREDの境界を維持する。現在採録した関数・メモリは[事典](../../reference/README.md)、保存本文と制約は[回収の入口](README.md)、既存の採録判断は[受付統合履歴](../intake/README.md)を参照する。
