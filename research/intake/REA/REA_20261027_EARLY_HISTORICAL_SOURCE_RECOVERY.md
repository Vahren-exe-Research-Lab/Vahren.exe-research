# REA owner research recovery 20261027 / EARLY

**Private owner intake, STATIC/INFERRED/VERIFY, NOT CURATED / NOT READY.** These 12 already existing source research IDs are preserved, not newly decompiled functions. The same source reports and evidence JSON hashes were measured read-only on the authorized REA research PC on 2026-11-02 JST. Source relative paths and bytes are included. Evidence candidates matched by report-hour are hash-only references and must be confirmed per-report by KB curator; original evidence bytes stay on PC. Machine-only static text excerpts below are selected from the old owner reports, not rerun native tests. Current PE/V9 real-time SHA not freshly measured in this intake, no game launched. Existing formal Wave1–5 64/64 not counted again. Golden PASS 0, READY 0.

### REA-LOCAL-20261027-01H-P0-DMUSIC-EXACT-LOOKUP-CACHE-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_01H_P0_DMUSIC_EXACT_LOOKUP_CACHE_STATIC.md`; actual SHA256 `EF422B01D74486D170C8C068029BCFC861B0B35D2C0CE6C0F9F4DB325A12B8B0` (4521 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_01HB_P0_DMUSIC_SUFFIX_DISPATCH_EVIDENCE.json` SHA256 `B75053653214D45B24C8887C3E0D769D1802814AAAAA6638BD6238C234B93BE4`; `REA_20261027_01H_P0_DMUSIC_EXACT_LOOKUP_CACHE_EVIDENCE.json` SHA256 `26494A54603B809969143C118F1D2595BA2DBCC946742894F506E04E4E003968`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 前回23Hまでで0x004BE820の名前検索不一致→乱数×個数→+0x70配列参照をSTATIC確認済み。本回では「どの比較条件で不一致になるか」と「選択後のキー登録」を新規限定監査。既存64関数や23Hの結果は再カウントしない。
  - ## 新規結果A：lower_boundに加えて一致確認する（STATIC）
  - 0x004BDE40:0x004BE178 CALL 0x004BE820。0x004BE820:0x004BEEACでESI=[EBP+0x7C]の検索木、0x004BEEBE CALL 0x004C1200。0x004C1200:0x004C1209 CALL 0x004682B0で木のlower_bound候補を取得。
  - 0x004682B0:0x004682F9 CALL 0x00402C40、0x0046830D/0F/14/18の分岐は「candidate>=requested key」の先頭候補に向かう。0x00402C40はmovzxの非符号byte比較、差の符号を0/-1/+1へ変換（0x00402C6E/0x00402CA3/0x00402CA7）。
  - 0x004C1200:0x004C1244でも同じ比較器を逆側の引数順で使用し、0x004C124Fの長さ分岐と0x004C1258の符号分岐によって候補がkeyより大きいと番兵を返す。lower_bound候補がkey未満にならないことと合わせ、返したノードは実質的にkey一致。Ghidra擬似Cのみでなく各命令をCapstoneで確認。
  - 0x004BE820:0x004BEEE3 CMP ECX,[EBP+0x80]→0x004BEEE9 JE 0x004BEEFAで番兵時のみ既報の乱数fallback。一致時は0x004BEEEBでnode+0x28から登録済み値を使用、乱数を使わない。
  - ## 新規結果B：乱数fallbackの直後に木への登録がある（STATIC）
  - 0x004BEF04 rand→0x004BEF1B FTOL→0x004BEF27 [EDX+EAX*4]でPerformanceスロット取得（ここは既報）。
  - 追加で0x004BEF2F MOV [EBX],EAX（EBX=[EBP+0x78]）。0x004BEF48 CALL 0x00510F70が文字列+値ペアを構築し、0x00510F91でpair+0x1Cへ値を書き込む。
  - 0x004BEF5C CALL 0x00436680がノードを生成。0x004366FE/0x00436701によりnode+0x28へペアの値を格納する。0x004BEF68 CALL 0x00463280は検索時と同じESI=[EBP+0x7C]の木にinsert-if-absentを実行する経路と整合。generic insert-if-absent自体はMASTERの既存成果であり新規に数えない。
  - ## 独立照合・状態
  - 0x004BE820の検索キー生成・入力文字列変換（0x00426490、0x00402800、0x004261B0、0x0040B200）を限定追跡し、完全一致になる入力条件・大文字小文字・拡張子処理の仮説を整理。次に0x00463280のinsert成功フラグと同一キー再利用、count=0でのlookup miss到達性、+0x70配列所有権をVERIFY。原作Goldenは隔離環境がないためNOT RUN。
