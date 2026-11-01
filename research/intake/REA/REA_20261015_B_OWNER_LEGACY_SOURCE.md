# Historical REA 20261015 owner source B

REA owner PRIVATE research intake only; old source IDs and source SHA were independently rehashed 2026-11-02 JST. This is preservation, not 9 newly REA-verified functions. Prior safe ASM/CALL observations are recorded from original owner text; refused VA/operations/results are not copied or retried. A status-only entry is retained as historical audit metadata rather than new research. Five-method new VERIFIED=0, original game Golden PASS=0, READY=0. Current V9/PE SHA and native tests were not freshly rerun in this intake.

### REA-20261015-1340-TICK-EXPIRY-MAP-INSERT-XREF-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_1340_TICK_EXPIRY_MAP_INSERT_XREF.md`; actual SHA256 `38BBECE74914BA3CA8C689CA889B009B9B496BB2A13001B2F099355706E724AB`; 3209 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - # REA-20261015-1340-TICK-EXPIRY-MAP-INSERT-XREF-01｜0x57B380保存済み中間呼出の照合
  - [SOURCE] 保存済みexe/T005_REGISTRY_INSERT_CALLERS.txt 8130-8178行、exe/T012_STATUS_CORE_DUMP.txt 1175-1215行、data/T005_FORMAL_GRAMMAR.md 143-148行。すべてread-only。
  - [GHIDRA] 0x463280 callers evidence ev_cd55b9172146b1b73b06b54bbd571550221ca05419457de972262d896ecbf0b0（run 20261009T215200079Z、source SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187）は呼出元0x57b380を明示。
  - [DIRECT CALLS] 保存済み原作命令: 0x57B559 CALL 0x463280 / 0x57B779 CALL 0x463280 / 0x57B7D8 CALL 0x463280。すべて既知0x57B380内部。0x57B559後は0x57B56B JMP 0x57B82Fもあるため、3回全てが無条件に実行されるという意味ではない。
  - [MAP SEMANTICS] T005所有資料は0x463280をRB-tree insert-if-absent（重複keyは先勝ち）と静的確認。ただし0x57B380の各callsiteが対象にするkey/container、重複時効果や実分岐はVERIFY。毎tickの3件新規登録とは断定しない。
  - [LOOP] 0x57B7DDでUnit+0x1E520を読み、0x57B7E3でhead、0x57B7E9でhead==sentinelなら0x57B822。非空側0x57B7F0でDEC DWORD [EAX+0x28]。別保存T012には0x57B800以降の0x510030/0x405440、0x57B81Aの同sentinel比較→0x57B7F0再分岐。node+28減算を含む走査が存在するとの局所静的照合。node意味、反復回数、分岐の副作用はVERIFY。
  - [KNOWN FIVE] 0x463280は既存Ghidra5点VERIFIED: info ev_07594e48bf10c7d3f1b65f21e2f1917b2e74e083f54f09e9659022e04f70ace9; pseudo ev_ee41eff345d68943cc2f8abf1bc46b58fc5d3a09b4a42f7a22b9925fe921e17f; asm ev_88bd0a7af01cc8756c1dc8c48f37e805a052303f37d706d5f50439825fdc7f97; callers上記; callees ev_fc25c4b7deaa83dad01c4ceddecfb21b3a21b01861f6bb2a68b03569187ba066。0x57B380本体は5点未取得でVERIFY。
