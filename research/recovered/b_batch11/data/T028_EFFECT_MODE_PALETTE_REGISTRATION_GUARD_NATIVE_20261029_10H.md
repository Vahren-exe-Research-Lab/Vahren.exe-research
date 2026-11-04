# 新B T028｜effect mode 0..11 palette・runtime field・登録済みガード（2026-10-29 10H）
ID: B-20261029-1016-T028-EFFECT-MODE-MATRIX-ONCE-REGISTER-01
Owner: B / T028。状態: STATIC ORIGINAL-PE ASM + Ghidra V9 PSEUDOC / INFERRED / VERIFY / NOT READY。

## 証拠源・事前照合・安全
- Desktop Commander Local Compact PC ONLINE。MASTER E正式既知checkpoint196/READY596（今回再集計なし）。ANALYSIS_LANES_PROTOCOL、B HANDOFF、B5 owner、復旧記録/共有規約をread-onlyで先読。
- 復旧：旧SAFE134実byte照合/HOLD21旧拒否保留、B147の54件1B差、10/25 14H研究全文未発見を未解決維持。10/28 17H/22H部分コピーや旧安全拒否・禁止VAの再試行/迂回0。
- 従来search_index README.md / BUILD_MANIFEST.json / search.sqliteを読取。V3 DB=53,927,936B、immutable mode=roでSQLite quick_check=ok。標準V3 pointer変更0。
- 別名統合V9 CLIと独立verifyを読取実行：V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。Ghidra全面再解析なし。
- 読取対象はrea_lab/targets/hakushin067_Vahren.exe (2,910,720B)、原作対象実byte SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。PE映像をpefile+Capstone 32bitで静的検査し、原本EXE・DAT・SAVEの起動/改変なし。
- 原作窓0x5AA130 560B SHA256=04CF84CA58D10A86FE495F83B5E274454E6785F64D7E6DC765B8681FE7A9DB55；0x5AA360 table48B SHA256=F90C61BED88DC66BF848B560919588BAFC942D3BF9F3F153D65ADCEE763BB6D9。

## NEW 1｜mode保存と12分岐・範囲外の具体的native
- 0x5AA136 [ESI+0x5C]=255、0x5AA13D [ESI+0x7C]=29、0x5AA144 [ESI+0x78]=EAX(mode)をまず無条件に保存。ESIはeffectサブオブジェクト（09H既知O+0x1E0経路）。
- 0x5AA147 CMP EAX,0xB / 0x5AA14A JA 0x5AA223、範囲内のみ0x5AA150 JMP [EAX*4+0x5AA360]。table 12/12現物DWORD：0→0x5AA157、1→169、2→17D、3→188、4→19A、5→1AB、6→1B3、7→19A、8→1C2、9→1CA、10→1E7、11→206（省略先頭は各0x5AAxxx）。
- mode 0/1/2/3/4または7/5/6または8/9/10/11で選ぶglobal DWORDは順に0x65BC40/44/48/4C/50/54/58/58/40/44。switch tableでmode4==7は同一命令番地、mode6と8は別命令だが同じ元DWORD。
- 各caseはglobal値を0x00FFFFFFでmaskし [ESI+0x60]へ格納。mode9(0x5AA1D7/DE)、10(0x5AA1F6/FD)、11(0x5AA20C/213)だけ追加で [ESI+0x5C]=0、[ESI+0x7C]=200 へ上書き。
- 範囲外 mode（符号なし比較で負数も該当）はcaseの色書込を通らず0x5AA223へ合流。+0x5C/0x7C/0x78初期writerは実行されるが+0x60の従前値はこの関数の当該switchでは保持される。呼出上位が負値をこの関数へ通すかはVERIFY。

