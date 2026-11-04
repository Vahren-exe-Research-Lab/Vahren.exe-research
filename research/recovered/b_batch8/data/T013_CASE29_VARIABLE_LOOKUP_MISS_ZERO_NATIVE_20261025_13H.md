# T013 case 0x29：ExpresString 未定義名の値取得・0初期化（2026-10-25 13H）

研究ID: B-20261025-1312-T013-CASE29-MISSING-VARIABLE-ZERO-01 / B owner / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA-V3 / VERIFY / NOT READY
## PRECHECK / 出典
- Desktop Commander Local CompactでPC正本読取成功。MASTER正式checkpoint196・READY596は既存値（再集計なし）。規約・B HANDOFF・T011/T012/T013/T024/T028資料・既安全拒否/未同期索引を先読。
- 原作read-only対象 rea_lab/targets/hakushin067_Vahren.exe（現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187）。現物 0x463CA0..0x463DEA の331B SHA256=838A036A2C2801D39D228B98DA5B14AA08059E67184DCF376D4D6B338F37E646。
- 旧search.sqlite現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（legacy manifest一致）。現行V3 validator=PASS_ACTIVE_V3_STATIC / 14 input SHA / E8=44889 / E9/EB=6324 / gameplay NOT_RUN。
- 先行12HのExpresString → 0x49CD4F CALL 0x463CA0 → 0x49CD54 [EAX+0x1C] と親スコープは既知で再計上しない。
## 今回の新規ASM分岐・値取得
- 0x463CD9 EAX=ECX(name ptr), 0x463CDB ESI=EDX(owner), 0x463D0C EBX=owner+0x30C。0x463D19 CALL 0x4C1200 は検索結果iterator候補をcaller localへ書き込む（検索calleeはV3擬似C）。
- 0x463D1E MOV ESI,[owner+0x310] は辞書end/sentinel候補。0x463D24 MOV EAX,[ESP+0x14] / 0x463D28 CMP EAX,ESI / 0x463D2A JE 0x463D4A は発見・未発見の分岐。
- 発見時 0x463D31 MOV ESI,[EAX+0x28] で既存nodeの格納値ポインタ候補を取得し、0x463D43 MOV EAX,ESI → 共通epilogue 0x463DCD（return pointer）。既存値を書き換える命令はこの経路で確認されない。
- 未発見時 0x463D4A PUSH 0x20 / 0x463D4C CALL 0x5B6C2B で32Bオブジェクトを確保。非NULL側 0x463D5A/+5D/+64/+67 で文字列len0/cap15/先頭NULL と [EAX+0x1C]=0 を設定、0x463D6A EDI=EAX。
- 0x463D7E CALL 0x436560 は辞書候補（文字列キー＋格納値ポインタ）の構築。V3擬似Cの+0x1C=param_2->pointer と整合。0x463D9B CALL 0x4A69B0 は owner+0x30C の辞書へのinsert、0x463DCB MOV EAX,EDI は新32Bオブジェクトへのポインタを戻す。0x4A69B0内部の0x4A6A48→0x4A6700 はRB-tree構造登録（V3擬似C）。
- 合流：既存名は保存済値を[EAX+0x1C]から参照。欠落名は新規0値の32Bオブジェクトをinsertし、呼出元0x49CD54が同じ+0x1Cから0を読むことと整合（正常確保・正常挿入前提）。
## 推論・非重複・残課題
- STATIC確定は存在判定・欠落時の0初期化・登録CALL・EAXポインタ返却命令まで。『同じ名前が以後も同一スコープで残る』『例外/確保失敗時』『script variableの全仕様』はINFERRED/VERIFY、未実機。両Expres型にcastできない場合のThrowは既12H成果。
- 先行12Hは0x463DCB戻り値不一致まで。今回追加は 0x463D28/2A 分岐、0x463D31既存ptr、0x463D67の欠落初期0、0x463D9B挿入CALL。B T013/HANDOFF exact検索で新主要VA既載0；他lane/22回収+後続10+Library2の意味重複はVERIFY。
- GAMEPLAY GOLDEN: 未改変原作EXE＋20倍変更前DAT＋同SAVE/MAP/input/RNGで未定義名→初回0→再参照、既存0/非0、別owner、式Num/String、不正型、復帰後case29 clamp・辞書前後・次tickを比較。DESIGNED_NOT_RUN、原作Gameplay PASS0 / strict MATCH0。
- 安全：既拒否VA・拒否コマンドへの再試行/迂回0、Ghidra全体解析・原作ゲーム起動・原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/automation変更0。active.lock既知2候補なし。
- 復旧 OTHER: B-RC-20261025-1312-T028-PATH-01 は T028_MORALE_RETREAT.md のENOENT→正本 T028_MORALE.md 再読で復旧。B-RC-20261025-1312-V3-CLI-FLAG-01 は search_current.py --format markdown の未対応→--formatなしで同じ許可済V3照会へ訂正。安全拒否ではない。
- 未同期：10/21回収22件と後続10研究＋Library訂正版などの全ID照合は未完、今回のPC保存は本IDのみ。新B READY0、E MASTER0、Task DONE0。
- NEXT：0x49F730の辞書候補key/value lifetimeか、T024戦闘AIの未解明P0へ移動。誤ったvoid ABIでの再実装禁止。
