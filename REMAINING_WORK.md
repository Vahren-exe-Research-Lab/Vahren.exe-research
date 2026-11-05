# 現在使える範囲と継続する研究

関数・メモリの意味を探し、人とAIが同じ辞書を使い、新しい発見を追加するための入口は整備済みです。出典リンクの網羅や、すべての過去チャット・進捗報告の複製は、通常利用の条件にしません。保存済みの根拠は残し、重要な訂正や矛盾があるときに必要な範囲を確認します。

事典には370関数、122フィールド、165手動関係を収録しています。訂正と本文の現在件数は[事典](reference/README.md)・[本文一覧](reference/DOCUMENTS.md)に表示します。通常の参照・検索に元PCのDBやゲームは不要です。[追加・訂正ガイド](CONTRIBUTING.md)が今後の書き込み入口です。

## 最終確認で整理したもの

| 確認対象 | 結果と記録 |
|---|---|
| ローカルの別分岐18文書版 | 独立報告・REF差分に未収録の新結果なし。既存の保存先・現行説明・旧案内・保留に分類。[判定票](research/recovered/practical_branch18/README.md) |
| ローカルの未追跡・除外Markdown5件 | 既保存2、既保存primaryの要約2、既知保留1。新規本文なし。[判定票](research/recovered/practical_untracked5/README.md) |
| 更新PRの15文書版 | 合成検証コード2本を保存。10件は既存資料への対応を記録。複合文書3件は本文未取得・保留/範囲未解決。[判定票](research/recovered/practical_pr15/README.md) |
| 残るコメント103件 | 独自の訂正・注意4件を保存、97件は既存報告や反復案内、2件は本文保留。[判定票](research/recovered/practical_comments103/README.md) |
| 関数名の混乱 | `0x4C2240` の旧乱数専用名を、保存済み局所解析に合わせた4B要素vector追加の説明へ訂正。旧caller文脈・推定の確度は維持。[訂正一覧](reference/CORRECTIONS.md) |
| 未選択チャット84候補の最新窓 | REA8・B12・E/統合等24・project文脈40を短い表示から選別。局所研究/訂正2発言とWorkパーサ研究1発言を保存。切詰め・古い未選択回答は残る（E1153本文は後続回収済み）。各[REA](research/recovered/chat_rea_remainder2/README.md)・[B](research/recovered/chat_b_remainder2/README.md)・[E/統合](research/recovered/chat_e_integration_remainder2/README.md)・[project文脈](research/recovered/chat_context_remainder2/README.md)を参照 |
| 関数・メモリの実用説明 | 保存済みEXP CP22–24から5項目を詳細化。ALを技能効果の成功と一律対応させない訂正、RetreatVoice更新とSimpleStaticUnit無効化の推定2関数を追加。版対応の不足する退却メッセージ候補は本文検索に留める |
| Claude関連の現在文書（旧照合時点） | dev_labの指定4フォルダ158文書は全文一致131、既存加工保存版25、既知部分版1、既知保留1。別版・独立未収録の新候補0。この範囲とClaude Code会話履歴全体を区別する。[現文書照合](research/recovered/claude_docs_current2/README.md)・[採録と不足](research/recovered/claude_coverage2/README.md) |

候補数は発見数ではありません。大きい旧索引は役割・差分の確認を含み、全リンク先の意味を再研究したものではありません。既存監査票は当時のスナップショットとして保持し、その「未確認」は上の後続判定と併せて読みます。

## 今後に残る範囲

