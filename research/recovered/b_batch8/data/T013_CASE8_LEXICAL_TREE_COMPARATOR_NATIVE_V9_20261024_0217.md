# B-20261024-0217-T013-CASE8-LEXICAL-TREE-ORDER-01｜case8の文字列キー比較とtree iterator境界
[TASK] Owner B / T013、T011/T024参照。2026-10-24 02時台 JST。STATIC-ORIGINAL-PE-ASM + V9-STATIC-GHIDRA / STATIC-DERIVED / VERIFY / NOT READY。
[PRECHECK] MASTER checkpoint196/既正式READY596、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、B担当5資料、旧OFFLINE回収台帳と安全拒否境界をLocal Compactで先読。22ファイル原文一致回収を既知、後発10研究のID別重複照合とLibrary訂正版2・14:14拒否研究本文は未完了。
[INDEX] search_index旧search.sqliteは過去版。PC標準V3不変更。独立V9 CLIを明示使用しverify=V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、functions=11950、native callsites=51214。ゲーム実行・Ghidra/REA再解析なし。
[ORIGINAL] 原作ver0.67 exe rea_lab/targets/hakushin067_Vahren.exeのGet-FileHash SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、一致。読み取り専用のCapstone局所逆アセンブルを実施。
[NEW-KEY] 0x49E8B0の既知0x49E980→0x49F410は入力文字列をローカルstring相当へ複製してtree rangeを検索する。今回0x49F410では、検索キー+0x10のbyte長とnode+0x1Cのbyte長を参照し、先頭からmin(長さ)byteを比較、共通prefix同値時は長さで大小を決める経路を原作ASMから確認。キーのゲーム内名称は未確定。
[NEW-NATIVE-CALLS] 0x49F484、0x49F4E0、0x49F569のE8_DIRECT_CALL 3箇所が0x402C40へ。V9 CLI outgoing_calls_total=3および原作PE局所ASMで3/3照合。既01:10の『比較キー・語義VERIFY』とは独立した増分。
[NEW-COMPARE-ABI] 0x402C40原作ASM: 0x402C41 mov esi,eax (比較するbyte数)、0x402C50 [edx]と0x402C52 [ecx]の4byte比較、0x402C68以降のbyteごとのmovzx/sub、0x402CA3 sar eax,31 / 0x402CA7 or eax,1。全byte同値なら0x402CAD xor eax,eax→ret。局所的に EAX=length, ECX/EDX=byteptr入力、結果は符号付き -1/0/+1であり、Ghidra __fastcall 2引数形式を完成ABIとして流用しない。
[NEW-SSO] 0x49F45C/0x49F461および0x49F477/0x49F47Aはcap >= 0x10でheap pointer、cap < 0x10でinline bytesを選ぶ。0x49F484までにeax=min(検索keyLen,nodeLen)・ECX=key bytes・EDX=node bytesを設定する。0x402C40自体にはcasefold・日本語正規化分岐が見えない（byte比較）。
[BOUNDARY] treeの文字列比較はunsigned byte列の辞書式・prefix短い方優先に整合する。ただし同一キー内のUnit参照並び、キー生成/encoding/大文字小文字の上位正規化、node+0x28の最終Unit identity、複数mapの順序はVERIFY。『全Unitが名前順』とは主張しない。
[EXISTING-CROSSJOIN] 01:10の0x49E8B0 alive filter +1867C、tree successor、global vector 0xB050E0と00:15のUnit+0x1D0 visited-Troop dedupは既知として再計数0。今回の差分はtree比較の実byte・戻り値・SSO境界と3 call siteのみ。
[PE WINDOW SHA256] 0x402C40 len0x71=0B59C8A69F290BA8624117E2FAD0F33EF176F82CBE2CC3E4907502302BB6D77C。
[PE WINDOW SHA256] 0x49F450 len0x140=40A742F4DE9E20ADBA97C49B55A32E2AA4B3FBD91256DF5FC26F8A7E02F43CE6。
[PE WINDOW SHA256] 0x49E950 len0x80=084C4171BF6435AC3C3AF319733127B449FDC96B859B22C6178D70D81C53A3D5。
[GOLDEN] 無改変旧原作EXE＋空手x20適用前DAT＋同SAVE/MAP/input/RNGを用意し、キー同値/長さ15・16・17/共通prefix/大小文字/非ASCII byte・alive/dead・同一Troopを別々に試験。比較キー/候補Unit列挙/実Troop mode適用を観測。設計のみNOT RUN、原作Gameplay PASS0、strict MATCH0。
[SAFE/READY] 既拒否0x5710C0..0x571500、0x514C50、0x5769B0 XREF、旧T024、14:14拒否本文の再実行・別経路迂回なし。新安全拒否0（本記録作成前）。新規B READY0、E MASTER統合0、Task DONE増加0。原本/他lane/REA/dev_lab/Git/設定/schedules不変更。
[NEXT] 0x49E8B0の入力文字列producer（case8のEDX）と0x49F410の範囲端点・同名key複数nodeの対処を、拒否されていない既存B/静的出典で次に絞る。0x402C40を無関係の旧拒否XREF追跡の口実にしない。
