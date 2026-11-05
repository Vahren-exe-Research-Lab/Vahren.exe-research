# 雇用関係優先表示 V4　研究・実装・監査台帳
ID: REDEV-HIRE-SORT-V4-20261021
時刻: 2026-10-21 JST
Owner: 雇用UI専用レーン（Work所有dev_lab/srcは未変更）
状態: BUILT / STAGED_PC / WINDOWS_INSTALL_STAGE_PASS / SYNTHETIC_NATIVE_TEST_PASS / GAMEPLAY_NOT_VERIFIED / UI_DISPLAY_NOT_VERIFIED

## 背景（V3実機不合格）
ユーザーは起動できたが、画面が1.5倍程度に拡大し、マウス位置がずれ、雇用可能順にはなっていないと報告。
DPIは既存Vahren.exeにのみHIGHDPIAWAREが設定されており、新しいexe名では継承されない。ユーザーがWindows設定で手動調整する方針。
V3の重大な設計欠陥：押下ゲート +0x1480 を雇用可能関係と混同。Work実観測では初回候補17人すべて0、別観測では最初の1人のみ1。両者ともV3のstable partitionは元の順序のまま。
Workの観測では5雇用者×17人候補のうち関係成立6人。原作述語 0x586080 ECX=target, ESI=employer, AL=flag を実機UIスレッドで78回実行した証拠あり。

## V4の具体修正
- 原作に関する雇用者一覧(PersonsInfoWnd mode1)を +0x281468で読み、候補+0x27d420のタグを解決。候補別に5雇用者のnative関係述語をOR評価。
- 失敗時は未定義の可能優先順を作らず、元の描画と入力を保持する。
- 候補のC++文字列オブジェクト/値段/雇用判定/セーブは直接改変せず、画像画素とクリック/ホバー RECTを同じ順列で移す。
- 描画ルーチン0x004D4A50への機械語直接CALLを6サイトではなく8サイトに拡張。2サイトはDAT reloadMenuイベント側：0x004A5B28、0x004A5B54。
- 2026-10-21の実機結果を踏まえ、GAMEPLAY_NOT_VERIFIEDを別状態として保持。インストーラ成功をゲーム内表示成功として扱わない。
- 画面更新の成否を1つの HakushinRecruitSortV4.log に追記する。ログは表示・開発状態のみ、Cookieや認証情報は含めない。
- 別名で原本/V2/V3と独立共存させ、既存ゲーム・セーブ・研究MASTERは書き換えない。

## ビルドと検証
- コンパイラはWork管理の既存Zig0.14.1 x86-windows-gnu。Windows32bitの実機でV4.dllをコンパイル。
- PEのMachine 0x014C。裸名 HakushinSort_Install と旧stdcall名 HakushinSort_Install@0 の公開関数を確認。
- Windows起動前のステージ専用実行で2種類のEXEにV4 DLLをロードし、8箇所のフック設置が両方成功（終了0）。
- x86 native predicate接続を模した4MB仮想メモリの独立テストでは17人、5雇用者、6優先、61呼出で成功。
- モード不一致・雇用者キャッシュ欠損ではfail closed、出力変更なし。
- 機械語とWork観測でRECT逆マッピングを再確認し、10,000件のC実行で文字列・資金・状態不変、矩形の逆順列・復元成功。

## 既知リスク（必ず残す）
- 雇用関係があることと、資金・枠・距離等まで含んだ最終雇用成功は同一ではない。「雇用関係あり優先」として扱う。
- GDI並び替えが最終ウィンドウの前面に保持されることは未検証。Work旧実機の即時再描画で見た目の変化が消えたことがある。
- 候補行数が2未満、定義マップや雇用者情報の状態が未完成、描画サイズやRECT不一致は並び替えをスキップしログに記録。
- 100件より後の雇用可能人材を先頭にする機能は未実装。
- DPI設定は新しいV4 EXEのファイル名ごとに必要。ユーザーが手動調整する。
- まだV4を実際のゲームで起動・人材雇用画面を操作していない。初回はクリックで雇用確定しないこと。

