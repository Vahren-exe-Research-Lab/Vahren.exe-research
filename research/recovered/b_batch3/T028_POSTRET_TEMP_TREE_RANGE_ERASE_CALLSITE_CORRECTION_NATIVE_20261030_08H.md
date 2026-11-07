# B-20261030-0808-T028-POSTRET-TREE-ERASE-CORRECTION-01｜退却候補mode1後の一時木range-eraseとCALL site訂正
Owner B / T028 / 2026-10-30 08H JST。STATIC (原作ver0.67 ASM + V9擬似C) / INFERRED / VERIFY / NOT READY。新規正式READY0。
## 始業・証拠源・保全
Desktop Commander Local Compact PC接続成功。MASTER_LEDGER.md（TASK QUEUE/既正式checkpoint）、ANALYSIS_LANES_PROTOCOL.md、LANE_B_HANDOFF.md、T028_MORALE.md、B復旧索引・最新07H研究を先読。旧安全関連SAFE134/HOLD21、Library147中54件の1-byte差、10/25旧本文欠落はOPEN・保全済み扱いにしない。
旧search_index/README.md・BUILD_MANIFEST.jsonはENOENT。公式に許可された既存の統合V9別名CLI・DBを使用し、標準V3を変更しない。
原作解析コピー rea_lab/targets/hakushin067_Vahren.exe 2910720B 実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9 DB 141033472B 実SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、SQLite immutable readonly quick_check=ok。active.lock=なし、Java/Ghidra起動検出なし。元ゲーム/再Ghidra/他owner書込なし。
## 今回の原作ASM・既存07H誤記訂正（最優先）
旧07H HANDOFFとT028 ownerの「0x5AC609 CALL 0x510850」は誤り。原PEの **0x5AC609 LEA ESI,[ESP+0x38]**、0x5AC60D LEA EAX,[ESP+0x3C]、真の **0x5AC611 CALL 0x510850** をnative Capstoneで確認（STATIC）。0x5AC607 PUSH EAX / 0x5AC608 PUSH ECXが先行する。
0x5AC5F9 MOV BYTE PTR [ESP+0xB4],4 → 0x5AC601/605で一時木から2つの境界pointerをロード → 0x5AC611のrange-erase helperへ。今回のCALL命令は元EXE直接E8の実ディスアセンブル。V9擬似CはCALL-site行を正確に出さないのでASMを優先。
## 新規callee分岐：一時RB-treeの全域・部分消去を分離
0x510850は0x51085F / 0x510863で[head]とboundaryの一致を比較し、**全域条件成立時0x510867 CALL 0x44D0D0** → 0x510875復帰。比較不成立なら0x51087A begin==end判定、異なる範囲の要素ごとに **0x5108DF CALL 0x510C20** を反復し、0x5108EE付近で反復終了。
全域処理0x44D0D0は0x44D0E6 CALL0x4ED240（再帰/反復ノード破棄）と0x44D0EE CALL0x5B6BBBを含み、headリンクを自己参照に戻してcount=0にする（V9 STATIC）。部分処理0x510C20は先行2026-10-26 B研究で既知のnode unlinkで、0x510E6B free後0x510E82/83 count--（非零時）。**0x510C20の既存意味は再発見扱いにしない。**
0x5AC616で一時木head pointerを読み出し、0x5AC61B CALL0x5B6BBBでheadを解放、0x5AC623/627で別の一時格納器0x5AF030をcleanupする。0x5AC630 PUSH EDX → 0x5AC631 JMP 0x5AC5B5 → 0x5AC5B5 CALL0x5B6BBBで残りの一時バッファを解放し、0x5AC5BD MOV EAX,EBP、0x5AC5D8 RETへ合流。mode1後も正規の戻り先が存在するがゲーム実到達は未確認。
原PEの局所窓SHA: VA0x5AC60D 0x27B=B845F2B4823150EE76C7DDD5B59FE37EA1678F9CC2D926409FCA6CE62DB79B7E、VA0x5AC5AB 0x55B=12C3F7E79A64E551897EB8DE82F6EF17061D64A8727A8CA7F458868A2765DC8B。擬似C：V9 function 0x510850 / 0x510C20 / 0x44D0D0 / 0x4ED240 / 0x5AC1A0、ABI未検証。
## 非重複・再実装境界・Golden
事前にB所有T028*.md＋HANDOFFへ新址0x5AC611/0x510861/0x510867/0x5108DF/0x4ED240/0x5AC627の文字列検索：各0。0x510850と0x510C20は既知（各7/12ヒット）につき既存callee本体を新規計数しない。旧07H記録を削除せず本訂正を後追い追加。他lane・10/25欠落分の完全意味重複はVERIFY。
この0x510850木は0x5AC1A0ローカル候補列挙の一時木（INFERRED）であり、以前0x598450において解析したSpot側0x416080/0x415CF0木と同一コンテナと断定しない。+0xB8減算や士気変更の直接作用をこのgeneric helperへ帰属させない。
Golden DESIGNED_NOT_RUN：旧原作EXE・20倍以前DAT・同SAVE/MAP/input/RNGでmode1許容、0/1/複数候補、空木/部分/全域、退却先成功/失敗、cleanup前後のhead/count/ポインタ/Spot+0xB8/翌tickを別々に取得。原作Gameplay PASS0、strict MATCH0、新B READY0/E MASTER0/DONE0。
次のP0は0x5AC601境界pointerの正確なlocal対応・0x510850 full-range判定の合法成立性・0x5AC5BD返値のconsumer、T011経験値/召喚・T012 damage・T013最終対象選択・T024通常AI・T028本来の士気敗走。新安全拒否0、既拒否迂回0、原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/schedule変更0。