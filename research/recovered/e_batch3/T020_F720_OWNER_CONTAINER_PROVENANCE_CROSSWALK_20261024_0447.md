# 研究E｜F720候補コンテナ所有元・比較木の分離とG2誤昇格防止
ID: E-AUDIT-20261024-0447-T020-F720-OWNER-CONTAINER-PROVENANCE-01 / JST 2026-10-24 04時台 / owner E / STATIC receipt + SYNTHETIC ONLY / NOT READY
## 出典・同定
- Desktop Commander Local Compact接続。MASTER正本/レーン規約/A-D HANDOFF/REA PROGRESSと最新04H文書/DEV計画/T018/T019/既E T020/旧search BUILD_MANIFESTとV9入口をread-onlyで先読。原作は起動していない。
- 原作EXE研究コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 をE新checkerで実バイト再計算・一致。元原本EXE/ZIP/SAVE/DATは無変更。
- REA 04H source: rea_lab/decomp_task/REA_20261024_04H_P0_F720_OWNER_PROVENANCE_STATIC.md、実SHA 6FE0B7F3068BE34E4AB547B8C46F1270F4658A8D8BAD682B43BA7226EFFDDEE2。
- REA 04H native監査script実SHA F72B87051A6C75430FF453EE3418E345B67426E4CD5BD3065CD4372C5F4B831A。REA 03H evidence実SHA 78F8B1FCA145FD33552AD68F09A0FF2D23FE8CA71484ED539BDECC9D35B4911C。Eのsource hash4/4 PASSはファイルバイト照合であり新規native22/22実行の主張ではない。
## T018 静的契約への限定採用
- REAの既保存ASMによる0x40D0A0局所: 0x40D0AE→global 0x8B8E48へEDI、0x40D0B4→0x8B8E4CへEAX、0x40D0B9→0x8B8E50へECX、0x40D0BF→0x8B8E54をゼロ化、0x40D0C6→0x40F320をCALL。局所のポインタ設定は初期化CALL以前。
- 0x40D0A0の上位direct CALL siteは 0x491FFB,0x49204F,0x492143,0x4921F7,0x492473。上下位の引数対応はcontext+1EED1C/1EED20/1EED30、DL列1/0/0/0/1（意味未確定）。これらを実施済みの旧ゲームイベント数にしない。
- 0x40F38Dで[0x8B8E4C]を読み、0x40F393→0x48F720へ候補コンテナ、0x40F398→0x583C70へ戻り値を渡す。局所の戻り値NULLガード無しはREA03H以前の既知差分で再加算しない。
- 0x40F367..370 の比較用ESIは別のglobal 0x8B8D28由来、0x48F73Cの+1EED34参照と候補list ownerを混同しない。identity/alias/lifetimeはVERIFY。
- 0x48F720の先頭ヘッダ=候補headの空条件は0x48F7E4でEAX=0帰還へ到達し得る。0x49AF10には候補リストの空初期化/clear候補があるが、クリア後の挿入と戦闘入口時の非空保証は未解明。静的空経路と実クラッシュは別。
- REA 04H自身は PC-SAVED-PENDING-READBACK / NOT READY。Eが代理READY化しない。vtable・実行時owner・完全ABI・当該5callersの条件、比較木の一致や候補リスト寿命は追加VERIFY。
## T020 新しい負例・受入ゲート
- JSON18合成ケースでは「所有元は設定済みでも現時点の候補存在までは不明」「空listなら条件付きNULL」「非空でもfilterでNULLの余地」「過去resetと入口現在値は非同一」「比較木ownerは別」「DL=陣営識別・G2成功・クラッシュ・runtime/strict成功と断定禁止」を分離。
- Checker: tests/t020_f720_owner_provenance_gate_20261024_0447.py、SHA256 24D960687B4EC6BC799B192584A18882583C72EBFC48353DF24106FE341775F6。Fixture: tests/T020_F720_OWNER_PROVENANCE_NEGATIVES_20261024_0447.json、SHA256 9C11D5F7AFBE74648FF36ADA8016E7F6A74A14FE08236581A7006A4B19BE4D1F。
- 実行はpython -BのE-owned軽量checkerのみ。検査 source hashes4/4 PASS、直接caller5/5一致、合成回帰18/18 PASS。原作Gameplay NOT RUN・E DYNAMIC OBSERVED0・actual Golden PASS0・strict MATCH0、旧/new実比較無し。
- C-NB02 G0旧合法UI由来、G1同一run直前SAVE+入力バイト/SHA、G2実MAP・3side・ordered deployed Unit/Troop、G3実終了、G4戦略World差分は全未充足。内部pointerや状態フラグをG2名簿へ昇格しない。
## T019 / MASTER / 拒否・再開
- T019新確定矛盾0/新確定原作BUG0。GameClear DAT13/TXT2は字句source scopeのRESOLVEDのみ。script2 winner/phase flag/TXT runtime/gwriteはVERIFY。
- MASTER正式最後はcheckpoint196、累積READY596(A115/B229/C136/D116)、34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値・全履歴再計数無し。新規正式READY統合0。本回MASTER正本への書込0。
- OFFLINE-UNSYNCED暫定26研究は旧申告・ID別再照合未完了。旧T018表境界/E17:55/E18:56/E22:52/E00:52/22日08:49,08:57、C T026/T032、D T030、禁0x5710C0等はBLOCKED継続。拒否済操作の再試行/迂回0、本回安全拒否0。
- PC書込はE所有の本新規note/fixture/checkerのみ。A-D・REA・dev_lab・原本・Git/Work・自動化設定等の変更0。次は合法G0/G1/G2同一戦闘receiptの未採取を優先、REAは候補挿入と開始ガードのowner側確認待ち。READY候補はsource hash/owner/readback/重複・競合照合後のみEが採録。