## PC上の正本保存位置
REDEV_RESEARCH/data/recruit_sort_v4
- src/: V3からの派生、Work由来の読み取り専用native helper、V4優先判定、ログ
- tools/transform_v3_to_v4.py: 差分パッチ再現
- tools/extract_readonly_helpers.py: Work helperを未変更のまま読み取り専用抽出
- tools/build_v4.ps1: ビルド
- tools/build_v4_exes.py: 新EXE生成
- tools/probe_install_v4.py: 起動前段階検査
- tests/: x86 native predicateテストと10,000パターン矩形テスト
- dist/: V4 DLL / V4 EXE2種類（ゲームフォルダへ別名コピー済み）
- reports/: ソート研究台帳、ハッシュ記録、ステージ/模擬テスト結果

## 次の行動
最初の実機観測はゲームフォルダにあるV4 EXEで人材雇用画面を開いて終了するだけ。
描画上の並びとスクロール、人物とホバー結果を見る。初回の雇用確定・セーブ上書きはしない。
HakushinRecruitSortV4.log が出来れば研究担当が読み込んで、候補数と優先候補数・ソート成功数・理由番号を照合。
機能が動かなければ別の固定アドレスやフラグを推測で書き換えず、描画最終プレゼンタ経路を追加解析する。
検証成功と判定する条件：本人のスクリーンショット等でリスト順、マウスとホバーが一致、雇用元、価格、セーブ差分を実証した場合のみ。


## WORK-V4-FOUR-GROUPS-20261021

ユーザーからV4引継ぎを受領し、data/recruit_sort_v4を改修正本として確認。新要件は安定順: 0雇用可能、1雇用リンクあり領地不足、2リンク/領地あり資金不足、3リンクなし。複数雇用者では完全成立を優先し、なければ領地成立の資金不足を採用、誰も領地成立しなければ領地不足。表示グループの順番と複数雇用者の成立度を混同しない。rect_sort_core.hに4分類/雇用者間集約/安定順列を追加。関連条件がunknownなら拒否。新規5組の条件assertと既存10000矩形ケース成功。native relation模擬17人/5雇用者/61calls成功。4段階分類のネイティブ領地/費用入力は未接続: 製品DLLは依然relation-onlyであり4段階完成とは扱わない。原作UI保存4D4A50 L1066-1084には5AC880等の領域集合と資金/価格比較がある。価格はL1012-1046の雇用者依存補正を含むため、全員表示の価格をそのまま各雇用者の価格と推測しない。今後native ABIを確認して入力アダプターへ接続。
V4の再描画を修正: 通常thiscallだけでは不足する453C20のEBX=0を、Workで実測済みのbridgeと同形式で設定。対象window最小確認サイズを1554→1558へ修正。build成功、dist DLL SHA ac840dc8d20243e0d941ba65b30987e72e2f0fc148797f25d19cb42e48e84b7f。ゲームフォルダの配置DLLは今回は未更新、原本/セーブ/他担当は未変更。最新保存V4実機ログはrenderer初回→priority skipped reason=-8 n=17。ユーザーは並び変化ありと報告しており、ログと同一回の観測とは未確認。-8はHkReadNativeEmployers拒否であり、ロード時フック成功と分離して調査する。V4全完成/実雇用/クリック整合は未検証。Work旧105checks版panel/restoreソースはdev_labに残るが実機パネル起動未実施、V4へ混在させない。次P0=roster mode/count/取得時点を診断、原作領地・雇用者別価格/資金の意味/ABI確認、4段階入力接続、V4描画・hover実機試験。上限100件は継続VERIFY。Golden0/MATCH0。


## WORK-V4-NATIVE-CONTRACT-20261021

