# REA owner research recovery 20261026 / 10H_23H

**Private owner intake, STATIC/INFERRED/VERIFY, NOT CURATED / NOT READY.** These 13 already existing source research IDs are preserved, not newly decompiled functions. The same source reports and evidence JSON hashes were measured read-only on the authorized REA research PC on 2026-11-02 JST. Source relative paths and bytes are included. Evidence candidates matched by report-hour are hash-only references and must be confirmed per-report by KB curator; original evidence bytes stay on PC. Machine-only static text excerpts below are selected from the old owner reports, not rerun native tests. Current PE/V9 real-time SHA not freshly measured in this intake, no game launched. Existing formal Wave1–5 64/64 not counted again. Golden PASS 0, READY 0.

### REA-LOCAL-20261026-10H-P0-DMUSIC-PERFORMANCE-AUDIOPATH-ABI-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_10H_P0_DMUSIC_AUDIOPATH_STATIC.md`; actual SHA256 `FFDBB66BBE0EDF99BE126ACB216B62C10E7B7E76485265898DB3D0B2A743F562` (6366 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_10H_P0_DMUSIC_AUDIOPATH_EVIDENCE.json` SHA256 `9A9E588D7FBE039F913FCFF079B4591B4C9F32958A040935B8CB0ED7452E2364`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 新旧の境界
  - 本回では原作PE・Capstoneおよび保存済みSQLiteの4BF630間接CALL索引が0x4BF64A/0x4BF66B/0x4BF685/0x4BF697の **4サイト** で一致。09時台の本文「3つ」は誤り、既存09時台ファイルは改変せず本記録で訂正。監査数値・過去成果は二重計上しない。
  - ## 新しいP0 VERIFY / ABIと失敗経路
- **Correction/remaining VERIFY:** - 4BF697後、本関数内に取得したAudioPathのRelease呼出しは見当たらない。GetDefaultAudioPathが参照を加算して返す場合のownership・繰返しvolume呼出しによる参照残存はVERIFY。ここでは確定リーク/クラッシュとは判定しない。 / - 実行時Interface GUID/vptrとGetDefaultAudioPath成功/失敗実態、4BF697のHRESULTを上位が利用するか、他箇所でのAudioPathのrelease、音声0/極小音量フェードの再現性は未検証。 / - INFO=INDEX_ONLY / PSEUDO=INDEX_ONLY / ASSEMBLY=TARGETED_SOURCE / CALLERS=INDEX_ONLY / CALLEES=INDEX_ONLY。5種類のREA独立完備0、正式VERIFIED追加0。正式TODO/VERIFY/BLOCKEDファイル書込差分0/0/0。Golden旧実機PASS0、strict MATCH未測定、完全複製率未測定。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-11H-P0-DMUSIC-COM-CONSTRUCTOR-INIT-GUID-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_11H_P0_DMUSIC_COM_CONSTRUCTION_STATIC.md`; actual SHA256 `F57FA63658F43E7AA77E746E6A74DBB0F82237390214A8F29A50988A8DAB66AF` (5310 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_11H_P0_DMUSIC_INIT_EVIDENCE.json` SHA256 `8139BC761F8BBFBB546BE069732F099D9E975D768B65E592214AB1D7A74EE7E9`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 10時台既報: `0x004BF685`=Performance8 vtable`+0xCC`→AudioPath取得、`0x004BF697`=AudioPath vtable`+0x14`→SetVolume、HRESULT未検査、音量用スタックスロットを出力領域として流用。
  - `0x004BD2A0`から`0x004BD3E4`で`0x004BE480`（373 bytes）へ直接CALL。既存SQLiteと原作機械語が一致。
  - `0x004BE4BF`で全体数`DAT_0065BED8`を読む。研究用PEの静的初期値は**1**（`01 00 00 00`）。実行時変更の不存在までは未証明。
  - `0x004BE4E0`はサイズ=`count*4`のテーブル領域確保、`0x004BE4EB`で`stream+0x70`へ保存、`0x004BE4F7/FA`で各スロットをゼロ初期化。
  - `0x004BE582`: `CoCreateInstance(CLSID_DirectMusicLoader, NULL, 3, IID_IDirectMusicLoader8, &stream+0x6C)`、HRESULTは`0x004BE588/8A`で検査。
  - `0x004BE5BA`: ループ内で`CoCreateInstance(CLSID_DirectMusicPerformance, NULL, 3, IID_IDirectMusicPerformance8, &table[i])`、HRESULTは`0x004BE5C0/C2`で検査。
  - `0x004BE5DD`: Performance8 vtable`+0xB0`の仮想CALL。DirectMusic8定義では**InitAudio**と整合。機械語で`0,0,0,8,0x40,0x3F,0`に対応する引数を積んでいる。
  - **新規P0 VERIFY**: `0x004BE5DD`の直後`0x004BE5DF`は`INC EDI`。InitAudio相当の返値EAXを検査せず次の要素またはエピローグへ進む。
  - `0x004BE820`の`0x004BEF20/27/2F`は`stream+0x70`から要素を選び、`stream+0x78`へコピーする。10時台のGetDefaultAudioPath呼出オブジェクトに到達する。
  - | `0x006096EC` | `d2ac2892-b39b-11d1-8704-00600893b1bd` | CLSID_DirectMusicLoader |
  - | `0x006096CC` | `19e7c08c-0a44-4e6a-a116-595a7cd5de8c` | IID_IDirectMusicLoader8 |
  - | `0x0060970C` | `d2ac2881-b39b-11d1-8704-00600893b1bd` | CLSID_DirectMusicPerformance |
  - | `0x006096BC` | `679c4137-c62e-4147-b2b4-9d569acb254c` | IID_IDirectMusicPerformance8 |
  - `0x004BE6B0`（353 bytes）が`0x00555CD0`の`0x00555E60`から呼ばれる。`0x004BE79D`でLoader8（+0x6C）を参照してRelease、`0x004BE7C0`でPerformance8配列+0x70を走査。
  - 配列の非NULL要素について`0x004BE7D7`でvtable`+0x98`、`0x004BE7E5`でIUnknown::Release相当のvtable`+0x08`をCALLし、`0x004BE7EA`で要素をNULLに戻す。
  - 初回テストは`56/57 FAIL`（`0x004BE566`と`0x004BE567`の命令位置を1件取り違え）。監査条件を修正し、**58/58 PASS**でJSON排他保存・読み戻し成功。テスト条件58個であり、58関数VERIFIEDではない。
  - P0: `0x004BE6B0`の`+0x98`の厳密同定と、`stream+0x70`配列領域を最終的に解放する経路を限定xrefs・ASMで追跡。
  - 続けて`0x004BE5DD`（InitAudio）失敗後、`0x004BF685`（GetDefaultAudioPath）へ到達する必須条件とAudioPath所有権を詰める。動的Goldenは未実測のまま。
