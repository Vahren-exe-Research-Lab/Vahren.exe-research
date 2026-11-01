# REA early legacy research source audit B — original pre-ID T013/T014/unit/event/Wave notes

**Stage: SOURCE_PRESERVED_UNKEYED or EXISTING_ID_CORRECTION, NOT CURATED.** These 13 earlier independent REA owner Markdown files were never identified as newly decompiled functions by this recovery. Byte SHA256 of each original source was recomputed on the authorized research PC on 2026-11-02 JST; excerpts below are safe historical native/E8/ABI/semantic notes, not a formal Ghidra 5-method replay. They may duplicate a later source and need curator ID/VA/source-SHA/errata reconciliation. Files carrying a refused Wave6/refusal payload are represented by filename/SHA/BLOCKED metadata only, without denied target/results. Original Golden PASS 0 / READY 0, newly VERIFIED 0. No raw data, privacy-sensitive paths or unreviewed evidence JSON published.

### REA_T013_ALIAS_SAFE_VECTOR_APPEND_20261011_1834.md

- **Source key:** `rea_lab/decomp_task/REA_T013_ALIAS_SAFE_VECTOR_APPEND_20261011_1834.md`; measured source SHA256 `5E6A6CCD2E57A0FE4F0153DAFEA4FAD5FA74C6C3F09DB424DA824CBEF521F254`, 2759 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 対象：迫真戦記 ver0.67／T013（戦闘AI）、関数VA `0x5154F0`・`0x5155C0`・`0x5158A0`・`0x514F10`。
  - 親関数`0x57B870`のassembly evidence ID：`ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`。
  - | `0x5154F0` | 動的配列の末尾位置を取得する追加処理の入口 |
  - | `0x5154FA` | コピー元が配列内部にあるかを確認 |
  - | `0x515508` | 配列内のコピー元であれば、その要素位置を計算 |
  - | `0x515523` | 必要に応じ容量拡張を実行 |
  - | `0x515534` | 容量拡張後にコピー元位置を再計算 |
  - | `0x51553E` | 24バイトの候補レコードを追加先へコピー |
  - | `0x515566` | 要素末尾を24バイト進める |
  - `0x514F10`は既存の作業用候補がある場合、補助処理`0x5158A0`を呼ぶ経路を持つ。
  - その後`0x514F62`付近で作業用配列の末尾を先頭位置へ戻す。候補を**論理的に空**にすることと、確保済み領域の解放とは区別する。
  - `0x5154F0`の追加処理自体では、候補順位決定や重複候補の除外は確認されていない。別処理の解析が必要。
  - 配列の詳細な容量成長規則、`0x5155C0`/`0x515640`のメモリ再確保、副作用、例外・割当失敗経路はVERIFY。
  - `0x57CFA0`・`0x57CFD0`での候補の利用と優先順位を、保存済み証拠から追加確認する。
  - `0x5154F0`などの子関数についてinfo/pseudo/assembly/callers/callees・entry・source SHA・evidence IDの5点確認が揃うまでVERIFIEDにしない。
- **Source limitations:** - 状態：`STATIC-AUDIT / VERIFY`。新規REA/Ghidra実行なし。子関数のGhidra5点証拠未取得につき、新規 `VERIFIED` 昇格なし。 / - 配列の詳細な容量成長規則、`0x5155C0`/`0x515640`のメモリ再確保、副作用、例外・割当失敗経路はVERIFY。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T013_CLEAR_BEFORE_REPLACE_AUDIT_20261012_0335.md

- **Source key:** `rea_lab/decomp_task/REA_T013_CLEAR_BEFORE_REPLACE_AUDIT_20261012_0335.md`; measured source SHA256 `0D454D83A9A7C9C7D17EAA7C29D3E40732F15113A7B1FB337027A058D3CDEDB4`, 3621 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 1. 0x57CFA0の0x57CFA0..0x57CFB5: ESIが保持するvectorのbegin=[ESI]とend=[ESI+4]を読み、非空ならECX=end、EDX=end、EAX=beginで0x5158A0を呼ぶ。0x5158A0は最初のCMP ECX,EDXが等しいので即RET、EAX=beginは不変。呼出元は戻ったEAXを[ESI+4]へ格納する。すなわちこの呼び方は一般range copyではなく、vectorの論理endをbeginに戻す「clear」動作。
  - 3. 親0x57B870の0x57BA46..0x57BA58では0x514F10が返すbegin/endを0x57CFA0へ渡す経路を確認。別経路0x57BA6C..0x57BA97でも同一の0x5158A0（ECX=EDX=endなので即RET）→vector.end=begin→0x57CFD0を明示的に実行する。したがって少なくとも二つの更新枝で古い候補rangeを残すappendではなくclear-before-range-insertを確認。
  - 4. ABI注意: 0x5158A0のGhidra pseudoはvoidだがEAXが戻り値として実使用される。0x57CFD0のpseudoは4引数相当に見えるが実assemblyは5 PUSH / RET 0x14、今回も疑似関数宣言の自動流用は禁止。候補の意味/戦闘AI選択順序は未確定。
  - 0x57CFA0 assembly ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789 / pseudo ev_af8c7dc6fe7871eb38bb0c219d8494ae7fa96d2e11c2b198fda926e5c813fb61。
  - 0x5158A0 assembly ev_d4d1952d5b5e5da305467de47caec6d2ce02aadfbc2cd5475a12f7f41e291e80 / pseudo ev_256892f9bf4a31e4d302c31129c7094cad30e15db60647104f40fe356ba63239。
  - 0x57B870 assembly ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c / pseudo ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc。
  - 0x57CFD0 assembly ev_08eb96aea33c3dbd4a1ae58fa08f3b20bfb31b8ccea4539a5bc0044cbb4887b5 / info ev_f85bc7f40298b5ec205b3f4f8c0365f48b2fa30e5e8afc42691ec110f5c23efa。
