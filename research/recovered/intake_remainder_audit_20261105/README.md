# 残作業の全体監査と限定回収

[現在使える範囲と残作業](../../../REMAINING_WORK.md)を入口に、旧目録・ローカル別分岐・研究チャット・全状態のGitHub履歴・事典の出典接続を横断した。元の目的の完了は未証明であり、単一の回収率を全体進捗へ読み替えない。

監査の固定基準はdevelop525b37e。旧目録未照合441行は、373source SHA一致、3歴史的catalog SHAのみ、29pathのみ、31capture header、5関連scope leadに分けた。path一致や歴史的SHAをcurrent exact scope保証としない。31のうち2compact scalar本文を[追加回収](../remaining_capture_receipts7/README.md)し、5failure票もraw_reads buffer集合と確定して本文なしにした。元の監査票は凍結し、[後続対応](CURRENT_CATALOG_FOLLOWUP.tsv)を別表にした。

[3ローカル分岐](../remainder_branches_audit1/README.md)はmetadataで追跡し、18文書版を次の確認候補へ分けた。[GitHub全状態の一覧](../remainder_github_audit1/README.md)は6Issue/54PR、113commentの全metadata接続末尾まで確認。3つのowner PR更新とclosed PR5のtree metadata比較から15blob候補を特定。exactblobなしを未回収の新発見としない。[小さい群の10コメント](../github_comments_small1/README.md)は完全保存し、[現在のコメント状態](CURRENT_COMMENT_STATUS.tsv)に対応付けた。Issue側日時と本文版の厳密bindingは未検証という制約を残す。

[チャット監査](../remainder_chats_audit1/README.md)では、既存93候補のうち84は回答未選択と判明。古いA/C/D27回答の未確認は後続取得で22保存+5保留に解消されており、残作業へ重複計上しない。[固定22先行回答の限定回収](../chat_selected22/README.md)は12本文保存/10今回未返却。[新たに選択した14回答](../chat_additional14/README.md)は別snapshotで14本文保存。元responseを再現したと主張せず、対象外で新たに見えた1IDはmetadataだけ残した。2cursor・84候補・10未返却・Library原報告14件の未取得を別の範囲として維持する。14原報告と4回収集約、著者の回収成功claimと現在KBの本文取得は同一視しない。

今回の新規38出典は、チャット26、コメント10、scalar summary2。原文バイトまたは返却UnicodeのUTF8完全版を、元URI/ID・保存SHA・取得範囲・時刻制約付きで登録した。研究status/訂正guide/保存claimは一次native証明ではなく、リンク先のnative/Library/PR本文/code/log/DB/assetsを新規取得・実行していない。ユーザー/ツール/添付本文は保存せず、既存6whole-message保留を再復元していない。

[事典の明示リンク監査](../remainder_core_links_audit1/README.md)では220func/18fieldの明示source_linksが未解決。別の関係やVA言及に根拠が存在する可能性があり、無根拠とは断定しないが、次は文書数追加より根拠への接続を優先する。今回のsemantic辞書・型・関係・訂正・静的CALL・実装コードは不変（収録allowlistと生成物だけ更新）。原本の移動・削除・公開設定変更はまだ行わない。
