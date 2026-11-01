# REA early legacy / pre-ID owner archive C

**SOURCE_PRESERVED_UNKEYED or existing-ID ERRATUM, not formally CURATED.** 13 original REA owner reports were inspected read-only for source byte SHA, safe original-x86/ABI/control-flow statements and correction/status markers. No new Ghidra/REA/game tests, no newly formal five-method VERIFIED or Golden PASS. Current original PE/V9 were not re-hashed. Exact native-source IDs are recorded only when declared in a report header; no synthetic new research IDs. Safety refused Wave6/file/export material is metadata-only and omitted from substantive excerpts. Original reports and evidence stay on authorized PC.

### REA_T014_GRAPH_READER_MODE_TRIPLE_SECTION_AUDIT_20261012_1038.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_GRAPH_READER_MODE_TRIPLE_SECTION_AUDIT_20261012_1038.md`; actual SHA256 `10A0268E7080BB1A3D7F13794CD0A8CA7E49607C7F40F8C12A7EA3EFC00C0B31`, 10904 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 主関数 0x435550 / T014 / saved run 20261011T124000308Z: info `ev_8fc065296a08a2f672a520399680a38404d656f96ecd59f4747278ec964409a4`、pseudo `ev_7a9e58e9b0b538edf453aaf98e7755f5ebedda9102d81657c549716351eec905`、assembly `ev_775c749267e95e4682d3e76c638e9a612068de9345aedb4557eabd74e6eaafe2`、callees `ev_c4837ec9612a87de6e6c808ce950dde13e92ada453d6d4ac779eabc2d905b175`。body非連続4 ranges、1672bytes、完了run。
  - 根本呼出元 0x45E1E0 / T014: assembly `ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124`、pseudo `ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e`。0x45E547 PUSH 1 → 0x45E54C CALL 0x435550で通常save rootはparam_2=1経路を呼ぶ。
  - 0x435550は共通の先頭token/header一致検査後、param_2==0とparam_2!=0で後段を分岐。先頭headerの文字列値・失敗時例外は別途検証。
  - mode 0（param_2==0）: Unit相当の対象オブジェクト+0x1EEBD0の既存treeをclearし、+0x1EEC70を0へ初期化する経路。3セクションごとに0x5B6C2Bで0x36C,0x240,0x240 byteのオブジェクトを確保（構築0x4319B0,0x431E00,SpotEscapePath vtable）し、virtual +0x5Cをmode 0で呼ぶ。各レコードを0x436680→0x463280へ接続して挿入。これを一般的な全save reset条件と断定しない。
  - mode 1（param_2!=0）: 既存treeの上記clear/新規allocate経路ではなく、global側の0xB128B8,0xB12678,0xB12438にある3つの静的インスタンスを利用し、各サブreaderを最後の引数1でcallする。実際のcallee内部で他状態を更新しないことは未証明。
  - section #1: sentinel長/文字列 `0x65C854/0x65C844`、0x435774 CALL `0x5A90E0`、this=0xB128B8、呼出回数はループ内でレコード数に依存。
  - section #2: sentinel長/文字列 `0x65C870/0x65C860`、0x4357F0 CALL `0x5B0400`、this=0xB12678。
  - section #3: sentinel長/文字列 `0x65C88C/0x65C87C`、0x435874 CALL `0x5B0400`、this=0xB12438。この同一calleeをsection #2と共有するがthisが異なる。markerの実バイト列と3構造の意味はVERIFY。
  - 裏付け: `0x4705F0` callers `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`に0x5A90E0と0x5B0400が存在。保存済み全calleeファイルread-only走査でも両者の直接親は0x435550。両callee自身の5種類のREA証拠ファイルはruns内未発見。resolved referencesのみで間接caller網羅は不可。
  - 共通token reader 0x4705F0のresolved caller13中、独立に用途分類確定は引続き8件。今回2件(0x5A90E0,0x5B0400)は親における用途「graph subreader」まで局所確認（独立callee仕様未確定）。未分類5件0x45EAC0/0x470550/0x58E480/0x5A90E0/0x5B0400を完了扱いしない。
  - 0x435550 procedure_callers evidence `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`（runs/20261011T124000308Z）にはdirect callerが正確に `0x45E1E0` と `0x45EAC0` の2関数。前者のmode=1は前記PUSH 1で確定、**後者0x45EAC0がmode 0を渡すかは未確定**。
  - 0x45EAC0は0x4705F0 caller setにも含まれ、normal-save rootとは別のtoken消費・graph読込上位関数の候補として優先する。ただし0x45EAC0自身の保存済み5-method本文証拠は未発見なので「関数の完全分類済み」へ昇格しない。
  - ## 2026-10-13 04時台 — SpotPath/EscapePath reader 0x5B0400 のmode別終端／リンク条件（REA-T014-5B0400-MODE-20261013-0445）
  - [STATUS / SCOPE] T014。既存owner `data/T014_GLOBAL_SAVE.md` §「SpotPath / SpotEscapePath shared payload」に6フィールド順・endpoint名と再解決は既記録。重複発見として再加算せず、今回は**未記載の欠損endpoint枝とリンク引数条件／具体的reader-mode分岐**のみ追加する。保存済みlocal native静的照合であり、REA/Ghidra新規解析0、新しいinfo/pseudo/assembly/callers/callees一式なし、関数0x5B0400を新VERIFIEDにしない。
  - [PRIMARY] `exe/T014_SPOT_PATH_VFUNCS.txt` 282行以降の `0x5B0400..0x5B05F2`／直後別関数writer `0x5B0600`。対象保存nativeファイルSHA256 F95EF8CC0ECDFAE026F2B873C735C9B69F37689265F392CE1720110C6A77E23F（04:45 JST実測）。親Ghidra `0x435550` assembly ID `ev_775c749267e95e4682d3e76c638e9a612068de9345aedb4557eabd74e6eaafe2`、callee ID `ev_c4837ec9612a87de6e6c808ce950dde13e92ada453d6d4ac779eabc2d905b175`、`0x4705F0` callers ID `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`。5-methodの新規evidence IDではない。
  - [ABI/BRANCH] `0x5B0437 CMP BYTE [EBP+0x10],0`、`0x5B0447 JE 0x5B04E7`。呼出の第三stack引数low byteが非0なら**一時領域への読込／discard系**、0なら**当該objectへ読み込む経路**。THIS=ECX→EBX、stream pointer=[EBP+8]→EDI。未知world/registry入力=[EBP+C]は実型VERIFY。RET 0xC。親mode=1 direct `0x4357F0/0x435874`は同関数を別this=0xB12678/0xB12438で呼ぶ。
  - [NONZERO / DISCARD] `0x5B0468,0x5B0484,0x5B0491,0x5B049E` の`0x4705F0`計4回＋`0x5B0477 CALL 0x4707D0`計1回＋`0x5B04AB CALL 0x470700`計1回。取得先はESP上の一時領域（同領域を複数回再利用）で、**EBX+0x6C/+0x88/+0x1E8/+0x204/+0x220/+0x23Cへ直接storeは当該非0枝に無い**。文字列一時objectの条件付free `0x5B04B3..0x5B04C4`後、共通epilogue `0x5B04C7`。読取・stream cursor変化は発生するので「完全no-op」ではない。
  - [ZERO / REAL PAYLOAD] `0x5B04E7..0x5B0538`でobject+0x6C string、+0x88 byte-reader、+0x1E8/+0x204/+0x220 string、+0x23C dword-readerに直接格納。writer `0x5B0600` は同順（owner既知）。追加で`0x5B055D`と`0x5B0577`の `0x49E490` により+1E8/+204から取り出した2名称の参照先pointerを取得。
