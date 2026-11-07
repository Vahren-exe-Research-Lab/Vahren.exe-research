# B-20261019-0408-01｜T012 保存済54DA10座標計算・2B8分岐（限定STATIC）
[OWNER] B/T012。対象は迫真戦記同梱Vahren.exe既保存SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。原本EXE実行・新逆解析なし。
[PROVENANCE] B既存 read-only exe/T012_DAMAGE_CALLER_CONTEXTS.txt のVA0x54DA10..0x54DADB。原作DATからのskill識別・合法取得証拠は本件では未取得。
[FACT-A] VA54DA16はESI+0xB0のpointerを参照し54DA1Cでbyte+0x2B8を検査。ESI+0x40/+0x48から中点相当の第1座標を算出（54DA2E..33または54DA3F..43）。+2B8!=0の場合はESI+0x44/+0x4Cから第2座標も中点化（54DA34..3B）、==0の場合はESI+0x4Cをそのまま第2座標候補にする。
[FACT-B] VA54DA56..66は上記2座標・引数1・ESI+0xA4を用意し0x4FACA0をCALL。返却pointerの先頭2成分を54DA73/54DA7CでESI+0xE0/+0xE4へ格納する。54DA82..91はESI+0xA4からのvtable+8を2座標引数でCALLし、返却object+0x10Cの値を読む。
[FACT-C] VA54DA9Dで同+2B8を再判定。非0は54DAACでESI+E4からvirtual-result+10Cを減じ、54DABCで0x4C5EF0をCALL。ゼロは54DAC9でも差を算出し54DAD2で0x4C60F0をCALL。両方54DAD5付近から別RETへ。両helperの内部作用は未確認。
[STATIC-SCOPE] 条件付きの座標準備・値格納・helper分岐の命令列だけ確定。ESI実体のruntime型、+2B8のproperty名、4FACA0/4C5EF0/4C60F0の意味、後続の可視位置・当たり判定・攻撃結果はVERIFY。
[DEDUP] 先行B-20261019-0209-01（別関数54DAE0のdamage core/virtual/F8）とB-20261019-0210-02（別関数54DB60の580280/F8）を再計上しない。保存窓の54DADC..DF INT3境界を超えた同一object/同一action連結は未証明。
[REIMPLEMENT] sourceSkillField2B8(nullable)、入力rectangle4座標、midpointMode、4FACA0戻り2成分、virtualResult+10C、helperA/B呼出を別stageにし、「弾発生」「命中」「HP減少」を推測成功扱いにしない。
[GOLDEN] 合法旧UIで当該Skillと+2B8=0/非0の実効差が独立に確定した場合のみ、同EXE/DAT/SAVE/map/input/capture SHA、可視軌道・位置・発射時刻・対象HP/MP・次tickを旧新比較。内部fieldのみならINELIGIBLE。現状DESIGNED_NOT_RUN、原作Gameplay PASS0、新旧strict MATCH0。
[VERIFY-NEXT] 保存済みB所有parser/xref資料から+2B8のproducer・callerとSkill実体、54DA10経路と攻撃resultの別stage関係を調べる。未保存資料や安全拒否領域は再解析しない。
[READY-GATE] detail/T012_BATTLE_CALC.md/LANE_B_HANDOFF.mdの独立3/3 readback後のみB LIMITED SAVED-ASM STATIC READY。EのみMASTER正式統合。Task DONE増0。
[SAFETY] 原本ZIP/EXE/SAVE・MASTER/T018/他lane・REA/dev_lab/Work/WRQ/Git/push/設定/automationを変更しない。既拒否B-20261019-0117-01、B-20261019-0210-02、B-20261018-1813-01はBLOCKED/NOT READYのまま。