# REA 2026-10-20 historical owner QC and native findings

Private REA owner intake. Eight distinct pre-existing research/QA IDs, original PC Markdown report SHA rehashed read-only on 2026-11-02 JST. Existing native/ASM/ABI claims are excerpted only in allowed scope; refused Wave6, forbidden VA and prior denied evidence remain outside this document. No REA/Ghidra/executable replay or new verified five-method set; original Golden PASS0, READY0. This is not formal curator adoption in develop.

### REA-20261020-0035-T013-T031-STEALTH-RNG-CANDIDATE-CARDINALITY-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_0035_T013_T031_STEALTH_RNG_CARDINALITY_QC.md`, SHA256 `B3BF139B30C5C9AA4F2FCCA96C4C8D59E133BA80DDCAA28088BDE4C43A20632D`, 5478 bytes.
- **Research type:** RESEARCH_QC; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - [SOURCE SHA] 保存済みrun 20261009T225741694Z source=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。承認済みコピー現物の今回の再SHA測定なし。
  - [PARENT] 0x57B870 Ghidra assembly ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c / callees ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203。info ev_c4fcdda0f9486944ccdcfe1354a6d2e37f2b68761dfd2e47b7df9a11cd367612、pseudo ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc、callers ev_911883dad3560c441dc40b2e53fe8fb1e83d4b85c4cbf622e80eb7ed59e4a8c4。親は5方法既存証拠。
  - [CHILD SOURCE / LIMIT] read-only既存exe/T013_TARGET_SELECTOR_PROBE.txtの0x514D60..0x514F0Bアセンブリ窓。0x514D60自身のREA5方法evidenceは未取得、関数単位VERIFIEDへ昇格禁止。保存済みx86局所照合/意味VERIFY。
  - [CHILD ENTRY] 0x514D81/0x514D86で候補第1配列begin/end=(base+0x48,+0x4C)、差をSAR2して要素数。0x514DA2で空なら第2配列開始0x514E75へ。
  - [PER CANDIDATE] 第1配列では0x514DB1のbyte(candidate+0x1867C)!=0を除外、0x514DBEでcandidate==selfを除外。その後0x514DC4でdword(candidate+0x1C0)!=0の時だけ0x514DCF CALL 0x5B6EABを1回実行する。負数の非0値でもCALL自体は行う。0x514DEDはrollとの比較、当落にかかわらずこのCALLは消費済み。
  - [POOL 2] 第1配列を全て走査後、距離/範囲条件で0x514E69から早期RET、そうでなければ0x514E75から第2配列(base+0x58,+0x5C)走査。第2ループ0x514E8C..0x514EE8には直接0x5B6EAB呼出なし。第2配列にも別callee間接作用が無いとは未証明。
  - [CHILD LOCAL COUNT / NORMAL VALID POINTERS] K=Σ_{p in firstPool}[byte(p+0x1867C)==0 ∧ p!=self ∧ dword(p+0x1C0)!=0]。Kは0..firstPoolCount。同じ候補集合・変化しない状態ならKの件数は順序非依存だが、rand値が各候補へ割り当たる順序と採否は候補列順序に依存する。第2配列だけに候補がある場合K=0。
  - [PARENT REACHABILITY] 0x57B87F: signed(Unit+0x1E534)>=signed global[0x65BCAC]で更新枝、かつ0x57B930でUnit+0x1E570==0（cached target未保持）の場合に限り、0x57B983 CALL 0x514D60へ到達。cached targetありなら0x57B9BBへ移り子CALL無し。
  - [SELECTED BASE] 0x57B938 signed(Unit+0xC8)<0の場合だけ0x57B940 CALL randのroll→0x57B95E比較で、0x57B966のbase=[Unit+0x1D4]または0x57B974のbase=[[Unit+0x1D4]+0x1C]を選択。Unit+0xC8>=0なら後者。poolの内容・Kがこの条件付きrandom結果で変わる可能性がある。
  - [ORDER] counter到達時の親0x57B8FE rand →（T&&Nなら親0x57B940 rand）→0x514D60第1配列の該当候補ごとの0x514DCF rand→（S&&Nなら親0x57BA10 rand）の順であり、子候補側はpool順序を維持すること。下位calleeの未知消費があり得るため全PRNG列の確定とはしない。
  - [BOUNDARY / NEXT] 0x514D60は5方法不足につきVERIFY、未確認の他callee消費もVERIFY。次回T013/T031では原作のstealth raw倍率定数・signed境界の既存証拠を点検し、候補firstPool orderを再実装の検査条件へ落とす。T010/T012死亡処理も優先維持。