- **Correction/remaining VERIFY:** - `info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY`。新規REA正式5種完備0、新規VERIFIED0。正式TODO/VERIFY/BLOCKEDファイル書込差分0/0/0。 / - PC online（SAITO）、`active.lock`なし。11時台開始時空きRAM約17.42GiB、CPU負荷不明。監査本体0.3577秒、研究全体所要時間は未計測。新REA/Ghidra/ゲーム実行0、Work不使用。 / - 続けて`0x004BE5DD`（InitAudio）失敗後、`0x004BF685`（GetDefaultAudioPath）へ到達する必須条件とAudioPath所有権を詰める。動的Goldenは未実測のまま。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-12H-P0-DMUSIC-CLOSEDOWN-ARRAY-OWNERSHIP-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_12H_P0_DMUSIC_CLOSEDOWN_OWNER_STATIC.md`; actual SHA256 `811939F8AF2B87381D5CED93FAE2CD39DCF958E1B4F60C98F6D20ABA78043379` (5862 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_12H_P0_DMUSIC_CLOSE_ARRAY_EVIDENCE.json` SHA256 `DC75026401BBE5781E7ACAD74F585D9C871CE7F9CD08AA9FCE22F28FF0510377`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 新旧成果境界
  - 11時台の既報: 0x4BE480でPerformance8生成とInitAudio(+0xB0)、0x4BE6B0で+0x98→Release(+0x08)、管理表+0x70の解放先は未解決。
  - *今回新規**: +0x98のSDK vtable順序による**CloseDown**同定、呼出元0x555CD0→0x4BE6B0→0x4BE600→親オブジェクトfreeの実命令順、+0x70の配列領域がこの破棄経路で直接freeされないこと、AudioPath成功時の参照数VERIFYを分離。
  - 0x004BE4E0: `CALL 0x005B5C0B` 管理配列確保、0x004BE4EB: `MOV [ESI+0x70],EAX`。
  - 0x004BE7C0: 管理配列読み取り、0x004BE7D0: `MOV EDX,[ECX+0x98]`、0x004BE7D7: `CALL EDX`（thisは直前PUSH EAX）。
  - 0x004BE7E1: `MOV EDX,[ECX+8]`、0x004BE7E5: `CALL EDX`（IUnknown::Release）、0x004BE7EA: 管理配列の当該スロットをNULL化。
  - 0x00555E60: `CALL 0x004BE6B0`（COM/音声shutdown）。
  - 0x00555E71: `CALL 0x004BE600`（親オブジェクトの他所有フィールド破棄）。
  - 0x00555E77: `CALL 0x005B6BBB`（親オブジェクト本体free）。
  - 0x004BE600: 0x4BE651/667/686のfreeは+0x80配下、+0x44、+0x28系であり、+0x70を直接解放する命令なし。
  - 0x004BE6B0: 0x4BE7B3以後の管理配列走査・NULL化〜ret経路に配列領域そのものをfreeするCALLなし。
  - ## 新規VERIFY：所有権を区別する
  - *V1 / 管理配列+0x70:** shutdownの各Performance8要素はCloseDown→Release→NULL化されるが、配列本体の動的確保に対応するfreeは確認した破棄経路（0x4BE6B0、0x4BE600、0x555CD0の該当直列部分）にはない。OSによるプロセス終了時回収を考慮するとゲーム中の増加リークとは未判定。別所の解放・初期化回数をさらに検査する。
  - *V2 / AudioPath参照:** 0x004BF685でGetDefaultAudioPathと整合するCALL後、0x004BF697でSetVolumeを実行して0x004BF69Bでreturn。返されたローカルAudioPathのReleaseは同一関数中にない。Wineの実装ではGetDefaultAudioPathの成功返却時にAddRefするため、互換実装で同じ契約なら音量更新ごとに参照が残る懸念がある。Windowsの実COM実装でのAddRefや回数は未確認、確定バグ・量的リーク値とはしない。
  - P0次候補: `0x004BD2A0`と`0x00555CD0`の全owner lifecycleを追い、+0x70配列が別関数でfreeされる可能性/初期化が複数回走る可能性を限定xrefsで検査。
  - 次点: `0x004BF630`AudioPathポインタの寿命とDirectMusicGetDefaultAudioPathの参照契約を実機トレース設計へ。GetDefaultAudioPath/SetVolume失敗時も別のゴールデン条件に分離。
