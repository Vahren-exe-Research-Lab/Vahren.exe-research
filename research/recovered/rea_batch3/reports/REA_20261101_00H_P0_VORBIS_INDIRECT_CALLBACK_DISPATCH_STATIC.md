# REA 2026-11-01 00H｜Vorbis 間接CALL分岐と3つのgrow呼出元の接続（P0）
研究ID：`REA-LOCAL-20261101-00H-P0-VORBIS-INDIRECT-CALLBACK-DISPATCH-STATIC-01`
Owner：REA / T015。分類：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規原作Goldenなし。

## 既存資料・正本確認
- `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`rea_lab/decomp_task/README.md`、`QUEUE.json`、`PROGRESS.md`、旧成果を参照。旧PROGRESSは既知EPERMにより古く、元の正式VERIFIED64件は前回同期結果から継承し今回増分には数えない。
- 23H研究ID `REA-LOCAL-20261031-23H-P0-VORBIS-GROWTH-TAIL-BOUNDARY-STATIC-01` では `0x5E0CF0` と `0x5E0DC0` の直接E8 CALLERS=0が判明。今回の新規差分は**間接CALL入口の実在と対応する関数ポインタ表の実バイト照合**であり、23H本体や19–22Hのgrow解析を再計上しない。
- 指定旧検索 `search_index/README.md` / `BUILD_MANIFEST.json` はENOENT、統合V9の `00_START_HERE_UNIFIED_V9_20261023.md` を使用。V9独立verify PASS。
- PEコピーSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、統合V9 DB SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- private GitHub `ButaMonky/Hakushin067-Research-Knowledge` のdevelop、V9 coverage/protocolとローカル `knowledge/SYNC_STATUS.md` を読取。KBの対象VA直接登録は見つからず、候補自動確定なし。共有KB/Gitは変更しない。

## 新規STATIC：第3グループのcallback三連鎖
- .rdataの4段参照元 `0x00612E60`〜`0x00612E6C` は順に `0x0061AE60`、`0x0061AE80`、`0x0061AEA0`、`0x0061AE40` を格納。**グループ番号2**の `0x0061AEA0` に `+0x14→0x005E0B80`、`+0x18→0x005E0CF0`、`+0x1C→0x005E0DC0` が元PEの4バイト値として格納されている。
- `0x005DEDF0` 内 `0x005DF6F2` は選択子を `[ecx+eax*4+0x520]` から取り、`0x005DF6F9` で `[selector*4+0x612E60]` を読む。`0x005DF703` で表の `+0x14` から呼出先をロードし、`0x005DF717: call ecx` を実行する。selector=2なら `0x005E0B80` に対応。
- 同じ関数内 `0x005DF75F` で選択グループを取り、`0x005DF769` の `+0x18` を経て `0x005DF788: call edx`。selector=2なら `0x005E0CF0` に対応。
- 別関数 `0x005DF7D0` 内 `0x005DF973` でグループを取り、`0x005DF97D` の `+0x1C` を経て `0x005DF991: call ecx`。selector=2なら `0x005E0DC0` に対応。
- V9 `refs-to 0x00612E60` に3つのロードsiteがあり、各入口の `pe-to` は `0x0061AEB4/B8/BC` を指す再配置スロットを返す。`callers` の直接E8=0と**矛盾しない**。元x86の `FF D1/FF D2` 命令は間接CALLであり、E8だけのリストでは見えない。
- selector=0の表には `+0x14/+0x18` に0、selector=3の表にも `+0x14` に0、`+0x18/+0x1C` は関数として未検証の非コード値がある。**選択値0/3が問題のCALLまで到達するかは未調査**。ここから実ゲームのNULL CALL/クラッシュは主張しない。
- これにより先行「E8呼出元0だから孤立関数かもしれない」という仮説を修正：**静的な間接呼出経路は存在**。実行到達・ABI・エラー伝播の動的意味はなおVERIFY。

## 静的監査・二重計上防止
- 新規専用プローブ `REA_20261101_00H_P0_VORBIS_CALLBACK_DISPATCH_PROBE.py`。独立監査 `REA_20261101_00H_P0_VORBIS_CALLBACK_DISPATCH_AUDIT.py`。
- 監査 **45/45 PASS**：原本PE/V9 SHA、root4項目、2グループのcallback6項目、12ネイティブsite命令バイト＋独立Capstone命令境界、V9 PE再配置3件・E8=0照合・3 xref site。検査対象と各命令hex、native窓SHAは `REA_20261101_00H_P0_VORBIS_CALLBACK_DISPATCH_EVIDENCE.json`。
- 静的証拠5種（info/pseudo/assembly/callers/callees）の**今回新規完備0、今回正式VERIFIED0**。既存正式VERIFIED64件は維持、正式TODO/VERIFY/BLOCKEDの状態変更0/0/0。新しいREA・Ghidra実行は無し。
- 原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定。開始時 `active.lock` なし、競合Java/Ghidraプロセス0、空きRAM約16.14GiB。CPU負荷と総所要時間は不明。

## KB_CANDIDATE・未確認・再開位置
- **KB_CANDIDATE**: 分岐入口 `0x5DEDF0` / `0x5DF7D0`、root `0x612E60`、群 `0x61AEA0`、条件付きcallback `0x5E0B80/0x5E0CF0/0x5E0DC0`。機械語CALL sites `0x5DF717/0x5DF788/0x5DF991`。原本/索引SHAと相対証拠ファイルは上記。分類STATIC、選択子の実際の到達性はVERIFYでありKBに無断反映しない。
- **次回優先**：選択子 `[decoder+0x520+index*4]` の上流writerと0..2/3の値域、各callback呼出時の引数個数・スタックバランス、`0x005E0DC0` 2除数のproducer。最も重要なのは **selector=2が原作で選択される条件** を証拠付きで特定すること。
- REA本務以外のMASTER、QUEUE/PROGRESS、他lane、Git、共有knowledge、ゲーム原本・スケジュールは変更しない。安全拒否済みVA・抽出操作には触れない。
