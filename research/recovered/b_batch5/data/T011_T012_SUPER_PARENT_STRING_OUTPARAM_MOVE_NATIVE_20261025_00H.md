# 新B T011/T012｜super親名tokenのoutparam・return・ScriptData格納（2026-10-25 00時台）
研究ID: B-20261025-00H-T011-T012-SUPER-PARENT-STRING-MOVE-01 ／ Owner B(T011主、T012関連) ／ STATUS STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY
## 証拠・正本・安全
Desktop Commander Local Compact接続成功。MASTER最新既読正式checkpoint196/READY596（E旧値）、LANE規約、B HANDOFF/B担当資料、T011/T012未同期回収索引、T013拒否回復索引を先読。旧22-file回収/後発10研究/Library訂正版2/10～18H研究の意味的ID統合は未完、新しい同期主張なし。
検索基盤 README/BUILD_MANIFESTを読取、search.sqlite現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（manifest一致）。PE現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。
原本ゲーム実行/変更・Ghidra全面再解析・REA実行なし。active.lockはheadless_analysis直下/検索索引直下ともENOENT。既安全拒否(0x5710C0..0x571500等)の再試行・迂回0、新安全拒否0。
## NEW｜parent字句の格納契約（原作PEと既存Ghidra疑似C）
0x005049E0入口0x00504A1D XOR EBX,EBX。0x00505064 PUSH 0x24でScriptData候補確保→0x00505072 VTable=0x00638D1C→0x00505089 EBP=新オブジェクト。
0x0050508F MOV ECX,[ESP+0x24]→0x00505093 PUSH EBX(0)→0x00505094 PUSH ECX→0x00505095 LEA ECX,[ESP+0x4C]→0x00505099 CALL 0x00502DD0；字句取得の戻りを0x005050A4 MOV EDI,EAXで受ける。
0x00502DD0 のGhidra宣言は void __thiscall だが、原作0x00502E0B MOV EBX,ECXで出力文字列オブジェクトを保存し、共通復帰0x00503420 MOV EAX,EBX／0x00503440 RET。従ってこの呼出経路では戻りEAXは呼出時ECXのoutparam指示先。戻り値を捨てるvoid契約は不正確（C++厳密署名はVERIFY）。
0x005050A1 LEA ESI,[EBP+0x4]→0x005050A4 MOV EDI,EAX→0x005050AB CALL 0x00405300。callee擬似CはESI先とEDI元の24B string相当を移動/コピーし、長さ+0x10・容量+0x14更新、元を空stringへ戻す。従ってtoken文字列はScriptData候補の +0x4 に格納され、長さは ScriptData+0x14 に置かれると静的に接続。
続く0x005050D4 MOV [ESP+0x18],0x0062C918(文字列super)→0x005050E2 CALL 0x004528E0→0x005050EE CALL 0x00463280登録候補は前回22H既知で二重計上0。0x005050F7 XOR EBP,EBP→0x005050F9 PUSH EBP→0x005050FF CALL 0x00502DD0は登録後の次字句取得（返値を0x00505107 MOV EDX,EAX）、同一親名の再取得とは断定しない。
既21Hの属性検索0x00464290 @0x0046452C と値取得0x004647D0 @0x00464B19 にある [EAX+0x14]==0 停止gateは、今回確認したScriptData+0x4 string長の配置と構造的に一致。これが同一オブジェクトを必ず辿るか・合法DATでの値はINFERRED/VERIFY。
## 限定窓SHA256（PE、末尾アドレスinclusive）
0x00502DD0..0x00502E10 65B = ED021D0B6F1DF132C4EA88D24FE53BA8BE6ACF3E702869472BCCE312D00A84A3
0x00503420..0x00503440 33B = DFFF6E0B28684BE31C29094649B483361CC78D6BC7E8B85047E24CC4225D272C
0x00505064..0x00505104 161B = A29C5EA1B8D377780553A25F38AEFBCCBE2388814280ED1DB48534DFEBA44234
0x00405300..0x00405366 103B = 12232CEBD89712860E96DA83F1C34A30A349FA046A47DF6CF07A3DE0D4EECFC2
## 非重複・未解明・再開点
22Hのcolon→super登録、23Hの「:」initializer、21Hの空親名停止/原DAT u_diplo_nt3..nt6、20H以前のstr_ratio/50回上限は再計数0。新増分は getter型ではないparser 0x502DD0 のECX→EBX→EAX戻値契約と、0x405300によるparent字句のScriptData+4格納・string長の下流停止gate対応。
VERIFY: token字句がu_diplo_nt2の実名になる実行経路、親属性登録時の重複・適用優先、子Skill+0x288の実効ratio、呼出param_2詳細、CRTのcolon初期化到達、エラー時契約、別owner/Library完全重複。
Golden DESIGNED NOT RUN: 無改変EXEとX20改造前DAT、同SAVE/MAP/input/RNGでu_diplo_nt2親とnt3..nt6、parent欠損/空/正常とstr_ratio未指定/明示0を比較。旧原作Gameplay PASS0、strict MATCH0、新B READY0、E MASTER統合0、DONE0。次は0x005050FF後のparser状態と原DAT親参照解決→ScriptData node格納先を狭いASM/検索で突合。
