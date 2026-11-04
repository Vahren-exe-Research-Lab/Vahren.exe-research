# 迫真戦記再開発・独立DEVLAB引き継ぎ（2026-10-10 17時台 JST）

## 正本／所有境界／安全

- 最新照合開始時MASTERは **checkpoint69**（E正式統合READY119 ID＝A33/B23/C40/D23、Task34: DONE9/IN_PROGRESS21/VERIFY4）。5レーン規約 `evidence/ANALYSIS_LANES_PROTOCOL.md` を読取専用で確認。原本ZIP/EXE、owner A〜Eのdata/exe/MASTER/T018、Git/push、Remote、プラグイン・OS設定・定期タスクは変更なし。
- 保存済みGhidra 5点証拠の優先関数は依然 **39/48**（Wave1 16, Wave2 10, Wave3 10, Wave4 3）。これは全EXE解析完了率ではない。新規REA/Ghidra/EXE起動・Ghidra batch再試行 **0**。過去にSAFETY_REFUSALされた既往操作を別shell/tool/path/Remoteへ迂回しない。
- 新しい独立研究メモ `rea_lab/decomp_task/STATIC_EB40_NEGATIVE_HEAL_20261010.md` を追加。既存 `rea_lab/decomp_task/STATIC_SPATIAL_EVENT_MISSILE_20261010.md`の検討事項を引き継ぐ。所有権のあるB/T012/T013、A/T006/T031へ新IDを代行登録しない（重複防止）。

## 今回の新たな解析

### 1. 0x57EB40の2つの異なるcaller制御フロー（本体は未解析）

- `exe/T013_UNIT_SEARCH_CONSUMERS.txt` 0x57E5A0..0x57E610：+0x1E538 delay>0は値-1/早期ret。それ以外ではsearchCounter=unit_search_bdr→0x57B870→vtable行動dispatch。局所branch 0x57E5D0 `push 0; push Unit(ESI); call 0x57EB40`。後続0x57E5EC `test AL,AL; jne 0x57E610`。AL==0の時だけ0x57E5F0 `0x57DF90`自然回復→0x57E5FF `0x4E13F0`へ。AL!=0なら両call skip。
- `exe/T013_1D0_GLOBAL_PROBE.txt` 0x4B618C..0x4B61B3：先行比較で該当branchへ到達し、stackbyte[EBP-0x76]が0なら候補Unit+0x1867Cを確認（非0ならskip）。条件通過で0x4B61A4 `push 1; push candidate; mov EAX,[EBP-0x88]; call 0x57EB40`。直後は0x4B61B2 `inc edi`→0x4B61B3 `jmp 0x4B6170`、**当該callsiteではALを参照しない**。
- body `0x57EB40`は保存済Ghidraの個別5点解析対象として未取得。`0x4E7ED0_procedure_callers.json`のcaller refだけあるため、mode0/1の内部意味・callee side effectは推測しない。jump table具体indexや0x4B618F以前の比較もVERIFY。
- `src/hakushin_compat/eb40_caller_contract.py`＋`tests/test_eb40_caller_contract.py`を独立実装、callsite 2パターン／AL lazy branching／iterating/skipの6件PASS。

### 2. 負値heal/status core 0x551490 は抵抗とdextで異なる終了順序

- `exe/T012_HEAL_ATTR_PROBE.txt` VA0x5514D7..0x551E23、`data/T012_BATTLE_CALC.md` §43–46の既存B-owner仕様をread-only確認。r absent default5、0..10 clamp、chance<100時は1コアにつき1 CRT draw、>=100時chance drawは無し。
- amount>=0なら負値専用gateへ入らない。amount<0はまずroll<r²（VA0x551855..0x551857）を1 drawで判断、真なら**0x551DF5関数終了**して残りの候補を処理しない。偽ならATT/DEF dext contestで追加2 drawを実施、差<=10で**0x551D40 次候補へ**、>10でその候補のeffect側へ進む。
- `damage_consti`は初期11スロットの表（3,2,1.75,1.5,1.2,1,5/6,2/3,4/7,0.5,1/3）に対し、native初期化0x45B3E1..0x45B43Bで最大11個の非zero raw int値×0.01を上書き、zeroは初期値維持。r0なら係数10、r10なら0の別分岐。**x87 score演算・0x5D1B80整数化、実能力値mutationは未実装/VERIFY**。
- `src/hakushin_compat/negative_heal_flow_subset.py` と専用test10件PASS。合成oracleからnative丸め整数とdext marginを受けることで、branch/CRT直接draw数/次候補処理を保存nativeと整合させる。負値r²ブロックとdextコンテスト失敗を『同じ対象skip』に統合しない。

## 既存含む最終回帰

- `dev_lab/run_checks.ps1`はLocal Windowsでprocess PID28000／**exit0**／`DEV_LAB_ALL_CHECKS_PASSED`。Python単体テスト **172/172 PASS**（直前156＋新規16）。
- Map 151/151 byte-exact、atlas513 records、context204 assignments/203unique、script DAT590/14,591,845bytes、lexical spans42912、parent refs21,214（unresolved56,ambiguous1292）、sample event/scenario AST516 body（recognized71,346, opaque172）、1v1/2v2 headless各traceとAI120tickもPASS。
- **旧ゲームTARGET OBSERVED golden actual PASS0／新エンジンstrict REIMPLEMENT MATCH0。** 内部合成テスト172件を原作完全互換の証明と解釈しない。Unit/Spot/Power後半saveも前回と同じVERIFY。

## 次回優先

- 0x57EB40本体・0x4B618F上位分岐・`0x4E7ED0`との呼出関係は、将来適法かつ安全に許可された新しい証拠が得られた場合のみ追跡。拒否済Ghidraランナの再実行は不可。
- 負値heal実機比較の候補：同seedで候補2体、先頭候補r10で全停止 vs r0+dext差<=10で2体目へ、draw数とターゲット変化を記録。x87 integer roundingは実際の画面観測まで推測で決めない。
- DEV側は`docs/USER_MANUAL_TASKS_DEFERRED.md`に人手の要求を保留。ユーザーは現在PCを操作できないので提出を急がせず、後日一括確認に従う。

## 主要パス

- 研究結果: `rea_lab/decomp_task/STATIC_EB40_NEGATIVE_HEAL_20261010.md`
- 開発引継ぎ: 本 `dev_lab/docs/DEVLAB_HANDOFF_20261010_EB40_HEAL_172.md`
- 回帰一括実行: `dev_lab/run_checks.ps1`。結果JSONは`dev_lab/reports/`内。
