# REA｜2026-10-31 10H｜Vorbis codebook所有権・解放順と借用ポインタ（P0）
研究ID: `REA-LOCAL-20261031-10H-P0-VORBIS-CODEBOOK-OWNERSHIP-TEARDOWN-STATIC-01`
owner=REA / task=T015 / **PC-SAVED / STATIC + INFERRED / VERIFY / NOT READY**。
これは09H `REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01` の所有権調査の差分。01H tag guard、22Hの間接callは新発見として再計上しない。

## 先行照合と安全な範囲
- MASTER、分析レーン規約、REA README/QUEUE/PROGRESS、既存RUN `logs/progress_sync_20261011T153958076Z.json`、09H証拠・01H tag writer、knowledge README/SYNC_STATUS、KB addr/docs/researchを読取専用で確認。
- GitHub private `ButaMonky/Hakushin067-Research-Knowledge` のdevelopから `REF_AUDIO_VORBIS.md`・coverage・curationを読取専用で確認。統合V9 `tools/v9_coverage.py --inspect` もread-only実行、--exportなし。共有knowledge等は更新しない。
- 原作と同一SHAの専用PE: `rea_lab/targets/hakushin067_Vahren.exe`, SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`、SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- 事前 `active.lock`なし、09H/10H成果の名前競合なし。Ghidra・REA・原作ゲームは実行せず。CPU/RAM負荷は取得できず不明。

## 差分1：borrowedとownedの区別
- `0x005D57C0` の構築経路では、codebook所有者の `inner+0x720` 配列を入力に `inner+0xB20` の0x38-byte lookレコード配列を作る。
- `0x005D5922 E8 -> 0x005D9F40`。本体の `0x005D9F55: mov [edi+0x0C],esi` は **元のcodebookポインタをlookレコード+0x0Cへ保存**。新規複製・参照カウント増分はこの操作にはない。所有権観点では借用参照（INFERRED）。
- この構築経路では元codebook自体を解放しない。対して後述の変換経路では変換成功後に元codebookを解放し、所有者スロットをゼロ化する。両経路の違いを保存済み機械語で確認した。
- `0x005D9ED0` はlookレコード+0x10/+0x14/+0x18/+0x1C/+0x20をNULL検査して個別解放し、その0x38バイトをzeroにする。借用元+0x0Cは解放しない（対象全103バイトの局所ディスアセンブルとV9疑似Cを照合）。

## 差分2：変換成功・失敗時のowner slot
- `0x005D5B51` でlookレコード変換 `0x005DA070` を呼ぶ。戻り値0のみを成功扱いし、`0x005D5B60` で元codebookを `0x005D9E70` に渡して解放、`0x005D5B6C` で対応する `inner+0x720+4*i` スロットへ0を代入する。
- 変換失敗または入力スロットがNULLの場合は `0x005D5B89` へ分岐。配列を再走査し、各非NULLスロットを `0x005D5B9D` で解放、`0x005D5BA5` で0化、`0x005D5BB8` で新規構築中の状態を `0x005D4AE0` へ渡し、-1を返す。すでに成功し0化したスロットは再走査で再解放しない。
- **正常な一意ポインタ・逐次制御という前提では**、成功済みスロットを失敗時に二重解放しない。複数スロットの別名・非同期書込・部分初期化・確保失敗は未実証であり、全面的なdouble-free不可能とは言わない。

## 差分3：全体teardownと先行間接CALL
- `0x005D3DE0` は `param_1[7]` が非NULLの場合のみ対象innerを解放。 `0x005D3ECC` で `inner+0x720` の非NULL codebookを解放、`0x005D3EE4` で `inner+0xB20` のlookレコードを後始末、`0x005D3F04` でlook配列を解放。最後に `0x005D3F35` でinner領域を解放し、`0x005D3F44..0x005D3F58` で親の8 dwordを0化する。
- `0x005D3E3C`、`0x005D3E6E`、`0x005D3EA7` は型別関数テーブルを参照する間接CALL。テーブル基底は `0x00612E6C/0x00612E58/0x00612E60`、selectorは各 `[edi-0x100]`。**01H/22H既知事象の追加接続**であり新規発見数には加えない。局所cleanup内にselector範囲検査は見つからないが、先行01Hでは通常writer側にtag上限検査を確認済み。別writer・破損等はVERIFY。
- `v9_coverage --inspect`: `0x005D3DE0` はnative E8 caller 5 / outgoing 6 / 未解決owner site 3、`0x005D57C0` はcaller 1 / outgoing 24 / 未解決owner site 2。いずれも正式symbols未登録・ABI未確認。索引docs=0はREA所有原本を全文索引していないことと両立する。

## 検証・復旧
- 新規read-only Capstone PE + SQLite V9独立照合 `REA_20261031_10H_P0_VORBIS_OWNER_AUDIT.py`：**46/46 PASS**、0.878秒。native E8/関数range/ASM/zero化/借用ポインタ/cleanup対象を照合。
- 一部旧PROGRESSはEPERMで古い。正式5種証拠の進捗は `logs/progress_sync_20261011T153958076Z.json` の **64/64** を維持。今回新規5種完備0、新規VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0。原作ゲームGolden実測PASS0、完全複製率未測定。
- 非致命的環境差異：`psutil` は研究PCのPythonに未インストール（`ModuleNotFoundError`）。`RECOVERY-REA-20261031-10H-PSUTIL-ENV-01`、分類OTHER。依存導入はせずCPU/RAM計測は不明。分析と証拠保存には影響しない。新規安全拒否・接続障害は発生なし。
- MASTER/QUEUE/PROGRESS/既存RUN/A〜E/原本/共有knowledge/Git/スケジュールの変更0。REA担当内の新規ファイルだけに保存。

## KB_CANDIDATE（未承認・共有辞書未反映）
- owner REA/T015、差分IDは本書冒頭。元codebookポインタは `inner+0x720` のスロットが所有。look `inner+0xB20` の各0x38-byteレコードは、`0x005D9F55` で `+0x0C` に元codebookポインタを借用保存。変換成功/失敗時の所有者スロット解放+ゼロ化は上記VA。STATIC/INFERRED/VERIFY、READY=NO、Golden=0。
- 出典: `REA_20261031_10H_P0_VORBIS_CODEBOOK_OWNER_EVIDENCE.json` の検査ごとの命令bytes、E8、7領域の独立PE-window SHA256とV9 hash。訂正: 先行01Hのtag上限検査を尊重し、通常経路での表外参照を新規断定しない。

## 次回の安全な再開位置
`0x005DA070` の戻り値ごとの動的所有権ではなく、まず静的に成功/失敗分岐と `0x005D9ED0` が保有する `+0x0C` 借用ポインタの生存期間を追跡する。とくに `0x005D3DE0` の先行3間接CALLでtag/同一pointer aliasが保持されるか、別write xref・cleanup例外パスをV9/PEで範囲限定してVERIFY。ゲーム原作や新REAは起動しない。