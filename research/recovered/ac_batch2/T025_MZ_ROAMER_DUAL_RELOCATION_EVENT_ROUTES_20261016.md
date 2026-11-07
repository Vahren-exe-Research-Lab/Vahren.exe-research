# T025/T016 MZ roam と同一World内の二群addUnitイベント（静的限定）
ID: C-20261016-0023-01 / 2026-10-16 JST / Lane C / READY=原作ver0.67 SCRIPT差分限定 / Gameplay NOT READY
[PRIMARY] normalized a_default/script/event_world.dat:491-526; 7000_その他シナリオ/free_ev_world.dat:318-356; 100_イベント汎用/event_00_共通イベント.dat:416-486。3ファイルとも原作ZIPのread-only正規化コピーを照合。
[SCENARIO CONTRAST] sci1とsc_freeはNewTurn/PlayerTurn/ComTurnの重複return判定より後段に同形の二群を記述。5000_ランダムシナリオ/ev_rnd.dat全1397行と3000_淫ドリームマッチ/ev_dream.dat全1062行には両群のmz_is_kusakunaiN/mz_is_kusasouN直接literal呼出0。間接呼出が無いとは認定しない。
[CONFIRMED SCRIPT GROUP A] if(inPower(@plap,mz)==0 && (getMode()>1 || kimotica_togo==1) && isPlayer(poo1)==0 && isPlayer(poo23)==0)の内側でevent(mz_is_kusakunai6,1,2,3,5,4)を原文順に6回発行要求。
[CONFIRMED SCRIPT GROUP B] 直後にN=1..6の独立したif(inPower(@plap,mz) && mzpoliN<0 || isRoamer(mz)==1)を置き、各々event(mz_is_kusasouN)を順番に発行要求。各predicateにはgetMode/yet/checkturnの専用latchを直接記述しない。
[CONFIRMED CHILD BODIES] event_00_共通イベント.dat:416-486の正の6 eventはzngm/hsgdn/hitokage/togepi/achamo/hassamuをaddUnit(child,mz)、負の6 eventは同じchildをaddUnit(child,sp0)する。Aの発行順は6/1/2/3/5/4、Bは1/2/3/4/5/6。各子の原文bodyでは単一addUnit命令を確認。
[CONDITIONAL] 式が標準的に(A&&B)||Cと評価され、isRoamer(mz)==1かつinPower(@plap,mz)==0でGroup Aの残りの条件が成立するとき、同一World entryに正6と負6の計12個のevent()命令へ到達し得る。これは命令到達仮説で、旧VMのparser結合/child schedulerを確定していない。
[A SAVED NATIVE CROSSCHECK] read-only exe/T006_TARGET_DISPATCH.md はevent/call=opcode0/AL1(parent Yield)、routine=opcode1/AL0(Continue)を確認済み。12個が1passで同期完走する証拠ではなく、先行イベント後のparent復帰PC、子のDone/queue/FIFOとaddUnit実効果はVERIFY。
[OTHER KNOWN / DEDUP] T025§54=C-20261011-2040-01のmz_is_butigire hsgdn比較1/2は別イベント。T025§62/63のsp0既存Unitと§51のpre-guard item欄、T025§106/107のNewTurn farm発行は再READY計上しない。増分は二群間の同対象6人の移送先競合候補・ローマーOR・シナリオ差に限定。
[REIMPLEMENT] World phase guard、二群predicate、6子event IDと原文呼出順、pending parent frame、addUnit target Power/Spot（mz対sp0）、child実行履歴を別trace。条件を見て6イベントを単一直接移送へ合体しない。旧動作未観測の最終所属や実バグを断定せず、必要ならMODEL_GAPとする。
[GOLDEN DESIGNED NOT RUN] 合法sci1/sc_freeでMZがplayer所属/非所属/roamerの各可視状態、mode1/2、kimotica_togo0/1、poo1/poo23 player0/1、各mzpoliN -1/0の到達可能な組合せを原作SAVE/同入力で比較。World entry前→各演出後→同turn再入→次turnの6child所属/spot、sp0可視/保存名簿、MZ持ち部隊数をold/new画面・SAVE SHAと共に採取。合法到達不能はINELIGIBLE。
[OPEN P0 / CLASSIFICATION] T025 boss_dead setv/clear/erasePower、World War poo/po inactive-self union、sc_free queue実FIFO/parent resumeは依然VERIFY。T029城壁sentinel、T026教育temp、T027財布stock5、T033 legacy loadも未解決。旧原作Gameplay actual PASS0、新旧strict MATCH0、Task DONE増0、原作BUG認定0。
[SAFETY] 原本ZIP/EXE、MASTER/T018/他レーン、REA/dev_lab、Git/push、Remote/MCP/スケジュールを変更しない。過去のT026/T032/C2026安全拒否を再提出・迂回しない。EだけがMASTER公式READYを採否する。
