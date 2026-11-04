# 迫真戦記 dev_lab — T012 状態異常 dext 計算・安全なstage連結（2026-10-11）

## 前提・安全
- Windows Desktop Commander Local Compact のみを使用。原本ゲーム/EXE、MASTER、A〜E owner、保存REA run、Git・Remote・scheduleへの変更なし。
- 逆コンパイルの新規起動なし。以前SAFETY_REFUSALされた処理を再試行・迂回しない。本メモは既存保存nativeを読んだ独立DEVコードの成果。
- 研究正本は今回read-onlyで checkpoint 81 / 179正式ID（A54/B45/C43/D37）/ DONE9 of 34 を確認。今回のDEV追加をこの179 IDに加算しない。
- 元ゲーム実機DYNAMIC OBSERVED=0、target golden PASS=0、strict MATCH=0。以下のPython試験はSTATIC/SYNTHETICのみ。

## 保存証拠（再読した範囲）
- exe/T012_DAMAGE_CORE_DUMP.txt 0x551370..0x551438。sourcebook recovered_source/ghidra_c_pseudocode/FUN_00550E70.c も同式の裏付け。
- 0x551370..0x551392：抵抗r=0なら係数10、r=1..9はruntime table [0x65BF18+r*8]、r=10なら0。
- 0x5513A6：直接CRT rand15（攻撃側）、0x5513B2..0x5513D8：攻撃Unit+0xACに係数と線形乱数係数を掛け、0.5を加える。
- 攻撃側の係数は hi=double[0x65BF00], lo=double[0x65BEF8], hi + rand15/32768 * (lo-hi)。
- 0x5513DEで0x5D1B80を呼んだ後、0x5513F9の別rand15、0x55140A..0x551426で target Unit+0xAC × hi=double[0x65BF10], lo=double[0x65BF08] の補正+0.5。
- 0x55142C別native変換→0x551431 SUB ESI,EAX でsigned32 wrap→0x551435/438 margin>10 なら0x578B70へ。

## 今回作成した互換実装
- src/hakushin_compat/damage_status_dext_expression.py: NativeUnit+0xACと4個のbinary64定数、2個のCRT raw値、実行時damage_consti係数から数学的Fraction式を生成。2つの整数化を明示native oracleへ委譲し、32bit SUBとsigned >10判定を分離。
- x87中間80-bit値・FPU control word・0x5D1B80 default ftolを実装済みとはしない。Fractionはbinary64ロード値の厳密な数学的式。native完全一致はVERIFY。
- tests/test_damage_status_dext_expression.py: 乱数上下端・中点、二者異stat、r0/r10とruntime slot、負値、native変換順序、INT32 wrap、oracle必須、既存per-candidate gateとの接続を対象。15 / 15 focused PASS。
- src/hakushin_compat/damage_status_pipeline_subset.py: 旧2個の限定tracer (damage_status_dispatch_subset.py, damage_status_candidate_subset.py) を連結し、known direct rand15本数を積算。
- optional 0x576F10 が到達する場合は前段効果と乱数状態が不明なので開始前 fail-closed。0x578B70要求後は状態変化/RNGが不明なので次候補に進めず停止。
- native 0x415530/0x4ACE30 候補生成は正しい候補数・順序のoracleが必須。builder内部RNGとselection内部RNGは個別計数、暗黙コピー・分布仮定はしない。
- tests/test_damage_status_pipeline_subset.py: source absent/chance reject/context gate、copy/vector-single/map、build空集合・build内部draw、抵抗で次record・unknown helper停止、bad input fail-closedを検証。17 / 17 focused PASS。

## 実装境界・残課題
- 従来の trace_post_hit_status_dispatch は 0x576F10 到達をtraceで示すだけ。今回のstrict composerは副作用未観測のため、その先を実行せず証拠ギャップとして例外化。
- 0x578B70が実際に状態異常を変更する条件・優先順位・draw本数は未取得。従ってsuccess record後も残recordへ同じ乱数で継続するのはstrict互換不可。
- 0x65BF00/0x65BEF8/0x65BF10/0x65BF08のnative binary64実値は今回の保存された命令範囲には無い。合成fixtureは明示値を供給。原EXEの定数を偽装固定化しない。

- 0x5D1B80の DAT_00B14A40==0 経路は0x5D1BDF以降が未取得で、round()/trunc()固定化できない。INT32 overflow/default rounded value、x87 intermediate tiesもVERIFY。
- MAP builder 0x415530 / 0x4ACE30のbuild結果・順序・filter効果、single-selector 0x40ED80内部rand、0x576F10副作用もVERIFY。前段0x550E70 damage本体のHP変更は未実装。
- 独立開発用の新規ファイルのみ。MASTER/T018/A-D/既存REAと混ぜず、Eへは必要ならDEVLAB-006で横断依頼。
- 手動観測/セーブデータはユーザーがPC復帰後まとめて。ここでは要求しない。

## 回帰状態（新規focused）
- 新規 focused 合計 32/32 PASS (15 dext + 17 pipeline)。
- 前回引継ぎ保存値は254件全PASSだが、今は別AIのPEER_SCRIPT01専用testファイルが追加されており、全件の総数はこれより増え得る。
- 全run_checks.ps1の終了・readback後に最終集計を更新。原ゲームTARGETと比較したgoldenには数えない。


## フル回帰の確定結果（2026-10-11 06時台 JST）
- Desktop Commander Localのrun_checks.ps1（PID28336）で **Ran 322 tests in 62.963s, OK** を確認。
- その後も map/atlas 151/151・513、context 204 assignments、DAT lexer590 files/14,591,845 bytes、parent21,214 refs、AST 516 selected / 71,346 recognized / 172 opaque、1v1/2v2 map/clock/合成VM/合成AIを完走。
- 末尾出力 **DEV_LAB_ALL_CHECKS_PASSED (static data checks only)** と **SCRIPT_LAST_EXIT=0** を直接readback。原作TARGET gameplay goldensは依然0。
- 以前の254件 + 本成果32件 + この実行時に追加されていたPEER_SCRIPT01の36件 = 322件。別AI所有のpeer_script01_*・test_peer_script01_*・PEER_SCRIPT01_FINDINGS_20261011.mdは一切変更していない。
- 注意: run_checks内の既存test_package_source_snapshot.pyが固定OUTPUT「recovered_source_snapshot_20261011_parallel_status.zip」を再生成。現SHA256は **889607c8c92fedd6b699dcc5b6917cdef8ccbb4e4347d6ad709760aae2be9c2c** (316,092 bytes) に変化。旧引継ぎ §13 のSHAは過去スナップショット記録であり、現ファイルのhashではない。
