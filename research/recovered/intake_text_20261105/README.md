# TXT・CSV・JSONLの役割確認とメモリの採録

403候補から118出典を受け入れ、[TXT役割確認1](../text_roles1/README.md)・[TXT役割確認2](../text_roles2/README.md)・[所在目録と行形式記録](../other_records1/README.md)を共通検索へ接続した。70出典は元バイト完全一致、40出典はUTF16LE BOMからUTF8への損失のない完全版、8出典は個人パスのみ伏せた完全版。元SHA・保存先SHA・編集区間/不変区間・元形式への再符号化一致を親でも照合した。ファイル保存の件数を新規の関数発見や実機成功の数にしない。

285候補は、短いheader/schema・必要な形式統計により、未解釈の単独native命令/擬似C/window集合、元MIDIの全event輸出、具体的な既存保留の内容、または帰属未解決のjump-site表と判断し、全文・抜粋・代替再構成を保存せず[識別・確認範囲・理由](DEFERRED_AT_INTAKE.tsv)を残した。全文意味レビューや個人情報不在確認を行ったとの主張ではない。新しい取得拒否とは扱わない。既存の2件はexact path/SHAの保留を照合して再読していない。

受理資料は語句・RTTI・xref・定数・推定callbackの索引、短い著者の解析、資産の所在/件数/hash目録、継承の選別事例、選別された状態/counter/eventの行形式記録。元ゲームの音声・アーカイブ・設定ファイル自体やリンク先のraw captureを取得したものではない。受理本文は全文または全行形式ノードと異なる記述/値域を確認し、個別票に方法を分けた。空欄・既存mojibake・誤decode・None・callback_guess・歴史的な留保や訂正を勝手に修復/確定していない。静的・推定・合成検査・実機の区分を維持する。

[メモリ採録](MEMORY_BINDINGS.tsv)では既存の2関数と2つのnode+0x28を結んだ。[保存木ノード](../../../reference/structs/SaveUnitDataTreeNode.md)はUnitDataポインタを格納し、[召喚記録cacheノード](../../../reference/structs/SummonRecordCacheNode.md)は埋め込み記録の先頭を置く。前者は0x460000のread、後者は0x577260が返すアドレスとして元の著者報告に結ぶ。共通オフセットから型同一性・同じ間接参照段数を推定しない。cacheの宣言型はunknown、468Bは別証拠票の限定構造導出にとどめる。完全ABI・全save経路・EXP事前転送の有無・実行時到達性は未確認。

新しい関数/型alias・実機試験・Golden/READYは増やしていない。原本は変更・削除せず、ゲーム/native/DB/リンク先を実行・追加取得していない。公開設定は非公開のまま。未回収の他形式やチャット・PR履歴まで完了したとは扱わない。
