# 保存済み機械語の追加照合: T012 mode6固定damageと0x5D1BB6 FPU fallback

**時点** 2026-10-11 JST。対象ver0.67同梱Vahren.exeの既存REA/Ghidra 5点static VERIFIEDデータと、以前保存されたnative TXTだけを読み直した。**新規逆コンパイル/Ghidra/旧EXE起動0**、拒否済み操作を別shell/tool/pathで再実行しない。

## 結論1: mode6には通常の2-rand処理の後、独立した固定値変換がある

- 一次保存証拠 `exe/T012_DAMAGE_CORE_DUMP.txt` VA0x550F09..0x55103D、および `rea_lab/results/run_20261009T175957025Z_550E70_assembly.json`（初回validated）を照合。
- VA0x550F09でattack側rand15、VA0x550F38で0x550D80 attackBase、VA0x550F53でattack寄与のnative int変換、VA0x550FD2で独立defense側rand15、VA0x551003でdefense寄与のnative int変換、VA0x55100Bでattack−defenseを整数減算。**この2randはmode6分岐より前に発生する**（該当context gate通過時）。
- VA0x550FF9 `FLD qword [0x63B050]`=0.5、0x550FFF `FADD ST1,ST0`、0x551001 `FXCH ST1`の後0x551003で変換を呼び、変換がST0を消費すると元0.5がFPU stackに残る。
- VA0x55101BでSkill+0x27C==6のみ、0x551020 `FLD [Skill+0x280]`、0x551026 `FMUL QWORD [0x63B060]`、0x55102C `FADDP ST1`、0x55102E `CALL 0x5D1B80`、0x551033 `MOV EDI,EAX`。
- 保存PE定数証拠 `exe/T006_AUDIO_LOOP_PREDICATE_PROBE.txt` は0x63B050=0.5、0x63B060=100.0をhex bytesまで確認。したがってmode6にて変換直前の**数学式は `Skill+0x280 * 100.0 + 0.5`**。通常攻撃/防御の差とは独立して当該数値をEDIへ上書きする。`0x5510E1`以降のr10/scale0/ordinary minは更に別の分岐。
- 注意: x87 80bit intermediate、関数0x5D1B80のデフォルト丸め・FPU control wordは未確定。Python FractionとCVTTSD2SI非default局所で算術式・分岐・rand消費を試験したのであり、原作丸めへのgolden一致ではない。

## 結論2: 通常ftol branch 0x5D1BB6の保存native断片が存在した

- 前回SourcebookではGhidra `runs/20261009T215200079Z/5D1B80_procedure_{info,pseudo_code,assembly}.json` のbody=28bytes、0x5D1B87 `JE 0x5D1BB6`だけ確認。だからデフォルトbranch未解明としていた。
- 今回、新規逆解析コマンドを使わず、**既存 A所有 `exe/T010_RUNTIME_PROBE.txt` からVA0x5D1B9C..0x5D1BDDをread-only再読**。さらに0x5D1BB6以降の分岐前半が保存されていると判明。
- A/native記録：0x5D1B9Cは別の入口形で0xB14A40を比較し、0x5D1BA8 `FNSTCW`、0x5D1BAC `AND AX,0x7F`を扱う。0x5D1BB6 `PUSH EBP`、0x5D1BB9 `SUB ESP,0x20`、0x5D1BBC `AND ESP,0xFFFFFFF0`、0x5D1BBF `FLD ST0`、0x5D1BC1 `FST DWORD [ESP+0x18]`、0x5D1BC5 `FISTP QWORD [ESP+0x10]`、0x5D1BC9 `FILD QWORD [ESP+0x10]`、0x5D1BD9 `FSUBP ST1`、0x5D1BDDはsign branch。
- **FISTP QWORDによるx87 control word依存の整数化と、その値の再ロード・差分計算が存在**。これはGhidraで得た28byte限定pseudoの単純な`ROUND(in_ST0)`へ丸ごと置換できない根拠。ただし下流0x5D1BDF..0x5D1C15などの命令とフラグはまだ未取得で、`ceil`/`floor`/ties-to-even等の最終規則は未確定。
- この未取得下流を元EXE逆コンパイルの新規実行で取りに行ったわけではない。以後は既存保存TXTに完全なtailが無ければVERIFY/NOT RUN維持。既往SAFETY_REFUSALの迂回は禁止。

