# Historical 2026-10-15 REA owner research A: legacy unit/task/ABI notes

REA independent owner / private research intake, not officially CURATED. 10 original source research IDs existed on PC and were rehashed read-only 2026-11-02 JST. These are **older source records** (not new Ghidra function analysis). Short native/ABI passages are excerpted from each report, while refusal-specific lines, targets and evidence are deliberately excluded; only the separate historical safety status is retained. No original binary/runtime inspection or actual game run occurred. Wave1–5 historical 64/64 is not recalculated; new five-method VERIFIED=0, original Golden PASS=0, READY=0.

### REA-20261015-0034-UNIT-DISABLED-TASK-LIFETIME-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_0034_UNIT_DISABLED_TASK_LIFETIME_REVIEW.md`, actual SHA256 `C3103A2F9E9E23E2B628760E4D39A48C0188CA0F55613583FB3058A4F4A874E1`, 4500 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [SOURCE NATIVE] B所有の既保存 `data/T012_BATTLE_CALC.md` §65 / evidence B-20261010-2117-01 / `exe/T012_STATUS_CORE_DUMP.txt` 0x57AA0F..0x57AA17: Unit v+04 Task tick=0x57AA00はUnit+0x1867C!=0を読み0x57B36E epilogueへ早期分岐。これはUnitメモリが有効でvirtual +04を呼べた場合の入口分岐。unit Task解除済・二重呼出を示す証拠ではない。
  - [SOURCE LIFECYCLE] 既存REA DEATH-33/47・ND-001の原作順序: 通常死亡0x575A60でU+0x1867Cを先に立てるが、0x575DF0の後、外側0x575C54以降でUnit Task 0x4C22B0を登録解除し、0x575D0Dで帰還。flag writerとTask tombstone/returnを同時完了扱いにしない。
  - [DERIVED INVARIANT / NOT A NEW BUG] 「Unit.disabled=1」単独では「Task unregister正常return済」も「rosterからUnitを削除可能」も証明できない。通常Unit Task pointerがactiveに残り、かつUnitオブジェクトが合法に存続する場合、Task+04のdisabled早期returnとTaskの後続tombstoneは別段階。Workの現在のself._unitsはconstructor固定であり、今回読んだ範囲に死亡時の明示的deleteは見つからない。従って現実にWorkがUnit mapから早期削除する不具合は**未立証**。以前のphase gate、Task事前型検証、embedded pointer identityを新バグとして再計上しない。
