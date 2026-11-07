# 現在使える範囲と残作業

2026-11-05の[全体監査](research/recovered/intake_remainder_audit_20261105/README.md)。**全体完了・公開準備完了ではありません。** 件数は別々の対象を数えており、重複し得るため合計や全体の進捗率には使いません。今も研究者のPR/チャットが更新されるため、取得時点と未確認範囲を残します。

現在の事典は363関数、122フィールド、165手動関係、15訂正を収録し、[関数・メモリ](reference/README.md)・[本文](reference/DOCUMENTS.md)を検索して使えます。確度・未確認事項・保存版SHAは各根拠に従います。原作や元PCのDBは通常の知識参照に必要ありません。

## 次に優先する作業

| 優先 | 残る範囲 | 次の確認・終える条件 |
|---|---|---|
| 1 | 関数220・フィールド18に明示出典リンクなし | 保存済み一次報告の意味と該当行を比較し接続する。別の関係・VA言及だけを意味の証明にしない。取得できない根拠は不足として明示。[監査票](research/recovered/remainder_core_links_audit1/README.md) |
| 2 | ローカル3分岐の18文書版、更新PR等の15blob候補 | 旧版/重複/訂正/保留を本文範囲を限定して判定する。候補数は新発見数ではない。[ローカル](research/recovered/remainder_branches_audit1/README.md)・[GitHub](research/recovered/remainder_github_audit1/README.md) |
| 3 | コメント103件の内容未確認 | 113metadataのうち10本文を保存済み。残りをscope確認・重複/訂正照合する。本文の日時bindingにも制約がある。[現在表](research/recovered/intake_remainder_audit_20261105/CURRENT_COMMENT_STATUS.tsv) |
| 4 | チャットの未返却10回答、未追跡cursor2、未選択84候補 | 84は研究/監査題名44とproject文脈40で、全てが未回収研究とは限らない。まず研究成果に関係するものを選別する。取得窓の限界を全履歴回収と誤認しない。[監査](research/recovered/remainder_chats_audit1/README.md) |
| 5 | Library原報告14件の本文未取得 | 保存済み4回収集約と区別し、取得できた正確な原文/範囲を確認する。opaqueURIや別wrapperから禁止内容を復元しない |
| 6 | 旧目録439行が本文未照合、別に部分1/版差9 | 多くは理由付き保留/原データ集合。全439を取り込む作業ではない。pathのみ29/歴史的SHAのみ3/関連scope5は適用版を確認する。[目録監査](research/recovered/remainder_catalog_audit1/README.md)・[後続対応](research/recovered/intake_remainder_audit_20261105/CURRENT_CATALOG_FOLLOWUP.tsv) |
| 7 | 公開前確認と原本整理 | 現在treeと非公開Git履歴の公開範囲、引用/内部リンク/元PC不要の復元を確認する。依存・復元・全対象の保存対応が揃ってから不要原本をゴミ箱へ。現在は非公開・原本保持 |

明示source_linksがないことは、その項目に根拠が存在しないとの断定ではありません。初期の略記、実装ファイル名、曖昧なセッション参照、未解決の節番号などが混在します。主要な関数・メモリの意味から根拠へ辿れるよう補うことを、次の中心作業にします。

## 今回までの扱い

旧目録は1,937行で、1395件に同SHA本文、93件にレビュー済み別版が対応し、部分1・版差9・未照合439。これは旧目録内の保存状態だけです。目録外の収録・チャット・PR履歴・根拠接続の完了を証明しません。監査の固定441行は凍結し、後から回収した2summaryを別の後続表で示しています。

新しい研究は[追加・訂正ガイド](CONTRIBUTING.md)に沿って保存・採録します。保存数/合成PASS/著者statusを実機確認・Golden・READYへ昇格せず、既存保留は守ります。完了までの時間は、出典接続と未確認履歴の量・内容が確定してから見積もります。
