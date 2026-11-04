# T013｜Troop RTTI・仮想周期処理・半数以上の近接比率判定（V9静的研究）
ID: B-20261023-1708-T013-TROOP-RTTI-RATIO-GATE-01 / Owner B:T013（T024/T028は関連候補に限定）
日時: 2026-10-23 17時台 JST。状態: STATIC-PE-RTTI / STATIC-EXE-ASM / STATIC-V9-GHIDRA / INFERRED / VERIFY / NOT READY。
PRECHECK: Local Compact PC接続成功。MASTER既確認cp196/公式READY596、レーン規約、B HANDOFF、T011/T012/T013/T024/T028既存資料と拒否/未同期を読取。旧03～12時オフライン10件・02時訂正版は未同期。14:14拒否本文はPC未保存。
V9 PROVENANCE: search_index/00_START_HERE_UNIFIED_V9_20261023.mdに従いV9別名CLIを読取専用使用。既存PC標準search_current.pyはV3のまま。`build_unified_v9_20261023.py verify` = V9_INDEPENDENT_READBACK_PASS、SQLite quick_check/DB SHA照合。
V9 DB SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。元Vahren.exe現物SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回Get-FileHash再計算、一致）。
RTTI slot: PE HIGHLOW 0x00639A2C→0x0063F400（MSVC RTTI CompleteObjectLocator）、+0x0Cの0x0063F40C→TypeDescriptor 0x0068D034、TypeDescriptor+8実bytes=`.?AVTroop@@`。
Vtable: 0x00639A30→0x0051C9E0、0x00639A34→0x0056AB20、0x00639A38→0x00431910、0x00639A3C/40/44→0x0043B5A0。0x00639A30はTroop vftable先頭。0x0056AB20はslot+4のTroop仮想関数。
V9 refs-to 0x00639A30は 0x0051C92F（fn 0x0051C900）と0x00567F0F（fn 0x00567EE0）を2件、PE relocation即値slotは0x0051C931/0x00567F11の2件。両保存擬似Cは `*param_1=Troop::vftable`。実ランタイムvirtual callerは未捕捉。
旧16:18のDATA 0x00639A34→0x0056AB20、E8 direct caller0件は再発見計上0。今回の新規増分はRTTI型名・仮想slot確定と下記半数閾値・単一アンカー規則・局所状態更新。
Troop 0x0056AB20は+0x1Cが非zero、またはengine+0x1EF148が0なら周期更新へ進まない。通過時Troop+0x3Cを増加、`%100==0`の条件付き経路で0x0056ADC1/0x0056AE85→0x00569360を使用（他gateあり）。
0x00569360（Ghidra未検証prototype: `FUN_00569360(int param_1,double param_2)`）はTroop+0x0C/+0x10構成員vectorを走査。最初にUnit+0x1867C==0 かつ +0x1867E==0のUnitを「アンカー」に選び、同関数内で後続全員をアンカーとして再反復するのではなく戻り値を決定する。
候補パートナーはアンカー以外で +0x1867C==0 かつ +0x1867E==0。全対象候補パートナー数Nをdoubleで計上し、範囲条件を満たす数Mを別doubleで計上。単位加算に使用する 0x0063B048実bytes=000000000000F03F（double 1.0）。
距離側候補はアンカー+0x220/+0x224と相手+0x220/+0x224の座標差二乗和から `0x00569453 → 0x005E3B70`へ渡す。上限候補はTroop+0x34 + 2*アンカーUnit+0x228（Unit+0xB0/+0xA8/+0x1E530の代替0値条件あり）。正確なFPU特殊値はVERIFY。
原作ASM: 0x00569453 call 0x005E3B70、0x00569458 fild dword [esp+0x14]、0x0056945C fcompp、0x00569460 test ah,1、0x00569463 jne 0x00569473。不一致側はM加算しない。距離が閾値以下の候補をカウントする読みが擬似Cと整合（NaN/丸め別VERIFY）。
0x0063B050実bytes=000000000000E03F（double 0.5）。0x005694B2 fdivr / 0x005694B6 fcomp qword [esp+0x30] / 0x005694BF jne 0x005694D0→0 / 0x005694C1→1。STATIC制御フローでは N>0 のとき M/N >= 0.5 で返値1、未満は0（FPU unordered例外はVERIFY）。
N=0（有効アンカーに比較相手がいない）なら 0x0056949A の返値1へ。構成員vector長0も 0x0056937C je 0x0056949A で1、有効アンカーが存在しない場合も擬似C上1。0名/単独名を「士気低下」と扱わない。
仮定上、有効3名なら最初の1名以外の2名のうち少なくとも1名が範囲内で判定1。有効4名なら3名中少なくとも2名。これは数学モデルであり実機Golden PASSではない。
Troop+0x44は `0x00568080`で0へ初期化。0x0056AB20内部でも0へ戻す枝が2つ、`0x0056B0A7 mov byte ptr [ebp+0x44],1` の枝がある。状態保持の意味や他writerの網羅はVERIFY。
0x0056B0A1 push ebp / 0x0056B0A2 call 0x00569730 / 0x0056B0A7 set +0x44=1を現物ASMで確認。命令・移動の候補となるが、単純な士気/敗走フラグだとは決めない。
DEDUP: B-20261023-1519-T013-GROUP-AGGREGATE-LIFECYCLE-01の+0x34 writer、B-20261023-1618-T013-GROUP-SPACING-CONSUMER-01の0x569360・周期2 CALL・0x639A34 pointerを再READY計上0。T013 owner/B HANDOFFの`0x639A30`,`0x63B050`,`Troop::vftable`は今回保存前に一致0件。
REIMPLEMENT: Troopという所有クラスと仮想slot+4を識別し、Group/Troop構造を混同しない。距離判定は最初の適格アンカー基準のM/N式と空集合成功を候補仕様として分離し、FPU/ABI・動作到達確認まで本番互換実装READYにしない。
GOLDEN DESIGNED/NOT RUN: 無改変同一EXE/DAT/SAVE/MAP/入力・RNGで適格Unit 0/1/2/3/4、+1867C/+1867E、座標距離が境界±1、Troop+0x44=0/1、+0x3C 99/100/101。可視命令/配置/移動・HP/MP・候補順/ターンを時系列照合。
未解明P0: 0x0056AB20への実仮想CALL site、Troop+0x44すべてのwriter、0x00569730実副作用、0x005E3B70 FPU/NaN、+0x34算術ABI、士気・逃走/戦闘AIとの実関係。T011/T012/T024/T028の別P0は継続。
境界: PC標準V3/MASTER/他lane/REA/dev_lab/原本EXE・ZIP・DAT・SAVE/Git/設定/Work/scheduleは変更せず。過去安全拒否0x5710C0..0x571500、0x514C50、14:14 detailと他拒否済操作の再試行・迂回なし。原作実行0。
STATUS: 今回新規正式READY0、MASTER統合0、Task DONE0、原作Gameplay Golden PASS0、strict MATCH0。保存/readbackの実証はB HANDOFF追記時に別途記録する。