- **Limitations/corrections:** - [VERIFY] nativeで死亡graph INFLIGHT中に別host/Task passが合法に再入するか、live Unit vptr・Task slotの実寿命、Unit.ghost/tombstone、Work runtimeの同一Unit map使用時phase・callbackの正常帰還。旧未改変EXEのgolden/新旧strictはNOT RUN。 / - [WORK/F ACCEPTANCE DESIGNED/NOT RUN] U+1867Cを0/1に分けTask active ptrの有無とTask phaseを固定し、Task v+04入口/early return、4C22B0 tombstone、575D0D親return、pending flush/次pass時刻、self._units保持を個別receipt化する。unknown型をUnitへaliasせず、死亡graph途中の処理はINFLIGHT/VERIFYで止める。B/T012とA/T010の正本は変更しない。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-0240-UNIT-REGEN-V70-ABI-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_0240_UNIT_REGEN_V70_CALL_ABI.md`, actual SHA256 `4DFB590294D1C9D8FCAA011B0E38CD113570C59926B5728F505B6A997F887258`, 3863 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [SOURCE] 承認済コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（本回Local再照合一致）。保存run=20261009T223622536Z、0x57DF90 entry/body 0x57DF90..0x57E173(length484)、Ghidra12.1.4。
  - [EVIDENCE IDS] procedure_info=ev_0c8f9a4e1bd5870aaf62a2605bdd65c8b51600c87ee44869d6596b1b7f16f938; assembly=ev_e50e0ad44fe14809a8e00c7e3754f2816f095b4d9686c6ba0d876d5ee0a337a1; callers=ev_43c77a49fb73c68c10f047d7febdc2dfbed7b901365ef01e249b11bcff311fee; callees=ev_e48cd61ab643e7cc8fb3ebe1a77fe3e379412db5f98273b0df7a59121d93a8e4; pseudo=ev_5a3e17e1d68d81c9aa62213f2e77e5ca9d1c90c4e1fda186678a72e6a88684ce。すべて既存証拠の再利用。
  - [XREF] 保存callersは0x545740/0x57AA00/0x57E4E0の3件。保存exe/T012_STATUS_CORE_DUMP.txtの0x57AA11..17はUnit+1867C非0ならepilogueへ早期分岐、0x57B345条件成立時の0x57B34B call 0x57DF90と0x57B369 call 0x57DF90の入口を支持。callers集合は間接経路を網羅しない。
  - [HP GATE] 既保存0x57DFB3..0x57DFFD：Unit+BC<0かつUnit+B4>=0ならHP回復をskip、他の場合はUnit+90 += Unit+B4をUnit+DCで上限clamp。結果のEAXが負なら0x57E039へ、負でなければ0x57E061のMP/status側へ。HP==0をこの分岐で即死にしない。
  - [NEW ABI DELTA] 0x57E039 EAX=[ESI]、0x57E03B EDX=[EAX+0x70]、0x57E03E push0、0x57E040 push0xB09758、0x57E045 push ESI、0x57E046 push0xF4241、0x57E04B ECX=ESI、0x57E04D call EDX。したがってこの呼出位置で観測されるスタック引数はpush順で(0,0xB09758,Unit,0xF4241)、ECX=Unit。B既存§26『0xF4241等』の具体化のみで、0xB09758の意味・vtable+70の実target/ABI callee cleanupはVERIFY。
  - [RETURN] 0x57E04F..60はcall帰還後、そのままepilogue/RETに進む。MP自然回復・7ゲージ更新・0x578EF0は同一57DF90 invocation内では実施されない。ただしvirtual+70内部の副作用、再入、元Task+04 callback正常帰還は未知。
  - [ACCEPTANCE/NEXT] B/Workは同Unit identity、+1867C、+BC/+B4/+90/+DC、57DF90入口caller/return PC、0x57E04D virtual実target・4args、575A60有無、task frame cursor/pending flushを別receiptで追う。原作合法旧SAVE/captureが無ければ旧goldenに加算しない。REA側は既存保存vtable/callersからv+70 concrete targetを安全に追加照合する。
- **Limitations/corrections:** - [NEW ABI DELTA] 0x57E039 EAX=[ESI]、0x57E03B EDX=[EAX+0x70]、0x57E03E push0、0x57E040 push0xB09758、0x57E045 push ESI、0x57E046 push0xF4241、0x57E04B ECX=ESI、0x57E04D call EDX。したがってこの呼出位置で観測されるスタック引数はpush順で(0,0xB09758,Unit,0xF4241)、ECX=Unit。B既存§26『0xF4241等』の具体化のみで、0xB09758の意味・vtable+70の実target/ABI callee cleanupはVERIFY。 / - [NOT DEATH GRAPH VERIFIED] normal Unit virtual+58=0x575A60は別slot。v+70を0x575A60と同一視しない。0x57DF90呼出が合法通常Task pass内でHP<0を作るか、v+70がその後0x575A60→0x575DF0へ到達するか、task 0x4C28D0へ正常returnするかは全てVERIFY。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-0345-REGEN-V70-NORMALVT-BRIDGE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_0345_REGEN_V70_NORMALVT_BRIDGE.md`, actual SHA256 `A3C426AAC3069F9DF95C58B504A4560BF29D8EF6685EF2CBD3D4B5301B5F5A8D`, 5955 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [SOURCE] Approved isolated rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187を本回03:37 Local preflightで実測一致。原本ZIP/EXE未実行・未変更。
  - [PREVIOUS LINK] 既存REA_20261015_0240_UNIT_REGEN_V70_CALL_ABI.md の保存run 20261009T223622536Z / 0x57DF90 (body 0x57DF90..0x57E173)。0x57AA00内の0x57B34B/0x57B369から条件付き0x57DF90呼出。0x57DFFB負HP分岐→0x57E04DがECX=Unit、stack push順0,0xB09758,Unit,0xF4241で [live_vptr+0x70] を間接CALL。帰還後0x57E060 RET、同一呼出でMP自然更新へ継続しない。
  - [EXISTING VTABLE EVIDENCE] 同REA所有SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md「ND-LETHAL」(旧保存証拠) は通常Unit vtable=0x63A9E4、virtual+0x70=0x578370と既に確定記載。ND-ENTRYは同VTの+0x58=0x575A60、+0x34=0x575DF0。B保存data/T012_BATTLE_CALC.md §17もhit handler 0x578370の生存/致死後処理を記録。今回の増分は2つの既存資料間で未接続だったcaller→VT→calleeの限定JOINであり、0x578370の新発見ではない。
  - [CONDITIONAL CHAIN] live Unit vptrが0x63A9E4で維持されたケースに限り、0x57E04D→0x578370が静的dispatch先。578370側の致死条件・付随afterdeath/効果が成立し、0x5789F0まで到達した場合はnormal +0x58 0x575A60→virtual+0x34 0x575DF0→既存Task/Spatial/部隊除去graphという条件付き呼出鎖。0x57DF90側のHP<0だけでこの完走は証明されない。
  - [GOLDEN LIMIT] 原作合法Unit/同identity、57AA00→57DF90のcaller/負HP発生、vptr実値、0x57E04D実target、0x578370の実入/帰、575A60/575DF0/Task解除/元callback帰還の各receiptを同一timestamp・同じ旧SAVE/seedで照合する。Work側への直接書込・受領なし。旧EXE actual gameplay golden PASS0、strict MATCH0。
  - [EVIDENCE IDS EXISTING] procedure_info=ev_0c8f9a4e1bd5870aaf62a2605bdd65c8b51600c87ee44869d6596b1b7f16f938; pseudo=ev_5a3e17e1d68d81c9aa62213f2e77e5ca9d1c90c4e1fda186678a72e6a88684ce; assembly=ev_e50e0ad44fe14809a8e00c7e3754f2816f095b4d9686c6ba0d876d5ee0a337a1; callers=ev_43c77a49fb73c68c10f047d7febdc2dfbed7b901365ef01e249b11bcff311fee; callees=ev_e48cd61ab643e7cc8fb3ebe1a77fe3e379412db5f98273b0df7a59121d93a8e4。新Ghidra5method evidence ID0。
  - [ADDITIONAL SAVED CALLEE JOIN / SAME-SESSION] B所有の既保存exe/T012_STR_AFTERDEATH_PROBE.txt VA0x578370..0x5785A3をread-only再確認。0x5783BBでUnit+1867C!=0なら0x578B3A早期終了。aliveなら0x5783D4でstack第1引数を読み、0x5783D7で0xF4241と比較、一致時0x5783E6でUnit+1E568=0、続く0x5783F0でUnit+90 HPからその0xF4241を減算、0x5783F6..FDでsigned HP<=0なら0x5785A3の致死側へ分岐する。従って57DF90呼出時点HP<0かつ同VT維持・未disabled・signed overflowなしなら0x5785A3入口までの順序を接続できるが、その後のafterdeath/virtual+58/Task正常帰還とINT32端のwrapはVERIFY。前段CALLによるその他副作用/RNGも未証明。新Ghidra取得0、関数VERIFIED増0。
  - [IMPORTANT PRE-DISPATCH REACHABILITY] B既保存exe/T012_STATUS_FUNCTION_ENTRY.txt 0x57DFFF..0x57E039では負HP判定後もglobal BYTE[0xB0A178] bit0を検査、非zeroなら0x57E039へ直接移るがzeroならbitを立てた後0x599600と0x5B6BA4を順にCALLしてから0x57E039へ至る。両calleeの正常復帰・警告/異常終了は未検証。したがってHP<0だけで0x57E04Dを必ず呼ぶとは断言せず、上記5785A3接続の前提に「0x57E039へ到達し0x57E04Dが正常dispatchする」を追加する。
