# REA owner 2026-10-19 historical source recovery (B)

Private owner intake only; no formal CURATED/READY. 7 old research and independent QA IDs, byte SHA256 of each original owner Markdown remeasured read-only on research PC 2026-11-02 JST. Substantive excerpts of saved ASM/ABI/branch logic are below, with older unsafe/denied evidence and path-specific private metadata omitted. Current original EXE/V9 and formal five-method evidence were not newly acquired; legacy Wave1–5 64/64 never counted again; original Golden PASS0, READY0. Owner source itself is PC-only and can be recovered via relative filename/SHA.

### REA-20261019-1739-T014-T031-SAVE-RNG-VECTOR-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_1739_T014_T031_SAVE_RNG_REFERENCE_VECTORS_QC.md`; actual SHA256 `11019054506A169A32B796EA5FFF5A24E7D66C8DB42CA5191F9FD22962A61781`, 4214 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [OWNER] 独立REA。T014(P1: 0x427040) / T031(P1: 0x5B6EAB)、戦闘側0x40ED80との関係は条件付きVERIFY。2026-10-19 17:39 JST。旧原本ゲームは実行していない。
  - [G1] VA0x5B6EAB、run 20261009T194358486Z、assembly ev_b1254a8fd74b2e65bc7d0dd87874866862fe9db02fd920de0dc7d93b35348924：PTD+0x14に state=(214013*state+2531011) mod 2^32、rand15=(state>>16)&0x7fff。
  - [G2] VA0x427040、run 20261011T113414092Z、assembly ev_21d9cad3ff2b047a9f34ec1a4be3a8053e3bdb9ad5acc35c0d93e42dc035b9d4、pseudo ev_cc5bde730579a34289233a8406ed8b02996d9ffebd7ec12b375398fd353359f3。5種結果VERIFIEDは保存済RUN_RESULT.jsonで照合、今回の新規Ghidra取得0。
  - [ALGORITHM] 0x427057..4270A0でCRT randを28回消費、x87 CWのRC=11(0方向)でkey[i]=8+floor(rand15*112/32768)。生成範囲8..119。0x42704Fは4-byte magic 01 02 03 04。0x4270A8で入力byte長が32以下ならpayload loopは無いが28回消費は済み。
  - [DERIVED] 28回合成は state28=(0x405BAF31*seed+0x08C0D79C) mod 2^32。32bit環の逐次合成計算から導出した計算上の主張で、旧EXE実行テストではない。
  - [VECTOR seed=0] 28回後state=0x08C0D79C、keyHex=08225010263024762b701c680b084e3e2661123a4f755260470c6a0f、zero-payload8の暗号化offset32..39=263024762b701c68。
  - [VECTOR seed=1] 28回後state=0x491C86CD、keyHex=08471d62493d2f6c645b1b6857412a091230181a7639150808324347、zero-payload8の暗号化offset32..39=493d2f6c645b1b68。
  - [VECTOR seed=12345] 28回後state=0x8E040985、keyHex=214960531b57651a6b573b3a4d522838532a61152a242e3c112b5114、zero-payload8の暗号化offset32..39=1b57651a6b573b3a。
  - [THREAD LIMIT] 0x5B6EABが__getptdを使用するため、saveとbattleが同一スレッド・再seedなしで呼ぶ場合に限りsave28消費は後続のbattle乱数列をずらす。他スレッド、srand、実frame順はVERIFY。
  - [NEXT] 初回死亡処理T010/T012/T013の0x575F91正常帰還とtroop選択更新の許可済み既存証拠を優先。T014のセーブ後乱数影響は同一スレッド/再seed順の旧実機合法観測を待つ。本fixtureと先行オフライン未同期資料はE/所有レーンが重複審査するまで独立REAの追加試験候補に留める。
