# 迫真戦記 REA｜2026-10-29 11H Ogg codebook符号復号・symbol表・ビットカーソル
研究ID: `REA-LOCAL-20261029-11H-P0-OGG-CODEBOOK-SYMBOL-BITCURSOR-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規REA正式VERIFIED=0、ゲームGolden=NOT RUN。

## 先行証拠・競合の照合
- PC LocalでMASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、共通作業ルール、REA README/QUEUE/PROGRESS、既存run一覧、最新有効sync、10H報告・EVIDENCE・readback、索引README/BUILD_MANIFESTを先読。10Hのmode0所有権およびcodebook 3 consumerの発見を二重計上しない。
- 対象は隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索DB `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。双方実測一致、SQLite quick_check=ok。
- 現在の有効sync `progress_sync_20261011T153958076Z.json` はWave1～5=**64/64 STATIC VERIFIED**（16+10+10+12+16）。QUEUE/PROGRESSはEPERMによる古い表示のため正式数へ使わない。開始前後 active.lock無し。先行Java/Ghidra無し。PC接続正常、開始時空きRAM約16.26GiB。
- 11H同名成果の事前存在なし。10/28 Library未同期記録は未統合のまま。新規REA/Ghidra、ゲーム、Workは実行せず。

## 新規のP0静的根拠：bitstreamから元symbolへの変換
- `0x005DA070` はcodebook entryを0x38バイトに初期化し、`0x005DA1AC`で `entry+0x14`（ソート済code境界の配列）、`0x005DA229`で `entry+0x18`（元symbol番号へのmap）、`0x005DA25F`で `entry+0x1C`（正code長配列）、`0x005DA2DC`で `entry+0x20`（高速lookup表）を格納。 `+0x24` は最初のbit peek幅、`+0x28` はfallback長さを保持する（局所x86命令と既存疑似C一致）。
- `0x005DA930` はまず `0x005DA94A` → `0x005E6CF0` で `entry+0x24` bitをpeek。非負のfast-table entry（`entry+0x20`）なら `0x005DA982` → `0x005E6DB0` で消費して **symbol内部index** を返す。負のentryやpeek失敗時は `entry+0x28` 幅から段階的に減らし再peekし、`0x005DA9D5` → `0x005DA8D0` でbit反転した値を `entry+0x14` 閾値表と比較してindexを選ぶ。code長は `entry+0x1C` を使用。bit不足が残れば **-1** を返す。
- `0x005DAA60` は入口で `entry+8` の正件数を検査（`0x005DAA67`）、`0x005DAA72` から `0x005DA930` を呼ぶ。非負indexなら `0x005DAA7E / 0x005DAA81` で `entry+0x18` の元symbol mapを読んで返す。件数0またはdecode負値は `0x005DAA87` で **-1** に統一。つまり `0x005DA930` のindexをそのまま元symbol番号として扱う実装は誤り。
- `0x005DAD60` は `0x005DAD8B` と `0x005DADE5` の2箇所で内部indexを直接取得し、`entry+0x10` の浮動小数ベクトルにstride（entry先頭の次元数）を掛けて加算。 `0x005DAD93 / 0x005DADED` で **-1** と比較してエラー帰還。元symbol mapへ変換する `0x005DAA60` とは契約が異なる。

## 関数・CALL関係と限界
- 索引の `0x005DA930` 直接CALL siteは `0x005DAA72`, `0x005DAD8B`, `0x005DADE5` の3件。下位のbit peek `0x005E6CF0` はbit数>32や残bit不足で `0xFFFFFFFF` を返し、bit消費 `0x005E6DB0` はカーソル・bit位置を更新する（既存Ghidra疑似C；動的fixture未実施）。
- `0x005DAA60` の直接CALL元は `0x005E06C0`、`0x005E0DC0`、`0x005E2A80`（後者は2 site）の計4 site。対照的に `0x005DAD60` の直接CALL元は**0件**。これは間接呼び出しの不存在を示さず、実ゲームの到達証明でもない。
- 組合せが重要：decoded index→元symbol map (`+0x18`) は整数値取得の `0x005DAA60`、decoded index→vector (`+0x10`) は `0x005DAD60`。これを一律にsymbol番号として扱う再実装は構造上誤る。+0x10 vectorの初期化/寿命、invalid selector・OOM・bitEOFの完全な異常系、関数ポインタ/RTTI到達は**VERIFY**。
- 設計すべきGolden：empty codebookの-1、fast lookup成功、長符号fallback、bit不足から-1、index→元symbol mapping、vector次元毎の加算、読込cursor最終位置を独立fixtureとする。**条件設計のみでゲームGolden実測PASS=0**。

## 検証格付け・作業状態
- `REA_20261029_11H_P0_BITBOOK_SYMBOL_ABI_PROBE.py` ではなく、実在する `REA_20261029_11H_P0_BITBOOK_ABI_PROBE.py` で隔離EXEをCapstone独立局所読取。 `REA_20261029_11H_P0_BITBOOK_SYMBOL_AUDIT.py` はEXEとDBのSHA、SQLite健全性、旧syncと10H結果、索引7関数、CALL 9 site、direct-caller件数3種、対象ASM20地点、lock前後を照合。**47/47 PASS、監査0.747秒、終了コード0**。EVIDENCE.jsonに各証拠を保存。
- 初回監査の命令位置期待値1件を `0x005DADF0`（実際はJE）から実際のCMP `0x005DADED` に修正し、独立Capstone出力に整合させ再検証済み。これは監査スクリプトのオフセット誤記であり、原作不具合や新しい研究成果として計上しない。別件のPowerShell 5 `ConvertFrom-Json` 文字エンコードエラーは既存sync読み取り時だけで、Python UTF-8解析により回避ではなく正規の文字コードを明示した読み戻しで成功。
- **5種証拠**：info=既存検索DB関数入口/size、pseudo=既存Ghidra擬似C、assembly=対象EXE局所Capstone、callers/callees=既存DB direct CALL。新規REA正式5種証拠一式=**0**、新規正式VERIFIED=**0**。既存Wave1～5 **64/64**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。完全複製率不明。
- CPU負荷と研究全体所要時間は未測定（監査時間のみ0.747秒）。旧RUN・QUEUE/PROGRESS・MASTER・他レーン・原本・索引DB・Git・公開先・スケジュールを変更しない。REA所有領域への新規ファイルのみ保存。
- **次のP0**：`0x005DAA60` の直接caller `0x005E06C0 / 0x005E0DC0` で元symbol値の利用先・-1扱いを追う。並行して `0x005DAD60` の間接dispatch table候補をread-only照合し、直接caller=0を到達不能と誤読しない。
