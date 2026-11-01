# REA historical audio research: 2026-10-26 00–09H

**Owner:** REA; PRIVATE owner intake, STATIC/INFERRED/VERIFY, not CURATED or READY. These ten are old research IDs, not newly analyzed native functions. The PC-owned source Markdown and same-hour EVIDENCE JSON candidate digests were recalculated read-only on 2026-11-02 JST. Original PE/V9 hashes and prior native audits were **not rerun** in this recovery; original-game Golden PASS=0. Evidence JSON remains PC-only. Summaries below are excerpted mechanically from original owner reports, so semantic acceptance requires curator review of the full original reports and the later V9 corrections.

### REA-LOCAL-20261026-0036-P0-OGG-QI-HRESULT-NULL-GATE-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_00H_P0_OGG_QUERYINTERFACE_STATIC.md` / actual source SHA256 `2B8E6EEFDFE8C8C570BF2DADE88E984E774D8A8FB55EC9AA097E28EBCD1A025B` / 3407 bytes.
- Same-hour PC-only evidence `REA_20261026_00H_P0_OGG_QUERYINTERFACE_EVIDENCE.json` SHA256 `0FEB13134C81F1CDC1DDFA5C9F2A300D3B8414D71094EC44EEA06B78BFC0A13D`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - 既存19H証拠では0x005022C4/0x005022D9/0x005022E5の間接CALL 3件のみ登録。今回の新規内容はQueryInterfaceのGUID・戻り値無検査・後段NULLアクセス条件の接続。
  - Ghidra検索CLIで0x00502220/0x00502330/0x00502160の関数・参照・擬似Cを照合。擬似Cは形式的VERIFIEDではない。
  - 0x005022A9: [esi+8]!=0 なら既存バッファ経路0x005022E7へ分岐。
  - 0x005022C4: CALL EAX（[ecx]vtable+0x0C）。CreateSoundBuffer候補。直後0x005022C6 TEST EAX,EAX / 0x005022C8 JS 0x00502314により負HRESULTならcleanup。
  - 0x005022D2～D9: push edi（out=&[esi+8]）、push 0x0060971C（RIID）、push eax（元buffer）、CALL EDX（vtable+0）。IID bytes=49A425682475824D920F50E36AB3AB1E → GUID 6825a449-7524-4d82-920f-50e36ab3ab1e（IID_IDirectSoundBuffer8）。
  - 0x005022DB～E5: QueryInterfaceの戻りEAXを検査せず、元bufferを改めてロードしてvtable+8のRelease候補CALL。
  - 0x005022E7～E9: 続いて0x00502330に無条件CALL（0x005022E9）。
  - 0x0050233B/3D: 0x00502330は[esi+0]（decoderポインタ）だけをNULL検査。0x0050234A mov eax,[esi+8] / 0x0050234D mov ecx,[eax]でbuffer8ポインタを無条件参照。
  - 0x0050234F/54: vtable+0x34経由CALL。通常のIDirectSoundBuffer8ならSetCurrentPositionスロット。
  - ## 推論の範囲
  - CreateSoundBuffer成功後、QueryInterfaceが失敗し、かつ[esi+8]に有効な旧ポインタが存在しない場合、0x0050234DでNULL参照となる可能性がある。失敗時に常にクラッシュするとは断定しない。通常COM QueryInterface失敗時の出力ポインタ処理と実ゲーム異常系は未実測。
  - 0x005022D9 QueryInterface戻値は0x005022DBで上書きするため失敗判定の分岐が見えない。これは既存のスレッド生成失敗経路とは別の新規VERIFY事項。
  - 次: 0x00502330のNULL到達条件と同一関数の既存buffer8経路、0x004BE820の失敗cleanupとの整合を許可範囲の保存済み証拠から照合。Golden設計のみ、実機PASS0。
