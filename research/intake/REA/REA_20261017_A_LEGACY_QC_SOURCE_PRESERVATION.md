# REA 20261017 A: legacy owner research / safe QC intake

**PRIVATE REA owner source preservation, STATIC/INFERRED/VERIFY or STATUS_ONLY; NOT CURATED/READY.** All 7 original reports have source research IDs and were hashed read-only 2026-11-02 JST. Historical evidence snippets are taken from already saved owner Markdown (not newly acquired x86 or original-game behavior). Sections referring to safety-refused operations/results/targets are excluded from the excerpt; metadata remains status/BLOCKED. No source PE or V9 rehash, new runner, formal 5-method verification, or original gameplay test. Original Golden PASS=0, READY=0.

### REA-20261017-0837-V80-SCALE-0P9-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_0837_VIRTUAL80_SCALE_LITERAL_0P9.md`; source SHA256 `41811185F6CDBC61C05B1BFC1213A81B103590008454EC9B0599085C868EF493`, 4445 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [STATIC CONST CONFIRMED] 承認済copy PE32 ImageBase=0x00400000、VA=0x0063B260は`.rdata` RVA=0x23B260/raw offset=0x23A660。8bytes little-endian `CD CC CC CC CC CC EC 3F`=IEEE754 binary64 bits `0x3FECCCCCCCCCCCCD`=`0.9`。read-only FileStream/BinaryReaderで該当8bytesのみを読み、再hash一致。Ghidra新しい5種結果ではない。
  - [CALLER PROVENANCE] 既保存 `exe/T012_DAMAGE_CALLER_CONTEXTS.txt` SHA256=`9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3`。0x546C4B `FLD qword [0x63B260]`→0x546C5C `SUB ESP,8`→0x546C5F `FSTP qword [ESP]`→0x546C6E `CALL [Unit.vtable+0x80]`。8-byte第三実引数は0.9（通常FPUロード/ストアが正常完走する条件）。値が未知だった前回記録を限定更新する。
  - [CONDITIONAL CALLEE] `exe/T012_UNIT_VIRTUAL80_579290_NATIVE_20261013.txt` SHA256=`FB5455359F51961EB266AB6CD7C1C5D524AF229E83C07E8920B72B63461023C7`。もしlive vptr slot+0x80が0x579290なら、callee 0x579321は[EBP+0x10]の同0.9をFLDし、0x579327 `FMUL ST(1),ST(0)`で0x5E3B70後の距離候補に0.9を乗ずる。0x579341以降Skill+0x40=1/5やUnit+0x228等で分岐・補正があるので最終移動距離・弾速を0.9倍と断定しない。
  - [LOCAL POINTS / PATH LIMITED] 0x546A83..0x546A96はUnit=EBPの矩形centerX=(left+((right-left)>>1))とbottomYを初期ESP+0x18/+0x1Cへ格納。0x546A9A..0x546AAFはUnit+0x1E570から得た対象のcenterX/bottomYを、PUSH2後のESP+0x18/+0x1C（元ESP+0x10/+0x14）へ格納。0x546AD6で一時PUSH2を解放。0x546B74 JE→0x546C45 の直行枝では0x546BBEの別の`SUB ESP,0x1C`を通らないため、546C62 pointer B=元ESP+0x10（対象）、546C67 pointer A=元ESP+0x18（自Unit）と一致。補助取得枝や他callerへ一般化しない。
  - [ABI BOUNDARY] 0x546C6E時点のlive Unit vptr未固定。0x63A9E4/0x63A8E4のslot+0x80=0x579290、別表0x63A4BCは0x544F80（B既存）。具体的なUnit型・0x544F80の処理はVERIFY、normal returnも未証明。今回0.9を実ゲーム倍率・軌道演出確定と誤認しない。
  - [SOURCE CLASS] 新規証拠ID `REA-20261017-0837-V80-SCALE-0P9-01` は許可済みコピーの静的byte/保存済ASMの再照合receipt。Ghidra info/pseudo/assembly/callers/calleesの新ev_* evidence IDは0、関数5種の新VERIFIED0。旧ゲームGolden PASS0/strict MATCH0。ゲーム再実装率は測定していない。
  - [NEXT P0] 保存済み異なるUnit vtableの実this到達判定、0x546BBE経由のpoint A/B保持、0x547FC0の第3stack実消費、0x580280の正常帰還、通常死亡0x575A60→0x575DF0→0x5684B0の既保存callback完走根拠を重複なくVERIFY。B所有READYやゲームstrict PASSを代理作成しない。
