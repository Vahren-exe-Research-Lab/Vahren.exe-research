# Stage11：原作実戦の構造データ4件を独立再検証
研究ID：BRIDGE-20261022-RESEARCH-11。対象セッション BATTLE_USER_20261021T164622798833Z_b8419f5d。
原作SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。実行時baseは0x00270000、記録時PID32468。
今回の作業は保存済みRAW/FAILUREと原作PEコピーのオフライン解析のみ。元ゲームへの接続・起動・メモリ書込・入力操作・セーブ更新はしない。
SUMMARYの成功4件／失敗1件は原本のまま保持。保存成功4件すべてを既存decoder v5で再解析し、READY/RAW/FAILURE全6ファイルのSHAと記録されたコード4本のSHAが一致。

## F11-01：実戦構造の保存成功を再確認
| 試行 | 3SideのUnit参照数 | 3SideのTroop数 | Task更新counter：採取前→後 | active Task全スロット／空き |
|---|---|---|---|---|
| RAW01 | 192 / 192 / 0 | 24 / 24 / 0 | 73→94 | 1107 / 158 |
| RAW02 | 377 / 192 / 0 | 24 / 24 / 0 | 100→134 | 1281 / 12 |
| RAW04 | 377 / 192 / 0 | 24 / 24 / 0 | 176→253 | 1966 / 162 |
| RAW05 | 377 / 200 / 0 | 24 / 24 / 0 | 272→373 | 1694 / 152 |
すべてAttackMap3項目（Def参照8/16/8）、HelpMap1項目。Sideは内部配列順であって、攻撃／防衛／援軍との対応をこの数字だけで決めない。
原本Task空きスロットを許容するv7の修正が、この新しい実戦で初めて4件の自動保存まで到達した。先の失敗記録からの部分回収とは区別する。

## F11-02：1件の停止はTask数2138と採取器上限2048の不一致
FAILURE03のtracebackはGameTask.activeのcapture_task_vector。最後に取得したのはGameTask header128byteで、一覧本体は未取得。
headerのbegin=0x4B68B628、end=0x4B68D790、capacity=0x4B68D950。実count=(end-begin)/4=2138、capacity count=2250。大小関係・4byte区切りは矛盾しない。
v7のmax_tasks既定値2048を上回ったため、範囲制限で拒否した。Unit上限超えや原作破損の証拠ではない。
元の上限検査を無効化したり無制限に読み出したりはしていない。今回は4件の構造が揃ったため、録画のやり直しを要求せず保存証拠から研究を継続する。
FAILURE03のraw_readsから最初の時刻guard4読取を別扱いにし、残りの矛盾しない実バイトを回収。Unit377/192/0、Troop24/24/0を解析できた。Task本体・pending・終了guardなど未読領域は捏造しない。
回収データ：BATTLE_STAGE11_RECOVERED_PARTIAL_03_20261022.json。原本SUMMARYの成功数を5へ書き換えない。

## F11-03：UNKNOWNだったTask型を原作PEのRTTIと照合
4件に保存された非空TaskのvtableをASLR補正し、原作PEのCompleteObjectLocatorと型名に対応づけた。出現したvtableは全体で14種、今回の非空スロットはすべて静的RTTI名へ照合可能だった。
型名：Unit、UnitFlash、FlyText、SummonFlash、StaticUnit、Troop、Missile、Enemy、GameEvent、DialogWnd、Player、BattleVSync、AllLifeWnd、BattleMsg。
これは既存の原作型名を新発見とするものではなく、実戦スナップショット内のTaskと原作静的情報を対応づけた研究増分。Task数は兵士数と一致しない。
Player/EnemyのTask登録参照はRTTI上complete objectから+0x90の部分オブジェクト。Task pointerから0x90を引くと保存済みSideの基底pointerと一致する。別のPlayer/Enemyオブジェクトが増えたと誤認しない。
今回の4件ではBattleWndActionable型のTaskは観測されなかった。ただし別戦闘経路・別時点でも常に不在とは結論しない。

