# B-20261029-1713-T013-UPSTREAM-FOUR-CALL-GROUP-FILTER-01｜T013/T024 mode1仮想処理の4上流入口とUnit候補フィルタ
Owner B（主T013／T024・T011・T028参照）｜2026-10-29 17時台 JST｜STATIC ORIGINAL-PE ASM + V9 INDEX / INFERRED / VERIFY / NOT READY

## PRECHECK・証拠源
- Desktop Commander Local Compact ONLINE。MASTER既知公式checkpoint196/READY596を読取、規約・LANE_B_HANDOFF・5担当owner・回収索引を確認。旧search.sqlite/READMEは10/29整理後の原位置に存在しないため再生成せず、現LATEST V9を読取専用使用。
- 原作解析用PE `rea_lab/targets/hakushin067_Vahren.exe` 実バイトSHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9実バイト141033472B SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable ro sqlite `PRAGMA quick_check=ok`。
- 未同期回収の旧判定を維持：SAFE134個別byte確認、HOLD21安全関連、旧B147の54件1byte差、10/25 14H研究本文未発見。前回16H研究は保存・readback済。今回拒否済みVA/証拠・操作に再接触せず、安全拒否迂回なし。

## NEW：0x44CF80への4種のoriginal E8 caller gate
- V9 callers全4件：0x44AEBF（関数0x44AE70）native E8BC200000、0x44B700（0x44B240）E87B180000、0x44C705（0x44BBB0）E876080000、0x44CF3E（0x44CD70）E83D000000。各siteは原作PE x86 Capstoneでも確認。
- 0x44AEB0 FCOMP [ESI+0xD0] → 0x44AEB8 TEST AH,0x41 / 0x44AEBB JNE skip → 0x44AEBF CALL。0x44B6F1 FCOMP [EBX+0xD0] → 0x44B6F9 TEST AH,0x41 / 0x44B6FC JNE skip → 0x44B700 CALL。0x44CF2F FCOMP [EBX+0xD0] → 0x44CF37 TEST AH,0x41 / 0x44CF3A JNE skip → 0x44CF3E CALL。通常ordered finiteでST0 > +0xD0のgate候補。
- 逆向き比較入口0x44C6F2 FLD [EBX+0xD0] / 0x44C6F8 FCOMP ST(2) / 0x44C6FE TEST AH,5 / 0x44C701 JP skip / 0x44C705 CALL。通常ordered finiteでは前3者と異なる比較向き（境界・NaN・x87 stackを要検証）。4入口とも実行条件と管理オブジェクト同一性は未証明。

## NEW：0x44CF80内部の二階層filterをoriginal ASMで確認
- 0x44CF80：manager[+0xA5]==0なら+0x20=4、さらにmanager[+0x18]==0なら0x44CFA0 CALL0x49D1B0。0x44CFAB manager[+0x48]==[+0x4C]なら全group走査skip。manager[+0x38..+0x3C]は4-byte要素group配列、group[+0x0C..+0x10]は候補Unitポインタ配列（型はINFERRED）。
- 0x44CFE1 CMP firstUnit[+0x8C],0 / 0x44CFEA CMP firstUnit[+0x1F8],0 → 両条件が「+8C==0 かつ +1F8!=0」のとき0x44D043で当該groupをskip（初要素NULL時の実合法性はVERIFY）。
- 0x44D002 unit[+0x1867C]!=0はskip。残りはunit[+0x1D0] pointer非NULLが必須。0x44D00B unit[+0x18615]==0の場合はpointer非NULLだけで0x44D033へ、+18615!=0の場合はpointer[+0x1F]!=0かつpointer[+0x40]!=0を追加で要求（0x44D027/2D）。合格のみ0x44D033/35 vtable+0x68、0x44D038 PUSH1、0x44D03A CALL EAX。
- unit[+0x1867E]の一回限りlatchはこの上流関数で直接検査していない。前回確認した下位0x544D10/0x578110でのlatch判定と混同せず、両段の入力・実動作はVERIFY。16Hに既知のvtable slot4件と0x44D03Aは再計上0。
- PE局所窓0x44CF80..0x44D05A 219B SHA256=5F75E2F514503AE716CB6A0C358BE6F8C48CA722CB3F20F544894E2D6302220E。上流0x44AEAC 31B SHA0E23DEEE55371B3F72624D361B1948F43517DB5E652CB4863B310912695DE99B。ほか局所窓のSHA/ASMはB HANDOFF参照。

## DEDUP・回帰・継続
- 5 owner代表文書＋本HANDOFFで新site 0x44C701/0x44D002/0x44D014/0x44CFAB/0x44AEBF の先行literal=0。欠落10/25・他Bサブ資料・他ownerの意味的全重複照合は未了。旧16H indirect dispatch・2 entry・旧RTTIは再発見として加算しない。
- Golden必要条件：原作未改変PE＋2026-10-22 x20強化前DAT、同SAVE/MAP/input/RNG、4入口の比較時ST値/FPU status/manager+0xD0、グループ初Unit+0x8C/+0x1F8、候補+0x1867C/+0x18615/+0x1D0参照、下位+0x1867E/F・可視移動/敗走・次tickの同run trace。DESIGNED_NOT_RUN。
- 原作Gameplay Golden PASS0 / strict MATCH0 / 新正式B READY0 / E MASTER統合0 / Task DONE0。STATIC/INFERRED/VERIFY/NOT READY。新安全拒否0。読取専用Python -c quoting NameError はOTHER/RECOVERED（PowerShell here-stringで合法な独立読取に成功）。
- NEXT：manager[+0x38] group生産・+0x48空判定の型、0x49D1B0副作用、4入口のx87 ST/provenanceとUnit+0x1D0型、T024通常AI/T028士気・敗走、T011召喚EXP/T012 damage P0。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/automation変更なし。