- **Limitations/corrections:** - [FAILED OPTIONAL VALIDATION/RECOVERY REA-RC-20261015-0345-RAWVT-PARSER-01] Local read-only one-shot vtable four-DWORD spot-check はPowerShell ParserError EmptyPipeElementでEXEファイルopen前に終了。生pointer4件の本回再取得0。失敗スクリプトは繰返し・改変再提出せず、既保存ND-LETHALに根拠範囲を限定。停止ではなく既保存証拠で独立照合を続行。RAW VT追加取得/直接再検証は未完了VERIFY。 / - [IMPORTANT PRE-DISPATCH REACHABILITY] B既保存exe/T012_STATUS_FUNCTION_ENTRY.txt 0x57DFFF..0x57E039では負HP判定後もglobal BYTE[0xB0A178] bit0を検査、非zeroなら0x57E039へ直接移るがzeroならbitを立てた後0x599600と0x5B6BA4を順にCALLしてから0x57E039へ至る。両calleeの正常復帰・警告/異常終了は未検証。したがってHP<0だけで0x57E04Dを必ず呼ぶとは断言せず、上記5785A3接続の前提に「0x57E039へ到達し0x57E04Dが正常dispatchする」を追加する。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-0435-REGEN-SENTINEL-INT32-EDGE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_0435_REGEN_SENTINEL_INT32_EDGE.md`, actual SHA256 `06728CAC22EB9A82F1BC8911E37FD1417902DD2BD75E6649588A6FE65C078491`, 4031 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [INPUT/PROVENANCE] Desktop Commander Local Compact限定・B既保存exe/T012_STATUS_FUNCTION_ENTRY.txt（0x57DF90）とexe/T012_STR_AFTERDEATH_PROBE.txt（0x578370）をREAD ONLY照合。保存REA run 20261009T223622536Z の0x57DF90の5方法IDはREA_20261015_0240_UNIT_REGEN_V70_CALL_ABI.mdを参照。承認済COPY SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回Local再測定一致）。新規Ghidra evidence ID 0。
  - [CHAIN/GATES] 57DF90の57DFFB TEST HP→負なら57E039へ、前段B0A178 latch・599600・5B6BA4の正常帰還/合法到達はVERIFY。57E04D CALL [Unit.vptr+70]はECX=Unit、stack first arg 0xF4241 (=1,000,001)。既保存通常Unit VT0x63A9E4では+70=578370（他subclassへ一般化不可）。5783BBのUnit+1867C==0が必要。
  - [EXACT SAVED INSTRUCTIONS] 5783D7 CMP firstArg,0xF4241; 5783E6 MOV [Unit+0x1E568],0; 5783F0 SUB DWORD PTR [Unit+0x90],EAX; 5783F6 CMP DWORD PTR [Unit+0x90],0; 5783FD JLE 5785A3。32-bit SUBのwrap後の値をsigned CMP/JLEで評価する。INT32の数学上の減算と同一視しない。
  - [NEW BOUNDARY] 入口HP h がint32負値 [-2147483648,-1]の場合、h - 1000001 < INT32_MIN となるのは h <= -2146483648。これらはSUBで正値へwrapし、0x5783FD JLEを通らず0x578403側に進む。h >= -2146483647 なら結果は負で0x5785A3致死分岐へ入る（上記ガード成立・callee正常帰還を条件）。
  - [NEXT/TEST] Workはまず保存済み実装と合法旧HPレンジ制約を調べ、old合法入力の到達可否をVERIFY。合成単体は境界h=-2146483648/-2146483647、flag+1867C、vptr、0x1E568、SUB後HP、5785A3/578403、returnPCと後続effectsを分けて記録。実旧EXE goldenが無ければstrict MATCH扱い禁止。Workコード/原作の変更・実行なし。
- **Limitations/corrections:** - [NEW BOUNDARY] 入口HP h がint32負値 [-2147483648,-1]の場合、h - 1000001 < INT32_MIN となるのは h <= -2146483648。これらはSUBで正値へwrapし、0x5783FD JLEを通らず0x578403側に進む。h >= -2146483647 なら結果は負で0x5785A3致死分岐へ入る（上記ガード成立・callee正常帰還を条件）。 / - [NEXT/TEST] Workはまず保存済み実装と合法旧HPレンジ制約を調べ、old合法入力の到達可否をVERIFY。合成単体は境界h=-2146483648/-2146483647、flag+1867C、vptr、0x1E568、SUB後HP、5785A3/578403、returnPCと後続effectsを分けて記録。実旧EXE goldenが無ければstrict MATCH扱い禁止。Workコード/原作の変更・実行なし。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-0540-REGEN-SENTINEL-AUX-GATE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_0540_REGEN_SENTINEL_AUX_GATE.md`, actual SHA256 `C6E5F8007633D1238DD78DE7729639E972F4BCC1F33A9ECC0D38FC97DF4CF90B`, 4502 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [SOURCE] approved rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（2026-10-15 05:39 JST Local Get-FileHash一致）。既存B-owned read-only exe/T012_STR_AFTERDEATH_PROBE.txt 0x5783BB..0x5785C0、exe/T012_STATUS_FUNCTION_ENTRY.txt 0x57DFFB..0x57E04D、REA ND-LETHAL/20261015-0345/0435を照合。
  - [ENTRY GUARD] 0x5783BB: Unit+0x1867C!=0は0x578B3Aへ早期分岐し、以下のHP/補助カウンタ変更は未実行。通常Unit vptr=0x63A9E4でvirtual+0x70=0x578370という保存済み対応を前提とし、他種別へ一般化しない。
  - [SENTINEL VS ORDINARY] 0x5783D7 cmp amount,0xF4241（1,000,001）。一致時0x5783E6は[Unit+0x1E568]=0、非一致時0x5783DEは[Unit+0x1E568]-=amount（signed32 wrap）。両経路は0x5783F0の[Unit+0x90]-=amountに合流し、0x5783F6..FDで符号付き結果<=0なら0x5785A3へ。
  - [NEW CONDITIONAL LINK] 0x5785A3は現時点の[Unit+0x1E568]を再読、0x5785A9 TEST→0x5785AB JNSで非負なら0x5785C0へ。負なら0x5785AD PUSH Unit→0x5785AE CALL 0x4E1950→0x5785B6 [Unit+0x1E568]=0→0x5785C0へ。したがって正常なsentinel経路は当該helperを呼ばないが、通常amountの致死枝では補助値が負ならcallされる。0x4E1950の副作用・例外・正常帰還は未確定。
  - [INTERPRETATION] 自然HP負値→0x57E04Dでsentinel dispatchという既知接続と、致死tailの既知『条件付き4E1950』を結び、単なる死亡実装では取りこぼす2種類の処理パスを分離。正味HPも補助値もsigned32であり、補助値の符号は他writerやwrapに依存する。自然HP<0が合法にこのvirtualまで到達すること自体はVERIFY。
  - [SAVED Ghidra IDs] 0x57DF90 5方法: info ev_0c8f9a4e1bd5870aaf62a2605bdd65c8b51600c87ee44869d6596b1b7f16f938, pseudo ev_5a3e17e1d68d81c9aa62213f2e77e5ca9d1c90c4e1fda186678a72e6a88684ce, assembly ev_e50e0ad44fe14809a8e00c7e3754f2816f095b4d9686c6ba0d876d5ee0a337a1, callers ev_43c77a49fb73c68c10f047d7febdc2dfbed7b901365ef01e249b11bcff311fee, callees ev_e48cd61ab643e7cc8fb3ebe1a77fe3e379412db5f98273b0df7a59121d93a8e4; bounds 0x57DF90..0x57E173。0x578370について今回新5方法取得なし。
