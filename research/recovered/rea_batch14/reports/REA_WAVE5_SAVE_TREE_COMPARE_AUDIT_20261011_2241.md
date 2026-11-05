# REA Wave5 追加4関数 — 保存タグ/木挿入/文字列照合の独立静的監査（2026-10-11 JST）
対象: 承認済みコピー rea_lab/targets/hakushin067_Vahren.exe のみ。SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
根拠run: runs/20261011T133432356Z/RUN_RESULT.json（22:34:32–22:40:46 JST、completed=true、failure=null、no_game_execution=true）。REA6.1.0/Ghidra12.1.4。既存5レーン資料・MASTER・T018は編集しない。
## VERIFIED（全関数にinfo/pseudo/assembly/callers/callees・固有evidence ID・source/end SHA・Ghidra入口/境界あり）
- 0x598980 / T014 / Spot runtime読込 / 859 bytes。info=ev_53ed1be96bc20ed0ffbc4d954ae100f1967fd59ebe9ce1884069085408de84aa
  pseudo=ev_0acff01a3a0b32c2efc27bc4c2c113a5990bee48a71916922824806d419968ad / assembly=ev_66c1bf6fd99abcfd7034dc3de539e043f9ab1f39ea402827967a1ab418ca929b
  callers=ev_4d7481471a3b7dd25ba99a255743190483ec355ad0f0e6519faff740ac1a22e9 / callees=ev_6597562b214fb07ef9cf92fb2a7c26825f7f6c86082b307f37ef650e62a31f52
- 0x5964C0 / T014 / Power runtime読込 / 1489 bytes。info=ev_105b1c184be5d868744bee92f4d32362e03bb147780923add1925cff2553acea
  pseudo=ev_9608d350a99e5ba1453392474e951d01a83321124085c78de8ef29ffc8ea96d9 / assembly=ev_225abdeab1240aef12bae0642c86e2bc6494b630fee961f55233f5c29cbb5e25
  callers=ev_24c083a492c9b10125bdeecdfbc3db2f2d263a8cd19efd9d17513b9bc771efef / callees=ev_ff3bf40913871207a524bdcdc61a67694df2d6300e9bcae944c544e93caf631d
- 0x4A6700 / T005,T014 / tree挿入primitive / 478 bytes。info=ev_f1a511812cc60f2d44928133ae37f2dd7702b5455677c9675e1f0387edef3654
  pseudo=ev_11cd3d1b65fb7672cf0cc86955c08cd96acab2b7a8521e74a5d3020b89452acb / assembly=ev_29d636b279a7b1f14f59ba9fc63f0f425e7a9058d49f6eb9d34409590d4fb2f3
  callers=ev_ae28dc9e0f7124cd4b7d1aa288bbf1a5fd55c83a77381a63a72ef6bbc2b51f42 / callees=ev_43e13092422659aa0f51e6931f70295286d1642dbe32a8ac2c89a61e3e188ff6
- 0x40B200 / T006,T010（用途ラベル再検討）/ 文字列比較helper候補 / 84 bytes。info=ev_ec2dd487c7478081fb26ce910a9b854f47c123371b542f12e59e6bdf5534439f
  pseudo=ev_d3b60611f4e0570c118727b471bbd19bd10cd6c9f187e0812023914cb8ccef61 / assembly=ev_80377536380b1f73406c409003776dc07da99b7a8d860e3f70dc06941a55541a
  callers=ev_35291b767472758d4d578ad386e03faa8202014e9f2b0cbe76deb646f1cbfb7b / callees=ev_f5bba603bb289fe46001acbd2e9227eb0df15c0d4b88f12e77e1f47cd0125ca6
## 新しい局所観察（意味論確定ではない）
- 0x598980 は既存tree/複数fieldを初期化してtagを逐次読込。tag長0でreturnし、長8/12/10/7の比較を経て読み込むfieldが分かれる。特殊tagで入力stream状態を検査しLoadExceptionを送出する分岐がある。tag名と各field意味はVERIFY。
- 0x5964C0 はPower関連複数field/tree/vectorを初期化し、tagを逐次読込。長7/9/8/10の識別や0x40B200照合を経て格納先を分ける。特定tagが見つからない経路で+0xDCに0x80000008を設定する。数値が示す意味と書込側との整合はVERIFY。
- 0x4A6700 はmap/set長さ上限guard、node挿入位置のleft/right接続、red-black tree向け色/rotation更新の局所実装。ここから重複keyの先勝ち/後勝ち・payload mergeを直接確定しない（caller契約が必要）。
- 0x40B200 はC文字列の長さと[EDI+0x10]を照合し、0x402C40比較結果が0で両者同長の場合だけtrueを返す。**単独ではevent flagやゲーム条件を判定していない**。現キューの「eventフラグ条件判定helper」は仮称で、87解決済みcallerに基づく実使用域の分類が次課題。
## 課題と次回
- T014: tag literal/長さ/typed valueとwriter順序のcrosswalk、旧保存データは読取専用、実機load golden未実施。
- T005/T006/T010: 0x40B200 callersから実用途を分類、0x4A6700を呼ぶwrapperのduplicate handlingを区別。疑似コードのunaff_*引数は未確定ABIに留意。
- 現Wave5=8/16 VERIFIED、今回+4、Wave1/2/3/4=16/16・10/10・10/10・12/12、累計56/64。残Wave5はP1 8件（0x4705F0,0x470700,0x471D20,0x5154F0,0x5158A0,0x57CFA0,0x57CFD0,0x5155C0）。旧EXE gameplay golden PASS0、研究MASTER DONE9/34、ゲーム再実装率未測定。
- 既存QUEUE.json/PROGRESS.mdはWindows rename EPERMでSTALE。正本はRUN_RESULT+logs/progress_sync_20261011T134047704Z.json。既往拒否箇所/抽出再試行なし、原本/5レーン/MCP/自動化/Git変更なし。