- **Correction/remaining VERIFY:** **V3 / InitAudio異常:** 11時台のHRESULT未検査とGetDefaultAudioPathのHRESULT未検査を接続して、初期化に失敗したPerformanceが音量APIまで進む場合の異常経路をGolden候補にする。実機到達性不明。 / - 5方法: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。今回正式VERIFIED追加0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。 / - 12:36 JSTのPC SAITO online、active.lockなし、DBとPEハッシュ一致、空きRAM約13.44GiB。CPU単発値約9.7%。監査単体初回約0.356秒、保存時約0.379秒、全体所要時間不明。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-13H-P0-DMUSIC-DEBUGCOUNT-UPPERONLY-ALLOC-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_13H_P0_DMUSIC_DEBUGCOUNT_STATIC.md`; actual SHA256 `03B6E205298720600A7874D4864782659E25A141083B577CF69900193A5D65D8` (5626 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_13H_P0_DMUSIC_DEBUGCOUNT_EVIDENCE.json` SHA256 `77351B2188AF2CD20D558760F294FBF553A562B35F69D7284DDB947B6176982D`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 今回の新規発見と既存研究の切り分け
  - 12時台まで既知: `0x004BE480`が管理配列(+0x70)を確保、`0x004BE6B0`がPerformance8要素をCloseDown→Releaseし配列そのもののfreeは未確認。
  - *今回の差分**: 配列要素数`DAT_0065BED8`の全11件のGhidraデータxrefを取り出し、実際のwrite元を`0x00558000`の3命令（`0x5584B7/0x558506/0x558521`）に限定して観測。初期値は1だが静的な固定値ではない。
  - `0x00558000`は`debug_paper.txt`または`a_system/debug_paper.txt`を探して解釈する処理を持つ（検索DBの定義済みstring xrefも一致）。
  - `0x005554F0`の`0x005558AB`で設定関数`0x00558000`を直接呼び出し、その後条件付き`0x00555918`で`0x00555CD0`を呼び出す。
  - `0x00555CD0:0x00555DEF`→`0x004BD2A0:0x004BD3E4`→`0x004BE480`が管理配列生成の直列CALL鎖。よって**設定値が配列確保に先行する経路が存在**する。
  - `0x005B7576`は`_atol`（`0x005B7560`）への11-byte wrapperとGhidra索引上で確認。入力文字列の厳密な到達性は未実測。
  - `0x005584B7`で当該設定コマンドの初期値を1へ設定し、`0x005584F7`でテキストの数値変換、`0x00558506`で結果をグローバルへ格納。
  - `0x00558515`で`10`と比較、`0x0055851B`は**signed JLE**。10以下なら受理し、10を超えると`0x00558521`で10へ制限する。**下限側の明示的clampはこの分岐にはない**。
  - `0x004BE480:0x004BE4BF`で数を読み、`0x004BE4CD`のunsigned MUL 4、`0x004BE4CF`のSETO、`0x004BE4DB`のNEG、`0x004BE4DD`のORを経て`0x004BE4E0`で確保関数を呼ぶ。この算術は32-bit productに上位桁があると要求サイズを0xFFFFFFFFへ飽和する。
  - 静的算術例: 個数0→要求0バイト、1→4バイト、10→40バイト、-1→**0xFFFFFFFFバイト**。負値指定を経路上で許すなら巨大確保要求候補になる。
  - `0x004BE4F3/0x004BE4F5`はsigned `count<=0`なら配列初期化ループをスキップ。`0x004BE6B0:0x004BE7B5/BB`もsigned `count<=0`ならCOM要素解放ループをスキップ。
  - 初期値1なら配列長4バイト。debug設定による正値は最大10→40バイト。これらは`0x004BE480`単回の確保要求量であり、実際のヒープ占有量/反復回数ではない。
  - Ghidra xrefのwrite元はこの11件中`0x00558000`のみだが、未索引の間接書込や実行時改変の不在までは証明しない。
  - ## 独立監査・未確定項目
  - 最初は`index_writers_only_558000`を4命令と誤記し45/46だったが、`0x558515`はREADで、WRITEは3命令が正しい。条件を訂正後46/46、証拠JSONを排他作成して読み戻し。旧成果の数値・ファイルには非干渉。
  - 次P0: `0x005B5C0B`確保失敗経路、`0x005558AB`へ到達する起動条件、`0x004BE480`の負値/ゼロ分岐および旧`+0x70`配列領域のfree漏れと参照増加を区別して追跡。
- **Correction/remaining VERIFY:** - 最初は`index_writers_only_558000`を4命令と誤記し45/46だったが、`0x558515`はREADで、WRITEは3命令が正しい。条件を訂正後46/46、証拠JSONを排他作成して読み戻し。旧成果の数値・ファイルには非干渉。 / - 5方法は`info/pseudo/callers/callees=INDEX_ONLY`、`assembly=TARGETED_NATIVE`。新規REAの5種完全取得0、新規正式VERIFIED0、正式TODO/VERIFY/BLOCKEDファイル書込差分0/0/0。 / - PC SAITOオンラインを実測、active.lockなし。初回空きRAM約17.96GiB、CPU負荷・全研究時間は不明。単体監査は約0.36〜0.41秒。重いREA/Ghidra/原作ゲームは起動0、Work不使用。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-14H-P0-DMUSIC-NEW-TAILJMP-THROW-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_14H_P0_DMUSIC_NEW_TAILJMP_STATIC.md`; actual SHA256 `7126EEDD261AB3DE4BE72C676378E95F44FBCFB703240CCF52D4FC72C4F1B4D5` (5019 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_14H_P0_DMUSIC_NEW_TAILJMP_EVIDENCE.json` SHA256 `C84CD31ECAB6B14D129F2FCCB8FB077A0D7890DB7C634F5E031D0DB89FEAFFD3`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 13時台には `DAT_0065BED8` がdebug設定で0/負数になり得て、配列のnew要求量 `count=-1` で `0xFFFFFFFF` に飽和することを固定済み。2026-10-25 08～11時台のCRT _malloc/new-handler研究は、通常malloc失敗時のbad_allocとhandler初期化を解析済みであり、今回は加算しない。
  - *新規**: 配列確保の呼出先 `0x005B5C0B` は11バイトのホットパッチ形式ラッパーで、`0x005B5C11 JMP 0x005B6C2B` によって同じスタック引数を保ったままoperator new相当へtail transferする。
  - `0x004BE4DF PUSH ECX` → `0x004BE4E0 CALL 0x005B5C0B` → `0x005B5C11 JMP 0x005B6C2B` → `0x005B6C45 CALL _malloc` → 成功時EAX非NULLを保持して `0x005B6C50 RET`。
  - 呼出元 `0x004BE4EB MOV [ESI+0x70],EAX` には、直前の例外throwに対する明示的なNULL比較は存在しない。
  - *索引分類注意**: 新検索DBの `calls` に `0x005B5C11 → 0x005B6C2B` がUNCONDITIONAL_CALLとして登録されるが、実バイトはCALLでなく**JMP**。09時台に別関数で3箇所の同種例があり、今回は別のsiteを新たに確認した。
  - `count=0` → `operator new(0)` → `_malloc(0)` は `0x005B9BF9..0x005B9C03` でHeapAllocへ**1バイト**を渡す。成功なら非NULLを格納し、`0x004BE4F5`からCOM要素初期化ループを飛ばす。サイズ0は即NULLとは限らない。
  - `count=-1` → 要求サイズ `0xFFFFFFFF`。 `_malloc 0x005B9BD1 CMP EBX,-0x20` + `0x005B9BD4 JA 0x005B9C45` によりHeapAlloc前に巨大サイズ分岐する。`0x005B9C46 __callnewh`、`errno=12`、`EAX=0`で戻る経路を持つ。
  - そのNULLを外側new `0x005B6C2B` が検出し、`0x005B6C38 __callnewh` が0なら `0x005B6CA5 __CxxThrowException`（bad_alloc）に進む。**通常のNULL返却はしない**。
  - ## 独立監査と判定
  - まず `0x004BE480` のC++ EH unwinderおよび上位 `0x004BD2A0` のcatch/終了経路を限定調査し、bad_alloc時に`stream+0x70`やloader COM状態をどう破棄するか区別する。
