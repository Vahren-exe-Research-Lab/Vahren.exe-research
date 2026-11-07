# REA-LOCAL-20261023-23H-P0-BATTLEWND-DEMO-FIELD-IDENTITY-STATIC-01
- 日時: 2026-10-23 23時台 JST / owner=REA / T010・T012 P0 / **PC-SAVED-PENDING-READBACK, STATIC, VERIFY, NOT READY**。原作ゲームNOT RUN。
- 出典: 承認済み研究コピー rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回PE実バイト再計算）。
- 検索基盤: 統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、verify=V9_INDEPENDENT_READBACK_PASS、11950関数・243678参照。PC標準ポインタはV3のまま。
- 先行非重複: REA_20261023_1638 / 17H / 18H / 20H / 21H / 22H の生成・vtable・500-tick解析を保持。22Hで未解明だった+0x1C8/+0x1CCの具体的な静的生成・参照一致、および実slot+0x0C初期化接続だけを新規差分とする。
## 新規静的証拠：BattleWndの実体に対する2ポインタのアドレス一致
- 保存済BattleWnd固定実体の基準アドレス 0x008B8C90（既報17Hの主・副vptrと整合）に対し、0x008B8E58-0x008B8C90=+0x1C8、0x008B8E5C-0x008B8C90=+0x1CC（整数差独立計算）。
- 0x0040CB90: +0x1C8/+0x1CCの固定アドレスに対し0x40CCE0/0x40CCE5でゼロ初期化。0x0051DF94からE8直接CALL（V9 callers）。
- 0x0040CCF0: 0x40CD22で[0x8B8E58]がNULLか、0x40CD85で[0x8B8E5C]がNULLかを各別判定。NULL時のみ0x188バイトを確保し、0x447280を引数2/4で呼んだ後、DemoPerson主vptr=0x638030、副vptr(+0x90)=0x638054を設定。保存 site 0x40CD7F → 0x8B8E58、0x40CDD2 → 0x8B8E5C。生成失敗/既存非NULL時はこの新規確保経路を通らない。0x0051ED78からE8直接CALL（V9 callers）。
- 0x0040E2F0の既知の[EDI+0x1C8]/[EDI+0x1CC]、0x0040E42E/0x0040E445のvirtual slot+0x04と固定global2ポインタは、**EDIが0x8B8C90を指す場合**アドレスが厳密に一致。実行時のEDI/型/置換・全経路固定は未証明。
## 新規静的証拠：初期化・状態フラグへのvtable接続
- 0x0040D0A0→0x40D0C6 E8 CALL 0x0040F320。0x40F320は0x40F39D/0x40F3AFで各globalをECXに取り、主vtable+0x04を0x40F3AD/0x40F3BAのFF D0で呼ぶ。DemoPerson主vtable実バイト: 0x638034→0x5149C0、0x638038→0x514A80、0x63803C→0x447810。
- 同じ0x40F320後段の0x4103B6/0x4103D7が各globalをECXに取る。0x4103D5/0x4103E2のFF D0は主vtable+0x0Cを呼ぶ。DemoPersonであれば**両方0x00447810**（先行21Hの+0xA5 RTTI判定）へ到達する。主vtable+0x08の間接CALLも0x40F3D6/0x40F3F*周辺に存在し、意味・引数を別途検証。
- その後の静的設計上の候補連結: global初期化(0x40CB90)→条件付きDemoPerson生成(0x40CCF0)→主vfunc段階(0x40F320)→副vfunc状態更新(0x40E42E/0x40E445)。**複数関数の同一実行時順序、通常ゲームでの実到達、割当失敗時挙動は未証明**。
## 検証・進捗・安全
- PE32 RVA→rawをpefileで読み、機械語18アドレス、vtable4ポインタ、E8相対CALL3箇所をCapstone/structとは独立に実バイト比較、合計**25/25 PASS**（原本SHA一致）。期待値・実値は別JSONに機械可読保存。V9 Ghidra疑似Cとの照合は静的参照のみでABI未認定。
- 既存REA Wave1〜5はlogs/progress_sync_20261011T153958076Z.jsonの保存済み64/64（各Wave=16+10+10+12+16）、queueUpdate=STALE_RENAME_DENIED。今回新規正式5種類(info/pseudo/assembly/callers/callees)完全セット0、正式VERIFIED+0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- 旧ゲームGolden実測PASS0、strict MATCH0、完全複製率未測定。設計済み比較条件は元global一致/相違、片側NULL/双方既存、+0xA5条件、vptr置換、+0x288正/非正などで全NOT RUN。
- preflight観測: active.lockなし・Java/Ghidraプロセス0、空きRAM約9.85GiB、CPUロード66%（瞬間値）。高負荷かつ版差・Wave6拒否既存のためREA/Ghidra新規起動0、研究コピーはread-only。全調査所要時間未計測。
- 今回のPC書込はREA所有の新規固有名レポート/独立証拠に限定。原本ZIP/EXE/SAVE、他A～E/MASTER/T018、QUEUE/PROGRESS、既存RUN/Evidence、dev_lab/Work、Git/push/公開、スケジュール無変更。既拒否VA 0x5710C0..0x571500・Wave6四VA・抽出操作は不実行。
- 次P0: 0x0040F320内+0x08の正確な仮想CALLと引数を調べ、0x00410420および0x0040F320等からの同global代入/寿命変更の有無を実ASMで分離する。0x40D0A0→0x40F320/0x40D220の制御と、0x40E220から0x40E2F0のthis補正を動的時系列だと誤認しない。
- 保存/readback: 本MDとJSONの保存後に別操作で独立読み戻し・ハッシュ検査を実施して結果を別途報告する。