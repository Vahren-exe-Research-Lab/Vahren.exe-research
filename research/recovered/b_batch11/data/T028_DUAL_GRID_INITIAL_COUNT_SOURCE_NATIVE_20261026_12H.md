# T028｜初期空間モデルの二重格子・定数幅・ABI連鎖（12H / STATIC・VERIFY・NOT READY）
研究ID: B-20261026-1217-T028-DUAL-GRID-INITIAL-COUNTS-01
日時: 2026-10-26 12時台 JST。担当B/T028。成果は死亡・移動時の空間登録の前提に限る。士気・索敵の実意味は未確定。
証拠源: Desktop Commander Local Compact接続、MASTER正式cp196/READY596（既存値）、ANALYSIS_LANES_PROTOCOL、B5 owner、B HANDOFF、既存復旧台帳、旧search_index README/BUILD_MANIFEST。旧OFFLINE 2026-10-25 14H全文と他lane/Library完全意味照合は未同期/VERIFY。
原作: rea_lab/targets/hakushin067_Vahren.exe 2,910,720B、実読取SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。既存search.sqliteは読み取り専用参照。原作起動/書換なし。
【新証拠・初期値】PE .data VA 0x0065D150 の実バイト C0 3F 00 00 = signed DWORD 0x00003FC0 = 16,320。ファイル初期値であり実行時に不変とは未証明。
【新証拠・二方向の計算】FUN_004B9E50、元EXE 0x4B9E73 MOV ECX,[0x65D150]。0x4B9E79..0x4B9E93で ESI=trunc_toward_zero(W/128)、EDI=trunc_toward_zero(W/64) を同時に生成。負数補正は CDQ/AND 0x7F・0x3F/SAR。0x4B9E96 INC EDI、0x4B9EB1 LEA ECX,[ESI+1] により2種類の count が生じる。
W=16,320というファイル初期値なら ECX=trunc(16320/128)+1=128、スタック引数EDI=trunc(16320/64)+1=256。**以前の11H報告の N=W/64+1 だけでは基底側を説明できず、2系統の片側のみを記述していたことを訂正。**
【新証拠・連鎖】0x4B79B8→0x4B9E50 は startup FUN_004B78C0 からのGhidra direct CALL。0x4B9EAF PUSH EDI／0x4B9EB0 PUSH EAX／0x4B9EB1 LEA ECX,[ESI+1]／0x4B9EB4 CALL 0x4E4830。0x4E485F PUSH EDI／0x4E4860 CALL 0x4BBC90、callee 0x4BBCB7 MOV ESI,ECX、0x4BBD02 MOV [EDI+0x10],ESI。基底 GameModel に128を渡す register-argument path を原作ASMで接続。
【二層配置】GameModel ctor 0x4BBC90では+0x10=count128、+0x24=128、+0x28=-128、+0x2C=shift7。NewGameModel ctor 0x4E4830では+0x50=count256（0x4E4999 MOV [EDI+0x50],EBP）、+0x54=64、+0x58=-64、+0x5C=shift6。Ghidra擬似Cの各二重ループでcount×countの格子確保候補：128×128と256×256。座標カバー長は両方とも16,384相当。ただし合法MAP寸法や検索/衝突に使う正確なモデル用途はVERIFY。
【静的直接参照の範囲】既存10,268内部関数の search.sqlite data_refs で 0x0065D150 への記録は 0x4B9E73 READ 1件／直接WRITE 0。原作PE .text のDWORDリテラル C0 3F 00 00ではなく、アドレス 50 D1 65 00 の出現は0x4B9E75の1箇所のみ。これは間接writer、extern、memcpy、実行時変化の不存在証明ではない。よって「実行中に必ず128/256」とは断言しない。
【非重複】11H既存は0x4B9E73/0x4E4830と一方のN。今回増分はPE初期DWORD現物、128側のsigned /128経路、GameModel基底thiscall ECX受渡し、二階層 count128/256の対応。B主要5owner/HANDOFFに0x4BBC90/0x4B9E93/0x4BBCB7先行literal0、未同期全文・他laneとの意味的照合はVERIFY。過去の格子登録・削除は再READY計上0。
【検証条件】改変前DAT＋無改変旧原作EXE＋同SAVE/MAP/input/RNG、構築時 Wの実値、2格子各count/shift、+3C mode、境界座標0/16319/16320と移動・死亡・次tick登録を同runで採取。DESIGNED_NOT_RUN、旧Gameplay Golden PASS0/strict MATCH0、新B正式READY0・Task DONE0・E MASTER統合0。
【次のP0】0x65D150の間接/初期化後writerとstartupから実戦開始までの状態変化、0x4B9E50 caller の合法タイミング、+3C mode0/1 のowner対象、T013索敵・T028死亡と二層格子のconsumer接続。拒否済0x5710C0..0x571500/他操作は未再試行。
【安全/復旧】B資料以外への書込無し。OTHER/RECOVERED: 最初のEXE相対位置誤指定FileNotFoundError→rea_lab/targets現物へ修正。最初のPython内scanが高負荷になる式を認識し自分のREPLを終了、その後はbytes.find/re.finditerの軽量readに変更。対話REPLの改行SyntaxError・日本語コードページエラー・未設定変数NameErrorは結果に使用せず、成功した静的読取のみ採用。新安全拒否0、既拒否迂回0。Work/Git/設定/スケジュール/原本・MASTER・他lane/REA/dev_labは不変更。
