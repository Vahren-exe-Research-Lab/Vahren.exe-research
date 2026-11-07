# B-20261017-1313-01｜F13 heal3技能が同じ別名gun_delay=b_heal*3を明示（T011主／T012参照）
[DATE/OWNER/CLASS] 2026-10-17 13:13 JST。T011 raw Skill model／T012 heal待機参照。CONFIRMED-SOURCE-DECLARATION ONLY。E正式統合待ち。旧原作Gameplay actual PASS0、新旧strict MATCH0、Task DONE増0。
[ORIGINAL] normalized original 新約迫真戦記ver0.67 CORE a_default/script/30_スキル/F13_heal_support.dat。原本ZIP/EXEは実行・変更せず、既存正規化コピーをLocal Compactでread-only照合。
[SOURCE FACT 1] F13 1-based L80-87 skill b_heal:m_heal は mp=0, gun_delay=b_heal*3, str=magic*150。
[SOURCE FACT 2] F13 L89-98 skill cook_heal:m_heal は mp=0, gun_delay=b_heal*3, str=magic_dext*1500, str_ratio=0, slow_per=35。
[SOURCE FACT 3] F13 L2163-2173 skill dango1:m_heal は mp=0, gun_delay=b_heal*3, str=magic*200。三者は別skill ID・共通parent m_heal・同一raw gun_delay参照キーである。
[CORPUS-BOUNDED] F13全2204行のコメント(/* */・//)を除外した宣言字句集計ではactive skillヘッダ141、直接gun_delay=NAME*integer 27、宣言skill名と参照キー名が異なるもの18。これはF13限定のraw行数で、全script数・effective Skill数・共通クールダウンの実作用数ではない。
[EXE/XREF PREEXISTING ONLY] B保存native exe/T012_SKILL_POST_57BE30_NATIVE_20261013.txt VA0x57BEC3 call0x4C1200（Skill+0x210>0、key+0x214→Unit+0x1E53C map）、0x57BEDB node+0x28更新は既B-20261013-1110-01の既知事実。raw gun_delayキーが+0x210/+0x214へcompileされるproducer／consumer結合は今回未証明であり、類推から断定・READY化しない。
[DELTA/DEDUP] 既T011の親/skillグラフとT012 postskillノード処理を再採番せず、新しいのは同一F13内の独立heal3種→同じ他Skill delayキーという具体的raw alias事実＋コメント除外集計。安全拒否済B-20261017-1216-01はBLOCKED/NOT READYのまま、本IDはそのfactory/postskill crossjoinを救済・再投稿しない。
[REIMPLEMENT] raw skill ID／parent edge／gun_delay参照キー／倍率を別カラムとして保存。cook_healとdango1を自身のIDキーへ機械的に正規化しない。native effective cooldown slot、key共有・duration単位はVERIFY。実際に3技能が同じUnit上で共有待機するか・別Unitへ影響するかはUNKNOWN。
[GOLDEN DESIGNED NOT RUN] 原作で3技能取得が合法なら、b_heal→cook_heal→dango1の使用順を入替、初回・連続・別Unit同tickをold/new同EXE/DAT/SAVE SHA、入力列、seed可視範囲で比較。可視使用可否・再使用までの時間・HP/MP・対象と次tickを観測。未取得/内部keyのみはINELIGIBLE、原作actual PASS0・strict MATCH0。
[NEXT/READY GATE] 既保存合法native loader/consumerの独立照合、3技能のUnit/Class取得元、他技能とdelayキー共有例の正規化source調査。detail・T011・T012・LANE_B_HANDOFFの4点ID/境界/VERIFY独立readback成功まではNOT READY。EのみMASTER/T018統合。
[SAFETY] 0x5710C0..0x571500等旧拒否VAやB-1216拒否payloadの別tool/shell/path/Remote迂回なし。原本、他レーン、MASTER/T018、REA、dev_lab/Work/WRQ、Git/push、設定/automation変更なし。
