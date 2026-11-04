# B-20261026-0310-T024-MODE-PARAM-FILTER-TWO-CALLERS-01｜T024候補列挙: global modeと引数が独立する範囲
記録: 2026-10-26 03H JST / owner B T024 / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / VERIFY / NOT READY。
## 出典・安全境界
Desktop Commander Local Compact接続成功。MASTER E正式cp196/READY596（旧値）、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、B5 task資料・UNSYNC register・旧安全拒否を先読。原作PEは rea_lab/targets/hakushin067_Vahren.exe 読取のみ（SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187）。旧search.sqlite README/BUILD_MANIFESTはSTATICの索引、現行V3と混同しない。原本起動・変更、Ghidra/REA再解析なし。
先行B-20261026-0115の「0x41EF50 param_1は表示候補filter候補」は再計数しない。先行B-20261026-0212のcaller共通gateと引数PUSH0/1・空配列NULL可能性も既知。本研究は**分岐命令とcount実効範囲**を追加。
## 今回限定的に元EXEから独立したmachine code確認
0x41EFE9 CMP global byte [0x65EB64],0 → 0x41F007 JE 0x41F07E。global==0枝は0x41F07E以降のfirst-eligible選択へ移る。global!=0枝だけが下記param gateを通る。
0x41F020 CMP BYTE PTR [ESP+0x8C],0 → 0x41F028 JE 0x41F03B。arg==0なら0x41F03Bへ直行しowner+0x1C gateを省略。
arg!=0なら0x41F032 MOV EDI,[ECX+ESI*4] → 0x41F035 CMP BYTE PTR [EDI+0x1C],0 → 0x41F039 JNE 0x41F06D。該当owner+0x1C!=0ならこの候補をcountせず次へ。
通過後は0x41F043 [ECX+ESI*4] → 0x41F046/49 inner+0xC/+0x10 vector、空なら0x41F04E XOR EAX,EAX / 0x41F050 JMP 0x41F054。
0x41F054 CMP [EAX+0x8C],0 / 0x41F05D CMP [EAX+0x1F8],0が成立する場合、0x41F066 INC EBX → 0x41F067 [0x65EB60]=EBX。初期EBX=3 (0x41EFF0)。
global==0枝も0x41F094..0x41F0A5で各owner inner vectorの空時にECX=0→[ECX+0x8C]を参照。両枝の内側vector非空保証と正常合法到達は未証明であり確定BUGにはしない。
0x41F0E2 MOV ECX,0x1B、0x41F0E7 CMP EBX,0x1B、0x41F0EA JG 0x41F0EE、0x41F0EC MOV ECX,EBX、0x41F0F5 MOV [0x65EB60],ECX。表示候補数の上限は27（物理戦闘Unit上限とは無関係、実際の画面表示未確認）。
0x54F30A CMP [ESP+0x20],3 / 0x54F30F JNE 0x54F353、0x54F311 CMP [ESP+0x58],0 / 0x54F316 JNE 0x54F353。これらは前02H記録の0x54F31C firstUnit gateへ入るための追加の必要条件。前02HのPUSH1=0x54F345、別caller0x4B4D4A PUSH0は既知。
## 追加解釈（静的境界）
0x41EF50の「global mode決定」はparam比較より先、paramによる+0x1C owner除外はmode!=0時のみ。したがって2 callerの引数0/1相違はglobal mode==0では、この限定列挙枝へ影響しない。これは制御フローに関するSTATICで、操作/ゲーム動作の同値性はVERIFY。
内側vector空によるNULL+0x8C照会は前02Hの**caller側空配列**とは別レイヤ。game合法の内側vector不変条件は不明（INFERRED/VERIFY）。
## 出典の局所PE window SHA256
0x41EFD0 /270B = 199463DBB4C9F1BEC4B91D1851F8A5727AC5C82A2C06D279BBE3EE9A3941C40E。0x41F020/95B = AB60B1A00F899E4361965CC98BC519D6C418767127FB8104A2E2532B2FD7602E。
0x41F07E/124B = C38DA3531CEA1867893D12DF730F37BDDF971DA89F69E5C0A82A5AE3E14B2132。0x54F30A/78B = 4498F8BB52404012863915627EC5819E798F53DCC0DD4A660FC2D6A100B2AE57。
## 重複/拒否/同期・Golden
B data既存の完全文字列「0x41F020」事前検索0件（全owner/Library意味一致まではVERIFY）。旧01H「param filter」の一般観察と02H caller外側NULL条件は今回新規加算0。旧14H OFFLINE全文など完全同期は未完。
既拒否0x5710C0..0x571500・拒否本文・コマンドは非接触。B own detail/T024 owner/本HANDOFFのみ書込。原本/他owner/MASTER/REA/dev_lab/Git/Work/設定/schedule変更0。
Golden条件は無改変原作EXE、20倍前DAT、同SAVE/MAP/input/RNGで global0/1×param0/1×owner+1C0/1×inner空/非空、候補count+0x65EB60・UI通知・次tick比較。DESIGNED_NOT_RUN / Gameplay PASS0 / strict MATCH0 / 新B READY0 / E MASTER0 / DONE0。
次回: 0x41EF50のinner nonempty保証を設定元の範囲で追跡、0x54F30A/311の元stack引数出典と0x41F0E2 cap27が実表示へ接続する範囲を確認。