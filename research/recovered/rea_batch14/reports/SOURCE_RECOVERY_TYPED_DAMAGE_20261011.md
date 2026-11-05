# 保存済みGhidraからの型付きダメージ/状態更新ソース復元（2026-10-11）

## Scope and evidence

- 実行対象の原EXEではなく、保存済みREA/Ghidra results・native owner TXTのread-only照合。新規EXE/Ghidra解析0、以前のSAFETY_REFUSALの迂回・再試行0。
- EXE SHA256は過去のRUN_RESULT記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（この回の再hashなし）。
- 0x550D80: runs/20261009T194358486Z/550D80_procedure_{pseudo_code,assembly}.json、native exe/T012_DAMAGE_CORE_DUMP.txt。
- 0x550E70: rea_lab/results/run_20261009T175957025Z_550E70_{pseudo,assembly,info}.json、保存済validated SHA manifest、native exe/T012_DAMAGE_CORE_DUMP.txt。
- 0x5D1B80: runs/20261009T215200079Z/5D1B80_procedure_{pseudo_code,assembly}.json、exe/T012_CONSTANT_PROBE.txt。
- 0x551E50: runs/20261009T215905915Z/551E50_procedure_{pseudo_code,assembly}.json、B所有data/T012_BATTLE_CALC.md §59。

## R1 0x550D80: 5つのx87攻撃式を疑似コードが省略

- Ghidra pseudoの各mode1..5はすべて引数なしのFUN_005D1B80()に見えるが、native assemblyはECX=skill、EDX=unit、Skill+0x27Cで異なる値を読み分ける。
- 数値A=Unit+0x98、B=+0xA0、C=+0xAC、R=Skill+0x288、S=Skill+0x280とした数学式（実際のx87中間丸めとは別）：
  - mode1: A*S+0.5、mode2: B*S+0.5
  - mode3: (A*R+B*(1-R))*S+0.5
  - mode4: (A*R+C*(1-R))*S+0.5
  - mode5: (B*R+C*(1-R))*S+0.5
  - その他mode: EAX=0。関数VA0x550D8E..0x550E69。
- mode1..5の末尾は0x5D1B80へのtail JMPで、Python round()と無条件に同一視しない。0x63B050=0.5は保存PE定数資料で確認。

## R2 0x550E70: 攻撃/防御fieldは別、randは2回

- 0x550F09: attack側の直接CRT rand15 1回。effective min/maxによりfactor(k)=min+(max-min)*k/32768。0x550F38: 上記0x550D80でattack base変換。0x550F53: attack base × damage_consti[r] × factor1 +0.5の別native整数化。
- 0x550F60..0x550FBEのdefense baseは mode1/4: target Unit+0x9C、mode2/5: +0xA4、mode3: +0x9Cと+0xA4を32bit ADD後、CDQ/SUB/SARで合計/2を0方向truncate。その他は0。負奇数へのPython //2、無制限整数加算は互換ではない。
- 0x550FD2 でdefense側のCRT rand15を別に1回引く。0x551003 でdefense base × factor2 +0.5をnative整数化、0x55100Bでsigned32 SUBによる攻撃寄与−防御寄与。
- ここはあくまでmode6特殊fix/距離補正/最低ダメージ補正より前。2 randを他calleeのdrawや原作1フレーム総RNGと混同しない。

## R3 0x5D1B80: 28-byte VERIFIED bodyの外へJZ

- Ghidra infoの当該function bodyは28byte。assembly 0x5D1B80 CMP [0xB14A40],0; 0x5D1B87 JZ 0x5D1BB6。分岐先0x5D1BB6はこの保存body外であり、通常の丸め動作は関数5点の取得だけでは未確定。
- 非zero分岐では0x5D1B92 FSTP double; 0x5D1B95 CVTTSD2SIによりbinary64 spill後の符号付きint32への0方向truncate。overflow/NaNのinvalid戻値は未実装。標準branchをPython roundと推測置換しない。
- dev_labのFractionモデルは読み出したbinary64 operandからの正確な数学値を記述するだけで、x87 80-bit演算や繰返し中間丸めは再現していない。native結果は明示callbackで受ける。

## R4 0x550E70最終damage仮想呼出の条件順

- VA0x5510E1..0x551156: r=10ならdamage handler virtual callをskipして後段へ。r!=10でもSkill+0x280=0ならhandlerには0を渡す。mode6なら普通の最低値補正を通らずpre-gate値を渡す。通常modeかつr=0なら0xF4240(1000000)を渡す。
- 通常r1..9はUnit+0x1867E非0ならglobal+0x65BD80倍率を別native整数化して、その後btl_min_damageとsigned比較し最低値へ引上げる。
- 0x551154の仮想関数の効果をこの局所staticだけでHP減少成立と断定しない。r10でdamage virtual skipでも、0x551156以降のhit-context処理へ進み得る。

## R5 0x551E50 命中文脈の先行フラグとlinked object更新

- Skill+0x2A8=-123456.0 sentinel、actor+0x1D0 null、actor+0x18614!=0、context+0xC既非zeroで早期return。通過時0x551E9Fでcontext+0xC=1を先にstoreし、Unit+0x1C8 linked objectへ。
- ratioは分母0なら0。Skill+0x40 mode3=0.02固定、mode4=0.01固定、mode5=clamp(0.01..0.2)、その他=clamp(0.01..0.33)。第1引数object+0x185FCとの算術と0x5D1B80丸めはnative callbackで表現。加算先は別のUnit+0x1C8 linked objectであり両者を混同しない。
- Skill+0x2A8==0時のみSkill+0x44/+0x4C/+0x74条件を処理した後10最低値へ。非zero時は別倍率計算でこの最低値保証はない。
- VA0x551FB2でlinked+0x16CへのDWORD加算、0x551FC9ではlinked+0x170をunsignedで比較し、閾値成立で0x58A650を呼ぶ。ここから先のlevel-up実作用/UIはVERIFY。

## DEV成果と境界

- dev_lab内に typed_damage_fragments.py（10試験）、damage_two_draws_subset.py（8）、damage_final_branch_subset.py（8）、hit_linked_award_subset.py（9）を追加、専用合成計35試験が成功。
- 全回帰を別途実行する。原作EXEのTARGET OBSERVED0、golden実機PASS0、new strict MATCH0。重点静的39/48は変わらず、新規Ghidra関数取得0。
- 原本ZIP/EXE・A〜E owner/T018/MASTER・Git・Remote・MCP/Windows設定・automationに書込しない。

