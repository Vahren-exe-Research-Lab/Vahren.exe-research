# B-20261016-1110-01｜T024 AI移動・待機Skillの同一block内 far/func 重複宣言と継承辺
[STATUS] B owner限定 STATIC ORIGINAL SOURCE READY CANDIDATE（detail/T024 owner/HANDOFFの3点readback後のみREADY）。原作Gameplay actual PASS0／old-new strict MATCH0／Task DONE増0。
[SOURCE] 迫真0.67正規化原本コピー data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_速度・待機スキル.dat（1-based行）。同フォルダ Ai戦闘制御_軍楽隊なし版.dat は使用caller。原本ZIP/EXE未実行・未改変、新binary解析なし。
[RAW BLOCK A] lines3..36 skill form_slow90 に func=missile がlines5,14の2回、far=on line6 と far=off line24が同一block内に明記される。check=2199(line18), range_min=800(line21), slow_per=90(line25), gun_delay=form_slow*3(line27)も同block。
[CHILDREN A] 同file lines38..68 の form_slow80/70/60/50/40/30/20/10 はいずれも :form_slow90 と slow_per 個別値をraw宣言。lines72..93の form_dash:form_slow90→form_dashb:form_dash→form_dashdummy:form_dashb も同sourceで親辺が明記される。
[RAW BLOCK B] lines102..126 skill a_wait1000_1 では func=missile lines104,112の2回、far=on line105 と far=off line115を同一block内に明記。check=2199(line113), range_min=600(line114), special=3(line116), slow_per=2(line117)。
[CHILDREN B] lines128..155 の a_wait1000_2/_3/_zinzai/_0/_999 は :a_wait1000_1 を明記。子にはspecialやcheck/range_minなど別raw overrideがあるが、自身のfar宣言はこのsourceにない。
[CONSUMER DECLARATIONS] Ai戦闘制御_軍楽隊なし版.dat lines730..772 は slow90..30 の addSkill→eraseSkill 命令を記述。lines536/649/656..663/1722 は a_wait1000_999/_zinzai/_1/_2/_0、lines2121..27 は form_dashb add/erase と slow90等removeを記述。これは原作sourceのcall宣言であり合法実行の確証ではない。
[DIFFERENCE/DEDUP] 既T024§7・§13・§14・§26 と T011 のspecial parserは再計上しない。本IDの新規scopeは「2基底skill内の明示重複field」と「そのfieldを自身で再宣言しない子へのraw親辺」の同定のみ。既T009 context battle_fast first-winsやA T005 generic property parser0x505210→insert-if-absent 0x463280をSkill farへ移植する根拠はない。
[FACT vs VERIFY] sourceには先行far=onと後行far=offが両方あることは確定。**effective far が on/off のどちらか、最後勝ち/先勝ち、special setter/親resolverの実順、farと通常射撃/移動BUFFの効果はVERIFY**。func重複は同値で、2回発火・2発になる証拠でない。
[REIMPLEMENT] AI skill raw declarationを入力順の重複key付きで保持。parse→property registration→inherit/override→effective Skill→合法battle add/erase→そのskillの動作/MP/方向・対象/slowを段階分離し、far=offを後勝ち前提でhard-codeしない。
[GOLDEN] 原作合法 full/簡易battleでslow tier90/80とwait1000_1/2/dashbの取得・発動を画面で確認し、同旧SAVE SHA/seed/inputの可視slow移動速度/MP/発射/対象/次tickを新側と比較。未取得=DESIGNED_NOT_RUN、内部property fieldのみINELIGIBLE。
[BOUNDARY] 対象EXE既登録SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。新規native VA/xref無し。既B source特有の新しいbranchやfirst-wins成立を捏造しない。
[NEXT] B-owned保存Skill far parser/lookupの合法既証拠が無ければVERIFY維持。並行でP0 T012 576E80/4E7ED0→弾/HP/MP とT013対象順位へ戻る。旧安全拒否payload/VAを別tool/path/shell/Remoteで迂回しない。
[OWNERSHIP] Bの本detail＋data/T024_HAKUSHIN_BATTLE_AI.md＋evidence/LANE_B_HANDOFF.mdのみ編集。MASTER/T018/他owner/REA/dev_lab/Work/WRQ/原本/Git/push/設定/automation変更禁止。正式MASTER採否はEのみ。