- **Boundaries and possible errata:** - [MASTER/GOLDEN] MASTER末尾2026-10-19 23:48 checkpoint192（正式590予定値）、34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0、strict MATCH0、ゲーム再実装率は測定していない。 / - [BOUNDARY / NEXT] 0x514D60は5方法不足につきVERIFY、未確認の他callee消費もVERIFY。次回T013/T031では原作のstealth raw倍率定数・signed境界の既存証拠を点検し、候補firstPool orderを再実装の検査条件へ落とす。T010/T012死亡処理も優先維持。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

### REA-20261020-0135-T013-T031-STEALTH-QUANTIZED-THRESHOLD-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_0135_T013_T031_STEALTH_QUANTIZED_THRESHOLD_QC.md`, SHA256 `CEB576ABA9498F3B87ACD09430FA13A9FA095E5AA8CB314FF60F133085ADE7C4`, 5070 bytes.
- **Research type:** RESEARCH_QC; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - [SOURCE] target SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（保存REA証拠に紐づく値、今回現物ハッシュ未計測）。旧原本実行/編集なし。
  - [LOCAL ASM] 既存exe/T013_TARGET_SELECTOR_PROBE.txt VA0x514DB1..0x514DF5: candidate+0x1867C!=0は除外、candidate==selfは除外、candidate+0x1C0==0なら乱数CALLをskip、それ以外は0x514DCF CALL0x5B6EAB→0x514DD8 FILD→0x514DDC FMUL[0x63B080]→0x514DE2 FMUL[0x63B060]→0x514DE8 CALL0x5D1B80→0x514DED CMP candidate+0x1C0,EAX→0x514DF3 JG skip。
  - [CONSTANTS] data/T013_AI.md §stealth: 0x63B080=1/32768、0x63B060=100.0、Unit+0x1C0=stealth。既存CRT rand(0x5B6EAB)は0..32767の15bit値を返す。x87入力積は有限で0以上100未満。
  - [DERIVED NORMAL-FINITE] 0<=r<=32767で正常なゼロ方向32bit整数変換なら roll=floor(100*r/32768) ∈[0,99]。ステルスsは符号付きdword、候補除外条件は s>roll（signed JG）、乱数を引く条件は s!=0。抽選結果とdraw有無を混同しない。
  - [EXACT THRESHOLD COUNT] 15bitの可能な入力32768通り中、正の整数1<=s<=100の除外入力数 N(s)=ceil(32768*s/100) (s=100も32768)；s<=0ではN=0、s>=100ではN=32768。ただしs=0はDRAW0、s<0とs>=100はDRAW1。これは生rand出力空間の組合せ分布であり、実機戦闘の確率測定ではない。
  - [RELATED] parent 0x57B870 saved assembly ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c / callees ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203。子0x514D60はREA5方法未充足につき新VERIFIED扱い禁止。
- **Boundaries and possible errata:** - [MASTER] 最新末尾研究E checkpoint193 (2026-10-20 00時台)、34 Task DONE9/IN_PROGRESS21/VERIFY4、旧EXE実機golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。 / - [NEXT] T013/T031: 同じrand15で候補順/stealth境界の期待抽選cursorを数学テスト化（実機とは区別）、原作FPU profile/候補本体合法到達はVERIFY。研究P0のT010/T012通常死亡/選択復帰も維持。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