- **Limitations and errata:** - [PARENT MODE0 CORRECTION] 旧本メモ末尾「0x45EAC0がmode0を渡すか未確定」は保存済み `REA_T014_DUAL_MODE_CALLSITE_CONFIRMED_20261012_1142.md` のnative `0x45EF25 PUSH 0 →0x45EF34 CALL 0x435550`で**callsiteの渡す値0は確認済み**。ただしGhidra側caller関数境界 `0x45EAC0`の実入口/所属は依然VERIFY。従来文言を局所訂正するだけでGhidra caller 13を別高水準関数13件と断定しない。 / - [REIMPLEMENT/GATE] 0x5B0400のmode非0ではstream cursorは進むがobject field set／graph rebindを行わない局所枝。mode0ではフィールド復元→2 endpointの照合→エラーまたは条件付きlink flag。再構築型ロード時にmodeを混ぜず、5E72E5/5AFB30/5B864Eが未実装なら各calleeの直前で正常復帰を偽造せずVERIFY。Task T014 ownerへの読み取り連携対象、owner原本へ代行書込しない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_GRAPH_SENTINEL_AND_CALLER_EOF_AUDIT_20261011_1537.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_GRAPH_SENTINEL_AND_CALLER_EOF_AUDIT_20261011_1537.md`; actual SHA256 `669172215F25ADE63C23F068A8EDAD7DA5A13E89844D550B972EBD46B85E50A2`, 3834 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 対象VA: reader core 0x45E1E0 / graph reader 0x435550 / load wrapper 0x45E5F0（研究T014）。
  - REA 0x45E1E0: info ev_5da50720924339f770fe37dd127f90a1d8faff1b1c9c80922819ec9f7c999ef0; pseudo ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e。
  - REA 0x45E1E0: assembly ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124; callers ev_25b1ebae191adb744c52e90f5c7faa796423ecd9edc00b29aa5a5b241415b65e; callees ev_1c6253652438f3553d6e578d8b3afdc47b832a780c4732bf2d4117a9ca1a3f42。
  - 保存REAのcallers結果は0x45E1E0の解決済direct callerとして0x45E5F0を1件返す。indirect caller全件不在の証明ではない。
  - 0x45E5F0: 0x45E691 CreateFileA(GENERIC_READ / OPEN_EXISTING=3)、0x45E6C4 file size取得、0x45E6E3 ReadFile、0x45E6E9 CloseHandle、0x45E6F2 decode 0x4270F0。その後0x429C60経由で読み取り用streamを作る。
  - 0x45E75Eで 0x45E1E0 をcallし、戻った直後は0x45E763 add esp,4→0x45E76E 0x5B71DD→0x45E780 0x428680→buffer cleanup→0x45E7B2 ret 8。coreの後に直接のstream position/size/EOF比較は見えない。
  - 0x45E1E0は0x45E53E 0x471AF0（外交）、0x45E54C 0x435550（Spot graph）へ順にcallし、0x45E551以降cleanup、0x45E5EF return。core後に直接EOF比較は見えない。
  - 0x435550は先頭group sentinel 0x65C828を0x4355A8から比較、続く0x65C844/0x65C860と最後の0x65C87Cを使った文字列終端判定を持つ。
  - 最終の0x65C87C比較（0x435ADE..0x435B32）で一致側は0x435BBDのcleanupへ進み、0x435BEA ret 8に至る。最終sentinelを読んだ後の直接stream残量/物理EOF比較は見えない。
  - writer 0x460000がOPEN_ALWAYSで明示truncateしない従来確認と独立に照合。短い再保存→旧末尾残存は依然条件付きVERIFY。
  - T014: 0x45E5F0の直接caller/後続処理、0x429C60 stream構築/0x4270F0 decode失敗時の扱い、0x435550末尾のvirtual payload error伝播を保存済み証拠で確認。
- **Limitations and errata:** - writer 0x460000がOPEN_ALWAYSで明示truncateしない従来確認と独立に照合。短い再保存→旧末尾残存は依然条件付きVERIFY。 / - Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12、累計39/48。新規VERIFIED0、P0 20/21・P1 19/27、TODO8/VERIFY1。MASTER checkpoint83、DONE9/34、旧EXE actual golden PASS0、ゲーム再実装率未測定。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_NORMAL_SAVE_IO_RETURN_AUDIT_20261011_0738.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_NORMAL_SAVE_IO_RETURN_AUDIT_20261011_0738.md`; actual SHA256 `C08E03B034B3BBCC1680B7622140AF88399901364893AB1F8673BDBEF9BED25D`, 3295 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 状態: CONFIRMED-SAVED-ASSEMBLY（0x460000局所制御フローのみ）／実機でのエラー時挙動は VERIFY。新規逆コンパイル0件。
  - 対象関数: 0x460000, T014, Ghidra entry 0x460000, length 2096 bytes, status VERIFIED（元runで5操作整合）。
  - 0x4605B7..0x4605CA: CreateFileA引数はGENERIC_WRITE 0x40000000、share=0、OPEN_ALWAYS(4)、FILE_ATTRIBUTE_NORMAL(0x80)。既存A/T014で確認済みの条件を再確認。
  - 0x4605D4..0x4605DD: CreateFileAがINVALID_HANDLE_VALUE(-1)なら0x4606ADの共有後始末へ直接分岐し、WriteFile/CloseHandleの両callを飛ばす。
  - 正常handleなら0x46065Cの暗号化helper 0x427040を経て0x460687: WriteFile、0x46068E: CloseHandleを連続呼出。
  - WriteFile直後にその戻り値(EAX)のtest/cmpはなく、bytesWritten出力用stack slotの予定長との比較もこの局所後段では見られない。次の0x460694のCMPは文字列buffer capacity 0x10対[ESP+0xEC]であり、I/O成否フラグ比較ではない。
  - CreateFileA失敗時とWriteFile/CloseHandle後はいずれも0x4606ADの共通cleanupへ合流し、関数はvoid型としてretする（保存Ghidra疑似コードとも整合）。本関数内の明示的なI/O error result返却は確認できない。
  - 既存A/T014のglobal.sav Writer 0x428F84でのWriteFile返値非検査とは別の、通常 .savの独立callsite証拠であり、旧ゲームgolden PASSへの加算はしない。
