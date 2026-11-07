# 迫真戦記 ver0.67｜REA 22時台 P0 DirectMusic個数設定とランダム選択境界
研究ID: REA-LOCAL-20261026-22H-P0-DMUSIC-COUNT-RAND-STARTUP-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-26 JST）
原作研究EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
2026-10-21検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 既存成果と今回差分
13HでグローバルDAT_0065BED8への書込み3箇所（0x5584B7、0x558506、0x558521）、21Hで初期化と終了時の個数別読込みを確認済み。本報告で二重計上しない。
**新規成果**：個数変数の別のreader 0x004BE820:0x004BEEFAを追跡し、名前解決不一致時のDirectMusicPerformance配列ランダム選択に個数が使われる実命令経路を確定。さらに起動関数0x005554F0の全1206バイトを独立復号し、設定呼出しと初期化呼出しの局所的な反復可能性を限定検証。

## ランダム選択の新しいネイティブ証拠（0x004BE820）
- 0x004BEEE3 CMP ECX,[EBP+0x80] → 0x004BEEE9 JE 0x004BEEFA。検索結果が終端/不一致を表す条件の候補であり、そのときランダム選択側へ入る。通常の名前一致側は0x004BEEEBで[ECX+0x28]のポインタを使用。
- 0x004BEEFA MOV ECX,[0x65BED8] → 0x004BEF00 MOV [ESP+0x24],ECX（個数をローカルへ）。
- 0x004BEF04 CALL 0x005B6EAB（CRT rand）、0x004BEF0D FILD [ESP+0x14]、0x004BEF11 FMUL qword [0x63B080]、0x004BEF17 FIMUL [ESP+0x24]。
- 定数qword 0x63B080は実バイト 000000000000003f、doubleで **1/32768 = 0.000030517578125**。
- 0x004BEF1B CALL 0x005D1B80（x87浮動小数→整数変換）、0x004BEF20 MOV EDX,[EBP+0x70]、0x004BEF27 MOV EAX,[EDX+EAX*4]（選ばれたCOM配列スロットを実際に参照）。
- 対象処理0x004BE820の直接callerは0x004BDE40:0x004BE178（旧検索DB・統合V9双方一致）。実際の音声再生・クラッシュは未実測。
- 正常なSSE変換経路（0x005D1B95 CVTTSD2SI）の選択値は **trunc(rand() / 32768 * count)** と整合。SSE未使用時のx87丸め補助は別途厳密に確認する。

## 静的境界・影響（実機Golden NOT RUN）
SSEのtrunc経路を仮定し、randの標準0..32767を用いた算術模型では count=1→index0、count=10→index0..9、count=0→index0、count=-1→index0、count=-10→index-9..0。
14H既報ではcount=0のoperator new(0)相当はmalloc内部で1バイト確保、配列要素初期化ループは省略。今回の0x4BEF27は少なくとも4バイトのスロット読出しなので、**count=0かつランダム選択到達時に未初期化/論理境界外読出し候補**となる。
負の個数は確保要求が巨大化しbad_allocへ進み得る（旧14H/15H証拠）。負のindexの実行到達を即時断定しない。count=0の実プレイ到達、分岐条件、例外/クラッシュ/ヒープ影響はいずれも未測定。

## 設定値が途中で変わるか：新しい到達性の限定結果
- DAT_0065BED8のGhidra登録済みデータ参照は11件（3 WRITE／8 READ）。3 WRITEは全て0x00558000内。記録済みの関数外writerは0。
- 0x00558000への直接CALLは0x005554F0:0x005558ABの1箇所（旧検索DB/V9一致）。0x005554F0の既知直接callerはCRT起動関数0x005B84D7:0x005B85ECの1箇所。
- 0x005554F0には0x005558ABの後、0x00555918 CALL 0x00555CD0（音楽側初期化を含む上位処理）が続く。0x00555916 JE 0x0055591Fのため初期化は条件付き。
- 0x005554F0の1206バイト全体で**関数内へ戻る直接後方分岐は0件**。したがって、通常の1回の起動関数呼出し内で設定読込みを繰り返す根拠は見つからない。
- 結論は「単一の確認済み起動呼出しでは設定→条件付き音楽初期化の順序で、同一関数内ループによる再設定なし」。間接呼出し、外部フック、他スレッド/他の未索引writer、WinMain再入の不存在までは保証しない。
- 21Hの『ゲーム中に個数が変化するとteardown範囲が不一致』は引き続き**条件付きVERIFY**。静的に通常起動中の再設定を立証していないため、実害を断定しない。

## 監査、正式進捗、安全
Python/Capstoneで起動関数、debug設定関数、音楽選択関数、整数変換の4関数を対象限定ASM確認。原作・旧DB・V9 SHA256、双方quick_check、直接CALL所有元、個数3writer、1/32768実バイト、先行21H証拠、64件旧同期記録を照合して**50/50 PASS**（監査条件であり関数数ではない）。独立監査実行時間約2.40秒、証拠保存実行約3.38秒。研究全体時間・CPU負荷は不明。
REA5種: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY。新規5方法完備0、新規正式VERIFIED0、旧Wave1～5の64/64は2026-10-11旧同期ログからの過去成果（非重複）。正式TODO/VERIFY/BLOCKED書込差分=0/0/0。原作Golden PASS=0、strict MATCH/完全複製率=未測定。
PC SAITOオンライン、active.lockなし、開始時空きRAM約13.64GiB、Java/Ghidra稼働検出なし。重いREA/Ghidra/原作ゲームは起動せず、Work未使用。
今回の新規調査操作に安全拒否なし。禁止VA 0x5710C0..0x571500、拒否Wave6/REA export/FLS操作は非接触。MASTER、QUEUE、PROGRESS、既存runs、他レーン、原本、T018、Git、公開先、予定は変更しない。

## 次回のP0・実測設計
次P0は0x004BE820の0x004BEEE3分岐に到達する名前解決/初期化条件、および0x005D1B80のx87非SSE変換経路を限定静的追跡。併行して+0x70所有配列の別名freeと初期化失敗時の配列未解放を継続VERIFY。
Golden設計は承認済み隔離コピーでdebug値0/1/10、名前一致/不一致の両経路、正しく初期化されたCOMスロット数、rand値、配列アクセス範囲を計測するが**本回はNOT RUN**。
OFFLINE-UNSYNCED旧成果の正式同期なし。新規報告・証拠JSON・監査コードはREA専用所有領域のみへ保存。
