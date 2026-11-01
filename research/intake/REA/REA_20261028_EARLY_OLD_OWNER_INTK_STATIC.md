# REA 2026 historical research intake: 20261028 EARLY

**REA owner / PRIVATE owner branch / STATIC or conditional INFERRED / VERIFY, NOT CURATED or READY.** The original owner wrote these 10 studies previously. This archive remeasures only the source Markdown SHA256, bytes, and small same-hour evidence filename/SHA candidates read-only; no Ghidra, REA, original game, new native evidence, or Golden run performed. Original PE and V9 actual hashes were not recalculated in this intake. Source excerpts preserve bounded x86 CALL/ABI/control-flow observations, but are not a full verbatim copy; detailed owner report still exists on the authorized research PC. Machine evidence remains PC-only. Formal newly VERIFIED 0 and Golden PASS/READY 0.

### REA-LOCAL-20261028-00H-P0-XCPT-ACTIONTABLE-SEH4-CXXGATE-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_00H_P0_XCPT_SEH_STATIC.md`; SHA256 `ADFB912EC72774D2C04218CF18B199AB5E3334F7B4AD4A9651FC7912E083F6BD`, 3372 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_00H_P0_XCPT_SEH_EVIDENCE.json` SHA256 `83D47A338EB437B3791D2A0672E17232B7A0ECEE2FAA367A42CE49B41E342815`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 23Hの`0x005B8612 CALL 0x005BE999`・SEH4 scope発見を再利用し、今回初めて**CRTの例外アクション表の全12スロット**と、SEH4 dispatcherのC++例外専用分岐を原作PEから独立照合した。
  - ## 新規静的証拠A：CRT既定アクション表
  - `0x005BC596 MOV [ESI+0x5C],0x0060B198`は`__initptd`の既定表ポインタ設定。 `0x005BE9AE`で`__XcptFilter`が`[ESI+0x5C]`を読む。
  - `0x005BE9BB ADD EAX,0xC`、`0x005BE9BE LEA EDI,[ECX+0x90]`：12バイト×12件の比較。
  - PEの`0x0060B198`から全12×12バイトを直接読み、コードは`C0000005, C000001D, C0000096, C000008D..C0000093, C00002B4, C00002B5`。12個のaction初期値は全て0。
  - **C++ EH例外コード`0xE06D7363`は既定12件に存在しない**。`0x005BE9D6 XOR EAX,EAX`から不一致は0を返す経路。既定表・通常コード一致比較を前提とした静的判定であり、実動作観測ではない。
  - ## 新規静的証拠B：SEH4 dispatcherはフィルター戻り値で分岐
  - `0x005B8612 CALL 0x005BE999`で起動SEH filterが例外コードをCRT分類関数へ渡す。既存両DBはこの直接CALLのsite登録0件のまま。
  - `0x005BB769 CALL 0x005C35F2` → `0x005BB772 TEST EAX,EAX` → `0x005BB774 JS`（負）／`0x005BB776 JG 0x005BB7BF`（正）。
  - 正の場合だけ`0x005BB7C2 CMP [ECX],0xE06D7363`と条件付き`0x005BB7EA CALL [0x609AF8]`に到達。非正のフィルター戻り値ではこのC++例外オブジェクト破棄分岐を通らない。
  - 次回：`0x005B861A`のhandler末尾と`0x005BB625`のunhandledフィルター後続、あるいは`_pxcptacttab`の初期化後書換えxrefsを優先。実機GoldenはDESIGNED/NOT RUN。
- **Original-report limitations/errata:** - **既定表とC++例外コードの組み合わせでは、当該起動SEH4フィルターの正値catch/handler経路は選択されない**という条件付き結論。別の上位/外部ハンドラー・実行時のテーブル差替・例外伝搬は未確認。 / 関数別5証拠：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED **0**、5種完全充足 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。新規ローカルVERIFYは既定表の実行時変更可能性と例外伝搬先。 / 原作Golden PASS **0**／strict MATCH NOT RUN／完全複製率未測定。CPU負荷・全体所要時間は不明、開始時空きRAM約11050MiB、active.lock無し、Java/Ghidra稼働未検出。新規REA/Ghidra/ゲーム起動0、Work不使用。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261028-01H-P0-CRT-SEH-NATIVE-EXIT-GATE-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_01H_P0_CRT_EXIT_GATE_STATIC.md`; SHA256 `13E4BC394A5587B63551A87E0E320EBD719ECF082A8C2167E31A8A419E26469B`, 3824 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_01H_P0_CRT_EXIT_GATE_EVIDENCE.json` SHA256 `053704977F963DF7AD7684889DCB519C02761804BBC93AA5703DBCBB063433F8`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 前回00HのCRT既定例外表12件／C++ EH 0xE06D7363が表に無いという条件付き結論（25/25 PASS）を維持する。新規分析対象は上位起動関数 `0x005B84D7` に埋め込まれた未索引SEH4 handler `0x005B861A` と、`0x005B862A`、`0x005B862F`の直接CALL、PEのCOM descriptor分岐。以前の64 VERIFIEDは再計上しない。
  - ## 新規STATIC A：原作native PEのhandler分岐
  - `0x005B8534 CMP [EAX+0x400074],0xE`、`0x005B853F CMP [EAX+0x4000E8],ESI`、`0x005B8545 SETNE CL`、`0x005B8548 MOV [EBP-0x1C],ECX`。COM descriptorの存在をローカル分岐フラグへ変換。
  - filter `0x005B8606` は `0x005B8612 CALL 0x005BE999`。filterが正を返してhandlerに入った**場合のみ**、`0x005B861A MOV ESP,[EBP-0x18]`→`0x005B861D MOV EAX,[EBP-0x24]`→`0x005B8623 CMP [EBP-0x1C],0`→`0x005B8627 JNE 0x005B862F`。
  - 実際の原作EXEはCLR directoryゼロなので、handlerの条件付き受入経路では `0x005B8629 PUSH EAX` / `0x005B862A CALL 0x005BB625`が選択される。対する`0x005B862F CALL 0x005BB64A`はCLR directoryがある場合の別経路。後続の通常returnや上位伝搬は実機未測定。
  - `0x005BB625`はGhidra上でも `__exit`、機械語 `0x005BB62C PUSH 1` → `0x005BB631 CALL doexit(0x005BB4CF)`。`0x005BB64A`は `PUSH 1; PUSH 1; PUSH 0; CALL 0x005BB4CF`。前回「0x005BB625を未処理例外フィルター後続」と表現したのは不正確。**実体はCRTの終了ラッパー**。起動SEH filter自体にC++ EHコードが未登録という00H条件とは区別する。
  - ## 新規STATIC B：索引欠落の独立再確認
  - Ghidra旧索引 `calls` および統合V9 `native_callsite` は、`0x005B8612`、今回追加した`0x005B862A`、`0x005B862F`の3 CALL siteを**各0件**。PE32機械語は3箇所とも直接CALL。未索引のfunclet領域を通常関数グラフと混同しないこと。原因の確定、検索DB側への修正は他owner領域なので未実施。
  - 次回優先：`0x005BB4CF`（doexit）を検索CLIで抽出し、`0x005B862A`から正常return可否とCRTアクションテーブルの変更箇所を静的照合。原作Goldenは設計のみ、実測なし。