- **Limitations and errata:** - 上記は単一writerの局所静的分岐のみ。上位callerによるファイル存在・sizeの事後検査、CRT/SEH経路、I/O障害のユーザー表示、失敗セーブの再ロード結果は未検証。原作の確定バグ／silent corruptionとは断定しない。 / - Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、累計39/48 STATIC VERIFIED。今回新規VERIFIED0、未着手8/VERIFY1、P0 20/21・P1 19/27。最新MASTER cp82は研究DONE9/34、旧EXE実機golden PASS0。再実装率未測定。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_OPEN_ALWAYS_TRAILING_BYTES_AUDIT_20261011_0831.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_OPEN_ALWAYS_TRAILING_BYTES_AUDIT_20261011_0831.md`; actual SHA256 `8F14419B5D10E53D63DB7F193EDECEC13E135612F81E032F88218515E0217C6E`, 3241 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 状態: CONFIRMED-SAVED-ASSEMBLY（0x460000局所API呼出と分岐のみ）／末尾残存・ロード影響・原作不具合はVERIFY。新規REA/Ghidra実行0件。
  - 関数: 0x460000、T014、info ev_76fca377cfc1ee6b6dd225934568ef4fb94e52cc359d35beff1ccb7ef68d99c3。
  - 0x4605B7..0x4605CA: CreateFileAへGENERIC_WRITE=0x40000000, share=0, creationDisposition=4 (OPEN_ALWAYS), flags=0x80, template=NULLを渡す。CREATE_ALWAYS(2)やTRUNCATE_EXISTING(5)ではない。
  - 0x4605D4..0x4605DD: INVALID_HANDLE_VALUEなら書込を飛ばしてcleanupへ。
  - 0x46065Cで0x427040を呼んだ後、0x46067D..0x460687でWriteFile(hFile, buffer, EBX byte count, &stackBytesWritten, NULL)を1回呼ぶ。
  - 0x46068D..0x46068Eで直ちにCloseHandle。0x460694のCMPはbuffer capacityと比較し、I/O戻り値や実書込長の検査ではない（前回監査を再確認）。
  - これは**条件付きの互換性リスク**であり、現時点でゲーム画面のセーブ破損/原作バグと認定しない。呼出元0x45F960/0x53A100や事前helper 0x435C10による削除、別の保存経路、readerがEOF以降を無視するかは未検証。
  - 次回優先: 既存の合法な静的証拠で0x45F960/0x53A100および0x435C10の事前ファイル処理が判明するか調べる。原作実機goldenはNOT RUN、制御された長→短save UI比較は将来の試験設計のみ。
- **Limitations and errata:** - これは**条件付きの互換性リスク**であり、現時点でゲーム画面のセーブ破損/原作バグと認定しない。呼出元0x45F960/0x53A100や事前helper 0x435C10による削除、別の保存経路、readerがEOF以降を無視するかは未検証。 / - Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、累計39/48静的VERIFIED。今回増加0。P0 20/21・P1 19/27・TODO8・VERIFY1。MASTER最新cp83、研究DONE9/34。旧EXE Gameplay golden PASS0。ゲーム再実装率は測定していない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_POST_GRAPH_EOF_SCOPE_AUDIT_20261011_1434.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_POST_GRAPH_EOF_SCOPE_AUDIT_20261011_1434.md`; actual SHA256 `AE1DCA71AD1C8E4F3F6B0DC44DD9F1D2C9E35279D05BDEB01D4E3038182005EA`, 2867 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 状態: CONFIRMED-SAVED-NATIVE（0x45E1E0局所return経路）/ VERIFY（calleeと上位callerの検証）。実ゲームNOT RUN。
  - 対象 VA 0x45E1E0 / T014 / 保存run runs/20261009T225741694Z/RUN_RESULT.json。Ghidra関数長1028 bytes、非連続4 ranges。
  - 保存済みGhidra pseudoと既存 native exe/T014_NORMAL_LOAD_PROBE.txtのVA 0x45E536..0x45E5EFを突合。
  - 0x45E53Eで外交reader 0x471AF0、0x45E54Cでworld-map/Spot-Path graph reader 0x435550を呼ぶ。両方とも戻り値に対する局所成否分岐は見えない。
  - 既存writer 0x460000はCreateFileA OPEN_ALWAYS(4)を使用する（別保存run 20261009T212627835Z / assembly ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394）。同一パス長→短上書きで末尾残存があり得る、という以前の条件付き論点に対し、reader core内の直接EOF検査は見当たらないと範囲を限定して補足。
  - ただし0x435550がファイル終端・余剰データを自ら検査するか、0x45E1E0の上位callerが保存後のstream位置を確認するかは未確認。『末尾ごみを必ず許容』『旧セーブの確定バグ』と断定しない。
  - 0x435550内の余剰byte処理 / 0x45E1E0上位callerのstream state判定 / 合法な短いセーブ再保存での実機golden（未実行）を独立課題として区分。原本EXE実行はしない。
