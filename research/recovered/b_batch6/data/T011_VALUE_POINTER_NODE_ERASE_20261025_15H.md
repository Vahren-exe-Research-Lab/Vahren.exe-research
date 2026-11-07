# T011｜変数辞書のnode破棄と値オブジェクト所有権を分離する静的検証（2026-10-25 15H）
ID: B-20261025-1513-T011-VALUE-PTR-NODE-ERASE-01 / Owner B T011 / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / INFERRED / VERIFY / NOT READY
## 証拠源・事前保全
- Local Compact接続成功。MASTERの正式cp196/READY596は既存値、ANALYSIS_LANES_PROTOCOL・B HANDOFF・B T011/T012/T013/T024/T028・未同期/拒否索引を先読。旧13H詳細はPCに実在し、全文独立readbackとSHA照合に成功。13Hのowner/HANDOFF索引追記は未着手であることを確認。
- EXE read-only: rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。search.sqlite 実SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFEST一致）。
- Ghidra/原作ゲーム/REA全体解析・原本実行・他owner書込0。active.lock候補2箇所なし、Java/Ghidra稼働表示なし。既安全拒否VA/拒否操作は未実行・迂回0。
## 旧14Hの確認範囲（既存IDは再発番しない）
- B-OFFLINE-20261025-1411-T011-COUNTER-REPLACE-ERASE-01（会話内旧OFFLINE-UNSYNCED）で示された 0x004637A0 内の 0x0046386C CALL 0x0058F7E0（旧key erase）→0x00463896 CALL 0x00436680（node生成）→0x004638A2 CALL 0x004A69B0（insert）は今回PC原作ASMでも再確認。旧14Hの発見として計上し直さず、PC未登録旧IDの重複同期は保留。
## 今回の新規増分：node+0x28の値pointerの破棄は別問題
- 0x00436680 の原作ASM：0x004366AF PUSH 0x30 / 0x004366B1 CALL 0x005B6C2Bで48Bのnode候補を確保。0x004366D2 LEA ESI,[EBX+0x0C]、0x004366FE MOV EDX,[EDI+0x1C]、0x00436701 MOV [ESI+0x1C],EDX。ゆえにnode基点では[EBX+0x28]へ値オブジェクトpointerがコピーされる（STATIC）。
- 0x004637A0 は更新値用32Bオブジェクトを先に確保（+0x1Cに数値を格納）、旧keyの削除が必要なら0x0046386Cからerase。その後新48B nodeへ新値pointerをコピーして登録する（STATIC）。
- 0x0058F7E0（旧key削除）は0x004BF820へ範囲erase。0x004BF820は通常の1node除去で0x004BF8BF CALL 0x00510030、全範囲側で0x004BF83A CALL 0x00463070（subtree後片付け）へ分岐。
- 0x00510030原作ASM後半：0x0051027A CMP [EBP+0x20],0x10（key文字列capacity）、条件時0x00510284 CALL 0x005B6BBB（key動的領域）、0x0051029F CALL 0x005B6BBB（node自体）、0x005102B6 DEC EAX→0x005102B7 store count。今回確認した削除経路にnode+0x28値pointerの明示free/derefはない。
- 0x00463070原作ASM（全86B）：0x00463089 自身へrecursive CALL、0x0046309A key文字列領域free、0x004630B0 node free。node+0x28への明示アクセスや値オブジェクトのfree CALLはこの関数にない。
- PC原作PE限定窓SHA256：0x00436680/188B=3616D203D7498C7254AF55EC5D6E17FD2C9EA62A2C4732259268B62516632BE0、0x00510030/657B=412E0184448A7FE624F973D091A7B563612FB26E620B7748945E99080620D203、0x00463070/86B=40C8B860C2A43EF0A2BCE19E78CA1103D9E1300AB89CD6EF02D014298D6F2671。
- Ghidra既存擬似C crosscheck: FUN_00436680の(pcVar1+0x28)=*(param_1+0x1c)、FUN_00510030とFUN_00463070のfreeはkey文字列とnodeに限定。戻り値/レジスタ推定はASM優先（STATIC-GHIDRAは補助）。
## 適用境界・非重複・検証
- ここで証明したのは「この2種のerase path自体はnode+0x28が参照する32B値オブジェクトを明示解放しない」ことまで。別のowner arena/後段cleanup・間接alias・値再参照による生存・リーク可能性はVERIFY。未解放=メモリリーク確定とはしない。
- 13Hは未定義名の32B値0初期化/検索（T013）、14Hは既存key delete+reinsert（T011）の既知部分。本IDの新規差分は node+0x28値pointerコピーと 2種類のnode破棄経路で値pointerをfreeしない契約の静的境界。旧研究と二重READY化しない。他レーン/Library未同期研究との全意味重複はVERIFY。
- 原作Goldenの必要条件：非改変旧EXE、20倍強化前DAT、同一SAVE/MAP/入力/RNG、同一name初回0・再更新/別owner・erase前後のkey/node/value addressと解放追跡・次tick・save/load・可視結果。同条件native実測NOT RUN、旧Gameplay PASS0、strict MATCH0。
- STATUS: STATIC / INFERRED / VERIFY / NOT READY。新B READY0、E MASTER統合0、Task DONE0、旧未同期全ID照合未完。NEXT：値ポインタの外部所有者/保管・全参照の合法範囲で絞込、T024/T028の未解明P0へ研究配分を戻す。