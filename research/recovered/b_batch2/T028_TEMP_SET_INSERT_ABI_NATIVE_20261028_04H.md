# B-20261028-0410-T028-TEMP-SET-INSERT-ABI-01｜T028 二次木フラグで選ばれる一時集合更新の実体（04H）
Status: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。Owner B/T028。E MASTER未統合。
## 出典・保全と非重複
- Local Compact ONLINE。MASTER最終正式既知checkpoint196/READY596、レーン規約、B5 owner、HANDOFF/拒否・未同期索引を確認。2026-10-25 14H OFFLINE全文・他lane完全意味dedupは未了、既安全拒否の再試行・迂回なし。
- 対象read-only原作 PE 2,910,720B SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧検索DB 53,927,936B SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、SQLite immutable read-only quick_check=ok。
- search.py function 0x498EE0 / 0x565780 / 0x40EBE0 / 0x5AF0F0の抽出済み擬似Cを読取。原作PEのCapstone x86-32限定ASMで主要命令を独立照合。Ghidra全面再解析・REA・原作実機起動なし。
- B所有T011/T012/T013/T024/T028 Markdown317件＋B HANDOFF 1件（計318）を読取検索し、新site 0x498F1C/0x498F3F/0x498F5F/0x5657A7/0x40EC03/0x5AF1AD/0x498F11の直接出現は各0。前03Hの2 CALL siteとN=0/1/2は既知で再加算せず、新規はcallee内部の正確なデータ構造・分岐・呼出ABI。
## 原作ASM新規確定
- 0x498EE0 は uint32キーの開始・終端ポインタを引数として受け、0x498EE7/ECで等しければreturn、0x498F70～0x498F7Fで入力+4ずつ巡回。this様集合ポインタは EAX→ESI。
- 集合+0x08が0なら0x498EFF→0x498F00 CALL 0x565780で新ノード作成、0x498F11 CALL 0x40EBE0で挿入。非空の場合0x498F18～0x498F21で木端のキーと比較し、境界より外なら0x498F24/0x498F35の高速挿入。別の境界側は0x498F3C～0x498F58で比較・高速挿入。境界以外は0x498F5F→0x498F65 CALL 0x5AF0F0一般挿入・既存キー判定経路。
- 0x565780 は 0x565783 PUSH 0x14→0x565785 CALL 0x5B6C2Bで20Bノード確保、0x565793..A1で子・親様ポインタをheaderへ初期化、0x5657A7で+0x10の2byteフラグを0、0x5657AF..B5で入力uint32キーをnode+0x0Cへコピー。
- 0x40EBE0 は 0x40EBE0 [EDI+8]サイズ読込→0x40EC03 INC→0x40EC04格納、0x40EC07以降で木ノードを接続し赤黒木色/回転を処理（Ghidraおよびnative確認）。この加算は**集合サイズの増加**で、死亡数・士気・Unit経験値の加算ではない。
- 0x5AF0F0 は node+0x0Cのキーを比較して木探索、必要なら0x565780/0x40EBE0経由で追加し、0x5AF15B/5D・0x5AF19C/9Eでoutparam node+flag=1、既存の場合0x5AF1AB/ADでnode+flag=0。重複キー経路を含む通常集合挿入である。
- 03Hで確認済み0x493AB6 N>=1→0x493AD1 0x498EE0(EAX=&[ESP+0x7C])、0x493AD6 N==2→0x493AF4同関数(EAX=&[ESP+0xA0])。両者は異なる一時的な**整数キー赤黒木集合**の構築/更新を指し、2回の死亡/士気加算と読む根拠はない。keyのゲーム上の型・用途、2集合の後続consumerはVERIFY。
## 検証
- 原作E8 REL32 7/7一致: 0x498F00/24/47→0x565780、0x498F11/35/58→0x40EBE0、0x498F65→0x5AF0F0。03H CALL0x493AD1/AF4→0x498EE0は既証拠として再計上0。
- 原作0x498EE0～0x498F8D (174B) SHA256 24CF783E378CB85F0B5CD315E14AB3EF727E2592E968AA48E17E6A6F1C0D0994。0x565780(102B) SHA ABFFACCAE70611665083D972E40D5567F9A1A23B005462CB22F193A59306E825。0x5AF0F0(200B) SHA 21DC09A10F3E7B959A7BC7BCAA844449C579203599879A61AC2EB3014F4F7D3C。
## P0・受入境界
- 2集合のキーproducer、同一managerの実体、+0x1EED34索引木のwriterとnode+0x14論理名、2集合のconsumer→実戦モード/士気/敗走との関係はVERIFY。T013最終対象選択、T024戦闘AI、T011召喚親・経験値帰属、T012効果/RNGも未解明P0として維持。
- Golden: 無改変ver0.67原作 EXE＋20倍強化前DAT＋同一SAVE/MAP/入力/RNG、索引木key一致/不一致・+0x14=0/非0・一時集合キー重複/境界/内部値で比較する原作合法観測DESIGNED_NOT_RUN。Gameplay PASS0 / strict MATCH0 / 新B READY0 / E MASTER統合0 / Task DONE増加0。
- 安全拒否既存 VA0x5710C0..0x571500、0x58021E..0x580340および拒否済み操作は再試行・迂回なし。新規安全拒否0、接続障害0、実行エラー0。原本/REA/dev_lab/他lane/MASTER/Git/Work/設定/スケジュール非変更。