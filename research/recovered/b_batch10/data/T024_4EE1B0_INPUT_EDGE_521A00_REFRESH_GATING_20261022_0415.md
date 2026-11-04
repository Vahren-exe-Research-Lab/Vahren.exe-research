# 新B T024｜0x521A00再評価条件の上流はキーボード入力ラッチ候補
研究ID: B-20261022-0415-INPUT-01
日時: 2026-10-22 04:15 JST。Owner: B/T024（T011 Skill参照）。STATIC / INFERRED / VERIFY / NOT READY、正式READY0。
原作EXEはread-only検索基盤のsource SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回原本実バイト直接hash/起動/改変なし。
PRECHECK: Local CompactでMASTER最終E checkpoint196 / READY596(A115/B229/C136/D116)・34Task9/21/4（いずれもE記録の値）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028、22ファイル回収索引、旧拒否とsearch_index README/BUILD_MANIFEST PASS/DBサイズ53927936を確認。active.lockとsearch.sqlite.buildingはENOENT。java/Ghidra活動は未確認、Vahren.exeはユーザー側で起動中、今回操作なし。
PROVENANCE: Ghidra search.py function 0x4EE1B0(343B; codeSHA256=423C00E299B8A68C9CBA99B6FB1FCB5F957221F8B46DFC1B7746638DAB573870)、0x4EE170(49B; 55DD02BAC08AFCB73AAA5CCD5BF03612026EBFD8BE4C5711FE110900CCA494AA)、0x4BCF70(458B)、0x521A00(874B; 410C8106FF93452A279B5A3B57062556F0B486CEEAEAEE70678E5DC2143EB384)、0x46FB00(471B)。既生成DATA_POINTER_REFS.jsonl L468-484をread-only確認。拒否済み0x599BD0の新検索なし。
STATIC-1: 0x4EE1B0はparam2先頭の入力codeでswitchし、case 0x2Fではイベント+4バイトの上位nibble((byte&0xF0)==0)時にInputState+0x42の1byteのみ0、非0時は+0x42/+0x43に16bit 0x0101を格納。コードが0x2Fでない複数入力codeも別の隣接byte-pairへ同様の0x0101/0制御を行う。単独のSkill更新フラグsetterだと断言できない。
STATIC-2: ジャンプテーブルはDATA_POINTER_REFS.jsonl site 0x004EE334 -> target 0x004EE215 / target_symbol caseD_2f / function 0x004EE1B0。case 0x1C/0x9C→+0x56、case 0x1D/0x2A/0x36/0x9D→+0x50、case 0x2F→+0x42。一般的なkeyboard scan codeに似るが、DIK_V等の人間向けキーラベルは原本入力device/マップでVERIFY。
STATIC-3: 0x4EE170は同じ形式のInputState候補の奇数offset +0x3D,+0x3F,...,+0x43,...,+0x57を0へclearする一方、対応偶数offset+0x42は同関数でclearしない。+0x42=current-latch、+0x43=edge-latchという解釈はINFERRED。フレーム間実行順は未確認。
STATIC-4: 0x4BCF70はkeyboard device候補のGetDeviceData vfunc(+0x28)でイベント列を取得し、code 0x39を特別処理、その他入力イベントをparam1のvtable+8経由でdispatch。0x4EE1B0にはGhidra直接caller0なので、ここが派生型入力コールバックかはINFERRED（vtable実束縛VERIFY）。
STATIC-5: 既B-20261022-03H-T024-REFRESH-TRIGGER-02の0x521A00では state=*(param1+0xFC)、global DAT_0087981C!=0の下でstate+0x42 OR +0x43を読み、同2byteを先に0へclearし、非0ならsite0x521D14で0x46FB00(*(param1+0x100))をcall/return。さらに既存の別のouter mode/case前提も必要。0x46FB00には"skill" keyの比較・tree非空の追加gateがあり、call自体は再parse成功の保証ではない。前回「Skill再評価要求フラグ」と呼んだ2byteは独立producerを見ると入力キー状態の可能性が高く、必ずしもSkill変更通知ではないと分類を改める。
DEDUP: B-20261022-0213-01のwait/com字句分布は再加算0。B-20261022-03H-T024-REFRESH-TRIGGER-02のconsumer局所gateは再加算0。独立増分は0x4EE1B0 / 0x4EE170 のproducerと0x4BCF70入力dispatch経路・jump-table site 0x004EE334との横断接続。03Hの拒否済0x599BD0検索・T024_SKILL_INSTANCE_REPARSE_RESET_COPY詳細本文を再提出しない。
VERIFY: 実vtable slot→0x4EE1B0の型同定、param1+0xFCと入力バッファ同一identity、キー0x2Fが利用者操作の何に対応するか、+0x43のframe lifetime、global DAT_0087981Cの意味、実"skill"再parse/待機時間変化、元ASM/ABI、ゲームGolden。
GOLDEN DESIGNED_NOT_RUN: 同一合法原作版における入力code 0x2F押下/解除と他code、global flag on/off、Skill key不一致/空tree/非空treeの可視Skill・MP・待機時間/RNG差を記録。現在の空手x20改変DAT状態の観測は無改変原作strict Golden受理不可。
BOUNDARY: original Gameplay Golden PASS0、old-new strict MATCH0、DYNAMIC0、B READY0、E MASTER統合0、DONE0。ユーザー起動中Vahren.exe操作0。原本ZIP/EXE/DAT/SAVE・MASTER・A/C/D/E/REA/dev_lab/Git/Work/設定/automation書込0。拒否済み旧0x5710C0..0x571500/各旧payloadの迂回0。
NEXT: 既存静的vtable参照と入力オブジェクトの保持場所を許可範囲で検証し、Skill再評価はキー入力依存かを原作ASMで確認する。T012最終MP不足・T028死亡士気の独立P0も継続。
