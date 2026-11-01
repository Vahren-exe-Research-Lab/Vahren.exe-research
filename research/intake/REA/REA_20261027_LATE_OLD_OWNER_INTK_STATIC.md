# REA 2026 historical research intake: 20261027 LATE

**REA owner / PRIVATE owner branch / STATIC or conditional INFERRED / VERIFY, NOT CURATED or READY.** The original owner wrote these 12 studies previously. This archive remeasures only the source Markdown SHA256, bytes, and small same-hour evidence filename/SHA candidates read-only; no Ghidra, REA, original game, new native evidence, or Golden run performed. Original PE and V9 actual hashes were not recalculated in this intake. Source excerpts preserve bounded x86 CALL/ABI/control-flow observations, but are not a full verbatim copy; detailed owner report still exists on the authorized research PC. Machine evidence remains PC-only. Formal newly VERIFIED 0 and Golden PASS/READY 0.

### REA-LOCAL-20261027-12H-P0-D3D9-DUAL-DISPLAYMODE-BORDERLESS-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_12H_P0_D3D9_DISPLAY_MODE_CHAIN_STATIC.md`; SHA256 `AAA73D5A41B49B6CF923CB797008634C3AEF5D60E38699CE16F01BA70EF85964`, 5604 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_12H_P0_D3D9_DISPLAY_MODE_CHAIN_EVIDENCE.json` SHA256 `7F03D2C6E03920F52E3399DD7ECD8D3131B1CE21D1DD56FBFE3480EA4BBAE233`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - ## 発見1：同じDirect3D9 COMオブジェクトへ2度問い合わせる
  - `0x00555561 PUSH 0x20 → 0x00555563 CALL [0x6092B4]` はPEインポート表で **d3d9.dll!Direct3DCreate9** と独立照合した。戻り値を`DAT_00879808`へ格納（`0x00555569`）。
  - 起動前半：`0x0055559E` vtable `+0x20` → `0x005555A8 CALL EDX`。adapter=0、出力先`[ESP+0x44]`、HRESULT負値で失敗終了（`0x005555AA/AC`）。成功時、`[ESP+0x44]`→幅`DAT_0065BEEC`、`[ESP+0x48]`→高さ`DAT_0065BEF0`（`0x005555DF..ED`）。
  - ゲーム初期化後半：`0x0055969E`で同じグローバルCOMオブジェクトを再取得し、`0x005596AD` vtable `+0x20` → `0x005596B0 CALL EAX`。adapter=0、出力先`[ESP+4]`、HRESULT負値でAL=0復帰（`0x005596B2/B4`）。
  - ## 発見2：0x38バイトのD3DPRESENT_PARAMETERS生成
  - `0x005596DD..EB`は`DAT_008795F0`から0x38バイトをゼロ初期化。`0x00559728/35`でW/H→`+0x00/+0x04`、`0x0055971A`で2回目DisplayModeの`Format`候補`[ESP+0x10]`を読み`0x00559766`で`+0x08`へ格納。`+0x0C` BackBufferCount=1、`+0x18` SwapEffect=1、`+0x1C` HWND、`+0x24` EnableAutoDepthStencil=0。
  - `0x0055976E` vtable `+0x40`→`0x00559774 CALL EAX`は標準IDirect3D9 ABIのCreateDevice相当。adapter=0、DeviceType=1、BehaviorFlags=0x20、D3DPRESENT_PARAMETERSポインタ=`0x008795F0`、出力オブジェクト=`0x0087980C`。HRESULT負値でAL=0経路へ入る。
  - ## 発見3：Window styleとD3D Windowedフラグを分離する別モード
  - 起動引数パーサ`0x00556250`の分岐に`0x00556639 MOV BYTE PTR [0x00879821],1`、直後`0x00556640 MOV DWORD PTR [0x0065BEE4],0`が同居する。
  - ウィンドウ生成側`0x00555710..27`では、モード0ならstyle計算は`0x80000000`（WS_POPUP、枠なし）、位置は`0x00555782..AB`の分岐で(0,0)へ、`0x005557CC`でstyleを渡し`0x005557D8`のCreateWindowExAを呼ぶ。PEインポートのCreateWindowExA/AdjustWindowRectExも照合した。
  - 一方D3D初期化側は`0x005596EE`でこの専用フラグを検査し、非ゼロなら`0x005596F7`で`D3DPRESENT_PARAMETERS.Windowed (+0x20)=1`、ゼロなら`0x00559703/09`で画面モード値を採用する。従って**枠なしウィンドウ（WS_POPUP）だがD3DはWindowed=1**の組合せを作れる。
  - ## 独立監査と未検証
  - 原作機械語（0x005554F0/0x00559690/0x00556250）を限定逆アセンブルし、命令位置、PE imports、両SQLite quick_check、前回67検査、同期64件を独立照合。**72/72 PASS、失敗0**（監査条件数であり新規関数数ではない）。
  - *次のP0**：`0x00556250`で`0x00556639`へ至るオプション認識条件の文字列起源と、`0x00559690`の`0x00879821`の初期値・全writerを照合。2回のDisplayMode照会が異なる結果を返した場合の優先関係をGolden条件として明示する。
- **Original-report limitations/errata:** ## 独立監査と未検証 / 5証拠：info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。今回新規の完全5種取得=0、正式VERIFIED追加=0、QUEUE TODO/VERIFY/BLOCKED変更=0/0/0。実機Golden PASS=0、strict MATCH/完全複製率は未測定。 / Golden設計（NOT RUN）：(A) 通常ウィンドウ、(B) 排他的フルスクリーン、(C) パーサ専用フラグの枠なしWindowed=1 を分け、GetAdapterDisplayMode二回の戻り値・画面W/H・Format・HWND style・D3DPRESENT_PARAMETERSをトレースして比較する。DisplayMode幅/高さ0の実到達は未証明。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261027-13H-P0-FF-TOKEN-FLAG-LIFETIME-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_13H_P0_FF_BORDERLESS_TOKEN_STATIC.md`; SHA256 `0571D35B9E90EB9C1099126CC097060993DF045D53839360690E4146F169A958`, 3785 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_13H_P0_FF_BORDERLESS_TOKEN_EVIDENCE.json` SHA256 `38176EE16DCB9556CEDEA876D183007AB57E30FDD2CB221C0D2C4EC1E4FC502F`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - ## P0発見：ff は f と区別される2文字トークン
  - 原作アドレス 0x00629AB4='f\0'、0x00629AB8='s\0'、0x00629ABC='ff\0'。0x0055660C は後者へのポインタを比較器 0x00402C40 に渡し、0x00556611 CALL→0x00556616 TEST→0x00556618 JNE→0x0055661A CMP ESI,2→0x00556633 JE の分岐で比較値と長さを検査する。
  - 一致時のみ 0x00556639 MOV byte [0x00879821],1 および 0x00556640 MOV dword [0x0065BEE4],0。1文字 'f' 判定(0x00556588/8D/AF)は後者モード0だけへ進む別経路。
  - 0x005596EEは専用フラグを検査、非ゼロなら0x005596F7でD3DPRESENT_PARAMETERS.Windowed=1、ゼロなら0x00559703経由で画面モード値を採用。'f'と'ff'の区別がD3Dフルスクリーンの種類を変える。
  - 0x00879821はPEの.data仮想領域のうちRAW_SIZEを超える領域にあり、新規ロード時はPEローダによりゼロ初期化される。ディスクの実バイトとして「00」が存在するとは主張しない。
  - 原作PE内にある0x00879821絶対アドレスのlittle-endian直接参照は2箇所：命令即値 0x0055663B（MOV書込）と0x005596F0（CMP読取）。これは**直接絶対参照の調査結果**であり、ポインタを経由した間接書込の不存在証明ではない。
  - 比較器0x00402C40は生のbyte比較で、今回確認した比較経路には大小文字変換がない。入力正規化/トークン化前に変換があるかは別途VERIFY。
  - 'f'は0x0065BEE4=0へ向かうが、専用フラグはセットしない。一方'ff'では同モード値0に加えて0x00879821=1、D3D Windowed=1。前回12Hの枠なしWS_POPUPと合わせてborderless-windowed候補を補強する。
  - 次：0x0055630Fの文字列tokenizerと0x00555519の引数生成を調査して、'ff'を外部から入力する**正確な構文**および'f'との優先順位を静的確認。Goldenは通常・f・ffの別条件としてDESIGNED / NOT RUN。
