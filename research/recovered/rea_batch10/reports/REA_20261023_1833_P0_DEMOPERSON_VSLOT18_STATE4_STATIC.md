# REA-LOCAL-20261023-1833-P0-DEMOPERSON-VSLOT18-STATE4-STATIC-01
日時: 2026-10-23 18時台 JST / owner=REA / P0 T010・T012 / 状態=STATIC・VERIFY・NOT READY（正式MASTER未統合）。
## 既存成果との非重複
- 16時台REA FASTSIM: 0x0040E2F0の500 tick、50 tickごとの検査、戻り値0/1/2は既知。17時台REA BattleWnd secondary vptr: 0x0040E220・BattleWnd+0x28は既知。今回これらは新規計上しない。
- 今回の新規差分は0x40E644/0x40E658のreceiver構築元・具体vptr/vslot実装・戻り値4との比較実体の解決。UI/操作性の変更は0。
## 環境・出典
- Desktop Commander Local Compact接続成功。MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存17時台Markdown/JSON、保存済みsync、V9入口・CLIをread-only確認。
- 承認済み研究コピー rea_lab/targets/hakushin067_Vahren.exe 実バイトSHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- V9: search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite、SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。verifyはV9_INDEPENDENT_READBACK_PASS、functions=11950。PC標準検索CLIは依然V3。
## 新発見1｜BattleWnd+1C8/+1CCはDemoPersonへの2ポインタ
- グローバルBattleWnd主実体=0x008B8C90（既知）につき primary+0x1C8=0x008B8E58、primary+0x1CC=0x008B8E5C。V9 refs-to各14件/11件で照合。
- 0x0040CB90で両ポインタを0へ初期化（既存Ghidra疑似C）。0x0040CCF0は各フィールドがNULLのとき0x188バイトのオブジェクトを確保する経路を持つ。
- 0x40CD5A PUSH 2 → 0x40CD5E CALL 0x447280、0x40CD63 [ESI]=0x638030、0x40CD69 [ESI+0x90]=0x638054、0x40CD7F [0x8B8E58]=ESI。
- 0x40CDB5 PUSH 4 → 0x40CDB9 CALL 0x447280、0x40CDBE [ESI]=0x638030、0x40CDC4 [ESI+0x90]=0x638054、0x40CDD2 [0x8B8E5C]=ESI。
- RTTI COL for 0x638030 = 0x63C618、subobject offset 0、type desc 0x68BD00、name .?AVDemoPerson@@。secondary 0x638054のCOL=0x63C604、offset=0x90、同DemoPerson。両生成経路はNULL/割当成功条件付きであり全実行時を保証しない。
- V9直接caller: 0x0051ED78 (所属0x0051E6F0) → 0x0040CCF0。constructor共有0x00447280は少なくとも0x40CD5Eと0x40CDB9の2 E8 callsiteで確認。
## 新発見2｜両vcall +0x18の実装先は0x005146E0
- DemoPerson primary vtable=0x00638030、slot+0x18=0x00638048の生ポインタは0x005146E0。V9 refs-to/PE HIGHLOWで0x00638048を独立確認。
- 0x005146E0 実ASM 8B 41 20 C3 = MOV EAX,[ECX+0x20]; RET。したがってこの関数は受信オブジェクト+0x20の32bit値を返すstate getter。
- 同じ0x005146E0はEnemy vtable 0x638B60、Person 0x6396E0、Player 0x639B08のslot+0x18にも登録。4種RTTIを原EXEから復元・照合。
- 0x40E639 はECX←[EDI+0x1C8]、0x40E644はFF D2間接CALL、0x40E646はCMP EAX,4。
- 最初の比較が4なら0x40E64BでEDI←[EDI+0x1CC]、0x40E656でECX←EDI、0x40E658でFF D2、0x40E65AでCMP EAX,4。
- 構築済みDemoPersonのvptr不変という条件下では「第一state!=4→return2／第一state==4かつ第二state!=4→return1／双方state==4→return2」。上位の勝敗・時間判定とは別に静的条件として扱う。
- value4は現時点で **オブジェクトの+0x20に格納される状態コード** という意味まで確定。ゲーム上の『勝利/敗北/戦闘可能』等の名前は未確定。以前の『return4の意味不明』を『field+0x20が4』まで限定解決し、意味論はVERIFY。
## 独立検証
- 保存済みGhidra疑似C・V9検索に加え、pefileで原本研究コピーのRVA→ファイル位置変換、structでvtable/RTTI読み出し、Capstone x86でCALL siteとgetterを独立逆アセンブル。
- byte/構造/出典 24/24 PASS：EXE SHA1、RTTI 4、vtable+0x18ポインタ4、命令・field書込等実バイト15。DB validator=V9_INDEPENDENT_READBACK_PASS。
- Ghidra/REAの新起動0、ゲーム実機起動0、Golden原作実測PASS0、新旧strict MATCH0、完全複製率未測定。
- REA公式5種 info/pseudo/assembly/callers/callees の新規完全組0、新規VERIFIED 0。既存Wave1～5 64/64（2026-10-11進捗同期保存値）据置。正式TODO/VERIFY/BLOCKED更新0/0/0。
- 初回Python read-only照合は非ASCIIパスのstdin文字化けでOSError22となり何も変更せず終了。後続はPath.home().globを使った別の独立読取処理で正常検証（安全拒否ではない）。新安全拒否0。
## 制約・次P0
- 関数0x0040E220のBattleWnd secondary +0x04への**実行時virtual CALL site**は依然未解明。今回のDemoPerson vptrとBattleWnd secondary vptrを混同しない。
- 0x005146E0は静的getter先であり、ランタイムのvptr変更・破棄・NULL・状態コード4の意味、結果0/1/2の陣営定義は別途VERIFY。
- 次は0x0051E6F0→0x0040CCF0のライフサイクルとDemoPerson+0x20のwriter/意味、BattleWnd secondary dispatch元をREAD-ONLYで追う。原本、A～E/MASTER/T018、QUEUE/PROGRESS/runs、dev_lab/Work、Git、スケジュールは変更しない。
- PC負荷: 前半瞬間観測空きRAM 15.07GiB/計30.78GiB、Java/Ghidra 0。CPU値と調査全所要時間は未測定。
- [表記補足] 上記「EXE SHA1」はSHA-256出典ハッシュ一致検査を1件実施したという件数表記であり、SHA-1方式を使用したという意味ではない。
