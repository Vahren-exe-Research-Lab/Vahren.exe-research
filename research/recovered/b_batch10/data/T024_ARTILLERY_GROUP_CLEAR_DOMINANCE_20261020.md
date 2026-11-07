# B-20261020-0109-01｜T024 砲兵一時集団のbattle側clear支配とindexed槽との非対称
[OWNER/STATE] T024主。2026-10-20 01時台 JST。SOURCE STATIC CANDIDATE；本detail・T024所有索引・B HANDOFFの独立readbackと重複検査前はNOT READY。
[SOURCE] 迫真戦記0.67 COREの認可済み正規化コピー data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat（3707行、2026-10-04保存）。Local Compact read-only。今回新規EXE VA/xrefなし。
[GROUP FLOW] story change_form_battle L333 if(@bbb != @ && isWorld()==0 && isMaster(@maikyara)==1)内でL349 clear(@form_art)、L806 addv(@form_art,@enemy_army_idx)、L1979 countVar(@form_art)、L1981 storeIndexVar。source順はclear→addv→消費であり、同じeligible処理に限れば旧group値がそのまま砲兵index生成へ入るとは推論できない。
[GROUP CENSUS] 3707行全体のexact base @form_art（末尾英数字/underscoreなし）参照はL349/L806/L1979/L1981の4箇所。@form_cavはL18/347/786/1747/1749の5、@form_infはL19/348/792/1863/1865の5。commented lineは除外。
[CORPUS] normalized CORE a_default/script/*.datをLocal Compact content-search literal '@form_art'で検索し、COMPLETED 54hit（@form_art_idx等も含む）、該当ファイルは当該DAT1件。他ファイルの別名や動的参照・エンジン内部操作は除外不能。
[WORLD DIFFERENCE] story change_form L13 if(count(@enemy_army)>0)内の非indexed group clearはL18 @form_cav とL19 @form_infのみ。@form_artには同ブロックの明示clear無し。対してbattle eligible入口では三group全てL347/348/349でclear。新増分は砲兵単独groupのstage全出現と同一呼出し内のclear支配である。
[INDEXED CONTRAST] @form_generalart0..50へのclearはworld L177..227の条件付き処理だけ（既B-20261020-0009-01、E cp193）。battleはgroup @form_artをclearしてもindexed art0..50を同入口でclearしない。groupとindexedを同一配列として扱わない。
[CONDITIONAL JOIN] 世界側guard falseでindexed slotが残り、engineが自動resetせず、新eligible戦闘でL1985以降addvされればslot残存/追記の可能性はある。一方、単独group @form_artに関しては通常eligible入口L349でclearが先行する。両者のruntime lifetimeは未観測。
[ART-ONLY GATE] L1985砲兵indexed slot生成は後段L2093のfull/kanni分岐判定より前。先行B-20261019-2321-01によりart0はfull gate三群ORに含まれず、art-onlyがkanniとなっても索引生成命令自体は前段に存在する。生成=AI消費や実命中ではない。
[DEDUP] 既B-20261019-2213-01の29→30欠番、B-20261019-2321-01の二gateと砲兵除外、B-20261020-0009-01の204 indexed conditional clear/後衛51正表は新規計上しない。本IDは非indexed group四点censusとeligible内clear→append→consumeの局所stage接続に限定。
[VERIFY] VMのclear実作用、world/battleのscope・保存寿命・イベント呼出順、eligible gate実通過、戦闘開始前group値、indexed slot累積、候補leader合法数、原作可視AI差/bug認定は全て未確認。
[REIMPLEMENT] art-group(一時仕分け)とgeneralart[0..50](持続が未確定の編隊槽)を別状態で持つ。原作script順にgate・clear・append・indexed-read・indexed-append・full/kanni decisionをtrace可能にし、無条件global resetや旧値引継ぎを勝手に確定しない。
[GOLDEN] 合法旧戦闘で初回→連戦、world enemy_army=0/>0 (不可視ならUNKNOWN)、敵talent砲兵only/混成、eligible条件、実captured slot/stats・AI技能/移動・nexttickをEXE/DAT/SAVE/map/input/capture SHAとseed可否付きで比較。旧原作Gameplay PASS0/new-old strict MATCH0、DESIGNED_NOT_RUN。
[SAFETY] 禁止VA0x5710C0..0x571500や旧拒否 B-RC-20261019-2010-T024-INDEX-SAFETY-01 の拒否本文に非接触。原本EXE/ZIP/保存ゲーム・REA/Ghidra新解析/Remote/Git/push/Work/MASTER/T018/他lane/dev_lab/設定/automation変更なし。
[READY] B所有3点保存＋独立readback＋ID重複検査の成功後に限りB LIMITED SOURCE STATIC READY候補。E MASTER統合は別審査。実機観測無し・Task DONE+0。
