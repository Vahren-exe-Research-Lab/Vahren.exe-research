# REA early legacy research source audit A — original pre-ID T013/T014/unit/event/Wave notes

**Stage: SOURCE_PRESERVED_UNKEYED or EXISTING_ID_CORRECTION, NOT CURATED.** These 13 earlier independent REA owner Markdown files were never identified as newly decompiled functions by this recovery. Byte SHA256 of each original source was recomputed on the authorized research PC on 2026-11-02 JST; excerpts below are safe historical native/E8/ABI/semantic notes, not a formal Ghidra 5-method replay. They may duplicate a later source and need curator ID/VA/source-SHA/errata reconciliation. Files carrying a refused Wave6/refusal payload are represented by filename/SHA/BLOCKED metadata only, without denied target/results. Original Golden PASS 0 / READY 0, newly VERIFIED 0. No raw data, privacy-sensitive paths or unreviewed evidence JSON published.

### REA-20261021-0133-T014-255BYTE-CROSSCALL-01

- **Source key:** `rea_lab/decomp_task/REA_20261021_0133_T014_255BYTE_WRITER_READER_BOUNDARY_QC.md`; measured source SHA256 `C072454DA8E2051080825A4A3BCFF4269F25BD388E51EAF72F08AD52CC846D23`, 4631 bytes.
- **Explicit owner ID:** `REA-20261021-0133-T014-255BYTE-CROSSCALL-01`. 
- **Allowed source-native excerpt:**
  - [SOURCE] 既存Ghidra REA6.1.0/Ghidra12.1.4。writer 0x470830 run 20261009T220712454Z、reader 0x4705F0 run 20261011T144115307Z。両run記録のsource SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回のEXE現物SHA再検証は未完了。
  - [EVIDENCE] writer 0x470830 assembly ev_1ffa032ec901cde47d6811b2e2941ff163adbcd1a68d9573bed5f6efe6b58d02、info ev_f5a8158a6b43e2506ce3d112878862b8be232e8a7c08fc0fe9ec860f3c4f13b7、pseudo ev_f4d406c9b915c36f64a7240ca52a5c0345099560a2e9dd81232283f7c17caeaa、callers ev_8fd58bea9f3f6285fa73f9136ed4579d386ca9d352795c38d35e05fede16f880、callees ev_4be1ac4fd6e4af83c86e6b6cb48154a8d4a875b9350ce5c5bec15ea9fa4e1845。
  - [EVIDENCE] reader 0x4705F0 assembly ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d、pseudo ev_3851d07b1e0119564efeb2d7215b9c16ff9a63f274ce843c13ed100dfee38752。reader 5-method VERIFIEDはrun 20261011T144115307Zで既確認。
  - [WRITER X86] 0x470837 EDX=[ESI+0x10] length、0x47084F/0x470860で各byteのsigned許可範囲0x20..0x7Fを事前走査、0x47086B..0x47088Aで全length byteを0x4294B0へ渡す。255 byte上限はこの関数に存在せず、0x47088C..0x47088Fで末尾NULを1byte書く。
  - [READER X86] 0x470611が0x470980で1byte取得、0x470643..0x470645が読んだNULで終了。非NUL許容byteの場合0x470653でESI++、0x47065C CMP ESI,0xFF /0x470662 JL 0x470610で255未満のみ次byteを取得。255個目で返る経路0x470664以降に追加readはない。
  - [NEW DELTA 254/255] 非NUL合法ASCIIで不変stream・正常stream flags・連続する同reader呼出を前提とすると、len=254はreaderが255番目の終端NULを取得して停止するが、len=255は255個目取得時点で停止し、writerが書いた終端NULをstreamに未消費で残す。
  - [NEW DELTA 256] len=256の場合、初回readerは先頭255byteだけ取得し、後続readerは残る256番目のbyteから読み始める。いずれも単一reader呼出の通常終了時に元のwriter文字列境界と必ずしも整列しない。
  - [CONSEQUENCE] 255個の許可byte列に続く正常NULなら次の0x4705F0は空tokenを返し得る。上位のempty token/sentinel判定がレコード終端と解釈すれば項目ずれの可能性。ゲーム内で255byteの合法キーが生じるか、上位が追加読み飛ばし/長さ検査を行うかはVERIFY・旧実機NOT RUNであり原作バグとは断定しない。
  - [NEXT] T014でreader 0x4705F0 callerの境界/空token処理を既存証拠で確認し、長さ254/255/256を合成契約として設計（旧原作実機goldenに換算禁止）。次点T010/T012の0x575F71/0x575F91正常帰還。原本・A〜E・MASTER・T018・QUEUE/PROGRESS・他研究・Git/push/公開・MCP/automation変更なし。
