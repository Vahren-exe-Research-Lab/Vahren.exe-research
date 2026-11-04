# B-20261020-1015-02｜T024/T028 ボス死亡limit加算と集合/逃走防止の相補gate（限定原作source）
[ORIGIN] 2026-10-20 10時台 JST。normalized迫真ver0.67 COREのAi戦闘制御_軍楽隊なし版.dat全3707行と50_その他新システム/siki_ボス側近.dat全398行をBがLocal read-onlyで対照。今回EXE新VA/xrefなし。
[T028 FACT] siki_ボス側近.datのboss_tisa_demoralizationとboss_web_demoralizationはrank=0/1..4のskillTroop分岐の**後**、そのif/else連鎖とは別にif(inBattle(chuboss_alc)){addLimit(514)}を記載。dialog gateも別。rank0/非表示でもこの文面上は時間延長の条件を除外しない。
[T024 FACT] Ai戦闘制御_軍楽隊なし版.dat L2201前後のfull form_inbattle集合rifは getLimit()>=500 と isInterval(345/285),getTime()>=/<1333を組み合わせる。L2427前後の集合移動も getLimit()>=500 と isDead(reference leaders)==0でguardされる。
[T024 CONTRAST] 同scriptの簡易L2137前後・full L3523前後の逃走防止callerは getLimit()<500 && cpu_red==1 のときroutine(form_gannnigeboushi)。このcall済みskill付与の解除/永続は未証明。
[DERIVED IF] 仮にaddLimit(514)がgetLimit()値へ514を加え、評価間に時間減少が無ければ、非負残りR=0..499はR+514>=500となり、full戦闘では逃走防止callerの時刻gateがfalseへ、集合rifおよび集合移動の時刻gateがtrueへ切替わり得る。full登録・実interval成立・leader生存・CPU側など追加gateは維持。
[SYNTHETIC] R=0/1/498/499/500/-14/-15/-16の算術比較8/8を確認。負Rは合法性不明の境界モデルで実runを意味しない。R>=500では両時刻gateの変化無し。
[DEDUP] 既T028 §5/B-20261016-1210-01のboss死亡addLimit、既T024 §5/§7/§22の500条件、B-20261020-0208-01の赤CPU優先、未同期B-OFFLINE-20261020-0316-01の『anti-kite一時不成立』は再計上0。今回の限定増分は**同じlimit延長がfull側のperiodic regroupを再許可し得る二gate接続**とrank非依存配置の独立照合。
[VERIFY] addLimit/getLimit同一残秒のnative実作用、event発火/繰り返し、battleEvent登録と実評価順、500閾値cross時の既付与dashの状態、getTime/isIntervalと残time更新、boss死がfull/kanni戦と合法に同時到達できるかを未確認。原作バグ/可視挙動確定ではない。
[REIMPLEMENT] boss death rank/dialog→skillTroop試行→limit変更候補→次AI評価（full集合rif/移動とfull・kanni逃走防止）を別stage receiptにし、全gateと可視移動/RNG/MP/HPを分ける。
[GOLDEN] 旧合法chuboss_alcでboss_tisa/web rank0/4・dialog0/2、cpu_red0/1、full/kanni、limit499/500付近の死亡前後のlimit UI/隊列・dash・集合・次tickを原作旧EXE/DAT/SAVE/map/input/capture SHA付きで採取できた場合のみ旧新比較。INELIGIBLEなら不能明記、DESIGNED_NOT_RUN、Gameplay PASS0/strict MATCH0。
[NEXT] T010既保存timer nativeとイベントschedulerの許可済read-only照合、T024 full/kanniが当該bossイベントと同一合法戦闘で成立するかの原作source条件を先に確認。原本実行しない。
[STATUS] 詳細＋T024索引＋T028索引＋B HANDOFFの4点独立readback/重複検査前NOT READY、E正式統合0。