- **Limits/errata:** CreateSoundBuffer成功後、QueryInterfaceが失敗し、かつ[esi+8]に有効な旧ポインタが存在しない場合、0x0050234DでNULL参照となる可能性がある。失敗時に常にクラッシュするとは断定しない。通常COM QueryInterface失敗時の出力ポインタ処理と実ゲーム異常系は未実測。 / 0x005022D9 QueryInterface戻値は0x005022DBで上書きするため失敗判定の分岐が見えない。これは既存のスレッド生成失敗経路とは別の新規VERIFY事項。 / 既存64/64は2026-10-11保存済み同期記録（今回増加0）。QUEUE/PROGRESS/MASTERは未変更。新規5種証拠完備0、TODO/VERIFY/BLOCKED正式書込差分0/0/0。13/14時のOFFLINE-UNSYNCED成果は未同期のまま。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-0136-P0-DS8-SHUTDOWN-REFILL-DOUBLE-CLEANUP-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_01H_P0_BUFFER_SHUTDOWN_STATIC.md` / actual source SHA256 `544D36BE34168682B999EA15BBB07377EC60E164187BAB35D26C1CB23EBD9B6C` / 3023 bytes.
- Same-hour PC-only evidence `REA_20261026_01H_P0_BUFFER_SHUTDOWN_EVIDENCE.json` SHA256 `8F258521E6FEC8727ED9493F540825F4250DBC6A7203DF46B7C937FA6B57529B`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - 00時台は0x502220 QueryInterface失敗→0x502330 buffer+8未検査参照を報告済み。今回は0x004BF2B0の上位cleanup呼出条件と0x502330異常系を独立接続。前回のQI発見は新発見に再計上しない。
  - 0x004BF303 CMP BYTE PTR [EDI+0x44],BL ; 0x004BF306 JE 0x004BF321。streamフラグが0ならStopと0x502330を省略。
  - 0x004BF318 CALL EDX は[buffer vtable+0x48]を使用。IDirectSoundBuffer8であればStop。
  - 0x004BF31C CALL 0x00502330 はStopの直後、上記status非ゼロの場合に呼ばれる。0x502330は初期化時だけではなく終了処理経路からも呼ばれる。
  - 0x004BF321 MOV EAX,[ESI+0xA0] ; 0x004BF327 CALL 0x00502160。Stop/0x502330を省略しても、streamオブジェクト非NULLならここへ到達する。
  - 0x00502330: 0x0050233Dでdecoder+0のNULLは検査するが、buffer8+8への0x0050234D参照前に明示的NULL検査をしない（00時台から既知）。
  - 0x00502354 buffer8 vslot+0x34呼出結果は未検査。0x00502387 vslot+0x2C呼出の後は0x00502389 TEST EAX / 0x0050238B JS 0x005023C9。
  - 0x005023CB CALL 0x00502160: Lock系失敗時の内部cleanup。上位0x004BF2B0はその後0x004BF327で再度0x00502160を呼ぶ経路が存在する。
  - 0x00502160は正常経路でポインタとstatusをクリアするため、二度呼び出しが直ちに二重freeを意味しない。異常時idempotenceや実ゲーム発生率は未確認。
  - 原作機械語20箇所、Ghidra直接CALL4サイト、間接CALL5サイト、EXE/DB SHA各1、SQLite quick_check1を独立assert → 32/32 PASS。検索基盤から関数 0x004BF2B0 / 0x00502220 / 0x00502330 / 0x00502160 を確認。新REA実行なし。
  - 次は0x00502330の0x005023BF Unlock結果未検査、0x004BF2B0二度cleanup時の具体的レジスタ・フィールド状態を静的照合し、Golden条件のみ設計。実ゲームは未実行。
- **Limits/errata:** 状態: STATIC / VERIFY / NOT READY、PC側独立証拠。Game Golden実測0、新規正式REA VERIFIED 0。 / 5種証拠 info/pseudo/callers/callees = INDEX_ONLY、assembly=TARGETED_SOURCE。新規5種完備0 / 新規VERIFIED0。旧Wave1–5 64/64は2026-10-11同期ログに基づき据置。QUEUE/PROGRESS/MASTER書込差分0、TODO/VERIFY/BLOCKED書込差分0/0/0。 / PCオンライン、active.lock不在、専用Java0、空きRAM約13.62GiB（単発観測）。CPU負荷・総所要時間不明。過去13/14時オフライン成果は未同期。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-0238-P0-DS8-UNLOCK-RETURN-IDEMPOTENCE-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_02H_P0_DS8_UNLOCK_CLEANUP_STATIC.md` / actual source SHA256 `C8E2F6BA061EF7B8B953E01C85957A72E477F4D40184D24CCC1D8DCD173F63BA` / 4778 bytes.
- Same-hour PC-only evidence `REA_20261026_02H_DS8_UNLOCK_CLEANUP_EVIDENCE.json` SHA256 `F24FE14FB75EE2C10E08AAFBCE7F8DA881C4B029A08D3E4DC5BBBF921215D9C8`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - ## 新規P0発見1：Lock成功後のUnlockエラーが成功扱いになる
  - 0x00502387: CALL EAX＝buffer8 vtable+0x2C（IDirectSoundBuffer8::Lock想定）。
  - 0x00502389 TEST EAX,EAX / 0x0050238B JS 0x005023C9：Lock失敗時は0x005023CB cleanup→AL=0で復帰。
  - 0x005023A0：decoder側vtable+0x04間接CALL（返値の成否判定なし）。
  - 0x005023BF：buffer8 vtable+0x4Cの間接CALL（IDirectSoundBuffer8::Unlock想定）。戻り値の検査・分岐なし。
  - 0x005023C2 MOV AL,1：UnlockのHRESULT値にかかわらず、正常経路はAL=1を返す。
  - 上位0x005022E9が0x00502330を呼び、0x005022EEでTEST AL,AL。1なら0x00502300で__beginthreadまで進み得る。
  - ## 新規P0発見2：2回cleanup経路でのポインタ解放抑止
  - 0x004BF31C→0x00502330、Lock失敗で0x005023CB→0x00502160を1回実行。
  - 0x00502160は+0x08がNULLでなければ0x005021A5からRelease、+0x00がNULLでなければ0x005021B2/0x005021C0からcleanup/destructorを呼ぶ。
  - 正常復帰時0x005021C2でstream+0x08=0、0x005021C5でstream+0x00=0、0x005021C7でstream+0x44=0とする。
  - 呼出元0x004BF321で同一所有ポインタを取り直し、0x004BF327で2度目の0x00502160を呼ぶ。
  - 次回P0：0x005023A0 decoder vslot+0x04の引数・戻り値型とバッファ書込サイズ。0x005023BF Unlock 4引数と二領域Lockの整合を確認。初期化0x00502220とshutdown 0x004BF2B0で同じ戻値をどう扱うか比較する。