- **Source limitations:** - [CONSEQUENCE] 255個の許可byte列に続く正常NULなら次の0x4705F0は空tokenを返し得る。上位のempty token/sentinel判定がレコード終端と解釈すれば項目ずれの可能性。ゲーム内で255byteの合法キーが生じるか、上位が追加読み飛ばし/長さ検査を行うかはVERIFY・旧実機NOT RUNであり原作バグとは断定しない。 / - [MASTER/GOLDEN] MASTER現存末尾checkpoint195、研究DONE9/34・IN_PROGRESS21・VERIFY4。旧EXE実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。
- **Stage:** PUBLISHED_INTAKE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA-20261021-02H-T014-SPOT-PREFIX255-CASCADE-STATIC-01

- **Source key:** `rea_lab/decomp_task/REA_20261021_02H_T014_SPOT_PREFIX255_FIELD_SHIFT_STATIC_QC.md`; measured source SHA256 `E743D67ED86C3ACFF5963C8786E94609AA27C2B44D9BCAA6F73997450E9B1BFE`, 4361 bytes.
- **Explicit owner ID:** `REA-20261021-02H-T014-SPOT-PREFIX255-CASCADE-STATIC-01`. 
- **Allowed source-native excerpt:**
  - [SOURCE] 既存run 20261011T133432356Z（0x598980）と20261011T144115307Z（0x4705F0）、両者REA6.1.0/Ghidra12.1.4、source SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回承認済コピー現物SHAも一致。
  - [EVIDENCE] Spot reader 0x598980: assembly ev_66c1bf6fd99abcfd7034dc3de539e043f9ab1f39ea402827967a1ab418ca929b / info ev_53ed1be96bc20ed0ffbc4d954ae100f1967fd59ebe9ce1884069085408de84aa / pseudo ev_0acff01a3a0b32c2efc27bc4c2c113a5990bee48a71916922824806d419968ad / callers ev_4d7481471a3b7dd25ba99a255743190483ec355ad0f0e6519faff740ac1a22e9 / callees ev_6597562b214fb07ef9cf92fb2a7c26825f7f6c86082b307f37ef650e62a31f52。
  - [EVIDENCE] Token reader 0x4705F0: assembly ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d / callers ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87。5-method VERIFIEDは既存runにて確認済み。
  - [SPOT PREFIX] x86 0x5989B8 PUSH EBX→0x5989B9 CALL 0x4705F0、0x5989C4 PUSH [EBX+2C]→0x5989C5 CALL、0x5989D0 PUSH [EBX+64]→0x5989D1 CALL。0x5989E2と0x5989F1にCALL 0x470700が続く。最初の3文字列の間に余剰NULを捨てるCALLはこの直列領域にない。
  - [READER BOUND] 0x470643 NUL判定、0x470653 INC ESI、0x47065C CMP ESI,0xFF / 0x470662 JL。正常stream・許容byte 0x20..0x7Fなら非NUL 255個を取った時点で0x470664へ進み追加NULを消費しない。
  - [SCOPE] 上記は長さ>=255の許可byte列、通常ストリーム、連続する0x4705F0呼出、回復処理無しという限定仮定。後段0x470700のstream flag/異常例外/旧EXE可視結果はVERIFY。既存ゲームSpotキーに該当長が存在することは未確認であり原作バグとは断定しない。
  - [DEDUP] 20261021 01:33既存REA_20261021_0133_T014_255BYTE_WRITER_READER_BOUNDARY_QC.mdはwriter-reader一般境界。今回の独立差分は保存済みSpot reader 0x598980の連続3token+2数値という具体的な呼出位置への接続のみ。
  - [NEXT] T014: 0x598980の先頭token後の異常処理と、原作script内Spot keyの長さ上限（別owner資料はread-only）、読み出し済み第2tokenからの後続数値読み取り位置を条件付きで検証。次点T010/T012の0x575F71・0x575F91。
- **Source limitations:** - [MASTER/GOLDEN] 最新MASTER checkpoint195、研究DONE9/34、IN_PROGRESS21、VERIFY4。旧EXE実機golden PASS0、strict MATCH0。ゲーム再実装率は測定していない。 / - [NEXT] T014: 0x598980の先頭token後の異常処理と、原作script内Spot keyの長さ上限（別owner資料はread-only）、読み出し済み第2tokenからの後続数値読み取り位置を条件付きで検証。次点T010/T012の0x575F71・0x575F91。
- **Stage:** PUBLISHED_INTAKE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_20261026_07H_P0_DSHOW_EVENT_PARAMS_VERIFY_ADDENDUM.md

