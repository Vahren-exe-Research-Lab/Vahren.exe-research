# REA legacy unkeyed T014 static source recovery — 2026-10-21/22

**Stage: SOURCE_PRESERVED_UNKEYED / OWNER_REVIEW / NOT CURATED.** These 16 historical REA-owned `T014` static Markdown documents have no identifiable `REA-LOCAL-...`/ `REA-OFFLINE-...` ID in their source text. They must **not** be counted as 16 new research IDs, function proofs, or formally verified findings. Their filename + actual report byte SHA256 form a stable temporary recovery key. They may duplicate an earlier T014 source or later REA/KB claim; curator must compare full text and original VA/meaning with `REF_SAVE_FORMAT.md`, `REF_SAVE_PERSISTENCE.md`, existing T014 source IDs and corrected native V9 evidence. Only owner-approved static excerpts and PC-only evidence hash candidates are preserved here.

No game or REA/Ghidra new execution, original PE/V9 SHA rerun, or simulation was conducted. No original data, raw logs, denied evidence, absolute sensitive path or generated SQLite is published. Formal new five-method VERIFIED 0, original Golden PASS 0, READY 0.

### SOURCE_KEY: `REA_20261021_1735_T014_SENTRY_EOFBIT_V34_CONTRAST_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261021_1735_T014_SENTRY_EOFBIT_V34_CONTRAST_STATIC.md`; actual source SHA256 `8A333E31437F13B4B0159FC902DAA4862A23D468F1CFAE3BB99271AFFED370AF` (6031 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - [OWNER/STATE] 独立REA / T014(P0: 0x42E700) / STATIC, VERIFY, NOT READY。Local CompactでPC正本を先読し、既存Ghidra検索DBをread-only利用。前回16時台のostream終端処理、REA既往save-IO監査とは別に「読込sentryのゼロ一致」と「書込postflushのmask=6」の述語差を限定追加。PC正本への本独立記録保存以外はread-only。
  - 0x42EC60（read sentry）pseudo SHA BA687A12FA8459739AA47BE9E79DC502205A11B3CBF3DB07972208DA265C7D8F、0x42E700 site 0x42E753 CALL、0x470980 site 0x4709D5 CALL。状態が厳密に0の時だけtied streamの事前sync候補0x429620（site 0x42EC99）を試行し、状態を**再検査**して0なら1返却。非0なら0x426E00（site 0x42ECD1）を通り、通常帰還があれば0返却。同期helperや状態設定はthrowし得るので「常にreturn 0」は断定不可。
  - 0x429620（事前sync候補）pseudo SHA 305D6AAB27225209E34DE81322321934905E9207EFDAB369FFA02D8BA149CEDF、0x42EC60→0x429620 site 0x42EC99、間接CALL site 0x42963A(+0x34)。内部は (state&6)==0 のとき virtual+0x34; 戻り値-1のとき0x426E00(site 0x429661)。
  - 0x42AA80（write postflush条件）pseudo SHA 1F7BD4122B9D55DC9BDDA44FC45BD4FEE9338C0AE1596AB285AB1DE5A5145506、0x4295B5 site 0x4295EA と0x4629DB site 0x462A10の双方からCALL。条件は (flags at object+0x14 & 2)!=0 **かつ** (state at object+0x0C & 6)==0 の場合だけ virtual+0x34（site 0x42AAD2）。return=-1なら0x426E00(site 0x42AAF9)。
  - 0x4295B5 / 0x4629DB は前回確認済の同構造107byte epilogue、pseudo SHA 28AC205F6A7C2E89753BE7A1C51FA59FE1425479925A936755B98E6D157F2F4C / FEF974B0ED8227C9195929EEA4EFCC6B3F23CA813C4801EDB675BC0502A8C497。両者の内部ProcessingThrow=0→42AA80は**既知**、今回の成果として加算しない。
  - ## 今回の限定的新規差分
  - **status=1（eofbit候補）** はread sentry 0x42EC60の「state == 0」には失敗する。一方、write postflush 0x42AA80の「state&6 == 0」には成功し、別途flags&2とProcessingThrow=0が成り立てばvirtual+0x34の試行候補として残る。state 2/4/6 はどちらも通常の転送/flush許容条件を満たさない（個別の例外・cleanupは別）。
  - 0x42E700（P0、pseudo SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76）ではsite 0x42E753にread sentry、成功時site 0x42E77F→0x42ECF0。内部0x42ECF0 pseudo SHA 509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21、間接CALL site 0x42ED07(vtable+0x20)。ABIの64-bit戻り値がGhidraでvoidとして復元される不一致は前回からVERIFY継続。
  - 0x42E700正常transfer後の後始末は0x42E7D4(site 0x42E7A2; pseudo SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C)へ入り、疑似C上は0x42AA80のpostflush呼出しを持たない。書込側0x4629DBは0x42AA80を条件付きで呼ぶ。read epilogueへのwrite flush挙動の無条件共通化は禁止。
  - write 1byte 0x4294B0は異常事前状態で0x4295B5へ直接進む一方、block write 0x4628F0は同状態で0x426E00を明示的に経由し後始末へ進む。前回の「同じepilogue」と混同して本体preflightまで完全同値扱いしない。
  - [VERIFY] 0x42EC60/0x42AA80の復元ABI、EH stack frameとレジスタ伝搬、ProcessingThrowの再入・例外中挙動、0x42ECF0戻値EDX:EAX、実vptrと+0x34関数VA、旧原作eofbit状態の合法到達性。新規REA info/pseudo/assembly/callers/calleesセット未取得、子関数VERIFIEDへの昇格禁止。ゲーム旧EXE Golden PASS0、strict MATCH0、再実装率未測定。
  - [NEXT] PC新規Ghidraを起動せず、許可済み既存ASMの有無から0x42ECF0のEAX/EDX受渡と0x42E7D4の正常帰還を先に検証。T014 owner A / E統合には本報告を非READY参照とし、既存同内容の非重複照合をしてから引き継ぐ。旧ゲームGoldenは状態0/1/2/4・tied stream有無・short read・正常/例外maskを分けてDESIGNED_NOT_RUN。
