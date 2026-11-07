# T024: form_dashdummy 静的参照境界（2026-10-19）
ID候補: B-20261019-2116-01 / Task T024 primary・T011 source inheritance参考。
SOURCE: data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_速度・待機スキル.dat L72-93（read-only）。
SOURCE: data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat L2117-2134, L2137-2142, L3522-3529（read-only）。
[FACT] skill form_dashdummy : form_dashb は自身で slow_per = 500 のみ明示。親 form_dashb:form_dash は slow_per=300, slow_time=3, check=30000, range_min=800, special=999 等を明示する。
[FACT] normalized /a_default/script 内 *.dat を対象とするLocal Compactの文字列 form_dashdummy exact content searchは検索終了、検索一致 1・原文宣言1箇所のみ（2026-10-19 21時台）。検索範囲外・名前動的生成は不明。
[FACT] form_gannnigeboushi 本文が明示操作するのは form_dash / form_dashb。form_dashdummy を明示addSkill/eraseSkill/removeSkillしない。
[DELTA] 旧B-RC-20261019-2010-T024-INDEX-SAFETY-01 が扱った「2つの明示dashを加える処理」の再証明・代理登録ではなく、第三の継承Skill宣言とその直接参照の有無のみを独立確認。
[INFERENCE-VERIFY] 同じparent chainでも宣言があるだけでbattle runtimeに自動取得されるとは限らない。slow_per=500 が有効Skill実体になるか・別名前経路で生成されるかは不明。parent field mergeやspecial=999のruntime意味を断定しない。
[REIMPLEMENT] raw Skill declarationとparent edgeを保持し、form_dashdummy を form_gannnigeboushi の3番目のactive追加Skillとして捏造しない。定義存在・直接参照・effective inheritance・配布・実発動を別段階へ分ける。
[GOLDEN-DESIGNED/NOT RUN] 旧原作合法戦闘の full/kanni × getLimit=500/499 × cpu_red=0/1で、メッセージ、攻撃側Skill、移動/加減速、MP/RNG/next tickを可視確認。EXE/DAT/SAVE/map/input/capture SHAを記録し同一条件のnewと比較。dummyが非表示なら原本Runtime不存在と断定しない。
[STATUS] SOURCE-ONLY CANDIDATE; runtime VERIFY; 原作Gameplay Golden PASS=0、新旧strict MATCH=0、Task DONE+0。
[SAFETY] 既B-20261019-2010-01の拒否されたT024索引内容は再提出・分割・転記せず、同復旧IDはBLOCKED/NOT READYのまま。原本EXE/ZIP未実行・未変更。新規REA/Ghidra/Git/Remote/MASTER/T018/他レーン/設定/automation変更なし。
[NEXT] 同一文字列以外のSkill作成/差替え・既存B資料と衝突しない実効継承の独立証拠、合法戦闘の可視発動、許可されるB HANDOFF更新と読み戻しを確認する。