- **Original-report limitations/errata:** 前回00HのCRT既定例外表12件／C++ EH 0xE06D7363が表に無いという条件付き結論（25/25 PASS）を維持する。新規分析対象は上位起動関数 `0x005B84D7` に埋め込まれた未索引SEH4 handler `0x005B861A` と、`0x005B862A`、`0x005B862F`の直接CALL、PEのCOM descriptor分岐。以前の64 VERIFIEDは再計上しない。 / - 実際の原作EXEはCLR directoryゼロなので、handlerの条件付き受入経路では `0x005B8629 PUSH EAX` / `0x005B862A CALL 0x005BB625`が選択される。対する`0x005B862F CALL 0x005BB64A`はCLR directoryがある場合の別経路。後続の通常returnや上位伝搬は実機未測定。 / 5種証拠: info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED **0**、5種完全充足 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。新規ローカルVERIFYは「実行時アクション表変更」「doexitの非復帰性／C++例外上位伝搬」。REA/Ghidra/実ゲームの新規実行なし、Work不使用。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261028-02H-P0-DOEXIT-ATEXIT-SKIP-NORETURN-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_02H_P0_DOEXIT_ATEXIT_STATIC.md`; SHA256 `D77F2D5892A908C448921517BE00E6A07D23233182CDBAECD3A7A900C0A0FAD8`, 3400 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_02H_P0_DOEXIT_NATIVE_EVIDENCE.json` SHA256 `7C88AD4339563FCDEC78B1BFE2EFF8E9614BEC70BA045C6DE6DD2E2335061498`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 前回01Hの起動SEH handler `0x005B861A`、native分岐、および03箇所の未索引CALLは維持。今回は先に未解決だった `0x005BB4CF` の原作native本体・CRT終了ABI・callback条件を限定分析し、`0x005BB650`の追加索引欠落を新たに確認。既存Wave1-5 64件は再計上しない。
  - `0x005BB625 (__exit)` は `0x005BB62A PUSH 0 / 0x005BB62C PUSH 1 / 0x005BB62E PUSH [EBP+8] / 0x005BB631 CALL 0x005BB4CF`。doexit(code,quick=1,return=0) に相当。
  - `0x005BB64A` は `PUSH 1 / PUSH 1 / PUSH 0 / 0x005BB650 CALL 0x005BB4CF`。doexit(0,quick=1,return=1) に相当するため、通常は後始末後に復帰する経路であり、プロセス終了と同一ではない。
  - `0x005BB503 CMP [EBP+0xC],0 / 0x005BB507 JNE 0x005BB5AD`：quick=1なら通常の動的復号callback配列 `0x00B14A34/0x00B14A30` と `0x0060966C..0x00609678` を飛ばす。ただし `0x0060967C..0x00609680` の1スロットの非NULL callback実行候補は残る。
  - `0x005BB4EA CMP [0x0068DFDC],1 / 0x005BB4F0 JE 0x005BB5CE`：終了済み状態ならcallback区間全体を飛ばす。
  - `0x005BB5DA CMP [EBP+0x10],0 / 0x005BB5DE JNE 0x005BB609`：return=1ならExitProcessへ進まずアンロック後にreturn。return=0なら `0x005BB5EC CALL 0x005C0F68`、`0x005BB5F5 CALL 0x005BB3B7`。
  - `0x005BB3C8 CALL [0x00609108]` の実インポートは `KERNEL32.dll!ExitProcess`、直後は `0x005BB3CE INT3`。正常なWindows動作では戻らない。この非復帰性をGhidraの見かけのreturnと混同しない。
  - `0x005BB631` は旧検索DBとV9の双方で直接CALL各1件。`0x005BB650` は実機械語で直接CALLにもかかわらず双方0件（新規発見）。`python search.py function 0x005BB64A` もNOT_FOUNDで、CRT wrapperの関数境界・call graph取りこぼしが疑われるが原因はVERIFY。DB自体は変更していない。
  - 例外フィルターの受理自体、終了callbackの実登録値と副作用、実際のC++例外動的伝搬は未実測。次回は `0x0060967C` の登録元と、SEH側の処理済み例外コードの設定経路を重点調査する。
