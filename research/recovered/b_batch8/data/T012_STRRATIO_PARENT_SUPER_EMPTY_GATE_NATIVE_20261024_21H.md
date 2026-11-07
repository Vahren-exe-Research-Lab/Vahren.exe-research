# B/T012｜str_ratio親参照：super空文字長ゲート・値取得との一致・原DAT子継承候補
研究ID: B-20261024-21H-T012-SUPER-EMPTY-GATE-STRRATIO-PARENT-01
Owner B/T012（T011 Skill継承参照）。2026-10-24 21時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-SOURCE / INFERRED / VERIFY / NOT READY。
## 事前確認・安全・出典
Desktop Commander Local CompactでMASTER(cp196/公式READY596は旧値)、規約、LANE_B_HANDOFF、B5担当、未同期復旧登録、既拒否を先読。10/21回収22 filesと後発10研究・10～18H Library研究のPC完全統合は未完。拒否済アドレス/操作/本文へ再試行なし。
原作読取対象 rea_lab/targets/hakushin067_Vahren.exe。実ファイルSHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
Ghidra抽出済み search.py function 0x00464290 / 0x004647D0のみ軽量閲覧。統合V9 verify は V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。PC標準CURRENT_ACTIVEはV3のまま。検索元の擬似CはSTATICでありGoldenなし。
## 原作ASMの独立増分：両属性関数で同一のsuperデータ停止条件
存在判定 0x00464290：0x0046451C MOV EAX,[ESP+0x20]→0x00464520 CMP EAX,[ESI+4]→JE 0x00464567（superノード欠損）。0x00464525 MOV EAX,[EAX+0x28]→0x00464528 CMP EAX,EBX→JE 0x00464567（super値ポインタNULL）。
続く0x0046452C CMP DWORD [EAX+0x14],EBX→0x0046452F JE 0x00464567（superのScriptData文字列長が0）。条件を満たしたときだけ0x00464539 LEA EDI,[EAX+4]→0x0046453F CALL 0x004C1200で次親名を検索。0x00464548..4B結果欠損でも停止。0x00464554..5C counter<50は既16/17H成果で再計上0。
値取得 0x004647D0：0x00464B09 MOV EAX,[ESP+0x20]→0x00464B0D CMP EAX,[ESI+4]→JE 0x00464B4F、0x00464B12 MOV EAX,[EAX+0x28]→0x00464B15 CMP EAX,EBX→JE 0x00464B4F。
続く0x00464B19 CMP DWORD [EAX+0x14],EBX→0x00464B1C JE 0x00464B4F。非空時だけ0x00464B26 LEA EDI,[EAX+4]→0x00464B2C CALL 0x004C1200。0x00464B35..38次親候補欠損でも停止。0x00464B41..49 counter<50は既成果。
存在判定の失敗復帰は0x0046457A XOR AL,AL、成功復帰は0x004645B3 MOV AL,1（既17/18H成果）。値取得の失敗経路0x00464B4F..0x00464B7Cは出力オブジェクトの+0x20へデフォルト数値0をコピー。成功経路0x00464BDD..0x00464C1Fは候補ScriptData+0x20を同スロットへコピー。成功/不成功がともに数値0となり得るため、存在ALと値スロットを混同不可（既17/20Hを補強）。
この2関数の局所superゲートは「super項目自体不在」「値ptr NULL」「super値string長0」「名前を解決できない」を分けている。空文字が実際のDAT構文からどのように生成されるか、全parser pathと上流call可到達はVERIFY。
原作PE限定範囲SHA256: 0x0046451C..0x0046455E=2A81073F8E1D32C19FC9898B11D91F4CB563760905617A72BAC226B11E866D52 (67B)。
原作PE限定範囲SHA256: 0x00464B09..0x00464B4A=83BFD72AAAC07645EE726D6451D41CEFE51F62893F9BF7241109E46A4BBBB445 (66B)。
getter失敗窓0x00464B4F..0x00464B7E SHA256=E53CCFEA1B562A700C20F2E4379CA1FCC449A73F4940C604143E8B5B291C3A5B、成功窓0x00464BDD..0x00464C22 SHA256=33D90B01532FB27D6F44B9AEE8C1086FFCAC061AB65A28AC1ED960E7547015A3。
## 原DATとの新しい接続（原本ZIP正規化コピーのみ読取）
data/normalized/hakushin067_core/a_default/script/32_ボススキル/B_14_ヌエバ・デスパセーニャ.dat L193前後：skill u_diplo_nt2 { func=heal; attr=speed; str=attack_dext * -200; str_ratio=0 }。すぐ下に u_diplo_nt3/u_diplo_nt4/u_diplo_nt5/u_diplo_nt6 : u_diplo_nt2、各子は attr のみ上書き。前段 next3 列には nt2～nt6 が列挙される。
このraw Skill継承4枝では、各子でstr_ratioが省略され親に0がある。上記のpresence/getterが通常の親検索を完走するなら、子の実効倍率は0となる候補。実際のSkill loader・戦闘時実効値・発動可到達はINFERRED/VERIFY、Golden PASSとみなさない。
同folderの限定検索でstr_ratio明示0の例を少なくとも9地点で別途直接読んだ（B14/B525、U必殺、U40、U21、U16など）。既T012 §32で全scriptのraw str_ratio文字列22件・F10実例、既T011/F13 cook_heal等が確認済み。今回の9件を全件網羅や新たな一般仕様と主張しない。
## 非重複・受入・未解決
既T012 §32の省略1.0/明示0.0と既16～20HのAL/getter/50回は新規加算0。今回の独立増分はsuper ScriptData文字列長ゼロという停止条件の両関数ネイティブ対比、および未掲載u_diplo_nt2→nt3～nt6の原DAT継承候補との接続。B owner T011/T012/T013/T024/T028の u_diplo_nt2/nt3 exact search 0、PC最新の意味的全重複はVERIFY。
Golden設計：無改変旧EXE＋20倍改造前原DAT＋同SAVE/MAP/入力/RNGで u_diplo_nt2直接とnt3～nt6派生のロード時compiled +0x288、対象/HP/MP/状態/次tickを比較。super欠損/NULL/空値の局所フラグは合法DAT fixtureを別途確認するまでDESIGNED_NOT_RUN。旧原作Gameplay PASS0、strict MATCH0。
新B READY0、Task DONE0、E MASTER統合0。未同期10～18H・既安全拒否状態は不変。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール書込0。次：u_diplo child属性解決とsuper文字列の実loader/親名変換をB担当証拠から追跡し、原作Goldenを合法出陣後に検討。
