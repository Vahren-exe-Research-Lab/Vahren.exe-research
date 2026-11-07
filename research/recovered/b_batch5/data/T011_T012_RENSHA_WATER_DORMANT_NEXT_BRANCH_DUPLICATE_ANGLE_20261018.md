# B-20261018-2313-01｜T011主/T012参照：連装放水砲のコメント化next枝と別枝の角度キー二重宣言
[DATE/TARGET] 2026-10-18 23時台 JST。迫真0.67の正規化原作script限定STATIC照合。同梱EXE既保存SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。新EXE実行・逆解析0。
[ORIGINAL FILE] data/normalized/hakushin067_core/a_default/script/32_ボススキル/B_2222_レイノアレフ.dat L318-546付近。既B-20261018-2021-02でroot rensha_watecannon→nt0→next2 nt1/nt2→next3 watecannon_w_nt1/nt2/pr2/pr0 の原文辺を保存済み（本IDで再READY計数しない）。
[NEW SOURCE 1] 同DAT L387-395の skill watecannon_w_nt1:b_cannon_nt1 は `//next = watecannon_w_nt3` をコメントに置き、有効な `next = @` を直接記す。watecannon_w_nt2:watecannon_w_nt1 (L396-411付近) は別途 `next = @` を直記。
[NEW SOURCE 2] 同DAT L412-443の skill watecannon_w_nt3:sk_ms は `next=watecannon_w_nt4` を直接指定。nt4は `next3 = watecannon_w_nt6,watecannon_w_nt7,watecannon_w_pr4` を直記する。
[NEW SOURCE 3] 同DAT L527-539の skill watecannon_w_pr4:sk_ms は同一block内で `start_degree_type = 4` の直後に `start_degree_type = 0` を再指定。sourceの宣言順は確定、nativeの二重key優先/実効角度は未確定。
[LITERAL CENSUS] Desktop Commander Local Compact正規化a_default/script全DAT literal search: `watecannon_w_nt3`計2行（コメント参照1、定義1）、`watecannon_w_nt4`計2行（nt3.next参照1、定義1）。`watecannon_w_pr4`計4行は部分文字列を含み、pr4bにもhitするため「4incoming edges」と解釈しない。
[STATIC CONSEQUENCE] 保存されたrootからの字面上の有効next/next2/next3辺だけを辿る場合、nt1のコメント内nextはedgeではなく、有効next=@からnt3/nt4/pr4へ到達する根拠にはならない。別の名前生成・native consumer・未知の間接経路による発動不可能性までは証明しない。
[EXE/VA/XREF] 既保存VA0x547096/0x5470A9の一般使用距離gate、0x57E5D3→0x57EB40のaction、0x550E70 damage、0x59FA40のSkill+A18/A1C callback表は参照のみ。これらと今回のnt3/pr4の直接xrefは未接続。拒否済VA0x5710C0..0x571500等の新規解析0。
[VERIFY] コメント/明示@のSkill.next専用解決、pr4.start_degree_type二重キーのparser precedence、子Skill runtime作成と到達、実方向Unit+0x18688、shoot latch+0x1E560、0x4E7ED0/0x580280、MP fallback/対象優先/着弾・HP変化・RNG・次tickは未確定。
[REIMPLEMENT] raw statement/comment/explicit-null/parent/referenceとcompiled effective child graphを分離。原作コメントをedgeとして登録せず、pr4の同一キー両宣言を順序付きrawとして保存し、どちらがeffectiveかはloader証拠まで決めない。
[GOLDEN] 原作合法なkmkks系列またはkmkks4の可視技能取得/出撃後のみ、原作旧新同EXE/DAT/SAVE/map/input/capture SHA・seed観測可否で実際の連装弾/効果/角度/HP/MP・次tickを比較。nt3/pr4不可視なら枝専用fixtureはINELIGIBLE、DESIGNED_NOT_RUN、旧GameplayPASS0・strictMATCH0。
[DEDUP/SAFETY] 既B-20261018-2021-02のroot chain、B-2109/2211のkmkks4出現経路、T024の別far二重キーとT005のgeneric precedenceを再計上しない。B-1813 / E-2053 / E-2145は独立BLOCKEDのまま。原本・MASTER/T018・他lane・REA/dev_lab・Git/push・Remote・設定・automationは変更禁止。
[READY GATE] 本detail、data/T011_DATA_MODEL.md、data/T012_BATTLE_CALC.md、evidence/LANE_B_HANDOFF.mdを同一IDで各独立readbackした場合のみ B OWNER LIMITED STATIC ORIGINAL SOURCE READY 1。E正式MASTER統合は別。