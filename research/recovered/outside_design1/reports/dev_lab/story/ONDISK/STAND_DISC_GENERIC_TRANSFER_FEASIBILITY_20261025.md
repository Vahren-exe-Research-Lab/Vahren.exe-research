# ON-STAND-008｜汎用・戦闘限定スキル奪取／譲渡と既存召喚技の非改変利用

作成: 2026-10-25 JST。状態: DESIGN / RESEARCH STATIC、ゲーム実機未検証。
所有範囲: story/ONDISKのみ。製品DAT、研究B・Ghidra・EXE・セーブ、他担当成果は変更しない。

## 今回のユーザー要求 [USER_FIXED]
- 技能を一覧表示して選ばせる仕組みは今は不要。敵が技能を奪取する。
- **奪われた能力はその戦闘に限って失われ、次の戦闘では元に戻る**こと。技能を奪うと、すでに召喚されている該当スタンドも消える。
- 付与技で別の人材へ技能を与えたら、その人材が**新しい召喚者としてスタンドを自動召喚する**。以後は新しい召喚者のHPとスタンドHPの完全同期、通常物理攻撃無効、専用standhit攻撃、術者中心の射程R規則が引き継がれる。
- **スタンド以外の召喚技（例：既存ポケモン召喚）も、原本の召喚技能DATへ追記・変更せず奪って別人に付与できる**ことが理想。元の通常召喚物にはその元の召喚ルールが適用され、スタンドのHP同期・物理無効を勝手に与えない。
- 「任意のスキル」に対して使えるか調査する。現時点で任意技能名の実行時引数を渡せるか・任意召喚物を術者別に特定できるかの実機証拠はない。

> **2026-10-26 見直し（ON-019）**：一般召喚（チコリータ等）は「同一トークンが複数体でもよい」。同種の一意性・厳密な召喚元追跡はP2品質課題に移し、汎用DISC導入の前提条件から外す。一方スタンドのHP/絶対射程/奪取時消滅/新術者へ自動再召喚/戦闘終了復帰はP0で厳密。正本は STAND_SPEC.md、原作の既存親子vectorの研究は SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md 参照。

> 【2026-10-26 ON-020 重要更新】チコリータ・スタンドは固有型で同名全消しを許容。一方、いんゆめくんやALC役クッキー☆声優の歳納人形は量産型で同名全消し禁止。量産型は取得者のスキル（COM用派生含む）を奪うが、既存召喚体を残す案を優先。未知召喚もデフォルトは封印のみ。最新表とテストは`SUMMON_DISC_REMOVAL_POLICY_20261026.md`。

> **ON-STAND-014（2026-10-26）更新**：戦略側addSkillは恒久リストに残り得る。一方removeSkillは戦闘中の削除用。原作CPU AIで addSkill→eraseSkill が実際に617箇所使用され、戦闘限定の付与が原作DATで行われている。新しいDISC受領者にもこのパターンを利用可能な見込み。ただし元から同スキルを持つ受領者のeraseSkill、リーダースキル由来、GUI再描画、戦闘終了/SAVE復帰は要試験。詳細：SKILL_BATTLE_SCOPE_NATIVE_DAT_20261026.md。

