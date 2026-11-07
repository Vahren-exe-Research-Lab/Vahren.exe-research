# E T018/T020｜簡略戦闘 nonzero 戻り値と条件付き後処理の未照合分岐
ID: E-AUDIT-20261023-2052-T020-FASTSIM-RET-DOMAIN-TAIL-01
日時: 2026-10-23 20:52 JST / E所有 / STATIC・VERIFY・NOT READY / 原作Gameplay NOT RUN
対象原EXE SHA(索引記録値): E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回はEXE実体の再hashなし）
出典: 2026-10-23統合V9（SQLite SHA既記録値 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE）、同CLI function 0x0040E220, 0x0040E2F0, 0x0048EEE0, 0x0048ABF0。
注意: V9 pseudoCは原ソースではなく ABI 未認証。出典 E8 native索引・callsiteとC擬似コードは強度を区別。原作実行・新プロセス観測0。
## 新しい独立差分（前19:52 T020 selector の追補）
0x0040E220 の元擬似Cには、0x0040E2F0のret==0時は0x0040D220(1)へ進むが、ret!=0なら **間接virtual +0x10** を先に呼ぶ経路がある。間接callの実到達先/終了は未確認。
ret!=0経路は 0x0040E2B9→0x00493630（boolean=ret==1）、0x0040E2BE→0x0040F000、0x0040E2C3→0x0048ABF0 の直接CALLを持つ。3箇所のE8 opcode_kindはV9 native索引一致。
さらに 0x0048ABF0 後、参照先に関連する byte +0x1EF175 == 0 の場合に 0x0040E2D2→0x0048EEE0(iVar4) へ分岐する。E8 direct CALL site実索引一致。前19:52の3関数説明ではこの**条件付き後段**が省略されていた。
0x0048EEE0のpseudoCは global field +0x1EEC71更新と複数callを含むため、可視World/G4への副作用は未同定。後段存在だけで戦闘結果commit完了は宣言できない。
0x0040E2F0自身のpseudoC上のreturn定数は0/1/2のみ（実機返値域はVERIFY）。これと親0x0040E220の条件が **ret==0 / ret!=0** であることを分離する。
想定外の非ゼロ値3/-1の場合でも、親のコード上はbool=falseで終了処理側へ入る候補。ただし子関数の実返値3/-1を観測した証拠はなく、native正常挙動として宣言しない。
前19:52 fixture S04(ret3→VERIFY_UNKNOWN_RET)は「出現可否未確認」としてはよいが、**親分岐が未確定**と誤読させる。この追補ではFINISH_UNEXPECTED_RET/false とし、実観測と区別する。旧成果の再編集・撤回は行わない。
## T020検証
E所有独立 fixture: tests/T020_FASTSIM_NONZERO_TAIL_FIXTURES_20261023_2052.json（17ケース、bool/int型混同・byte域外・想定外非ゼロ・flag未観測を含む）。
E所有 checker: tests/t020_fastsim_nonzero_tail_gate_20261023_2052.py。ret0 drawのみ、ret1 true、ret2 false、その他nonzeroは想定外false、post flag=0で追加call条件、unknownはVERIFYにする設計。
初回合成実行16/17。F16を作るJS上の0.0がJSON.stringifyで整数0に正規化されたfixture生成ミス。F16を不正文字列"0"に訂正後17/17 PASS（失敗0）。エラーは元原作の不具合ではない。原作Gameplay/比較runner/Golden NOT RUN。
## T018/T019と統合境界
C-NB02合法旧UI G0、同一run直前SAVE+入力G1、MAP/三勢力/ordered Unit・Troop G2、終了前G3、戦略復帰World差分G4はE受入未充足。DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
T019の確定新矛盾0。GameClear DAT13/TXT2字句検索スコープ差RESOLVED、script2優先/flag用途/TXT実読込/gwrite復帰 VERIFY 維持。
MASTER最終確認checkpoint196 / READY596(A115/B229/C136/D116)、34 Task DONE9/IN_PROGRESS21/VERIFY4は旧値、全件再集計なし。今回正式READY統合0。OFFLINE-UNSYNCED暫定26研究は競合/重複未照合。
旧安全拒否 T018表境界、12時台T020記録・MASTER復旧、C T026/T032、D T030 TSV、禁止VA 0x5710C0等は別案件BLOCKED、迂回・再試行0。
NEXT: 同一runでretと後段 +0x1EF175/virtual 呼出/0x0048EEE0到達を別々に可視一次receiptと照合。C-NB02 G0/G1/G2正規一次採取を優先。正式統合はsource/owner/READY/重複/競合readback後のみ。