- **Original-report limitations/errata:** `0x005BB631` は旧検索DBとV9の双方で直接CALL各1件。`0x005BB650` は実機械語で直接CALLにもかかわらず双方0件（新規発見）。`python search.py function 0x005BB64A` もNOT_FOUNDで、CRT wrapperの関数境界・call graph取りこぼしが疑われるが原因はVERIFY。DB自体は変更していない。 / 5種証拠: info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED **0**、新規5種完備 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。Golden実ゲームPASS **0**、strict MATCH **NOT RUN**、完全複製率 **未測定**。 / 例外フィルターの受理自体、終了callbackの実登録値と副作用、実際のC++例外動的伝搬は未実測。次回は `0x0060967C` の登録元と、SEH側の処理済み例外コードの設定経路を重点調査する。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261028-03H-P0-XT-NULL-SLOT-NATIVE-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_03H_P0_XT_CALLBACK_STATIC.md`; SHA256 `24FA2B942F05DF14C7102914C63D19FCB0E429383C44228A9A6AAC4F3BF64BF0`, 4604 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_03H_P0_XT_CALLBACK_EVIDENCE.json` SHA256 `386C2BBECD25496337ABDA444DBBAB6B08AF3628DD98C33D78CE118D8D7D1174`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - MASTER/5レーン規約、REA README/QUEUE/PROGRESS、最終progress_sync(64/64)、2026-10-21検索DB manifest、2026-10-28 02H `doexit` 原作ABI監査41/41を参照。既存の「quick=1でも0x0060967C..0x00609680のcallbackループは残る」という**構造**と、実配布PEの**登録値**を今回初めて切り分けた。既存02H/以前のCRT研究を新規成果として再計上しない。
  - 原作PE `.rdata` の特性フラグは `0x40000040`（`IMAGE_SCN_MEM_WRITE` なし）。PE内4-byte DWORDを直接読み取り次を確認：
  - | `0x0060966C` | `0x00000000` | 通常コールバック範囲の左端 |
  - | `0x00609670` | `0x005CCD70` | 通常時の非NULL callback 1 |
  - | `0x00609674` | `0x005BDAB1` | 通常時の非NULL callback 2 |
  - | `0x00609678` | `0x00000000` | 通常範囲右端 |
  - | `0x0060967C` | **`0x00000000`** | quick時にも検査される唯一のcallbackスロット |
  - | `0x00609680` | `0x00000000` | 右端（排他的） |
  - `0x005BB5AD` はループ先頭ポインタを `0x0060967C` に設定。`0x005BB5B4` は `0x00609680` と比較。`0x005BB5C0 MOV EAX,[EAX]` → `0x005BB5C2 TEST EAX,EAX` → `0x005BB5C4 JE 0x005BB5C8` → `0x005BB5C6 CALL EAX` という分岐。元PEスロットが0のため、**未改変のロードイメージであれば`0x005BB5C6`のCALLはスキップ**される。`0x005BB5C8`で+4し範囲外へ。`quick=1`は`0x005BB503/507`から通常コールバック部分を飛ばす。通常部分に登録された非NULL2件は`0x005CCD70`（内部でCloseHandle IATへ到達）と`0x005BDAB1`（`0x005BD9F7`呼出し）。これらはquick=1では実行対象にならない。
  - 初期Ghidra DBの`0x0060967C`参照は`0x005BB5AD`（DATA）・`0x005BB5C0`（READ）の2件で、直接WRITE参照0。native `.text`にスロットのリテラル4byteは`0x005BB5B0`の1箇所のみ。**間接ポインタ書込み、OS/プラグイン等による変更は否定しない**。動的な例外伝搬・ExitProcess到達も未実測。
  - 次P0: `0x005BD9F7`通常終了callbackの役割と`0x005B861A`→`0x005BB625`のexitCode由来、終了時guard優先順位の追加静的確認。実ゲーム観測は別の合法な検証工程へ分離する。
