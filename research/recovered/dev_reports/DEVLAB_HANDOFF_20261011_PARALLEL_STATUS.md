# 迫真戦記 dev_lab 引き継ぎ — 並列他AI＋0x550E70状態異常後段（2026-10-11）

## 並列運用を開始できる指示文

- `dev_lab/docs/PARALLEL_AI_SCRIPT_ASSISTANT_20261011.md` にPEER_SCRIPT01専用のコピペ指示を作成。対象はscript grammar/event VM（T005/T010など）のread-only逆解析と固有Python新規ファイルの作成のみ。
- 新しいサブフォルダ・worktree・branch・repoを増やさず、既存dev_lab/src/hakushin_compat、dev_lab/tests、dev_lab/docsに`peer_script01_*`および`PEER_SCRIPT01_*`という**担当者専用ファイル名**を用いる。共有元の各 `.py`、既存`run_checks.ps1`、README、正本・他AI成果はread-only。
- 他のAIを**まだ起動していない**。ユーザーが指示を渡して初めて並列稼働する。PEER_SCRIPT02などを追加するときはID・担当・ファイル接頭辞を全て変え、同一ファイルを同時編集しない。
- Ghidra/REAに以前SAFETY_REFUSALがあり、同種操作の別shell/tool/path/Remote迂回は厳禁。Local非公開ならBLOCKED。原EXE起動や原本改変、Git/push、研究5レーンA〜E owner文書の変更は禁止。

## 今回main側の追加静的解析

- 保存済み初期Ghidra `rea_lab/results/run_20261009T175957025Z_550E70_assembly.json` をREAD-ONLYから再読、VA0x55116C..0x55144Bの状態異常後段を調べた。一次断片は`exe/T012_DAMAGE_CORE_DUMP.txt`。詳しい命令対照とVERIFYは `rea_lab/decomp_task/SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md`。
- 0x55116E context+0xE & Skill+0x248>0なら0x576F10補助call→0x55119B Unit+0x8D suppress早期ret。補助callは早期retより先に到達し得る。callee副作用は不明。
- sourceはSkill+0x14C非zeroなら+0x13Cからmap-based builder、そうでなければSkill vector +0x158/+0x15C。emptyなら発動RNGもskip。候補ありでVA0x5511C5直接rand15→0x5D1B80百分率相当→roll>=Skill+0x230なら早期ret。続くcontext+0xDが0なら**chance消費後**にreturn。
- source vector非空のときSkill+0x234非zeroなら0x4ACE30へ全rangeを渡す。0なら0x40ED80 selector→0x40AFB0 index lookup→0x415530で1件append。selector内部の実rand本数・候補builder内部効果は未検証、選択oracleを外から注入。
- attr recordは28byte stride。各recordの抵抗r（無指定5、0..10 clamp）について0x551345直接rand15→roll<r²なら**0x55144B次recordへ**。負値heal `0x551490` のr²成立=全体停止とは異なる。通過時だけ0x5513A6と0x5513F9で独立rand15を2回、dext score差>10なら0x551446でstatus helper `0x578B70`をcall要求。helperへの局所強度候補はmax(10,0x5511FC時点のpre-gate damage)。native x87、actual mutation、status helper内部drawは推測しない。

## 作成した独立dev_labソース

- `src/hakushin_compat/damage_status_dispatch_subset.py`：optional補助call・source/Unit/active gate・common chance direct draw・map/copy-all/select-oneをtrace。`tests/test_damage_status_dispatch_subset.py`：**11/11専用PASS**。
- `src/hakushin_compat/damage_status_candidate_subset.py`：候補ごとのr²/score/次record制御・直接draw数・status helper requestのみをtrace。`tests/test_damage_status_candidate_subset.py`：**10/10専用PASS**。
- 新規テスト21件（status source 11・候補gate 10）、**全254/254 unittest PASS**。`dev_lab/run_checks.ps1`をWindows Local PID28556で実行、最後 `DEV_LAB_ALL_CHECKS_PASSED`、exit0。
- 旧原作target dynamic golden=0、strict engine MATCH=0。保存重点39/48 STATICは増えていない（EXE全体完成率でない）。MASTER最新cp80公式175研究ID/34Task DONE9・IN_PROGRESS21・VERIFY4は本runでは編集せずread-only。

## 継続

- 既存データ検査もPASS：map151 byte exact・atlas513・script DAT590（14,591,845 bytes）・親参照21,214・ASTサンプル516本文、合成RTS1v1/2v2。上記254件は**原作実機とは比較していない**。
- B/T012 ownerとstatus T005/T010 peerの修正所有権を交差しない。未知の0x578B70 effect・x87 rounding・attr map builder・選択RNGについて引き続き保存済みnativeだけで裏付けを探す。
- 手作業/セーブデータはユーザーがPC復帰後まとめて依頼する。既存`USER_MANUAL_TASKS_DEFERRED.md`を参照し、今は催促しない。


## 最新ローカル・ソースZIP

- `dev_lab/recovered_source_snapshot_20261011_parallel_status.zip` を作成し、CRC self-test＋専用ZIPテスト3件PASS。ZIP内は既存Ghidra疑似C39・現行Python実装・専用テスト・新たな並列AI指示と最新handoff。exe/ゲームアセット/sav無し。**新規フォルダ無し**、dev_lab直下の1ファイル。
- ZIP生成時報告：158 source files、295,843 bytes、SHA256 `8284c7b5596a195d10371ec0a2dcaaba7702fe466ad452f39941ac9ce9916ab1`。既存旧ZIPは上書きせず残した。メインDEV以外はpackage scriptを編集・再実行しない。

