# B-20261015-0709-01｜T012 kind2通常射撃の子候補vectorは各反復後にbegin/endを再読取する
[DATE/TASK/STATUS] 2026-10-15 07時台JST、T012 primary/T013 reference。BOUNDED SAVED-X86 STATIC CANDIDATE。旧未改変原作Gameplay PASS0、新旧strict MATCH0、Task DONE+0。
[ORIGINAL/READ-ONLY] 迫真ver0.67 CORE同梱Vahren.exe SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。B既保存exe/T013_SKILL_HANDLERS_BOUNDED_NATIVE_20261013.txt VA0x57EFA9..0x57F0A0を参照。原本EXEは起動・変更・再抽出しない。
[ENTRY-FACT] VA0x57EFA9/0x57EFAFがSkill+0x100(begin)と+0x104(end)を読み、0x57EFB5..0x57EFCAでend-beginから0x1C-byte record数を計算。0件なら0x57F0A6へ。0x57EFD2はordinal用offset=0、0x57EFDEで現在begin+offsetを参照する。
[PER-ITERATION-FACT] 子候補lookupの後、VA0x57F02E/0x57F045/0x57F06Fで分岐別calleeを呼び正常に0x57F077へ合流。57F077でSkill+0x100(begin)を再読、57F07Dで+0x104(end)を再読し、57F083でoffsetを0x1C増分、57F088..57F09Eで再度vector個数を求め、次ordinalが現時点個数未満なら0x57EFDEへ戻る。
[STATIC CONSEQUENCE] 正常に整合したrecord配列・callee正常returnを前提に、初回のend pointer/件数スナップショットを反復終了まで使い回すループではない。各callee後の現在のbegin/endから次回分を判定・参照する。beginの再配置・個数増減が起きれば次ordinalが異なるrecordを指し得るが、calleeが実際にこのvectorを書き換えるかはVERIFY。
[BOUNDARY] 0x57F0A6の+F4/+E4追加段階・57BE30・AL出口は既B-20261015-0611-01でREADY、本IDでは再READY化しない。Skill+0x100/+0x104を原作DATのnext3等の特定キーと同一視するnative setter証拠はまだ無い。ill-formed pointer/negative count、0x57F121 error branch・例外の合法到達も不明。
[WORK IMPLICATION] child begin/end とordinal/offsetをstageごとに保持し、factoryが正常帰還した後にcurrent begin/endとcountを再評価する契約。固定配列へ無条件変換・初回件数のまま全反復する実装はstrict候補として未証明。実際の変動や原作結果を捏造せずVERIFYを残す。
[GOLDEN DESIGN / NOT RUN] 未改変原作で合法kind2/mode0技能・子候補0/1/2と合法に子配列変化が誘発できる場合の前後画面/Skill/弾数/HP/MP/次tickを同SAVE SHA/seed/入力で新実装と比較。vector内部観察だけならINELIGIBLE。原作Gameplay actual PASS0、strict MATCH0。
[DEDUP/NEXT] B-20261015-0611-01の後半call graphとB既存support_ai_a子loopを再計数しない。次はB保存Skill parser/list writerから+100/+104 raw keyの根拠と合法実Skillにおけるvector変動可否、T013最終target順位、T012射撃結果、T011 cross-kind。拒否済0x5710C0..571500/0x58021E..580340/0x4E13F0や過去書込拒否payloadを別tool/path/shell/Remoteで迂回しない。
[OWNERSHIP] B資料/本HANDOFFのみ編集可、MASTER/T018/他owner/REA/dev_lab/Work/原本/Git/設定/automation非変更。研究Eのみ正式統合。