- **Original-report limitations/errata:** 比較器0x00402C40は生のbyte比較で、今回確認した比較経路には大小文字変換がない。入力正規化/トークン化前に変換があるかは別途VERIFY。 / 起動コマンドの**生文字列にプレフィクスが必要か**、複数引数の優先順位、実機での動作、既存起動プロセスの現在値は未検証。むやみにゲームを起動していない。 / 5証拠：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED変化は0/0/0。strict MATCH未測定、完全複製率未測定。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261027-14H-P0-CMDLINE-SPACE-FF-S-ORDER-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_14H_P0_CMDLINE_TOKEN_STATIC.md`; SHA256 `B6036BDF0ED5B53FDAEDBA6CBD56D1ABC9DC984E9A5264DED678DF0C6B604AB2`, 4709 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_14H_P0_CMDLINE_TOKEN_EVIDENCE.json` SHA256 `A3967BD99998D8F596CB6DC5FA8B9A72BE351FCB0848A8C14C3932B6DB7B9D37`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - ## 新規P0証拠：WinMainの生文字列
  - CRT 0x005B85D0で __wincmdln 相当の呼出し→0x005B85E5で結果を第3引数としてPUSH→0x005B85EC CALL 0x005554F0。0x00555509 は[EBP+0x10]をESIへ読み、0x00555517 MOV ECX,ESI →0x00555519 CALL 0x00556250。つまりargv配列の後処理ではなくWinMainへ渡るcommand-line tailの文字列を直接解析している（呼出先の具体的なCRT文字列整形は別途VERIFY）。
  - 0x0055630F →0x00402800 はtokenizerでは**なくstd::stringへの全文コピー**。先行報告13Hの「0x0055630F tokenizer」は訂正。真の字句分割は0x00556373の_memchrと0x005563B0→0x00558C70、部分文字列0x005563CB/0x00556433、vectorへの追加0x005563DE/0x00556452で構成。
  - 元PEアドレス0x00629A98と0x00629A9CはそれぞれASCII 0x20（半角スペース）。0x0055636B/6D の len=1 を伴う _memchr は先頭側の半角スペースを飛ばし、0x005563A3/A5 の len=1 を伴う 0x00558C70 は次の半角スペースを探す。TAB（0x09）・引用符の除去や正規化は当該直接経路には無い。大小文字変換も比較器0x00402C40には存在しない。
  - 0x0055658Dは1文字「f」、0x005565D1は「s」、0x00556611は2文字「ff」をbyte単位で比較し、トークン長も確認。よって、この関数の入力上は単独の半角スペース区切り「ff」が一致候補。「-ff」「/ff」「FF」や引用符を含んだトークンはこの認識経路では不一致（外側での引数加工は実機未観測）。
  - ## 新規P0証拠：順序依存
  - 「f」一致は0x005565AFから0x00556640へ分岐してモード0を設定。「ff」一致は0x00556639で0x00879821=1、続いて0x00556640でモード0、0x0055664A～52で次トークンを処理。fにはffフラグを消す命令が無いため、新規起動時の初期フラグ0という前提では「f ff」「ff f」は**どちらもff優先**という静的推論（間接書込や外部変換をすべて排除した動的証明ではない）。
  - 「s」一致は0x005565F3→0x0055665Dで数値幅・高さの読込・上下限clamp後に0x0055671A終了処理へ入り、残りの引数走査へ戻らない。「s 800 600 ff」は末尾ffを認識しない一方「ff s 800 600」は先にffフラグを設定できる、という静的な優先順位差を導く。通常の起動実験では未測定。最大10トークンはGhidra疑似CからのINDEX_ONLYで別途生ASM一部追加検証要。
  - 次回：0x005B85D0→0x005BF601のCRT __wincmdln 仕様および「s」値欠落・重複を優先し、通常/f/ff/順序入替の原作Golden条件を DESIGNED/NOT RUN として維持する。