- **Source key:** `rea_lab/decomp_task/REA_20261026_07H_P0_DSHOW_EVENT_PARAMS_VERIFY_ADDENDUM.md`; measured source SHA256 `7A90FAEBAADEC29CCD4FEF2E1505C45128CC9DD9FF67B5A35AF55C4AAB3204CE`, 1513 bytes.
- **Explicit owner ID:** `REA-LOCAL-20261026-0738-P0-DSHOW-EVENT-LOOP-STATIC-01`. This ID is already indexed; this file is an erratum or supporting source, not a second research ID.
- **Allowed source-native excerpt:**
  - 出典: Ghidra search.sqlite の 0x004BF6A0/0x004BF780 の疑似C・間接CALL索引と、同SHA原作EXEのCapstone限定ASM。
  - 0x004BF6A0はGetEvent相当 (0x004BF6D8) が成功した場合、0x004BF700で vtable+0x30 (=IMediaEvent::FreeEventParamsに整合) を呼んでから復帰する。
  - 0x004BF780はGetEvent相当 (0x004BF7AD) の直後に 0x004BF7AFでeventCodeを比較し 0x004BF7BBで直接RET。第一のDirectShow分岐にはFreeEventParams相当のCALLが存在しない。
  - 追加のGolden設計NOT RUN: DirectShowのパラメータ所有イベントを一つ受信した時、0x004BF780の枝でFreeEventParams相当が呼ばれないか実際のvptr/COMログで採取し確認する。
- **Source limitations:** Microsoft公式GetEvent契約は成功したイベントのFreeEventParams呼出しを推奨。通常EC_COMPLETEはパラメータ解放が不要な場合もあるため、これだけで実際のメモリリークを確定できない。eventCodeの種類とp1/p2の所有権は原作実ゲーム未測定、P0 VERIFYとして保持。 / 本追加発見は既存監査54/54の検査数には加算しない。正式REA5証拠完備0、VERIFIED+0、Golden0、TODO/VERIFY/BLOCKED正式変更0/0/0。
- **Stage:** DUPLICATE_OR_ERRATUM_LINKED, not formal CURATED; original Golden PASS0 / READY0.

### REA_20261027_18H_P0_DEBUGPAPER_EOL_ERRATUM.md

- **Source key:** `rea_lab/decomp_task/REA_20261027_18H_P0_DEBUGPAPER_EOL_ERRATUM.md`; measured source SHA256 `75089B6F555AC740E44586767BAD4DDFE670CB9EF49B086CD5E57050F18CED18`, 718 bytes.
- **Explicit owner ID:** `REA-LOCAL-20261027-18H-P0-DEBUGPAPER-CRLF-EOF-STATIC-01`. This ID is already indexed; this file is an erratum or supporting source, not a second research ID.
- **Allowed source-native excerpt:**
  - No additional source-native assertion promoted; historical refusal/status metadata or no safe extractable statement.
- **Source limitations:** これはMarkdown表示だけの訂正。証拠JSON・監査スクリプト・元報告書は変更せず、保存済みSHA・45/45 PASS・正式VERIFIED増分0・Golden 0を維持する。
- **Stage:** DUPLICATE_OR_ERRATUM_LINKED, not formal CURATED; original Golden PASS0 / READY0.

### REA_20261030_11H_P0_FRAMECOMMIT_GUARD_ADDENDUM.md

- **Source key:** `rea_lab/decomp_task/REA_20261030_11H_P0_FRAMECOMMIT_GUARD_ADDENDUM.md`; measured source SHA256 `BF9F96EE84AB186477D7421723F09F8B22934A0D99A9E92DA4904819E86EE884`, 2661 bytes.
- **Explicit owner ID:** `REA-LOCAL-20261030-11H-P0-VORBIS-FRAMECOMMIT-UNHANDLED-VERIFY-02`. This ID is already indexed; this file is an erratum or supporting source, not a second research ID.
- **Allowed source-native excerpt:**
  - 既存V9の`0x005D5790`（37bytes）と原本同一SHAの研究専用PEを直接照合。`0x005D5799 TEST ECX,ECX` の後、countが非0なら `0x005D57A0 ADD EDX,ECX`、`0x005D57A2 CMP EDX,[EAX+0x14]`、`0x005D57A5 JLE`で上限内を許容する。
  - 上限を超えると `0x005D57A7 MOV EAX,0xFFFFFF7D`（-131）からreturnし、`[EAX+0x18]`の消費カーソルを増やさない。成功側 `0x005D57AE ADD [EAX+0x18],ECX` はframe数を進め、`0x005D57B1 XOR EAX,EAX`で0を返す。
  - 呼出元 `0x005D0FB0` の `0x005D128D CALL 0x005D5790`直後は`0x005D1292 MOV ECX,[ESI+0x48]`、`0x005D1296 CALL 0x005D48E0`へ直行し、**commit helperの-131を判定しない**。その後 `0x005D12B7/BA` でframeBytes×frameCountの正の復号バイト数を返し得る。
  - 直前の`0x005D5730`が返すframesが利用可能frames上限内なら通常はcommit guardに収まると考えられるが、その不変条件は未検証。異常状態・競合・入力破損での到達は不明。音声欠落・同じPCMの再読込・原作バグを確定したものではない。
  - *次の最優先：** `0x005D5730`が与えるフレーム数と`0x005D5790`の残量ガードを直接照合し、消費失敗が実経路から到達可能かどうかをVERIFYする。