- **研究そのものの不足。** 未確認の型・経路・実機動作は各項目に残しています。保存成功や合成テストを動作の確定へ読み替えません。
- **取得できていない履歴。** [旧チャット監査](research/recovered/remainder_chats_audit1/README.md)の84候補は上記で最新窓を選別しましたが、全回答の取得・意味確認ではありません。旧窓の未返却10回答は後続の表示確認で判定済み。後続確認済みcursor2の残る旧範囲・継続取得不能、Library添付コード・証拠等の未回収、追加窓の切詰め・未選択回答・選択API制約は残ります。すべてが未収録の独自研究とは未確認です。Claude Codeの既定ローカル記録も限定選別であり、他保存先・過去全履歴の回収は証明していません。
- **旧目録・保留資料。** 旧目録1,937行の対応は同SHA本文1395、レビュー済み別版93、部分1、版差9、未照合439。多くは保留・原データ集合で、一括取り込みの対象ではありません。[照合表](research/recovered/COVERAGE.md)から必要な対象だけ確認します。
- **任意の出典改善。** 明示リンク未接続の関数220・フィールド18は旧監査時点の値で、根拠不存在の意味ではありません。将来の制作で必要になった項目から補えばよく、全件接続を制作開始や今回の仕上げの条件にしません。
- **公開と原本整理。** リポジトリは非公開です。公開切替や非公開Git履歴の一括公開は未実施です。原本は依存・復元・保存対応を確認できた不要品だけを整理する方針で、未取得・保留・現役の資料は残します。現時点でゴミ箱へ移した原本はありません。

研究者のPR・チャットは更新され続けます。新しい発見は短い結論、対象の関数/メモリ、確度、未確認事項を残し、既存の入口につなぎます。過去全件の再監査から始める必要はありません。

Claude主要記録の後続範囲訂正では、既存保留の具体契約が残った旧保存版3182行を追加除外した。現在の保持原行は4,123。旧監査票の4,124・旧SHAはその入力時点の値であり、[現在の訂正票](research/recovered/findings/REVISION_20261105.json)を優先する。旧公開候補ZIPは非公開の旧版保存へ移し、公開候補としては扱わない。元の研究原本は変更していない。

## 後続回収（2026-11-05）

- [Library元報告14件](research/recovered/library_originals3/README.md)は全件取得し、既存集約の記録SHAと一致。3関数を名称推定で索引へ追加し、条件付き訂正を音声REFへ接続。
- [Claude現primaryの改版](research/recovered/claude_current_update3/INTEGRATION.md)を旧版と別保存。旧197行は完全一致prefix、新規12行のruntime14/15を確認。並行して届いたGitHubの2関数と実機報告を正本へつなぎ、節番号重複・dispatcher名を修正。
- [E1153訂正発言](research/recovered/e_witness3/README.md)を対象発言だけの表示テキストとして回収。添付原報告は読込失敗のため未取得。
- [旧チャットの後続確認](research/recovered/chat_cursor_followup3/README.md)：NewBの旧cursorはUnknown cursorで継続取得できず。旧Eのcursorは1ページ確認したが保存件数の進捗要約で新規独立本文はなく、次cursorが残る。Bの旧8候補は当時4件対応・部分2・保留1・未解決1。後続の3候補の判定は下記を優先する。全履歴回収の完了を意味しない。

## 既知候補の追加判定

- [Claude CLIの固定9セッション](research/recovered/claude_cli_followup4/README.md)：関連assistant text27項目のうち短文20項目を全文確認し、独自研究・研究保存先は見つからなかった。生診断集合7項目は役割上のメタデータ記録のみ。無関係23セッションや別端末・削除履歴まで確認した意味ではない。
- [旧Bの未解決3候補](research/recovered/chat_b_followup4/README.md)：同じ詳細研究文書の保存拒否と、その内容の言い直しであることを確認し、全体保留へ分類した。旧8候補の現在区分は可視結果対応4・同一詳細研究保留4。本文・代替要約・新辞書項目は追加していない。

今回の追加は既知候補の判定と取得範囲の明確化であり、研究本文や新発見の件数を増やすものではない。旧監査票は各時点の入力・未確認状態を残すため上書きしない。

- 旧未返却10発言は対象IDをブラウザで確認した。[E5件](research/recovered/e_unreturned5_review4/INTEGRATION.md)から未収録だった退却判定の型検査コード1本を原bytesで保存し、他4件は既存対応・保留資料の状態案内。[REA5件](research/recovered/rea_unreturned5_review4/README.md)は状況報告4件・既知保留の具体契約を含む発言1件。表示文をサービス原文bytesの完全複製とはしない。
- 既保存のsave局所報告から、stream異常の状態だけで全WriteFile経路を否定しない注意を1関数の説明へ反映し、見出し/byte writerに残る旧「外交」名をターン進行へ統一した。新たな実機検証・型の確定は行っていない。
