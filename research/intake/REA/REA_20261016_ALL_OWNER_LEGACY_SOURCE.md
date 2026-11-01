# Historical REA 20261016 owner source ALL

REA owner PRIVATE research intake only; old source IDs and source SHA were independently rehashed 2026-11-02 JST. This is preservation, not 6 newly REA-verified functions. Prior safe ASM/CALL observations are recorded from original owner text; refused VA/operations/results are not copied or retried. A status-only entry is retained as historical audit metadata rather than new research. Five-method new VERIFIED=0, original game Golden PASS=0, READY=0. Current V9/PE SHA and native tests were not freshly rerun in this intake.

### REA-20261016-0040-PREV58-AUX-GATE-CROSSCALL-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261016_0040_PRE_V58_AUX_GATE_CROSSCALL.md`; actual SHA256 `E49C33943E2846387BACA55A2F0ED959D43426E99E28E880F42CCCF19862AC2F`; 3969 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - SOURCE: exe/T012_STR_AFTERDEATH_PROBE.txt stored original assembly (prior recorded SHA256 591B3DF940D8D847D0EF44CAE3E4E87B9C80F7E90339CD33A06C2B1BF79F61F7), blocks 0x544B3C..0x544BC7 and 0x578963..0x5789F2.
  - COMMON BEFORE-GATE: A 0x544B4A and B 0x57896F push Unit EBX then call 0x588470; both copy AL into byte [ [EBX+0x1C8] + 0x1B0 ] at 0x544B56 / 0x57897B. Actual meaning and call side effects remain VERIFY.
  - A GATE: 0x544B5C CMP [EBX+0x1D0], EDI; EDI was zeroed at 0x544B3C (callee-save EDI convention assumed). If nonzero jump to 0x544B6D; else 0x544B64 TEST BYTE [ESI+0x1BC],1, if zero skip; in both eligible paths 0x544B6D CMP [ESI+0x194], EDI; equality skips helper.
  - B GATE: 0x578981 CMP [EBX+0x1D0],0; 0x578988 EAX=[ESP+0x18]; if nonzero jump 0x578997; otherwise 0x57898E TEST BYTE [EAX+0x1BC],1, zero skips; 0x578997 CMP [EAX+0x194],0, zero skips helper.
  - A CALLEE: 0x544BAB prepares zero ECX, EDX from 0x4678A0 result, pushes 3 DWORD args and calls 0x547FC0 at 0x544BB0; caller 0x544BB5 ADD ESP,0xC; joins 0x544BBE.
  - B CALLEE: 0x5789D4..0x5789E1 prepares 4 pushed DWORD args, ECX=EDX=0, calls 0x580280 at 0x5789E1; caller 0x5789E6 ADD ESP,0x10; joins 0x5789E9.
  - BOTH CONTINUE TO VIRTUAL+58: A 0x544BC5 and B 0x5789F0 call [Unit.vptr+0x58]. Only after callee return do A 0x544BC7 / B 0x5789F2 inspect Unit+0x1862C string length and conditionally compare count.
  - IMPLICATION: the two hit-handlers share the optional-helper gate but not the invoked callee/argument ABI. Do not collapse 0x547FC0 and 0x580280 into one proven equivalent effect, skip it when Unit+1D0 is nonzero, or assume the downstream virtual+58 or postlethal event has already returned.
  - VERIFY: real P pointer provenance; live Unit+1D0/+1C8 field semantics; helpers 0x547FC0/0x580280 inputs, side effects and normal returns; Unit virtual+58 receiver; outer Task callback/old EXE strict golden. No 5-method new Evidence ID (0) and no new VERIFIED function.
  - NEXT: WRQ-20261013-REA-DEATH; inspect already authorized saved callee/return evidence for 0x547FC0 and 0x580280 before connecting each to 0x575A60->0x575DF0->0x5684B0, and seek independent normal-return receipts. Do not promote to full gameplay VERIFIED.