### REA-20261020-1033-T013-T031-ORDER-CURSOR-SYNTH-QC-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_1033_T013_T031_ORDER_CURSOR_SYNTHETIC_QC.md`, SHA256 `5756BA5DDD50C713D57EBF6BBC2295344DDD0E3B6B019CD7DE22AAC8350223AD`, 5178 bytes.
- **Research type:** RESEARCH_QC; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - [SOURCE] 承認済コピー rea_lab/targets/hakushin067_Vahren.exeのread-only Get-FileHashはE8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187に一致。原本ZIP/EXEにはアクセス・変更・起動なし。
  - [EVIDENCE] 親0x57B870の保存Assembly ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c、callees ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203（run 20261009T225741694Z）。子0x514D60は保存exe/T013_TARGET_SELECTOR_PROBE.txtのASMであり5手法未揃い、子VERIFIEDへの昇格禁止。
  - [NATIVE ORDER] 第1候補loop：0x514DB1 disabled除外→0x514DBE self除外→0x514DC4 stealth !=0→0x514DCF CRT rand→0x514DE8 int変換→0x514DED signed CMP/0x514DF3 JG除外→0x514DF5以降の距離評価。乱数は距離・最終採用可否が決まる前に消費。
  - [SECONDARY] 0x514E48..0x514E72第1候補の成立状況等による早期帰還後、未帰還時は0x514E75から第2候補loopへ。第2loop直接CRT randなし。距離・fallbackの正式意味/到達ケースはVERIFY。
  - [DERIVED INVARIANTS] 各候補状態/配列構成が走査中不変・正常終了という条件で、同一第1候補multisetの順序変更は当該子の直接draw数 K=Σ[enabled ∧ !=self ∧ stealth!=0] を変えない。一方、どの候補がどのrand値を受け取るか・stealth通過集合は変わり得る。続く距離選択・第2候補へのfallback・未来のAI更新結果はこの局所証拠だけでは確定できない。
- **Boundaries and possible errata:** - [SECONDARY] 0x514E48..0x514E72第1候補の成立状況等による早期帰還後、未帰還時は0x514E75から第2候補loopへ。第2loop直接CRT randなし。距離・fallbackの正式意味/到達ケースはVERIFY。 / - [DERIVED INVARIANTS] 各候補状態/配列構成が走査中不変・正常終了という条件で、同一第1候補multisetの順序変更は当該子の直接draw数 K=Σ[enabled ∧ !=self ∧ stealth!=0] を変えない。一方、どの候補がどのrand値を受け取るか・stealth通過集合は変わり得る。続く距離選択・第2候補へのfallback・未来のAI更新結果はこの局所証拠だけでは確定できない。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

### REA-20261020-1837-T013-RADIUS-TIE-FPU-STATIC-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_1837_T013_RADIUS_TIE_FPU_STATIC_QC.md`, SHA256 `FFAC7F74ABAD7300FC4E9DE2A4AB0E228ED3C590E39DD6DA4F2496BBBE99B9A7`, 3983 bytes.
- **Research type:** RESEARCH_QC; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - [SOURCE] rea_lab/targets/hakushin067_Vahren.exe はread-only SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。保存Ghidra run 20261009T225741694Zも同SHA。
  - [EVIDENCE] 親0x57B870 Assembly ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c、info ev_c4fcdda0f9486944ccdcfe1354a6d2e37f2b68761dfd2e47b7df9a11cd367612、callees ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203。子0x514D60は既存exe/T013_TARGET_SELECTOR_PROBE.txtの保存ASMで5方法未揃い、独立VERIFIEDには昇格不可。
  - [PRIMARY DISTANCE] 0x514E1E FLD保持最短距離→0x514E22 FCOM新候補距離→0x514E26 TEST AH,0x41→0x514E29 JNE skip。正常な有限値では保持距離<=候補距離で更新せず、厳密に近い場合だけ0x514E2D以降で更新する。同距離候補は既存の先着選択が残る。
  - [RADIUS EQUALITY] 0x514E48で主候補NULLならsecondaryへ。非NULL時、0x514E50 FILD主候補+0x18C、0x514E56 FCOMP保持距離、0x514E5A TEST AH,1→0x514E5D JNE secondary。正常有限値では半径<距離だけsecondaryへ進み、半径==距離も0x514E5F..0x514E72の早期帰還側となる（境界はinclusive）。
  - [SECONDARY TIE] early returnしない場合、0x514E75からsecondary。0x514ECA FCOM新候補距離→0x514ED2 TEST AH,0x41→0x514ED5 JNE skip。ここでもstrict closerのみ更新、主pool保持距離を明示リセットしない。主/副で同距離なら既存選択を維持する。
  - [LIMIT] x87 unordered/NaN、signed32平方和overflow、0x5E3B70の数値契約、実Unit属性意味、呼出元が候補をどう使うか、原作の可視target結果は未確定。x86局所テストを実ゲームGolden/MATCHに換算しない。