- **Correction/remaining VERIFY:** 状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規REA正式VERIFIED=0、原作Golden実測=0。 / - 10/25 10時台の独立成果では通常CRT初期化後のhandlerはNULL、new-modeは0と整理済み。これが実際の状態なら `-1` はbad_alloc経路へ進み、`stream+0x70`への正常保存以前に制御を外れる（上位catch/終了処理は未検証）。 / 5種: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY。REA正式5種完全充足0・新規VERIFIED0。旧Wave1～5 64/64は過去同期ログの値を維持し二重計上しない。正式TODO/VERIFY/BLOCKED書込差分0/0/0。Golden PASS0、strict MATCH/完全複製率未測定。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-15H-P0-DMUSIC-EH-CATCH-SCOPE-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_15H_P0_DMUSIC_EH_CATCH_SCOPE_STATIC.md`; actual SHA256 `F6D435B697F4768999FD291297A96199839D4B2A83E3A30AD51635EE5923B066` (4869 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_15H_P0_DMUSIC_EH_SCOPE_EVIDENCE.json` SHA256 `BC153F1B5B9C979AD2548C000671646045F18586B2F0A81CA2E7035F50DB0657`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 既報14H: debug設定負数、配列 new の bad_alloc候補、0x005B5C11 tail-JMP、初期化途中の後片付け未解決。これらは新規成果に再計上しない。
  - 検索DBからCALL: 0x004BD3E4 (0x004BD2A0→0x004BE480)、0x00555DEF (0x00555CD0→0x004BD2A0)を照合。
  - ## 独立静的証拠
  - 子0x004BE480: EH handler 0x005E79BB→FuncInfo 0x00641AB0（magic=0x19930522, maxState=1, nTryBlocks=0）。
  - 子unwind map 0x00641AA8: state0→state-1, cleanup 0x005E79B0。機械語 0x005E79B4 CALL 0x005B6BBB（free系）。
  - 0x004BE4E0: +0x70管理配列確保、0x004BE4EB: pointer保存。これらはまだEH state=-1の段階である。
  - 0x004BE522: 別の0x5C byteオブジェクトを確保。0x004BE530でEH state0設定、0x004BE56Fでstate=-1へ戻す。unwindのfreeはこの一時オブジェクトに対するものと整合する。+0x70配列のfreeはこの子EH mapに存在しない。
  - 親0x004BD2A0: EH handler 0x005F2A36→FuncInfo 0x0064C28C（magic同一、maxState=7、nTryBlocks=0）。7つのunwind actionは一時new領域free、静的フラグ解除、局所文字列後片付け等であり、子の管理配列freeではない。
  - 上位0x00555CD0: EH handler 0x00600A68→FuncInfo 0x00657D10（maxState=3, nTryBlocks=1）。TryBlockMap 0x00657CFC: tryLow=0, tryHigh=0, catchHigh=2, nCatches=2。
  - Catch descriptor 0x00657CDC: RTTI名 `.?AVGameException@@`、handler 0x00555EBC。第2descriptor 0x00657CEC: catch(...)、handler 0x00555F02。**catchが存在しないわけではない**。
  - ただしBGM初期化call 0x00555DEF時のowner EH stateは-1のまま。保護対象のstate0設定は0x00555E3A（0x004B9930呼出0x00555E3D直前）、state-1復帰は0x00555E45。よって、この2本のcatchは **0x00555DEF経由のbad_allocを捕捉するスコープではない**。
  - 子0x004BE480と親0x004BD2A0はnTryBlocks=0。C++ EH登録自体があっても、それだけでcatchが存在すると解釈しないこと。
  - ## 結論と未確認
  - 上位0x00555CD0のcallerと更に外側のcatch（特にbad_alloc/例外全般）を検索DB→限定ASM→FuncInfoで追跡。次いで+0x70配列の全書込・free xrefsを限定調査。上位復旧確認前にGolden成功・クラッシュ確定・リーク確定とはしない。
- **Correction/remaining VERIFY:** [VERIFY] 2番目の0x5C byte newでbad_allocが発生すると、先に確保された+0x70配列についてこの子unwind mapによる解放が確認できない。上位の別クリーンアップ、process exception handler、実際のリーク/異常終了は未実測。バグ確定には昇格させない。 / [VERIFY] GameException/catch(...)は別のtryスコープのみ。BGMのエラーを捕捉するという以前の一般的推測があれば訂正する。 / REA5種: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規正式VERIFIED=0。旧Wave1–5=64/64は2026-10-11の保存同期記録、二重計上せず。正式QUEUE/PROGRESS TODO/VERIFY/BLOCKED書込差分=0/0/0。完全複製率・strict MATCH未測定。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-16H-P0-DMUSIC-CRT-SEH-XCPT-FILTER-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_16H_P0_DMUSIC_CRT_SEH_STATIC.md`; actual SHA256 `9AC24C4F23F16DFDEEA0789B2A8EC620E65148EDB9904B189FB7510CDCCFB9BA` (5947 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_16H_P0_STARTUP_SEH_EVIDENCE.json` SHA256 `CCD970E8F00B8434D53D2944BFA126C5B14B1E32FA017563BD9689595572EBCE`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 15Hで確定済み: 0x004BE480/0x004BD2A0にはC++ catchなし、0x00555CD0の2個のcatchは0x00555DEFの呼出位置を保護しない。今回は**さらに外側のCRT例外フィルタ**を新たに調べた。
  - ## 新規静的証拠A：DirectMusicからEXE entryまで
  - 0x004BE480（new失敗）→0x004BD2A0（CALL site 0x004BD3E4）→0x00555CD0（CALL 0x00555DEF）→0x005554F0（CALL 0x00555918）→___tmainCRTStartup 0x005B84D7（CALL 0x005B85EC）→PE entry 0x005B8644（0x005B8649はJMP）。原作PEとGhidra索引を照合。
  - 0x005554F0は本範囲の機械語内に自身のFS:[0]例外登録がなく、0x00555918の呼出し後に通常後片付け（0x00555929のDeleteDC相当、Direct3D関連Release、CoUninitialize相当）が続く。例外時に通常命令順へ戻るとは仮定しない。
  - ## 新規静的証拠B：CRTにはSEH4の外側フィルタがある
  - 0x005B84D9 PUSH 0x006412C0、0x005B84DE CALL 0x005BB680（__SEH_prolog4）。
  - scope header（0x006412C0）: FFFFFFFE / 00000000 / FFFFFF88 / 00000000。
  - scope row（0x006412D0）: enclosing=FFFFFFFE, filter=0x005B8606, handler=0x005B861A。
  - 0x005B8572でEH state=0に変更した後、0x005B85ECで0x005554F0を呼ぶ。従ってこの外側SEH filterは起動側のcallを覆う。
  - filter 0x005B8606は0x005B8612で0x005BE999（__XcptFilter）を呼ぶ。例外handler 0x005B861Aは0x005B862Aの__exit等へ分岐する。
  - ## 新規静的証拠C：C++ bad_allocは初期状態のXcptFilter対象外
  - 0x005B6C2B→0x005B864E（__CxxThrowException@8）経由のRaiseException用静的定数0x00609978は **0xE06D7363**。
  - 0x005BC596: CRT __initptdがPTD+0x5Cに既定例外表0x0060B198を設定。
  - __XcptFilterの0x005BE9BBは1件12byteずつ比較し、0x005BE9BEの表長は0x90(144=12×12)。不一致側0x005BE9D6/0x005BE9E3でEAX=0を返す。
  - 検索索引の ___tmainCRTStartup size_bytes=319 を関数先頭から直線的なbyte spanと仮定すると0x005B8616で終わり、0x005B8612のCALL命令末端や0x005B861Aのhandlerを取りこぼす。原作機械語では0x005B8643のRETまで続く。これは body size と線形ASM範囲を同一視しない警告であり、Ghidra DBの関数帰属情報そのものが不正だとは断定しない。
  - ## 独立監査・結果・差分
  - 3. 正常終了では0x00555929後のDeleteDC/Release/CoUninitializeが呼ばれることを比較。
  - 次P0：0x005BE999の例外表変更者・signal API経路と、0x004BE480 +0x70配列の全参照/後片付け有無を既存DBから追跡。原作クラッシュ・メモリリークの確定はGoldenまで保留。
