# T013/T012 — 実owner候補・支援置換・cooldown木・数値境界
Run: 2026-10-13 00:31 JST / owner B / Status: PENDING_FINAL_CHECK
原作Gameplay Golden PASS0 / new strict MATCH0。Work所有sourceは編集しない。
既存B2140・2356とREA保存監査を継承。古い未収録全面検索、近傍4E53B0とSkill3本体の再解析は行っていない。
本書は実owner入力からWork停止点を閉じる接続契約。既存selector規則を新発見として重複計上しない。
## 証拠の読み方
S1=exe/T013_TARGET_SELECTOR_PROBE.txt: 514D60..514FF9、57CFA0..57D0FC（後続欠落部はS3）。
S2=exe/T013_SELECTOR_HELPERS2.txt: 5158A0..5158D2、5159B0..5159E6、57D180..57D1C5、5154F0群。
S3=rea_lab/decomp_task/runs/20261011T153309850Z/{57CFA0,57CFD0}_procedure_assembly.json（保存済み）。
S4=exe/T013_SEARCH_CORE.txt: 57B870..57BB9B。後半update_gateの途中開始断片は本体境界根拠にしない。
S5=exe/T012_ACTION_KNOCK_ORDER.txt: 57AF5A..57AF94と545ADA..545B14。
S6=exe/T013_COOLDOWN_SUCCESSOR_20261013_0031.txt: 今回の限定read。405440..40548A本体、63B0D0の8byte。
S7=dev_lab/reports/CHATGPT_HEAL_MUTATION_20261012.log: 保存sqrt1434..1474、CW helper1509..1543、毒数値prefix8628..8652。行番号は読取snapshot時点。可変ログ全hashは後続更新され得る。
S8=rea_lab/decomp_task/runs/20261009T215200079Z/5D1B80_procedure_assembly.json: evidence ev_0bcb24273794aa659538ffb7ed13e373239d40b71eb8680fcb8c077e62ec4321。
S9=data/T013_AI.mdのpool登録/RTTI・unit_element_heal、REA_T013_PRIMARY_SUPPORT_FILTERS・EMPTY_RANGE_REPLACE_ABIの保存監査。
Source hash/切出し行/検査結果はdata/T013_OWNER_CANDIDATES_CHECK_20261013_0031.json。S6だけ新しい分離targetの固定範囲readで、原作実行・変更・Ghidra起動なし。