Progress: STATIC入力契約をreports/native_four_group_contract.jsonに保存（SHA一致原作解析コピーの限定x86、原本未変更）。4D6B3E..6B98: 5AC880(element,1,0) cdecl、始点Spotを集合へ追加しtargetの583CF0結果が集合にあるか確認。領地不足は資金判定より先。4D6BC0..6BE6: signed資金>=price、またはprice<=0で資金通過。4D6781..68B3: 585960 priceに相性/係数/x87丸めを適用、候補+75/+77と雇用者/候補の583A80で追加係数分岐。勢力表示の相性は5878A0(target EDI,power EBX)、人材プレイは5878F0。従って「雇用者別価格」は主に傭兵等の追加条件による差で、勢力モード基本相性は候補対勢力。4D4A50開始保存C: wnd+98→+4 manager、manager+20C powerの+5C資金（人材プレイ条件成立時はmanager+208 def+174）。いずれもnative関数の新実行は行っていない。597BA0は要素不在時にdummyを生成する枝を持つので、単純なread-only関数として無検証呼出ししない。新規REA MCPは現行ツールから削除されており、既存GhidraとLocal限定読取を使用。
実装: native_priority_v4.cにロスターmode/count/decoder_status診断、hakushin_recruit_sort_v4.cの拒否logへ追加。tests/test_priority_win32.cで不正mode0/count5/decoder1と出力無変更を検証。PID24720 exit0: 模擬native判定PASS、DLL build/PE check PASS。DLL SHA bd9d773b7535297928b70897057ae8feb1861722ba0d6452843653c3f5cdcd14。ゲームフォルダ未配置、最新4分類の実機実行なし。四分類コアは前checkpointのテスト済みだがnative領地/費用アダプター未接続。原作保存済ログ-8の具体原因は未確定、タイミング説は仮説であり追加観測/呼出経路確認が必要。次: 取得タイミングの診断、領地/価格の残るABI・副作用を確認して4分類へ接続、実機表示とhover/click整合。ユーザー承認待ちで作業を止めたわけではない。元EXE/DAT/save・他担当は変更なし、Git stage/commit等なし。Golden/MATCH 0。


## WORK-V4-USER-STATUS-20261021

ユーザー補足: V4は未完成だが、並び方が変わる段階まで到達。これをV4の表示変化の報告として保持し、四分類や全行クリック整合の成功とは扱わない。最新ソースは依然relation-only。追加STATIC確認: 597BA0はEDI=Spotを受け、Spot文字列/ctx経由のmanager+504辞書を49E490へ渡す。結果なしの場合AC0990の共有dummyを再利用または生成、597C89はplain ret。native_four_group_contract.jsonへ限定命令と副作用を保存。新しい原作実行・配備・テストは今回なし。既存DLLビルド/模擬試験結果を新規実機結果へ読み替えない。次P0は副作用を避ける既存element取得契約、領地・価格入力アダプター、四分類の本番接続。表示の変化がすでに得られた箇所を初めから作り直さない。


## WORK-V4-EXISTING-ELEMENT-20261021

P0 PARTIAL / 所有V4のみ。native_priority_v4.cにrs4_lookup_existing_elementを実装。SHA一致コピー49E490限定x86と既存4C1200/4682B0によりmanager+1EF0D4のstring->SpotElm辞書を確認。597BA0のdummy生成枝を呼ばず、既存Spotからcontext/manager対応、辞書key、element+ A0のSpot逆参照を検証して取得。欠損は1=VERIFY、破損は-1として出力を変更しない。領地不可とは混同しない。tests/test_priority_win32.cに存在/無変更/欠損/逆参照不正/循環/owner不一致を追加。RED PID17992欠落関数link error→GREEN PID6456 exit0。既存17候補/5雇用者/6優先/61呼出試験もPASS。PID10168: 10000矩形ケースPASS、DLL build/PE check PASS。新DLL SHA da7291b53b51a03b8d2e1ef17fdae18420e30e05241274b5c3df76f0e6b914f6。ゲームフォルダへの配置・実機呼出しなし。新getterは4分類アダプター用で本番分類からはまだ未使用、V4現行分類はrelation-only。原作EXE/DAT/save・他担当は未変更、Git書込操作なし。
次具体位置: native_priority_v4.cのrs4_lookup_existing_elementを使用し、583CF0で対象/雇用者Spotを取得するABI bridgeと5AC880(element,1,0)領地集合取得を接続。5AC880の返却集合はshared scratchで初回alloc/毎回clearがあるため純read-onlyとは呼ばない。saved44D070は集合head+4,node key+0C,nil+11のunsigned pointer比較を確認済み。始点Spotを含める原作呼出側の意味を維持。価格585960/46F4C0/583A80のABI・所有権を確定後4段階へ接続する。全体Python未実施、旧2FAILは未解消、Golden/MATCH0。全完成とは扱わない。