- **Source limitations:** Verify native instruction windows, current V9 and later owner corrections before adoption.
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T013_DUAL_VECTOR_GROWTH_SCOPE_20261012_0435.md

- **Source key:** `rea_lab/decomp_task/REA_T013_DUAL_VECTOR_GROWTH_SCOPE_20261012_0435.md`; measured source SHA256 `DD8AAA4FBC0248D5701866DB9B9FD60A44F4A2841F31C17B48FA00ACA145EEA6`, 3520 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 1. `0x5154F0` は共有作業用vectorの global `0xAC09EC` (begin), `0xAC09F0` (end), `0xAC09F4` (capacity) を参照し、容量満杯時に `0x5155C0` を呼ぶ（0x5154F0 assembly 0x5154F0..0x515523）。`0x5155C0` の疑似コードは同global vectorの `new_capacity=max(old_capacity+floor(old_capacity/2), size+1)` を示す（巨大数ガード別途）。この **約1.5倍成長規則は現時点ではglobal scratchに限定**。
  - 2. `0x57B870` の通常support側は、Unit `+0x1E584` を別のvector先頭アドレスとして `0x57CFD0` へ引渡す（0x57BA72..0x57BA97）。Unit-localのbegin/end/capacity（+1E584/+1E588/+1E58C）と、global 0xAC09EC/F0/F4を混同しない。
  - 4. `0x5155C0` のsaved callersは `0x5154F0` の1関数、`0x57CFD0` のsaved callees一覧は7件。これはGhidraが解決した静的呼出関係の範囲内の観測であり、関数ポインタ等まで完全網羅とみなさない。
  - `0x5154F0` assembly `ev_6a53e867e218f8905561e0687a0340e1dafe224e61cc7d465b0047e7b21c3d64` / callers `ev_8ce283bf9f936114ed4749b1907814810be35fb077af15de779d65256288d320`。
  - `0x5155C0` pseudo `ev_e0069ba6edcf643c2dc695615ff75d8db9c7f580aa072947eefff66fe9bddd00` / callers `ev_8ce57a11472ca4f7210743bb6347db6942fe6f05f256522503722b53d44ff2ce`。
  - `0x57B870` assembly `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`。
  - `0x57CFD0` pseudo `ev_fa33cc83cda4f064bed5262e5fa063359e2fbb86a07b22329757999821da3725` / callees `ev_2dc9297fab51c57cfc686ea99152528224402c6e4b39256935a1d5594e621958`。
- **Source limitations:** Verify native instruction windows, current V9 and later owner corrections before adoption.
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T013_EMPTY_RANGE_REPLACE_ABI_AUDIT_20261012_0536.md

- **Source key:** `rea_lab/decomp_task/REA_T013_EMPTY_RANGE_REPLACE_ABI_AUDIT_20261012_0536.md`; measured source SHA256 `2C42027EB53EC86EE6DEBEDD9F93A2E2C327752359943985F22E1EC1B3B973EC`, 3637 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 1. 0x57CFA0では begin!=end 時、EAX=begin、ECX=EDX=end で0x5158A0を呼び、戻りEAXをvector.endへ書く（0x57CFA0..0x57CFB5）。これは既存要素の**論理的clear**。元storageのfreeや要素破棄はこの操作からは確定しない。
  - 2. 0x57CFA0はその直後に0x57CFD0へ5値をPUSHして呼ぶ（0x57CFC2..C7）。空入力（src_begin==src_end）なら0x57CFD0の0x57CFFB..0x57D012は0レコードを算出し、JZ 0x57D15Eへ直接進む。保存assembly上、この早期分岐ではvector.begin/end/capへの書込もallocator呼出も行わない。
  - 3. 従って「既存候補が非空／入力候補が空」で0x57CFA0を通過すると、論理end=beginのまま、0x57CFD0は0件挿入で戻る。これは空の新候補範囲に置換された状態。古い候補を維持するappend型実装は非互換になる可能性がある。
  - 5. ABI補足: 0x57CFA0で5 PUSH、0x57CFD0でRET 0x14を再確認。今回照合した非連続2区画の保存assemblyでは[EBP+0x08..0x14]参照はあるが[EBP+0x18]参照は見えない。5番目を必須意味引数と断定せず、疑似コードの4引数形式も確定宣言とはしない。
  - 0x57CFA0/T013 assembly: ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789。
  - 0x57CFD0/T013 assembly: ev_08eb96aea33c3dbd4a1ae58fa08f3b20bfb31b8ccea4539a5bc0044cbb4887b5。
  - 0x57CFD0/T013 pseudo: ev_fa33cc83cda4f064bed5262e5fa063359e2fbb86a07b22329757999821da3725。
  - 0x5158A0/T013 assembly: ev_d4d1952d5b5e5da305467de47caec6d2ce02aadfbc2cd5475a12f7f41e291e80（既存監査での空range即RET根拠）。
