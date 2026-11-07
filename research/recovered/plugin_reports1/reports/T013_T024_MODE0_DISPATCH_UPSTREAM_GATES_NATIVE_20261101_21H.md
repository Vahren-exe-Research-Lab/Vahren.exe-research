# 迫真戦記 新B｜T013/T024 0x528E86呼出の上位4段gateとループ復帰（2026-11-01 21H JST）

研究ID: B-20261101-21H-T013-T024-MODE0-DISPATCH-FOUR-GATE-01。owner: B/T013・T024。STATIC_NATIVE / STATIC_V9 / INFERRED / VERIFY / NOT READY。
原作Gameplay Golden PASS=0、strict MATCH=0、DYNAMIC=0、新B READY=0。元EXE・ゲーム・他lane・Git・共有knowledgeは変更しない。

## 証拠源・原本同一性
研究PC Local Compact ONLINE。最初にMASTER_LEDGER.md、ANALYSIS_LANES_PROTOCOL.md、B HANDOFF、T011/T012/T013/T024/T028、knowledge README/SYNC_STATUS、未回収07H/03H台帳を読取。旧search_index README/BUILD_MANIFESTはENOENT、V9現行CLIへ読取専用で切替。
原作EXE: rea_lab/targets/hakushin067_Vahren.exe、実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、2910720B。起動なし。
Native限定window: [0x528DFB,0x528E9A) 159B、SHA256=5D5E6C23FA297BC53738A074074CB68064C1FFB7BEB71CE98F270F2077D14497（PE read-only/Capstone x86）。V9 search_unified_v9_20261023.py function 0x528DB0 はSTATIC、ABI未検証。

## 新規分岐 crosswalk（従来20Hのcandidate+0x1C gateは再計上しない）
0x528DF9 XOR ESI,ESI → 0x528DFB CMP DWORD [EBP+0x34C],ESI → 0x528E01 JE 0x5295BA。owner+0x34C==0では対象分岐全体へ進まない。
0x528E45 MOV EAX,[EBP+0x474] → 0x528E4B CMP EAX,ESI → 0x528E4D JNE 0x528E9A。mode==0のときだけ、この先の0x528E86 list配送枝へ進む。他modeは別枝であり全関数停止と誤認しない。
0x528E4F MOV EAX,[EBP+0x348] → 0x528E55 MOV ESI,[EAX] → 0x528E57 CMP ESI,EAX → 0x528E59 JE 0x5295BA。空listでは配送枝を抜ける。list head/sentinelの呼称はINFERRED。
既知20H: 0x528E67 MOV EAX,[ESI+8] → 0x528E6A CMP BYTE [EAX+0x1C],0 → 0x528E6E JNE 0x528E8B。非zero候補はこの回のCALLだけskipし、zeroなら0x528E86 CALL 0x569730。
新規ループ戻り: 0x528E8B MOV ESI,[ESI] → 0x528E8D CMP ESI,[EBP+0x348] → 0x528E93 JNE 0x528E67。非zero候補を飛ばしても後続要素の検査は続く。
この4ゲートのANDは「この特定0x528E86 siteへの到達」のSTATIC条件であり、すべての0x569730 caller・最終攻撃対象選択・実ゲーム行動には一般化できない。

## 重複・KB_CANDIDATE
先行 B-20261101-20H-T013-T024-528E86-ONEC-DISPATCH-GATE-01 のcandidate+0x1C条件と、既存0x569730/T013 2026-10-23 Troop配送は別発見として再計上しない。B所有T011/T012/T013/T024/T028 Markdown+HANDOFFで0x528DFB/0x528E01/0x528E45/0x528E4D/0x528E59の字句先行0件。意味的完全重複はVERIFY。
KB_CANDIDATE：owner B/T013,T024、VA 0x528DB0/0x528DFB/0x528E01/0x528E45/0x528E4D/0x528E59/0x528E6A/0x528E86/0x528E93、off owner+0x34C/+0x474/+0x348,candidate+0x1C。RAW bit interpretation ONLY。辞書名称・Unit/Troop型・holder/AI意味は未確定。専任KB統合担当が重複審査後にREFへ反映。
原作Golden要件：同一runの無改変原作EXE/DAT・SAVE/MAP/input/RNG、owner+0x34C=0/非0、mode0/他、list空/非空、candidate+0x1C=0/1/混在、それぞれのcall出現/候補順/翌tickの結果を独立観測。NOT RUN。
保留：03H保存成否UNKNOWN、07H B core4未回収、10/25原文欠落/Library byte差、旧SAFE134・HOLD21は未再監査。既安全拒否0x5710C0..0x571500および0x5769B0 XREF/内部には再接触せず、迂回もしない。新安全拒否0。
次：この4ゲートの登録形式をKB統合担当へ渡し、独立許可済み証拠で候補オブジェクト+0x1Cの意味と0x528DB0 caller 0x5272AB/0x528A04の上位条件を検証。T011召喚EXP/T012ダメージ・回復/T013最終対象/T024 AI/T028士気・敗走はP0/VERIFY。
