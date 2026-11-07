# B-20261030-0711-T028-MODE1-POSTRET-BUFFER-RELEASE-01｜退却候補mode1早期分岐の配列バッファ条件付き解放
Owner B / T028 / 2026-10-30 07H JST。STATIC-ORIGINAL-ASM / STATIC-V9 / INFERRED / VERIFY / NOT READY。新規正式READY0。
## 証拠源・既存状態
Desktop Commander Local CompactでMASTER cp196/READY596（E旧正式値）、規約・B5 owner・HANDOFF・復旧索引・V9入口を先読。
原作解析コピー rea_lab/targets/hakushin067_Vahren.exe 2910720B、実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
統合V9 DB 141033472B、実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、SQLite immutable quick_check=ok。原作実行・Ghidra再解析無し。
従来のSAFE134/HOLD21、Library B147中54件の1-byte差、2026-10-25原文未回収はOPEN。旧安全拒否の再試行・別経路迂回なし。
## 今回の新規原作ASM：早期経路でも配列解放に再合流
0x5AC3AC: EDX=[EDI+ECX*4]。0x5AC3AF/+0x77と0x5AC3B5/+0x75が共に0なら0x5AC3B9 JE 0x5AC5E3。ここで既知の0x5AC5E7 CALL 0x598450(mode=1)に移る（05/06H既知、再計上0）。
通常の走査完了時は0x5AC3C4 CMP EDI,EBX / 0x5AC3C6 JE 0x5AC3D1。異なる場合だけ0x5AC3C8 PUSH EDI→0x5AC3C9 CALL 0x5B6BBBを実行。
**新site**: mode1後0x5AC5EC CMP EDI,EBX / 0x5AC5EE JE 0x5AC5F9。異なる場合だけ0x5AC5F0 PUSH EDI→0x5AC5F1 CALL 0x5B6BBB。よってmode1へ早期ジャンプした経路にも同じEDI-vs-EBX条件の解放処理がある（STATIC）。
後続0x5AC5F9で[ESP+0xB4]=4、0x5AC609 CALL 0x510850、0x5AC61B CALL 0x5B6BBB、0x5AC631 JMP 0x5AC5B5。後2callの実オブジェクト型・所有権・例外時到達・終端作用はVERIFY。
0x467DE0の既知0x467E25 sentinel比較と0x467E30 resolved+0x1A4 backlink writer（2026-10-28 05H既存）は今回の候補破棄前に起き得るが、同pointer別名/二重freeの有無は未証明。既知writerを再発見として加算しない。
## 独立PE証拠・非重複
原作PE局所窓SHA256：0x5AC3A0+0x7A=43B013048E6BDE945B84BEFEBBE3EE5124DF98328D829851906F26A68AF2A8DC；0x5AC5E3+0x70=6D421D77C8258538E8567B72C6C24783E877A567FB2780A41B39950010192F35。
B owner Markdown＋HANDOFFの事前literal照合で0x5AC5F0 / 0x5AC5F9 / 0x5AC609 / 0x5AC61B / 0x5AC631各0。0x5AC5ECは既存4件が次回検索先として言及済みで、CALL siteの実解析のみ新規。10/25旧原文・他lane完全意味dedupはVERIFY。
## 再実装/Golden/次のP0
正常走査とmode1早期分岐で同じEDI!=EBXの条件付き解放を持つ点を再実装境界とする。EDI/EBXの割当元、配列長とcleanup後アクセス、0x510850/0x5AC5B5下流は未解明。
原作無改変EXE＋20倍化前DAT、同SAVE/MAP/input/RNGで+0x75/+0x77の0/非0、配列0/1/複数、EDI==EBX/!=、候補resolved NULL/非NULLと退却画面・翌tickの整合を比較。DESIGNED_NOT_RUN。
Original Gameplay Golden PASS0、strict MATCH0、新B正式READY0、E MASTER統合0、Task DONE0。次=0x5AC5B5/0x510850・EDI/EBX producer・T011経験値/召喚・T012ダメージ・T013最終対象選択・T024 AI。
変更許可はこのB詳細、T028 owner、本LANE_B_HANDOFFのみ。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/自動化は変更しない。