## B-20261013-0031-01 — owner候補生成・2pointer出力・支援置換のWork接続
Classification: CONFIRMED-SAVED-NATIVE / NORMAL-FINITE-INPUT。allocator/非有限FPU/実生成はVERIFY。保存検査とHANDOFF後READY-CONNECTION。
### 1. 実ownerと入力identity
U+1D4のDWORDがowner O。反対poolはmem32(O+1C)。player/neutral/敵などの名称で別ownerを推測せず、実リンクを読む。owner self/alias関係も勝手に修正しない。
514D60: EAX=選択owner、stack arg1=出力record*、arg2=U*。caller57B983→57B988、callee RETは514E72/514F0Bともret8。ALは成功boolではない。
514F10: EAX=U*、ECX=選択owner。caller57BA41→57BA46又は57BA62→57BA67。RET514FF9、EAX=&global vector AC09EC。
攻撃通常O+1C、攻撃混乱成立O。支援通常O、支援混乱成立O+1C。各selectorの中へさらに独自の敵味方filterを加えない。
攻撃primaryはownerのDWORD列[+48,+4C)、fallbackは[+58,+5C)、capは走査に不要。pointer列の既存順を使う。countはsigned差をsar2したもの、正でない場合走査なし。
登録側の分類根拠はUnit+8Dであり、SimpleUnit/SimpleStaticUnitは確認済み型の例。すべての実owner構成をクラス名だけで再生成したと主張しない。Unit+1D0は別の部隊関連リンクで、owner+1D4や召喚boolと同一化しない。
入力検査はhost方針: array範囲/4byte alignment/Unit pointer identityの不足を拒否し、未bindingを空配列にしない。nativeが不正pointerを安全にskipするという意味ではない。
### 2. 514D60の走査・選択と出力record
source X/Y=U+214/+218は入口で固定。primaryを元順に全走査し、各candidateでbyte+1867C非0→self pointer一致→stealth非0時の抽選→距離、の順。
stealth draw=514DCF→5B6EAB。514DEDのsigned stealth>native_I(rand15*(1/32768)*100)なら除外。0のみdraw省略、負値/100超を勝手にclampしない。alive/self gateで落ちる候補のstealthや座標を先読みしない。
距離はn=s32(s32(dx*dx)+s32(dy*dy))をFILDして5E3B70へ（514E19、fallback514EC5）。collision用のsqrt+.5→整数化とは別。正しい数値calleeを未接続ならここで停止し、消費済みstealth drawと候補indexを保持。
初期best distance=double[63B0D0]=2147483647.0（S6のraw0000c0ffffffdf41）。候補なしはout.pointer0=0、out.pointer10=0、out.distance8=この値。Infinity/0/Noneはnative出力値ではない。
比較514E22/514ECEはmemoryのbest binary64と新ST値を比較し、AH&0x41==0のときだけ更新する。有限で比較値が等しい場合は元順を保持。非平方数・x87拡張値とbinary64 spillの差を単なる数学的同距離へ一般化しない（数値節）。
primary全走査後、選ばれた単一Pのsigned +18C>=保持距離なら即return。候補ごとにrangeで先に除外しない。遠いがrange内の別primaryへ探索し直す処理はない。
primary無し又はrange不足ならfallbackを元順に走査。best距離を初期化し直さず、+1867C/self除外のみでstrict closerなら更新。fallbackではstealth/rangeを読まず、直接rand0。
出力out+0=最終best、out+8=保持距離、out+10=元のprimary PがあればP、なければ最終best。staticが近くて置換したときout+0とout+10は異なる。out+4/+14は本selectorで初期化されないopaque/paddingであり0補完をネイティブ事実にしない。
caller57B988..57B9B9がout+0/+8/+10をU+1E574/+1E578/+1E580へ保存。U+1E570はこの出力で上書きしない。実Unit更新完了やMP/効果発動はここでは決まらない。
具体境界: primary P(d=10,range=5),Q(d=12,range=20),fallback無しならPが残る。fallback(d=10)ではP保持、fallback(d=8)ならbest=static/aux=P。これらは正確な整数距離を持つ限定モデル条件。
### 3. 514F10の共有scratchと支援cacheの置換
global vector=(AC09EC begin,AC09F0 end,AC09F4 cap)、初回AFD118 bit0で0初期化/5B6BA4登録。毎回非空なら5158A0(begin,oldEnd,oldEnd)→end=begin、容量は保持。その後source X/Yを読んでowner[48,4C)だけを走査。
filter順はcandidate+1867C非0を除外→global87984F==0のときだけcandidate+1D0==0を除外→距離計算。self除外もstealth判定もrange判定もない。条件を通るsource自身・重複pointerは候補に残り得る。
各通過で24byte recordへ+0=candidate、+8=距離double、+10=candidateを設定し5154F0で末尾追加。+4/+14はopaque。入力順を保持、sort/set/dedupはしない。builder本体の直接CRT draw0、allocator/初回登録/数値calleeは別作用。
返値は共有vectorヘッダのアドレスであり、次回builderで内容が変わる。Workは即時にUnit-localへcopyするか、必要なrecord payloadをsnapshotする。遅延参照だけを保持して別Unitの候補で上書きされないようにする。並行呼出可能とは仮定しない。
支援反転側57BA53→57CFA0（ESI=&U+1E584,stack=(srcBegin,srcEnd)）は旧cacheを論理clearして57CFD0へ。通常側57BA7E..57BA97も非空なら同clearを先に行う。
5158A0は24byte copy関数。ここではECX==EDX==oldEndなのでコピーせず、EAX=oldBeginを返す。したがってfree/destructorを根拠なく追加しない。callerがend=beginを書いて論理的に空にする。
57CFD0の5 stack値は(vector,position,srcBegin,srcEnd,opaque)。本callsiteではposition=begin=end、旧要素0にしてから挿入。一般insertの全alias/中間positionをこの置換契約へ混ぜない。
srcCount=trunc(signed(srcEnd-srcBegin)/24)。0なら57D15E→RET57D16Fでinsert・allocate無し（旧cacheは既に空）。非空はcap判定後、容量内なら57D180で24byte群をcopy、54B460回転の同末尾境界を経てend+=24*n。容量不足では515750/515790→prefix copy→57D180→suffix copy→旧storage free→begin/end/cap差替え。正常結果はsource順、重複を保った置換。
57CFA0 RET57CFCD(ret8)、57CFD0正常RET57D112/57D16F(ret14)。exception/allocator失敗の原状復帰保証、一般自己参照insert、54B460の全範囲、第五値の例外時意味はVERIFY。成功を受領する前にcache更新完了扱いにしない。
### 4. 混乱とstealthの乱数順・再開PC
full刷新jitter57B8FEは既存Workが実行済み。nearby=0の時だけ57B938から攻撃混乱判定、U+C8<0なら57B940のrand1回、その後に514D60の各生存非self・stealth非0候補が元順にrandを引く。
攻撃結果の保存後、支援capability byte+137非0の場合だけ57BA07から独立の混乱判定、U+C8<0なら57BA10でrand1回。その後514F10は直接rand無し。攻撃と支援で同じ混乱抽選結果を共有しない。
既存nearby非0なら攻撃混乱/514D60/stealthをすべてskipするが、後段の支援混乱は独立に発生し得る。支援capability0なら新候補builderもcache消去もskipし旧cache保持。
順序=既実行jitter→attack混乱（条件付）→primary stealth列（条件付）→support混乱（条件付）→builder/置換→range latch→毒/577100→条件付route。早期returnや既実行prefixを含む抽選を一括前払いしない。
rand15の百分率変換は既存定数とIの組合せであり、独立一様0..99の乱数へ置き換えない。整数モデルでの発生頻度と原作実機での観測を区別する。
[Work提案] 現在停止57B938にはselected_owner_refとattack_draws、514D60のindex/P/best/距離ST値・memory値、57BA07にはsupport側stateを保存。戻先57B988/57BA46/57BA67とcaller57E5B2又は57AFC9を区別。新しい継続stageは提案で製品未編集。
[VERIFY/次] 実owner配列を作る全factory/登録順、数学callee/heap外部作用、general insert、実機FPUは未完。targeting_subset.hypot、uidによる自他判定、synthetic候補列をそのままstrict実ownerへ流用しない。
[GOLDEN設計/NOT RUN] owner/alt pointer、primary range不足とfallback同距離、死/self/stealth非0、支援self/0件/重複/次Unit scratch再利用、混乱独立drawと中断再開で可視target/HP/MP/位置/RNGを比較。原作PASS0。
[置換順の追加根拠] 容量内copy後の54B460が未閉鎖だったためS6へ54B460..54B495の固定範囲を追加。入力EBX=position、EDI=oldEnd、EAX=newEnd。514F10からの置換ではposition==oldEnd==beginなので54B463/465→54B492→RET54B495、CALL・候補writeなし。よって正常置換経路ではcopy順を後段で並べ替えない。54B8B0へ進む一般rotateは対象外。