## WORK-V4-TERRITORY-CURRENT-GHIDRA-20261021

ユーザーのGhidra機械解析について確認。これまで旧10/11保存ZIP中心だったが、新しいrea_lab/headless_analysis/search_index/00_START_HERE_ACTIVE_RESEARCH.mdとCURRENT_ACTIVE_RESEARCH_STATE_20261021.jsonを読み、正本をHakushin067_FunctionRepair_20261021.gpr + HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite + search_current.pyに更新。DB SHA282924553309c4778ff6c5d5346ccf5c2bcb1b6fd17e46dbbae9031547453f8d、CLI SHA372fafd6751ef9593a12df7b503723df082deacfb53659f3d6272766d9d16baaをマニフェスト照合済み。新CLI read-onlyで4D4A50呼出8箇所と585960/583CF0を照合。reloadMenuの4A5B28/54は4A1250所属へ修復済み、V4既存8フックと一致。修復擬似C10件/verified ABI3件に限り、全関数のABI確定ではない。以後新規調査は現行DB/CLIを先に参照。旧ZIPは履歴比較用に保持、他担当正本は変更しない。
実装: native_priority_v4.cにrs4_native_territory/583CF0 EAX bridge/44D070相当pointer集合読取を追加。existing element取得→5AC880(element,1,0)→target Spot→集合membershipと始点Spotの和集合という入力経路を接続。5AC880はnative scratch変更/一時allocationあり、純read-onlyとは記載しない。unknown/欠損は出力不変でVERIFY。これはまだ実行adapterでありrs4_priorities本番から未使用。価格接続前に雇用可能として出力しない。
テスト: RED PID464欠落symbol→GREEN PID4424 exit0、呼出順整理後PID7568でもnative模擬試験全PASS、DLLbuild/PEcheckPASS。領地包含/不包含/同地点/集合破損/element欠損/Spot欠損とcdecl引数/EAX引数を模擬確認。DLL SHA3337a7ef85f066470c6c20cd2e19b16d60bf9c12df69f946f3eb890decb3d82b。実原作呼出・ゲームへの配置なし。4段階並替えPARTIAL。次: 現行検索DBから585960/46F4C0/583A80の価格ABI/出力所有権を確認し、本番4分類と価格/資金へ接続、ロスター取得時点診断と実機画面整合。原作/save変更なし、全体Python未実施、Golden/MATCH0。


## WORK-V4-BASE-PRICE-20261021

