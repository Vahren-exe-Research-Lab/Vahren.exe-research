# REA｜2026-10-31 13H｜Vorbis外側配列の独立確保・cleanupの条件付き解放漏れ（P0）
研究ID: `REA-LOCAL-20261031-13H-P0-VORBIS-CLEANUP-COUPLED-ARRAY-GUARD-STATIC-01`。owner=REA、Task=T015、状態 **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。
前回12H `REA-LOCAL-20261031-12H-P0-VORBIS-LOOK-ARRAY-CALLOC-PARENT-GATES-STATIC-01` を先読し、12Hのlook配列と親0x88確保、11Hの4つのlook内部確保を**新規計上しない**。

## 使用出典・事前照合
- 専用PE `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、`PRAGMA quick_check=ok`。標準V3を切替えない。
- MASTER・レーン規約・REA README/QUEUE/PROGRESS、既存12H evidence/readback、`logs/progress_sync_20261011T153958076Z.json`（正式64/64）、PC knowledge README/SYNC_STATUS、kb addr/docs、GitHub知識ベース `develop` の `REF_AUDIO_VORBIS.md` / coverage / curation をread-only照合。旧 `search_index/README.md`、`BUILD_MANIFEST.json` は現行配置に存在せず、既知04HのENOENTとの差分として統合V9入口を確認。
- V9関数 `0x005D4AE0` はbody **3非連続range/552 bytes、ABI未検証**。直接CALL元7件、CALL先24件（V9索引上）。出典不明の仮想呼出先やC擬似コードからのABI確定はしない。
- 実行前後 `active.lock` なし、Java/Ghidra競合0。確認時空き物理RAM **13.9GiB**、CPU負荷と総作業時間は不明。REA/Ghidraの新規起動・原作実行0。

## 新規差分1｜外側の2つの配列は独立してmallocされるがcleanupのガードが連動
- 初期化 `0x005D59BA: E8 -> 0x005B9BC8` の戻りは `0x005D59C2` で `outer+0x08`、別の `0x005D59CD: E8 -> 0x005B9BC8` は `0x005D59D5` で `outer+0x0C` にそれぞれ保存。どちらも独立の確保呼出である（STATIC）。
- cleanup `0x005D4AE0` の `0x005D4C7F` は **`cmp [ebx+8],0`**、`0x005D4C83` の **`je 0x005D4CCC`** は1つ目がNULLなら内側の配列解放と、2つ目の `0x005D4CB9..0x005D4CC4` (`[ebx+0xC]`のNULL検査→free) の**両方を飛び越す**。
- 後続 `0x005D4D09..0x005D4D0E` は `memset(outer,0,0x70)` を実行する。したがって **`outer+8=NULL` かつ `outer+0xC!=NULL` という部分構築状態をcleanupに渡すと**、2つ目の確保領域をfreeせず参照をゼロ化して失う **条件付きメモリリーク**が成立（ASM/CFG条件はSTATIC、該当状態の通常到達性はINFERRED/VERIFY）。
- これは12Hのlook配列 calloc失敗や11Hのlook内部malloc失敗と**別の配列所有階層**。現実のallocator結果・入力値・ゲーム時のリーク量は未実測。

## 新規差分2｜count>0の場合には、その前に別の失敗経路がある
- `0x005D59E0..0x005D59E3` の比較は `[param_2+4]` の**要素数**であり、`outer+8`の確保結果NULL検査ではない。要素数>0なら `0x005D59EB` のcalloc戻りを `0x005D59F6` で `[edx+ecx*4]` に書き込むが、EDXは `outer+8` 由来。
- **要素数>0、1つ目mallocがNULLの条件**では、この書込自体に先に到達する可能性がある。従って、単に「malloc失敗ならcleanupでリークする」と一括りにはできない。要素数<=0の経路の実在・呼出制約・OOM後の制御を次回VERIFYする。
- `0x005D5BB8 -> 0x005D4AE0` の失敗cleanupは、codebook変換側の `0x005D5BC2: EAX=-1` returnと接続する（既知10Hの後続）。この失敗分岐が**外側2配列の確保後に来る証拠ではない**ため、今回の条件付きリークをこの分岐で実証したことにはしない。

## 独立監査とREA正式進捗
- 新規 `REA_20261031_13H_P0_PARENT_CLEANUP_PROBE.py` は指定3分割function rangeを尊重して命令表示。独立 `REA_20261031_13H_P0_CLEANUP_COUPLED_ARRAY_GUARD_AUDIT.py` が同一SHAとV9・以前の12H検証・native E8 8 sites・元ASMとPE windowを照合。**44/44 PASS、1.8814秒**。
- `REA_20261031_13H_P0_CLEANUP_COUPLED_ARRAY_GUARD_EVIDENCE.json` に命令bytes/target、PE window SHA256、44判定、旧研究IDと根拠を保存。独立 `REA_20261031_13H_P0_CLEANUP_COUPLED_ARRAY_GUARD_READBACK_VERIFY.py` は元PE bytes・E8/V9索引・4 window・前回リンク・source SHAを新しく読み直し、**56/56 PASS、1.4816秒**。結果は同名 `READBACK.json`。
- 正式REA5種（info/pseudo/assembly/callers/callees）の**今回新規5種完備0**：既存V9疑似C/関係索引の存在と局所ASM独立監査は、正式REA5種完備ではない。新規正式VERIFIED **0**、過去正式STATIC VERIFIED **64/64維持**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。
- 原作Golden実測PASS **0**、完全複製率 **未測定**、DYNAMIC **0**。本調査は原作実行・脆弱性再現・全面的メモリ安全性検証ではない。

## KB_CANDIDATE（共有辞書への自動反映禁止）
- IDは本報告冒頭、owner=REA/T015、source path/PE SHAとV9 SHAは上記。差分は `0x5D59BA/0x5D59CD` の外側独立確保に対する `0x5D4C7F/0x5D4C83` の一方に偏ったcleanupガード、`0x5D4CB9/0x5D4CC4` の解放スキップ、`0x5D4D0E` のポインタゼロ化。局所STATIC、部分状態到達性INFERRED/VERIFY、READY=NO、Golden=0。
- 既存 `REF_AUDIO_VORBIS.md` の12Hまでの記載を先行根拠とし、重複しない「outer+0x08 / outer+0x0C cleanup条件依存」だけを統合専任へ候補として残す。新規symbols確定は行わない。
- **次回再開**：`0x005D5BD0` の独立caller側から通常teardown到達を調べ、`0x005D57C0` の `0x005D59E0` 要素数の上流制約と `0x005D5A0A..0x005D5AB4` の正常returnを追跡。例外・new-handlerやmalloc(0)の実際の到達条件は未確認。
- 新規安全拒否/接続失敗なし。MASTER、QUEUE、PROGRESS、既存RUN、A～E、原本、共有knowledge、Git、生成DB、スケジュールへの書込み0。今回許可済みREA自身の新規6ファイルだけ保存し旧成果は変更なし。