- **Unresolved/corrections:** - [ABSOLUTE INDEX] VA4270B0..4270DDは絶対ファイルoffset p>=32に対し、out[p]=(in[p]+key[p%28])&255。例：p=32はkey[4]でありkey[0]ではない。既存T003のabsolute-index訂正と整合。out[4..31]は28鍵byte。 / - [THREAD LIMIT] 0x5B6EABが__getptdを使用するため、saveとbattleが同一スレッド・再seedなしで呼ぶ場合に限りsave28消費は後続のbattle乱数列をずらす。他スレッド、srand、実frame順はVERIFY。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-1835-TROOP-SELECTION-OWNER-REBIND-GATE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_1835_TROOP_SELECTION_OWNER_REBIND_GATE_QC.md`; actual SHA256 `AF482A210CB30EC4598FB5275635292E8974E3E094EDE04C8D50A26178B9DCC1`, 4861 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [NATIVE GATE 1] 0x575F6C CALL0x5684B0→0x575F71帰還後、Unit+0x1867Dを再読。非0時、engine+0x1E8B34のselectionOwnerをその時点で取得して+0x358の別Troopへ0x575F8C CALL0x5684B0→0x575F91。2回のownerが常に同じと示す証拠は今回なし。
  - [NATIVE GATE 2] 0x56852D(selected empty)および0x5685F8(normal empty controlled)は0x527ED0を呼ぶ。calleeは選択ownerのlinked-node/display/UI状態を変更し得るが、owner pointerそのものが更新される合法pathは未確認。
  - [CURRENT REQUIREMENT] native_battle_outcome.py TroopSelectionCleanup.advanceは binding.owner.pointer==parent.object_ref を要求。後続0x5684B0が異なるselectionOwnerをparent.object_refに採用した場合、既存binding複製からはこの照合を満たせずSessionGap/ValueError相当で止まる。
  - [INDEPENDENT CASES / NOT RUN] A: first selectionが同一ownerで再入する。B: 1st 0x527ED0完了後にengine+1E8B34が別ownerを指す（2nd selectedTroopも別）。C: 異なる2nd ownerに対し前回ownerのnodes/objectsを誤用しない。各例でfirst/second owner ptr、Troop ptr、0x575F71/0x575F91、binding generation、deleted nodes、callee/UI completedを個別trace。旧EXE合法到達が観測されるまではcase B/CはDESIGNED_NOT_RUN。
  - [RETURN/COMPAT] graphの二つのcallsiteは独立で、2nd 0x575F91の正常RET前に0x575F95へ昇格させない。semantic redraw通知は原作GDI/vertexの厳密帰還証拠でない。既存0x575F91の未露出差分と重複READY計上しない。
  - [EVIDENCE] 今回新規Ghidra info/pseudo/assembly/callers/callees Evidence IDはいずれも0、新たな静的VERIFIED関数0。再利用契約ID=REA-ND-20261013-001、SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md。source SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（保存run、今回現物再hashなし）。
- **Unresolved/corrections:** - [INDEPENDENT CASES / NOT RUN] A: first selectionが同一ownerで再入する。B: 1st 0x527ED0完了後にengine+1E8B34が別ownerを指す（2nd selectedTroopも別）。C: 異なる2nd ownerに対し前回ownerのnodes/objectsを誤用しない。各例でfirst/second owner ptr、Troop ptr、0x575F71/0x575F91、binding generation、deleted nodes、callee/UI completedを個別trace。旧EXE合法到達が観測されるまではcase B/CはDESIGNED_NOT_RUN。 / - [MASTER/GOLDEN] 今回読取MASTER最終checkpoint190、研究DONE9/34・IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-1933-TROOP-OWNER-DIRECT-WRITE-SCOPE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_1933_TROOP_OWNER_DIRECT_WRITE_SCOPE_QC.md`; actual SHA256 `DEE88237732792EAA8E8F41C317453AED046A1C80F10B13D5AA2C88FFDCB75D1`, 4777 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [SOURCE] REA保存契約REA-ND-20261013-001、`SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md` §ND-GRAPH-TAIL/§ND-TROOP/§REA-WRQ-20261013-DEATH-11,12,18、`REA_20261019_1835_TROOP_SELECTION_OWNER_REBIND_GATE_QC.md`。target saved SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回EXE再hashなし）。
  - [NATIVE LOCAL WRITES] 保存済み0x527ED0..0x527F55の局所ABIでは、T+1D==0なら0x527EE6→0x4EC680でowner+348選択listから対象Tに一致する全nodeを解除。owner+34C==0かつowner+368/-364の空条件成立なら0x527F0Eでowner+45D=0、owner+20C非0なら0x527F1Eでowner+20C=0→0x527F22で4C5C40（display first match）。この保存済み局所命令列にengine+1E8B34の直接storeは確認されない。
  - [NATIVE INDIRECT BOUNDARY] ただし0x527F27 CALL41F850→0x527F2E CALL56BA80→0x527F43 global660F78.virtual+C→条件付き0x527F4E CALL401BE0の先でselection関連global/別ownerに副作用がある可能性は排除できない。特に既存DEATH-18では56BA80がselection-related global65EC14等を参照すると記録。これらcalleeを純粋な表示no-opと判定しない。
  - [PARENT READ WINDOWS] 第1Troop call：0x575F6C→0x5684B0→0x575F71。そこでUnit+1867Dを再読し非0ならUnit world/engineからselectionOwnerを新しく取得し+358の別Troopに0x575F8C→0x5684B0→0x575F91。`0x527ED0`内のownerローカル変更と上位エンジンowner pointerの変更を区別する。
  - [OBSERVATION DESIGN NOT RUN] ①選択解除前のengine+1E8B34/owner identity、②4EC680/4C5C40帰還時、③41F850/56BA80/global virtual/401BE0の各正常帰還、④0x527F55→0x568532または0x5685FD、⑤0x575F71でのengine+1E8B34再読、⑥二番目のowner/Troop/0x575F91を別receiptで追う。各callee未帰還ならVERIFYのまま。合法な旧EXE UI採取なし＝DESIGNED_NOT_RUN。
  - [EVIDENCE ID] 保存済み契約 ID `REA-ND-20261013-001` を再利用。今回新規Ghidra(info,pseudo,assembly,callers,callees) evidence ID=0件、独立5方法を新規検証した関数=0、STATIC VERIFIED増分=0。