- **Limitations:** - [KNOWN FIVE] 0x463280は既存Ghidra5点VERIFIED: info ev_07594e48bf10c7d3f1b65f21e2f1917b2e74e083f54f09e9659022e04f70ace9; pseudo ev_ee41eff345d68943cc2f8abf1bc46b58fc5d3a09b4a42f7a22b9925fe921e17f; asm ev_88bd0a7af01cc8756c1dc8c48f37e805a052303f37d706d5f50439825fdc7f97; callers上記; callees ev_fc25c4b7deaa83dad01c4ceddecfb21b3a21b01861f6bb2a68b03569187ba066。0x57B380本体は5点未取得でVERIFY。 / - [MASTER] 最新checkpoint151、研究DONE9/34・IN_PROGRESS21/VERIFY4、旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-1440-TICK-EXPIRY-TREE-ERASE-VS-ADVANCE-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_1440_TICK_EXPIRY_TREE_ERASE_VS_ADVANCE.md`; actual SHA256 `2B626FCB4691CE73BDCE88D2F23F51339E163ED78E9D12DDF60466CCFDA47FA0`; 4845 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - # REA-20261015-1440-TICK-EXPIRY-TREE-ERASE-VS-ADVANCE-01｜0x57B380木iteratorの変更/削除経路の区別
  - [SOURCES] exe/T005_REGISTRY_INSERT_CALLERS.txt lines8153-8177、exe/T012_STATUS_CORE_DUMP.txt lines1193-1204、exe/T005_ASSIGNMENT_BUILDER_PROBE.txt lines320-400、exe/T006_SELECT_SETTER_FULL.txt lines236-242、data/T013_OWNER_CANDIDATES_NUMERIC_CONTRACT_20261013_0031.md lines60-73、data/T012_BATTLE_CALC.md lines1084-1090。すべて既保存read-only。承認済みcopy source SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
  - [LOOP CURRENT] 0x57B7DD U+1E520 head取得、0x57B7E9 head==sentinelなら0x57B822へskip、非空では0x57B7F0 DEC DWORD[node+0x28]。保存断片では減算前にsigned>0判定が存在せず、各訪問nodeでDEC命令へ進む局所順序。上位到達条件はVERIFY。
  - [TWO UPDATE ROUTES] 0x57B800 CALL 0x510030後0x57B805 MOV EAX,[EAX]→stack cursor更新し0x57B81Aへ。一方0x57B80D LEA EAX,&stack_cursor→0x57B811 CALL 0x405440→cursor再読→0x57B81A。両routeとも0x57B81AでU+1E520 headと比較しneqなら0x57B7F0へ反復する。0x57B7F4..0x57B7FFの条件命令は既保存x86で未確認なので二者の選択predicateはVERIFY。
  - [CALLEE SEMANTICS 405440] B所有の保存x86確定: 0x405440はEAX=&cursorを受けRB-tree successorを計算してcursor DWORDを変更、非nil右子のleftmost/右子無しならparent昇行、CALL/heap操作無し。これはnode eraseではない。別tree 0x57AF83はU+1E540の**positive-only DEC、node非erase**であり、今回のU+1E520とは区別する。
  - [CALLEE SEMANTICS 510030] 保存exe/T005_ASSIGNMENT_BUILDER_PROBE.txt 0x510030..0x51011CにRB-tree node+4 parent/child+0,+8のリンク書替え、head link更新、0x405440によるsuccessor算出あり。exe/T006_SELECT_SETTER_FULL.txt 0x463A46 CALL 0x510030→EAXをcursor pointerとしてdereference。したがって0x57B800側は木構造の変更を伴うerase系経路を含み得る。対象nodeの実解放/全条件/事後状態は追加保存断片なしではVERIFY。
  - [NOVEL DELTA] 前回の「0x510030/0x405440が後続に存在」から、両calleeの役割差（tree mutationを伴うhelper対cursorのみ更新）と、B既知別treeのpositive-only/non-eraseとの差異へ限定的前進。U+1E520 loopをU+1E540 cooldown loopへ同一実装として統合しない。
  - [EVIDENCE IDs] 本回新規Ghidra evidence ID0件、STATIC VERIFIED増0件。既存0x463280 callers ev_cd55b9172146b1b73b06b54bbd571550221ca05419457de972262d896ecbf0b0 (run 20261009T215200079Z)を参照、0x57B380・0x510030・0x405440を今回新規5-method VERIFIEDにしない。
  - [LIMIT/VERIFY] exact 0x57B7F4..57B7FF branch、erase後のnode+28/owner/size、iterator invalidation、3回insertのkey/container、実ゲーム到達、正常死亡→Task callback returnは未確定。旧原作golden PASS0、新旧strict MATCH0。
- **Limitations:** - [CALLEE SEMANTICS 510030] 保存exe/T005_ASSIGNMENT_BUILDER_PROBE.txt 0x510030..0x51011CにRB-tree node+4 parent/child+0,+8のリンク書替え、head link更新、0x405440によるsuccessor算出あり。exe/T006_SELECT_SETTER_FULL.txt 0x463A46 CALL 0x510030→EAXをcursor pointerとしてdereference。したがって0x57B800側は木構造の変更を伴うerase系経路を含み得る。対象nodeの実解放/全条件/事後状態は追加保存断片なしではVERIFY。 / - [LIMIT/VERIFY] exact 0x57B7F4..57B7FF branch、erase後のnode+28/owner/size、iterator invalidation、3回insertのkey/container、実ゲーム到達、正常死亡→Task callback returnは未確定。旧原作golden PASS0、新旧strict MATCH0。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-1537-TICK-DEC32-FLAGS-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_1537_TICK_DEC32_FLAGS_BOUNDARY.md`; actual SHA256 `A6786725DF20E596B5EEEE8F2CC7C8320DA9D95267C06E5843FE7647A8087884`; 4618 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - [SOURCE] exe/T005_REGISTRY_INSERT_CALLERS.txt 0x57B7DD..0x57B7F0、exe/T012_STATUS_CORE_DUMP.txt 0x57B800..0x57B822、data/T013_OWNER_CANDIDATES_NUMERIC_CONTRACT_20261013_0031.md（405440と別tree比較）、REA_20261015_1440_TICK_EXPIRY_TREE_ERASE_VS_ADVANCE.md。承認コピー実測SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
  - [EXACT X86] 0x57B7DDはUnit+1E520のheadを取り、0x57B7E9 headと先頭nodeを比較。非空経路の0x57B7F0は「DEC DWORD PTR [EAX+28]」。この命令が実行されたnodeでは、旧値をsigned clampせず32bit modulo 2^32で1減算する。
  - [EDGE CASES; CONDITIONAL INPUTS] 旧0x00000001→新0x00000000(ZF=1)、旧0x00000000→新0xFFFFFFFF(ZF=0,SF=1)、旧0x80000000→新0x7FFFFFFF(OF=1)、旧0xFFFFFFFF→新0xFFFFFFFE。これはx86命令意味の導出であり、それぞれの旧値の合法ゲーム内到達は未証明。
  - [FLAGS] DECはZF/SF/OF等を更新するがCFを変えない。0x57B7F4..0x57B7FFの命令が未保存なので、後続条件分岐がZF/OF/比較命令のどれを採用するかはVERIFY。旧値1→0で消去する、または旧値0でretainする等は確定させない。
  - [CONTINUATION] 保存済み0x57B800はCALL 0x510030→0x57B805 MOV EAX,[EAX]→stack cursor更新、別の0x57B80DはCALL 0x405440(&cursor)→cursor read。両経路とも0x57B81Aのhead比較へ合流。DECは両経路の直前にあるため、callee内部未完時に0x57B7F0を無条件再実行させずnode/cursorと更新済み状態を保存する必要がある（有効呼出到達はVERIFY）。
  - [EVIDENCE IDs] 新規5種Ghidra evidence ID0件、新規STATIC VERIFIED0件。再利用：0x463280 callers ev_cd55b9172146b1b73b06b54bbd571550221ca05419457de972262d896ecbf0b0、0x40ED80 callers ev_fcaab3749388b92aabc79016efbbda7d48d5fb29ace7cc6bfc5d46d2dca4f6f3。0x57B380/0x510030/0x405440は新たに5種VERIFIEDへ加算しない。
  - [NEXT] P0死亡graph 575A60→575DF0→5684B0の正常return/Task callback帰還を既存保存証拠から優先。タイマーloopは0x57B7F4..FFの保存済み許可根拠が見つかる場合だけbranchを決める。実ゲームカウンタ0/1/負境界の観測・同条件Goldenは未実施。推測でdeleteや正常returnを確定させない。
