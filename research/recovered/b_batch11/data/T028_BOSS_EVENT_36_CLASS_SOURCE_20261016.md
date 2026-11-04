# B-20261016-1210-01｜T028 ボス死亡イベント36定義の分岐別原文分類
[TASK/DATE/OWNER] 2026-10-16 12時台 JST。T028主・T011参照。SOURCE-ONLY CANDIDATE／HANDOFFとownerの3点readback前はNOT READY。原作Gameplay PASS0／strict MATCH0／Task DONE+0。
[SOURCE] 原本COREから既存正規化された data/normalized/hakushin067_core/a_default/script/50_その他新システム/siki_ボス側近.dat、全398行。36個のevent宣言を閉じ括弧対応で走査し、各bodyのroutine/skillTroop/pushRank/setv/addLimitを分類。正規化コピーのみread-only。
[FACT CENSUS] 36件=ランク直接4分岐5件（boss_skrnbu/jgn/tisa/icg/web）＋直接固定Skill12件（ganboru・sakerobo_23/23b/23c・noel/wagnas/dantag/bokhohn/kzinssie/subier/rocbouquer/boss_snnm）＋@commander設定→base_demoralization呼出18件（hzn_r等）＋特殊rank非0 gate 1件（kankure_po5_r）。以上は本ファイルの構文別宣言数であり原作戦闘での発動回数ではない。
[FACT SOURCE POSITIONS] 直接rank群L3-111、固定群L114-203、汎用base委譲群L207-265/L280-398、例外kankure L267-278。各18件委譲bodyでpushRank(...,commander_rank)・setv(@commander,...)・routine(base_demoralization)を同時に1回ずつ原文宣言。固定12件はdirect skillTroopであり、このbodyにroutineはない。
[INDEPENDENT CONTRAST] boss_web_demoralization L90-111はrank1..4のskillTroop後に独立if(inBattle(chuboss_alc)) addLimit(514)。boss_web_r_demoralization L237-245はpushRank(boss_web_r)→setv(@commander,boss_web_r)→routine(base_demoralization)を宣言し、当該body内にaddLimit無し。別原作siki.dat L536-548のbase_demoralizationはrank0..4のskillTroopのみでaddLimit命令無し。
[NATIVE PRIOR/BOUNDARY] 既T028§2の標準死亡イベント入口 VA0x5789F2→0x4321B0は参照のみ。上記36個別eventの実dispatchとcall順、runtime rank/flag、別eventでの追加addLimit、VM実行やSAVE回復はVERIFY。web_rでゲーム全体としてaddLimitが絶対起きないとは結論しない。
[NEW VS OLD] T028§5のボス個別効果列挙、B-20261013-0915-01のsnnm固定Lv2、B-20261013-0915-02のkankure ID相違は再READY計上0。新増分は36宣言の漏れなし構文別分類＋web正編/ランシナ別bodyのlimit command有無＋base委譲18件の受渡し形の横断比較のみ。
[REIMPLEMENT] 36イベントを名前→body種別のdistinct dispatchとし、5 direct rank・12 fixed・18 base-routine・1 exceptionalを混同しない。boss_web本編とboss_web_rランシナのaddLimit命令を一律共通化しない。dialog gate・skillTroop・inBattle/addLimit・VM yield/returnを独立stage/receiptに保持。
[GOLDEN DESIGNED/NOT RUN] 正規ゲーム導線のboss_web vs boss_web_r死亡、rank0/2/4、inBattle(chuboss_alc)真偽、demoralization_dialog 0/1/2を可能な条件だけ比較。旧/新同SAVE SHA・同seed/操作で可視士気stats、戦闘残り時間（+514の表示変化）、死亡ダイアログ、HP/MP/次tickを別receipt化。実入力成立・旧原作captureは未取得、internal event文字列だけはINELIGIBLE。
[VERIFY/NEXT] Unit dead_eventと36個別名の合法ユニット紐付け・特にweb/web_r双方が存在し得る場面、inBattleの真偽・limit実適用・イベント実発火・重複呼出/帰還。T012通常射撃/HPが最大P0なのは不変。本source taxonomyはT012攻撃結果の解決ではない。
[SAFETY/STATUS] 原本ZIP/EXE/SAVE実行/編集なし、新Ghidra/REA/逆解析なし。拒否済みB-20261016-1110-01 T024のHANDOFF payloadと拒否VAには触れずNOT READY維持。MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/設定/automation変更無し。
[STATUS] DETAIL CANDIDATE SAVED; T028 OWNER/HANDOFF READBACK PENDING; E FORMAL PENDING; ORIGINAL GAMEPLAY PASS0; STRICT MATCH0。