- **Limitations and errata:** - 既存writer 0x460000はCreateFileA OPEN_ALWAYS(4)を使用する（別保存run 20261009T212627835Z / assembly ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394）。同一パス長→短上書きで末尾残存があり得る、という以前の条件付き論点に対し、reader core内の直接EOF検査は見当たらないと範囲を限定して補足。 / 今回の新規REA/Ghidra=0、VERIFIED増加0。Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12、計39/48。P0 20/21, P1 19/27, TODO8, VERIFY1。MASTER確認checkpoint83・研究DONE9/34。旧EXE golden PASS0。ゲーム再実装率は測定していない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_PREOPEN_SERIALIZER_SCOPE_AUDIT_20261011_0936.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_PREOPEN_SERIALIZER_SCOPE_AUDIT_20261011_0936.md`; actual SHA256 `67548ABB24CA731F761A55A5A5ECE2D6C579B60268E4F38921B196CEB2FA87CA`, 3114 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - # REA T014 — CreateFileA直前の0x435C10の役割境界（2026-10-11 09時台 JST）
  - 対象関数VA 0x460000、Task T014。保存run 20261009T212627835Z。
  - 0x460571: string writer 0x470830、0x460585: 0x471D20、0x460596: 0x435C10、0x4605CA: CreateFileAの順に保存Ghidra assemblyで確認。
  - A所有data/T014_GLOBAL_SAVE.mdの「normal save tail」節では0x471D20をDiplomacy runtime状態writer、0x435C10をworld-base+0x504のSpotElm/SpotPath/SpotEscapePath graph serializerと同定し、reader対応0x471AF0/0x435550を記録。
  - 従って0x435C10を「事前にファイルをDelete/Truncateしている候補」として最優先監査する根拠は弱い。主機能はstream graph直列化として独立資料でも整合。
  - 0x4605BE: disposition=4（OPEN_ALWAYS）、0x4605D4..DD: INVALID_HANDLE_VALUE時cleanup、0x460687: WriteFile、0x46068E: CloseHandleを保存assemblyで再照合。
  - 0x460000内の直APIフローはOPEN_ALWAYSを切詰め操作へ変更せず、WriteFileの戻り値/実書込長をこの局所経路では検査しない。
  - 優先1: caller 0x45F960（auto.savを含む）・0x53A100の同パス事前削除/rename/切詰めを、既存owner-A保存nativeで追加検証。
  - 優先2: 0x46060Aの間接virtual呼出の副作用、loaderのファイル長/余剰末尾処理、合法な旧EXE UI長→短save実測（PASS0、現時点で実行せず）。
- **Limitations and errata:** Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12。合計39/48 STATIC VERIFIED、今回新規0。P0 20/21、P1 19/27、TODO8、VERIFY1。 / 研究MASTER cp83 DONE9/34（IN_PROGRESS21/VERIFY4）、旧EXE Gameplay golden PASS0。ゲーム再実装率は測定していない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_SAVE_TOKEN_SIGNED_BYTE_LENGTH_AUDIT_20261012_0637.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_SAVE_TOKEN_SIGNED_BYTE_LENGTH_AUDIT_20261012_0637.md`; actual SHA256 `F0E548392D1064EC6CA77F1CFF4282E5686384D15758FB13C3AE6326122258FA`, 3570 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 研究: T014。関数VA `0x4705F0` (Wave5 VERIFIED、保存run `20261011T144115307Z`、length256 bytes)。
  - 1. `0x4705F0..0x470608`: 一時バッファ `0xB060F8` を0x400byteゼロ初期化。反復の `0x470610` は `0x470980` を呼び、戻値 `-1` のときは文字を格納しない。
  - 2. `0x47063D..0x470645`: 読んだbyteが0ならNUL終端として終了。0以外なら `CMP AL,0x20; JL` と `CMP AL,0x7F; JG` を経て `0x470653` に到達する。
  - 4. `0x470653`でカウンタを1増やし、`0x47065C CMP ESI,0xFF; JL` で反復する。最大255個の非NUL byteを読むと、`0x470669`で添字255へNUL書込し正常側へ進む（stream state異常の分岐が先に発火しない前提）。
  - 5. `0x470654 CMP ESI,0x3E8; JG` の1000-byte guardは、この通常ループの255-byte反復上限のもと到達不能。1000を「実際の入力許容上限」と解釈してはならない。
  - EOF(`0x470980=-1`)時のstream flag検査と例外が発生する可能性があるため、「EOFを空文字として許容」とは確定しない。
