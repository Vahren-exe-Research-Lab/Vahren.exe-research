# B-20261025-0810-T013-RESULT-CONSUMER-VEC-CLEANUP-01
Task: T013 (T028 death_event map writer is cross-reference only) / owner B / 2026-10-25 08H JST
判定: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY. Gameplay Golden PASS0; strict MATCH0.

## 前提と保全
Local CompactでMASTER / ANALYSIS_LANES_PROTOCOL / LANE_B_HANDOFF / 5担当資料 / UN-SYNCED復旧索引 / README・BUILD_MANIFESTを先に確認。MASTER checkpoint196・READY596はEの旧確認値（全件再集計なし）。
10/21回収22ファイル・後発10研究、Library訂正版2、10/24オフライン成果のID別完全照合は未完。既拒否0x5710C0..0x571500、0x514C50、0x5769B0 XREF等の拒否操作・証拠へ再試行/迂回なし。
原作PE実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。search.sqlite実SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF (manifest一致)。active.lockのrea_lab以下探索で検出なし。read-only限定Capstoneと既存search.pyのみ使用。

## 増分A: death_event map writer側でhidden insert resultは直接消費されない
前07H ERRATUMのstack位置再利用: 0x49CE07/08 PUSH x2→0x49CE09 LEA EBX,[ESP+18]→0x49CE0D CALL 0x49F7D0(RET8)の出力領域は復帰後[ESP+10] iterator候補と[ESP+14] byte flag。
原作PE命令0x49CE12 MOV EAX,[ESP+44]で、calleeのEAX result ptrは直後に上書き。0x49CE16 XOR EBX,EBX。そこから0x49CEC6 ADD ESP,0x54のepilogueまで実命令を連続decodeした範囲で[ESP+10]と[ESP+14]への直接参照は0。
0x49CE52 MOV ESI,[ESP+18]→0x49CE56 TEST相当CMP/JE→0x49CE5A MOV EDI,[ESP+1C]は別のローカル要素をfreeする分岐。したがって本callerの可視直接CFGでは挿入結果を使った成功/失敗分岐は確認されず、結果返却値をゲームの死亡処理結果コードと混同しない。外部alias、間接副作用、callee例外・re-entryはVERIFY。
この書換writerのキー範囲消去→挿入自体、および05H result layout・07H +10/+14訂正は既知で、新仕様/READYへ再加算しない。

## 増分B: 0x4A60AA callerの直後は「結果判定」でなくESI系vector cleanup
原作ASM 0x4A60AA CALL 0x49F7D0→0x4A60AF CALL 0x4A64A0→0x4A60B4 LEA ECX,[EBP-0xF40]。0x4A64A0の第1命令 MOV EAX,[ESI+4]が先行EAXを上書きし、0x4A64A3 TEST EAX,EAX→0x4A64A5 JE 0x4A64BD。
非NULL branch: 0x4A64A8 MOV EDI,[ESI+8]→0x4A64AB CALL 0x415A60→0x4A64B0 MOV EAX,[ESI+4]→0x4A64B4 CALL 0x5B6BBB。共通側0x4A64BD/C4/CBで[ESI+4,+8,+C]を全0化し0x4A64D2 RET。
従って0x4A64A0はESIを入力とする3-pointer buffer/vector様 cleanupの局所証拠であり、[result+4]のbyte flag評価という証拠ではない。ただしESIの完全な所有者・0x4A60AA branch到達条件、例外動作はVERIFY。
既存Ghidra CLI 'callers 0x4A64A0' は0x60056Cの1件のみ返すが、原作PEに0x4A60AFの直接E8 CALLが存在する。これは当該Ghidra索引の局所的なcoverage gap。PE検証済み参照と索引網羅性を区別する。

## 署名・差分・次回
原作read-only PE窓SHA256: 0x49CE0D+187B = 92D1FAE1C0217E310FF0BEB3AE860DF511DD01EA76DA99492BFEAE8A896B40AD; 0x4A64A0+51B = 3075B8217C7AF264DC6F94EB6E898BB82BF18B86150307128A362DC172B5AAD8; 0x4A60AA+47B = 843DEDFD748BBE84415D457FE838DE6D711EBFBB082234E8CCF272240279B149。
B担当T013/T028/HANDOFF既存では0x4A64A0 / 0x4A60AF一致0、旧0x49CE12は06H既知（新規扱い0）。今回増分はresult direct-consumption不在の全後段照合・別caller vector-only cleanup契約・Ghidra caller gap。全lane意味照合未完。
Golden条件: 無改変原作EXE/20倍強化前DAT/同SAVE/MAP/input/RNG、death_event_a/d両経路・重複キー/nondup/NULL参照・再入・辞書前後と可視効果を同run記録。DESIGNED NOT RUN; DYNAMIC OBSERVED0 / actual Gameplay Golden PASS0 / strict MATCH0。
P0継続: 0x4AE0F0内の残り挿入callerでresult+4のconsumerとESI ownershipを、既存静的B成果とread-only局所ASMで確認。0x49F7D0のalias副作用はVERIFY。新B READY0、E MASTER統合0、Task DONE0。原本/Git/設定/Work/他lane/REA/dev_lab/schedules変更しない。
