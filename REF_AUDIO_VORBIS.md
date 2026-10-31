# Native Ogg/Vorbis header parsing — curated REA/T015 source map

Scope: original ver0.67 PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; composite V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`.
All findings below are bounded original-x86 **STATIC**. Branch reachability under real allocation failure, ABI, crash behavior, recovery, and observed gameplay remain **VERIFY**. Original-game Golden PASS **0**, strict MATCH **0**; owner READY **0**.

## 1. Parent header-error mapping (04H, not another router discovery)
- `0x005CF010` calls header router `0x005D44C0` at `0x005CF167` and `0x005CF279`. The first call's nonzero result goes through `0x005CF1E9` (`EDI=-133`) and cleanup, masking the specific router error; the second preserves its return value in `EDI` and returns it through `0x005CF206`. Do not assume all Ogg header errors retain their original code.
- Both branches converge on native cleanup calls `0x005CF1F2 -> 0x005D3DE0`, `0x005CF1FB -> 0x005D3D00`, with state `outer+0x58=2` at `0x005CF20A`. Separate packet-I/O error paths must not be attributed to router behavior.
- Source/owner: REA ID `REA-LOCAL-20261031-04H-P0-VORBIS-PARENT-ERROR-NORMALIZATION-STATIC-01`; `rea_lab/decomp_task/REA_20261031_04H_P0_VORBIS_PARENT_ERROR_NORMALIZATION_STATIC.md`. Existing 02H/03H header-router/type results are antecedents, not newly counted findings. Original-PE window `0x5CF150..0x5CF290` independent SHA256 `62AF0C962E6B1D7BFA3AD2E13467BE1C07F8220EC001E24F9B7CE5002A569CD2`.

## 2. Type3 comment parser and conditional allocation guards (05H)
- `0x005D4030` parses a type3 comment header. Its native `0x005D4061` calls `_calloc` (`0x005D1C71`) and stores the result to `ESI+0xC`; for vendor length >0 it writes through that pointer at `0x005D407D` without a preceding local null check. A length-zero branch bypasses this write. **Potential null-write path is static, not a measured game fault.**
- With comment count >0, two further allocation calls `0x005D40BE`/`0x005D40C8` precede array stores `0x005D4112`/`0x005D411C` without local null checks; per-comment calloc at `0x005D4115` feeds the later `0x005D3CB0` helper. The zero-vendor/zero-count route and subsequent type5 vendor-pointer check (`0x005D455B`) are conditional and untested dynamically.
- CRT `_calloc` (`0x005D1C71`) calls `0x005C303C`, which invokes heap allocation and checks for null at `0x005C3085`. These CRT helpers were already identified in V9; do **not** count them as two new game-semantic discoveries or auto-rename them.
- Source/owner: REA ID `REA-LOCAL-20261031-05H-P0-VORBIS-CALLOC-NULL-GATE-STATIC-01`, `rea_lab/decomp_task/REA_20261031_05H_P0_VORBIS_CALLOC_NULL_GUARD_STATIC.md` and its evidence JSON (owner static QA 56/56; no gameplay). Independent PE-window SHA256 `0x5D4030..0x5D4160` = `6F8B35B6949E04FCD340738CFCBBEAA66DDE342ED16FD320783ACF9978EE25E7`. V9 name/address is an index, not a passed Golden test.

## 3. Remaining validation and indexing boundary
- REA research under `rea_lab/decomp_task/` is **outside** the intentionally shallow `research_index.py` corpus; neither the 04H nor the 05H original text was silently bulk-indexed. These explicit source links are curated read-only references, not full-text inclusion.
- Confirm real input states, allocator/new-handler lifetime and parent handling in separately authorized tests; do not equate native potential null dereference with demonstrated exploitability, reproduction or safe failure. Owner's synchronized 5-method completeness and E-MASTER READY counts remain unchanged.
- Preserve earlier 04H index-path ENOENT and 05H PowerShell CLI argument encoding error as **OTHER/VERIFY**, not as missing findings or a safety refusal. Do not reroute blocked evidence through another tool or path.

## 4. Type3 comments: 配列と部分構築cleanup（REA 06H）
- 0x005D4030はcount+1個のpointer配列とlength配列をcallocする。成功時だけ末尾1枠がゼロ初期化され、格納構造体は+0（文字列配列）、+4（長さ配列）、+8（count）、+0xC（vendor）。0x005D3D00は非NULL要素・配列・vendorを解放して4 fieldをゼロ化する。0x005D3CB0は長さ0なら早期終了、正ならbitreaderからbyte-copy。先行05Hのcalloc NULL未検査は依然VERIFY。
- REA/T015 ID REA-LOCAL-20261031-06H-P0-VORBIS-COMMENT-SENTINEL-TEARDOWN-STATIC-01、source rea_lab/decomp_task/REA_20261031_06H_P0_VORBIS_COMMENT_SENTINEL_TEARDOWN_STATIC.md。安全な二重cleanup・異常入力時の実到達は推定にとどめる。

## 5. Codebook確保失敗と所有権（REA 09H–10H）
- 09H: 0x005DA604/0x005DA6D6でcodebook+0x08、0x005DA811で+0x20にmalloc戻り値を格納。正の要素数で書込へ進む場合の局所NULLチェックは未確認。0x005D9E70 cleanupはmarker+0x24を見て+0x20/+0x08の非NULL分をfreeし、fieldsをゼロ化して本体解放。cleanupが後ろにあることは先行NULL参照を防ぐ証明ではない。
- 09H: CRT 0x005B9BC8はmalloc(0)をサイズ1へ正規化する経路とnew-handler再試行候補を持つ。「0要素ならNULL」という推論を訂正。失敗頻度・CRT mode・実クラッシュは未観測。
- 10H: 0x005D57C0はinner+0x720のowned codebookを入力に、inner+0xB20の0x38-byte lookを構築。0x005D9F55はlook+0x0Cに元codebookを保存（借用参照とINFERRED）。0x005D9ED0はlookの+0x10..+0x20の保有領域を解放して0x38バイトをゼロ化するが、borrowed+0x0C自体をfreeしない。
- 10H: 0x005D5B51の変換が0を返すと0x005D5B60で元codebookをfreeし0x005D5B6Cで元slotをzeroにする。失敗時は残存非NULL slotsを再走査し解放/zero。正常逐次経路での二重free回避は条件付き推論で、alias・部分初期化・再入保証は無い。
- IDs: REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01、REA-LOCAL-20261031-10H-P0-VORBIS-CODEBOOK-OWNERSHIP-TEARDOWN-STATIC-01。sources rea_lab/decomp_task/REA_20261031_09H_P0_VORBIS_CODEBOOK_MALLOC_CLEANUP_STATIC.md; rea_lab/decomp_task/REA_20261031_10H_P0_VORBIS_CODEBOOK_OWNER_STATIC.md。
- 10H独立原作PE-window SHA256: 0x005D3DE0..0x005D3F60 = A9D7CDB38DA170F3D7FBA17F280C4EC1037716B03ABDE44DEA88B531600B6F51; 0x005D9ED0..0x005D9F37 = 7DF64C41C5A7369E9C31FFD8A3A57563FA9D3B603EC2ED50127A6E34C5F21F4D。

## 6. Look変換で借用参照消去・確保guard非対称（REA 11H）
- 0x005D5922→0x005D9F40はlook+0x0Cへ元codebookを保存。通常逐次変換0x005D5B51→0x005DA070に入ると0x005DA07C..82のmemset(look,0,0x38)で古いborrowed参照も消去する。成功0の後0x005D5B60/6Cで元codebookのfreeとslotゼロ化に進む。10H所有権報告とは独立した「変換開始時の借用参照クリア」のみ追加計上。
- 0x005DA0C7の最初の確保結果には明示NULL gateとcleanup→-1失敗分岐がある。一方0x005DA1A7/0x005DA224/0x005DA255/0x005DA2D4の後続確保は直後の明示NULL gateが見つからない。書込は正の入力数等で条件付き、entry数0なら4確保へ進まない。実クラッシュや脆弱性の証明ではない。
- ID REA-LOCAL-20261031-11H-P0-VORBIS-LOOK-CONVERSION-ALLOCATION-GATES-STATIC-01、source rea_lab/decomp_task/REA_20261031_11H_P0_VORBIS_LOOK_CONVERSION_STATIC.md。証拠JSONの8窓SHA/11 E8と原作PE readback一致（10Hも7窓/9 E8一致）。
- 原PE命令とCALLはSTATIC、逐次到達・allocator失敗・別名・ABIはINFERRED/VERIFY。REA 5種正式COMPLETE増分0、原作Golden PASS=0、strict MATCH=0、READY増分0。原本バイナリ・音声・実行ログはGitHubへ送らない。