- **Limitations/corrections:** - [OWNER/REQUEST/CLASS] 独立REA / WRQ-20261013-REA-DEATH / T012 primary・T013/T010参照。新規Ghidraなし、既保存native命令の条件付きJOIN。STATIC-DERIVED、helper意味・実行到達・正常returnはVERIFY。新たな原作バグ／Work確定バグ扱い禁止。 / - [INTERPRETATION] 自然HP負値→0x57E04Dでsentinel dispatchという既知接続と、致死tailの既知『条件付き4E1950』を結び、単なる死亡実装では取りこぼす2種類の処理パスを分離。正味HPも補助値もsigned32であり、補助値の符号は他writerやwrapに依存する。自然HP<0が合法にこのvirtualまで到達すること自体はVERIFY。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-0732-AUX-TIMER-STICKY-ZERO-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_0732_AUX_TIMER_STICKY_ZERO.md`, actual SHA256 `D4D3BB051598E5CB2511064C35C9AABC63244327A682522C4DA90A07393AC32D`, 4435 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [OWNER/CLASS] 独立REA / WRQ-20261013-REA-DEATH / T012主体、T010/T013参照。保存済みx86とB owner T011§25、新Work codeのread-only独立照合。新Ghidra0、旧原作実機0。STATIC-DERIVED、0x4E1950のcallee意味/実到達/returnはVERIFY。
  - [SAVED SOURCE] exe/T012_STATUS_CORE_DUMP.txt 0x57AAF6(ESI=EBP),0x57AAF8(call57E180),0x57E180..57E1C3; exe/T012_KNOCK_CORE_DUMP.txtの同一caller。B所有data/T011_DATA_MODEL.md §25はctor0x571852/setup0x5708F8で+1E564を0初期化すると既に記録（他owner成果は再計上なし）。
  - [EXACT TIMER] 57E181 load [ESI+1E564]; >0なら57E18B dec→57E18C store。再読して>0なら57E1C2 ret。<=0なら57E19B [ESI+1E568]をtestし、ゼロなら57E1C2 ret。ゼロ枝では+1E564と+1E568に追加store無し。負timerも0へ正規化されない。
  - [NEW CROSS-CONDITION] timer=0/負値、aux=0のtickは再装填せずtimerが期限切れのまま残る。合法writerが後のtickまでにaux!=0とすれば、そのtickで直ちにcall条件に入る（50tickの新規待機を必須としない）。初期timer=0はB-owner保存知見だが、aux writerの合法時刻はVERIFY。
  - [TWO-CALLER POSTRETURN DISTINCTION] 致死caller 0x5785A3..5785C0はaux負時にPUSH EBX/CALL4E1950/ADD ESP4の後aux=0のみ、局所+1E564=0x32再装填なし。周期callerはaux=0とtimer=50の両方をpostreturnする。二つの呼出元の共通calleeを理由にtimer resetを一律適用しない。下流他writerは未確認。
  - [EVIDENCE] 新規Ghidra5方法 evidence ID=0、source SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。保存済み57DF90証拠ev_0c8f9a4e/ev_5a3e17e1/ev_e50e0ad4/ev_43c77a49/ev_e48cd61aは関連だが57E180や4E1950自体を今回VERIFIEDへ昇格しない。
- **Limitations/corrections:** - [TEST DESIGN NOT RUN] timer=-2/0/1/2、aux=-1/0/+1、engine active/disabledとUnit death flagで次tick caller arrival・4E1950呼出有無・postreturn aux/timerを区別。return値利用は呼出元に局所AL判定なしだがcallee正常帰還未証明。旧EXE golden PASS0、strict MATCH0、原作バグ認定0。 / - [FOLLOWUP-SAVED-RESULTS-SCOPE] 同Local Compactのread-only検索でrea_lab/results内のファイル名にliteral「4E1950」を含む保存成果は0件。さらにrea_lab/decomp_task・exe・evidence内のcontent検索で当該VAは確認した2 callsiteとREA文書の参照のみ。これは限定した検索範囲の記録であり、関数本体が原本に存在しない、または他の保存形式にも無いという証明ではない。未承認の新規逆解析は実行せずVERIFY維持。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-0940-UNIT-TICK-CALLBACK-ORDER-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_0940_UNIT_TICK_CALLBACK_ORDER.md`, actual SHA256 `A4D51B8F166620287879EF3FA4FA81DB20CB741DDF1FD0A703C069749659FC88`, 4690 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [NATIVE PRIMARY] read-only `exe/T012_STATUS_CORE_DUMP.txt` 0x57AA00..0x57AAFD, 0x57B30D..0x57B375, 0x57E180..0x57E1C3。承認済みEXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。新規binary読取・逆コンパイルなし。
  - [FRESH-ENTRY GATES] 0x57AA11でUnit+0x1867C!=0なら0x57B36Eへret。生存時0x57AA1DがUnit+0x1E0を読み、0x57AA23でengine+0x1EEC44を0と比較。0x57AA29のJNEで0x57AA86へ進む側だけが0x57AAF8へ流れ得る。zero側は0x57AA2B..0x57AA85の早期経路（正常終了/早期退避）であり、この入口経由の57E180 timer callは実行されない。
  - [BEFORE-CALL WRITES] active側0x57AACDにUnit+0xA8を読み、0x57AAD3で+0x1E52Cへ加算、0x57AAD9で+0x1E530へ加算、0x57AADFで+0x1E534をincrement。0x57AAF1 `CALL 0x4DFA30`の正常帰還後0x57AAF6 ESI=Unit、0x57AAF8 `CALL 0x57E180`。この時点で上述counterはすでに変更され得る。
  - [TIMER CALLEE] 0x57E181..0x57E1A3はtimer+0x1E564を正なら1減じ、結果<=0かつaux+0x1E568!=0なら0x57E1A6 `CALL 0x4E1950`。正常帰還後0x57E1AE aux=0、0x57E1B8 timer=50。aux=0なら呼出・再装填なし。これは前回REA-20261015-0732の確定済み局所証拠。
  - [NEW PC CONTRACT] 0x57AAF8のcallee正常帰還後に実行する次PCは**0x57AAFD**（Unit+0x1E55Cの読取）。0x57AA00へ再入して続行済みと扱うと、0x57AAD3/0x57AAD9/0x57AADF等の実行済みcounter更新を重複させ得る。4E1950から正常帰還するか、PCを保持できるかはVERIFY。既存Workのdeferred ValueErrorを虚偽の成功復帰へ置換しない。
  - [PHASE ORDER] 同じ0x57AA00の後段0x57B345のAL条件付57B34Bおよび0x57B369の自然更新CALL 0x57DF90は、57AAF8より後に置かれている。両処理を通過する合法経路では57E180周期callback判定→自然更新の順。ただし全経路で両者到達するとは示していない。別のaux writerがどの時点で呼ばれるかは未確定。
  - [TEST CONTRACT / NOT RUN] 同Unit identityでdisabled0/1×engine byte0/非0×timer1/0/-1×aux0/非0を固定。counter(+1E52C,+1E530,+1E534)、呼出0x4E1950の有無、正常return PC=57AAFD、翌tick、Task解除・再入を区別。callback nonreturn時にcaller後段を成功扱いしない。旧実機golden PASS0／strict MATCH0。
  - [EVIDENCE / CLASS] 今回新規Ghidra5方法evidence ID0。既存57DF90 info=ev_0c8f9a4e、pseudo=ev_5a3e17e1、assembly=ev_e50e0ad4、callers=ev_43c77a49、callees=ev_e48cd61a（保存run20261009T223622536Z）。0x57AA00/57E180/4E1950は今回5方法VERIFIEDへ新昇格させない。