- **Source limitations:** 4. 既存候補も空ならclear枝をskipし、挿入0件もno-op。動的意味（容量維持、旧レコード破棄、並列状態・実ゲーム可視性）は引き続きVERIFY。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T013_FULL_REFRESH_POSTGATES_20261011_0638.md

- **Source key:** `rea_lab/decomp_task/REA_T013_FULL_REFRESH_POSTGATES_20261011_0638.md`; measured source SHA256 `8E3A5787F80BD42B0FA781B160CC5E79DF0B6A2B93EF17B8CAD31C13AA083D25`, 5510 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 保存run: 20261009T225741694Z。対象関数入口: 0x57B870（T013、関連T012）。今回の新規REA/Ghidra実行0。
  - 0x57BA9C..0x57BAB4: Unit+0x188と+0x18Cのsigned比較後、大きい方を局所値へ保持。
  - 0x57BAB4..0x57BACE: FILD / FCOMP Unit+0x1E578 / FNSTSW / TEST AH,1。max(+188,+18C)>=距離（NaNやFPU例外は別VERIFY）かつUnit+0x1A8==0なら、+0x1A8へ1を書く。既に非0の場合は上書きなし。
  - 0x57BAD8..0x57BB21: Unit+0xBC<0の時のみ+0xDCとglobal 0x65BD78からx87値を作り、0x5B6ED0→0x5D1B80の結果をUnit+0x90から減算、符号付き負なら0へclamp。その後0x577100を呼ぶ。
  - 0x57BB26..0x57BB8F: Unit+0x186A0>=8、byte+0x8C==0、byte+0x1F8!=0、+0x18684!=2、virtual[+0x1D4]+0x18の戻り値!=5、+0x186B4!=0、+0x186C0==+0x186C8==0x80000008 の全条件を順番に満たした時だけ 0x5767B0(args: two dwords from [Unit+0x186B0]+4,0,1)を呼ぶ。
  - +0x1A8の意味、+0x90のゲーム上のHP確定、+0xBCの負値意味、0x577100/0x5767B0副作用は別のowner native証拠・実機観測までVERIFY。
  - +0x186A0の条件はsigned J(L)で、0x80000008は二重sentinelの32bitパターン。magic数字をゲーム仕様名へ自動変換しない。
  - 根拠: `runs/20261009T225741694Z/57B870_procedure_assembly.json`。関数VA=0x57B870、確定入口/body=0x57B870..0x57BB9B。T013/T012、REA保存証拠のread-only検査（新規逆コンパイルなし）。
  - 0x57B87F比較: signed Unit+0x1E534 < global[0x65BCAC]なら早期経路であり、この関数による直接CRT rand消費は0回。条件を満たさない場合のfull-refreshに進む。
  - 0x57B8FE: full-refresh入口で`0x5B6EAB`を無条件直接CALL（1回）。同結果から0x5D1B80を使った変換後、0x57B92AでUnit+0x1E534を更新する。x87実機丸めはVERIFY。
  - 0x57B940: Unit+0x1E570がnull、かつsigned Unit+0xC8<0の枝に限り追加で`0x5B6EAB`を直接CALL（1回）。
  - 0x57BA10: Unit byte+0x137!=0、かつsigned Unit+0xC8<0の枝に限り追加で`0x5B6EAB`を直接CALL（1回）。直前の候補選択・null判定と同一条件へまとめない。
  - Ghidra callers: 0x57B870←0x545740,0x57AA00,0x57E4E0。57E4E0が57B870を呼び得るのは保存済みB契約の0x57E5AD段階と整合。別の0x40ED80呼出元には0x57E1D0があるが、0x57E4E0の直接caller登録は無い。両経路のRNGを混同しない。
  - Work連携: 現在の通常AI継続0x57AEBC→0x57E4E0の後段でfull-refresh呼出に到達した場合、ここで消費したdrawとUnit+1E534等の書込みをstage単位で保持し、57AEBCからやり直さない。既存Workコードはread-onlyであり編集しない。
- **Source limitations:** - 0x57B8FE: full-refresh入口で`0x5B6EAB`を無条件直接CALL（1回）。同結果から0x5D1B80を使った変換後、0x57B92AでUnit+0x1E534を更新する。x87実機丸めはVERIFY。 / - 0x57BA10: Unit byte+0x137!=0、かつsigned Unit+0xC8<0の枝に限り追加で`0x5B6EAB`を直接CALL（1回）。直前の候補選択・null判定と同一条件へまとめない。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T013_PRIMARY_SUPPORT_FILTERS_20261011_1733.md

