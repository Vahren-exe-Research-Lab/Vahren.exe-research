# T013 Group派生値+0x34の消費・100tick評価・間接ディスパッチ（V3 STATIC）
ID: B-20261023-1618-T013-GROUP-SPACING-CONSUMER-01 / Owner B:T013（T028関連は未確定）
状態: STATIC-GHIDRA / PE-VERIFIED-E8 / INFERRED / VERIFY / NOT READY。原作Gameplay Golden PASS0、strict MATCH0。
一次派生源: PC現行 V3 HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite / search_current.py。verify_active_research_state_v3_20261022.py は PASS_ACTIVE_V3_STATIC、input SHA14/14、E8 44889、JMP 6324、errors=[]。
原EXE識別SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（既存manifest。今回原本実ファイルSHA再計算なし）。
既存先行: B-20261023-1519-T013-GROUP-AGGREGATE-LIFECYCLE-01 に 0x569280 writer・5 caller・Group+0x34集計と breast_width/+0x38 が既存。ここを再発見として計上しない。
今回増分1: 0x00569360 は同一Group候補 param_1+0x0C/+0x10 の構成員vectorを走査し、param_1+0x34（0x569280算出値）を実際に読み取る後段consumer。
今回増分2: 0x00569360 は先頭候補/比較相手に Unit+0x1867C==0 および +0x1867E==0 を要求し、Unit+0xB0/+0xA8/+0x1E530の条件に従って Unit+0x228 または0を使う。生存者集計の0x569280と違い+0x1867Eも除外条件。
今回増分3: 候補対に対し Group+0x34 + 2*Unit+0x228候補 と FUN_0x005E3B70 戻り値候補を比較、条件成立数/評価対象数を定数引数（_DAT_0063B050）と比較する構造。距離/結束判定の可能性は INFERRED、厳密FPU引数・不等号・NaN・0除算枝はVERIFY。
今回増分4: 0x0056AB20 内の PE E8 site 0x0056ADC1 と 0x0056AE85 はどちらも 0x00569360 を呼ぶ（V3 PE relative target検証済、E8 bytes e89ae5ffff / e8d6e4ffff）。CALLの一方の条件はGroup+0x44。返値が続く移動/目標経路の分岐に使われる。
今回増分5: 0x0056AB20 は Group+0x3Cを増分後、%100==0 の条件付きブロックから2 CALLを評価する。外側の +0x1C と engine+0x1EF148 の条件があるので100tick無条件実行とはいえない。
今回増分6: 0x0056AB20 のE8直接callerは0件。DATA xref 0x00639A34→0x0056AB20 が1件、PE .rdata HIGHLOW relocationも同スロット1件。vtable/関数ポインタ経由の入口候補だが実際のクラス・呼び出し時機は VERIFY。
関連: 0x0056AB20 の別枝は 0x00569730 へ E8 0x0056AB97/0x0056AC99/0x0056ACDA/0x0056AE77/0x0056B0A2 を持つ。0x00569730 はgroup構成員を調べ 0x005699C0・0x0047BB50（sort）・0x005769B0 につながるが実際の命令/移動効果は未確証。
分類: 統計に見える Group+0x34 を『士気』とは確定しない。ペア状態/距離・隊列維持候補としてT013/T028の境界に保留。CALLとDATA pointerは別物。
Golden案: same original EXE・無改造DAT・SAVE・MAP・入力・乱数初期状態。構成員0/1/3、生死1867C・別状態1867E、Group+44=0/1、tick99/100/101、breast_width分岐とunit+228境界、命令変更/配置位置/移動を時系列取得。DESIGNED NOT RUN。
未解明P0: 0x00639A34 vtable所属および外側indirect dispatch; 0x00569360のfloat比較/比率ABI; 0x00569730の実副作用; Group+0x34他consumer; T024 AIとT028逃走・士気との接続。
次回再開: 0x00639A30周囲のRTTI・vtable（読取のみ）で 0x56AB20 の所有クラスを確定→0x56AB20 +0x44 writer とparam1+0x34・unit+0x228の型を照合。拒否済み0x5710C0..0x571500/0x514C50/14:14保存等へ非介入。
既存未同期: 03～12時台オフライン研究10件、02時台Library訂正版2件はPC未同期。14:14の詳細文書は安全拒否・未保存のまま。最新MASTER統合はEのみ、最終既確認cp196/READY596。
禁止: 原EXE/DAT/SAVE・MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール非変更。原作実行、Ghidra再抽出、REA重複起動なし。
