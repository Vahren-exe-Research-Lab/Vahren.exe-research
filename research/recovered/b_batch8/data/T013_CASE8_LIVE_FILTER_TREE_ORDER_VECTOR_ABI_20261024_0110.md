# B-20261024-0110-T013-CASE8-LIVE-TREE-VECTOR-01｜case8候補Unit抽出・列挙順・戻値ABI
[TASK/STATE] B:T013（T011/T024参照）/ 2026-10-24 01時台 JST / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。
[PRECHECK] Desktop Commander Local CompactでMASTER cp196/既正式READY596、レーン規約、B HANDOFF・T011/T012/T013/T024/T028正本、未同期・拒否索引を先読。既B-20261023-2317とB-20261024-0015を再計数しない。
[BASELINE] 現行V3 validatorを今回実行: PASS_ACTIVE_V3_STATIC、input SHA 14/14、E8 44889、JMP 6324、errors[]、gameplay NOT_RUN。原作EXE現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。
[NEW CASE8 CALL] 0x4B5987～0x4B5997: 大文字列heap判定後EDXへ文字列参照を置き、0x4B5993 `push 1`; 0x4B5995 `mov ecx,ebx`; 0x4B5997 E8→0x49E8B0。したがってこのcase8 callerは0x49E8B0のstack boolに1を明示。
[NEW NATIVE FILTER] 0x49E9C0 `cmp byte ptr [ebp+8],0`、0x49E9CB `je 0x49E9DA`、0x49E9CD `cmp byte ptr [edi+0x1867C],0`、0x49E9D4 `jne 0x49EAC5`。上記push1との合成でcase8候補列挙はUnit+0x1867C!=0の参照を格納せず次tree nodeへ進む。+0x1867C=0をalive候補とするのは既B先行証拠。
[NEW TREE RANGE] 0x49E96B～0x49E980: `ecx=engine+0x1EEBEC`に対し`0x49F410`を呼び、文字列キーからtree iterator2端を取得。0x49F410 Ghidraはtree node+0x1Cの比較と0x402C40 comparatorを含む。キー比較の意味・厳密なABIはVERIFY。
[NEW TREE ITER] 0x49E9C4 `mov edi,[ebx+0x28]`でtree nodeからUnit参照候補を取り、0x49EAC5～0x49EB0Dではnodeの子/親/番兵+0x2Dに従ってin-order successorを計算して次へ。元挿入順ではなく検索したtree rangeのiterator順に収集するSTATIC-ASM。
[NEW VECTOR ABI] 0x49E8F6～0x49E914の一回限り初期化はグローバルvector descriptor 0x00B050E0/0x00B050E4/0x00B050E8、0x49E91C～0x49E939でend=beginへ論理リセット。0x49EA31/0x49EA94の0x501A40呼出は必要容量確保の候補。
[NEW RETURN] 0x49EB13 `mov eax,0x00B050E0`、0x49EB35 `ret 4`。0x4B599C `mov edi,eax`、0x4B59B5/0x4B59B7で[edi]/[edi+4]を読みUnit pointer列として処理。Ghidra `void __fastcall FUN_0049e8b0` は戻値について誤復元、EAXがvector descriptor addressを返すことを原作ASMで確認。
[CROSSJOIN] 先行00:15のvisited-setはUnit+0x1D0 pointer候補をkeyとし一度のみ0x569530へmode値を渡す。今回のcase8ではalive filtered tree range順がvisited-set適用順の入力。treeキー/recordの式・複数Troopの実副作用/RNGはVERIFY。
[LIMIT] 全検索経路・登録キー/文字列からUnitまでの厳密対応、node+0x28構造体名、global vectorの再入可能性、同戦闘内の実順序、+0x1867C状態のゲーム内実値と呼出規約全体は未確定。例外・allocatorの動的副作用もVERIFY。
[NATIVE SOURCE SHA] 原作PE bounded VA0x4B5957 len0xDD SHA256=4D38429E4ADC259DD5BC53AED6CE486037D4B59C5425DC8FF8980A222E712A62。
[NATIVE SOURCE SHA2] VA0x49E8B0 len0x120 SHA256=AD3BBB5F4AEAA3E1FE355C6BF0415851A682CC65EC3A3A9B8BC5D4E722B20E6A。
[NATIVE SOURCE SHA3] VA0x49E9C0 len0x181 SHA256=4711B075D02FB001A233D01BF6C6C057D8426C243F3EFC8D6BE219CB6936630A。原作実バイトCapstone静的逆アセンブル・対象関数は既存V3 Ghidra cached pseudoC。
[RECOVERY STATE] 2026-10-21 B-RC-20261021-17H-OFFLINE-SYNC-19-01とB-RC-20261021-17H-LIBRARY-02-RECOVERY-01により過去22ファイルはPC保存/原文readback済の記録がある。最近の『03～12時台10件未同期』記載は一括状態として再照合要、回収22と二重計数しない。08:10拒否本文・後日のLibrary訂正版2件・14:14拒否詳細は引き続き別BLOCKED/VERIFY。
[GOLDEN DESIGN] 無改変原作EXEと改変前DAT（2026-10-22 X20テストDAT混入を排除）、同SAVE/MAP/操作/RNGでalive/dead mixed、shared Troop+0x1D0、キー列挙順・複数Troopと同Troop重複、連続case8によるglobal vector再利用、命令配送・戦闘UIを比較。DESIGNED NOT RUN、原作Gameplay PASS0、strict MATCH0。
[BOUNDARY] 0x5710C0..0x571500 / 0x514C50 / 0x5769B0 XREF・既拒否書込payloadへ再試行・別経路迂回0。原作ゲーム起動/改変0、MASTER/他lane/REA/dev_lab/Git/Work/設定/scheduleの書込0。
[RESULT] 新B正式READY0、E MASTER統合0、Task DONE0。次はcase8のEDX文字列producer・0x49F410 node比較キー/0x402C40語義・+0x1D0 pointer型・global scratchの再入寿命を許可済み静的資料で照合。
