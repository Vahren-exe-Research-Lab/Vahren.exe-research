# 迫真戦記 新B｜T013/T024 0x528DB0 の直接配送前 +0x1C gate と並べ替え後配送の3 E8 site（2026-11-01 20H JST）

研究ID: B-20261101-20H-T013-T024-528E86-ONEC-DISPATCH-GATE-01
owner: B/T013（主）・T024（連関）
status: STATIC_NATIVE / STATIC_V9 / INFERRED / VERIFY / NOT READY。原作実機 Golden PASS=0、strict MATCH=0、DYNAMIC=0、正式新READY=0。
新発見を狭く限定: 既存の 0x528DB0 → 0x569730、二つの距離ソート後 CALL (0x529750/0x529921) と、10/23の T013 Troop 配送研究は先行成果。**今回の新規差分は先行 B 5-owner markdown/HANDOFF に字句未掲載の 0x528E86 入口と、直前 [candidate+0x1C] バイト条件の原作ASM証拠、および同一owner内3 CALL経路の引数準備差のcrosswalk。** 0x569730本体の機能全体、Unit+0x1BC sort、0x5699C0候補生成、距離ソート自体を再発見として計上しない。

## 出典・一次根拠
Original PE (read-only): rea_lab/targets/hakushin067_Vahren.exe / SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（本run独立実バイト再計算一致）。原作EXE未起動。
V9 composite DB (read-only): rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite / SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（本run実バイト再計算一致）。旧 README/BUILD_MANIFEST はENOENTであり使用せず、LATEST JSON + 00_START_HERE_UNIFIED_V9_20261023.mdがV9を指定。
V9 read-only CLI `callers 0x569730`: E8 direct CALL合計15 site、そのうち owner function 0x528DB0 の3 site=0x528E86、0x529750、0x529921。 `function 0x569730` は333 bytes・ABI未検証・Ghidra擬似CはSTATIC。原作PE限定Capstone 32bit逆ASMを本runの3窓に適用。

## NEW：先頭リスト由来の条件付き配送
PE window [0x528E53,0x528E9D) (74B), SHA256 08EAB802FA80394DE0B271FBE2B0879A6390C16B74A823E996E579FEE09921A8。
- 0x528E67 MOV EAX,[ESI+8] → 0x528E6A CMP BYTE PTR [EAX+0x1C],0 → 0x528E6E JNE 0x528E8B。
- [+0x1C]!=0 ならこのリスト要素の 0x528E86 CALL をskipし、0x528E8B MOV ESI,[ESI] で次要素へ進む。
- [+0x1C]==0 なら 0x528E70 FLD QWORD [ESP+0xF8] → 0x528E77 SUB ESP,8 / 0x528E7A FSTP [ESP]、0x528E7D PUSH1、0x528E7F PUSH1、0x528E81 PUSH0、0x528E83 PUSH EDI、0x528E84 PUSH EBX、0x528E85 PUSH EAX → 0x528E86 E8 A5 08 04 00 = CALL 0x569730。
- 0x528E8D CMP ESI,[EBP+0x348] はループのsentinel照合。candidateの実型・+0x1Cの語義は未確定（TroopかUnitの最終同定もVERIFY）。「生存」「士気」「再配布済み」と命名しない。

## KNOWN CALLS 再接続：別々の並べ替え後配送
PE window [0x529724,0x52975B) (55B), SHA256 303C43BB763C0343AFD5DB3B3E28011C04FA1B238F0C08E0EE9CA0C35128BB16。
0x52972B/2D/2F PUSH1/1/0、0x529731 E8 -> 0x5D1B80(ftol)、0x529742 E8 -> 0x5D1B80、0x52974B MOV EDX,[EDI+8]、0x529750 E8 DB FF 03 00 -> 0x569730。
PE window [0x5298FA,0x52992E) (52B), SHA256 6A07DC885952A1FB01E9C92DBE469294B99EB49DDCEADB9876D878CDB5D4F6B3。
0x5298FC/FE/900 PUSH1/1/0、0x529902 E8 -> ftol、0x529913 E8 -> ftol、0x52991C MOV EDX,[ESI+8]、0x529921 E8 0A FE 03 00 -> 0x569730。
**区別**：0x528E86は事前のcandidate+0x1C分岐とqword stack源を持つ。0x529750/921は先行18/19Hの変換後浮動座標・ftol連鎖の結果を配送に渡す。後2siteに+0x1C gateがどの上位経路にも存在しないという一般化はしていない。param ABI（push 1/1/0と0x569730疑似C param_6の対応）、実座標、真の攻撃対象、乱数/副作用はVERIFY。

## 重複・安全・kb
先行B/T013: B-20261023-18H-T013-TROOP-DISPATCH-ROUTE-01（0x569730の動作/flag既知）、B-20261023-19H-T013-TROOP-POSITION-SCRATCH-01、20H-TROOP-SORT-1BC-NATIVE-01、21H-SORTED-PAIR-COMPACTION-01。先行B/T011,T024: B-OFFLINE-20261101-13H-T011-T024-DISTANCE-SORT-MODE-GATE-01、B-20261101-18H-T024-DUAL-REFERENCE-COORD-AND-PC-RESTORE-01、B-20261101-19H-T024-GROUP-REF-FTOL-YFLIP-CROSSJOIN-01。V9 E8 3/3確認、原PE byte 3/3一致。新住所 0x528E86/0x528E6A は既存B5owner markdown+HANDOFFの単純字句検索0件（他owner意味重複・未保存07Hとは全量照合でない）。
Bの既存安全拒否 0x5769B0 XREF/内部と 0x5710C0..0x571500 等は手続き禁止を維持。V9の無害な caller 0x569730 は確認したが、0x5769B0への独立query・深掘りは行わない。MASTER/他lane/REA/共有knowledge/Git/原本/設定/automation変更禁止。既HOLD21の現物全件検査なし、SAFE134も本run全件再検査なし。

## KB_CANDIDATE / 実装に必要な条件
KB候補: 言及対象 0x528DB0 / 0x528E6A / 0x528E86 / 0x569730 / 0x529750 / 0x529921 / 0x5D1B80、候補オブジェクト+0x1C、owner B/T013,T024。新シンボル名は確定せず、GitHub REF_BATTLE_AI_MORALE へ「Troop配送の事前gate/別座標producer入力」を条件付きで追記する候補とする。既登録 ftol は二重追加禁止。担当Bは報告と機械可読 TSV / B-own HANDOFF まで、専任KB統合担当がSHA/証拠・分類を検証して承認。
Golden必要条件: 正規ver0.67 EXE+無改変DAT+同run SAVE/MAP/input/RNG、候補+0x1Cが0/1、候補list 0/1/複数、モード3/非モード3で各CALL site/実配送順/次tick行動を個別receiptで照合。NOT RUN、Golden PASS0/strict MATCH0。T011召喚EXP/T012ダメージ/T013最終対象/T024全AI/T028士気・敗走のP0は未解明。
Recovery: 11/01 07H B core4はPC未回収、03H保存UNKNOWN、10/25原文欠落、Library byte差54/SAFE134 HOLD21は既存と区別。今回Library 07H名検索は対象原文不発見（「完全不存在」ではない）。
次回: 0x528DB0の早期gatingを下流の合法イベント観測へ接続するか、0x569730の**許可済み**上流選択条件から別の未解明P0を調査。拒否済 0x5769B0 XREF/内部の別経路調査は禁止。