native_priority_v4.cにrs4_native_base_price/585960 bridgeを追加。現行search_current.pyで585960/4647D0/46F4C0/583A80を先に確認。585960はEDI=def、stack(output,key)、585AC6 ret8。価格返却は36byte ScriptData（vptr+0,string+4,size+14,capacity+18,int+20）。注意: callerのpush後leaを補正するとbufferは旧ESP+1C8であり、capacityをoutput+14と扱ってはいけない。容量16以上のheap文字列を原作delete5B6BBBで一度解放。原作関数のnew/delete所有権をDLL CRTへ渡さない。STATIC契約はnative_four_group_contract.jsonに保存。
TDD RED PID18556欠落symbol→GREEN PID29020 exit0。新3ケース（inline価格、heap価格/native解放、無効引数で出力不変）と既存relation/element/territory模擬ケースすべてPASS。PID17752 DLLbuild/PEcheck成功、SHA7c66776eca9712609fe9c783b0c95b6d84736ddbc213031b6417ab5754a5b952。新たな実機呼出・配置はなし。getterは本番分類にはまだ未使用、V4はrelation-onlyのまま。
残るP0: 5878A0(E DI target/EBX power)相性と46F4C0(ECXkey,stack ctx/default,ret8)係数、583A80(EDI,AL)傭兵判定を呼び、4D67EA..68B1と同じx87順序/64bit一時値/ftol2丸め/32bit積で最終価格を得る。基本価格だけで資金条件を満たすと扱わない。その後領地/資金/複数雇用者の成立度を集約し、本番rs4_prioritiesとhrs_ranked_firstへ接続。所属ロスターmode/取得時点と100件上限は継続VERIFY。原作/DAT/save、他レーン所有は未変更。新全体回帰なし、既知2FAIL未解消、Golden/MATCH0。


## WORK-V4-FINAL-PRICE-20261021

V4 native_priority_v4.cへrs4_price_arithmeticとrs4_native_faction_priceを実装。保存x86 4D67EA..6837/686C..68B1に基づき(100-affinity)*percentを64bit一時保存、係数*percent→base*一時値→fmulp→half加算→元ftol2入口、ADD32bit wrap、追加補正はIMUL32bit後x87という順を使用。FPU制御をDLL独自値に変更しない。最終価格adapterは585960の基本価格と解放→5878A0(EDI target/EBX power)→46F4C0(ECX key/stack ctx,default/ret8)→通常補正→target+75/+77時だけ583A80(EDI,AL)をemployer優先/target次の順に評価→倍率1000/33系の条件補正。元EXE内constant/ftol2をbase相対で利用する構成。勢力プレイ・def行用のみ。人材プレイ/非def行を勝手に同じ扱いにはしない。
TDD: arithmetic RED PID21396→GREEN PID14284、最終価格RED PID28088→GREEN PID26872 exit0。新7計算例（通常/ゼロ差/係数/二段補正/負値丸め/IMUL32bitoverflow/ADD32bitoverflow）、FPUcontrol/TOP維持、無効引数、4本のnative呼出模擬連結（通常、employer特殊、target特殊、両方false）PASS。既存relation/element/territory/property試験もPASS。整数変換はテスト用x87切捨てstubであり元5D1B80実行ではない。原作MATCHとは扱わない。PID13220 DLL build/PEcheck成功、SHA29d8c854f09caab3439876dfbbbe40c0f93a7a613b8c80bdde0c8976a060506e。未配置・実機未実行。
次P0: rs4_prioritiesの共通入力読取を使い、wnd+98→controller+4のmanagerとmanager+20C power+5C資金を検証、個々の雇用者の関係/領地/最終価格を4分類に集約。表示order0,1,2,3と集約優先0>2>1>3を区別。hakushin_recruit_sort_v4.cからhrs_ranked_firstに接続し、1候補でも4条件/複数雇用者/unknownを模擬統合試験。その後ロスター取得時点診断・原作実機。現行描画本番はrelation-onlyのまま、完成ではない。元EXE/save/DAT変更なし。全体Python未実施、旧2FAIL残存、Golden/MATCH0。


## WORK-V4-FOUR-GROUP-STAGED-20261022