- **Correction/remaining VERIFY:** **訂正**: 15H時点の「3関数のcatch外」を「更に外側にもcatchが無い」と拡大解釈してはいけない。SEH4フィルタは存在する。ただしそれがC++例外を処理するかは別問題。 / 正式QUEUE/PROGRESS TODO/VERIFY/BLOCKEDの書込差分=0/0/0。今回独立のVERIFYは「標準CRTフィルタがbad_allocをcatchしない」という条件付き仕様と、グローバルVEH等の存在未調査。原作ゲームGolden実測PASS=0、strict MATCH・完全複製率は未測定。 / PC接続成功、active.lockなし。空きメモリ約12.28GiB、CPU負荷16%（開始時PC全体の単発値）。研究総時間不明。新規REA/Ghidra/ゲーム起動0回、Work0回。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-18H-P0-CRT-SEH-ORPHAN-E8-XREF-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_18H_P0_CRT_ORPHAN_E8_STATIC.md`; actual SHA256 `434A0A6EF681794D3F2D1293896F6693D7EC7F19AD715DB15E0A37B2025212B6` (3704 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_18H_P0_CRT_ORPHAN_E8_EVIDENCE.json` SHA256 `2CCEF122498AE5B067202B6D2AE24B49266787915CFB0A9A1BE9638F8B2E49CD`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 独立静的証拠：3つの未索引E8
  - | 0x005B8612 | e882630000 | 0x005BE999 (__XcptFilter) | 0 | 0 |
  - | 0x005B862A | e8f62f0000 | 0x005BB625 | 0 | 0 |
  - | 0x005B862F | e816300000 | 0x005BB64A | 0 | 0 |
  - 原作EXEのPE ImageBase=0x00400000を使用し、各E8+rel32の転送先を個別計算。Capstone独立逆アセンブルでも3個ともCALL。
  - CRTのSEH4 scope record (0x006412D0) は filter=0x005B8606、handler=0x005B861A。つまり0x005B8606..0x005B8633の46バイトは例外処理用の実行コードであり、単なる未使用paddingではない。
  - 現行V3の0x005B84D7(___tmainCRTStartup)のfunction_rangeは 0x005B84D7..0x005B8605 (303B) と 0x005B8634..0x005B8643 (16B)。間の46Bはこの関数のbodyに属していない。
  - 比較対象の0x005B7CA7→0x005BE999と0x005B863E→0x005BB6C5はV3にE8として存在。索引全般の壊れではなく、今回の未所有例外funcletの限定的な参照欠落。
  - その結果、現行V3のcallers 0x005BE999は__callthreadstart側 0x005B7CA7だけを返し、CRT startup SEH filter側0x005B8612を表示しない。**V3の44,889件はGhidraに既登録されたE8参照の分類結果であり、EXE上の全E8の網羅証明ではない。**
  - ## 境界・リスク・継続
  - 次P0は0x004BE480の+0x70管理配列の例外時解放者を限定確認。また0x005B8612/2A/2Fは他担当へ修正要請する場合も静的索引欠落として渡し、Ghidra全件再抽出は禁止。
- **Correction/remaining VERIFY:** 状態: PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-26 JST） / 16Hで示した「初期状態の12種のCRT例外表にbad_allocコードE06D7363が無い」という条件付き結論を維持。今回、runtime signal登録/VEHの有無やゲームでの終端を追加実証していない。 / 新規限定監査: 20/20 PASS。info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_NATIVE、callers/callees=INDEX_ONLY（例外funclet欠落あり）。正式REA5種完備追加0、正式VERIFIED追加0、TODO/VERIFY/BLOCKED公式書込差分0/0/0、原作ゲームGolden実測PASS0、strict MATCHと完全複製率は未測定。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0.

