# REA early legacy / pre-ID owner archive D

**SOURCE_PRESERVED_UNKEYED or existing-ID ERRATUM, not formally CURATED.** 14 original REA owner reports were inspected read-only for source byte SHA, safe original-x86/ABI/control-flow statements and correction/status markers. No new Ghidra/REA/game tests, no newly formal five-method VERIFIED or Golden PASS. Current original PE/V9 were not re-hashed. Exact native-source IDs are recorded only when declared in a report header; no synthetic new research IDs. Safety refused Wave6/file/export material is metadata-only and omitted from substantive excerpts. Original reports and evidence stay on authorized PC.

### REA_T014_TOKEN_CALLER_FORMAT_MATRIX_20261012_0842.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_TOKEN_CALLER_FORMAT_MATRIX_20261012_0842.md`; actual SHA256 `29E38601695657D84F07BBE50B4EC0E8B308A4AA14AF12ED46F0E74A57698DF4`, 5203 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - # REA T014 — 0x4705F0 caller format matrix / 2026-10-12 08:42 JST
  - `0x428010` (T014, global.sav): saved pseudo `ev_7d8bf27f8f623acdc9c301d57fa247cf6372db3a769910b9ed7ad2099114e881`, ASM `ev_8f357dc6b9e49591c6a5cec5ac76b4bd2c9019e4bc9cd61f15e5b3ba1bd55118`.
  - At `0x4280A4..0x4280C2`, literal `"----------"` (10 chars) is installed as the global sentinel string. At `0x42839B..0x428412`, an input token from `0x4705F0` is compared against it with `0x402C40` **and a separate length check**; exact match branches to `0x4284C4` without consuming an entry payload.
  - Non-sentinel path `0x42843B..0x428494`: second string token read with `0x4705F0`, then numeric field with `0x470700`, then `0x4A69B0` insert wrapper. The resulting temporary tree feeds `0x4C1200`; found value is assigned to global `0xB06D78` at `0x42850F`. Exact lookup semantics and duplicate-key behavior remain VERIFY.
  - The function probes `global.sav` via FindFirstFileA, opens for reading, reads bytes, invokes decode `0x4270F0`, creates an input stream via `0x429C60`; failure/short read and extra data after sentinel are NOT established as permissible.
  - `0x45E1E0` (T014, normal save root): saved pseudo `ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e`, ASM `ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124`.
  - Four successive root groups use the shared marker string at `0x65CD28` (length field `0x65CD38`) with content and length equality: first string+int payload, second `0x58E870` Unit reader, third `0x598980` Spot reader, fourth `0x5964C0` Power reader. After these groups the function calls `0x471AF0` diplomacy and `0x435550` graph readers.
  - `0x58E870` (T014, Unit save state): saved pseudo `ev_992508cdab86c44fc73e0f72aa80b7ab30679a2b84144a444f5afe7a7d80760d`, ASM `ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839`.
  - Four repeated variable-field loops break on a zero-length token, then a subsequent map loop handles **empty token separately** from equality with the Unit-specific marker string at `0x68B9D0` (length field `0x68B9E0`), which calls `0x58E480` before fixed tail. This is not the same group delimiter as normal-save's `0x65CD38` nor the 10-hyphen global.sav sentinel.
  - Previously classified: `0x598980` Spot, `0x5964C0` Power, `0x435550` graph, `0x471AF0` diplomacy (see `REA_T014_CALLERS_GLOBAL_SCRATCH_SCOPE_20261012_0738.md`).
  - Remaining 6 resolved callers **not** independently assigned: `0x428710`, `0x45EAC0`, `0x470550`, `0x58E480`, `0x5A90E0`, `0x5B0400`. Indirect calls are outside the 13 resolved set.
  - `0x4705F0` byte limit 255 and signed allowed `0x20..0x7F` are **token-local**. Do not collapse global.sav, normal save root, Unit fields into one generic terminator or infer all saved game text uses this reader.
  - Open tasks: six caller uses, byte values of the normal-save marker at `0x65CD28` and Unit marker at `0x68B9D0`, `0x58E480` body, malformed/EOF/trailing bytes and duplicate key handling. This is static-only; no gameplay compatibility PASS.