ユーザー方針: 一度に複雑な機能を実機へ投入せず、小さな試験を繰り返す。今回V4 native_priority_v4.cの共通入力読取へ四分類モードrs4_four_group_prioritiesを接続。manager/power/fundsを検証し、各候補のリンク→領地→原作最終価格→signed資金比較で分類、複数雇用者は0>2>1>3で集約。非def行/勢力なし/領地unknownは明示拒否で出力不変。既存relation-only入口rs4_prioritiesと描画側は保持し、ゲームへの適用はまだ切替しない。
段階1 RED PID15948 missing symbol→GREEN PID29836 exit0。1候補/1雇用者で4分類、資金同額と1不足、欠損情報/unsupported modeを確認。段階2 PID29188: 2雇用者で最初のリンクあり候補が高額でも次の安価なofferを採用、全員資金不足ならrank2を確認。新8シナリオと既存全native模擬試験PASS。rect_sort_core.hは共有headerの未使用警告をinline化で解消、再コンパイルの10000矩形ケースPASS。DLLbuild/PEcheck PASS、SHA67365f3ae8b15d22ff43f6864f1362f7dccfdc08517b04a0d5dbe25b3abd815f。原作実行/ゲームフォルダ配備なし、Golden/MATCH0。原作/save/DAT・他担当未変更、Git書込操作なし。
次: 段階3として複数候補の4群表示順と矩形/hover対応を検証する。さらに実機はまず判定結果の記録だけを行い、原作画面の各候補と照合してから表示順変更へ進む。最新Ghidra正本/検索CLIは10/21 FunctionRepair/current canonicalを継続。現行rendererはrelation-onlyであるため四分類画面完成とは報告しない。ロスター全所属/hover絞込との区別、表示更新タイミング、100行上限、個人プレイは残るVERIFY。旧全体Python2FAILは未解消。


## WORK-V4-STAGE3-20261022

PID12276 exit0: stage3 seven candidates/four-group stable order/native IDs unchanged/hover rectangles/exact restore PASS。既存stage1/2およびnative模擬試験もPASS。テストのみ追加、DLL再ビルド・配備なし。実機判定と描画は未検証。段階試験方針を維持。


## WORK-V4-DIAGNOSTIC-20261022

Opt-in HAKUSHIN_SORT_V4_DIAGNOSTIC=1: original renderer retained, four-group classification logged once; retry limit8; filtered views do not consume attempts. No sorting/present/RECT write in diagnostic branch. Engine query scratch side effects remain, so not a read-only observer. Tests: new renderer-dispatch synthetic4 PASS, all existing priority tests PASS, rectangle10000 PASS (PID21688 exit0). DLL SHA975362f28923e6177a0c38588517f3a7859d96b81bd08d57300d51b6057e4b1e. Loader-only2 PASS PID23040, OEP/gameplay not executed. No game-folder deployment. Actual classification remains VERIFY.


## WORK-V4-ACTUAL-SORT-20261022

Production renderer now uses rs4_four_group_priorities + hrs_ranked_first. Real Windows GDI synthetic row colors and inverse RECTs PASS; unknown result preserves window. 6 renderer tests PASS PID1552 exit0; build/PE PASS. DLL45540b5f10352135e97d96d7bcd6a94620a7280e30770a93542767705aa96b0c deployed with user-authorized closed-game replacement, baseline backup retained. ACTUAL diagnostic17rows/5employers/78calls/6rank0/11rank3. Native yaju UI press gate1 for kbs,kuso,pinegaki,tnok agrees with aggregate rank0. ACTUAL user confirms visible sorting and Reset reapplication in PID17564. Log includes startup roster skips -8/-9; retained without suppressing. Territory/funds edge cases and hire click unverified. No original EXE/save modifications.


## WORK-ORIGINAL-EXE-ATTACH-20261022

Original EXE image750000 accepted with existing identity checks. Added UI-thread WH_GETMESSAGE bootstrap, module PIN before install, nonce reply, temporary hook removed after completion. New host self-test rejects non-game process as expected. Actual original PID32128/UI32132 installed1, four-group rendering logged, user confirms visible sorting. DLL b050fbda01cd82159301bffe6e9c8324da9ad02113c1b393daaa4036257ec634. Disk original hash unchanged. Runtime is extended, not pristine-original observation. Launch script CheckOnly PASS; full scripted launch not yet executed (equivalent split launch executed).


