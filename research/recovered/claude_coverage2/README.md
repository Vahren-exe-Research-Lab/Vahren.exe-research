> 後続訂正：この監査票はFの追加範囲訂正前の保存状態を固定したもの。現在のFは旧保存版3182行を追加除外し、保持原行は4,123。旧SHA・4,124保持という値は当時の入力を示す。[現在の範囲訂正](../findings/REVISION_20261105.json)とSCREENINGを併読する。全体手動レビュー未完了は継続。

# Claude関連成果の保存と事典への反映：限定監査

現在root台帳2428行のうち、source_pathが`dev_lab/`で始まる受理出典は167行／保存先166種類ある。**これはパス範囲の件数で、167件すべてがClaude著作、独立研究、完全回収という意味ではない。** 今回は保存済み資料と辞書metadata、5例の該当段落だけを確認した。原本・native・ログ・CLI会話の新規取得/実行、全出典追跡、repo共通/core/Git変更は0。

## 実際に確認した保存先と反映

- 主要解析F：`research/recovered/findings/PEER_SCRIPT01_FINDINGS_20261011.md`。本文冒頭にClaude所有と明示され、`reference/sources.json`のFとCが同じSHA256/節へ接続する。**C(§93)はこのClaude記録への引用であり、Cレーンの著作という推定ではない。** F§31のレベルアップ関数、F§58のPower資金、F§93の解雇ボタン印が現在の関数/メモリページへ明示接続している。
- EXP/実機記録：`research/recovered/outside_design1/reports/dev_lab/_work/summon_exp_20261103/EXP_DAT_DESIGN_20261103.md`。SHA256`072445be4234927625ba840b2da45349b2e8b4ffd05070f8ef3eb1d5499e2000`の完全保存版。現REF§10はClaude PEER_SCRIPT01と明記し、元報告LF83もClaude STATICと記す。一方、実機記録の一部はユーザーのプレイ/ログと明示される。通常召喚CALLsite0x54F245、名前検索0x49E780と評価器base訂正が現在の辞書意味に反映されている。STATUStsvに元行・保存SHA・現在ページと限界を示した。REFは二次curation、生成ページのVA言及はlookup補助であり、それだけを意味proofへ昇格していない。
- 関連RTTI：`research/recovered/dev_reports/PEER_SCRIPT01_RTTI_CLASSES_20261011.md`は25,738Bの完全保存、台帳の原本/保存SHA一致を現存bytesで確認した。ヘッダーは194type descriptors/180vftable classesを著者集計とし、virtual slot数はupper boundと明記する。元C++名/vftableのlookup資料として保存されているが、これだけで各methodの意味や完全class ABIが採録済みとはしない。単独ヘッダーにClaude名がないため、PEER_SCRIPT01-family関連資料であること以上の著者同一性も推定しない。

## Fは部分版である

Fは原本4,683行のうち4,124原行を保持し、559原行分を除外したscreened derivative。保留段落、個人パス段落、未確認付録の範囲はSCREENING.jsonにある。目録の旧SHA、後の原本SHA、保存部分版SHAは別物であり、古い目録版の全文回収でも全体の手動意味/privacy確認済みでもない。ここで確認したのは現保存SHA`6c61b104076363710e09535c6db62daedbe0f0ee159a6ce3240aceb4f417d2d8`と、5例の許可された段落/接続だけ。除外原文は開き直していない。

## 拡張製品コードとの境界

root READMEは研究知識/根拠を本repo、拡張製品コードを関連非公開`HakushinExtensions`で管理すると区別する。EXP報告内のDLL/plugin/commit/ログへの参照は、製品ソース一式、実行可能DLL、全ログ、全runtime証明をこのKBへ保存した証拠ではない。今回は外部repoや参照先を取得せず、runtime/PASS/READYは元報告の当時の観測として保持した。

## CLI履歴だけに残った成果の範囲

親の限定metadata調査では、既定CLI保存先の32JSONL(8,109,693B、parse error0)をdecoded Unicode+casefold markerで選別して9関連候補。markerを含むassistant textの先頭最大700文字を6件(短文全体4/長文prefix2)だけ確認した。見えたのはx32dbg状態・thread/register/CallStack/module-base・tool一覧などの診断断片で、**その範囲では独立した再利用可能な関数/メモリ研究reportや保存先を同定できていない。** 9候補の全assistant発言、非該当23session、他保存先や履歴全体は未review。研究履歴の不存在・全回収の証明ではない。CLI_SCOPE.jsonは親報告aggregateとして記録し、この監査が会話本文を再読したと装わない。session/user/tool/rawdump本文のGit保存は0。

現在ローカルrootの保存SHAと明示の反映例を確認した。台帳の過去GitHub readbackは当時の証拠であり、本監査でfresh GitHub readbackや公開切替を行ったものではない。INPUT_PINSが使用した保存資料を固定し、OUTPUT_MANIFESTがこのフォルダの他4ファイルを固定する。新しい研究の採録や確度変更はしていない。
