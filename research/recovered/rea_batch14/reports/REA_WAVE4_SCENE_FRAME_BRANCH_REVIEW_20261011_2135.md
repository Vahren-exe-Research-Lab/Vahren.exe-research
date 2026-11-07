# REA独立静的監査: 0x432EE0 scenario/event frame install（2026-10-11 21時台 JST）
対象はver0.67承認済みコピーの保存済みREA/Ghidra証拠のみ。新規逆コンパイル・原本EXE実行なし。研究T006/T010/T014への照合候補であり、A〜E/MASTER/T018は編集しない。
source/end SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。run=20261011T114202395Z、VA=0x432EE0、関数長1663byte。5方法VERIFIEDは既存runに由来。
Evidence IDs: info=ev_c97f4e962b1489302846931cefa60a172f2cfb249b372a5cb9d7f1dfd132615e
pseudo=ev_9a8d40a12039ddb3d2876b7644bb5182e229138268bb4af87e0f64df9ad94e28
assembly=ev_10ab11de19b6a7f2b68a0776da8d3f12544384752ac74fb6cc1abbf2cc2d1322
callers=ev_586a711d325329f445e5788d742d8bffb32677196d2b04cc8ad35a64bd9bbfb6 (9件)、callees=ev_3661abc5445d8faaab750d4e20ed0e952bfd8ea0b348e4ede70ac82c38f67276 (19件)。

## 保存済みpseudoとassemblyの交差観察
- 0x432F39は0x4647D0で`scenario` propertyを参照、0x432FB5は0x465060で`event`を参照。0x433017..0x43306Fは入力文字列とstatic `politics`値を比較し、一致時だけScriptFunc関連のlazy初期化/0x4C1290側へ進む（0x433071..0x4330E2）。この文字列比較のみで全phaseの政治ターン順序は証明しない。
- 0x433121は第3引数を0判定し、非0だけ0x433141で0x46E250を呼ぶ。0x43312E..0x433140は**第3引数==2**を1、それ以外を0として別引数に変換。結果が空でなければ0x433168..0x4331FDにて選択結果を局所vectorに順次追加する。第3引数0はこの候補収集をskip。
- 0x433207は第2引数(byte)を0比較。**0でないとき**0x433215以降へ進み、+0x1EED7C, +0x1EED8C, +0x1EED9C, +0x1EEDACに対応するframe-vector末尾を個別に延長する（後続vectorへの0値投入やreserve分岐あり）。
- **第2引数0のとき**0x433423へ分岐し、+0x1EED7Cへvector追加、0x4334A0で0x4365F0、+0x1EED9Cへ追加、0x433507で0x436080へ進む。4本のframeを常時同じ形でpushする実装にはしない。
- 0x432EE0自身のGhidra解決済みcallerは0x4342A0,0x434CC0,0x434EB0,0x471E80,0x48C880,0x4922A0,0x493630,0x4D79C0,0x51F3B0。各callerが実際に渡す第2/第3引数の意味はまだVERIFY。

## 厳密な未確定事項・実装側への境界
確定できるのは直接CALL、引数分岐、局所frame追加というSTATIC契約。関数名「world/fight/politics phase dispatcher」はキューの仮称であり、この1関数が全phaseを直接dispatchすることは未証明。0x46E250のfilter、0x4365F0/0x436080副作用、nested event/routine stack整列、参照先生存期間、正常gameplay traceはVERIFY。
次回は先行重いJava/Ghidraがなければ新Wave5の通常run、並行プロセス存在時は本9 callersの保存nativeから引数追跡を軽量実施。Wave1=16/16、Wave2=10/10、Wave3=10/10、Wave4=12/12（全てSTATICのみ）。Wave5=0/16 TODO、累計48/64、今回新関数VERIFIED0。
PCガード: 事前RAM15.28GB/CPU22%/Java0/active.lock=falseだったが通常`run_decompile.ps1`直前ガードでRAM14.46GB・先行java PID7164を検出、重い起動をskip。別shell/tool/Remote迂回や先行プロセス終了なし。旧EXE gameplay golden PASS0、研究DONE9/34、ゲーム再実装率は未測定。