- **Limitations:** - COMMON BEFORE-GATE: A 0x544B4A and B 0x57896F push Unit EBX then call 0x588470; both copy AL into byte [ [EBX+0x1C8] + 0x1B0 ] at 0x544B56 / 0x57897B. Actual meaning and call side effects remain VERIFY. / - VERIFY: real P pointer provenance; live Unit+1D0/+1C8 field semantics; helpers 0x547FC0/0x580280 inputs, side effects and normal returns; Unit virtual+58 receiver; outer Task callback/old EXE strict golden. No 5-method new Evidence ID (0) and no new VERIFIED function.
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261016-1034-REPEAT-ARITY-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261016_1034_REPEAT_ABI_BRANCH_AUDIT.md`; actual SHA256 `070E32B44D289FCE35CC803DA623919ECD728E3A702C87F15B34BFB754843F4D`; 3982 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - SOURCE: exe/T012_DAMAGE_CALLER_CONTEXTS.txt, stored native x86 block 0x546BCC..0x546C79. Historical reported evidence-file SHA256 9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3 (not rehashed this run).
  - After 0x546BCC temporary initialization, 0x546BD2 calls resolver 0x4678A0 with ECX=[EBP+0x1DC], stores result as ESI at 0x546BD7.
  - 0x546BD9 reads DWORD [ESI+0x74]. Value 0 is replaced by 1 at 0x546BE0; negative values skip loop at 0x546BE7; positive values become EDI repeat count at 0x546BE9.
  - Each iteration 0x546BEB loads qword [ESI+0x1D8], then FLDZ/FUCOMPP/FNSTSW AX/TEST AH,0x44 at 0x546BF1..0x546BF7; JP 0x546C2C.
  - When x87 comparison completes normally, JP is not taken only for ordered equality to zero (C3=1,C2=0); unequal ordered or unordered cases take 0x546C2C (C3/C2 mask has even parity). Unmasked FP exceptions remain VERIFY.
  - Equality branch prepares two additional PUSH values at 0x546C08/09; calls 0x447150 at 0x546C0E and stores its x87 result as qword; then PUSH 0,PUSH 0,PUSH EBP, ECX=address of temporary data, EDX=ESI; calls 0x547FC0 at 0x546C22; caller ADD ESP,0x14 at 0x546C27.
  - Other branch at 0x546C2C pushes 0, [EBP+0x1E574], EBP; ECX=0, EDX=ESI; calls 0x547FC0 at 0x546C3A; caller ADD ESP,0xC at 0x546C3F.
  - Both paths join 0x546C42 DEC EDI/JNE 0x546BEB. If normal callees return, positive repeat count N thus makes N helper invocations; value 0 defaults to 1; negative count skips.
  - Important boundary: this caller is DIFFERENT from previously reviewed 0x5449B1/0x544B21/0x544BB0; do not treat all 0x547FC0 uses as an invariant 3-stack-argument ABI.
  - VERIFY: exact consumer use of fourth/fifth pushed words, 0x447150 effects, local pointer lifetime, invalid pointers/NaN/FP exception handling, side effects/normal returns of 0x547FC0 and 0x580280, reachable gameplay inputs and Task callback.
- **Limitations:** - MASTER last read checkpoint161, research DONE9/34, IN_PROGRESS21/34 VERIFY4/34; gameplay original EXE golden PASS0; strict MATCH0; game reimplementation rate NOT MEASURED. / - PREFLIGHT: Local read/list success, latest RUN_RESULT verified 4×5 evidence; active.lock absent in directory listing and java/Ghidra/REA absent in Local process list, CPU n/a/free memory unmeasured. One read-only PowerShell preflight had SyntaxError due nested shell variable expansion, so no current target/evidence SHA measurement; RECOVERY REA-RC-20261016-1034-PREFLIGHT-PARSER-01 OTHER/VERIFY. No heavy runner started; new Ghidra runtime0s.
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261016-1138-DEFERRED-STACK-ARGS-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261016_1138_DEFERRED_STACK_ARGS_AUDIT.md`; actual SHA256 `548F14577C271A817AF03954763D9186C671360CA684CCE46E862A493336D6AE`; 5607 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - # REA-20261016-1138-DEFERRED-STACK-ARGS-01 | 0x547FC0 caller stack reconciliation
  - SOURCE: exe/T012_DAMAGE_CALLER_CONTEXTS.txt lines 113-151 (native VA 0x546BD9..0x546C43), 0x547FC0 entry VA 0x547FC0..0x548099. SHA256 independently measured this run: 9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3.
  - CORRECTION to REA-20261016-1034-REPEAT-ARITY-01: 0x546C22 has five DWORDs in the eventual caller cleanup, but only THREE PUSHes immediately preparing 0x547FC0. The earlier two PUSHes at 0x546C08/09 precede and belong to the 0x447150 call. Five cleaned DWORDs alone do NOT establish a 5-argument formal ABI of 0x547FC0.
  - STACK proof (S=ESP immediately before 0x546C08, assuming ordinary return without callee ESP cleanup from 0x447150): 0x546C08 push EDX -> S-4; 0x546C09 push EAX -> S-8; 0x546C0E call 0x447150; 0x546C13 FSTP qword [ESP+0x28] -> local address S+0x20.
  - 0x546C17 push 0 -> S-12; 0x546C19 push 0 -> S-16; 0x546C1B push EBP -> S-20; 0x546C1C LEA ECX,[ESP+0x34] = S+0x20, exactly the previous FSTP qword; 0x546C20 EDX=ESI; 0x546C22 call 0x547FC0.
  - 0x546C27 ADD ESP,0x14 restores S; its 20-byte cleanup accounts for two deferred 0x447150 pushes PLUS three newer 0x547FC0 pushes. 0x546C2A joins 0x546C42; stack depth matches non-equality branch.
  - Non-equality/unordered branch: 0x546C2C loads ECX=[EBP+0x1E574]; PUSH 0 (0x546C32), PUSH ECX (0x546C34), PUSH EBP (0x546C35), XOR ECX (0x546C36), EDX=ESI (0x546C38); CALL 0x547FC0 (0x546C3A); ADD ESP,0xC (0x546C3F). Three immediate PUSHes and no deferred pushes.
  - Therefore the salient proven callsite difference is ECX=pointer to local qword built from 0x447150 versus ECX=NULL, and second immediate stack arg=0 versus [EBP+0x1E574]. Both supply immediate stack args [EBP, alternate, 0] in push order; infer callee argument order from push reversal.
  - 0x547FC0 saved prefix at 0x548000/0x548003 explicitly reads [EBP+0xC] and [EBP+8]; at 0x548006 uses EDX and 0x548008 saves ECX. No available saved prefix establishes fourth/fifth formal stack parameters or whole-callee exit paths.
  - VERIFY: 0x447150 calling convention, local qword consumer/bounds, all 0x547FC0 stack-slot accesses beyond saved prefix, handling of x87 invalid/NaN, normal return and side effects; never label 3-versus-5 formal ABI VERIFIED from stack cleanup.
  - Application: preserve branch-specific ECX data path and second pushed argument, and 0x546C42 repeat counter; do not invent five-argument overload or equate with 0x580280 or Unit.virtual+58 before callee/callback evidence.
  - NEXT: use only allowed saved callee evidence to locate 0x547FC0's [EBP+0x10] and any higher accesses or return; trace ECX local qword and compare with 0x580280 separately. Preserve Work NormalDisableFrame 0x575C52 return and T012/T013 ownership.
  - INDEPENDENT CALLER CHECK: exe/T012_ALLFUNC_FLOW_PROBE.txt native VA0x54722B/2C PUSH EDI/ESI -> 0x54722D CALL 0x447150 -> 0x547232 FSTP -> 0x547238 ADD ESP,8. This separate site directly demonstrates caller cleanup of the two 0x447150 pushes. SHA256 checked 6BD148AF2F2D5906252B2AF742DD59469AD507CE359AA9B8E6A958CC2D87CFB6.
  - SECOND DEFERRED-CLEANUP PATTERN: exe/T012_DAMAGE_CALLER_CONTEXTS.txt 0x57E3A1/0x57E3A6 PUSH two words for 0x447150; 0x57E3AC FSTP qword [ESP+0x30]; four new pushes at 0x57E3B0/B2/B4/B5 before 0x57E3BC CALL 0x580280; 0x57E3B6 LEA EDX,[ESP+0x40] points at the same qword after 4 pushes; 0x57E3C1 ADD ESP,0x18 cleans six words (two earlier+four fresh). This is an independent corroboration of deferred stack cleanup but NOT equivalent callee semantics.
  - UPDATED PRIORITY: distinguish 0x547FC0 ECX qword pointer plus 3 freshly pushed words from 0x580280 EDX qword pointer plus 4 freshly pushed words; do not merge the two separate call contracts. Both effects and normal return still VERIFY.