- **Source limitations:** `REA_20261030_11H_P0_FRAMECOMMIT_GUARD_AUDIT.py`のPE命令/V9/CALL静的検査 **23/23 PASS**。11H先行60/60を保持。新規正式REA 5種完備0・VERIFIED0、既存静的64/64、正式TODO/VERIFY/BLOCKED差分0/0/0。原作Golden0、完全複製率未測定。実ゲーム・Ghidra・REA再起動なし。 / **次の最優先：** `0x005D5730`が与えるフレーム数と`0x005D5790`の残量ガードを直接照合し、消費失敗が実経路から到達可能かどうかをVERIFYする。
- **Stage:** DUPLICATE_OR_ERRATUM_LINKED, not formal CURATED; original Golden PASS0 / READY0.

### REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01

- **Source key:** `rea_lab/decomp_task/REA_20261031_09H_V9_COVERAGE_INSPECT.md`; measured source SHA256 `9EC1483ABEA7D193C56F0775CB873A2ACC68556DA670AA74424F7DC196C1EEE5`, 1446 bytes.
- **Explicit owner ID:** `REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01`. 
- **Allowed source-native excerpt:**
  - `--inspect 0x005D9E70`: 関数入口同VA、pseudoあり、辞書symbols未登録。検証済E8 caller 4、callee 3、ghidra xrefs 4、unresolved owner sites 0、研究索引documents 0。
  - caller `0x005D3ECC` (`0x005D3DE0`)、`0x005D5B60` / `0x005D5B9D` (`0x005D57C0`)、`0x005DA857` (`0x005DA550`)。全てV9ネイティブCALL site記録。
  - callee `0x005D9E85`, `0x005D9E95`, `0x005D9EBD` は `0x005B71E8` へ直接E8。
  - `--inspect 0x005DA811`: 所属関数 `0x005DA550`、pseudoあり、辞書symbols未登録。検証済E8 caller 1（`0x005D41A1`→`0x005DA550`）、callee 27、unresolved owner sites 0、研究索引documents 0。
- **Source limitations:** Research ID: `REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01`, owner REA/T015, STATIC_METADATA/VERIFY/NOT READY.
- **Stage:** PUBLISHED_INTAKE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_B_AI_OWNER_EVIDENCE_CROSSWALK_20261012_2035.md

