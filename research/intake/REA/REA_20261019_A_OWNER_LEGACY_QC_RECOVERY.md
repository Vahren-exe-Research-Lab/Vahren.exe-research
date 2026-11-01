# REA owner 2026-10-19 historical source recovery (A)

Private owner intake only; no formal CURATED/READY. 7 old research and independent QA IDs, byte SHA256 of each original owner Markdown remeasured read-only on research PC 2026-11-02 JST. Substantive excerpts of saved ASM/ABI/branch logic are below, with older unsafe/denied evidence and path-specific private metadata omitted. Current original EXE/V9 and formal five-method evidence were not newly acquired; legacy Wave1–5 64/64 never counted again; original Golden PASS0, READY0. Owner source itself is PC-only and can be recovered via relative filename/SHA.

### REA-20261019-0133-TROOP-CALLFRAME-METADATA-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_0133_TROOP_CALLFRAME_METADATA_QC.md`; actual SHA256 `260E6979A877E4829C0DFDCE21E30095D20FFFCFE01647B31BBD4F9F4962B594`, 5025 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [NATIVE PARENT CALLS] 死亡側0x575F6C CALL0x5684B0→戻り0x575F71、および0x575F8C CALL0x5684B0→戻り0x575F91。前者帰還後Unit+1867D再読によって後者実行を判断するため両callの継続元は同一ではない。
  - [BRANCH ONE] selectedかつ剪定後非空: codeはui(0x56853B,0x568540,callee=0x41F850)を生成。nativeは0x41F850へarg1=1を渡すが、このTroopUpdateTrace型は引数の保存欄を持たない。選択解除0x527ED0内部のTroopSelectionTraceではcallee_stack=(1,)を別に保持しており粒度が不統一。
  - [BRANCH TWO] normal・live_count>0・先頭controlled: codeはui(0x5685C5,None,callee=0x527EA0,tail=True)を返し、return_pc=None。これは正当なtail-callの内部帰還先が無いという記録であり、外側0x5684B0呼出元へ戻るPCが不要という意味ではない。
  - [OTHER BRANCHES] selected emptyの0x56852D→0x527ED0→0x568532、normal empty controlledの0x5685F8→0x527ED0→0x5685FDも内部return_pcのみで外側死亡callerの帰還先を表さない。TroopSelectionTrace.parent_return_pcは0x568532/0x5685FDであり0x575F71/0x575F91とは別階層。
  - [ACCEPTANCE DESIGN/NOT RUN] 発火元0x575F6Cと0x575F8Cを別fixtureにし、caller VA/outer returnPC、Troop pointer、branch nextVA、callee VA、callee stack、inner returnPC、tail_call、callee returned、outer returned、selection binding generationを段階別に保持。未確認returnを正常値に偽装しない。