- **Limitations and errata:** - この局所ルーチンの許容範囲を全セーブ文字列・日本語ゲームテキスト一般へ無条件拡張しない。別APIの文字コード/タグ形式と混同禁止。 / - MASTER最新checkpoint83: 34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE gameplay golden PASS0。ゲーム再実装率は測定していない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_SHARED_470550_SCENARIO_XREF_AUDIT_20261012_1541.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_SHARED_470550_SCENARIO_XREF_AUDIT_20261012_1541.md`; actual SHA256 `3E74F5B3E8066BD834414CAD94E33D206D0B75F633BBDC5CA9434D52E8DE3DF8`, 3213 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - # REA T014 — 共通0x470550の追加scenario xref（2026-10-12 15時台 JST）
  - 前回メモでは0x470550のcallsiteは3件。今回、別の既存native資料で第4の異なるcallsiteを確認。
  - | 0x45E2D8 | T014_LOAD_CORE_DUMP.txt:62 | ADD ESP,0xC / temporary整理 |
  - | 0x45ECBB | T014_NORMAL_LOAD_PROBE.txt:619 | ADD ESP,0xC / 一時文字列解放判定 |
  - | 0x4CFC2A | T014_NORMAL_SAVE_CORE.txt:1296 | ADD ESP,0xC → 0x4CFC54でscenario literalをpush、0x4CFC66で0x4647D0をcall |
  - | **0x539364** | **T033_SCENARIO_LITERAL_XREFS.txt:2355**（T010_PHASE_XREFS.txt:815にも同site） | ADD ESP,0xC → 0x539385でscenario literalをpush、0x539397で0x4647D0をcall |
  - 第4地点の実命令：0x53935A LEA ECX,[EBP-0x29C] → 0x539364 CALL 0x470550 → 0x539369 ADD ESP,0xC → 0x539385 PUSH 0x62A72C ('scenario') → 0x539392 MOV EDX,0x62A724 → 0x539397 CALL 0x4647D0。
  - 0x4CFC2A地点も3個のstack pointerを準備し、共通helperからscenario property lookupへ進む。関数名を「T014専用save reader」と確定するのは不適切。
  - 4件は検索対象の保存済みexe資料にあるcallsite集合であり、0x470550の直接xrefs総数ではない。callee本体、ABI、戻り値、副作用、0x539364の高水準処理所属はVERIFY。
  - 0x4705F0 callers ID ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87 は別関数の証拠。0x470550に対する5-method VERIFIEDへ転用しない。
  - 0x58E480の本体契約とUnit marker 0x68B9D0のraw bytesは引き続きVERIFY（取得証拠IDなし）。
- **Limitations and errata:** - 0x58E480の本体契約とUnit marker 0x68B9D0のraw bytesは引き続きVERIFY（取得証拠IDなし）。 / - MASTERの最新既知値DONE9/34、IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0。ゲーム再実装率は測定していない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_SHARED_STREAMPOS_SENTINEL_AUDIT_20261011_1237.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_SHARED_STREAMPOS_SENTINEL_AUDIT_20261011_1237.md`; actual SHA256 `49E2CDCB1BA815146A483B29C13977913B47760DBCE0A9D95B0B030EB92612C1`, 2101 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 対象 T014、主VA `0x460000`、保存run `20261009T212627835Z`、target SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回再計算なし）。
  - 正常側`0x46060A`でストリームの間接関数を呼び、`0x46060C`/ `0x460613`で書込数を取得する。
  - 異常側`0x46061C`と`0x460622`はグローバルDWORD `0x6098B4`/ `0x6098B0`を読み、`0x460628`でEAX=0。
  - `0x460638`でEBXへEAXを加算し、`0x460684`でEBXをWriteFileへ渡す書込サイズ引数としてpushする。
  - 保存済み別native資料では`0x429695`のストリーム異常時も同2DWORDを結果値として使い、`0x462AAD`周辺で二値比較に使う例がある。
  - `0x6098B0`を固定`0xFFFFFFFF`と断定しない。間接stream関数・暗号化callee・WriteFile実戻値の副作用や実エラー時の挙動は未検証。
