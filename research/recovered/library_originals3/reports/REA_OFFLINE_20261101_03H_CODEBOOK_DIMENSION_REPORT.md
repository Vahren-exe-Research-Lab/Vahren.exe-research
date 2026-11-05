# 迫真戦記 ver0.67｜REA P0 2026-11-01 03時台（JST）｜Vorbisコードブック次元数の二系統構築元

**研究ID** `REA-OFFLINE-20261101-03H-P0-VORBIS-CODEBOOK-DIMENSION-DUAL-BUILDER-PROVENANCE-STATIC-01`  
**所有区分** REA独立静的研究、`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。公式REA VERIFIED、動的検証、ゲームGoldenを意味しない。  
**既存成果との差分** 2026-11-01 02時台の2研究IDが示した「正常初期化時に二つの除数は非ゼロ」を再計上しない。新たに**コードブック次元数の二つのコンパイル経路が同じ原本フィールドをコピーすることと、復号器までのポインタ受け渡し**を独立のPEバイト・検索DBで検証した。

## 1. アクセスと入力の真正性

最初にLocal Compactで研究PCの `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`rea_lab/decomp_task/README.md`・`QUEUE.json`・`PROGRESS.md`、検索DB README/manifest、knowledge README/SYNC_STATUSの一括読取を試行したが、`McpServerError: Session terminated`。別のディレクトリ列挙も同じ障害で終了した。これは**PC接続障害であり安全拒否ではない**。当該PCの現在のowner、active.lock、QUEUE、実行中処理、CPU/RAM、最新run/DBは確認できない。復旧ID `REA-RC-20261101-03H-LOCAL-SESSION-TERMINATED-01`。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` にあるV9カバレッジ、優先ギャップ、未研究CALL、Bレビュー、`KNOWLEDGE_CURATION_PROTOCOL.md` を読取専用で確認。`0x005E0DC0` など該当VAのGitHub本文検索はヒットなし（PCに既報告が存在しない証拠ではない）。V9集計は静的メタデータであり原作実行を示さない。

Library上に**実在した** `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe` を研究用隔離領域に素材として取得。原本の起動・編集をせず、ZIP収録の旧SQLiteを隔離一時コピーして `mode=ro&immutable=1` で照合。一時コピーは監査終了時に削除。

| 入力 | 実測 SHA256 |
|---|---|
| 原作とSHA一致のPE32 | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| 2026-10-21オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内 `headless_analysis/search_index/search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP CRC正常、SQLite `PRAGMA integrity_check=ok`。この索引は2026-10-21時点の**旧スナップショット**で、PCの現行V9や正式REA再解析結果ではない。

## 2. 新しい独立静的証拠

- **構築元 `0x005D57C0`**。コードブック登録配列は要素あたり `0x38` バイトで割当て、親状態の `+0xB20` に配列先頭を保存（PE `0x005D58E7` のCALLと `0x005D58F3` の書込）。コンパイル方式に応じて `0x005D5922 → 0x005D9F40`、`0x005D5B51 → 0x005DA070` の二つの直接CALLを使い分ける。旧DBで両構築関数の直接CALL登録は各1件。ただし間接経路を否定しない。
- **方式A `0x005D9F40`**。原本ASM `0x005D9F64 MOV EDX,[ESI]` → `0x005D9F66 MOV [EDI],EDX`、擬似C19行目 `*param_1 = *param_2;` が一致。原始コードブックの先頭DWORDをコンパイル済み先頭DWORDへコピーする。
- **方式B `0x005DA070`**。原本ASM `0x005DA0B2 MOV EAX,[EBX]` → `0x005DA0B4 MOV [ESI],EAX`、擬似C52行目 `*param_1 = *param_2;` が一致。方式Aと同じ次元数フィールド由来である。
- **residue初期化 `0x005DFFC0`**。`0x005DFFEB` で親`+0xB20`のコンパイル済み配列を取得し、選択インデックス×`0x38`から対象コードブックを指し、`0x005E0000` で residue instance `+0x10` に記録、`0x005E0003` でその先頭DWORDを読む。擬似C34〜35行にも一致。
- **type 2復号 `0x005E0DC0`**。`0x005E0DD0` でinstance `+0x10` のコードブックポインタを取り、`0x005E0DD3` で先頭DWORDを除数にロード。`0x005E0E0C IDIV ECX` が使用箇所。前回の「通常初期化時は非ゼロ」という条件付き結果に、今回の経路証拠を追加した。

