# B/T011・T012｜Skill親指定と内部 super ScriptData の生成側接続（2026-10-24 22時台）
研究ID: B-20261024-22H-T011-T012-SUPER-PARSER-PRODUCER-01
Owner: B/T011（T012参照）。状態: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / STATIC-DAT / INFERRED / VERIFY / NOT READY。
## 事前照合
Desktop Commander Local CompactでMASTER旧公式checkpoint196・READY596、解析規約、B HANDOFF、T011/T012・担当資料、OFFLINE回収台帳と既安全拒否を読取。旧22ファイル/後発10研究/Library訂正版2・10～18HのID単位完全統合は未了。既拒否範囲・ペイロード・要求の再試行0。
原本対象: rea_lab/targets/hakushin067_Vahren.exe。今run実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search_index/search.sqlite実SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、BUILD_MANIFESTと一致。Ghidra/REA全体再実行・EXE起動/書込0。active.lock無し。検索CLIはmode=ro。
## 新規原作ASM：定義ブロック解析→super属性登録
親側パーサのdirect CALLは0x0050B8E6→0x005049E0（search.py callers 0x005049E0でcaller 0x0050B220を確認）。0x0050B8BB CMP [0x008797E0],EBX→0x0050B8C1 JNE 0x0050B8F3、非分岐側のみ0x0050B8E6へ到達。EBX=0とした意味はGhidra 0x0050B220のDAT_008797e0==0枝で整合するが全入力条件はVERIFY。
0x00504FE4 MOV EAX,0x0065DC08→0x00504FED CALL 0x0041DED0→0x00504FF2 TEST AL,AL→0x00504FF4 JE 0x00505064。0x0041DED0擬似Cは2つの長さ/バイト列を比較して「不一致」を返す関数。**入力トークン一致時だけ後続super生成枝**へ進むことを局所ASMで確認。0x0065DC08のランタイム文字列の具体的字句（コロン等）は未確定。
0x00505064で0x24 byte ScriptData候補を確保し、0x00505072でvtable 0x00638D1C、0x00505078で容量0xF、0x0050507Fで文字列長0、0x00505086で+0x20を0へ初期化。Ghidra 0x005049E0も ScriptData::vftable と解釈。
0x0050508F以降は0x00505099 CALL 0x00502DD0で入力を解析。次に0x005050C9がDAT_008797E0を取得し、0x005050D4 MOV [ESP+0x18],0x0062C918でキーを設定。原作PE 0x0062C918の6生バイトは 73 75 70 65 72 00 = "super\0"。
0x005050E2 CALL 0x004528E0でkey/valueをペア化、0x005050EE CALL 0x00463280でDAT_008797E0に紐づく辞書構造へ登録を試みる。0x00463280擬似Cは木の比較・挿入/重複判定を含むため、重複キー時に無条件で上書きとは断定しない。
直後0x005050FF CALL 0x00502DD0で次トークン取得、0x00505113 CALL 0x00416920で比較。字句の実意味/入力パース成功・例外/重複・グローバル状態の実機推移はVERIFY。
## 21Hの下流証拠との新接続
既証拠B-20261024-21H: 属性存在0x00464290と値取得0x004647D0が [super] を探索し、superノード欠損/値NULL/親名長0・名前解決失敗・50回上限で停止。今回の独立増分は、そのsuperに対応する名前付きScriptDataをパーサ0x005049E0が作る候補経路をASM/キー生バイト/辞書登録CALLで特定したこと。
合法原DAT「32_ボススキル/B_14_ヌエバ・デスパセーニャ.dat」のskill u_diplo_nt3/4/5/6 : u_diplo_nt2 と親u_diplo_nt2 str_ratio=0（21H原文確認）を、入力構文→superパーサwriter→属性getter→Skill+0x288の仮説的クロスウォークに配置。特定の4Skillがこのwriterを実際に通過するDYNAMIC証拠は0で、子の実効ratio=0は引き続きINFERRED/VERIFY。
## 限定証拠SHA・重複・復旧
原作PEウィンドウ 0x00504FE4..0x00505016（51B）SHA256=48A84CC945659AFBAE2912540EC6A924613738A06C2F405AD01EEBEC38C30DE6。
原作PEウィンドウ 0x00505064..0x00505117（180B）SHA256=58495C9A36B27100BE9341BB57167064F8594C3FC65D520FB08A7D73FDD79056。
原作PEウィンドウ 0x0050B8B0..0x0050B90F（96B）SHA256=6DF58BC9B3137A96C7C9BE3931686E455A677A9AEF4096D488E9A7EF337D2408。
B主資料T011_DATA_MODEL/T012_BATTLE_CALC、LANE_B_HANDOFF、MASTERに0x005049E0/0x005050D4/0x005050EE/0x0050B8E6の既存明記0件（今run read-only exact check）。21Hの空親停止/str_ratio子DAT、16H/17Hの50回上限は再採番0。E/T019一般parser/他ownerとの意味的完全重複は未照合。
RECOVERY B-RC-20261024-22H-PE-WINDOW-ORDER-OTHER-01: 限定read-only SHA検査1回で誤ってstart=0x505064/end=0x505014（負長-80）を指定しempty SHAが返ったため証拠採用0。直後に正しいend=0x505118で180 byteを再取得しSHA一致。安全拒否/PC書込/原本破損ではない。
## 互換性・未解明・受入条件
再開発では親文字列を直接Skillへコピーするモデルと、ScriptData上のsuper参照による実効属性検索を区別すること。parser tokenの具体字句、同名ブロックのsuper書込順/競合、DAT宣言→当該parserへの到達、各子Skill+0x288最終値、RNG、副作用はVERIFY。
Golden: 無改変EXEと20倍強化前DAT・同一SAVE/MAP/入力/RNGでu_diplo_nt2およびnt3～nt6の親名ScriptData格納、compiled Skill+0x288、対象/HP/MP/状態/次tickを旧新比較。DESIGNED_NOT_RUN。原作Gameplay PASS0、strict MATCH0、新B READY0、E MASTER統合0、Task DONE0。
次回: 0x0065DC08の初期化元と0x00502DD0の実際の親名入力字句、0x00463280重複挿入時の意味を既存許可済証拠から軽量read-only照合。拒否済み調査の迂回は行わない。