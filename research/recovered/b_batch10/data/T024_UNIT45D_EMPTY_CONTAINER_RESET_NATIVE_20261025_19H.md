# T024｜Unit+0x45D解除の二つの空コンテナ経路（2026-10-25 19時台）
ID: B-20261025-1910-T024-EMPTY-CONTAINER-45D-RESET-01
OWNER: B / T024。STATUS: STATIC-ORIGINAL-PE-ASM / STATIC-V3 / VERIFY / NOT READY。新B READY=0 / E MASTER=0 / Task DONE=0。
## ソース／前提
- Local Compact PC正本。原作 `rea_lab/targets/hakushin067_Vahren.exe` 実測 SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- V3 `verify_active_research_state_v3_20261022.py` 実行PASS_ACTIVE_V3_STATIC、input 14/14、PE E8=44889、JMP=6324、errors=[]、gameplay NOT_RUN。古いsearch.sqliteは歴史資料のみ。
- 検証済みE8 caller索引：0x56852D,0x5685F8 (owner 0x5684B0)→0x527ED0。0x4DE64D (owner 0x4DE410)→0x528870。呼出先E8 byteがV3原PE検証済み。間接/vtable完全性は未確定。
## 新規原作ASM分岐 A：0x00527ED0（136B・SHA256 FD5D61471A5D4A9084AF1091EBB7212AFD51C4973515635B27C6330CF3F266A0）
- 0x527EEB CMP [ESI+0x34C],0／JNE 0x527F27：候補数非0なら下記解除をスキップ。
- 0x527EF4 MOV ECX,[ESI+0x368]；0x527EFA SUB ECX,[ESI+0x364]；0x527F00 TEST ECX,0xFFFFFFFC／0x527F06 JNE 0x527F27。
- 両gate通過時のみ 0x527F0E MOV BYTE PTR [ESI+0x45D],0。続く0x527F15 CMP BYTE PTR [ESI+0x20C],0、非0時0x527F1Eで+0x20Cも0、0x527F22 CALL 0x4C5C40。
- +0x20Cが0でも+0x45D解除は先に起こる。続く0x527F29 CALL 0x41F850／0x527F2E CALL 0x56BA80は共有後処理。+0x1D引数次第で0x527EE6 CALL 0x4EC680も存在。
## 新規原作ASM分岐 B：0x00528870（427B、限定後半VA0x528955-0x528A19の197B SHA256 C1E67594302333B7882778CB53F5593A3CB0742CDE45507C799DC83018DEC6A1）
- 0x528877 MOV EAX,[ESI+0x368]；0x52887D SUB EAX,[ESI+0x364]；0x528884 TEST EAX,0xFFFFFFFC；0x528889 JLE 0x528955。整合した通常vectorでは空なら後半へ。
- 0x528955 CMP DWORD PTR [ESI+0x34C],0；0x52895C JE 0x528A12（AL0で復帰）。候補非0の場合だけ0x528968 MOV BYTE PTR [ESI+0x45D],0。
- この後は候補内を走査し、0x5289EF CALL 0x5E743Aを経て0x528A04 CALL 0x528DB0、0x528A09 AL=1で復帰する経路。上流の0x528889不成立なら別経路（0x52893D CALL 0x569730）へ進み、ここから一般の状態解除を推定しない。
## 解釈・重複境界
- +0x34C（候補カウント様）と+0x364/+0x368（4バイト要素span候補）がいずれも空の時に、Aは+0x45Dを0へ解除。Bはspan空かつ+0x34Cが非0の別パスで解除。関数が異なるため全体の同一tick排他的網羅は主張しない。
- 既B-20261025-1712の優先CALLおよび18Hの0x5271E2解除条件は既知で再計上0。今回は0x527F0Eと0x528968の独立する二つの解除経路、戻値AL境界、PE E8 callerを増分とする。
- V3 `search '0x45d'` の擬似C該当9関数では直接値1の代入を発見せず。ただしレジスタ別名・間接setter・未認識ASMを網羅せず「生成不能」とは判定しない。
- B owner T024/T028/HANDOFFの4主要VA（527ED0/528870/527F0E/528968）を事前literal検索、直接一致0。他lane/10-21回収22＋後続10/Library・OFFLINE成果の意味的完全照合はVERIFY。旧14HのFULL OFFLINE資料も未同期。
## Golden・安全・再開
- 原作無改変EXE＋20倍変更前DAT＋同一SAVE/MAP/input/RNGで、+34C=0/非0、span空/非空、+45D/+20C before/after、両caller到達時刻と後続AL、候補と可視挙動を観測。DESIGNED_NOT_RUN／Gameplay PASS0／strict MATCH0。
- 正規実ゲーム上のAI/士気意味、+45Dを1にするproducer、vector破損・例外・vtable/indirect副作用はVERIFY。次は0x5684B0の二つの呼出条件と0x4DE410の0x528870到達条件を既存証拠に照合し、+45D=1 producerの別名代入を合法限定調査。
- 今回は新Ghidra全解析なし、旧原作起動なし。原本/MASTER/他lane/REA/dev_lab/Work/Git/設定/schedules変更禁止。拒否済みVA/操作を再試行しない。