- **Limits/errata:** 状態：PC-SAVED / STATIC / VERIFY / NOT READY。担当REA専用証拠、原作Golden実測0、新規正式REA VERIFIED0。 / - 正式TODO/VERIFY/BLOCKED書込差分0/0/0。独立VERIFY候補は2点、正式キュー未変更。ゲームGolden PASS0、strict MATCH/複製率未測定。 / E. 解放処理とワーカースレッドの並行終了：レース・例外経路は実機未検証。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-0334-P0-OGG-LOCK-DECODER-ONE-SEGMENT-ABI-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_03H_P0_DECODER_FILL_STATIC.md` / actual source SHA256 `D979161FA51664E015FD4D21B615712559BCDA8B1AD3D63EB910563E2FD39F6F` / 4744 bytes.
- Same-hour PC-only evidence `REA_20261026_03H_P0_DECODER_FILL_EVIDENCE.json` SHA256 `ECCC91F75AFCA39554D382B24F75835569AE70C43751957FDE0572411EADB46A`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - ## P0新規解決：0x005023A0のdecoder仮想CALL
  - 原作機械語 0x00502391～0x005023A0：ECX=[stream+0x00]（Decoder this）、EDX=decoder.vptr[+0x04]、CALL EDX。
  - OggDecoder vtable 0x006395CC の +0x04 スロット実バイトは 0x00501F10（今回再照合）。
  - 通常のOggDecoder vtableが設定されていれば、0x005023A0 → 0x00501F10。別の実行時vtableでは別処理になり得る。
  - COM Lock 0x00502387 後のESP復帰を前提に、ローカル領域は [ESP+0x08]=len1、[ESP+0x0C]=p1、[ESP+0x10]=len2、[ESP+0x14]=p2。
  - 0x0050238D/0x0050239Aでlen1、0x0050239B/0x0050239Fでp1をpush。先行する0x00502398/99の二つのpush 0と合わせ、decoderへ (p1,len1,NULL,NULL) が渡される。
  - 0x005023A2は直ちに二番目の長さを読み、decoder戻りEAXをtest/cmpしない。以降0x005023BF Unlock、0x005023C2でAL=1。
  - ## P0新規：二領域の書込範囲
  - 0x00502359からのLock引数は buffer8, offset=0, requestedSize=0, &p1, &len1, &p2, &len2, flags=2。
  - 0x005023A0のDecoder fillはp1/len1のみ。p2/len2は0x005023A2/0x005023A6で取り出されて0x005023BF Unlockへそのまま渡され、二番目の領域への書込は当該関数内に見つからない。
  - ## OggDecoder::fill(0x00501F10)の独立対照
  - Ghidra疑似Cの引数はthiscall (this, outputBuffer, requestSize, optionalActualBytes*, optionalEOF*)。機械語0x00501F4A/0x00501FF0のRET 0x10で4個のstack引数を確認。
  - 0x00501F19はdecoder+5を確認し、0x00501F5DはoutputBuffer全体を_memset(0)する。
  - 0x00501F62のchunk=0x1000(4096)を上限に、0x00501F91→0x005D12E0からデータを取得するループ。
  - 0x00501F9B/0x00501FA3で読込0・ループ属性+4を判定。非ループ時はoptionalEOFへ1を書けるが、今回のcallsiteはNULLを渡す。
  - 0x00501FE6でoptionalActualBytesに実読込バイト数を返せるが、今回のcallsiteはNULLを渡す。0x00501FEA AL=1は一部不足でも可能。呼出元はDecoder ALも未検査。
  - 2026-10-21 search.sqliteのfunction 0x00502330/0x00501F10、callers、callees、related、および過去18/02時台vtable・Lock/Unlock成果を事前照合。
  - 次は0x005023E0ワーカー側で0x00502330が定期再呼出されるかを追跡し、デコーダ戻り値・EOS/ループ値による停止とバッファ再書込の実際の呼出条件を確定する。Golden：短い非loop OGG、空OGG、loop OGG、二領域Lock、Lock成功かつdecoder異常。
- **Limits/errata:** 状態：PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden実測0、REA新規正式VERIFIED0。 / - 正式TODO/VERIFY/BLOCKED書込差分0/0/0。独立VERIFY：p2/len2が非ゼロになる条件、Decoder戻値/EOF無視時の実際の再生、ループかつ空入力時の経路、実バイト数と無音領域の境界。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-0431-P0-OGG-WORKER-PINGPONG-EOF-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_04H_P0_OGG_WORKER_PINGPONG_STATIC.md` / actual source SHA256 `D94E623CE15513DE0820C039ACB64BDE4757EC53DAEB5289E250C72997EF3D8A` / 6300 bytes.
- Same-hour PC-only evidence `REA_20261026_04H_P0_WORKER_PINGPONG_EVIDENCE.json` SHA256 `5C9A54634291D61ECAF596F2331E21DE60A1D2DD05514A0E4D29EB86A29094D4`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - # REA P0｜Ogg worker 0x005023E0：二相バッファ更新・EOF分岐・間接CALL
  - ## 新規P0-01｜ワーカースレッドは0x00502330を呼ばない
  - Ghidra12.1.4検索DB：worker 0x005023E0 は414バイト。callers/calleesの直接CALL索引はいずれも0。0x005022FBから関数アドレスを__beginthreadへ渡すDATA参照があり、直接CALL無しは未使用を意味しない。
  - 独立PE/Capstone全関数逆アセンブル：worker内にGetCurrentPosition/Lock/Decoder::fill/Unlock相当の間接CALLを直接持ち、前回初期化専用0x00502330へのCALL無し。
  - vtable+0x10を0x00502445（再生カーソル取得）、+0x2Cを0x00502479/0x0050250D（Lock）、decoder+0x04を0x0050249E/0x0050252E（Ogg設定なら0x00501F10）、+0x4Cを0x005024BD/0x0050254D（Unlock）で呼ぶ。0x00502567はSleep(100)に相当するimport間接CALL。
  - ## 新規P0-02｜再生カーソルによる二相交互更新
  - 0x005023EC/0x005023F0：stream+0x28を2で割ってH=floor(N/2)とする。0x00502410：stream+0x4C終了要求なら終了。
  - 0x00502420：stream+0x50==1のみ通常動作。+0x50==3なら0x0050242Fで内部位相EDIを0へ戻す。それ以外は更新せずSleep(100)。
  - 0x00502445：DirectSoundBuffer8 vtable+0x10で再生カーソルposを取得（HRESULT検査無し）。
  - EDI==0かつpos>=H（0x00502447/4F/53）なら0x00502479 Lock(offset=0, bytes=H, flags=0)。Lock HRESULT<0なら更新せず次のSleep。
  - Lock成功→0x0050249E decoder vtable+0x04→0x005024BD Unlock。戻り値を検査せずEDI=1へ切替（0x005024BF）。
  - EDI==1かつpos&lt;H（0x005024DA/E3/E7）なら0x0050250D Lock(offset=H, bytes=2H, flags=0)。0x00502506のLEA [EBP+EBP] をbytesにpush、0x0050250BのEBPをoffsetとしてpush。
  - 後段は0x0050252E decoder fill→0x0050254D Unlock、戻値を検査せずEDI=0（0x0050254F）。ここでbytes=2HはHではない。範囲が折返す際はp2/len2が非ゼロになり得る。
  - ## 新規P0-03｜EOFの方向情報と実読込byte数
  - worker側decoder呼出はNULL出力でなく、0x0050248A/0x0050251AのEOF out pointerと0x0050248F/0x0050251Fの実読込bytes out pointerを渡す。前回0x005023A0初期化経路のNULL/NULLとは異なる。
  - decoder 0x00501F10：0x00501F54でEOF outを0へ毎回初期化。非loopのread==0では0x00501FDCでEOF=1、実読込bytesを0x00501FE6で出力。loop flag==1なら0x00501FB7で読込位置を先頭へ戻して同要求を続行する。
  - EOF=1で第1半分を書いた場合、0x005024CEでstream+0x58=2。第2半分を書いた場合、0x00502557でstream+0x58=1。どちらも0x0050255E/62でstream+0x54に実読込bytesを書き込む。
  - ## 独立証拠・既存成果の区別
