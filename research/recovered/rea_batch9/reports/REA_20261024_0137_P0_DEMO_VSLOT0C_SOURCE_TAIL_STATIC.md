# REA-LOCAL-20261024-0137-P0-DEMO-VSLOT0C-SOURCE-TAIL-STATIC-01
日時: 2026-10-24 01時台 JST。owner=REA、P0=T010/T012、状態=STATIC / VERIFY / NOT READY / PC-SAVED-PENDING-READBACK。Golden未実測。
## 参照正本・先行研究・境界
- 承認済み専用コピー `rea_lab/targets/hakushin067_Vahren.exe` SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` を今回実バイト再計算。
- 統合V9検索DB SHA256=`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、`build_unified_v9_20261023.py verify`=`V9_INDEPENDENT_READBACK_PASS`。関数11950、参照243678。PC標準はV3のままで未変更。
- 既存 `REA_20261024_0043_P0_DEMOPERSON_PAIR_INIT_ABI_STATIC.md` と同READBACK、23Hまでの連鎖、REA README/QUEUE/PROGRESS、旧RUNの64/64同期、MASTER/所有規約を先読。既知+0x08初期化ABI・100代入・交差ポインタを再計上しない。
## 新規P0：二段階ソース選別と初期化仮想呼出しの接続
- `0x0040F383 E8 -> 0x00597B00` の返値EAXは `0x0040F388` で固定領域 `[0x008B8E60]` に保存。`0x0040F398 E8 -> 0x00583C70` の返値EAXは `0x0040F3A3` で `[0x008B8E64]` に保存。元の入力EAXは前者 `[0x008B8E48]`、後者 `0x0048F720` の戻り値。両方を同一取得関数と扱わない。
- `0x00597B00` は入力EAXの `+0xB0` が指す所有領域から `+0x2DC` を経由しリスト/ツリーを検索。候補オブジェクトの `+0x68` と `0x00415460` の比較値が不一致なら候補ポインタを返す。該当無しなら `[input+0xB0]+0x58` を返す。リストの意味・キーの型はVERIFY。
- `0x00583C70` は入力EAXの `+0x94` を検査し、非ゼロなら `[input+0x1A4]+0x58` へ。ゼロなら `[input+0x1A4]+0x2F0` の候補リストを走査、候補 `+0x20` と `0x00415460` の値を照合。不一致時は `0x583CDD MOV EAX,ESI` 後に `0x583CE6 E9 JMP 0x597B00`。一致のみ・空リストなら所有領域 `+0x58` を返す。
- **命令種別修正**: `0x583CE6` は `E9_TAIL_JMP`、通常の `E8 CALL` ではない。Ghidra擬似Cの `FUN_00597b00()` を呼出フレーム追加と見なさない。V9のnative索引と原本PEのrel32再計算が一致。
- 前回の `0x40F3D6/0x40F3F3` は2オブジェクトの主vtable+0x08初期化。今回、`0x4103D5/0x4103E2` がそれぞれ `[vptr+0x0C]` を `CALL EAX` すること、DemoPerson主vtable `[0x0063803C]=0x00447810` をPEから独立確認した。4件はすべて間接CALLで、通常E8 caller件数には現れない。
- **実行時の順序の制限**: `0x40F320` の通常直線経路では `+0x08` 初期化2回の後に相当量の処理があり、関数末尾で `+0x0C` を2回呼ぶ。直後の呼出しではない。中間処理・例外/早期return・実際のdynamic型は未証明。
## +0x14が状態フラグに与える影響（新しい入口ゲート）
- `0x447852 XOR EBX,EBX`、`0x4478D5 CMP [ESI+0x14],EBX`、`0x4478D8 JE 0x44861A` をnative確認。`+0x14` がNULLなら `0x4479C5 [+0xA5]=0`、`0x4479F5 [+0xA5]=1` の両代入より前に末尾へ飛ぶ。今回の呼出しでは+0xA5再設定が実行されない。以前の値や後続cleanupの全副作用は未検証。
- NULLでなければ `0x4479C5` で+0xA5を0にしてRTTI呼出し`0x4479CC -> 0x5E72E5`を行い、追加条件により `0x4479F5` で1に設定する。各陣営のソース選択とフラグ更新は同一一括処理ではない。
- `+0x20=100` は `0x514A95` の直前初期化値として以前確認済みだが、長い中間処理を挟むため `+0x0C` 実行直前にも100と断定しない。`+0x14` が常にnonnullとも、実戦でDemoPerson型が維持されるとも主張しない。
## 独立検査／静的証拠とGoldenを分離
- 同一承認済みPEをpefileでRVA→rawへ変換しCapstone x86で厳選31命令のバイトと命令を独立照合。主vtableポインタ1件、rel32転送先3件を追加照合（31+1+3=35検査）。選定命令の一致であり、全関数網羅・ABI全体検証ではない。
- V9 function: `0x40F320`、`0x447810`、`0x597B00`、`0x583C70`、`0x514A80` をread-only参照。`0x4103D5` 単体function lookupはNOT_FOUND（`0x40F320` の内部siteのため）。Ghidra疑似Cは機械出力でABI未認定。
- REA既存Wave1～5は保存済同期ログで64/64。新規正式 `info/pseudo/assembly/callers/callees` 完全セット0、VERIFIED+0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。原作Golden PASS0、strict MATCH0、完全複製率未測定。
- PRECHECK CPU29%、空きRAM7.66GiB、Java/Ghidraプロセス未検出、`active.lock` 不在。低空きRAMと版差・拒否Wave6・EPERM不整合が残るためGhidra/REA再実行0、ゲーム実行0。総作業時間は未計測。
- 原本ZIP/EXE/SAVE・A～E/MASTER/T018・旧REA RUN/QUEUE/PROGRESS・製品コード/Work/Git・V9 DB/PC標準・自動化は変更しない。既拒否VA/Wave6/エクスポートを再試行しない。書込は本固有IDのREA研究文書・証拠・後続readbackのみ。
## 次P0 / Golden設計（DESIGNED / NOT RUN）
- `0x0048F720` が第2ソースのEAXをどの型・条件で返すかを調べ、`0x00597B00` と `0x00583C70` の候補比較を元ゲーム同一戦闘runで照合する。 `0x40F320` 中間で+0x14/+0x20に影響する処理と、`0x4103D5/0x4103E2` 前のオブジェクト同一性・NULL条件を重点検証。
- 黄金条件: 初期化+0x08→候補選択→+0x0C両陣営、+0x14 NULL/nonnull、+0xA5変更、+0x20=100→4遷移、結果0/1/2を**同run同一時相**で捕捉するまで実測PASSとしない。
