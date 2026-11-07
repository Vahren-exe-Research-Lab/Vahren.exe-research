# REA Wave5完了・Wave6候補（2026-10-12 00:41 JST）
- 対象: 承認済コピー rea_lab/targets/hakushin067_Vahren.exe、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本未実行・未変更。
- 出典: runs/20261011T153309850Z/RUN_RESULT.json、logs/progress_sync_20261011T153958076Z.json。REA 6.1.0 / Ghidra 12.1.4。completed=true、failure=null、end SHA一致、no_game_execution=true。
- Wave5: 12/16→16/16、今回+4件、P0=29/29、P1=35/35、未着手0・VERIFY0。全Wave累計64/64（Wave1 16、Wave2 10、Wave3 10、Wave4 12、Wave5 16）。
- 研究MASTER: DONE9/34（最新MASTER優先）、旧EXE実機golden PASS0。ゲーム再実装率は測定していない。VERIFIEDは静的証拠整合のみ。
- preflight: CPU約1%、空きRAM16.06GB、Java/Ghidraなし、active.lockなし、SHA一致。runner開始時RAM16.13GB。
- 今回の起動: 00:33:09→00:39:57 JST、Localのprocess runtime約409.55秒、単一MCP・最大4関数・Ghidra900000ms/request960000ms。
## 取得5種類のGhidra証拠（info / pseudo / assembly / callers / callees）
- 0x5158A0 / T013 / length51: ev_c97fc852e527432b7c4133fcd0cf44a46e8bcac9841716ff1ee8a7bdab39f3dc / ev_256892f9bf4a31e4d302c31129c7094cad30e15db60647104f40fe356ba63239 / ev_d4d1952d5b5e5da305467de47caec6d2ce02aadfbc2cd5475a12f7f41e291e80 / ev_f1b2e9df780790d39cc4c42081dd4ff8813673b4f722010e464e684117ea8cd0 / ev_9580fc36d5a882144f83d2138df7118646307a29bc3070812a2466cace840b6e
- 0x57CFA0 / T013 / length48: ev_9a9d3d062613659028586f8d8af0eae8a7381d9bac3f782112c75b50116aaac3 / ev_af8c7dc6fe7871eb38bb0c219d8494ae7fa96d2e11c2b198fda926e5c813fb61 / ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789 / ev_c82dd1dff727f53cb60373ba56501df0d68afb419c8aebf3e04dbb962d4e6f0b / ev_4322b0d609d2b48ca8311e8a1e55d2455a54cb30a7c331b8d67b020d1e3c3d39
- 0x57CFD0 / T013 / length397: ev_f85bc7f40298b5ec205b3f4f8c0365f48b2fa30e5e8afc42691ec110f5c23efa / ev_fa33cc83cda4f064bed5262e5fa063359e2fbb86a07b22329757999821da3725 / ev_08eb96aea33c3dbd4a1ae58fa08f3b20bfb31b8ccea4539a5bc0044cbb4887b5 / ev_2165e20b9ddd5e43f31ed380772fac96908f75d04017f95794667c1f5a9113a0 / ev_2dc9297fab51c57cfc686ea99152528224402c6e4b39256935a1d5594e621958
- 0x5155C0 / T013 / length115: ev_08e6efd0872abd3f6c80338578a06041183074e527ad2d9e3b1a0ee01664a78d / ev_e0069ba6edcf643c2dc695615ff75d8db9c7f580aa072947eefff66fe9bddd00 / ev_72f380c9a2ac729db657c8f2196ab2fa8d3140b10696808ff3f72f8a1b1e470b / ev_8ce57a11472ca4f7210743bb6347db6942fe6f05f256522503722b53d44ff2ce / ev_3daab45e80edd1c3310fdc82eaa078cc4d0a5ecc6d3a8ac4257be7b4bc515442
## 静的観察と未確定点
- 0x5158A0: 24byte幅レコード（6×4byte）をsrc範囲からdstへ順次複写するloop。関数仮称「支援候補cache更新」は実処理を過剰に意味づけるため、24byteレコードrange copyが正確。コピー範囲重複時の安全性は未確定。
- 0x57CFA0: 非空の既存範囲に0x5158A0を適用後、0x57CFD0を呼んで範囲insertする薄いwrapper。引数の実質の始点・終点、候補の意味は呼出側でVERIFY。
- 0x57CFD0: 24byte候補vectorの範囲insert。最大件数/容量不足時の別allocation、旧storage解放、容量十分時の後方移動を分岐する。vector<T> too longのexception経路あり。allocator・Move/Copy順序はcallee追跡が必要。
- 0x5155C0: グローバル配列DAT_00ac09ec（begin）/09f0（end）/09f4（capacity）を基に、1件追加時容量不足なら約1.5倍のgrow、新規件数より少なければその件数へ補正。0x515640を呼ぶ。0x5154F0からの再確保経路。
- 上記は5手法一致の静的局所挙動。候補の評価・支援AI意思決定・バトル互換の確証ではない。
## Wave6 暫定16候補（すべて既存Ghidra callee/xref由来、QUEUE未投入・未解析・関数入口は今後検証）
| 順 | VA | Task/優先 | 既存xrefs根拠・目的 |
|---:|---|---|---|
| 1 | 0x515750 | T013/P0 | 0x57CFD0 callee、vector増量時の長さ算出 |
| 2 | 0x515790 | T013/P0 | 0x57CFD0 callee、vector allocation/insert |
| 3 | 0x5159B0 | T013/P1 | 0x57CFD0 callee、24byte range移動・破棄順 |
| 4 | 0x57D180 | T013/P0 | 0x57CFD0 callee、candidate vector range copy |
| 5 | 0x54B460 | T013/P1 | 0x57CFD0 callee、tail adjustment |
| 6 | 0x470980 | T014/P0 | 0x4705F0 callee、セーブ1byte取得 |
| 7 | 0x42E700 | T014/P0 | 0x470700/0x598980/0x5964C0 callee、セーブ数値取得 |
| 8 | 0x4628F0 | T014/P1 | 0x471D20 callee、外交書込内部 |
| 9 | 0x4708A0 | T014/P1 | 0x471D20 callee、外交書込共通 |
| 10 | 0x4707D0 | T014/P1 | 0x5964C0 callee、Power読込補助 |
| 11 | 0x436560 | T014/P1 | 0x5964C0 callee、Power読込派生 |
| 12 | 0x436680 | T014/P1 | 0x5964C0 callee、Power読込派生 |
| 13 | 0x4633E0 | T005/T014/P1 | 0x4A6700 callee、tree map primitive |
| 14 | 0x402C40 | T005/T014/P1 | 0x40B200/0x5964C0 callee、文字列比較周辺 |
| 15 | 0x416790 | T014/P1 | 0x598980/0x5964C0 callee、共通読込補助 |
| 16 | 0x416870 | T014/P1 | 0x598980/0x5964C0 callee、共通読込補助 |
- 登録前に改めてQUEUE全Wave/既存証拠/禁止範囲/関数入口/研究の未解明項目を照合する。現在は16候補すべてQUEUE.jsonのaddressと重複しないことをread-only検索で確認したが、他の過去出力・非入口・意味論の確認が残る。採用済みと表記しない。
## キュー更新制限・次回再開位置
- 実行はSUCCESS、RUN_RESULT5方法とも成功。logs/progress_sync_20261011T153958076Z.jsonは64/64で整合。
- 一方、既存QUEUE.jsonとPROGRESS.mdのatomic renameはEPERMで、正式な表示へは反映されない。固有tmp snapshotsは保存済み。ACL変更、強制上書き、別手法での更新迂回、繰返し失敗操作はしない。Wave6は暫定候補記録のみ、runnerキューへ未登録。
- 次回優先: まずQUEUE/PROGRESSの既存正本との不一致とPC負荷・Java/lockを再点検し、保存済み静的証拠を再使用。安全な登録手段が確立するまではWave6を重い解析の対象にしない。必要ならread-onlyでcandidateのentry/xrefsを整理。
- 原本ZIP/EXE、5レーン資料、MASTER_LEDGER、T018、Git/push/公開、MCP設定、既存スケジュールは無変更。禁止範囲0x5710C0..0x571500と過去拒否済みREAテキスト抽出は未実施。