- **Source key:** `rea_lab/decomp_task/REA_T013_PRIMARY_SUPPORT_FILTERS_20261011_1733.md`; measured source SHA256 `1CFDF9B2D54010AD1625018F5B8EED9BF7241372410BC9F3EFDE4D46293062E1`, 2495 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - Ghidra（親関数0x57B870） info `ev_c4fcdda0f9486944ccdcfe1354a6d2e37f2b68761dfd2e47b7df9a11cd367612`；pseudo `ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc`。
  - ※0x514D60・0x514F10自身には5点REA evidence IDが未取得。これらをVERIFIED関数へ昇格してはならない。
  - ## 0x514D60 — 主探索（T013、候補レコード返却）
  - 0x514D71..0x514D9E: 引数UnitのXYを取得し、選択された候補コンテナ +0x48/+0x4C に含まれる4byteポインタ列を走査。
  - 0x514DB1..0x514DC2: 候補Unit+0x1867C≠0ならskip。候補ポインタ==引数Unit（self）ならskip。
  - 0x514DC4..0x514DF5: Unit+0x1C0=0ならstealth roll無し。非0ならCRT rand15→FPU 0..100相当→0x5D1B80変換を行い、Unit+0x1C0>rollでその候補をskip。丸め・境界分布はVERIFY。
  - 0x514DF5..0x514E42: XY差を32bit IMUL/ADDして0x5E3B70へ渡し、最短候補を更新する局所FPU比較。signed overflow / x87は保持すべき未確定境界。
  - 0x514E48..0x514E75: その時点の単一選択候補の+0x18Cと保持距離を比較し、半径不足側・未選択側は第2走査へ。全候補の+0x18Cを先に除外する方式とは異なる。
  - 0x514E75..0x514EF2: 第2候補列+0x58/+0x5Cを走査。+0x1867C!=0とselfはskip、XY距離比較を行うが、このループには直接の+0x1C0ステルスrandゲートはない。
  - 0x514EF2..0x514F0B: 選択済ポインタ/距離の組を呼出側レコードへ書く。第1/第2列のゲーム上の名称・選択順位全体はVERIFY。
- **Source limitations:** - 0x514DC4..0x514DF5: Unit+0x1C0=0ならstealth roll無し。非0ならCRT rand15→FPU 0..100相当→0x5D1B80変換を行い、Unit+0x1C0>rollでその候補をskip。丸め・境界分布はVERIFY。 / - 0x514EF2..0x514F0B: 選択済ポインタ/距離の組を呼出側レコードへ書く。第1/第2列のゲーム上の名称・選択順位全体はVERIFY。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T013_SUPPORT_CACHE_GUARD_MATRIX_20261011_0037.md

- **Source key:** `rea_lab/decomp_task/REA_T013_SUPPORT_CACHE_GUARD_MATRIX_20261011_0037.md`; measured source SHA256 `85DF534C15616512AC2E182C69046F71B5D4439788E87BF2A611CA886EAE3BED`, 2986 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 判定: CONFIRMED-SAVED-ASSEMBLY（0x57B870関数内の制御フロー限定）。他関数によるcache無効化、実ゲームへの効果はVERIFY。
  - 対象: ver0.67承認済みコピー、保存run `20261009T225741694Z`、T013、関数 `0x57B870`（812 byte）。本回のEXE hash再測定・新規REA/Ghidra実行なし。
  - `0x57B87F`で`Unit+0x1E534 < unit_search_bdr`なら`0x57B88F/0x57B8D4..DB`の早期return。support builder/mergeは到達せず、この関数内でsupport vector `Unit+0x1E584/588/58C`を直接更新しない。
  - 閾値到達時はtarget選択またはcached target距離再計算の後、`0x57B9F4 CMP byte [Unit+0x137],0`→`0x57BA01 JZ 0x57BA9C`。capabilityが0ならbuilderとmergeを回避し、この関数内ではsupport vectorを明示clearしない。
  - capability非0・混乱判定成功では`0x57BA41 CALL 0x514F10`→`0x57BA53 CALL 0x57CFA0`→`0x57BA58 JMP 0x57BA9C`（`0x5158A0`と`0x57CFD0`は経由しない）。
  - capability非0・通常側では`0x57BA62 CALL 0x514F10`→`0x57BA7E` begin/end照合。非空の場合のみ`0x57BA84 CALL 0x5158A0`の結果を`0x57BA89`でendへ書込。続いて`0x57BA97 CALL 0x57CFD0`。
  - どの分岐でも`0x57BA9C`以降の距離条件ラッチ・負値statusによるHP変化・特殊action gateはsupport vector更新とは独立に後続評価される（ただしcounter未達枝はreturn済み）。
  - 過去フレームの候補が現実に残るか、後続evaluatorがそれを使用できるかは外部writer/consumerとlifecycle未追跡のためVERIFY。`0x5158A0/0x57CFA0/0x57CFD0`の内部副作用も未確定。
  - テスト候補（DESIGNED/NOT RUN）: counter未達/到達 × `+0x137` 0/1 × vector空/非空 × confusion成否、各分岐で3 helper呼数と`+0x1E584/588/58C`前後値・可視support行動を別々にtrace。