- **Correction/remaining VERIFY:** 同一オブジェクト・同一正規化キーで登録成功した後の再呼出しなら、次回は既存ノードを使って乱数選択を省略する構造と推定。ただし挿入成功率・オブジェクト破棄/再生成・名前正規化・実ゲーム時の再利用は未実測のためVERIFY。 / 正式REA新規VERIFIED 0。旧Wave1～5 VERIFIED 64/64を旧同期記録として保持。5種はinfo/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED書込差分=0/0/0。原作Golden実測PASS0、strict MATCH・完全複製率未測定。 / 0x004BE820の検索キー生成・入力文字列変換（0x00426490、0x00402800、0x004261B0、0x0040B200）を限定追跡し、完全一致になる入力条件・大文字小文字・拡張子処理の仮説を整理。次に0x00463280のinsert成功フラグと同一キー再利用、count=0でのlookup miss到達性、+0x70配列所有権をVERIFY。原作Goldenは隔離環境がないためNOT RUN。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-01HB-P0-DMUSIC-FIRST-DOT-EXT-DISPATCH-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_01HB_P0_DMUSIC_FIRST_DOT_SUFFIX_STATIC.md`; actual SHA256 `0DA553F2CC75597B9AA4CEC07CE938B121FDC981D712F8F4DE2F5D5B6BFC9924` (4813 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_01HB_P0_DMUSIC_SUFFIX_DISPATCH_EVIDENCE.json` SHA256 `B75053653214D45B24C8887C3E0D769D1802814AAAAA6638BD6238C234B93BE4`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 新規STATIC：拡張子の3バイト部分だけを比較
  - 0x004BE820:0x004BE917 PUSH 1、0x004BE919 PUSH 0x00630024（ASCII '.'）、0x004BE92E CALL 0x00426490。0x00426490は先頭からmemchr→比較を繰り返し最初の一致位置を返すfind系。
  - 一致位置があれば0x004BE93E INC ESIで「最初のドットの次」へ移動、0x004BE951 PUSH 3→0x004BE95E CALL 0x004261B0で3バイト文字列を構築する。長さ不足ならこの抽出をしない。
  - 0x004BE9B5のECX=0x00630028はASCII 'ogg'、0x004BE9BA CALL 0x00402C40の非符号バイト比較と3バイト長一致でOGG分岐を決める。
  - それ以外は0x004BE9DC JE 0x004BEC0Cへ進み、0x004BEC0CのECX=0x0063002C（ASCII 'mp3'）と0x004BEC15 CALL 0x0040B200で同じ3バイト候補の完全一致を検査する。
  - MP3でなければ0x004BEC31 JE 0x004BEE7Eに進み、既報のDirectMusic系名前検索・ランダムfallbackの処理へ入る。判定関数0x00402C40の比較はmovzx byteによる大文字小文字を区別した比較。
  - ## 新規STATIC：上流の拡張子補完も最初のドットで分岐
  - 呼出元0x004BDE40:0x004BDEB6は0x00630000の'.'を検索し、0x004BDEC7 CALL 0x00426490で不在か判断する。
  - ドット不在時は0x004BDED5から0x0068C7D0の3ポインタ配列を巡回する（".mid"→".mp3"→".ogg"）。候補文字列を0x00416970で作り、0x004BDF0F CALL 0x004BDAF0で既存登録/音楽名を確認し、値が非0なら採用する経路がある。
  - ドットが1つでもあればこの自動拡張子探索を迂回する（0x004BDECF JNE 0x004BDF82）。ドットがパス中のディレクトリ名にある場合でも最初のドットが使われる可能性を静的に確認。
  - 上流にも0x004BDF89 PUSH '.'、0x004BDF93 CALL 0x00426490、0x004BDFB3 CALL 0x004261B0、0x004BDFBD ECX='mp3'、0x004BDFCC CALL 0x0040B200があり、3文字抽出によるMP3判定が存在する。
  - ## 合成例（引数のバイト列を0x004BE820に直接渡すモデル、原作実機ではない）
  - 拡張子なしは子関数内ではDirectMusicだが、上流0x004BDE40が補完候補を試すため、ゲーム全体の結果と同一視しない。
  - VERIFY: 実際のBGM指定に階層ドット/大文字拡張子/長い拡張子が存在するか、0x004BDE40の呼出元が入力を正規化するか、ドット無し自動補完の実ゲーム時の探索成功条件。
  - 次の関数: 0x004BDE40のcallerおよび0x00416970/0x004BDAF0の候補組立・探索副作用、0x00463280の挿入成功/重複時帰結。原作ゲーム Golden隔離環境なしにつきNOT RUN。
- **Correction/remaining VERIFY:** 16入力の合成分類を監査した結果、想定との不一致0。ファイル存在/コーデック成功/ユーザー指定文字列が上流で変換される可能性は実機未検証。 / 5種類のREA証拠: info/pseudo/callers/callees=INDEX_ONLY_V9、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED=0。過去Wave1～5 64/64は既存同期記録のみを保持。正式TODO/VERIFY/BLOCKED書込差分0/0/0。 / VERIFY: 実際のBGM指定に階層ドット/大文字拡張子/長い拡張子が存在するか、0x004BDE40の呼出元が入力を正規化するか、ドット無し自動補完の実ゲーム時の探索成功条件。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-02H-P0-DMUSIC-TWO-PATH-BANKS-RING-BUFFER-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_02H_P0_DMUSIC_TWO_PATH_BANKS_RING_STATIC.md`; actual SHA256 `DE3E460A928533927CC18FF2E54632B770359790681DAB8041172F0A04F80C90` (4932 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_02H_P0_DMUSIC_PATH_BANK_RING_EVIDENCE.json` SHA256 `9E0DE71B531849433F2DDC3E9677FE45D858FB2660F8BD661DE41AA9C3A6764A`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 01HBは最初のドットによる拡張子判定と、拡張子なしの候補 .mid→.mp3→.ogg を既に確認済み。今回は候補名を実パスへ解決する0x004BDAF0と0x00406CF0を深掘りした。
  - ## 新規STATIC A：二つのパスバンクを優先順で巡回する
  - 0x004BDE40の0x004BDF0Fと0x004BE018は、0x004BDAF0を呼ぶ直接E8 CALL。
  - 0x004BDAF0では、構造体の[ESI+4]～[ESI+8]を第一バンク、[ESI+0x14]～[ESI+0x18]を第二バンクの範囲として順に巡回する。各エントリは0x1Cバイト刻み（0x004BDB72,0x004BDBF0）。
  - 第一バンクは0x004BDB37 CALL 0x00406CF0で候補パスを組立て、0x004BDB47 CALL [0x00609178]でFindFirstFileA、成功なら0x004BDC2Eへ分岐。
  - 第一で見つからなければ第二バンクへ移行し、0x004BDBB5 CALL 0x00406CF0、0x004BDBC5 CALL [0x00609178]で同APIを呼び、成功なら0x004BDC6Cへ分岐。
  - 二つの成功経路は0x00609174のFindCloseを呼び、見つかった候補パスの文字列を返す。双方が不一致なら0x004BDC15で空文字列を構築して返す。
  - ## 新規STATIC B：パス組立ヘルパーの共有16スロット
  - 0x00406CF0はDAT_00AC0860のカウンタを増加し、0x10到達で0に戻し、0x00406D07 SHL EAX,0xAにより1スロット0x400=1024バイト分のオフセットを計算する。
  - 0x00406D0BでベースDAT_00ABC460を加えて保存先を選択。続いて0x00406D16～0x00406D1Eでパス接頭辞をNUL込みコピー、0x00406D20～0x00406D48で後続文字列をNUL込み連結する。
  - 関数内のCMPは0x00406CFBのスロット循環判定だけ。入力2文字列の合計長を1024バイトと照合する分岐は機械語上確認されなかった。
  - ## 条件付きP0 VERIFY：1024バイト境界
  - ## 独立監査・関数別5証拠
  - 0x00406CF0の外側入力長の上限とDAT_00AC0860初期化、0x004BDAF0の二つのパスバンクが何の設定から組み立てられるかをそれぞれ参照元から静的追跡する。候補選択の実ゲームGolden・同名ディレクトリ・ロングパスの再現は隔離環境が無いため NOT RUN。
  - 対象は0x00406CF0 callers、0x004BDAF0の保持オブジェクト構築元、0x004BDE40の引数供給元。重複を防ぎ既存V9のデータを優先し、REA再実行を先行させない。