## DEVLAB追加

- `dev_lab/src/hakushin_compat/typed_damage_fragments.py` に `mode6_fixed_damage_before_native_convert`を追加（式と必須mode6確認）。`damage_two_draws_subset.py` のtraceに`mode6_fixed_override`を追加し、attack/defense rand15×2とmode6 extra native conversionを区別。
- `dev_lab/tests/test_mode6_native_fixed.py` 8新規試験、既存`test_damage_two_draws_subset.py` mode6期待2変換→**3変換**を新たな保存native証拠に基づいて訂正。
- 実ゲームのdamage virtual、x87 80bit丸め、r10抵抗によるhandler skip、scale0分岐は引き続き独立に扱う。全ゲーム実機Golden0、strict MATCH0。

## 次の優先

- FPU fallback 0x5D1BB6以降の保存済み原文が別の既存証拠に含まれるかREADONLY検索。既存保存末尾が無ければ未解析として残す。
- 0x550E70の0x55103D..0x5510D2距離/範囲補正のx87 stack・signed overflowを局所契約に切り出す。新規逆解析の安全拒否を再試行しない。
- Userのsavと実画面観測は後日まとめて。MASTERはEレーンのみ編集。


## 続報: 0x550E70の距離減衰式の局所契約 (新規保存Ghidra実行0)

- 保存済み一次native `exe/T012_DAMAGE_CORE_DUMP.txt` VA0x55103D..0x5510D7 と旧Ghidra 0x550E70 pseudo/assemblyをread-only照合。
- Skill+0x250==0ならVA0x551044から0x5510E1へ分岐し、距離sqrt・倍率・新たなint convertを**まるごとskip**。+0x250非zeroではsource/target x/y(Unit+0x214/+0x218)の符号付き32bit差を取り、2つのIMULとADDの低32bit算術を行う。
- VA0x55108Dで0x5E3B70 sqrt helper、0x551092 FSUBR [max+0x290]でmax-sqrt(squaredDistance)、0x551096..0x5510A4で(max-min+0x250)により除算する。0x5510A6..0x5510C6のFLD1/FLDZ/FCOM/FNSTSWによって倍率を**[0,1]へclamp**。
- 0x5510C8 FIMUL signed raw damage→0x5510CC FADD 0.5→0x5510D2 CALL 0x5D1B80のint変換→0x5510D7に結果格納。数学式 factor=clamp((max-sqrt(dx²+dy²))/(max-min),0,1) を確認。skill/射程/距離のユーザーUI意味はVERIFY。
- `dev_lab/src/hakushin_compat/damage_distance_gate_subset.py`で**平方根が厳密な整数になる合成ケースのみ**Fraction計算＋native converter callbackへ渡す。非平方距離・denominator0・負のwrapped squaredはfail-closed。元EXEのsqrt(x87 80bit)/rounding/ties/NaNを実装したとは呼ばない。
- 専用tests `test_damage_distance_gate_subset.py`10件PASS。mode6固定damage（100×scale+0.5）を同modelへ入れ、r通常時は最低damage clampをskipする局所経路の連結試験も合成PASS。HP virtualや旧実機strict matchは依然0。


## Final local test/packaging evidence

- `dev_lab/run_checks.ps1` をLocalでフル実行：PID22012 exit0、Ran 233 tests/OK、末尾DEV_LAB_ALL_CHECKS_PASSED。既存原作Map151/151,atlas513,script590,親21,214,ASTサンプル516のcheckもPASS。
- 以前215からmode6新規8、距離減衰新規10の**18件**増加。Synthetic source-side testであり旧EXE golden0/new strict MATCH0のまま。
- 新チャット総合引継ぎ `dev_lab/docs/PROJECT_HANDOFF_MASTER_20261011.md`（保存・readback済）、今回差分 `dev_lab/docs/DEVLAB_HANDOFF_20261011_MODE6_DISTANCE_233.md`、SOURCE_RECONSTRUCTION_ROADMAPのsource mappingを更新。
- 新独立source snapshot `dev_lab/recovered_source_snapshot_20261011_mode6_distance.zip`（39疑似C、Python、tests、2つのhand-off含む、原本EXE/画像/音楽/実sav無し）を生成、ZIP3専用テストPASS。