- **Limitations/corrections:** - [PHASE ORDER] 同じ0x57AA00の後段0x57B345のAL条件付57B34Bおよび0x57B369の自然更新CALL 0x57DF90は、57AAF8より後に置かれている。両処理を通過する合法経路では57E180周期callback判定→自然更新の順。ただし全経路で両者到達するとは示していない。別のaux writerがどの時点で呼ばれるかは未確定。 / - [NEXT / SCOPE] 次は保存済の他の4E1950 callsiteと57AAFD以降のTask callback寿命を同一フレームの条件で照合し、実正常帰還はVERIFY。原本/MASTER/T018/A～E/Work製品・共有WRQ/Git/push/MCP/automation不変更。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-1040-TICK-POSTCALL-TIMER-ORDER-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_1040_TICK_POSTCALL_TIMER_ORDER.md`, actual SHA256 `86F92CB8565E33DF7F870F0FC395A0BDEEB1008A2BB47690052E7183C5A2964B`, 4382 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [ENTRY/RETURN] 0x57AAF8 CALL 0x57E180、正常帰還後の次PCは0x57AAFD。4E1950の副作用・正常帰還は別VERIFY。0x57AA00へrestartすると事前の+1E52C/+1E530/+1E534等を重複更新し得る（前回確認事項を再計上しない）。
  - [NEW ORDER A] 0x57AAFD..57AB08: Unit+1E55Cは>0時だけdecrement。次に0x57AB0E..57AB22: Unit+1E4F8は>0時だけdecrement、ちょうど0になった時だけ0x57AB22 CALL 0x57B380（stack PUSH Unit）。0以下で開始した場合はこのcallを起こさない。
  - [NEW ORDER B] 0x57AB27..57AB32: Unit+1E518は>0ならdecrement。次に0x57AB38..57AB68: Unit+185F4が>0ならdecrement、ちょうど0になった時に、Unit+1867C==0かつUnit+8C==0であれば0x57AB5D LEA Unit+6CC→0x57AB63 CALL 0x41E160。正常帰還した場合だけ0x57AB68でUnit+185F4=0を再storeする。
  - [CALLER DISTINCTION] 0x41E160はND-DETACH既存契約ではowner子window recordの最初の一致をinactive化・末尾交換し、条件付きwindow cleanup 4C5CC0へ進む。今回のtick caller 0x57AB63の戻り先は0x57AB68であり、死亡graph側の同helperを含む他callerのPCと混同しない。4C5CC0などの正常帰還は依然VERIFY。
  - [AFTER WINDOW] 0x57AB72でUnit+238を検査、非0時は0x57AB81/0x57AB8Cで2回CALL 0x5A8040。0x57AB91で+186D4特殊値0x80000008を比較し、異なれば+53C increment→0x5795E0→返AL非0時0x57B36E早期復帰。関連calleeの意味/returnは未解明。
  - [NEW PARTIAL-ORDER CONTRACT] 同tickに+1E4F8=1かつ+185F4=1の場合、57B380が必ず41E160より前のcallsite（ただし前段57E180正常帰還・合法継続・57B380正常帰還が条件）。57B380途中中断時は+1E518/+185F4を実行済み扱いしない。41E160途中中断なら57AB68以降を実行済み扱いしない。resumeは各calleeの本当のreturn PCから行い、57AA00再入で二重処理しない。
- **Limitations/corrections:** - [NEW PARTIAL-ORDER CONTRACT] 同tickに+1E4F8=1かつ+185F4=1の場合、57B380が必ず41E160より前のcallsite（ただし前段57E180正常帰還・合法継続・57B380正常帰還が条件）。57B380途中中断時は+1E518/+185F4を実行済み扱いしない。41E160途中中断なら57AB68以降を実行済み扱いしない。resumeは各calleeの本当のreturn PCから行い、57AA00再入で二重処理しない。 / - [WORK READ-ONLY] advance_unit_tickは4 timerの順序を持ち、57B380をValueError('57B380 expiry callback VERIFY')で停止、41E160の未完了はwindow_registry.pending/next_vaを保持する既存design。前者はstaged deepcopy未commitのため原作部分commitを厳密再現した証拠ではない。完成・バグ断定ではなく未実装境界の追跡条件。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-1140-TICK-EXPIRY-XREF-CONTRACT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_1140_TICK_EXPIRY_XREF_CONTRACT.md`, actual SHA256 `10FCF6F0ADF8CE3A97EE8031B4CB542A00B718F6230561F497E4C6D8D8843975`, 4397 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - [CALLSITE] exe/T012_ACTION_KNOCK_ORDER.txt lines 845前後と exe/T012_STATUS_CORE_DUMP.txt の0x57AB14..0x57AB27を照合。Unit+0x1E4F8が正で1減じた結果が0になったときのみ 0x57AB21 PUSH EBP → 0x57AB22 CALL 0x57B380。正常帰還した場合の再開位置は 0x57AB27（Unit+0x1E518更新）であり、次の+0x185F4 window処理より前。
  - [XREF-RNG] 保存run 20261009T194358486Z / 40ED80_procedure_callers.json: Ghidra12.1.4 が 0x57B380 を 0x40ED80 のresolved callers 37件の1件として報告。evidence_id=ev_fcaab3749388b92aabc79016efbbda7d48d5fb29ace7cc6bfc5d46d2dca4f6f3。0x40ED80は既存T031の乱数範囲選択helper（既存VERIFIED）。
  - [XREF-ATTR] 保存run 20261009T203528568Z / 4C1200_procedure_callers.json: 同じ 0x57B380 を 0x4C1200 のresolved callers 92件の1件として報告。evidence_id=ev_00c4f526dbb29cda9775fdebaca5010097da35a3f9661301d7a393ff98efe6b9。0x4C1200は既存T012の属性/耐性キー探索helper（既存VERIFIED）。両runのsubject source SHAは上記と一致。
  - [NEW RECONCILIATION] タイマー0到達だけで単純なtimer resetとは限らず、0x57B380 body内には乱数range helper・属性探索helperへの解決済み参照がある。したがって同tickの副作用評価/RNG位置は0x57B380完了境界より後へ勝手に進めない。ただし各helperを必ず呼ぶという証拠ではない。
  - [BODY LIMIT] 現在確認した保存済みT012_ACTION_KNOCK_ORDER.txtの0x57B380本文は0x57B380..0x57B39Fの不完全prefix（途中.byte解釈あり）。57B380自身のinfo/pseudo/assembly/callers/callees5方法、確実な関数境界、両helperの命令VA/分岐条件/呼出順/返値、実call/return、RNG消費・耐性実意味はすべてVERIFY。今回0x57B380をVERIFIEDへ昇格しない。
  - [POSTCALL CONTRACT] 呼出0x57AB22中に停止した場合+0x1E518・+0x185F4は未実施扱い、ただし0x57AB19のtimer減算は既に実施済み。Unit更新入口0x57AA00へ巻き戻した成功扱いは禁止。実帰還確認までは57AB27を予定return PCとしてのみ保持。
  - [GOLDEN/NOT RUN] Unit+1E4F8を1/2/0、+1E518と+185F4を1/0、同Unit identity・同SAVE/seedでold/newのcallback発火/行動/HP/RNG可視結果を分ける。内部乱数消費や0x4C1200は合法旧観測で証明できなければINELIGIBLE。旧EXE実機golden PASS0、strict MATCH0。
