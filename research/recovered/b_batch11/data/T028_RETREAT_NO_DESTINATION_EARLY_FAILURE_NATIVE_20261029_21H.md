# T028 原作retreat_ok後段：退却先未発見→メッセージ返却→mode1分配抑止（21H）
研究ID: B-20261029-2112-T028-RETREAT-NO-SPOT-EARLY-FAIL-01
日時: 2026-10-29 21時台 JST / B-owner T028（T013/T024参照） / STATIC ORIGINAL-PE ASM + V9 GHIDRA / INFERRED / VERIFY / NOT READY

## 先行資料・未同期・権限
Desktop Commander Local Compactオンライン。MASTER既正式cp196/READY596（再集計なし）、解析規約、LANE_B_HANDOFF、T011/T012/T013/T024/T028 owner、横断復旧ハブと操作規約をread-only確認。Bの旧SAFE134/HOLD21、Library54件1-byte差、10/25原文欠落、未統合成果はOPENであり本件で回復扱いにしない。
解析コピー rea_lab/targets/hakushin067_Vahren.exe は実バイトSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。統合V9 DB SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable PRAGMA quick_check=ok。既存V9 CLI検索のみ、原作実行・Ghidra再解析なし。
今回の原作ASMはread-only Python pefile+capstoneで局所逆アセンブル、V9擬似C/直接E8索引と突合。新規安全拒否0・既拒否対象への再試行0。

## 新規原作ネイティブ接続
[ENTRY] 0x5681F2 XOR EBX,EBXでEBX=0。0x568265/26Bにて [context+8]+0x18!=0 なら直接0x568335（Unit処理）へ。0x568274/27Aで [[context+4]+0x1EF22C]==0 でも同じく直行。いずれも「検索しない＝失敗メッセージ」とはならない。
[UNIT GATE] 検索側は0x568280..0x568290でUnit pointer vector begin/endを照合し、先頭Unit+0x18610==0の場合にのみ実施。空vector時はEAX=0のまま0x568290のbyte読込へ進む静的経路が見えるため、合法な空vector到達・例外/不変条件はVERIFY（原作BUG認定しない）。
[SEARCH CALL] 0x5682A6で firstUnit+0x1C8をEBPへ、0x5682AE CALL0x583CF0、0x5682B5 CALL0x597BA0。0x5682BA..0x5682C3は PUSH EBX(=0), PUSH [[context+8]+0x14], PUSH EAX → 0x5682C3 CALL 0x5AC1A0、0x5682C8 ADD ESP,0xC。V9擬似C上の第3引数param_3=0に一致し、calleeのparam_3非零限定フォールバック分岐はこのCALLでは使えない（STATIC）。
[CALLEE GATE] 0x5AC1D6 CMP DWORD [secondArg+0x10],0、0x5AC1D9 JE 0x5AC6A0、0x5AC6A0 XOR EAX,EAX：第2引数+0x10==0なら選択失敗0となる（ORIGINAL ASM）。V9 0x5AC1A0ではSpotElm/Spot RTTI候補と候補の条件分岐を探索するが、返却先が常に退却可能とはDYNAMIC未確認。
[FAILURE] 0x5682CB EAX==0→0x5682CF..0x568325で既存global stringへCP932 literal VA 0x628B4Cを連結し非零文字列pointerをEAXに返す。原生53 byte CP932は「の部隊は退却に失敗しました\n退却出来る領地がありません」。0x568327 JMP 0x568384なので0x568335以降のUnit vtable+0x68(PUSH1)呼出しに入らない。
[SUCCESS] EAX非零なら0x568329 MOV [EBP+0x1B4],EAX、0x56832F INC DWORD [EAX+0xB8]を先に実行し、0x568335以降で各Unitの+0x1867Cを検査→既知0x56835C vtable+0x68(PUSH1)へ。+0x1B4リンクと+0xB8参照数様の増分は静的に確定、所有権/永続化・戦場での退却成立はVERIFY。
[CONSUMER] retreat_okの既知caller 0x5221B7 CALL0x5681C0→0x5221BC MOV ESI,EAX、0x5221BE/0x5221C0でEAX非零なら0x522239 CALL0x52CCF0へ。0x52CCF0のV9擬似Cは0x52CDDE CALL0x43F470を含む文字列処理だが、具体的な画面表示の実機確認は未実施。失敗文字列の確定とUI可視化の確定を分離する。

## 出典・非重複・Golden条件・次回
EXE原生窓: 0x5681C0 493B SHA256 AEDE9147D0DD7957F4568FEF450D9706021DA71640E8B73008B0C3F4A3E41E2A、0x5682C0 117B SHA256 5D0B20A65FFAD6E2946896879B5EFC65A051CA642517CD98A53C7CD965A4B2D3、0x5AC1A0 1378B SHA256 4C7B54378A8A83C79984A300A7C7D96B5366394EA5A5825D9F92A1F81F36A0BD、CP932 53B literal SHA256 1366C316757297D58D7123724E314BF60DC7225247F079F5105F96DD340FEC60。
B-owned data内422 Markdownの新literal/VA 0x628B4C,0x5682C0,0x568329,0x5AC1D9,該当日本語全文は先行一致0。旧20Hの0x5681C0戻り非void・slot+0x68接続、19H state4判定は既知で再計上0。10/25欠落・他ownerの意味的完全重複はVERIFY。
原作無改変EXE＋20倍改変前DATで、同SAVE/MAP/input/RNGの退却対象Unit・空/非空候補vector・secondArg+0x10の有無・0x5AC1A0返値・+0x1B4/+0xB8前後・EAX通知・翌tickを合法同run比較（DESIGNED_NOT_RUN）。原作Gameplay Golden PASS0、strict MATCH0、B新規正式READY0/E MASTER統合0/DONE0。STATIC/INFERRED/VERIFY/NOT READY。
次回は0x5AC1A0のSpot選別成功条件とrefcount +0xB8の戻しwriter、0x52CCF0の表示受入条件、T024通常AIとの関係をB権限内で追跡。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/自動化変更なし。