**新しいVERIFY論点：** `0x005DFFC0` の `0x005E00E0 IMUL EAX,EDX` と `0x005E00EF LEA EDX,[ESI*4]` では、局所的にオーバーフローを拒否する分岐を今回の観察範囲で確認できない。`0x005E00FD` は確保処理へのCALL。数の上限は上流パーサ／選択値で保証され得るため**オーバーフローを確認したわけではない**。型2音声が原作の実データで実行されるかも未実測。別の書込エイリアスが編纂次元数を変更しない保証も未確認。

## 3. 証拠完備・静的試験・安全境界

| 指標 | 今回の実績 |
|---|---|
| 原本命令バイト照合 | 21箇所 |
| 直接CALL照合 | 4件（旧SQLite索引と原本相対E8を別々に照合） |
| 関数別検索資料 | 5件（関数入口・擬似Cハッシュ・関数サイズ照合） |
| 隔離静的監査 | **81/81 PASS**, FAIL 0 |
| 監査実測 | 1.9653 秒（監査処理のみ） |
| CPU・RAM・作業全体時間 | 不明（PCアクセス不可） |
| 公式REA 5種 `info/pseudo/assembly/callers/callees` 新規全完備 | 0関数 |
| 公式REA新規VERIFIED | **0件** |
| 公式TODO / VERIFY / BLOCKED変更 | **0 / 0 / 0**（正本へ書込なし） |
| 原作ゲームGolden PASS | **0件** |
| strict MATCH / READY | 0 / 0 |
| 原作完全複製率 | 未測定 |

従来会話に現れた正式STATIC VERIFIED **64件**は**過去の報告値**として保持。旧ZIPの `PROGRESS.md` は2026-10-09時点の15/16で現在の値ではない。64件の今回の独立再確認も、総数の加算もしていない。擬似Cや局所ASMの観察は正式REA5種証拠ではない。

## 4. 保存、KB候補、次の再開位置

隔離コンテナに根拠JSON・検証用Python・本日本語報告・独立readback記録を保存する。これは**PC正本保存ではなく未同期成果**。Library保存時もPC owner/QUEUE/MASTER/既存研究IDの競合照合なしに正式同期したとは扱わない。原本EXE/ZIP/SAVE、他lane、Git、共有knowledge、MASTER、QUEUE、PROGRESS、スケジュールは変更していない。REA/Ghidra再実行、原作ゲーム実行、禁止VA操作はいずれも0回。

`KB_CANDIDATE`（自動確定禁止）：owner `REA P0`、研究IDは冒頭、ソース `headless_analysis/search_index/search.sqlite:functions.code`・原作PE `Vahren(2).exe`（双方SHA上記）、対象VAは上記5件、CALL site `0x005D5922` / `0x005D5B51` / `0x005E0E17`（および `0x005DFFCD`）、offset `+0xB20 / +0x38 / +0x10 / +0x00`。分類 `STATIC / VERIFY`、矛盾・訂正なし、Golden 0、READY 0。共有辞書への採録は専任キュレーターによる原本再確認待ち。

**再開位置：** PC接続復旧後に最新 `MASTER/QUEUE/PROGRESS`、REA owner/lock、現行V9・既存研究ID・SHAを先に照合し、重複IDがあれば統合候補として紐付けるだけに留める。そのうえで `0x005DFE10` のコードブック数・次元数の境界条件、`0x005DFFC0` の積と確保サイズの上限、コンパイル済み先頭DWORDへの追加エイリアス書込を優先調査する。新規REA実行は必要性と正規許可が揃うまで実施しない。
