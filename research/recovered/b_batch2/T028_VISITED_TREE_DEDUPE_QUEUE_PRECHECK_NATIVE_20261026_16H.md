# B-20261026-1614-T028-VISITED-TREE-DEDUPE-01｜T028/T011 代替位置探索の訪問座標重複除外（STATIC/VERIFY/NOT READY）
研究日時：2026-10-26 16時台 JST。所有者：B／T028主、T011召喚配置にクロス参照。正式READYではない。
[PRECHECK] Local Compact online。MASTER既存E正式checkpoint196/READY596、LANES規約、B5 owner、B HANDOFF、拒否・復旧索引、検索README/BUILD_MANIFESTを読取。未同期2026-10-25 14H全文の完全統合未了。
[BASELINE] 無改変原作 ver0.67 PE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 現物一致。旧search.sqlite SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF 現物一致、URI mode=ro PRAGMA quick_check=ok。
## 新規静的結論1：exact lookup と ordered tree
- 0x49EE00（96B／原作窓SHA256=2518B9985430F664BD8662C1455973129BA400DA4F8BAEBF97BC982747A72206）は0x49EE0Aから0x49F5B0を呼ぶ。0x49EE16/18でend sentinelを確認、0x49EE1A..3Cで候補キーと要求キーを比較し、不一致なら0x49EE4D..59でsentinelを返す。
- 0x49F5B0（71B／SHA256=75202F36DF059581EE8939FC30F027A0A43CDD9E857FE3A042D86F73B7F3BACA）の0x49F5E1..EAは nodeKey < queryKey なら右、そうでなければ左へ辿るlower_bound型探索（原作ASM）。0x49EE00はnodeKey<=queryKeyも確認するため有効範囲でexact equalityになる。
- 比較キーは k=(Y<<16)|(X&0xFFFF) を32bit符号付きで比較（0x49EE1A..3C／0x49F950..74）。座標の全値域で一意性保証は未証明、通常到達範囲はVERIFY。
- 0x4ED3B0（101B／SHA256=18B86CE19806C80912D9448EAE8D8C7732211DDBAE90297B5F9D940AD01A0AF2）の0x4ED3B3で24B node確保、0x4ED3C6..D1でリンク初期化、0x4ED3DF..E6でnode+0xC/+0x10に2座標をコピー。整列木の参照対象であり、容器クラスの厳密型と例外効果はVERIFY。
## 新規静的結論2：挿入結果とdeque重複除外を接続
- 0x49F930（261B／SHA256=7B0F134B9C10A0CA9527B0D8AE1F68A2E8096DC0911906CD207E93CB5B6BF7F5）は0x49F9B8/0x49FA0Eでout+4=1（新規挿入）、0x49FA27でout+4=0（既存キー）を設定、out先頭はiterator/node pointer。挿入経路は0x49F9AF/0x49FA02→0x49FC40。ABIをvoid扱いしない。
- 管理mode!=0の代替探索0x4E7770は0x4E7845先頭候補をenqueue→0x4E785E visited木にinsert。その後の近傍候補は範囲判定0x4E7903..1D、距離系gate0x4E7923..58を通った後、0x4E7969 exact lookup→0x4E7975候補iterator==sentinelのときだけ0x4E7982 enqueue→0x4E799F insertへ進む。既訪問なら0x4E7977 JNE→0x4E79ABで両処理をskip。
- 別系統の配置探索0x4E70E0（既15Hの召喚クロス参照）は0x4E71B1 enqueue→0x4E71CF insert開始点、近傍は0x4E7284 exact lookup→0x4E7290/92で非訪問に限り0x4E729D enqueue→0x4E72BA insert。既訪問は0x4E72C3へskip。
- mode0の0x4E7770は0x4E7D72→0x49F5B0 lower_boundと0x4E7D7F..B2のキー比較／sentinel検査を経て、未登録に限り0x4E7DBD enqueue→0x4E7DDA insert。異なる探索座標解像度／探索条件は既知で、本回は重複判定joinのみ新規。
- Native E8照合：0x4E785E/0x4E799F/0x4E71CF/0x4E72BA/0x4E7DDA→0x49F930、0x4E7969/0x4E7284→0x49EE00、0x4E7D72→0x49F5B0、計8/8元PE一致。
## 差分・制約・次回
[DEDUP] 15HのFIFO/8Bペア/召喚0x54F0E1、14Hの方向配列とセル空判定は再計数0。新規増分はmap node/キー/lookup exact/挿入結果/「先にlookup→未訪問だけenqueue→insert」の二経路、mode0はlower_bound直使用。B5 owner+HANDOFFでは主要新CALL site 0x4E7969/0x4E7975/0x4E7284/0x4E7290/0x49FA27事前literal0件。全未同期/他laneの意味重複照合はVERIFY。
[VERIFY] mode0とmode!=0で境界/距離/開始方位が異なる。数学上の最短到達、RNG非使用、全例外・間接CALL、同一keyの符号/16bit境界衝突、合法原作シーンでの実機位置は未証明。位置探索の実行時意味とT013索敵への関与もVERIFY。
[GOLDEN] 原作無改変EXE＋20倍強化前DAT、同一SAVE/MAP/input/RNG。開始候補・複数の8方向候補・循環経路・重複候補・負座標/境界・先着位置/次tickを旧実機と比較するまでDESIGNED_NOT_RUN。旧Gameplay Golden PASS=0、strict MATCH=0、新規B READY=0/E MASTER統合=0/DONE=0。
[NEXT] 0x49F930重複挿入フラグの例外・0x4E7770/0x4E70E0の開始方位からの8方向順序を候補一覧まで限定追跡。0x4E8E00 deque容量境界、T013のgrid consumerを別証拠で調べる。
[SAFETY] 原作起動・書換なし、Ghidra全面解析/REA重複なし。既安全拒否0x5710C0..0x571500および既拒否payloadを再試行・別経路迂回なし。MASTER/他lane/REA/dev_lab/ZIP/EXE/SAVE/Git/Work/設定/スケジュールは不変更。
