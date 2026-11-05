# GitHub受付・所在メタデータの照合

取得完了: **2026-11-05 00:30:02 UTC（2026-11-05 09:30:02 JST）**。比較基準はdevelop **`2a6af7b389d82a92b85bef475aaf981d31d1990d`**。この固定版の回収台帳1395行と正本全ツリーを使い、今回の未コミット追加回収や将来の先端を混ぜていない。

これは所在と保存版の同一性の目録であり、研究の正しさ・正式採録・全原本回収とは区別する。今回のメタデータ票は[取得票](GITHUB_METADATA_RECEIPT.json)から追跡できる。

- [受付一覧](GITHUB_QUEUE.tsv): open PR 13件（#7–#19）とopen Issue 6件。題名・状態・時刻・URL・PR固定HEADのみ。本文は取得せず、body_sha256のNOT_FETCHED_METADATA_ONLYはハッシュではない。
- [PR研究ファイル目録](GITHUB_SOURCE_CATALOG.tsv): research配下1695 blob所在、1145種類のGit blob SHA1。PRごとの研究ツリー全体で、各PRが追加した差分だけではない。
- [回収保存版とのGit blob一致](GITHUB_EXACT_BODY_LINKS.tsv): 99対応。基準版の採用済み保存先と同じGit blobの所在を結ぶ。原本全文との一致・個人情報整形・版違いは別途[回収台帳](RECOVERY_LEDGER.tsv)の原本/保存版SHA256と確認範囲で判断する。
- [正本との差分・発見キュー](GITHUB_DISCOVERY_DIFF.tsv): 同一blobの別名、同名別内容、PR側だけの所在を分ける。旧目録のliteralパス、回収台帳のsource SHA、Git blob SHA1を混同しない。

| 状態 | PR内の所在数 | 意味 |
|---|---:|---|
| EXACT_ALREADY_DEVELOP | 709 | 正本のどこかに同じGit blobがある。意味の正式採録済みとは限らない。 |
| SAME_PATH_CHANGED | 35 | 同名パスはあるが内容が異なり、同じblobは正本の他の場所にも見つからない。 |
| AVAILABLE_QUEUE_ONLY | 951 | 同名も同一blobも基準正本に見つからない。新発見・未保存全原本・採用可能の判定ではない。 |

## 前回からの変化

前回はc8b9686a版基準、1693所在・1143種類。今回同じPR番号＋パスで追加2、blob変更7、同一1686、削除0。正本との比較とは別の集計。変更3HEADは次の固定版へ更新した。

| PR | 前回HEAD | 今回HEAD |
|---|---|---|
| [#16](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/16) | `35dfcb14b70940ded4a5dcfeca8347ae009694a1` | `68c5ec9ec766776f027ac27e77c8b50d0f3b80de` |
| [#17](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/17) | `c6abc1e0c065280125d7122659a7ee7a4360c12a` | `f22c89d3a691ab6b431cbfaa56cbcdd01ea593d2` |
| [#18](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/18) | `144f93f6ebe1adc1c0706d31ac20300fad0b8cbe` | `885ad7a069a2b67cf3ba378e7241341ad951128b` |

新規2所在はREAの旧空間・vector研究のcurator crosswalk Markdownと、Eの合成判定補助Python。変更7所在はREA INDEX、E INDEX/対応表、Bの4報告。パスや題名だけで採用しない。Bの2022系IDは既知の保留関連crosswalkのID群にも現れるため、依存が解決するまで別経路で本文を取り直さない。これは個々のB報告の取得拒否が新たに確定したという意味ではない。Eコードもメタデータ所在のみで取得・実行していない。選択したREA本文は独立レビューで既知の保留2本文との具体的な依存が確認されたため、全体を保留して本文は保存せず、[PR crosswalkの確認票](pr_crosswalk1/README.md)だけ残す。

## 取得方法と検証の境界

接続ツールではPR/Issue本文を除外する項目選択ができないため、GitHub CLIのGraphQLで上記メタデータだけを指定した。repository PRIVATE、default branch developと固定SHA、両一覧hasNextPage=falseを確認。変わったPR16/17/18の固定HEADのgit/treesを取得し、3応答ともtruncated=false。残り10件は前回完全取得した不変HEADのツリーメタデータを再利用し、今回の再ダウンロードとは数えない。

正本は固定SHAのgit ls-tree全ツリー、元の目録と回収台帳も同じGit版を用いた。Git blob SHA1同士を比較し、原本SHA256と混ぜていない。この所在点検ではIssue/PR本文・原本・ゲーム・保留本文・リンク先コードや証拠を取得していない。別途選択・レビューした1研究本文も全体を保留した。個別レビューは本目録の網羅性を広げず、新しい採用本文にも数えない。

この目録は保留解除、自動取得、正式採録や削除の許可ではない。現在の知識は[事典](../../reference/README.md)とREF・訂正根拠、回収の制約は[入口](README.md)・[スコープ監査](e_reports/SCOPE_AUDIT.md)・個別DEFERREDを参照する。旧スナップショットはGit履歴に残す。
