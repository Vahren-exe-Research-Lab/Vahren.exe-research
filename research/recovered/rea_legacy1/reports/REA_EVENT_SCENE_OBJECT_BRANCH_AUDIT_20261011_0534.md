# REA / eventシーンオブジェクト生成分岐の静的監査（2026-10-11 05時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（局所命令のみ）／実画面・callback副作用はVERIFY。
対象: T006/T010（関連T015は他レーン所有・参照のみ）。関数VA 0x4321B0、既存run 20261009T225741694Z。
source SHA (保存run start/end): E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回のファイル再hash未実施。
assembly ID: ev_56f9a3557ec9eaa37a3dae138562b66cdde8d20a39e915d61d3e8c37709157db
pseudo ID: ev_6443778f30890c0e5cb33fc7bbabf54b8cd665a1424f7b354c6bd439dbac2051
info ID: ev_b0baec02c8d12ecbd78d2700c4b72f41016dad1c8fd11c33be96aa29aa107dea
callers ID: ev_0794fd174f88daf043f78ebffa04ea6ebc0dd6598eb55eee4075f1bce00664ac
callees ID: ev_a7a4d0b5de1642953e3949dce36374369bf2c5c14b77ff0611341f0a68fa9d8e
## 確認した順序
- 0x432B49でengine+0x1EEC4D=1の後、0x432B6Fでevent property lookup (0x4647D0)。
- 0x432BA1で取得property+4を0x402710に渡して局所文字列へ転写。0x432BE1で局所値と0を比較して分岐。
- 条件ゼロ側 (0x432BE8以下): 0x34 bytes確保 (0x5B6C2B)、0x543A30初期化、vtable 0x6388D4 (FadeOutSheet)、virtual offset +0x18へ引数0xA (10)を渡す。
- 非ゼロ側 (0x432C3C以下): 同0x34 bytes FadeOutSheet初期化に続け、0x432C6Eで0x30 bytes確保し、0x432CB1で0x5434B0 (args: engine window, 0xC8=200, 0x32=50, 0x32=50) を呼ぶ。virtual +0x18へ引数0を渡す。
- 通常経路のどちらでも仮想callは0x432CC9で行われ、ただし受信オブジェクト/引数が分岐ごとに異なる。
- 入口0x4321F4と0x432209の両guard真なら0x432216側へ進み、一般経路の上記シーン生成処理を通らない（本関数内の経路に限る）。
## 再実装・制限
- 0x5434B0オブジェクトの意味と画面効果、0x402710で導かれる厳密な条件、FadeOutSheet副作用、その他callerの重ね合わせはVERIFY。文字列の空/非空として実機仕様を断定しない。
- Scene遷移を必ず単一のFadeOutSheet呼出へ単純化せず、条件別のオブジェクト構成/virtual引数をtraceすること。
- 保存済みREAのread-only再監査。新規Ghidra/REA実行0・静的VERIFIED増加0・実機golden PASS0。既往安全拒否の再試行や迂回なし。
- 進捗: Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12, 累計39/48（重点静的関数のみ）。P0 20/21、P1 19/27、TODO8/VERIFY1。
- 研究MASTER checkpoint80: DONE9/34、再実装率未測定。QUEUE/PROGRESSのrename EPERM不整合は未変更。