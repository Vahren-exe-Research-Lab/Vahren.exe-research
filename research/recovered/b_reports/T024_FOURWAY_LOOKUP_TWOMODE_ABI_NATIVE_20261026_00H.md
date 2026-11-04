# B-20261026-0011-T024-FOURWAY-LOOKUP-TWOMODE-01｜T024 fourway fallback の二系統Unit解決とイベント伝播
日時: 2026-10-26 00時台 JST。Owner B / T024。分類 STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。
## 出典・前提
Desktop Commander Local Compact成功。MASTER正式checkpoint196/READY596は旧既存値、規約・B5 owner・復旧索引・HANDOFFを事前読取。旧14H OFFLINE全文と回収22+後続10+Library2の全意味照合未了。安全拒否元・禁止VAには非接触。
原作EXE = rea_lab/targets/hakushin067_Vahren.exe; SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回現物計算一致）。search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（一致）。active.lock false、java/ghidraプロセス検出なし。既存PE read-only Capstone、search.py function 4C7040/5284A0/5282C0/49E6B0 の限定利用のみ。
PE function SHA256: 0x4C7040 (545B)=14AB2AD148AAFAEF3423A69DD4AAC753B6978C762BCD511C1BA2389E7565B4D1; 0x49E6B0 (195B)=487A23C58266AF500C0EB2479F3B12FD22D303EB3A26FA785FBC810892807510。
追加: 0x5282C0 (92B)=F6B491371D0F0B3056A71E601582E341AB2A187B4060BC7D608495DB8BECF932; 0x5284A0 (81B)=14CA7ECA265976A84D8DBB73B68E3C4B987DBB90379A2F30CB1F3CC011C07A15。
## 新しい分岐証拠
先行23Hの 0x526C4E/76/9E/CC6 →0x4C7040, ECX=0/1/2/3 は既知・再計上0。新規は0x4C706F LEA EDI,[ECX+2]→0x4C70B9 SHL EDI,4→0x4C70BC/C2 で0x67B608/+0x67B604を起点とするindexed 16B table slotから28B record配列のbegin/endを取得すること（4 caseはslot 2..5候補）。
0x4C70DC CMP byte [0x65EB64],0; 0x4C70E3 JE 0x4C7181。非0側 0x4C7128 CALL 0x49E6B0→0x4C712D TEST EAX→0x4C7131 MOV EAX,[EAX+1D0]→非NULLかつ[EAX+1C]==0なら0x4C7148 CALL 0x5282C0。
0x65EB64==0側 0x4C71C0 CALL 0x49E6B0→0x4C71C5 TEST EAX→0x4C71C9 CMP byte [EAX+1867C],0→0x4C71D9 CALL 0x5284A0。両modeともkeyごとの候補文字列を探し、存在・状態条件で下位処理へ進む。ゲーム内フラグ意味はVERIFY。
0x49E6B0 は Ghidra prototype void 表示だが原作 0x49E744 MOV EAX,[ESP+8]→0x49E748 CMP EAX,[ESI+1EEBE0]→一致時0x49E755 XOR EAX,EAX、非一致時0x49E750 MOV EAX,[EAX+28]、0x49E772 RET。つまり現CALLで使用する戻値はエントリ+0x28のポインタまたはNULL。Ghidra void署名を再実装契約に採用しない。
0x5284A0 原作 0x5284A1..0x5284D9 では ECXのNULL、+8C==0、+1F8!=0、+1867C==0、+1D0!=0、+1867E==0、+1FA==0をgate。成立時 0x5284E2 CALL 0x568710、0x5284EA CALL 0x5695B0。既23Hのfourwayの新規作用方向はUnit系の候補再設定と整合、行動名VERIFY。
0x5282C0 原作 0x5282C5 [ESI+1C]==0、0x5282CC..DA 子候補の先頭ポインタ評価、0x5282DA [EAX+1FA]==0、0x5282E3..FE 既登録listで同一ESIを探索、未登録時0x528304 CALL 0x5299E0、0x52830C CALL 0x5695B0、0x528312 CALL 0x529B60。空vectorでEAX=0から+1FAを読む経路の到達安全性はVERIFY。
0x4C714D/0x4C71DE は下位CALL後に戻値でなく stack +0x1B を1にする。0x4C722Fにて同byteを判定、非0なら0x4C7241/46/4B vtable+0x24 に文字列 'change' と0を渡す。**通知条件はhelperを呼んだこと**であり、実際に登録変更が発生した証明ではない（helper内早期終了あり）。
## 差分・限定
既23H: pair優先消費/4種CALLとV3四site収録。既22H: 一時選択list/UI。今回独立増分は+2→slot2..5展開、global flag別2mode、lookupの本来のEAX戻値、calleeの追加gate、change通知latch。B T024/T028/HANDOFF新主要VA 0x4C70DC/0x4C71D9/0x49E750/0x5284D2/0x4C723F の前方exact match0。全owner/LIBRARY意味非重複はVERIFY。
DYNAMIC: 本run原作ゲーム起動・書込0。X20改変DATが存在するため正式旧原作Gameplay比較に使わない。無改変原作EXE、X20前DAT、同SAVE/MAP/input/RNGで4 slot×global flag0/1×lookup miss/hit×子候補空/非空、候補listとchange通知/次tickを観測する必要あり。Golden DESIGNED_NOT_RUN、PASS0/strict MATCH0。
正式 READY 追加0、E MASTER統合0、Task DONE0。安全拒否0、既拒否再試行・別経路迂回0。元EXE/ZIP/DAT/SAVE/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール変更0。
NEXT: 0x65EB64 setter と 0x67B604 table slot2..5の生成元、0x5282C0 の空配列到達性、0x5284A0の+358候補処理、および 0x4C724B 'change' の条件付き可視実機を小範囲で照合。