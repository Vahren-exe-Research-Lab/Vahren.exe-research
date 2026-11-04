# REA 2026-10-31 18H｜Vorbis bitbuffer解放・NULLスロット境界（P0）
研究ID: `REA-LOCAL-20261031-18H-P0-VORBIS-BITBUFFER-TEARDOWN-NULL-SLOT-STATIC-01`
Owner: REA / Task: T015 / 状態: **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。17H研究ID `REA-LOCAL-20261031-17H-P0-VORBIS-BITBUFFER-TWOLAYER-ALLOC-STATIC-01` の後続であり、15件初期化と2層mallocの発見を新規として二重計上しない。

## 出典・重複照合
- 研究専用PE `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。対象窓の元bytesとE8相対CALLをCapstoneと独立計算で照合。
- 統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`（17H照合SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`）。`function/callers/callees`は読取専用。CLIで本関数の関数範囲 `0x5D4A60..0x5D4AD3`、CALL元5・CALL先6を確認。
- `knowledge/kb.py addr/docs 0x5D4A60` の名前と研究全文直接言及なし。private GitHub `develop` の先行 `REF_AUDIO_VORBIS.md` と現地の17H証拠を参照。15時までのpostinit研究、16Hの親確保、17Hのbitbuffer初期化と区別する。
- 指定旧`search_index/README.md`・`BUILD_MANIFEST.json`は実在せず ENOENT。既存V9公式入口 `00_START_HERE_UNIFIED_V9_20261023.md` に従い別名の現行read-only CLIを使用し、拒否済みV3標準化は再試行しない。

## 機械語からの新規STATIC差分
- `0x5D4A68`で管理構造体 `outer+0x68` をEBXへ読込み、`0x5D4A6C`にてリスト後処理 `0x5D49F0` を実行。`0x5D4A77/79`で `outer+0x44` が非NULLならfreeする。`0x5D4A84/86`では**配列親EBXのみ**NULL判定し、NULLなら全スロット処理を省略する。
- EBX非NULLでは `0x5D4A8B` の `EBX+0x0C` を起点に、`0x5D4A90`で各スロットポインタを取得。毎回 `0x5D4A93 E8 -> 0x5E6CA0` に渡す。 `0x5D4AAF/B2`までで **15件（index 0..14）**処理する。各スロットがNULLかどうかの局所guardは見当たらない。
- `0x5D4A9B/9E`で index==7 の場合だけ `0x5D4AA3 E8 -> free` を飛び越す。これは17Hに確認した **index7は親内埋込 `EBX+0x04`、残り14は独立確保**という所有権分岐と一致。index7も下位`0x5E6CA0`を呼ぶため「埋込＝何も解放しない」ではない。
- 下位`0x5E6CA0`は `0x5E6CA7 mov eax,[esi+8]` が**最初のNULL判定より前**。これは `slot`自体のNULL判定ではなく `slot+0x08`の内部bufferポインタのNULL判定（`0x5E6CAA/C`）である。内部bufferが非NULLなら `0x5E6CAF`からfree、その後5 dword（0x14バイト）を0にする。
- `0x5D4AB5`で親配列をfree、`0x5D4AC6`でouterの0x70バイトをmemset(0)し、正常終了でEAX=0。別の `0x5D49F0` が可変長リストの後処理と条件付きreallocを実行するが、エラー時realloc semanticsは未詳。

## 条件付きリスク・禁止する推論
- **STATIC**: 親ポインタが非NULLでも、その内部15スロットのいずれかがNULLなら `0x5E6CA7`の `[slot+8]`読出しは不正アドレスになる（NULL保護がない）。`free(NULL)`の標準的動作の有無より前にこの参照がある。
- **INFERRED/VERIFY**: 17Hのslot用calloc失敗では、初期化 `0x5E6C79` 側でもNULLスロットへの書込が先行しうる。したがって**通常実行でcleanupまで到達することや二重クラッシュを実証したわけではない**。部分初期化例外経路、実際のOOM、別所有者alias、同期、cleanupの反復到達は未確認。
- **KB_CANDIDATE**: 新候補は `0x005D4A60` / `0x005E6CA0` のNULLスロット扱いとindex7解放区別。既存17H `0x005D4900/0x005E6C70` の二層確保を新規計上しない。共有knowledgeの更新は専任統合担当のみ。

## 検証・未更新・次再開
- 独立監査 `REA_20261031_18H_P0_BITBUFFER_TEARDOWN_AUDIT.py`: **66/66 PASS**、Pythonプロセス終了コード0／1.19秒。元命令29箇所、ネイティブE8 13箇所、5関数窓SHA各1件と全disasm範囲を検査。構造化証拠 `REA_20261031_18H_P0_BITBUFFER_TEARDOWN_EVIDENCE.json`。探索 `REA_20261031_18H_P0_BITBUFFER_TEARDOWN_PROBE.py`。
- 正式5種の新規完備0／正式VERIFIED新規0。前回までの64/64に追加計上しない。QUEUE/PROGRESSのTODO/VERIFY/BLOCKED差分0/0/0。原作Golden PASS0、strict MATCH0、完全複製率未測定、READY0。
- 研究PC接続正常。開始時 `active.lock`なし、Java/Ghidra競合0、空きRAM約14.49GiB（実時間CPU負荷、作業全体の経過時間は不明）。原作ゲーム、REA再解析、Ghidra、共有Git、A-E資料、MASTER、QUEUE、PROGRESSを変更しない。
- **次優先**: `0x005D49F0` のリストcleanup/realloc結果・呼出元で部分初期化条件を限定し、`0x005CF9E0`、`0x005CFA10` のcleanup到達経路と親管理スロット初期化を追跡。実ゲームGoldenは別工程。
