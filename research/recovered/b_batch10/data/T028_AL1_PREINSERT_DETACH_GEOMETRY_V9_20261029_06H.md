# B-20261029-0608-T028-AL1-PREREG-DETACH-GEOMETRY-01｜T028 AL1時の旧効果解除→再登録候補
時刻: 2026-10-29 06H JST。担当 B/T028、T013既知汎用helperは参照のみ。STATIC/V9 + INFERRED/VERIFY/NOT READY。
## 事前確認・回収状態
Local Compact ONLINE。E MASTER最終正式checkpoint196/READY596（既値・全件再集計なし）、ANALYSIS_LANES_PROTOCOL/B5 owner/LANE_B_HANDOFF、2026-10-29 SAFE134監査を参照。
B関連Library155件中、安全に保全・PC byte照合済み範囲はV3収録134件、既拒否/関連21件はHOLD。旧10/25 14H研究原文未発見。過去03:00の17H・22H安全拒否、部分INVALIDを解除・再試行せず。
旧search.sqlite/BUILD_MANIFESTは履歴資料。CURRENT pointerはV3だが、2026-10-23 V9統合専用CLIを明示的にread-only使用。V9 validator verify今回PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
固定原作ver0.67 EXE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（V9 pseudoc banner/5H実byte確認値。今回原作現物の再hashはしない）。
## 新しい具体的接続
既05Hの0x48CFD7→0x5AA6E0 AL=1と0x48D089→同callee AL=0、0x5AA709→0x5A9CC0は既知。今回の増分は0x5A9CC0の関数内部、解除helper、座標更新の接続。
V9 function 0x005A9CC0: 178 bytes、E8 0x5A9CE7→0x4C22B0 (native e8c485f1ff)、0x5A9CFD→0x4C3E40 (e83ea1f1ff)、0x5A9D0F→0x4BC9C0 (e8ac2cf1ff)。3件ともV9にE8_DIRECT_CALL記録。
0x5A9CC0は仮想slot+0x34を呼び、slot+8が真なら0x4C22B0、slot+0x48が真なら0x4C3E40、slot+0x44を呼んだ後、0x4BC9C0を呼ぶ（擬似C）。vtable実体、分岐の合法到達、実引数ABIはVERIFY。
0x4BC9C0（103B）は0x4BC9E1 E8→0x4BC3C0（native e8daf9ffff）で位置/セル様レジストリを検索し、見つけたポインタの1件を末尾要素で置換してend-=4する swap-with-last 構造。0x4C22B0のactive/pending/defer三配列解除と、0x4BC9C0汎用swap-deleteは旧T013-20261013/20261027研究で既知：今回新発見件数には加えない。
0x5A9CC0はその後ポインタobj+0x40/+0x44/+0x48/+0x4Cの矩形様四座標を書換え、既存幅/高さから中心位置を再算出する擬似C。中央寄せ・形状resetの意味はINFERRED、原native幅/符号・実画面位置はVERIFY。
0x5AA6E0はAL!=0かつ保持obj vtable+0x64非zeroのときだけ0x5AA709から上記0x5A9CC0を呼ぶ。共通後続0x5AA7B1 E8→0x4BC920は新規挿入候補（旧04HにCALL既知）、spot_fire文字列処理へ続く。V9 0x4BC920擬似Cは0x4BC3C0(param1,1)を用いて末尾にpointerを追加し、管理側+8を増やし対象+0x54に連番様値を書込む。
従ってAL=1側では旧解除＋矩形変更を経て再追加する条件付パスがあるが、AL=0側はその旧解除を通らず共通登録を通る。双方が火災・士気/敗走、効果の新規生成/同一再利用と等しいかは未証明。以前の「0x5A9CC0も登録処理」という粗い分類は避ける。
## 重複・試験・次の一手
B5 ownerとHANDOFFの新site literal 0x5A9CE7/0x5A9CFD/0x5A9D0F/0x4BC9E1 は先行一致各0。0x5A9CC0名自体は既05HでNEXT指定あり、今回新規とは扱わない。他ownerおよび未回収10/25資料との意味的dedupはVERIFY。
Golden: 原作改変前DAT・同SAVE/MAP/input/RNGの合法戦闘で、同じ効果が移動してAL1/0それぞれが起こる条件、vtable+0x64真偽、旧登録解除/新登録/矩形座標/可視火・Unit/士気・敗走/次tick差分を同runで観測。DESIGNED_NOT_RUN。
原作Gameplay Golden PASS0/strict MATCH0、新B正式READY0/E MASTER統合0/Task DONE0。状態 STATIC/INFERRED/VERIFY/NOT READY。旧拒否21 HOLD・未回収10/25・全semantic-dedup保留。
NEXT: vtable+0x64 slotの実体、0x5A9CC0呼出時EAX/ESIのオブジェクト同一性と0x4BC9C0のkey、二vector producer、T028士気敗走、T013最終target、T024戦闘AI、T011召喚、T012ダメージ。安全拒否の迂回無し、原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール不変更。