## 現物・公開仕様で確認済み
- `removeSkill(unit,skill)`: 戦闘中の指定技能削除。 [SOURCE WEB] https://w.atwiki.jp/vahren_ency/pages/696.html / https://w.atwiki.jp/vahren_ency/pages/944.html
- `addSkill(unit,skill)` / `addSkill2` / `eraseSkill`：技能リストの変更可能。迫真原作 `Ai戦闘制御_軍楽隊なし版.dat` 530-612、955以降は `removeSkill`→`addSkill`→`eraseSkill` の戦闘限定スキル差替えパターン。ただし他戦闘への影響はゲームSAVE/LOADの実機検査未実施。
- `storeSkillOfUnit(unit,@var)`で全スキル識別子リストを取得可能。利用者は当面これを用いて動的選択することを要求していない。 https://w.atwiki.jp/vahren_ency/pages/614.html
- `func=summon`＋`add`/ `add2`: 召喚先は**元のスキル定義**に格納。新召喚者へ同じスキル識別子を付与すれば、元の技能DATの変更なしで既存召喚処理を利用する設計が可能。実際の新召喚者のMP・召喚枠・所属・Lv・クールダウンは別判定。https://w.atwiki.jp/vahren_ency/pages/405.html
- `skillTroop(unit,skill)`: 別人から強制発動。https://w.atwiki.jp/vahren_ency/pages/944.html
- `removeTroop(unit)`: 指定した部隊を消すが、**Skill IDから『その術者がこの技能で召喚した全Unit』を逆探索する操作は公開DAT関数では未確認**。同一classを他の術者が召喚した場合、全消しの危険がある。
- `satellite`は新召喚者を追うことが期待できるが絶対射程禁止ではない。HP同期も原作DATだけでは実証されていない（ON-STAND-001/006/007を参照）。
- `element_lost=on`は術者の死亡時の召喚体消失に対応。**スキルを奪われた時の消失とは異なる**。https://w.atwiki.jp/vahren_ency/pages/379.html

## ON-STAND-009｜TNOK / チコリータの具体例：追加調査
- [ORIGINAL_CONFIRMED] `unit tnok`は`learn=5,sp_chikorita1,15,sp_chikorita2,25,sp_chikorita3`。F20_summonの根技能はそれぞれ`next=sp_chikoritaX_nt`、`next_last=on`で投射物を出し、後続技能が`add=chiko/chiko2/chiko3`を発生させる。
- [USER_FIXED] TNOKの能力を奪われたら、その技能からTNOKが召喚したチコリータ・進化系は消滅。他の術者が同種を召喚した場合は巻き込まない。飛行中のボールが後から召喚する問題にも対処。
- [PROTOTYPE PASS] `TNOK_CHIKORITA_RECALL_20261025.md`に根拠と所有関係を記録。Python `summon_ownership_ledger.py`と新規13テストで同型別術者保護・進化・飛翔体キャンセル・譲渡後召喚・戦闘後復元を検証。独立Python総61 PASS。原作ゲームへの接続は未済。

## ON-STAND-010：親子リンクは原作が保持していた（重要訂正）
Unit+0x178/17C/180 に原作の召喚子Unitベクタを確認。登録処理0x005774A0、召喚可能数検査0x00577600、術者死亡時のelement_lost処理0x005445E0/0x00575A60。親子管理を新規開発する必要はない。**ただしDATの親別・技能別子取得/生存中の親からの子だけ消滅の公開命令は未確認**。完全に汎用化するならこの既存vectorを利用した最小adapterを優先。詳細は SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md。

## 実現可能性：2段階
### 第一段階（DATのみの限定版）
対象の**技能IDが事前に判明している場合**、既存技能定義を変更せず、奪取イベントだけで`removeSkill(original,skillTag)`→`addSkill(recipient,skillTag)`→`skillTroop(recipient,skillTag)`とすることができる見込み。
- スキルIDがポケモンの召喚技でも、同じ`func=summon`の`add/add2`を参照する。
- 戦闘終了で元技能が戻るか、譲渡先へ残らないかは**実機未検証**。原作CPU使用例の`addSkill`→`eraseSkill`を候補とするが保証しない。
- 元召喚体の消失は、技能IDと召喚先classの対応が固定で、かつ他の術者の同じclassと混同しない**限定戦場**でのみDATのremoveTroopを使用可能と考える。技能本体は無編集だが、奪取側の対応表や条件は必要。
- 使用中の `afterhit` や複合`next`技能、ランダム`add2`、leader/status/unique固有技能、元Caster専用条件は個別の互換性確認が必要。