- **Limits/errata:** 状態：PC-SAVED / STATIC / VERIFY / NOT READY。新規正式REA VERIFIED0、Golden実測0。 / - ループ対象が毎回read==0を返す場合、decoder内でreseek→read0の繰返しに出口が見当たらない。空loop OGGなどで本当に発生するかはVERIFYであり、再現済みのハングではない。 / - 正式TODO/VERIFY/BLOCKED書込差分0/0/0。新規独立VERIFY：二相Lockのp2/len2と保持内容、EOF状態の読み手、GET cursor失敗、loop空入力、odd N、worker終了との競合。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-0535-P0-OGG-EOF-LATCH-CONSUMER-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_05H_P0_OGG_EOF_CONSUMER_STATIC.md` / actual source SHA256 `FB9D3CC3444D27669DFC648ED34434B19DA6D139571CD69E8DA39F8D8FCF09F2` / 5882 bytes.
- Same-hour PC-only evidence `REA_20261026_05H_EOF_LATCH_EVIDENCE.json` SHA256 `0F7C9C54F57CAED41A52874C1ED25494FC3821DB80F27EBFA4C0D9D3E648BF39`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - ## 今回の新規事実（04時台のworker書込調査と区別）
  - 1. 05時台の限定Capstone xref probeで +0x58/+0x54 を読むstream自身の関数0x00502580（105 bytes）を特定。callers: 0x004BF780（CALL site 0x004BF7C8）1件。そのcaller: 0x004BE220（0x004BE29D）1件。そのcaller: 0x004C24B0（0x004C26CF）。
  - 3. 0x00502580: [ESI+0x58]==0 はAL=0。==2 はvtable+0x10 (CALL site 0x005025AA)でカーソル取得し、HRESULT>=0 かつplayCursor < (size+0x28)/2 なら 0x005025B6 で+0x58=1へ移行。この呼出しではAL=0のまま。
  - 4. +0x58が非0かつ2以外の場合、vtable+0x10 (CALL site 0x005025D4)でカーソル取得し、HRESULT>=0 かつunsigned playCursor >= [ESI+0x54] なら 0x005025E3 でAL=1。それ以外はAL=0。
  - 5. 0x005025B0はcmp dword ptr [esp + 4],edi。GhidraのpuVar4変数は誤ったポインタ意味付けで、実際は出力された再生位置DWORDとHの比較。0x005025DEも実DWORD値比較。
  - 6. 0x004BF780: manager+8==0・manager+9!=0のOGG分岐で[manager+0xA0]をESIへ置き、0x00502580をCALL。0x004BF7CD/CFはTEST AL / SETE AL。すなわちヘルパーAL=1で上位の継続判定はfalseになる。
  - 7. 0x004BE220: 0x004BE29Dで0x004BF780をCALLしAL==0で0x004BE2AB cleanup、0x004BE2CAで曲インデックスを加算、0x004BE307で0x004BDE40をCALLし次曲処理へ。ほかのゲート(manager+0x24、backend+0x38、param_2&0x1F等)も存在し、無条件の曲送りではない。
  - worker 0x005024CEは前半更新時EOFでstate2を記録。0x00502557は後半更新時EOFでstate1を記録。後半更新Lock(offset=H, request=2H)の最初の領域だけをデコードする。
  - 前回研究：REA-LOCAL-20261026-0431-P0-OGG-WORKER-PINGPONG-EOF-STATIC-01。今回はconsumer 0x00502580の状態機械、0x004BF780の戻り値反転、0x004BE220の曲送り分岐が新規。
  - P0次回：0x004C24B0の更新周期・バックエンド選択と0x004BF780戻り値の実条件を照合し、EOF後のstop/nextトリガを時系列で確定。read-onlyを先行し、Goldenは未測定のまま隔離。
- **Limits/errata:** ## 要VERIFY: 半バッファ判定の非対称性 / - 追加注意：state==2以外の非ゼロ値も第2分岐へ進む。通常生成源はstate1/2のみだが破損値経路は未検証。 / - 既存正式Wave1～5=64/64は2026-10-11ログによる旧同期値。04時台以前の監査件数を今回へ加算しない。今回の正式5証拠: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_SOURCE / callers=INDEX_ONLY / callees=INDEX_ONLY。正式新規5種完備0、VERIFIED+0。正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-0635-P0-AUDIO-TICK32-MULTIGATE-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_06H_P0_AUDIO_TICK_GATE_STATIC.md` / actual source SHA256 `9EAFA9A4DFBD1BD6C3761EAF16E7DF035BD7618EA3E4D1C43CD93E5CC00D7654` / 5629 bytes.
- Same-hour PC-only evidence `REA_20261026_06H_P0_AUDIO_TICK_EVIDENCE.json` SHA256 `5752B17E268A03728D8A2B335E7B68FD38A3B96EEB827D8AC6F26924D487A000`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - ## 今回の新規成果（05時台のEOF consumer追跡と非重複）
  - 1. メインタスク関数0x004C24B0の0x004C26BDで task+0x3CをEAXへ読み、0x004C26C0のTEST AL,3 / 0x004C26C2のJNEで下位2ビット非0をスキップする。条件成立時だけ0x004C26CFから0x004BE220を直接CALL。
  - 2. 0x004BE220では管理オブジェクト先頭ポインタの非NULLを確かめた後、0x004BE261で0x004BF410を呼ぶ。この4カウント段階では時間/フェード等の状態が進み得る。ここでまだEOFの判定をしていない。
  - 3. 0x004BE266のTEST BYTE PTR [ESP+0x4C],0x1F / 0x004BE26BのJNEで下位5ビット非0をスキップ。呼出引数は0x004C26C7でPUSHした同じtask+0x3Cの値。したがって、後続の0x004BF6A0 / 0x004BF780 / 0x004BE2CA曲index加算/0x004BE307の次曲起動は、両ゲート成立時（counter & 31 == 0）だけ到達可能。
  - 4. 0x004C2714から直接呼ばれる0x004C28D0の0x004C29C6はtask+0x3CをINCする。これは通常タスク更新経路でカウンタを進める仕組みの静的証拠。メッセージ処理・デバイス喪失・早期分岐では通常更新ルートを必ず通るとは限らず、実時間の更新周期は確定していない。
  - 5. 0x004BE28Aのmanager+0x24ゲートが0なら曲送りへ進まない。0x004BE297はstream+0x38が0なら0x004BF780を飛ばして後続の停止/次曲処理へ進む。非0なら0x004BE29Dで継続判定を呼び、ALが非0なら0x004BE2A4で次曲処理を回避する。
  - 6. 0x004BF6A0が非0を返すと0x004BE280から0x004BF720に進み、当該回の自動次曲は実行しない。0x004BF410内部には別の音声停止・再開へのCALL経路があるため「すべての音声停止/切替は32カウントごと」と一般化してはいけない。
  - 7. 0x004C2611のtimeGetTime、0x004C262CのSleep、0x004C2509のPeekMessageAを確認。32は時間msではなくタスクカウンタ単位。単純な32×一定ミリ秒への換算は実ゲーム未実測のため禁止。
  - EOF consumerは前回発見済みの0x00502580（stream+0x58/0x54）。今回はその読取が、メインタスクから条件付きでしか呼ばれない構造を解明した。
  - 通常ルートでEOFが32ゲート通過直後に変化すれば、次の評価まで最大31回のカウンタ更新を待つ可能性。ただし切替条件にはstream+0x38 / manager+0x24 / 0x004BF6A0 / 再生位置判定があり、実時間の上限や実際の遅延は保証できない。
  - 0x004BF410の4ゲート内フェード/リスタート経路と、0x004BE220の32ゲート内自動次曲は分離して実装・テストする必要がある。
  - ## 独立証拠・既存成果との区別
  - ## 未確認・再開位置・変更禁止範囲
  - 次回P0：0x004BF6A0の非0分岐と0x004BF720の効果、0x004BF410における4カウント更新の各経路を精査。0x004C28D0のcounter wrapはゲーム実測無し。
