# B-20261030-0916-T028-POSTRET-FULLERASE-PROVEN-01｜退却候補一時木の「全域削除」経路を呼出し実引数から証明
Owner B / T028 / 2026-10-30 09時台 JST。STATIC (原作ver0.67 ASM＋統合V9擬似C) / INFERRED / VERIFY / NOT READY。正式READY追加0。
## PC・復旧の先行確認
Desktop Commander Local Compact ONLINE。MASTER_LEDGER.md TASK QUEUE・E最新正式cp196/READY596旧値、ANALYSIS_LANES_PROTOCOL.md、LANE_B_HANDOFF.md、B5所有資料、RECOVERY_HUB.mdと先行08Hを先読。
元PE rea_lab/targets/hakushin067_Vahren.exe 2910720B、実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。統合V9 SQLite 141033472B、実SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable read-only quick_check=ok。root/search_indexのactive.lock検出なし、Java/Ghidraプロセス検出なし。
既存の安全関連SAFE134/HOLD21、B Library資料54件の1B差と10/25原文未回収は未解決。PC最新を見ていても未同期を回収済みとはしない。既拒否対象の再試行・迂回0。
## 今回の独立した原作ASM証明（0x5AC611のcaller-specific full-range）
0x5AC601: MOV EAX,[ESP+0x38]。この直前ESPをSとするとP=[S+0x38]（一時木head）。
0x5AC605: MOV ECX,[EAX] なので B=[P]（begin iterator）。0x5AC607 PUSH EAXでend=P、0x5AC608 PUSH ECXでbegin=Bを積む。
PUSH×2後ESP=S-8。0x5AC609 LEA ESI,[ESP+0x38]でESI=S+0x30（out iterator）、0x5AC60D LEA EAX,[ESP+0x3C]でEAX=S+0x34（tree localを指す）。0x5AC611 CALL 0x510850。
callee 0x510850 PUSH ECX、0x510851 MOV ECX,[ESP+8]でECX=B、0x510855 MOV EDX,[ESP+0xC]でEDX=P。0x51085A MOV EDI,EAX、0x51085C MOV EAX,[EDI+4]でEAX=[S+0x38]=P。
従って0x51085F CMP ECX,[EAX]はB==[P]で必ず一致し、0x510863 CMP EDX,EAXもP==Pで必ず一致する。直前にP/[P]を書換える命令はなく、正常な呼出し状態では両JNEは不成立。
**このcallerからは0x510867 CALL 0x44D0D0（全域erase）が確実に選択され、0x51087A以降のpartial route / 0x5108DF CALL 0x510C20は非到達。** 旧08Hの「全域または部分」をこのcallerだけ限定的に解消。他callerでpartialを否定しない。
0x510871 MOV EAX,ESI / 0x510873 MOV [ESI],ECXで出力iterator書戻し、0x510877 RET8。その後既知0x5AC61B一時木head解放、0x5AC627別容器cleanup、0x5AC5BD戻り値EBPへ。破棄済み参照を再利用しないための具体的な再実装境界。
## 原本バイト証跡・独立性
元PE Capstone x86 native再逆ASM（再Ghidraなし）。VA0x5AC601から0x15B SHA256=A53E7A689661E398DEE277860E8933E7B9EC90F7FAB50A7B85653FDF99E2F814、VA0x510850から0x25B SHA256=831A504E2009B2001517E43B86AED1B835CD83D7A6D338B3E6F024F28F2C3372。
B T028*.md＋HANDOFFで0x5AC605先行literal0、新ID先行0。0x5AC611・0x51085F・0x510863・0x44D0D0は旧08Hで既知として新規関数件数を増やさない。新規増分は「実引数から全域判定が必ず成立」の制御フロー証明。10/25旧原文・他lane意味重複はなおVERIFY。
## 未解明・必要Goldenと安全境界
全域消去自体はSTATIC。ただし原作Gameplayでmode1早期枝が起きる確率、未改変前DATでの合法到達、Spot+0xB8と退却通知・士気・翌tickへの影響はVERIFY。原作EXEと20倍改変前DAT・同SAVE/MAP/input/RNGを固定して、合法mode1分岐で一時木0/1/複数要素と返却先Spotおよびリソース状態を採るGoldenはDESIGNED_NOT_RUN。
原作実機Gameplay Golden PASS0、strict MATCH0、新規B正式READY0、E MASTER統合0、Task DONE0。STATIC/INFERRED/VERIFY/NOT READY。
次は0x5AC5BD返値の0x495050 callerでの最終分岐、0x597B00内部lookup比較（0x597B2F）と0x597A50容量count、T011召喚/EXP・T012 damage・T013最終対象・T024通常AI・T028本来の士気。
今回の先行読取ではT012_DAMAGE_MODEL.mdを誤想定しENOENT（OTHER）だったが、directoryで正式T012_BATTLE_CALC.mdを確認・読取してRECOVERED。安全拒否ではなく該当未保存成果なし。原本/MASTER/他lane/REA/dev_lab/Git/push/Work/設定/automation不変更。
