# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 08時台 P0独立静的研究

**研究ID:** `REA-OFFLINE-20261101-08H-P0-VORBIS-CACHED-STREAM-STATE3-REENTRY-STATIC-01`  
**状態:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。原作Golden実測PASS `0`、strict MATCH `0`、READY `0`、完全複製率は未測定。

## 1. 開始確認・安全境界・先行研究

Desktop Commander Local Compactで研究PCのMASTER、レーン規約、REA README/QUEUE/PROGRESSおよびknowledge資料を一括読み取りしたが、`INVALID_ARGUMENT: McpServerError: Session terminated` で失敗した。**接続障害**であり、安全拒否ではない。復旧ID `REA-RC-20261101-08H-LOCAL-SESSION-TERMINATED-01`。PCの電源・オンライン実態、active.lock、owner競合、現行V9、CPU/RAM、最新正式進捗は**不明**。禁止された別経路によるPC接続の迂回はしていない。PC正本には何も書いていない。

アクセス可能なChatGPT Libraryの実物 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe` を隔離された解析環境へ読取用コピーとして取得した。原作PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、オフラインZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP収録SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` は今回再計算し一致。ZIP CRC全項目PASS、SQLite `PRAGMA integrity_check=ok`。旧研究snapshotのMASTER・レーン規約・REA PROGRESSと検索README/BUILD_MANIFESTも存在・署名整合を照合。ただし旧REA PROGRESSは**2026-10-09時点15/16**であり、現在の正式数ではない。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` にある `GHIDRA_V9_COVERAGE_REPORT.md`、`REF_AUDIO_VORBIS.md`、`KNOWLEDGE_CURATION_PROTOCOL.md`、`SYNC_STATUS.md`、`symbols.tsv`、`structs.tsv` を読取専用で確認。GitHub記載の統合V9 SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` は**今回現物を再測定した値ではない**。対象の`0x005CFC16`・`0x005D0D4B`はGitHubのREF文書には見当たらず、symbols.tsvにも対象関数の完成辞書はない。しかしPC上の全研究との完全な非重複照合は未完了。

既存 `REA-OFFLINE-20261028-20H-P0-OGG-BOS-SERIAL-CHAIN-GATE-STATIC-01` はBOS/serialの仕組み、`REA-OFFLINE-20261028-22H-P0-OGG-CF010-CALLER-OWNERSHIP-CROSSCHECK-STATIC-01` は`0x005CFC2F`のパーサ呼出し時にシリアル配列を渡さない点、11月1日06H・07Hはmode割当とcleanupを研究済み。**今回の増分は、二つの別関数から状態3へ復帰して保存済み論理ストリームのheader recordを使う、ヘッダ再解析を挟まない局所経路**である。前述のBOS解析、既知CALL siteやmode OOMは新規発見として再計上しない。

## 2. 新規P0増分A：`0x005CFA10` の既知serialへの復帰

原本PEのx86命令を入口から照合した。`0x005CFB00`でEDI=2、`0x005CFB05`でEBX=4になる。再生状態とページシリアルの分岐条件を満たした場合、`0x005CFBA2`で外側デコーダの`+0x58`に状態2を保存する。`0x005CFB9E`は`outer+4`を検査し、単一ストリーム側では `0x005CFBAB` からVorbis setup cleanup `0x005D3DE0` を呼ぶ。一方、複数ストリーム側ではこのcleanupを避けて既知serial探索へ進める経路がある。

`0x005CFBD9` は `0x005D32A0` でOggページのserialを取得する。`0x005CFBF0` は `outer+0x40` のシリアルテーブルの要素と比較し、`0x005CFBF5` は4バイトずつ移動、`0x005CFBFB/FD` で件数と一致しなければ処理ループへ戻る。**既知serialが見つかった場合に限り** `0x005CFC03` で採用インデックスを`outer+0x60`へ記録し、`0x005CFC0B`で現在serialの`outer+0x5C`を更新する。`0x005CFC0E`からreader同期関数`0x005D3A80`を呼んだあと、**`0x005CFC16`で状態値3を直接書く**。`0x005CFC1D`のJMPはページキュー処理へ行き、そこから再生ループ `0x005CFA20` に復帰する。

状態3の再生ループ入口では `0x005CFA28` が複数ストリーム判定を行い、`0x005CFA34`でインデックス、`0x005CFA37`で32バイト単位の乗算、`0x005CFA3A`でヘッダレコード配列ベース`outer+0x48`を加える。`0x005CFA45`から**保存済みレコードを引数に**初期化関数`0x005D5BD0`を呼び、失敗時は戻り値を検査、成功時 `0x005CFA6D` で状態4へ進む。

**限定結論:** `0x005CFC16 → 0x005CFA20 → 0x005CFA45` の調査済み局所経路では、新しいsetup headerを`0x005CF010`で解析し直さず、インデックス付きの既存レコードを使う。これはキャッシュされた論理ストリームへの復帰・再初期化経路に見える。ただし、選択されるレコードが全入力・全失敗時に必ず有効であること、別スレッド/外部呼出し、実ゲームの再生挙動は未証明。`0x005CFC2F` のparser呼出し（**新規serial側の別経路**）は10月28日22H既知であり、新しいCALL siteとしては数えない。

## 3. 新規P0増分B：`0x005D0B60` の別の復帰経路

`0x005D0B60` 内の `0x005D0D06` は状態2に戻し、`0x005D0D17: CALL 0x005D32A0` から次ページのシリアルを取得する。`0x005D0D1C/2A` は`outer+0x34`の登録数と`outer+0x40`の既知serial配列を読み、`0x005D0D30..3E` は4バイト刻みで既存のシリアルを探索する。一致しなければ `0x005D0BA0` に戻る。一致した場合 `0x005D0D48` で`outer+0x60`にインデックスを格納し、**`0x005D0D4B` で状態3を直接設定**。`0x005D0D5F` からreader同期、`0x005D0D67` から `0x005CF970` を呼ぶ。

