# B-20261020-1015-01｜T013 24B支援候補vectorのself-alias append境界（限定保存ASM）
[ORIGIN] 2026-10-20 10時台 JST。B所有既保存exe/T013_SELECTOR_HELPERS2.txt VA0x5154F0..0x5155BEをLocal read-onlyで照合。原EXEは実行・変更・新規逆解析なし。既保存target SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。
[STATIC] 0x5154F0でsource EAX→ESI、global scratch begin=[0xAC09EC],end=[0xAC09F0],capacity=[0xAC09F4]。VA5154FA..515506はsourceが[begin,end)内かをunsigned address比較で分ける。
[INTERNAL] 範囲内sourceではVA515508..515519でbeginとの差を24B単位のordinalへ変換。end==capacityなら515523 CALL5155C0後にendとbeginを再取得し、VA515534..515537で新begin+24*ordinalをcopy sourceとして再構成する。
[EXTERNAL] 範囲外sourceではVA515572..515585でend==capacity時に同grow helper後endを再取得し、元ESIをsourceにしたまま51558B..5155AAの6 DWORD転送へ進む。
[COMMON] 両経路で24Bを6 DWORDとしてappendし、end+=0x18を保存。これはglobal scratch 0xAC09EC/F0/F4のvector、Unit-local+1E584/588/58Cでも28B postcore vectorでもない。
[BOUNDARY] internal pathのself-alias alias-protectは静的に確定。ただし0x514F10 callerは局所stack recordを渡しており、本helperのinternal pathが原作実ゲームで到達するcallerは今回未同定。grow先allocation/exceptionや実メモリ内容全域の精密互換はVERIFY。
[DEDUP] 既B-20261011-0718-02はscratch vector存在、B-20261011-0914-01は0x5158A0によるlogical reset、オフラインB-OFFLINE-20261020-0908-01は24B record+04/+14未初期化候補。それらを再登録しない。今回の独立増分はsource aliasをordinalで再定位するappend分岐。
[REIMPLEMENT] vector append時にalias(source in own storage)を識別し、capacity増設前のsource indexを保持。raw +04/+14を意味付きfieldとして固定せず、候補選別・HP/MP効果とは区別する。
[SYNTHETIC] begin/end/cap/srcの外部2・内部4ケースで内部index・grow条件を6/6分類。ASM局所構造に対する設計モデルであり原作実機の成功ではない。
[GOLDEN] 合法原作runで同一一時vectorを内部sourceとしてappendするcallerが確認された場合だけgrow境界0/1/multi candidateと旧新メモリ序列・最終target/MP/HP/RNGを比較。現時点はINELIGIBLE/DESIGNED_NOT_RUN、原作Gameplay PASS0、新旧strict MATCH0。
[NEXT] 許可済B保存callersから5154F0へ内部pointerが実際に渡る例の有無、5155C0の既保存grow結果/例外とrecord+04/+14下流consumerを別々に確認。
[STATUS] 詳細＋T013 owner索引＋B HANDOFFの各独立readback/重複検査前はNOT READY。E正式統合0。
