# REA legacy research 20261018 A

Private REA owner intake / static & conditional inferred / VERIFY; NOT CURATED or READY. All 8 historical source IDs are older independent QC or research notes. The original owner Markdown reports are SHA256-verified read-only on research PC (2026-11-02 JST); no new original EXE/V9 rehash, Ghidra or original game run. Excerpts below are only prior allowed static claims. Prior refused operations/results/VA remain BLOCKED and excluded. No newly verified five-method function; original Golden PASS/READY=0.

### REA-20261018-0035-DEATH-GRAPH-REENTRY-GATE-01

- Source `rea_lab/decomp_task/REA_20261018_0035_NORMAL_GRAPH_REENTRY_GATE_QC.md` / actual SHA256 `7794C22617BCA519AEE8377739BDC4C08289344214950AB8C9D2573C7C65D486` (4707 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE CONTEXT] 既保存0x575A60→0x575DF0→0x5684B0の死亡正常帰還は、marker処理・3埋込windowの各virtual/Task/Render/Spatial解除後に必要。既存ND-GRAPHは第一window W=Unit+5B0、第二=Unit+800、第三=Unit+89Cを分離し、returnまでVERIFY。
  - [NEW SOURCE GATE] session.continue_resolved_normal_disable_graph(pointer) は phase=="VERIFY_NORMAL_DISABLE_GRAPH"、frame.next_va==0x575C52、Unit identity一致を必要とし、begin_normal_disable_graph_575df0を1回呼び frame を置換する。
  - [BRANCH ZERO] unit.globals[0x87F783]==0 の初回呼出は graph=(W=Unit+0x5B0,virtual_slot=0x34,return_pc=0x575E18,world_pointer=Unit+C)、frame.next_va=0x575E16 を返す。
  - [BRANCH NONZERO] 同global byteが非0の初回呼出は graph=(Unit+0x540,virtual_slot=0x54,return_pc=0x4DDD99)、frame.next_va=0x4DDD97 を返す。graphがNoneという初回条件は以後満たさない。
  - [REENTRY COUNTEREXAMPLE] どちらの分岐でも初回後のframe.next_vaは0x575C52ではないため、同じsession API/actionを再送すると session guard で SessionGap("matching first normal-disable graph continuation required") に入る。return_pcを記録しただけでは実virtual戻りを証明せず、親+34の完走にはならない。
  - [EVIDENCE] 新規Ghidra5種類のevidence ID=0件（今回は保存済みNative ND-GRAPHとWork現行ソースのみ）。source SHAの今回再計算なし、関数境界の新認定なし。
- **Limitations/errata:** - [DELTA VS PREVIOUS] 22H資料のworld再取得リスク・後段window未実装を再計上しない。今回の独立増分は「marker両分岐が必ず初回guardから離れ、同APIで再開できない」という具体的停止条件をコード上の制御フローから導いた点。 / - [CLASSIFICATION] 既存Workソース限定STATIC IMPLEMENTATION GAP=1 / 未確認graph resume経路・合法入力再現・テスト・原作実機goldenはVERIFY。原作エンジンBUG、実機不一致確定、全死亡経路一般化は禁止。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-0135-RUNNER-REFUSAL-GATE-AND-GRAPH-STATE-01

- Source `rea_lab/decomp_task/REA_20261018_0135_RUNNER_REFUSAL_GATE_AND_GRAPH_STATE_REENTRY_QC.md` / actual SHA256 `719829FD1168FCB69D6842FEC063B061BA63CF74C0B3607DBD5D3FF91AF8CFE3` (4818 bytes).
- Category STATUS_AUDIT, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE STAGE/VA] 0x575A60→0x575DF0→0x5684B0 (T010/T012/T013); graph first virtual 0x4DDD97または0x575E16。既存ND-GRAPHが基準。正常callee帰還・全window/Task/Render/Spatial/親RETURNはVERIFY継続、擬似正常return禁止。
  - [EVIDENCE] 今回新規のinfo/pseudo/assembly/callers/callees evidence IDs=0。既存ND-GRAPH=REA-ND-20261013-001、およびRUN_RESULT 20261011T153309850Zの検証済み5方法を再利用。新規関数境界VERIFIED=0。