### 第二段階（完全に汎用化する場合の小型エンジン拡張）
- ルール正本を`TransferBattleSkill(originalUnitId, recipientUnitId, skillId)`とし、技能の所在を**戦闘インスタンスだけ**で変更。元の恒久習得情報を保存し変更しない。
- 召喚時に`SummonRecord{runtimeChildId,sourceOwnerId,rootSkillId,isStand}`を独立管理し、該当元術者が該当技能で出した召喚物だけを消す。原作既存ポケモンDATは改変しない。
- skillIdがスタンド型なら、受領者が発動すると`StandLink{ownerId=recipientId,childId,hpPool=recipient,currentRange}`を再作成。**旧術者のHPを新術者に転送しない**。新術者の現在HPを参照し、その後の有効ダメージ・回復は新術者HPと同期。
- skillIdが通常召喚（ポケモン）なら、新術者のレベル、MP、召喚上限、元の`skill{func=summon,add/add2}`をそのまま利用。スタンド限定の耐性やHP連動は適用しない。
- バトル終了/撤退/全滅/技能受領者死亡で借用記録を破棄。恒久Skillリストは変更せず元に戻す。必要に応じ継続戦闘内の再取得ギミックを別イベントに実装。
- 現状`Unit+0x1D0`の意味を「召喚者リンク」と断定しない。既存T013・召喚系B/REAの参照を重複照合したのち適切なruntime親IDを取得する。

## 汎用性の判定
| 能力 | 元技能DATの書換え | DAT単体の見込み | 完全汎用 |
|---|---|---|---|
| 既知の通常攻撃/魔法/回復スキルを戦闘だけ一時譲渡 | 不要 | 高い（実機未確認） | 動的skillTagの関数引数が要検証 |
| 既知のポケモン召喚スキルを新術者が発動 | 不要 | 高い（mp/slot依存） | 可能性高い、細部実機検証 |
| 元術者のポケモンを個体ごと安全に消す | 不要 | 識別可能な限定条件のみ | 召喚インスタンスの追跡が必要 |
| 別人へのスタンド召喚と新術者HP完全共有 | スタンドの元技能は改変しない設計可 | HPはDATのみでは未実証 | 小型runtimeが有力 |
| ランダムな未知skillと全召喚体の完全一括奪取 | スキル側は無改変を目指せる | 未確認 | 技能ID解決＋召喚グラフ＋識別・復帰が必要 |
| 攻撃ヒット相手の識別・任意ターゲットへの技能奪取 | スキル側は無改変で可 | 汎用hit-target受渡しは未確認 | hit hookなどの小型拡張候補 |

## 今回の阻害・検証状態
- REC-ON-STAND-008-LOCAL-SEARCH-SAFETY-20261025: Desktop Commander Local Compact経由で原作DAT全体から「技能変数を引数に渡す既存用例、ポケモン召喚技能」を横断検索するコマンドがOpenAI安全チェックによりブロック。結果ゼロ・試行継続なし・他ツール/方法で迂回なし。**動的@skill引数とポケモン技能IDのローカル実例は未検証**。この失敗は既存スクリプトやGitに影響していない。
- 先立つ同等目的の二つのPythonコマンドは正規表現構文エラー（OTHER）で走査を開始していない。これを成功証拠とみなさない。
- 公開Wikiの一般命令仕様と既存会話・原作の保存済研究で設計継続。ただし原作Vahren.exeでの汎用DISC転送・戦闘終了復帰については **GAME LIVE PASS 0**。
- `stand_proto/stand_disc_transfer_fixture.dat` は特定技能＆ONDISK・toonoの固定実験であり、今回の完全汎用設計を実装済みとは見なさない。前回の48/48 PASSは同fixtureの静的検査＋独立Pythonモデルであり、今回の汎用性の証明ではない。

## 安全な次工程
1. 元DATを触らず、まず隔離戦闘で技能一種を受け渡し、戦闘終了で恒久リスト変化なしを実測する（原作と比較）。
2. 召喚技能一種と通常技能一種で借用を行い、新術者から正規技能が発動するかを確かめる。
3. 旧召喚体が同型で複数存在する場合の非破壊・個体識別を検証。できなければDAT-only汎用破棄を禁止。
4. スタンドのみ厳密なHP共有・射程Rを加える。既存ポケモンの召喚Unitの仕様は変更しない。
5. `@skill`の任意ID受渡しとhit結果の目標判別については安全な原作観測または信頼できる公開資料で根拠を得てから一般化を主張する。