- **Source key:** `rea_lab/decomp_task/REA_B_AI_OWNER_EVIDENCE_CROSSWALK_20261012_2035.md`; measured source SHA256 `D28E2428CD6E59C92CC9563FC25B2B2D8339D3FB50BC8FE2927F16A4DB60E151`, 16052 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - Native evidence: exe/T013_NORMAL_AI_BOUNDED_NATIVE_20261012.txt, range 0x4E53B0..0x4E5854, sha256 3e2bceb1c7a36bd8ecf96df6587aac6a029ca2c739680265cf0aaf5006d6b428 (range digest from B evidence, not a newly computed hash).
  - 0x4E53B0 / T013/T012: 0x4E53BD..0x4E53DA classify owner+0xC as 1/4; 0x4E53DF checks actor+0xC8<0, then 0x4E53E8 directly calls CRT rand 0x5B6EAB. 0x4E5422 checks grid+0x3C; nonzero branch 0x4E5459 also directly calls rand 0x5B6EAB before the occupancy scan. Both results are mode/condition dependent.
  - 0x4E54C8..0x4E54FE: grid branch requires candidate+0x65!=0 and opposite effective owner side; first matching candidate is returned, not closest-distance winner. No direct self-pointer exclusion is present in this grid loop.
  - For non-grid, owner documents 0x4E5509..0x4E5854 as bucket-first then directed neighboring buckets; semantics and x87/overflow remain owner VERIFY where stated.
  - These native bytes are B-owned preexisting evidence; 0x4E53B0 has no recorded REA info/pseudo/assembly/callers/callees 5-point evidence here. No static VERIFIED promotion, no new evidence ID; do not duplicate the B disassembly or treat B's READY as gameplay PASS.
  - 主根拠: `exe/T012_ACTION_KNOCK_ORDER.txt` の0x57AD56..0x57AEE7（UTF-16LE、SHA256 CE1FF9D65200BD8A2F0A6EFDBC213E77319224228E979490091379BDF5FCA69B）。Bの全契約を重複転記せず、順序と再開位置に限定。
  - 対象の通常Unit vtable bindingはWork側0x63A9E4。native0x57AE39は当該Unitのvtable+0x7Cを呼ぶ。実callback先・全Unit subclassへ一般化せずVERIFYとする。
  - | 0x57AD56 | +1867E非0、+D4負、+186AC非0なら索敵をskipし+1E570=0 | bypass先0x57AEDB→0x57AEE7。索敵用RNGを呼ばない |
  - | 0x57AD84..0x57AD9A | oldNearbyをESIへ保存→0x57AD8C call4E53B0→返EAXを+1E570へ書込 | callee成功後は0x57AD91から再開。old/new pointerを別々に保持 |
  - | 0x57ADA0..0x57AE8E | +1868C>0、571A40のraw AL0、+1A4非0、byte+134非0の場合だけ0x40ED80を呼ぶ | EAX=100、EDI=0。抽選済み値とRNG状態を保存し次は0x57AE93 |
  - | 0x57AE93..0x57AEB5 | +18600と抽選値を比較した後でoldNearby/newNearbyを検査しBLを決定 | old/new pointerが不適格でも先行抽選を取り消さない |
  - | 0x57ADFF..0x57AE05 | nearby非null時+53Cを増加、+1869C=0 | 中断復帰で同じ更新を二度実行しない |
  - | 0x57AE33..0x57AE4F | +1E4D8を減算してからvtable+7Cを呼び、残量<=0なら+1E4D4を消去、その後AL判定 | callback前後を別stage化。成功済み減算を再実行しない |
  - | 0x57AEBC/0x57AECA | 57E4E0を先にcallし、そのAL0の場合だけ57E1D0をcall | return位置57AEC1/57AECF。真のUnit returnまでTask次slotへ進めない |
  - 今回の実装上の要点: **nearbyが無いから抽選不要、と先に短絡してはいけない経路がある**。0x57AE8Eのdrawは0x57AE9F/0x57AEA7のold/new検査より前。復帰のたびに57AD56を再実行すると索敵・抽選・counter更新が重複する。
  - RNG根拠: `runs/20261009T194358486Z/40ED80_procedure_assembly.json`、evidence ID `ev_74c7a4ee5e8d96d0bfb64e52035f32b76121125762d05ee7f56ce8300e56ea02`。同wrapperは0x40ED84でCRT randを直接1回、x87尺度変換→0x40EDA3で0x5D1B80→EDI加算。丸め・FPU環境の実機一致はVERIFY。
  - 4E53B0側の条件付きRNGと上の40ED80 draw、後続0x57AF3Eのtimer drawは別site。既存57B870の周期再探索と4E53B0近傍探索も同じ処理にまとめない。
  - 復旧後の優先: Workが実装中断している0x57AD56周辺の包含関数入口、0x4E53B0、0x57E4E0/0x57E1D0の5点証拠を既存結果と重複しない単位で取得。0x57AD56を未確認の独立関数入口としてキュー登録しない。
- **Source limitations:** - 0x4C5CC0の許可済保存命令には対象object vtable+0x34/+0x8、条件付き0x4C22B0、vtable+0x48/条件付き0x4C3E40、vtable+0x44、0x4BC9C0が含まれる。0x41E160からBL=0で到達することと、callee/virtualの全副作用まで確定していることは別。 / - 再構成用の境界: manager/record pointer identity、順序、vtableごとの生AL、TaskRegistry解除・render解除・graph vector最初一致のtail-swap・Unit/選択troop更新を別traceへ。未知virtual/calleeへの副作用や例外を0に補完せずVERIFYで停止。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_EVENT_FLAG_SLOT_MATRIX_20261011_0236.md