- **Limitations:** - Latest saved RUN_RESULT runs/20261011T153309850Z/RUN_RESULT.json REA6.1.0 + Ghidra12.1.4, four verified; README currently says runner pins REA6.4.0, version difference unmodified and VERIFY. / - UPDATED PRIORITY: distinguish 0x547FC0 ECX qword pointer plus 3 freshly pushed words from 0x580280 EDX qword pointer plus 4 freshly pushed words; do not merge the two separate call contracts. Both effects and normal return still VERIFY.
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261016-1240-ABI-W6-REFUSAL-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261016_1240_CALLSITE_ABI_AND_WAVE6_REFUSAL_RECONCILIATION.md`; actual SHA256 `F8A737A57CBEBA5B5E117F33DBB2D2723A94D6D06573A6734F3F6EF23F7D0243`; 4806 bytes.
- **Record class:** STATUS_AUDIT; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - [CONFIRMED SAVED X86 / CALLSITE] normal missile主loop 0x5472CD/CE/0x5472D1で PUSH loop_index=ESI / Unit+0x1E574 / Unit=EBP、0x5472D2 EDX=EBX(main Skill)、0x5472D4 CALL 0x547FC0、0x5472DA ADD ESP,0xC。
  - 主loopの+0x7C/+0x80 offset計算枝は 0x547284/0x5472B3 でECXを一時qwordへ設定し、無補正枝のみ0x5472CF XOR ECX,ECX。主/子のoffset優先・RNG条件と回数はB owner data/T012_BATTLE_CALC.md §56/§58既報なので、これら自体は新発見と再計上しない。
  - [CONFIRMED SAVED X86 / CALLSITE] child loop 0x547411..0x54741Eでも PUSH loop_index=EDI / Unit+0x1E574 / Unit=EBP の3 DWORD、EDX=ESI(child Skill)、ECX=一時qword pointerまたは0(0x547419)、CALL 0x547FC0、0x547424 ADD ESP,0xC。
  - [CROSS-FAMILY] allfunc近傍0x546F08/0A/0D PUSH 0 / Unit+0x1E570 / Unit=EBX、0x546F0B ECX=0、0x546F0E EDX=EDI、0x546F10 CALL 0x547FC0、0x546F15 ADD ESP,0xC。ここでは3番目の新規stack値=0でnormal主/子indexと異なる。
  - [CROSS-FAMILY] 別caller 0x546C22 は0x447150の2PUSH後に0x546C17/19/1Bで3PUSH(0,0,Unit)、ECX=&qword、EDX=Skill、ADD ESP,0x14で合計5PUSHを遅延解放。0x546C3A分岐では3PUSH(0,Unit+1E574,Unit)、ECX=0、EDX=Skill、ADD ESP,0xC。詳細・ABI誤解訂正は既存REA-20261016-1138を優先。
  - [INTERFACE RESTRICTION] 4 caller familyが各CALL直前に積む3 WORDとECX/EDX受渡の違いを整理しただけ。0x547FC0保存入口0x548000/003は[EBP+0xC]/[EBP+8]、0x548006/008はEDX/ECXを使うが、[EBP+0x10]が実際に消費されるか・追加2WORDが引数か・正式ABI/帰還・副作用は未証明。『indexをcalleeが利用』もVERIFY。
- **Limitations:** - [SYNC/MASTER] 保存sync progress_sync_20261011T153958076Z.json はW1=16/16 W2=10/10 W3=10/10 W4=12/12 W5=16/16、累計64/64 VERIFIED、P0=29/29・P1=35/35。今回新VERIFIED0、Ghidra info/pseudo/assembly/callers/callees新Evidence ID0。QUEUE/PROGRESS既往rename EPERMで表示旧値。最新MASTER checkpoint161・34Task DONE9/IN_PROGRESS21/VERIFY4。 / - [GAME] 旧未改変EXE実機golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。B既存成果と本caller interface照合は静的のみで、ゲーム機能の完走やスキル命中は不明。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261016-1430-AUX-POSTLOOP-STATUS-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261016_1430_AUX_POSTLOOP_VTABLE_STATUS.md`; actual SHA256 `EC9EC0781EE5B709F6C1C7D030518959A0484CFFA457FDC1EF50B6C062A7D366`; 4516 bytes.
- **Record class:** STATUS_AUDIT; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - SOURCE: exe/T012_DAMAGE_CALLER_CONTEXTS.txt、対象0x546B68..0x546C85。SHA256 9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3 を今回Localで再照合一致。
  - [CALLER FLOW] 0x546B6E CMP [eax+0xAC],[eax+0xA8] → 0x546B74 JE 0x546C45。補助処理反復より前のこの条件でも同じ終了側へ合流する。
  - 0x546BD9 skill+0x74の符号付きDWORDを取り、0は1へ置換、0x546BE7 JLE 0x546C45で負の値は反復を省略する。0は反復1回となる（callee正常帰還を条件）。
  - 反復された場合は0x546C22/0x546C3Aの分岐後0x546C42 DEC EDI;0x546C43 JNE 0x546BEB。回数消化後に同じ0x546C45へ合流する。
  - [COMMON TAIL] 0x546C45 EAX=[Unit+0x130]、0x546C4B FLD QWORD [0x63B260]。0x546C51 EDX=[Unit.vtable]、0x546C54 EDX=[EDX+0x80]。0x546C5A/5Bは同じEAXを2回PUSHし、0x546C5C..6Bはdouble値と2つのローカル領域アドレスを準備、0x546C6C ECX=Unit、0x546C6E CALL EDX。
  - CALL EDXが正常に戻れば0x546C70 MOV AL,1、レジスタ復元後0x546C79 RET 4。CALL先の返値をこの経路でTEST/CMPしていないため、AL=1はcall先の成功確認を意味しない。
  - [CONTRAST] 別の0x546C7C失敗出口は0x546C7F XOR AL,AL、復元後0x546C85 RET 4。先行分岐からこちらへ直接流入する例は0x546ADC JGE 0x546C7C。すべての異常退出・callee帰還条件を列挙したものではない。
  - [VERIFY] vtable+0x80実callee、単位内の0x130 pointerとlocal引数の意味、x87定数値、例外/コールバック帰還、0x547FC0第3引数の実消費、0x580280副作用、575A60→575DF0→5684B0の外側Task正常帰還。ゲームの動的効果・命中・BUG認定は行わない。
  - [DEDUP] 既存REA_20261016_1034/1138/1240の反復回数・stack cleanup・caller引数は新発見として再計上せず、既存B T012に同VA 0x546C45の記録検索結果0は検索範囲限定の事実。A-E資料はread-only。
  - [NEXT] P0: 許可済み保存済みvtable/caller x86から+0x80の特定とcall後の状態検査、0x547FC0第3引数の消費証拠の有無、正常死亡Task callbackへの接続を独立VERIFY。過去拒否操作は再試行しない。
