# B-20261031-04H-T013-CATEGORY-LABEL-WEIGHT-FANOUT-01｜AI categoryのラベルと乱数重みの非同一性、およびUnit配列へのfan-out
Owner: B/T013（T024連絡候補）｜2026-10-31 04H JST｜STATIC / INFERRED / VERIFY / NOT READY
## 証拠・先行回収
- Desktop Commander Local Compact PC ONLINE。E正本MASTER cp196/READY596（確認済み既存確定値のみ）、解析規約、BのT011/T012/T013/T024/T028 owner、B HANDOFF、2026-10-29復旧監査を読取。03Hの保存・独立readback 3/3を確認。既拒否済み操作を再実行しない。
- 元EXE読取コピー rea_lab/targets/hakushin067_Vahren.exe 2910720B 現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。PE局所 window 0x4495C3..0x4496F2 SHA256=E94D6BC79B299C67E444DDBCDB4B80C6B289279502F17EA1BB44BF5756A8291C。
- V9 search_unified_v9_20261023.py function 0x449500 / callers 0x449500を読取。独自B所有probe=data/T013_CATEGORY_WRITER_LOOP_STATIC_PROBE_20261031_04H.py、PE読み取り専用 pefile+Capstone使用。旧README/BUILD_MANIFEST/search.sqlite不存在は既知OTHERで再試行せず、CURRENT_ACTIVE V9から明示版を選択。
## 新規知見1｜同じラベルでも係数は同一ではない
- 0x4495E3で既定ポインタ0x6357D0（ASCII 'hold'）、0x4495EB/EEでEDX>8(unsigned)なら既定値。0x4495F0は9項目ジャンプテーブル0x449704。実9×DWORDテーブルSHA256=D38E53A02F5435DFDFA275A045BC57B1EA4CB76F51C1A8F1D8D614752255CAD5。
- 原PEの表と文字列を突合: category0→0x6357D8 'hold'、1→0x6357F0 'even'、2→0x6357F8 'even'、3→0x635800 'push'、4/5→既定0x6357D0 'hold'、6→0x6357E0 'advance'、7→0x6357E8 'even'、8→0x635808 'back'。0x6357D0と0x6357D8は異なる位置に同じ'hold'を格納。
- **0x44968E..0x4496A7の係数分岐はEDX==0のみ0.6、EDX==6のみ0.3、その他すべて0.8**。原PE double=0x63B1E8 0.6 /0x63B248 0.3 /0x63B0C8 0.8。従ってcategory0 'hold'は200×0.6=120を加え、**category4/5 'hold'は200×0.8=160を加える**。EDXが9以上または負なら表示文字列は既定'hold'だが数値はother0.8側（当該入力の実到達性は未証明）。
- 旧23Hの9ラベル表と旧00Hのカテゴリ係数そのものは既知で重複計上0。今回の独立増分は**category→labelが多対1なのに、category→係数と一致しない境界4/5/範囲外**のoriginal-PE交差検証。ゲーム上の制御意味・4/5の実到達はVERIFY。
## 新規知見2｜一括Unit更新の数とRNG消費
- 0x44963B/3Eでmanager+0x78..+0x7CのUnit*ベクタ、0x449643 SAR2で長さ、0x449646 EBP=0。0x44964Aは空なら終了。0x449658は Unit*[EBP]を読む。
- Unit+0x1867C=0、+0x1867E=0、+0xC0/+0xD0/+0xC8>=0の**全5条件**を通過した要素だけ0x449688数値演算→0x4496AF CALL0x5D1B80→0x4496B9 CALL0x40ED80（既知内部RNG）→0x4496C4 CALL0x577220（既知Unit+0x1E4FC文字列/+0x1E4F8数値writer）。失格要素は0x449662/6B/74/7D/86から**0x4496D7へ直接skipし、この経路内でRNG/writerを呼ばない**。
- 合格要素は0x4496C9 FLD0.5再投入、0x4496CF EDX category復帰、0x4496D3 EDI manager復帰。0x4496D7..E5で毎回ベクタ長を再計算してEBPを進め、0x4496E5 JA0x449658で繰り返す。**1件だけ選択する関数ではなく、ゲート通過Unitに順次書くfan-out**（calleeによるvector変更や翌tick意味論はVERIFY）。
- V9直接CALL元12 siteは原PEのE8と照合。11 siteは即値category0/1/2/3/6をpush、例0x44B12B PUSH6→0x44B12E CALL、0x44C9A7 PUSH2→0x44C9AA CALL。残り0x44C76C PUSH EBX→0x44C76D PUSH EBP→0x44C76E CALLは入力値producer未特定。**4/5や範囲外が本当に呼ばれるとは断言しない**。
## 既知との差分・安全・Golden
- B data/*.mdの'0x4496E3'正確一致検索0件（今回保存前）。旧23Hラベル/旧00H係数・既知Unit5gate/既知setterは再発見計数0。10/25未回収本文と他lane完全意味dedupはVERIFY。
- 既11H拒否要約3件BLOCKED、SAFE134/HOLD21、Library147中54件バイト差、10/25原文未回収を維持。禁止0x5710C0..0x571500・他既拒否操作は試行0。実Vahren.exe起動/操作なし、Ghidra全体解析なし。
- Golden条件: 無改変旧EXE＋20倍化前DAT、同SAVE/MAP/input/RNGでvector0/1/複数、各5gate単独失格、category0/4/5/8と範囲外の合法な再現、RNG state、全Unit+0x1E4FC/+0x1E4F8の前後、翌tickを比較。DESIGNED_NOT_RUN。原作Gameplay PASS0、strict MATCH0、新B READY0/E MASTER0/DONE0。
- 次: 0x44C76EのEBX category producerと4/5到達性、0x4496C9前後でUnit複数のRNG系列、0x577220後の最終移動/攻撃反映、T011召喚EXP/T012 damage/T024通常AI/T028敗走P0。STATUS STATIC/INFERRED/VERIFY/NOT READY。原本・MASTER・他lane/REA/dev_lab/Git/Work/設定/schedule書込0。
