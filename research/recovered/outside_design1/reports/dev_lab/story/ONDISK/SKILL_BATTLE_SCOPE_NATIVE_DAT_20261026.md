# ON-STAND-014｜戦闘中限定スキル操作と永続技能の違い（2026-10-26）

状態：公開仕様＋原作DAT ver0.67の静的照合 CONFIRMED。原作実機の戦闘終了／GUI表示はNOT VERIFIED。製品DAT・EXE、他レーンは変更しない。

## 結論
- addSkill/addSkill2は戦略画面でも使われる、所持技能リストへの追加。追加された技能は転職でも残ると原作仕様Wikiが説明。単体では永続的な変更となり得る。
- eraseSkillはユニットの所持技能リストから削除する命令で、removeSkillとは別物。
- removeSkillはWikiで「戦闘シーンで指定スキルを消去」と明記される。元技能の戦闘中の一時封印に向く。
- **戦闘中限定の新技能付与は、原作が多用する addSkill→eraseSkill を候補にする。** 戦闘用Unitには技能を残し、戦略に持ち越す技能リストからは消す狙い。原作実例は強いが、すべてのキャラ・UI・SAVEで復帰すると確認されたわけではない。
- よって「戦闘限定だから特に難しい」とは言えない。本当に難しいのは召喚物の安全消滅、HP共有、絶対射程R、情報パネル更新。

## 仕様Wiki出典
- https://w.atwiki.jp/vahren_ency/pages/696.html : addSkill、addSkill2、eraseSkill、removeSkill の区別。
- https://w.atwiki.jp/vahren_ency/pages/944.html : 戦闘シーンで addSkill/addSkill2/removeSkill を使用。
- https://w.atwiki.jp/vahren_ency/pages/379.html : 転職時にも宝箱・addSkill関数で追加した技能は残る。
- https://jbbs.shitaraba.net/bbs/read_archive.cgi/computer/42292/1517317218/-100 : 投稿922–923でremoveSkill/eraseSkillの取り違えによる技能残留バグの報告。あくまでコミュニティ事例。

## 迫真戦記の実使用（決定的）
a_default/script/Ai戦闘制御_軍楽隊なし版.dat 全3707行。静的トークン出現数（コメント行除外）：addSkill 617箇所、eraseSkill 617箇所、removeSkill 111箇所。**実行回数ではなくコード内出現数**。

- L307-309 story change_form_battle、fight=on。
- L533-536: 敵が遠いときの待機技能a_wait1000_999を addSkill→eraseSkillで一時追加。
- L540-570: CPUの s_inyume に removeSkill、派生 s_inyume_com0/1/2 のいずれかを addSkill→eraseSkillして入替。
- L572-591: s_toshino（歳納人形）も同様に入替。
- L1155-1161: ONDISKの sp_ondisk を removeSkillし、wait_ondisk/com_ondiskを addSkill×2→eraseSkill×2 とする。
- L545-549の原作コメント：リーダースキル由来の付与は入替不可となる場合がある。元リーダースキルの付与は残るため、任意技能を万能に奪えるとは断定しない。

## DISC技能移譲の実装候補（擬似例）
（1）元所有者の戦闘技能を封印:
    removeSkill(ondisk, on_stand_summon)

（2）受領者の戦闘技能へ一時追加:
    addSkill(receiver, on_stand_summon)
    eraseSkill(receiver, on_stand_summon)

（3）戦闘中、新術者に発現を指示:
    skillTroop(receiver, on_stand_summon)

※ receiverは実キャラ名か文字変数に置換する。これで実ゲームへの組込済みとは言えない。

- **必ず中盤発動を別に検証**：今回の原作証拠は story fight=on に登録された戦闘開始時のCPU技能差替え。ユーザーが求めるDISCの「戦闘が進行している途中で技能を奪い、付与する」時にも addSkill→eraseSkill が戦闘Unitの技能リスト・戦略Unitの恒久所持技能に同様に働くかは未確認。開始直後の静的成功だけで中盤の実戦成功としない。
### 重要な落とし穴
- **元から同じ技能を持つ受領者**に無条件の eraseSkill を行うと、その人の永続技能まで削る危険。付与前に恒久所持技能の有無と復帰方法を確認し、重複技能は別扱い。
- リーダースキル、職業由来の再計算、CPUの技能再追加は removeSkill で封印した技能が戻る要因になり得る。イベント順序/再付与源を確認する。
- removeSkillだけではすでに存在するスタンドが自動消滅しない。元の召喚体消去・再召喚待機キャンセルは別責任。
- 原作のaddSkill→eraseSkillは強い静的根拠だが、**戦闘終了、退却、セーブ/ロード後に恒久技能へ影響しないかは実機未検証**。

## 情報パネルの問題とのつながり
- 戦略側の所持技能リストと、戦闘中に使用可能なスキルリストは、少なくとも命令上区別して操作される。
- 既存RTTIには BattleStatusWnd、StatusWnd、TempStatusWnd があるが、情報パネルの更新・共有する描画関数までは未確定。
- したがってユーザーの推測「戦略画面でも使われる」は addSkill/eraseSkill については正しい。戦闘中の技能を奪ったとき情報パネルに即座に消えるかは別途実機で確認する。
- 戦略側のパネルは恒久所持技能のまま、戦闘用のパネルは使用可能な技能の増減を表示するのが希望仕様。戦闘中に表示が自動更新しない場合だけ描画更新を検討。

## 実機検証の最短コース
1. 原作の隔離コピーで、戦闘中のaddSkillのみを試して戦闘終了後に残るかチェック。
2. 同じ条件でaddSkill→eraseSkillを試し、戦闘中は使用可で戦略へ残らないかを確認。
3. removeSkillで元技能を戦闘中に削除した後、戦闘終了・次戦闘・保存/ロードで戻るか確認。
4. 受領者が元から同じ技能を持つケース、リーダースキル由来の技能、CPUによる再追加を個別確認。
5. 戦闘情報パネルを開いたまま技能アイコンが増減するか、再選択時のみ更新するか確認。

結論：戦闘限定の奪取・移譲はDATだけで狙える見込み。HP同期や最大射程等とは分離して実装し、未検証を成功と報告しない。