- **Source limitations:** - `support capability=0`と`support vector length=0`を同義にしない。0は本関数におけるmergeの非実行条件であり、vector消去の証拠ではない。 / - 過去フレームの候補が現実に残るか、後続evaluatorがそれを使用できるかは外部writer/consumerとlifecycle未追跡のためVERIFY。`0x5158A0/0x57CFA0/0x57CFD0`の内部副作用も未確定。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T013_SUPPORT_VECTOR_REFRESH_GUARD_20261010_2336.md

- **Source key:** `rea_lab/decomp_task/REA_T013_SUPPORT_VECTOR_REFRESH_GUARD_20261010_2336.md`; measured source SHA256 `B0217F473E83D3CF95DF829F3C37972B2E329987116C60ABBA52694E2805D782`, 2908 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 状態: CONFIRMED-SAVED-ASSEMBLY（関数内の条件・CALL・書込のみ）。0x5158A0/0x57CFA0/0x57CFD0の内部効果、実機動作はVERIFY。
  - 対象関数: 0x57B870（T013、run 20261009T225741694Z、812 byte、34 basic blocks）。
  - 0x57B9F4 CMP byte [Unit+0x137],0 → 0x57BA01のJZではsecondary候補経路をまるごと飛ばし0x57BA9Cへ。
  - 0x57BA07..0x57BA34ではUnit+0xC8<0なら独立CRT乱数と境界比較を行い、一方の選択時だけ0x57BA3Fの0x514F10を経て0x57BA53 CALL 0x57CFA0→0x57BA58 JMP 0x57BA9C。この経路では下記0x5158A0や0x57CFD0を呼ばない。
  - 他方の0x57BA5A..0x57BA67でも0x514F10を呼ぶが、後続0x57BA6C MOV ECX,[Unit+0x1E588] / 0x57BA72 MOV EAX,[Unit+0x1E584]→0x57BA7E CMP EAX,ECXで既存vector begin/end相当を比較。
  - 不一致なら0x57BA82 MOV EDX,ECX→0x57BA84 CALL 0x5158A0→0x57BA89 MOV [Unit+0x1E588],EAX。一致ならこのcall/writeをskipし0x57BA8Cへ。
  - 共通で0x57BA97 CALL 0x57CFD0（既存vector位置・候補範囲・local数値引数）後、0x57BA9Cへ。したがって0x57CFA0と0x57CFD0は同じ経路で無条件に連続実行されない。
  - [CONFIRMED] secondary候補の更新には少なくとも2経路があり、通常経路だけに「begin!=endなら0x5158A0で新endを設定」という前処理がある。単一の常時vectorクリアとして実装してはいけない。
  - [VERIFY] 0x5158A0の内部効果（縮小/再配置/終端整列等）は未取得。vector内容、所有権、既存要素破棄を断定しない。confusion判定と0x514F10内部の副作用も未知。
  - [TEST DESIGNED/NOT RUN] full refresh、Unit+0x137={0,1}、Unit+0xC8={負,非負}、乱数比較={成否}、vector begin=end/!=endで、3 calleeの呼数・+0x1E588・可視ターゲット・乱数系列を独立trace。
  - 本監査は保存済み5方法VERIFIEDの0x57B870に含まれる新しい分岐読み取りであり、新しい関数のVERIFIED昇格ではない。
- **Source limitations:** - 共通で0x57BA97 CALL 0x57CFD0（既存vector位置・候補範囲・local数値引数）後、0x57BA9Cへ。したがって0x57CFA0と0x57CFD0は同じ経路で無条件に連続実行されない。 / - [VERIFY] 0x5158A0の内部効果（縮小/再配置/終端整列等）は未取得。vector内容、所有権、既存要素破棄を断定しない。confusion判定と0x514F10内部の副作用も未知。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T014_CALLERS_GLOBAL_SCRATCH_SCOPE_20261012_0738.md

- **Source key:** `rea_lab/decomp_task/REA_T014_CALLERS_GLOBAL_SCRATCH_SCOPE_20261012_0738.md`; measured source SHA256 `FFCD39032C1A1C2658B0059650059EFA6311293ABA62CF1B5D8BFF3E0F37FE1D`, 4267 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - Scope: T014 0x4705F0 string-token helper; T014 0x470700 numeric helper; preserved Wave5 results.
  - Ghidra 0x4705F0 procedure_callers reports **13 distinct resolved calling functions**; evidence ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87.
  - 0x598980 (Spot runtime reader) invokes 0x4705F0 for initial fields and repeated record keys; saved pseudo ev_0acff01a3a0b32c2efc27bc4c2c113a5990bee48a71916922824806d419968ad.
  - 0x5964C0 (Power runtime reader) invokes 0x4705F0 for header/field tokens and repeated variable-length keys; saved pseudo ev_9608d350a99e5ba1453392474e951d01a83321124085c78de8ef29ffc8ea96d9.
  - 0x435550 (Spot graph reader) invokes 0x4705F0 before constant-tag comparisons and within successive graph record loops; saved pseudo ev_7a9e58e9b0b538edf453aaf98e7755f5ebedda9102d81657c549716351eec905.
  - 0x471AF0 (diplomacy runtime reader) invokes 0x4705F0 for record identifiers before resolution into known runtime entities; saved pseudo ev_1e776fb470e6e934d7fffa736600daa070a5e3e009552f7951f653edbc00f871.
  - 0x4705F0 assembly ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d: zeroes global 0xB060F8 length 0x400 at 0x4705F4..0x470608, reads bytes into this same global, then passes pointer+actual NUL-terminated length to 0x402800 at 0x470680..0x470686. Scratch is overwritten by the next call; do not expose it as a stable returned pointer.
  - 0x470700 assembly ev_f7ed3af4df1cdf7b14d9208f3d4aa735267b9ab022ee7d6b3860c4521bbb95cf uses distinct global DWORD 0xB060F0 (eight bytes before string scratch) through 0x42E700 and copies DWORD into caller destination at 0x470754..0x47075D.
