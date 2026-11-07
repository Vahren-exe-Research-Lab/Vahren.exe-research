# 迫真戦記ver0.67｜REA独立静的研究｜2026-11-01 07時台（JST）

**研究ID:** `REA-OFFLINE-20261101-07H-P0-VORBIS-MODE-ZEROED-SLOT-CLEANUP-BOUND-STATIC-01`  
**owner/task:** `REA / T015`  
**状態:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**原作Golden実測PASS / strict MATCH / READY:** `0 / 0 / 0`。完全複製率は未測定。

## 実環境・先行記録・重複照合

最初に研究PCの `rea_lab/decomp_task/PROGRESS.md` へDesktop Commander Local Compactで読取を試みたが、MCP接続が `UNAVAILABLE: MCP SSE probe returned 429 from openai.org` となり失敗。これは**接続・レート制限系の一時障害**であり、安全拒否ではない。復旧ID：`REA-RC-20261101-07H-LOCAL-MCP-HTTP429-01`。PCオンライン/オフライン実態、CPU/RAM、active.lock、進行中REA、owner権限、最新QUEUE/PROGRESS、現行統合V9実体は**確認できなかった**。別経路で同一PC操作を試していない。PCへ保存成功とみなさない。

続行可能な静的作業として、実在するChatGPT Library版 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe` の読取専用コピーを隔離コンテナに展開した。ZIP CRC PASS、旧 `search.sqlite` の `integrity_check=ok`、元PEのSHA256一致、旧DB・ZIPのSHA256一致。ZIP内の `research_snapshot/MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、旧 `rea_lab/decomp_task/PROGRESS.md` と旧検索README/manifestを参照した。ただし旧PROGRESSは2026-10-09時点の15/16 VERIFIED・1 TODOを指し、2026-10-31以降の64件履歴や現在の正式値に置き換えない。旧パックには最新RUN/QUEUE/ownerの実体はない。

GitHub private `ButaMonky/Hakushin067-Research-Knowledge` の `develop` を読取専用で照会した。`KNOWLEDGE_CURATION_PROTOCOL.md`、`SYNC_STATUS.md`、`GHIDRA_V9_COVERAGE_REPORT.md`、`REF_AUDIO_VORBIS.md`、`symbols.tsv`、`structs.tsv` にある対象VA/旧研究を照合した。現行V9本体はPC側のみなので未再検証。`REF_AUDIO_VORBIS.md` に今回の `0x005D3DA0` 内部0xE50初期化・mode領域の有界ゼロ初期化を独立した結論として記した部分は見当たらなかったが、PC側の全資料との完全非重複は未確認。

従前の `REA-OFFLINE-20261101-06H-P0-VORBIS-MODE-ALLOC-LIFECYCLE-STATIC-01` の**mode個別calloc失敗→0x005D4398のNULL由来書込候補**は既存成果として参照するのみで再計上しない。今回の差分は、その**前段に作られる内側構造体のゼロ初期化と、最大64スロットに対する部分解放の安全条件**である。

## 新規P0静的差分：modeスロットのゼロ初期化・境界・cleanup

`0x005CF010` の `0x005CF06B: call 0x005D3DA0` からセットアップ用内側構造体の初期化へ入る。`0x005D3DA0` は `0x005D3DB7: push 0xE50`、`0x005D3DBF: push 1`、`0x005D3DC4: call 0x005D1C71 (_calloc)` により **0xE50バイト**を確保し、戻り値を `0x005D3DCC` で外側 `+0x1C` に保存する。さらに `0x005D1C71 → 0x005C303C` のCRTへ辿ると、`0x005C3077: push 0x8` により **HeapAllocのHEAP_ZERO_MEMORYフラグ**を指定していることを原作命令バイトで独立照合した。したがって、**この割当が成功した場合**、内側構造体は全バイトがゼロで初期化される。

`0x005D4160` は入口 `0x005D4168` で外側 `+0x1C` を読み、`0x005D416B..0x005D416F` でNULLなら早期失敗する。このチェックがあるため、上記**内側構造体の確保失敗**は、ここでmodeスロット書込に直行することを防ぐ（別呼出経路や別スレッドの変更は未検証）。

同パーサ `0x005D4357..0x005D4368` では6bit読取値に1を足し、内側 `+0x08` にmode件数を保存、0以下ならabortへ分岐する。通常の6bit読取成功時、件数は **1～64**。modeポインタ配列は内側 `+0x20` から4バイト刻みで、最大64件の末尾は `+0x11C..+0x11F`。次のフィールド開始 `+0x120` を侵食せず、構造体全体 `0xE50` に収まる。成功した初期callocにより、まだ処理していないスロットも最初はNULL。

