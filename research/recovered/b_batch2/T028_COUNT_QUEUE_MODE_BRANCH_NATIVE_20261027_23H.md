# B-20261027-2315-T028-COUNT-QUEUE-MODE-BRANCH-01｜死亡count記録の共通初期化と戦闘モード引数
日時: 2026-10-27 23:15 JST / owner B / Task T028（T013・T024参照のみ） / STATUS STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA + INFERRED + VERIFY / NOT READY
## 証拠・着手前の回収
- Desktop Commander Local Compact PC接続。MASTER_LEDGER（E最終既知checkpoint196、READY596）、ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF（22Hまで）を確認。10/25 14H OFFLINE全文・他lane意味的照合はなお未統合VERIFY。新規安全拒否0、旧拒否済VA・操作再試行/迂回0。
- 原本コピー rea_lab/targets/hakushin067_Vahren.exe 2,910,720B / 実測SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。legacy検索DB search.sqlite 53,927,936B / SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、immutable readonly quick_check=ok。active.lockなし。
- 原本PE read-only Capstone x86、既存検索CLIの function 0x4922A0 / 0x491870 / 0x521D90 / callers 0x4922A0を限定使用。Ghidra全解析、原本実行、REA起動なし。
## 新規の呼出元・条件分岐とフィールド由来
- 0x00491870 の枝は 0x4921C4 MOVZX EAX,BYTE [EBP+0x1EED43] → 0x4921CB PUSH EAX → 0x4921CC PUSH EBP → 0x4921CD CALL 0x4922A0。つまり既存manager自身と保持済みmode byteを渡す経路。
- 0x00521D90 内は 0x521DD2 XOR EBX,EBX でzeroを作り、Ghidra擬似C上「simplebattle」文字列判定の後、0x52227D CALL 0x43F330 / 0x522282 CMP AL,BL / 0x522284 JE 0x5222B4 で候補を選別。
- 0x522286 CMP DWORD [0x0087F6F0],1 → 等しい場合0x52228F MOV EDX,[EBP+0x194] / 0x522295 PUSH EBX(0) / 0x522296 PUSH EDX / 0x522297 CALL 0x4922A0。異なる場合0x5222A1 MOV EAX,[EBP+0x194] / 0x5222A7 PUSH 1 / 0x5222A9 PUSH EAX / 0x5222AA CALL同関数。
- よってこの呼出経路でmanagerへの参照は共通 [EBP+0x194] で、比較結果だけが第2引数 mode=0/1 を変える。global 0x87F6F0 の論理名・先行upstream到達条件はVERIFY。
- callee 0x4922D5で EBP=param1 manager、0x4922DCで AL=param2、0x4922E3 MOV BYTE [EBP+0x1EED43],AL。modeは永続したmanager fieldへ書かれる。0x4922FC XOR EBX,EBX なので後続CMPは0との比較。
## 初期化が分岐より先にあること
- callee内 0x4923BA [manager+0x1EEFA4]=end、0x4923C0 [manager+0x1EEFA0]=begin、0x4923C6/C8 begin==endなら析構skip、非空なら0x4923D0 CALL 0x417160→0x4923E0 CALL 0x415A60→0x4923E5 [manager+0x1EEFA4]=begin。これは22H既知、再計上しない。
- その**後** 0x4923EB CMP BYTE [manager+0x1EED43],BL(0) / 0x4923F1 JNE 0x492441。mode 0 は0x4923F5 heap allocate0x34→0x492417 CALL0x543A30でFadeOutSheet系生成→0x49243A indirect virtual CALL。mode非0 は0x492441以降→0x49244E CALL 0x432EE0ほか戦闘処理。両方のmodeで先にcount記録配列初期化へ到達する原本静的CFGを確認。
- このjoinは「どちらのmodeでもキュー初期化後に分岐する」ことを示すのみ。実際のゲーム中の到達・[Unit+0x1E0]とcallee managerの同一性・消去タイミング・読出consumer・red/blueの用途/士気への影響はVERIFY。
## nativeバイト照合・重複境界
- 元PE E8 5/5: 0x4921CD→0x4922A0 / 0x522297→0x4922A0 / 0x5222AA→0x4922A0 / 0x4923F5→0x5B6C2B / 0x49244E→0x432EE0（E8 rel32現物計算）。0x49243Aは間接CALLで同カウントに含めない。
- PE窓SHA: 0x52227D..0x5222B4(55B)=D9BD39F5F0A3BA79CF922D64A1B3DA7870C9B136F143B9614874697D631D641A; 0x4922D5..0x49231D(72B)=A08C41C8F3556A0F7C73AC08D4ED48F24F6E3D78F0B69B37B6C7737C2627D92D; 0x4923BA..0x4923F2(56B)=59A4E51FCD5412A653B872A4B0E1B705614B755682DD8A0BC83833E2ABC2A6C8。
- B5主資料/T028前22H詳細/HANDOFFの新site文字列 0x522286 / 0x4922E3 / 0x4923F1 / 0x4921C4 と新研究IDは先行直接一致0。22H既知0x4922A0と3 CALL site、21H count writer、22H record clearを二重計上しない。他lane・10/25 OFFLINE全文の意味dedupは未完成VERIFY。
## 実装影響・Golden・次の合法手順
- 互換実装では queue清掃をmode固有の下流処理に移すと分岐ごとに消去時点が変わる可能性。原作の「共通初期化→mode0 FadeOutSheet / mode!=0 event処理」の順序を保留仕様とする。
- Golden DESIGNED_NOT_RUN：無改変ver0.67 EXE・20倍変更前DAT・同SAVE/MAP/入力/RNGで合法dead_event=count/named、0x491870通常経路/0x521D90 simplebattle分岐、mode=0/1、record begin/end及び画面/戦闘/士気を観測。実機Original Gameplay PASS=0、strict MATCH=0。
- NEXT P0：0x4921C4 の0x1EED43 writer・0x522286全条件源、Unit+0x1E0と[0x521D90+0x194]同一実体の証明、0x1EEFA0レコード消費関数、T013最終対象選択、T024本来AI、T028士気/敗走。旧拒否対象には近付かない。
- 新正式READY0、E MASTER統合0、Task DONE0、NOT READY。B data/T028_MORALE.mdとevidence/LANE_B_HANDOFF.mdのみに追記する。原本/他lane/REA/dev_lab/Git/Work/設定/自動化無変更。
