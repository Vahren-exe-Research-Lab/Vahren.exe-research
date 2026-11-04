# T028｜退却Spot index eraseのキー比較入口とノード破棄・長さ境界（02H）
研究ID: B-20261030-0215-T028-SPOT-TREE-ERASE-STRING-RELEASE-01
時刻: 2026-10-30 02時台 JST｜owner B / T028｜STATIC ORIGINAL ASM + V9 PSEUDOC / INFERRED / VERIFY / NOT READY

## Precheck・証拠源
Desktop Commander Local Compact ONLINE。MASTER cp196/旧READY596、evidence/ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、T011/T012/T013/T024/T028 owner資料、B未同期/安全拒否索引をread-only先読。
原作解析コピー rea_lab/targets/hakushin067_Vahren.exe の現物実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。実ゲーム・原本は不実行/不変更。
標準旧README.md / BUILD_MANIFEST.json は ENOENT（OTHER、既知の整理移動であり安全拒否でない）。V9 00_START_HERE / INTEGRITY を参照し別名V9 CLIとreadonly immutable DBのみ使用。V9実SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、PRAGMA quick_check=ok。
旧SAFE134/HOLD21、Library B147中54件1byte差、10/25原文未回収・他owner/未回収文書の意味重複はOPEN。既拒否操作の再試行/迂回0、新安全拒否0。

## NEW 原作ASM：検索キーは文字列長とSSO容量で分岐
既01H 0x416080のequal_range様・0x402C40比較関数は既知。今回新しく実PEで 0x4160F4、0x416150、0x4161D9 の3サイトが 0x402C40を直接CALLすることを確認。
0x4160D5 mov esi,[edi+0x1C] はnode文字列byte長、0x4160E4 mov ebx,[edi+0x20] は容量、0x4160E7 cmp ebx,0x10 / jb 0x4160F1 でheapとinline bytesを分岐。比較用EAXは2長のmin候補（0x4160DE..E4）で、ECX/EDXが両byte列、比較後0x416101/105..10Aはprefix一致時に長さ比較で大小を解く。0x416143/148/150 と 0x4161CC/1D0/1D9 の他2箇所も容量0x10分岐後の比較。
比較callee 0x402C40の原作ASM (0x402C41 input length EAX→ESI、0x402C50..62 4byte一致反復、0x402C68..A3 先頭異なるbyteを符号比較、0x402CA3 sar eax,31 / 0x402CA7 or eax,1、全一致0x402CAD xor eax,eax) は2026-10-24 B T013 CASE8研究で既知。比較演算自体を新規再計上せず、今回の新増分は退却Spot treeへの3呼出位置とnode/長さの接続のみ。入力文字列の実ゲーム名・同名重複・encoding正規化はVERIFY。

## NEW 原作ASM：RB-tree eraseでstring buffer・node・sizeを更新
0x416220冒頭の 0x416224 cmp byte ptr [eax+0x29],0 / 0x416228 je 0x416234 は無効iterator時に 0x41622F CALL 0x5B5BBA（invalid map/set<T> iterator）へ分岐。呼出条件の合法性はVERIFY。
0x41646A cmp dword ptr [ebp+0x20],0x10 / 0x41646E jb 0x41647C：capacity>=16なら 0x416470 mov eax,[ebp+0xC] → 0x416474 CALL0x5B6BBB で文字列のheap bufferを解放。capacity<16ならこの独立freeをskip。
共通末尾 0x41647C [ebp+0x20]=0xF、0x416483 [ebp+0x1C]=0、0x41648B [ebp+0xC]=0 → 0x41648F CALL0x5B6BBB はnode本体の解放経路。0x4164A2 test eax,eax、非零のみ0x4164A6 dec eax / 0x4164A7 [ecx+8]=eax でtree countを1減算、ゼロなら減算しない。
0x415CF0のfull-tree clear→0x416870とpartial-node erase→0x416220は01H既知。今回新規はpartial nodeの文字列バッファ容量境界・解放順・container count条件と検索キーtype結合。full clear側の同じallocator副作用/例外耐性は別証拠待ち。
元PE窓SHA256：0x402C40/113B=0B59C8A69F290BA8624117E2FAD0F33EF176F82CBE2CC3E4907502302BB6D77C（既T013と同値）；0x4160C0/349B=B0F2FDA122144ECE659EF9FD358751A0BCDDD85B7EDC8E24243B1C1C8CE7FFA9；0x416220/657B=FE6C11D887F0260C5A7D71AC4F90D2A1BC6B3422285472EA656152A8DA3C0DB5。

## ID・回復・Golden・次回
B担当T011/T012/T013/T024/T028のtop-level Markdown371件＋HANDOFF1件をreadonly scanし、新native 0x416474 / 0x41648F / 0x4164A6 / 0x4160F4 / 0x4161D9 は先行literal0。0x402CA3は旧T013 CASE8とHANDOFFに既存、二重計数0。旧欠落原文/他lane全意味dedupはVERIFY。
初回Python -c のPowerShell引用符ミスは SyntaxError（OTHER/RECOVERED、書込0）。正常なread-only python/pefile/capstoneとV9 CLIで局所検証成功。新Ghidra/REA重複実行無し。
実機Golden要件：無改変旧EXE + 強化前DAT、同一SAVE/MAP/input/RNGでretreat vector長0/1/2、tree空/一致/多重、key byte長15/16/17・prefix・非ASCII、mode0/1合法到達を別々に比較し、消去前後index count/pointer/Spot+0xB8・翌tick・可視動作を観測。DESIGNED_NOT_RUN / original Gameplay PASS0 / strict MATCH0。
新規B READY0、E MASTER統合0、Task DONE0、STATIC/INFERRED/VERIFY/NOT READY。次は 0x416870 full-clear destruct順、0x495580後のUnit+0x1B4寿命、0x597A50 linked+0x78意味、T011召喚/経験値・T012 damage・T013対象選択・T024 AI P0。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/automation不変更。
