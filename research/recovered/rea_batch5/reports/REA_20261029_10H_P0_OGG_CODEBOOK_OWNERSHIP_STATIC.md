# 迫真戦記 REA｜2026-10-29 10H Ogg mode0 codebook共有所有権・consumer経路
研究ID: `REA-LOCAL-20261029-10H-P0-OGG-CODEBOOK-OWNERSHIP-CONSUMER-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden **NOT RUN**、正式REA新規VERIFIED **0**。

## 旧研究・検索基盤・安全確認
- MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、共通作業規約、REA README/QUEUE/PROGRESS、09H監査37/37とreadback、検索基盤README/BUILD_MANIFESTを先読。既往09H「mode1到達条件と0x005D9970 ABI」を重複計上しない。
- 隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` とも一致、SQLite quick_check=ok。
- 既存sync `logs/progress_sync_20261011T153958076Z.json` はWave1～5=**64/64**、分母16+10+10+12+16。QUEUE/PROGRESSの古い値はEPERM残留のため公式集計には使用しない。10H同名資料の事前存在0、active.lock無し・Java/Ghidra無し。
- PC接続正常、初回空きRAM約16.16GiB。CPU使用率と研究全体所要時間は不明。新規REA/Ghidra・ゲーム・Workは起動しない。

## P0-A｜通常mode0の所有権移管とエラー処理（新規補強）
- `0x005D5BD0` (CALL `0x005D5BDE`) は `0x005D57C0` に mode=0 を渡す既知経路。mode1経路と混同しない。
- `0x005D57C0` は解析済みストリームの共有コードブック表を **codec state +0xB20** に保持する。0なら `calloc(book_count, 0x38)` で作成し、各入力について **CALL `0x005D5B51` → `0x005DA070`** が表中の0x38-byteエントリを生成する。
- 生成結果が非0なら `0x005D5B59 TEST EAX,EAX` / `0x005D5B5B JNE` から失敗処理へ。成功した元の未コンパイル構造体は **CALL `0x005D5B60` → `0x005D9E70`** で破棄し、`0x005D5B6C MOV [EBX],0` で参照をクリアする。これは共有コンパイル済み表へ所有権が移る構造を示す。
- `0x005D3DE0` が共有表の後始末を担当する。NULL guardの後 **CALL `0x005D3EE4` → `0x005D9ED0`** で各0x38-byteエントリの子ポインタ5個(+0x10,+0x14,+0x18,+0x1C,+0x20)を解放し、さらに **CALL `0x005D3F04` → `_free`** で共有配列本体を解放する（独立native/索引整合）。
- 一方 `0x005D4AE0` はdecoder instance側の領域 `decoder+0x68` と関連一時資産の後始末であり、**同じ共有表を通常decoder cleanupと二重解放するとは断定できない**。各間接destructorの副作用は未検証。
## P0-B｜正規mode0コンパイル済み表の読取consumer（新規）
- `0x005D4D20` はcodebook自体のconsumer **ではない**。decoder+0x68・stream+4・codec+0x1Cを非NULL確認してdecoderのoffset/状態を初期化し、成功0、失敗-1を返す。wrapper `0x005D5BD0` はそのCALL `0x005D5BFB` 後 `0x005D5C03 XOR EAX,EAX` を実行するため、**このhelperの戻り値を破棄して成功0を返す**。ただし実際の失敗到達性は未実測。
- `0x005DFFC0` は native `0x005DFFEB MOV EAX,[EAX+0xB20]` → `0x005DFFFD` (entry 0x38倍offset) → `0x005E0003 MOV EAX,[EAX]` でコードブック先頭フィールドを利用。
- `0x005E2A80` は native `0x005E2A97 MOV EAX,[EDX+0xB20]` から共有表を取得し、**CALL `0x005E2B94` / `0x005E2BF7` → `0x005DAA60`** へ選択したエントリを渡す。calleeはbook+8>0の場合に内部decode、-1失敗を返す。
- `0x005E3240` はselector `-1` およびselector count以上を除外してから、native `0x005E32BF` で+0xB20共有表を取得し、`0x005E32CE` でentryを算出、`0x005E32D4` でentry先頭値を読む。selector数の検査とselector→book indexの適法性は別であり、後者はVERIFY。
- 上記consumer3関数は**検索DBに直接callerが0**。間接dispatch/関数ポインタ経路の候補であり、ゲーム内実行到達・不正入力時のNULL参照は **未証明**。もし共有表のallocが失敗したままmode0の構築loopへ進めば出力引数NULL+offsetの可能性があるが、OOM実測・到達性はVERIFY。

## 静的検査・証拠の格付け
- 新規監査 `REA_20261029_10H_P0_OGG_CODEBOOK_OWNERSHIP_AUDIT.py` は隔離PEからCapstoneで対象命令を独立確認、検索DBで関数11件、直接CALL8件、3関数caller数、26地点native、SHA、SQLite、旧Wave、旧09Hを照合。**56/56 PASS、0.753秒、終了コード0**。詳細は同接頭のEVIDENCE.json。
- 証拠5種類の充足: **info**=索引関数入口と長さ、**pseudo**=Ghidra既存機械生成、**assembly**=隔離PEの局所Capstone、**callers/callees**=検索DB direct CALL。独立再照合は実施したが **新規REA正式5種bundle=0、正式VERIFIED増分=0**。旧64/64維持、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。原作Golden実測PASS **0**、完全複製率不明。
- 原本ZIP/EXE/SAVE、A～E、MASTER/T018、既存RUN、QUEUE/PROGRESS、検索DB、Git・公開先・定期設定は変更しない。10/28 Library未同期成果も未統合のまま。
- **次回**: `0x005DA930` のbitstream読込とcodebook entry+0x18の利用、または `0x005DFFC0` / `0x005E3240` の間接dispatch先テーブルの読取専用照合で到達性を検証する。動作GoldenはNOT RUN。