- **Limitations/corrections:** - [BODY LIMIT] 現在確認した保存済みT012_ACTION_KNOCK_ORDER.txtの0x57B380本文は0x57B380..0x57B39Fの不完全prefix（途中.byte解釈あり）。57B380自身のinfo/pseudo/assembly/callers/callees5方法、確実な関数境界、両helperの命令VA/分岐条件/呼出順/返値、実call/return、RNG消費・耐性実意味はすべてVERIFY。今回0x57B380をVERIFIEDへ昇格しない。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

### REA-20261015-1238-TICK-EXPIRY-EARLY-RETURN-GATES-01

- **Owner source:** `rea_lab/decomp_task/REA_20261015_1238_TICK_EXPIRY_EARLY_RETURN_GATES.md`, actual SHA256 `43BF0C3229C6DD695B5618B0FBAD3C9C13B7093F251DD71D6C6D31D7CC9C7BA5`, 3985 bytes.
- **Record category:** RESEARCH_QC; prior error/status evidence is not a formal new result.
- **Saved historical static proof and scope:**
  - # REA-20261015-1238-TICK-EXPIRY-EARLY-RETURN-GATES-01｜0x57B380保存済み早期returnゲート
  - [SOURCE] 保存済x86 exe/T013_1D0_GLOBAL_PROBE.txt lines4802-4829（VA 57B3AD..57B42A）、exe/T012_STATUS_CORE_DUMP.txt lines1207-1215（VA 57B834..57B864）、exe/T012_ACTION_KNOCK_ORDER.txt（VA 57AB19..57AB27）。他レーン原本はread-only。
