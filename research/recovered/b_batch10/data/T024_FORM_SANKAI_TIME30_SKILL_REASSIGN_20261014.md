# B-20261014-0013-01｜T024 前衛崩壊後の散開技能再配布と騎兵待機解除の独立ゲート
[OWNER/REQUEST/STATE] T024 primary / WRQ-20261013-B-SKILL P0関連 / READY-CANDIDATE SOURCE-ONLY。原作実機Gameplay PASS0／新strict MATCH0／Task DONE増加0。
[PRIMARY] 迫真0.67既存正規化原作 DAT: data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat。Local read-only範囲（0-based）2901..2952, 3030..3069, 3108..3166, 3240..3291。原本ZIP/EXEは読出し・実行・変更していない。
[PROOF-1] form_inbattle内、getTime()>=30かつ左翼+中央のgeneral群が全死亡、右翼general群に生存者がいる場合はremoveSkill(@enemy_army,form_sankai_r3/r4)。右翼+中央全死亡、左翼生存の対称分岐ではl3/l4を除去する。実際の対象/副作用はVERIFY。
[PROOF-2] getTime()>=30 && zenneibocchi==1 && (f_l_kaimetsu==0 || f_r_kaimetsu==0 || f_c_kaimetsu==0) はr3/r4/l3/l4を全てremoveSkillする。三つの旗をANDに置換しない。
[PROOF-3] 左翼general全死亡、右翼と中央の生存者あり、かつ(zenneibocchi==0 || f_l==1 && f_r==1 && f_c==1)の場合、中央general index2,5,...50と各storeMemberOfUnit結果へform_sankai_l3/l4のaddSkill直後eraseSkillを原文で列挙。右翼general全死亡・左翼/中央生存なら中央groupへr3/r4。中心の全17 slotが実Unitとして存在することは未証明。
[PROOF-4] 両翼general全死亡・中央生存の枝では敵armyから散開4種を除去。一方getTime()>=30 && f_l==1 && f_r==1 && f_c==1の「全前衛壊滅」枝は、zenneibocchiに関係なく先にa_wait1000_1/_2/_3/_zinzaiを全てremoveSkillする。その後の四散開除去・form_shuugou>0なら0へ変更・生存翼への再付与は追加のzenneibocchi==1条件の内側。
[VA/XREF] 本IDの新しいEXE VA／addSkill・eraseSkill・removeSkillのnative副作用確定は無し。既存T024§11 full-form activation、§17 frontline flag・§22 event時計、§23/§14 skill差替えはread-only依存であり新READY再計上しない。
[DELTA] 既存T024には編成壊滅・再集合・81 skill swapはあるが、この時間30以後の全軍removeSkillと中央group×memberへ隣接addSkill/eraseSkillを条件別に分割した証拠は未登録。本IDの増分は原文の条件順・対象範囲・4待機技除去の内外関係だけ。
[VERIFY] Scriptのif/rif実評価・native技能APIの実作用・隣接addSkill(...)eraseSkill(...)の最終保持状態・isDead(空配列)・getTimeと実戦開始点・死活とflagの整合・重複発動・実際の戦闘到達は未確定。作者コメントや直感から実ゲーム状態・確定バグを推測しない。
[REIMPLEMENT] T024 strict script state-machineで全軍removeとUnit/member add→eraseの順序と二重gateを保持。zenneibocchi==0でも全前衛3flag==1なら騎兵待機解除のsource枝が存在し、単純な「zenneibocchi時だけ解除」へ潰さない。対象Unitの技能一覧が実際にどう変わるかはSessionGapとして扱う。
[GOLDEN] 原作合法full-form戦闘を得てgetTime29/30、左右/中央死亡分布、zenneibocchi0/1、f三旗、対象leader/memberあり/なし、同seedのスキル一覧・騎兵の停止/移動・次行動/MP/RNGを旧新同条件で観測。現時点DESIGNED/NOT RUN、oldPASS0/newstrict0、内部原文分岐だけをMATCHにしない。
[NEXT] T024新規VA探索を必要条件とせず、既存T006 API保存資料(read-only)の許可済範囲と原作DAT技能宣言を独立照合、Workが実装するsemantic T024 layerへ段階trace条件を提示。EのみMASTER/T018正式統合。
[SAFETY] 既存Local軽量静的読取のみ。禁止49ED30/510C20/5710C0..571500ほか新逆解析や迂回ゼロ、原本・他owner・REA/dev_lab/Work・WRQ・MASTER/T018・Git/push・Remote・設定・スケジュール変更ゼロ。
[STATUS] READYはowner資料＋LANE_B_HANDOFFの同ID保存後readback成功時のみ有効。それ以前はNOT READY／E統合禁止。