### REA-LOCAL-20261026-19H-P0-DMUSIC-COMFAIL-V9-SEH-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_19H_P0_DMUSIC_COM_FAILURE_V9_SEH_STATIC.md`; actual SHA256 `15A885E9FDF3B77E2DB6CB8D28BF223B7C52A196993A9495D1A5EDE222CCE5BD` (3911 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_19H_P0_DMUSIC_COM_FAILURE_V9_SEH_EVIDENCE.json` SHA256 `F3D5CD6CE239546C8F5F1749BD36CB5E3807BC0AD933959C6F7F525AFEF70771`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## P0-1：CoCreateInstance失敗後、呼出元が通常処理を続行
  - 0x004BE480内では管理配列を0x004BE4EBで[ESI+0x70]へ保存する。
  - 0x004BE582のCOM生成後、0x004BE588 TEST EAX,EAX → 0x004BE58A JS 0x004BE5E8。
  - 2回目の0x004BE5BAでも0x004BE5C0 TEST EAX,EAX → 0x004BE5C2 JS 0x004BE5E8。
  - 共有出口0x004BE5E8～0x004BE5FAはフレームとレジスタ復元→RET 4。この出口には直接のReleaseや配列freeなし。
  - 親0x004BD2A0の0x004BD3E4 CALLから戻ると0x004BD3E9 LEA、0x004BD3F3 WinAPI CALL、0x004BD3F9 WinAPI結果比較へ進む。直後に子のHRESULTを調べない。
  - ## P0-2：統合V9でも3つの既知SEH E8が索引にない
  - 原作PEのE8 siteは0x005B8612→0x005BE999、0x005B862A→0x005BB625、0x005B862F→0x005BB64A。
  - 対照0x005B7CA7→0x005BE999は両DBで1件。従って3件の未収録はV3限定ではなくV9にも残る。
  - 次回はCOM失敗後に0x004BD2A0/0x00555CD0がcleanupに至る条件と+0x70の別free候補を追跡。SEH3siteはDB owner側へ必要性だけ伝え、既存DB書換え・拒否操作の迂回はしない。
- **Correction/remaining VERIFY:** 部分初期化のcleanup到達性、参照保持、実機クラッシュ・リークは未実測でありVERIFY。 / 推奨V9のverifyはV9_INDEPENDENT_READBACK_PASS、DBハッシュ一致。 / 新規REA正式VERIFIED=0、正式TODO/VERIFY/BLOCKEDの書込差分0/0/0、Golden実ゲームPASS=0、strict MATCHと完全複製率未測定。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0.

### REA-LOCAL-20261026-20H-P0-DMUSIC-LOADER-OUTPARAM-UNINIT-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_20H_P0_DMUSIC_LOADER_OUTPARAM_SDK_CONTRACT_STATIC.md`; actual SHA256 `31AE9FB27CD09537C3EBC8745B4F82C50A1762D19F4DDB85B710BA97C045CC7E` (4427 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_20H_P0_DMUSIC_LOADER_OUTPUT_EVIDENCE.json` SHA256 `1AF53870355C39264DF0C538C0E8DA401B63DAC5A7479E4702FF84717D5D26A4`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 今回新規：0x004BD9A0の構築処理と0x004BE480のCoCreate呼出前の「Loader出力変数+0x6Cの直接初期化なし」を独立ASMで確認し、Microsoftの公式[out]失敗契約と照合。表面上の未初期化を直ちに実害と認定しないという訂正。
  - 0x004BD369: CALL 0x005B6C2B（0xA8-byteの管理オブジェクトを確保）。
  - 0x004BD381: CALL 0x004BD9A0（コンストラクタ）。そのコンストラクタに[ESI+0x6C]への直接ストアは見つからない。
  - 0x004BD3DC: MOV ESI,[EAX]、0x004BD3E4: CALL 0x004BE480。コンストラクタ→初期化への接続。
  - 0x004BE480内：+0x70の配列ポインタ格納は0x004BE4EB。Loader出力[ESI+0x6C]への直接ストアなし。
  - 0x004BE563: LEA EAX,[ESI+0x6C]、0x004BE566 PUSH EAX、0x004BE582: CALL [0x609310]（既報のCoCreateInstance IAT）。
  - 0x004BE588 TEST EAX,EAX → 0x004BE58A JS 0x004BE5E8（HRESULT失敗時の共有出口）。
  - 0x004BE79D MOV EAX,[ESI+0x6C] → 0x004BE7A0 TEST EAX,EAX → 0x004BE7A2 JE 0x004BE7B3（NULLならReleaseを飛ばす）。
  - 0x004BE7A6 MOV EDX,[ECX+8]、0x004BE7AA CALL EDX（非NULL時のIUnknown::Release）。
  - 0x00555E60 CALL 0x004BE6B0 → 0x00555E71 CALL 0x004BE600 → 0x00555E77 CALL 0x005B6BBB。既報の終了順を再確認。
  - 0x004BF685のGetDefaultAudioPathは別APIであり、今回のCoCreateInstance契約を流用せず、HRESULT/出力/Release契約を独立検証する。
  - P0：0x004BE480で+0x70配列を確保した後、CoCreateInstanceが失敗した場合、0x004BE6B0/0x004BE600以外の解放経路が存在するかを限定XREFで検証。
  - P1：0x004BF685 GetDefaultAudioPathの[out]取得失敗と0x004BF697 SetVolumeの実行条件、参照数の契約を別試験系で設計。
- **Correction/remaining VERIFY:** ## 継続P0 VERIFY / 新規正式REA VERIFIED=0、旧Wave1～5=64/64（2026-10-11同期記録、再加算しない）、正式TODO/VERIFY/BLOCKED書込差分=0/0/0。 / CPUは不明、空きRAMは開始時14,506,212 KiB、独立監査単体約0.85秒、研究全体の所要時間は不明。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0.