- **Limitations:** - [RECOVERY REA-RC-20261015-1537-EXISTING-PSEUDO-ENOENT-01 / VERIFY] 保存済みファイル有無だけをread_fileで確認した dev_lab/recovered_source/ghidra_c_pseudocode/FUN_0057B380.c はENOENT。新規解析結果は得られず再試行なし。対象パス自体の存在を仮定せず、次回は既存のREA成果・原作x86保管資料から継続する。 / - [NEXT] P0死亡graph 575A60→575DF0→5684B0の正常return/Task callback帰還を既存保存証拠から優先。タイマーloopは0x57B7F4..FFの保存済み許可根拠が見つかる場合だけbranchを決める。実ゲームカウンタ0/1/負境界の観測・同条件Goldenは未実施。推測でdeleteや正常returnを確定させない。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-1640-LETHAL-POST-DISABLE-BRANCH-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_1640_LETHAL_POST_DISABLE_BRANCH.md`; actual SHA256 `2945BB59358CB2A6DB7E117AB16AEAB36A048DEC34F7A25D01A82E866D34B4C8`; 4593 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - [SOURCES] exe/T012_STR_AFTERDEATH_PROBE.txt lines 1349-1450（saved x86 VA5789E9..578B5F）、REA所有SOURCE_RECOVERY_DAMAGE_STATUS_20261011.mdのND-LETHAL/ND-VERIFICATION/DEATH-21/22、保存run21とlatest sync 20261011T153958076Z。承認済copy SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
  - [NEW LIVE GATE] 5789F2 CMP DWORD [Unit+0x1862C],0→5789F9 JE 578AFA。0なら追加handler分岐をskip。比較はvirtual+58帰還の後なので、事前snapshotを使わず同じlive Unitの値を再読する。+1862Cの人間向け意味・上流writer・合法到達はVERIFY。
  - [NONZERO STRING/RAW PREDICATE] 5789FF EDI=&Unit+0x1861C、578A05 ECX=0x627DAC、578A0A CALL 0x40B200、578A0F TEST AL,AL。AL非0なら578A13 ECX=[Unit+0x1E0]、578A19 ESI=Unit、578A1B CALL0x49CF20→578A20 JMP578AFA。文字列0x627DACの実バイト・0x40B200の等価規則・0x49CF20の副作用はVERIFY。
  - [RAW PREDICATE FALSE] AL=0なら578A25以降に進む。578A28 CMP DWORD [ESP+0x38],0から578A31/578A5Cの2通りの文字列準備、578A91 CALL0x49CD60、578ACD CALL0x49CD60、578AF5 CALL0x4321B0の順へ。途中4051D0/402670などのcalleeがある。各関数の意味や全副作用/例外経路は未確定で、成功no-op代用禁止。
  - [WORK STAGING] 5789F0以降の正しい継続は virtual+58 inflight→5789F2 fresh gate→(skip/0x49CF20/0x49CD60×2→0x4321B0)→578AFA cleanup→578B5F hit return。disable再入、子/owner/衝突/Task削除の二重適用、未帰還calleeへのAL1注入、5789F2未実行をhit完了扱いしない。旧原作実機trace未実施。
  - [NOT CLAIMED] 0x40B200がstrcmpかどうか、0x49CF20/0x49CD60/0x4321B0の具体的なゲーム効果、0x627DAC文字列、最後のcallerがGameTaskへ正常復帰する条件、旧EXE合法ヒット到達はVERIFY。既存NDの単なる『5789F2へ戻る』記述をVERIFIED増分として再計上しない。
  - [NEXT P0] 保存済み安全な呼出証拠で5789F2後の0x40B200戻り条件・0x49CF20/0x49CD60/0x4321B0と外側hit callerの関係を重複排除して特定。死亡graphの575C52後embedded各vtable・4BC9C0 ownerも依然VERIFY。動的挙動と復帰完了は推測しない。
- **Limitations:** - [MASTER/GOLDEN] 2026-10-15 Local読取MASTER checkpoint151、研究DONE9/34・IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。 / - [NEXT P0] 保存済み安全な呼出証拠で5789F2後の0x40B200戻り条件・0x49CF20/0x49CD60/0x4321B0と外側hit callerの関係を重複排除して特定。死亡graphの575C52後embedded各vtable・4BC9C0 ownerも依然VERIFY。動的挙動と復帰完了は推測しない。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-1734-POSTLETHAL-STRING-EQUALITY-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_1734_POSTLETHAL_STRING_EQUALITY_GATE.md`; actual SHA256 `AB2631905C4C05BFB7716F2D47D2E96EB1270761C306E1495CBD74BC48BDB83A`; 4751 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - OWNER/REQUEST: REA専用 WRQ-20261013-REA-DEATH。T012/T013（T006/T010参照）。従前REA-20261015-1640-LETHAL-POST-DISABLE-BRANCH-01に残した「0x40B200の等価規則VERIFY」のみを既存5証拠で精密化。原本・他owner変更なし。
  - SOURCE/SHA: 承認済みrea_lab/targets/hakushin067_Vahren.exeのみ。今回LocalでSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187を再確認。既存run 20261011T133432356Z/40B200_procedure_*.json、exe/T012_STR_AFTERDEATH_PROBE.txt 0x5789F2..0x578A25。
  - EXISTING FIVE EVIDENCES 0x40B200: info ev_ec2dd487c7478081fb26ce910a9b854f47c123371b542f12e59e6bdf5534439f；pseudo ev_d3b60611f4e0570c118727b471bbd19bd10cd6c9f187e0812023914cb8ccef61；asm ev_80377536380b1f73406c409003776dc07da99b7a8d860e3f70dc06941a55541a；callers ev_35291b767472758d4d578ad386e03faa8202014e9f2b0cbe76deb646f1cbfb7b；callees ev_f5bba603bb289fe46001acbd2e9227eb0df15c0d4b88f12e77e1f47cd0125ca6。
  - ENTRY/BOUNDARY: 0x40B200..0x40B253、84 bytes、12 blocks、5種Ghidra証拠整合。ABIはECX=zero-terminated literal pointer、EDI=MSVC風stringオブジェクト（+0x10現在長、+0x14容量、容量<16はinline/>=16は先頭にheap ptr）。高水準命名自体は復元仮説。
  - EXACT BRANCH: 0x40B207..20Eでliteral strlenを算出。0x40B210で[EDI+0x10]を取得し、0x40B217..21Bでmin(string length,literal length)を比較長とする。0x40B21D..229で短文字列/heap先頭をEDXへ、0x40B229で0x402C40比較helperを呼ぶ。
  - RETURN CONTRACT: 比較helper非0ならAL=0。helperが0でもstring長&lt;literal長ならAL=0、string長>literal長ならAL=0、同長のみAL=1（0x40B22E..253）。従ってAL=1条件は「0x402C40が一致を返し、保存長とliteral長も一致」。0x402C40の実byte比較/case規則は未独立5点証拠なのでVERIFY、単純strcmp確定と言わない。
  - CALLSITE: 0x5789F2でUnit+0x1862C==0なら0x578AFAへskip。非0なら0x5789FF EDI=&Unit+0x1861C、0x578A05 ECX=0x627DAC、0x578A0A CALL0x40B200→0x578A0F TEST ALで分岐。AL=1は0x578A1B 0x49CF20→0x578AFA、AL=0は0x578A25以降の0x49CD60×2→0x4321B0条件経路へ。
  - CRITICAL IMPACT: 0x40B200を一般的event flag存在判定やprefix一致で代用しない。Unit内stringの長さと内容の判定（comparison helper成功）があり、死亡解除とhit handlerの継続を区別。AL=0でもhit処理には残副作用、virtual+58だけでhit全体成功扱い不可。
  - VERIFY: 0x627DACの実文字列、0x402C40の厳密な照合規則、Unit+0x1861C/+0x1862Cの書込元、0x49CF20/0x49CD60/0x4321B0の全副作用、旧EXE合法到達、下位callee/Task callbackの正常帰還は未確定。これらの実処理やゲーム再実装の完了判定を推測しない。