- **Original-report limitations/errata:** 初期Ghidra DBの`0x0060967C`参照は`0x005BB5AD`（DATA）・`0x005BB5C0`（READ）の2件で、直接WRITE参照0。native `.text`にスロットのリテラル4byteは`0x005BB5B0`の1箇所のみ。**間接ポインタ書込み、OS/プラグイン等による変更は否定しない**。動的な例外伝搬・ExitProcess到達も未実測。 / 原作/旧DB/V9 SHA照合、両SQLite quick_check=ok、旧02H静的監査41/41確認、REA既存Wave1～5の保存済sync=64/64。今回の独立原作native監査 **38/38 PASS**、新規正式5種完備0・正式VERIFIED追加0・TODO/VERIFY/BLOCKED記録差分0/0/0。5種証拠はinfo/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。原作Golden PASS=0、strict MATCH NOT RUN、完全複製率未測定。 / PC preflight: active.lockなし、Java/Ghidra検出なし、空きRAM約9.91GiB、CPU負荷不明。保存前監査2.852秒、保存時2.556秒。研究全体の所要時間不明。新規REA/Ghidra/原作ゲーム/Work実行0。原本、MASTER、QUEUE、PROGRESS、既存runs、他レーン、Git、公開先、スケジュール不変更。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261028-04H-P0-CRT-STREAM-FLUSH-CALLBACK-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_04H_P0_CRT_STREAM_FLUSH_CALLBACK_STATIC.md`; SHA256 `706902E2D5B3367B89371BDB44354CE80B68F482090A51DB9E554BCA5B75FF5B`, 4683 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_04H_P0_FLUSHALL_EVIDENCE.json` SHA256 `97A18C04E90852BA1CF7BCCEF3303A937BAC6060AD474118F7BF2D89E1302C60`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - MASTER・owner規約・REA README/QUEUE/PROGRESS、保存済64/64同期、検索DB manifestと旧03H監査38/38を確認。前回は通常終了領域`0x00609674`に`0x005BDAB1`が登録される点まで。今回はその先の関数本体・副作用・索引差を独立検証し、既存発見を二重計上しない。
  - ## STATIC A｜通常終了の関数0x005BDAB1
  - 原作PEの`0x00609674`のDWORDは`0x005BDAB1`。当該入口から`0x005BDAD0 RET`までの原作x86機械語を独立読取した。
  - `0x005BDAB1 CALL 0x005BD9F7`：毎回`__flushall`を呼ぶ。
  - `0x005BDAB6 CMP BYTE PTR [0x0068DFD4],0`、`0x005BDABD JE 0x005BDAC4`：フラグが非0の場合のみ`0x005BDABF CALL 0x005CA6DB`（`__fcloseall`）。
  - `0x005BDAC4 PUSH [0x00B13A00]`、`0x005BDACA CALL 0x005B71E8`：CRT FILE*配列へのポインタを`_free`へ渡し、`RET`。
  - `0x005BB4FE MOV BYTE PTR [0x0068DFD4],AL`のALは第三引数`[EBP+0x10]`由来。したがってこのclose条件は`doexit`のreturnフラグに結び付く。対象は動的な通常終了時の分岐条件であり、実ゲームの終了動作は未実測。
  - `0x005BD9F7`は`PUSH 1 / CALL 0x005BD91D (flsall)`。呼出先は全FILEスロットを走査し、存在・flag&0x83条件で`0x005BDB12`によるFILEロック後、`0x005BD986 CALL 0x005BD8D5`（`__fflush_nolock`）へ進む。`EAX != -1`なら成功件数を増加させ、ループ終了時にロック解放する。書込み先、実際のflush結果は未実測。
  - `0x005CA6DB (__fcloseall)`はindex 3から開始。`0x005CA71B CALL 0x005B7A4E`で開いているFILEをcloseし、index>=20では`0x005CA73A CALL [0x006090A0]`（IAT=`DeleteCriticalSection`）、`0x005CA748 CALL 0x005B71E8`、`0x005CA753`でスロットをNULL化する。すべてのスロットが必ずopenであるとの主張ではない。
  - `doexit`のquick=1では`0x0060966C..0x00609678`の通常コールバックを飛ばすので、今回の`0x005BDAB1`にも到達しない。quick=0の場合のみ登録済みコールバックとして実行し得る。return=0ではフラグ0なので`__flushall`→`_free`、return=1ではフラグ非0なので`__flushall`→`__fcloseall`→`_free`の経路がある。終了済みguardや登録値のランタイム変更、実際の例外フローにより到達性は変わり得る。GoldenはそれぞれDESIGNED / NOT RUN。
  - 初期Ghidra検索DBの`0x005BDAB1`は関数としてNOT_FOUND。実際の直接CALL site `0x005BDAB1`、`0x005BDABF`、`0x005BDACA`も各0件。一方、**統合V9には同じ3 siteが各1件登録済み**。旧索引の不足をV9にも誤って一般化しない。既存V9を改変せず証拠を残す。
  - 次のP0候補は`0x005BD8D5 (__fflush_nolock)`の失敗値/書込側副作用、および`0x005B861A`の例外コードが`__exit`に伝わる経路。いずれも旧証拠と重複照合してから実施する。
