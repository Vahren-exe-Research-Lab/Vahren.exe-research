# B-20261013-1814-01｜WRQ-B-SKILL / B-MT-02 heal candidate attr-name gate and empty-vector divergence
[DATE/OWNER/STATUS] 2026-10-13 18:14 JST、T012 primary/T013 reference、READY-STATIC-SAVED-X86-BOUNDED。実原作Gameplay Golden PASS0、新strict MATCH0、Task DONE+0。
[SOURCE] B既保存 `exe/T012_HEAL_ATTR_PROBE.txt` の `heal_status_core 0x551490..0x551E4A` 命令をLocal Compact read-onlyで再利用。新EXE命令取得・原本実行/改変0。関連既存B `data/T012_BATTLE_CALC.md` §49–53、`data/T012_T013_WRQ_SKILL_INTEGRATION_BRIDGE_20261013.md`、Work `native_heal_mutation_subset.py`（read-only）を差分照合。
[VA/INPUT] add2/selectの各caller 5515A3/5515C9/551651 は551653へ合流。551653はglobal scratch [B0AAE8]=begin/[B0AAEC]=end を引いて28B stride数を符号補正除算で算出、zero時551678 JE551DEB、nonzero時551690へ。
[EMPTY-BRANCH] 551DEB push 637E04→551DF0 call5B5BBA、後段551DF5..551E4Aにはcleanup/RET4。5B5BBAの実作用・必ず帰還するかはVERIFY。候補0を暗黙の『通常成功0件』と同一化しない。
[RECORD/PRELOOKUP] 非空で551690はindex offsetをbeginへ加算、5516B8 call402710で候補内stringをlocal SSO scratchへcopy。5516D0から table [68D420+index*4] のNUL終端名前長を走査し、55170B call402C40の比較結果と長さを組み合わせて一致判定する。
[MATCH/NO-MATCH] 同じ比較後、一致なら55172B→551738に進み属性indexを[esp+1C]へ保存、551753 call550D80でamount計算へ。失敗は55172D index++、55172E CMP index,0x13、19未満なら5516D0へ、全19件不一致は551733 JMP551D40（対象attr作用本体551753/551924を通らず後処理）。
[NEXT-CANDIDATE] 551D40でscratch begin/endを再読、551D50でrecord offset+=0x1C、551D55で補助offset+=8、551D6F++candidate ordinal、551D76で最新countと比較し残りがあればcleanup後551690へ、尽きたら551E09/551E4A exit。recordの属性名解決失敗と空vector初期分岐は別stage。
[BOUNDARY] 402710/402C40/5B5BBAの全失敗・例外・allocationやRNG副作用は別VERIFY。callback registry B保存 `exe/T013_A18_A1C_CALLBACK_MAP_20261012.txt` のtable65BC60は独立の19属性登録表で、ここで参照する68D420と文字列・indexが同一だとは未証明。全合法DATで不一致が起きるか/実回復結果もVERIFY。
[DELTA] 既存T012の551653候補数と551D40ループはREADY済なので再加算しない。今回の独立差分は **per-candidate 402710 SSO copy → 19-name scan → no-match skipと、zero-vectorが5B5BBAを通る分岐の区別**。WIP Workは551653以降未接続、attribute-indexが既に確定した `native_heal_mutation_subset.py` だけではこの前段の原作pathを代行できない。
[REIMPLEMENT] Work ownerは scratch generation/end/begin/28B record index、raw attribute name + length/SSO、19-entry comparison index、matched/unknown、zero-vector branch VAとchild status、already consumed MP/chance/RNGを個別receipt化。全不一致の場合も『MP/RNG消費をなかったことにする』最適化禁止。child不明時はfail-closed/VERIFY。
[GOLDEN] 原作で合法なattr既知名（hp/attack等）と未知/独自名のeffective Skillを確認後、候補0/1/2・最初の名前一致/不一致/末尾一致・先行MP/確率、可視HP/状態/次行動/次RANDを同seed比較 DESIGNED/NOT RUN。原作Gameplay actual PASS0/strict MATCH0、未知属性が合法に到達する保証無し。
[NEXT] owner保存 `0x551924..551C7F` の実stat writerと本名解決stageをWorkへ別境界として受渡す。5B5BBAの意味は保存済み独立証拠が許可されるまでVERIFY。拒否済415530/415460/4E13F0/4C28D0/4C5CC0/579A20/5710C0..571500の新規取得や別tool/path迂回は行わない。
[SCOPE] B所有data/exe/HANDOFFのみ変更、MASTER/T018/他レーン/REA/dev_lab/Work/WRQ/Git/Remote/設定/schedule/原本は不変更。正式統合はEのみ。
[STATUS] READY（saved native bounded attr name guard; old gameplay not observed）
