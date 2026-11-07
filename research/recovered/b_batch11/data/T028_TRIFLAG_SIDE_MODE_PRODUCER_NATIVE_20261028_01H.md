# B-20261028-0114-T028-TRIFLAG-SIDE-MODE-PRODUCER-01｜T028 三状態分岐とbattle mode producer（2026-10-28 01H）
Status: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。B所有研究（E MASTER統合対象ではない）。
## 出典・照合境界
- 原作: rea_lab/targets/hakushin067_Vahren.exe 2,910,720B、実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 既存 search_index/README.md、BUILD_MANIFEST.json、search.sqlite 53,927,936B・SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、immutable read-only quick_check=ok。検索CLI function 0x490590。原作PEをpefile＋capstoneで限定ASM照合。active.lock無し、java/ghidra無し、Ghidra再解析無し。
- MASTER E正式最終既知checkpoint196/READY596。レーン規約、B HANDOFF・B5 owner・未同期回復索引を先読。10/25 14H OFFLINE研究全文と他レーン意味的重複は未回収/VERIFY。
## 新規原作ASM：2フラグ・第3フラグの区別
- 0x490632 MOV WORD PTR [EBP+0x1EED54],0 で隣接F54・F55をゼロ化。0x49063B [EBP+0x1EED56]=0 は別フラグF56の初期化。
- 0x49066C/672 は [EBP+0x1EED4C]取得、byte[参照+0x1D]検査、非0なら0x49067CでF54=1。0x4909DC/E3でbyte[ESP+0x74]!=0ならF54=1、0なら0x4909EF F55=1。別枝0x490A43 byte[ECX+0x14]==0なら0x4909EF F55=1、非0なら0x490A4E F54=1。0x4909FB・0x490A07はF56=1でF54/F55とは別。
- 0x490688 MOV AL,BYTE PTR [EBP+0x1EED54] → 0x49068E TEST AL,AL。F54非0は0x490696で[EBP+0x1E8630/34]を読む。F54ゼロは0x490A5A..0x490A71でF55を検査し[EBP+0x1E8630/34/38]を選ぶ。どちらも0x490A77/7Dでmanager+0x1EED44と+0x1EED48に保存する。
- 0x490A83 TEST AL,AL のALは直前の同一制御経路における0x490688のF54値（0x490A5A..0x490A7DではAL変更無し）。前回00Hの匿名ALのproducerをここまで静的に特定。
## 三状態マッピング（実際の陣営名はVERIFY）
- F54!=0: manager+0x1EED44=[manager+0x1E8630]、+0x1EED48=[manager+0x1E8634]、0x490AA0..AAでmode=(!player_battle)。
- F54==0 && F55!=0: +0x1EED44=[+0x1E8634]、+0x1EED48=[+0x1E8630]、mode=(!player_battle)。
- F54==0 && F55==0: +0x1EED44=[+0x1E8634]、+0x1EED48=[+0x1E8638]、0x490A8F..98でmode=(!enemy_battle)。
- 00Hで判明済みconfig loaderの0x683748/player_battleと0x683749/enemy_battle、および0x491870→0x4922A0の既mode consumer、21-23Hの死亡記録queue操作は今回新規として再計上しない。
## native独立検算・境界
- E8 original PE 0x4905F2→0x48F720、0x490650→0x469170、0x490661→0x469170、0x4906B3→0x597F40（4/4一致）。PE window 0x490632..0x490AAF SHA256 9433CE7071FCBBC00F304901429D158085DC3E3DE2FD9B47968E3A436E9AFCD8。
- B5 owner＋HANDOFFの先行literal照合: 0x490632、0x49067C、0x490688、0x4909EF、0x490A43、+0x1EED54一致0；既00H 0x490A83は既知で新規件数に加えない。他レーン/旧OFFLINE全文の意味的非重複はVERIFY。
- F54/F55が指すゲーム上の正式名称、[manager+0x1E8630/34/38]の実体（陣営・troop等）、実状態での到達、+0x1EED56の最終consumerとGameEvent副作用はVERIFY。+0x1EED54/55をenemy/player boolと命名しない。
- 合法Goldenは無改変ver0.67 EXE＋20倍修正前DAT・同SAVE/MAP/入力/RNGで3状態ごとのF54/F55/F56とside pointer2本、mode、死亡queue clear、実際の画面・戦闘結果を独立採取する。DESIGNED_NOT_RUN / Gameplay Golden PASS0 / strict MATCH0。
- B新正式READY0、E MASTER統合0、Task DONE0、NOT READY。既安全拒否VA0x5710C0..0x571500及び0x58021E..0x580340・過去拒否コマンド再試行/迂回0。原本/MASTER/他owner/REA/dev_lab/Git/Work/設定/スケジュール非変更。
- 次: 0x4909DC byte[ESP+0x74]のwriterと0x490A43 [ECX+0x14]の型照合、T028士気/敗走本P0、T013最終target、T024 AI判断を対象限定で調査。