## WORK-STARTUP-RECOVERY-20261022

Startup incident: user reports exit during script loading. Original EXE disk SHA unchanged. No residual game; unextended original PID30164 exited0 within5sec. Causality unproven. ZIP CRC/root+script compare612 matched, no changed known files, extra work_observation.dat. User extracting ZIP concurrently; no Work extraction/deletion/overwrite. Original runtime at funds495 recorded prior to extension; later extension hireable0/calls17, roster completeness unresolved so not full funds PASS. See staged_on_pc.json startup_recovery/funds_short_session.


## WORK-V4-DEFERRED-ROSTER-20261022

実機PID28584/base270000: 原版SHA確認・旧DLL b050...接続installed1。資金495、所属5、候補17。ログhireable0/calls85/First four-group rendered後、resetでroster0によるreason-9、後の読取ではroster5かつRECT原順。資金不足分類そのものが原因とは未確定、リセット途中の所属一覧準備待ちから再適用されない経路を修正。途中snapshot保存照合のAssertionErrorはtuple/list JSON変換の観測側ミスであり、ゲームの不安定状態の証拠ではない（会話説明を訂正）。
変更: src/hakushin_recruit_sort_v4.cにUI thread SetTimerによる16ms/最大8回の限定再試行を追加。分類reason-8/-9のみ対象、別renderer呼出でpendingを取消。candidate tags/sourceDC/count/選択雇用者/hover/modeが変われば中止。native rendererや候補構築・資金処理は再実行せず、既存分類→GDI/RECT→presentのみ。成功snapshotのログに4群件数を追加。tests/test_diagnostic_win32.cに準備完了後の再試行、上限8、選択変更時取消、雇用可0でもrank2をrank3より前へ出すケースを追加。RED PID32036→GREEN PID12276(9PASS)→最終PID27856(10PASS)。timer callbackは合成試験で明示呼出し、原作message pumpでの成功は未確認。
修正版DLL build/PEcheck成功: SHA533054961ce3b37450fb5caf40e2f5eb99c2d7ad36a77734df01748ddd5e0c65、231424bytes。ユーザー終了承認後、旧DLLhashを照合し研究dist正規DLLへ差替・読戻一致（.next.dll同内容も保持）。原版EXE/DAT/saveは変更なし。tools/launch_original.ps1でPID13368を1つだけ起動したが、起動直後の接続はreply0 timeout。process生存/応答/拡張未loadを確認し、同一PIDへattachのみ再試行→UI31040/reply1/installed1。二重起動なし。launcher早期接続のtimeoutは別VERIFY。ユーザーへ低資金save→人材雇用→Reset→一覧外マウスを依頼、結果待ち。全体Python未実施・旧2FAIL残存、Golden/MATCH増加なし。
次: 修正版の実機groupsログ/Deferred roster-ready/RECT順を確認し、資金不足がrank2として残ることを照合。領地が別雇用者で成立する場合はそのofferを優先する既存0>2>1>3集約を維持。全完成とは扱わない。


## WORK-V4-RESET-ONCE-20261022
ユーザー実機報告: 前版533054...はリセット2回目で変態糞娘先頭の並替え成功。資金495、原作ログgroups=0,0,6,11（資金不足6/リンクなし11）とDeferred roster-ready確認。分類の資金不足分離は動作しており、1回目の不完全表示は残る。
修正: 即時分類をやめ、全員表示の分類/並替えをnative rendererの呼出元が戻った後のUI timerに統一。空でない未完成ロスターでも早期判定しない。deferred完了後は元repaint引数が0でも必ずpresent（呼出元は既にreturn済みのため）。古いpending取消・candidate/画面state検査・最大8回は維持。分類ルールは変更しない。
tests/test_diagnostic_win32.c: native renderer直後はclassifier0回、timer後に分類/RECT/pixels/present1回を確認。RED PID31968→GREEN PID30828→最終PID14852、関連10PASS/FAIL0。src/hakushin_recruit_sort_v4.cと当該testのみ変更。DLL build成功、SHA420baf22e0d89224b379c7c370549fafe09198c5d8700dab79844489779c5f0d。原版SHA確認、ユーザー終了/差替許可後distの正規DLLへ配置・hash照合済み。原版PID33044を単独起動、次は同一PIDへDLL接続→低資金save→Reset1回の実機検証。現段階で1回での成功は未確認。原作/セーブ未変更。