- **Original-report limitations/errata:** 初期Ghidra検索DBの`0x005BDAB1`は関数としてNOT_FOUND。実際の直接CALL site `0x005BDAB1`、`0x005BDABF`、`0x005BDACA`も各0件。一方、**統合V9には同じ3 siteが各1件登録済み**。旧索引の不足をV9にも誤って一般化しない。既存V9を改変せず証拠を残す。 / PE・両検索DB SHA一致、SQLite quick_check両方ok、先行64/64と03H 38/38整合。独立native監査 **42/42 PASS**（失敗0）。途中の初回監査40/42は機械語切り出し末端がCALLの途中だった問題と、V9の既登録CALLを欠落と仮定した検査の誤り。対象範囲を広げ、V9の実測に従って修正し再監査して42/42 PASS。拒否・接続障害ではない。 / REA5種証拠: info=INDEX_ONLY、pseudo=callback NOT_FOUND（子関数INDEX_ONLY）、assembly=TARGETED_PE_NATIVE、callers=PE静的登録値、callees=PE-native+V9。新規5種完備0、正式VERIFIED+0、TODO/VERIFY/BLOCKED正式差分0/0/0、旧ゲームGolden PASS0、strict MATCH未実施、完全複製率未測定。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261028-05H-P0-FFLUSH-WRITE-COMMIT-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_05H_P0_FFLUSH_WRITE_COMMIT_STATIC.md`; SHA256 `837241CBC791CE25D2C7490DB5C2E27B1F153813282B1E88571A86C35EA84A60`, 3707 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_05H_P0_FFLUSH_NATIVE_EVIDENCE.json` SHA256 `6F13F78D2CD24037B8A3BEED75F28156827FA7C04AC8566BCC55346ACB5AA900`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 04Hまでは `flsall(1)`→`__fflush_nolock` の呼出元まで。今回は `0x005BD8D5` 内部と `0x005BD86D` / `0x005CA5D4` のnative ASM・IATを重点追跡。過去成果の再計上はしない。
  - ## STATIC A｜__fflush_nolock 0x005BD8D5
  - NULL FILE（`0x5BD8DE test esi,esi`）は `0x5BD8E3 CALL 0x5BD91D flsall(0)`。非NULLは `0x5BD8EC CALL 0x5BD86D __flush`。
  - `__flush` の戻り値が非0なら `0x5BD8F6` で戻り値 -1 とし `__commit` を実行しない。
  - 成功時かつ `FILE._flag & 0x4000` が真なら `0x5BD905 __fileno`→`0x5BD90B __commit(0x5CA5D4)`。このflagが無ければ0を返す。
  - `0x5BD911 NEG EAX` / `0x5BD914 SBB EAX,EAX` により __commitの0 / 非0を0 / -1に正規化。戻り値は静的に確定、実ファイル挙動は未観測。
  - ## STATIC B｜__flush 0x005BD86D の失敗処理
  - `FILE._flag & 3 == 2` かつ `FILE._flag & 0x108 != 0` のとき書込候補。 `_ptr-_base > 0` のときだけ `0x5BD8A3 CALL 0x5CA500 (__write)` に渡す。
  - `0x5BD8AB CMP EAX,EDI` で要求バイト数と戻り値が不一致なら `0x5BD8BE OR [esi+0xc],0x20` でFILE error flagを立て、戻り値 -1。
  - 重要: 成否にかかわらず、関数終端の `0x5BD8C9 AND [esi+4],0` と `0x5BD8CD MOV [esi],EAX` で `_cnt=0` / `_ptr=_base` に戻す。partial write時にもポインタが戻るnative構造を確認。
  - ## STATIC C｜__commit 0x005CA5D4
  - FILE handleが有効であれば lock / 再チェック後、IAT `0x006091BC = KERNEL32!FlushFileBuffers` を `0x5CA655` でCALL。
  - APIが0を返した場合は `0x5CA65F` でIAT `0x00609158=KERNEL32!GetLastError` をCALL。
  - 得られたエラーを `___doserrno` に格納、`0x5CA683` で `errno=9` (EBADF) に設定して -1 を返す経路が存在。これはerrno/doserrnoの差分を考慮すべき互換要件。
  - 独立監査 **34/34 PASS**、SQLite quick_check（初期DB/V9）ともok。CALL site `0x5BD8E3` / `0x5BD8EC` / `0x5BD905` / `0x5BD90B` / `0x5BD8A3` は初期DBと統合V9の双方で各1件登録。今回の5siteについて新規索引欠落0。
  - 次P0: `0x005CA500 (__write)`→`__write_nolock` の短書き／EOF / errno分岐と、`flsall(0)` における複数FILE失敗集約を限定調査。原作GoldenはDESIGNED / NOT RUN。
- **Original-report limitations/errata:** 状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。ゲームGolden実測0・正式REA新規VERIFIED0。 / ただしOSの実書込量、ディスク書込状態、再試行・利用者データ損失の実発生は未実測。 / 既存64/64維持。正式TODO/VERIFY/BLOCKED差分0/0/0。Golden PASS0、strict MATCH=NOT RUN、完全複製率=未測定。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261028-06H-P0-WRITE-NOLOCK-ERROR-RETURN-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_06H_P0_WRITE_NOLOCK_ERROR_RETURN_STATIC.md`; SHA256 `BB7B3ED53F0E5A25E742776F2DB3A9C7F21815AB090818C5AFB8C19F8A2F6320`, 4703 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_06H_P0_WRITE_NOLOCK_EVIDENCE.json` SHA256 `B2F92543352471BC068DA16822E44747CBC10DC3452A991B738244412A4720FE`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - MASTER / owner規約 / REA README・QUEUE・PROGRESS / 20261011最新保存同期64/64 / SEARCH README・BUILD_MANIFEST / 05H証拠34/34を先読。PCオンライン、active.lock不在。検索CLI `function 0x005CA500` → `__write`、`function 0x005C9E03` → `__write_nolock` を確認。`callers 0x005C9E03` には `0x005CA590` と `0x005D2FC9` を登録。今回は05Hの `__flush` 以前の証拠を再計上せず、`__write_nolock` のABI・エラー処理・Win32間接CALLを追加照合。
  - Win32 `WriteFile` が要求より短い非ゼロバイト数を返す場合、raw/binary枝 `0x005CA445`→`0x005CA44F` は返された数を保持し、`__write_nolock` 内で要求全量へ自動再試行する構造ではない。05Hで確認した上位 `__flush` は要求量との不一致を検査する。実際の書込量・例外動作は未観測。
  - `0x005C9E38` count==0 は `0x005C9E3D XOR EAX,EAX` で正常0返却（内部helperではbuf==NULLの検査より前）。count>0かつbuf==NULLなら `0x005C9E54` でerrno=0x16(EINVAL)。
  - Unicode系モード1/2では書込サイズが奇数なら `0x005C9EA1` のparity gateを経由して `0x005C9EB3` errno=0x16(EINVAL)。呼出側のファイルハンドル検査は `__write 0x005CA500` が実施するため、helper単体の0長返却を公開APIの全条件に一般化しない。
  - text変換にはLF→CRLF挿入経路（`0x005CA1D1` の0x0A比較、`0x005CA1D6` の補正数増加）がある。複数コードページ経路を一律のバイト換算とは断定しない。
  - `0x005CA464` の `GetLastError` を `0x005CA479` 以降で検査。Win32 error=5なら `0x005CA492` errno=9(EBADF)、`0x005CA49D` _doserrno=5。その他非ゼロエラーは `0x005CA4A7` の `__dosmaperr` に渡す。
  - 書込数0かつエラーコード0の場合、`0x005CA4B7` のデバイスflag 0x40と入力先頭0x1A(Ctrl-Z)の特例を除き、`0x005CA4D2` errno=0x1C(ENOSPC)、`0x005CA4DD` _doserrno=0、戻り値-1へ進む。非ゼロバイト進捗があれば、エラー確定より先に部分書込数の返却経路へ進み得る。実動作未観測。
  - 原作PE importから IAT `0x00609080`=KERNEL32!WriteFile、`0x00609158`=KERNEL32!GetLastError、`0x0060917C`=KERNEL32!WideCharToMultiByte と独立照合。Ghidraの `0x005CA445 CALL [0x609080]` 等は機械出力で「対象未確定」だが、固定IAT参照はPE静的証拠として解決可能。実行時IAT改変の可能性は未評価。
  - 独立監査 **40/40 PASS**、初期DBとV9のSQLite quick_check=ok。direct CALL `0x005CA590`・`0x005BD8A3` は両DBで各1件。新規索引欠落0（検査した2siteに限定）。
  - 次の調査優先: `0x005D2FC9` から同helperへの第2呼出元のパラメータ契約、及び `0x005CA4E5` のUnicode/console partial-write時のカウント補正を限定追跡。原作Goldenは別途観測が必要。