- **Boundaries and possible errata:** - [OWNER/STATE] REA専用／T013 P1・T031参照。STATIC SAVED X86（分岐命令）／VERIFY（ゲーム中意味）。新Ghidra関数解析0、今回新VERIFIED0、旧EXE実機NOT RUN。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

### REA-20261020-1941-W6-P0-STATUS-QC-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_1941_WAVE6_P0_PREFLIGHT_STATUS_QC.md`, SHA256 `2E6719FD4374BB0D5D4F9F5EAEDF5FA805E6334BFC9D23DE9C22F42AA6BE6FEB`, 3183 bytes.
- **Research type:** STATUS_AUDIT; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - [SOURCE] 承認済 rea_lab/targets/hakushin067_Vahren.exe をLocalでread-only SHA256測定し、E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致（2026-10-20T19:41+09）。
  - [RUN] 最新runs/20261011T153309850Z/RUN_RESULT.json はREA6.1.0・Ghidra12.1.4で0x5158A0/0x57CFA0/0x57CFD0/0x5155C0の5方法をVERIFIED。最新sync logs/progress_sync_20261011T153958076Z.json: W1=16/16,W2=10/10,W3=10/10,W4=12/12,W5=16/16。累計64/64(P0 29/29,P1 35/35)。今回新Ghidra 0、新Evidence ID 0、新VERIFIED 0。
  - [P0 SAFE XREF] T014 0x470980は既VERIFIED親0x4705F0の保存callee evidence ev_661507e7456c44d65dd153fff0f2c6b8de0e33a9519370d794118fae0def6743 と親ASM ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d の0x470611 CALLで参照。同0x470700親は0x42E700を0x470713でCALL（callee ev_3f9a89a60c30eee71f662be8ef197b9016cfe610caae887926287dcb5d131286）。対象2関数の入口・5方法は未取得・TODOであり親情報を子のVERIFIEDに流用しない。
- **Boundaries and possible errata:** - [MASTER/GOLDEN] 最新MASTER cp195、DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。QUEUE/PROGRESS rawは既往EPERMにより古く、sync記録を優先する。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

### REA-20261020-20H-RUNNER-VERSION-REFUSAL-FIREWALL-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_20H_RUNNER_VERSION_REFUSAL_FIREWALL_QC.md`, SHA256 `0C6FA06220DDDD5C701F03387FFA476D15CACD82F1AECCD6024BA79CAA9D6647`, 3647 bytes.
- **Research type:** STATUS_AUDIT; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - Safety/preflight-only checkpoint; substantive denied findings are not published.
- **Boundaries and possible errata:** - [MASTER/GOLDEN] 本run確認MASTER最終checkpoint195、研究DONE9/34・IN_PROGRESS21・VERIFY4、旧EXE実機golden PASS0・新旧strict MATCH0。ゲーム再実装率は測定していない。MASTER末尾のE READY候補は今回のREA数に含めない。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

