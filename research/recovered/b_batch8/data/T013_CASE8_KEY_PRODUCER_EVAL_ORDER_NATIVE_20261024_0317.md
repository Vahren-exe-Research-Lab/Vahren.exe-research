# B-20261024-0317-T013-CASE8-KEY-PRODUCER-ORDER-01｜case8の検索キー生成元とモード棄却前の式評価
[TASK] B/T013主、T011/T024関連は参照のみ。2026-10-24 03:17 JST。STATIC-ORIGINAL-PE-ASM＋V3-STATIC-GHIDRA／INFERRED／VERIFY／NOT READY。
[PRECHECK] Local Compact接続。MASTER最終正式checkpoint196/READY596（前回正式値）、レーン規約、B HANDOFF、5 owner資料、既拒否/未同期索引を先読。2026-10-21の19+Library3=22ファイル回収は既存記録。03～12時オフライン10研究とのID別対応未確定、後発Library訂正版2・08:10/14:14拒否本文は別保留。
[INDEX] 現行V3 verify_active_research_state_v3_20261022.py 実行＝PASS_ACTIVE_V3_STATIC、入力SHA14/14、E8 CALL44889、JMP6324、errors=[]、gameplay NOT_RUN。旧search.sqlite非正本。Ghidra/REA全面再起動なし。
[EXE] 原作rea_lab/targets/hakushin067_Vahren.exeの実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（当回Python実バイトhash一致）。原作実行・書込なし。
[NEW-1 CALL/PRODUCER] case8の0x004B5957 mov ecx,[eax]→0x004B5959 lea eax,[ebp-0x34]→0x004B595C push eax→0x004B595D push ebx→0x004B595E E8 call 0x0049C450。これは候補検索キー用の文字列をローカル[EBP-0x34]へ作成する入口。正確な式object型/ABIはVERIFY。
[NEW-2 SOURCE BRANCH] 0x0049C450 Ghidra pseudoCと実ASM: 0x0049C496 cmp [ebx+0x14],0、0x0049C499 JEで直接field+4文字列採用経路。非zeroの場合0x004261B0→0x0042F860の判定結果により直接field+4へ戻る経路、または0x0049C52E→0x0049ECA0で式参照解決へ進む経路がある。処理経路と文字列生成はSTATIC、ゲーム内入力名/型はVERIFY。
[NEW-3 EMPTY FALLBACK] 式参照解決では0x0049C55Bで戻ったノードをheader相当+0x1E8640と比較し、等しい場合または0x0049C56Aでnode+0x28/+0x2Cが同じ場合、0x0049C563で0x0068B3A8を選ぶ。原作PE 0x68B3A8は文字列長0・容量15相当のゼロ初期化構造。その他はnode+0x28の候補先頭値を選ぶ。0x0049C589→0x00402710が結果stringを出力する候補。
[NEW-4 SSO/DELIVERY] 0x004B5987 cmp [ebp-0x20],0x10、0x004B598B mov edx,[ebp-0x34]／0x004B5990 lea edx,[ebp-0x34]の選択は、結果string capacity>=16でheap、<16でinlineをEDXへ渡す局所SSO。続く0x004B5993 push 1・0x004B5995 mov ecx,ebx・0x004B5997 E8→0x0049E8B0で候補Unit検索へ。
[NEW-5 TREE JOIN] 0x0049E954～0x0049E962でEDX文字列のNUL終端長を計算、0x0049E966→0x00402800でlocal stringへ複製、0x0049E975でcontext+0x1EEBECを指定して0x0049E980→0x0049F410の範囲検索へ到達。前回の0x49F410辞書式比較規則は再計上しない。NUL埋込・encoding・前段正規化はVERIFY。
[NEW-6 ORDER] モード式0x004B5976→0x0049CCA0とsigned>2棄却0x004B597E/81の前に、キーproducer 0x004B595E→0x0049C450が実行される。mode>=3でも局所フローではキー生成処理が先に走り、候補tree検索/0x569530設定には進まない。式評価側の副作用・例外発火はVERIFY。棄却条件/0x49CCA0自体は既23時研究、今回再採番0。
[DEDUP] B owner T013_*.md 51点＋LANE_B_HANDOFFの計52文書をキーワード0x49C450/0x4B595E/0x49C52E/0x4B5987で読取検索。既01:10文書に0x4B5987のみあり、今回の追加は0x49C450 producer内部枝・空結果・入力→検索文字列データフロー・mode棄却前順序。既01:10 tree列挙/02:17 byte comparatorは再計上0。他lane全件の意味重複は未監査。
[WINDOW SHA256] PE VA0x49C450 len0x161: 98F4BFFBDD3B39B0DC0419BB629790B9478453F6B97E240142E4F2628D7CB981。
[WINDOW SHA256] PE VA0x4B594E len0x50: 6514A922E22766F9906695144993DAAD9B16640C1639A1C6D1C1FF3AA7E80B3B。
[WINDOW SHA256] PE VA0x49E954 len0x46: DD1EE30C1968E3F640D5FAD6EC0048EC3CA134430E8BAE83A511DCA1EEB5AE21。
[VERIFY] 0x49C450の式object/engine context ABI、0x49ECA0のnode型・empty sentinel語義、非ASCII/embedded NUL、正規化、実case8 DAT構文、mode3等の例外/副作用、同キー順・実戦配置、RNGは未解明。
[GOLDEN] 無改変原作EXE＋X20改変前DAT、同一SAVE/MAP/入力/RNGで文字列式直値/参照値/空値・15/16文字ではなくbyte長・mode2/3・共有Troopの採用順、可視命令と例外有無を対照：DESIGNED/NOT RUN。原作Gameplay PASS0/strict MATCH0。
[SAFETY] 旧拒否0x5710C0..0x571500／0x514C50／0x5769B0 XREF／T024旧検索・既拒否文書は再試行/迂回0。元EXE/DAT/SAVE/ZIP・他lane/REA/dev_lab/MASTER/Git/Work/設定/scheduleに書込なし。
[RESULT/NEXT] B新READY0、E MASTER統合0、Task DONE0、NOT READY。次は許可済み既資料から0x49ECA0の戻値node構造と0x49C450に渡る式オブジェクトの発生条件を追跡。原作実戦Goldenは0。