その `0x005CF970` は `0x005CF973` で状態3の条件を検査し、`0x005CF990..0x005CF996` で選択されたヘッダレコード `outer+0x48 + index*0x20` を組み立て、`0x005CF9A1: CALL 0x005D5BD0`で初期化する。戻り値が非0ならエラー値を返し、**成功時だけ**`0x005CF9CC`で状態4へ進む。これも局所区間では `0x005CF010` を挟まない。

**重要な区別:** 両経路で状態3へ戻る手順が似ていても、処理の所有者は `0x005CFA10` と `0x005D0B60` で異なり、`0x005CF970` は後者が使用する別の初期化入口。異なる実ゲーム実行経路・再生方式にどう対応するかはVERIFY。再発見・独立実機PASSを二重計上しない。

## 4. 監査と5種証拠の充足

独立監査 `REA_OFFLINE_20261101_08H_CACHED_STREAM_STATE3_AUDIT.py` は原作PE32のVA→ファイルオフセット変換、原本x86 **55箇所の固定命令バイト**、**9件のE8直接CALL先**（SQLite索引との9件の二重照合）、**9件のJcc/JMP分岐先**、Ghidra保存済み5関数の擬似Cハッシュと局所トークン、原本の4つの境界指定命令窓SHA、入力PACKのCRC/manifest/SQLite整合性を検証した。

結果は **125/125 PASS、FAIL 0**。監査内部実測 **1.53593秒**。ゲームを実行したGoldenではない。元データ読取以外にREA/Ghidraを一切起動していない。CPU/RAMの研究PC負荷と全工程時間は不明。

機械語の代表元証拠窓（末尾番地は含まない）：`0x005CF970..0x005CF9D7` SHA `E9F9D9A7B9007542C5C127B9A50CDC2CF176034912B5D2F67AABFBC058C200F3`、`0x005CFA20..0x005CFA75` SHA `DE417C1784F1664655E75554C30E0030C6B58A6FD690CD3600DD650C14A920FA`、`0x005CFB9E..0x005CFC5B` SHA `5AF938AEEE7750889814C3E5317057BA9598A49D7A4F645A10285382CF1B95A2`、`0x005D0D06..0x005D0D77` SHA `36CA638988F353CDE8F0F454B93D06DED2E1C87A38CADB945392049D53EAAA08`。

解析元は `headless_analysis/search_index/search.sqlite:functions/calls`、保存擬似Cは `full_pseudoc_20261020/functions/005C/005CFA10.c`、同`005CF970.c`、同`005CF010.c`、`functions/005D/005D0B60.c`、同`005D5BD0.c`。各擬似CのSHAは静的証拠JSONに個別保存。ソースは**旧2026-10-21版**で、最新V9ではない。

REA正式5種 `info / pseudo / assembly / callers / callees` の新規5点セット完成 **0関数**、新規正式VERIFIED **0**。既存の正式64件は過去の報告値（今回再検証していない）として保持し、旧ZIPの15/16と混同しない。正式TODO/VERIFY/BLOCKEDへの編集差分 `0/0/0`。本件は独立した**OFFLINE VERIFY候補1研究ID**であり、関数5件を解析完了として計上しない。ゲームGolden実測PASS=0、strict MATCH=0、READY=0。

## 5. KB_CANDIDATE、未解決、保存・再開

`KB_CANDIDATE`（**未確定**）: REA/T015、本研究ID、VA `0x005CFA10 / 0x005D0B60 / 0x005CF970 / 0x005CF010 / 0x005D5BD0`、状態遷移 `0x005CFC16 / 0x005D0D4B / 0x005CF9CC / 0x005CFA6D`、CALL site `0x005CFA45 / 0x005D0D67 / 0x005CF9A1`、offset `outer+0x34/+0x40/+0x48/+0x58/+0x5C/+0x60`、機械語SHA・擬似C SHAを証拠JSON参照。新規差分は、**既登録serial検出→state3直書き→保存済みヘッダレコード選択→初期化成功でstate4**の、二つの局所経路を機械語で独立確認したこと。既存の10月28日22H`0x005CFC2F`所有関係や11月1日06H・07H modeメモリ問題とは別。

**未確認:** 登録serial表と32バイトレコード表の対応・寿命、各配列の実際の確保数と上限・NULL異常経路、既存レコードに初期化済み情報が保持される契約、別入口・間接CALL・並行書換え、実ゲームでのページ選択状態。`0x005CFC16`が存在するだけで不具合や脆弱性とは判定しない。

**次のP0:** ① `0x005D1490`周辺で複数ストリームレコード `outer+0x48` とserial配列 `outer+0x40` の対応関係を確認、② `0x005D0B60/0x005CFA10` のキャッシュ復帰先で `index<count` が必ず成立する上流条件を追跡、③ `0x005D5BD0` の入力ポインタ有効性・失敗時クリアの契約を静的補強する。PC復帰時は最新MASTER、OWNER、QUEUE、PROGRESS、現行V9、既存ID、LOCKを先に確認して非重複・非競合のREA所有HANDOFFのみ一度同期。共有knowledgeは専任統合者が確認するまで変更しない。

原作・PC正本・MASTER・QUEUE・PROGRESS・他owner・Git・共有knowledge・スケジュールは変更していない。安全拒否・禁止VAへの迂回なし。**最終状態：OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**。
