# B-20261013-0718-01｜戦闘行動後 0x577600 の技能選択・可用性判定
Owner: B / T013（行動後選択）、T012（Skill/latch参照） / 2026-10-13 JST。
Status: READY-STATIC-BOUNDED（B HANDOFF同IDへの登録と読戻し成功。局所nativeのみ確定、gameplay VERIFY）。原作実機Gameplay PASS0、新strict MATCH0、Task DONE+0。
## 証拠
隔離された原本対応 Vahren.exe をread-onlyで固定窓VA0x577600..577A12（最終RET8は577A10開始）だけCapstone 32bit静的復号。元SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。
局所1043bytes SHA256=ce32076d927618972832b76fcac923e0c451c3f12b7b69c6a69531cee15fce44。B exe/T013_POST_ACTION_SKILL_577600_20261013.txtにVA/文字列/分岐・callerアンカーを保存。
呼出元：既存B exe/T013_SEARCH_CORE.txt VA57E610..57E635。pushの順は [Unit+1863C]値→Unit、call577600、次に571A40。577600の返ALは親側で分岐に使用されず571A40で上書きされる。
## 確定した局所順序
(1) 577607..577623：Unit+8C!=0又はUnit+1F8==0では577706のAL0出口へ。Skill種別+40==8かつSkill+110文字列=specialの場合、Unit+139==0でAL0、非0で576450後+1863C=0xAAFBB8/+18638=Skill、AL1/RET8（577683）。
(2) 通常枝はSkill+40が7/8かを区別。その他種別では577697 call44D070の結果をUnit+18660と比較し、5776B2等号ならAL0。Skill+4C>0の場合、5799D0(ECX=&Unit+1E4C4, stack=&Skill引数slot)のsigned返値が+4C以上ならAL0。種別4はUnit+138と (Unit+17C-Unit+178)>>2 対Unit+168の追加制限。
(3) 種別8でSkill+120!=0の場合、Skill+110の属性文字列sword/bow/magic/heal/care/powerup/summonについてUnit+134..138の対応許可flagを順序比較し、通過時のみ577800以降へ進む。+120==0では一連の文字列flag制限と後段の属性変換をskipする枝がある。
(4) 577800..57781Dで576450を呼ぶ。type8かつ+120!=0ならB052FC/B05300=(8,0)を初期化し、最初に成立する属性/flag順序に応じ(1,0),(2,0),(2,1),(3,0),(3,1),(3,2),(4,0)を選び、5779AC call579BA0。後段calleeの真の効果はUNKNOWN。
(5) Unit+18654==0なら5779BA..5779D9で576450を再度呼びAL0/RET8。非0ならSkill+4C>0の場合のみUnit+1E530へglobal65BC5Cを保存。旧[Unit+18638]のSkill+4C>0なら+1863Cへsentinel 0xAAFBB8、そうでなければ旧Skill*を保存。+18638へ今回渡されたSkill*を格納してAL1/RET8（577A10）。
## 既知との差分・再実装への影響
既存B-20261012-2356-01/02は5799D0と576450のcallee仕様。今回新規はその呼出元577600全体の入口→複数AL0/AL1出口・属性文字列gate・skill pointer更新・callerの返値非消費を閉じた点だけ。旧IDの内部作用を再採番しない。
577600のAL0を親57E4E0のAL0に転写してはいけない。親はこのcallの後571A40/条件付56BA80を実行し、VA57E62FでAL1を返す。+1863C保存旧pointerとsentinelを潰さず、+1E530・global B052FC/B05300をtraceに保持。
## 未確定・Golden
44D070の計算、579BA0全副作用、属性flagのruntime初期化、Skill+120の正確な役割、576450内に潜在するMP/RNG、Skillの合法組合せ、最終攻撃/HP/EXPはVERIFY。直接CRT rand call不在は下位関数のRNG0を示さない。
Golden DESIGNED/NOT RUN：可視合法Skillで種別7/8・属性7名・特殊special・flag0/1・+120=0/>0・+18654 null/non-null・旧Skill+4C=0/>0を分け、同seedでSkill一覧/次の行動/HP/MP/EXP/投射/表示/RNGを旧/new比較。内部pointerのみはINELIGIBLE。
NEXT：577600の実caller入力Skillと576450後のUnit+18654有効状態を、既存B証拠から絞る。対人戦で合法UI観測できるまで原作Gameplay PASS0。MASTER/T018への統合はEのみ。
