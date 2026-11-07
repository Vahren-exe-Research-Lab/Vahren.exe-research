# B-20261026-0417-T024-FIRST-ELIGIBLE-UI-COUNT-SPLIT-01｜T024 グローバルmode別の候補集計方式・表示入力の非対称性
日時: 2026-10-26 04時台 JST / B所有T024 / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / INFERRED / VERIFY / NOT READY
## 事前照合・出典
Desktop Commander Local Compact ONLINE。MASTER正式checkpoint196/READY596はE既存値（再集計なし）。LANE規約/B HANDOFF、T011/T012/T013/T024/T028、未同期索引と安全拒否記録を先読。旧search_index README/BUILD_MANIFEST、search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF と ro SQLite quick_check=okを確認。旧snapshotと現行V3を混同しない。検索は旧search.py function 0x41EF50、原作PE限定Capstone逆ASMで独立照合。Ghidra/REA再実行・ゲーム起動なし。
対象原作 _REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。0x41EF50開始の2108バイト窓 SHA256=2F2DB96BFC98ACFEF470A98D076399A3CDF595F2700E7BCC20D5FB1816683D0B。
## 新しい独立静的証拠：0x65EB64によって「候補数」の意味が変わる
原作0x41EFE9 CMP BYTE PTR [0x65EB64],0 → 0x41F007 JE 0x41F07E（0枝）。0x41EFF0 EBX=3、0x41F001 global [0x65EB60]=3 は両系統の初期値。
mode==0: 0x41F07E..0x41F0BFでouter owner vectorを前から走査。各ownerのinner begin/end(+0xC/+0x10)の先頭Unitに +0x8C==0 かつ +0x1F8!=0 が成立すると、0x41F0C1/0x41F0CFでそのownerのみを選択、0x41F0D2/0x41F0D5で inner(end-begin)/4、0x41F0DF ADD EBX,3 の後 0x41F0E2へ合流。後続のownerはこの経路では走査しない。候補未発見なら3を維持して合流。
mode!=0: 0x41F009..0x41F07Cではouter ownerを全走査。既03Hのarg!=0かつowner+0x1C!=0除外を経た後、先頭Unit +0x8C==0/+0x1F8!=0 を満たすownerごとに0x41F066 INC EBX、0x41F067 global[0x65EB60]=EBX。1 ownerが複数inner Unitを保有しても、この集計枝はownerにつき+1。
両枝は既03Hの0x41F0E2..0x41F0F5に合流し、N<=27に切り詰める。新規差分はcap自体ではなく、その前段の計算元がmode0「最初に条件合致したownerのinner個数+3」、mode非0「条件合致したowner数+3」と異なる点。
## 後続描画経路を原作ASMで照合
0x41F3BA CMP BYTE PTR [0x65EB64],DL → 0x41F3C0 JE 0x41F5AD（DLの値は近傍のゼロ初期化を前提とし、Ghidra擬似Cでもmode0枝）。mode0側0x41F5AD MOV EAX,[ESP+0x20]は0x41F0D8で保存した単一owner、0x41F5B9/0x41F5BCはそのinner範囲を取得。0x41F5E6 LEA ESI,[EDX+3]→0x41F5E9はcount上限、0x41F601でinner要素ポインタを取得し0x41F60Cでchild+0x1C8を読む。
mode!=0側の描画入口は0x41F3C6でouter vectorを読み、0x41F3F4でglobal countとの上限比較。したがってmode0は選択された単一ownerのinner展開、mode非0は選ばれた複数ownerの列挙という解釈に整合。ただし表示名/実UI/子ごとの描画下位処理はVERIFY、これを戦闘AIの攻撃対象・部隊数と同一視しない。
## 重複境界・未解決・Golden
先行03Hのarg0/1+owner+0x1Cフィルタ、inner empty NULL候補、27 cap、02Hの2 caller gateは既知扱い・今回READY再計上0。B T024 ownerとHANDOFFに新VA 0x41F0C1/0x41F5AD/0x41F3BA の直接一致先行0。旧14H OFFLINE全文、回収22件+後発研究+Library、他laneとの意味的完全重複照合はVERIFY/UNSYNCED。
空inner vectorで[EAX+0x8C]相当の参照が起こり得る前03Hの懸念は解消していない。owner内の有効先頭と以降の子の有効性が異なる場合の描画、mode0 branchの子件数上限、mode切替時のUI選択副作用、間接呼出しはVERIFY。実機クラッシュ・仕様確定はしない。
Golden案: 無改変原作ver0.67（x20改変前DAT）、同SAVE/MAP/input/RNGでmode0/非0、owner複数、先頭eligible位置、inner長1/2/25以上、arg0/1、owner+0x1C、表示件数、次tickを比較。DESIGNED_NOT_RUN/Gameplay PASS0/strict MATCH0/新B READY0/E MASTER0/DONE0。
既安全拒否（例0x5710C0..0x571500）・拒否済内容/コマンドに非接触、迂回0。PC-B所有詳細/T024索引/HANDOFF以外の書込なし。次は0x41F0CF single-owner選択から0x41F5AD描画の逐次参照と合法inner非空保証の設定元を許可済みSTATIC限定で追跡。