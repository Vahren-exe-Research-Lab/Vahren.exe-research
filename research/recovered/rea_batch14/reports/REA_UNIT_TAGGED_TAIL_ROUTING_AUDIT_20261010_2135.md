# REA Unit save 追加tag領域への制御移譲・境界監査（2026-10-10 21時台 JST）
- 区分: STATIC CROSSCHECK / REIMPLEMENT VERIFY。新規REA/Ghidra解析なし、元EXE実行なし。REA独立所有領域のみ。
- 対象: T014、Unit reader VA 0x58E870 / writer VA 0x58EFD0。未取得helper VA 0x58E480 はVERIFIEDに昇格しない。
- ソース: 保存済みreader run 20261009T223622536Z、writer run 20261009T224617297Z。
- reader ASM ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839、pseudo ev_992508cdab86c44fc73e0f72aa80b7ab30679a2b84144a444f5afe7a7d80760d。
- writer ASM ev_fc8c23eb060d4cca74ce05f46674a7ceb09d69e81637d412eed595d6c6e0cedb、pseudo ev_cde544509b86b04088d6dc930be72217c748a238c92970d25767aba134389c41。
- 保存RUN_RESULTのsource SHA256は E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回の実ハッシュ再計算なし。
## 観測できた命令順
- writer 0x58F333..0x58F3FF: Unit+0x130ツリーのkey＋DWORDを走査・出力。0x58F405 MOV ESI,0x68B9D0 → 0x58F40A CALL 0x470830で終端文字列を出力する。
- 直後にliteral arbeit→Unit+0x7C DWORD、arbeit_user→Unit+0xA0 string、item_skill→Unit+0x11C..0x120 vector、friend→Unit+0x15C treeを出力。各固定literalの文言は既存writer pseudoに見える。
- writer 0x58F63Aは別終端候補0x68B3A8を書き、0x58F644 MOV ESI,0x68B9D0 → 0x58F649 CALL 0x470830で同じ参照先の終端文字列を**再度**出力し、0x58F64EでUnit+0x13C string以降の固定tailへ進む。
- reader 0x58ED10はUnit+0x130のkey文字列を読む。空文字なら0x58EE8B以降の固定tailへ進み、marker一致なら0x58EE5F CALL 0x58E480を実行してから同じ固定tailへ進む。
- readerの保存済み本体にUnit+0x7C/+0xA0/+0x11C/+0x15Cを直接読む命令は見つからない。writerの中間tagを実消費する関数候補は、marker一致でのみ到達する0x58E480である（**推定**）。
## 再実装への影響／未確定
- Unit+0x130 map終端と直後のtag群／friend tree終端は別境界として扱う。markerを単に捨てて固定tailの+0x13Cへ飛ぶ読み込み実装は、writer側の中間tagでストリーム位置をずらし得る。
- 0x58E480の具体的なtag認識順、任意tagの扱い、追加フィールドの値更新、後半marker消費位置は未解明（VERIFY）。この関数の5種Ghidra証拠・実ゲーム動作は未取得。
- Golden候補（DESIGNED/NOT RUN）: 正規writerの空/非空map＋tag領域、Unit+0x130終端を空文字に置換した異常ストリーム、2番目のmarker欠落。比較前に合法観測可能性を判定する。
- 新規VERIFIED 0件。前回の重複キー専用メモ書込SAFETY_REFUSALは再試行せず、異なる本調査のみ記録。QUEUE/PROGRESS/MASTER/T018/A-E/Git/設定/自動化は未変更。