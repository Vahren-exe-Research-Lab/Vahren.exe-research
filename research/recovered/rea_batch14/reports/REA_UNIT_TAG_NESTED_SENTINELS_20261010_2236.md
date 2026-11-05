# REA Unitタグ領域の内外終端・空コンテナ分岐（2026-10-10 22時台 JST）
- 状態: CONFIRMED-SAVED-ASSEMBLY（CALL siteと直接分岐のみ）。旧EXE実機=NOT RUN、helper意味=VERIFY。新規REA/Ghidra実行0。
- T-ID: T014。writer `0x58EFD0` (saved run `20261009T224617297Z`)、reader `0x58E870` (saved run `20261009T223622536Z`)。
- writer ASM evidence: `ev_fc8c23eb060d4cca74ce05f46674a7ceb09d69e81637d412eed595d6c6e0cedb`。
- writer pseudo evidence: `ev_cde544509b86b04088d6dc930be72217c748a238c92970d25767aba134389c41`。
- reader ASM evidence: `ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839`。
- reader pseudo evidence: `ev_992508cdab86c44fc73e0f72aa80b7ab30679a2b84144a444f5afe7a7d80760d`。
- saved run source SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回再計算なし）。
## writerから直接確認できる固定オブジェクト参照の書込順
1. `0x58F405 MOV ESI,0x68B9D0` → `0x58F40A CALL 0x470830`：Unit+0x130ツリー直後の外側マーカー候補。
2. `item_skill` (`0x58F4D2` literal pointer)後に`Unit+0x11C..0x120`のvectorをstride `0x1C`で走査し、`0x58F54E CALL 0x470830`で各要素を出力。
3. `0x58F53C JZ 0x58F57E`：vectorが空でも`0x58F57E MOV ESI,0x68B3A8` → `0x58F583 CALL 0x470830`を実行。
4. `friend` (`0x58F58C` literal pointer)後に`Unit+0x15C` treeを走査し、`0x58F5E6 CALL 0x470830`でノードkey候補を出力。
5. `0x58F5E1 JZ 0x58F63A`：friend treeが空でも`0x58F63A MOV ESI,0x68B3A8` → `0x58F63F CALL 0x470830`を実行。
6. `0x58F644 MOV ESI,0x68B9D0` → `0x58F649 CALL 0x470830`：追加tag領域後の外側マーカー候補。直後`0x58F64E`でUnit+0x13C固定フィールド出力へ。
## 差分・重要な限定
- **追加発見**: 内側で同じ`0x68B3A8`参照をitem_skill終端相当・friend終端相当の2か所に渡し、外側では`0x68B9D0`参照を前後2か所に渡す。両コンテナが空の場合でもそれぞれの内側出力呼出が残る。
- **未確定**: オブジェクト参照の実際のバイト列、各終端の文字列一致/空値、`0x58E480`内部の読込規則と失敗時処理。pointer値をバイト列や実機互換PASSとみなさない。
- reader `0x58E870`では外側マーカー相当の一致経路で`0x58E480`を呼ぶが、このcallee自体は5種証拠未取得（VERIFY）。
- strict再実装の設計課題: `item_skill`と`friend`を同じ一つの終端判定だけで読まず、各内側境界と外側境界を別traceとして保持。正常空vector/treeと破損ストリームを別fixtureへ（DESIGNED/NOT RUN）。
- 進捗: Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、累計39/48。今回VERIFIED追加0。golden PASS0、再実装率未測定。
- 安全: 既往安全拒否バッチ/REAテキスト抽出の反復・迂回0。RUN_RESULTはread-only、QUEUE/PROGRESSはEPERM staleのため未変更。原本、MASTER/A-E/T018、Git/MCP/automation設定は変更しない。
