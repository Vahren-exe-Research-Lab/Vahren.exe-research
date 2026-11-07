# B-20261025-05H-T013-INSERT-RESULT-ABI-01｜map挿入のiterator/inserted返却契約
Owner B / T013（T028死亡callback辞書writerへの参考）。2026-10-25 05時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA-V3 / STATIC-DERIVED / VERIFY / NOT READY。
## 事前照合・証拠源
Desktop Commander Local Compact接続。MASTER最新正式cp196/READY596はE既存値（全件再集計無し）。解析規約/B HANDOFF/T011・T012・T013・T024・T028既存資料/未同期・拒否索引を先読。10/21回収22件・後発10件・Library訂正版2と10/24日中OFFLINE研究の全件ID照合未完。
CURRENT_ACTIVE_RESEARCH_STATE_LATESTはV3 canonicalを指す。read-only verifier=PASS_ACTIVE_V3_STATIC、input SHA14/14、E8 CALL44889、JMP6324、errors=[]、gameplay NOT_RUN。旧search.sqliteではなくsearch_current.pyのV3を使用。原本EXE実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、原本をPEとしてread-only参照し実行・変更なし。
## 新たに確認した戻値ABIと明示分岐
0x0049F7D0のV3擬似Cはvoid+unaff_EBXだが、原作native全3復帰枝ではEBXがout-result構造体ポインタとして使われる。挿入側0x49F8B2 MOV [EBX],EAX・0x49F8B4 MOV byte [EBX+4],1・0x49F8B8 MOV EAX,EBX・0x49F8BE RET 8。
別の挿入側0x49F8FD MOV [EBX],ECX・0x49F8FF MOV byte [EBX+4],1・0x49F903 MOV EAX,EBX・0x49F909 RET 8。両枝とも最終iterator候補+inserted=1を返す。
非挿入側0x49F90C..0x49F91Cでは0x49CED0・0x5B6BBBを呼び候補node/heap処理後、0x49F91F MOV [EBX],EDI・0x49F923 MOV byte [EBX+4],0・0x49F927 MOV EAX,EBX・0x49F92D RET 8。既存node iterator候補+inserted=0で戻る枝をnative確認。calleeの全例外時動作はVERIFY。
0x49F8D2 LEA EDX,[EDI+0x0C]（既存候補key）、0x49F8D5 LEA EAX,[EBP+0x0C]（新key）→0x49F8D8 CALL 0x405370→0x49F8DD TEST AL /0x49F8DF JE 0x49F90C。0x405370は前方bytes比較0x402C40と長さ比較によるstrict-less候補を返す。挿入位置検索後、既存keyが新keyより小さくないと判断する枝で既存node・flag0へ進む（等値判定の厳密前提は木不変条件を要する）。
caller 0x49CE07 PUSH EAX（0x49FE30生成node候補）、0x49CE08 PUSH ESI、0x49CE09 LEA EBX,[ESP+0x18]、0x49CE0D CALL 0x49F7D0：少なくともこの呼出ではEBXがcaller上のresultバッファを指す。戻値EAX=EBX・RET 8はGhidraのvoid署名を修正すべきABI証拠。ただしこのcallerがresult flagを後続で実際に参照するかはVERIFY。
## 先行成果との差分と解釈限界
既B-20261024-0616-T013-MAP-VECTOR-STRIDE-WRITER-01はwriter CALL鎖・insert候補のみ、B-20261024-07H-T028-DEAD-EVENT-CONTEXT-REPLACE-01はmap既key範囲erase→insert・duplicate-discard候補を既に記録。本研究はそのbranchを再発見として数えず、native挿入結果の「iterator + byte flag 1/0、戻値pointer、3本のRET8」、比較の方向とcallerでのEBX出力先という独立のABI増分。
T013_AI・T028死亡callback資料・B HANDOFFで0x49F923/0x49F90C/0x49F8BA/0x49F8FF等の正確な機械語アドレス一致をSelect-String read-onlyで検索し0件（他の意味的重複はVERIFY）。
## 限定原作PEバイト証拠（VAはImageBase 0x400000を引きRVAに変換）
0x49F7D0 len0x160 (352B) SHA256=45B301B602A424CD0524F2D9EB7ABDF26F3015C211015B5BC50BA7CE3A134545。
0x49F7D0 len0x75 (117B) SHA256=905E66B7159001026C3FB8CD8AAF6F3C3A5DA05F9BEE62A5686C1B0307D74F56。
0x49CDE0 len0x65 (101B) SHA256=52FC1CEA9EAF0D0D92E32B0A3004AACB018300E07B41C5A3AFFE80B22E784545（逆ASMは既知命令境界0x49CDE8から採用し0x49CDE0開始の2命令は非境界のため棄却）。
0x405370 len0x4B (75B) SHA256=2805D89B974FC8FC142ADB70102E8B6F15B8267E0E0CBF22912FF99CD7874BE3。
## 安全・復旧・次P0
OTHER B-RC-20261025-05H-T013-POWERSHELL-QUOTE-01：最初の読取専用python -c引数のPowerShell引用符解釈誤りでSyntaxError、PE取得0/書込0。合法な同一PE読取をPowerShellに適合する引用で実行して復旧。新安全拒否ではない。
既安全拒否対象0x5710C0..0x571500、0x514C50、0x5769B0のXREF、旧拒否済0x599BD0検索や文書書込の再試行・別経路迂回0。Ghidra/REA全再解析、原作ゲーム実行、原本/DAT/SAVE、MASTER/他lane、dev_lab/Git/Work/設定/スケジュールへの書込0。
残P0はmap比較/iterator木不変条件、同key異常時の枝、副作用・例外/再入・死亡callbackからの実到達と最終対象選択への影響。原作Goldenは無改変EXE・X20変更前DAT・同一SAVE/MAP/input/RNG＋合法同key再登録や前後辞書値を固定して比較 DESIGNED_NOT_RUN。旧原作Gameplay PASS0/strict MATCH0、今回新READY0・E正式MASTER統合0・Task DONE増分0。
次はT013/T028の既有CALL traceから同key duplicate pathの動的到達条件とresult使用元をread-onlyで追跡（既拒否対象は回避でなく対象外として維持）。