- **Limits/errata:** 7. 0x004C2611のtimeGetTime、0x004C262CのSleep、0x004C2509のPeekMessageAを確認。32は時間msではなくタスクカウンタ単位。単純な32×一定ミリ秒への換算は実ゲーム未実測のため禁止。 / - EOF consumerは前回発見済みの0x00502580（stream+0x58/0x54）。今回はその読取が、メインタスクから条件付きでしか呼ばれない構造を解明した。 / - 正式REA info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_SOURCE / callers=INDEX_ONLY / callees=INDEX_ONLY。正式5種類証拠新規完備0。Wave1〜5既存64/64は旧syncログの数値、二重計上しない。正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-0738-P0-DSHOW-EVENT-LOOP-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_07H_P0_DSHOW_EVENT_LOOP_STATIC.md` / actual source SHA256 `88F6D44900CCE3E8B03BBDF25E9FA0ED05B70CEA26BE0C97C9F6CB53E5D7449C` / 5111 bytes.
- Same-hour PC-only evidence `REA_20261026_07H_P0_DSHOW_EVENT_EVIDENCE.json` SHA256 `6A26CE999C4D3EC75CD2F09AFCCB22592F51F88A5C0AF26A0C53349C7663D724`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - ## 今回の新規静的証拠（06時台のtick周期とは別）
  - 1. 0x004BE220: 0x004BE274→0x004BF6A0のALが真なら0x004BE280→0x004BF720、0x004BE285のJMPで次曲処理を飛ばす。偽なら0x004BE29D→0x004BF780等へ進み通常曲送り判定を行う。
  - 2. 0x004BF6A0 (113 bytes): stream+8≠0、+0x98≠NULL、+0x0A≠0を検査。0x004BF6D8のvtable+0x20に3つの出力ポインタと1ms timeoutを渡す。IMediaEvent::GetEventにABI一致。0x004BF6DA TEST EAX / 0x004BF6DC JSで失敗を検査。
  - 3. 0x004BF6E8で出力eventCodeをECXへ読み込み、0x004BF6F6 CMP ECX,1 / 0x004BF6FD SETE BL。0x004BF700のvtable+0x30は3つのイベント値を引数に取り、IMediaEvent::FreeEventParamsと整合。FreeEventParamsのHRESULTは0x004BF702 MOV AL,BLで上書きされ、判断に利用しない。
  - 5. 0x004BF720 (92 bytes) は stream+8≠0なら0x004BF73A (+0x90 slot+0x24) → 0x004BF766 (+0x94 slot+0x38) → 0x004BF774 (+0x90 slot+0x1C)を順に呼ぶ。IMediaControl::Stop→IMediaSeeking::SetPositions→IMediaControl::RunとABI整合し、同曲を先頭から再生するルートと整合。
  - 6. SetPositionsには0x004BF742 PUSH 2、0x004BF749 PUSH 1と64bitゼロ初期化があり、current=0/absolute(1)、stop=0/relative(2)に整合。3 APIのHRESULTを判定する分岐はこの関数中に見当たらない。
  - ## P0 VERIFY：イベント失敗時の判定・二重ポーリング
  - 7. 0x004BF780のDirectShow分岐では0x004BF7ADでvtable+0x20 GetEvent相当をCALLした後、EAX/HRESULTを確認せず、0x004BF7AFで[ESP+4]に置かれたeventCode相当値を1と比較、0x004BF7B5でSETNE ALする。この出力ローカルを事前に初期化する命令も確認できない。
  - 9. 0x004BF6A0が非EC_COMPLETEイベントを消費してAL=0を返した同一32tick時に、上位0x004BF780が別のイベントを再取得し得る。イベントが複数並ぶ際のloop対next優先はVERIFY。2つのGetEventを統合して最適化すると原作のイベント消費順を変える可能性がある。
  - 次P0: MP3生成元のQueryInterface IIDを追って+0x90/+0x94/+0x98のvptr所有者を確定する。0x004BF410のフェード更新は別系列の継続候補。
- **Limits/errata:** 8. IMediaEvent::GetEventはタイムアウト時にE_ABORTを返し得る。出力が未更新なら不定のローカル値を比較する可能性がある。偶然1なら上位へAL=0を返して通常次曲処理へ進む候補。確定クラッシュ/誤曲送りとは判断しない。実機Golden NOT RUN。 / 9. 0x004BF6A0が非EC_COMPLETEイベントを消費してAL=0を返した同一32tick時に、上位0x004BF780が別のイベントを再取得し得る。イベントが複数並ぶ際のloop対next優先はVERIFY。2つのGetEventを統合して最適化すると原作のイベント消費順を変える可能性がある。 / - 2026-10-11 syncログでWave1-5=64/64（16+10+10+12+16）。QUEUE/PROGRESSはEPERMによるstaleを維持し変更しない。正式TODO/VERIFY/BLOCKED書込差分0/0/0。Golden実測0、strict MATCHと完全複製率は未測定。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-08H-P0-DSHOW-IID-CHAIN-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_08H_P0_DSHOW_IID_CHAIN_STATIC.md` / actual source SHA256 `62B9DAFB9A62AFD3E21C5468748D1004B91692B6B3466A6EA13BD29C58065AD8` / 4960 bytes.
- Same-hour PC-only evidence `REA_20261026_08H_P0_DSHOW_IID_EVIDENCE.json` SHA256 `70BE997BFCB355F88BA57A81055A84C8F19D25E01B743D0FF44ECC066909B323`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - ## 今回の新規証拠：QueryInterface IIDを6 GUIDの原作実バイトから確定
  - 0x004BE820 (2695 bytes) のMP3/DirectShow初期化枝。0x004BED21 = ole32.dll!CoCreateInstance（PE import 0x00609310で確認）。
  - 0x0060CD6C = e436ebb3-524f-11ce-9f53-0020af0ba770 = CLSID_FilterGraph。
  - 0x0060CDBC = 56a868a9-0ad4-11ce-b03a-0020af0ba770 = IID_IGraphBuilder。
  - | 0x004BEDC6 | 0x0060CD7C | IMediaControl | stream+0x90 |
  - | 0x004BEE17 | 0x0060CD8C | IMediaEvent | stream+0x98 |
  - | 0x004BEE30 | 0x0060CDAC | IMediaSeeking | stream+0x94 |
  - | 0x004BEE49 | 0x0060CD9C | IBasicAudio | stream+0x9C |
  - 各QueryInterface直後でHRESULTの負値をチェックし、失敗時は共通cleanup側0x004BEDCCへ移る（初回はJNSで成功先0x004BEE04、他3件はJS/JLで失敗先）。
  - 成功時は0x004BEE61のIGraphBuilder vtable+0x34（RenderFile相当）、続いて0x004BEE6BのIMediaControl vtable+0x1C（Run相当）へ進む。
  - ## 新たなVERIFY：RenderFile失敗後もRunへ進む可能性
  - 0x004BEE61 CALL EDX直後は0x004BEE63 MOV EAX,[EDI]で戻りHRESULTを上書きする。RenderFile失敗を調べる条件分岐はその間にないため、0x004BEE6BのRunが呼び出され得る。再生成功・失敗をどう上位へ伝えるかはVERIFY。実ゲーム不具合は未実測。
  - 0x004BF2B0の既存Ghidra疑似Cには+0x9C、+0x94、+0x98、+0x90のRelease/NULLクリアと+0x90のStopがある。これは部分初期化失敗時のcleanupと整合するが、各分岐の全ASM・実機所有権確認は未完了。
  - 0x004BE820を原作PEからCapstoneで全2695バイト限定逆アセンブルし、実CALL命令88件とGhidra SQLiteの直接/間接CALL site和集合88件が集合として完全一致した。今回の4つのQueryInterfaceも索引収録済み。
  - 0x004BE820正式5種: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。5種完全充足新規0、正式VERIFIED差分0、TODO/VERIFY/BLOCKED書込差分0/0/0。新たな独立VERIFY候補はRenderFile HRESULT経路。
  - Golden実測PASS=0、strict MATCH=未測定、完全複製率=未測定。次の候補VA 0x004BF410（音量/フェード状態更新）と0x004BF780（GetEvent失敗時の条件）。
