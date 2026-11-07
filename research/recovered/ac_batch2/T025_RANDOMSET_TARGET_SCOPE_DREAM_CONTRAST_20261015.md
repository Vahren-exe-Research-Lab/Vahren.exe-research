# C-20261015-1823-01 | T025/T016 | World入口でのrandomset対象スコープとDream非直接呼出
Status: READY（原作ver0.67 SCRIPTのWorld入口・命令対象照合に限定）／旧EXE副作用・GameplayはVERIFY/NOT READY。Owner Lane C。
## 一次証拠／確定
- [ORIGINAL] a_default/script/event_world.dat:3-13、7000_その他シナリオ/free_ev_world.dat:2-11、5000_ランダムシナリオ/ev_rnd.dat:1-6、3000_淫ドリームマッチ/ev_dream.dat:1-1062、102_ランダムイベント/randomset.dat:153-186（全てver0.67正規化sourceをLocal Compactで直接read-only照合）。
- [CONFIRMED-SCRIPT] main/free/rscの3入口はいずれも先にstorePlayerUnit(@plau)し、main/freeはstorePowerOfUnit(@plau,@plap)とstoreNowPower(@now_power)、rscもstorePowerOfUnit(@plau,@plap)の後にroutine(castleset)→routine(randomset)へ進む。後段phase重複returnより前。
- [CONFIRMED-SCRIPT] randomset後段はsabo>=1の期限満了時にstoreAllPower(@allp)→storeUnitOfPower(@allp,@allu)→eraseSkill(@allu,ps_sabo/ps_koyo)で広域Unitを対象指定する。続くpes_happy節はstoreSkillOfUnit(@plau,@aaa)→has(pes_happy)→pushStatus/setStatus/addStatus(@plau,...)で、対象の文字列引数は同じWorldで取得したplayer Unitである。
- [CONFIRMED-SCRIPT/NEGATIVE LITERAL] Dreamのwev_dream全1062行にはroutine(randomset)・routine(castleset)の直接literal呼出がない（他の間接event/routine入口の不在とは別）。DreamでもstorePlayerUnit(@plau)文字列は存在するが、main/free/rscと同じ2 routineがWorld冒頭にあるわけではない。
## 独立増分・誤実装リスク
- [NEW CROSSWALK] 直前C-20261015-1722-01はrandomevon/turn/phaseの周期gate外処理を固定。本件の独立差分は (1) sabo解除候補のPower全体対象とpes_happyの@plau個別対象の非対称、(2) @plauが3 World入口のpre-routineで取得されること、(3) Dreamには同じdirect-call経路がないことを一枚のsource route契約に接続した点のみ。周期4、解除閾値4、weed数値は再計上しない。
- [VERIFY] storePlayerUnitの実結果・観戦/COM/戦闘後のplayer Unit選択、storeUnitOfPowerの全対象、eraseSkillとper/statusのNative副作用、Dreamからの間接実行、VM Yield/reentryと合法scenario状態は未観測。『全勢力の全Skillが必ず消える』『Dreamでは絶対に効果が起きない』とは断定しない。
- [REIMPLEMENT] randomevON設定・turn60・4周期とは独立に、World入口での@plau取得、global sabo解除処理、@plau個別happy処理を別stage化。Dreamにmain/free/rscのroutineを無条件挿入しない。全World共通のphase guardや全Unit HP更新に畳み込まない。
## Golden・引継ぎ
- [GOLDEN DESIGNED_NOT_RUN] sci1/sc_free/rsc各合法SAVEとDream合法SAVEを対照。ON/OFF、turn59/61、PlayerTurn/End/COM/NewTurn、通常/背景/postbattle再入、sabo=3、pes_happy所持playerと非player・ps_sabo所持player/COM Unitを区別。旧新同一EXE/新build/SAVE SHA/input/captureでUnitごとの技能・player HP/HPrec・次turnとイベント発火を記録。内部変数・合法不能状態はINELIGIBLE。
- [STATUS/DEDUP] 原作旧EXE Gameplay PASS0、strict MATCH0、Task DONE+0。MASTER cp153正式540(A115/B189/C127/D109)はE所有。本IDはE未統合、READYはSCRIPT route限定。
- [P0/RECOVERY] T025 boss_dead setv/clear/erasePower・WW po/poo/inactive/self union・sc_free queue、T029 Castle5/sentinel、T026 teacher/student temp、T027 wallet5P/stock5、T033 legacy到達性はVERIFY継続。旧C-0824/C-1526 HANDOFF拒否、C/T026/T032、E cp152拒否は別BLOCKED・元拒否の再提出・迂回なし。
- [BOUNDARY] Local Compactだけで軽量read-only照合。原本EXE/ZIP/script、MASTER/T018、他lane/REA/dev_lab/Work/WRQ、Git/push/Remote/MCP/scheduleは変更しない。