- **Limitations:** - VERIFY: 0x627DACの実文字列、0x402C40の厳密な照合規則、Unit+0x1861C/+0x1862Cの書込元、0x49CF20/0x49CD60/0x4321B0の全副作用、旧EXE合法到達、下位callee/Task callbackの正常帰還は未確定。これらの実処理やゲーム再実装の完了判定を推測しない。 / - MASTER: 今回読み直した最新研究E checkpoint152、34 Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、旧新strict MATCH0。ゲーム再実装率は測定していない。STATIC evidence!=gameplay verified。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-1945-STATUS-GATE-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_1945_STATUS_AND_NEXT_CHECKPOINT.md`; actual SHA256 `11B1C3A91634D3A86B919C7137B560AFD1C86EE80428E2DD28EC5C17F083E0AC`; 2952 bytes.
- **Record class:** STATUS_AUDIT; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - Status/preflight-only owner record; no additional native finding published from restricted content.
- **Limitations:** - MASTER更新: checkpoint154、研究34Task DONE9/IN_PROGRESS21/VERIFY4、E正式READY累計543。REAの解析数とは混算しない。 / - VERSION: 成功runのREA 6.1.0＋Ghidra12.1.4と現在のrunnerのREA6.4.0は別のprovenance。6.4.0での新規解析互換は未検証。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-2137-POSTLETHAL-STACK-STRING-EPILOGUE-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_2137_POSTLETHAL_STACK_STRING_EPILOGUE.md`; actual SHA256 `FB37001640B826FC469A0124244CF5E905D8DF6DB050DF58250EF7D0217A9329`; 4293 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - DIFFERENT LITERALS: A 544BD9 passes 0x62A314; B 578A05 passes 0x627DAC to 40B200. Same comparator does NOT prove equal literal bytes. Actual literal strings / bytes still VERIFY.
- **Limitations:** - DIFFERENT LITERALS: A 544BD9 passes 0x62A314; B 578A05 passes 0x627DAC to 40B200. Same comparator does NOT prove equal literal bytes. Actual literal strings / bytes still VERIFY. / - VERIFY: lower callee actual side effects/returns, 40B200->402C40 byte comparison, real constant strings, exceptional string allocator behavior, normal outer Task callback and native gameplay old/new matching.
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-2240-POSTLETHAL-EVENT-FLAG-ABI-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_2240_POSTLETHAL_EVENT_FLAG_ABI.md`; actual SHA256 `453E9ADB53C7C42109F6D4EFA92AC3FEF38ACEBD2D48A6D05C7B85FD58C0C9AE`; 5545 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - SOURCE: exe/T012_STR_AFTERDEATH_PROBE.txt VA0x544CA5-544CC7、0x578AD8-578AFA; exe/T006_CORE_HANDLERS.txt VA0x4A13F8-4A1476,0x4321B0-432379。REA既存WAVE4_FINDINGSとREA_EVENT_SCENE_OBJECT_BRANCH_AUDITは0x4321B0個体のguard/writerを既報、本記録は死亡後2callsiteからの実引数接続が差分。
  - POSTLETHAL CALLER A: 0x544CA5 PUSH 1; 0x544CA7 PUSH 0; 0x544CA9 PUSH 0; 0x544CAB SUB ESP,0x1C (string); 0x544CC1 PUSH [Unit+0x1E0]; 0x544CC2 CALL 0x4321B0。入口SP0+0x2Cは最初にpushした1。
  - POSTLETHAL CALLER B: 0x578AD8 PUSH 1; 0x578ADA PUSH 0; 0x578ADC PUSH 0; 0x578ADE SUB ESP,0x1C; 0x578AF4 PUSH [Unit+0x1E0]; 0x578AF5 CALL 0x4321B0。同様に入口SP0+0x2C=1。
  - CONTRAST: script caller 0x4A13F8 PUSH 0; 0x4A13FA PUSH ECX; 0x4A13FB PUSH EDX; 0x4A13FC SUB ESP,0x1C; 0x4A1418 PUSH engine; 0x4A1419 CALL 0x4321B0。こちらの同flag byte=0。別caller 0x4A144F PUSH 1/0x4A1451 PUSH 0/0x4A1453 PUSH 0 は死亡後callerと同flag=1。
  - EXACT GUARD: 0x4321F4 flag!=0 THEN 0x432209 CMP BYTE [engine+0x1EEC44],0。両方非0なら0x432216 battle-special routeへ進み、一般経路0x432306をskipする。flag=1でもengine battle flag=0なら0x432306一般経路。
  - GENERAL ROUTE: 0x432306以下は保存済み原作x86で@evtend_文字列生成系を経て0x432379 CALL 0x4637A0（既存VERIFIED numeric writer）、event property lookup 0x4323AB→0x4647D0とVM frame処理へ。特殊経路ではこの関数内の0x432379 writerを通らない（既存WAVE4_FINDINGSの限界と一致）。
  - CRITICAL IMPLICATION: 死亡後両callerの明示flag=1は「常にhistory writerへ行く」を意味しない。0x49CD60を2回呼んだ後のlive engine+0x1EEC44状態に応じて0x4321B0内部のdispatch・履歴処理が異なる。先行virtual+58/0x49CD60の副作用は未知でbattle flagを事前固定できない。
  - NO OVERCLAIM: 0x4321B0全実行・@evtend_値/保存持続性・どの実ゲーム状態でspecial/generalに到達するか・Task callback外側正常帰還・例外処理/旧実機一致はVERIFY。ゲーム固有event意味論/確定BUGとしては扱わない。
  - EXISTING GHIDRA VERIFIED 0x4321B0: info ev_b0baec02c8d12ecbd78d2700c4b72f41016dad1c8fd11c33be96aa29aa107dea; pseudo ev_6443778f30890c0e5cb33fc7bbabf54b8cd665a1424f7b354c6bd439dbac2051; assembly ev_56f9a3557ec9eaa37a3dae138562b66cdde8d20a39e915d61d3e8c37709157db.
  - NEXT: P0 WRQ-20261013-REA-DEATHへこのA/B caller→0x4321B0のengine flag評価時点を引継ぎ、保存済み証拠で0x575A60→575DF0→5684B0外側Task callback帰還と0x49CD60後のflag writer/readerを再検証。個別callee return receiptなしで成功偽装しない。
  - ACCEPTANCE MATRIX (DESIGNED/NOT RUN): callerFlag0×battleFlag0→general; 0×1→general; 1×0→general; 1×1→special。死亡後A/BはcallerFlag=1固定なのでbattleFlagの実到達値と切替時点のcaptureが必須。既済event履歴writer/stackの副作用を先取りせず、分岐前後のengine state, `0x4637A0` call count, queue stack, return PCを別receiptにする。旧原作goldenは未観測であり、この行列は静的分岐のみ。
- **Limitations:** - MASTER: 今回read-onlyのcheckpoint157、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧未改変EXE gameplay golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。 / - ACCEPTANCE MATRIX (DESIGNED/NOT RUN): callerFlag0×battleFlag0→general; 0×1→general; 1×0→general; 1×1→special。死亡後A/BはcallerFlag=1固定なのでbattleFlagの実到達値と切替時点のcaptureが必須。既済event履歴writer/stackの副作用を先取りせず、分岐前後のengine state, `0x4637A0` call count, queue stack, return PCを別receiptにする。旧原作goldenは未観測であり、この行列は静的分岐のみ。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261015-COUNT-LITERAL-ALIAS-CORRECTION-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261015_COUNT_LITERAL_ALIAS_CORRECTION.md`; actual SHA256 `AC2B87DFDF14D6E39FEC2CAFBBC2FDA8596D1C0AD07C36221FBB8E99B2F509B1`; 4423 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - CORRECTION: 2026-10-15 18時台の「比較対象2アドレスが異なるため文字列も異なる可能性」という保留は、既存原作ASCII xref資料から解消できる。VA 0x62A314 と 0x627DAC は、ともにASCII literal **count** と分類済み。同一アドレスではないが同一内容の文字列として扱える。
  - PRIMARY SAVED EVIDENCE: exe/T006_API_STRING_XREFS.md 見出し「exact ASCII strings in Hakushin Vahren.exe」およびcount項目（およそ94行目）: count: str=0x627dac,0x62a314,0x6353c4; xrefs=0x44eeb3,0x544bd9,0x578a05。exe/T031_RNG_INDEX_PROBE.txt冒頭も同じcount三アドレス・xref三箇所を独立列挙。
  - LITERAL ANCHOR: exe/T013_UNIT_STRING_BAND.txt 0x627dac 'count'、exe/T014_ENTITY_MARKERS.txt 0x627dac 'count'。0x62A314についてはT006のASCII xref保存結果が文字列名根拠であり、今回の新規PE bytes抽出は0。
  - CALLER A: exe/T012_STR_AFTERDEATH_PROBE.txt 0x544BC5 virtual+58→0x544BC7 [Unit+0x1862C]長さgate→0x544BD9 ECX=0x62A314→0x544BDE call 0x40B200→0x544BEF 0x49CF20（比較成立時）。
  - CALLER B: 同保存native 0x5789F0 virtual+58→0x5789F2 [Unit+0x1862C]長さgate→0x578A05 ECX=0x627DAC→0x578A0A call 0x40B200→0x578A1B 0x49CF20（比較成立時）。
  - PREDICATE: 同一Unit string（Unit+0x1861C）を同じ0x40B200に渡すため、**同じ入力文字列・同じ比較規則を前提にした局所predicateは等価**。関数呼出の実時間/Unit identity/直前副作用が異なるため、A/B実行全体または結果が常に同一とは証明しない。
  - IMPORTANT REMAINDER: 比較不成立後は両callerに0x49CD60×2→0x4321B0の段階あり。既REA-20261015-2240のcallerFlag=1とengine battle flag gateは維持。dead_event_a/d関連の別定数0x62A31C/32C/33Cと0x627DB4/DC4/DD4の文字列同一性は今回未判定。
  - NO OVERCLAIM: 0x40B200下位0x402C40の文字単位比較規則、0x49CF20の副作用、0x49CD60後帰還、外側Task callbackの正常復帰、原作旧実機goldenはVERIFY。A/Bの違いを「固定比較文字列の内容差」に帰属させない。
- **Limitations:** - NO OVERCLAIM: 0x40B200下位0x402C40の文字単位比較規則、0x49CF20の副作用、0x49CD60後帰還、外側Task callbackの正常復帰、原作旧実機goldenはVERIFY。A/Bの違いを「固定比較文字列の内容差」に帰属させない。 / - MASTER READ: 最新checkpoint158、34Task DONE9/IN_PROGRESS21/VERIFY4。旧原作Gameplay golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

## Ownership and corrections

Previously known functions/calls and Work implementation interfaces cannot be relabeled as new native findings. Curator must independently verify current V9/ASM, original source SHA, prior owner corrections, privacy and tests. Shared develop/REF/dictionaries not modified. Forbidden Wave6/VA materials remain blocked.
