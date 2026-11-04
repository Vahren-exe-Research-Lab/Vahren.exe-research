# B-20261028-06H-T028-LOYAL-DOWN-POINTER-KEY-GATE-01｜戦闘後候補除外の実キーと loyal_down 消費（STATIC/INFERRED/VERIFY/NOT READY）
Owner: B/T028（T012異型offset注意）。2026-10-28 06H。新規正式READY0 / E MASTER統合0 / Task DONE0。
## PRECHECK / 出典
- Desktop Commander Local Compact ONLINE。MASTER最終公式確認 cp196/READY596、分析レーン規約、B5 owner、B HANDOFF、未同期回収索引、旧拒否を照合。10/25 14H未同期全文と他laneの完全意味重複はVERIFY。
- 原作 ver0.67 Vahren.exe 2,910,720B 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本は読取専用。
- 現行V3 search_current.py function 0x00493630、0x0046F4C0（出力はSTATIC擬似C）。V3 guard PASS_ACTIVE_V3_STATIC、14 input SHA一致、E8=44889/JMP=6324、gameplay=NOT_RUN。旧search.sqlite/README/BUILD_MANIFESTは履歴資料として読取。
- PE x86-32 Capstone限定ASM、オリジナルRDATA文字列、原作正規化DAT context.dat行232-235を独立照合。Ghidra再解析・原作実行なし。
## 新規原作ASM（05H既存の5除外gateを再計上しない）
- 五経路で名前解決 0x467DE0 の戻値EAXをESIと[ESP+0x1C]へ保存し、EBX=&[ESP+0x1C]として 0x44D070 を呼ぶ：0x4948FD/FF→0x49490B/17、0x494FFB/FD→0x495009/15、0x495252/54→0x495260/6C、0x49588D/8F→0x49589B/A7、0x495A03/05→0x495A11/1D。局所lookupの比較対象は解決済み**32bitポインタ値そのもの**（STATIC）。集合挿入元の全要素も同ポインタか、再利用時の同一性はVERIFY。
- 0x494858で第1経路はparam_4==0をgate、0x494869 PUSH 0xA（既定10）・0x49486C MOV ECX,0x632270（原作ASCII “loyal_down”）・0x494871 CALL 0x46F4C0。正規化原作 context.dat 行233は loyal_down = 10 で値と一致。
- 0x494881 CALL 0x5916E0、戻りが非NULLなら0x49488A..95で減算量に (100-[EAX+0xC4]) を加算する経路がある。0x5916E0戻値の型・+0xC4意味・符号/overflowはVERIFY。
- 非memberかつ名前解決成功時 0x494931 CALL 0x5882F0→4byte参照配列を走査。0x494968..84で候補byte+0x77==0、byte+0x75!=0、byte+0x7A==0、signed dword+0x80<3 のゲートを満たす候補だけ0x494986で [candidate+0xC0]-=EDI。0x49498E SETS/0x494991 DEC/0x494992 AND/0x494998 MOVで、SUB結果が負なら0にする符号ゲート。32bit符号overflow端はVERIFY。
- 対応する他方の処理でも0x4958A7集合非member時 0x4958C1 CALL0x5882F0→0x4958F4..0x495910同じbyte/整数条件→0x495916 SUB [candidate+0xC0],EDX→0x49591E SETS→0x495928 store。
- ほかのモード側0x4957B3は文字列win_gain（0x632314,既定50）、0x4957F1はloyal_up（0x632320,既定10）、0x495805は別文字列loyal_down（0x63232C,既定10）を0x46F4C0へ渡す。原作context.dat行232/233はloyal_up=10/loyal_down=10。各値が誰へ増減するかは未確定。
## 既存T012との重要な型境界
- T012_BATTLE_CALC.md既存B-20261012-1920-02は戦闘実行オブジェクトUnit+0xC0をparaと記録。今回の0x493630はloyal_down文字列を伴う**別オブジェクト／別局面候補**。同じ+0xC0だけで忠誠度ともparaとも同定しない（field alias/type VERIFY）。忠誠度関連の後処理という解釈はINFERRED、直接書込と設定文字列はSTATIC。
- 05Hで確定済みの集合5回lookup/除外や0x467DE0+0x1A4 backlinkは新規採番0。今回の増分は返却ポインタを5箇所でキーにする実ABI、loyal_down/win_gain/loyal_upのsource-native literal、非member後の+0xC0減算＋下限0処理への接続。
## 証拠・検証と次回
- 原作E8 REL32 site独立照合 9/9：0x494871,0x4948F8,0x494917,0x494931,0x4957B3,0x4957F1,0x495805,0x4958A7,0x4958C1。
- 原作PE窓SHA：0x4948F5..0x4949B6=0DCDE807671412920D9AC1DF3034790E76E53E37D0B29A6557A299707A0618E9、0x4958AC..0x495927=5429D1795822C2A9F2739ED504C6216223B438D745100A29728EC94AF266F6A0、0x494858..0x4948AB=C9C53B555C82640D7D7AA47CCFA67CBC8D232C8CE9A6CC51D60E2634FCF859FF。
- B所有資料＋HANDOFFの新しい主要命令 0x494986/49498C/494979 は先行literal一致0。旧10/25 OFFLINE全文・他lane完全意味照合未了につきOFFLINE-UNSYNCED/VERIFY維持。
- 原作Golden条件：無改変ver0.67 EXE、20倍改変前DAT、同一SAVE/MAP/入力/RNG、loyal_down 0/10/20、name解決hit/miss、set member内外、状態byte3種と+0x80境界、para/loyal field型確認、両modeの+0xC0前後と進行後画面を同run採取。DESIGNED_NOT_RUN、原作Gameplay Golden PASS0/strict MATCH0、NOT READY。
- P0次：0x5882F0戻vector要素の実型、0x5916E0戻object+0xC4、0x493AD1へのキーproducer 0x44D730、2つ目集合の使用先。T028本来の士気・敗走、T013最終target、T024 battle AI、T011召喚経験値/T012 damageは未完。
- 安全境界：既拒否0x5710C0..0x571500、0x58021E..0x580340および既拒否操作の再試行/迂回0。他lane/MASTER/REA/dev_lab/原本EXE/DAT/SAVE/ZIP/Git/Work/設定/スケジュール書込0。
