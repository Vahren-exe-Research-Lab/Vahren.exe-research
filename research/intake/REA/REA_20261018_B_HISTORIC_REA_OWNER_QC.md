# REA legacy research 20261018 B

Private REA owner intake / static & conditional inferred / VERIFY; NOT CURATED or READY. All 8 historical source IDs are older independent QC or research notes. The original owner Markdown reports are SHA256-verified read-only on research PC (2026-11-02 JST); no new original EXE/V9 rehash, Ghidra or original game run. Excerpts below are only prior allowed static claims. Prior refused operations/results/VA remain BLOCKED and excluded. No newly verified five-method function; original Golden PASS/READY=0.

### REA-20261018-1335-DEATH-UNITFLASH8-REGISTRY-COVERAGE-01

- Source `rea_lab/decomp_task/REA_20261018_1335_DEATH_UNITFLASH8_REGISTRY_COVERAGE_QC.md` / actual SHA256 `EF6669100F265D444ECFF58377F8272644DF596349B0EC030FF5F2549586C26D` (4741 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [SAVED NATIVE] 0x575F41から計8枠を順に確認し、base=U+0x928+i*0x264、active byte=base+0x78=U+0x9A0+i*0x264。非activeはskip。activeではowner=mem32(base+0x6C)を使用し、0x575F51でactiveを先に0にしてから0x575F54→0x41E160をcall。戻り位置0x575F59。i=0..7、通常帰還/副作用完了は引き続きVERIFY。
  - [NATIVE PROVENANCE] 既保存SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md ND-GRAPH-TAIL/UnitFlash ctor crosswalk。logs/NORMAL_DEATH_CONTRACT_VERIFY_20261013.json はcontract REA-ND-20261013-001、134チェック、failure0の保存済STATIC検証。旧EXE動的観測ではない。
  - [NEW LIMITED DELTA] prebindされたUnitWindowRegistry/MotionChild一覧が、死亡後段8 UnitFlashの現在のactive集合と同一とは証明できない。既存unregister_resolved_windowを順番に呼ぶだけでは、(i)nativeのslot順、(ii)active=0の事前書込、(iii)slotごとのlive owner、(iv)0x41E160の正常帰還を受理したことにならない。
  - [EVIDENCE] 今回取得の新Ghidra info/pseudo/assembly/callers/callees IDは0、関数境界の新認定0、STATIC VERIFIED増分0。承認済コピー再SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。一切のEXE実行なし。
  - [LIMIT/RESTART] 単一MCP、最大4関数/回、Ghidra900000ms/request960000ms。次回はUnitFlash8枠のowner/active/41E160 returnを保存済nativeで更に照合し、先行四window→8slot→575F62部隊update→575F95→575C54→575D0D→5789F2の未帰還点を独立管理する。
- **Limitations/errata:** - [NATIVE PROVENANCE] 既保存SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md ND-GRAPH-TAIL/UnitFlash ctor crosswalk。logs/NORMAL_DEATH_CONTRACT_VERIFY_20261013.json はcontract REA-ND-20261013-001、134チェック、failure0の保存済STATIC検証。旧EXE動的観測ではない。 / - [MASTER/GOLDEN] 最新MASTER checkpoint182、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-14H-DEATH-DETACH-CALLSITE-PC-01

- Source `rea_lab/decomp_task/REA_20261018_14H_DEATH_DETACH_CALLSITE_RETURN_PC_GATE_QC.md` / actual SHA256 `98782235E090B3E56A36AE4090CAD413EA81EF0936DEF803C921578E48A5C1CB` (5031 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE SAVED DIRECT CALLS] 0x575DF0後段の直接4回は41E160へ0x575F15→return 0x575F1A（W=U+0x638）、0x575F20→0x575F25（W=U+0x6CC）、0x575F2B→0x575F30（W=U+0x1C48）、0x575F36→0x575F3B（W=U+0xD11C）。ここは固定4callであり8slotのactive gateとは別。
  - [NATIVE SAVED FLASH LOOP] UnitFlash i=0..7、base=U+0x928+i*0x264、active=byte(base+0x78)。active=0なら41E160をskip、非0ならowner=mem32(base+0x6C)、activeを先に0にして0x575F54 CALL 41E160→0x575F59に復帰する。複数slotが同一帰還PCを使用するためindex・owner・targetも必要。
  - [SHARED INNER RETURN] 41E160内でrecord一致時、record byte0=0／末尾交換／end-=4のcommit後、0x41E1C3で4C5CC0をCALL。inner帰還0x41E1C8はtick/death共通。一致なし/空なら内側cleanupを呼ばない即帰還があり、同じ関数復帰PCでもpending有無は異なる。
  - [WORK SESSION ENTRY] native_battle_session.py L406-409はtick側advance時に0x41E1C3を検出した場合だけVERIFY_UNIT_WINDOW_DETACHとcontextを設定。source文字列検索では同phaseの使用箇所はここだけ。死亡側continue_resolved_normal_disable_graph（L281-290）は初回のみ受け付け、UnitWindowRegistry.detach/pendingと接続していない。
  - [NEW DELTA] 既存tick向けWindowDetachTraceのcaller_return_pcを無条件に使うと死亡後段の4種類の直接call帰還PC及びflash loop帰還PCと一致しない。共通callee処理を再利用する場合でも「inner 41E1C8」と「outer callsite固有575F1A/25/30/3B/59」を分離する必要がある。既往の『8flashのowner/active対応不足』とは別の厳密な継続PC上の制約。
  - [EVIDENCE] 新Ghidra info/pseudo/assembly/callers/callees evidence IDは各0。既存STATIC contract ID=REA-ND-20261013-001、保存SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md ND-GRAPH-TAIL/ND-DETACH、REA_SAVED_NATIVE_PREFIX_CONTINUITY_20261013.md、およびWork現行コードを根拠とする。source SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回承認コピーを再計算して一致）。
- **Limitations/errata:** - [NEW DELTA] 既存tick向けWindowDetachTraceのcaller_return_pcを無条件に使うと死亡後段の4種類の直接call帰還PC及びflash loop帰還PCと一致しない。共通callee処理を再利用する場合でも「inner 41E1C8」と「outer callsite固有575F1A/25/30/3B/59」を分離する必要がある。既往の『8flashのowner/active対応不足』とは別の厳密な継続PC上の制約。 / - [VERIFY BOUNDARY] 死亡時の各recordの存在、window vptrの実帰還、副作用、異常経路、UnitFlashのruntime owner、他モジュールにある未探索の継続実装、旧EXE実機一致はVERIFY。今回STATIC SOURCE CROSSWALKのみで原作の新規BUG・ゲーム仕様VERIFIED追加ではない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-1530-DEATH-DETACH-NOHIT-SCOPE-01

- Source `rea_lab/decomp_task/REA_20261018_1530_DEATH_DETACH_NOHIT_SCOPE_QC.md` / actual SHA256 `24E7A780481A30265F58FBFFE60BCB366F8BBCB2B4BF94B4CFBD5948778B1EA9` (3737 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE SOURCE] REA-ND-20261013-001 / SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md ND-DETACH・ND-GRAPH-TAIL。41E160はEAX=W,ESI=owner Oでrecord+4==Wの最初の一致を探索する。空/非一致はrecord変更なしで関数から帰還。一致時はrecord byte0=0、末尾swap/end-4を先行commit、41E1C3で4C5CC0へ入る。
  - [RETURN BOUNDARY] 四固定callの外側returnは0x575F1A/0x575F25/0x575F30/0x575F3B、Flash callの外側returnは0x575F59。41E18A/41E1CBとtick既定0x57AB68はこれらを代用しない。hit時のinner4C5CC0 return_pc=0x41E1C8はさらに別。
  - [NEW DELTA] 既往のhit時のPC不一致に加え、record非一致のcomplete=Trueを死亡側全体完了へ誤昇格させない必要がある。非active skip・非一致return・一致pendingの三者を明示的なcallsite/slot/owner状態で管理する。
  - [EVIDENCE] 既存contract REA-ND-20261013-001、REA_20261018_14H_DEATH_DETACH_CALLSITE_RETURN_PC_GATE_QC.md。今回取得のGhidra info/pseudo/assembly/callers/callees evidence IDは各0、関数VERIFIED増加0。承認コピーsource SHA指定値E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回はファイル再SHAなし）。
- **Limitations/errata:** - [VERIFY] 各実UnitFlashのruntime active/owner、record有無、仮想呼出先と実帰還、部隊更新への合法到達、Work全モジュールの別名resumeの有無、旧EXE実機一致は未確認。原作BUGや動的不一致の確定ではない。 / - [MASTER/GOLDEN] 最新MASTER checkpoint182、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0、ゲーム再実装率未測定。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-1833-TROOP-UI-PHASE-DEADEND-01

- Source `rea_lab/decomp_task/REA_20261018_1833_TROOP_UI_SELECTION_PHASE_DEADEND_QC.md` / actual SHA256 `0C21172736DB9D44FB8132B1FA539A7A0DAB1BABB0A17F59A7AC796CB1EE5313` (4499 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE] 既保存REA-ND-20261013-001 ND-GRAPH-TAIL/ND-TROOP：死亡側0x575F6C→0x5684B0（外側帰還0x575F71）、条件付0x575F8C→同関数（外側帰還0x575F91）。一回目の正常帰還後にUnit+0x1867Dを再読。
  - [TROOP BRANCHES] 選択中で剪定後空なら0x56852D→0x527ED0（復帰0x568532）。選択中・非空なら0x56853B→0x41F850（復帰0x568540）。通常・生存あり・先頭条件成立なら0x5685C5→0x527EA0へtail jump。通常・全滅・先頭条件成立なら0x5685F8→0x527ED0（復帰0x5685FD）。
  - [NEW DELTA] 前回の「0x41F850/0x527EA0が選択解除advance対象外」に加え、advanceが対応する0x527ED0経路さえ0x527F29→0x41F850のpending UIを戻す公開Session経路が確認できない。部分リング変更をもって0x527ED0、0x5684B0、0x575DF0全体の正常完了とは扱えない。
  - [RETURN STACK] 0x41F850から0x527F2E→0x527ED0内部復帰→0x568532または0x5685FD→0x5684B0の残余分岐→死亡側0x575F71または0x575F91の順の実return receiptが必要。tail-jump0x527EA0および選択中非空UI経路は別stage。状態フラグのみで成功帰還を偽装しない。
  - [EVIDENCE] 既存契約REA-ND-20261013-001、保存SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md ND-TROOP、dev_lab上記2ファイル。新規Ghidra info/pseudo/assembly/callers/callees evidence IDは各0。承認コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187を本runでLocal Get-FileHash再確認。
- **Limitations/errata:** - [VERIFY] 上記4経路の合法実到達、UI各helperの副作用/戻り値/失敗時挙動、Session他モジュールの外部操作の全量網羅、旧実機の挙動は未検証。既存静的照合の新発見であり旧実機BUG確定・5方法Ghidra VERIFICATIONではない。 / - [MASTER/GOLDEN] 現行MASTER checkpoint185、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-1935-TROOP-SELECTION-SINGLE-BINDING-01

- Source `rea_lab/decomp_task/REA_20261018_1935_TROOP_SELECTION_SINGLE_BINDING_QC.md` / actual SHA256 `F95D357F4EA5671998679A2DA28E7809889CCB1FF35E7CAEC9E9A466A3CD9FC7` (4640 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [SAVED NATIVE] REA-ND-20261013-001: 通常死亡0x575DF0後段は0x575F6C→0x5684B0（復帰0x575F71）と、Unit+0x1867D再読後に条件付き0x575F8C→0x5684B0（復帰0x575F91）の二層。0x5684B0の選択中空0x56852Dと通常全滅先頭条件0x5685F8はそれぞれcallee0x527ED0、帰還0x568532/0x5685FD。
  - [WORK SOURCE 2] native_battle_outcome.py: TroopSelectionCleanup.advanceはself.trace!=Noneで再実行拒否。TroopSelectionTraceにparent_return_pc（0x568532又は0x5685FD）と下位return_pc=0x527F2Eを分離保存しcomplete=False。再利用・再bind・parent returnの公開処理は今回確認したSessionの該当箇所では見つからない。
  - [NEW DELTA] 前回の単一0x527ED0内部UI帰還欠落に加え、仮に一回目の下位UI/parent帰還を後段で実装しても、同一Sessionで別の0x527ED0呼出へ進むためのbinding世代交代が現状確認できない。戻り先だけでなくbinding identity、caller pair、解除したnode、次の呼出でfresh ringを区別する必要がある。
  - [LIMIT/VERIFY] 原作で同一死亡eventから二つの0x527ED0枝へ合法到達するか、第二の対象troop・ownerが同一か、他module/runner外で新Sessionを生成するかは未確証。実機不一致確定ではない。既存の単発UI deadendとは別の条件付きintegration gateとして記録。
- **Limitations/errata:** - [LIMIT/VERIFY] 原作で同一死亡eventから二つの0x527ED0枝へ合法到達するか、第二の対象troop・ownerが同一か、他module/runner外で新Sessionを生成するかは未確証。実機不一致確定ではない。既存の単発UI deadendとは別の条件付きintegration gateとして記録。 / - [MASTER/GOLDEN] MASTER最終checkpoint185、34Task DONE9/IN_PROGRESS21/VERIFY4、旧EXE実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-2034-TROOP-HEAD-FLAG-SECOND-UPDATE-01

- Source `rea_lab/decomp_task/REA_20261018_2034_TROOP_HEAD_FLAG_SECOND_UPDATE_QC.md` / actual SHA256 `4A6E65EEE19CAB8B21C5519ECCFAAF8AF3087683028D2D4D2163EF1919189516` (4529 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE EVIDENCE] SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md §ND-TROOP（保存済native 0x5684B0..0x56861A）と§ND-GRAPH-TAIL（0x575F62..0x575F95）；既存契約REA-ND-20261013-001。新規Ghidraの5種類の証拠IDは0。
  - [ORDER] 0x5684B8→0x569280で部隊幅T+34を先に更新。T+1Dが非0ならdisabled memberをstable eraseし、そのU+1867D=0をcommit。T+1Dが0ならdisabled memberを部隊vectorから消さず、生存個数だけ数える。
  - [NORMAL NONEMPTY / IMPORTANT] T+1D==0かつlive_count>0時、0x5685C5→0x527EA0 tail-jumpの判定は**vector先頭troop.members[0]**のbyte+8C==0 && byte+1F8!=0。最初の生存Unitを選び直さない。先頭が既disabledでも判定元であり得る。
  - [BRANCH CASE A] normal, head disabled(1867C=1) かつ8C=0/1F8!=0、後続liveありなら、候補経路は0x5685C5 tail-call 0x527EA0。live_count>0でも既disabled headはvectorに残る。合法原作ゲーム到達はVERIFY。
  - [BRANCH CASE B] normal, head disabledだが8C!=0又は1F8=0、後続liveありなら、同じlive_countでも0x56861Aへ直接帰還し得る。旧実機・他calleeの副作用はVERIFY。
  - [BRANCH CASE C] selected T+1D!=0で同じhead disabled／後続liveなら、先頭削除とU+1867D=0が起こり、残存時は0x56853B→0x41F850のpending UI。normalと同じ整理にしない。
  - [SECOND UPDATE CONDITIONAL] normal T+1D==0ではこの部隊更新自身はU+1867Dを消さない。したがって最初の5684B0が正常RETしても、死亡側0x575F71後のU+1867D再読が非0なら0x575F8Cの第2部隊更新を省略できない。「第一call complete」や「生存memberあり」は第二call省略の十分条件ではない。第2対象selectedTroopは別pointerとして評価する。
  - [COMPAT ACCEPTANCE NOT RUN] 同一二Unit fixtureをselected=0/1、head+8C/+1F8、head disabled、tail live、U+1867D、selectionOwner/selectedTroop identityの軸で比較。各callのcallee, nextVA, returnPC、member order、U+1867D before/after、0x575F71→0x575F8C条件を記録し、未帰還UIを成功と偽装しない。
  - [LIMIT] この分析は保存済みnative仕様と現存Python条件の静的クロスウォーク。テスト実行・原作実機観測・新Ghidra逆コンパイル・新関数VERIFIEDは0。first-control flagsのゲーム上の意味、合法シナリオ到達、異なるworld所有者の一貫性はVERIFY。
- **Limitations/errata:** - [LIMIT] この分析は保存済みnative仕様と現存Python条件の静的クロスウォーク。テスト実行・原作実機観測・新Ghidra逆コンパイル・新関数VERIFIEDは0。first-control flagsのゲーム上の意味、合法シナリオ到達、異なるworld所有者の一貫性はVERIFY。 / - [MASTER/GOLDEN] 最新MASTER checkpoint185、34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-21H-TROOP-MODE2-AFTER-SELECTION-01

- Source `rea_lab/decomp_task/REA_20261018_21H_TROOP_MODE2_AFTER_SELECTION_CONTINUATION_QC.md` / actual SHA256 `8CD0CF743D76EA8FF81FD832787D7C69E73707E0610195ADD059705A63A6BD9E` (4633 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE SOURCE] REA所有 SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md §ND-TROOP / 既存契約REA-ND-20261013-001。対象VA 0x5684B0,0x5685CA,0x5685F8,0x5685FD,0x56860F,0x568614,0x56861A,0x527ED0,0x4C22B0。
  - [BRANCH PRECONDITION] 通常Troop T.byte+1D==0、生存Unit数0。0x5685CAでT+1C=1。配列先頭U.byte+8C==0かつU.byte+1F8!=0の場合、0x5685F8から0x527ED0(T)に分岐する（配列先頭と最初の生存Unitの同一視は禁止）。
  - [POSTCALL NATIVE ORDER] 0x527ED0が正常帰還して初めて0x5685FDに進む。そこでengine+1EF140==2を評価する場合、0x56860Fから0x4C22B0(engine+C,T,delete=0)を呼ぶ。正常帰還は0x568614、最後は0x56861A RET。UI未帰還は完了ではない。
  - [WORK CONTINUATION] native_battle_session.py continue_resolved_troop_selectionはbinding.advance後 phase=VERIFY_TROOP_SELECTIONとする。native_battle_runner.py のtroop_selection_resolvedもtrace生成後breakし、現存調査対象コード中に0x5685FD以降からmode2 Task解除へ戻す実装が確認できない。
  - [DELTA] 単に527ED0からUIを帰還させるだけでは足りない。normal・empty・controlled・mode2時の選択解除完了→0x5685FD mode2判定→条件付き4C22B0→0x56861Aのresume receiptが必要。mode2条件はnativeの後段評価であり、calleeの副作用を無根拠にゼロと置いて入口で早期判断しない。
  - [LIMIT/VERIFY] 合法ゲームで上記組合せへの到達、527ED0/UIの全帰還、副作用、Task結果の実機一致は未証明。Workの全モジュール横断の不存在証明ではなく確認したAPI/runnerにおける静的接続不足。旧EXE実機test 0、新規Ghidra取得0。
  - [ACCEPTANCE NOT RUN] first=disabled, liveCount=0, T+1D=0, head+8C/1F8 controlled=true, engine+1EF140=2のFixtureで trace→527ED0→UI→5685FD→4C22B0(delete0)→56861A→死亡側0x575F71又は0x575F91を個別継続し、各段階のnextVA/returnPC/owner/Task active/pending before-afterを保存。各callee未帰還ならVERIFYのまま。
- **Limitations/errata:** - [ACCEPTANCE NOT RUN] first=disabled, liveCount=0, T+1D=0, head+8C/1F8 controlled=true, engine+1EF140=2のFixtureで trace→527ED0→UI→5685FD→4C22B0(delete0)→56861A→死亡側0x575F71又は0x575F91を個別継続し、各段階のnextVA/returnPC/owner/Task active/pending before-afterを保存。各callee未帰還ならVERIFYのまま。 / - [MASTER/GOLDEN] 今回読取MASTER checkpoint185、34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-2340-DEATH-SELECTION-PREFIX-CROSSCHECK-01

- Source `rea_lab/decomp_task/REA_20261018_2340_DEATH_SELECTION_PREFIX_CONTRACT_CROSSCHECK_QC.md` / actual SHA256 `9265729F4A71D0EBF690A0CB52CECA912F42860B0D5460BA155E3CB2D9715FAD` (3244 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [SOURCE] SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md のREA-WRQ-20261013-DEATH-11/12（0x527ED0..0x527F55、0x4EC680、0x4C5C40）。保存run source SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
  - [STATIC CROSSCHECK 1] T+0x1D=0時のみselectionOwner+0x348 listからTroop*一致node全件を解除（0x4EC680）。Work selection全一致の抽出とfor/unlinkは、この局所の重複削除多重度と整合。
  - [STATIC CROSSCHECK 2] 解除後owner+0x34Cが0、かつ((owner+0x368-owner+0x364)&0xFFFFFFFC)==0の2条件でowner+0x45Dを0化。Work count=oldcount-len(selection)、bitmask比較、hide→+0x45D=0は局所条件と整合。
  - [STATIC CROSSCHECK 3] owner+0x20C非0なら先に0化し、4C5C40でtarget=&owner+0x1E0のdisplay list最初の一致1件だけ解除。Work display[:1]・+0x20C=0・unlinkが該当する。
  - [BOUNDARY] 整合は選択解除prefixの条件・削除多重度・書込順序に限定。0x4EC680/0x4C5C40のallocator障害、callee未帰還、続く0x527F27→41F850→56BA80→global vfunc→条件付401BE0→0x527F55 RET4と上位0x568532/0x5685FDへの帰還はVERIFY。WorkのVERIFY_TROOP_SELECTION後の復帰未実装懸念を解消していない。
  - [EVIDENCE] 新規Ghidra info/pseudo/assembly/callers/calleesの証拠ID各0、新規関数VERIFIED+0。再利用する既存静的契約=REA-ND-20261013-001。旧実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。
- **Limitations/errata:** - [BOUNDARY] 整合は選択解除prefixの条件・削除多重度・書込順序に限定。0x4EC680/0x4C5C40のallocator障害、callee未帰還、続く0x527F27→41F850→56BA80→global vfunc→条件付401BE0→0x527F55 RET4と上位0x568532/0x5685FDへの帰還はVERIFY。WorkのVERIFY_TROOP_SELECTION後の復帰未実装懸念を解消していない。 / - [MASTER] 最新読取checkpoint186、研究34Task DONE9/IN_PROGRESS21/VERIFY4。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

## Curator handoff

Older reports may overlap with current B/REA research and already-curated REF facts. Match source SHA, VA, exact branch semantics, corrected owner interpretations and provenance before adopting anything. No raw tool logs/secret paths/native binary or refused evidence added, and no develop/REF/symbol edits by REA. New formal evidence five-set 0, new VERIFIED 0, Golden PASS 0.