- **Limitations:** - [MASTER/GAME] 正本最新checkpoint162、研究DONE9/34・IN_PROGRESS21/34・VERIFY4/34。旧未改変EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。 / - [NEXT] P0: 許可済み保存済みvtable/caller x86から+0x80の特定とcall後の状態検査、0x547FC0第3引数の消費証拠の有無、正常死亡Task callbackへの接続を独立VERIFY。過去拒否操作は再試行しない。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

### REA-20261016-1537-AUX-VIRTUAL80-BRIDGE-01

- **Original REA source:** `rea_lab/decomp_task/REA_20261016_1537_AUX_VIRTUAL80_CALLEE_BRIDGE.md`; actual SHA256 `1C4AD7F513D3B23B33AA949441C70838CEBDA2C727327A19B6DD4E2283D15D4B`; 5084 bytes.
- **Record class:** RESEARCH_QC; evidence classification STATIC/INFERRED/VERIFY, NOT CURATED.
- **Source-native facts:**
  - SOURCE caller: exe/T012_DAMAGE_CALLER_CONTEXTS.txt SHA256 9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3、VA0x546C45..0x546C79。
  - SOURCE callee: exe/T012_UNIT_VIRTUAL80_579290_NATIVE_20261013.txt file SHA256 FB5455359F51961EB266AB6CD7C1C5D524AF229E83C07E8920B72B63461023C7、元の隔離window SHA256 987AEA6A83ACA5EB4E8C00DDA70DC013414A28A233A9C437C1BC69650B8C847F、VA0x579290..0x5795CE。
  - [SAVED CALLER] 0x546C51 EDX=[Unit.vtable]; 0x546C54 EDX=[EDX+0x80]; 0x546C6C ECX=Unit; 0x546C6E CALL EDX。0x546B74と0x546BE7の補助反復skipも0x546C45の共通tailへ来る（前REA-1430の既知、重複増分にしない）。
  - [CONDITIONAL BINDING] 既存B保存契約はUnit系候補vtable VA0x63A9E4/0x63A8E4のslot+0x80が0x579290、別表0x63A4BCのslot+0x80は0x544F80と記録。0x546C6E時点のlive Unit vptrを固定できないため、常に0x579290へ行くとは未証明。
  - [CALL ARG1/2] 0x546C62 LEA EAX,[ESP+0x20]→0x546C66 PUSH = localPointB、0x546C67 LEA ECX,[ESP+0x2C]→0x546C6B PUSH = localPointA。仮にcalleeが0x579290なら [callee EBP+8]=pointA, [+0xC]=pointB。
  - [CALL ARG3] 0x546C4B FLD qword [0x63B260]→0x546C5C SUB ESP,8→0x546C5F FSTP qword [ESP]。仮callee [EBP+0x10]に8byte scaleが渡る（定数の実数値/例外は未確認）。
  - [CALL ARG4/5] 0x546C45 EAX=[Unit+0x130]→0x546C5A/5B PUSH EAX twice。仮callee [EBP+0x18]と[EBP+0x1C]が同一current Unit+0x130値。近傍0x546B35/3B/43はその指す先の+0x24C/+0x27Cを参照しSkill形状を支持。
  - [B CALLEE CONSEQUENCE / CONDITIONAL] 0x579296 MOV EAX,[EBP+0x1C]→0x5792A3 Unit+0x1E49C writer。0x5792C1/CE/D4は[EBP+0x18]のSkill+0x264をUnit+0x1E4ACへ。0x5792A9 byte+0x186D0=1、0x5792B2/BB pointB XY→+0x1E4A4/+0x1E4A8。適合vtableが確定した場合に限り、このcallerの同一+0x130 pointerの2役を示す。
  - [STACK/RETURN] Caller outgoing two DWORD(8)+qword(8)+two local pointers(8)=24bytes、0x546C6E直後にADD ESP無し。保存B callee唯一の正常出口0x5795CE RET0x18は24byte callee cleanupと整合。その正常帰還後にcaller0x546C70 MOV AL,1 / 0x546C79 RET4、calleeの成功flagを検査していない。
  - [VERIFY] 0x546C6Eのlive vptr、別subtypeの+0x80実装、0x63B260 double値、pointA/Bローカル初期化とその後の可視使用、calleeの全例外帰還、0x547FC0実引数、0x580280副作用、0x575A60→0x575DF0→0x5684B0通常死亡Task callback。ゲーム動的golden未実施。
- **Limitations:** - [VERIFY] 0x546C6Eのlive vptr、別subtypeの+0x80実装、0x63B260 double値、pointA/Bローカル初期化とその後の可視使用、calleeの全例外帰還、0x547FC0実引数、0x580280副作用、0x575A60→0x575DF0→0x5684B0通常死亡Task callback。ゲーム動的golden未実施。 / - [MASTER/GAME] 2026-10-16 MASTER checkpoint163、34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Stage:** PUBLISHED_INTAKE/OWNER_AUDIT, Golden PASS 0, READY 0; prior blocked operation remains safety-hold with no denied evidence acquired.

## Ownership and corrections

Previously known functions/calls and Work implementation interfaces cannot be relabeled as new native findings. Curator must independently verify current V9/ASM, original source SHA, prior owner corrections, privacy and tests. Shared develop/REF/dictionaries not modified. Forbidden Wave6/VA materials remain blocked.
