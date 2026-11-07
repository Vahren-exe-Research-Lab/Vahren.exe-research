# ON-STAND-010｜原作召喚親子リンクとDAT・DLLの役割分担
2026-10-25 JST｜CONFIRMED-SAVED-NATIVE（既存Ghidra V9、静的）／DAT親子の直接参照NOT FOUND／原作実機NOT RUN。
対象：迫真戦記ver0.67。既存原作、研究B/REA、EXE、SAVE、共有MASTERは読み取り専用。新たなEXE逆解析や実機起動はしていない。

## 利用者の指摘／新しい結論
ユーザーから「召喚の親子関係は既存の研究記録にあった。DLLを使わずDATだけでできないか」と再調査依頼。
**原作には既に親Unit→子Unitポインタvectorが存在**する。独自の召喚親子所有台帳をゼロから実装する必要はない（旧方針訂正）。
ただし、エンジン内部の子リストを、DAT関数がそのまま列挙・個別消滅できるかは別問題。公開関数一覧でその命令を発見できていない。
DLL必須と断定しない。特定のTNOK戦ならDATだけでの限定再現を試せるが、「他術者の同型子を絶対に消さない完全汎用版」はDAT証拠不足。

## 保存済みV9 Nativeによる具体的な確認
根拠：_REDEV_RESEARCH/rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite の functions.pseudoc と ghidra_refs。これらは元CソースでなくGhidra擬似C。
- VA 0x005774A0: parent Unit の +0x178（子vectorのbegin）、+0x17C（end）、+0x180（capacity）へ child Unit* をappend。child+0x1E594が非0ならこの追従先にparentポインタを代入。child専用のvector生成ではなく、parentが所有する子ポインタ一覧。
- VA 0x00577600: 親Unitの召喚可能数らしき +0x168 と child_count=(end-begin)/4 を比較する召喚スキル種別のgate。子vectorが召喚数の管理対象であるという独立した確認。
- VA 0x005445E0: 生存している子を parent+0x178..17C で走査し、子のelement_lostを判定して子Unitのvtable+0x58を呼ぶ死亡処理。
- VA 0x00575A60: 別の死亡/消滅経路でも同じ子vector、element_lost、子vtable+0x58を使用。
- VA 0x0054E7B0: 0x0054F245から0x005774A0へ直接CALL。生成中にparentの子vector末尾を読む分岐もあり。
- VA 0x0056F880: 新規生成Unitの子vector領域を0初期化する記述。
- 参照文字列element_lostは0x0062834C→0x575A60、0x0062A2EC→0x5445E0を使用。
- 注意：Unit+0x1D4は戦場陣営ownerであり召喚者ポインタと混同しない。+0x1C8 / +0x1D0にもlinked objectがあるが正確な意味は未確定。今回特定した親子vectorとは分離して扱う。
- 既存T011/T012契約（SUMMON_RUNTIME_UNIT_56F880、SUMMON_CORE_54E7B0）と整合。T011のEffectRecord+0x6C=self Unitとは全く別の参照である。

## DATに見える機能と足りない部分
- 召喚：skill func=summon の add/add2、技能連鎖next。術者が親として管理される。
- satellite：召喚体がリーダーまたは術者へ自動追従。element_lost=on：術者の死亡で召喚物消滅。**技能を戦闘中に盗まれた時とは別条件**。
- removeSkill：技能を戦闘中に剥奪。既に召喚された子が自動で消えるという仕様は未確認。
- storeAliveUnit(基底クラス／Unit名,文字変数)：同型を列挙するが元術者条件を受け取らない。
- storeMemberOfUnit：リーダーの部下を取得するが、内部の子Unit vectorと等価であるという資料はない。TNOKの召喚技にはyorozu=troopの明示指定もない。
- removeTroop(Unit)：指定Unit部隊を消す。子Unitを術者別・技能別に選んで消す専用命令ではない。
- 参照： https://w.atwiki.jp/vahren_ency/pages/379.html  （unit）
- 参照： https://w.atwiki.jp/vahren_ency/pages/405.html  （summon/yorozu）
- 参照： https://w.atwiki.jp/vahren_ency/pages/614.html  （storeAliveUnit/storeMemberOfUnit）
- 参照： https://w.atwiki.jp/vahren_ency/pages/944.html  （removeTroop）
- 参照： https://w.atwiki.jp/vahren_ency/pages/696.html  （removeSkill）

