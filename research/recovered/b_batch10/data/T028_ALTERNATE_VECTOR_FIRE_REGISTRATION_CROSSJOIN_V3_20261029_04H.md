# B-20261029-0415-T028-ALTVECTOR-FIRE-REGISTRATION-JOIN-01｜二系統結果vectorとeffect登録sinkの静的接続
日時: 2026-10-29 04:15 JST。owner B / T028、T012/T013参照のみ。STATIC/INFERRED/VERIFY/NOT READY。原作実機起動・製品変更なし。
## 開始前・保全境界
- Local Compact ONLINE。MASTER正式checkpoint196/READY596 (A115/B229/C136/D116・旧値、全件再集計なし)、ANALYSIS_LANES_PROTOCOL、B HANDOFFとB5 owner、未同期最終台帳を読取。E統合は行わない。
- 10/29最終B147保存監査は「147/147同名PC存在、93件サイズ一致/54件1B差・全SHA未突合」。旧10/25 14H原文未発見・拒否関連8件BLOCKED・並行保存出自VERIFY。過去SAFETY_REFUSAL操作/拒否VAの再試行は0。
- 対象原作SHA256 manifest値 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回原作EXE実バイト再SHAなし）。
- 旧README/BUILD_MANIFESTは履歴参照。CURRENT_ACTIVE_RESEARCH_STATE_LATESTはV3 DB SHA 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25。python -B verify_active_research_state_v3_20261022.py: PASS_ACTIVE_V3_STATIC/verified inputs14/errors0/gameplay NOT_RUN。
## 独立増分と直接CALLの原作byte確認
- Ghidra V3修復検索の0x48C880 pseudoc（旧Ghidra由来・ABI未検証）では、manager+0x1EEC94..98 と +0x1EECA4..A8 の28-byte要素vectorを個別に順走査し、範囲外時は前03H既知0x48D18D throw sinkを共有する。この既知範囲検査は新規カウント0。
- 第一vector: 0x48CFB7 E8→0x49E490（native=e8d4140100）→ポインタ非NULLかつvirtual+0x64が非zeroの場合0x48CFD7 E8→0x5AA6E0（native=e804d71100）。
- 第二vector: 0x48D069 E8→0x49E490（native=e822140100）→同型の非NULL・virtual+0x64 gateを経て0x48D089 E8→0x5AA6E0（native=e852d61100）。
- この4 siteはV3 call indexで E8_DIRECT_CALL / independently_verified_target=1（4/4）。virtual+0x64の実vtable型、返値ABI、合法分岐条件は元ASM/動的検証待ち。Ghidra擬似CのCシグネチャを再実装仕様として採用しない。
- 0x49E490は195B、V3擬似Cで入力char*の長さを走査し、0x49E4EF→0x402800（e80c43f6ff）、0x49E50B→0x4C1200（e8f02c0200）へ。V3 caller索引は全13 E8 site/5 caller関数、うちB対象0x48C880に2 site。実戻り値・名称・vector要素型はVERIFY。
- 0x5AA6E0は287B、V3擬似Cで引数+0x8Cへフラグbyte、+0x90へ0を書き、内部のvirtual/位置調整を行う候補。条件付き0x5AA790 E8→0x4C2240（e8ab7af1ff）、0x5AA7A7 E8→0x4C3DC0（e81496f1ff）、0x5AA7B1 E8→0x4BC920（e86a21f1ff）、0x5AA7D1 E8→0x416E80、0x5AA7DD E8→0x416B90（e8aec3e6ff）。
- 0x5AA6E0のpseudocには文字列literal「spot_fire」を0x416E80/0x416B90へ渡す経路がある。V3 search spot_fireは同関数1件。ただしその効果が必ず発火する、UI火災を意味する、士気/敗走を直接変更する、までは不明。下位0x4BC920は既存T013 effect登録研究との条件付きcrossjoinであり、同一manager/オブジェクト保証はVERIFY。
- 0x5AA6E0へのV3 E8 callerは全8 site/6 caller関数（うち0x48C880内2）。全callers件数は参考・今回の新規B直接連結は上記4siteと登録下流。元原作 ASMは本runで局所追加逆アセンブルせず、verified_native_opcodeは既製V3索引の固定証跡。
## 重複・安全・次の検証
- B T012/T013/T028 ownerとB HANDOFFの今回追記前literal照合：0x48CFB7/0x48D069/0x5AA7B1/0x5AA7DD/0x49E4EF/spot_fireは各0、0x5AA6E0は1。先行03H「二vector＋49E490/virtual/5AA6E0」は再加算0。10/25未同期・他ownerの意味的完全非重複はVERIFY。
- CLI OTHER/RECOVERED: V3 CLIに未実装の「strings spot_fire」を1度要求してusage error（PC書込0、安全拒否なし）。公開済の正規V3「search spot_fire」で同関数1 hitを確認。元の安全拒否操作の代替実行ではない。
- Golden条件：無改変原作EXE・20倍改造前DAT、同SAVE/MAP/input/RNGで該当vectorの生成元→非NULL/virtual predicate→登録manager・次tick・表示/Unit変化を同一run観測。DESIGNED_NOT_RUN、旧Gameplay PASS0/strict MATCH0、新B READY0/E MASTER0/DONE0。
- 次の許可済み読取先：0x48CFB7/0x48D069直前の元ASM stack/ECX入力、virtual+0x64の型・callee、+0x1EEC94/+0x1EECA4 producer。さらにT013 final target/T024 AIとT028士気・敗走を個別に調査する。原本/他lane/REA/dev_lab/MASTER/Git/Work/設定/schedule変更0。