- **Original-report limitations/errata:** CRT 0x005B85D0で __wincmdln 相当の呼出し→0x005B85E5で結果を第3引数としてPUSH→0x005B85EC CALL 0x005554F0。0x00555509 は[EBP+0x10]をESIへ読み、0x00555517 MOV ECX,ESI →0x00555519 CALL 0x00556250。つまりargv配列の後処理ではなくWinMainへ渡るcommand-line tailの文字列を直接解析している（呼出先の具体的なCRT文字列整形は別途VERIFY）。 / 0x0055630F →0x00402800 はtokenizerでは**なくstd::stringへの全文コピー**。先行報告13Hの「0x0055630F tokenizer」は訂正。真の字句分割は0x00556373の_memchrと0x005563B0→0x00558C70、部分文字列0x005563CB/0x00556433、vectorへの追加0x005563DE/0x00556452で構成。 / 独立PE命令・文字定数・呼出site・DB参照・既存13H非重複・旧REA集約を56/56 PASS。旧原作Golden実機PASS=0、strict MATCH未測定、完全複製率未測定。新規正式REA VERIFIED=0／5種完全取得=0／正式TODO・VERIFY・BLOCKED差分0/0/0。5証拠 info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。保存済み監査はゲーム起動・REA/Ghidra再実行を含まない。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261027-15H-P0-CRT-WINCMDLN-S-MISSING-ARGS-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_15H_P0_CRT_S_EDGE_STATIC.md`; SHA256 `CCF132635C0369306BD45AFE6A2DADD880F3C017C807D4C93C08427291DBC0DB`, 4234 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_15H_P0_CRT_S_EDGE_EVIDENCE.json` SHA256 `DD46EAF2FF90CDC9DF1A556F4724E386474D9542E4342A7192D9C1EC7A74CF3E`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - ## P0新規発見1：CRT `__wincmdln` が実行ファイル名を切り離す
  - `0x005B85D0 CALL 0x005BF601` → `0x005B85E5 PUSH EAX` → `0x005B85EC CALL 0x005554F0` → `0x00555519 CALL 0x00556250`。
  - `0x005BF601`のネイティブ命令で`0x005BF625 CMP AL,0x20`、`0x005BF631 CMP AL,0x22`（ダブルクォートによる状態反転）、`0x005BF642 CALL 0x005B6D85`（MBCS先行バイト判定）、`0x005BF650 CMP AL,0x20`を確認。CRTはEXE名の終端判定で引用符を認識し、0x20以下の空白・制御文字を飛ばして引数文字列へのポインタを返す。
  - 一方ゲーム側`0x00556373`と`0x005563B0`が利用する区切り定数はともにASCII `0x20`のみ。ゆえに**CRTがプログラム名直後のタブを許すことと、オプション間のタブを区切りに認識することは別**。例`ff&lt;TAB>s`は一個の不一致トークンとなると予測する（実機未測）。
  - ## P0新規発見2：`s`の寸法値は省略可能な分岐構造
  - `0x005565F3 JNE 0x0055665D`（`s`一致）→`0x0055665E`で認識戻り値用フラグ1。続く`0x00556663/67`は幅の有無、`0x00556693/9A`は高さの有無を別々に判定し、存在する値にだけ`0x005B7576`（_atol経由）を適用する。欠落側は既存のグローバル幅`0x0065BEEC`／高さ`0x0065BEF0`を維持し、末尾で640～1600／480～1200へクランプする。
  - `s 1024 768 ff`はサイズ処理を終えると`0x0055671A`へ移り、後続ffを処理しない。これは14Hで記録済みの「s短絡」への欠落引数の追加検証。
  - ## P0新規発見3：未知トークンも残りの走査を中断
  - `0x00556633 JE 0x0055671A`は`f/s/ff`その他認識対象への不一致後、後続引数のループに戻らず終了する。例`unknown ff`は後続`ff`へ到達しないという静的予測（ゲーム実機はNOT RUN）。
  - `0x00558C70`の区切り探索とトークン10件上限、`0x00556250`の末尾トークン・未知引数による早期終了がWinMain側へ戻すALの挙動を重点確認。Golden計画：`f` / `ff` / `s` / `s 1024` / `unknown ff` / `ff&lt;TAB>s` / `ff s 800 600` はDESIGNED/NOT RUN。
- **Original-report limitations/errata:** 条件付き合成予測：他の上書きがなければ`s`→800×600、`s 1024`→1024×600、`s 0 0`→640×480。いずれもAL=1の認識成功となり、debug_paperへの代替読込を抑止し得る。**原作実機Goldenではない**。 / `REA_20261027_15H_P0_CRT_S_EDGE_AUDIT.py`の独立監査は63/63 PASS、旧DBと統合V9のCALL-site / SQLite quick_check / SHA256 / PE生ASM・初期値・14H evidence・64件の旧正式syncを照合。新規正式VERIFIED=0、5種完全充足=0、正式TODO/VERIFY/BLOCKED差分0/0/0、過去Wave1～5正式64/64を維持。 / 5種：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。関数意味論・全例外経路・実ゲームGolden=VERIFY/NOT RUN、strict MATCH/完全複製率=未測定。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261027-16H-P0-TOKEN10-FF-DEBUG-FALLBACK-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_16H_P0_TOKEN10_FF_RETURN_STATIC.md`; SHA256 `163C24BCC4CB2758BE18CE1E674C1519676F1C0706CD7CCD36F294C36ABE0F7E`, 6330 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_16H_P0_TOKEN10_FF_RETURN_EVIDENCE.json` SHA256 `A216D41CE8043CC6085ED22A74FF7CA612D1FED5846F918A6D1F4893854C92A2`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 過去15HのCRT空白処理、s欠落、未知引数短絡を二重計上せず、今回の差分は(1)0x00558C70の実機械語契約、(2)10件上限の機械語確定、(3)f/ffの戻り値ALがsと異なること。
  - ## P0新規発見1：0x00558C70は文字集合探索（最初の一致位置）
  - 関数入口 `0x00558C70`、呼出元 `0x00556250` の `CALL site 0x005563B0`。索引の直接CALLと原作PE機械語の両方で一致。もう一つの既知callerは`0x005588E0`の`0x00558BD3`。
  - `0x00558C7C`は探索文字集合の長さ0を検出、`0x00558C83/85`はstart>=string lengthの範囲外を拒否、`0x00558CBA`で`_memchr`を呼ぶ。見つからない場合`0x00558CCE`でEAX=-1、`0x00558CD2 RET 8`。一致時は`0x00558CE2 SUB EAX,EBX`で先頭からの位置へ変換して`0x00558CE5 RET 8`。
  - ゲーム引数側は`0x005563A3 PUSH 1`、`0x005563A5 PUSH 0x00629A9C`（実バイトASCII空白）、`0x005563AA MOV EAX,ESI`で開始位置を与える。よってここでの探索対象区切りは半角スペース1文字。一般化したヘルパそのものを「空白専用」とは誤認しない。
  - ## P0新規発見2：10件上限は機械語で明示される
  - `0x005562CF PUSH 0xA`と`0x005562D1 PUSH 0x1C`が10個×28バイトの文字列配列を構築し、`0x005562DB`のvector constructor iteratorへ渡す。
  - 区切りあり分岐は`0x005563FF`でトークン数を加算し、`0x00556403`で配列次要素へ28バイト進み、`0x00556408`でEBXを加算、`0x0055641E CMP EBX,0xA`と`0x00556421 JB 0x00556330`で10件未満の場合のみ続行。10件で`0x00556427`から終了。
  - 区切りが最後まで無い場合は`0x005563B9/BC`で-1を検出し、`0x00556429 PUSH -1`から残り全体を1トークンとして格納、`0x0055646B`で件数を加算して終了する。
  - 終了時は`0x00556733 PUSH 0xA`・`0x00556735 PUSH 0x1C`で10個×28バイトを破棄する。従って先頭から最大10件だけが走査候補、11件目以降は処理されないという静的制御フロー。
  - ## P0新規発見3：`f`・`ff`は設定を変更しても戻り値AL=0
  - `0x00556471`が戻り値用スタックbyte `[ESP+0x17]`を0に初期化。`0x0055665E`の`s`分岐だけが同byteを1に設定する。関数全体1344バイトを独立逆アセンブルし、このbyteへの明示的な直接MOV書込はこの2件と確認。終了`0x00556764`はこのbyteをALへ転送する。
  - `ff`側`0x00556639`は別のグローバルフラグ`[0x00879821]=1`、`0x00556640`は画面モード`[0x0065BEE4]=0`を変更するが、戻り値byteは変更しない。`f`も同様にAL=0のまま。したがってALは「何かしらのオプション認識」を意味しない。**sを見つけたことを示す特殊ゲート**として扱う必要がある。
  - 呼出元`0x00555519 CALL 0x00556250`→`0x0055551E MOV BL,AL`→`0x00555520 TEST BL,BL`→`0x00555522 JNE 0x0055552B`でALが0のとき`0x00555524 CALL 0x00557A20`（debug_paper処理）へ進む。
  - 限定機械語の対象は`0x00558C70`（120byte）、`0x00556250`（1344byte）、起動呼出元`0x005554F0`。`search.py function/callers/callees`と両索引の直接CALL site・原作PE生バイトを独立照合。全関数Ghidra再解析やREA再実行は実施しない。
  - *次の関数**：`0x00557A20`（debug_paper値の取込）、`0x00555524`（s以外での呼出到達）、必要時`0x00556250`の端末条件。`ff`単独 / `s` / `f ff` / 10トークン / 11番目ff / `s`10番目のGoldensはDESIGNED / NOT RUN。
