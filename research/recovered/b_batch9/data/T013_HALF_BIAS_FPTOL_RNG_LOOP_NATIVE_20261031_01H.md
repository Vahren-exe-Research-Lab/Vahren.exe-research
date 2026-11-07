# B-20261031-01H-T013-HALFBIAS-FPTOL-LOOP-01｜AIカテゴリ数値の0.5初期値・整数変換・候補loop
Owner B/T013（T024参照）｜2026-10-31 01H JST｜STATIC / INFERRED / VERIFY / NOT READY
## 証拠源・未回収と安全
- Desktop Commander Local Compact接続成功。E所有MASTER正式checkpoint196/READY596は既存確定値、解析規約、B5 owner、B HANDOFF、B Library/未同期監査、00H研究を先読。11H拒否要約3件はBLOCKED/再試行なし、SAFE134/HOLD21、Library差54、10/25原文欠落・他owner意味重複OPEN。
- 研究用原作PE `rea_lab/targets/hakushin067_Vahren.exe` 実バイト SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9 SQLite現物141033472B SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、URI mode=ro&immutable=1/PRAGMA quick_check=ok。PC標準V3を切替えず、Ghidra再解析・旧ゲーム操作・書換0。
## 新規ASM確認①：初期値と再投入
- 原作ASM `0x44951C FLD qword [0x63B050]` と `0x44C9D0 FLD qword [0x63B050]` はカテゴリ候補処理開始前にx87へ同じ値を積む。PEの64bit浮動小数定数 `0x63B050=0.5` を直接byteから確認。
- `0x449688 FILD DWORD [0x65C150]`、`0x449692/0x44969F/0x4496A7 FMUL`→`0x4496AD FADDP ST1`はこの0.5に200×係数を加算。後半 `0x4496C9 FLD [0x63B050]` は`0x577220`のUnit書込みを終えた後、次候補へ0.5を再投入する。`0x4496EB FSTP ST0`でループ最終値をpop。
- mode2後段にも `0x44C9D0 FLD`（別分岐`0x44CA0F FLD`）と、Unitラベル更新後の`0x44CBE6 FLD [0x63B050]`、`0x44CC21 FSTP ST0`があり、同じ候補間x87状態回復を示す。`0x4496C9`位置自体は00H資料のNEXTに出現済みで再新規計数しない。
## 新規ASM確認②：整数変換2系統と結果上限
- `0x5D1B80 CMP DWORD [0xB14A40],0` / `0x5D1B87 JE 0x5D1BB6`。非zero側は`0x5D1B92 FSTP qword`→`0x5D1B95 CVTTSD2SI EAX`（SSE、0方向への切捨て）。zero側は`0x5D1BBF FLD ST0`→`0x5D1BC5 FISTP qword`→`0x5D1BC9 FILD qword`→`0x5D1BD9 FSUBP`で丸め値との残差を求め、`0x5D1BDB`から符号に応じた`ADC/SBB`補正。x87 FISTPの丸め値そのものを返すだけではない。
- 有限・正・小さい値に限れば、両経路は整数変換を0方向切捨てに整合させる構造（INFERRED）。x87制御語・例外・NaN・INT32外・オーバーフロー時の同値はVERIFYでありABIの確証ではない。
- 元PE `0x5B6EAB CALL 0x5BC6A9`→`0x5B6EB5 IMUL 0x343FD`→`0x5B6EBB ADD 0x269EC3`→`0x5B6EC3 SHR16`→`0x5B6EC6 AND 0x7FFF`。返るRNGは整数0..32767（STATIC）。seed状態/各tickでの初期化・全系列のGoldenはVERIFY。
- 従来00Hの `0x4496AF CALL0x5D1B80`→`0x4496B9 CALL0x40ED80` と `0x44CBxx` inline RNGをこの新しい0.5と照合すると、通常有効Unit処理の正数系では N=trunc(0.5+200×c)、sample=1+trunc((RNG()/32768)×(N-1)) と解釈できる。
- 係数 c=0.6/0.3/0.8（category 0/6/その他）からN=120/60/160、推定sample範囲は1..119 / 1..59 / 1..159。RNG=32767でもNに達しないことが境界差分。呼出経路ごとの追加RAND・Unit有効性・初期FPU・副作用差はVERIFY。物理的な移動距離/行動時間との同定は禁止。
## 静的証拠・非重複
- V9 function 0x449500 / 0x5B6EAB、対象PE限定Capstoneを使用。PE 0x449500+0xF0 SHA=898EFBB570F1CD78DEAA5A5597BAAE64198028D71DA2B960607871C66490AA77、0x5D1BB6+0xB0 SHA=27E015BDFDD7B9C7BE7BE4ED399673D2FE4F2C772D8608D9DEC9A1C2F598、0x5B6EAB+33B SHA=46D40B1406D899214EB90271E479AA722B5F9238799485D5F833D881726C5DAA。
- T013 owner・B HANDOFF・00H詳細の事前literal検索では新`0x44951C/0x5D1BDF/0x5D1BF8/0x44CC21`は全て0件。旧`0x4496C9`は各1件（予定先）で重複計上なし。全別owner・10/25欠落資料の意味的完全重複照合はVERIFY。
## 原作Golden・未解明P0・再開
- 無改変原EXE、20倍前DAT、同一SAVE/MAP/入力/seedでcategory 0/6/2/7、0/1/複数候補・Unit5gate・[0xB14A40]分岐、FPU初期/丸め・RNG返値・Unit+0x1E4FC/+0x1E4F8・翌tickを同runで観測するまでDESIGNED_NOT_RUN。原作Gameplay Golden PASS0 / strict MATCH0、新B READY0/E MASTER統合0/DONE0。
- 次回は0x449549..0x4495B7の特別カテゴリ1/7での0.5再設定と、0x44CA0F..0x44CC21の2経路のFPU初期・終端を突合。その後T011召喚/EXP、T012 status/damage、T024通常AI、T028士気・退却を優先。
- 本研究は旧23H/00Hの係数・Unit2field/RNG helper既知成果を二重計数しない。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/既存scheduleへの書込禁止を維持。