- **Limitations/errata:** - [NATIVE STAGE/VA] 0x575A60→0x575DF0→0x5684B0 (T010/T012/T013); graph first virtual 0x4DDD97または0x575E16。既存ND-GRAPHが基準。正常callee帰還・全window/Task/Render/Spatial/親RETURNはVERIFY継続、擬似正常return禁止。 / - [MASTER/GOLDEN] 最新MASTER checkpoint178、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-0236-DOT54-OWNER-RETURN-GATE-01

- Source `rea_lab/decomp_task/REA_20261018_0236_DOT54_OWNER_RETURN_GATE_QC.md` / actual SHA256 `3487F23D8C267B9EB7FAC98A7CD27BD4882A8BEE5EAF0F63AE17570FB4A31968` (4561 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [SOURCE] MASTER checkpoint178（2026-10-18 01時台E非READY照合で据置）/プロトコル/README/QUEUE/PROGRESSを先読。保存RUN_RESULT 20261011T153309850Z、sync 20261011T153958076Z、SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md内DEATH-06/08、Work native_battle_outcome.py:113-159、session.py:281-290、runner.py:457-460を照合。
  - [NATIVE VA] 0x575DFD→0x4DDD80(Dot=Unit+0x540)。global87F783が0なら0x4DDE6B RET4→親0x575E02。非0なら0x4DDD97 Dot.virtual+0x54 CALL、正常帰還0x4DDD99でEAXを検査する。
  - [DOT BINDING SAVED] 既保存DEATH-08: ctor VA0x56FA52 がUnit+0x540へvptr0x639A4C（Dot RTTI）を格納。Dot+0x54 virtual=0x5428A0、命令8B416C C3 はEAX=[ECX+0x6C]を返す。Unit+0x540+0x6C=Unit+0x5AC、既存0x5707AEでowner=Unit pointerを格納する初期化証拠あり。
  - [BRANCH DIFFERENCE] CALL返EAX==0なら0x4DDD9D..ADでglobal0x8A2ED8へ0xF0byte memset(0)の後0x4DDDB1 RET4。EAX!=0なら0x4DDDB4以降にtree lookup（0x4F8A80）→条件付きerase(0x4DEC70)/72byte move/backref/countへ進む。最初のvirtual帰還をbool ALへ縮めずEAX全DWORDで判定する。
  - [CURRENT WORK] begin_normal_disable_graph_575df0はUnit本体vptr0x63A9E4/disabled flag/marker byteを確認し、marker!=0でgraph(object_ref=Unit+540, slot54, return_pc4DDD99)、next_va4DDD97を返して意図的に中断する。検査した関数はDot実vptr（Unit+540）、Dot.owner（Unit+5AC）、仮想結果EAXをまだ検証・取得しない。
  - [NEW LIMITED DELTA] 今回の追加は、旧保存Dot ctor/getterの具体的offsetをWork graph cursorに対応付け『slot54呼出直前のlive object-binding receiptと、0/nonzero return各分岐を再開時に別受理する必要』を明確化したこと。まだresume未実装は前回0135/0035で指摘済みにつき重複成果計上しない。
  - [WORK ACCEPTANCE / NOT RUN] Dot vptr/type identity・owner fieldと同一Unitの生存時identityを確認。virtual戻り値は再実装で捏造しない。EAX==0なら実memset完了receipt、EAX!=0ならtree検索→erase→配列backref/commit receipt後のみ0x575E02へ戻し、その後window virtual+34へ。非zeroのowner pointerとtree keyは同一視しない。
  - [EVIDENCE] 新Ghidra5手法evidenceID=0、静的VERIFIED増加0。許可済みND-DEATH-08/06と保存Native N1、最新20261011T153309850Zの5方法（例0x57CFD0 info ev_f85bc7f40298b5ec205b3f4f8c0365f48b2fa30e5e8afc42691ec110f5c23efa）を再利用。新規関数境界認定0。
- **Limitations/errata:** - [VERIFY BOUNDARY] 死亡直前にDot vptr/ownerがctor値から書き換わるか、callee例外/異常return、globalバッファの最終意味、tree iterator安全性、下流render/Task/Spatial、実Gameplayは未確認。元の原作BUG・Work実機不一致確定とはしない。 / - [MASTER/GOLDEN] 公式MASTER checkpoint178、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-0536-T014-OPEN-FAIL-ASYMMETRY-01

- Source `rea_lab/decomp_task/REA_20261018_0536_GLOBAL_SAV_OPEN_FAILURE_ASYMMETRY_QC.md` / actual SHA256 `321D048682AE2A513EAA6CEDCC49EF0481061DFD9C889C8053E1AC0AED2074EE` (4507 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [GHI 428710] runs/20261011T113414092Z: info ev_18083c1e4b216eb84426042a80e5dd8d28b884882f59162ab8f5fe1cb74a64d6（entry0x428710、3252bytes/4 body ranges）、ASM ev_a8b58058d05e576dbaa8ebd22736dcfa684d5fb5289e0897e1e5834eb351ec4b、pseudo ev_562ea04990ecb04a74ea0796d27a7c629a061894e46952f31b87c452af188775。
  - [GHI OTHER] 428710 callers ev_21421f53fb9052bf2f3b7cbee448c0bfe34b814e644d49db93939e7b14d7719a（0x514270/0x567210/0x567840）、callees ev_607a477af0d6bc95128190a05f5ff119d4c08a35d1691703c6e75331d4b7adc0。0x428010 reader ASM ev_8f357dc6b9e49591c6a5cec5ac76b4bd2c9019e4bc9cd61f15e5b3ba1bd55118。
  - [WRITER MISS→CREATE] 428710: 0x428831 FindFirstFileA→0x42883D CMP -1; absent branch 0x428846..0x42886D CreateFileA(GENERIC_WRITE, OPEN_ALWAYS=4)。invalid handle→0x42887D..0x428898 LoadException throw; valid→0x4288BF WriteFile(marker+NUL)→0x4288C6 CloseHandle。これは既存T014 upsert監査の再確認。
  - [WRITER READ-OPEN FAILURE / NEW CROSSWALK] 0x4288F3 CreateFileA(GENERIC_READ, OPEN_EXISTING=3)→0x4288F5 MOV EBP,EAX→0x4288F9 CMP EBP,-1→0x428901 JNZ 0x4289AE（成功時はdecode/parse）。失敗時は0x428907..0x4289ADで一時文字列を解放しRET。少なくともこの局所ではLoadException throw・後段upsert・再暗号化・再書込に到達しない。
  - [READ-ONLY READER CROSSCHECK] 0x428010: FindFirstFileA失敗0x428185..0x428188→0x42818A..0x4281FD cleanup/RET；READ OPEN_EXISTING失敗0x428225..0x428237→0x428239..0x428280→0x4281D1→RET。readerもこの局所の読込失敗ではthrowでなく早期RET。保存run/20261011T112315808Z/428010 ASM。
  - [NEW DISTINCT IMPLICATION] 同じglobal.savでも「writerの欠損file新規作成が不可（throw）」と「writerが対象をREADで再openできない（早期RET）」は異なる。readerも不在/読込open失敗は早期RET。missing/readDenied/writeDeniedを単一の正常セーブ完了・単一例外扱いに統合しない。
- **Limitations/errata:** - [VERIFY] CreateFileAの成功後ReadFileのshort read、WriteFile byte数/return、親callerがRETを成功と扱うか、初期marker書込の残存、例外catch、現物global.savゲーム挙動は未確認。『必ず黙って成功する』『破損する』とは断定しない。原作新確定BUG0、旧EXE実機golden PASS0、strict MATCH0。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-0638-T014-GWRITE-OPENFAIL-VM-CONTINUE-01

- Source `rea_lab/decomp_task/REA_20261018_0638_T014_GWRITE_OPENFAIL_VM_CONTINUE_QC.md` / actual SHA256 `0DF7F2CD9E321ECFC892FDCF703E988803B975F3ED506DB33DD7804AB9FE13CF` (3964 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [CORE RETURN/EXISTING] 0x428710（T014 writer）保存済みGhidra info ev_18083c1e4b216eb84426042a80e5dd8d28b884882f59162ab8f5fe1cb74a64d6、ASM ev_a8b58058d05e576dbaa8ebd22736dcfa684d5fb5289e0897e1e5834eb351ec4b。READ用CreateFileAは0x4288F3、invalid handle分岐0x428907..0x4289ADはcleanupしてRET。新規ファイル作成失敗0x42887D..0x428898はLoadException throw。後段upsert/writeまで到達するとは限らない。
  - [NEW CROSS-CALL] 原作保存済exe/T014_GLOBAL_DISASM.txt 0x4A60D1（gwrite opcode handler）：0x4A61BD CALL 0x428710、その帰還後0x4A61C2 add esp,0x3c、0x4A61C5/0x4A61D0 local string cleanup、0x4A61DB XOR AL,AL、0x4A61DD JMP 0x4A633C。保存済exe/T006_UNKNOWN_BRANCH.txt 0x4A633C..0x4A6357 epilogueは正常経路のALを変更せずRET。
  - [VM CONTRACT] 保存済exe/T006_HANDLER_RETURN_CFG.tsvで opcode77 gwrite=states0/exit0x4A633C。T006既確定dispatched AL0=同pass Continue／AL1=Yield。従ってREAD-open失敗が例外なく局所RETした条件では、gwrite handlerがAL0を返しVM interpreterは継続する（正常なファイル永続化完了の意味ではない）。新規の増分はT014失敗時局所RETとT006 opcode戻り値の条件付き接続のみ。
- **Limitations/errata:** - [VM CONTRACT] 保存済exe/T006_HANDLER_RETURN_CFG.tsvで opcode77 gwrite=states0/exit0x4A633C。T006既確定dispatched AL0=同pass Continue／AL1=Yield。従ってREAD-open失敗が例外なく局所RETした条件では、gwrite handlerがAL0を返しVM interpreterは継続する（正常なファイル永続化完了の意味ではない）。新規の増分はT014失敗時局所RETとT006 opcode戻り値の条件付き接続のみ。 / - [VERIFY] LoadException catch経路、ReadFile後のshort read、WriteFile API成功判定と永続化保証、実ファイルの部分書込、VM上位での他種エラー表示、旧EXE実機での観測は未確認。読込open失敗でも常にセーブ成功/破損と断定しない。原作新BUG確定0。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-0730-POSTLETHAL-PROBE-RECOVERY-01

- Source `rea_lab/decomp_task/REA_20261018_0730_POSTLETHAL_LITERAL_PROBE_RECOVERY_AND_PROGRESS_QC.md` / actual SHA256 `35E8AB43F18EAC35BF496400E48D0D348C079D71779AB5BAFA39D8D8B9D9CE38` (4166 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NATIVE EVIDENCE REUSE] REA-ND-20261013-001の通常死亡VA575A60→575DF0→5684B0、致死tailのvirtual+58 VA5789F0→5789F2 live string gate→必要後段→578B5F RET16を確認。既存REA_20261015_1734/2137/2240は40B200比較・stack cleanup・event dispatchを既に監査済みで、今回は再成果計上なし。
  - [RELATED VERIFIED] 保存Ghidra 0x40B200（T012/T013関連）info ev_ec2dd487c7478081fb26ce910a9b854f47c123371b542f12e59e6bdf5534439f、assembly ev_80377536380b1f73406c409003776dc07da99b7a8d860e3f70dc06941a55541a。新Ghidra関数境界/証拠取得0。
- **Limitations/errata:** - [NO-RETRY] 同じ失敗コマンドを再実行・別shell/tool/pathへ切り替えず、この二つのliteral実バイトは引き続きVERIFYとする。失敗した操作からの結果・SHA一致・文字列同一性を捏造しない。 / - [RESEARCH] 最新MASTER checkpoint180、研究DONE9/34(IN_PROGRESS21/VERIFY4)。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-0833-DEATH-GRAPH-PHASE-CROSSAPI-01

- Source `rea_lab/decomp_task/REA_20261018_0833_GRAPH_PHASE_API_COMPOSITION_GATE_QC.md` / actual SHA256 `C7571AC74904F0AB9EB868BC1CC0B7D0666288257AFCFA9DF8228D4FFA09A6BF` (4968 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [OWNER/REQUEST] 独立REA・WRQ-20261013-REA-DEATH P0。対象T010/T012/T013、VA0x575A60→0x575DF0→0x5684B0。Desktop Commander Local Compact限定、既存証拠/別owner実装read-only。新Ghidra/実機実行0。
  - [NATIVE CONTRACT] 保存済みREA-ND-20261013-001 ND-GRAPH: W=Unit+5B0/800/89Cを順序処理し、各W.virtual+08のAL!=0なら0x4C22B0 Task解除、virtual+48 AL!=0なら0x4C3E40 Render解除、virtual+44の後0x4BC9C0 Spatial解除。後段0x5684B0の部隊・選択解除も必要。各callee正常帰還はVERIFY。
  - [VERIFY] Dot+54のEAX、3Window実vtable、各Task/Render/Spatial managerとworld再取得、独立calleeの正常return、0x5684B0親子帰還、Task callback、実Gameplayは未検証。原作BUG・Work動的不一致確定ではない。
  - [EVIDENCE] 新Ghidra info/pseudo/assembly/callers/callees ID取得0、STATIC VERIFIED増0。既存ND-001、latest RUN_RESULT source_sha256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187を再使用。今回COPY EXE SHAは再計算なし。
- **Limitations/errata:** - [VERIFY] Dot+54のEAX、3Window実vtable、各Task/Render/Spatial managerとworld再取得、独立calleeの正常return、0x5684B0親子帰還、Task callback、実Gameplayは未検証。原作BUG・Work動的不一致確定ではない。 / - [MASTER/GOLDEN] 最新checkpoint181、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

### REA-20261018-0936-DEATH-MANAGER-PREBIND-GATE-01

- Source `rea_lab/decomp_task/REA_20261018_0936_DEATH_MANAGER_PREBIND_GATE_QC.md` / actual SHA256 `4397886494D69DD6774019F50C263DAB4A0073405924965F98086F77ED73E05D` (5041 bytes).
- Category RESEARCH_QC, does not represent a new native function; T010/T012/T013/T014/T031 related semantics need owner reconciliation.
- **Previously saved native/ABI and Work-interface boundary observations:**
  - [NEW SCOPE] 0833の「Graph停止後、既存unregister APIはACTIVE guardで使用不能」と異なり、本IDでは解除に必要なregistryの初回bind自体もGraph停止後に行えない前提条件を確定。これはWork実装の静的インターフェース制約であり原作の挙動不一致・動的BUG確定ではない。
  - [NATIVE BASIS] 既保存REA-ND-20261013-001 ND-GRAPH: W=Unit+5B0/800/89Cを順序解除、各WのTaskMgr=*(world+4)+C、RenderMgr=*(world+C)、SpatialMgr=*(world+8)。world=*(Unit+C)は各window入口で再取得。virtual ALや各callee正常帰還はVERIFY。
  - [INCREMENTAL CONSEQUENCE] 将来WorkがGraph stage実装を追加しても、未登録Task/Render/Motion managerをGraph内部で従来bind API経由で遅延bindするだけではACTIVE guardで停止する。合法開始前のregistry/World prebindingと、Graph専用の帰還receipt・実world manager identityとの照合を分けて設計する必要。
- **Limitations/errata:** - [STRICT VERIFY] TaskRegistry/RenderRegistry/MotionWorldの現在のbound pointerが原作world内の各managerと同一だとは今回証明していない。worldがWindow間で更新される可能性も残る。binding済みならGraphが完走できるとの推測は禁止。別のGraph-safe内部APIや合法動的manager獲得は未実装・未検証。 / - [MASTER/GOLDEN] 最新MASTER checkpoint181、DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。
- **State:** SOURCE_PUBLISHED_INTAKE or STATUS_ONLY / STATIC/VERIFY; original Golden PASS 0, READY 0. Denied operations only held as historical safety metadata.

## Curator handoff

Older reports may overlap with current B/REA research and already-curated REF facts. Match source SHA, VA, exact branch semantics, corrected owner interpretations and provenance before adopting anything. No raw tool logs/secret paths/native binary or refused evidence added, and no develop/REF/symbol edits by REA. New formal evidence five-set 0, new VERIFIED 0, Golden PASS 0.