### REA-20261020-22H-T014-DIPLO-LIVE-VECTOR-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_22H_T014_DIPLO_WRITER_LIVE_VECTOR_BOUND_QC.md`, SHA256 `5CD5EFEB6BD27C974B42CAE39A27CC4F347A05C96ADA85987A3AD6D6B01D403A`, 4562 bytes.
- **Research type:** RESEARCH_QC; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - [SOURCE] 保存run runs/20261011T144115307Z（REA6.1.0/Ghidra12.1.4）の0x471D20、source SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。2026-10-20 22:35 JSTに承認済コピー現物SHA一致。
  - [EVIDENCE] 0x471D20は5方法既存VERIFIED: info ev_d66eb9ca2ede2dddefec4ffa0700384bde6cdbe4d00f9186cf00ff67748de6fc、pseudo ev_ab5115883f3f7287b9e69a76b95333a8ddd343252dfc9c1efdafb3f4db81d846、assembly ev_64adbba14e1cee99ca12f12987032aa749c2890ee33057c941c4d0b3eed1fe6f、callers ev_a459496a5ab977b94c768d186aefbfc6f58bb2cb97dcc009e0be9b470f192a56、callees ev_8f32e24032fa7db1f4ddd3212cbf805c0509f176888721d560966984d495d307。
  - [PREFIX] 0x471D26..0x471D37はEDI+0x9,+0xAを各AL→0x4708A0。0x471D3C..0x471D63はEDI+0x14,+0x38の各DWORDを4byte長引数で0x4628F0へ渡す。calleeの内部効果はTODO/VERIFY。
  - [VECTOR BOUND] 0x471D68..0x471D75でEDI+0x18(begin),+0x1C(end)の差をSAR2しcount相当値として計算。0なら0x471D95へジャンプし要素writerを飛ばす。
  - [DEAD GUARD] 0x471D73 XOR EBP,EBP=0、0x471D75 TEST EAX,EAX; 0x471D77 JZ 0x471D95を通過したときEAXは非0。直後0x471D79 CMP EAX,EBP; 0x471D7B JBE 0x471DA6 はunsigned EAX<=0だけが条件であり、この直線入口では到達不能。疑似コードの『if(iVar1!=0){if(iVar1==0) invalid vector&lt;T> subscript}』を実到達する通常例外仕様として扱わない。
  - [LIVE REEVALUATION] 0x471D7Dで[begin+EBP*4]をESIへ読み0x471D80 CALL 0x470830。CALL後の0x471D85/88でbegin/endを再取得し差分を再計算、0x471D8D INC EBPの後0x471D91 CMP EAX,EBP; 0x471D93 JAで次要素へ。要素数は入口で固定していない（ただしcalleeによる変化が実在するとは未証明）。
  - [TRAILER] 0x471D95でESI=0x68B3A8、0x471D9A CALL 0x470830はcount=0の場合にも必ず実行。固定文字列実バイト/意味は未確認につき単に終端候補とする。
  - [CONTRACT] 正常不変vector n=0/1/2について要素writer呼出回数はn、固定0x68B3A8渡しが各1回。n=0でも2byte+2DWORDの前置書込後に固定参照を渡す。writer成功/バイト列/reader対称性/例外はNOT RUN・VERIFY。
  - [RISK] begin>end、end-beginの4byte非倍数、0x470830の副作用や失敗時stream state、0x68B3A8実文字列、0x471AF0 readerとの対応は未確定。到達不能な局所ガードの存在だけで全実行の例外安全性を保証しない。
  - [NEXT] T014担当が0x471D20を実装比較する際、n=0/1/2+終了参照の固定順とwriter後count再計算を観測点に分離。優先P0の0x470980/0x42E700は安全な正式Wave/環境整合後のみ5方法取得。T010/T012 0x575F71/0x575F91の未解明正常帰還は別途既存証拠で継続。
- **Boundaries and possible errata:** - [DEDUP] 既存REA_WAVE5_SAVE_IO_VECTOR_AUDIT_20261011_2347の『byte×2、DWORD×2、vector要素ごと、末尾追加』は既知・再計上0。本回の差分はwriter各CALL後のbegin/end再読と疑似コードの不可能subscript条件のASM訂正。 / - [MASTER/GOLDEN] 最新MASTER checkpoint195で研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。既存QUEUE/PROGRESSはEPERMでstale。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

### REA-20261020-2335-T014-DIPLO-MODE0-ZEROCOPY-01