- **Limits/errata:** ## 既存検索DBの参照被覆と訂正 / search.py function --limit 2の表示に間接CALLが2件だけ現れ、当初欠落と誤推定したが、全SQLite行確認で誤認と判明。最初の不適切な監査期待値46/50はファイル保存前に修正し、正式な結果に加算しない。検索DBのCALL漏れは今回認められなかった。 / - 0x004BE820正式5種: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。5種完全充足新規0、正式VERIFIED差分0、TODO/VERIFY/BLOCKED書込差分0/0/0。新たな独立VERIFY候補はRenderFile HRESULT経路。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

### REA-LOCAL-20261026-09H-P0-FADE-20PCT-15TICK-TAILJMP-STATIC-01

- Source: `rea_lab/decomp_task/REA_20261026_09H_P0_AUDIO_FADE_THRESHOLD_TAILJMP_STATIC.md` / actual source SHA256 `9015B654DFC9DF5A1DEC717663478C93EA68C1B09778A14D939ACFC7A819A646` / 6324 bytes.
- Same-hour PC-only evidence `REA_20261026_09H_P0_FADE_VA_EVIDENCE.json` SHA256 `D6C82824B86130DCF6322FC7E1262D203BED65AF271AD1C9912588B79A5C66A7`.
- **Owner-source bounded original x86/ABI/branch evidence:**
  - 既存06時台は0x004BE220→0x004BF410の4/32カウンタゲート、08時台はDirectShow COM IIDを調査。今回は0x004BF410の機械語、0x004BF520/0x004BF570のフェード開始、0x004BF630の3系統の音量反映を別範囲として扱った。
  - ## 新規の静的証拠A：フェードは振幅0ではなく0.2の閾値で停止する
  - 原作静的double 0x0062FFA0 = 0.2（実バイト 9a9999999999c93f）。0x004BF485 FLD [0x62FFA0] と0x004BF48B FCOMP ST(1)がfade-out中の現在値 stream+0x18 と比較し、0x004BF492のJPでstream+0x18 <= 0.2（ordered通常値）なら0x004BF4AEへ進む構造と整合。
  - 終了経路は0x004BF4B5の音量反映、0x004BF4BEのvolume→amplitude逆変換、0x004BF4CBでstream+0x20=0、0x004BF4D0で0x004BF2B0 cleanup。stream+0x54が非0なら0x004BF4FDで0x004BDE40再openに進み、0x004BF50Cで0x004153D0へtail-JMPする。
  - ## 新規の静的証拠B：正負のランプ幅を構成する定数
  - 0x0062FF90 = 15.0、0x0063B1C8 = -15.0、0x0063B1C0 = -9600.0（いずれも研究用EXEのPEバイトからdouble復元）。
  - fade-in開始0x004BF520：0x004BF531の0x004BD240により目標音量を線形振幅へ逆変換し、0x004BF536で0.2を読み込む。0x004BF53C FSub、0x004BF541 /15、0x004BF547へdeltaを書込む。0x004BF54Aで現振幅+0x18を0.2に設定し、0x004BF550以降で音量反映。
  - fade-out初期化0x004BF570：0x004BF5D9以降の経路は0x004BF5E5で現振幅を-15.0で割り、stream+0x20へ保存。stream+0x10には静音側の音量目標を保持する。
  - 0x004BF410は毎回stream+0x18 += stream+0x20を実行し、増加時は目標stream+0x10のdBに到達すると停止、減少時は振幅0.2で切る。15は更新回数計算用doubleであり15ミリ秒・15描画フレームと断定しない。
  - ## 新規の静的証拠C：CALL索引はtail-JMPを含む
  - 0x004BF410の原作x86実CALL命令は8箇所：0x004BF438, 0x004BF455, 0x004BF45E, 0x004BF49A, 0x004BF4B5, 0x004BF4BE, 0x004BF4D0, 0x004BF4FD。
  - 元SQLite callsに記録されたsiteは11箇所。その追加3箇所 0x004BF44E→0x004BF630、0x004BF4A9→0x004BF630、0x004BF50C→0x004153D0 はすべて機械語ではJMP（tail-transfer）でありCALLではない。
  - 0x004BF630の0x004BF64Aはstream+0x9C vtable+0x1C（08時台IIDよりIBasicAudio::put_Volumeに整合）。
  - 0x004BF66Bはstream+0xA0内のインタフェース vtable+0x3C（DirectSoundBuffer8::SetVolumeに整合）。
  - 0x004BF685はstream+0x78 vtable+0xCC経由で得たポインタからslot+0x14をCALL。この2段階vtableの実行時所有者は未解決、次のP0 VERIFY対象。
  - 次P0: 0x004BF630の未同定+0x78→vtable+0xCC→slot+0x14のowner/ABIと、音量0/極小音量でのfade-in slope<0境界を限定追跡。どちらも元の旧証拠やレーンDとの重複照合を先行する。
