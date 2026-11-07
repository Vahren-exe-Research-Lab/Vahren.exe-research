# 迫真戦記再開発・Ghidra疑似CからT012型付き再実装（2026-10-11）

## 何をしたか

- 正本MASTERは開始時checkpoint79、正式統合170 ID(A50/B42/C43/D35)、Task34=DONE9/IN_PROGRESS21/VERIFY4。5レーン所有規約をLocal Compactでread-only照合。開始時Local active sessions0。
- 前回sourcebookで保存済みGhidra5点STATIC VERIFIED39/48を確認した状態を継承。今回の新規Ghidra/REA/EXE解析process0。拒否済run_decompile.ps1やUnit constructor等を別ツール・別shell・path変更で試行しない。
- 保存済T012 Ghidra疑似コードと本来のx86 assembly、B所有T012_BATTLE_CALC.md/既存native probeを交差検証し、Ghidraが省略するx87引数・field・条件順を再構成した。

## 一次証拠により復元した局所意味

1. T012 Skill-mode helper 0x550D80: mode1..5でUnit+0x98/+0xA0/+0xACを区別。Skill+0x288のratioで2種statを混合、Skill+0x280でscale、+0.5後に0x5D1B80へtail-call。Ghidra pseudoの引数なし同一変換だけを信じない。mode外0。
2. T012 damage core 0x550E70: 0x550F09 attack側rand、0x550F38 attack stat helper、0x550F53 attack抵抗coef×乱数の変換。defense側はUnit+0x9C/+0xA4から mode1/4=9C、2/5=A4、3は符号付32bit加算→CDQ/SUB/SARで0方向平均、その他0。0x550FD2で独立rand2、0x551003防御変換、0x55100B 32bit減算。
3. FPU helper 0x5D1B80: Ghidra VERIFIED bodyは28byteのみ。global0xB14A40!=0側のFSTP binary64→CVTTSD2SIはtruncate0を確認。global0側は0x5D1BB6へJZし、保存body範囲外。x87 normally-used branch/80-bit中間丸め/overflow/NaNはVERIFY。開発コードでは外部callback・Fraction数学式を使い、binary一致と偽称しない。
4. damage final dispatch 0x5510E1..0x551156: resistance10ではdamage-handler virtualをcallせず後段hitへ。scale0はhandler(0)。mode6はordinary minを迂回（mode6値生成は別区画）。resistance0は1,000,000、通常r1..9ではunit+0x1867E flagにより追加倍率、最後にbtl_min_damage。順序を一律 clampへ統合しない。
5. hit post 0x551E50: Skill+0x2A8 sentinel(-123456), Unit+0x1D0 null/+0x18614 disabled, hitcontext+0xC already setでreturn。通過時は先に+0xC=1。ratioは分母0なら0、Skill mode3=0.02固定、4=0.01固定、5は0.01..0.2、その他0.01..0.33。native converter経由でUnit+0x1C8にあるlinked Unitの+0x16Cへ加算。threshold+0x170とのunsigned比較成立なら0x58A650別calleeをcall。EXP・levelup実機側作用は未確認。

## 新規実装4モジュールと35件の専用試験

- src/hakushin_compat/typed_damage_fragments.py + tests/test_typed_damage_fragments.py: 10 PASS。各attackモード、binary64入力の数学的Fraction、防御mode3負奇数/32bit overflow、非default CVTTSD2SI、fail closed。
- src/hakushin_compat/damage_two_draws_subset.py + tests/test_damage_two_draws_subset.py: 8 PASS。攻撃/防御rand2回、変換3回、defense選択、coef、int32 signed wrap、mode6最終値未実装。
- src/hakushin_compat/damage_final_branch_subset.py + tests/test_damage_final_branch_subset.py: 8 PASS。resistance10/scale0/mode6/r0/ordinary最小値のbranch順、damage virtual要求有無、実virtual呼出なし。
- src/hakushin_compat/hit_linked_award_subset.py + tests/test_hit_linked_award_subset.py: 9 PASS。hit once、ratio上限、skill+0x2A8の異なる変換/最低10、linked+0x16C符号なし加算/level helper要求、実virtual呼出なし。

## 検証済み

- Desktop Commander Local Windowsでrun_checks.ps1フル実行 PID13604、最終 exit0 / DEV_LAB_ALL_CHECKS_PASSED。**Python unittest 215/215 PASS**（前回180→+35）。Map151 byte-exact、atlas513、context204、script590/14,591,845 bytes、親参照21,214、AST 516本文/recognized71,346/opaque172、既存headless1v1/2v2/AI120tickの内部合成検査もPASS。
- 原作EXE実行観測TARGET0、原作actual golden PASS0、新エンジンstrict MATCH0。215は静的・合成テストであり元ゲームの完成率ではない。

## 新しい研究資料／未解決

- 研究: rea_lab/decomp_task/SOURCE_RECOVERY_TYPED_DAMAGE_20261011.mdに保存済み。関数0x5D1B80はGhidra body28byteで、global flagゼロ側のジャンプ先がこのbody外にある問題を記載。
- sourcebook: dev_lab/recovered_source/SOURCE_RECONSTRUCTION_ROADMAP.mdで0x550D80/0x550E70/0x5D1B80/0x551E50と対応実装4件を明記。検証済39個の疑似Cは変更していない。
- 次の課題: (a) 0x5D1BB6通常native x87 conversionを許可済み証拠で検証 (b) mode6の固定damage算出＋距離range分岐 (c) native damage virtualの副作用 (d) Hit+0x58A650レベル処理/複数caller (e) 原作実機goldenをユーザーがPC使用可能になったとき実測。
- 今回もユーザーへ手作業やセーブは要求しない。docs/USER_MANUAL_TASKS_DEFERRED.mdに保持。原本ZIP/EXE・A〜E所有資料、MASTER/T018、Git/push、Remote、MCP/OS設定、定期タスクを変更しない。