- **Original-report limitations/errata:** 以前の「認識フラグ」という総称を訂正：AL=1は少なくともこの原作関数では全オプション共通の成功ではない。ほかの機能フラグの副作用とも区別する。 / `REA_20261027_16H_P0_TOKEN10_FF_RETURN_AUDIT.py`の検査 **59/59 PASS**、失敗0。旧正式Wave1～5 **64/64維持**、新規正式VERIFIED **0**、新規5種完全充足 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。静的59件は関数数ではない。 / PC接続成功、`active.lock`無し、事前空きメモリ約17.11GiB、Java/Ghidra稼働を示すプロセスなし。CPU負荷と研究全体所要時間は不明。監査本体約1.23秒。ゲームGolden/REA/Ghidra新規実行0。拒否・接続障害なし。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261027-17H-P0-DEBUGPAPER-FALLBACK-PRECEDENCE-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_17H_P0_DEBUGPAPER_FALLBACK_STATIC.md`; SHA256 `72A9CC6452C7DD6B0B49334AA93C84F1E631E6790E3C5DE799C6137D898FB551`, 6278 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_17H_P0_DEBUGPAPER_NATIVE_EVIDENCE.json` SHA256 `D23943089161D1BE51BE4DFE6EC0259494AC69E7E1C83D53CB49D82234BB9251`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 検索 `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。両DB read-only/immutable SQLite quick_check PASS。新検索CLIで `function/callers/callees/related 0x00557A20`を限定抽出。
  - Ghidra擬似C code SHA `066E349DF3091B13D84DE06252B92CD5494CCD3F8827F4F8B38E2C30A888E8FF` は機械出力。独立検証は原作PE機械語1500バイト全359命令の限定逆アセンブル。直接CALL `0x00555524 -> 0x00557A20` を原作ASM/2索引で照合。
  - ## 新規発見A：ファイル探索の優先順位
  - `0x00557A9A` は `FindFirstFileA("debug_paper.txt")`。無効handleの場合のみ `0x00557AB0` で `a_system/debug_paper.txt` を検索。ルート側を発見すれば、その読み込みに失敗しても後者を探索し直す経路は確認できない。
  - `0x00557AEE` FindClose、`0x00557B30` CreateFileA（GENERIC_READ=0x80000000、OPEN_EXISTING=3、share=0）、`0x00557B5F` GetFileSize。サイズが1024バイト超なら `0x00557B6F` で0x400に切り詰める。
  - `0x00557B84` ReadFile -> `0x00557B8B` CloseHandle -> `0x00557BBB` 文字列コピー。ReadFile戻り値と実際の読み込みバイト数を明示検査しない局所経路。失敗時の挙動はVERIFY。
  - ## 新規発見B：寸法2値だけを直接変更
  - 処理対象のキーは小文字の `width`（文字列VA 0x00629C60）と `height`（0x00629C68）。`0x00557D98` / `0x00557E77` で `0x005B7576` を呼び、結果を `0x00557DA0 -> [0x0065BEEC]`（幅）、`0x00557E7F -> [0x0065BEF0]`（高さ）に格納。
  - キーが1つでも正常に値変換へ到達するとスタックbyte `[ESP+0x1B]` を1にする（`0x00557DA5` / `0x00557E84`）。終端 `0x00557FD0` でALに返す。見つからず早期終了する経路はAL=0。Ghidra疑似Cの戻り値 `void` は呼出元の使用事実と不整合。
  - 1つ以上の寸法値を認識した場合だけ、`0x00557F21..0x00557F69` で符号付き比較を用いて幅640..1600／高さ480..1200へ補正。1軸しか指定しない場合も両軸の補正候補に入る。
  - 関数 `0x00557A20` の直接グローバル書込先は幅と高さのみ。画面モード `0x0065BEE4`、ff専用フラグ `0x00879821` への直接書込は0。**debug_paper自身がffフラグを直接解除するという仮説は支持されない**。呼出先の副作用や後段DisplayMode経路までは未証明。
  - ## 新規発見C：配布スナップショットの実値
  - 16時台に確認した `f/ff -> AL=0 -> 0x00555524` と結合すると、s未指定の場合に上記寸法設定を読み込む経路がある。ffは専用フラグを立てたままこの関数へ入るが、**後段のDisplayMode分岐で画面幅/高さを上書きし得るため、最終画面が1320×990と断定しない**。
  - ## P0残VERIFYとGolden設計
  - `0x00557C6E` _strpbrk("\\n\\r") の戻り値を直後の `0x00557C7D SUB EAX, ECX` で差分化。NULL検査は局所的に見えない。スナップショット末尾の `switch` 行には行末CRLFがない。stream EOF検査が当該行の処理を回避するか、ヘルパの戻り値規約と合わせてVERIFY。
  - 重要な実装上の注意：debug_paperのALは「実ファイル発見」ではなく「寸法キー値を少なくとも1件処理」のゲート候補。0x005554F0のBL結果と全起動状態は実機未確認。
- **Original-report limitations/errata:** `0x00557C6E` _strpbrk("\\n\\r") の戻り値を直後の `0x00557C7D SUB EAX, ECX` で差分化。NULL検査は局所的に見えない。スナップショット末尾の `switch` 行には行末CRLFがない。stream EOF検査が当該行の処理を回避するか、ヘルパの戻り値規約と合わせてVERIFY。 / 監査 `REA_20261027_17H_P0_DEBUGPAPER_NATIVE_AUDIT.py` **64/64 PASS**、失敗0。64は監査条件数、正式REA 64関数とは無関係。5種類：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規5種完全充足0、新規正式VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0。既存Wave1～5 VERIFIED 64/64を維持。原作Golden PASS0、strict MATCH NOT RUN、完全複製率NOT MEASURED。 / PC Local接続OK、事前active.lock無し、空きメモリ約12.28GiB、対象のJava/Ghidra/Vahrenプロセスをこの照会時は検出せず、CPU負荷不明。監査本体約1.3秒、研究全体の所要時間未測定。新規REA/Ghidra/ゲーム起動0、Work未使用。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261027-18H-P0-DEBUGPAPER-CRLF-EOF-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_18H_P0_DEBUGPAPER_EOL_STATIC.md`; SHA256 `B237282E787915196FBCFA15551985988BEA117B841161D517D735808AF9E546`, 3551 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_18H_P0_DEBUGPAPER_EOL_EVIDENCE.json` SHA256 `FA05F6A20687A8CB088B2F7BE6F2BE76A07448CF80592EC72F40262B6649E346`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 新Ghidra起動なし。検索CLI `function/callers/callees/related 0x00558CF0`、`function 0x00558E68`、`_strpbrk 0x005B83B0`を使用。原作PE機械語で `0x00557A20`、`0x00558CF0`、`0x00558E68`、`0x005B83B0`の対象命令を独立照合。
  - ## 新規確定A：改行のない最終行はパースに入らない
  - `0x00557BFF PUSH 0x0A`→`0x00557C1C CALL 0x00558CF0`（改行で区切るストリーム読込）。`0x00558D93 CMP EAX,-1`→EOFで`0x00558D98 OR [EBP-0x14],1`→`0x00558DA3`から終了ヘルパ`0x00558E68`へ。ヘルパ`0x00558E6B`はNUL終端し、エラー状態を更新する。
  - 呼出元`0x00557C2C TEST AL,1`→`0x00557C2E JNE 0x00557F73`により、EOFに遭遇した読込結果は`_strpbrk`の前に処理を抜ける。後続の2回目の読込`0x00557F02`にも同じbit1ゲート`0x00557F12/14`がある。最終未終端行のテキストはバッファに残り得るが、行として適用されない（static）。
  - ## 新規確定B：配布fixtureはCRLF×5、末尾switch改行なし
  - ## 新規VERIFY：LF-onlyのパーサー到達条件
  - 読込関数は区切り`0x0A`を消費し、バッファへ格納しない。`0x00557C68`でCR/LF集合 `\n\r`を`_strpbrk(0x005B83B0)`へ渡す。`0x005B83DC`は不一致終端でNULLを返す経路。LF-onlyの非空長>2の行では、区切りLFは既に除去されCRもなく、NULL候補に到達する。呼出元`0x00557C7D SUB EAX,ECX`はNULL検査なしで長さを計算し、`0x00557CA4`のstring構築へ渡す。この経路の実際の例外・クラッシュ・設定適用可否は **VERIFY / NOT RUN**。
  - *次優先：** `0x00557C4A`の長さ判定、`0x00402800`のNULL由来サイズに対する境界処理、`0x005555DF`のDisplayMode寸法上書き。LF-onlyとCRLF・最終未終端行のGolden設計はDESIGNED / NOT RUN。
- **Original-report limitations/errata:** 読込関数は区切り`0x0A`を消費し、バッファへ格納しない。`0x00557C68`でCR/LF集合 `\n\r`を`_strpbrk(0x005B83B0)`へ渡す。`0x005B83DC`は不一致終端でNULLを返す経路。LF-onlyの非空長>2の行では、区切りLFは既に除去されCRもなく、NULL候補に到達する。呼出元`0x00557C7D SUB EAX,ECX`はNULL検査なしで長さを計算し、`0x00557CA4`のstring構築へ渡す。この経路の実際の例外・クラッシュ・設定適用可否は **VERIFY / NOT RUN**。 / 独立静的監査 **45/45 PASS**。既存VERIFIED 64維持、新規5種完全証拠0、正式TODO/VERIFY/BLOCKED差分0/0/0。5種：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。原作Golden PASS0、strict MATCH NOT RUN、完全複製率NOT MEASURED。ゲーム・REA・Ghidraの新規起動0、Work未使用。 / CPU負荷不明、作業全体の所要時間未測定、監査本体約2.092秒。開始時active.lockなし/空きRAM約12.1GiB。所有範囲のみ新規ファイルを保存し、MASTER/QUEUE/PROGRESS/旧RUN/他owner/原本/Git/スケジュールは変更しない。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261027-19H-P0-LF-NULL-SIZE-STRING-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_19H_P0_LF_NULL_LENGTH_STATIC.md`; SHA256 `9206D5B0F81F699C5C989FFD2D13159A4BBA4E850770E7A886DCE789066831E4`, 4047 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_19H_P0_LF_NULL_LENGTH_EVIDENCE.json` SHA256 `F4DCBA2035C4E1B75097E0C0A5886CC652620F50CEF7A45BCE918D38731ADF91`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 10/21検索CLI `function/callers/callees/related 0x00402800`、`function 0x00402710,0x00402A40,0x00557A20,0x00558CF0`、`strings/symbols`を使用。擬似CはINDEX_ONLY、確認は原作PEのx86 ASMを対象限定で独立逆アセンブル。
  - ## 新規発見：NULL由来の長さが巨大なunsigned countとして後段へ伝搬
  - 既存18時台：LF-only行の場合、ストリームが区切りLFを消費し、`0x00557C6E CALL 0x005B83B0`（_strpbrk）の返却がNULLとなる候補。
  - *今回の追加**：`0x00557C7D SUB EAX,ECX`は、戻り値NULL=0から行バッファのアドレスECXを32bit減算し、結果を`0x00557C81 PUSH EAX`経由で`0x00557CA4 CALL 0x00402800`へ長さとして渡す。CALLと減算の間にNULLチェック分岐なし。
  - `0x00402800`は文字列代入相当。新規構築された空文字列の初期容量は15。渡された長さをEDIに受け、`0x0040286A CMP EDI,-2`→`0x0040286D JBE 0x00402879`で通常の巨大長（UINT_MAX以外）を通し、`0x0040287C CMP EAX,EDI`から`0x00402887 CALL 0x00402A40`で容量拡張へ進み得る。
  - `0x00402A40`ではサイズを調整して`0x00402ABA CALL 0x005B6C2B`（割当候補）へ進み、失敗側には`0x00402AEE CALL 0x005B864E`（C++例外送出候補）がある。つまり、NULL直後に必ずアクセス違反と断定するより、**不自然に大きなサイズでの割当要求／例外**をまず疑うべき構造。
  - 32bitの純粋な算術例：行バッファアドレス`0x0012F000`なら`0 - addr mod 2^32 = 0xFFED1000`。これは実測されたスタックアドレスではない。長さが`0xFFFFFFFF`と一致する特殊条件や、例外捕捉・heap結果は未検証。
  - `0x00557C4A/5B`には短い行や空行をスキップする条件がある。LF-onlyかつ正常ストリームで長さ>2の行が実際に問題の`_strpbrk`へ到達するか、例外が上位で捕捉されるか、ゲームがどう反応するかはVERIFYであり原作実機未実測。
  - 次の優先は`0x00557C4A`に至る入力行長条件と、`0x00402A40 -> 0x005B6C2B/0x005B864E`の例外伝搬・catch境界。Golden候補：CRLF正常、LF-onlyの長さ2/3/10、末尾改行なし、1024byte上限。全件DESIGNED / NOT RUN。
- **Original-report limitations/errata:** `0x00557C4A/5B`には短い行や空行をスキップする条件がある。LF-onlyかつ正常ストリームで長さ>2の行が実際に問題の`_strpbrk`へ到達するか、例外が上位で捕捉されるか、ゲームがどう反応するかはVERIFYであり原作実機未実測。 / **39/39独立静的監査PASS**。監査条件数と関数数は別。関数別証拠 info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED=0、TODO/VERIFY/BLOCKED正式差分0/0/0、Golden PASS=0、strict MATCH未実施、完全複製率未測定。 / 実ゲーム・新REA・Ghidra・Workは起動せず、原本・他レーン・MASTER/QUEUE/PROGRESS・既存RUN・Git/スケジュールは未変更。保存・独立読戻しの最終結果は別READBACKに記録する。CPU負荷は不明、空きRAM事前約11.7GiB、全作業時間未測定。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0.

### REA-LOCAL-20261027-20H-P0-LF-LENGTH64-NEWH-ABI-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_20H_P0_LF_LENGTH64_NEWH_ABI_STATIC.md`; SHA256 `19AF69EE9A4D071080EEFEDEE8716C2845C2177D86352DDB276D8A2148B006B5`, 4995 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_20H_P0_LF_LENGTH64_NEWH_ABI_EVIDENCE.json` SHA256 `8BBB18E13FBA5E412A7F166D379BF86A6959F8CC9BAFE039840C4A1C4D82BF1F`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。対象：`0x00557A20`, `0x00402A40`, `0x005B6C2B`, `0x005BBA77`。
  - 両DBは `mode=ro&immutable=1` / `PRAGMA query_only=ON` で quick_check=ok。`0x00402ABA -> 0x005B6C2B` のsite照合済み。
  - CLI `function 0x00402A40/0x005B6C2B/0x005B864E/0x005BBA77`, `callees/callers 0x005B6C2B`, `related 0x00402A40 --depth 2`を使用。対象のPE機械語はCapstoneによって独立確認。
  - ## 新規静的結果A：短行ゲートは上位・下位DWORDを順に比較
  - `0x00557A5B XOR EBP,EBP` により比較用EBP=0。
  - `0x00557C4A CMP [ESP+0x30],EBP`、`0x00557C4E JL 0x00557EC8`、`0x00557C54 JG 0x00557C61`。
  - 上位DWORDが0の場合のみ `0x00557C56 CMP [ESP+0x2C],2` → `0x00557C5B JBE 0x00557EC8`。
  - ただし、入力からこれら2DWORDへの全代入経路とゲーム上の影響は未検証。`0x00557C6E`の `_strpbrk` NULL分岐候補は18H、`0x00557C7D`からの巨大長伝搬は19Hの既存発見であり再計上しない。
  - ## 新規静的結果B：mallocラッパーはGhidraのvoid疑似CとABIが異なる
  - 既存擬似Cは`void FUN_005b6c2b(size_t)`と表示。しかし原作命令は `0x005B6C45 CALL 0x005B9BC8`（`_malloc`）→ `0x005B6C4B TEST EAX,EAX` → 非NULL側 `0x005B6C4F LEAVE` / `0x005B6C50 RET`。
  - 成功時、EAXを上書きせず戻るので、**成功ポインタはEAXで呼出元へ返る**。呼出元 `0x00402ABA CALL 0x005B6C2B` → `0x00402AC2 TEST EAX,EAX` がこれを確認する。
  - ## 新規静的結果C：new-handler復旧とbad_allocは別の経路
  - `0x005B6C2B`でmallocがNULLなら`0x005B6C38 CALL 0x005BBA77`（`__callnewh`）。非ゼロで `0x005B6C42`へ戻りmalloc再試行、ゼロなら `0x005B6C51`以降で `std::bad_alloc`を組み立て、`0x005B6CA5 CALL 0x005B864E` でthrowへ進む。
  - `0x005BBA77`内部は `0x005BBA82 CALL [0x006091C0]` (DecodePointer経由)、`0x005BBA8F CALL EAX` (動的new-handler) を含む。callbackの実アドレスと有無は未確定で、間接CALL候補として保留。
  - さらに文字列拡張側 `0x00402AC2 TEST EAX,EAX` → NULL時の `0x00402AEE CALL 0x005B864E` は独立したthrow経路。通常の `0x005B6C2B` 成功復帰は非NULL、失敗復帰はthrowなので、呼出元のNULLフォールバックは防御的経路と解釈できるが、常時到達不能の証明はしない。
  - 次優先は `0x005B9BC8`（CRT malloc自身のnew-handler内部再試行と割当失敗時errno）と `0x00557A20` のSEH catch/unwindの実際の到達・例外処理。Golden案：CRLF/LF-only長さ2・3・10/末尾改行なし/1024byte境界、全件DESIGNED/NOT RUN。
- **Original-report limitations/errata:** ただし、入力からこれら2DWORDへの全代入経路とゲーム上の影響は未検証。`0x00557C6E`の `_strpbrk` NULL分岐候補は18H、`0x00557C7D`からの巨大長伝搬は19Hの既存発見であり再計上しない。 / 限定静的監査 **47/47 PASS**（関数数ではなくassert条件数）。保存済みWave1〜5の**64/64 VERIFIED**を維持、新規正式VERIFIED 0、新規5種完全証拠0。正式TODO/VERIFY/BLOCKED差分0/0/0。 / Windows研究PC接続成功、事前active.lockなし、空き物理RAM約11.58GiB、CPU負荷不明。監査本体約1.17秒、研究全体時間不明。新REA・Ghidra・Vahren実行0、Work使用なし。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261027-21H-P0-CRT-MALLOC-DUAL-NEWH-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_21H_P0_CRT_MALLOC_DUAL_NEWH_STATIC.md`; SHA256 `82254AEA919EBD5D693A513162AF1EB330B161377FA6E8C8DE5FAE524801ED4E`, 4387 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_21H_P0_MALLOC_DUAL_NEWH_EVIDENCE.json` SHA256 `FFFF613E921C4BF5F24C2320EB803D4AFF250C49715E99FA40FEBF7F67CA7E4A`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。重点`0x005B9BC8`、連鎖`0x005B6C2B`、`0x005BBA77`、`0x00402A40`。
  - ## 新規差分A：_malloc内部のサイズ境界と0バイト要求
  - `0x005B9BD1 CMP EBX,-0x20`、`0x005B9BD4 JA 0x005B9C45` は**unsigned**比較。要求サイズ `>0xFFFFFFE0` はHeapAllocを呼ばず、`0x005B9C46 __callnewh` 後 `errno=12`（`0x005B9C51`）とNULL（`0x005B9C57`）へ向かう。handler自体が例外等を送出する可能性は未判定。
  - 要求サイズ0は `0x005B9BF9～0x005B9C04` でHeapAllocの要求が**1バイト**となる。通常サイズはサイズを維持。
  - `0x005B9C0D` はPEインポートテーブル `KERNEL32.dll!HeapAlloc` (IAT `0x00609134`) を呼ぶ間接CALL。Ghidraの候補から独立にIATを確認した。
  - ## 新規差分B：malloc内部と外側に別々のnew-handler再試行
  - HeapAlloc失敗なら `0x005B9C1C` の `DAT_0068E8C0` 非ゼロ時だけ `0x005B9C25 __callnewh` が呼ばれ、戻り値非ゼロで `0x005B9C2D JNE 0x005B9BD8` から再度HeapAllocを試みる。
  - フラグがゼロ、またはhandler戻り値が0なら `0x005B9C38 __errno` と `errno=12`、EAXはNULLで返る。フラグの正確な設定元と実際のhandler登録は要検証。
  - *外側`0x005B6C2B`は、_mallocがNULLを返すと`0x005B6C38 __callnewh`をもう一度呼ぶ。** こちらのhandler戻り値が非ゼロなら`0x005B6C42`から_mallocを再実行。0なら`0x005B6CA5`のbad_alloc throw経路へ進む。
  - `0x005BBA82` はPE IAT `KERNEL32.dll!DecodePointer` (`0x006091C0`) でhandlerを復元し、`0x005BBA8F CALL EAX`（動的実体未特定）。`HeapAlloc`と`DecodePointer`はPE importから直接確認、callback実体を推測で埋めない。
  - 呼出し記録：`0x005B6C45→0x005B9BC8`、`0x005B9C25/0x005B9C46→0x005BBA77`。初期indexとV9の両方でCALL siteを照合。
  - 次回：`0x00557A20`の例外catch/unwind実入口・`0x005B9BC8`中のhandler設定フラグ書込元を個別VERIFY。CRLF/LF-only/末尾改行なし/1024byteはGolden **DESIGNED / NOT RUN**。
- **Original-report limitations/errata:** 正式TODO/VERIFY/BLOCKED差分0/0/0、原作Golden実測0、strict MATCH NOT RUN、完全複製率未測定。静的根拠のみでクラッシュ/永続ループを確定しない。 / PC接続確認、事前active.lockなし、空きRAM約13.46GiB、CPU負荷不明。初回監査約2.035秒、保存時約1.259秒。研究全体の所要時間不明。原作/REA/Ghidra実行なし。Workなし。 / 次回：`0x00557A20`の例外catch/unwind実入口・`0x005B9BC8`中のhandler設定フラグ書込元を個別VERIFY。CRLF/LF-only/末尾改行なし/1024byteはGolden **DESIGNED / NOT RUN**。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261027-22H-P0-DEBUGPAPER-EH-UNWIND-MAP-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_22H_P0_DEBUGPAPER_EH_STATIC.md`; SHA256 `AC8F3450F8576E969BD1092D342D1F6DEE2A96A12FB1B317DD5E1E41307852F8`, 5125 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_22H_P0_DEBUGPAPER_EH_EVIDENCE.json` SHA256 `9B0757FA292175565B1E20D9F5C332488BC448AEBA26E8799BC2FA4FC5670DBA`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。対象 `0x00557A20`、新規重点 `0x005EE240`、そのFuncInfo `0x0064873C`、unwind map `0x0064870C`。
  - Ghidra旧索引は `0x005EE240` をNOT_FOUND、統合V9では `EH_FH3_WRAPPER_005EE240`、body 46 bytes、FuncInfo VA 0x0064873C と認識。今回は未読だったFuncInfo本体とunwind tableを**原作同SHAのPE専用コピーから独立で復元**。GhidraやREAを再起動していない。
  - ## 新規の機械語・FuncInfo根拠
  - `0x00557A20 PUSH -1`、`0x00557A22 PUSH 0x005EE240`、`0x00557A55 MOV FS:[0],EAX` が例外登録。正常出口 `0x00557FDB MOV FS:[0],ECX` で元に戻す。
  - EHラッパー `0x005EE264 MOV EAX,0x0064873C` に続き、`0x005EE269 JMP 0x005B8B1E` でC++ EHフレーム処理へ**末尾JMP**。通常の関数戻りABIや通常のE8 CALLとは区別する。
  - `0x0064873C` の9 DWORD：`19930522, 00000006, 0064870C, 00000000, 00000000, 00000000, 00000000, 00000000, 00000001`。
  - MSVC EH3 FuncInfoの`maxState=6`、`pUnwindMap=0x0064870C`、**`nTryBlocks=0`、`pTryBlockMap=NULL`**。unwind table 6×8=48 bytesは、`0x0064870C`からFuncInfo先頭`0x0064873C`まで丁度連続する。
  - | 0 | -1 | `0x005EE1D0` | 文字列`-0x588`、`JMP 0x004026B0` |
  - | 1 | 0 | `0x005EE1DB` | 文字列`-0x56C`、`JMP 0x004026B0` |
  - | 2 | 1 | `0x005EE1E6` | istringstream`-0x660`、`JMP 0x00428680` |
  - | 3 | 2 | `0x005EE1F1` | 文字列`-0x5A4`、`JMP 0x004026B0` |
  - | 4 | 3 | `0x005EE1FC` | `-0x668 & 1`で文字列`-0x5C0`の片付け |
  - | 5 | 3 | `0x005EE21E` | `-0x668 & 2`で同領域`-0x5C0`の片付け |
  - `0x004026B0` は短文字列容量を0xFへ戻し必要時freeする関数、`0x00428680` はistringstream関連破棄関数と既存擬似Cが整合。全6つのactionを原作PEから逆アセンブル、V9にあるcompiler unwind fragmentとも関係確認。4/5は同じバッファを**別フラグ**で条件付き片付け、直接両方実行するとは限らない。
  - *この関数のC++ EHメタデータにはローカルtry/catchが0件**。LF-only debug_paper の不正な文字列長が実際にbad_alloc等を送出した場合、`0x00557A20`内のC++ catchで回復する経路はこのメタデータからは見つからない。一方、6状態のunwindにより生存オブジェクトを後始末する設計は確認できた。
  - 後続の優先対象：呼出元`0x005554F0`からCRT入口までの例外伝搬・catch境界、`DAT_0068E8C0`の書込元（直接/間接xref）。ゲームGoldenはCRLF/LF-only/最終行改行なし/1024byteをDESIGNED / NOT RUNで保持。
  - 出典：既存`search.py function/callers/callees/related`、V9 `function 0x005EE240/0x005EE1FC`、原作同SHAのPEバイト、同所有内の独立 `REA_20261027_22H_P0_DEBUGPAPER_EH_PROBE.py`・`...EH_AUDIT.py`・`...EH_EVIDENCE.json`。
- **Original-report limitations/errata:** `0x004026B0` は短文字列容量を0xFへ戻し必要時freeする関数、`0x00428680` はistringstream関連破棄関数と既存擬似Cが整合。全6つのactionを原作PEから逆アセンブル、V9にあるcompiler unwind fragmentとも関係確認。4/5は同じバッファを**別フラグ**で条件付き片付け、直接両方実行するとは限らない。 / REA正式Wave1～5 VERIFIED=既存64/64維持、**新規正式VERIFIED=0**、新規5種完全充足=0。info/pseudo/callers/calleesはINDEX_ONLY、assemblyはTARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED差分=0/0/0、ゲームGolden PASS=0、strict MATCH=NOT RUN、完全複製率未測定。 / Windows研究PC接続あり。active.lockなし、空き物理RAM約13.48GiB、CPU負荷不明、研究全体時間不明。新規REA/Ghidra/原作ゲーム実行なし、Workなし。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

### REA-LOCAL-20261027-23H-P0-STARTUP-SEH-CRT-FILTER-SCOPE-STATIC-01

- **PC owner source:** `rea_lab/decomp_task/REA_20261027_23H_P0_STARTUP_SEH_SCOPE_STATIC.md`; SHA256 `DC4AEF00BBA5A9639E5BB0FC83D67107295513B461C151EDA545FACED618FE22`, 4688 bytes, remeasured 2026-11-02 JST.
- **Same-hour evidence candidates (PC only):** `REA_20261027_23H_P0_STARTUP_SEH_SCOPE_EVIDENCE.json` SHA256 `D5512D7DC8605FA5DE0BA215B3B2473CDCEA520C1FB15E980B7A3C6E6B09A9FC`. Check original report for exact provenance.
- **Source evidence (bounded historic native excerpts):**
  - 状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。対象`0x005554F0`→`0x005B84D7`、新重点`0x006412C0`・`0x005B8606`・`0x005B861A`・`0x005BE999`。
  - 22時台には`0x00557A20`のEH3 FuncInfo maxState=6／tryBlocks=0とその後始末6件を確認済み。**今回の新規対象はその上位`0x005554F0`を呼ぶCRT起動側のSEH4スコープ表**であり、過去研究を再計上しない。
  - 検索DBの直接CALL `0x00555524: 0x005554F0→0x00557A20`と`0x005B85EC: 0x005B84D7→0x005554F0`を先に照合。Ghidra機械出力のCRT型識別は初期ヒントとし、以下の値はPE専用コピーから独立確認した。
  - ## 新規証拠A：CRTスタートアップのSEH4スコープ
  - `0x005B84D7 PUSH 0x58`、`0x005B84D9 PUSH 0x006412C0`、`0x005B84DE CALL 0x005BB680`（SEH4プロローグ）を原作機械語で照合。
  - `0x006412C0`の7 DWORD：`FFFFFFFE,00000000,FFFFFF88,00000000,FFFFFFFE,005B8606,005B861A`。
  - `0x005B85EC CALL 0x005554F0`はこのSEHフレームの範囲にある。従ってdebug_paper呼出元より上位に**SEHフィルターが存在する**。
  - フィルター`0x005B8606`では例外情報を取り、`0x005B8612 CALL 0x005BE999`でCRT `__XcptFilter`に渡す。条件付きhandler入口`0x005B861A`では`MOV ESP,[EBP-0x18]`によるスタック復元経路を確認した。
  - ## 新規証拠B：既存Ghidra索引の直接CALL取りこぼし
  - 原作PEの`0x005B8612 CALL 0x005BE999`は**直接CALL**と確認。しかし初期Ghidra索引`calls`と統合V9`native_callsite`の双方で`site_va=0x005B8612`は**0件**。該当CALLを既知47,550件に追加済みと誤認しない。例外funclet周辺の関数範囲/登録漏れが疑われる（原因はVERIFY）。
  - `DAT_0068E8C0`の初期索引参照は、`0x005B9C1C`（malloc）、`0x005C3089`（calloc）、`0x005C3109`（realloc）で**3件ともREAD**。索引上の直接WRITEは0件。ただし間接ポインタ書込や実行時設定まで否定していない。フラグ設定元はVERIFY継続。
  - 次優先：`0x005BE999`のCRT例外テーブルと`0x005BB6E0` SEH4 dispatcherを対象限定で追い、C++ EH codeの一致可否を**静的条件**として解明。原作実機は未実施。対象VA `0x005B8612`のインデックス取りこぼしは自レーン独立STATIC記録として残し、他owner正本への直接変更なし。
- **Original-report limitations/errata:** `DAT_0068E8C0`の初期索引参照は、`0x005B9C1C`（malloc）、`0x005C3089`（calloc）、`0x005C3109`（realloc）で**3件ともREAD**。索引上の直接WRITEは0件。ただし間接ポインタ書込や実行時設定まで否定していない。フラグ設定元はVERIFY継続。 / 5種関数証拠：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED=0、5種新規完全充足=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。既存64件を維持。原作Golden PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。 / PCオンライン、active.lock不在、空き物理RAM約12.69GiB、Java/Ghidra新規起動なし、CPU負荷・全作業所要時間不明。原作ゲーム起動0、Work使用0。
- **Status:** PUBLISHED_INTAKE (GitHub readback required), not CURATED, not an additional function VERIFIED; original Golden PASS 0 / READY 0. Mentioned safety holds remain blocked; refused content and target operations are excluded.

## Integration handoff

Original owner source SHA and research ID are primary recovery keys. Native x86 and current unified V9 outrank old V3 pseudotypes; repeated instruction sites across reports are not new functions. Existing denied VA/Wave6/18H results, raw EXE/SAVE/SQLite, and any private identities not uploaded. All refs/dictionaries/develop remain curator-only. Only reviewed source-backed facts may be formally adopted. No new native test was performed by the recovery.