## F11-04：原作pauseだけでの完全停止は引き続き未証明
原作PEのvf+0x0Cを見ると、Player/Enemy・GUI等で停止時の呼出許可が異なる。既存のFALSE関数0x43B5A0、TRUE関数0x431910も原本3byteで再確認。
FlyTextの0x4DF000はオブジェクト+0x94のbyte、Missileの0x546A10は+0x1C4のbyteを返す7byte関数。これらの実フィールドは今回のTask読取には含まれず、静的な型名だけで現在の停止可否を決定しない。
全Task型を判別できたことと、全処理を安全にfreezeできることは別。G2は未完了のまま。

## F11-05：4件とも複数Task更新にまたがる読み取り
全4件でbefore/after counterが変化（21、34、77、101増加）。GPU描画フレーム数とは呼ばず、元GameTask更新counterの差として扱う。mode2/active1/AttackMap3は前後一致している。
RAW01→02でSide0に185件のUnit pointer追加、既存pointerのUnit-record/Troopリンクは変わらず。RAW04→05でSide1に8件追加。理由は召喚等の可能性があるが、現資料から発生原因を確定しない。
RAW01～04ではSideごとのUnit集合と各Troopのメンバー集合が一致。RAW05ではSide1のUnit参照200件に対しTroop側の合計参照203件で、3件が先に読んだSide一覧にない。これを強制修復しない。非原子的読取中の変化等が候補だが原因は未確定。
したがって構造検査PASSは「完全な同一瞬間の戦闘開始状態」を意味しない。最初の取得でもcounter73から始まっており、最初の戦闘tick直前ではない。

## 完了範囲・未完了・保全
開始情報の一部を原作実戦中に自動保存し、後からオフラインで再解析できる段階に到達。今回はゲーム再起動や再戦なしで4件を解析し、失敗1件の一部も回収した。
G1完全開始packetに必要なMAP、最終配置、HP/MP、スキル、同一スレッドRNG、イベントVM、同一時点保証は未取得。元戦略→外部EXE→元戦略の往復は0、Work引継ぎゲートは3/9を維持。過去の参考準備度51.75%を今回は再推定しない。
今回の追加発見を理由に無条件で採取器上限を引き上げない。Taskのraw保存と意味解釈を分け、詳細分類を取得後へ移すこと、読取時間と整合性の改善が次の設計検討点。今回の記録ツール自体は変更しない。
研究本体：analyze_stage11_native_success_20261022.py。機械可読証拠：BATTLE_STAGE11_NATIVE_CAPTURE_ANALYSIS_20261022.json。
検証結果：BATTLE_STAGE11_VALIDATION_20261022.json（生成後）。公式MASTER、他レーンA～E、Git、製品コード、原作EXE、DAT、save、今回の元RAW/FAILURE/SUMMARYは不変。新ZIPなし、Workなし。

## 回復・再開記録
RC11-PIPE-PATH RESOLVED：最初のPowerShell内Python読取で日本語絶対パスを含む標準入力のimportに失敗しModuleNotFoundError。正規フォルダへSet-Locationし、UTF-8出力とPath.cwdを用いて再解析成功。元データ書込前の読取失敗であり、未保存発見や迂回操作なし。
LIMIT11-TASK-2138 OPEN/DOCUMENTED：v7のTask上限2048に対して実header2138。今回の失敗原因は特定、先行バイト回収済み。上限・収集方式の変更は未実施。単なる数値の引上げを完全修復とは主張しない。
CONSISTENCY11 NONATOMIC/VERIFY：全4件でTask counter増加、RAW05に3member不整合。成功ファイルを原作同一フレームGoldenとみなさない。
次回独立ID BRIDGE-20261022-RESEARCH-12。今回の実戦構造を基準に、原作Taskの登録種類と同時刻条件、Unit/Defの意味情報、VM/RNG/Mapの不足を追跡する。直ちに同じ戦闘を繰り返す必要はない。