## B-20261013-0031-02 — 405440 cooldown木successorの本体・全正常RET
Classification: NEW-BOUNDED-SAVED-NATIVE。S6の405440..40548Aを新規取得。S5の既存減算callerへ接続。新しい木の全体を検索したものではない。
ABI: EAX=&cursor_DWORD、stack引数なし。cursorが指すnodeのleft+0/parent+4/right+8、nil byte+2Dを読む。keyやpayload+28は読まない。nilは非0、特定値1への限定ではない。
RETは40546Cと40548Aの2か所だけ。CALL/tailcallなし、CRT RNG0、heap操作0。EAXはcursorのアドレスを保持し、結果nodeはmem32(EAX)へ書く。AL真偽値やEAX=nodeとして解釈しない。
1) cursor nodeの+2D!=0ならそのまま40548Aへ（既存end sentinelは変更しない）。
2) 非nil右子がある場合: 右子のleftを非nilの間だけ辿り、最後のnodeをcursorへstoreして40546Cへ。右子のさらに左孫がある経路を省略しない。
3) 右子がnilの場合: parentを取得。parent非nilかつ現在cursor==parent.rightの間は、cursor=parentを**途中store**してさらにparentへ。条件不成立のparent（またはhead sentinel）を最後にcursorへstoreし40548Aへ。
変更は渡されたcursorのDWORDだけ。実callerがstack localを渡す場合、treeのlink/値は不変。任意aliasを許した一般memoryで「何も変わらない」とは主張しない。ECX/EDX/flagsはscratch。
【別treeとの区別】B2356の5799D0が使うtreeはnil byte+11。405440は+2Dであり、同レイアウトとして流用しない。calleeは文字列key比較やmap lookupを行うものではない。
### cooldown callerと中断継続
57AF5AでU+1E544==0なら全走査skip。非0ならhead=U+1E540、first=mem32(head)。first==headならskip、それ以外はcurrent.payload(+28)>0の時だけ1減算する。
減算したか否かに関係なく57AF83 call405440(&stack_cursor)→57AF88でcursorを再読し、headと一致するまで57AF76へ。値1→0でもnodeを削除しない。0/負値nodeも訪問し次へ進む。
減算の時間条件は既存57AEE7のclock閾値と先行RNGを通過した更新機会。405440自身がtimer周期を作るのではない。別更新caller545B03→545B08にも同successorを渡せる。
Workの非空cooldown停止からの提案state: U/head/current/visited-path/declared-countと、payload減算前後のnext_pc。payload更新済みで405440未実行なら、再開でpayloadを二度減らさない。既存cooldown空枝・timer jitterの再実装は不要。
[正当入力の前提] tree/head/parent/left/rightが整合した非循環pointer graph。host検証は不正・循環を拒否してよいが、nativeの安全検証と混同しない。全走査のsort順は既存tree構造のin-orderで、keyを新しくsortして代用しない。
[GOLDEN設計/NOT RUN] 空/単node、左深/右深、右子左孫、parent複数段上昇、最大node→end、既存end再呼出、同値key複数、payload=-1/0/1/正で可視再使用待ち/乱数/次Unitを比較。原作PASS0。

