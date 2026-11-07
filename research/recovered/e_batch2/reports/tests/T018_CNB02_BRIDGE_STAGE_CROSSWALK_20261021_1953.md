# E T018/T020 C-NB02｜Golden段階の名称衝突と入口/配置区別（2026-10-21 19:53 JST）
ID: E-AUDIT-20261021-1953-CNB02-BRIDGE-STAGE-CROSSWALK-01
状態: STATIC DOCUMENT CROSSWALK / VERIFY / DESIGNED_NOT_RUN / NOT READY。原作DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
所有: E/T018主・T020受入設計。A-D/B研究正本はread-only、B-20261021-1830-BOUNDARY-03はNOT READYのまま。
原作EXE識別SHA（Ghidra BUILD_MANIFEST記録）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回原本EXE実バイト再ハッシュなし。
参照: tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md、tests/T018_CNB02_G0_UI_ROUTE_TRIAGE_20261020_2348.md。
B参照: evidence/LANE_B_HANDOFF.md §B-20261021-BOUNDARY-01/02/03、rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_NEW_FINDINGS_20261021_1830.mdとPROTOCOL_DRAFT_20261021.json（いずれもSTATIC/NOT READY）。
## 新しい受入上の差分：同名G0/G1/G2は同じphaseを意味しない
E_G0_UI: 旧原作の合法な通常侵攻操作が成立・戦闘へ進む可視入口。battle_id/run_id、シナリオ/攻撃元/対象、旧UI画面と入力証拠。
E_G1_PRE_SAVE_INPUT: 同一run戦闘直前SAVEの実bytes/SHAと、SAVE/攻撃/開始の入力順・時刻・TZ・input capture SHA。旧原作保存以前に宣言した戦闘IDの流用禁止。
E_G2_VISIBLE_DEPLOY: 実際に開いたMAPのID/SHAと、攻撃/防衛/支援の可視3side、順序付き出撃Troop/Unit、画面/動画SHA。保存Spot.memberやscript参照を代用しない。
B側設計ではB_G0=戦闘前、B_G1=dispatcher、B_G2=配置完了。E_G1はnative dispatcherの実行観測ではなくSAVE+入力証拠。E_G2可視観測はBの内部native配置確定snapshotと同一の証明にはならない。
BのH0=入口種別識別、H1=配置確定後/初tick前のStartSnapshotも別の任意設計名。E側G0/G1/G2の自動読み替えを禁止し、別列で相関させる。
## 入口intent対roster／実装の一対一証拠
B静的資料: native 0x004321B0/0x0048F9E0/0x0049AF10はE+1EED1C/4C/50 producer候補、0x004922A0が@battlefield/@battledefense/@battleattackを公開する。これらは参加Unit全件・順序・配置確定を意味しない。
B静的資料: 0x0048A5B0は別サイズ(0x4B8/0x188/0x188)の3objectを構築。pointer 3個を攻防支援の確定名簿3配列と同一視しない。native scene経路・実runtimeの手順はVERIFY。
B静的資料: DAT simplebattle→0x4922A0、war→0x48F9E0、prewar独立候補であり、C-NB02の合法通常UIがどの枝を通るかは未観測。B成果のE正式READY計上0。
T020比較票はintent_source(script 3key/VA/callsite)、old_visible_deploy(ordered roster/map)、new_runtime_deploy、native_H1(if_observed)、evidence_tierを別nullable列とする。Bのnative raw pointerは別EXE向け安定IDではない。
受入負例: (a) E_G1 SAVE欠落、(b) 異run G0とG2混在、(c) script3keyからG2 roster捏造、(d) B_G1 dispatcher推測だけでE_G1 PASS、(e) B H1未観測なのにnative snapshot確定。すべてGolden拒否/VERIFY、strict MATCH禁止。
G0/G1/G2旧原作一次観測NOT RUN、原作Gold PASS0、strict MATCH0、T020 GameClear13/loader8/作者変更6条件NOT RUN。旧T018表境界/他owner/禁VA・旧安全拒否の元操作を再試行せず。
次: 合法sci1/po2/sp2→sp16旧UIで同一runの実SAVE+入力+MAP/出撃順を集め、証拠時点を分けてB H0/H1と一対一照合。原本/他owner/rea_lab/dev_lab/Git/Work/自動化設定不変更。