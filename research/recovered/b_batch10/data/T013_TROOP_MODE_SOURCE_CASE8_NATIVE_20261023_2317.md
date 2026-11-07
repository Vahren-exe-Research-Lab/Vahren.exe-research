# T013｜Troop+0x30への値producerとcase8条件付き伝播（23時台）
ID: B-20261023-2317-T013-TROOP-MODE-SOURCE-CASE8-01 / owner B:T013 / STATIC-PE-ASM + STATIC-GHIDRA / VERIFY / NOT READY。
【PRECHECK】Desktop Commander Local Compact接続、MASTER checkpoint196/公式READY596（E既存値）、レーン規約、B HANDOFF、T011/T012/T013/T024/T028正本、旧未同期・安全拒否を先読。旧未同期10件、02時訂正版2件、14:14詳細拒否は未統合・未保存のまま。
【CURRENT INDEX】標準V3 guard=PASS_ACTIVE_V3_STATIC、input SHA14/14・E8 44889・JMP 6324・errors=[]。V1旧search.sqliteのCALL数とは混同しない。
【ORIGINAL】原作 ver0.67 EXE read-only現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（一致）。原作実行・書込・全体Ghidra/REA再実行0。
【NEW / BRANCH】0x004B4710 のGhidra擬似C switch case8に相当する原作ASM：0x4B5976 E8 call 0x49CCA0 → 0x4B597B mov [ebp-0x80],eax → 0x4B597E cmp eax,2 → 0x4B5981 jg 0x4B5A44。比較はSIGNEDで、3以上はmode setterを経由しない。負値はこの局所gateでは排除されないが、producerが負値を返す到達性はVERIFY。
【NEW / LIST】gateを通ると0x4B5997 E8 call 0x49E8B0で得た配列候補を0x4B59B5以降に走査。0x4B59CC mov edi,[ecx+0x1D0]、0x4B59D8 test edi,edi → 0x4B59DA je 0x4B5A2BによりNULL候補はskipped。+0x1D0の型・所有者関係はVERIFY。
【NEW / IDENTITY】0x4B59EE E8 call 0x44D070 → 0x4B59F3 mov edx,[eax] → 0x4B59F5 cmp edx,[ebp-0x98] → 0x4B59FB jne 0x4B5A2B。ここで比較不一致はsetterをskip。比較対象がTroopの何のidentityかは未確定。
【NEW / VALUE-FLOW】成立時0x4B59FD mov eax,[ebp-0x80] → 0x4B5A00 E8 call 0x569530 → callee native 0x569531 mov [edi+0x30],eax。0x49CCA0戻値から保存localを経由しTroop候補+0x30へ渡る静的データフロー。callee自体のmode writerとfirst-live配送は旧B-20261023-22Hで既知のため再計上0。
【NEW / SECOND CALLER FLAGS】別のowner 0x4F9510では0x4F9831 xor eax,eax、0x4F9833 mov byte ptr [edi+0x1f],1 → 0x4F9837 call 0x569530。さらに0x4F9FF2 mov byte ptr [ebx+0x20],1を通る条件枝と、0x4FA036 mov byte ptr [ebx+0x1f],1を通る別条件枝のいずれも、0x4FA03A mov eax,[esp+0x28]→0x4FA03E mov eax,[eax+0x28]→0x4FA041 mov edi,ebx→0x4FA043 call 0x569530へ合流する。flag意味はVERIFY。
【SOURCE WINDOWS】原作PE VA0x4B5957 len0xDD SHA256=4D38429E4ADC259DD5BC53AED6CE486037D4B59C5425DC8FF8980A222E712A62。VA0x4F9FEB len0x69 SHA256=E83D3D54FD10D09B62BA0FF79B0BA103EBE5AB7811467DE0EBFCE078AE3BCB6C。
【SOURCE WINDOWS 2】VA0x4F982D len0x15 SHA256=DB438E081E72ED666133DCF70E6CF3D85FF1C5667FD740610F99579CD34AF478。window hashは原作byte同一性のみでruntime成功証明ではない。
【DEDUP】B HANDOFF / data/T013_AI.md / T011 ownerで新固有site 0x4B597B/7E/CC、0x4F9FF2、0x4FA036 の一致0件をread-only確認。先行22Hのsetter直接call site 3件、+0x30 mode消費・座標配布・Troopフラグは新READYに再加算しない。
【INTERPRETATION】0x4B4710 case8の「signed <=2」は局所受理gateであり、mode自体が0/1/2に限定される証明ではない。0x5699C0/0x56A790のmode 1/2/その他分岐へ負値も論理的には流れ得るが、実入力・DAT command mapping・実走時の到達性はVERIFY。
【GOLDEN / NOT RUN】同EXE・無改変DAT・SAVE・MAP・入力/RNG・capture SHAに対し、source戻値 -1/0/1/2/3、0x1D0 NULL/nonNULL、identity match/mismatch、Troop+1F/+20初期値、構成員0/1/3を別々に検証。setter実CALL回数・+30変化・配置候補生成/移動・RNGを観測。実機Gameplay Golden PASS0、strict MATCH0。
【SAFETY】既拒否 0x5710C0..571500、0x514C50、0x5769B0 XREF、T024と旧拒否書込は再照会/迂回なし。原本・MASTER・他lane・REA/dev_lab・Git/Work・設定・schedule変更0。
【STATE / NEXT】B新READY0、E MASTER統合0、Task DONE0。0x49CCA0戻値のDAT入力/符号許容、0x44D070返値と+1D0実型、0x4F9FF2/0x4FA036のflag語義を次の独立合法staticで追跡。PC保存/readback可否は別途記録。