- **Unresolved/corrections:** - [SESSION CHECK] native_battle_session.pyのupdate_resolved_troopはACTIVE限定でtraceのみ保存し、continue_resolved_troop_selectionはVERIFY_TROOP_UPDATE→VERIFY_TROOP_SELECTIONへ遷移する。両APIは死亡呼出元のPCやcall generationを引数・戻り値に含めない。native_battle_runner.pyのtroop_selection_resolvedはpending UIでbreakする。 / - [RESEARCH/GOLDEN] MASTER直読最新checkpoint187、研究DONE9/34・IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-0230-CP187-W1-STALE-REPEAT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_0230_CP187_W1_STALE_COUNT_RECONCILIATION_QC.md`; actual SHA256 `540F567B1003D211EF54333614F3910C1B9F9A5EE3A0AA9521DC5D497030EA20`, 3615 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [PRIMARY FUNCTION] runs/20261009T213635897Z/RUN_RESULT.json は0x479A30(T031 shuffle)をVERIFIED、完走true、関数入口0x479a30・278bytes・body inclusive 0x479a30..0x479b45、source/end SHAともE8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187と記録。
- **Unresolved/corrections:** - [E-HANDOFF/NOT READY] cp187の『REA初期16候補STATIC15/TODO1』は歴史的PROGRESS snapshotとしてのみ有効。現行正式Wave1は16/16。E担当が自分の許可されたMASTER監査で古い値を訂正・引用根拠を更新することが再開条件。本REAからE/MASTERへ直接書かず、受領・統合済みとは宣言しない。T031の同関数を再取得・再コミットしない。 / - [RESEARCH/GOLDEN] 最新MASTER cp187、34 Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE gameplay golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。64/64は選択関数だけの静的証拠。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-0335-DEATH-TROOP-SEMANTIC-RESUME-DRIFT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_0335_DEATH_TROOP_SEMANTIC_RESUME_DRIFT_QC.md`; actual SHA256 `02A53F6A14FD72FC9C5891D1625E34F946A211AD037EFE38CDBC6B62D6850C1A`, 5128 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [SOURCE] 保存済み原作静的契約REA-ND-20261013-001 / SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md。最新保存run20261011T153309850Z・sync20261011T153958076Z、source SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回は対象EXE再SHAなし。
  - [NEW BINDING CONTINUATION] native_battle_session.py continue_resolved_troop_selectionは、前回binding.trace.complete=trueの場合に同じlive storageからfresh TroopSelectionCleanupを構築し、二度目の正規選択解除を受け付ける。未完了bindingは再使用しない。従来の「二度目のbinding交換経路なし」は現在のコードへ適用不可。
  - [NEW UI SEMANTIC] continue_semantic_troop_uiは選択中非空0x56853B→0x41F850/0x568540と、通常非空tail0x5685C5→0x527EA0を別条件で完了扱いにし、troop_ui_revisionを進める。描画の完全なnative return receiptではなく新エンジンの意味的再描画通知。
  - [NEW POSTSELECTION MODE2] continue_semantic_troop_selection_uiは0x56852D→0x527ED0→0x568532と0x5685F8→0x527ED0→0x5685FDを区別し、後者では選択解除後にengine+0x1EF140を再読、mode==2時にTaskRegistry.unregister(pointer,defer_delete=False)。旧『後段Task解除なし』は現コードでは解消候補。ただし合法動的到達・Task副作用・実機一致は未検証。
  - [NEW OUTER DEATH GRAPH] continue_resolved_normal_disable_troopsは0x575F62/0x575F6C/0x575F71/0x575F8Cを状態として保持し、第1所属部隊NULLのとき0x575F71を経由、第1帰還後にUnit+0x1867Dを再読して選択owner+0x358の第2部隊更新を判断する。同一pointerでも別callsiteとして扱い、graph.completed_troopsに別々に記録する。
  - [RETURN-PC SCOPE] pending第1、第2callのgraph.return_pcはそれぞれ0x575F71・0x575F91。TroopUpdateTrace型には依然outer_return_pc/callee_stack欄がないが、親Graph側にouter originが存在するため『全体で復帰先情報なし』という旧解釈は過剰。第2完了時はframe.next_va=0x575C54へ移り、0x575F91を独立した完了段としては露出しない。
  - [NEW RUNNER ACTIONS] native_battle_runner.pyはtroop_ui_semantic、troop_selection_ui_semantic、normal_disable_troops_resolved、normal_disable_complete_resolvedを公開済み。以前のrunnerがselection時breakのみという観察は現行版で失効。
  - [NOT A GOLDEN / OPEN] 新UIは明示的にGDI/vertex native表示を再演算しないsemantic host notification。原作0x41F850/0x56BA80/0x401BE0の実画面、通常死亡0x575A60上位へ全帰還、合法同一pointer/NULL初回到達、exception時副作用、旧新同条件fixtureはVERIFY。コード静的照合であって旧原作BUG解消・実機strict互換合格とは宣言しない。
  - [EVIDENCE STATUS] 今回Ghidra新規info/pseudo/assembly/callers/calleesのEvidence IDは各0件、新関数STATIC VERIFIED+0。以前のREA-ND-20261013-001を再利用し、既存旧メモは歴史的snapshotとして保全。