### REA-LOCAL-20261026-21H-P0-DMUSIC-ARRAY-COUNT-TEARDOWN-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_21H_P0_DMUSIC_ARRAY_COUNT_TEARDOWN_STATIC.md`; actual SHA256 `2385C6C60F142A5DE82632858C76C1BC137F9DBEB8C788384A7198DC45D8AC1C` (7110 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_21H_P0_DMUSIC_ARRAY_COUNT_TEARDOWN_EVIDENCE.json` SHA256 `2D85359DC666CED0EEC1D85D12799FE0FD7DC559DAE5305147E015404C7FF231`.
- **Old owner's bounded static control-flow / ABI findings:**
  - init `0x004BE480`: `0x004BE4E0 CALL 0x005B5C0B`で配列を確保、`0x004BE4E5 MOV ECX,[0x65BED8]`、`0x004BE4EB MOV [ESI+0x70],EAX`、`0x004BE4F7 MOV EDX,[ESI+0x70]`。取得した個数の範囲でスロットを0初期化する。
  - teardown `0x004BE6B0`: `0x004BE7B3 XOR EDI,EDI`、`0x004BE7B5 CMP [0x65BED8],EDI`、`0x004BE7BB JLE 0x4BE7FA`（0以下なら全ループスキップ）。
  - `0x004BE7C0 MOV EAX,[ESI+0x70]`、`0x004BE7C3 CMP [EAX+EDI*4],0`、非NULL要素に対し`0x004BE7D7 CALL EDX`（vtable+0x98、既報CloseDown同定）、`0x004BE7E5 CALL EDX`（vtable+8、Release）、`0x004BE7EA MOV [EAX+EDI*4],0`（**配列要素**を0にする）。
  - `0x004BE7F1 INC EDI`、`0x004BE7F2 CMP EDI,[0x65BED8]`、`0x004BE7F8 JL 0x4BE7C0`。shutdownは**ループ終了判定でもグローバル値を再読み**する。
  - 親`0x00555CD0`：`0x00555E60 CALL 0x004BE6B0` → `0x00555E71 CALL 0x004BE600` → `0x00555E77 CALL 0x005B6BBB`。最後はオブジェクト本体を渡している。
  - ## 今回の7関数限定の所有権対照
  - | 0x004BD9A0 constructor | なし | 対象外 |
  - | 0x004BE480 initializer | +0x70へ確保ポインタを保存、後に読出し | +0x70をfreeしない |
  - | 0x004BE6B0 shutdown | +0x70を3回読出し、配列要素を0化 | 0x004BE6F0は+0xA0由来のEDIをfree |
  - | 0x004BE600 destructor | +0x70参照なし | 0x004BE651は内部木領域、0x004BE667/0x004BE686は文字列領域 |
  - | 0x004BF2B0 stop/reset helper | +0x70直接参照なし | 間接COM操作あり、+0x70 free未同定 |
  - | 0x00502160 nested-object cleanup | +0x70直接参照なし | オブジェクト内部のCOM release、+0x70 free未同定 |
  - | 0x00555CD0 outer owner | +0x70直接参照なし | 0x00555E77は親オブジェクト本体をfree |
  - ## 新しい条件付き VERIFY：allocation count と teardown count が分離
  - teardown<=0：`0x004BE7BB`で配列走査を実行しない。すべての参照が未解放になり得る。
  - 次P0：`0x00558000`のDAT_0065BED8書込みが初期化後にも呼ばれ得るかをcallers→時系列で検証。続いて`0x004BE480`を複数回呼ぶ経路、他のaliasが+0x70を解放するかを、関数限定で裏付ける。
- **Correction/remaining VERIFY:** **重要な制限**：DAT_0065BED8を実行中に変更できること・同一オブジェクト生存中の再設定経路は**未証明**。デバッグ設定の読込が初期化前に一度だけであれば、この差異は通常プレイでは発火しない。元ゲームのクラッシュ・リークの確定診断ではない。 / - 正式TODO/VERIFY/BLOCKEDの**書込差分**=0/0/0。新規の独立VERIFY候補は正式キューにはまだ追加しない。 / PC SAITO online、21:51 JST時点active.lockなし、Java/Ghidra稼働検出なし、空き物理RAM約14,484MiB、CPU使用率28%（PC全体の単発値、今回の処理専用値ではない）。独立監査単体は約1.19秒、研究全体の厳密な所要時間不明。ゲーム実行、REA再実行、Ghidra起動はいずれも0回。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-22H-P0-DMUSIC-COUNT-RAND-STARTUP-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_22H_P0_DMUSIC_COUNT_RAND_STARTUP_STATIC.md`; actual SHA256 `6F8E86CA2ECC7F43C0DC6748E5075C177A6DAAF1364A449D755FD033FB65371A` (6311 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_22H_P0_DMUSIC_COUNT_RAND_STARTUP_EVIDENCE.json` SHA256 `7A8DC38B1A4F71F9186F3B5355826794AB63EE6CFEE2A3928FCA4665429F7BDA`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 13HでグローバルDAT_0065BED8への書込み3箇所（0x5584B7、0x558506、0x558521）、21Hで初期化と終了時の個数別読込みを確認済み。本報告で二重計上しない。
  - *新規成果**：個数変数の別のreader 0x004BE820:0x004BEEFAを追跡し、名前解決不一致時のDirectMusicPerformance配列ランダム選択に個数が使われる実命令経路を確定。さらに起動関数0x005554F0の全1206バイトを独立復号し、設定呼出しと初期化呼出しの局所的な反復可能性を限定検証。
  - ## ランダム選択の新しいネイティブ証拠（0x004BE820）
  - 0x004BEEE3 CMP ECX,[EBP+0x80] → 0x004BEEE9 JE 0x004BEEFA。検索結果が終端/不一致を表す条件の候補であり、そのときランダム選択側へ入る。通常の名前一致側は0x004BEEEBで[ECX+0x28]のポインタを使用。
  - 0x004BEEFA MOV ECX,[0x65BED8] → 0x004BEF00 MOV [ESP+0x24],ECX（個数をローカルへ）。
  - 0x004BEF04 CALL 0x005B6EAB（CRT rand）、0x004BEF0D FILD [ESP+0x14]、0x004BEF11 FMUL qword [0x63B080]、0x004BEF17 FIMUL [ESP+0x24]。
  - 定数qword 0x63B080は実バイト 000000000000003f、doubleで **1/32768 = 0.000030517578125**。
  - 0x004BEF1B CALL 0x005D1B80（x87浮動小数→整数変換）、0x004BEF20 MOV EDX,[EBP+0x70]、0x004BEF27 MOV EAX,[EDX+EAX*4]（選ばれたCOM配列スロットを実際に参照）。
  - 対象処理0x004BE820の直接callerは0x004BDE40:0x004BE178（旧検索DB・統合V9双方一致）。実際の音声再生・クラッシュは未実測。
  - 正常なSSE変換経路（0x005D1B95 CVTTSD2SI）の選択値は **trunc(rand() / 32768 * count)** と整合。SSE未使用時のx87丸め補助は別途厳密に確認する。
  - ## 静的境界・影響（実機Golden NOT RUN）
  - 14H既報ではcount=0のoperator new(0)相当はmalloc内部で1バイト確保、配列要素初期化ループは省略。今回の0x4BEF27は少なくとも4バイトのスロット読出しなので、**count=0かつランダム選択到達時に未初期化/論理境界外読出し候補**となる。
  - DAT_0065BED8のGhidra登録済みデータ参照は11件（3 WRITE／8 READ）。3 WRITEは全て0x00558000内。記録済みの関数外writerは0。
  - 0x00558000への直接CALLは0x005554F0:0x005558ABの1箇所（旧検索DB/V9一致）。0x005554F0の既知直接callerはCRT起動関数0x005B84D7:0x005B85ECの1箇所。
  - 0x005554F0には0x005558ABの後、0x00555918 CALL 0x00555CD0（音楽側初期化を含む上位処理）が続く。0x00555916 JE 0x0055591Fのため初期化は条件付き。
  - 0x005554F0の1206バイト全体で**関数内へ戻る直接後方分岐は0件**。したがって、通常の1回の起動関数呼出し内で設定読込みを繰り返す根拠は見つからない。
  - 次P0は0x004BE820の0x004BEEE3分岐に到達する名前解決/初期化条件、および0x005D1B80のx87非SSE変換経路を限定静的追跡。併行して+0x70所有配列の別名freeと初期化失敗時の配列未解放を継続VERIFY。
