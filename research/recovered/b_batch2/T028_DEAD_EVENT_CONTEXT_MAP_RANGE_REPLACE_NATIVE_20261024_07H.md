# B-20261024-07H-T028-DEAD-EVENT-CONTEXT-REPLACE-01｜死亡callbackのdead_event_a/d環境設定・辞書range置換
[OWNER/STATUS] 主担当B/T028、B/T013の辞書writerへ横断参照。2026-10-24 07時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / STATIC-DERIVED / VERIFY / NOT READY。実原作Gameplay Golden PASS0、strict MATCH0。
[PRECHECK] Desktop Commander Local Compact PC接続、MASTER cp196/公式READY596（既存記録値）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028各ownerおよび旧拒否・復旧索引先読。22回収ファイル対後発10研究はID対応未決。Library訂正版2・08:10/14:14拒否資料は未解決。
[INDEX] rea_lab/headless_analysis/search_index README/BUILD_MANIFESTを読取し、search.py callers/functionで既存SQLiteを読取専用検索。Ghidra全面解析/REA再実行は0。原作EXEをPE read-only+Capstone限定窓照合、原作起動・改変0。
[HASH] 対象rea_lab/targets/hakushin067_Vahren.exe 現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。
[CALLERS] Ghidra既存indexで0x0049CD60へのE8直接caller計4site：0x00544C5E / 0x00544CA0（fn 0x00544790）、0x00578A91 / 0x00578AD3（fn 0x00578370）。この4siteは原作PE E8命令でも照合。間接/vtableおよび他種類の全参照網羅ではない。
[KEYS] 原作PE .rdata 0x0062A31C,0x0062A32C,0x00627DB4,0x00627DC4はいずれもNUL終端 literal `dead_event_a`、0x0062A33C/0x00627DD4は`dead_event_d`。0x006240C7/0x00623FB7は先頭NULの空文字列。文字列の実バイトをPEから読取照合。
[FIRST PATH] 0x544C00 TEST ESI / 0x544C02 JE：ESI非NULLなら0x544C04でEAX=[ESI+0x1C8]→0x544C0C E8 0x4051D0で28B string-like値をコピー、NULLなら0x544C2B..35で空文字列構築。続いて0x544C46のdead_event_a→0x544C5E E8 writer（ECX=[EBX+0x1E0]）。
[FIRST PATH continued] 0x544C63でEAX=[EBX+0x1C8]→0x544C72 E8 0x4051D0 string-like値をコピー、0x544C80 literal dead_event_d → 0x544CA0 E8 writer（同じ[EBX+0x1E0]）。0x544CC2 E8→0x4321B0 callback入口。
[SECOND PATH] 0x578A28 CMP [ESP+0x38],0 /0x578A31 JE：参照非NULLなら[ref+0x1C8]を0x578A3F E8 0x4051D0でcopy、NULLなら0x578A5E空文字列。0x578A79 literal dead_event_a→0x578A91 E8 writer。次に[EBX+0x1C8]を0x578AA5 copy、0x578AB3 literal dead_event_d→0x578AD3 E8 writer。0x578AF5 E8→0x4321B0 callback。
[CALL ORDER] 以上2経路の局所静的制御フローはdead_event_a更新→dead_event_d更新→0x4321B0。a/dのゲーム内での攻撃者/被害者identityや登録タイミングは未確定で、field+0x1C8を勝手に『名前』と固定しない。
[STRING ABI] 0x4051D0の既存Ghidraはdestination cap+0x14=15/len+0x10=0初期化後0x402710でsource全長copy。0x402670はNUL終端literalから文字列構築。0x49CD60の原作終端0x49CEC9 RET 0x38＝56byteのスタック引数回収（28B string-like値2個と整合）。完全ABIはVERIFY。
[RANGE] 0x49CD60原作ASMは0x49CDB5 E8 0x415530（一時vectorへstring一件append）→0x49CDCB E8 0x49F1F0（同key候補rangeの2 iterator出力）→0x49CDDE E8 0x49EE60（[begin,end)範囲のnode erase）。0x49F370..384では2 iteratorをoutparamへ書込み、0x49EEA4..0x49EF13ではbegin!=endの間0x49EF20でerase。
[INSERT] 同writer 0x49CDF2→0x49F730 pair→0x49CE02→0x49FE30 node→0x49CE0D→0x49F7D0 tree insert。0x49F8D8 E8 0x405370の判定から挿入/duplicate-discardの枝を確認。これらは旧値を単にappendせず、既キー範囲を削除した後の単一値再登録と整合（STATIC-DERIVED）。例外/再入/参照別名の完全意味論と他writerはVERIFY。
[IMPACT] T028の既§2『dead_event_a/d文脈を生成』から進展し、具体的な2箇所のnative writer呼出系列、NULL→空値、値producerと辞書範囲置換を明示。T013の06H既『writer候補関数鎖』を重複採番せず死亡callbackとの実CALL接続だけを増分とする。
[SCOPE/VERIFY] 0x544790と0x578370は別経路。各callerの上流条件/死亡イベント型、a/d参照identity、null時の観測、multi-value古値消滅、script handler内部からの再登録、RNG副作用、全writerの網羅、動的時序はVERIFY。0x4321B0呼出先後半の全挙動も未検証。
[GOLDEN] 同SHAの無改変原作EXE＋20倍強化前DAT/SAVE/MAP/入力/RNGで source参照NULL/非NULL、繰返し死亡callback、a/d上書き前後、複数値既登録、別2経路のイベント入口を観測。before/after辞書snapshotと合法旧新の可視event結果を同一run条件で比較。DESIGNED_NOT_RUN、原作Gameplay PASS0/strict MATCH0。
[DEDUP] 既B/T028§2 callback一般説明、B-20261024-0616-T013-MAP-VECTOR-STRIDE-WRITER-01の0x49CD60内部CALL鎖および02-05Hの文字列getterは既存成果。今回は4 caller sites/値producer/NULL/2key順序/範囲eraseの局所意味論とcallback橋渡しのみ。B owner/HANDOFFで両siteと0x49CD60の既研究を照合。
[PROVENANCE] native 0x49CD60 len0xB5 SHA=43F680CDA838F71D58DA9496253BED6AC9A13728404EEA6D1DACF7AB27C51A53。0x49EE60 len0xB6 SHA=F9FE7DB66CF93DE5105699AEA108422E14D059A5E66F4384A767C96EC5955BAE。
[PROVENANCE] native 0x49F1F0 len0x198 SHA=EF47A756E55A0A785E1E893A6520CA69B426557846358476D2BEE18F3F4DD089。0x49F7D0 len0x15C SHA=B90644BC77EF90EF6DA9F57070DD4CD8C082E782D60B99ECEEE98860557DDB02。
[RECOVERY/OTHER] 今回初回PowerShell here-string内に日本語絶対pathを埋込んだ読取専用Pythonは標準入力エンコーディングで「????」化しOSError errno22（EXE read 0/write 0）。その後sys.argvに認可済み同一正本pathを渡し正常に原作SHA/ASMを取得。安全拒否や接続障害ではない。復旧ID B-RC-20261024-07H-PE-ARG-PATH-OTHER-01。
[SAFETY] 既拒否0x5710C0..0x571500、0x514C50、0x5769B0 XREF/既拒否payload再試行・迂回0。新安全拒否0。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール変更0。
[NEXT] まず原作native 0x544790 / 0x578370入口のdead_event起動条件を既T028§2と差分照合し、0x4051D0コピー元+0x1C8の実オブジェクト型を追跡。0x49F1F0/0x49EE60の同key範囲/再帰的callback中の旧値保存寿命を静的検証。正式READY=0、E MASTER統合=0、Task DONE=0。