- **Correction/remaining VERIFY:** 実入力で1024バイトを超える合成パスを渡せるか、OS側の長さ制限、外側のスクリプト・パーサで制限されるかは未検証。実際のヒープ破壊・クラッシュを確認したものではない。 / FindFirstFileAはファイルをopenして内容を検査する処理ではない。Find結果の属性を見てdirectoryを拒否する処理も、このヘルパー内では未確認。実際の音声ファイル探索・存在しない/同名ディレクトリ時のゲーム挙動はVERIFY。 / 既存Wave1～5 VERIFIED 64/64（旧同期ログ）、新規正式VERIFIED=0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。旧Golden実測PASS=0、strict MATCH・完全複製率は未測定。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-03H-P0-DMUSIC-2K-RING-BGM-SUBDIR-BANK-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_03H_P0_BGM_BANK_ENUM_2K_STATIC.md`; actual SHA256 `8F7900CB88E776D61238A4678A1E645AFD2CFBDF4E123457DE090789165FFD8D` (5158 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_03H_P0_BGM_BANK_ENUM_2K_EVIDENCE.json` SHA256 `C4C91985C3C35FCE12B9BC837289D2835097B62B627742DEEACA37A5D6A86B8B`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 02Hでは0x004BDAF0の2つの検索パスバンクと0x00406CF0（16×1024B）の存在確認まで完了。本研究では初期化側の0x004BD2A0と別ヘルパー0x00406D50を限定解析し、バンクに投入されるパス形式、ディレクトリ列挙条件、独立した大容量バッファを追加固定した。02H 56/56、旧REA 64/64を新規に二重計上しない。
  - ## 新規STATIC A：二系統の「bgm/」+直下ディレクトリ
  - 0x004BD2A0は第1の動的ベースパスDAT_0068B370、第2のDAT_0068B38Cを使用する（いずれも実行時の文字列内容は未確定）。
  - 原作の文字列定数0x0062FFC8・0x0062FFE4は「bgm/」、0x0062FFD0・0x0062FFECは「bgm/*」、0x0062FFDC・0x0062FFF8も「bgm/」、0x0062FFD8・0x0062FFF4は「/」。
  - 第1バンクでは0x004BD4CF→0x00406D50で基点「ベース+bgm/」を作成し、0x004BD51E→0x00429A00で登録。0x004BD563→0x00406CF0で「ベース+bgm/*」を作り、0x004BD56CのFindFirstFileAを実行する。
  - 検索結果は0x004BD580のFILE_ATTRIBUTE_DIRECTORY(0x10)を満たしたときだけ候補となり、0x004BD5C8/0x004BD618の比較分岐を通過すると0x004BD664→0x00406D50で「ベース+bgm/+ディレクトリ名+/」を構築、0x004BD6A8→0x00429A00で登録される。0x004BD6DBのFindNextFileAで次の候補へ進み、0x004BD6EFでFindCloseする。
  - 第2バンクでも0x004BD775→0x00406D50と0x004BD7C0→0x00429A00で基点を追加し、0x004BD805→0x00406CF0と0x004BD80EのFindFirstFileAで列挙。0x004BD821でディレクトリ属性を確認後、0x004BD8D0→0x00406D50で直下名を加え、0x004BD917→0x00429A00で第2バンクへ追加し、0x004BD956/0x004BD966でFindNextFileA/FindClose。
  - ## 新規STATIC B：0x00406D50は独立した16×2048Bリングバッファ
  - 0x00406D50はDAT_00AC0864をインクリメントし0x10で0へ戻す（0x00406D50, 0x00406D5C, 0x00406D61, 0x00406D68）。
  - 0x00406D6DのSHL EAX,0xBにより2048B単位のスロットを選択、0x00406D75でDAT_00AB4460をベースにし、0x00406D70/0x00406D7Eで2048B memsetを呼ぶ。0x00406DAFのrep movsdと0x00406DBBのrep movsbで複数のNUL終端文字列を連結する。
  - 既知の0x00406CF0は別カウンタDAT_00AC0860、別ベースDAT_00ABC460、16×1024B。0x00AB4460+0x800×16=0x00ABC460で、両バッファ群はアドレス上で隣接する。
  - 0x00406D50の0x78バイトを独立逆アセンブルした範囲では、CMPはカウンタの0x10比較だけ。連結する全入力長を0x800と照合するチェックは見つからない。合計長+NULが2048以下ならスロット内、2049以上ならスロット容量超過の条件付き危険がある。
  - ただしスクリプト/入力側の制限、OSのパス長制限、長い入力の実行到達性は未確定。クラッシュ・実際の破壊の発生は未証明で、P0 VERIFYを維持。0x00406CF0の1024B側についても従来のVERIFYを維持する。
  - 原作PE32・IAT、原作機械語30アンカー、文字列定数8件、旧SQLiteと統合V9の4 CALL site（0x004BD4CF/0x004BD664/0x004BD775/0x004BD8D0）、リングカウンタxrefs、2バンク確保先、02H証拠、旧64件をそれぞれ照合。**65/65 PASS**（監査条件数。新規関数数ではない）。
  - 次は0x00556F00等のDAT_0068B370/0x0068B38C設定経路と、0x004BD2A0で先に作る検索バンクの実パス意味、個々の文字列長上限を絞る。DirectMusic関連の実行Goldenは未実測。
- **Correction/remaining VERIFY:** ただしスクリプト/入力側の制限、OSのパス長制限、長い入力の実行到達性は未確定。クラッシュ・実際の破壊の発生は未証明で、P0 VERIFYを維持。0x00406CF0の1024B側についても従来のVERIFYを維持する。 / 5証拠分類: info=INDEX_ONLY_V9 / pseudo=INDEX_ONLY_V9 / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY_V9 / callees=INDEX_ONLY_V9。REAの独立5種類証拠を新たに全完備した関数は0。新規正式VERIFIED=0、旧Wave1～5の64/64は保存済み同期記録を保持、正式TODO/VERIFY/BLOCKED書込差分0/0/0。原作ゲームGolden=0、strict MATCH/完全複製率は未測定。 / 次は0x00556F00等のDAT_0068B370/0x0068B38C設定経路と、0x004BD2A0で先に作る検索バンクの実パス意味、個々の文字列長上限を絞る。DirectMusic関連の実行Goldenは未実測。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-04H-P0-STARTUP-BASE-RETURN-ABI-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_04H_P0_STARTUP_BGM_PATH_STATIC.md`; actual SHA256 `311C1BA8B8B79F69FDC4A64DAF363D0F23A76E1655F6D0B51C19C8EB08C960CE` (4213 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_04H_P0_STARTUP_BGM_PATH_EVIDENCE.json` SHA256 `C74F04E41D9BAFC039470A6A0DFEBE864ADC5370A6550CF062104F5A9CBE82D3`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 新規静的事実A: 0x00556F00はALにbool相当値を返す
  - 旧Ghidra10/21検索索引の0x00556F00機械生成疑似Cは「void FUN_00556f00(void)」「return;」だが、原作PE32の命令0x00557209は MOV AL,BYTE PTR [ESP+0x17]、0x00557231は RET。
  - 0x00556F3Bでstack byte 0x17に1を入れ、0x005571B9でBL(0)に変更する経路がある。少なくともこの戻り値は無意味なvoidではない。
  - 親0x005554F0の0x00555904から直接CALLし、直後0x00555909でTEST AL,AL、0x0055590BでJE。索引DB双方に0x00555904→0x00556F00のCALLが登録される。
  - 0x0055590Dは0x00559690を呼び、その返りALを0x00555914でTEST、成功側のみ0x00555918で0x00555CD0へ進む。0x00555CD0は前回までに音声初期化を含むことを確認済み。
  - 厳密な仕様では、0x00556F00の戻り値で直接BGM初期化が決まるのではなく、さらに0x00559690の戻り値判定が介在する。0x00559690自身の戻り値の定義/全異常経路は未確認。
  - ## 新規静的事実B: 1番目のベースパス長が初期起動時の分岐に影響する
  - 0x00556F40はグローバルDAT_0068B380を0と比較し、非0なら0x005571DEへ分岐して通常のメッセージループを迂回する。
  - 0x00557165 MessageBoxA戻り値を0x0055716Bで6(IDYES)と比較し、Yesなら0x005571BFへ。Yes以外では0x00557175 MOV [DAT_0068B380],EBX で長さ0、0x00557183/0x00557188でSSO/heapポインタ先頭をNUL終端し、0x005571B4で0x00556F50に戻る。
  - 0x005571B9ではWM_QUIT（GetMessageA=0）側で戻り用stack byteを0にする。この一連は「第一ベースの消去・待機再試行」と、ウィンドウ終了を区別する実装の証拠となる。
  - 03H研究は0x004BD2A0による「第一/第二ベース + bgm/ と直接サブフォルダ」登録、および2048Bのringを既に確定。今回は起動関数0x00556F00の返り値ABIと第一ベースの消去・音声初期化条件の連鎖のみを追加。03H 65/65と正式Wave1-5 64/64を新規件数に加算しない。
  - 原作PE32 Native Capstone20命令、両SQLite SHA256・quick_check、両DB3 CALL、旧DB直接WRITE xref 0x00557175→0x0068B380、過去65/65、64/64同期ログの計37条件PASS。
  - 0x00559690の戻り値ABI・Direct3D初期化失敗時の分岐を機械語で独立確認し、0x00556790およびDAT_0068B370/DAT_0068B38Cの設定経路、第一パス長が0になった後にBGMバンクがどう構築されるかを照合する。長い入力の1024/2048バッファ越境到達性は条件付きVERIFY維持。
- **Correction/remaining VERIFY:** Yes選択の意味（どのパスか）、どのUIで選択させるか、DAT_0068B38Cの設定元やパス内容は未検証。実ゲームでの動作は断定しない。 / info=INDEX_ONLY, pseudo=INDEX_ONLY, assembly=TARGETED_PE_NATIVE, callers=INDEX_ONLY, callees=INDEX_ONLY。正式REA5種類の新規完全取得0、新規VERIFIED=0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。 / 0x00559690の戻り値ABI・Direct3D初期化失敗時の分岐を機械語で独立確認し、0x00556790およびDAT_0068B370/DAT_0068B38Cの設定経路、第一パス長が0になった後にBGMバンクがどう構築されるかを照合する。長い入力の1024/2048バッファ越境到達性は条件付きVERIFY維持。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-05H-P0-D3D9-INIT-AL-RET-ABI-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_05H_P0_D3D9_INIT_RETURN_ABI_STATIC.md`; actual SHA256 `2C0D13E746312B2E1E89882A8C77D1B498926EF2DA4FF7FA5C83CA04FE26201E` (4511 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_05H_P0_D3D9_INIT_RETURN_ABI_EVIDENCE.json` SHA256 `1F2CA595699E0F4C8B2852943F898EEED43B32535C34AE8F01793BA0144D0C9A`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 今回の新規STATIC：0x00559690の返り値を全4 RET経路で固定
  - 前回04Hは親0x005554F0のCALL 0x00559690（site 0x0055590D）直後にTEST AL,AL（0x00555914）が存在することを確認したが、子自身はGhidra擬似Cで「void FUN_00559690(void)」として出力され、返り値の生成は未検証だった。今回は原作機械語を別途逆アセンブルした。
  - 原作機械語の該当関数範囲は0x00559690..0x00559985。関数内のRETは上記4件。Ghidra機械生成の「void」を返り値不使用とみなすと、起動制御が原作と食い違う。
  - 3か所のMessageBoxAに渡される文字列(0x006299E8/0x00629A0C/0x00629A30)は原作バイト列が一致し、CP932で「DirectX9」の初期化失敗を示す。API/HRESULTは負値判定、0以外の成功HRESULTは拒否していない。
  - 0x00555904 CALL 0x00556F00 → 0x00555909 TEST AL,AL → 0x0055590B JE 0x00555912。前段が0なら子0x00559690を呼ばない。前段が非0なら0x0055590D CALL 0x00559690を実行する。
  - 0x00555912 XOR ESI,ESIはALを変更せず、0x00555914 TEST AL,AL→0x00555916 JE 0x0055591Fにより、AL=0では0x00555918 CALL 0x00555CD0（音声初期化を含む）を省略する。AL=1では呼び出す。
  - ## 独立証拠・集計の区別
  - 旧検索DBと統合V9の両方で0x0055590D→0x00559690の直接CALLを照合。旧DBでは0x005596B0/0x00559774/0x005597CAの間接CALLが当該関数に属することを再確認。間接CALLの対象vtable関数への意味付けは今回の正式VERIFIEDではない。
  - 0x00559990と0x00559690の成功後の仮想CALL群の副作用/失敗時挙動を重点調査。次に0x00556790およびDAT_0068B38Cをread-onlyで追い、BGM第2ベースパスの決定元を確定する。
- **Correction/remaining VERIFY:** 前回04Hは親0x005554F0のCALL 0x00559690（site 0x0055590D）直後にTEST AL,AL（0x00555914）が存在することを確認したが、子自身はGhidra擬似Cで「void FUN_00559690(void)」として出力され、返り値の生成は未検証だった。今回は原作機械語を別途逆アセンブルした。 / よって「DirectX9の最初の3ゲートの成功」が後続初期化の前提となる。後段の追加仮想CALLのエラー処理・全部の初期化成功をAL=1が保証するかは別件VERIFY。 / 5証拠：info INDEX_ONLY / pseudo INDEX_ONLY / assembly TARGETED_PE_NATIVE / callers INDEX_ONLY / callees INDEX_ONLY。REA新規正式VERIFIED=0、5種新規完全取得=0、過去Wave1～5 64/64維持、TODO/VERIFY/BLOCKED正式書込差分0/0/0。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-06H-P0-D3D9-POSTGATE-UNCHECKED-VTABLE-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_06H_P0_D3D9_POSTINIT_STATIC.md`; actual SHA256 `32D430ABD8428E0BC8E8FDC2C6F868265FF78E46FF00BD267DC30C0F565E36DC` (4288 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_06H_P0_D3D9_POSTGATE_EVIDENCE.json` SHA256 `E258C3AA40E55E1460B0BF30E5CC0BAA405C1C05359E4B5BD99276BC3136F4F6`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 関数 0x00559690 は前回05Hに0x005596B0(vptr+0x20)、0x00559774(+0x40)、0x005597CA(+0x68)の3失敗ゲートと0/1のAL returnを確認済み。今回はそこから後段 0x005597F7～0x00559975 の原作機械語を独立で解析した。
  - 間接CALL18件: 0x00559804, 0x00559811, 0x0055982E, 0x00559848, 0x0055985C, 0x00559873, 0x00559887, 0x0055989B, 0x005598AF, 0x005598C3, 0x005598D9, 0x005598EF, 0x00559905, 0x0055991B, 0x00559931, 0x00559947, 0x0055995D, 0x00559973。旧Ghidra検索DBのindirect_callsと18件一致。
  - 直接CALL: 0x00559830 → 0x00559990。旧DBと統合V9の双方で同じdirect CALLを確認。
  - ## NEW STATIC: 0x00559990の補助初期化
  - 関数0x00559990の原作線形逆アセンブル範囲は0x00559990～0x00559D22(RET1箇所)。
  - 仮想CALL4件: 0x005599BC, 0x005599D3 (両者+0xB4), 0x00559A28 (+0xC0), 0x00559B05 (+0xB4)。旧DBのindirect_callsと一致。
  - そのほか0x00559A73/0x00559B43/0x00559BA0/0x00559BCF/0x00559BFE/0x00559C1Dの6件の動的API/関数ポインタCALLを保存済み擬似Cと原作機械語で照合。PEインポート表の独立読出しでIAT 0x006092CC=D3DXPlaneFromPoints、0x006092D0=D3DXMatrixPerspectiveFovLH、0x006092F4=D3DXMatrixLookAtLH、0x006092DC=D3DXVec3Unproject を確認した。仮想CALL先の実体・戻り値型はまだ未確定。
  - 0x00559990は戻り値として初期化成否を親へ渡さず、途中に浮動小数点を使う反復処理がある。収束条件・NaN/ゼロ増分・API失敗による挙動はVERIFY。
  - 次回は0x00559990の浮動小数点反復条件(0x00559C1F～0x00559CF0)、入力定数のゼロ・NaN・非有限値の到達性を限定追跡。または0x00556790と第二BGMベースパスDAT_0068B38Cの生成元を調査。
- **Correction/remaining VERIFY:** 0x00559990は戻り値として初期化成否を親へ渡さず、途中に浮動小数点を使う反復処理がある。収束条件・NaN/ゼロ増分・API失敗による挙動はVERIFY。 / 5種類: info=INDEX_ONLY, pseudo=INDEX_ONLY, assembly=TARGETED_PE_NATIVE, callers=INDEX_ONLY, callees=INDEX_ONLY。新規正式VERIFIED=0、5種新規完全取得0。正式TODO/VERIFY/BLOCKEDの書込差分は各0。旧64件を二重加算しない。 / VERIFY: 仮想CALLの戻り値型と各D3D9メソッドの失敗条件。戻り値未検査というSTATICと実ゲームの不具合発生は別。成功後のAL=1をすべての後段API成功とみなさない。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-07H-P0-D3D9-FPU-MINIMA-NONTERMINATION-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_07H_P0_D3D9_FPU_LOOP_STATIC.md`; actual SHA256 `7359594B5F8A9B41E236085FC5612B311EBDFD665E9581A194C41A991D868F81` (5632 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_07H_P0_D3D9_FPU_LOOP_EVIDENCE.json` SHA256 `2A960704F9148F52CD7E55FEE1B76A0FAC9933239E6744D4DBE14CC52B61497A`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 06Hで0x00559690後段の間接CALL18件、直接CALL site 0x00559830 → 0x00559990、子関数の間接CALL群をSTATIC確定済み。今回は既存のGhidra全関数擬似Cを再収集せず、子関数0x00559990（0x00559990～0x00559D22）の**ループ停止条件をx87 status byteと実命令から追加検証**。06Hの43検査と今回の58検査は別検査項目であって、解析完了関数数として合算しない。
  - Ghidra search.py function/callers/callees/relatedをread-only実行。direct callerは0x00559690のsite 0x00559830。Ghidra pseudoは機械出力・型推定であり、独立の関数別REA 5方法証拠ではない。
  - 0x00559B49: FLD [0x0063B0A8] → 初期走査値float32 = -2.0。
  - 0x00559B63: FLD [0x0063B150] → 2本の最小誤差初期値float32 = 1,000,000.0。
  - 0x00559B77～0x00559C1D: D3DXMatrixLookAtLH / D3DXVec3Unproject ×2 / D3DXPlaneIntersectLine の計算・反復。
  - 0x00559C1F～0x00559C3E: 誤差e1 = abs(-1.0 - 交点座標1)。double基準値 [0x0063B148] = -1.0。
  - 0x00559C42～0x00559C5F: 誤差e2 = abs(1.0 - 交点座標2)。
  - 0x00559C6B/0x00559C7C: FCOM/FCOMP → FNSTSW AX; 0x00559C73/0x00559C80 TEST AH,5 → JP/JNP判定。
  - 有限のordered値では、0x00559C83のJNP→0x00559CDB退出は **e1 > best1 かつ e2 > best2** の場合のみ。どちらか一方が等しい・改善したなら続行する。
  - 0x00559C87～0x00559CA7: それぞれ旧best > 新誤差の時だけ最小値を更新。等値・unorderedでは更新しない。Ghidra疑似Cのwhile(true)と整合。
  - 0x00559CB3 / 0x00559CCC: float走査値からqword [0x0063B140] = 0.009999999776482582を減算、float32へ格納。
  - 0x00559CBD / 0x00559CD6: 共通入口0x00559B77へ無条件後方JMP。対象ループ内に独立した反復回数・整数カウンタ上限は見つからない。
  - 0x00559B69 は IAT 0x006092E4 (=D3DXPlaneIntersectLine) をEBXへ格納し、0x00559C1D CALL EBXの直後0x00559C1Fで出力浮動小数点を読み込む。戻り値EAXをその場で検査していない。交差失敗時のAPI結果・出力未更新・有限値保証はVERIFY。
  - 1. P0: 0x00559C1Dの交点出力がNaN/無限/未初期化になり得る初期入力、D3DXPlaneIntersectLineと2件のD3DXVec3Unproject失敗時の挙動を、元の保存静的資料から限定検証する。実機証明は別。
  - 2. P0: 0x00559990を呼ぶ0x00559690の初期値・3Dオブジェクト生成の条件と、0x00879838の値consumerを追跡し、反復不成立条件の到達性を狭める。
- **Correction/remaining VERIFY:** 0x00559B69 は IAT 0x006092E4 (=D3DXPlaneIntersectLine) をEBXへ格納し、0x00559C1D CALL EBXの直後0x00559C1Fで出力浮動小数点を読み込む。戻り値EAXをその場で検査していない。交差失敗時のAPI結果・出力未更新・有限値保証はVERIFY。 / 今回の独立静的監査 58/58 PASS。合成float32・比較モデルは原作ゲームGoldenではない。新規正式VERIFIED=0。正式TODO/VERIFY/BLOCKEDの書込差分は各0。Golden実測PASS=0、strict MATCH/完全複製率=未測定。 / 3. P1: 第二BGMベースディレクトリDAT_0068B38Cの書込元とパスサイズ上限は従来VERIFYを維持する。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-08H-P0-D3DX-CAMERA-GEOMETRY-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_08H_P0_D3DX_CAMERA_GEOMETRY_STATIC.md`; actual SHA256 `C58CE9D39BBE8964A5C1868ADAB68AA0FDAAF6BBE8D350391ECC2A65E955CE53` (5909 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_08H_P0_D3DX_CAMERA_GEOMETRY_EVIDENCE.json` SHA256 `969A0BDD6423DB2EEBD348CC0E2FE43A593509F7B7347FC02E9C1E353FF84C1E`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 07H報告では 0x00559990 の無上限ループ・FPU両誤差悪化停止と、float32停滞の合成例をSTATIC/VERIFY管理。今回はそれらを再取得・二重加算せず、**ループに渡る固定幾何入力を原作PE機械語から別途復元**した。原作実行、REA/Ghidra再実行なし。
  - 検索CLIで `function/callers/callees/related 0x00559990` を確認。直接親 `0x00559690`、CALL site `0x00559830` は旧DB/V9双方で一致。関数長915バイト、最後のRETは `0x00559D22`。
  - `0x00559A2A..0x00559A73` で組立てる3点を、x87のfld/fst/fstp・pushに伴うESP移動を追って復元した。
  - 3点は非共線で、平面方程式は **z=0**。`0x00559A73` のIAT `0x006092CC` は `D3DXPlaneFromPoints`。
  - 関数先頭の `0x005599D5..0x00559A1C` は、視点の上方向(0,1,0)、原点を見る基準点(0,0,0)、スクリーン座標の端点(0,0,0)・(0,0,1)を用意する。
  - 反復内 `0x00559B77..0x00559BA0` は Eye=(0,0,z)、At=(0,0,0)、Up=(0,1,0) の視点行列を作成。初期z=-2.0、各反復で約0.01減少。
  - `0x00559BCF` と `0x00559BFE` の2回の `D3DXVec3Unproject` は、同一画面位置(0,0)で深度0/1の2点を逆投影。続く `0x00559C1D` は `D3DXPlaneIntersectLine` でz=0平面との交点を計算し、結果のx/yを `0x00559C1F`、`0x00559C42` で読み出す。
  - PE定数: `0x0063B0E0`=45.0 (f64)、`0x0065C4C0`≈π/180、`0x0063B154`≈0.1 (f32)、`0x0063B0EC`=10.0 (f32)。
  - `0x00559B25` のFLD1によるaspect=1とともに、`0x00559B43` の `D3DXMatrixPerspectiveFovLH` へ渡す。従ってFOV≈45°、aspect=1、near=0.1、far=10。初期視点は面z=0から距離2で、near/far区間内にある。
  - IAT `0x006092F4=D3DXMatrixLookAtLH`、`0x006092DC=D3DXVec3Unproject`、`0x006092E4=D3DXPlaneIntersectLine` もPEインポートで独立照合。
  - 重点VERIFYを **GetViewport失敗/ゼロ寸法/非標準原点、D3DX逆投影失敗・NaN・平行線で交点未更新、射影行列非特異性** に限定して深掘りする。 `0x00559C1D CALL EBX` の戻り値は直後の `0x00559C1F FLD` より前に検査されない。
  - `0x00879838` は `0x00559D11` で計算値が書かれ、既存索引では `0x004C3C20` などが読取。画面変換の基準値候補として位置付け、実際のデバイス状態・厳密な値・不具合発生はVERIFYとする。
  - 次回: `0x00559A28` vtable+0xC0のGetViewport戻り値・出力値使用、`0x00559C1D` の交差失敗時pOut規約、`0x004C3C20` 等による `0x00879838` 消費者の追加ASM照合。すべて本owner範囲内で静的調査する。
- **Correction/remaining VERIFY:** 重点VERIFYを **GetViewport失敗/ゼロ寸法/非標準原点、D3DX逆投影失敗・NaN・平行線で交点未更新、射影行列非特異性** に限定して深掘りする。 `0x00559C1D CALL EBX` の戻り値は直後の `0x00559C1F FLD` より前に検査されない。 / `0x00879838` は `0x00559D11` で計算値が書かれ、既存索引では `0x004C3C20` などが読取。画面変換の基準値候補として位置付け、実際のデバイス状態・厳密な値・不具合発生はVERIFYとする。 / 5種: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY。新規5種完全取得0、新規正式VERIFIED0。旧64件保持、正式TODO/VERIFY/BLOCKED書込差分各0。原作Golden PASS0、strict MATCH/完全複製率は未測定。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-09H-P0-D3DX-VIEWPORT-RETURN-FLOW-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_09H_P0_D3DX_VIEWPORT_RESULT_STATIC.md`; actual SHA256 `63AA1E1CE0A73A7CAB71020D914BA5AD7AC69B303DAFA4C789C3425D1522E365` (6131 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_09H_P0_D3DX_VIEWPORT_RESULT_EVIDENCE.json` SHA256 `DF498298ECD528BB54714FB3DAAC385A0B2264756C88070E212FAC3DD17E7498`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 新規静的証拠と先行研究との区別
  - 07Hは0x00559990のFPUループの終了条件、08Hはz=0平面/理想幾何/通常約42反復の合成モデルを記録した。本回ではこれらの成果は破棄・二重計上せず、**vtable +0xC0の戻り値検査有無、スタック出力の実引渡し、失敗出力を消費する後段の新関数**を対象限定で原作PE機械語から調べた。原作実行・REA/Ghidra再実行はゼロ。
  - 関数0x00559990は保存Ghidra索引で915バイト、直親0x00559690の直接CALL siteは0x00559830（旧/V9 DB双方）。新規後段0x004C3C20は264バイト、旧/V9 DB双方に7直接CALL siteを確認した。
  - 0x005599E4 `LEA EDX,[ESP+0xF0]` → 0x005599EF `PUSH EDX`、対象グローバル0x0087980Cのvtable +0xC0を0x00559A22で取得して0x00559A28 `CALL EAX`。このスロットはDirect3DDevice9 GetViewport相当の候補。戻り値EAX/HRESULTを0x00559A2A以降で判定せず、次の平面・行列計算へ進む。
  - `S`=各stdcall呼出し前の安定ESPとすると、0x005599E4の出力バッファ候補は`S+0xF0`。D3DXVec3Unproject呼出し0x00559BCF/0x00559BFEの第3引数用`LEA [ESP+0xFC]`（その時点で12バイトPUSH済み）も同じ`S+0xF0`に対応する。したがってViewport出力がそのまま逆投影に入力されることをABI上確認。
  - 0x00559BCF, 0x00559BFEはPE IAT 0x006092DC=`D3DXVec3Unproject`をESIから呼ぶ。第1出力は`S+0xE4`、第2出力は`S+0xD8`。両方とも戻り値を条件分岐に使用せず、0x00559C1DのEBX（PE IAT 0x006092E4=`D3DXPlaneIntersectLine`）へ入力される。
  - 交差点出力は`S+0xCC`。0x00559C1D `CALL EBX`の**直後**0x00559C1F `FLD [ESP+0xCC]`、0x00559C42 `FLD [ESP+0xD0]`でx/yを読む。NULL相当の失敗返却や交点出力未更新の場合でも原作側に明示的な直後ガードはない。交点不成立の実際の到達性、FPU例外/NaNの挙動はVERIFY。
  - 初期化ループ終了時0x00559D11はfloat走査値を`DAT_00879838`へ格納する。旧検索FTSで別関数0x004C3C20がこの値を参照し、限定逆アセンブルで0x004C3C4F `FLD [0x00879838]`を確認。
  - 0x004C3C20は`[ESI+0x54]`、`[ESI+0x58]`を整数寸法として用い、0x004C3C93、0x004C3CBB、0x004C3CD9で`FIDIV`する。関数全体0x004C3C20..0x004C3D27にはCMP/TEST/条件分岐がなく、内部にゼロ寸法ガードは見えない。
  - 同関数はPE IAT経由で`D3DXMatrixScaling`(0x006092D8)、`D3DXMatrixTranslation`(0x006092F0)、`D3DXMatrixMultiply`(0x006092D4)を呼ぶ。直接CALL sites: 0x0048B2E6, 0x0048BBBA, 0x0048BEAF, 0x004C2D28, 0x00520546, 0x00520758, 0x005208BC（双方の検索DBで一致）。
  - ## 再実装・Goldenの実験設計（まだ未実行）
  - 0x004C3C20の7親のうち、幅/高さを+0x54/+0x58へ設定する経路を限定追跡し、ゼロ値到達性を判定。0x00559690のdevice設定からvtable +0xC0の実装同定・異常Viewportの発生条件、交差API失敗時のpOut契約を追加検証。後段の危険性は実測までVERIFY/NOT READY。
- **Correction/remaining VERIFY:** 交差点出力は`S+0xCC`。0x00559C1D `CALL EBX`の**直後**0x00559C1F `FLD [ESP+0xCC]`、0x00559C42 `FLD [ESP+0xD0]`でx/yを読む。NULL相当の失敗返却や交点出力未更新の場合でも原作側に明示的な直後ガードはない。交点不成立の実際の到達性、FPU例外/NaNの挙動はVERIFY。 / 5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規正式VERIFIED=0（既存64保持）、正式TODO/VERIFY/BLOCKED更新差分=0/0/0。原作Golden PASS=0。strict MATCH・完全複製率=未測定。 / 0x004C3C20の7親のうち、幅/高さを+0x54/+0x58へ設定する経路を限定追跡し、ゼロ値到達性を判定。0x00559690のdevice設定からvtable +0xC0の実装同定・異常Viewportの発生条件、交差API失敗時のpOut契約を追加検証。後段の危険性は実測までVERIFY/NOT READY。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-10H-P0-GAMEVIEW-SIZE-LINEAGE-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_10H_P0_GAMEVIEW_SIZE_ORIGIN_STATIC.md`; actual SHA256 `BA35DCAB19BDDBCA21950DCCFEE265729E16FD152D85184378D59E90D5B4FFF3` (4647 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_10H_P0_GAMEVIEW_SIZE_ORIGIN_EVIDENCE.json` SHA256 `AA66C9C9B7BD76404C27480139EB51BCBAAE8835EDF65336E884D7DD818877CD`.
- **Old owner's bounded static control-flow / ABI findings:**
  - ## 今回の新規発見（09Hの52条件とは別の42条件）
  - 前回09Hは `0x004C3C20` の `+0x54/+0x58` 分母と3箇所のFIDIVを特定した。今回は**分母の供給元をコンストラクタまで遡及**し、PE初期値・起動経路を新たに照合した。既存成果を破棄・二重計上していない。
  - 2. `0x004C29E0`（GameViewコンストラクタ、1029バイト）で、`0x004C2A22`が幅を読み、`0x004C2A27`が高さを読む。続く`0x004C2BB2`（`MOV [EBP+0x54],EAX`）と`0x004C2BB5`（`MOV [EBP+0x58],EDI`）でGameViewへ固定格納する。
  - 3. **さらに重要**: コンストラクタ自身も`0x004C2C96`で`FIDIV [EBP+0x58]`、`0x004C2CCB`で`FIDIV [EBP+0x54]`を実行する。つまりゼロ寸法があれば後段`0x004C3C20`以前にも数値異常が起こり得るが、到達性は未確認。
  - 4. `0x004B9E50`のCALL site `0x004B9EE5 → 0x004C29E0`、コンストラクタ内部`0x004C2D28 → 0x004C3C20`を旧/V9両DBで照合。後段の7直接CALL sitesも両DBで一致。
  - 5. 起動側`0x005554F0`で幅・高さの上書き8箇所（`0x005555E7/ED, 0x0055560F/19, 0x0055562C/32, 0x00555646/57`）を原作機械語で確認。表示モード、設定値、環境によって800×600から変化する。
  - 6. 保存済み検索DBの`0x00556250`疑似Cでは設定幅・高さを最低640×480、最大1600×1200へ制限する経路がある。`0x00557A20`疑似Cにもdebug_paperの値を同範囲へ制限する経路がある。**ここは機械語全分岐未検証のINDEX_ONLY**であり、全経路で寸法が必ず正になると証明したものではない。
  - ## 重要性と未確定条件
  - 正常な初期値（800×600）および確認した設定制限の存在により、09Hの「分母に0を渡せるか不明」はより限定されたVERIFYになった。単に`0x004C3C20`内にガードがないことは**ゲームのゼロ除算バグの証明ではない**。DisplayModeからの寸法代入・設定失敗・初期化順序・インスタンスの生存中更新・別の書込元を未検証。x87 FIDIVのゼロ分母は常に即クラッシュを意味しない（FPU制御ワード・例外マスク次第）。
  - `0x00556250`と`0x00557A20`の全寸法設定分岐・変換ヘルパー`0x005B7576`を原作機械語で限定検証し、DisplayModeからの0寸法伝播とGameView生成順を比較する。次にGameViewの`+0x54/+0x58`へ後から書込む経路の有無を型・インスタンス単位で調査する。安全な実機観測環境がない限りバグ確定せずVERIFYを維持。
- **Correction/remaining VERIFY:** 独立静的監査: **42/42 PASS**、失敗0。前回09Hの52/52および保存済みREA64/64は非加算で照合。新規正式VERIFIED=0、正式TODO/VERIFY/BLOCKEDのファイル更新差分=0/0/0、Golden=0。 / 開始時PC接続OK、owner active.lockなし、空きRAM約17GiB、Javaプロセス0、CPU負荷不明。REA/Ghidra/ゲーム/Workの新規起動0。監査単発約1.976秒、研究全体時間は厳密に未測定。 / `0x00556250`と`0x00557A20`の全寸法設定分岐・変換ヘルパー`0x005B7576`を原作機械語で限定検証し、DisplayModeからの0寸法伝播とGameView生成順を比較する。次にGameViewの`+0x54/+0x58`へ後から書込む経路の有無を型・インスタンス単位で調査する。安全な実機観測環境がない限りバグ確定せずVERIFYを維持。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

### REA-LOCAL-20261027-11H-P0-DIMENSION-PARSER-ABI-DISPLAY-GATE-STATIC-01

- **Source:** `rea_lab/decomp_task/REA_20261027_11H_P0_DIMENSION_ABI_GATE_STATIC.md`; actual SHA256 `00C8D3D0F01F4EA4ED18D5E5A59F73CE121FEF6F0AFB2EC3EA2A2C8453304DE2` (5657 bytes), checked this recovery.
- **Same-hour PC-only evidence:** `REA_20261027_11H_P0_DIMENSION_ABI_GATE_EVIDENCE.json` SHA256 `F6C13F39599AD2274AEE7D8DC5A5B2FA4A9BDFB50FED2FF03D58ECDF07A8A611`.
- **Old owner's bounded static control-flow / ABI findings:**
  - 前回10HはGameViewコンストラクタ`0x004C29E0`で幅・高さをコピーし、GameView生成中`FIDIV`があることを確認した。今回は前回未検証の`0x00556250`（起動引数）、`0x00557A20`（debug_paper）、`0x005B7576`（整数変換）、呼出元`0x005554F0`の原作機械語を限定検証した。
  - ## 新規発見1：Ghidra void誤推論3関数
  - `0x00556250`: Ghidraは`void __fastcall`と表示するが、`0x0055665E`で一時フラグを1、`0x00556764`で`MOV AL,[ESP+0x17]`として復帰。呼出元`0x00555519`がCALL→`0x0055551E MOV BL,AL`→`0x00555522 JNE`で使用する。
  - `0x00557A20`: Ghidraは`void`と表示するが、`0x00557DA5/0x00557E84`でフラグを1へ書き、`0x00557FD0 MOV AL,[ESP+0x1B]`で返す。起動側`0x00555524 CALL`→`0x00555529 MOV BL,AL`で使用する。
  - `0x005B7576`: Ghidraは`void`と表示するが、`0x005B757C JMP 0x005B7560`で`_atol`へtail-jump。`_atol`は`0x005B756C`で数値変換を呼び、EAXを変更せずRET。パーサ側`0x00556686/0x005566B9/0x00557D98/0x00557E77`はCALL後のEAXを画面寸法グローバルへ保存する。少なくとも返り値は32ビット整数として必要。
  - ## 新規発見2：設定ファイル・起動引数の寸法clampは符号付き
  - `0x00556250`は`0x005566D3/0x005566D9`等のCMP/JGE、`0x005566F7/0x005566FD`等のCMP/JLEにより、解析済みの`640<=width<=1600, 480<=height<=1200`を**signed x86比較**で実装する。
  - `0x00557A20`も`0x00557F27/0x00557F2D`等のCMP/JGE、`0x00557F50/0x00557F56`等のCMP/JLEで同じ範囲へ補正する。ただしファイル認識・行抽出・数値変換が成立したときの経路に限定する。
  - ## 新規発見3：DisplayModeは別経路で直接上書き
  - `0x005554F0`ではDirect3Dのvtable`+0x20`のCALL（`0x005555A8`）後、`TEST EAX,EAX`→`JNS`（`0x005555AA/0x005555AC`）でHRESULT負値だけを失敗判定する。
  - `DAT_0065BEE4==0`の経路は`0x005555DF/0x005555E3`でDisplayMode出力の幅と高さを取り出し、`0x005555E7/0x005555ED`でグローバルへ**そのままコピー**する。このコピー区間には非ゼロ・上下限の再検査がない。
  - 別のウィンドウ経路でも`0x0055563E/0x00555644/0x00555646`および`0x0055564F/0x00555655/0x00555657`で、設定値がDisplayModeの幅・高さより大きいとき値を引き下げる。ここも引下げ後の下限再clampはない。
  - ## 今回の監査・正式進捗
  - 次回は`0x005555A8`のDirect3D vtable+0x20をCOM interfaceの定義と原作初期化経路で突合し、DisplayMode構造体の幅・高さと`0x00555710`以降のDevice生成に渡る値を追跡する。必要なら画面モード条件ごとの未実測Golden fixtureをDESIGNED/NOT RUNで残す。
- **Correction/remaining VERIFY:** したがって、両パーサの範囲clampだけからGameViewの全実行経路の非ゼロ不変条件は証明できない。一方、HRESULT成功時にDirect3Dが幅または高さ0を返す実例もない。**実際のゼロ除算・クラッシュは未証明、VERIFY**。GetAdapterDisplayMode(+0x20)の正規COM割当は有力だが本報告の全vptr実体は未検証。 / 既存Wave1～5公式VERIFIEDは最終同期ログに基づく**64/64維持**。新規正式VERIFIED 0、正式TODO/VERIFY/BLOCKEDの更新差分0/0/0。5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規5種類完全充足0。原作ゲームGolden PASS=0、strict MATCH=未測定、完全複製率=未測定。 / 次回は`0x005555A8`のDirect3D vtable+0x20をCOM interfaceの定義と原作初期化経路で突合し、DisplayMode構造体の幅・高さと`0x00555710`以降のDevice生成に渡る値を追跡する。必要なら画面モード条件ごとの未実測Golden fixtureをDESIGNED/NOT RUNで残す。
- **Stage:** PUBLISHED_INTAKE upon GitHub source/readback, STATIC/VERIFY, formal five-method newly VERIFIED 0, game Golden PASS 0, READY 0. Previous refusals referenced in source remain safety-hold; no denied material included.

## Curation handoff

All detailed source passages belong to original owner and must be matched by SHA before formal adoption. Differences among CALL E8, indirect virtual dispatch and E9 tail transfer must be preserved. Current V9/PE native call evidence outranks older V3 guesses; cross-hour overlap is not new function identity. No blocked requests, original game binaries, forbidden VA evidence, secrets, or raw generated SQLite were added. Curator alone owns canonical develop REF/dictionaries and tests; the present work makes original findings discoverable without promoting accuracy. Source IDs are non-overlapping with the previous owner-index snapshot.
