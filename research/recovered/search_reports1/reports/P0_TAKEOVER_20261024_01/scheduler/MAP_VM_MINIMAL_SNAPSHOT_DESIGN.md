# MAP/VM 最小追加snapshot設計
研究ID P0_TAKEOVER_20261024_01。DESIGN ONLY。probe実装0、原作操作0、共有script変更0。
元EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
entry/ENTRY_FINDINGS.md と既存Stage14、scheduler保存命令を再利用。新発見数やnative成功を追加しない。

## 採取境界と予算
次probeのeligible C1=004C2935で、Wait前・Wait後かつ原作continuation前に同じ項目を読む案。
run/session/battle_seq/snapshot_epoch/thread/Task pass/index/E/G/main_snapshot_digestに紐付ける。
MAP/VM追加は診断sidecarとし、workerへ全VM命令列や全MAPを送る変更を今回要求しない。
追加予算案は各snapshotでraw読取4KiB、200 read、JSON16KiB、soft時間予算5ms。数値はcollectorの提案であり原作上限・達成済み性能ではない。
時間超過ならoptional読取を止め、BUDGET_EXCEEDEDと既読値を保存。5msはメモリread一回を途中で止めるhard deadlineではない。

## VM：headerだけでなく実PCを読む
現行state.vm_headerはE+1EED78から64byteで、四vectorのheaderを含むが別メモリにあるPC値そのものは含まない。
四vectorのbase offsetsは1EED78 / 1EED88 / 1EED98 / 1EEDA8。各12byte begin/end/capacity、要素4byte。
意味はblock pointer / PC uint32 / mode raw32 / frame-kind raw32。順序とzero要素を保持する。
全depth<=64なら四stackのactive要素を全部読む。最大64*4*4=1024byte。命令列を全部読む必要はない。
depth>64ではheaderとtopだけをTOP_ONLY_LIMITEDとして記録し、full stack digestを出さない。64は観測予算でありengine限界ではない。
top block pointerが指すvector header12byteとtop PCを照合。PC==block_lengthは合法な末尾。PC>lengthはPC_OUT_OF_BOUNDS。
PC>0なら直前要素、PC<lengthなら次要素のpointerを各1つ読む。ScriptElementのpayloadや命令列全体はコピーしない。
Start onEnterのScriptBattle引数が別途記録済みなら「直前要素との一致」を診断する。捕捉がなければUNKNOWN。
00433B1B/1CでPCはhandler前に増加済み。再開のためにPCを戻す・Startを再実行する設計ではない。
指標: four depths、深さ一致診断、top PC/length、at_end、全active stack取得範囲、header再読一致、stack digest前後一致。

## MAP：owner chain、寸法、固定25点標本
G=ptr32(E+4)、M=G+1EF570は埋込object。owner=ptr32(M+E8)がGと一致する場合だけgrid=ptr32(owner+90)へ進む。
M+90をgridとして読まない。E==G+504は既知Scene経路の補助整合条件であり、owner不一致を引算で補修しない。
grid+60から32byteだけで3層row_table pointers、width(+6C)/height(+70)、coarse寸法(+74/+78)とpointer(+7C)を取得する。
寸法はraw32も保持し、標本読取許可は1..4096各軸、積<=16,777,216とする案。これもcollector上限でありnative limitではない。
標本各軸はsorted unique floor(k*(dimension-1)/4), k=0..4。最大5x5=25座標、全3層でセル実値最大225byte。
row=ptr32(row_table+4*y)を層・選択行ごとに読む。行が隣接すると仮定せず、cell=row+x*cell_bytes。
cell幅は+60層1byte、+64層4byte、+68層4byte。0x80000008をそのまま保持し、+68 pointer様値の先は追わない。
coarse層はheaderだけ。既知の初期ceil(width/2),ceil(height/2)は診断値とし、runtime全意味の保証にしない。
Unit logical X/Yをgridのx/yへ変換する式は別途未証明なので、参加者位置から勝手にcell indexを作らない。
stable MAP IDとfile/generated/memory-input枝は別に観測できなければUNKNOWN。heap pointerを恒久MAP IDにしない。
map_sample_digestには標本座標とcoverageを含め、full_map=falseを必須とする。全地形digest・全オブジェクト取得と呼ばない。

## 数値境界・不整合
全pointerは32bit rawとして扱い、加算・差分・積を広いunsigned計算で検査してから読む。4GB wrapを許さない。
begin<=end<=cap、4byte整列、実読取spanのreadabilityを検査。全zero headerは空vectorとして別扱い。
0x80000000以上のpointerを一律無効にせず、実rangeで確認する。全memory走査や原作getter/VM関数呼出はしない。
owner chain/headerをdependent read前後で再読し、差があればINCONSISTENT_SNAPSHOT。counter一致だけでatomicとはしない。
読取失敗を0で埋めず、MAP/VM群だけUNKNOWNにして既存core/名簿証拠は保持する。
VM complete stack digestとMAP sample digestを別々に記録し、coverageが違う前後を同等比較しない。
heap pointer込みdigestは同run/同battle比較専用。別runの論理状態比較には直接使わない。

## 次回の観測指標と限界
VM header一致でもPC stackが変われば、現header-only比較が見逃す進行を検出できる。
MAP header一致でも標本セルが変われば、標本範囲の変化を検出できる。一致しても未標本セル・object payloadは未確認。
採取byte数/read数/所要時間を実測し、上限超過・read失敗・PC異常・owner不一致を明記する。
これは元VMを保持したまま再開したことを補強する観測設計であり、VMの移植、全入力取得、全状態凍結の証明ではない。
再開地点: 親が次probeとして採否を判断して別実装・別観測を行う。現在ready中のscriptへは反映しない。

