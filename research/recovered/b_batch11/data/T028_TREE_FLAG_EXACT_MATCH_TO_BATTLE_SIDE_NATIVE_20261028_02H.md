# B-20261028-0214-T028-TREE-FLAG-F54-F55-01｜T028 参加者索引照合と戦闘モード三状態の旗生成（2026-10-28 02H）
Status: STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY。新規B所有研究・正式READYではない。
## 前提・証拠源
- Desktop Commander Local Compact接続。MASTER最終E正式checkpoint196/READY596は最新確認できた既知値。規約・B HANDOFF・B5所有資料・未同期回収/既拒否索引を先読。2026-10-25 14H未同期全文と他lane意味的完全重複はVERIFYのまま。
- 既存search_index/README.md/BUILD_MANIFEST.json/search.sqliteをread-only確認。active正本はLATEST指定V3（search_current.py）、既存verify_active_research_state_v3_20261022.pyはPASS_ACTIVE_V3_STATIC、14 input hashes verified、errors=[]、gameplay NOT_RUN。java/ghidra稼働無し、active.lock無し。
- 原作rea_lab/targets/hakushin067_Vahren.exe現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。PEの限定ASMをpefile/capstoneで静的確認、EXE実行・再逆コンパイル無し。
## 01H既知のF54/F55三状態分類の「生成条件」を追加解明
- 0x4907A5 MOV EAX,[EBP+0x1EED24]、0x4907AB MOV ECX,[EAX]で一次木の要素へ進み、0x4907CF MOV ESI,[ECX+0x0C]で索引キーを取得。
- 0x4907C0 MOV EDX,[EBP+0x1EED34]、0x4907C6 MOV EAX,[EDX+4]。0x4907D2 CMP [EAX+0x0C],ESI、0x4907D5 JAE 0x4907DCは二次の木をキーで探索する枝。候補をEDXに保持。
- 0x4907F0 CMP EDX,EAX(header)、0x4907F7 CMP ESI,[EDX+0x0C]、0x4907FA JB 0x490802で候補キーが一致しないとheader sentinelへ戻す。探索の比較関係と組み合わせると、ここでexact-key-matchを検査する構造（STATIC/INFERRED）。
- 0x49080A MOV EAX,[EAX]、0x49080C MOV BYTE PTR [ESP+0x74],0、0x490811 CMP EAX,[EBP+0x1EED34]、0x490819 MOV DL,[EAX+0x14]、0x49081C MOV [ESP+0x74],DL。つまり一致ノード未取得時は一時フラグ0、取得時はnode+0x14の1バイトを採用する。
- 0x4909DC CMP BYTE PTR [ESP+0x74],0、0x4909E1 JE 0x4909EF。非0なら0x4909E3でF54（manager+0x1EED54）=1、0なら0x4909EFでF55（+0x1EED55）=1。これは01Hで残った「stackフラグのwriter」を限定的に解決。
- 他枝0x490730はECX+0x10で得る参照先のbyte+0x1Dを判定、非0なら0x490A43 CMP BYTE PTR [ECX+0x14],0、0なら0x4909EF F55、非0なら0x490A4E F54へ進む。これは二次木によるstackフラグ経路とは区別する（直接node flag）。ECXが指すゲーム上の型/陣営名は未確定。
- +0x14をUnitのステータスとは確定しない。木ノードまたは関連レコードのフラグ候補。0x49080Cは[ESP+0x74]の一時セルを0クリアしており、以前置いたポインタを永続ポインタとして使用する意味ではない。
## 既存01H結果への差分と未解明
- F54非0: side refs 1E8630/34、player_battle側。F54=0/F55非0: side refs 1E8634/30、player_battle側。両方0: 1E8634/38、enemy_battle側。参照元とmode表自体は01H既知、再計上0。
- 新規は「一次要素のキー+0x0Cで二次木+0x1EED34を等値探索し、node+0x14をF54/F55の入力にする経路」と「direct +0x14との二経路対比」。01Hの0x490A43は既知で再計上0。
- B5所有316 markdown＋HANDOFFを照合し0x4907C0/0x4907EC/0x49080C/0x490819の先行直接文字列一致0。旧OFFLINE全文/他レーン完全意味的dedupは未完VERIFY。
- 元PE 0x4907C0..0x4909FB（571B）SHA256 D41BA7971596E23E086E606698F8BD8274C086BDB895B71C177005C508B3CD5A。E8 0x4908CF→0x402710、0x4908D7→0x467DE0、原作REL32再計算2/2一致。
- P0残: 二木のオブジェクト型と構築/破棄、direct+0x14がいつ使われるか、F56の実際の役割、T028士気/敗走実計算、T013最終target/T024 AI、合法戦闘の実側表示・結果、RNG・実体同一性をVERIFY。
- Golden必要条件: 無改変原作ver0.67、20倍強化前DAT、同SAVE/MAP/input/RNGにて二木のキー一致/不一致とnode+0x14の0/非0、F54/F55/F56、side参照、mode、戦闘UI/結果を追跡。DESIGNED_NOT_RUN、Gameplay Golden PASS0、strict MATCH0、B新READY0、E MASTER統合0、Task DONE0。
- 既拒否VA 0x5710C0..0x571500、0x58021E..0x580340および既拒否操作には立ち入らず、原本/MASTER/他owner/REA/dev_lab/Git/Work/設定/scheduleを変更しない。
- 復旧メモ B-RC-20261028-0214-V3-CLI-FORMAT-OTHER-01: 初回V3 CLIに旧CLI用 --format markdown を渡し「unrecognized arguments: --format markdown」、読取処理のみで書込0。V3標準の --format無し再実行で正常取得。OTHER/RECOVERED、SAFETY_REFUSALではない。
