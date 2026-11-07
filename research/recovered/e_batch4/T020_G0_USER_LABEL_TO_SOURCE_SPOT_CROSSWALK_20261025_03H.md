# E-AUDIT-20261025-03H-T018-T019-T020-NATIVE-G0-SPOT-LABEL-DIVERGENCE-01
Owner: E/T018,T019,T020 | 2026-10-25 03H JST | STATIC SOURCE VERIFIED / SAVED ORIGINAL OBSERVATION REVIEW / NATIVE ID VERIFY / NOT READY / old-new Gameplay NOT RUN.
## 独立に確認した証拠（Desktop Commander Local Compact READ ONLY）
- 正規化原作 `data/normalized/hakushin067_core/a_default/script/spot.dat` を直接読取。実バイトSHA256=5B36F2A9D1788EB0B45FE058CBEA8493FC521CE5ABEE9AE88D290087C17DAB4C（正規化ファイルのSHAで、原本ZIP全体のSHAではない）。
- 同DATの宣言と表示名：`spot sp50:sp` → `name=岡山県南; map=s50`、`spot sp2b:sp` → `name=アゼルバイジャン; map=s2b`。
- 対照：`spot sp2:spgood` → `name=迫真空手道場; map=s2`、`spot sp16:sp` → `name=ソーダ洋西部; map=s16`。旧 `scenario1.dat` のsci1宣言内には4Spot IDを含む（合法攻撃可否までは保証しない）。
- `search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json` 実バイトSHA256=87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C。旧ユーザー報告 `岡山県南からアゼルバイジャンへ攻撃`、PID23272、first active 2026-10-21T14:31:37.765392Z。native攻防Spot ID検証は双方false、battle_packet_complete=false。
- `search_index/BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json` 実バイトSHA256=B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005。ユーザー申告は `岡山県南→アゼルバイジャン`、WATCH1 SHA=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7；これはG0 native mode遷移のみの根拠。
- E既存 `T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md` / `T018_CNB02_BRIDGE_STAGE_CROSSWALK_20261021_1953.md` は別のC-NB02設計対象を `sci1/po2/sp2→sp16` と明記。 `BATTLE_BRIDGE_CNB02_NATIVE_SAVE_CROSSWALK_20261021.json` も `requested_war_sample`=sp2→sp16の保存状態候補で、`old_exe_executed=false`。
## 新しいE受入判定上の差分
- 静的宣言上、ユーザー申告の表示名ペアは `sp50→sp2b` に対応し、C-NB02静的サンプルの `sp2→sp16` とは異なる。よって既WATCH1を自動的にC-NB02固有の合法G0一次証拠へ昇格するのは不適切。
- ただし旧EXE runtimeのSpot-name overlay、同名再定義、UI選択・内部native SpotポインタとIDの対応を本回は実証していない。WATCH1の実際のnative Spot IDがsp50/sp2bであるとも、sp2/sp16でないとも原作確定していない：`USER_LABEL_RESOLVED_STATIC_ONLY / NATIVE_ID_UNPROVEN`。
- WATCH1はユーザー申告付き実原作戦闘のmode2/active1観測として存続。C-NB02 G0固有QUALIFIEDではない。WATCH2(PID同じ、別時刻)へWATCH1の表示名を伝播しない。
- spot宣言内のmap=s50/s2b/s2/s16はSpot static map propertyであり、実戦闘でロードされたMAPの観測・SHAではない。G2に代用しない。
## T020負例設計（DESIGNED / NOT RUN）
- L01: WATCH1 source user labelsをC-NB02 `sp2→sp16` と同一視 → `SPOT_PAIR_PROVENANCE_MISMATCH_OR_VERIFY`。明示runtime ID receipt無しにeligibleへ昇格しない。
- L02: WATCH2にWATCH1のuser labelsを同PIDという理由だけで継承 → `CROSS_BATTLE_WINDOW_UNPROVEN`。
- L03: sci1/po2と一致した任意の旧SAVEだけでWATCH1/ C-NB02のG1直前SAVE証明 → `PREBATTLE_SAVE_UNPROVEN`。
- L04: spot.map propertyだけでE_G2実MAP/三side/ordered deployed Unit/Troop証明 → `G2_UNPROVEN`。
## 現状・統合・安全
- E G0(C-NB02合法UI＋native Spot ID)/G1同戦闘SAVE・操作/G2実MAP・三side・確定出撃/G3終戦結果/G4戦略World差分は未充足。今回新E DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0、新合成実行0。
- T019新規確定原作Wiki/DAT/EXE矛盾0。今回の差分は原作BUGではなくEの観測名↔対象fixtureの証拠帰属境界。GameClear lexical scope RESOLVED、script2優先/phase flag/TXT実load/gwrite復帰VERIFY維持。
- MASTER最終公式checkpoint196/READY596=A115/B229/C136/D116は既報値、34Task DONE9/IN_PROGRESS21/VERIFY4は02H再集計値で本回再集計なし。新規正式READY0。B-20261025-0312はNOT READY、他owner代理統合0。
- 過去E旧T018表境界・session-join/DAT note/Stage15等の安全拒否、C T026/T032、D不完全T030 TSV、禁止VA0x5710C0等は各BLOCKEDのまま再試行・別tool/path/shell/Remote/ZIP迂回なし。
- 本回PC書込は本E-owned新規T020研究ノートだけ。原本EXE/ZIP/DAT/SAVE、MASTER、既存T018/T019、A～D/REA/dev_lab/Git/Work/設定/他automations不変更。OFFLINE-UNSYNCED正式採否保留。
- NEXT: C-NB02専用旧合法UI観測（画面＋入力＋攻撃元/対象native Spot識別）をWATCH1の別ペアと区別して採取。次に同一runのSAVE実バイト/SHAとG2実MAP/三side/ordered rosterを結合し、owner/READY/hash/重複を満たすものだけ一度正式統合。
