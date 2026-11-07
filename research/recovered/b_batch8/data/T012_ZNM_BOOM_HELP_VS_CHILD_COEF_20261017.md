# B-20261017-2316-01｜ZNMブーメランhelp表示値と爆発子Skill原文係数の不一致（T012主・T011参照）
[TYPE/DATE] 2026-10-17 23:16 JST。B/T012 primary、T011 data model reference。STATIC ORIGINAL SOURCE LEXICAL比較のみ。実機Gameplay PASS0、new-old strict MATCH0、Task DONE+0。
[SOURCE] 読取専用の正規化原作 data/normalized/hakushin067_core/a_default/script/31_ユニットスキル/U_1_5_マリナーズ～革命企画.dat：root skill znm_boom:sk_ms（1-based L5040台）、末端 skill znm_boom_bomb1 / bomb2（L5132-5155）。新規EXE解析・原本実行なし。
[ROOT HELP LITERAL] rootのhelpは複数の攻撃説明を含み「[攻撃× 85％]」と「[魔力× 15％]」を表示する。いずれも近接/小範囲として作者が記述したヘルプ文字列。MP回復100の文面は既B-20261017-2017-01で記録済みにつき新規加算しない。
[CHILD RAW] bomb1は attr=sw / str=attack * 85、bomb2は attr=msw / str=magic * 10 をそれぞれ直接記述。両子のraw式は既B-20261017-2217-01で確定済み。本IDで再登録しない。
[NEW CROSS-CHECK] root helpの『攻撃85％』と子bomb1原文係数85は字面数値が一致。一方『魔力15％』と子bomb2原文係数10は一致せず、表示15対raw10という異なる数値が同じ技能族内に共存する。二子へのnext3参照は既B-20261017-2017-01/2114-01。
[NOT A GAMEPLAY BUG PROOF] root help文字列がbomb2の実効威力を直接記述すること、str=magic*10をそのまま10%と評価すること、親継承/他係数/重複ヒットの影響がないこと、どの子が何回発動するかは未確認。『原作の実ダメージは15%でなく10%』『作者のバグ』は主張しない。
[PRE-SAVED NATIVE / VA] B既存 data/T011_DATA_MODEL.md §10 のstr parser契約は Skill+0x27C mode attack=1/magic=2、B T012既存damage core VA0x550D80/0x550E70。今回の各子のcompiled Skill生成/実caller到達・最終HPはVERIFYで、上記一般VAを新規証拠として再算入しない。
[IMPLEMENTATION] help表示と実効damage formulaを分離し、UI文面から内部係数15を合成しない。原文ではbomb2 magic*10を保持しつつ、最終原作実機結果の補正と照合するまで係数の意味/乗算scaleを推測せずraw provenanceを添付。
[GOLDEN DESIGNED / NOT RUN] 旧原作の合法znm出撃＋root保有＋bomb2可視発火をまず確認。旧EXE/DAT/SAVE/input/capture SHA、seed（観測可能なら）、同Unit/HP/耐性/配置で旧可視HP差と新build結果を照合。ヘルプと子係数の文字列差だけではgolden成功とせず、実機Gameplay PASS0・strict MATCH0を維持。
[DELTA/DEDUP] B-20261017-2017-01はbranch graph、B-20261017-2114-01はnext timing、B-20261017-2217-01は爆発二子raw係数を既計上。本IDの新増分はroot help 15と子bomb2 raw10の『表示対実データ』対照だけ。T019はE所有につき本件から直接編集しない。
[OPEN/NEXT] 最優先T012 0x580280実作用、0x4E7ED0→射撃結果、Unit+0x1E560/0x18688、MP fallback、発射/HP/MP、T013 target優先、T011 parent継承はOPEN。本件だけで実HP結果は閉じない。
[READY GATE / SAFETY] detail＋data/T012_BATTLE_CALC.md＋data/T011_DATA_MODEL.md＋evidence/LANE_B_HANDOFF.md の4点独立readback後だけB限定STATIC SOURCE CROSS-CHECK READY。EのみMASTER正式統合。既安全拒否0x5710C0..571500/0x58021E..580340や旧B拒否はBLOCKED、別shell/tool/path/Remote等の迂回なし。原本/他owner/REA/dev_lab/Work/WRQ/Git/push/設定/automationは不変更。