- **Unresolved/corrections:** - [NOT A GOLDEN / OPEN] 新UIは明示的にGDI/vertex native表示を再演算しないsemantic host notification。原作0x41F850/0x56BA80/0x401BE0の実画面、通常死亡0x575A60上位へ全帰還、合法同一pointer/NULL初回到達、exception時副作用、旧新同条件fixtureはVERIFY。コード静的照合であって旧原作BUG解消・実機strict互換合格とは宣言しない。 / - [RESEARCH/GOLDEN] 今回読取MASTER checkpoint187、DONE9/34、IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-0535-T014-PARENT-IO-COMMIT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_0535_T014_PARENT_IO_COMMIT_GATE_QC.md`; actual SHA256 `AE238201FAE1F265DF761A75AA6C5A1EB5F9CE405D6BF0BD907DBCEDA4979DDD`, 4082 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [SOURCE] runs/20261011T144115307Z/470700_procedure_assembly.json ID ev_f7ed3af4df1cdf7b14d9208f3d4aa735267b9ab022ee7d6b3860c4521bbb95cf、pseudo ID ev_fa4f2750e44895495089baaea76f6c2e6b39e1ec155c9b68af4b63bc17ac8e07、info ID ev_e676039e3083db867c85605ee376898d307e4a18d8f264c9c6f5003be1deb31e、callees ID ev_3f9a89a60c30eee71f662be8ef197b9016cfe610caae887926287dcb5d131286。
  - [STATIC INPUT ABI] 0x470709..0x470713は順にPUSH 0、PUSH 4、PUSH 0xB060F0、PUSH ESI、CALL 0x42E700。Ghidra pseudoのFUN_0042e700()に引数が表示されないことを根拠に0引数と判定してはならない。calleeの実RET時スタック清掃、各引数の意味、部分読取副作用は未取得でVERIFY。
  - [COMMIT ORDER] 0x470718..0x470732はcallee後のstream state参照とbits判定。異常なら0x470734へ分岐してLoadException生成/throwへ進む。正常枝0x470754からだけglobal DWORD [0xB060F0]をロードし、0x47075A..0x47075Dで呼出元の出力pointer [EBP+8]へ格納する。0x42E700戻り値を直接成功判定として用いる命令はこの親範囲に見えない。
  - [BOUNDARY] 異常フラグ後の親関数による出力pointer書込は到達しない。ただし呼出元pointerの別経路mutationや0x42E700内部の状態変化・例外以外の失敗方針を一般化しない。0x470700 infoはentry0x470700/body0x470700..0x470762/99byte、既存VERIFIEDの親のみ。
  - [TOKEN CROSSCHECK] 同じ保存runの0x4705F0はCALL 0x470980の戻値-1を一時bufferへの非書込とし、同じstream-state bits検査後に文字/NUL等を評価する。既存REA_T014_SAVE_TOKEN_SIGNED_BYTE_LENGTH_AUDIT_20261012_0637の許容byte0x20..0x7F/上限255/EOF不明を再採用し、新しい事実として二重計上しない。今回の増分はscalar親0x470700の引数push・出力commit順との対比。
- **Unresolved/corrections:** - [ACCEPTANCE/DESIGNED_NOT_RUN] T014 owner向け受入条件: scalar正常4byte時の出力書込、stream異常フラグ時の親出力未commit、短読込と誤サイズ、token EOS/文字異常を別fixtureにする。stream bitの厳密論理名、callee RET清掃、short readでflagが立つかはVERIFY。ゲーム実機Goldenではない。 / - [MASTER/SAFETY] MASTER最新checkpoint188：DONE9/34、IN_PROGRESS21、VERIFY4。旧EXE gameplay golden PASS0、strict MATCH0、ゲーム再実装率は測定していない。PC CPU/RAM/Java/lock/現在SHA未測定（既往拒否preflightの別tool/shell/path迂回なし）。重いrun/sync0秒、軽量総時間未計測。単一MCP、最大4関数、Ghidra900000ms/request960000ms。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-06H-T014-POWER-TAG-READER-DUALPATH-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_06H_T014_POWER_TAG_DIRECT_VS_WRAPPER_READ_QC.md`; actual SHA256 `AE7256857E3DCAEA709A3B87434CE64E2B6466785AC73CDF08E1D13B26F004E0`, 4425 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [PARENT VERIFIED] VA0x5964C0（Power runtime reader/T014）は保存RUN_RESULTで5/5 VERIFIED。info ev_105b1c184be5d868744bee92f4d32362e03bb147780923add1925cff2553acea、pseudo ev_9608d350a99e5ba1453392474e951d01a83321124085c78de8ef29ffc8ea96d9、assembly ev_225abdeab1240aef12bae0642c86e2bc6494b630fee961f55233f5c29cbb5e25。
  - [PARENT XREFS] callers ev_24c083a492c9b10125bdeecdfbc3db2f2d263a8cd19efd9d17513b9bc771efef、callees ev_ff3bf40913871207a524bdcdc61a67694df2d6300e9bcae944c544e93caf631d。Ghidra body ranges=0x5964C0..0x596656と0x596660..0x596A99、total1489bytes/non-contiguous。全spanを関数本文と誤認しない。
  - [DIRECT FOUR-BYTE TAG A] 保存assembly 0x59679C..0x5967A6はPUSH 0/PUSH 4/PUSH 0xB060F0/PUSH EBX→CALL0x42E700。0x5967AB..0x5967C5のstream状態bit検査を通過して初めて0x5967CB..0x5967D5でPower+0xD0へscratch DWORDをcommit。失敗は0x596A5AのLoadException経路。
  - [DIRECT FOUR-BYTE TAG B] 同型0x596822..0x59682C CALL0x42E700→0x596831..0x59684B状態検査→正常0x596851..0x59685BでPower+0xD4にcommit。失敗は0x596A7AのLoadException経路。両CALLのGhidra pseudo表記FUN_0042e700()の0引数表示をx86 ABI確定としない。
  - [WRAPPER TAG C/D] tag別0x5968A8..0x5968B4はPower+0xD8をPUSHしCALL0x470700、0x596902..0x596914はPower+0xDCをPUSHしCALL0x470700。wrapperは保存済み別VERIFIED 0x470700の内側0x42E700および例外後commitを経る。4枝全てを一律の直接CALLで実装しない。
  - [DISCRIMINATOR] 各枝は保存assemblyの0x402C40比較とタグ長条件（順に7/9/8/10）に由来。参照static string候補0x626A84/0x626A8C/0x626A98/0x626AA4のraw bytes・human-readable field名は本回未確認のため命名VERIFY。0x596997にも別の0x470700呼出があり、数値読取をこの4枝だけと一般化しない。
  - [BARRIER] 保存疑似CとASMの一致は読取ルート/出力先/stream状態検査に限定。0x42E700のcallee関数入口・RETスタック清掃・short read時の部分更新・タグ実意味・例外後外側状態・合法旧実機到達はTODO/VERIFY。LoadException以前にcalleeがscratchを変更した可能性を否定しない。
