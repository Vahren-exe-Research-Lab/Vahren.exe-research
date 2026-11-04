# B-20261030-22H-T013-SUM88-AH41-01｜mode2の二集計・raw/zero補正・x87比較後の引数2ディスパッチ
Owner B / T013（関連 T024）｜2026-10-30 22H JST｜STATIC ORIGINAL-PE ASM + V9 PSEUDOC / INFERRED / VERIFY / NOT READY
## 最新正本・復旧照合
- Local Compactオンライン。MASTER cp196/READY596（最終E公式値・当run再集計なし）、規約、LANE_B_HANDOFF、T011/T012/T013/T024/T028、B未保存/未同期索引、21H詳細を先読。既11H拒否要約3件、SAFE134/HOLD21、Library 147中54件バイト差、10/25 14H原文未回収はOPEN/BLOCKED据置。拒否内容再提出・迂回なし。
- 解析コピー原作PE 2910720B 現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。明示V9 SQLite 141033472B 現物SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable read-only quick_check=ok。旧search.sqlite/README/BUILD_MANIFEST欠落は既知OTHER、V9別名を使用。
- Java/Ghidraプロセス不在（ただしユーザー起動済みVahren.exeを発見。触らず・新規実行せず）。全体Ghidra再解析・原作ゲーム操作なし。
## 新增分1：0x515060はUnitData+0x1C4の二集計（native）
- 原PE 0x515076 LEA EAX,[ECX+0x88] / 0x51507C [+0x88]=0 / 0x51507E [ECX+0x8C]=0。0x515084/87 [obj+0x4C]-[obj+0x48] を SAR 2し、0以下ならloopなし。
- 0x515091/94 Unit vector要素を順次取得し、0x515097 CMP BYTE Unit+0x1867C,0 / 0x51509E JNE 0x5150C9 で除外。+0x1867Eの検査は当関数には無し。
- 通過したUnitについて 0x5150BB..C7 が UnitData=[Unit+0x1C8] の +0x1C4 DWORDをobj+0x88へ加算。さらに Unit+0x1D0 !=0 のときだけ0x5150A9..B5で同じ値をobj+0x8Cへ加算。意味名/符号/overflow/合法NULLはVERIFY。
- 0x5150D7 CALL 0x5B6513 はsecurity cookie検査。native cookieの正常経路0x5B6513 CMP ECX,[0x65A220]→0x5B651B REPZ RETでEAXを変更しない。通常経路のEAXは 0x515076 で作った &obj+0x88 に保たれる。Ghidra擬似Cがvoid fastcallと表示しても、hook ABI確定ではない。
## 新増分2：二つのobj集計とraw値/ゼロ正規化の順序
- 原PE 0x44C6AD ECX=EBX(manager)→0x44C6BD CALL 0x515060。0x44C6C2 ECX=[EBX+0x1C]（別group obj）/ 0x44C6C5 ESI=EAX（&manager+0x88）→0x44C6C7 CALL 0x515060。
- 0x44C6CC ECX=[ESI]（元のmanager+0x88合計）、0x44C6CE [EBX+0xB0]=ECXで **正規化前raw値** を保持。0x44C6D4..DF はこのECXがゼロの時だけ1に変更し[ESI]（manager+0x88）へ書き戻す。負値の0 clampではない。
- 0x44C6E1..F0 FILD manager+0x88(正規化済) / FILD group+0x88 / FDIV ST(1) / FILD group+0x8C / FDIVRP ST(2)。二つの集計比を作り、0x44C6F2 FLD [manager+0xD0]→0x44C6F8 FCOMP ST(2)比較へ接続。FPU/NaN/ゼロ除算の細部はVERIFY。旧21HのCALL存在・旧+0xD0評価は再新発見としない。
## 新増分3：0x44C99Eの反対枝
- 原PE 0x44C99E FCOMPP / 0x44C9A0 FNSTSW AX / 0x44C9A2 TEST AH,0x41 / 0x44C9A5 JNE0x44C9B4。非ジャンプ側0x44C9A7 PUSH2、0x44C9A9 PUSH EBX→0x44C9AA CALL0x449500、0x44C9AF JMP 0x44CC23共通cleanup。ここで**manager+0x20=2を書いた証拠はない**。2は0x449500の第二引数でありAI modeと同一視不可。
- 分岐側0x44C9B4..C3は [EBX+0x78] と[EBX+0x7C]のvector空チェック（同値→0x44CC23）、非空側0x44C9C9 manager+0x98・0x44C9E1 group+0x1EF244を評価し、0x44CA82 JMP [EDX*4+0x44CD4C] 9-wayへ。0x449500側もnative 0x449509..50Fに同vector空の早期return。表示・行動の語義はVERIFY。
## バイト証拠・重複・受入条件
- PE windows SHA256: [0x515060,0x5150E0)=F868C59576D65042EF40F1CF87DFCD0C2FB9C6D59CC16848244567814F9B0154；[0x44C6AD,0x44C705)=26CF5F36AA6C611330D4D03F505BBD8D2712168F0712DBBB3F02D16476CAF8AA；[0x44C99E,0x44CA89)=72E4F0876A5439E26E1D1DA0BB320B3F94C2253251997A2A9358B8CBD972E940。
- B関連Markdown+HANDOFF 436件の事前literal照合で新0x515097/A0/B5・0x44C6CC・0x44C9A5/AA/C0と本IDは0。0x5150C7、0x44C6DFは先行資料にも現存し再計数0。旧10/25原文・他レーン意味的重複はVERIFY。
- Golden条件: x20前DATと無改変原EXEの同SAVE/MAP/input/RNGで、managerとgroupのUnit vector(0/1/複数)、Unit+0x1867C/+0x1D0、UnitData+0x1C4、前後+0x88/+0x8C/+0xB0/+0xD0、FPU status、0x449500到達、選択Unit/翌tickを原作観測。DESIGNED_NOT_RUN。Gameplay Golden PASS0、strict MATCH0、新B正式READY0/E MASTER0/DONE0。
- NEXT: 0x44CA89..0x44CC23 Unit巡回とcategoryの収束、0x449500第2引数2の実作用、0x515060の型/overflow条件、T011召喚EXP/T012 damage/T024通常AI/T028士気敗走P0。元拒否・原本・MASTER・他owner・REA/dev_lab/Git/Work/設定/スケジュールへの変更は禁止継続。
