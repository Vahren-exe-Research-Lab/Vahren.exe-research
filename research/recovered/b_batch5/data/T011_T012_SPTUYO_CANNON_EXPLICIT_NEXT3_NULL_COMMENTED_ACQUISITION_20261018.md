# B-20261018-1717-01｜T011主/T012参照・sp_tuyo_cannonの明示next3=@と取得宣言のコメント境界（限定原文STATIC）
[DATE/SCOPE] 2026-10-18 17時台 JST。normalized原作scriptと既保存T005/T011/T012・B HANDOFFの軽量照合のみ。新しいEXE逆解析・実行なし。
[EXE BASELINE/XREF] 対象既保存EXE SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。既T012 VA0x547096/0x5470A9通常使用gate、既T005 generic @ parser/fallbackはREFERENCE ONLY。next/next3専用native consumerまたはspecial経路の実際の値は新規に特定していない。
[SOURCE ROOT] normalized 30_スキル/C_必殺_クラス専用.dat L69-95のskill sp_tuyo_cannon:b_cannonはspecial=on/far=off、check=800/range=750/range_min=@/fkey=@、gun_delay=cannon*6を明示し、特にnext3=@とnext=sp_tuyo_cannon_nt、pair_next=sp_tuyo_cannon_prを直接指定。
[SOURCE CONTRAST] 同file L2-32の別子skill sp_cannon:b_cannonはnext3=sp_cannon_nt,b_cannon_nt_crit,b_cannon_nt_crit2,taiho_bom（原文4項）とpair_next=sp_cannon_prを直接指定し、rootにnext=sp_tuyo_cannon_ntのような直接経路を指定しない。既B-20261018-1616-01のsp_cannonを再採番しない。
[SOURCE NEXT] 同file L94-101のskill sp_tuyo_cannon_ntは独立宣言でrush=2/rush_interval=30/joint_skill=on、next3=tuyo_cannon_nt1,tuyo_cannon_nt2,tuyo_cannon_pr1,tuyo_cannon_pr2を指定。sp_tuyo_cannon_pr2は同file後段でnext=b_cannon_pr0を指定。
[LITERAL CENSUS] normalized a_default/script配下の全*.datについてliteral sp_tuyo_cannon検索は13マッチ行（20_クラス6、30_スキル7）。Class側の6行は 00_汎用兵科.dat L369/402/417と07_10_TNOK_レ_VAN_スカ.dat L329/363/378にある `//,self_a...sp_tuyo_cannon,` の行コメント内部である。
[ACQUISITION BOUNDARY] この限定検索ではsp_tuyo_cannonの有効なClass/Unit直接取得指定を確認できなかった。検索されたClass行はactive skill=...行の次にあるが `//` によりコメント扱い。コメント文字列には `self_a005sp_tuyo_cannon` 等の長いtokenの部分一致も含む。全ての間接取得・実際のUI保有が無いとは断定しない。
[GRAMMAR BOUNDARY] 既T005では通常generic propertyの単独@は明示suppressorとして親fallbackを遮る一方、特殊/list propertyはconsumer別検証が必要。sp_tuyo_cannonのnext3=@から『弾0・親の7件全部消去・nextが必ず実行』とは断定不可。
[NEW DELTA] 前B-1616はsp_cannonのraw next3直接4とnt後段を特定。今回の別増分は同じ親b_cannonを持つsp_tuyo_cannonのrootにある明示next3=@ + singular next + 別後段tuyo_cannon系4名、そして候補取得箇所6行がすべてコメントという取得ゲートを接続したこと。
[REIMPLEMENT] 原文parent/directNext3/presence+raw@/directNext/pairNext/chain-childを個別保持。source occurrenceをClass取得と誤認せず、コメント除去後にacquisition graphへ登録する。parent next3継承とnext発火・範囲・MP・発射/HP結果はresolved/runtime別receiptへ。
[GOLDEN] 合法な旧原作通常UIでsp_tuyo_cannon保有・発動の可視入口をまず確保できた場合に限り、old/new同EXE/DAT/SAVE/map/input/capture SHA・seed可能条件でsp_cannonとの差、発射段数・技能切替・MP・HP・次tickを比較。現在は取得未証明でINELIGIBLE/DESIGNED_NOT_RUN。
[VERIFY/P0] 有効取得/親・list parser・next3=@の実効意味/next実行順/normal-vs-special、Unit+1E560 latch/+18688方向、0x4E7ED0/0x580280攻撃結果、MP fallback、T013 final target/A18/A1CはOPEN。原作Gameplay PASS0・新旧strict MATCH0・Task DONE増0。
[DEDUP/SAFETY] 既B-20261018-1616-01と以前のCLASS cannon関係は再計数0。拒否済B-0121/0228/0515/0911/1110・E統合拒否0316/1328/1418と禁止VA5710C0..571500、58021E..580340は別BLOCKED／迂回0。原本・MASTER/T018・他レーン/REA/dev_lab/Work/Git/設定/automation変更0。
[READBACK/READY] 本detail、data/T011_DATA_MODEL.md、data/T012_BATTLE_CALC.md、evidence/LANE_B_HANDOFF.mdの4点へ同ID・境界・再実装・Goldenを保存し個別readback照合できた場合のみB LIMITED STATIC ORIGINAL SOURCE READY 1件。E正式統合別。
[STATE] DETAIL-CANDIDATE / B READY PENDING / E FORMAL PENDING / GAMEPLAY PASS0 / STRICT MATCH0
