# C-20261014-1930-01 | T025/T016/T033 | sc_free 観戦初回 setup の未列挙勢力への resetLeague
[STATUS] READY（原作ver0.67 SOURCE の caller/初期 roster 比較のみ）。VERIFY/NOT READY＝旧EXE native resetLeague 副作用・対象Power生成/alias・合法観戦到達・VM queue/Done・実GamePlay。旧原作 Gameplay Golden PASS0、新旧 strict MATCH0。
[PRIMARY] normalized原作 a_default/script/7000_その他シナリオ/free_ev_world.dat:144-149,693-725 と同 free_sc.dat:29-34。原本ZIP・EXE・シナリオ変更なし。
[CONFIRMED SCRIPT] wev_free の turn1/NewTurn かつ yet(firstsetupfree1) の呼出候補は event(firstsetupfree1)→event(chara_create)→event(choice_otherunit) の順（既存T025§96で登録済、ここでは再READY計上しない）。
[CONFIRMED SCRIPT / INDEPENDENT DELTA] firstsetupfree1 の body は isScenario(sc_free) 部分と別に if(isWatching()){ set(watch,1); resetLeague(poo4,poo15); } を持ち、その後に add(polip,6) を記述する。watchのとき resetLeague を直接呼ぶ script site がある。
[CONFIRMED SCENARIO DECLARATION] free_sc.dat の scenario sc_free 初期 power 列挙には poo4 があるが、poo15 は無い。列挙は poo14 の次が poo16 で、poo15 の初期登録は確認できない。これは宣言 roster の差であり、runtime 非存在・resetLeague 失敗の証明ではない。
[DEDUP] 既存T025§9（初回 polip+6）, §66（firstsetupfree2 敵軍強化）, §96（二つの独立 yet と直接6 event）, §97（COM phase gate）と重複計上しない。本件の増分は「isWatching() 専用 resetLeague が未列挙 poo15 を第2引数に取る」caller×scenario roster mismatch のみ。既存C担当T025/HANDOFF/T033で poo15 の言及は事前 literal 探索0。
[VERIFY / UNOBSERVED] 観戦モードが初回 firstsetupfree1 へ到達するか、poo15 の native object が生成/非active/別名解決されるか、resetLeague の missing対象時の効果/例外、waitや event queue との interleave は未観測。元原作の確定バグ/不具合とは認定しない。
[REIMPLEMENT] strictでは初期 declared Power 集合と実 runtime Power object、観戦フラグ、firstsetupfree1 発行/完走、resetLeague(poo4,poo15) 呼出引数、watch writer、polip+6 を別 stage にする。poo15 を黙って poo14/poo16 に補正しない、例外や no-op を断定しない。
[GOLDEN DESIGNED/NOT RUN] 合法な旧 sc_free 新規開始を観戦と非観戦で比較し、turn1 初回/同turn再入/turn2、旧SAVE SHA・入力列、可視勢力 poo4/poo15 と外交同盟 UI/効果、polip / watch の観測可能範囲を新実装と同条件対照する。合法実例無し=DESIGNED_NOT_RUN、内部対象不明=INELIGIBLE、原作ゲーム未観測 PASS0。
[OTHER P0] T025 boss_dead setv/clear/erasePower、World War poo/po inactive/self union、sc_free native event queue、T029 Castle 5/sentinel、T026 tmp、T027 wallet/stock、T033 legacy loader は引続き VERIFY。本件は以前の外交 C-RC-20261014-1824-01 の拒否 write と別題材・別操作で、その元の拒否 payload を再提出したものではない。
[RUN CAPACITY] Desktop Commander Local Compact の既存原文・owner読取だけ。先行 PID21336 blocked 非操作、CPU 実率 n/a。新 EXE/Ghidra/Java/REA 重量 run 0、原本・MASTER/T018・他lane・dev_lab/rea_lab/Work・Git/push・Remote/MCP/automation 変更 0。