- **Limits/errata:** - 0x004BF685はstream+0x78 vtable+0xCC経由で得たポインタからslot+0x14をCALL。この2段階vtableの実行時所有者は未解決、次のP0 VERIFY対象。 / - info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規5種完全充足=0、新規正式VERIFIED=0、正式TODO/VERIFY/BLOCKED書込差分=0/0/0。新規独立VERIFY候補=tail-JMP分類と音声0.2 cutoff仕様。 / - PCオンライン、09:39時点active.lockなし。Java/Python既存プロセスあり重いGhidra/REA起動を回避。空き物理RAM16.9GiB。CPU負荷不明。監査単体約0.34秒、研究全体の所要時間未測定。
- **Classification:** PUBLISHED_INTAKE after readback, STATIC/INFERRED/VERIFY, not formally VERIFIED; Golden PASS/READY=0. Prior denied operations mentioned in owner report remain excluded; only allowed pre-existing source statements retained.

## Curator gate

Do not count repeated CALL sites or identical semantics across neighboring studies as independent native functions. Native x86, V9, source report SHA, owner/correction chain and safe ownership must be checked before REF/symbol adoption. Earlier refused FLS/Wave6/protected VA and partial evidence not reobtained. Formal REA five-method additions 0, newly VERIFIED 0, original-game Golden PASS 0, READY 0. Next chronological source: 2026-10-26 10H.