- **Source caveats/errata:** - [ABI BOUNDARY] 0x546C6E時点のlive Unit vptr未固定。0x63A9E4/0x63A8E4のslot+0x80=0x579290、別表0x63A4BCは0x544F80（B既存）。具体的なUnit型・0x544F80の処理はVERIFY、normal returnも未証明。今回0.9を実ゲーム倍率・軌道演出確定と誤認しない。 / - [NEXT P0] 保存済み異なるUnit vtableの実this到達判定、0x546BBE経由のpoint A/B保持、0x547FC0の第3stack実消費、0x580280の正常帰還、通常死亡0x575A60→0x575DF0→0x5684B0の既保存callback完走根拠を重複なくVERIFY。B所有READYやゲームstrict PASSを代理作成しない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-0939-AUX-POINT-REBASE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_0939_AUX_POINT_STACK_REBASE.md`; source SHA256 `95EC81A62DAEFAAC44042D9536E75DF634647C0F9A8952CAAA37E747315E81D0`, 4406 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - # REA-20261017-0939-AUX-POINT-REBASE-01｜0x546C6E の枝別pointポインタ再基準化
  - [SOURCE] exe/T012_DAMAGE_CALLER_CONTEXTS.txt SHA256=9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3（本run照合）。exe/T012_UNIT_VIRTUAL80_579290_NATIVE_20261013.txt SHA256=FB5455359F51961EB266AB6CD7C1C5D524AF229E83C07E8920B72B63461023C7、B detail SHA256=3177992D5829E2C359E6C851D4B2DA1505BD39AB56B54C9B22FC7F21FD26589A、3点とも今回一致。
  - [DIRECT] 0x546B74 JE 0x546C45は0x546BBE SUB ESP,0x1Cを通らない。0x546C45開始時ESP=Sと定義すると、PUSH [Skill]×2→S-8、SUB ESP,8→S-16、0x546C62 LEA B=[ESP+0x20]=S+0x10、Bをpush後0x546C67 LEA A=[ESP+0x2C]=S+0x18。0x546A83..AFで作成したtarget/selfの座標と一致するのは、この枝の正常なESP収支を前提とした範囲のみ（既0837メモ）。
  - [SCRATCH] 0x546B7E/+0x8Cか0x546BB9選択後は0x546BBE SUB ESP,0x1C→S-0x1C、0x546BC1 ESI=ESP、0x546BC7 CALL 0x4051D0、0x546BD2 CALL 0x4678A0へ進む。0x546C27 ADD ESP,0x14と0x546C3F ADD ESP,0xCは各loop callsiteのpush数と釣り合い、通常帰還なら共通tail入口ESP=S-0x1Cのまま。
  - [REBASING] SCRATCH枝で0x546C5A/5B PUSH×2→S-0x24、0x546C5C SUB8→S-0x2C。0x546C62 B=[ESP+0x20]=S-0x0C=新規scratch+0x10、次のPUSH後0x546C67 A=[ESP+0x2C]=S-0x04=新規scratch+0x18。両pointの参照先はDIRECT枝のS+0x10/+0x18とは**0x1C bytes異なる**。
  - [NORMAL RETURN / ABI] 0x546C6E Unit.vtable+0x80へのoutgoing24bytesは、calleeが0x579290の場合、[EBP+8]=A、[+0xC]=B、[+0x10]=0.9 double、[+0x18/+0x1C]=同一Skill系pointer。0x5795CE RET0x18は24byte cleanupと整合。ただしlive vptrを確認しておらず0x544F80別候補あり。
  - [DELTA/DEV CONSEQUENCE] 既0837メモのDIRECT枝のself/target point対応を、選択済みscratch枝へ**流用しない**ことを新たに証拠化。0x4051D0の出力とscratch+0x10/+0x18の中身・初期化完了、例外時ESP、calleeの正常帰還・後段見た目はVERIFY。scratchの両pointが必ず原座標/別座標のどちらかとも断定しない。
- **Source caveats/errata:** - [DELTA/DEV CONSEQUENCE] 既0837メモのDIRECT枝のself/target point対応を、選択済みscratch枝へ**流用しない**ことを新たに証拠化。0x4051D0の出力とscratch+0x10/+0x18の中身・初期化完了、例外時ESP、calleeの正常帰還・後段見た目はVERIFY。scratchの両pointが必ず原座標/別座標のどちらかとも断定しない。 / - [MASTER/GOLDEN] 最新MASTER checkpoint165、研究34 Task DONE9/IN_PROGRESS21/VERIFY4。旧未改変EXE gameplay golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-1031-SCRATCH-POINT-BOUNDARY-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_1031_SCRATCH_POINT_PAIR_BOUNDARY.md`; source SHA256 `3CF18CFFBE0F36FF1C10F0FA0A10C6A1C3AB01412994885328A33820D32EECC5`, 4661 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [SOURCE CALLER] exe/T012_DAMAGE_CALLER_CONTEXTS.txt SHA256=9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3。本回Get-FileHash一致。
  - [SOURCE CONDITIONAL CALLEE] exe/T012_UNIT_VIRTUAL80_579290_NATIVE_20261013.txt SHA256=FB5455359F51961EB266AB6CD7C1C5D524AF229E83C07E8920B72B63461023C7、B契約data/T012_UNIT_VIRTUAL80_579290_CONTRACT_20261013.md SHA256=3177992D5829E2C359E6C851D4B2DA1505BD39AB56B54C9B22FC7F21FD26589A。今回一致。live subtype/slotはVERIFY。
  - [ADDRESS MODEL] S=0x546BBE SUB ESP,0x1C直前のESP。通常stack-preserving call帰還を仮定。補助枝0x546BBE後はscratch基底=S-0x1Cで、0x546C45共通tailまでSUB0x1Cを戻すADDは見えない。直行枝0x546B74 JEではこのSUB自体なし。
  - [POINT PTR RECHECK] 補助枝0x546C62 B=ESP+0x20(scratch+0x10=S-0x0C)、0x546C67 A=次のPUSH後ESP+0x2C(scratch+0x18=S-0x04)。直行枝はB=S+0x10、A=S+0x18（REA-20261017-0939で既報）。
  - [NEW 8-BYTE SPAN] calleeが0x579290であれば、Bは0x5792B0/0x5792B8と0x5792FB/0x5792FDでDWORD×2を参照：補助枝ではscratch+0x10と+0x14、両方とも28byte領域内。Aは0x579300/0x579303/0x579306と0x57942C/0x57942F/0x579431でDWORD×2を参照：補助枝ではscratch+0x18（末尾4byte）とscratch+0x1C=S（scratch領域の直後4byte）。
  - [UNRESOLVED CONTENT] scratch+0x10/+0x14/+0x18と旧slot[S+0]のwriter/初期化・0x4051D0/0x4678A0正常return/例外cleanup・callee 0x544F80側の実読幅・呼出時live vptr未確定。callee 0x579290への条件付き推論であり、ゲーム内可視軌道・距離倍率は未検証。
  - [NEXT] 最優先：許可済み保存済x86からscratch+0x10/+0x14/+0x18と[S+0] writer/0x4051D0出力、vtable+80 subtypeを追加照合。次いで0x547FC0/0x580280既存正常帰還・0x575A60→0x575DF0→0x5684B0の外側callback未解明境界。未証明のRETURNやゲーム進捗をREADY/DONEにしない。