- **Unresolved/corrections:** - [OBSERVATION DESIGN NOT RUN] ①選択解除前のengine+1E8B34/owner identity、②4EC680/4C5C40帰還時、③41F850/56BA80/global virtual/401BE0の各正常帰還、④0x527F55→0x568532または0x5685FD、⑤0x575F71でのengine+1E8B34再読、⑥二番目のowner/Troop/0x575F91を別receiptで追う。各callee未帰還ならVERIFYのまま。合法な旧EXE UI採取なし＝DESIGNED_NOT_RUN。 / - [MASTER] 直近MASTER checkpoint191、研究 DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-2034-DEATH-SECOND-RETURN-EPILOGUE-SCOPE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_2034_DEATH_SECOND_RETURN_EPILOGUE_SCOPE_QC.md`; actual SHA256 `B9FBBFF697D454806817EA6ADF0A85C431CD9E4B0BFCC9EEF9F1472C296DDF69`, 4268 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [BRANCH 1] 0x575F62はU+1D0をEDIへ読む。0x575F68 TEST／0x575F6A JE 0x575F71、非nullなら0x575F6C CALL 0x5684B0→0x575F71。第一CALLを無条件実行しない。
  - [BRANCH 2] 0x575F71 CMP BYTE [U+1867D],0、0x575F78 JE 0x575F91。非0の場合だけ0x575F7A..86でU+C→world+4→engine+1E8B34を再読、+358して0x575F8C CALL 0x5684B0→0x575F91。第一CALL後のflag再読が必須。
  - [NEW NARROW CROSSCHECK] 0x575F91 POP EDI／0x575F92 POP ESI／0x575F93 POP EBP／0x575F94 POP EBX／0x575F95 RET。第二CALL正常帰還PCからnative graph exitまでの可視命令は4つのregister restorationとRETのみで、新たなUnit/Troopメモリ書込・条件分岐はこの5命令に見えない。
  - [VERIFY BOUNDARY] High-levelでEpilogueを省略しても副作用差が無いという限定仮説は、outer return 0x575C54へのstack/register/呼出継続の一致をまだ証明しない。第二callee未帰還・未完了中は0x575C54へ進めない。Task/Spatial cleanup完了・caller return 575D0Dは別判定。0x575F91 stateをデバッグtraceで保持すべきかは互換性設計上のVERIFY。
- **Unresolved/corrections:** - [VERIFY BOUNDARY] High-levelでEpilogueを省略しても副作用差が無いという限定仮説は、outer return 0x575C54へのstack/register/呼出継続の一致をまだ証明しない。第二callee未帰還・未完了中は0x575C54へ進めない。Task/Spatial cleanup完了・caller return 575D0Dは別判定。0x575F91 stateをデバッグtraceで保持すべきかは互換性設計上のVERIFY。 / - [MASTER/GOLDEN] 最新読取checkpoint191、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-2143-DEATH-SECOND-CALL-REACHABILITY-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_2143_DEATH_SECOND_CALL_REACHABILITY_QC.md`; actual SHA256 `A1597220EFE5DDB2302C925F97D7750D12862B25E1A799A8DED2186D50FD2B04`, 5498 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [PRIMARY] 既存 logs/NORMAL_DEATH_CONTRACT_VERIFY_20261013.json（REA-ND-20261013-001、134 saved shape checks PASS）、SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md §ND-TROOP、dev_lab/reports/CHATGPT_HEAL_MUTATION_20261012.log の保存命令0x575F62..575F95。SHAは保存runのE8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、現物再hashなし。
  - [NATIVE PARENT] 0x575F62はU+1D0を取得、nullなら第一0x5684B0をskipして0x575F71へ。null以外は0x575F6C CALL0x5684B0を正常帰還まで待つ。0x575F71でU+1867Dを**再読**し、0なら0x575F91へ飛び第二call無し。非0だけengine+1E8B34の現在owner+0x358を使い0x575F8Cで第二0x5684B0を実行。
  - [NATIVE CHILD EFFECT] 0x5684BDはT+1Dを検査。T+1D非0のselected枝で、memberのU+1867C非0を検出すれば0x5684EBでそのmemberの+1867Dを0にして0x568501以降のstable-pruneへ進む。第一Troopが選択モードで死亡Unit自身をmemberとして含む場合、この局所書込によりflagは0になる。ただし後続UI/calleeがflagを再設定するか未確認のため、第二callをskipするのは0x575F71時点でも0のケースに限る。
  - [HOST MATCH] native_battle_outcome.py のupdate_troop_5684b0はselected枝のremovedについてunits[p].fields[0x1867D]=0を実行。native_battle_session.py のcontinue_resolved_normal_disable_troopsは第一callのcomplete後0x575F71へ進み、unit.read(0x1867D)&255を再評価して第二callをgateする。これらの局所条件は保存命令と整合する。
  - [TEST CONTRACT / NOT RUN] 旧原作では第一/第二Troop ptr、各T+1D、死亡U+1867C/+1867Dの第一call前後、engine+1E8B34、第二T live数、527ED0到達、0x575F71/0x575F91各正常帰還を独立nullable receipt化。原本実機golden/strict PASSに加算しない。
  - [DEDUP] 直前18:35はowner rebinding、19:33は527ED0の局所owner書込、20:34は0x575F91純epilogue。本回の増分は「第一selected pruneによる第二call抑制」と「owner bind懸念の3重到達gate」の限定照合のみ。新取得info/pseudo/assembly/callers/callees Evidence ID=0、新VERIFIED=0。
