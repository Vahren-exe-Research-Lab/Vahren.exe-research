# T024｜選択リンク解除後の条件再評価・2種の後処理とtail JMP（2026-10-25 21時台）
ID: B-20261025-2117-T024-POSTUNLINK-ZERO-TAILJMP-01
OWNER: B / T024。STATE: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。
## 接続・根拠・境界
- Desktop Commander Local Compact PC接続成功。MASTER既存正式checkpoint196/READY596、LANES_PROTOCOL・LANE_B_HANDOFF・B担当5 owner・未同期/拒否復旧と直前19/20H詳細を照合。14H OFFLINE全文および旧回収22+後続10+Library2の全ID意味照合は未完。13H詳細は15Hに回収済。
- PE: rea_lab/targets/hakushin067_Vahren.exe、現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search.sqlite現物SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF＝manifest。V3再検証なし。
- 既存search.py function 0x527EA0/0x527ED0/0x4EC680、callersを読み、原作PEの局所Capstoneで命令境界を独立照合。0x527EA0 44B SHA256 2D8FB23D5F064FD6AD5CD874DD56E264FD79E188F9658A2D0D23B2C56CE82ADE；0x527ED0 136B SHA256 FD5D61471A5D4A9084AF1091EBB7212AFD51C4973515635B27C6330CF3F266A0；0x4EC680 55B SHA256 5D01A76241BE501D0C39BC93132496B8682B71B94AC45787E98903DA6495956B。
- Vahren.exeプロセスPID22984稼働を読取専用で確認。原作ゲームは本runで起動/改変なし。既拒否（0x5710C0..0x571500等）への再試行・迂回なし。PC高負荷解析・新Ghidra/REAなし。
## NEW 1: 0x527ED0は+0x34Cの空判定より前にリンクを削除し得る
- 0x527ED1 MOV EAX,[ESP+8]（渡されたownerポインタ）；0x527ED5 CMP BYTE PTR [EAX+0x1D],0；+0x1D==0側で0x527EDC LEA EDI,[ESI+0x348]、0x527EE2 LEA EAX,[ESP+0xC]（owner引数のstack slotアドレス）、0x527EE6 CALL 0x4EC680。
- 0x4EC680はEDIが指す循環双方向リストを走査。0x4EC690 CMP [ESI+8],EBP（EBP=*EAX=owner）の一致要素を0x4EC695..69Dでunlink、0x4EC6A0 CALL 0x5B6BBBでnode解放、0x4EC6A8 DEC DWORD PTR [EDI+4]（owner状況の+0x34Cに対応）。一致が複数あれば継続走査。
- その後0x527EEBで[ESI+0x34C]==0、0x527F00で+368-+364 span空を評価し、成立時0x527F0E +45D=0／+20C非0なら0x527F1E reset→0x527F22 CALL0x4C5C40。
- 重要: +0x1D==0時の+0x34C判定は削除前ではなく削除後の値。入口時count>0でも今回のowner削除で0になり、span空なら+0x45D解除に進む可能性がある。削除する対象はowner pointerキー一致ノード、Unit死亡専用かはVERIFY。
## NEW 2: 0x527EA0と0x527ED0は異なるABI・状態変更
- 0x527EA0：0x527EA0 PUSH1→0x527EA2 CALL0x41F850、0x527EA7 CALL0x56BA80、0x527EBB CALL EDX(vtable slot+0xC)、AL非0なら0x527EC6 CALL0x401BE0、0x527ECB RET。自関数内に+45D/+34C書込なし。
- 0x527ED0：上記owner除去・場合により+45D/+20C reset後、0x527F27 PUSH1→0x527F29 CALL0x41F850、0x527F2E CALL0x56BA80、0x527F43 CALL EAX(vtable slot+0xC)、AL非0→0x527F4E CALL0x401BE0、0x527F55 RET4。
- 両者は末尾の表示/通知候補関数群を共有するが、呼出ABIは0x527EA0=RET、0x527ED0=RET4。render/UI具体効果・仮想CALL実先・+45D状態のゲーム上意味はVERIFY。
## NEW 3: 0x5685C5はCALLではなくtail JMP（旧callgraph分類訂正）
- 元0x5684B0のcount>0、先頭Unit+0x8C==0 && +0x1F8!=0経路：0x5685BF POP ESI、0x5685C0 POP EBP、0x5685C1 POP EBX、0x5685C2 ADD ESP,8、0x5685C5 JMP 0x527EA0。これはスタック復元後のtail jumpであり、E8 CALLではない。0x527EA0 RETで元0x5684B0 callerへ復帰する契約。
- 旧Ghidra search.py callers 0x527EA0は0x5685C5をUNCONDITIONAL_CALLと記載するが、元原作PEではJMP。CALL siteではなくJMP siteとして扱う。source index由来のref_typeのみで命令種別を断定しない。以前20HのJMP表記は正しい。
- 0x56852C PUSH EDI→0x56852D CALL0x527ED0（callee RET4）とは独立のABIであり、hook/再実装時に無条件同一関数へ統合しない。
## 既存IDとの非重複・制約・次
- 19Hの単純な+34C==0/+45D reset、20HのTroop分岐・2 callerは再計上0。新規増分は前処理でのowner鍵unlink（+34C減少後判定）、2後処理のRET対RET4／共通UI系CALL、0x5685C5のtail JMPと旧CALL参照索引の不一致。既存T024/T028/HANDOFF literal調査で0x527EDC/0x5685C5は前20H概要のみ、unlink count変化/RET契約の詳細なし。他lane/未同期全文の意味重複はVERIFY。
- Golden: 無改変原作EXE＋20倍改変前DAT＋同一SAVE/MAP/input/RNGで、owner+1D=0/1、+348/34Cリンク候補数1/複数/0・一致/不一致、+364/368 empty/nonempty、+45D/+20C before/after、0x527EA0 tail到達と0x527ED0 call到達を別runで観測。後続レンダラ・次tick結果も取得する。DESIGNED_NOT_RUN；旧原作Gameplay actual PASS0、strict MATCH0、新B READY0、MASTER統合0、Task DONE0。
- 次P0: 0x56BA80の副作用・0x4EC680 owner同一性／ノード寿命、+1D/+1C writer、0x527EA0へ至る別callerとインゲーム上の意味、+45D=1 writer。安全拒否既存範囲には非介入。
- PC保存・読み戻しreceiptはB HANDOFFに別追記して確定。原本/他lane/MASTER/REA/dev_lab/Git/Work/設定/スケジュール書込0。STATE: STATIC / VERIFY / NOT READY。