- **Source key:** `rea_lab/decomp_task/REA_EVENT_FLAG_SLOT_MATRIX_20261011_0236.md`; measured source SHA256 `98AC7E0E8C3D3A92F9C703411CFB83F9E23A3A1A2DBDDE4B1A879D7196B82C78`, 2733 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 判定: CONFIRMED-SAVED-ASSEMBLY（関数0x4321B0内部のみ）。参照slotのゲーム上の意味と実機再現はVERIFY。
  - 0x4329B6..0x4329DB: 2入力参照を個別にNULL補完。NULLなら[engine+0xC]+0x58を代入、非NULLは元値を維持。0x4329E1で+0x1EED54/55の2byteを0、+0x1EED56を0にする。
  - 0x432A74..0x432AD2: まずrefA+0x1D非0、または0x40B200(literal VA0x636224)が非0ならflagA=1（+0x1EED54）。flagA=1の場合、flagBを評価せず分岐。
  - flagA=0の場合のみrefB+0x1D非0、または0x40B200(literal VA0x63622C)が非0ならflagB=1（+0x1EED55）。同じ呼出内でflagAとflagBが同時に1になる経路は見えない。
  - 0x432AD9..0x432B3A: flagの組合せでengine+0x1E8630/34/38から選んだ値を+0x1EED48と+0x1EED44へ設定。
  - | flagA | flagB | +0x1EED48 | +0x1EED44 |
  - | 0 | 0 | value at +0x1E8634 | value at +0x1E8638 |
  - | 1 | 0 | value at +0x1E8634 | value at +0x1E8630 |
  - | 0 | 1 | value at +0x1E8630 | value at +0x1E8634 |
  - 0x432B49で+0x1EEC4Dへ1書込、その後も実行継続。二つの出力slotは同一値のコピーではなく3ケースの選択結果。
  - 上記は保存済み静的アセンブリの局所分岐。+0x1E8630/34/38の型・意味・有効期間、0x40B200 comparator実効、他関数の書換、旧EXE実機挙動はVERIFY。
- **Source limitations:** # 観測した命令と条件 / - 上記は保存済み静的アセンブリの局所分岐。+0x1E8630/34/38の型・意味・有効期間、0x40B200 comparator実効、他関数の書換、旧EXE実機挙動はVERIFY。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_EVENT_POWER_NULL_FALLBACK_AUDIT_20261011_0138.md

- **Source key:** `rea_lab/decomp_task/REA_EVENT_POWER_NULL_FALLBACK_AUDIT_20261011_0138.md`; measured source SHA256 `DBCD54E6C77082A1FC37CB501EFAC15078303E30B6AD86EADEC59DF8435B3B20`, 1814 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 対象: `0x4321B0`、保存run `20261009T225741694Z`、target SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回再hashなし）。
  - `0x432992`/ `0x432999`で2つの入力参照を取得し、`0x4329AA`/ `0x4329B0`で`engine+0x1EED4C`/ `+0x1EED50`へ一旦書く。
  - 第1入力がNULLの場合`0x4329BA..0x4329C0`で`*(engine+0xC)+0x58`をアドレス値として代入、非NULLの場合は入力保持。
  - 第2入力も独立に`0x4329C6..0x4329DB`で同じfallback計算、非NULL値は入力保持。
  - `0x4329E1`で2フラグを初期化。続く条件判定`0x432AA6`/ `0x432AC0`へ進む前に両参照の補完が終わる。
- **Source limitations:** - `0x4329E1`で2フラグを初期化。続く条件判定`0x432AA6`/ `0x432AC0`へ進む前に両参照の補完が終わる。 / - 上記は保存済み機械語の局所経路CONFIRMED-STATIC。NULL補完先のゲーム上の意味、入れ子のイベント参照復元、他呼出経路はVERIFY。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_EVENT_SCENE_OBJECT_BRANCH_AUDIT_20261011_0534.md

- **Source key:** `rea_lab/decomp_task/REA_EVENT_SCENE_OBJECT_BRANCH_AUDIT_20261011_0534.md`; measured source SHA256 `1B1159747CB1574E7B73AEF1A2C96B98ADEA0A0698A1E28F93397D0BDF6B7E56`, 2622 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 対象: T006/T010（関連T015は他レーン所有・参照のみ）。関数VA 0x4321B0、既存run 20261009T225741694Z。
  - 0x432B49でengine+0x1EEC4D=1の後、0x432B6Fでevent property lookup (0x4647D0)。
  - 0x432BA1で取得property+4を0x402710に渡して局所文字列へ転写。0x432BE1で局所値と0を比較して分岐。
  - 条件ゼロ側 (0x432BE8以下): 0x34 bytes確保 (0x5B6C2B)、0x543A30初期化、vtable 0x6388D4 (FadeOutSheet)、virtual offset +0x18へ引数0xA (10)を渡す。
  - 非ゼロ側 (0x432C3C以下): 同0x34 bytes FadeOutSheet初期化に続け、0x432C6Eで0x30 bytes確保し、0x432CB1で0x5434B0 (args: engine window, 0xC8=200, 0x32=50, 0x32=50) を呼ぶ。virtual +0x18へ引数0を渡す。
  - 通常経路のどちらでも仮想callは0x432CC9で行われ、ただし受信オブジェクト/引数が分岐ごとに異なる。
  - 入口0x4321F4と0x432209の両guard真なら0x432216側へ進み、一般経路の上記シーン生成処理を通らない（本関数内の経路に限る）。
  - 0x5434B0オブジェクトの意味と画面効果、0x402710で導かれる厳密な条件、FadeOutSheet副作用、その他callerの重ね合わせはVERIFY。文字列の空/非空として実機仕様を断定しない。
