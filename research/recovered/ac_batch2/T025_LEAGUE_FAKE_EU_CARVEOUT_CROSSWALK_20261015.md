# T025 同盟支援の301 fake-EU例外とT024橋渡し（2026-10-15）
ID: C-20261015-0128-01 | T025/T016（T024はB担当read-only）
状態: READY＝原作ver0.67のSCRIPT構文・限定301件census／VERIFY＝native列表現・実EU所属・実加算。原作Gameplay NOT READY。
原本相対: a_default/script/event_world.dat:2089-2408（leaguepowerevent）、a_default/script/7000_その他シナリオ/free_ev_world.dat:1092-1411（leaguepowereventfree）、a_default/script/Ai戦闘制御_追加部分.dat:1097-1119（unit eu0: talent=on、eu1等はeu0継承）。
保存済B所有 data/T024_HAKUSHIN_BATTLE_AI.md §15 は偽人材eu0..eu300の301体プール・speu・非人材leader代理化をSOURCE限定確定。本研究ではBの成果を再採番・編集しない。

## 今回の独立増分 / CONFIRMED SCRIPT
両同盟routineは `getMode()>0 && getTurn()%4==0 && count(@ccc)>0` 内で `storeUnitOfPower(@ccc,@aaa)`→`storeAllTalent(@eee)`→`subv(@eee,eu0)`から`subv(@eee,eu300)`まで個別列挙→`subv(@aaa,@eee)`→`addLevel(@aaa,1)` の順に記述。
Local Compactで各原文を独立に字面集計し、本編301命令・フリー301命令、双方eu0..eu300が各1回、欠番0・重複0。原作のliteral列をカウントしたもので旧EXEの実行回数ではない。
本来のtalent除外集合からfake EUの301 IDを予め除外する構造なので、nativeが通常の集合差分として動き、実際にfake EUが同盟PowerのUnit集合とTalent集合に両方含まれる条件下では、そのfake EUを後続addLevel対象集合から除外せず残す可能性がある。
旧T025§57には4turn周期・同盟別の除外・土地Gain効果が記録済。新規性はEU全301件の完全列挙と、B T024のfake talent poolを同盟Unit育成対象へ接続した条件付き意味差分のみ。

## VERIFY / 未観測
`storeUnitOfPower`と`storeAllTalent`の実返却値、subvの要素比較・重複/alias意味、euNの所属・同盟配置・育成可能性、加算時のnative clamp・EU recycle、実GamePlayは未観測。偽人材が実際に必ずLv+1となる・原作BUG確定とは主張しない。
同盟勢力のSpotへ行う`addGain`は後続の別gateで、EU抽出条件と自動連動させない。既存A保存VMのYield/Done時相はこのSCRIPT静的確認だけでは解決しない。

## 再実装と必要Golden
strictでは`storeAllTalent`後にeu0..300を明示除外する処理と、残った人材一覧を同盟Unit一覧から差し引く処理を独立stage化。人材種別判定だけで全fake EUを除外しない。
合法なsci1/sc_freeの同盟成立状態で、mode0/1・turn3/4/5・fake EUが同盟Power所属/非所属・普通人材の対照を用意できる場合のみ、同一原作SAVE/SHA・同入力の旧EXEと新EXEでEU本人Lv、一般Unit Lv、通常Talent Lv、同盟Spot Gainを比較する。成立不能なfixtureはINELIGIBLE、原作Gameplay actual Golden PASS0・strict MATCH0、DESIGNED/NOT RUN。
未解決P0: T025 boss_dead setv/clear/erasePower、WW po/poo inactive/self union、sc_free queue、T029 castle周期/50000、T026 teacher/student temp、T027 wallet/stock、T033旧ID到達。旧C-RC-20261014-1824-01/T026/T032の拒否はBLOCKED継続で再試行・迂回なし。
統合: MASTER cp149公式531（C123）、このIDはEによる正式採否・統合前。C資料＋HANDOFFにのみ保存。原本・他owner・MASTER/T018・dev_lab/REA・Git/Remote/MCP/automation不変更。