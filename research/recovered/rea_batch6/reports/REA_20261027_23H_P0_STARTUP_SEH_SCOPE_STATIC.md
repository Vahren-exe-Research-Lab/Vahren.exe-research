# REA 2026-10-27 23時台｜P0・CRT起動SEH4フィルターと検索DBから漏れた直接CALL
研究ID：`REA-LOCAL-20261027-23H-P0-STARTUP-SEH-CRT-FILTER-SCOPE-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。対象`0x005554F0`→`0x005B84D7`、新重点`0x006412C0`・`0x005B8606`・`0x005B861A`・`0x005BE999`。
EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、初期DB SHA `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
## 既存成果との差分
22時台には`0x00557A20`のEH3 FuncInfo maxState=6／tryBlocks=0とその後始末6件を確認済み。**今回の新規対象はその上位`0x005554F0`を呼ぶCRT起動側のSEH4スコープ表**であり、過去研究を再計上しない。
検索DBの直接CALL `0x00555524: 0x005554F0→0x00557A20`と`0x005B85EC: 0x005B84D7→0x005554F0`を先に照合。Ghidra機械出力のCRT型識別は初期ヒントとし、以下の値はPE専用コピーから独立確認した。
## 新規証拠A：CRTスタートアップのSEH4スコープ
- `0x005B84D7 PUSH 0x58`、`0x005B84D9 PUSH 0x006412C0`、`0x005B84DE CALL 0x005BB680`（SEH4プロローグ）を原作機械語で照合。
- `0x006412C0`の7 DWORD：`FFFFFFFE,00000000,FFFFFF88,00000000,FFFFFFFE,005B8606,005B861A`。
- 先頭4語はSEH4 cookieオフセット情報。残り3語はscope（enclosing=-2、**filter VA=0x005B8606、handler VA=0x005B861A**）として構造的に整合。
- `0x005B85EC CALL 0x005554F0`はこのSEHフレームの範囲にある。従ってdebug_paper呼出元より上位に**SEHフィルターが存在する**。
- フィルター`0x005B8606`では例外情報を取り、`0x005B8612 CALL 0x005BE999`でCRT `__XcptFilter`に渡す。条件付きhandler入口`0x005B861A`では`MOV ESP,[EBP-0x18]`によるスタック復元経路を確認した。
## 新規証拠B：既存Ghidra索引の直接CALL取りこぼし
原作PEの`0x005B8612 CALL 0x005BE999`は**直接CALL**と確認。しかし初期Ghidra索引`calls`と統合V9`native_callsite`の双方で`site_va=0x005B8612`は**0件**。該当CALLを既知47,550件に追加済みと誤認しない。例外funclet周辺の関数範囲/登録漏れが疑われる（原因はVERIFY）。
`__XcptFilter`の疑似Cでは、スレッド別の例外処理表から一致する例外番号と登録処理を探し、一致・登録がない場合0を返す構造。**任意のC++例外を確実にcatchするとは言えない**。特にLF-only debug_paperが`bad_alloc`に至ること、その例外を起動SEHが受けること、クラッシュはいずれも未実測。
## new-modeフラグ直接xrefの補助監査
`DAT_0068E8C0`の初期索引参照は、`0x005B9C1C`（malloc）、`0x005C3089`（calloc）、`0x005C3109`（realloc）で**3件ともREAD**。索引上の直接WRITEは0件。ただし間接ポインタ書込や実行時設定まで否定していない。フラグ設定元はVERIFY継続。
## 監査、制約と再開位置
read-only PE32/native限定監査：**27/27 PASS**、失敗0、初回成功1.263秒、保存時1.407秒。SHA3件一致、旧新DB両方`quick_check=ok`、最終sync `64/64`と22H証拠`47/47`を独立確認した。
5種関数証拠：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED=0、5種新規完全充足=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。既存64件を維持。原作Golden PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。
PCオンライン、active.lock不在、空き物理RAM約12.69GiB、Java/Ghidra新規起動なし、CPU負荷・全作業所要時間不明。原作ゲーム起動0、Work使用0。
小障害：対話PowerShellの一行Pythonにアンパサンドの引用符エラー（OTHER）発生。独立保存スクリプトへ移行。初回監査では調査用ASMバイト範囲が狭く`0x005B862A`を含まずKeyError（OTHER）、監査用範囲を修正して27/27 PASS。**安全拒否・接続切断ではない**。
保存先はREA所有`rea_lab/decomp_task`内の新規probe/audit/evidence/report/readbackのみ。MASTER、A～E、QUEUE/PROGRESS、既存runs、原本、Git、公開先、スケジュールは一切変更しない。
次優先：`0x005BE999`のCRT例外テーブルと`0x005BB6E0` SEH4 dispatcherを対象限定で追い、C++ EH codeの一致可否を**静的条件**として解明。原作実機は未実施。対象VA `0x005B8612`のインデックス取りこぼしは自レーン独立STATIC記録として残し、他owner正本への直接変更なし。
