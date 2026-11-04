# REA｜2026-10-31 11H｜Vorbis codebook look変換・借用参照消去・確保失敗分岐（P0）
研究ID: `REA-LOCAL-20261031-11H-P0-VORBIS-LOOK-CONVERSION-ALLOCATION-GATES-STATIC-01`
owner=REA / task=T015 / **PC-SAVED / STATIC + INFERRED / VERIFY / NOT READY**。
先行09H→10Hの正規差分検証。旧発見と今回の調査結果を新規正式VERIFIEDへ二重計上しない。

## 事前照合・source
- MASTER・分析レーン規約・REA README/QUEUE/PROGRESS、既存10H/09Hの証拠・readback、`logs/progress_sync_20261011T153958076Z.json`を確認。古いPROGRESSの15/16表示はSTALE_RENAME_DENIEDで正式同期値ではない。
- 原作と同一SHAの研究専用PE `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。read-only SQLite quick_check=ok。
- 非公開GitHub KB develop のPRIVATE、`KNOWLEDGE_CURATION_PROTOCOL.md`、`REF_AUDIO_VORBIS.md`、`GHIDRA_V9_COVERAGE_REPORT.md`を読取専用で確認。PC knowledge README/SYNC_STATUS、kb addr/docs/research/findも照合し、本VAの登録・全文索引hitなし。
- 旧 `search_index/README.md`/`BUILD_MANIFEST.json` は現行rootに存在せず、正式研究入口は `00_START_HERE_UNIFIED_V9_20261023.md`。V9検索CLIは動作。専用 `v9_coverage.py` は指定のローカル候補pathに存在せず、native E8/PEとV9 CLI・SQLiteをread-only照合（--export不使用）。
- 先行10H本体46/46・独立readback29/29を確認。今回 `active.lock`なし、Java/Ghidra競合なし。空き物理メモリ確認時約14.88 GiB、CPU負荷/全体作業時間不明。REA/Ghidra/原作ゲームの起動0。

## 新規差分 A：borrowed +0x0C は正常変換前に初期化で消える
- `0x005D5922 E8 -> 0x005D9F40` はコードブックを入力に、`inner+0xB20+0x38*i` のlookレコードを初期構築。 `0x005D9F55` が `look+0x0C` に元codebookポインタを保存（先行10Hで確認したborrowed参照）。
- 同じlookレコードの変換は `0x005D5B51 E8 -> 0x005DA070`。後者入口の `0x005DA07C..0x005DA082` は `memset(look,0,0x38)` を行う。すなわち**通常の逐次変換に達した場合は旧borrowed +0x0Cをクリア**し、先行参照を引き継がない。
- `0x005DA070` が成功0を返すと `0x005D5B59/5B5B` が成功側へ進み、`0x005D5B60`で元codebookを解放、`0x005D5B6C`で元所有者スロットをゼロ化する。旧borrowed参照がこの成功経路で保持されるという懸念を狭めた。
- ただし別のowner/aliasや再入、初期化前の参照、非同期アクセスまで安全性を証明したものではない。旧10Hの解放順調査も再計上しない。

## 新規差分 B：最初の失敗処理と後続4確保の非対称
- `0x005DA0C7` の `0x005D97C0` 戻りポインタは `0x005DA0E9/0x005DA0EB` でNULL検査され、NULLなら `0x005DA0EE -> 0x005D9ED0` cleanup、`0x005DA0F6` のEAX=-1で終了する。これが**局所的に確認できた明示的失敗ゲート**。
- これに対し `0x005DA1A7` (malloc→`look+0x14`)、`0x005DA224` (malloc→`look+0x18`)、`0x005DA255` (malloc→`look+0x1C`)、`0x005DA2D4` (calloc→`look+0x20`) は、戻り値を保存した直後に明示的NULLテストがない。
- 書込・参照例: `0x005DA201` (`+0x14`)、`0x005DA24A` (`+0x18`)、`0x005DA287` (`+0x1C`)、`0x005DA393/0x005DA52A` (`+0x20`)。いずれも**正のcodeword数などの入力条件を満たす場合にのみ**該当参照へ進む。確保失敗時の局所NULL参照候補だが、実クラッシュ・悪用可能性は未確認。
- 入口 `0x005DA0B6/0x005DA0B8` は有効エントリ数0なら `0x005DA53D` のEAX=0へ早期分岐し、後続4確保へ進まない。したがって全てのVorbisコードブックで失敗すると言わない。
- `0x005DA070` は0x38レコードを構築する変換担当。Ghidra V9の疑似Cは機械出力で、関数は5個の非連続range・合計1223 body bytes、native ABI=未確定。厳密な例外到達性は原機械語の全CFGと別の独立検証が必要。

## 独立監査
- `REA_20261031_11H_P0_VORBIS_CONVERSION_PROBE.py`: source PE/V9のSHA256一致条件付き、局所Capstone逆アセンブルを読み取り専用で表示。
- `REA_20261031_11H_P0_VORBIS_CONVERSION_AUDIT.py`: V9 SQLiteのquick_check・native E8 site 11件とPE bytes照合・元ASM 25点・先行10Hの46/46・29/29をチェック。**52/52 PASS、1.8011秒**。自己監査成功は実ゲーム成功と無関係。
- `REA_20261031_11H_P0_VORBIS_CONVERSION_EVIDENCE.json`: 11 call siteのbytes/target、25命令bytesとoperand、8つのPE window SHA256、各52判定、先行研究ID、元ソースSHAを保存。
- REA正式5種（info/pseudo/assembly/callers/callees）新規完備0／新規VERIFIED0。既存正式STATIC VERIFIED **64/64維持**、正式TODO/VERIFY/BLOCKED差分0/0/0。原作Golden実測PASS0、完全複製率未測定。
- 新規安全拒否・接続失敗なし。指定 `v9_coverage.py` 不存在はツール配置差異（OTHER/VERIFY）、既存の検索CLI/SQLiteで独立検索を継続し、禁じられた再解析や--exportは実行せず。

## KB_CANDIDATE（専任統合担当の審査待ち）
- ID: `REA-LOCAL-20261031-11H-P0-VORBIS-LOOK-CONVERSION-ALLOCATION-GATES-STATIC-01`、owner REA/T015。先行 `REA-LOCAL-20261031-10H-P0-VORBIS-CODEBOOK-OWNERSHIP-TEARDOWN-STATIC-01` の差分。
- VA/CALL: `0x5D5922->0x5D9F40` (borrowed `+0x0C`)、`0x5D5B51->0x5DA070` (0x38 memset)、`0x5D5B60` (source free)、`0x5D5B6C` (source slot=0)。確保/書込の4系列VAは上記。
- 証拠: 本報告と `REA_20261031_11H_P0_VORBIS_CONVERSION_EVIDENCE.json`、独立source SHA/命令bytes、V9 PE verified E8、先行10H証拠。新規要点は**同一lookレコードの古いborrowed参照消去を成功分岐と接続**した点、および変換段階4確保の局所ガード差。
- 確度: clearingとCALL先はSTATIC、同一レコードの正常逐次到達/失敗後NULL参照候補はINFERRED/VERIFY。DYNAMIC=NO、Golden=0、READY=NO。疑似CからABIを確定しない。
- 既知差異: 旧検索root manifest/READMEは現行V9では移転済み。研究ファイル本体がknowledge全文索引に載らないことを「未研究」と断定しない。未解決: 空きメモリ枯渇時の入力前提、他所有者alias、異常終了とEH、実ゲーム可観測性。
- 共有knowledge/MASTER/A-E/Git/原本/QUEUE/PROGRESS/既存RUNは変更しない。新規REA担当所有ファイルだけに保存。

## 次の安全な再開位置
`0x005DA070` の `0x005DA1A7/0x005DA224/0x005DA255/0x005DA2D4` から書込までの全CFG、`0x005D58E7` look配列calloc後のガード、`0x005D3DE0` のteardownと `0x005D9ED0` の部分構築cleanupを区別して追加静的検証する。関係VA/既存研究IDを先に照合し、正式REA再実行や原作ゲーム実行なしで進める。
