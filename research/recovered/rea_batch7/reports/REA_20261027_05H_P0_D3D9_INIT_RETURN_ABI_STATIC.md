# 迫真戦記 ver0.67 REA｜P0 DirectX9初期化のAL戻り値ABI・失敗ゲート
研究ID: REA-LOCAL-20261027-05H-P0-D3D9-INIT-AL-RET-ABI-STATIC-01
日時: 2026-10-27 05時台 JST。状態: PC-SAVED / STATIC / VERIFY / NOT READY。実ゲームGolden: NOT RUN。
対象EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 今回の新規STATIC：0x00559690の返り値を全4 RET経路で固定
前回04Hは親0x005554F0のCALL 0x00559690（site 0x0055590D）直後にTEST AL,AL（0x00555914）が存在することを確認したが、子自身はGhidra擬似Cで「void FUN_00559690(void)」として出力され、返り値の生成は未検証だった。今回は原作機械語を別途逆アセンブルした。
- 失敗ゲート1：0x005596B0のvtable+0x20経由CALL後にTEST EAX,EAX（0x005596B2）、成功ならJNS 0x005596DD。負値ならMessageBoxA、0x005596CC XOR AL,AL、0x005596D4 cookie-check、RET 0x005596DC。
- 失敗ゲート2：0x00559774のvtable+0x40経由CALL後にTEST EAX,EAX（0x00559778）、成功ならJNS 0x005597A1。負値ならMessageBoxA、0x00559790 XOR AL,AL、0x00559798 cookie-check、RET 0x005597A0。
- 失敗ゲート3：0x005597CAのvtable+0x68経由CALL後にTEST EAX,EAX（0x005597CC）、成功ならJNS 0x005597F7。負値ならMessageBoxA、0x005597E6 XOR AL,AL、0x005597EE cookie-check、RET 0x005597F6。
- 成功経路：0x0055997B MOV AL,1、0x0055997D cookie-check、RET 0x00559985。
- 原作機械語の該当関数範囲は0x00559690..0x00559985。関数内のRETは上記4件。Ghidra機械生成の「void」を返り値不使用とみなすと、起動制御が原作と食い違う。
- 0x005B6513 __security_check_cookieの正常経路は0x005B6513 CMP ECX,[0x0065A220]、0x005B6519 JNE、0x005B651B REPZ RET。EAX/ALを変更しないため、直前の0/1は通常復帰で保存される。
- 3か所のMessageBoxAに渡される文字列(0x006299E8/0x00629A0C/0x00629A30)は原作バイト列が一致し、CP932で「DirectX9」の初期化失敗を示す。API/HRESULTは負値判定、0以外の成功HRESULTは拒否していない。

## 親制御フローと影響
0x00555904 CALL 0x00556F00 → 0x00555909 TEST AL,AL → 0x0055590B JE 0x00555912。前段が0なら子0x00559690を呼ばない。前段が非0なら0x0055590D CALL 0x00559690を実行する。
0x00555912 XOR ESI,ESIはALを変更せず、0x00555914 TEST AL,AL→0x00555916 JE 0x0055591Fにより、AL=0では0x00555918 CALL 0x00555CD0（音声初期化を含む）を省略する。AL=1では呼び出す。
よって「DirectX9の最初の3ゲートの成功」が後続初期化の前提となる。後段の追加仮想CALLのエラー処理・全部の初期化成功をAL=1が保証するかは別件VERIFY。

## 独立証拠・集計の区別
旧検索DBと統合V9の両方で0x0055590D→0x00559690の直接CALLを照合。旧DBでは0x005596B0/0x00559774/0x005597CAの間接CALLが当該関数に属することを再確認。間接CALLの対象vtable関数への意味付けは今回の正式VERIFIEDではない。
原作PE32ハッシュ、両SQLiteハッシュ/quick_check、Native命令アンカー、RET構成、cookie戻り値非破壊、04H証拠・旧64件syncの独立監査 **53/53 PASS**。検査53件は関数数ではない。
5証拠：info INDEX_ONLY / pseudo INDEX_ONLY / assembly TARGETED_PE_NATIVE / callers INDEX_ONLY / callees INDEX_ONLY。REA新規正式VERIFIED=0、5種新規完全取得=0、過去Wave1～5 64/64維持、TODO/VERIFY/BLOCKED正式書込差分0/0/0。
原作Golden PASS 0、strict MATCH・完全複製率は未測定。REA/Ghidra/原作ゲーム/Workを起動せず、旧DB・V9はimmutable read-only。直前04Hの37件は再加算しない。
PCはオンライン、開始時active.lockなし、空きRAM12.01GiB、CPU4%単発観測。監査保存run約1.235秒、研究全体の所要時間は未計測。
原本ZIP/EXE/SAVE、MASTER、QUEUE、PROGRESS、旧runs、他レーン、Git、公開物、スケジュールは未変更。拒否済み操作は再試行していない。

## 次のP0・要検証
0x00559990と0x00559690の成功後の仮想CALL群の副作用/失敗時挙動を重点調査。次に0x00556790およびDAT_0068B38Cをread-onlyで追い、BGM第2ベースパスの決定元を確定する。