- **Owner REA source:** `rea_lab/decomp_task/REA_20261020_2335_T014_DIPLO_MODE0_ZERO_COPY_CLEAR_QC.md`, SHA256 `31BBFA894BCB77975D6058E513A5D85E3BBDD087535C1E6270EDC35B4B4927F3`, 4489 bytes.
- **Research type:** RESEARCH_QC; source owner provenance and past limitations retained, not counted as fresh discoveries.
- **Allowed old static data/ABI notes:**
  - [STATE/OWNER] REA専用・T014。2026-10-20 23時台JST、Local Compactによる保存済みGhidra証拠のread-only静的再照合。新Ghidra取得なし、原作実機NOT RUN、疑似コードを実ソース扱いしない。
  - [SOURCE] runs/20261011T124000308Z/471AF0_procedure_assembly.json (ev_f7d8db97a2ec936312735e2bb6c29f421ff95b1eeeccd1a089237dfda632947b)、pseudo (ev_1e776fb470e6e934d7fffa736600daa070a5e3e009552f7951f653edbc00f871) 、info (ev_29f03715d97de300e639f60e6e2ae24d400cd4bff3edb921ae126c14e4cb09b5)。親run complete=true、failure=null、REA6.1.0/Ghidra12.1.4、source SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
  - [MODE BRANCH] 0x471B71 CMP byte [EBP+8],0; 0x471B7C JNZ 0x471BA6。mode !=0ならvector clear区間をskip、mode=0なら既存begin/end比較へ。
  - [NONEMPTY] 0x471B7E MOV ECX,[EBX+1C] end、0x471B81 MOV ESI,[EBX+18] begin、0x471B84 CMP、0x471B86 JZ 0x471BA6。空配列はcopy/clearなし。
  - [ZERO-BYTE MEMORY COPY] 既存配列非空時、0x471B88 MOV EAX,ECX →0x471B8A SUB EAX,ECX=0 →0x471B8C SAR EAX,2=0 →0x471B8F LEA EDI,[EAX*4]=0。0x471B96 PUSH EDI(=0),0x471B97 PUSH ECX,0x471B98 PUSH ESI、0x471B99 CALL 0x5B6720 (CRT memcpy相当)。この局所直線経路の転送長は常に0で、配列内容のコピーは起こらない。
  - [LOGICAL CLEAR] 0x471BA1 ADD EDI,ESI → 0x471BA3 MOV [EBX+1C],EDI。EDI=0なのでend=beginに設定。基底beginとcapacity(EBX+20)はこの範囲で不変。すなわちsize=0への論理clearであり、storage bytesのゼロ消去や解放ではない。
  - [PSEUDO CORRECTION] Ghidra pseudoには memcpy(_Dst,end,0) と end=_Dst の形が現れている。0x471B88..0x471BA3の機械語によれば正常直線経路で「既存全要素をmemcpyで複製する」解釈は誤り。
  - [MODE CONTINUATION] mode=1は0x471BA6から文字列reader 0x4705F0を反復し、0x471BD9 JZ 0x471BF5の条件を通過せずに0x471BA6へ戻るので、当該loopでは文字列→pointer変換0x467F40とvector追加0x471CCBをskipする。一方mode=0は非空tokenを0x467F40で変換し、既存pointer比較0x471C53等を経てappendし得る。
  - [SCOPE] mode=1が上位処理で何を意味するか、0x4705F0のEOF/LoadException、vectorの外部alias・実capacity、0x5B6720の異常呼出副作用、pointer intern同値と保存データ互換性はVERIFY。内部の無copyは正常有効配列での局所静的分岐に限定。
  - [DEDUP] 既REA_T014_DUAL_MODE_CALLSITE_CONFIRMED_20261012_1142はmode0/1 caller区別を確定済み。既REA_WAVE5_SAVE_IO_VECTOR_AUDIT_20261011_2347はwriter反復を確認済み。本増分はreader 0x471B88..0x471BA3のzero-copy lengthとlogical clear、およびmode=1のappend skipの命令証拠。既存成果再VERIFIED加算なし。
- **Boundaries and possible errata:** - [SCOPE] mode=1が上位処理で何を意味するか、0x4705F0のEOF/LoadException、vectorの外部alias・実capacity、0x5B6720の異常呼出副作用、pointer intern同値と保存データ互換性はVERIFY。内部の無copyは正常有効配列での局所静的分岐に限定。 / - [MASTER/GOLDEN] 最新MASTER checkpoint195、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Status:** PUBLISHED_INTAKE or STATUS_ONLY; formal new VERIFIED0, original game Golden PASS0, READY0. Prior safety refusal remains BLOCKED without retry.

## Dedicated KB curator acceptance

Reconcile by original research ID, report SHA, VA/ASM and supersedes relation; do not reclassify a QC or previous Wave6 state receipt as an independent verified native function. Prior refuses and protected VA cannot be reacquired. Only the assigned knowledge curator may update shared REF/symbol/struct/develop after review. No user PC sources modified.