- **Source limitations:** - Scene遷移を必ず単一のFadeOutSheet呼出へ単純化せず、条件別のオブジェクト構成/virtual引数をtraceすること。 / - 進捗: Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12, 累計39/48（重点静的関数のみ）。P0 20/21、P1 19/27、TODO8/VERIFY1。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_SAVE_GROUP_SENTINEL_EXACT_MATCH_AUDIT_20261011_0337.md

- **Source key:** `rea_lab/decomp_task/REA_SAVE_GROUP_SENTINEL_EXACT_MATCH_AUDIT_20261011_0337.md`; measured source SHA256 `A060FA42C20BB053BB8D097D96FD99C2199304EDDCE5FC62AF7DDFFE7AE44AAB`, 3086 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 4 groupの比較ブロック: #1 0x45E350..0x45E390、#2 0x45E3E4..0x45E425、#3 0x45E467..0x45E4A8、#4 0x45E4E3..0x45E524。
  - 各ブロックは読み込んだ名前の長さと共通marker長(0x65CD38)から短い方を比較長として0x402C40へ渡し、比較結果0の場合も別途「両長さが等しいか」を判定する。よってprefixだけ一致する短い/長い文字列は区切りとは認識しない。
  - 完全一致した区切りの場合は当該record payload readerを呼ばず次groupへ進む。通常名の場合だけ第1群0x4705F0+0x470700、後続群0x58E870/0x598980/0x5964C0へ進む。
  - 書込側0x460000は各群の後に共通marker 0x65CD28を0x470830で記録。Writer 0x470830は1byteでも0x20未満/0x7F超のbyteを見つけると文字列内容を捨ててNULだけを書く（既存確定）。通常名がmarkerと同じbyte列に変換された場合、readerはrecord境界と誤認する可能性がある。
- **Source limitations:** - 書込側0x460000は各群の後に共通marker 0x65CD28を0x470830で記録。Writer 0x470830は1byteでも0x20未満/0x7F超のbyteを見つけると文字列内容を捨ててNULだけを書く（既存確定）。通常名がmarkerと同じbyte列に変換された場合、readerはrecord境界と誤認する可能性がある。 / - 保存済み39/48=Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12。今回新規VERIFIED0。P0 20/21、P1 19/27、TODO8/VERIFY1。MASTER cp78 研究DONE9/34、旧EXE実機golden PASS0、ゲーム再実装率未測定。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_SAVED_NATIVE_PREFIX_CONTINUITY_20261013.md

- **Source key:** `rea_lab/decomp_task/REA_SAVED_NATIVE_PREFIX_CONTINUITY_20261013.md`; measured source SHA256 `4F3BA787A1BCF4909682163EB0470E9BC972C5DCD0D0F3DE1E1D13F920ABE7F4`, 16783 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - [NEW WORK STAGES] `normal_graph_broad`=699 tests/0 failure/0 error、`render_unregister_broad`=710/0/0、`window_unregister_broad`=720/0/0、`troop_selection_broad`=900/0/0、`window_expiry_broad`=915/0/0、その後`window_guard_broad`=916/0/0。**異なる時点のテスト総数を合算しない**。
  - [SOURCE CURRENT] Localのread-only `Get-FileHash`：`native_unit_tick.py`=`C18E2616F51EB89705D18F19932E3C2D8F4F6970D460067636AE9EDC4F262117`、`native_battle_session.py`=`2828152C0E0ABA1B6C6A357C93F9369453C8B3BF3007D5A32BD3A2D614BAA6E5`、`native_battle_runner.py`=`1DFBFD1D91C38378976AE38E94C6B296D3C0A4A99F88CA1088FE8E638D45B168`。
  - [SOURCE HASH LIVE] Local Compact Get-FileHash: `native_unit_tick.py`=`C18E2616F51EB89705D18F19932E3C2D8F4F6970D460067636AE9EDC4F262117`（前回同一）、`native_battle_session.py`=`5958C38062194C309A156BC86EE60A3C0B020C395ECFC387AE65713EA50FFE1D`（前回2828152C...から更新）、`native_battle_runner.py`=`B8AC7F9AD7221A333529478942F2D8F1576C13DCFEE1C522B88A0355B1EC2541`（前回1DFBFD1D...から更新）。前回REA-OWNER-DRIFT-20261013-1354-01の2hashは現行ではない。
  - [INNER SESSION] native_battle_session.py advance_resolved_unit_tick(): blocked nextVA 0x41E1C3でphase VERIFY_UNIT_WINDOW_DETACH・_unit_window_detach_context=(pointer,pending)を保管。専用の復帰handlerは今回確認した公開API/指定callerに存在せず、別名や別moduleにある全機能の不存在までは断言しない。
  - [OUTER TASK SUSPENSION] native_task_registry.py dispatch_unit_frame/_dispatch_tail(): tickがblockedならcursor.waiting_pointer、suspended_slotsを保持しTaskFrameTrace.complete=Falseを返す。native_battle_session.py advance_resolved_task_frame(): _task_child_phase=VERIFY_UNIT_WINDOW_DETACH、_task_child_next_va=0x41E1C3を保管した後self.phaseをVERIFY_TASK_FRAMEへ変更。これは直接window停止とは**別の再開必要条件**。
  - [OUTER API GAP] native_battle_session.py continue_resolved_task()のchoicesにwindow-detach stage/VERIFY_UNIT_WINDOW_DETACH用handlerがなく、未知stageはSessionGap。native_battle_runner.py task_continue_resolvedはこのchoicesを呼ぶだけ。単独unit_tick_resolvedの自動後続は0x57ABC0 knock又は0x57AA4D movement限定で、0x41E1C3は含まれずbreak。現行露出runnerでこの二段の停止から完走した証拠は0。
