# 迫真戦記 ver0.67 REA独立追加監査 — T013 主探索・支援探索の除外順序
日時: 2026-10-11 17時台 JST。状態: CONFIRMED-SAVED-NATIVE（局所分岐のみ）／VERIFY（callee・ゲーム挙動）。新規Ghidra=0、既存VERIFIEDへの新昇格=0、原作実機NOT RUN。
対象SHAは保存run `20261009T225741694Z` の `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。今回の実体SHA再計算なし。
照合元（既存／読取専用）: `exe/T013_TARGET_SELECTOR_PROBE.txt`、`exe/T013_SUPPORT_BUILDER_FULL.txt`、`exe/T013_SELECTOR_HELPERS2.txt`、`rea_lab/decomp_task/runs/20261009T225741694Z/57B870_procedure_assembly.json`。
Ghidra（親関数0x57B870） info `ev_c4fcdda0f9486944ccdcfe1354a6d2e37f2b68761dfd2e47b7df9a11cd367612`；pseudo `ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc`。
assembly `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`；callers `ev_911883dad3560c441dc40b2e53fe8fb1e83d4b85c4cbf622e80eb7ed59e4a8c4`；callees `ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203`。
※0x514D60・0x514F10自身には5点REA evidence IDが未取得。これらをVERIFIED関数へ昇格してはならない。

## 0x514D60 — 主探索（T013、候補レコード返却）
- 0x514D71..0x514D9E: 引数UnitのXYを取得し、選択された候補コンテナ +0x48/+0x4C に含まれる4byteポインタ列を走査。
- 0x514DB1..0x514DC2: 候補Unit+0x1867C≠0ならskip。候補ポインタ==引数Unit（self）ならskip。
- 0x514DC4..0x514DF5: Unit+0x1C0=0ならstealth roll無し。非0ならCRT rand15→FPU 0..100相当→0x5D1B80変換を行い、Unit+0x1C0>rollでその候補をskip。丸め・境界分布はVERIFY。
- 0x514DF5..0x514E42: XY差を32bit IMUL/ADDして0x5E3B70へ渡し、最短候補を更新する局所FPU比較。signed overflow / x87は保持すべき未確定境界。
- 0x514E48..0x514E75: その時点の単一選択候補の+0x18Cと保持距離を比較し、半径不足側・未選択側は第2走査へ。全候補の+0x18Cを先に除外する方式とは異なる。
- 0x514E75..0x514EF2: 第2候補列+0x58/+0x5Cを走査。+0x1867C!=0とselfはskip、XY距離比較を行うが、このループには直接の+0x1C0ステルスrandゲートはない。
- 0x514EF2..0x514F0B: 選択済ポインタ/距離の組を呼出側レコードへ書く。第1/第2列のゲーム上の名称・選択順位全体はVERIFY。
