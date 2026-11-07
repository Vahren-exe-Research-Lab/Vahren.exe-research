# B-20261026-0816-T028-SIMPLESTATIC-SPATIAL-TREE-ERASE-01｜SimpleStaticUnit死亡後の空間キー探索・削除
[OWNER/STATE] B/T028 primary、T011/T012参照。2026-10-26 08H JST。STATIC-GHIDRA＋STATIC-ORIGINAL-PE-ASM、意味論INFERRED・合法実機VERIFY・NOT READY。新B READY0／E MASTER0／Task DONE0。
[PRECHECK] Local CompactでMASTER正式checkpoint196/READY596（既存正式値）、LANES_PROTOCOL/B HANDOFF/B5owner/未同期復旧索引/旧拒否記録、search_index README・BUILD_MANIFESTを先読。旧search.sqliteの関数0x49D9F0/0x510C20限定検索。新Ghidra全解析・原作起動なし。
[SOURCE] 原作rea_lab/targets/hakushin067_Vahren.exeの現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187が一致。PE ImageBase0x400000。pefile/Capstone x86の原作bytes読取専用。
[DIRECT CHAIN] 先行07H Static/Simple後処理vtable+0x58は再計数0。SimpleStaticUnit finalizer 0x55B030: 0x55B033 byte Unit+0x1867C !=0なら0x55B05A復帰。0なら0x55B03C [Unit+0x1E0]をPUSH、0x55B043 Unit+0x1867C=1設定、0x55B04A E8 CALL0x49D9F0。その後0x55B055 CALL0x4E4F60。
[EARLY GATE] 0x49D9F8 CMP BYTE PTR [arg+0x1EED40],0 /0x49D9FF JE0x49DB4F。0なら領域照合とtree削除をスキップ。arg=[Unit+0x1E0]（呼出先でスタックから取得）、+0x1EED40の意味・型はVERIFY。
[GRID] 0x49DA05/11 Unit+0x220/+0x224から座標を読み、CDQ/AND 0x1F/ADD/SAR5で負値を含む32単位のゼロ方向除算へ変換。中心(gridX,gridY)に対し x∈[X−2,X+2),y∈[Y−2,Y+2)を候補にする。右端排他により上限は4×4=16セル、5×5ではない。
[CLAMP] 0x49DA2F..0x49DA81で引数オブジェクトの+0x1EEC60/64/68/6C境界も32単位へ変換し、候補の左右/上下限をmax/minでclip。0x49DAAEの外側と0x49DABA/0x49DB33の内側は厳密小な比較、境界により0件にもなる。
[KEY/LOOKUP] 0x49DAC2 SHL EBX,16（Y側）/0x49DAD8 AND ECX,0xFFFF（X側）/0x49DADE OR ECX,EBXで32bit整数key構成。0x49DAE0..0x49DB18はarg+0x1EEC30 tree headerを使いmap/set様検索。値比較・Unit identity検証の直接処理は当該関数内で確認できない（他ownerの役割はVERIFY）。
[ERASE] 非sentinel key一致時0x49DB1A/20条件を通過、0x49DB22..29でtree context・結果 outptr・nodeをPUSHし0x49DB29 E8 CALL0x510C20。後者0x510C20はiterator validity判定と木ノードのlink修復/色調整、0x510E6B CALL0x5B6BBB、0x510E7E..83のnode count減算を持つ。単なる描画消去ではなくtree entry除去と整合（STATIC）。
[WINDOW HASH] 元PE 0x49D9F0 size355 SHA256 1AA05D1AE7EA1977D3F9CA1CA56F71E7DEC5B1D75AABBF0A3CE7DBA09BDFBB58 /119 instructions/end0x49DB53。0x510C20 size621 SHA256 D738727B7F734694A21A0EACDAF929B22AC6F82C6F2C03C636823A06DE0269E3 /216 instructions/end0x510E8A。0x55B030 size44 SHA D69B430D1977DA95039BC4C62250580B1D46B311FD6A37BBCCC8DD3EB3680647。
[DEDUP] 07HのHP gate・slot+0x58・死フラグ・CALL0x49D9F0は既知。今回独立増分はcalleeの引数オブジェクトflag、32単位の座標→最大16キー・範囲clip、map/set lower_bound様検索・ノード消去とcount。B dataの0x49D9F0リテラル検索は前07Hと主owner参照のみ。旧10/25 14H OFFLINE全文と他レーン完全意味照合は未了。
[BOUNDARY] ヒットキーの実所有者・同一セル複数Unit・空間インデックスの実用途、keyの符号解釈、各座標の画面座標⇔ワールド座標同一性、0x5B6BBBの割当副作用、他経路の空間削除はVERIFY。新規確定バグ0。士気・敗走イベントへ自動接続しない。
[GOLDEN] 無改変EXE/20倍強化前DAT＋同SAVE/MAP/input/RNG、SimpleStaticUnit vs StaticUnit、境界近傍/中央・負座標・+1EED40=0/1、死亡前後のtree keys/count・Unit+1867C・次tickを原作と再実装で比較。全DESIGNED_NOT_RUN。原作Gameplay Golden PASS0／strict MATCH0／DYNAMIC0。
[NEXT] 0x4E4F60の共通最終登録の作用、0x55AA50側にも同等の空間除去が間接的に存在するか、+0x1EED40設定元と+0x1EEC30 tree所有者を限定照合。既拒否0x5710C0..0x571500・拒否ペイロード/操作は再試行・迂回せず、原本/MASTER/他owner/REA/dev_lab/Git/Work/設定/scheduleは変更しない。
[SYNC] 10/25 14H OFFLINE全文及び既回収全ID意味統合は未完。詳細・T028 owner・B HANDOFFを独立保存/読戻しするまで現地反映未確定。