- **Source limitations:** - [INNER SESSION] native_battle_session.py advance_resolved_unit_tick(): blocked nextVA 0x41E1C3でphase VERIFY_UNIT_WINDOW_DETACH・_unit_window_detach_context=(pointer,pending)を保管。専用の復帰handlerは今回確認した公開API/指定callerに存在せず、別名や別moduleにある全機能の不存在までは断言しない。 / - [OUTER API GAP] native_battle_session.py continue_resolved_task()のchoicesにwindow-detach stage/VERIFY_UNIT_WINDOW_DETACH用handlerがなく、未知stageはSessionGap。native_battle_runner.py task_continue_resolvedはこのchoicesを呼ぶだけ。単独unit_tick_resolvedの自動後続は0x57ABC0 knock又は0x57AA4D movement限定で、0x41E1C3は含まれずbreak。現行露出runnerでこの二段の停止から完走した証拠は0。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_SIGNED_BYTE_WRITER_AUDIT_20261010_1636.md

- **Source key:** `rea_lab/decomp_task/REA_SIGNED_BYTE_WRITER_AUDIT_20261010_1636.md`; measured source SHA256 `ECC0DEAAD6365F2E474EE66903FB6B9FB97A3EAD5D65BA12662A0DB05FCDB267`, 2435 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 対象T-ID：T014。主関数VA `0x470830`、Unit writer caller `0x58EFD0`、Unit reader `0x58E870`。
  - `0x47084F: CMP byte,...,0x20` → `0x470853: JL 0x47088C` は **符号付き**条件。0x00..0x1Fだけでなく、0x80..0xFF（signed -128..-1）もここで拒否される。
  - `0x470860: CMP byte,...,0x7F` → `0x470864: JG 0x47088C` も符号付き条件。8-bit signed最大値が0x7Fであるため、この上限JG枝は8-bit入力に対して成立しない（到達不能条件）。
  - 判定は書き出し前の1passで全文を走査し、不適格byteが1つでもあればbyte本体を**一切出力せず**`0x47088C`からNUL終端のみを出す。途中まで出力する形ではない。
  - Unit writer `0x58F005`と`0x58F00D`はこの同じ `0x470830`を連続して呼ぶ。前者/後者の文字列フィールドはそれぞれ`+0`/`+0x1C`。
  - `0x4705F0`読込側が書込時に空文字化された名前をどの位置でsentinel扱いするか、Unit内部名前とouter-groupキーの合法な非ASCII値、意図せぬ読込終了・ゲーム上の実害は**VERIFY/NOT RUN**。旧EXE実機golden PASS0。
- **Source limitations:** - **再実装上の補正**：二つの比較をunsigned-byte範囲チェックと注釈するのは不正確。出力可能な範囲の結論は同じでも、命令の到達率・branch tracing・decompilerの差分検証ではsigned条件をそのまま保持する。 / `0x4705F0`読込側が書込時に空文字化された名前をどの位置でsentinel扱いするか、Unit内部名前とouter-groupキーの合法な非ASCII値、意図せぬ読込終了・ゲーム上の実害は**VERIFY/NOT RUN**。旧EXE実機golden PASS0。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

## Curator instructions

Earlier T013 support selection, T014 save parser/serialization and unit/event documents have overlapping existing native evidence. The exact old source SHA and specific VA/call/condition should be cross-checked with current REF/owner before assigning any distinct ID; file counts are not independent proof counts. Do not attempt any denied 0x target or Wave6 extraction, and do not publish raw original material. The unrelated readback and recovery receipt group is a validation aid, not source claims. Only curator may edit develop/REF/symbols.
