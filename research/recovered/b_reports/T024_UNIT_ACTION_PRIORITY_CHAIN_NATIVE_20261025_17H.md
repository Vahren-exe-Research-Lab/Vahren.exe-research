# B-20261025-1712-T024-UNIT-ACTION-PRIORITY-CHAIN-01｜Unit更新候補の短絡アクション優先順（STATIC / VERIFY / NOT READY）
- Owner: B / T024。日時: 2026-10-25 17時台 JST。原本: 迫真戦記0.67 Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回PC現物再ハッシュ一致）。原本実行・変更なし。
- 証拠: rea_lab/targets/hakushin067_Vahren.exe x86 PE machine ASM (Capstone read-only); search_index active V3 search_current.py function/callees 0x005263E0/0x00527710/0x005205B0/0x005276C0、guard PASS_ACTIVE_V3_STATIC input SHA14/14、E8 44889、JMP6324。旧search.sqliteは履歴。
- 原作PE 0x005263E0 全299B SHA256=21F8B7EA83795DE0C90941DF36A523F472BFC78036023583C5606F698C75C418、0x00527710 全211B SHA256=057F139341D72384B8C1960EBBAD659BF03A271AEE9B4AA380147958E602EF8A。
## 0x005263E0 直接ASMで確認した経路
- 0x5263EB..0x526401: Unit候補ESI+4先の+0x20==0かつ+0x14==0の場合のみ 0x526401 CALL 0x4498E0。満たさなくても 0x526406へ合流。
- 0x526406 CALL 0x527710。0x52640B TEST AL,AL / 0x52640D JNE 0x526504。AL非0なら以下の処理を完全にスキップ。
- 0x526414 CALL 0x5205B0。AL非0枝は0x52641D～65へ：ESI+0x38!=+0x3C時に [ESI+0x18C]+0x24/+0x25の両byte0なら0x52643C CALL 0x527890→RET。そうでなくESI+0x430!=0x80000008なら0x52645A CALL 0x5277F0→RET。該当しなければ0x526504共通終了。AL=0枝のみ次項へ進む。
- AL=0枝 0x526466～0x5264CF：owner [ESI+0x194]+0x1EED54/+0x1EED55の少なくとも一方が非0の場合だけ領域走査。EBX=0; stride 0xB4; EBX<0x10E0 なので最大24候補領域。候補有効 +0x1ED244、座標 [ESI+0x32C/+0x330] から領域オフセットを引いた点が PtInRect(...) に入る場合0x5264BE CALL 0x403D70。PtInRectはIAT間接呼び出し(0x609268)でありE8と混同しない。
- 0x5264D2 CALL 0x526510 は上記走査を実施しない場合も通過。次に ESI+0x38 != +0x3C の場合のみ 0x5264E1→0x5276C0、返AL0なら0x5264EB→0x526E50、返AL0なら0x5264F5→0x5271A0の順。各CALL直後にTEST AL,AL / JNE 0x526504で短絡。候補枯渇または全3件AL0なら0x5264FF→0x526A40。空なら最初から0x526A40。
- V3 callees 原作E8検証済11件：0x526401→4498E0, 406→527710, 414→5205B0, 43C→527890, 45A→5277F0, 4BE→403D70, 4D2→526510, 4E1→5276C0, 4EB→526E50, 4F5→5271A0, 4FF→526A40。11/11のcall-siteと宛先は索引で確認、元PEの299B Capstone限定decodeとも整合。
## 0x527710 の短絡理由（原作ASM限定）
- 0x527716/722 は Unit+0x430==0x80000008（sentinel）かつUnit+0x45D==0でなければAL0。Unit+0x18Cの+0x50/51及び+0x26/27の各ペアに少なくとも1つ非0が必要。
- 条件成立かつ Unit+0x44C==0x80000008 なら0x52775B..0x52778Bで座標等を+0x44C/+450/+454/+458に保存し+0x464=0、0x527792 AL=1。そうでなければ0x5277B7→0x520800後+0x464=0、0x5277C3 AL=1。
- ペア条件不成立では0x5277C7..0x5277D9で+0x44C/+450/+454/+458をsentinelに戻し、0x5277DF AL0。他の初期条件不成立もAL0。ゲーム内での移動/攻撃の意味、Unitの具体型、入力・副作用・例外はVERIFY。
## 新規差分・非重複・境界
- 既B-20261022-0815-T024-T028-DUAL-CLOCK-01は 0x521CDF→5263E0→4498E0→565750 の時間CALL鎖のみを既知とする。本IDは5263E0の11 E8＋AL短絡順序・24領域gate・527710のsentinel状態遷移を追加。T024/T028/HANDOFFの新主要VA 0x5264E1/0x5264EB/0x5264FF の先行直接記録0。回収22＋後続10＋Library2の全意味重複はVERIFY。
- 0x5205B0は既擬似Cで座標・表示寸法計算あり、戦闘AIに固有と断定禁止（T024「Unit更新/行動候補」）。Ghidra 0x5263E0型はvoid、0x5271A0は疑わしい返型のため ABI未確定、hook/再実装の関数シグネチャとして利用禁止。ASMのAL制御フローのみSTATIC。
- Golden: 無改変原作＋20倍前DAT＋同一合法SAVE/MAP/Unit/入力/RNGで 527710 true/false、5205B0 true/false、選択vector空/非空、5276C0/526E50/5271A0各短絡分岐と次tick可視行動・Unit差分を観測。DESIGNED_NOT_RUN、原作Gameplay PASS0、strict MATCH0。新B READY0、E MASTER0、Task DONE0。
- 次のP0: 0x5276C0→0x527F60の実効果、0x526E50・0x5271A0の返AL contractと候補者条件、0x526A40 fallback副作用、0x521CDF呼出元の合法Unit更新時相。既拒否0x5710C0..0x571500／拒否されたcommand・資料へアクセスなし。原本・他owner・REA/dev_lab/Git/Work/設定・スケジュール変更なし。
