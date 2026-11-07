# REA｜2026-10-31 08H｜Vorbis bitreader初期化とcodebook長さ・積算上限（P0）
研究ID: `REA-LOCAL-20261031-08H-P0-VORBIS-CODEBOOK-INIT-WIDTH-STATIC-01`
owner=REA、関連Task=T015（音声）、状態 **PC-SAVED / STATIC / INFERRED / VERIFY / NOT READY**。
前回07H `REA-LOCAL-20261031-07H-P0-VORBIS-BITREADER-EOF-BOUND-STATIC-01` の後続。07HのEOF/vendor差分は再発見として計上しない。

## 参照基盤・非重複
原作同一SHAの研究専用コピー `rea_lab/targets/hakushin067_Vahren.exe`: SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`: SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
先読したMASTER / owner規約 / QUEUE / PROGRESS（表示はEPERM由来の旧15/16）/ 07H証拠 / KB README・SYNC_STATUS、非公開GitHub developのV9 coverageとcuration protocolに基づく。
正式進捗は既存保存済み `logs/progress_sync_20261011T153958076Z.json` の64/64を採用。KB addr/docs/research 0x005DA550 は事前検索で未登録・該当なし、V9 CALL索引で担当の未検証関数と照合した。

## 新規差分A：packet bitreader初期状態の実命令
`0x005D44DF: E8 EC 27 01 00` → `0x005E6CD0`。入口はpacket内 `[0]` の先頭ポインタと `[1]` の総byte数を引数として受ける（Ghidra疑似C、ネイティブ正式ABI未検証）。
`0x005E6CD8/DA`: reader `+0` cursor=0、`+4` bitOffset=0。
`0x005E6CE0/E3`: `+0xC` currentDataPtrおよび `+8` baseDataPtr に同一ポインタ。
`0x005E6CE9`: `+0x10` packet byte lengthを格納（Ghidra 5種証拠には未昇格）。
従来07Hの `0x005E6F10` 残量計算に使うpacketSizeの供給経路を追加で静的固定した。

## 新規差分B：codebook側のbit幅の安全上限
type5セットアップの `0x005D41A1` → codebook構築 `0x005DA550` をV9の独立E8と実PEで照合。
`0x005DA584` で16bitの次元、`0x005DA58C` で24bitのエントリー数を読み取る。
`0x005D97A0`（命令 `0x005D97B1: shr ecx,1`）は非負整数のbit_lengthを返す。
`0x005DA5AA/B3` で両bit_lengthを算出し、`0x005DA5C0/C3` の `cmp ecx,0x18; jg error` により和が24より大きければ拒否。
したがって（条件付きの純粋な算術証明）次元×エントリー数の上限は `(2^12-1)^2=16,769,025`。map type2の `0x005DA7CF: imul ebx,[esi+4]` は、この前提ではsigned32 overflowしない。
最大16bitのlookup値長 `0x005DA7A2/A7`、残量比較 `0x005DA7E9/F6/FC/0x005DA804` では必要bit数の上限 `16,769,025*16+7=268,304,407` でsigned32内。map type2配列の4byte要素数上限は67,076,100 byte。
同様に24bit entry数×5bit相当の予算計算（`0x005DA6B6/BD/C3/C8`）もsigned32内。**符号付き積算が無条件安全という意味ではない**：これは正常なwidth helper・ヘッダ順序・値の不変性を前提とする局所証明。
`0x005DA6A1` と `0x005DA7E9` の2つの `0x005E6F10` 呼出は、それぞれentry長配列の予算・lookup payloadの予算を別々に検査する。07HのVorbisコメント部とは別経路。

## 新規差分C：独立のメモリ確保失敗経路
`0x005DA559/5B` の `push 0x28; push 1` と `0x005DA55D` のcalloc wrapper `0x005D1C71` で40byteの0初期化codebook構造体を確保。
`0x005DA565` で戻りポインタをESIに入れた後、NULL分岐を挟まず `0x005DA56A: mov [esi+0x24],1` を実行する。callocがNULLを返すならNULL+0x24への書込が起こり得る。
後続 `0x005DA6D6` および `0x005DA811` のmalloc戻り値もそれぞれ配列に格納されるが、局所のNULL保証は未確認。前回05Hの**comment解析calloc経路とは別**なので二重計上せず候補として管理。
原作ゲームでメモリ不足やクラッシュを再現したわけではない（STATIC/VERIFY、実機DYNAMICなし）。

## 検証・保存
`REA_20261031_08H_P0_VORBIS_CODEBOOK_WIDTH_GUARD_AUDIT.py` → 同名 `_EVIDENCE.json` を専用owner領域に新規保存。
原作同一SHA研究用EXE・V9 SHA、SQLite、旧07H、保存済み正式64、V9の直接E8 siteとPE機械語、bit幅の全候補組による整数上限を独立照合：**64/64 PASS、0.7957秒**。合成算術だけでGoldenではない。
正式info/pseudo/assembly/callers/calleesの新規5種完備=0、新規正式VERIFIED=0、既存正式STATIC VERIFIED=64/64、正式TODO/VERIFY/BLOCKED差分=0/0/0。原作Golden実測=0、完全複製率未測定。
REA/Ghidra追加起動・ゲーム実行・原本変更なし。CPU負荷と総作業時間は不明。owner lock不在（開始・監査時）。

## KB_CANDIDATE（統合専任への未承認候補）
- owner REA/T015、研究ID上記、source相対path/SHAは本書先頭。
- `0x005E6CD0`: 20byte bitreaderのゼロcursor/bitOffsetとpacket pointer/size設定。STATIC。
- `0x005DA550`: Vorbis codebook parser（仮名）。`0x005D97A0` bit_length×2から和<=24の上限検査、合法入力の積算局所上限。STATIC/INFERRED。
- `0x005DA55D/56A`: codebook calloc戻値非検査の条件付きNULL deref。STATIC/VERIFY、実機未検証。
- 既存07H EOF/vendorの知見と分離。正式辞書/共有knowledge/MASTER/Gitへ反映しない。

## 次回
`0x005DA6D6` / `0x005DA811` のmalloc失敗後の配列書込到達条件、`0x005D9E70` cleanupのNULL許容を精査。既存codebook配列のcallee/ownerを確認してからP0継続。
