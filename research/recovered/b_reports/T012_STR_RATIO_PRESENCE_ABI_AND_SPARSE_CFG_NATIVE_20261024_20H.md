# B/T012｜str_ratio存在判定のネイティブ引数契約とGhidra未所属5Bの流入監査
研究ID: B-20261024-20H-T012-STRRATIO-PRESENCE-ABI-GAP-CFG-01
日時: 2026-10-24 20時台 JST。Owner B/T012。状態 STATIC-ORIGINAL-PE-ASM＋STATIC-V3-REFS／VERIFY／NOT READY。
## 根拠・事前安全／復旧
Desktop Commander Local CompactでPC正本・MASTER cp196/旧READY596・レーン規約・B HANDOFF・T011/T012/T013/T024/T028・未同期回収索引を先読。B既存拒否0x5710C0..0x571500、0x514C50、0x5769B0 XREF、08:10/14:14拒否文書/操作を再試行・迂回していない。
2026-10-21回収済22ファイルと後発10研究のID単位意味照合、2026-10-24 10H～18H Library成果のPC全件同期、Library訂正版2件は未完。旧安全拒否は解除しない。
検索正本 CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json はV3を指す。既存 read-only guard `verify_active_research_state_v3_20261022.py`=PASS_ACTIVE_V3_STATIC、14入力SHA一致、E8直接CALL44889、E9/EB JMP6324、errors=[]、gameplay NOT_RUN。旧20261021検索DBとは混同しない。
対象原作rea_lab/targets/hakushin067_Vahren.exe現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原作PEをバイト読みしただけで原作起動・変更、新Ghidra/REAなし。
## 新しいSTATIC差分1｜str_ratio存在確認のレジスタ／スタックABI
EXE 0x0059CDAA PUSH EBX, 0x0059CDAB PUSH ESI, 0x0059CDAC MOV EDX,0x00625040、0x0059CDB7 MOV ECX,0x0062504C、0x0059CDCA CALL 0x00464290、0x0059CDCF TEST AL,AL、0x0059CDD1 JE 0x0059CE3A。PE生文字列0x00625040=`str_ratio`、0x0062504C=`skill`。
callee 0x004642C5/[ESP+0x94]と0x004642CC/[ESP+0x98]は2つのstack引数、0x004642D7 MOV [ESP+0x1C],EDXは`str_ratio`文字列ポインタを保存。0x0046442A MOV EDI,[ESP+0x1C]→0x0046442E CMP EDI,0→0x00464430 JNE 0x00464442。従ってこの0x59CDCA呼出しではEDX!=NULLで2次属性検索側へ進む（手前の検索失敗分岐は別）。
存在確認AL=0のとき0x0059CE3Aへ飛び、0x0059CDC2 FLD1→0x0059CDC4で初期化したSkill+0x288=1.0をこの局所経路では維持。AL!=0なら0x0059CDE1 MOV EDX,0x00625054（同じ文字列`str_ratio`）→0x0059CDE8 CALL 0x004647D0→0x0059CDED FILD [EAX+0x20]→0x0059CDF5 係数乗算→0x0059CDFB Skill+0x288へ格納。存在確認と値取得は異なる文字列VAを使うが生文字列は一致。
## 新しいSTATIC差分2｜2段検索・50回境界・未所属5Bのincoming
0x004643FA以降の初期lookupは0x0046440D MOV EAX,[ESP+0x14]→0x00464411 CMP EAX,ESI(header)→0x00464413 JNE 0x0046442Aで候補を確保。header一致なら失敗復帰側へ。0x0046442EのEDX非NULLなら0x00464442 MOV ESI,[EAX+0x28]→0x00464445 counter=0→0x00464449 JMP 0x00464454。
2段目loop 0x004644BC MOV EAX,[ESI+4](header)、0x004644BF CMP [ESP+0x24],EAX、0x004644C3 JNE 0x004645A0→0x004645B3 MOV AL,1は該当ノード検出側。未検出なら親super探索を進める。0x00464548 CMP EAX,[ESI+4]→0x0046454B JE 0x00464567は親候補不在、0x00464554 INC counter→0x00464559 CMP counter,0x32→0x0046455C JL 0x00464450。終了失敗枝0x0046457A XOR AL,AL。初回基点lookupと内側50反復を混同しない。
19時台既存のGhidra body gap 0x0046444B..0x0046444F=EB 03 8D 49 00は再発見扱いにしない。今回V3 `refs-to`で0x0046444B=0件、0x0046444D=0件、0x00464454は0x00464449から1件。原作PE [0x00464290..0x004645B6]を命令境界からCapstone走査し、gap入口0x0046444B/4Dを宛先とする直接Jcc/JMPは0件。loop復帰は0x0046455C→0x00464450。
結論：この5Bは現在列挙できる局所直接CFGから到達しない孤立命令列の候補であり、Ghidraが末尾5Bを取りこぼした証拠ではない。関数外の未認識・間接分岐／例外起点をゼロと証明したわけではない（VERIFY）。
## バイト根拠と非重複
原作PE VA 0x00464290..0x004645B6（807B）のSHA256=EE8E10D45114F34C965EC3924291DCE60F2DC7A349642C358F5199D9DEBEB543。
原作PE VA 0x0059CDA3..0x0059CE51（175B）のSHA256=62F84863FC9B4A64F5586067B773133BB1B278A2B6A17DF0915367B602A16188。
原作PE VA 0x00625030..0x0062507F（80B）のSHA256=6B8EC3AA404DB747E828E27012DFD93EDFDEDF1791C06068699C0065A8F020C4。
既B-20261024-17HのAL戻値/存在と値の別関数/50上限、18H肯定末尾、19H sparse body2範囲・gapバイトは再計上0。新規はcallsiteのECX/EDXとstack対応、二つの同値str_ratio literal、現存V3 refs-toと全関数直接branchのgap流入0、初回入口と50反復のCFG細分。PC最新B HANDOFFとowner文書3点で同一VAの当該新結合記録を見つけなかったが、先行OFFLINE研究との意味重複はVERIFY。
## 実機受入・次回
同一未改変原作EXE、X20強化前DAT、同SAVE/MAP/操作/RNGを固定。Skillのstr_ratio欠損/明示0/親のみ/直接指定、50反復付近の合法継承実到達について取得AL・実最終倍率・ダメージ/HP/tickを比較する。Golden条件DESIGNED/NOT RUN。旧Gameplay Golden PASS=0、strict MATCH=0、新正式READY=0、E MASTER統合=0、Task DONE増分=0。
次の許可された検索先は0x00464450内の属性検索と0x0046454B親欠損処理のvalue getter(0x004647D0)との非対称性、親深さの境界、合法DATの実使用例。必要な場合も原作ASM・既索引を軽量に読取のみ。
保存先はB所有dataのみ。MASTER/他lane/REA/dev_lab/Git/Work/原本/SAVE/設定/スケジュールは書込対象外。
