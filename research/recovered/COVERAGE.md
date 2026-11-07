# 研究本文の収録範囲

RESEARCH_SOURCE_CATALOG.tsv の既存スナップショットを、Git管理対象のテキスト本文とレビュー済み回収台帳に照合した一覧。
[全行の照合結果](COVERAGE.tsv)から元の相対パス、SHA256、研究ID、保存先を追跡できる。

| 状態 | 行数 | 意味 |
|---|---:|---|
| EXACT_BODY_AVAILABLE | 458 | 同じSHA256の本文をリポジトリ内で確認 |
| RECOVERED_REVIEWED_VARIANT | 24 | 元SHAと保存版SHAを持つレビュー済み別版を確認 |
| PARTIAL_BODY_AVAILABLE | 0 | レビュー済みの抜粋を確認。本文全体の回収は未完了 |
| SOURCE_REVISION_DIFFERS | 3 | 同じ原本相対パスの別SHAに対応する回収記録を確認。目録版の本文や全文回収を証明しない |
| CATALOG_ONLY_UNRESOLVED | 1452 | 同じ本文やレビュー済み別版の対応を、この検査では確認できていない |

対象は目録の 1937 行。未解決行にも別名の要約・訂正・出典参照が存在し得る。SHAの文字列が資料中に登場しただけでは本文収録と数えない。
目録のSHAは採録時点の値。研究PCの現在の文書との一致、研究の確かさ、GitHubへの送信完了はこの表だけでは判定しない。
recovered_source_sha256 は対応する回収元のSHA。SOURCE_REVISION_DIFFERSの場合は目録のsha256を保持したまま別の版を示す。部分回収の範囲は回収台帳のcoverage_stateとlimitationsで確認する。
目録作成後に追加された研究や、目録に含まれないファイルの全件把握も別途必要になる。原作素材・保留原資料にはアクセスしない。

再生成は `python tools/recovery_coverage.py build`、鮮度確認は `python tools/recovery_coverage.py check`。