- **Original-report limitations/errata:** 状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式VERIFIED=0、原作ゲームGolden PASS=0。 / 正式TODO/VERIFY/BLOCKED差分0/0/0、既存Wave1～5は64/64維持、Golden実測0、strict MATCH=NOT RUN、完全複製率=未測定。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261028-07H-P0-CHSIZE-ZEROFILL-WRITELOOP-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_07H_P0_CHSIZE_ZERO_EXTENSION_STATIC.md`; SHA256 `D16B1D561DF2E1290846C81D76243921D2FF3FF39D86E66C2E9064FD5365D8CE`, 6099 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_07H_P0_CHSIZE_NATIVE_EVIDENCE.json` SHA256 `2F8282B7E8B70CA9FA65143288083754837B7B106C3B3830595AB3198A03C967`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 07Hは06Hが残した第2呼出元 `0x005D2FC9` を分析。検索CLI `callers 0x005C9E03` から caller function `0x005D2F0C` を特定。単独の `function 0x005D2FC9` はNOT_FOUNDだが、これはCALL siteであって関数入口ではない。正しい `function 0x005D2F0C` は `__chsize_nolock`（438 bytes、Ghidra VS2010 library match）。この区別を新規索引欠落と誤認しない。
  - `0x005D2F26` 現在位置、`0x005D2F42` ファイル終端を `__lseeki64_nolock` で取得。x86で戻り値はEDX:EAX、`0x005D2F59 SUB ESI,EAX` / `0x005D2F5B SBB EDI,EDX` で要求最終サイズと現ファイル終端の64-bit差分を算出する。
  - 正の拡張差分には `0x005D2F6D MOV EBX,0x1000`（4096 B）と `0x005D2F73 PUSH 8` → `0x005D2F75 GetProcessHeap` → `0x005D2F7C HeapAlloc` を使用。Windows HeapAlloc flags 8 = HEAP_ZERO_MEMORYでゼロ初期化したバッファを確保する。
  - `0x005D2FA0 PUSH 0x8000` → `0x005D2FA8 CALL 0x005D30C2` は `__setmode_nolock` で**一時的にbinary mode**へ切替える（改行変換防止）。`0x005D2FB2..0x005D2FC2` で残量と4096の小さい方を選び、`0x005D2FC3` buffer、`0x005D2FC6` fdをpush、`0x005D2FC9 CALL 0x005C9E03` でゼロデータを追記する。
  - `0x005D2FD1 CMP EAX,-1` が失敗判定。非-1なら `0x005D2FD6 CDQ` と `0x005D2FD7 SUB` / `0x005D2FD9 SBB` で64-bit残量から**実際の返却書込バイト数**を差し引き、正の残量は `0x005D2FDD JG 0x005D2FB2` で再試行する。06Hの一般`__flush`とは異なり、この伸張loopは部分書込を残量から差し引いて続行する。
  - 要求サイズ < 現終端の場合、`0x005D303D` で要求サイズへseekし、`0x005D3053` でOSハンドルを取得して `0x005D305A CALL [0x006091D8]`（KERNEL32!SetEndOfFile）により切詰めを要求。失敗時 `0x005D307A` でerrno=13(EACCES)、`0x005D3087` GetLastErrorを_doserrnoへ格納する経路を確認。
  - 拡張時のHeapAlloc失敗は `0x005D2F8E` でerrno=12(ENOMEM)。書込-1の場合は `0x005D300C` で_doserrno確認、値5なら `0x005D301B` でerrno=13(EACCES)へ変更する経路を確認。
  - 拡張loopを離れると `0x005D2FE6` で保存済みモードを `__setmode_nolock` に渡して復元し、`0x005D2FFF` HeapFreeで一時バッファを解放する。成功時は `0x005D30A8` のseekで**元のファイル位置へ復帰**してから `0x005D30BB XOR EAX,EAX`（成功0）となる。失敗時 `0x005D2F94` → `0x005D2F99 MOV EAX,[EAX]`（errno値を戻す）へ分岐して元位置復帰を省く経路がある。よってこのCRT helperの失敗時にはseek済み現在位置が残り得る（要Golden観測）。
  - 固定IATをPEインポートテーブルから独立確認: `0x00609188` GetProcessHeap、`0x00609134` HeapAlloc、`0x00609154` HeapFree、`0x006091D8` SetEndOfFile、`0x00609158` GetLastError。すべてKERNEL32.dll（実行中のIAT変更は対象外）。
  - 初期DB `calls` / V9 `native_callsite` とも、`0x005D2FC9` (__write_nolock)・`0x005D2FA8`・`0x005D2FEC` (__setmode_nolock)・`0x005D2742` (__chsize_nolockへの上位CALL)の**4箇所各1件**。この範囲の直接CALL索引漏れ0。
  - 次VAは `0x005D2370` の `0x005D2742` call-site（ゲームコードとの到達関係/CRTのみの使用状況）と、前回繰越 `0x005CA1D1..0x005CA4EB`（console/Unicode部分書込の正確な補正）。
