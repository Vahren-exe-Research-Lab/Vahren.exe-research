# C-20261015-1722-01 | T025/T016 (T032はread-only参照) | randomsetの周期gate外の継続副作用
Status: READY（原作ver0.67 SCRIPTの制御構造・World入口crosswalkのみ）／旧EXE Gameplay・VM反復・API実効果VERIFY/NOT READY。
Owner: Lane C。原本EXE/ZIP/DAT/SAVE read-only。T032の既存安全拒否対象は再試行・転記しない。
## 一次資料・独立差分
- 原本相対: a_default/script/102_ランダムイベント/randomset.dat:3-17,145-186、event_world.dat:5-13、7000_その他シナリオ/free_ev_world.dat:3-11、5000_ランダムシナリオ/ev_rnd.dat:1-7。Local Compact read-only。
- [CONFIRMED-SCRIPT] randomsetのPlayerEndまたはNewTurn非master・非tutorial・randomevon=1・turn<=60の周期ifが閉じた後に、独立のif(randomev_sabo>=1)がある。4回周期のrandomevturn >=4には包含されない。
- [CONFIRMED-SCRIPT] randomev_sabo>=1ならadd(randomev_sabo,1)、結果>=4なら全PowerのUnitを取得しeraseSkill(@allu,ps_sabo)、eraseSkill(@allu,ps_koyo)を発行後、set(randomev_sabo,0)。初期1からは通常の逐次数値規則を仮定すると3回目の該当呼出でcleanup発行候補。実際の3ターン後と同義ではない。
- [CONFIRMED-SCRIPT] 同じ周期ifの外でstoreSkillOfUnit(@plau,@aaa)→if(has(@aaa,pes_happy))。weed1/weed2/weed3/no-weedの順で(aa,bb)=(97,-30)/(98,-20)/(99,-10)/(96,-60)を選択し、HPへper(cc,aa)→setStatus、HPrecへbbを加算し-500未満なら-500へsetStatusする命令を記述。終端で@aaaとaa/bb/ccをclear/reset。
- [NEW C CROSSWALK] main/free/rsc World冒頭は重複checkturn/checktiming returnより前にroutine(randomset)。このroutine本体が実行されるなら、PlayerTurnのみ・NewTurn master・randomevon=0・turn>60・tutorialで4回周期が無効でもsabo/happy後段は独立到達候補。World再入が合法なら呼出数が暦turnとずれる可能性。
- [DEDUP] C-20261015-1625-01の二周期/前段routine、T032既知のrandomev1/2のsabo=1 writer・randomev77のpes_happy付与自体は再計上しない。今回の新増分は二つの後段枝がrandomevon/turn/phase制限の外で、しかもpre-guard World routineにあることだけ。
## VERIFY・再実装・Golden
- [VERIFY/NOT OBSERVED] routine実行・Yield/再入・Done、numeric variableの寿命、eraseSkill全員実作用、per/status native clamp、合法なhappy所持・戦闘後phase・同turn多重作用・SAVEは未観測。原作バグ断定なし。
- [REIMPLEMENT] randomsetを単に4回ごとのイベントへ縮約せず、routine invocation、turn10特別event、4回周期、sabo expiry、pes_happy status、World duplicate guardとVM continuationを別stageに保持。ON/OFF/turn60のgateは4回周期部分だけに限定する（source表現）。
- [GOLDEN DESIGNED/NOT RUN] 合法sci1/sc_free/rsc、randomevon=0/1、turn59/60/61、PlayerTurn/End/NewTurn(master/nonmaster)、sabo=0/1/2/3、pes_happyなし/weed0/1/2/3、通常/背景/postbattle Worldを組合せ、同一原作SAVE SHA・操作列の旧新HP/HPrec/skill表示・イベント・次turnを比較。合法不能/内部不可視条件はINELIGIBLE。
- [STATUS] 旧原作Gameplay actual Golden PASS0、新旧strict MATCH0、Task DONE追加0。T025 boss/WW/queue、T029 Castle50000、T026教育temp、T027 wallet5P/stock5、T033旧IDはVERIFY継続。
- [SAFETY/OWNER] 既C-0824/C-1526 HANDOFF拒否・旧C/T026/T032・E過去cp152拒否は別BLOCKED維持。元payload再送・別shell/tool/path/Remote迂回なし。C所有の本evidenceとHANDOFF以外変更禁止。
- [INTEGRATION/CAPACITY] E MASTER checkpoint152はB1611/C1625を正式統合記載・累計目標538（E側完全検算は未代行）。本C-1722はE未統合。Local Compactのみ・既存blocked sessions非介入・CPU率n/a、重量旧EXE/REA/Java/Ghidra/tests新規起動0。原本・MASTER/T018・他lane・dev_lab/Work/Git/Remote/MCP/scheduleは不変更。