- **Unresolved/corrections:** - [BARRIER] 保存疑似CとASMの一致は読取ルート/出力先/stream状態検査に限定。0x42E700のcallee関数入口・RETスタック清掃・short read時の部分更新・タグ実意味・例外後外側状態・合法旧実機到達はTODO/VERIFY。LoadException以前にcalleeがscratchを変更した可能性を否定しない。 / - [MASTER/GOLDEN] MASTER直読最新checkpoint189、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。QUEUE/PROGRESSは保存syncのSTALE_RENAME_DENIEDで旧表示。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-0738-T014-POWER-GENERIC-NUMERIC-DC-SENTINEL-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_0738_T014_POWER_GENERIC_NUMERIC_DC_SENTINEL_QC.md`; actual SHA256 `AFD076998A45D968B604509111E1A7B91892FF11B88E5E29F16EE44F0AB05971`, 4586 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [SOURCE] runs/20261011T133432356Z/5964C0_procedure_assembly.json（ev_225abdeab1240aef12bae0642c86e2bc6494b630fee961f55233f5c29cbb5e25）およびprocedure_pseudo_code.json（ev_9608d350a99e5ba1453392474e951d01a83321124085c78de8ef29ffc8ea96d9）。既VERIFIED info ev_105b1c184be5d868744bee92f4d32362e03bb147780923add1925cff2553acea、callers ev_24c083a492c9b10125bdeecdfbc3db2f2d263a8cd19efd9d17513b9bc771efef、callees ev_ff3bf40913871207a524bdcdc61a67694df2d6300e9bcae944c544e93caf631d。
  - [PRIOR DEDUP] REA_20261019_06H_T014_POWER_TAG_DIRECT_VS_WRAPPER_READ_QC.mdの4専用タグD0/D4/D8/DCと、REA_20261019_0535_T014_PARENT_IO_COMMIT_GATE_QC.mdの0x470700正常commitは再発見として加算しない。
  - [TREE RESET BEFORE TAG LOOP] 0x5966FE..0x59673FはPower+0xB0の既存tree headerを0x463070へ渡した後、関連header linksを自参照に戻しPower+0xB8へ0を書き、タグループへ進む。0x463070内部の厳密allocator副作用はVERIFY。
  - [ADDITIONAL BRANCH] 0x59691Eはstring候補0x626AB0を0x40B200で判別し、非一致時0x596997へ分岐。そこではCALL0x470700で数値をstack scratchへ読み、0x5969B4 CALL0x436560→0x5969CF CALL0x436680→0x5969DB CALL0x463280（destination ESI=Power+0xB0）へ進む。四つの専用数値タグ以外が一律discardされるわけではない。
  - [TREE DUPLICATE BOUNDARY] 0x463280の既確定generic insert-if-absent契約を流用すると、同じキーとして構築されたentryの再投入は既存キーを残す候補。ただし436560/436680が構築する実key/valueの型・重複時の前処理は未照合。現時点でPower全タグの一律first-winsと断定しない。
  - [DC PRESENCE FLAG] 0x5965A2でlocal byteの0初期値があり、長さ10の専用tag D枝0x59690Fでbyte=1。全タグ読込後0x596A14で同flagを検査し、0の場合だけ0x596A1B..1FでPower+0xDC=0x80000008とする。D枝が実行された場合の値は0x596914 CALL0x470700によって決まり、既定のsentinelで上書きしない。
  - [KEY LIMIT] 比較文字列VA0x626A84/8C/98/A4/B0の生文字列と各Power field名は今回未取得。0x40B200 predicateの比較詳細・任意タグ構文・EOF/短読込・例外後の部分tree状態と重複keyの実到達はVERIFY。
  - [IMPACT] Powerの再実装受入条件に①専用4tag、②0x626AB0の特別string系、③その他数値tagのPower+B0 tree挿入、④D tag不在時だけDC sentinelという4種の処理境界を分離する。未知タグを無条件に捨てたりDCを常に0に初期化しない。実原作save golden/実機比較はNOT RUN。
- **Unresolved/corrections:** - [IMPACT] Powerの再実装受入条件に①専用4tag、②0x626AB0の特別string系、③その他数値tagのPower+B0 tree挿入、④D tag不在時だけDC sentinelという4種の処理境界を分離する。未知タグを無条件に捨てたりDCを常に0に初期化しない。実原作save golden/実機比較はNOT RUN。 / - [MASTER/GOLDEN] 今回読取最新MASTER checkpoint189、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0・strict MATCH0。ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

### REA-20261019-0834-T014-POWER-HOMESPOT-DUAL-END-01

- **Owner source:** `rea_lab/decomp_task/REA_20261019_0834_T014_POWER_HOME_SPOT_DUAL_TERMINATOR_QC.md`; actual SHA256 `1671399C1D6101665023415DE95763A6E26BE77D994147118058891FF0E9FEBD`, 4039 bytes.
- **Source category:** RESEARCH_QC, STATIC/INFERRED/VERIFY; do not count QC as new native function.
- **Previously saved native/ABI evidence:**
  - [SOURCE] runs/20261011T133432356Z/5964C0_procedure_assembly.json ID ev_225abdeab1240aef12bae0642c86e2bc6494b630fee961f55233f5c29cbb5e25、pseudo ID ev_9608d350a99e5ba1453392474e951d01a83321124085c78de8ef29ffc8ea96d9。保存source SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回実ファイル再hashなし）。
  - [LITERAL] 保存済みA所有 exe/T014_ENTITY_MARKERS.txt は0x626AB0='home_spot'、writer側0x626AE8も'home_spot'と記載。0x59691E MOV ECX,0x626AB0→0x596927 CALL0x40B200→0x59692E JZ0x596997により、home_spot一致時だけ文字列vector path、不一致時は従来の一般数値tree pathへ進む。
  - [INNER LIST] 0x596930で文字列scratch(ESP+0x48)初期化、0x59694D CALL0x4705F0で次のnameを読み、0x596955で長さ0なら0x596984へ分岐。非空なら0x59695B..0x596969でPower+0xC0と文字列scratchを準備しCALL0x415530、0x596973..0x596982でheap string処理の後0x596930へ戻る。0x415530の厳密なappend/replace・失敗時副作用は未検証。
  - [FIRST EMPTY TOKEN] home_spot内の空tokenは0x596984へ進み、必要な一時文字列解放後0x5969F9に合流して外側0x4705F0を再び呼ぶ。従ってvector終了はPower全tag領域の終了ではない。
  - [SECOND EMPTY TOKEN / CONTROL FLOW] home_spot内終了後の外側tag再読は0x5969F9..0x596A05。0x596A0C TEST EDI→0x596A0E JNZ0x596756で非空だけ次tag処理へ戻す。2個目が空なら0x596A14のD-tag存在flag判定を経て、flag0で0x596A1BのPower+0xDC sentinel、flag1で0x596A29 cleanupへ。初回tag読取0x596740後に即空の場合だけ0x59674E TEST EDI→0x596750 JZ0x596A1Bと直接sentinelへ進む別経路であり、この2経路を混同しない。
  - [WRITER CROSSCHECK] 既保存REA STATIC_UNIT_SPOT_POWER_WIRE_LAYOUT_20261010.md S-POWER-04はwriter 0x596AA0側のhome_spot vector＋空文字2回を記録。今回reader分岐と突合して、最初の空文字=home_spot要素列終端、次の空文字=Power tag外側終端という局所STATIC対応を追加。先行資料の「2番目のスコープ不明」を限定解消する。
  - [BOUNDARY] home_spot tagの名前自体は保存済みnative文字列一覧とのクロスウォーク。0x40B200 full ABI、0x415530 mutate/allocator、直前の+0xC0状態、短読込/EOF/不正2重終端時の動作はVERIFY。合法実save観測/旧EXE gameplay Goldenは未実施。
  - [NEXT] T014 Power home_spot vector初期状態と0x415530 return/payloadを保存済み証拠から可能な範囲で確認。最優先の死亡T010/T012/T013では0x575F91正常帰還と初回troop NULL+selectedのfixture不足を継続。新しい旧実機golden証拠がない限りPASSにしない。
- **Unresolved/corrections:** - [BOUNDARY] home_spot tagの名前自体は保存済みnative文字列一覧とのクロスウォーク。0x40B200 full ABI、0x415530 mutate/allocator、直前の+0xC0状態、短読込/EOF/不正2重終端時の動作はVERIFY。合法実save観測/旧EXE gameplay Goldenは未実施。 / - [COUNTS] 保存sync 20261011T153958076Z W1 16/16 W2 10/10 W3 10/10 W4 12/12 W5 16/16 = 64/64 STATIC (P0 29/P1 35)。QUEUE/PROGRESSはrename EPERMでSTALE。最新MASTER checkpoint189・研究DONE9/34、IN_PROGRESS21、VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0、再実装率未測定。
- **Status:** PUBLISHED_INTAKE if confirmed readback, or STATUS_ONLY for gate-only record; new formal VERIFIED+0; Golden PASS0; READY0. Prior safety refusals remain BLOCKED; denied content not retrieved.

## Curator review

Same VA, condition or source E8 is not a fresh function each hour. Correlate with REA earlier/later IDs, T013/T014 native/Work fixes and original source SHA before adopting a correct feature into REF/symbol dictionary. No raw original EXE, denied Wave6, original-game SAVE or unrelated owner workspace changed. Current develop belongs exclusively to KB curator.
