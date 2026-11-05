# E-AUDIT-20261028-0250-T020-T028-INDEXED-FLAG-PROVENANCE-01
[OWNER/DATE/STATE] E owner T020/T018/T019 crosswalk, 2026-10-28 02時台 JST。STATIC / SYNTHETIC EXECUTED / VERIFY / NOT READY。新規正式READY採録0。
[PRECHECK] Desktop Commander Local Compactオンライン。MASTER 4642行のTASK QUEUE/末尾・evidence/ANALYSIS_LANES_PROTOCOL.md・A-D HANDOFF・REA decomp_task/PROGRESS.md・dev_lab/docs/IMPLEMENTATION_PLAN.md・E T018/T019・前回01H E T020およびsearch_index README/BUILD_MANIFESTをread-only参照。重いGhidra/Java/EXE実行無し。
[INPUT B02] B-20261028-0214-T028-TREE-FLAG-F54-F55-01、data/T028_TREE_FLAG_EXACT_MATCH_TO_BATTLE_SIDE_NATIVE_20261028_02H.md、実ファイル SHA256 8BB642AB3A4B9180BF06597DE9F48074B2BD809908DB1393FCC1B51BE717050C（今回Eテストで検算一致）。
[INPUT B01] data/T028_TRIFLAG_SIDE_MODE_PRODUCER_NATIVE_20261028_01H.md SHA256 E2B8A6AC9D364ED314E247885D6B37BA7A1F8DEE22041B577EB1802EE98C5A5A（今回Eテストで検算一致）。
[INPUT B00] data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.md SHA256 D6708901880A1E7C85BE81C542027506546E443EDAF377E5E88577E4BB87AA36（今回Eテストで検算一致）。
[PE PROVENANCE] 元EXE 2026-10-21索引識別SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。B02報告のASM範囲0x4907C0..0x4909FB / PE窓SHA D41BA7971596E23E086E606698F8BD8274C086BDB895B71C177005C508B3CD5A、CALL site 0x4908CF→0x402710/0x4908D7→0x467DE0 のB側REL32 2/2を継承。今回EからPE再実行・再ハッシュ・CALL独立再検証無し。
[NEW DIFFERENCE] 01H三分岐のF54/F55「最終値」モデルとは別に、B02が限定解明したF54/F55の「writer候補」生成経路を区別。一次ノード+0x0Cキー→manager+0x1EED34二次木のexact-key候補、命中時node+0x14の1 byte→[ESP+0x74]一時フラグ、確定不一致なら一時フラグ0、0x4909DCで非0→0x4909E3 F54=1、0→0x4909EF F55=1。
[DIRECT SEPARATION] 0x490A43で参照先byte+0x14を直接判定する別経路と、二次木のnode+0x14はアドレスが同名offsetでも同一レコードである証拠がない。0x490730の+0x1D gate不成立/不明なら直接経路のF54/F55へ決め打ちしない。
[NEGATIVE GATES] 「二次木のexact missが一次証拠で確定」ならscratch=0から局所F55 writer候補。exact判定が不明、木探索未到達、flag byte未取得はVERIFYとし、未観測をmiss扱いしない。flag値はuint8のみ認め、Python boolや範囲外数値を拒否。
[PROVENANCE GUARD] node+0x14をUnitステータス/召喚親ID/陣営名と誤変換しない。stack+0x74は一時セルで永続ポインタとみなさない。B01 F54/F55集約先、B00 config、B23 mode consumerのowner/run同一性は未証明。
[AGGREGATION] 局所F54/F55 writer候補を01H route()の戦闘mode/side slotsへ直接接続しない。その他writerの不在が証明されない限り mode/side = null・VERIFY_AGGREGATE_WRITERS。例外的に「ほかのwriterを排除した合成fixture」に限りside/modeの条件付き算出を許すが、SYNTHETIC_PROJECTION_ONLYでありnative join/Golden PASSではない。
[TEST FILE] tests/t020_t028_tree_flag_aggregation_gate_20261028_02H.py、コードSHA256 5CC38C5D164E8E44436180669C9ADB81678EF6BD2F3047091FEDFD4D146A4854。B02/B01/B00 SHA pin・index hit/miss/unknown・direct gate/flag・bool不正値・2経路provenance・集約未証明・ゲーム実証への誤昇格抑止を26件で検証。
[TEST RESULT] Desktop Commander Local Compact経由 PC python -B を実行：新規26/26 PASS（0.003s）、前回01H 21/21 PASS（0.003s）、合計47/47 PASS、双方exit 0。合成unittestであり原作ゲーム試験ではない。
[T018 GOLDEN G0] 原作無改変ver0.67・20倍強化前DATを使用し、合法旧通常UIから同一runの戦闘開始、Spot・開始操作・画面capture/raw hashを保持する。今回G0はNOT RUN。
[T018 GOLDEN G1] G0と同一run・同一戦闘の直前SAVE実bytesとSHA・正規入力時系列を別receiptで保持、合成の「state snapshot」や手動UI画像で代用しない。今回G1はNOT RUN。
[T018 GOLDEN G2] 実MAPのidentity/SHA・攻防支援三陣営・ordered deployed Unit/Troop・配置とsource/timeを取得。二次木node/key・直接nodeの内部値が合法UIで不可視ならunknown/INELIGIBLEとし、可視陣営からF54を逆算しない。今回G2はNOT RUN。
[T018 G3/G4] 戦闘結果とWorld復帰差分もNOT RUN。同一SAVE/MAP/input条件で新buildから別記録後のみstrict比較可能。ゲームDYNAMIC OBSERVED新規0、actual Golden PASS0、strict MATCH0。
[T019 CHECK] GameClear DAT13/TXT2のsource-scope差はRESOLVED維持。script2同名優先、phase flag、TXT実読込、gwrite復帰はVERIFY。今回の二次木・直接node+0x14は「同じフィールド」と断定できず、確定矛盾/原作BUG新規0。
[T020 IMPLEMENTATION FIELDS] fixture比較列: {source_path, index_lookup_reached, primary_key+0x0C, secondary_lookup_exact, node_flag+0x14, direct_gate+0x1D, direct_flag+0x14, scratch+0x74, local_write_F54_or_F55, other_writer_exclusion, manager_identity, run_epoch, compiled_config, final_F54_F55_F56, selected_side_slots, mode, source_sha, original_UI_receipt}。unknownはnull。生ポインタの同数値だけで同一インスタンス認定しない。
[MASTER TASKS] 本runでMASTER TASK QUEUEの正規T-ID行を独立集計34件/unique34、DONE9/IN_PROGRESS21/VERIFY4。checkpoint196/READY596=A115/B229/C136/D116は最終既知正式値（今回全READY履歴の再計数無し）。今回新規READY統合ID無し、MASTER書込無し。
[UNSYNCED/BLOCKED] B02はSTATIC/VERIFY/NOT READYで代理READY統合不可。2026-10-25 OFFLINE-UNSYNCED旧全文・他owner意味的dedupは未解決。既存のT018表境界・session-join、T019拒否XREF、C T026/T032、D T030 TSV、0x5710C0ほか既拒否はBLOCKED継承。元操作の分割/別tool/path/shell/Remote/ZIP迂回無し。
[RECOVERY/SAFETY] B02のB-RC-20261028-0214-V3-CLI-FORMAT-OTHER-01はB-ownerによるOTHER/RECOVEREDの既記録（E代理変更無し）。本E runの新規接続障害/安全拒否0。原本EXE/DAT/ZIP/SAVE、A-D、REA、dev_lab、Git/push、Work、設定、automationsへの書込0。
[NEXT] 最優先はC-NB02合法G0/G1/G2同run一次証拠。次点はBがキー照合のactual node owner・direct node型と多重writer時の優先/リセットを確証した場合の条件照合。実装のtraceと静的証拠を一対一照合し、異なる原作/合成証拠レベルを混ぜない。

[READBACK RECEIPT] Desktop Commander Local Compact read_multiple_filesで新規PYと本ノートを2/2独立読み戻し成功。PY candidate関数/test26、ノート研究ID/47 PASS/NEXTを確認。PC Get-FileHashでPY=5CC38C5D164E8E44436180669C9ADB81678EF6BD2F3047091FEDFD4D146A4854、本ノート追記前=AEFBA4D4774479F54915644146057E148182295B538C3AC7E7B558058462CB76。本文追記後のSHAは別途取得。新規未保存差分0。