- **Unresolved/corrections:** - [MASTER/GOLDEN] MASTER最終確認checkpoint191、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。 / - [NEXT] 新規逆解析せず、許可済証拠で第二527ED0の発生条件と既存binding寿命を照合。Ghidra 5方法の追加取得、合法旧ゲーム到達・実機goldenは未実施/VERIFY。条件が成立するまで仕様変更提案止まり。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-2338-T013-T031-DIRECT-RAND-CALL-COUNT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_2338_T013_T031_DIRECT_RAND_CALL_COUNT_QC.md`; actual SHA256 `23678568EA6F4AF12CBE03E3B77E892C2ED00776CF007D84A217E9FB5EADD81C`, 4698 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [EVIDENCE] runs/20261009T225741694Z/57B870_procedure_assembly.json ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c。
  - [CROSSCHECK] 同run procedure_info ev_c4fcdda0f9486944ccdcfe1354a6d2e37f2b68761dfd2e47b7df9a11cd367612（entry0x57B870、0x57B870..0x57BB9B、812bytes）、pseudo ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc、callees ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203。callersも既存証拠を参照、新取得なし。
  - [DIRECT RAND SITES] 0x57B8FE CALL 0x5B6EAB：U+0x1E534 >= global[0x65BCAC]の再評価枝では無条件1回。0x57B940 CALL 0x5B6EAB：U+0x1E570==0かつsigned(U+0xC8)<0の場合だけ追加1回。0x57BA10 CALL 0x5B6EAB：U+0x137!=0かつsigned(U+0xC8)<0なら、候補vector分岐に先立ち追加1回。
  - [EARLY EXIT] 0x57B87Fのsigned CMPでU+0x1E534&lt;global[0x65BCAC]なら0x57B887..0x57B8DB/0x57BB94から帰還。直CALL 0x5B6EABは0回で支援vector+0x1E584/588/58Cの本関数内更新も0。
  - [EXACT LOCAL FORMULA / NORMAL RETURN] C=(signed U+0x1E534>=signed global[0x65BCAC])。C falseならdirectRandCalls=0、trueなら 1 + int(U+0x1E570==0 && signed(U+0xC8)<0) + int(byte(U+0x137)!=0 && signed(U+0xC8)<0)。対象はこの関数本文に存在する0x5B6EABへの直接CALL回数のみ。下位calleeからの間接消費・異常終了は含めない。
  - [GATE VECTORS / STATIC DESIGNED NOT RUN] (counterBelow)→0、(counterReached, cachedTarget!=0, C8>=0)→1、(reached,cachedTarget!=0,C8<0,cap=0)→1、(reached,cachedTarget!=0,C8<0,cap!=0)→2、(reached,cachedTarget=0,C8>=0)→1、(reached,cachedTarget=0,C8<0,cap=0)→2、(reached,cachedTarget=0,C8<0,cap!=0)→3。
  - [IMPORTANT DISTINCTION] +0x137=0でもcounter到達なら0x57B8FE等でrand消費し得る。支援候補vector更新停止はPRNG不消費と同義でない。既存support cache早期return/能力gate記録とは別に「direct CRT RNG数」を今回式に限定した。
  - [LIMIT] target未キャッシュ時の0x514D60はSTEALTH判定で条件付きCRT乱数消費し得る（既存REA_T013_PRIMARY_SUPPORT_FILTERS_20261011_1733.md）。0x514D60/0x514F10の5種新規証拠なし。従って上式を全スレッドrand総消費回数や後続戦闘乱数列の一致へ拡張しない。実Unit条件とcaller/コール副作用はVERIFY。
  - [NEXT PRIORITY] T013/T031:0x514D60内STEALTH RNGの条件付き呼数を既存許可済み保存証拠と突合し、本直呼出式から分離したRNG連結を設計。T010/T012死亡処理の通常帰還・所有者変更は既存VERIFY継続。新Wave登録/重い解析は正規キュー更新・安全な負荷確認後のみ。
- **Unresolved/corrections:** - [MASTER/GOLDEN] 最新MASTER checkpoint191、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、old-new strict MATCH0、ゲーム再実装率は測定していない。 / - [NEXT PRIORITY] T013/T031:0x514D60内STEALTH RNGの条件付き呼数を既存許可済み保存証拠と突合し、本直呼出式から分離したRNG連結を設計。T010/T012死亡処理の通常帰還・所有者変更は既存VERIFY継続。新Wave登録/重い解析は正規キュー更新・安全な負荷確認後のみ。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-23H-T013-TRANSITIVE-CALL-GRAPH-CORRECTION-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_23H_T013_TRANSITIVE_CALL_GRAPH_CORRECTION_QC.md`; actual SHA256 `6B93639092B999F89E0DC072C57EDE3436059801E7A3F19807A52CBBE4B66FF3`, 4107 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [SOURCE] 承認済みコピー hakushin067_Vahren.exe の保存run SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回現物hash再測定なし。
  - [PARENT] run 20261009T225741694Z、0x57B870 assembly ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c。0x57BA53 CALL 0x57CFA0 と0x57BA97 CALL 0x57CFD0を別枝に保存。
  - [CHILD] run 20261011T153309850Z、0x57CFA0 assembly ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789、callees ev_4322b0d609d2b48ca8311e8a1e55d2455a54cb30a7c331b8d67b020d1e3c3d39。
  - [CHILD2] 同run 0x57CFD0 assembly ev_08eb96aea33c3dbd4a1ae58fa08f3b20bfb31b8ccea4539a5bc0044cbb4887b5、callers 0x57B870/0x57CFA0、callees ev_2dc9297fab51c57cfc686ea99152528224402c6e4b39256935a1d5594e621958。
  - [EXACT TRANSITIVE FLOW] 0x57BA53→0x57CFA0→(0x57CFAA begin!=end時 0x57CFB0 CALL 0x5158A0→end書換)→0x57CFC7 CALL 0x57CFD0。従って0x57BA53側が0x5158A0/0x57CFD0を『経由しない』という2026-10-11旧メモの表現は誤り。
  - [OTHER BRANCH] 0x57BA7E begin/end比較→非空時0x57BA84 CALL 0x5158A0、0x57BA89 end書込→0x57BA97 CALL 0x57CFD0。こちらは0x57CFA0 wrapperを経由せず同2子処理へ直接進む。
  - [INPUT DIFFERENCE] 0x57BA36..0x57BA41 はUnit+1D4を取得してその+1Cから0x514F10へECX引渡。0x57BA5A..0x57BA62はUnit+1D4自体をECX引渡。共通子を使うがbuilder入力を一律同一とみなさない。
  - [DEDUP/CORRECTION] REA_T013_SUPPORT_CACHE_GUARD_MATRIX_20261011_0037.md の「0x5158A0と0x57CFD0は経由しない」、REA_T013_SUPPORT_VECTOR_REFRESH_GUARD_20261010_2336.md の直接CALL/間接CALL混同を限定訂正。REA_T013_EMPTY_RANGE_REPLACE_ABI_AUDIT_20261012_0536.mdの子内部CALLと同一既知証拠であり関数新規VERIFIED=0。元ファイルは編集しない。
  - [COMPAT TEST DESIGN/NOT RUN] cache begin=end / !=end、+137=0/!=0、+C8正負、乱数branch、0x514F10入力別に直接CALL・間接CALL・0x5158A0回数、0x57CFD0回数、Unit+1E584/588/58C、候補元・結果を独立receipt化。Ghidra静的callerは解決済みCALLのみ、間接関数ポインタの完全性は保証しない。
- **Unresolved/corrections:** - [LOAD] Desktop Commander Local接続成功。list_processesにVahren.exe PID26568が存在（他担当所有/原本か不明のため非介入）、CPU表示n/a、空きRAM未測定、Node/Chrome多数。Java/Ghidra名称を検出できないことは低負荷証明にならない。active.lockは直前のフォルダ一覧に未表示、原子的検査ではない。重いREA/Ghidra起動0秒。 / - [MASTER/GOLDEN] 研究MASTER最新確認checkpoint191・DONE9/34, IN_PROGRESS21, VERIFY4。旧EXE実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

## Curator review

Same VA, condition or source E8 is not a fresh function each hour. Correlate with REA earlier/later IDs, T013/T014 native/Work fixes and original source SHA before adopting a correct feature into REF/symbol dictionary. No raw original EXE, denied Wave6, original-game SAVE or unrelated owner workspace changed. Current develop belongs exclusively to KB curator.
