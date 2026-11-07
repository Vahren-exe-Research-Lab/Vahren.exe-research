# REA P0｜OggDecoder仮想fillの引数ABI・二領域Lockとの接続（03時台）
研究ID：REA-LOCAL-20261026-0334-P0-OGG-LOCK-DECODER-ONE-SEGMENT-ABI-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden実測0、REA新規正式VERIFIED0。
原作研究用EXE SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
新検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
前回：REA-LOCAL-20261026-0238-P0-DS8-UNLOCK-RETURN-IDEMPOTENCE-STATIC-01。Unlock HRESULT未検査・cleanupの既出事項は再計上しない。

## P0新規解決：0x005023A0のdecoder仮想CALL
- 原作機械語 0x00502391～0x005023A0：ECX=[stream+0x00]（Decoder this）、EDX=decoder.vptr[+0x04]、CALL EDX。
- OggDecoder vtable 0x006395CC の +0x04 スロット実バイトは 0x00501F10（今回再照合）。
- 通常のOggDecoder vtableが設定されていれば、0x005023A0 → 0x00501F10。別の実行時vtableでは別処理になり得る。
- COM Lock 0x00502387 後のESP復帰を前提に、ローカル領域は [ESP+0x08]=len1、[ESP+0x0C]=p1、[ESP+0x10]=len2、[ESP+0x14]=p2。
- 0x0050238D/0x0050239Aでlen1、0x0050239B/0x0050239Fでp1をpush。先行する0x00502398/99の二つのpush 0と合わせ、decoderへ (p1,len1,NULL,NULL) が渡される。
- 0x005023A2は直ちに二番目の長さを読み、decoder戻りEAXをtest/cmpしない。以降0x005023BF Unlock、0x005023C2でAL=1。

## P0新規：二領域の書込範囲
- 0x00502359からのLock引数は buffer8, offset=0, requestedSize=0, &p1, &len1, &p2, &len2, flags=2。
- 0x005023A0のDecoder fillはp1/len1のみ。p2/len2は0x005023A2/0x005023A6で取り出されて0x005023BF Unlockへそのまま渡され、二番目の領域への書込は当該関数内に見つからない。
- 通常の「offset=0・ENTIREBUFFER」条件下では二番目の領域が空になり得るため、この事実だけで音声破損・未初期化バグと断定しない。実際のLock出力p2/len2を測定するGoldenは未実行。
## OggDecoder::fill(0x00501F10)の独立対照
- Ghidra疑似Cの引数はthiscall (this, outputBuffer, requestSize, optionalActualBytes*, optionalEOF*)。機械語0x00501F4A/0x00501FF0のRET 0x10で4個のstack引数を確認。
- 0x00501F19はdecoder+5を確認し、0x00501F5DはoutputBuffer全体を_memset(0)する。
- 0x00501F62のchunk=0x1000(4096)を上限に、0x00501F91→0x005D12E0からデータを取得するループ。
- 0x00501F9B/0x00501FA3で読込0・ループ属性+4を判定。非ループ時はoptionalEOFへ1を書けるが、今回のcallsiteはNULLを渡す。
- 0x00501FE6でoptionalActualBytesに実読込バイト数を返せるが、今回のcallsiteはNULLを渡す。0x00501FEA AL=1は一部不足でも可能。呼出元はDecoder ALも未検査。
- したがって「初期化成功＝要求バイト数の実音声データが全充填」とは限らず、ゼロ埋め分が混在し得る。これはデコーダ仕様上の無音化と整合し、障害発生を意味しない。

## 証拠・非重複・未解決
- 2026-10-21 search.sqliteのfunction 0x00502330/0x00501F10、callers、callees、related、および過去18/02時台vtable・Lock/Unlock成果を事前照合。
- 研究用EXEをPE/Capstoneで独立逆アセンブルし、同一SHAのvtable bytes/50+機械語・DB参照を監査。新専用監査55/55 PASS（検査条件数）。
- 5種証拠：info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規正式5種完備0・VERIFIED0。
- 既存Wave1～5の64/64は保存済みprogress_sync_20261011T153958076Z.jsonの旧記録。重複加算0。QUEUE/PROGRESSのEPERM由来旧表示を更新しない。
- 正式TODO/VERIFY/BLOCKED書込差分0/0/0。独立VERIFY：p2/len2が非ゼロになる条件、Decoder戻値/EOF無視時の実際の再生、ループかつ空入力時の経路、実バイト数と無音領域の境界。
- 原作ゲームGolden PASS0、strict MATCH未測定、完全複製率未測定。新規REA/Ghidra/ゲーム起動0回。FLS拒否済み・Wave6・禁止VAの操作には触れていない。

## 次回再開
次は0x005023E0ワーカー側で0x00502330が定期再呼出されるかを追跡し、デコーダ戻り値・EOS/ループ値による停止とバッファ再書込の実際の呼出条件を確定する。Golden：短い非loop OGG、空OGG、loop OGG、二領域Lock、Lock成功かつdecoder異常。
PC正本readbackで証拠JSON/report/監査scriptを再取得するまで保存結果を正式実測としない。13/14時台オフライン成果は未同期のまま（今回同期操作なし）。