- **Correction/remaining VERIFY:** Python/Capstoneで起動関数、debug設定関数、音楽選択関数、整数変換の4関数を対象限定ASM確認。原作・旧DB・V9 SHA256、双方quick_check、直接CALL所有元、個数3writer、1/32768実バイト、先行21H証拠、64件旧同期記録を照合して**50/50 PASS**（監査条件であり関数数ではない）。独立監査実行時間約2.40秒、証拠保存実行約3.38秒。研究全体時間・CPU負荷は不明。 / REA5種: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY。新規5方法完備0、新規正式VERIFIED0、旧Wave1～5の64/64は2026-10-11旧同期ログからの過去成果（非重複）。正式TODO/VERIFY/BLOCKED書込差分=0/0/0。原作Golden PASS=0、strict MATCH/完全複製率=未測定。 / 次P0は0x004BE820の0x004BEEE3分岐に到達する名前解決/初期化条件、および0x005D1B80のx87非SSE変換経路を限定静的追跡。併行して+0x70所有配列の別名freeと初期化失敗時の配列未解放を継続VERIFY。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261026-23H-P0-DMUSIC-FTOL-SHAREDTAIL-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261026_23H_P0_FTOL_FALLBACK_STATIC.md`; actual SHA256 `396CED75000C42CB3D74AADA3479E947D733D5BEB1C8F33574F2EB080D07255E` (4572 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261026_23H_P0_FTOL_FALLBACK_EVIDENCE.json` SHA256 `B356B1DBD8C0609CC8BED768BCF88002B63D221F63F34CAE281D6EB00025ABB2`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 新規静的成果（過去22H・2026-10-11の断片との非重複）
  - 旧研究は0x4BEEE3で名前探索結果を判定、0x4BEEFAで個数読み、0x4BEF1BでFTOL、0x4BEF27で配列要素取得と報告。2026-10-11のSOURCE_RECOVERY_MODE6_FTOLには0x5D1BB6以降の**前半**（～0x5D1BDD）まで、下流0x5D1BDF..0x5D1C15は未取得と明記。本回の新しい静的証拠はその下流から最終RETまでの原作ネイティブ命令。
  - 0x004BEEBE CALL 0x004C1200（検索ヘルパー）。0x004BEEE3で戻ったノードと[EBP+0x80]の番兵を比較、0x004BEEE9 JE 0x004BEEFAでランダムfallbackへ。非番兵では0x004BEEEBで[ECX+0x28]を採用し、乱数抽選をskip。
  - 0x004BEF04 CALL 0x005B6EAB、0x004BEF0D/11/17でrand×(1/32768)×count、0x004BEF1B CALL 0x005D1B80、0x004BEF27 MOV EAX,[EDX+EAX*4]。名前解決fallbackに入った後の配列参照で、count=0時の論理範囲外候補は22Hから引継ぎVERIFY。
  - 0x005D1B80はGhidra SQLiteのsize_bytes=28だが、0x005D1B87 **JE 0x005D1BB6**で登録関数範囲外の共有tailへ分岐する。SSE側は0x005D1B95 CVTTSD2SI→0x005D1B9B RET。非SSE側の0x005D1BB6..0x005D1C2Aも呼出しの実処理であり、28バイトのGhidra疑似Cだけを完全な制御フローとして扱えない。
  - x87側は0x005D1BC5 FISTP QWORD、0x005D1BC9 FILD QWORD、0x005D1BD9 FSUBP ST(1)。0x005D1BDF..0x005D1BFBは負数の残差に応じADCで丸め済値を+1、0x005D1BFD..0x005D1C13は非負数の残差に応じSBBで-1。0x005D1C15..0x005D1C29には低DWORDゼロの特別処理・共通復帰、**RETは0x005D1C2A**。
  - DAT_00B14A40の旧Ghidra索引参照はREAD6件・WRITE0件。0x005D1B9Cの読出しは登録された0x5D1B80の28バイト範囲外にある。SSE gateの実ゲーム時の値や未索引のwriterは不明であり「非SSE確定」とはしない。
  - 0x004BE820の呼出元0x004BDE40:0x004BE178と0x004C1200の検索キー構築・番兵条件をさらに絞る。入力が名前不一致となるBGM指定経路とcount=0の到達性、+0x70の別名free候補を優先。次にDAT_00B14A40の初期化条件・未索引の書込みを独立確認。実機Goldenは隔離試験が準備されるまではNOT RUN。
- **Correction/remaining VERIFY:** - DAT_00B14A40の旧Ghidra索引参照はREAD6件・WRITE0件。0x005D1B9Cの読出しは登録された0x5D1B80の28バイト範囲外にある。SSE gateの実ゲーム時の値や未索引のwriterは不明であり「非SSE確定」とはしない。 / 既存Wave1～5 VERIFIED **64/64は2026-10-11同期記録**から継承、今回新規正式VERIFIED0。5種の証拠はinfo/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED更新差分0/0/0、原作Golden実測PASS0、strict MATCH・完全複製率未測定。 / PC接続成功、23:44時点空きRAM約13.01GiB、23:50時点active.lock無し。CPU負荷不明、今回監査単独4.9～5.2秒、全作業時間未測定。新REA/Ghidra/ゲームの起動なし。Workなし。初回read-only Python stdin経由の日本語パスが文字化けしたためPath.cwd()方式で正常復旧（OTHER、SAFETY_REFUSALではない）。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0.

## Curation handoff

All detailed source passages belong to original owner and must be matched by SHA before formal adoption. Differences among CALL E8, indirect virtual dispatch and E9 tail transfer must be preserved. Current V9/PE native call evidence outranks older V3 guesses; cross-hour overlap is not new function identity. No blocked requests, original game binaries, forbidden VA evidence, secrets, or raw generated SQLite were added. Curator alone owns canonical develop REF/dictionaries and tests; the present work makes original findings discoverable without promoting accuracy. Source IDs are non-overlapping with the previous owner-index snapshot.