- **Source limitations:** - The 13 caller taxonomy is incomplete; additional caller-specific label semantics and downstream overlength behavior remain VERIFY. No static evidence promoted into gameplay golden. / - Latest MASTER checkpoint83: DONE9/34 (IN_PROGRESS21/VERIFY4); old-EXE actual gameplay golden PASS0; game reimplementation percentage NOT MEASURED.
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T014_DUAL_MODE_CALLSITE_CONFIRMED_20261012_1142.md

- **Source key:** `rea_lab/decomp_task/REA_T014_DUAL_MODE_CALLSITE_CONFIRMED_20261012_1142.md`; measured source SHA256 `A6C9B9B7F9CC7E2E78BEBA40A51C6D893DDCE6BD5D4F31C25BE958FFEEAC4639`, 3546 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 通常save reader内 `0x45E53A PUSH 1 → 0x45E53E CALL 0x471AF0`、`0x45E547 PUSH 1 → 0x45E549 PUSH ecx → 0x45E54C CALL 0x435550`。外交readerとgraph readerへ双方 mode=1 を渡す。
  - 別の保存済みコード区間 `0x45EF0F PUSH 0 → 0x45EF1D CALL 0x471AF0`、`0x45EF25 PUSH 0 → 0x45EF2D PUSH edx → 0x45EF34 CALL 0x435550`。両readerへ双方 mode=0 を渡す分岐を命令列から確認。
  - mode=0の呼出は直前 `0x45EEFE SETE AL / 0x45EF01 TEST AL,AL / 0x45EF03 JE 0x45F66E` を経て到達する。無条件に全saveを毎回初期化するとは言えない。
  - graph reader `0x435550` のsave済Ghidra callersは `0x45E1E0` と `0x45EAC0`。証拠ID `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`。呼出命令のVAは `0x45E54C` / `0x45EF34` として区別する。
  - `0x45EAC0`からは `MOV ECX,[EBP-0x14]`など途中コードが保存され、通常プロローグがない。入口境界・親routine・到達条件は独立Ghidra 5-method証拠未取得のため VERIFY。別個の高水準loader関数2個と断定禁止。
- **Source limitations:** - graph関数既存info `ev_8fc065296a08a2f672a520399680a38404d656f96ecd59f4747278ec964409a4`、assembly `ev_775c749267e95e4682d3e76c638e9a612068de9345aedb4557eabd74e6eaafe2`。mode=0は既存tree clearと3種allocate、mode=1は既存3 global objectに作用する別経路。callee副作用/再初期化範囲はVERIFY。 / - 対象T-ID=T014。再実装では diplomacy/graph 両者について mode 0/1 を区別し、root reader全件へ無条件clearを追加しない。旧EXE実機trace未取得。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T014_FOUR_GROUP_SENTINEL_LOOPS_CORRECTION_20261012_1336.md

- **Source key:** `rea_lab/decomp_task/REA_T014_FOUR_GROUP_SENTINEL_LOOPS_CORRECTION_20261012_1336.md`; measured source SHA256 `D8DF3851257D7FDD22BD162062DAB96C84D4E35EC71DC9776C03402CFC0A772B`, 4191 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 読取専用一次資料: `exe/T014_NORMAL_LOAD_PROBE.txt`、特に保存disasm VA 0x45ED20..0x45EF34 と 0x45F66E..0x45F92E。既存ソース/所有ファイルへの変更なし。
  - | 1 numeric persistent | 0x45ED2D / 0x45ED72 | 0x45ED92→0x45F8A2 | 0x20 byte record; `0x4705F0` key + `0x470700` int; `0x4A69B0` | 0x45F92E→0x45ED20 |
  - | 2 Unit runtime | 0x45EDA5 / 0x45EDED | 0x45EE0D→0x45F80E | alloc 0x1D4 / init `0x582AA0` / reader `0x58E870`; `0x463280` at owner+0x2FC | 0x45F89D→0x45ED98 |
  - | 3 Spot runtime | 0x45EE20 / 0x45EE68 | 0x45EE88→0x45F75D | alloc 0xD0 / init `0x5971A0` / reader `0x598980`; `0x463280` at owner+0x2EC | 0x45F809→0x45EE13 |
  - | 4 Power runtime | 0x45EE9B / 0x45EEE3 | 0x45EF03→0x45F66E | alloc 0x138 / init `0x590560` / reader `0x5964C0`; `0x463280` at owner+0x2DC | 0x45F758→0x45EE8E |
  - 比較は毎群、同じ global string `0x65CD28`（長さ `0x65CD38`、SSO容量 `0x65CD3C`）との `0x402C40` 内容比較+長さ検証。**一致=当該群を終了して次群へ、非一致=レコードを読んで同群を反復**。群順は numeric → Unit → Spot → Power で、4群終了後だけ `0x45EF1D` diplomacy reader mode0 と `0x45EF34` graph reader mode0 へ。
  - Spot読込後、+0x88が0なら `@spot_capacity` を取得する分岐（0x45F7A2..B5）。Power読込後、+0xDCが0x80000008なら scenario/base_level のfallback（0x45F6AF..EE）。それぞれの入力値・補正有効域はVERIFY。
  - 過去の`0x4705F0` callers証拠ID: `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`。`0x435550` callers証拠ID: `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`。今回の新規5-method evidence IDなし、静的VERIFIED増加0。
  - VERIFY: 4グループの実際の区切り文字 raw bytes と malformed/EOF時挙動、numeric側の正確なtree所有参照、重複キー勝敗、0x470550の内部契約、0x58E480の利用範囲、Unit/Spot/Power後続 side effects、関数0x45EAC0の境界と原作実機挙動。
  - 次回: saved native 内の`0x470550`と`0x58E480`の本体/呼出関係を安全に読み、4群のmarker raw bytesをソース内で確証。所有A/Eに統合を委ね、他レーン/MASTER/T018は更新しない。
