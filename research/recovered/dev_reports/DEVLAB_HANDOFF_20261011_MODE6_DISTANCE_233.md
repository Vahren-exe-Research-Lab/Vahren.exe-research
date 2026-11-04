# 迫真戦記再開発 dev_lab 追加解析: Mode6 / x87 / 射程減衰 (2026-10-11)

## 正本と作業範囲

- 作業開始時Eレーン MASTER_LEDGER.md checkpoint80、統合175ID=A52/B44/C43/D36、Task34 DONE9/IN_PROGRESS21/VERIFY4、evidence/ANALYSIS_LANES_PROTOCOL.md read-only確認。後続スケジュールにより進む場合はその最新版を優先。
- 以前保存したGhidra静的5証拠セット39/48に新規取得なし。重点81.25%は**全EXEの逆解析率ではない**。ユーザーのゲーム再実装の客観的完成率は未測定（主観的初期推定約5～10%）。
- 原本EXE/ZIPやA～E所有native/read-onlyレーン資料、MASTER/T018、既往REA runner/QUEUE/PROGRESS、Git/push、Remote/MCP/OS/automation設定に変更なし。過去SAFETY_REFUSALされた解析/Unit constructor操作を同tool・別shell・Remote経路で再試行しない。

## 新しいソース互換仕様（既存nativeだけに基づく）

1. `exe/T012_DAMAGE_CORE_DUMP.txt` VA0x550FF9..0x551033: 0x551003 defense丸めの後にFPU stack+0.5が残り、mode6はSkill+0x280（binary64）×PE定数0x63B060(100.0)を加算、0x55102Eで追加native整数変換し結果でordinary attack−defenseを**上書き**。mode6でもこの地点へ来る前の攻撃/防御の独立rand15×2は消費済み。0x63B060は `exe/T006_AUDIO_LOOP_PREDICATE_PROBE.txt` hex記録。
2. `exe/T010_RUNTIME_PROBE.txt` VA0x5D1BB6..0x5D1BDD: Ghidra 0x5D1B80 body28byteの外にあるdefault変換の前半、FISTP QWORD→FILD QWORD→FSUBP等を新たに保存済み証拠から確認。以降のtailが無く、global0xB14A40の挙動/制御語/ties・80bit丸めの完成モデルは **VERIFY**。新しい逆コンパイルプロセスを実行していない。
3. `exe/T012_DAMAGE_CORE_DUMP.txt` VA0x55103D..0x5510D7: Skill+0x250=0なら距離減衰をskips。非zeroはsource/target座標+0x214/+0x218のsigned32差・2×IMUL・ADD、0x5E3B70 sqrt、(Skill+0x290 − 距離)/(Skill+0x290 − Skill+0x250)をx87で計算、0..1 clamp、damage×ratio+0.5→0x5D1B80 int変換。通常整数平方根の明確なsyntheticケースのみFractionで再実装し、非平方根やdenominator0をfail-closed。

## DEVLAB追加・試験

- src/hakushin_compat/typed_damage_fragments.py: `mode6_fixed_damage_before_native_convert`（明示mode6限定）。
- src/hakushin_compat/damage_two_draws_subset.py: trace `mode6_fixed_override` 追加。mode6のnative converter回数（局所）は以前の2→3へ修正（内訳 attack contribution / defense contribution / fixed）。
- src/hakushin_compat/damage_distance_gate_subset.py: 新規、範囲分岐と完全平方根限定のmath factor計算、native converterは明示callback。
- tests/test_mode6_native_fixed.py 8件 PASS、tests/test_damage_distance_gate_subset.py 10件 PASS、変更した既存test_damage_two_draws_subset.py 8件 PASS。
- 研究メモ: rea_lab/decomp_task/SOURCE_RECOVERY_MODE6_FTOL_20261011.md に関連命令と未確定範囲を保存。
- フル回帰 `dev_lab/run_checks.ps1`: Desktop Commander Local PID22012の実行完了exit0、**233/233 unittest PASS**（以前215件＋新規mode6 8件＋距離10件）。原作Map151、atlas513、DAT590、parent21,214、sample AST516、clock/VM/AI合成の各検査も成功、末尾`DEV_LAB_ALL_CHECKS_PASSED`。`EXE actual golden=0 / strict MATCH=0`継続。

## 新チャット向け再開順

1. 最初に `dev_lab/docs/PROJECT_HANDOFF_MASTER_20261011.md` と最新 MASTER_LEDGER/ANALYSIS_LANES_PROTOCOLを読んで、研究レーン予約・owned filesを確認。
2. `rea_lab/decomp_task/SOURCE_RECOVERY_MODE6_FTOL_20261011.md` のVAと `dev_lab/src/hakushin_compat/{typed_damage_fragments,damage_two_draws_subset,damage_distance_gate_subset}.py` を見てから、距離減衰の未知x87端点・全save・AI更新順を部分実装する。
3. 39件の保存済み疑似Cは `dev_lab/recovered_source/ghidra_c_pseudocode`、sourcebookやmanifestに揃う。新規Ghidraを安全拒否迂回で起動せず、保存証拠だけを使う。
4. 変更後テストをまず限定、最後にrun_checks全体を実行、旧EXE実機PASSとsynthetic internal testsを必ず別集計。
5. ユーザーはまだPCに触れず、sav・画面観測などは `dev_lab/docs/USER_MANUAL_TASKS_DEFERRED.md`に一括保留。いま依頼しない。