- **Limitations/corrections:** - [NEXT/TEST] 保存済みB42A..B800中間欠落、57B83Dへ至らないbranch、helper内部副作用と正常returnを優先。実機goldenは合法Unit+1E4F8=1の条件で+1867Eの0/非0、+D0/+C0 signed負/非負、parent有無を同一SAVE/seed・可視範囲だけ分ける。旧原作実機PASS0、新旧strict MATCH0。 / - [COUNTS] 保存21run＋progress_sync_20261011T153958076ZでW1-5合計64/64 VERIFIED（W5=16/16）、今回増0、P0=29/29、P1=35/35。W6正式0/16・候補P0=5/P1=11、正式未着手16・候補既往拒否4/未試行12・結果VERIFY0。MASTER最新cp151、研究DONE9/34・IN_PROGRESS21/VERIFY4。ゲーム再実装率は測定していない。
- **Classification:** SOURCE_PUBLISHED_INTAKE/STATIC or historical QC, VERIFY, NOT CURATED; original-game Golden PASS=0, READY=0. Historical safety refusal mentioned; denied content/results not copied or retried.

## KB curator required

Do not promote prior native observations to new VERIFIED without original instruction/VA, target SHA, five-evidence gate, and correction review. Some old studies concern Work interface constraints, which are not original-game behavior proof; some are merely preflight/status/QC. Preserve source chronology; link exact duplicate ideas instead of counting the same function multiple times. Only curated owner may modify develop REF/symbols; blocked targets and refused data are not acquired here.