- **Limitations and errata:** - 同じ2DWORDは複数writer（通常/auto/global.sav）で使われ、**64bitストリーム位置の失敗sentinel候補**。正確な実値・初期化元・書換え条件はVERIFY。 / - `0x6098B0`を固定`0xFFFFFFFF`と断定しない。間接stream関数・暗号化callee・WriteFile実戻値の副作用や実エラー時の挙動は未検証。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_SPOTPATH_VTABLE_GATE_20261013.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_SPOTPATH_VTABLE_GATE_20261013.md`; actual SHA256 `C29E5BE5CAA516C1954974C1E7C693C18C8D75F1117C06F0612654F67C3064EB`, 10325 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - `exe/T014_SPOT_PATH_VFUNCS.txt`: SHA256 F95EF8CC0ECDFAE026F2B873C735C9B69F37689265F392CE1720110C6A77E23F、保存VA `0x5B0120..0x5B03DB`。
  - `exe/T014_SPOT_PAYLOAD_PROBE.txt`: SHA256 CE130D8432D239AE7E553C9D16F6F203D0130DBD547EFF83A447A5B91CEB9E1F、RTTI `SpotPath` vtable 0x6387F4／`SpotEscapePath` 0x638864。両typeの+0x54=`0x5B0120`、+0x58=`0x5B0250`。
  - `exe/T010_BATTLE_FRAME_ORDER.md`: SHA256 567D87BB18B753D8D2B908065B4884FE3BCC0D9D1767F5C43153BB120100A5AC、共有callee `0x43B5A0=raw AL0` の保存Cに基づく照合。これを別クラスに無条件一般化しない。
  - | Vtable slot | SpotPath 0x6387F4 | SpotEscapePath 0x638864 | 呼出側の直接効果 |
  - | +0x08 | `0x43B5A0` / AL0 | 同左 | 登録5B020D、解除5B02ECのTask条件はfalse |
  - | +0x34 | `0x4BBBD0` | 同左 | 解除5B02E1で呼出。callee作用は保存疑似C範囲に限定 |
  - | +0x44 | `0x43B5A0` / AL0 | 同左 | 解除5B037Cで呼出、返ALは検査しない |
  - | +0x48 | `0x43B5A0` / AL0 | 同左 | 登録5B0226・解除5B0368のRender条件はfalse |
  - | +0x54 | `0x5B0120` | 同左 | 登録処理の実体 |
  - | +0x58 | `0x5B0250` | 同左 | 解除処理の実体 |
  - `0x5B0120`: `0x5B020D`でvtable+8のAL0→`0x5B020F JE 0x5B021D`、従って条件付き`0x4C2240` Task登録呼出を**実行しない**。`0x5B0226`でvtable+48のAL0→`0x5B0228 JE 0x5B0234`、従って`0x4C3DC0` Render登録も**実行しない**。その後`0x5B0239`の`0x4BC920`空間索引登録は引き続き到達する（下位の成功・重複方針はVERIFY）。
  - `0x5B0250`: +34呼出後、`0x5B02EA`の+8がAL0→`0x5B02EE JE 0x5B035F`でTask active tombstone/待機配列stable eraseへの局所経路を丸ごとskip。+48もAL0→`0x5B036A JE 0x5B0375`で`0x4C3E40` Renderリスト解除をskip。ただし+44呼出後、`0x5B039C`の`0x4BC3C0`による空間セル検索と`0x5B03C5..0x5B03D5`の最初一致tail-swap除去は残る（cell不在・対象不在ならreturn）。
  - `0x5B0123`でbyte[this+0x88]を検査。非0かつ第一stack arg low byte=0なら`0x5B0131 JE 0x5B0241`で**全登録処理を早期return**する。
  - 非0でも第一stack arg low byte!=0ならこの早期returnを通らない。backlinkの重複検査はある一方、空間登録`0x4BC920`にはcallが到達するため、下位関数のdedup保証なしに「必ず一度のみ」と断定しない。
  - `0x5B0250`には同じ+0x88の入口ガードが見えない。再入・二重呼出への正規上位gateはVERIFYで、解除を二重実行しても常に安全と仮定しない。
  - `0x5AFB30`の本体命令は保存exe資料の今回検索で未発見（確認callsite: `0x5AFAD5`, `0x5B05B3`, `0x5B05C8`）。この関数と`0x5B0120`/`0x5B0250`の直接caller-callee関係は未確定。既存callee情報は `0x46F4C0`へのxrefsを示すだけである。未知calleeの返値や実効果を注入しない。
  - 次の重点は `0x4BC920`の空間登録時重複方針と、`0x5AFB30`の既存の呼出証拠・callee境界。既往拒否で未承認の本文取得は別手段で反復しない。
  - ## 2026-10-13 08時台 — 空間索引登録 0x4BC920 / セル取得 0x4BC3C0（REA-T014-SPATIAL-20261013-0834）
- **Limitations and errata:** - [COUNT] `0x4BC9A0 MOV EAX,[EBP+8]; 0x4BC9A3 INC EAX; 0x4BC9A4 MOV [EBP+8],EAX; 0x4BC9A7 MOV [EDI+0x54],EAX`。manager単位の32bit登録カウンタを1増やし、同値をobject+54へ格納する。これをゲーム内時間・優先順位・グローバルIDと呼ばない（実consumer VERIFY）。連続登録時はoverwriteされる。 / - [NEXT] 許可済み証拠で 4BC3C0 tree cell新規登録と4C12F0 vector grow／0x4BC9C0解除の重複1件だけの意味差を整合。上位5B0120のflag=1再登録で実際に二重到達するcaller条件、空間grid外の実到達・heap成功はVERIFY。新Ghidra一式を未取得なら本関数をVERIFIEDへ昇格しない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_STREAM_FAIL_STATE_TO_WRITE_AUDIT_20261011_1036.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_STREAM_FAIL_STATE_TO_WRITE_AUDIT_20261011_1036.md`; actual SHA256 `8259B61D3A4551F04ED16FDBE19B599B56A897D0E16D3096D014B4CCB2D3FDC8`, 3151 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 状態: CONFIRMED-SAVED-ASSEMBLY（関数0x460000の局所branchのみ）。stream failure時の実際のI/OとgameplayはVERIFY。新規Ghidra実行0。
  - VA: 0x460000 / Task T014 / 保存runでinfo・pseudo・assembly・callers・calleesの5結果がVERIFIED。
  - 0x4605D4..5DD: CreateFileAが-1なら0x4606ADへ直行（既知）。それ以外でstream状態検査へ入る。
  - 0x4605E3..5EF: stream系object vptr offsetからfield indexを得て、stack状態byteに0x06 maskでTEST。非0なら0x46061Cへ。
  - mask=0の分岐は0x4605F1..60Aで仮想関数offset+0x28を呼ぶ（引数0,0,1,2）。0x46060Cと0x460613が返却された長さ/位置候補をEAX・EBXへ格納し0x460638に合流。
  - mask非0の分岐0x46061C..631ではglobal[0x6098B4]およびglobal[0x6098B0]を使用し、EAX=0にする。0x460638でEBX+=EAX。
  - 両分岐は0x46063A..65Cの変換helper 0x42A340→暗号化helper 0x427040へ合流し、0x46067D..687のWriteFile到達経路が残る。stream状態mask非0だけを理由とする、この局所での即時cleanup分岐はない。
  - 0x46068D..68E CloseHandle、0x460694以降はbuffer容量条件（既知）。WriteFile戻り値の局所チェックは見えない。
  - global[0x6098B0/0x6098B4]の静的値・意味、mask0x06の正確なstd::ios状態対応、仮想関数戻りの妥当性と例外経路は未確定。pseudoの型推論は警告付きのため、fallback書込byte数や破損発生を決めつけない。
  - 呼出元 0x45F960 / 0x53A100 の事前削除・事後確認は未解析。旧EXE gameplay goldenはNOT RUN、原作確定バグとはしない。