- **Limitations and errata:**   - Non-sentinel path `0x42843B..0x428494`: second string token read with `0x4705F0`, then numeric field with `0x470700`, then `0x4A69B0` insert wrapper. The resulting temporary tree feeds `0x4C1200`; found value is assigned to global `0xB06D78` at `0x42850F`. Exact lookup semantics and duplicate-key behavior remain VERIFY. / ## Reimplementation / VERIFY
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_UNIT_MARKER_DISPATCH_20261012_1437.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_UNIT_MARKER_DISPATCH_20261012_1437.md`; actual SHA256 `9EFB8F1312CD7CDF02DB53360DF5347BDAF1A22AED72776B61B0E0996A776111`, 16040 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - Task T014。親0x58E870はruns/20261009T223622536Z/RUN_RESULT.jsonで5手法VERIFIED。assembly ID ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839 / pseudo ID ev_992508cdab86c44fc73e0f72aa80b7ab30679a2b84144a444f5afe7a7d80760d。
  - token reader 0x4705F0 callers ID ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87 は0x58E870と0x58E480を両方resolved callerとして列挙。ただし0x58E480本体の5種は保存されていない。
  - ## 分岐検証（保存済み0x58E870 assembly）
  - 1. 0x58ED10 CALL 0x4705F0後、0x58ED1C TEST EDI,EDI、0x58ED1E JZ 0x58EE36。空tokenは反復を終え、0x58EE56→0x58EE8Bで固定末尾readerに進む。この経路は0x58E480を呼ばない。
  - 2. 非空tokenはUnit固有marker 0x68B9D0（文字列length 0x68B9E0 / SSO capacity 0x68B9E4）に対して0x58ED55 CALL 0x402C40＋長さ比較。0x58ED75 JNZ 0x58EE58の一致枝で0x58EE5F CALL 0x58E480を経由し、0x58EE8Bの共通固定末尾へ。marker一致は単なる終了ではなく追加sub-readerを起動する。
  - 3. 非空・marker不一致は0x58ED7B..0x58ED8Aで0x42E700へ4byte取得を依頼。stream状態検査が正常なら0x436560→0x436680→0x463280を経てUnit側+0x12C treeへkey/value record挿入を試み、0x58EE1E/0x58EE31から0x58ECEBへ戻る。異常フラグでは0x58EDA4 JNZ 0x58EFA2へ。
  - どちらの終端経路も0x58EE8B以後、0x58EEA5の文字列token・0x58EEB6の数値reader等で固定フィールドを復元するが、0x58E480の実副作用はmarker一致側のみ。
  - ## 0x470550 cross-callsite（追加観察）
  - A所有read-only native: exe/T014_LOAD_CORE_DUMP.txtの0x45E2D8、exe/T014_NORMAL_LOAD_PROBE.txtの0x45ECBB、exe/T014_NORMAL_SAVE_CORE.txtの0x4CFC2Aに0x470550直接CALLがある。
  - 通常saveの2処理系と別consumerで同じ0x470550を使い、Ghidra 0x4705F0 callersにも現れる。特定mode専用readerと命名しない。callsiteにはstack上の3pointer＋register準備が見えるが、引数/出力型と関数本体はVERIFY。
  - 0x58E480内部のnested block読取量・副作用・例外、0x68B9D0 markerのraw bytes、重複keyでの保存値、EOFと空tokenの相違、通常経路到達条件は未確定。
  - 通常save root marker 0x65CD28、Unit marker 0x68B9D0、global.savの10ハイフンは別の保存場所。raw byteの同一性は証明されておらず一律marker処理にまとめない。
  - ## 2026-10-13 01時台 — 0x58E480追加tag readerの保存済み疑似C接続（REA-T014-58E480-PSEUDO-20261013）
  - [SOURCE] `dev_lab/recovered_source/peer_script01_ghidra_named_decomp_20261011.zip` SHA256=`C167DC8B09E8CAE6ABAA14E23BAC94E675585AE432595A1608FDBC1CC8249B9A`（今回再照合一致）、保存member `peer_script01_ghidra_named_decomp_20261011/decomp_0058xxxx.c` の `/* ==== 0x0058E480 FUN_0058e480 ==== */` から次関数までの疑似C単独4759文字。**member単独SHA・native assembly・callers/callees 5方法は今回未収録**。正式ソース形式/全関数境界はVERIFY、Ghidra pseudoは関数ABI・hidden register callを誤復元し得る。
  - [PARENT-ABI / SAVED VERIFIED] 保存run `runs/20261009T223622536Z/58E870_procedure_assembly.json`、assembly ID=`ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839`。Unit+0x130 treeのmarker一致後 `0x58EE58 MOV ECX,[ESP+14]`（Unit ptr）→`0x58EE5C PUSH ECX`→`0x58EE5D MOV ECX,EBX`（読込stream context）→`0x58EE5F CALL 0x58E480`→正常帰還`0x58EE64 ADD ESP,4`→固定末尾`0x58EE8B`（Unit+0x13C等）へ。疑似C側の引数`param_1`=Unit pointer、隠れた`in_ECX`=streamと整合するが異常終了副作用はVERIFY。元caller帰還なしに固定末尾を読まない。
  - [TAG A / 6BYTES] 最初の既知6byte名比較が真なら`0x42E700`で4byte値を読み、stream異常フラグならLoadExceptionへ。正常ならグローバルscratch`B060F0`から`Unit+0x7C`へDWORD store。この分岐は保存writerの `arbeit`（6字）と対象field順に整合するが、比較引数がpseudo上省略されているため**名前の厳密対応はwriterとの高確度crosswalk**でありnative literal照合はVERIFY。次token読込はouter loop復帰後。
  - [TAG B / 11BYTES] 次の比較枝は完全な11byteの名前に一致すると`0x4705F0(Unit+0xA0)`を1回呼ぶ。writerの`arbeit_user`（11字）と整合。値の長さ制約/CP932/writerとのbyte互換はtoken helper契約を継承し新規確定しない。
  - [TAG C / 10BYTES] 次の比較枝は10byte名（writerの`item_skill`と整合）。まずUnitのvector `[+0x11C,+0x120)` が非空なら`0x417160`→`0x415A60`→`Unit+0x120`へ更新が先行。次に`0x4705F0`でtokenを反復し、**長さ0のtoken**で終了、非空tokenは`0x415530`に渡す。SSO容量>0xFの場合の一時文字列解放が各反復にある。既存vectorの全要素の破棄意味や新規append型・allocator副作用は各callee未解析のためVERIFY（単なるclear+list上書きと断定しない）。
- **Limitations and errata:** - [VERIFIED / VERIFY] `0x603BB0`の命令bytes、文字列リテラルbytes、`.data`初期値、既存0x470830 assemblyによるゼロ文字列書込は局所STATIC。実初期化到達、`0x402800`の全副作用、追加文字列変更有無、write失敗・reader例外、旧実機save上の消費・互換はVERIFY。5手法が未取得の`0x58E480`は`VERIFY-PARTIAL-SAVED-PSEUDO`維持。既存実saveのbyte完全再構築報告は別所有・旧EXE gameplay Golden0である。 / - [WORK REUSE] save parser設計上、`UNIT_EXTRA_BEGIN/END="@@@@"`（通常初期化を前提）、`item_skill/friend end=empty token`（ランタイムinner object不変を要確認）という**別階層の条件**として追跡できる。検証なしの製品実装・未知tagを無害にskipする仮説は行わない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_UNIT_TAG_NESTED_SENTINELS_20261010_2236.md

- **Source relative path:** `rea_lab/decomp_task/REA_UNIT_TAG_NESTED_SENTINELS_20261010_2236.md`; actual SHA256 `8A9D65550CB791737F4963BB18AA2866C9ED4146C87EC397987CC19E9745A018`, 3053 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - T-ID: T014。writer `0x58EFD0` (saved run `20261009T224617297Z`)、reader `0x58E870` (saved run `20261009T223622536Z`)。
  - 1. `0x58F405 MOV ESI,0x68B9D0` → `0x58F40A CALL 0x470830`：Unit+0x130ツリー直後の外側マーカー候補。
  - 2. `item_skill` (`0x58F4D2` literal pointer)後に`Unit+0x11C..0x120`のvectorをstride `0x1C`で走査し、`0x58F54E CALL 0x470830`で各要素を出力。
  - 3. `0x58F53C JZ 0x58F57E`：vectorが空でも`0x58F57E MOV ESI,0x68B3A8` → `0x58F583 CALL 0x470830`を実行。
  - 4. `friend` (`0x58F58C` literal pointer)後に`Unit+0x15C` treeを走査し、`0x58F5E6 CALL 0x470830`でノードkey候補を出力。
  - 5. `0x58F5E1 JZ 0x58F63A`：friend treeが空でも`0x58F63A MOV ESI,0x68B3A8` → `0x58F63F CALL 0x470830`を実行。
  - 6. `0x58F644 MOV ESI,0x68B9D0` → `0x58F649 CALL 0x470830`：追加tag領域後の外側マーカー候補。直後`0x58F64E`でUnit+0x13C固定フィールド出力へ。
  - **追加発見**: 内側で同じ`0x68B3A8`参照をitem_skill終端相当・friend終端相当の2か所に渡し、外側では`0x68B9D0`参照を前後2か所に渡す。両コンテナが空の場合でもそれぞれの内側出力呼出が残る。
  - **未確定**: オブジェクト参照の実際のバイト列、各終端の文字列一致/空値、`0x58E480`内部の読込規則と失敗時処理。pointer値をバイト列や実機互換PASSとみなさない。
  - reader `0x58E870`では外側マーカー相当の一致経路で`0x58E480`を呼ぶが、このcallee自体は5種証拠未取得（VERIFY）。
- **Limitations and errata:** - 状態: CONFIRMED-SAVED-ASSEMBLY（CALL siteと直接分岐のみ）。旧EXE実機=NOT RUN、helper意味=VERIFY。新規REA/Ghidra実行0。 / - reader `0x58E870`では外側マーカー相当の一致経路で`0x58E480`を呼ぶが、このcallee自体は5種証拠未取得（VERIFY）。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_UNIT_TAGGED_TAIL_ROUTING_AUDIT_20261010_2135.md

- **Source relative path:** `rea_lab/decomp_task/REA_UNIT_TAGGED_TAIL_ROUTING_AUDIT_20261010_2135.md`; actual SHA256 `CD6CC334C3AD9DAC20E52620CF9C1668AAB89157F29504276DD5EE6E142B6472`, 2900 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 対象: T014、Unit reader VA 0x58E870 / writer VA 0x58EFD0。未取得helper VA 0x58E480 はVERIFIEDに昇格しない。
  - writer 0x58F333..0x58F3FF: Unit+0x130ツリーのkey＋DWORDを走査・出力。0x58F405 MOV ESI,0x68B9D0 → 0x58F40A CALL 0x470830で終端文字列を出力する。
  - writer 0x58F63Aは別終端候補0x68B3A8を書き、0x58F644 MOV ESI,0x68B9D0 → 0x58F649 CALL 0x470830で同じ参照先の終端文字列を**再度**出力し、0x58F64EでUnit+0x13C string以降の固定tailへ進む。
  - reader 0x58ED10はUnit+0x130のkey文字列を読む。空文字なら0x58EE8B以降の固定tailへ進み、marker一致なら0x58EE5F CALL 0x58E480を実行してから同じ固定tailへ進む。
  - readerの保存済み本体にUnit+0x7C/+0xA0/+0x11C/+0x15Cを直接読む命令は見つからない。writerの中間tagを実消費する関数候補は、marker一致でのみ到達する0x58E480である（**推定**）。
  - 0x58E480の具体的なtag認識順、任意tagの扱い、追加フィールドの値更新、後半marker消費位置は未解明（VERIFY）。この関数の5種Ghidra証拠・実ゲーム動作は未取得。
- **Limitations and errata:** - 区分: STATIC CROSSCHECK / REIMPLEMENT VERIFY。新規REA/Ghidra解析なし、元EXE実行なし。REA独立所有領域のみ。 / - 0x58E480の具体的なtag認識順、任意tagの扱い、追加フィールドの値更新、後半marker消費位置は未解明（VERIFY）。この関数の5種Ghidra証拠・実ゲーム動作は未取得。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_UNIT_TREE_BOUNDARY_AUDIT_20261010_1834.md

- **Source relative path:** `rea_lab/decomp_task/REA_UNIT_TREE_BOUNDARY_AUDIT_20261010_1834.md`; actual SHA256 `283A583326B2031F462A82102E52853933076E822A761454F17F43D779F6EB24`, 3502 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - T014 / Unit reader `0x58E870`、writer `0x58EFD0`、共通文字列writer `0x470830` を比較。これらの5種証拠は既存VERIFIEDで、新規昇格なし。
  - `0x58ED10..1E`: 文字列read直後に長さを検査。長さ0では`0x58EE36`を経て`0x58EE8B`の次fieldへ進む。marker終端処理`0x58E480`はこの経路では**呼ばれない**。
  - 長さ非0なら`0x58ED24..75`でグローバル文字列 `0x68B9D0` と比較。完全一致時だけ`0x58EE58..5F`で`0x58E480`を呼び、次fieldへ進む。
  - 非空かつmarker不一致では`0x58ED7B..85`でDWORD系のstream reader `0x42E700`を呼び、`0x58ED93..A4`でstream state bitsを判定。
  - stream stateが問題を示す枝は`0x58EFA2`へ分岐し、`0x58EFAB..BD`の異常処理（疑似コード上はLoadException throw）へ進む。成功枝は`0x58EDAA..E8`でkey/valueの挿入処理を行いtree読込loopを継続。
  - writer `0x58F343..38C`はtree node由来key文字列＋DWORD、`0x58F405..40A`は固有marker `0x68B9D0` を保存する。vectorの空文字終端(`0x68B3A8`)とこのtree markerを単一種類として扱わない。
  - STATIC CONFIRMED: 上記CALL/branchの順序。`0x58E480`の作用、`0x42E700`のexact I/O、throwの上位回復、実ゲームで空key/不正byteが到達可能かはVERIFY。
- **Limitations and errata:** - 共通writerは不適格byte混入時にその文字列全体を空として書く。tree keyが空へ変換された場合のreader分岐差は静的に成立するが、原作ファイル破損や正規ゲームバグは**未観測・断定禁止**。 / - 進捗: Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、累計39/48・今回新規VERIFIED0・P0 20/21・P1 19/27・TODO8・VERIFY1。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_UNIT_TREE_CLEAR_ORDER_AUDIT_20261010_1931.md

- **Source relative path:** `rea_lab/decomp_task/REA_UNIT_TREE_CLEAR_ORDER_AUDIT_20261010_1931.md`; actual SHA256 `9224831E83D42EF81643B553AD5CF42A1B19CF84179696C82D16280CA4FD146E`, 2912 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 対象 T014：reader `0x58E870` (1861 bytes, five-method existing VERIFIED)、writer `0x58EFD0` (existing VERIFIED)、新規調査対象helper `0x58E480` は未取得でVERIFY。
  - reader `0x58ECB2..0x58ECC2`: Unit+0x130のtree先頭からnodeを取得し、`0x463070`を呼んで既存node群を処理する。
  - `0x58ECC7..0x58ECE1`: tree sentinelのprev/next/parent相当の3ポインタをsentinel自身へ戻し、Unit+0x134 countを0にする。**これは先頭keyの`0x4705F0`読込（`0x58ED10`）より前。**
  - writer `0x58F333..0x58F405`: nodeが0件でもtree走査をskipした後に専用marker `0x68B9D0` を`0x470830`へ渡す。marker文字列は要素件数によらず出力される。marker値の具体的bytesと文字列writerによる例外的変換の可能性は未検証。
  - reader `0x58ED1C`は空文字ならnext fieldへ、marker一致なら`0x58EE5F`で`0x58E480`後にnext fieldへ、通常keyなら`0x42E700`で4byteを消費・stream error判定後insert。`0x58E480`の内部副作用や、reader異常終了時のrollbackは未同定。
  - 新規5方法の取得は0件。既存関数VERIFIEDの追加監査1件であり、helper `0x58E480`をVERIFIEDに昇格しない。新設fixtureは「既存tree非空→空文字終了」「既存tree非空→専用marker終了」「通常entry→途中I/O異常」の順序・残存state比較をDESIGNED/NOT RUNとする。
- **Limitations and errata:** ## 誤認防止・次回 / - Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12 =39/48、今回増0、P0=20/21、P1=19/27、TODO8/VERIFY1。研究DONE9/34 (MASTER cp70)、旧EXE実機golden PASS0、ゲーム再実装率未測定。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_UNIT_TREE_DUPLICATE_KEY_AUDIT_20261010_2035.md

- **Source relative path:** `rea_lab/decomp_task/REA_UNIT_TREE_DUPLICATE_KEY_AUDIT_20261010_2035.md`; actual SHA256 `FB40B2723D61BD533C22F4258ED1CD0F5C803BCD261BCC7C965842EF1E927CE6`, 2290 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 対象: `0x58E870`（T014, Unit save reader）, `0x463280`（T005, RB-tree登録）, `0x58EFD0`（T014, Unit writer）。
  - `0x58E870`はUnit+0x130の既存treeをclearし、キー文字列を読込。空文字なら区間終了、専用markerなら`0x58E480`へ進む。
  - 通常キーでは追加のstream値を読み、`0x436680`系のnode構築を経て`0x463280`へ渡す。stream異常時は`LoadException`経路がある。
  - `0x463280`はRB-tree比較で既存キー候補を探索し、同一扱いのノードでは新規挿入せず既存ポインタ・挿入フラグ0を返す分岐を持つ。
  - 次回はキー比較器（`0x402C40`, `0x405370`）とresult flagのconsumerを既存保存native証拠で照合する。
- **Limitations and errata:** - 状態: **STATIC HYPOTHESIS / VERIFY**。この資料の保存は新規Ghidra関数取得・新たなgolden PASSを意味しない。 / - 同一Unit区間に`keyA=100`の後で`keyA=200`を読ませた場合、最初の値が残る**先勝ち候補**。ただし比較器の厳密な等価条件と後続callee副作用は未検証。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_WAVE4_CODEC_CLOCK_NATIVE_20261011.md

- **Source relative path:** `rea_lab/decomp_task/REA_WAVE4_CODEC_CLOCK_NATIVE_20261011.md`; actual SHA256 `DD526F87AF3169B097E58EB887EDEB4CAB105BF3219B49184D2D5218B0E3F44C`, 2363 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - ## T014: 0x427040 encrypt / 0x4270F0 decrypt
  - Encrypt `0x427040`（174 bytes）：info `ev_04f97081148c5b70a34c1f70d55ef4100240002c8aade454c183f1c6c1f267be`、pseudo `ev_cc5bde730579a34289233a8406ed8b02996d9ffebd7ec12b375398fd353359f3`。
  - `*dest=0x04030201`のlittle-endian先頭4byte、続けて28byteの鍵を生成。28回の直接CRT rand `0x5B6EAB`消費経路がある。各鍵byteはGhidraの `round(rand * (1/32768) *112)+8` 形だが、真のx87丸め契約はVERIFY。
  - Decrypt `0x4270F0`（148 bytes）：info `ev_635c2e10a0dc0c5959db8b9dbe207d6add73016686659c7d69d1ebc6ebf6d861`、pseudo `ev_39248efde5737b8ffb423ef2219bf7f22a8407ba4d2fba240047fa9dc22d9e8e`。
  - ## T010: 0x565700 battle timing gate
  - `0x565700`（35 bytes）info `ev_38f76e7e1e556dbcfffe3e8830f53a66c5080b395e7673add73eb5a6e73ceeac`、pseudo `ev_4236ba2cb5bd0403d1f1c52ce271be5a980a0170aaca244cd2a26067d727ed38`、assembly `ev_199f778915fba3f40b5f0f5c530cd39c09ae578cfceb26396b480efca1a1a6fa`。
  - グローバル `0x67B938==0x80000008` の場合 `0x67B93C`を1増やしてreturn。そうでなく `0x67B93C>0`の場合は1減算、0以下は維持。
- **Limitations and errata:** - 不正サイズ(0..31)、Magic不一致時の上位エラー伝播/stream長、rand/x87丸め、in-place overlapを含む完全実行結果はVERIFY。 / - sentinelの人間向け意味・実戦フレーム頻度・callback側の補足処理はVERIFY。既存T010とは別の新規STATIC監査資料として記録。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_WAVE4_SCENE_FRAME_BRANCH_REVIEW_20261011_2135.md

- **Source relative path:** `rea_lab/decomp_task/REA_WAVE4_SCENE_FRAME_BRANCH_REVIEW_20261011_2135.md`; actual SHA256 `12FCD855D1496133CC8B2408A70CCBC524F7BFB37E9AC9E96716A377E195CDDA`, 3347 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - # REA独立静的監査: 0x432EE0 scenario/event frame install（2026-10-11 21時台 JST）
  - source/end SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。run=20261011T114202395Z、VA=0x432EE0、関数長1663byte。5方法VERIFIEDは既存runに由来。
  - 0x432F39は0x4647D0で`scenario` propertyを参照、0x432FB5は0x465060で`event`を参照。0x433017..0x43306Fは入力文字列とstatic `politics`値を比較し、一致時だけScriptFunc関連のlazy初期化/0x4C1290側へ進む（0x433071..0x4330E2）。この文字列比較のみで全phaseの政治ターン順序は証明しない。
  - 0x433121は第3引数を0判定し、非0だけ0x433141で0x46E250を呼ぶ。0x43312E..0x433140は**第3引数==2**を1、それ以外を0として別引数に変換。結果が空でなければ0x433168..0x4331FDにて選択結果を局所vectorに順次追加する。第3引数0はこの候補収集をskip。
  - 0x433207は第2引数(byte)を0比較。**0でないとき**0x433215以降へ進み、+0x1EED7C, +0x1EED8C, +0x1EED9C, +0x1EEDACに対応するframe-vector末尾を個別に延長する（後続vectorへの0値投入やreserve分岐あり）。
  - **第2引数0のとき**0x433423へ分岐し、+0x1EED7Cへvector追加、0x4334A0で0x4365F0、+0x1EED9Cへ追加、0x433507で0x436080へ進む。4本のframeを常時同じ形でpushする実装にはしない。
  - 0x432EE0自身のGhidra解決済みcallerは0x4342A0,0x434CC0,0x434EB0,0x471E80,0x48C880,0x4922A0,0x493630,0x4D79C0,0x51F3B0。各callerが実際に渡す第2/第3引数の意味はまだVERIFY。
  - 確定できるのは直接CALL、引数分岐、局所frame追加というSTATIC契約。関数名「world/fight/politics phase dispatcher」はキューの仮称であり、この1関数が全phaseを直接dispatchすることは未証明。0x46E250のfilter、0x4365F0/0x436080副作用、nested event/routine stack整列、参照先生存期間、正常gameplay traceはVERIFY。
- **Limitations and errata:** - 0x432EE0自身のGhidra解決済みcallerは0x4342A0,0x434CC0,0x434EB0,0x471E80,0x48C880,0x4922A0,0x493630,0x4D79C0,0x51F3B0。各callerが実際に渡す第2/第3引数の意味はまだVERIFY。 / 確定できるのは直接CALL、引数分岐、局所frame追加というSTATIC契約。関数名「world/fight/politics phase dispatcher」はキューの仮称であり、この1関数が全phaseを直接dispatchすることは未証明。0x46E250のfilter、0x4365F0/0x436080副作用、nested event/routine stack整列、参照先生存期間、正常gameplay traceはVERIFY。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_WAVE5_COMPLETE_WAVE6_CANDIDATES_20261012_0041.md

- **Source relative path:** `rea_lab/decomp_task/REA_WAVE5_COMPLETE_WAVE6_CANDIDATES_20261012_0041.md`; actual SHA256 `7D5040F5E2D96B77C6D041767E706659845CABC19591D4F54AAA0A5436ACB4C4`, 6452 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - No additional native result declared from this safety/metadata-only source.
- **Limitations and errata:** - Wave5: 12/16→16/16、今回+4件、P0=29/29、P1=35/35、未着手0・VERIFY0。全Wave累計64/64（Wave1 16、Wave2 10、Wave3 10、Wave4 12、Wave5 16）。 / - 0x57CFA0: 非空の既存範囲に0x5158A0を適用後、0x57CFD0を呼んで範囲insertする薄いwrapper。引数の実質の始点・終点、候補の意味は呼出側でVERIFY。
- **Status:** BLOCKED_METADATA_ONLY; original Golden PASS 0, READY 0.

### REA_WAVE5_SAVE_IO_VECTOR_AUDIT_20261011_2347.md

- **Source relative path:** `rea_lab/decomp_task/REA_WAVE5_SAVE_IO_VECTOR_AUDIT_20261011_2347.md`; actual SHA256 `0AAA8EFD7CAFC3FB30A78152778BED893A6C26537F5B19DC209ED75CDA86BAE4`, 4323 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - | 0x4705F0 / T014 / 256B | ev_8d6b4c6b269ce0021d9fc898bb87d4fb557a70421b0ed4453ab1d6c4d161784f | ev_3851d07b1e0119564efeb2d7215b9c16ff9a63f274ce843c13ed100dfee38752 | ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d | ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87 | ev_661507e7456c44d65dd153fff0f2c6b8de0e33a9519370d794118fae0def6743 |
  - | 0x470700 / T014 / 99B | ev_e676039e3083db867c85605ee376898d307e4a18d8f264c9c6f5003be1deb31e | ev_fa4f2750e44895495089baaea76f6c2e6b39e1ec155c9b68af4b63bc17ac8e07 | ev_f7ed3af4df1cdf7b14d9208f3d4aa735267b9ab022ee7d6b3860c4521bbb95cf | ev_14939a8b9ce66f7858434d5f57609aca8f4d26a7781078754cfc513c5032989c | ev_3f9a89a60c30eee71f662be8ef197b9016cfe610caae887926287dcb5d131286 |
  - | 0x471D20 / T014 / 144B | ev_d66eb9ca2ede2dddefec4ffa0700384bde6cdbe4d00f9186cf00ff67748de6fc | ev_ab5115883f3f7287b9e69a76b95333a8ddd343252dfc9c1efdafb3f4db81d846 | ev_64adbba14e1cee99ca12f12987032aa749c2890ee33057c941c4d0b3eed1fe6f | ev_a459496a5ab977b94c768d186aefbfc6f58bb2cb97dcc009e0be9b470f192a56 | ev_8f32e24032fa7db1f4ddd3212cbf805c0509f176888721d560966984d495d307 |
  - | 0x5154F0 / T013 / 207B | ev_49cbc451308e458f59684fb8b64adbb92e6d0bcdd5abb08e63f08fcf044184d2 | ev_8c2e00fbbaaca29b29284ec0899df000751530685da489a4b210c6bffdad8b4d | ev_6a53e867e218f8905561e0687a0340e1dafe224e61cc7d465b0047e7b21c3d64 | ev_8ce283bf9f936114ed4749b1907814810be35fb077af15de779d65256288d320 | ev_c8e76cb2fcf962a30ce7b57a87aa46569443fdfdf23f9314b8ef66435ce3447a |
  - T014/0x4705F0: 共有0x400B buffer初期化→0x470980から1文字ずつ取得→NUL終端。0x20未満の非NUL制御文字・stream errorでLoadException。ループ境界はi<0xFF。FUN_00402800へ文字列長を渡す。実際の入力エンコーディング/例外再現はVERIFY。
  - T014/0x470700: 0x42E700経由で4バイト相当の値を共有領域へ読み込み、stream errorを確認して出力先へ代入。解釈型・endiannessや既存save全体の互換性はVERIFY。
  - T014/0x471D20: 0x4708A0×2、0x4628F0×2、32bit幅vectorの要素数ぶん0x470830を反復し、最後に同関数を1回追加。tag / sentinelの対応、reader 0x471AF0とのbyte-by-byte対称性はVERIFY。
  - T013/0x5154F0: 固定24byte候補レコードを末尾追加。コピー元が配列内なら再配置前にoffsetを保存し、0x5155C0による再配置後にsourceを再基準化する。候補のrank・重複排除はここでは処理しない。容量成長/例外処理はVERIFY。
  - Wave5: 12/16 VERIFIED（今回+4）/未着手4/関数VERIFY0。残りP1=0x5158A0,0x57CFA0,0x57CFD0,0x5155C0（T013）。P0 29/29、P1 31/35。全Wave 60/64。
- **Limitations and errata:** - Wave5: 12/16 VERIFIED（今回+4）/未着手4/関数VERIFY0。残りP1=0x5158A0,0x57CFA0,0x57CFD0,0x5155C0（T013）。P0 29/29、P1 31/35。全Wave 60/64。 / - 次回は前提負荷を確認し残りT013 4関数の正式5方法取得を優先。部分失敗はVERIFY/BLOCKEDへ区分。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_WAVE5_SAVE_TREE_COMPARE_AUDIT_20261011_2241.md

- **Source relative path:** `rea_lab/decomp_task/REA_WAVE5_SAVE_TREE_COMPARE_AUDIT_20261011_2241.md`; actual SHA256 `368DF7D69C302870A0C191C4E6159218CD4BB63D99065AD545D6F8FFDB88B350`, 4478 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 0x598980 / T014 / Spot runtime読込 / 859 bytes。info=ev_53ed1be96bc20ed0ffbc4d954ae100f1967fd59ebe9ce1884069085408de84aa
  - 0x5964C0 / T014 / Power runtime読込 / 1489 bytes。info=ev_105b1c184be5d868744bee92f4d32362e03bb147780923add1925cff2553acea
  - 0x4A6700 / T005,T014 / tree挿入primitive / 478 bytes。info=ev_f1a511812cc60f2d44928133ae37f2dd7702b5455677c9675e1f0387edef3654
  - 0x40B200 / T006,T010（用途ラベル再検討）/ 文字列比較helper候補 / 84 bytes。info=ev_ec2dd487c7478081fb26ce910a9b854f47c123371b542f12e59e6bdf5534439f
  - 0x598980 は既存tree/複数fieldを初期化してtagを逐次読込。tag長0でreturnし、長8/12/10/7の比較を経て読み込むfieldが分かれる。特殊tagで入力stream状態を検査しLoadExceptionを送出する分岐がある。tag名と各field意味はVERIFY。
  - 0x5964C0 はPower関連複数field/tree/vectorを初期化し、tagを逐次読込。長7/9/8/10の識別や0x40B200照合を経て格納先を分ける。特定tagが見つからない経路で+0xDCに0x80000008を設定する。数値が示す意味と書込側との整合はVERIFY。
  - 0x4A6700 はmap/set長さ上限guard、node挿入位置のleft/right接続、red-black tree向け色/rotation更新の局所実装。ここから重複keyの先勝ち/後勝ち・payload mergeを直接確定しない（caller契約が必要）。
  - 0x40B200 はC文字列の長さと[EDI+0x10]を照合し、0x402C40比較結果が0で両者同長の場合だけtrueを返す。**単独ではevent flagやゲーム条件を判定していない**。現キューの「eventフラグ条件判定helper」は仮称で、87解決済みcallerに基づく実使用域の分類が次課題。
  - T005/T006/T010: 0x40B200 callersから実用途を分類、0x4A6700を呼ぶwrapperのduplicate handlingを区別。疑似コードのunaff_*引数は未確定ABIに留意。
  - 現Wave5=8/16 VERIFIED、今回+4、Wave1/2/3/4=16/16・10/10・10/10・12/12、累計56/64。残Wave5はP1 8件（0x4705F0,0x470700,0x471D20,0x5154F0,0x5158A0,0x57CFA0,0x57CFD0,0x5155C0）。旧EXE gameplay golden PASS0、研究MASTER DONE9/34、ゲーム再実装率未測定。
- **Limitations and errata:** - 0x5964C0 はPower関連複数field/tree/vectorを初期化し、tagを逐次読込。長7/9/8/10の識別や0x40B200照合を経て格納先を分ける。特定tagが見つからない経路で+0xDCに0x80000008を設定する。数値が示す意味と書込側との整合はVERIFY。 / - 0x40B200 はC文字列の長さと[EDI+0x10]を照合し、0x402C40比較結果が0で両者同長の場合だけtrueを返す。**単独ではevent flagやゲーム条件を判定していない**。現キューの「eventフラグ条件判定helper」は仮称で、87解決済みcallerに基づく実使用域の分類が次課題。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_WAVE6_ABI_BOUNDARY_AUDIT_20261012_0236.md

- **Source relative path:** `rea_lab/decomp_task/REA_WAVE6_ABI_BOUNDARY_AUDIT_20261012_0236.md`; actual SHA256 `88A96ED229BDFC480F803937F4C03F9D5EB0A59C23415EC949D96F7AE2118DA6`, 8698 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - No additional native result declared from this safety/metadata-only source.
- **Limitations and errata:** - [POSTSTATE] 早期RETはEAXを変更しないため、`57CFB5 MOV [ESI+4],EAX`は`end=begin`を設定する。元から空の枝も`end==begin`である。続く`57CFB8..57CFC7`で5 DWORDをpushし`0x57CFD0`へ進む。従ってこのwrapperの実局所効果は**既存vectorの論理サイズをゼロへ戻してから新しい範囲insertへ進む**ことであり、既往Wave5説明の『非空既存範囲に5158A0を適用（実データコピー）』はこの呼出元について訂正が必要。 / - [IMPORTANT LIMIT] 5158A0の一般関数自体は`ECX!=EDX`なら24byte単位でsrc→dstを前向き複写する（Ghidra既証）。今回のゼロ回コピー断定は`57CFA0`からの上記レジスタ設定に限定。他callersや`57CFD0`内部のmemcopy/alloc/free/失敗exceptionまでno-opとは断定しない。元データが破棄される時の例外安全性と正常挿入後の結果・ゲーム観測はVERIFY。
- **Status:** BLOCKED_METADATA_ONLY; original Golden PASS 0, READY 0.

### REA_WAVE6_XREF_ELIGIBILITY_AUDIT_20261012_0140.md

- **Source relative path:** `rea_lab/decomp_task/REA_WAVE6_XREF_ELIGIBILITY_AUDIT_20261012_0140.md`; actual SHA256 `AB2293CC22D21566745E25099773DFD248F98C41D82C51DBB879754749DEC972`, 4672 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - No additional native result declared from this safety/metadata-only source.
- **Limitations and errata:** ## 保留理由と安全な再開条件
- **Status:** BLOCKED_METADATA_ONLY; original Golden PASS 0, READY 0.

## Curator-only formal integration

These old T013/T014/Unit/Save/Wave records are searchable by source SHA. Assign a distinct research ID only after checking full source native VA/call evidence and competing owner reports. No prohibited VA/denied Wave6 material has been reacquired or posted. No unrelated Work/user PC files, game originals, private raw logs or current develop modified. New formal VERIFIED=0; Golden PASS=0; READY=0.
