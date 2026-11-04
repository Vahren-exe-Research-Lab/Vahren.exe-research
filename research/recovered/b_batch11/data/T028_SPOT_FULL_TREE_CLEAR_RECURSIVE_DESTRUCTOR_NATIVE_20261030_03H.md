# T028｜退却Spot索引の全木削除：再帰／反復デストラクタとヘッダ復位（03H）
研究ID: B-20261030-0308-T028-FULL-TREE-CLEAR-POSTORDER-01
時刻: 2026-10-30 03時台 JST｜owner B/T028｜STATIC ORIGINAL ASM / INFERRED / VERIFY / NOT READY
## 証拠／回復 preflight
Desktop Commander Local Compact ONLINE。E MASTER旧公式cp196/READY596、レーン規約、B5 owner、B HANDOFF、復旧HUB・既存拒否索引と02H研究原文をread-only照合。新B READY0。
旧SAFE134/HOLD21、Library B147うち54件の1B差、10/25原文欠落はOPEN。旧README/BUILD_MANIFESTは既知ENOENT=OTHER、正規V9専用CLIを使用。既拒否操作・0x5710C0..0x571500は未接触。
原作read-only解析copy rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 DB実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE／immutable SQLite quick_check=ok。Ghidra・Java・active.lock無し、ゲーム実行無し。
## 新規原作native：全木削除の反復・再帰、allocator
0x415CF0のfull-range gate（first=[head+0]かつlast=head）が成立すると、0x415D04 root=[head+4]→0x415D0A CALL 0x416870。full-range入口自体は01H研究で既知、新規計上0。
0x416870（86bytes）0x41687E CMP byte ptr [ESI+0x29],0 / 0x416881 JNE 0x4168BF：nil/sentinel候補ならただちに帰還。既存0x416220のinvalid-iterator gateとは別。
有効nodeでは0x416883 EAX=[EDI+8]、0x416889 CALL 0x416870（片枝を再帰）；次に0x416892 EDI=[EDI]、0x4168B8 ESI=EDI、0x4168BA/BDで他枝をwhile型に繰り返す。
各node解放は0x41688E CMP [ESI+0x20],0x10。容量 >=16なら0x416899→0x41689A CALL 0x5B6BBBで[ESI+0xC]の文字列heapを先に解放、<16はこのfreeを省略。
共通で0x4168A2 capacity=0xF、0x4168A9 length=0、0x4168AD inline byte=0、0x4168B0 CALL 0x5B6BBBでnode本体を解放。末尾0x4168C3 RET 4。0x416220の部分削除helperはこの全木pathでは直接CALLされない。
0x415D0F..0x415D1Dはheadの3リンクをhead自身へ戻し、0x415D23 container+8=countを0に設定。ノードごとの逐次count--ではなく、全消去後の一括reset。0x415D2C/2Eは出力iteratorへ更新されたheadリンクを格納。
V9 callers 0x416870 は36 E8 matches（自再帰を含む）でgeneric tree destructorと推定。今回のretreat経路0x415D0Aへの接続は原PEでも確認。ただし36件の各caller意味・対象container同一性はVERIFY。
## 実装境界／出典／非重複
全木clearは「各node片枝再帰＋もう片枝反復→heap string条件解放→node解放→head/count初期化」であり、元の退却Spot容量予約(+0xB8)をこのcallee自身が減算する命令は無い。別経路0x495580による減算との前後・同一オブジェクト性は未確定、再実装で合算しない。
PE byte-window SHA256: 0x416870 /86B = 392FC0BC3857D9DB4A4EDE2E00379C8D875E1CD7FA0C10D81586DAE11F997498。0x415CF0 /190B=1FB1E8D382DE998CE5CD5A88D6348CE7BBAE5F649730839E0246C26EA4FA0FDE。
原作ASMはpefile VA→RVAを変換後Capstoneで局所逆ASM。V9擬似Cでループ形を照合。B T011/T012/T013/T024/T028 top-level Markdown＋HANDOFF 373件で新0x416889/0x41689A/0x4168B0/0x4168BF先行文字列0；0x415D12/0x415D23は01H資料に既出のため再計上0。10/25欠落原文・他ownerの意味的重複VERIFY。
初回原作PEのPython stdin Unicode pathが'????'になりOSError22=OTHER。禁じられた操作ではなく、同一Localの環境変数でパスを受ける正常なread-only処理へ修正・成功。安全拒否0／迂回0。
## Golden／再開
無改変原作EXE+20倍改変前DAT、同SAVE/MAP/input/RNGでindex tree空/1/複数、キー長15/16/17、nil/valid、全range/部分range、retreat vector0/1/2、容量+0xB8変化と可視敗走・翌tickをbefore/after観測するまでDESIGNED_NOT_RUN。
Original Gameplay Golden PASS0、strict MATCH0、新B正式READY0、E MASTER統合0、Task DONE0。STATIC / INFERRED / VERIFY / NOT READY。
次は0x495580後のUnit+0x1B4参照寿命／0x597A50 linked +0x78型（T028）、0x44CF80からT024 AIへの接続、T011 summon EXP、T012 damage、T013 final target。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/automationは書込禁止・不変更。