- **Limitations and errata:** - 『stream状態異常ならwriterは一切WriteFileしない』という仮定を再実装に埋め込まない。正常・異常streamのbuffer生成・byte countと上位save完了通知は独立VERIFY。 / - Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12。重点累計39/48 STATIC VERIFIED、今回増加0、P0 20/21・P1 19/27、TODO8/VERIFY1。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_STREAM_WRITE_BYTECOUNT_ORIGIN_AUDIT_20261011_1136.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_STREAM_WRITE_BYTECOUNT_ORIGIN_AUDIT_20261011_1136.md`; actual SHA256 `C5073EF037490539E4918C171D0D3A0430750FF9D49DD62F1038D3882F5344B0`, 3025 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - 状態: CONFIRMED-SAVED-ASSEMBLY（0x460000の局所データフロー）。実行時値・上位エラー制御・保存結果はVERIFY。新規Ghidra/REA実行0。
  - 対象: 既存run 20261009T212627835Z / VA 0x460000 / T014 / 保存記録source SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回再hashなし。
  - 0x4605EA..EFの(TEST state & 0x06)が正常なら、0x4605F1..60Aでvtable+0x28を呼び、0x46060CでEAX=[ESP+0xC4]、0x460613でEBX=[ESP+0xBC]を取得する。
  - 異常なら0x46061CでECX=[0x6098B4]、0x460622でEBX=[0x6098B0]、0x460628でEAX=0。0x46062AでECXを[ESP+0xC0]へ、0x460631で0を[ESP+0xC8]へ格納する。正常側の仮想関数は通らない。
  - 0x460638 ADD EBX,EAXで両分岐は合流。すなわちbytecount候補は正常側が[ESP+0xBC]+[ESP+0xC4]、異常側が[0x6098B0]+0（32-bit加算）となる。
  - 0x460645の0x42A340と0x46065Cの0x427040を経て、0x460684 PUSH EBX / 0x460687 CALL [0x609080]。import解決済みWriteFileのnNumberOfBytesToWriteにそのEBXを渡す。書込bufferは0x460661..676のinline/heap選択結果、file handleはCreateFileA戻りEBP。
  - pseudoは異常側に0xffffffff sentinelを表示するが、assemblyはglobalメモリからのロードである。実行時のglobal値が常に-1だと断定しない。特に『異常時に4GiB近いbytecountを実際に要求する』との断定はしない。
  - WriteFileの直後0x46068D PUSH EBP / 0x46068E CloseHandle。戻り値やbytesWrittenを当該局所経路で比較する命令は見えない。
  - [VERIFY] globals 0x6098B0/0x6098B4の定義・初期値とruntime書換え元、0x42A340/0x427040の異常状態での例外・副作用。
  - [VERIFY] bytecount候補と暗号化後buffer lengthの一致、partial write/stream fail時の上位returnやUI通知（caller 0x45F960/0x53A100）。
- **Limitations and errata:** - [VERIFY] bytecount候補と暗号化後buffer lengthの一致、partial write/stream fail時の上位returnやUI通知（caller 0x45F960/0x53A100）。 / Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、重点累計39/48 STATIC VERIFIED・今回追加0（P0 20/21/P1 19/27、TODO8/VERIFY1）。研究MASTER最新cp83 DONE9/34。ゲーム再実装率は測定していない。
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

### REA_T014_TEMP_OBJECT_LIFETIME_AUDIT_20261011_0435.md

- **Source relative path:** `rea_lab/decomp_task/REA_T014_TEMP_OBJECT_LIFETIME_AUDIT_20261011_0435.md`; actual SHA256 `39064BEC026B3D909008C50065B270A2912EAF3DD7EC060B11CC3B2A278E221E`, 1747 bytes.
- **Declared ID:** not present / UNKEYED_SOURCE. 
- **Allowed original owner x86/ABI/save/event findings:**
  - Task: T014、入口VA `0x45E1E0`、保存run `20261009T225741694Z`。指定target SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（再計算なし）。
  - 構築: `0x45E25A → 0x582AA0`、`0x45E26F → 0x5971A0`、`0x45E284 → 0x590560`。
  - 本体事前処理: `0x45E2D8 → 0x470550`。これを第7保存データ群とはまだ解釈しない。
  - 既知4group読み込み後、`0x45E53E → 0x471AF0`（外交）、`0x45E54C → 0x435550`（Spot/Path graph）。
  - 後始末: `0x45E58B → 0x45DF70`、`0x45E5A0 → 0x432DF0`、`0x45E5B4 → 0x4591F0`。
- **Limitations and errata:** ## VERIFY
- **Status:** PRESERVED_UNKEYED_SOURCE / VERIFY; original Golden PASS 0, READY 0.

## Curator-only formal integration

These old T013/T014/Unit/Save/Wave records are searchable by source SHA. Assign a distinct research ID only after checking full source native VA/call evidence and competing owner reports. No prohibited VA/denied Wave6 material has been reacquired or posted. No unrelated Work/user PC files, game originals, private raw logs or current develop modified. New formal VERIFIED=0; Golden PASS=0; READY=0.