- **Source caveats/errata:** - [MASTER/GOLDEN] MASTER最新checkpoint165・研究34 Task DONE9/IN_PROGRESS21/VERIFY4。旧未改変EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。 / - [NEXT] 最優先：許可済み保存済x86からscratch+0x10/+0x14/+0x18と[S+0] writer/0x4051D0出力、vtable+80 subtypeを追加照合。次いで0x547FC0/0x580280既存正常帰還・0x575A60→0x575DF0→0x5684B0の外側callback未解明境界。未証明のRETURNやゲーム進捗をREADY/DONEにしない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-1133-AUX-POINT-447150-QWORD-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_1133_AUX_GEOMETRY_QWORD_CALLSITE_CROSSWALK.md`; source SHA256 `ABE729812798280B4A7AC09BE85360891F37C23C8AEF9BE85F6A5FB33D65466C`, 4772 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [EVIDENCE] `exe/T012_DAMAGE_CALLER_CONTEXTS.txt` SHA256 `9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3` を本回再hash一致。VA 0x546BBE..0x546C3F。補足既存証拠 `REA_20261017_0939_AUX_POINT_STACK_REBASE.md`・`REA_20261017_1031_SCRATCH_POINT_PAIR_BOUNDARY.md`・`REA_20261016_1138_DEFERRED_STACK_ARGS_AUDIT.md`。
  - [STACK BASIS] S=0x546BBE `SUB ESP,0x1C` 直前ESP、通常の呼出/帰還時のstack保存を仮定。補助scratch基底はS-0x1C。A=(DWORD[S-4],DWORD[S])、B=(DWORD[S-0xC],DWORD[S-8])と既存メモのpoint対を明記。
  - [NEW CALLER INPUT] 0x546BFC `EDX=[ESP+0x1C]=A.y`; 0x546C00 `EAX=[ESP+0x18]=A.x`; 0x546C04 `ECX=[ESP+0x10]=B.x`; 0x546C08/09 `PUSH A.y`, `PUSH A.x`; 0x546C0A `EAX=[ESP+0x1C]=B.y`（2push後のESPで再評価）; 0x546C0E `CALL 0x447150`。したがってcallerはAをstack、BをECX/EAXとして準備する。callee内部演算や正式ABIは未確定。
  - [NEW RESULT BRIDGE] 上記push2個後のESP=S-0x24。0x546C13 `FSTP QWORD [ESP+0x28]` の書込先は `[S+4..S+0xB]`（scratch直後より更に4byte上）。続く0x546C17/19/1Bで3pushしESP=S-0x30。0x546C1C `LEA ECX,[ESP+0x34]` は同じ `[S+4]` へのpointer。0x546C22 `CALL 0x547FC0` にECXで渡す。実際の0x547FC0消費/帰還はVERIFY。
  - [STACK BALANCE] 0x546C27 `ADD ESP,0x14`で2個の先行`0x447150`用pushと3個の`0x547FC0`直前push、計20byteを解放しESPはS-0x1Cに戻る（両callee正常復帰を条件）。分岐0x546C2C→3push→0x546C3A→ADD ESP,0xCも同じ深さで合流。
  - [SEPARATE OUTPUT SLOT] 0x546BC3 `MOV [ESP+0x48],ESP` はscratch基底S-0x1Cを別slot `[S+0x2C]`へ記録し、前述A.y=[S]や結果qword=[S+4]のwriterではない。この窓の保存情報だけでA.y=[S]の初期化元を確定しない。
  - [BRANCH GATE] 0x546BF7/FA `TEST AH,0x44; JP 0x546C2C` の非遷移側だけが0x447150→結果qword→547FC0を通る。遷移側は0x546C32/34/35の3push、ECX=0、EDX=ESIで547FC0へ直接渡す。x87 flagsのゲーム上の意味と例外パスは未確認。
  - [LIMITATIONS] 0x4051D0/0x4678A0によるscratchのwriter、A.y=[S]の値、0x447150内部の計算、0x547FC0第3正式stack引数の消費・正常return、vtable+0x80のlive型はVERIFY。0x575A60→575DF0→5684B0外側callbackも未完。完走や弾/命中/HP/MP/RNG・動的可視ゲーム性は証明しない。
- **Source caveats/errata:** - [LIMITATIONS] 0x4051D0/0x4678A0によるscratchのwriter、A.y=[S]の値、0x447150内部の計算、0x547FC0第3正式stack引数の消費・正常return、vtable+0x80のlive型はVERIFY。0x575A60→575DF0→5684B0外側callbackも未完。完走や弾/命中/HP/MP/RNG・動的可視ゲーム性は証明しない。 / - [MASTER / GAME] MASTER最新checkpoint166、研究34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-1238-DIRECT-POINT-ORIGIN-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_1238_DIRECT_BRANCH_POINT_ORIGIN_CROSSWALK.md`; source SHA256 `F46D88652C3C65BAED5A868F61D3858A77043126FE5D8ADF352579A79A3C5F63`, 5096 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [PRIMARY SOURCE] exe/T012_DAMAGE_CALLER_CONTEXTS.txt SHA256 9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3（今回再hash一致）、VA 0x546A83..0x546C6E。
  - [INDEPENDENT RETURN EVIDENCE] rea_lab/results/run_20261009T175957025Z_550E70_assembly.json、SHA256 DD13253E385C1F3F5B292C5C29066ECF6883285801EC938E7DAFB68D3AAD8A46、Ghidra evidence_id ev_d4f259d6f70f56eb5bf60484f7ac0a551684b9cb2488e87248609be43b78f59d。正常出口0x551481 RET 0x8。新規取得ではない。
  - [STACK MODEL] S=0x546BBE SUB ESP,0x1Cの直前ESP。以下は中間calleeが通常にスタックを戻す経路だけで成立。直行枝0x546B74→0x546C45はこのSUB自体を実行しない。
  - [POINT A ORIGINAL WRITERS] 0x546A83 EAX=[EBP+0x40]、0x546A86 EDX=[EBP+0x48]、0x546A89 EDI=[EBP+0x4C]、0x546A8C/8E/90でX=(x48-x40 arithmetic_shift_right_1)+x40。0x546A92 [ESP+0x18]=X、0x546A96 [ESP+0x1C]=Y([EBP+0x4C])。通常のSと同じ深さならA=(S+0x18,S+0x1C)。
  - [POINT B ORIGINAL WRITERS] 0x546A9A..A0はPEER=[EBP+0x1E570]の+0x40/+0x48/+0x4Cを使用し、0x546AA3/AA5/A7でX中点を算出。0x546AA9/AAAの2 PUSH後0x546AAB [ESP+0x18]=X、0x546AAF [ESP+0x1C]=Yなので、元のS基準ではB=(S+0x10,S+0x14)。
  - [CALL BALANCE] 0x546AB3 CALL 0x447180後0x546AD6 ADD ESP,8が2 PUSHを解放。条件付き0x546B51/52の2 PUSH→0x546B53 CALL 0x550E70は保存Ghidra正常出口RET8と整合。0x546B85..BBEまで他にcaller側pushの恒久的増減は確認されない（各callee正常帰還が前提）。
  - [DIRECT BRANCH GATE] 前段の合法な実行で0x546B64 CMP [EBP+0x130]+0x9C,ESI（先行0x546AE5 XOR ESI,ESI）→0x546B66 JNEなら補助側。+0x9C==0で0x546B68/6Eの+0xA8/+0xAC比較が等しいと0x546B74 JE 0x546C45で直行する。さらに外側gateあり、ここだけでゲーム上の到達条件を確定しない。
  - [DIRECT TAIL REBASE] 直行時ESP=S。0x546C5A/5B PUSH EAX×2、0x546C5C SUB ESP,8後ESP=S-0x10。0x546C62 LEA EAX,[ESP+0x20]=S+0x10(B)→PUSH、0x546C67 LEA ECX,[ESP+0x2C]=S+0x18(A)→PUSH、0x546C6E CALL vtable+0x80。したがって保存命令が渡すポインタ元はA=EBP側XY、B=[EBP+0x1E570]側XY。
  - [LIMITS] 0x4051D0後のscratch writer、PEER実型と座標意味、virtual+0x80のlive callee、全callee/異常returnと実ゲーム入力到達は未確定。座標が演出・射撃等の最終出力になることは未証明、正常returnを偽装しない。
  - [EVIDENCE CLASS] 新規独立REA分析メモ1件、Ghidra 5種info/pseudo/assembly/callers/calleesの新ev_* ID 0、新VERIFIED関数0。
  - [NEXT] 0x4051D0と0x447150の合法保存済x86証拠で補助scratchの初期値とcallsite境界を確認し、0x547FC0の引数消費・正常帰還、死亡処理0x575A60→0x575DF0→0x5684B0外側callbackはVERIFY維持。