## B-20261013-0031-03 — 平方根・整数変換・毒：保存事実と実行profileの分離
Classification: EVIDENCE-BOUNDARY-CONTRACT。新しい数学関数全復元ではない。S1/S4/S7/S8とWork AssumedHealArithmeticの明示仮定を照合。
### 記録から確定すること
全selector/builderの距離前段はsigned32の減算・IMUL・ADDを経てFILDする。Pythonの無限精度hypot(dx,dy)と違い、座標差・二乗和は32bitでwrapする。負の二乗和になればsqrtのdomain処理が必要。
514D60/514F10はsqrt結果のdouble距離を使う。collisionの丸め距離（sqrt+.5→整数）に置換しない。514D60はbestをbinary64にspillした後もST値を扱うので、有限値同士でも精度とstore箇所を保持する。
5E3B70保存log: 入力を一度FST qwordで置き、5E4AE8/5E3B8Dへ。5E3B8F FNSTCW、0x027F比較、必要時5E4A75、符号等判定、FSQRT（5E3BAC）。5E4A75は(cw&0x300)|0x7Fを作ってFLDCW。FSQRT後はglobal68E658と5E4AFE/5E4B0B等へ分岐する。
従って「常にhost math.sqrt」とは未確定。PC/Rounding/例外mask・CRT route・flags/errnoの復帰は別。保存されたwrapperの分岐を、現在解析用PythonプロセスのFPU設定で実機観測した扱いにはしない。
5D1B80のS8はglobalB14A40!=0側を保存: ST入力をFSTP binary64にしてCVTTSD2SI EAX、RET5D1B9B。この経路はbinary64化後のゼロ方向切捨て。B14A40==0は5D1BB6へ分岐するがS8の関数本文には含まれない。
S8のREA環境欄はnull、保存ABI/命令の確定と原作runtimeでSSE経路が選ばれることは別。NaN/範囲外変換・例外mask・alternate経路を未証拠のまま統一しない。
### 毒の呼出順・切り捨てと呼んではいけない範囲
S4 57BAD8でsigned U+BC<0の時だけ開始。p=x87_round(FILD(s32(U+DC))*binary64(global65BD78))を作り、FSTPでbinary64引数aへ保存。5B6ED0(a)→5D1B80(return_ST)の二段変換で整数dを得る。
その後U+90=wrap32(oldHP-d)、符号bitが立てば0へclampし、57BB21で577100(U,1)を呼ぶ。U+BC>=0ならこの一連の処理をskip。毒でHP変更→577100の完了後にroute後段へ進む。死亡処理を先に済んだ扱いにしない。
5B6ED0の既存保存prefixはB14A24を検査。非0ならMXCSR&0x7F80==0x1F80、x87 CW&0x7F==0x7Fを検査し、適合時5B6F10のSSE演算へ。非適合は5BCF71へ。保存prefixはPSRLQ等の途中で終わっており、SSE側最終式/alternate全体はこの資料だけで閉じない。
5B6ED0をfloor/ceil/trunc/確率処理のいずれかと推測で固定しない。後段5D1B80が切捨てでも、前段5B6ED0が同じである証拠にはならない。最大HP×毒係数を直接int()する実装は未承認の近似。
毒callerと表示済数値prefixに直接rand命令はないが、未回収数学/例外/577100等を含む総RNGを0と確定しない。既知の攻撃・支援抽選列の後にこの未完了段階を置く。
### Workに渡すprofile分類
CONFIRMED: opcode/ABI/32bit wrap/比較mask/64bit保存箇所/既存分岐のglobal参照/毒のHP減算とclamp順。
ASSUMED-RUNTIME: Work AssumedHealArithmeticのx87 precision53又は64、nearest ties-even、全例外mask、B14A40!=0側、finite bounded入力。profile.runtime_unverified=Trueを維持する。PC環境の版・CPU名から証明しない。
EXACT-VALUE-SUBSET: 現Workの正の完全平方数nに対するisqrt値は通常数値経路の値を限定できるが、CRT全flags/例外/return実装の証明とは別。非平方数をrounded_native_distanceへ代用しない。
VERIFY: 非平方数のST→binary64丸め/tie、負wrap/NaN/overflow、SSE以外5D1BB6、5B6ED0の両経路と戻り、CRT error hooks、原作CW/MXCSR/global実値。doubleからexact rationalへの置換も演算順を無視してよい根拠にならない。
[再開境界] sqrtの未確定は514E19→514E1E、514EC5→514ECA、514FD2→514FD7。candidateのstealth判定が済んでいれば再抽選せずその場を保持。攻撃出力書込み/支援cache置換のcommit境界も別々にする。
毒の未確定は57BAF3→57BAF8（5B6ED0）、57BAFB→57BB00（5D1B80）、57BB21→57BB26（577100）。数値戻りが未確定ならHPを書き換えず、既実行jitter/candidate/cache/latchは保持する。
[GOLDEN設計/NOT RUN] 二乗和0/1/2/25/INT_MAX/負wrap、同距離とbinary64 spill、HP毒係数の整数前後、B14A40/B14A24、CW/MXCSRを実観測と仮定に分けて比較。旧ゲーム起動なし・PASS0。

