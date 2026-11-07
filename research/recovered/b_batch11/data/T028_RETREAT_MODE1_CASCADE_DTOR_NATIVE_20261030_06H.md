# B-20261030-0615-T028-MODE1-CASCADE-DTOR-01｜退却候補mode1の二段階破棄とゼロ要素例外経路
Owner B / T028（士気・敗走）/ 2026-10-30 06H JST。STATIC-ORIGINAL-ASM / STATIC-V9-PSEUDOC / INFERRED / VERIFY / NOT READY。正式READY0。
## 出典・既存成果への依存
- Desktop Commander Local Compact ONLINE。MASTER E最終公式cp196/READY596（旧値）、ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF、RECOVERY_HUBを先読。旧SAFE134/HOLD21、Library54件1B差、2026-10-25未回収原文はOPENで同期成功としない。
- 原作解析コピー rea_lab/targets/hakushin067_Vahren.exe は2910720B、今回実測SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本非実行・非編集、pefile/Capstoneによる局所ASM。
- 統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite 実測SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable SQLite quick_check=ok。旧search.sqlite不在とDEFAULT V3不変更は既知OTHER。
## 新しい原作ASM静的接続：mode1でregistry cleanupとオブジェクト破棄が走る
- 05H既知0x5AC3B9 JE 0x5AC5E3の合法CFG枝から0x5AC5E3 PUSH1 / 0x5AC5E5 PUSH EDX / 0x5AC5E6 PUSH EBP → 0x5AC5E7 CALL0x598450(mode1)。この到達辺・CALL site自体は今回再計上しない。
- 原PE 0x598455 MOV EBP,[ESP+0x28]が第2引数を保持、0x59845A MOV ESI,[ESP+0x28]が第1引数を保持（スタック深さ変化後）。すなわち下記 final EBX=EBP は第2引数/候補object、ownerは第1引数由来とSTATICで追える。Ghidra署名・実クラスはABI未確定。
- 既00Hのmode差に新しい下流の破棄を接続：0x5984DFのmode非0分岐のみ、0x598543 CALL0x467DE0を実行し、0x598548 TEST EAX,EAX / 0x59854A JE 0x59855E。**EAX!=0の時**0x59854C owner=[EDI+0xB0]、0x598552 PUSH owner、**新site 0x598553 MOV EBX,EAX → 0x598555 CALL0x463590**。NULL戻りではこの要素の0x463590をskip。
- 0x59855Aで処理後にEBXをローカル+0x10のループindexから再取得。0x463590によるEBXの破壊/ポインタ解放と次要素indexを混同しない。vector幅0x1C、各要素のrange eraseは旧01Hで確認済み・重複計上0。
- loop終了後 **0x598591 CMP mode,0 / 0x598596 JE0x5985AA**。mode1では **新site 0x5985A2 PUSH [owner(param1)+0xB0] / 0x5985A3 MOV EBX,EBP(第2引数) → 0x5985A5 CALL0x463590**。つまりresolvされた各EAX候補とは別に、第2引数object自体にも共通cleanupが実行される。0x5985A5自体は既00Hで既知、今回の増分は第2引数ポインタの原ASM追跡と要素ごとの経路との結合。
- **vector0要素でも**旧01H 0x5984A8 JE0x598591により最終cleanupへ進み、mode1なら第2引数への0x463590が走る。mode0なら0x598596 JE0x5985AAでdeep cleanupはskipするが、旧01Hの共通tree eraseは継続。例外・不正ポインタによる非正常終了は別途VERIFY。
## 既知calleeとの接続（重複再計上0）
- 10/28 12H既知 0x463590 はowner+0x2FCの0x49F410→0x4BF820 erase、owner+0x330/0x32Cを使う0x460F10経路を持つ。0x4635E9 TEST EBXが非0なら0x4635EE CALL0x4591F0（内部資源destructor様）、続けて0x4635F4 CALL0x5B6BBB（当該ポインタ解放）。したがってmode1での0x463590は通知のみではなく索引更新・破棄経路を含む。
- 旧0x497C21→0x463590のNULL候補cleanup、旧00H/01Hのvector range erase、旧05H mode1枝、既存0x463590/0x460F10本体を新規発見数へ加えない。
## 独立証跡・非重複
- native窓SHA256: 0x598539+37B=0B56E4873314BDC2D3F83BD14116FA52E98470AA0DE1A9D4D31CABAD3400CEC5、0x598591+33B=E185C5D13F6F5D81785BB153ABC19DEF1DA5AC26B6345ACACD08ED17EF87FB5B、0x4635E9+17B=3EF80F3DFA63DD8BC448BD0E4E45E688822DA135D5C2C676AAE80FFEB70993C7。
- B所有T011/T012/T013/T024/T028のdata/exe Markdown＋HANDOFF376ファイル、**新site 0x598553、0x5985A3、0x5985A2、0x59855A は既存literal各0**。0x5985A5既存2、callee 0x4635EE/0x460F10既知。10/25欠落全文・他lane完全意味的重複はVERIFY。
## 再実装・Golden・次のP0
- mode1を単なる追加索引削除で代替すると、各resolved候補と第2引数の別々の資源解放・vector空時の破棄・owner二索引清掃を失う可能性。元の実クラス/所有権、同一ポインタ重複/二重解放防御、+0x1A4 side effect、後続Unit/Spot状態はVERIFY。
- GOLDEN DESIGNED_NOT_RUN：無改変旧EXE・20倍改変前DAT/同一SAVE/MAP/input/RNG、mode0/1×vector0/1/2×0x467DE0 NULL/nonNULL、owner索引2FC/32C/330・候補/第2引数生存・+0xB8・通知・翌tickを原作合法実測。Gameplay PASS0 / strict MATCH0 / 新B READY0 / E MASTER統合0 / Task DONE0。
- 次=0x467DE0のowner+0x1A4戻り副作用、0x463590で第2引数とvector候補が同一になる条件、mode1後0x5AC5ECのcleanup、Unit+0x75/+0x77設定元、T011/T012/T013/T024のP0。既拒否0x5710C0..0x571500等は再試行しない。
- 今回新SAFETY_REFUSAL0/接続障害0、元拒否操作迂回0。MASTER/他lane/REA/dev_lab/Git/原本EXE/DAT/SAVE/ZIP/Work/設定/スケジュール不変更。