- **Original author caveats:** state=0: read sentryに正常帰還候補、write mask=6 gateも許可; state=1: read sentryはreturn0/throw候補、write mask=6 gate許可; state=2,3,4,5,6,7: read sentryはfalse/throw候補、write mask=6 gate不許可。writeの実flushはflags&2、ProcessingThrow=0、virtual実装、例外マスクでさらに制限。state 0..7 × tied yes/no × flagsbit2 yes/no =32条件のブール表を確認（論理モデルのみ、実機未実測）。 / [VERIFY] 0x42EC60/0x42AA80の復元ABI、EH stack frameとレジスタ伝搬、ProcessingThrowの再入・例外中挙動、0x42ECF0戻値EDX:EAX、実vptrと+0x34関数VA、旧原作eofbit状態の合法到達性。新規REA info/pseudo/assembly/callers/calleesセット未取得、子関数VERIFIEDへの昇格禁止。ゲーム旧EXE Golden PASS0、strict MATCH0、再実装率未測定。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261021_1835_T014_READ_EH_FRAME_SPLIT_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261021_1835_T014_READ_EH_FRAME_SPLIT_STATIC.md`; actual source SHA256 `6AA37BACA0CB873F058C01C7D6B31D622E7F83D8342B95CADBA91164822FF391` (6137 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## P0未解決ABIとEH境界の新規差分
  - 関数 `0x42E700`（code SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76）は始めにstreamの64bit gcount下位+8/上位+12をゼロ初期化。`0x42E753→0x42EC60` read sentry、成功時 `0x42E77F→0x42ECF0`、その後 `0x42E7A2→0x42E7D4` とつながる。これらのCALL siteは検索DBの直接CALL索引に存在。
  - `0x42ECF0`（31 bytes、code SHA 509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21）は `0x42ED07` の未解決間接CALL `CALL EAX`（vtable+0x20）を行う。疑似Cは`void`だがcaller `0x42E700`は`uVar5`(64bit)としてその結果をgcount下位/上位に加算。**呼出元期待値と呼出先デコンパイルの戻り値型が一致しない。** 具体的なEDX:EAXは未実証。
  - `0x42E7D4`（84 bytes、code SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C）は`unaff_EBP`/`unaff_EDI`を参照し、EBP-0x14非ゼロで `0x42E7F2→0x426E00`、EBP-4を-1へ設定、tied stream候補のvtable+8を `0x42E810` で間接CALLし、`ExceptionList`をEBP-0xCから復元する。したがって親のframe/SEH状態に依存する可能性が高い。
  - 親 `0x42E700` の成功分岐では、Ghidraが`piVar4=(int *)FUN_0042E7D4(); return piVar4;`を生成する一方、子 `0x42E7D4` は`void`として復元される。この**型矛盾は正常戻り値を子の独立returnとして確定できない根拠**。sentry不成立分岐の疑似Cでは `return param_1`。成功分岐も同じ戻り値とはASM未照合につき断定しない。
  - `0x42E7A4` はGhidra命名 `Catch_All@0042e7a4`、45bytes、code SHA 3E535771EFAAAF577B0A3C7EDDE9E62202A6949F8951F25C26BE1C98154A89D0。`0x42E7BF→0x426E00`をCALL、EBP-4=1を設定し、`0x42E7D1`を復帰位置として返す疑似C。直接CALL索引のcaller=0でも**EHハンドラであれば到達し得る**ためdead codeと解釈しない。
  - `0x42E700` にSEHハンドラ候補 `LAB_005EB8D0`のデータ参照(site 0x42E705)があり、同疑似Cは`0x42E7E4/EE/F1`のunreachable block除去警告を出す。0x42E7A4がそのハンドラとどう結び付くかはEHメタデータ/ASM未照合。推測をVERIFIEDにしない。
  - `0x426E00` は状態/例外マスクを使って条件付きthrow可能なhelper。`0x42E7A4`のCALLを『常に例外を投げる』とは解釈しない。`0x42E7D4`のEBP-0x14が何由来かも、親frameのASM検証なしに状態フラグと断定しない。
  - 直前17:35記録はread sentryのstate==0対write (state&6)==0が中心。本記録は新たにcatch側0x42E7A4／cleanup側0x42E7D4／戻り値型の矛盾を対応づけた差分で、既知のread/write predicateや既往vtable mappingを再計上しない。
  - 再照合CLI: `search.py function`で0x42E700/0x42EC60/0x42ECF0/0x42E7D4/0x42E7A4/0x426E00、`callers 0x42E7D4`、`callees 0x42E7A4`、`related 0x42E7D4 --depth 2 --limit 30`を既存DBに限定して実行。直接CALL、indirect CALL、関数別code SHAと矛盾なし。
  - 保存済みASM(対象EH範囲)について、REA担当Markdown内の`0x42E7A4`と`exe`のtxt内の`42ECF0`を文字列検索したが該当0。見つからなかったことはASM非存在の証明ではない。現時点のassembly充足は0。
  - NEXT P0: 既存許可済みASMまたは次回PCのread-only調査で`0x42E77F`前後のEAX/EDX・ESP、`0x42E7A2`から子cleanupの正常return、0x42E7A4 EH table、EBP-0x14初期化と`0x42E7D4`例外経路を照合。原本・拒否対象を別経路で再抽出しない。
- **Original author caveats:** - 所属: 独立REA / T014(P0) / STATIC・VERIFY・NOT READY / 新REA VERIFIED=0 / 旧EXE Golden PASS=0。 / - NEXT P0: 既存許可済みASMまたは次回PCのread-only調査で`0x42E77F`前後のEAX/EDX・ESP、`0x42E7A2`から子cleanupの正常return、0x42E7A4 EH table、EBP-0x14初期化と`0x42E7D4`例外経路を照合。原本・拒否対象を別経路で再抽出しない。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261021_1936_T014_CATCH_CONTINUATION_END_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261021_1936_T014_CATCH_CONTINUATION_END_STATIC.md`; actual source SHA256 `F71473BC86FBD3B268287250B568E78E1CA63DC45915738D220EAE456DFF2752` (6858 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - 重点対象: P0 block-read parent 0x42E700, catch 0x42E7A4, epilogue 0x42E7D4。既往18時台で親フレーム依存（unaff_EBP、ExceptionList）、Catch_All@42E7A4、ABI void矛盾を既に報告済み。今回これら自体を二重計上しない。
  - ## 新しい独立差分：Catch_All継続ラベルの6関数対照
  - 使用したのは検索CLI `search.py function 0xVA --limit 12 --max-chars 20000 --format json` と `related 0x42E7D4 --depth 2 --limit 30` の保存済み擬似C、関数境界、直接CALL/data-ref索引。各行のreturn targetは疑似C内の `return &DAT_...`。
  -   |block read|0x42E7A4|0x42E7BF|0x42E7D1|45|0x42E7D4|3|
  -   |1byte read|0x470A78|0x470A93|0x470AA5|45|0x470AAC|7|
  -   |block write|0x4629AB|0x4629C6|0x4629D8|45|0x4629DB|3|
  -   |1byte write|0x429585|0x4295A4|0x4295B2|45|0x4295B5|3|
  -   |別stream|0x43A4BD|0x43A4D8|0x43A4EA|45|0x43A4ED|3|
  -   |別stream|0x558E35|0x558E50|0x558E62|45|0x558E68|6|
  - 複数関数において継続アドレス=Catch入口+45=Ghidra関数範囲の直後。計算6/6一致、FAIL0。CALL siteは5/6で入口+27、0x429585のみ入口+31。4ケースでcleanupまで3bytes、ほか6/7bytes。継続先を通常の独立関数復帰値と同一視しない根拠が増加。
  - 先行18時台の単独0x42E7A4観察を、今回は5つの異なるstream系ハンドラの幾何条件で独立比較したもの。生ASM同一・例外表が同じ・実際のEH遷移成功は未証明。
  - 関数コードSHA（検索DB由来、EXE生ASM SHAではない）: Catch 0x42E7A4=3E535771EFAAAF577B0A3C7EDDE9E62202A6949F8951F25C26BE1C98154A89D0、0x470A78=43CF83D92FE754DFBA87E9F086D535174B8FEFAA0E967688E96DC150683CA79C、0x4629AB=BE6CF7F56AD8BF27A3BB4F6BDD5C1435CEC38400A75A62264F24F2BD2BA4C7F9。
  - 残りSHA: 0x429585=25943FA0BBA548DEC970C193BD09ED5659C6FF885ABC9A60FFE37CE52B480206、0x43A4BD=D66E853CD681F17059A3BE32E8FB22E45D92CF496C7E9AFD087322CA2DAB5B2C、0x558E35=153B8CF2BC965E29C067FF8EBA7A581FE6CCE757EEECD033D0FAEB139399DB80。
  - 親0x42E700（SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76）は0x42E7A2からcleanup 0x42E7D4へGhidra直接CALL索引を持つ。親の関数範囲は[0x42E700,0x42E7A4)で0x42E7A2は末尾2bytes位置。ただし命令bytesの一次ASM照合は未完了。「CALL実命令」「JMP」「通常return」はこの索引だけで確定しない。
  - 1byte parent 0x470980は0x4709EF/0x470A2F/0x470A5F/0x470A76からcleanup 0x470AACへ分岐するGhidra索引、catch 0x470A78は通常CALL caller0件。0x470AACは親frameのEBP-0x14を返す疑似Cを持つ。異なるreturn APIの安易な統合は禁止。
  - **VERIFY:** EHハンドラメタデータが各Catchに実際に到達するか、継続ラベルがSEH funcletの何を指すか、親フレームのEBP-0x14意味、cleanup戻りEAX、0x42ECF0の64bit戻りABI、0x42E7A2命令bytesはいずれも未確定。
  - 独立した既存Ghidra検索CLIによる別対象のCatch_Allパターン比較は実施成功。拒否されたsiteの命令bytes取得は行っていない。0x42E7A2の命令種はVERIFYへ据置。
  - NEXT P0: owner権限・最新重複・lockを確認後、許可済み別のASM静的証拠が自然に得られる場合に限り、0x42E7A2の命令種、0x42E7D1→0x42E7D4の継続、0x470AA5→0x470AACの継続を検証。拒否されたCALL_INDEX_V2クエリの迂回は禁止。次に0x42ECF0のEDX:EAX戻りABIを独立確認。
- **Original author caveats:** - NEXT P0: owner権限・最新重複・lockを確認後、許可済み別のASM静的証拠が自然に得られる場合に限り、0x42E7A2の命令種、0x42E7D1→0x42E7D4の継続、0x470AA5→0x470AACの継続を検証。拒否されたCALL_INDEX_V2クエリの迂回は禁止。次に0x42ECF0のEDX:EAX戻りABIを独立確認。 / - 保存・readbackはこの後に実施する。失敗時は未保存・未確認と明示する。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261021_2035_T014_RDSTATE7_LOAD_EXCEPTION_CALLERS_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261021_2035_T014_RDSTATE7_LOAD_EXCEPTION_CALLERS_STATIC.md`; actual source SHA256 `D8C2610FB0E9564D6DA330007E0D51C4EB4B3D9EE045DF83543EE1FEE9FAB2CE` (5899 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## 今回の新規STATIC差分: 固定幅loadの上位検査を単純述語へ正規化
  - 保存済みGhidra検索CLI function 0x470700 / 0x470770 / 0x4707D0 / 0x58E480 に同形のstream state検査を独立確認。0x42CC80にも同じ条件式の使用例があるが、本報告の固定幅ロード4例とは区別する。
  - 0x470700 は site 0x470713→0x42E700、code SHA=873CD6F6F7A5DF2EDE7A631557223DEDB71B3AEA7262FADE79ACA0A9AD86D6C8。成功側でDAT_00B060F0をparam_1へ格納。
  - 0x470770 は site 0x47077D→0x42E700、code SHA=6A6004BA86FA14622CDB1F14E9B57FDBD4864AAAE1D5951FE8EE74D904EEFAC9。Ghidraの出力先puStack_cは復元不完全のため書込先確定はしない。
  - 0x4707D0 は site 0x4707DD→0x42E700、code SHA=A6F57840EB564D48C00D8757E6CE0CDEB98DE66016C5C5C327BC6E429DF3A45B。同様に出力先puStack_cは不確定。
  - 0x58E480 は site 0x58E597→0x42E700(4bytes, 0)、code SHA=90553750D5B72BCA40DB94F594AC6E6B8B570F59289197E2C41E4F8AB0693D94。成功側で読込global DAT_00B060F0→対象param_2+0x7Cに代入、異常状態ならLoadExceptionへ進む。
  - 既知のread sentry 0x42EC60は入口state==0を要求。書込postflush 0x42AA80は (state & 6)==0 を要求する（他のflag/例外条件あり）。今回は上位固定幅loaderの (state & 7)==0 を別の新しい層として追加しただけで、既知2述語を新規成果に二重計上しない。
  - 0x42E700 block read親のsite 0x42E77F→0x42ECF0、0x42ECF0 site 0x42ED07 virtual+0x20（computed CALL）は既知。該当実vptrがbasic_stringbufなら0x4297D0候補。ただし戻り値EDX:EAXと独立ASMは未検証。今回新しい仮想関数の実装先をVERIFIED認定しない。
  - 0x42E700はgcount64bitを更新するが、上位loaderの検査はGhidra上gcount値そのものではなくstream stateである。『取得数が4なら必ず成功』『4未満なら必ずLoadException』は実機未観測につき断定禁止。
  - 直前19時台の6 Catch_All継続規則、0x42E7A2の命令種不明、以前のCALL_INDEX_V2特定命令照合 SAFETY_REFUSAL は据置。この回は拒否されたSQL、命令bytes取得、別経路の再試行を実施していない。
- **Original author caveats:** - 数学的同値: (state & 7) != 0。最初の項はbit2又はbit0、次の項はbit1又はbit2の検査。state上位bitは判定に寄与しない。 / - 新規5種REA証拠(info/pseudo/assembly/callers/callees)完全取得0関数。Ghidra DBの保存済みpseudo/参照とREA正式method証拠を混同しない。正式REA Evidence ID=0、新VERIFIED=0、TODO/VERIFY/BLOCKED正式差分=0/0/0。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261021_2135_T014_SHORTREAD_STATE_GAP_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261021_2135_T014_SHORTREAD_STATE_GAP_STATIC.md`; actual source SHA256 `879FA36B0EC6DBCEBCE172042A640BFA37E2096906F3CF2FA9BF0620D6A1E5CD` (5924 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## 新しい独立STATIC差分: 短いブロック読込後の状態ビット更新が疑似C上は未接続
  - `0x470700` (code SHA 873CD6F6F7A5DF2EDE7A631557223DEDB71B3AEA7262FADE79ACA0A9AD86D6C8): site `0x470713`→`0x42E700`、要求size=4、直後にstream state `&7` が非ゼロならLoadException、ゼロならDAT_00B060F0を出力。
  - `0x42E700` (code SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76): gcount下位+8/上位+12を0初期化、site `0x42E753`→sentry `0x42EC60`、site `0x42E77F`→`0x42ECF0`、返却候補64bitをgcountへ加算し、site `0x42E7A2`→cleanup `0x42E7D4`。親疑似Cには明示的な`gcount < requested`比較がない。
  - `0x42ECF0` (code SHA 509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21): site `0x42ED07` はvtable+0x20への間接CALL。Ghidraは戻り型`void`、親は`uint64`として消費するABI矛盾を維持。
  - 既存vtable監査上のbasic_stringbuf候補`+0x20` = `0x4297D0`（実行時vptr未検証、REA正式vtable VERIFIEDではない）。今回保存検索CLIでその疑似Cとcaller/indirect一覧を独立抽出。
  - `0x4297D0` (217 bytes, code SHA 851F477F38B06755F148F603E3D5387DE54DDCF5FB726345BD836EC30D9CAD2D): 読込可能分があればmemcpy＋ポインタ/残量更新、残量なしはvtable+0x1C (`0x42985F`のcomputed CALL)で1byteを取得。-1なら累計lVar1（部分読込数）を返す。
  - `0x4297D0`自身の保存疑似Cにstream stateの明示書込や`0x426E00`直接CALLは見えない。**これは下層の静的観察であり、上位がEOF/failbitを立てないと証明するものではない**。
  - `0x42E7D4` (code SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C) は親frameの`EBP-0x14 !=0`で `0x42E7F2`→`0x426E00`を実行する。親疑似Cにそのslotの完全な値伝達が復元されておらず、このcleanupが短読込状態を更新する可能性はVERIFY。
  - `0x426E00` (code SHA 7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43) はGhidra疑似Cでstream state `&0x17` と例外マスクを扱う。レジスタ引数`in_EAX`は未解決。`0x42E7D4`からの実際の値を断定しない。
  - `0x42EC60` (code SHA BA687A12FA8459739AA47BE9E79DC502205A11B3CBF3DB07972208DA265C7D8F) は入口とsentry後のstate==0条件を確認、失敗時 `0x42ECD1`→`0x426E00`。すでに発生した短読込の事後判定とは別段階。
  - ## 新しく明確にした不確定境界
  - 4bytes要求で3bytes/0bytesしか返らない場合、`gcount`は部分数を反映する静的候補だが、`LoadException`発生は**上位ロード前のstate**に依存。`0x42E7D4`の未復元レジスタ/親frame状態を解消するまで「短読込でLoadExceptionになる/ならない」は共に断定禁止。
  - 上記拒否以後、0x429620についてツール・shell・path・ZIPを変えた再試行なし。取得済み0x4297D0以前の既存合法データのみ使用し、独立な関数間比較を継続。許容される次手は安全境界を維持した状態で対象外の証拠を照合すること。
- **Original author caveats:** - `0x42E7D4` (code SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C) は親frameの`EBP-0x14 !=0`で `0x42E7F2`→`0x426E00`を実行する。親疑似Cにそのslotの完全な値伝達が復元されておらず、このcleanupが短読込状態を更新する可能性はVERIFY。 / - 上記拒否以後、0x429620についてツール・shell・path・ZIPを変えた再試行なし。取得済み0x4297D0以前の既存合法データのみ使用し、独立な関数間比較を継続。許容される次手は安全境界を維持した状態で対象外の証拠を照合すること。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261021_2236_T014_STATE_MASK10_EPILOGUE_CROSSWALK_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261021_2236_T014_STATE_MASK10_EPILOGUE_CROSSWALK_STATIC.md`; actual source SHA256 `7B8DB05D55BDD1605083F28A1D293CD33D1C4C51CE25792B676AE75900E56C96` (5926 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## 新規静的差分A: 状態更新helperのマスクと上位LoadException条件の非同値
  - `0x426E00`（code SHA 7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43）疑似Cは、入力レジスタ値Sを `S & 0x17` にマスクし、ストリーム内のstate候補 `[param_1+0xC]` に代入。例外マスク候補 `[param_1+0x10]` との交差が非0ならthrow経路。**Sの供給元と旧状態のOR有無はABI未解明**。
  - `0x470700`（code SHA 873CD6F6F7A5DF2EDE7A631557223DEDB71B3AEA7262FADE79ACA0A9AD86D6C8）、CALL site `0x470713 → 0x42E700` は正常return後に `(observed_state & 7)!=0` で `LoadException`。上位は0x10ビットを条件に含めない。
  - `0x426E00`内のthrow優先度は `(masked & 4)`→badbit、次に`(masked & 2)`→failbit、残りのマスク交差は`eofbit set`文字列。従ってmasked=0x10だけでも最後のメッセージ候補へ落ちる。ただし通常許容マスク範囲と実call register値が不明であり原作実到達・バグの証拠ではない。
  - ## 新規静的差分B: cleanup間のfailbit組み立てを同一視できない
  - P0 `0x42E7D4`（code SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C）は親`EBP-0x14 !=0`でsite `0x42E7F2 → 0x426E00`をCALLするが、疑似C内に明示`|2`がない。親frameへの書込起源・渡すEAXは未復元。
  - 比較 `0x43A4ED`（code SHA E35CFF4E28E894B80AEF51FF5D0776C7581A6D7E6A1A8509EF29E209663638B0、site `0x43A514`）は親frameのbyte `EBP-0x11==0`で `uVar2 |= 2` とした後、非ゼロ時に同helperをCALL。
  - 比較 `0x558E68`（code SHA B605B03D944834CCC9BC96B0E662CE671F554AD4007F1BBAFDDB54E0A40354A2、site `0x558E92`）はgcount候補 `[EDI+8/+0xC]` が両方0なら `uVar2 |= 2`。この`|2`が見えない0x42E7D4へコピーして『短読込は必ずfailbit』と決めつけない。
  - 共通helperのcallerはGhidra直接CALLで確認済み。`0x42E7D4`への親site `0x42E7A2`、`0x42ECF0`へのsite `0x42E77F`、仮想CALL `0x42ED07(+0x20)`も保存索引と一致。ただしvirtual実体/ABI/正常returnはVERIFY。
  - NEXT T014: 許可済み既存ASMの存在を照合し、0x42E7D4 の EBP-0x14 と直前 EAX、0x42ECF0 return EDX:EAX、上位state検査実体を別々に確定。S=0x10経路の実行可能性は仮説で保留。
- **Original author caveats:** - NEXT T014: 許可済み既存ASMの存在を照合し、0x42E7D4 の EBP-0x14 と直前 EAX、0x42ECF0 return EDX:EAX、上位state検査実体を別々に確定。S=0x10経路の実行可能性は仮説で保留。 / - 保存はファイル作成後の独立readback/ハッシュ確認が完了するまで未確認扱い。現時点ではREA正式VERIFIEDでもMASTER同期でもない。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261021_2339_T014_SINGLEBYTE_EOF_GCOUNT_BRANCH_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261021_2339_T014_SINGLEBYTE_EOF_GCOUNT_BRANCH_STATIC.md`; actual source SHA256 `242B49DE31274A47094C334254A2ECC41E71EA1C4B40D8377F5FD83D73682557` (5763 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - 0x470980：Ghidra機械疑似C SHA256 850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446、248 bytes。保存索引ではcallers 0x4705F0 site 0x470611が1件、Ghidra内部のdirect cleanup sites 0x4709EF/0x470A2F/0x470A5F/0x470A76→0x470AACが4件。
  - 初期化 param_1[2]=0、param_1[3]=0（gcount低/高候補）。sentry 0x42EC60へsite 0x4709D5で入り、sentry falseのときは1byte取得処理へ進まずcleanup。
  - バッファ位置/残量が利用可能なら現在byteをunsigned 0..255に広げる経路がある。不足時はvtable+0x18を呼び、返ったuintが0xFFFFFFFFならcleanupへ進む。
  - uint 0x000000FF（データbyte 0xFF）と0xFFFFFFFF（EOF int_type sentinel）は一致しない。従ってデータ0xFFをEOFとして扱わないのが索引疑似Cの候補動作。後段token readerのsigned-char拒否とは別層。
  - 0xFFFFFFFF以外なら、バッファ消費可能時にはポインタ+1/残量-1/取得数+1、そうでなければvtable+0x1C呼出後に取得数+1の候補経路。vtable+0x18に対応するcomputed site 0x470A1B、+0x1Cにsite 0x470A66、tie側computed site 0x4709D0。vptr実体・副作用・戻値は未確定。
  - 0xFFFFFFFFの経路ではGhidra疑似C上は取得数+1を通らない。正常な1byte取得成功時は低32bits加算、carry時高32bits+1。原作動的gcount値は未実測。
  - ## 今回の差分B：callerとcleanupの二段判定
  - 0x4705F0：コードSHA256 86E597D129AFE91C0A27CEF00A3E529B959C5BFCAA1A1B6221DFCDFF0F138889。site 0x470611→0x470980。返値候補iVar3!=-1の場合のみ DAT_00B060F8[i]へbyteを格納し、その後stream state&7を検査してLoadExceptionへ分岐する。0xFF拒否・255上限自体は既存REA資料にあるため再加算しない。
  - 0x470AAC：code SHA256 EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D。疑似Cはunaff_ESI!=unaff_EBXならsite 0x470AC5→0x426E00、最後に親frame EBP-0x14を戻値とする。一方block側0x42E7D4（SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C）は親frame EBP-0x14非0でsite 0x42E7F2→0x426E00。両者を同じ「状態フラグslot」と断定しない。
  - 0x42E700（code SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76）→0x42ECF0（code SHA 509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21）site 0x42E77F、virtual+0x20 site 0x42ED07はbulk転送経路。1-byte 0x470980の仮想+0x18/+0x1Cと別APIであり、EOF/partial状態を単一実装へ雑に統合しない。
  - Ghidraは0x470980をvoidと推定する一方0x4705F0はintとして消費、0x470AACは親frame returnを記述。0x42ECF0もvoid対親uint64の矛盾。いずれもASM未照合のため戻値ABI、EBP slotの実意味、state引数はVERIFY。
  - 先行REA 0x4705F0の5種VERIFIEDは既存RUNの成果（asm ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d）。今回0x470980・0x470AAC等の新規正式info/pseudo/assembly/callers/calleesの5種セット0、Evidence ID新規0、VERIFIED新規0。索引本文/機械xrefsはREA正式証拠に転換しない。
- **Original author caveats:** - Ghidraは0x470980をvoidと推定する一方0x4705F0はintとして消費、0x470AACは親frame returnを記述。0x42ECF0もvoid対親uint64の矛盾。いずれもASM未照合のため戻値ABI、EBP slotの実意味、state引数はVERIFY。 / ## 差分の限界・安全・次の再開
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0047_T014_TOKEN_EAX_MINUS1_STATE_PRIORITY_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0047_T014_TOKEN_EAX_MINUS1_STATE_PRIORITY_STATIC.md`; actual source SHA256 `814CA8CFE7FC52AF8212F898FC402965C11B313127C62BCB16C45273F0E055EF` (7802 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - 根拠A（保存済み正式REA assembly、既存VERIFIEDを再利用）: `runs/20261011T144115307Z/4705F0_procedure_assembly.json`、evidence `ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d`。読取成功。関数0x4705F0のREA5種は既存成果であり、新規には数えない。
  - 根拠B（Ghidra12.1.4検索DB機械疑似C、REA VERIFIEDではない）: 0x470980 SHA `850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446`; 0x470AAC SHA `EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D`; 0x4705F0 SHA `86E597D129AFE91C0A27CEF00A3E529B959C5BFCAA1A1B6221DFCDFF0F138889`; 0x42EC60 SHA `BA687A12FA8459739AA47BE9E79DC502205A11B3CBF3DB07972208DA265C7D8F`; 0x426E00 SHA `7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43`。
  - ## 新たに絞り込んだ重要な条件分岐（1byte reader戻値とtoken読取）
  - 保存済み0x4705F0の**実アセンブリ**は以下の順序を示す。
  - 1. `0x4705F4..0x470600`: global scratch `0xB060F8`を`0x400`バイト零初期化。既報。
  - 2. `0x470610 PUSH EDI; 0x470611 CALL 0x470980` → `0x470616 CMP EAX,-1; 0x470619 JZ 0x470621`。**EAX=-1なら現在の1文字をscratchへ格納せず**、EAX!=-1なら`0x47061B MOV [ESI+0xB060F8], AL`。この呼出元のEAX依存はASM根拠あり。呼出先のABI復元はなお未確定。
  - 3. `0x470621..0x47063B`: 直後にstream stateを読み、下位bit0/1/2のいずれかが立てば`0x470690`のLoadException経路。条件は `(state & 7)!=0`（既報、ASMで再照合）。
  - 4. `0x47063D..0x470645`: その状態検査を通過してから現在位置のscratch byteを検査、0なら正常な終端として`0x470664`へ進む。ゼロ初期化された位置へEAX=-1時には格納しないため、**「呼出先から戻る・EAX=-1・post-call state&7==0」の3条件を仮定した場合、NUL入力と同じ正常終端経路へ入る**。これは局所制御フローの条件付き結論で、原作が実際にEOFでその状態を返す証明ではない。
  - 5. `0x470647..0x470662`: 有効な非NUL byteは符号付き0x20..0x7F検査後、添字を増やし255に達すると次byteを読まず終了（既報、境界挙動を再加算しない）。
  - ## 今回の論理的成果: エラーの優先順位と正常終端条件を分離
  - | 0x470980の呼出元から見た戻値 | 通常帰還後のstate | 0x4705F0内の帰結 |
  - さらに0x470980内部・0x470AACで例外が投げられた場合は、そもそも0x4705F0のEAX/state検査に戻らない。0x470AACは`unaff_ESI!=unaff_EBX`のときsite 0x470AC5→0x426E00を呼ぶ候補。0x426E00はstream例外mask交差でios_base::failureを投げ得る。よって少なくとも**（1）callee例外、（2）callerのLoadException、（3）callerの正常NUL終端**という別々の結果候補を持つ。例外経路の優先度・状態ビットの生成を一括のif文へ単純化しない。
  - callee内`0x470AAC`のEAX/ESI/EBX/親フレーム`EBP-0x14`の実値伝播と、`0x470980`が真のEOFで`-1`を返すか、stateを何にするかは未解決。特に**「EOFなら無条件にprefix正常受理する」という主張は不適切**。
  - `0x470611: 0x4705F0→0x470980`（保存REA asm・Ghidra CALL双方）。`0x4709D5: 0x470980→0x42EC60`、`0x4709EF/0x470A2F/0x470A5F/0x470A76: 0x470980→0x470AAC`、`0x470AC5: 0x470AAC→0x426E00`（Ghidra CALL索引）。
  - 未解決の間接CALL: `0x4709D0` (CALL EAX、tie候補)、`0x470A1B` (CALL EAX、vptr+0x18候補)、`0x470A66` (CALL EDX、vptr+0x1C候補)、`0x470AE3` (CALL EAX、cleanup vptr+8候補)。実行時vptr/対象関数を確定扱いしない。
  - 次のP0: 許可済み既存ASMがあるかownerの既存runs/evidenceで再照合したうえで、0x470980/0x470AACの正常帰還EAXと親EBP-0x14由来、ESI/EBX→0x426E00の入力、およびcallee内throw可否を決着する。既拒否CALL_INDEX_V2照合や0x429620 CLI命令取得を他ツール・経路で再実行しない。
- **Original author caveats:** 次表は**CALLEEから通常帰還したあとの**局所的な条件付き結果である（新しいゲーム動作観測ではない）。 / - 次のP0: 許可済み既存ASMがあるかownerの既存runs/evidenceで再照合したうえで、0x470980/0x470AACの正常帰還EAXと親EBP-0x14由来、ESI/EBX→0x426E00の入力、およびcallee内throw可否を決着する。既拒否CALL_INDEX_V2照合や0x429620 CLI命令取得を他ツール・経路で再実行しない。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0137_T014_STRINGBUF_VTABLE_SLOT_GAP_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0137_T014_STRINGBUF_VTABLE_SLOT_GAP_STATIC.md`; actual source SHA256 `E17D4E6A1D79237506E6D6689AD40306245949C962FE2D84F588810BEF673835` (4491 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## 今回の独立静的差分：input stream生成から実vtableスロットアドレスへ
  - Ghidra関数0x429C60 (code SHA256 6882798514D6787EC7429991A5CF2DF76F037760F6B1951D3DD053491426AD56) はbasic_istringstreamを組み立て、ストリームのbuffer pointer `[adjusted iVar3+0x38]` に `param_1+4` を格納。CALL 0x429D0B→0x42A7A0(param_1+4,0x21)。
  - 0x42A7A0 (code SHA256 EA6C9787B7D13414C659B7D7A0AEBA972766848610030090AD011DDF025924AD) はそのsubobjectの先頭vptrを `std::basic_stringbuf<...>::vftable` = 0x0063848C に設定。Ghidra DATA site 0x42A7D8、型hint `pointer[15]`。
  - 同0x42A7A0の内部flag変換を固定引数0x21へ代入すると uVar2=2、param_1[0x10]=2。入力モードflagの物理的意味・後続の変更は未確定。
  - 0x470980 (code SHA256 850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446) はadjusted stream field +0x38からbufferを引き、buffer vptr経由でCALL。上記constructorで作られた同一bufferが変更されていなければ、vptrの静的基準位置は0x0063848C。
  - | 0x4709D0 | +0x04 | 0x00638490 |
  - | 0x470A1B | +0x18 | 0x006384A4 |
  - | 0x470A66 | +0x1C | 0x006384A8 |
  - | 0x470AE3 (0x470AAC cleanup) | +0x08 | 0x00638494 |
  - Ghidra computed CALL indexは0x4709D0/EAX、0x470A1B/EAX、0x470A66/EDX、0x470AE3/EAX。site→slotはconstructorを前提とする条件付き追跡で、site→calleeの絶対関数VA解決ではない。
  - SQLite `pointer_refs` read-onlyで0x0063848C..0x006384C4の15個の4-byte slotを個別照合：recordありは先頭0x0063848C→0x0042A460の1件、残り14 slotには該当record無し。問題の+0x04/+0x08/+0x18/+0x1Cは全て索引未収録。
  - `0x4705F0`の既存REA 5種VERIFIED（既存asm ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d）は再利用のみ。0x429C60/0x42A7A0/0x470980/0x470AACの今回新規のREA info/pseudo/assembly/callers/callees完全充足0、Evidence ID新規0、VERIFIED新規0。
  - Golden: 旧EXE実機PASS0、新旧strict MATCH0、実再現率未測定。次回は保存済みの許可済みvtable/listing証拠が既存runsにあるか照合し、stream constructorから0x4705F0 callerまで同一object identityを確認。+0x18/+0x1C targetはその後も独立証拠が必要。GoldenはNOT RUN。
- **Original author caveats:** - Golden: 旧EXE実機PASS0、新旧strict MATCH0、実再現率未測定。次回は保存済みの許可済みvtable/listing証拠が既存runsにあるか照合し、stream constructorから0x4705F0 callerまで同一object identityを確認。+0x18/+0x1C targetはその後も独立証拠が必要。GoldenはNOT RUN。 / - 変更範囲: REA owner内のこの独立新規文書だけ。原本ZIP/EXE/SAVE・MASTER/A〜E/T018/dev_lab・旧runs/evidence・QUEUE/PROGRESS・Git/公開先・スケジュール不変更。保存readback前は未確認扱い。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0234_T014_GLOBAL_SAV_CTOR_TOKEN_CROSSCALL_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0234_T014_GLOBAL_SAV_CTOR_TOKEN_CROSSCALL_STATIC.md`; actual source SHA256 `49110AC7F4C520A94A703A5EAACC8018FF543B357A23B0CC890C9C5EAF27689E` (5173 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## 今回の新規静的差分: global.sav の2つのcaller内にあるコンストラクタ→token reader鎖
  - | 親関数 | basic_istringstream ctor CALL site | token reader 0x4705F0 CALL site | Ghidra疑似Cで見える入力streamローカル |
  - | 0x428010 | 0x4282F4 → 0x429C60 | 0x4283A7、0x428444 | aiStack_24c |
  - | 0x428710 | 0x428A1F → 0x429C60 | 0x428ADF、0x428B7F | aiStack_26c |
  - 親0x428010 code SHA256=FBB4B43CEB8B979ED8A41554C5CC40505AA47D8066296A09E802C0328FC3E369。親0x428710 code SHA256=6513A1B7C947F4A0F76FDAFC21F9F59A90B24CA3163B0226E0FF1E049ABEF878。
  - 0x429C60 code SHA256=6882798514D6787EC7429991A5CF2DF76F037760F6B1951D3DD053491426AD56。CALL 0x429D0B→0x42A7A0（0x21）。0x42A7A0 code SHA256=EA6C9787B7D13414C659B7D7A0AEBA972766848610030090AD011DDF025924AD。
  - 0x429C60疑似Cには stream内のadjusted iVar3+0x38 に param_1+4（buffer subobject）を格納する箇所がある。0x42A7A0ではbasic_stringbuf vptr候補=0x0063848Cを設定（旧0137根拠の再利用）。
  - 0x4705F0 CALL site 0x470611→0x470980（token読込→1byte読込）。0x470980疑似Cはstreamのadjusted field+0x38経由でbuffer pointerを取得し、vptr経由の+0x04/+0x18/+0x1Cを使う。cleanup 0x470AACでは+0x08（旧0137根拠の再利用）。
  - Ghidraでは0x429C60の定義が1引数に見える一方、0x428010/0x428710の疑似Cではそれぞれ2引数相当の呼び出しを復元する。constructorの隠れたthis/引数対応はASM未確認。
  - 0x4705F0は疑似Cでunaff_EDIによりstream state参照。一方親0x428010等は token readerを出力文字列バッファらしき引数付きで表現しており、**親ローカルstreamオブジェクトと0x4705F0のEDIが等しいというレジスタ/ABIの実証は未了**。
  - 次の許可済み解析位置: 0x428010のCALL 0x4282F4→0x4283A7 / 0x428710のCALL 0x428A1F→0x428ADFにおいて隠れたthisの同一性を既存許可済み証拠で検証。その後0x470980の+0x18/+0x1Cの実指先を証拠で限定。
- **Original author caveats:** ## 証拠/状態/実行と次回 / - 次の許可済み解析位置: 0x428010のCALL 0x4282F4→0x4283A7 / 0x428710のCALL 0x428A1F→0x428ADFにおいて隠れたthisの同一性を既存許可済み証拠で検証。その後0x470980の+0x18/+0x1Cの実指先を証拠で限定。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0337_T014_GLOBAL_SAV_EDI_IDENTITY_ABI_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0337_T014_GLOBAL_SAV_EDI_IDENTITY_ABI_STATIC.md`; actual source SHA256 `68E09A8ED4E9DB219649BD6FC99598CD1C643D89C32C7C276C8294B3FAB1C979` (5768 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## 新規差分1：global.sav親関数の同一stream objectを実ASMのESP相対アドレスで解決
  - 基準S1=0x4282DF時ESP。`0x4282E6 PUSH ECX`後の`0x4282E7 LEA EDX,[ESP+0x48]`は S1+0x44。`0x4282EB PUSH EDX`→`0x4282F4 CALL 0x429C60`がctor第1引数にそのポインタを渡す。
  - `0x429D25 RET 8`を保存済ASMで直接確認。ctorは2スタック引数をcallee-cleanupし、通常帰還後ESP=S1に戻る。以後readerまでの`PUSH 0x30`は`ADD ESP,4`で均衡する。
  - `0x4283A2 PUSH EAX`後の`0x4283A3 LEA EDI,[ESP+0x48]`=S1+0x44、直後`0x4283A7 CALL 0x4705F0`。`0x42843B PUSH ESI`後の`0x42843C LEA EDI,[ESP+0x48]`=S1+0x44、直後`0x428444 CALL 0x4705F0`。**両方ともctor第1引数と同一アドレス**。
  - 基準S2=0x428A07時ESP。`0x428A0E PUSH ECX`後の`0x428A0F LEA EDX,[ESP+0xF0]`=S2+0xEC、`0x428A17 PUSH EDX`→`0x428A1F CALL 0x429C60`。
  - 通常帰還後ESP=S2。`0x428AD7 PUSH EAX`後の`0x428AD8 LEA EDI,[ESP+0xF0]`=S2+0xEC→`0x428ADF CALL 0x4705F0`。`0x428B73 PUSH ESI`後の`0x428B74 LEA EDI,[ESP+0xF0]`=S2+0xEC→`0x428B7F CALL 0x4705F0`。**こちらも両token読込はctor第1引数と同一アドレス**。
  - ## 新規差分2：Ghidra疑似Cの引数復元の具体的誤差
  - `0x429C60`のGhidra擬似C宣言は`int *FUN_00429c60(int *param_1)`だがASMは`MOV EBX,[ESP+0x28]`/`MOV EDI,[ESP+0x2C]`、親側は2回PUSH、末尾は`RET 8`。**最低限、2つのスタック引数を取るABI**であり1引数の擬似C宣言を関数ポインタ型に流用しない。第2引数の意味はVERIFY。
  - `0x4705F0`はGhidra上`void FUN(void)`だが、親側は`PUSH 出力先`＋`LEA EDI,stream`、既存REA ASMは`0x47067A MOV ECX,[ESP+0x14]`で出力先を読み、`0x470621 MOV EAX,[EDI]`でstreamを参照し、`0x47068F RET`。**EDI暗黙stream＋caller-cleanupの1stack出力先引数**。C標準呼出規約名までは確定しない。
  - ctorの`0x429CC8 LEA EBP,[EBX+0x10]`、`0x429CCC MOV [ESI+0x38],EBP`、`0x429D03 PUSH EBP`→`0x429D0B CALL 0x42A7A0`はbuffer subobjectとの連鎖を補強。ctorの初期stringbuf vptr=0x0063848Cは旧0137既知、追加VERIFIED扱いにしない。
  - Ghidra検索CLI callers 0x4705F0 から上記4サイトを再照合。callees 0x429C60 は`0x429D0B→0x42A7A0`、related 0x470980 depth2 は`0x470611→0x470980`、`0x4709D5→0x42EC60`、`0x4709EF/0x470A2F/0x470A5F/0x470A76→0x470AAC`。CLIはread-only。
  - ABI静的到達点: global.sav親2つ→同一stack stream address→EDI implicit token reader→`0x470610 PUSH EDI`→0x470980。間接CALLスロット+0x04/+0x08/+0x18/+0x1Cの実指先は未解決。動的vptr不変性、EOF時state、0x470980戻値/終了ABIはVERIFY。
- **Original author caveats:** - `0x429C60`のGhidra擬似C宣言は`int *FUN_00429c60(int *param_1)`だがASMは`MOV EBX,[ESP+0x28]`/`MOV EDI,[ESP+0x2C]`、親側は2回PUSH、末尾は`RET 8`。**最低限、2つのスタック引数を取るABI**であり1引数の擬似C宣言を関数ポインタ型に流用しない。第2引数の意味はVERIFY。 / - ABI静的到達点: global.sav親2つ→同一stack stream address→EDI implicit token reader→`0x470610 PUSH EDI`→0x470980。間接CALLスロット+0x04/+0x08/+0x18/+0x1Cの実指先は未解決。動的vptr不変性、EOF時state、0x470980戻値/終了ABIはVERIFY。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0443_T014_SINGLEBYTE_EOF_ESI3_STATE_ABI_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0443_T014_SINGLEBYTE_EOF_ESI3_STATE_ABI_STATIC.md`; actual source SHA256 `1CD52958D9591FB504904B13FEEABF091D56B374E3E677A7E2ECED5DD99D0F6D` (9083 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - 既存資料先読: MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存runと最新progress_sync_20261011T153958076Z、前回0337と既存0047/2339/0137報告。0x4705F0既存RUN_RESULT=20261011T144115307Z、5種の保存済み証拠の存在確認（新規計上禁止）。
  - 保存済みGhidra12.1.4機械疑似C: 0x470980 code_SHA=850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446、0x470AAC=EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D、0x426E00=7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43。これらはREA5種証拠の新規取得には該当しない。
  - ## 新たに結び付けたP0静的結論：1-byte readerのEOF=−1でESI=3、stateへeofbit|failbit
  - 原資料ASM: 0x4709AE XOR EBX,EBX、0x4709BF XOR ESI,ESI、0x4709C1 MOV [EBP-0x14],EBX。0x4709D5 CALL 0x42EC60（読込sentry）。
  - sentry=0の別枝: 0x4709E8 MOV [EBP-0x14],0xFFFFFFFF、0x4709EF JMP 0x470AAC。ESIは0のままなので、cleanupで新しいbitのORを行わない（先に立っていたstream state等は別検証）。
  - sentry成功後の1-byte候補取得: 0x470A1B CALL EAX（vtable+0x18候補）または0x470A11 MOVZX EAX, BYTE PTR [EAX]（buffer）。0x470A1D MOV [EBP-0x14],EAXで取得値を退避。
  - **決め手:** 0x470A20 CMP EAX,-1、0x470A23 JNE 0x470A31。EAX=-1のとき0x470A25 LEA ESI,[EAX+4] -> 32-bit ESI=3、0x470A2F JMP 0x470AAC。ここでの3は別の「取得長」ではなくcleanupの状態bitマスク候補。
  - cleanupの既存ASM: 0x470AAC MOV EDX,[EDI]、0x470AAE MOV ECX,[EDX+4]、0x470AB1 ADD ECX,EDI、0x470AB3 CMP ESI,EBX(=0)、0x470AB5 JE 0x470ACA、0x470AB7 MOV EAX,[ECX+0xC]、0x470ABA OR EAX,ESI、0x470ABC CMP [ECX+0x38],EBX、0x470AC1 OR EAX,4（buffer参照0の場合）、0x470AC4 PUSH EBX(=0)、0x470AC5 CALL 0x426E00。
  - よって**「sentry成功後に仮想1byte取得でEAX=-1を返した通常cleanup」**の局所条件下では、下層0x426E00へ渡すEAX=(元state|3|[buffer==0 ?4:0])。0x426E00疑似Cはstateフィールドへ EAX&0x17 を格納し、例外マスク交差を判定する。元stateに何があっても下位2bit=1/2が立つので、正常帰還できればcallerの(state&7)!=0に必ず該当する。
  - 正常byte: 0x470A20のEAX!=-1経路ではESI=0を維持。0x470A48..0x470A55または0x470A61..0x470A6Cでbuffer消費しgcount低32+1/carry高32+1、cleanupの0x470AB3は等値で0x426E00状態更新を飛ばす。この正常経路の「更新無し」は新規状態仕様として独立したものではなく今回のEOF対照。
  - 0x470A61..0x470A66のvtable+0x1C呼出しでEAXが変わっても、0x470A1Dで既に[EBP-0x14]へ退避している。最終返値候補は取得時EAXであり消費時のvcall返値ではない。ただし実際の出口のMOV EAX,[EBP-0x14]とRETの命令は保存ASMの切出しが0x470AC5で終わるため未観測、Ghidra疑似Cとの照合によるVERIFY。
  - 入力の部分ABI: caller 0x470610 PUSH EDI / 0x470611 CALL 0x470980、callee 0x4709AB MOV EDI,[EBP+8]を保存ASMで確認。最低1スタック引数は確実。callerにADD ESP,4が見えないためcallee-cleanup RET4の可能性が高いが末尾RETはASM原資料範囲外、ABI正式確定扱いにはしない。
  - 0x426E00の保存疑似Cでは新stateと例外maskの交差が非ゼロならios_base::failureをthrowしうる。throwされなければcaller 0x4705F0は0x470616でEAX=-1を判定後、0x470621..0x47063Bでstate&7異常を優先しLoadExceptionへ。sentry失敗、間接関数が他の挙動をするケース、例外ハンドラ経路は別VERIFY。
  - 情報の出典VA/CALL: 0x470611→0x470980、0x4709D5→0x42EC60、0x470A1B computed vtable+0x18、0x470A2F→0x470AAC（GhidraはCALLと登録、実ASMはJMP）、0x470AC5→0x426E00。**索引CALL分類とASMに不一致を発見**：0x470A2FはGhidra isCall=直接CALL記録だが実ASMではJMP。現行検索DBの呼出種別を blindly 信用せず、その他3箇所の0x470AAC参照も実ASMでJMPを確認（0x4709EF/0x470A5F/0x470A76）。分類問題は検索基盤ownerへ情報共有候補、当担当から索引を編集しない。
  - 次のREA P0: 保存済み許可ASMにある0x470ACA以降の正規末尾が既に独立保管されていないかだけ確認。見つからなければreturn ABIはVERIFYを維持。続いて直接CALL索引がJMPを誤分類するケースを許可範囲内の既存データと照合し、分類誤差を他ownerへHANDOFF候補として提示（他ownerファイル編集禁止）。
  - 注意（分類上の補正）: Ghidraが0x470AAC宛edgeをUNCONDITIONAL_CALLと付すのは、物理opcodeがCALLでなくJMPでも**tail-call等の関数間フロー**として分類した結果の可能性がある。したがって現段階で索引生成の「不具合」とは断定せず、ASM opcodeと機械call-edgeの意味論の差としてVERIFYに置く。再実装・フックで戻りアドレス/スタック効果を決める際は実ASMのJMPを一次根拠とする。
  - 到達性の厳密な限定（上記結論の補正）: 「正常帰還できればcallerで必ずstate&7非ゼロ」という表現はcleanup末尾の仮想CALL+0x08がstream状態を変更しないことを暗黙に仮定していた。**直接証明できたのは0x470AC5→0x426E00へ渡す入力に0x03が必ず含まれること、および0x426E00の正常帰還直後にstate&3が立つことまで**。0x470AE3仮想CALLの副作用とepilogueを独立確認するまでは最終caller到達時のstate&7はVERIFYのままとする。今回の重要成果は「EOF枝でflag3を組み立て状態更新するコードが存在すること」の確証。
- **Original author caveats:** - 注意（分類上の補正）: Ghidraが0x470AAC宛edgeをUNCONDITIONAL_CALLと付すのは、物理opcodeがCALLでなくJMPでも**tail-call等の関数間フロー**として分類した結果の可能性がある。したがって現段階で索引生成の「不具合」とは断定せず、ASM opcodeと機械call-edgeの意味論の差としてVERIFYに置く。再実装・フックで戻りアドレス/スタック効果を決める際は実ASMのJMPを一次根拠とする。 / - 到達性の厳密な限定（上記結論の補正）: 「正常帰還できればcallerで必ずstate&7非ゼロ」という表現はcleanup末尾の仮想CALL+0x08がstream状態を変更しないことを暗黙に仮定していた。**直接証明できたのは0x470AC5→0x426E00へ渡す入力に0x03が必ず含まれること、および0x426E00の正常帰還直後にstate&3が立つことまで**。0x470AE3仮想CALLの副作用とepilogueを独立確認するまでは最終caller到達時のstate&7はVERIFYのままとする。今回の重要成果は「EOF枝でflag3を組み立て状態更新するコードが存在すること」の確証。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0535_T014_CATCH_RETHROW_MASK_CONTRAST_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0535_T014_CATCH_RETHROW_MASK_CONTRAST_STATIC.md`; actual source SHA256 `BF459AFD1692F5E319C929A7DE23C279C9887701018671CBF307957406EF1228` (5804 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - 保存済み擬似CコードSHA: 0x470A78=43CF83D92FE754DFBA87E9F086D535174B8FEFAA0E967688E96DC150683CA79C、0x470AAC=EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D、0x426E00=7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43。
  - ## 新規差分：catch時の再送出と通常EOF時の新例外は別経路
  - catch入口0x470A78の保存実ASM: 0x470A82 MOV EAX,[ECX+0xC]→0x470A85 OR EAX,4、0x470A88 CMP [ECX+0x38],0、0x470A8E OR EAX,4（重複）、0x470A91 PUSH 1→0x470A93 CALL 0x426E00。元のstateにbadbit=4を必ずORして更新関数へ渡す。
  - 0x426E00の既存Ghidra疑似C（新REA VERIFIEDではない）: field state=[incoming EAX]&0x17、交差=exception_mask & incoming EAX &0x17。交差0ならreturn、交差非0かつ第2引数!=0なら__CxxThrowException_8(0,0)を呼ぶ。これは既存例外再送出の候補であり、ASMによるcallee内部の確証は今後VERIFY。
  - catchは第2引数1なので、badbitを含む新状態とexception maskが交差すればrethrow候補、交差しなければ正常return。続いて0x470A98で[EBP-4]=1、0x470A9Fで継続0x470AA5を返す。0x470AA5はEDI復元・EBX/ESI=0化を経て0x470AACの共通cleanupへ合流する。
  - 前回0443の通常EOF経路（sentry成功→virtual +0x18 が EAX=-1）: 0x470A25 LEA ESI,[EAX+4] => ESI=3、0x470AB7..0x470AC5で oldstate|3（buffer==nullなら更に|4）を作り、PUSH 0で0x426E00。exception_maskが交差すると、badbit > failbit > eofbit相当のメッセージで新ios_base::failureを構築する候補。catchのPUSH1/rethrowとは異なる。
  - 重要な関数関係: 0x470A93→0x426E00（catch）、0x470AC5→0x426E00（normal cleanup）、0x470AE3=未解決computed CALL vtable+0x08。0x470A78はGhidra Catch_All・size45、0x470AA5が関数範囲直後に位置するが、前回既知の境界規則なので新規として重複計上しない。
  - 次のP0: 0x470AE3のvtable+0x08仮想calleeの既存許可済み証拠を照合し、stateを書き換える可能性を評価。0x470ACA以降の実ASMが正規保存済み資料にない場合はABI推測をVERIFIEDへ昇格させない。既存同ID/owner競合確認後の正本統合のみ許す。
- **Original author caveats:** - 実ASM後半探索: exe配下既存*.txtの文字列00470ACAをread-only検索し一致0件。これは探索対象内の未発見であり、バイナリ上に存在しない証明ではない。新Ghidra抽出は実施せず、後半ABI=VERIFY維持。 / - 次のP0: 0x470AE3のvtable+0x08仮想calleeの既存許可済み証拠を照合し、stateを書き換える可能性を評価。0x470ACA以降の実ASMが正規保存済み資料にない場合はABI推測をVERIFIEDへ昇格させない。既存同ID/owner競合確認後の正本統合のみ許す。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0638_T014_VCALL04_08_PAIR_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0638_T014_VCALL04_08_PAIR_STATIC.md`; actual source SHA256 `E144C64E01CAADDB91FDF39A0057337F920D8F15F7E9561F3791955B3CD9B9C9` (5410 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - 今回の既存機械疑似C抽出VA/codeSHA: 0x470980=850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446、0x470AAC=EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D。
  - 比較側既存機械疑似C抽出VA/codeSHA: 0x42E700=E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76、0x42E7D4=5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C。
  - ## 新規の独立横断比較：2系統でvptr+0x04→+0x08が前後対応
  - 1byte reader 0x470980: buffer!=NULLなら冒頭のcomputed CALL site 0x4709D0 で vptr+0x04 を呼び、その後 0x42EC60 sentry、byte取得・gcount/EOF状態処理。通常終了/失敗sentryは共通 0x470AAC へ合流し、0x470AE3 の computed CALL vptr+0x08 を buffer!=NULL で呼ぶ。
  - block reader 0x42E700: buffer!=NULLなら冒頭の computed CALL site 0x42E74E で vptr+0x04 を呼ぶ。sentry失敗時の親関数 inline cleanup と、成功時に0x42E7A2でつなぐ共通cleanup 0x42E7D4 の computed CALL site 0x42E810 の双方が vptr+0x08 を呼ぶ。
  - 0x470AACでは 0x470AC5 の0x426E00状態更新CALLが +0x08(0x470AE3)より先にある。0x42E7D4でも状態更新CALL 0x42E7F2 は+0x08(0x42E810)より先。よって『+0x08が読込後の後処理として使われる』順序が二系統で再現。
  - 直接CALL(参照DB): 0x470980→0x42EC60 site=0x4709D5、0x42E700→0x42EC60 site=0x42E753、0x42E700→0x42E7D4 site=0x42E7A2、0x42E7D4→0x426E00 site=0x42E7F2、0x470AAC→0x426E00 site=0x470AC5。4個のcomputed CALL は実装先未解決として別記。
  - 既存実ASM: exe/T014_READER_CHAR_PROBE.txt SHA256=B42A217769E1E6EC3E770308665A6EA79E0F2BD31431D0710E664DA157E0EDAD。0x4709D0のcall eax(+4)は同資料で確認。0x470AE3/0x42E810等の命令列は今回実ASMで直接確認しておらず、Ghidra機械疑似Cとindirect索引による静的推論。
  - vftable条件付き基準0x0063848C、+0x04 slot0x00638490、+0x08 slot0x00638494は既存0137報告を再利用。既存pointer_refsが14/15 slotを収録していない事実も既知であり、新規欠損件数として計上しない。
  - symbols('basic_streambuf')結果0件。C++標準ライブラリからの関数名推測を実体の証拠に昇格させない。0x470ACA以降の実ASM、0x470AE3のcallee実体、0x470980 RET4/EAX、0x42ECF0 ABIは引き続きVERIFY。
- **Original author caveats:** - symbols('basic_streambuf')結果0件。C++標準ライブラリからの関数名推測を実体の証拠に昇格させない。0x470ACA以降の実ASM、0x470AE3のcallee実体、0x470980 RET4/EAX、0x42ECF0 ABIは引き続きVERIFY。 / - 次Golden設計（NOT RUN）: 同一streamのbuffer!=NULLとNULL、開始sentry成功/失敗、正常1byte/EOF、4byte block正読込/short-readを分け、+0x04/+0x08前後のvptr/stream state/gcount/例外型を比較。原本と新実装は今回いずれも未実行。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0737_T014_STREAMBUF_VIRTUAL_SLOT_SEMANTICS_ABI_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0737_T014_STREAMBUF_VIRTUAL_SLOT_SEMANTICS_ABI_STATIC.md`; actual source SHA256 `86FC7D61D60EE5E5C23AB538988BE9B665FAAE9C5D0C18987123149A6B2563A7` (5461 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - 0x42A460の新規照合: 先頭スロット0x0063848C→0x0042A460（旧pointer_refs既知）。疑似Cはvptrをbasic_stringbufのvftableに戻し、破棄helper・条件付きdeallocateを呼ぶので、先頭は削除デストラクタの高確度候補。codeSHA=5B13545504CA6CA932905AA01D4C4B918BC82F510E9AC4274E96240F54852D96。
  - +0x04（site 0x4709D0/0x42E74E）: 両readerの開始側、buffer非NULLならsentryより前に呼ぶ。_Lock相当の候補。callee未確定。
  - +0x08（site 0x470AE3/0x42E810、別途0x42E700のsentry失敗枝）: 全終了側で呼ぶ。_Unlock相当の候補。stateの副作用が無いことは未証明。
  - +0x18（site 0x470A1B）: 先読みで値を得る。後でbuffer pointerを進めるか+0x1Cを呼んで消費するため、非消費のunderflow相当という候補。0x470980 codeSHA=850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446。
  - +0x1C（site 0x470A66）: bufferから直接消費できない場合に呼ぶ。返値を使わずgcountを1加算するため、消費するuflow相当の候補。動的副作用は未検証。
  - +0x20（site 0x42ED07）: 0x42ECF0経由でブロックを読み、0x42E700のgcount低高32bitへ実取得数を加算。xsgetn相当の候補。stub codeSHA=509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21。
  - 5スロットを順序・用法で横断比較するとMSVC basic_streambufの_lock/_unlock/underflow/uflow/xsgetnという一貫した契約候補になる。先頭0x42A460は破棄系。この型付けは機能意味の仮説であり、vtable各slotの実ポインタ値を復元したものではない。
  - ## 新たに明確になった64-bit ABIの注意
  - 0x42ECF0の機械疑似Cはvoid __thiscallで3つのstack値を+0x20仮想関数へ転送する。一方0x42E700の疑似Cは戻りをundefined8として使い、64-bit gcountへ加算する。両者のvoid/uint64の型が一致せず、擬似C宣言をそのままhookシグネチャに採用不可。
  - 0x42ECF0→vtable+0x20 CALLsite0x42ED07、0x42E700→0x42ECF0 CALLsite0x42E77F。0x42E700 codeSHA=E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76。
  - 0x470AACの旧疑似CはEH状態[EBP-4]=-1→+0x08仮想CALL→ExceptionList復元→親[EBP-0x14]返値という順序を示すが、保存実ASMは0x470AC5で切れる。epilogue/RET4・仮想unlock非throwは決め付けない。cleanup codeSHA=EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D。
- **Original author caveats:** - xsgetn相当ならスタックはdestポインタ1 dword + 要求数streamsize 2 dwordという3 dwordに整合し、戻り値EDX:EAXの64-bit実取得数が自然なABI候補。ただし実ASMでPUSH順・RET n・EDX:EAX更新を未確認のためVERIFY維持。 / ## 検証境界・差分・次手
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

### SOURCE_KEY: `REA_20261022_0843_T014_BYTE_WIRE4_PAIR_STATIC.md`

- **Owner/path:** REA / `rea_lab/decomp_task/REA_20261022_0843_T014_BYTE_WIRE4_PAIR_STATIC.md`; actual source SHA256 `0E1EC82063B0CBC91CFFFBD6CCF17A22FE4D7888DE42B8B6E1FCA4C032646082` (6351 bytes, checked 2026-11-02 JST).
- **Research ID:** not present / `UNKEYED_SOURCE`, not minted here.
- **PC-only same-hour evidence candidates:** No matching same-hour EVIDENCE JSON found.
- **Native-source evidence excerpts (not rerun):**
  - ## 今回の新規STATIC：ローダーとライターの1byte/4byte非対称な保存幅
  - `0x4707D0`: 0x4707D3 PUSH 0、0x4707D5 PUSH 4、0x4707D7 PUSH 0x00B060E8、0x4707DC PUSH ESI、0x4707DD CALL 0x42E700。固定長4byteを一時領域へ読み込む。成功状態の場合のみ0x47081E MOV DL,BYTE [0x00B060E8]、0x470824 MOV EAX,[ESP+0x14]、0x470828 MOV BYTE [EAX],DL。出力先への1byte storeは実ASM確認。
  - 同0x4707D0の状態判定は0x4707EB..0x4707FC。下位state &7異常なら0x470802/0x470819 LoadException経路へ進み、0x47081Eコピー処理を経由しない（それ以前の内部例外可能性は別）。
  - `0x4708A0`: 0x4708B1 MOVZX EAX,AL（元byteを0..255へゼロ拡張）、0x4708B6 MOV DWORD [ESP+0x14],EAX、その格納位置を0x4708AD LEA ECX,[ESP+0xC]で事前取得。0x4708A9 PUSH 0、0x4708AB PUSH 4、0x4708B4 PUSH ECX、0x4708B5 PUSH EDX、0x4708BA CALL 0x4628F0。byte値をzero-extended DWORDの一時4byte領域として出力関数へ渡す。実ファイル書込副作用は未実機。
  - 旧WAVE5は0x4708A0と0x4707D0の個別CALL存在を既知としたが、同一型の4byte wire→1byte fieldの入出力対称性をこの回に新規横断照合。古い結果を新規関数として加算しない。
  - 書込親0x596AA0: 0x596ADE MOV AL,BYTE [EBP+0x1C] →0x596AE3 CALL 0x4708A0、0x596AE8 MOV AL,BYTE [EBP+0x1D] →0x596AED CALL 0x4708A0。よって隣接1byteメンバーを2度呼出し、正常時4byte transferを2回指示する（合計8byteの対象部分）。次に0x596AF2 DWORD [EBP+0x5C]を取得。
  - 読込親0x5964C0: 既存Ghidra擬似Cでは0x59650D CALL 0x4707D0に `param_1+0x1C`、0x59651D CALL 0x4707D0に `param_1+0x1D` を渡し、次の0x596529 CALL 0x470700には `param_1+0x5C` を渡す。後者のABI・ESI等の引数モデルはGhidra機械復元なので完全確定ではないが、親の対称関数順序は直接CALL索引と一致。
  - Ghidra codeSHA: 0x4707D0=A6F57840EB564D48C00D8757E6CE0CDEB98DE66016C5C5C327BC6E429DF3A45B、0x4708A0=4A51D26D7141B63406F7EDEF0FE7A04E5B34AE4DC8BD7905C3A2FDDDE08ADD43。
  - Ghidra codeSHA: 0x5964C0=A3A43FB167F7CEDE8A2E9AB94D364F8B62CC2F13A62294BDB3BA1868C7C5F41A、0x596AA0=AC59C5508CEA1686A98F84FF9D72F58F7C476D70CB6479E5DCD5A189B3858D11。
  - Ghidra検索の直接CALL: reader 0x59650D/0x59651D→0x4707D0、0x596529→0x470700、writer 0x596AE3/0x596AED→0x4708A0、0x4708BA→0x4628F0、reader 0x4707DD→0x42E700。
  - 非正規4byte例 `00 01 00 00`→byte0、`FF 00 00 01`→byte255、`78 56 34 12`→byte120という低byte投影候補（上位3byte非ゼロをreaderが検査する直接命令は今回の0x4707D0本体では見当たらない）。読込前段や後段の検証有無はVERIFY。
  - 重点P0は0x4707D0/0x4708A0で実ASM局所処理を確認。0x4628F0の実バッファへのwrite到達性、0x42E700の実取得数とEOF/exception、親0x5964C0の正確な引数ABI、actual wire file bytesはVERIFY。インターフェイスを推測で厳密フック型にしない。
  - 0x42ECF0の0x42ED07 indirect CALL +0x20、EDX:EAXの64bit戻り値は依然未解決。0x470AE3 +0x08の実calleeと副作用も旧VERIFY。今回ここを解決済みとはしない。
  - 次P0: 0x5964C0の2つのbyte格納先callsiteの既存ASM照合で引数ABIを確定、writer 0x596AA0のentry objectとreader 0x5964C0同型接続、4byteワイヤ値上位3byteの検証有無を親/下層から検査。必要なら0x4708A0→0x4628F0のwrite pathを既存DBのみ追う。
- **Original author caveats:** - 0x42ECF0の0x42ED07 indirect CALL +0x20、EDX:EAXの64bit戻り値は依然未解決。0x470AE3 +0x08の実calleeと副作用も旧VERIFY。今回ここを解決済みとはしない。 / - 次P0: 0x5964C0の2つのbyte格納先callsiteの既存ASM照合で引数ABIを確定、writer 0x596AA0のentry objectとreader 0x5964C0同型接続、4byteワイヤ値上位3byteの検証有無を親/下層から検査。必要なら0x4708A0→0x4628F0のwrite pathを既存DBのみ追う。
- **Action:** map to actual older or newer source research ID by VA + source SHA + semantic correction, then mark DUPLICATE_LINKED or adopt genuinely distinct safe evidence by curator. NOT READY.

## Ownership/curation gate

This document is source conservation, not new ID generation, not a formal REF replacement and not proof of gameplay. Do not alter existing owner files. All 16 entries need manual distinction between identical observations and genuine additions; no direct develop/symbol/struct edits by the REA owner. Safety refused operations remain blocked.