## Work向け入口索引（提案、製品未編集）
- 57B938: attack側pool選択とordered514D60。必要なobject graph・RNG・出力recordの既知fieldを入力として、57B988へ返す。
- 57BA07: support側pool選択→514F10 shared scratch→57BA46/57BA67→Unit cache置換。後段57BA9C以降は既存Work工程を再利用。
- 57AF63/57AF76/57AF83: 非空cooldown header/current/payloadと405440。前段clock/jitterや当該nodeの減算を再実行しない。
- 57E5AD内で止まった検索と57AFC2からの検索はouter帰還先が異なる。parent call frameを失わず、helper returnだけで次Unit/frameに進まない。
SOURCE/OBSERVATION/ASSUMPTIONをtrace別列にし、unknown inputを空/0/単純無作用で補完しない。本書は通常戦闘全体の完走・実機一致を宣言しない。

## 保存検査・受渡し状態
FINAL_CHECK_COMPLETE — 2026-10-13 00:45の事前検査232項目PASS/失敗0/exit0を確認。HANDOFF登録後の--final検査結果を最終とする。
0031-01=READY-CONNECTION（実owner候補/支援cache/乱数順、正常有限条件）、0031-02=READY-STATIC（405440本体と減算caller）、0031-03=READY-EVIDENCE-BOUNDARY（既存数値証拠とruntime仮定の分離）。3関数の新規完全復元という集計ではない。
検査script exe/T013_OWNER_CANDIDATES_CHECK_20261013_0031.py、結果data/T013_OWNER_CANDIDATES_CHECK_20261013_0031.json。保存byteのhash・RET/branch・405440の命令インタープリターと独立in-order比較・payload一度更新・有限平方数selector/支援境界・数値証拠を検査。原作EXEコードを実行していない。
新規rawは405440と63B0D0定数、および支援置換の未閉鎖だった54B460等号出口だけ。同じLocal既存分離targetの固定範囲readであり、禁止xref/constructor/文書保存の再試行なし。
Work入力アダプターはowner pointer→実[48,4C)/[58,5C)のordered pointer列をbindingする。Session全Unitをuid順へ並べて擬似生成しない。traceにはchosen_owner、array_begin/end、candidate_index/pointer、除外理由、draw/callsite、sqrt停止状態、out+0/+8/+10、shared scratch世代とUnit-local置換完了を含める。
未知calleeでの停止はparent frame/cursorと既実行prefixを保つ。source未binding・未解決numericなら完了receiptを出さず、Workの独立工程を止めない。原作Golden0/strict MATCH0。

