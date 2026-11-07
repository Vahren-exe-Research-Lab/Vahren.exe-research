# C-20261015-1425-01 | T025/T016 | sc_free のボスイベント前置と戦闘後 World frame-install の別契約
Status: READY（原作ver0.67 SCRIPT × A保存Nativeの静的crosswalkのみ）／旧EXE実行・queue効果 NOT READY
Owner: Lane C。原作EXE/ZIP/シナリオ改変無し。他レーン/A保存資料はread-only。

## 原本・証拠位置
- 原本相対（normalized静的コピー）`a_default/script/7000_その他シナリオ/free_ev_world.dat:1-35,38-125`：World wev_free は castleset/randomset、battle flags reset に続き event(boss_dead)、event(tdnastk_dead)、event(kuroknn141919_dead) を記述し、これらは NewTurn/PlayerTurn/ComTurn の checkturn/checktiming 重複return より前。
- 本編 `a_default/script/event_world.dat:~54-95` にも同じ3件の前置き。
- A所有保存証拠 `data/T010_EVENT_SCHEDULER.md`「phase frameInstallMode=0 caller分類」「frameInstallMode vector transform」「normal strategic battle lifecycle」、`exe/T010_FRAME_HELPER_PROBE.txt` と `exe/T010_ARG2_ZERO_CALLERS.txt`（新規逆コンパイル無し）。
- A保存Native address: phase dispatcher 0x432EE0、frame helper 0x4365F0/0x436080、current-frame reader 0x4339B1以降。World arg2=0 caller 0x43550E/0x48D615/0x494E4D/0x496121、通常World arg2=1 caller 0x434DD2/0x47265D/0x4738B6/0x473B2F/0x51F8BE。

## 確認済みの新しい接続範囲
[CONFIRMED-SCRIPT] sc_free World bodyに到達する場合、3件のevent命令はsource上の重複return guard以前にあり、guardでreturnすることだけでは命令「発行箇所」到達を排除できない。これは既存C§71/74/77の再確認で、新しいスクリプト命令発見ではない。
[CONFIRMED-SAVED-NATIVE (A所有)] 同一World phaseでも通常entryはframeInstallMode=1で4vector {block,pc,executionMode,frameKind} の全末尾append、戦闘結果からのWorld再entry（0x494E4D/0x496121）は0でblock/mode末尾append・pc/kind先頭insertという非対称stack transformを持つ。interpreterのcurrent frame読取は4vector各末尾。
[NEW C CROSSWALK / CONDITIONAL] このため、旧EXEの合法な戦闘後sc_free World再入と通常sc_free World入口を「同一のWorld blockの単純な末尾push」として一本化すると、3つのpre-guard event発行を評価する際のframe contextを誤るリスクがある。旧Cのpre-guard三event / AのframeInstallMode0/1を初めて特定のsc_free入口ごとの受入条件として接続したもの。Aのnative確定成果自体や旧Cの三event位置を再度新発見として計数しない。

## 非確定・未観測
[VERIFY] frameInstallMode=0で開始する時の既存stack depth、単一event()が実際にqueueへ入る/Done判定、Yield/Resume、checkturn/checktimingによる再入、三eventのbody実行回数、合法な同turnの追加entryは未確認。nativeでmode0 stackに残る先行PCが別scriptへ接続されるとも、三eventが必ず再実行されるとも断定しない。
[BOUNDARY] frameInstallModeは World「phase」の入力であり、個々のevent() opcodeや難易度getMode()==0とは別物。frameMode0=easyと解釈しない。原作バグ確定0。

## strict再実装／Golden
[REIMPLEMENT] phase dispatch {phase=World,frameInstallMode raw0/1,executionMode=1,stack depth} と、script内3 event()の発行要求、history/Done、VM body開始、Yield/Resume、turn重複returnを別traceにする。mode0をmode1末尾pushへ置換/一律queue replay or skipしない。
[GOLDEN DESIGNED/NOT RUN] 合法sc_freeの通常World入口と通常戦闘（攻撃成功/防衛成功）直後のWorld再入を異なる入力scenarioとして各old/new同一SAVE SHA・操作列・可視capture SHAで照合。各回のboss/TDN/黒KN生存・撃破条件、背景演出再入の有無、@evtend三件（合法SAVEに現れた場合）、撃破message、Power/Unit/Spot変化、次turnを別々に確認。内部frame四vector/queueが原作UIや合法SAVEから不可視なら項目INELIGIBLE、旧EXE未観測はDESIGNED_NOT_RUN。旧原作Gameplay PASS0／新旧strict MATCH0。
[DEPENDENCY] A T010/T031/T006によるframe depthとevent opcodeの実continuation、E T018実機goldenが必要。CはA/E資料・MASTER・Workへ書込/直接受領確認を行わない。
[PRIORITY] T025 boss_dead setv/clear/erasePowerとWW po/poo・inactive/self union、sc_free queueは依然P0 VERIFY。T029 Castle5/sentinel、T026教育一時変数、T027 wallet/stock5、T033 legacy到達は未解決。
[CAPACITY] Local Compactのみの軽量保存証拠×原作normalized read-only照合。先行PID21336入力待ちには非介入、CPU n/aのため低負荷断定なし。原作EXE/Ghidra/Java/REA/重いtestの起動0。前回拒否済C-20261015-0824-01/T026/T032/E cp152操作はBLOCKEDのまま再試行/迂回無し。34Task DONE9/IN_PROGRESS21/VERIFY4、MASTER cp151正式536はE所有で不変更。本IDはMASTER未統合。