## 実装方法の比較
A: TNOK限定・DAT近似：TNOKの召喚技能sp_chikorita1/2/3を戦闘中に封印。同じ戦場に他のchiko/chiko2/chiko3術者も一般Unitも一切いないことを保障できるなら、storeAliveUnitでclassごとに集め、removeTroopで対象部隊を消す方式を試す。投げたmonsterballが飛んでいる間は後から再出現するため再チェックが必要。クラスに対する実際の列挙・削除対象は未実機検証。
B: 完全汎用・高精度：最小DLLや新戦闘adapterがparent+0x178..17Cの**原作既存**子一覧を参照して子個体だけ消す。独立した親子リストを同期管理することは原則不要。特定技能から生まれた子だけを選ぶ場合は追加のrootSkillID識別が必要。
C: 改造なし完全DAT汎用：現時点で実装を裏付ける親→子列挙／生存中の親から子だけ消滅の公開関数が見つからず未証明。絶対不可能という断定も禁止。
- 「親をわざと死亡させてelement_lostを発火」案は不適切。本人の死亡、EXP、勝敗、イベントなどが変わる。
- 子のvtable+0x58を外から無条件呼出することも危険。子部隊削除や参照解除を含む安全な既存消滅ルートは別途実機で確認。

## ON-STAND-009 TNOKの具体例との接続
原作DAT現物：unit tnok は learn=5,sp_chikorita1,15,sp_chikorita2,25,sp_chikorita3。
F20_summon.datの根技能はmonsterballを飛ばし、next=sp_chikorita*_ntからfunc=summon、add=chiko/chiko2/chiko3。chikoは後にchiko2/3へ進化し得る。
**親TNOKの既存vectorへ当該召喚Unitが登録される想定が強固**。ただしどのrootSkillがどの子を作ったかはvector単体では確定しない。他人の同型ポケモンは、TNOK親のvectorから消す設計で保護できる。
stand_proto/summon_ownership_ledger.pyの個体所有モデルは仕様テスト用。原作に親子リストがなかったことを示すものではなく、今後のproduction実装ではnative子vectorを正本にする。

## 次の確認
- [ ] 原作DATのみの隔離戦闘でstoreAliveUnit(chiko/chiko2/chiko3)→個別removeTroopの作用と、ほかの部隊への副作用を確認。
- [ ] 2人の術者が同じclassを召喚する時、class削除は巻き込むか確認（巻添えならDAT-only汎用版は不合格）。
- [ ] 親子vector内の子がレベル進化や飛翔中の召喚effectでどう変化するか、原作実機で検証。
- [ ] DLLを使う場合も独自親子管理は作らず、既存消滅ルートに安全接続する。元の子一覧の整合性と後戻り不能な死亡処理は慎重に扱う。
- [ ] 技能奪取→受領者で召喚→戦闘終了で技能復帰の原作実機試験。現時点ゲームGolden/実機PASSは0。
## 復旧記録 REC-ON010-EDIT-DEPENDENCY-20261025
2026-10-25 JST、Desktop Commander Local Compact の edit_block で追加資料を編集しようとした際に ERR_MODULE_NOT_FOUND（fastest-levenshtein が不足）が発生。種別 OTHER/TOOL_DEPENDENCY、セキュリティ拒否ではない。最初の訂正以外の資料更新は未反映だったことを確認。原作EXE・DAT、他レーンへの変更は0。正規の同一Local接続上で、更新対象のファイルと一意アンカーを個別検査したうえで、正確な文字列置換により未反映部分だけを復旧。証拠保存場所は本資料、HANDOFF、TASKS。今後の再開はDAT限定隔離試験と、必要時のみ原作子vectorを使う最小adapterの設計。