modeループは `0x005D4384` で各16バイトを確保し、`0x005D438C` で個別ポインタをスロットへ格納する。検証エラーが**通常のパーサabort経路**へ進むと `0x005D4401: call 0x005D3DE0`。cleanup側は `0x005D3DFC` で `inner+0x20` を走査し、`0x005D3E00` でスロットを読取り、`0x005D3E02/04` のNULL検査を経た**非NULLのスロットだけ** `0x005D3E07` でfreeする。`0x005D3E13/16` は格納した件数をループ境界とする。これにより、正常割当・無改変・上流パース成功条件下では**未訪問スロットの未初期化ポインタをfreeしない**という追加の静的根拠が得られた。

**限界:** 個別modeの `_calloc(1,0x10)` がNULLなら、06時台に既発見の `0x005D4398` 書込問題は依然成立候補。NULLをfreeしないcleanupは、そこに到達する以前のNULL書込を防がない。ほかに既存構造体の再利用、mode件数の後刻書換え、内側ポインタへの別名・競合書換え、任意の別入口からの不正な渡し方、実ゲームでのOOMやクラッシュは未検証。**全面的な安全性証明ではない。**

## 情報源・独立検査

| 項目 | 実際の値 |
|---|---|
| 原作一致PE SHA256 | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| 2026-10-21オフラインZIP SHA256 | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| 旧Ghidra search.sqlite SHA256 | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |
| 新規主要関数 `0x005D3DA0` の擬似C SHA256 | `670A3CA9C264C879D98A44307743D365D3C1EE1058F70C1DDC17E06BD50C19D7` |
| PE命令窓 `0x005D3DA0..0x005D3DD2`（終端非含）SHA256 | `3FE84D6EFF23ED93B2D52B9E3ABBAFAD38D764DD848F0D17928A45D5B0745360`（証拠JSONでも確認） |
| 検査 | **117/117 PASS**、FAIL 0、監査内部実測 **0.71117秒** |
| 独立証拠 | 保存JSONに各命令バイト、直接E8呼出先、条件分岐、Ghidra擬似C SHA・検索DB CALL、6つのPE窓SHA、境界・順序条件を記録 |
| CPU・RAM・全作業時間 | PC未接続のため不明 |

対象VAは `0x005CF010 / 0x005D3DA0 / 0x005D4160 / 0x005D3DE0 / 0x005C303C`。直接CALL siteは `0x005CF06B / 0x005D3DC4 / 0x005D4384 / 0x005D4401 / 0x005D1C86`。Ghidra全擬似Cは既抽出機械出力で、REAの `info/pseudo/assembly/callers/callees` 正式5点を新たに揃えたとは数えない。

**正式進捗変更:** 新規5種完備0、VERIFIED 0、TODO/VERIFY/BLOCKEDの正本編集差分 `0/0/0`。過去の64件は前回までの履歴上の報告値であり、今回PC正本で再確認できたわけではない。原作Golden PASS 0、strict MATCH 0、READY 0、完全複製率未測定。新規REA/Ghidra逆コンパイル、ゲームEXE実行は行っていない。

## KB_CANDIDATE／再開先

`KB_CANDIDATE`（**未確定**）: owner `REA/T015`、研究IDは冒頭。分類 `STATIC / VERIFY`。相対証拠パスは `headless_analysis/search_index/search.sqlite`（旧検索DB）および対応擬似C `full_pseudoc_20261020/functions/005D/005D3DA0.c`、`.../005D4160.c`、`.../005D3DE0.c`、`functions/005C/005C303C.c`。それぞれの擬似C SHA、元PE命令窓SHAは添付証拠JSONに記録。訂正対象は「mode個別calloc失敗」と「内側構造体のゼロ初期化」を混同しないこと。既存06HのNULL書込候補は残す。

PC復帰時は最新MASTER/QUEUE/PROGRESS/owner/lock/研究ID/現行V9を先に読取り、重複・競合がないことを確認して初めてREA所有の許可済みHANDOFFに一度だけ反映する。追加調査の順序は①内側 `+0x1C` の他の生成／別名書換え、②mode件数 `+0x08` とmodeスロット `+0x20` の他の書込元、③親`0x005CF010` のstate=3 transient経路と初期化入口の到達性。今回の共有knowledge・MASTER・Git・原作・他owner・既存スケジュールは**変更していない**。