- **Original-report limitations/errata:** 状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、原作ゲームGolden PASS=0。 / 07Hは06Hが残した第2呼出元 `0x005D2FC9` を分析。検索CLI `callers 0x005C9E03` から caller function `0x005D2F0C` を特定。単独の `function 0x005D2FC9` はNOT_FOUNDだが、これはCALL siteであって関数入口ではない。正しい `function 0x005D2F0C` は `__chsize_nolock`（438 bytes、Ghidra VS2010 library match）。この区別を新規索引欠落と誤認しない。 / 既存Wave1～5の最終保存同期=64/64 VERIFIED（旧QUEUE/PROGRESSのEPERM表示は古い）。新規VERIFIED=0。正式TODO/VERIFY/BLOCKED差分=0/0/0。今回静的証拠はゲーム実行結果ではない。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261028-08H-P0-OGG-FOPEN-CHSIZE-UNREACHABLE-GATE-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_08H_P0_OGG_FOPEN_CHSIZE_STATIC.md`; SHA256 `67B34425C140B977B0527D4601B6B7430878075B7E28BC63AB69A990A78E648C`, 5975 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_08H_P0_OGG_FOPEN_CHSIZE_EVIDENCE.json` SHA256 `AECD5CCE3B82030F429F84CF9A61600A250E7FC5097655FA4F7312D598B4DED0`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - MASTER、所有権規約、REA README/QUEUE/PROGRESS、10/11最終sync(64/64)、10/21検索README/BUILD_MANIFEST、07H静的監査証拠を読取。07H証拠の52/52 PASSを確認。active.lockなし、Windows PC接続成功。08Hは07Hで未解決の `0x005D2742` CALL siteの上位到達性を対象とし、07Hの4096-byte zero-fill解析を二重計上しない。
  - ## 新規STATIC-A：__chsize_nolockの呼出元はCRTオープン関数
  - `0x005D2742 CALL 0x005D2F0C` は、Ghidraで `FUN_005d2370` と記録されたCRT `__sopen_nolock` 相当関数の内部。そこへ到達する直接CALLを、次のように上位まで辿った。
  - `0x005D16C0`（ファイル読取用wrapper）→ `0x005D16CF CALL 0x005D1D6D`（`_fopen`）→ `0x005D1D7A CALL 0x005D1CB1`（`__fsopen`）→ `0x005D1D43 CALL 0x005D1ECE`（`__openfile`）→ `0x005D212E CALL 0x005D2B68`（`__sopen_s`）→ `0x005D2B7E CALL 0x005D2AA4`（`__sopen_helper`/VS2010 FID候補）→ `0x005D2B0E CALL 0x005D2370`。
  - `0x005D2AA4`はGhidra FIDで狭文字/ワイド文字の競合警告あり。呼出元の`_fopen`がchar*で、下流PEにはCreateFileAが存在するため、**今回の特定経路**は狭文字経路と整合するが、一般CRTライブラリの全入口を形式同定した主張ではない。
  - ## 新規STATIC-B：ゲームのOggDecoderからはrbで開く
  - ゲーム側の音声ルート `0x004BEAD9 CALL 0x00501E20` → `0x00501E93 CALL 0x00502020`（OggDecoder::vftableを持つオブジェクト）→ `0x00502038 CALL 0x005D16C0` を保存済検索索引と原作機械語で照合。
  - `0x005D16C9 PUSH 0x0065B5B4` は`_fopen`のmode引数。原作PEの`0x0065B5B4`にある実バイトを確認したところ **`72 62 00` = `"rb"`**。
  - `__openfile`の `0x005D2046 OR EBX,0x8000` はb指定でバイナリフラグを設定する経路。r指定は読み取りモードで、`_O_RDWR=2`を付与しない。したがって本Ogg読取経路はread-only/binaryであり、後述の条件を満たさない。
  - ## 新規STATIC-C：__chsize_nolockはテキストRW + 末尾Ctrl-Z時の限定処理
  - 原作機械語 `0x005D26E2 TEST CL,0x80` → `0x005D26E5 JE 0x005D2992` がテキスト/バイナリ系ガード、`0x005D26EB TEST byte ptr [EBP+0x10],2` → `0x005D26EF JE 0x005D2760` がread/writeフラグのガード。
  - 通過後に `0x005D2729 CALL 0x005BDCD1`（`__read_nolock`、1byte）を実行し、`0x005D2731 TEST EAX,EAX` → `0x005D2733 JNE 0x005D274E` と `0x005D2735 CMP byte ptr [EBP-4],0x1A` → `0x005D2739 JNE 0x005D274E` の両ガードを満たすと `0x005D2742 CALL 0x005D2F0C`へ到達する。
  - 読み取り戻り値0かつバッファ中の0x1Aが成立する場合、EOF相当の末尾Ctrl-Zを切詰めるCRT互換コードと整合。返値-1なら `0x005D274C JE 0x005D2711` からclose/error処理へ分岐する。
  - 次の対象は `0x005CA1D1..0x005CA4EB`（`__write_nolock` Unicode/console戻り値補正）、またはOggDecoder `0x00502020` の仮想CALL `0x0050202A`のvptr解決。いずれも既存証拠と重複しないか先読する。
