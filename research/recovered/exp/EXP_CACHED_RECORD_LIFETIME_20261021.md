# EXP-COLLAB-20261021-2112-01 / CP01｜召喚経験値レコードRの配置と解放境界

- 状態: STATIC_ASM（既存P0のR返値位置）＋ STATIC_PSEUDOC（今回局所照合）＋ VERIFY。原作実機NOT RUN、新B READY0、E MASTER統合0。
- 原本識別: SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。Ghidra DB=search_index/search.sqlite（BUILD_MANIFEST PASS）。
- 先行重複: `../rea_lab/headless_analysis/search_index/P0_SUMMON_EXP_OWNER_REPORT_20261021.md`は+1C8=Rと0x577260/node+0x28を既報。現研究は**破棄側の同一オフセット**を独立再照合したcrossjoin。

## 機械的に追える配置（局所的事実）
1. `0x577260@0x5772B2`: 検索hit時 `lea esi,[eax+0x28]`。返値Rはtreeノードの先頭ではなく内部 `node+0x28` を指す（既存P0保存ASM）。
2. `0x577310@0x577380` → `0x57A6E0`: 召喚元ツリーへキー付きノードを生成。ノードの割当には `0x57A70F push 0x200` が存在（既存P0保存ASM）。
3. `0x54E7B0@0x54F07A` → `0x56F880@0x56FEAF`: 生成BattleUnitの `+0x1C8` がRを参照する（既存P0/T011）。
4. `0x543E00@0x543F21` → `0x5450C0@0x5450DA` → `0x5454D0`：BattleUnit内部の `+0x1E4B8` ツリーについて破棄経路がある（今回Ghidra保存擬似C確認）。
5. `0x5454D0` はtree nodeの再帰処理中、`FUN_004591f0(param_1+10)` を呼ぶ。ここで `int* param_1+10` は **node+0x28**。その後nodeのstring/heapを片付けて `FUN_005B6BBB(param_1)` でノードを解放する。
6. `0x4591F0` はUnitData相当payloadの複数内部vector/stringを破棄する関数である（局所Ghidra擬似C）。この呼出しはノード全体をfreeする前に発生する。
7. `0x55A000` → `0x543E00`、`0x55B010` → `0x55A000` の連鎖があり、`0x55B010` は引数flag bit0成立時のみobject自体もfreeするscalardeleting-destructor風コード（Ghidra擬似C）。

## 新しい限定結論と重要な不明点
- [STATIC/INFERRED] Rは独立の永続Unitを指す単なる参照ではなく、**0x200-byte検索ノードの+0x28に埋め込まれた値オブジェクト**である可能性が高い。先行P0のR取得点と今回のR destructor引数が同一オフセットで一致する。
- [STATIC] この破棄経路が起動すると、ノード中のR payloadが破棄されてノードもfreeされる。Rポインタを保存したまま後段処理が生参照する設計は危険。
- [VERIFY] `0x55B010` が戦闘終了時に必ず呼ばれるか、すべての召喚元に適用されるか、破棄前にEXPが戦略側へ同期されるか、間接virtualが他の解放経路を持つかは **未証明**。
- [DESIGN-ONLY] 別戦闘EXEの返却packetでRのネイティブアドレスだけを永続owner ID扱いしない。R生成キー＋召喚発動者ID＋経験値delta＋生存世代/commit時点を区別する候補契約。
- [EVIDENCE] P0既存raw `P0_SUMMON_CALLSITE_ASM_20261021.json`; 今回Local `search.py function 0x543E00/0x5450C0/0x5454D0/0x4591F0/0x55A000/0x55B010`。Ghidra擬似CのC++型・正確なvirtual解決は保留。
- [NEXT] `0x55B010` のvtable所有型、battle finish（0x493630・0x49B5C0）からの間接到達、戦略save writer 0x58EFD0とRツリーの実所属を読取専用で照合。原本Gameplay Golden PASS0。

## 重複照合・追加注記（重要）
- 本CP01のnode+0x28と0x543E00→0x5454D0→0x4591F0破棄連鎖は、既存独立資料 `HAKUSHIN067_EXP_DEEPER_20261021/CP12_SUMMON_CHILD_UNIT_LIFETIME.md` でも既報。新発見ではなく**PC正本での独立再照合結果**として扱い、発見数・READYを増やさない。
- 今回の差分価値は、PC上の既存REA P0報告と旧CP12を相互参照し、元の検索DBでデストラクタ実体を読み戻して一致を確認したこと。未検証のbattle-finish常時到達は未解決のまま。
