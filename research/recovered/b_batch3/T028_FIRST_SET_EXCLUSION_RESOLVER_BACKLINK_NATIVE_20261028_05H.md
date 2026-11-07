# B-20261028-05H-T028-FIRST-SET-EXCLUSION-RESOLVER-BACKLINK-01｜T028 戦闘一時集合の消費側・名前解決副作用（05H）
Status: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。Owner B/T028。E MASTER未統合。
## 証拠・既存成果との差分
- Desktop Commander Local Compact ONLINE。MASTER E最終既知checkpoint196 / READY596。ANALYSIS_LANES_PROTOCOL、B5 Task owner、LANE_B_HANDOFF、復旧・拒否索引、共通ルールを先読。旧10/25 14H OFFLINE研究全文と他owner完全意味重複は未照合（OFFLINE-UNSYNCED/VERIFY）。
- 原作 ver0.67 read-only PE 2,910,720B SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search.sqlite 53,927,936B SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、immutable readonly quick_check=ok。active.lock2候補無し。Ghidra全面再解析・REA・原作起動なし。
- 03H B-20261028-0317-T028-TREEFLAG-DUAL-CONTAINER-GATE-01 は二集合N=0/1/2分岐、04H B-20261028-0410-T028-TEMP-SET-INSERT-ABI-01 は0x498EE0によるuint32赤黒木集合への挿入を既確認。T013の2026-10-24 00Hは0x44D070を別Troop-key重複排除に使用済み。今回の新規増分は **0x493630内の同じ集合への5回の照会/逆向きskip条件** と **名前解決の先行副作用**。既存関数・callの一般的存在を二重計上しない。
- B5所有319 Markdown/HANDOFFで新CALL site 0x494917/0x495015/0x49526C/0x4958A7/0x495A1D、および0x467E30の先行literal一致は各0。0x44D070自体はB T013で既知・非重複計上0。
## 新規原作ASM・Ghidra結合
- 戦闘処理0x493630内部では先に0x493AD1（条件N>=1）で一時整数集合を形成。消費側の0x49490B LEA EBX,[ESP+0x1C]（32bit key）、0x49490F LEA EAX,[ESP+0x3C]（out iterator）、0x494913 LEA ECX,[ESP+0x74]（第1集合）→0x494917 CALL0x44D070、0x49491C MOV EAX,[EAX]、0x49491E CMP EAX,[ESP+0x78]（第1集合header）、0x494922 JNE0x4949E0。**一致キーが存在する場合に当該枝をskip、見つからない場合に後続へ進む負のメンバーシップgate** と静的に読める。
- 同じ first-set照会と「iterator != headerならskip」は 0x495015→0x49501C/20、0x49526C→0x495273/77、0x4958A7→0x4958AE/B2、0x495A1D→0x495A24/28 の4経路でも確認。新規5CALLで同一helperと同一ローカル集合を参照する。実際の対象スコープ、各後続のHP/士気/敗走/勝敗副作用の正式意味はVERIFY。
- 共通0x44D070は原作 x86-32 ASMで ECX=木object、EBX=[key]、EAX=iterator outptr、0x44D083-0x44D097で node+0x0C uint32をunsigned比較して木探索。0x44D0A1-0x44D0C3で等値候補かheaderをoutへ保存。Ghidra擬似Cの曖昧なvoid署名よりnative ABIを優先。関数自体の用途はT013既知で再採番しない。
- 5つのgateの手前にはname/object解決 0x4948F8,0x494FF6,0x49524D,0x495888,0x4959FE CALL0x467DE0 があり、戻り値0なら少なくとも0x494903/905でskip。0x467DE0内部は0x467E1C CALL0x4C1200（名前木探索）→0x467E25 取得nodeとowner+0x300 sentinel比較。hit時0x467E2D ECX=[node+0x28]、**0x467E30 [ECX+0x1A4]=ESI(owner)**、0x467E4D EAX=resolved object。miss時0x467E77 EAX=0。従って名前解決成功時のbacklink副作用は集合の除外判定より先に発生し得る（STATIC）。+0x1A4の厳密な意味/生存期間はVERIFY。
## 原作byte検証・回復
- E8 REL32機械語で第1集合lookup 5/5、名前解決 5/5、解決内部0x467E1C→0x4C1200 1/1、合計 **11/11一致**。0x44D070 /90B SHA256 FF21FFD6CFB210AAD1A2F95CB94B45917E1746A33E702BAA03B447E5379F7144（過去T013にも同値）、0x467DE0 /173B SHA256 C91FD2DBFEDBE0DBB7882B75A3BABE6C8809F323EF9B3442D439465B33B73632、0x493630 /11376B SHA256 20543ED919164316FE4F14B6A90AEAE8165E5A36ADB61A9E852C3CB88218ED11。
- RECOVERY-ID B-RC-20261028-05H-PSEUDOC-PATH-OTHER-01: 既抽出Cの初回read_fileパスにsearch_indexを誤挿入しENOENT。正規のheadless_analysis/full_pseudoc_20261020/functions/0049/00493630.cを確認・read成功。OTHER/RECOVERED。
- RECOVERY-ID B-RC-20261028-05H-PYTHON-QUOTING-OTHER-01: Python -cの初回引用符にSyntaxError、後続のroot raw path末尾\\にもunterminated string literal。修正した同Local環境の明示文字列でPE SHA/DB quick_check/E8 11/11を完了。OTHER/RECOVERED。両失敗時書込なし、新安全拒否なし、未保存差分0。
## P0・受入境界
- 一時集合キーがUnit ID/Team ID/参照など何を表すか、0x467DE0が返す実オブジェクト型と+0x1A4 backlink目的、第1・第2集合の後続実作用、同一managerと実戦到達はVERIFY。T028本来の士気・敗走、T013最終target、T024戦闘AI、T011召喚親EXP、T012 HP/RNGを継続。
- Goldenは無改変原作EXE・20倍強化前DAT、同一SAVE/MAP/入力/RNGで、解決成功/不成功×キー集合内/外・重複×N=0/1/2時、選別後の対象変化と+0x1A4を観測。DESIGNED_NOT_RUN、原作Gameplay PASS0/strict MATCH0。新B正式READY0、E MASTER統合0、Task DONE増加0、NOT READY。
- 安全拒否済VA 0x5710C0..0x571500 /0x58021E..0x580340・既拒否SQL/操作へ再アクセス/経路迂回0。原本EXE/DAT/ZIP/SAVE、他lane、MASTER、REA/dev_lab、Git、Work、設定、スケジュール書込0。
