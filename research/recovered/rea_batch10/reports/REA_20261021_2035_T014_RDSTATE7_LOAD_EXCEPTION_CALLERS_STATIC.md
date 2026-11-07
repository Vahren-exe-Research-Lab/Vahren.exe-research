# REA-20261021-2035-T014-RDSTATE7-LOAD-EXCEPTION-CALLERS-STATIC-01
- 実施: 2026-10-21 20時台 JST。owner=REA独立研究。T014/P0、STATIC / VERIFY / NOT READY。新規REA VERIFIED=0、Golden実測PASS=0、strict MATCH=0。
- source EXE SHA256（既存BUILD_MANIFEST記録）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本EXE現物再hashは行っていない。
- Ghidra12.1.4既存DB search.sqlite（今回Get-FileHash実測）SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。BUILD_MANIFEST一致。新Ghidra/REA実行0。
- 先読: MASTER_LEDGER（直近checkpoint195）、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、保存RUN_RESULT 20261011T153309850Z、sync progress_sync_20261011T153958076Z、REA直前17/18/19時台STATIC資料と既往T014 save IO監査。
- 旧同期によりWave1..5=64/64 VERIFIED（16+10+10+12+16、P0=29/P1=35）。QUEUE/PROGRESSはEPERMで古値。Wave6前回候補0/16・TODO12(P0=2)・SAFETY_BLOCKED4(P0=3)・VERIFY0。正式状態変更なし。
- Local Compact PC接続成功。decomp_task一覧にactive.lockなし。Local sessionsにBlocked=trueの2件あり、他ownerのセッションへ介入せず。CPU使用率・空RAM不明。
## 今回の新規STATIC差分: 固定幅loadの上位検査を単純述語へ正規化
- 保存済みGhidra検索CLI function 0x470700 / 0x470770 / 0x4707D0 / 0x58E480 に同形のstream state検査を独立確認。0x42CC80にも同じ条件式の使用例があるが、本報告の固定幅ロード4例とは区別する。
- 疑似C条件: ((((byte)(state >> 2) | (byte)state) & 1) != 0) || ((state & 6) != 0)。
- 数学的同値: (state & 7) != 0。最初の項はbit2又はbit0、次の項はbit1又はbit2の検査。state上位bitは判定に寄与しない。
- JavaScript uint32モデルで下位16-bit全値65,536＋上位bit境界値14＝65,550照合、全一致/不一致0（合成論理検査、旧ゲームGoldenではない）。下位16bitではfalse=8192、true=57344。
- この検査に失敗すると保存疑似C上はLoadException::vftableを準備し __CxxThrowException_8へ進む。ストリーム内のios_base::failureマスク連動と別階層の、上位loader独自状態検査の候補。
- 0x470700 は site 0x470713→0x42E700、code SHA=873CD6F6F7A5DF2EDE7A631557223DEDB71B3AEA7262FADE79ACA0A9AD86D6C8。成功側でDAT_00B060F0をparam_1へ格納。
- 0x470770 は site 0x47077D→0x42E700、code SHA=6A6004BA86FA14622CDB1F14E9B57FDBD4864AAAE1D5951FE8EE74D904EEFAC9。Ghidraの出力先puStack_cは復元不完全のため書込先確定はしない。
- 0x4707D0 は site 0x4707DD→0x42E700、code SHA=A6F57840EB564D48C00D8757E6CE0CDEB98DE66016C5C5C327BC6E429DF3A45B。同様に出力先puStack_cは不確定。
- 0x58E480 は site 0x58E597→0x42E700(4bytes, 0)、code SHA=90553750D5B72BCA40DB94F594AC6E6B8B570F59289197E2C41E4F8AB0693D94。成功側で読込global DAT_00B060F0→対象param_2+0x7Cに代入、異常状態ならLoadExceptionへ進む。
## 分岐の層と重複回避
- 既知のread sentry 0x42EC60は入口state==0を要求。書込postflush 0x42AA80は (state & 6)==0 を要求する（他のflag/例外条件あり）。今回は上位固定幅loaderの (state & 7)==0 を別の新しい層として追加しただけで、既知2述語を新規成果に二重計上しない。
- 状態0: 4 loaderとも検査通過候補。1(eof)・2(fail)・4(bad)・7(混合): ローダー側では明示LoadException経路（それ以前にstream例外が発生している可能性を除く）。状態8など上位bitのみ: この述語だけなら通過するが、事前sentry/別状態処理の到達性は未確定。
- 0x42E700 block read親のsite 0x42E77F→0x42ECF0、0x42ECF0 site 0x42ED07 virtual+0x20（computed CALL）は既知。該当実vptrがbasic_stringbufなら0x4297D0候補。ただし戻り値EDX:EAXと独立ASMは未検証。今回新しい仮想関数の実装先をVERIFIED認定しない。
- 0x42E700はgcount64bitを更新するが、上位loaderの検査はGhidra上gcount値そのものではなくstream stateである。『取得数が4なら必ず成功』『4未満なら必ずLoadException』は実機未観測につき断定禁止。
- 直前19時台の6 Catch_All継続規則、0x42E7A2の命令種不明、以前のCALL_INDEX_V2特定命令照合 SAFETY_REFUSAL は据置。この回は拒否されたSQL、命令bytes取得、別経路の再試行を実施していない。
- 新規5種REA証拠(info/pseudo/assembly/callers/callees)完全取得0関数。Ghidra DBの保存済みpseudo/参照とREA正式method証拠を混同しない。正式REA Evidence ID=0、新VERIFIED=0、TODO/VERIFY/BLOCKED正式差分=0/0/0。
- Golden NOT RUN条件: 正常な4bytes読込／3bytes+EOF／0bytes+EOF／既にeofbit=1／failbit=2／badbit=4／ios例外mask0と各mask設定を分離。同一old/newデータと合法操作、可視LoadException/戻りstream/gcount/書込先変更を別々に観測。旧ゲームPASS0、新旧strict MATCH0、実装率未測定。
- 次のP0: 0x470700/0x58E480のcalleeと入口readerを既存証拠で比較し、短読込でstateへ立つbitの生産箇所を確定可能か調べる。0x42ECF0のEDX:EAX、0x42E7D4の正常return、例外tableはVERIFY残し、拒否済み0x42E7A2命令bytes照合は再試行しない。
- 保存境界: 新規REA owner Markdownのみ。原本ZIP/EXE/SAVE、MASTER、他レーンA-E、T018、dev_lab、Git、旧runs/evidence、QUEUE/PROGRESS、設定、Work、スケジュールは変更しない。
- PC負荷: CPU実測不明・RAM実測不明。新規Ghidra/REA実行時間0秒。検索CLI数関数のみ、調査全体時間は未計測。
- 保存後のreadback／SHA256はこの段落の後に独立操作で確認する（ファイルを保存しただけで成功扱いしない）。