- **Source caveats/errata:** - [MASTER / GAME] 最新E checkpoint167、研究34件 DONE9/IN_PROGRESS21/VERIFY4。旧原作EXE実機Golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。 / - [NEXT] 0x4051D0と0x447150の合法保存済x86証拠で補助scratchの初期値とcallsite境界を確認し、0x547FC0の引数消費・正常帰還、死亡処理0x575A60→0x575DF0→0x5684B0外側callbackはVERIFY維持。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-1340-447150-STACK-REUSE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_1340_447150_STACK_REUSE_CROSSCALL.md`; source SHA256 `958A309674D18257EE4C0DDAF838111373540766AA9F0905EF217A4226CD5EB5`, 4631 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [PRIMARY] exe/T009_CAPACITY_CLAMP_PROBE.txt SHA256 56427A137B0E9CB6CF85DFE8A8D95CC8AA7BF4472208111C125D0A8540F148B5、保存VA 0x57DE35..0x57DE65。Local読み取り専用hash照合。
  - [COMPARE-A] exe/T012_ALLFUNC_FLOW_PROBE.txt SHA256 6BD148AF2F2D5906252B2AF742DD59469AD507CE359AA9B8E6A958CC2D87CFB6、VA 0x547223..0x547238。
  - [COMPARE-B] exe/T012_DAMAGE_CALLER_CONTEXTS.txt SHA256 9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3、VA 0x546BFC..0x546C27。3保存ファイルを今回Localで読取、SHAを再確認。
  - [SAVED WINDOW A] 0x547223 MOV EAX,[ESP+24]、0x547227 MOV ECX,[ESP+20]、0x54722B/2C PUSH EDI/ESI → 0x54722D CALL 0x447150 → 0x547232 FSTP QWORD [ESP+38] → 0x547238 ADD ESP,8。
  - [SAVED WINDOW B / ALREADY KNOWN] 0x546C08/09の2 PUSH → 0x546C0E CALL 0x447150 → 0x546C13 FSTP QWORD → 3後続PUSHと0x547FC0 → 0x546C27 ADD ESP,0x14。既REA-20261017-1133を再成果計上しない。
  - [NEW COMPARISON / TEMP DEPTH] 0x57DE49 SUB ESP,8 → 0x57DE4E FSTP QWORD [ESP]で既存8-byte slotを用意し、0x57DE51/52 PUSH EBP/EBX → 0x57DE53 CALL 0x447150。CALL前にEAX,ECXも設定される。
  - [NEW POST-CALL SLOT REUSE] 0x57DE58 FADD QWORD [0x62A190] → 0x57DE5E LEA ESI,[ESP+0x20] → 0x57DE62 FSTP QWORD [ESP] → 0x57DE65 CALL 0x420900。CALL447150直後から0x420900直前までADD ESPがない。
  - [CONDITIONAL STACK MODEL] 0x447150が上記比較callsite A/Bどおり8-byte caller-cleanup（通常のCALL/RET）なら、57DE53への2 DWORD PUSHは57DE62で一つのqword結果slotに上書きされ、その直後に57DE49の別qword slotが連続して残る。57DE65のcallee 420900がどちらをどう消費するかは未確認。
  - [IMPORTANT DELTA] この第三callerでは447150の戻りを単に別ローカルへ保存するのでなく、押し込んだ2 DWORDの**同じスタック位置に戻りqwordを重ねる**可能性を、独立した保存命令で確認した。447150の式・幾何学的意味・420900の正式ABI/副作用はVERIFY。結果を距離・角度・成功と命名しない。
  - [EVIDENCE] 本メモID REA-20261017-1340-447150-STACK-REUSE-01（REA-owned分析receipt）。新規Ghidra info/pseudo/assembly/callers/callees ev_* 取得0、関数5手法の新VERIFIED0、ゲーム旧EXE実行0。
  - [NEXT] WRQ-REA-DEATHの正常死亡0x575A60→0x575DF0→0x5684B0の未解決callback帰還を、合法保存証拠から独立照合。0x547FC0/0x580280引数消費・正常帰還、447150/420900のcallee境界は未確定とする。
- **Source caveats/errata:** - [IMPORTANT DELTA] この第三callerでは447150の戻りを単に別ローカルへ保存するのでなく、押し込んだ2 DWORDの**同じスタック位置に戻りqwordを重ねる**可能性を、独立した保存命令で確認した。447150の式・幾何学的意味・420900の正式ABI/副作用はVERIFY。結果を距離・角度・成功と命名しない。 / - [MASTER/GOLDEN] 最新MASTER checkpoint168、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-1440-V80-OPTIONAL-ARG-PATH-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_1440_V80_OPTIONAL_ARG_BRANCH_CROSSCALL.md`; source SHA256 `5A2AA4ABFB91C8A3721BF429E919664958F1CD4ACC0724A7C24E8A9D36938866`, 4644 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [SOURCE A] exe/T012_DAMAGE_CALLER_CONTEXTS.txt SHA256 9A2ED3B4DAA72ECB2D32511471BBDD18CC1E883EC5CFBCD31B4FD6B1A4566CA3（2026-10-17 14:40 JST Local再hash一致）。VA 0x57E37C..0x57E3FB、および対照0x546C45..0x546C79。
  - [SOURCE B] exe/T012_UNIT_VIRTUAL80_579290_NATIVE_20261013.txt SHA256 FB5455359F51961EB266AB6CD7C1C5D524AF229E83C07E8920B72B63461023C7（同時再hash一致）。VA 0x579290..0x5792A3、0x5795CE RET0x18。
  - [BRANCH A] 0x57E376/37Cの0x4678A0戻り値がESI。0x57E381 CMP byte [EBX+0x26F],0；0x57E38A JNE不成立なら0x57E38C PUSH ESI→0x57E3D9へ直接合流。これはvirtual+80呼出に渡る最後のDWORD候補をESIにする。
  - [BRANCH B] byte[EBX+0x26F]!=0なら0x57E38Fへ。ESI+0x74==0の枝は0x57E3BC CALL0x580280→0x57E3C1 ADD ESP,0x18→0x57E3D7、非0の枝は0x57E3CF CALL0x54F720→0x57E3D4 ADD ESP,0xC→0x57E3D7。双方、各callee正常帰還時には0x57E3D7 PUSH 0→0x57E3D9。
  - [SAME DEPTH] 0x57E3D9には上記2経路で1 DWORDを積んだ状態で合流（前段caller-cleanupとcallee正常帰還を条件）。0x57E3D9 FLD qword [ESP+0x24] のscaleはcaller側stackから読み、0x546C4Bの絶対定数0x63B260(既確認double0.9)とは由来が異なる。前者の実数値は未確定。
  - [SHARED OUTGOING] 0x57E3E6 PUSH EBX、0x57E3E7 SUB ESP,8→57E3EA FSTP qword [ESP]、0x57E3ED/57E3F2の2点ポインタPUSH→0x57E3F9 Unit.vtable+0x80へCALL。先行ESI/0(4)+EBX(4)+scale(8)+point×2(8)=24bytesで、正常bindingが0x579290ならRET0x18と整合。
  - [CONDITIONAL CALLEE] live vptr+0x80==0x579290の場合だけ、callee [EBP+0x1C]=ESIまたは0、[EBP+0x18]=EBX。0x579296 MOV EAX,[EBP+0x1C]→0x5792A3 MOV [Unit+0x1E49C],EAXにつながる。したがって同一callerの枝によってUnit+0x1E49Cへ書く候補値が異なる。
  - [COMPARE] 0x546C5A/5BではUnit+0x130を2回PUSHするため、0x546C6Eの候補callee 0x579290は[EBP+0x1C]と[+0x18]の双方に同一pointerを受ける。57E3F9ではEBXと別のESI/0を渡す。2 callerの引数を同一テンプレートに正規化しない。
  - [LIMIT] 実Unit vptr、0x544F80等の他slot実装、57E3D9のlocal qword writer、ESIの実identity、0x580280/0x54F720の内部副作用/異常帰還、virtual+80の可視効果はVERIFY。成功や弾数・HP・MP・RNG一致と断定しない。既Bの既知単体命令や前回の546C6E ABIは再成果計上0。
  - [NEW RECEIPT] 新規REA分析ID REA-20261017-1440-V80-OPTIONAL-ARG-PATH-01（本ファイル）。新規Ghidra info/pseudo/assembly/callers/callees evidence ID 0件、新規静的証拠VERIFIED関数0件。
  - [NEXT P0] WRQ-REA-DEATHの通常死亡 0x575A60→0x575DF0→0x5684B0 から外側callback/正常帰還を保存証拠で確認。次いで0x57E3F9 live vptr/枝別source qwordと0x547FC0・0x580280のABI/副作用をVERIFY。別レーン/T018/原本/Work/WRQ/Git/push/設定/automationは変更しない。
- **Source caveats/errata:** - [MASTER/GAME] MASTER checkpoint168（最新末尾にE-RC-20261017-1344-CP169-MASTER-SAFETY-01：cp169未保存/BLOCKED）。研究34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。 / - [NEXT P0] WRQ-REA-DEATHの通常死亡 0x575A60→0x575DF0→0x5684B0 から外側callback/正常帰還を保存証拠で確認。次いで0x57E3F9 live vptr/枝別source qwordと0x547FC0・0x580280のABI/副作用をVERIFY。別レーン/T018/原本/Work/WRQ/Git/push/設定/automationは変更しない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

## Required KB curator processing

Compare original source SHA, VA/ASM and correction history before consuming any interpretation in REF/symbols. Later owners' corrections outrank older static hypotheses; Work implementation gates are not original game behavior. Do not publish denied evidence, original PE/DAT/SAVE or personal paths. No develop/other-owner writes by REA.
