# B-20261028-1515-T028-WANDER-MERCENARY-TEMPLATE-DISPATCH-01｜T028候補処理の放浪／傭兵文面への二経路
Owner B / Task T028。2026-10-28 15H JST。STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY。
## PRECHECK / RECOVERY / 安全境界
Desktop Commander Local CompactでPC接続。MASTER最終正式既知checkpoint196/READY596（本回全件再計数なし）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028各owner、未同期復旧索引とRECOVERY_HUB、旧search README/BUILD_MANIFESTおよびACTIVE V3 LATESTを読取。14H詳細のreadbackとIDを照合。
2026-10-25 14H旧OFFLINE全文と他lane全件意味的dedupは未回収・未同期/VERIFY。既拒否VA0x5710C0..0x571500、0x58021E..0x580340と拒否済み操作の再提出・別tool/shell/path/Remote/ZIP迂回0。Ghidra全体解析・旧原作実行0。
現物原作EXE 2,910,720B SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187をread-only再計算一致。current V3はLATESTが指すSTATIC正本、旧manifestはlegacy。原本・DB・他レーン・MASTER・REA/dev_lab/Git/Work/設定/automationへ書込禁止。
## 新規原作ASM: 上位分岐と二つの結果文面
14Hの0x497C4D candidate+0x74→decide3/500 または decide11/10|25 のproducer、0x497CAF文字列生成は既知で再計上しない。
経路A: 0x49891E CMP DWORD [EDI+0x1EEC3C],EBX(=1) / 0x498924 JNE 0x4989F1。等値枝は0x4989AD MOV EDX,0x63298C→0x4989BA CALL 0x436BC0→0x4989E7 CALL 0x52CF50。原作rdata 0x63298Cに CP932文字列「$$$は放浪しました」。
経路B: 0x498BB1 TEST AL(0x583A80戻値) / 0x498BB3 JE 0x498D5A。成功枝の0x498BC6 CMP DWORD [EDI+0x1EEC3C],EBX / 0x498BCC JNE 0x498C9F。等値枝は0x498C5A MOV EDX,0x6329BC→0x498C67 CALL 0x436BC0→0x498C95 CALL 0x52CF50。原作rdata 0x6329BCに CP932文字列「$$$は傭兵になりました」。
0x4989BA/0x498C67は同じ0x436BC0（文字列テンプレート展開候補）へ入り、どちらも同一の0x52CF50へ到達する。文字列出現とCALL到達はSTATIC、実表示・対象Unitの状態変更・士気／敗走／雇用確定ではない。
## 数値パラメータ経路・型の境界
14Hの[ESP+0x34]へ500/10/25保存の後、0x498952 MOV EAX,[ESP+0x6C]→0x498956 PUSH EAX / 0x498966 CALL0x4051D0、および別枝0x498BFF MOV EAX,[ESP+0x6C]→0x498C03 PUSH EAX / 0x498C13 CALL0x4051D0を原作ASM確認。スタックのpush/subやSSO構築を考慮した実引数同一性はGhidra擬似Cのlocal_e0=local_70とも照合したが、callee引数全境界と用途はINFERRED/VERIFY。
0x4051D0は32B Ghidra擬似Cで文字列初期化と0x402710 CALLを示すのみ。0x436BC0の擬似Cには「$$$」「###」「%%%」「&&&」を走査・置換する分岐があるが、テンプレート二本自体に「%%%」は含まれず、500/25/10を『画面に表示された数値』とは断定しない。
0x52CF50のGhidra擬似Cは0x52AD90→0x402710群→0x43F470等の呼出しを示すが、原作実ゲームのUI通知やオブジェクト更新に何が確定するかは未判明。正式オブジェクト型と処理の時相もVERIFY。
## 機械語検証・非重複
原作PE x86-32限定read-only逆ASM。0x4988EFから253Bの実bytes SHA256=D7E9400C84169ACFF94EDDF632F2CABD8C6CA87438BB983475CBDFCD047623C1。
0x498BB9から225Bの実bytes SHA256=FE22A1FF18BA553269EBBCA956720236DFC9040AAB7355EAB48DC5B5097488BD。
E8 REL32独立照合6/6: 0x4989A6→0x4051D0、0x4989BA→0x436BC0、0x4989E7→0x52CF50、0x498C53→0x4051D0、0x498C67→0x436BC0、0x498C95→0x52CF50。
B担当T011/12/13/24/28 data/exe MD＋HANDOFF計329件で新site・literal6個(0x4989BA/0x498C67/0x63298C/0x6329BC/0x4989E7/0x498C95)直接一致0。他レーン・10/25 OFFLINE完全意味的非重複はVERIFY。14H decide selector、既存0x497BB0の4 NULL caller/非NULL2 caller、T012の旧 decide3 文字列は重複計数0。
## Golden / P0 / 次回再開
無改変原作ver0.67 EXE、20倍改変前DAT、同SAVE/MAP/input/RNG、候補+0x75/+0x77/+0x74/+0x1B0・manager+0x1EEC3C・0x585E00/0x583A80戻値を合法runで分離し、放浪/傭兵の実UI、候補存否、忠誠度・士気、World帰還、再雇用の前後を原作Goldenで比較するまでは DESIGNED_NOT_RUN。
次P0は0x4989BA/0x498C67各上位到達を最小native ASMで確定、0x52CF50の通知消費・候補の実status変更を別途検証。第2赤黒木集合consumer、T028本題士気敗走、T013最終target、T024 AI、T011召喚親ID、T012ダメージRNGも未解明。
原作Gameplay Golden PASS0 / strict MATCH0 / 新正式B READY0 / E MASTER統合0 / Task DONE増加0。今回成果は NOT READY。作業はB所有詳細・T028 owner・B HANDOFFだけに保存、独立readbackと実SHAは別receipt記録。
## RECOVERY
B-RC-20261028-1515-PY-QUOTE-OTHER-01：初回Local PowerShellのpython -c引用符が欠落しSyntaxError: invalid syntax。原本/PC研究ファイル書込0、同じ正規Local環境のcmd python -B -cで純read-only取得に成功。OTHER/RECOVERED、SAFETY_REFUSALではない。
B-RC-20261028-1515-OWNER-NAME-OTHER-02：T013_TARGET_SELECTION.md / T024_BATTLE_AI.mdを仮指定しENOENT。正本T013_AI.md / T024_HAKUSHIN_BATTLE_AI.mdをLocalで読み戻し成功。OTHER/RECOVERED。旧拒否済み操作は一切再試行していない。