## WORK-V4-RESET-ONCE-ACTUAL-20261022
ユーザー実機確認（PID33044、DLL420baf22...）: 人材雇用を開いた時点で既に並替え済み。Reset1回で一瞬原順が表示され、その後自動で並替えされる。旧「2回押す必要あり」はこの操作で解消。game logのDeferred roster-ready view renderedも確認。起動時/Reset1回の再適用はACTUAL_USER_CONFIRMED。全4条件/全セーブ/雇用後の完全検証ではない。残る問題は原順の一瞬表示（deferred適用前の描画が原因候補）、領地不足rank1の実機照合、実雇用後の更新、launcher初回接続timing。関連10PASS/FAIL0、原作EXE/DAT/save変更なし。追加の再起動依頼はせず、この動作版を維持。


## WORK-V4-DISTRIBUTION-PREVIEW-20261022
雇用後の問題を実機で特定: reason-11、所属6/候補16。新規雇用者のdef+160 friend-cache件数0をDLLが全体拒否していた。保存current Ghidra 586080→586AB0→586320を再利用し、原作が必要時にfriend情報を生成する枝を確認。native_priority_v4.cの4分類製品経路だけは件数0でも原作判定へ渡す。旧relation観測入口のwarm-only制限は保持。friend_num/friend_ex生成はRNGを使用しうるため、RNG完全中立とは扱わない。元の定義/セーブを書き換えて埋める実装はしていない。tests/test_priority_win32.cへcold employerの原作側初期化stubを追加、RED PID28924 exit80→GREEN PID2292。native suite11 PASS表示（複数ケース内包）＋renderer13PASS、失敗0。
DLL SHAffdc73d2f416ab29d89089bdafee487b712b85d693426c31db4539bac3e0c981をユーザー許可後配置・hash検証。原版PID27644/UI21416への接続成功。WaitForInputIdleだけでは初期接続reply0を防げず、同一PIDへの再接続でinstalled1。ユーザー実機:「雇用後も自動で並替わった」。KBSトリオ雇用自体も成功しており、左欄を見る手動操作が必要な問題は今回解消。領地不足の実機試験・ちらつきは残存。
配布依頼を受けdata/recruit_sort_v4/dist/HakushinRecruitSort-0.1.0-preview.zipを作成。原作EXE/DAT/MAP/素材/saveは同梱しない。6 entries: DLL、attach host、portable launch_original.ps1、START.cmd、README.txt、SHA/size manifest。配置はゲームのVahren.exeと同じ階層にHakushinRecruitSortフォルダを置きSTART.cmd実行。元EXEhash限定・既存ゲーム起動中拒否。
launcherはreply0/installed999時のみ同一PIDへ最大3回再試行、拒否応答/ゲーム終了では中止。tests/test_launcher_retry.ps1 4PASS（成功、拒否、3回上限、終了済み）。CheckOnly PASS。起動全体の配布版実機試験は未実施とREADMEに記載。
ZIP SHA: 27040aa51b02c497ce2824986f7f44130dc7ebee3f7748c3be97ad934a4fb9f0
ZIP CRC/全entry byte一致/原作データ非同梱を検証。tools/package_preview.pyで再作成可能。README_DISTRIBUTION.txtに確認済み範囲・ちらつき・領地不足未検証・100件上限・RNG副作用を明示。配布はユーザーが行うため、外部公開/アップロード/Git release等は未実施。