## WRQ-20261013-B-NUMERIC｜2026-10-13 09:48 JST 依頼受領と未完VA（新READYなし）
[OWNER/STATE] B T012/T013。P1/PARTIAL、今回新しい数学calleeの解析・原作実機検証なし。既存B-20261013-0031-01/02/03と本資料の236項目保存STATIC PASSを継承し、同じowner・405440を再解析・再採番しない。Work製品コード/共有キューはread-only。
[REUSE] 514D60 primary/fallback、514F10 shared scratch置換とstealth/confusion RNG順はB0031-01、405440 cursor successor/RETはB0031-02、signed32 wrap・5E3B70/5D1B80/毒5B6ED0の確認済命令と仮定の分離はB0031-03。
[OPEN-VA] 0x5E3B70→0x5E4A75/0x5E4AFE/0x5E4B0Bの非平方/例外とruntime x87 profile、0x5D1B80のB14A40==0側0x5D1BB6、0x5B6ED0のSSE/alternate（0x5B6F10・0x5BCF71）、0x577100の毒後の副作用、owner virtual+0x18/0x5767B0の意味。保存不足はVERIFY、拒否済み新規解析を別経路で反復しない。
[TEST] 正の完全平方数だけの限定モデル、非平方/負平方和/over-underflow・CW/MXCSR分岐、毒HP減算→577100の同条件fixtureはDESIGNED/NOT RUN。Gameplay actual PASS0／strict MATCH0。最優先WRQ-B-SKILL後に未確定点だけ継続。


## B-20261013-1247-01｜WRQ-B-NUMERIC：5D1BB6 alternate のx87戻りが候補距離を左右する
[STATUS] READY-STATIC-BODY（T012同IDに詳細）。0x5D1BB6はB0031未収録だったx87 FISTP qword→FILD/FSUBP→sign別ADC/SBB補正、正常RET5D1C2Aであり、B14A40非0のCVTTSD2SI/RET5D1B9Bとは実行命令が異なる。source B exe/T012_NUMERIC_FTOL_5D1B80_NATIVE_20261013.txt。原作実Gameplay PASS0、新strict MATCH0。
[DELTA/WORK] 主owner候補514D60/514F10のFILD/sqrt/5D1B80呼出結果について非平方/FP profileを無理に確定せず、既存B0031-03の未完境界だけ追加。Work既存AssumedHealArithmeticのruntime_unverifiedを維持し、円滑なresumeのためST・globalB14A40・CW/MXCSR・callPC・HP/RNG cursorを分離。P0 B-SKILL状態はPARTIAL、P1 NUMERICもPARTIAL。EのみMASTER/T018統合。
[STATUS] READY