- **Source limitations:** - 旧メモに対する訂正: marker不一致を一律「ロード拒否/例外」と読むのは誤りで、通常のグループ内レコードを処理する経路が明示される。marker連続4個なら各群空の直線パスとしてmode0へ進むが、各群に0件以上の要素があることを許す。 / - VERIFY: 4グループの実際の区切り文字 raw bytes と malformed/EOF時挙動、numeric側の正確なtree所有参照、重複キー勝敗、0x470550の内部契約、0x58E480の利用範囲、Unit/Spot/Power後続 side effects、関数0x45EAC0の境界と原作実機挙動。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T014_FOUR_SENTINEL_MODE0_GATE_AUDIT_20261012_1241.md

- **Source key:** `rea_lab/decomp_task/REA_T014_FOUR_SENTINEL_MODE0_GATE_AUDIT_20261012_1241.md`; measured source SHA256 `8E2039E515E811E821F28C3C65B76E968ADC01FF98466D2ECBB795CE7051748B`, 4378 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - `0x45E5F0`には通常の関数プロローグがあり、同じ保存済み長大ロードコード内の`0x45EAB6→0x45EAC0`はfall-throughしている。`0x45EAC0`には独立プロローグがなく、内部ループのヘッドとして解釈するのが整合的。Ghidraがcallerに挙げた`0x45EAC0`を高水準の独立loaderとして確定しない（関数境界VERIFY）。
  - `0x45EAC0..0x45EB39`はowner `[EBP-0x14]` の`+0x2E0`木を走査し、node+0x28が非nullなら`0x45DF70→0x5B6BBB`、その後木iteratorを更新するループ。`0x45EB3B..0x45EC0D`は少なくとも+0x310/+0x300/+0x2F0/+0x2E0の複数ツリーを`0x463070`などでclearしてsentinel linksと件数欄を初期化する。
  - `0x45ECBB`で`0x470550`を呼ぶ。以降、共通reader`0x4705F0`で取り込んだroot markerを`0x402C40`の内容比較と長さ比較で4回チェックする。
  - 第1比較: reader `0x45ED2D`、marker比較`0x45ED72`、不一致側`0x45ED92→0x45F8A2`。
  - 第2比較: reader `0x45EDA5`、marker比較`0x45EDED`、不一致側`0x45EE0D→0x45F80E`。
  - 第3比較: reader `0x45EE20`、marker比較`0x45EE68`、不一致側`0x45EE88→0x45F75D`。
  - 第4比較: reader `0x45EE9B`、marker比較`0x45EEE3`、不一致側`0x45EF03→0x45F66E`。
  - この直線経路で4照合を通過した場合のみ `0x45EF0F PUSH 0→0x45EF1D CALL 0x471AF0`、`0x45EF25 PUSH 0→0x45EF34 CALL 0x435550` に到達。前段ゲートと全ての例外枝の全到達性は未確定。
  - mode0 graph読込後、`0x45EF61..0x45F008`に木の追加巡回があり、`0x45F00E..0x45F0D9`で`@gamemode` / `@scenario` / `@spot_capacity` / `@war_capacity` / `@max_unit` / `@gain_per` / `@support_range` / `@my_range` / `@myhelp_range`を属性から読み込み、一部rangeへ下限1を適用する。mode0完了が高水準load終端ではない。
  - 既存Ghidra caller evidence: `0x435550` callers `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`; `0x4705F0` callers `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`。
  - 既存親reader `0x45E1E0` pseudo `ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e`。`0x45EAC0`自身のinfo/pseudo/assembly/callers/callees 5点と入口境界はVERIFYのまま。
  - 課題: `0x470550`内部契約、4個のmarkerそれぞれのレコード階層、条件分岐先各4か所の処理、EOF/malformed、後段cap clampとroot契約の実機一致。T014 ownerへの正式統合はA/E担当であり本REAは書換えない。