## NEW 2｜位置調整と登録済み判定の順序
- 0x5AA223～0x5AA30F は[ESI+0x70]をリンク先として+0x40..+0x4Cの矩形計算・位置更新を行う。更新後の0x5AA312 CMP BYTE [ESI+0x74],0 / 0x5AA316 JNE 0x5AA359で既登録なら追加登録をスキップする。
- +0x74==0のときのみvtable+0x08判定true→0x5AA32F CALL0x4C2240、vtable+0x48判定true→0x5AA346 CALL0x4C3DC0を経由し、0x5AA350 CALL0x4BC920で登録。0x5AA355 MOV BYTE [ESI+0x74],1。3直接CALLは原作native REL32一致。
- よって「登録済み=何もしない」ではない。毎回のmode/+0x5C/+0x7C/+0x60更新と矩形更新は登録guardより前にあり、追加登録だけ省く（処理全体が正常に到達した場合）。登録解除・field reset・合法再入場はVERIFY。

## NEW 3｜共通calleeへの第2直接入口と特殊sentinel
- V9 callers(0x5AA130) は直接E8を2件返す：0x4189CB(09H既知) と **新site 0x49E064**（0x49DF90内）。原作PE相対値を独立復号し2/2一致。新siteでは0x49E045 CMP [ESP+0x2C],0x80000008、非sentinel側0x49E056 virtual+0x64→AL真判定→0x49E060 EAX=[ESP+0x2C]→0x49E064 CALL0x5AA130。
- sentinel側は0x49E06E CMP BYTE [EBP+0x1D],0から分岐し、V9擬似Cでは0または非0によってmode6/5相当の設定処理を**inline**実行する。0x49E064共通calleeには入らない。このinline経路の全副作用が共通関数と等価かは未確認（INFERRED/VERIFY）。
- 独立原作REL32検算は0x5AA32F→0x4C2240、0x5AA346→0x4C3DC0、0x5AA350→0x4BC920、0x4189CB→0x5AA130、0x49E064→0x5AA130、合計5/5一致。0x49E020 96B native window SHA256=C4E4B200AF2EEA5BEF1254EB9C9C61D83BA85D3B18A6DFDA6B20ED5C38869793。

## 既存との差・例外復旧・判定
- 09Hの「mode>=0は0x5AA130、0..11のswitch」という粗い接続は既知で**再計数0**。今回のみの増分はmode毎+0x5C/+0x7C/+0x60・table全12値、範囲外保持、登録+0x74後置gate、2番目の直接caller 0x49E064とsentinelの分岐。B data/T0*.md とB HANDOFFで 0x5AA312/0x5AA147/0x5AA355/0x49E064/0x5AA360 の先行文字列一致0。他owner/10月25日欠落全文の意味dedupはVERIFY。
- OTHER/RECOVERED: PCの初回読取専用Python stdinに日本語絶対pathを渡した際、Windows stdin文字化けで OSError[22] pathに「????」。ファイル書込0、安全拒否ではない。同じ許可Localで作業rootへSet-LocationしASCII相対pathに変更して原本SHA・Capstone/PE照合を完了。
- GOLDEN: 原作無改変EXEかつx20改変前DATの同SAVE/MAP/input/RNGでmode 0,3,4,6,7,8,9,10,11,12/負mode・特殊sentinel、再登録+0x74(0/1)、登録配列件数、色field、矩形前後、次tickと実表示を合法採取。vtable真偽/別caller実到達・型・RNG・士気/敗走の意味はVERIFY、原作Gameplay PASS0、strict MATCH0、新B正式READY0、E MASTER統合0、Task DONE0、NOT READY。
- NEXT: 0x49DF90 sentinel inlineと0x5AA130共通処理のbyte単位差、+0x74のreset writer/登録解除、0x593400候補元、T013最終対象選択・T024戦闘AI・T028士気敗走本体・T011親子EXP・T012ダメージ。既拒否操作/危険VA迂回0、新安全拒否0、原本・MASTER・他lane・REA/dev_lab・Git・Work・設定・schedule更新0。