- **Original-report limitations/errata:** 状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。Game Golden実測0、strict MATCH NOT RUN、正式REA新規VERIFIED 0。 / 関数別5種の充足は info=INDEX_ONLY、pseudo=INDEX_ONLY+原作ASM対照、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY+TARGETED_PE_NATIVE。正式REAの5種類完全パックの新規取得0、新規VERIFIED=0。既存Wave1～5最終保存同期64/64のまま。正式TODO/VERIFY/BLOCKED差分0/0/0。原作Golden PASS0、完全複製率未測定。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261028-09H-P0-OGG-RESET-VTABLE-SLOT-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261028_09H_P0_OGG_VTABLE_STATIC.md`; SHA256 `9BC093555163F81506F389254A77C3A7014415478F76FC4639C43FC83A33CC92`, 4417 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261028_09H_P0_OGG_VTABLE_EVIDENCE.json` SHA256 `DA4BC90F9BEABED63A4658F7B91B119A32934B1E0CB56D76D85018513B92E952`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - ## 新規 STATIC-A: 間接CALLの具体的なスロットを原作PEで解決
  - `0x00501E7E: MOV dword ptr [ESI], 0x006395CC` でOggDecoderオブジェクトのvptrを設定。
  - vtable `0x006395CC` の5エントリは順に `0x00501DF0, 0x00501F10, 0x00502000, 0x00502020, 0x00501EB0`（原作PEの値をread-only取得）。
  - `0x00501E93: CALL 0x00502020`。該当関数は `0x00502022 MOV ESI,ECX` → `0x00502024 MOV EAX,[ESI]` → `0x00502026 MOV EDX,[EAX+0x10]` → **`0x0050202A CALL EDX`**。
  - 従って、**このコンストラクタから渡されたvptrが維持される経路**に限り、間接CALL `0x0050202A` は `0x00501EB0`（vtable+0x10）に解決する。一般の仮想呼出し全体を解決したわけではない。
  - `0x00502038 CALL 0x005D16C0`（旧08Hで確認済みのrbファイルopen）より**前に**cleanup/resetが走る。
  - ## 新規 STATIC-B: スロット関数は状態に応じた解放＋初期化
  - `0x00501EB4 CMP byte ptr [ESI+5],1` と `0x00501EB8 JNE 0x00501EC9`：状態フラグが1のときだけ `0x00501EC1 CALL 0x005CFE00`。
  - `0x005CFE00`の保存済擬似Cは内部領域（対象オブジェクト+0x118）のコーデック関連メモリ解放を示す。詳細な解放順と副作用は未正式VERIFIED。
  - その後 `0x00501ED8` / `0x00501EEB` の2回のmemsetでデコーダ内部領域をゼロ初期化し、オブジェクトのサイズ・状態フィールドを0化、`0x00501F07 RET`。
  - 旧検索DBの `indirect_calls` に `0x0050202A` 1件、同siteの直接`calls`0件。分類は正しく、vtable slotの値をGhidraが補完しないこと自体は索引欠落ではない。
  - `0x00501E93,0x00502038,0x00501EC1` は旧検索DBの直接CALLにそれぞれ1件。2DBの `PRAGMA quick_check` はok。既存スナップショット/独立PEを横断監査。
  - Golden PASS 0、完全複製率未測定。実行時vptrの変更・別インスタンス・関数 `0x005CFE00` 内の追加間接CALL `0x005CFEEE` は引き続きVERIFY。
  - 次回 P0： `0x005CFEEE` のコールバックポインタの設定元、呼出条件、ABIを旧検索DB・PEから先に調査。または `0x005CA1D1..0x005CA4EB` のUnicode/console戻り値の前回未解決経路。
- **Original-report limitations/errata:** - 初回構築時は状態=0からreset経由でopenへ進む。再open時に状態=1なら以前のコーデックを解放してから新規ファイルを開く構造。**ファイルopenが失敗しても以前の状態は既に消去される可能性**があり、失敗後のユーザー可視挙動は実機VERIFY。 / - 自動静的監査 **27/27 PASS**。既存正式VERIFIED 64/64（Wave1〜5、最終保存syncを参照）、今回新規VERIFIED 0。TODO/VERIFY/BLOCKEDの正式差分0/0/0。 / - Golden PASS 0、完全複製率未測定。実行時vptrの変更・別インスタンス・関数 `0x005CFE00` 内の追加間接CALL `0x005CFEEE` は引き続きVERIFY。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

## Integration handoff

Original owner source SHA and research ID are primary recovery keys. Native x86 and current unified V9 outrank old V3 pseudotypes; repeated instruction sites across reports are not new functions. Existing denied VA/Wave6/18H results, raw EXE/SAVE/SQLite, and any private identities not uploaded. All refs/dictionaries/develop remain curator-only. Only reviewed source-backed facts may be formally adopted. No new native test was performed by the recovery.