- **Source limitations:** - 課題: `0x470550`内部契約、4個のmarkerそれぞれのレコード階層、条件分岐先各4か所の処理、EOF/malformed、後段cap clampとroot契約の実機一致。T014 ownerへの正式統合はA/E担当であり本REAは書換えない。 / - 最新MASTER checkpoint83: DONE9/34（IN_PROGRESS21/VERIFY4）。旧EXE Gameplay golden PASS0。ゲーム再実装率は測定していない。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

### REA_T014_GLOBAL_SAV_UPSERT_BRANCH_AUDIT_20261012_0937.md

- **Source key:** `rea_lab/decomp_task/REA_T014_GLOBAL_SAV_UPSERT_BRANCH_AUDIT_20261012_0937.md`; measured source SHA256 `720E937679667378CEEA2D30AC2100A86FF5B06C45A799034B4C19E2E4CDDC2D`, 4527 bytes.
- **Explicit owner ID:** not declared in document header; do not invent one. 
- **Allowed source-native excerpt:**
  - 範囲: REA保存済みrun `20261011T113414092Z` の0x428710（T014）をread-only照合。新規REA/Ghidra実行0、関数VERIFIED増加0。承認コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を今回再hash MATCH。原本EXEは実行・変更しない。
  - info `ev_18083c1e4b216eb84426042a80e5dd8d28b884882f59162ab8f5fe1cb74a64d6` (entry 0x428710, length3252, noncontiguous 4 ranges)
  - callers `ev_21421f53fb9052bf2f3b7cbee448c0bfe34b814e644d49db93939e7b14d7719a` (resolved 0x514270/0x567210/0x567840)
  - 0x428757..0x42879B: guard bit `0xB09620 & 1` の初回経路で、`0xB09604` の固定文字列を「----------」（10文字）に初期化する。
  - 0x428831..0x4288C6: global.sav がFindFirstFileAで見つからなければCreateFileA(disposition4 OPEN_ALWAYS)を実行し、既定marker文字列を長さ+1（NULを含む）でWriteFile後CloseHandleへ進む。これを完全な新規save妥当性・初期ファイル形式として一般化しない。
  - 0x4289B0..0x428A1F: 既存ファイルサイズを取得、読込、`0x4270F0`を通して復号、`0x429C60`でstreamを構成。
  - 0x428ADF..0x428B4A: 共通token reader `0x4705F0` を用い、10文字markerとの文字列内容・長さ一致ならrecordループを脱出。通常recordは0x428B7F token/0x428B8D int32を読み、`0x4A69B0`へ渡す。
  - 0x428C31..0x428C5D: `0x4C1200` tree lookupの結果がsentinelと異なる（既存node）場合、node+0x28で辿ったpayload+0x1C DWORDに新数値を**その場で上書き**して新規node挿入をせず進む。
  - 0x428C62..0x428CD9: tree lookupの結果がsentinel（未登録）の場合、0x20-byte candidateを作り、payload+0x1Cへ値を格納し、`0x436560 -> 0x436680 -> 0x4A69B0` によって**新規挿入経路**へ進む。
  - 0x428DB3..0x428EAA: tree entryごとに`0x470830`で文字列2件と`0x4628F0`でDWORD数値をstreamへ出力し、最後に共通終端token `0xB09604` を出力。0x428F59 encryption `0x427040`、0x428F84 WriteFile、0x428F8B CloseHandle。
  - 0x428EC2..0x428ED4: 更新時CreateFileA(disposition4 OPEN_ALWAYS)。既存長より短くなる場合に末尾残留の可能性はあるが、先行事前操作やdecoderの余剰扱い・実ファイル短縮は今回未証明。これを確定破損バグとしない。
  - 0x4705F0のGhidra resolved caller13件のうち、既存7件に今回0x428710を加えて**8/13用途分類済み**。未分類5件=0x45EAC0,0x470550,0x58E480,0x5A90E0,0x5B0400。間接呼出は13に含まれない。
- **Source limitations:** - 0x428EC2..0x428ED4: 更新時CreateFileA(disposition4 OPEN_ALWAYS)。既存長より短くなる場合に末尾残留の可能性はあるが、先行事前操作やdecoderの余剰扱い・実ファイル短縮は今回未証明。これを確定破損バグとしない。 / - T014: global.savは「キーがあればpayload DWORDを更新、無ければnodeを追加、その後全件を直列化し直す」局所フロー。重複キーの全保存形式・順序の全保証、I/O return検査の上位作用、EOF、不正/不足バイト、旧EXE実機結果はVERIFY。
- **Stage:** PRESERVED_UNKEYED_SOURCE / VERIFY, not formal CURATED; original Golden PASS0 / READY0.

## Curator instructions

Earlier T013 support selection, T014 save parser/serialization and unit/event documents have overlapping existing native evidence. The exact old source SHA and specific VA/call/condition should be cross-checked with current REF/owner before assigning any distinct ID; file counts are not independent proof counts. Do not attempt any denied 0x target or Wave6 extraction, and do not publish raw original material. The unrelated readback and recovery receipt group is a validation aid, not source claims. Only curator may edit develop/REF/symbols.
