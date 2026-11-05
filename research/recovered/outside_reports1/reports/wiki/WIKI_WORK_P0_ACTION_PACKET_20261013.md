# Work／研究B向けP0 実装入力パケット（2026-10-13）
Status: SOURCE_READY / SYNTHETIC STAGE PASS / INTEGRATION PENDING / ORIGINAL GOLDEN 0 / STRICT MATCH 0

依頼正本: WRQ-20261013-B-SKILL。Workが戦闘製品実装、研究BがNative証拠、研究Cが合法出撃、研究EがGoldenを担当。本ファイルは独立Wiki調査者のread-only交差照合結果であり、Work受領や実装済みとの宣言ではない。

## A. Workがすでに実装した段階（重複着手しない）
- Work1041はm_healのHP→EXP/D8→flash入口に接続済。Work _work/resolved_battle_support_core_return_source_result.jsonは合成fixtureで0x54E31Cのcore returnまで到達し、blocked=True。親Unit/Task return、可視原作一致は未達。
- Work既存 test_native_unit_tick.py::SupportCoreFlashTests はflash0/-1の551CF2短絡分岐を持つ。これを新規実装しない。

## B. 原作に存在するflash=-4回復技能（現在の+6F0ボトルネックとは別のテスト経路）
- 原DAT Unit fmrim: 10_ユニット/26_クッキー☆原理主義党.dat:413。宣言上Level8/MP500/Magic750/Class c_fmrim。実ゲーム内の最終値は未観測。
- Random scene 5000_ランダムシナリオ/sc_rnd_sys.dat:331、event push_rndm_routineで addSkill2(fmrim,sp_fmrim_joker)。別の6000_スキルテスト/event_test.dat:77にも付与源あり。合法イベント発火は未確認。
- U_必殺_26_30_原理～イースター.dat:220 の sp_fmrim_heal:m_heal は flash=-4、attr=hp、str=magic*100、range1200、exp_per=off、実効cost80。派生heal2:250、heal3:263もflash=-4を継承。
- sp_fmrim_jokerからnext/next2/next3をたどる静的経路でheal/heal2を発見。heal3の同root到達は未確認。次Skillを発動すること・種類の異なるnative handlerが実帰還することは未証明。
- Work現行resume_selected_support_core_flashはコンパイル済みSkill+0x248<=0で0x551CF2へ進み、Skill+0x6F0読取・4DFBB0は未呼出。今回の局所試験は原DAT実効flash=-4を手動Skill+248へ束縛して3/3PASS、対象Unitは変更せず、親UnitのreturnはFalse。証拠 WIKI_WORK_FLASH_NEGATIVE3_SMOKE_20261013.json。
- 実用: Workはこのsource skillを別の正規入力として構築できるか検証する。m_healのflash5を-4へ改変した架空互換テストは厳禁。現行Work test helperはあくまで合成Unitであり、合法原作Battle開始・終了の証拠ではない。
- 次gate: 551CF2のHP post→551D40/551E4A→54E31C→57FA9E/Unit return。対象の既存HPバーtimerがnonzeroなら新規attach処理が省略され得るが、これもWork/Nativeの実Unit state検証必須。

## C. 現行m_healの危険な合成値を先に閉じる
- WIKI_WORK_MHEAL_FIELD_PROVENANCE_20261013.jsonにWork fixture SHA256と13項目の監査を保存。原DAT mp80→Skill+278、flash5→+248、attr hp→+A1C、add_per未指定→既Bのchance100は根拠あり。
- Work合成Skill+4C=3はraw m_healにspecial指定がない。合成Skill+74=0はraw rush指定がない。+6F0 source_count=2、+6F4 record producerは未確定。+268/+2A0/+2B4も別producer経路の結合が必要。
- B1740でspecial→Skill+4C、B-20261013-1920-02/B-20261013-1930-01でrush→Skill+74が保存STATIC。A/T005 generic getterの未指定/@/親を別々に確認し、元m_healの+4C=3/+74=0を無根拠に正本化しない。B新producerをMASTERの新READYとしてこちらで二重採番しない。
- +6F0禁止済みliteral抽出を別経路でやり直すことはしない。flash>0 m_healで未確定なeffect recordや4DFBB0の成功を偽装しない。

## D. 別のP0：複数属性add2をWorkが引き取る
- WIKI_HEAL_ADD2_20FIXTURES_20261013.jsonは原DAT20件/15件add_all on/すべて既知19属性。sp_ryuma_nt2はhp/all/attack/defense/magic/dext/speedの7属性、sp_move_nt2はmove/para/stone。
- Workの単一非空属性551653→551924 HP writerは実装済み。これを再実装しない。残るのは全件ベクタ5515C4→4ACE30→479B50、空ベクタ551DEB、順序・28byte要素所有権・MP/PRNG既消費と正常returnである。
## E. 受領/検証条件と記録先
1. Work担当は最新のWork HEADとWORK_REQUEST_QUEUEを必ず再確認し、1041やcore_return fixtureの既済段階を再度実装しない。
2. Bは既存B-MT-02/06とB-1856-02/B-1930等のREADYを重複採番せず、必要なSkill fieldコンパイラの最終値が本当に証明されているかだけ判定する。
3. C/Eはランダムシナリオpush_rndm_routine/Unit fmrimの合法出撃と画面でのSkill付与を確認できるまでoriginal Gameplay NOT RUN扱い。発動できない場合、合成分岐PASSを実戦互換へ昇格しない。
4. Work新たな変更は既存の製品所有者のみが実施。原DAT ZIP/EXE/SAVE、他lane資料、MASTER、Work専用共有キュー、Git、Remoteは本Wiki研究では変更しない。
5. 固定機械可読ファイル: WIKI_WORK_P0_ACTION_PACKET_20261013.json。補助: WIKI_WORK_FLASH_MINUS4_RETURN_ROUTE_20261013.json／WIKI_WORK_HEAL_FLASH_GATE_CANDIDATES_20261013.json／WIKI_WORK_MHEAL_FIELD_PROVENANCE_20261013.json／WIKI_WORK_FLASH_NEGATIVE3_SMOKE_20261013.json。
