# T020 更新履歴・作者調整方針の回帰候補（Lane E、2026-10-08）
状態: read-only照合由来のNEW AUDIT / 実機golden未実施。MASTER/TASK QUEUE統合は別途必要。
資料: data/source_snapshot/hakushin067_core/readme_3＿更新内容.txt（5062行）、readme_6＿調整方針.txt（137行）。
## 優先候補：作者の記載でありnative・現行到達性の確定ではない
- [AUTHOR, T027] ver0.67（2026-08-10）: 人材プレイで稀に商品価格が負になる不具合を修正。財布・価格・乱数・インフレ/discount極値を検証。現行でも絶対に負値が出ないことは未検証。
- [AUTHOR, T025/T027] ver0.60（2024-08-10）: 資金不足の商品購入、商品価格変動、企業訪問残留を修正。T027の財布=価格×5という別境界はなおVERIFY。
- [AUTHOR, T031/T010] ver0.60: 討伐/制圧勝利後はランダムイベントが発生しなくなる仕様変更。post-battle world-entryのcadenceと通常turnを比較。
- [AUTHOR, T026/T006] ver0.61（2024-12-20）: 教師選択後キャンセルでアイテム使用に不具合が出る現象を修正。choice/cancelと一時ステータス復元を重点テスト。
- [AUTHOR, T012/T028] ver0.61: 特定の追加スキルが戦闘終了後も残る不具合を修正。battle-only skill付与→終了→次戦闘のcollectionを比較。
- [AUTHOR, T014/T010] ver0.61: CPU勢力ターン開始時に自動セーブを追加。保存タイミングと実際のsaveファイル挙動を検証。
- [AUTHOR, T014/T025] ver0.57（2024-05-05）: イベント戦闘敗北後、リトライせず次回起動時に再戦できるセーブ作成選択肢を追加。通常saveと別の再開契約を確認。
- [AUTHOR, T006/T013] readme_6 ver0.66: unctrlTroopがCPU変数でも自部隊選択を解除する旧VT本体の不具合、と作者が説明。CPU限定技への変更で回避したとのこと。現行スクリプトにunctrlTroop呼出23件を検索したが実際の選択解除はVERIFY。
- [AUTHOR FORMULA, T011/T012] readme_6 ver0.66: 経験値設定 exp=1.833×speed+110（例speed70→239、180→440）、Lv上昇増分=初期ステータス×multi×0.01。丸め、例外、全unitへの普遍性は原本/EXE照合待ち。
- [AUTHOR, T025/T032] readme_6 ver0.562: ランシナ/旗揚げの一般雇用追加でリスト上書き、当時は一部ランダムイベントで未修正。ver0.67でも存続するかは未確定。
- [AUTHOR HYPOTHESIS, T014] readme_6 ver0.562: 異常saveや白画面はメモリ圧迫の可能性と記載するのみ。engine確定仕様にしない。
## 静的根拠と未実施golden
- E-CHG-01: 0.67人材プレイ負値価格と5個分財布境界を同じケースで再現。
- E-CHG-02: 教師選択cancel→アイテム使用→magdef/変数/選択復元。
- E-CHG-03: 一時スキル→戦闘終了→load→再戦でskill collection確認。
- E-CHG-04: CPU turn autosave、討伐後random event抑止、reentry phaseを分離。
- E-CHG-05: unctrlTroopに対する自軍選択解除の実有無を条件差で比較。
- 全条件は実機PASS 0。既往のT018本文append安全拒否は再試行しない。Eの正本への統合は保留。
RUN CAPACITY: 更新履歴5062行を550行×9範囲でread-only走査、重点5範囲再読、調整方針137行全読、unctrlTroop全script検索23 match確認。原本・実機未変更。
## 2026-10-08 レーンE 第2回: 既存T018の回帰網羅率監査（保存先変更による拒否迂回ではない）
- 調査: `tests/T018_GOLDEN_CORPUS.md` 464行をread-onlyで4分割走査し、T020作者変更5系統を既存fixtureの説明本文と照合。今回の追加は**欠落・重複の監査結果だけ**であり、過去拒否されたT018本文追記を別の場所で代行しない。
- E-CHG-01 [GAP]: `MERCHANT-QTY-FIVE-EXACT-WALLET`, `MERCHANT-PRICE-TURN-SPOT`等は存在するが、ver0.67の**負値商品価格**を直接検証するfixtureは未収録。
- E-CHG-02 [GAP]: `EDU-TURN-BUDGET`には教育メニューcancelとpolip/count確認があるが、作者が修正した**教師選択cancel直後のアイテム使用**という連鎖条件の直接fixtureは未収録。
- E-CHG-03 [GAP]: `DM-LEARN-TRANSFORM`等にはskill寿命調査があるが、**追加skillが戦闘終了後に消去されるか**を作者回帰として直接対照するfixtureは未収録。
- E-CHG-04 [GAP]: `SAVE-MAIN-4GROUP`, `RE-RNG-WORLD-REENTRY`等は個別にあるが、**CPU勢力のターン開始時自動セーブ**および**討伐・制圧勝利後のランダムイベント抑止**は独立fixtureとして未収録。
- E-CHG-05 [GAP]: T018本文に`unctrlTroop`の明示試験名・条件が見当たらず、自軍選択解除の作者報告を直接検証していない。
- 判定: 5/5系統に直接専用fixtureの欠落。関連する近似fixtureはあるため「この機能全体が未調査」とは言わない。作者変更履歴はHYPOTHESIS/回帰候補でありtarget実機での再現を確認していない。
- 対応: MASTER/T018統合は安全拒否履歴を尊重して**未反映**。実機PASS増加0、DONE増加0。Eの本件成果は既存テストのread-only監査と本T020資料の欠落判定のみ。
- RUN CAPACITY: LocalでMASTER先頭/QUEUE/末尾、規約、A/C/D引継ぎ、関連owner資料のread-only照合、T018約464行分割read。実EXE実行・Remote・Git・原本/研究外書込0。次回も小単位で証拠確認し、拒否されたMASTER/T018編集を迂回しない。

### 実行基盤の現状（read-only inventory）
- `_REDEV_RESEARCH/tests/` の直下には `T018_GOLDEN_CORPUS.md` と `T028_GOLDEN_CORPUS.md` の2資料のみ。少なくともこのディレクトリにはT018 fixtureを実行するテストランナー、観測値の機械可読データ、PASS記録は存在しない。別の場所にあるT022 decoder用golden等と同一視しない。
- 再実装側に独立の小さな入力→出力テストランナーを先に用意し、静的期待と旧EXE実測値を別カラム管理する必要あり。エンジン実機測定は未実施。MASTER/T018編集のBLOCKEDは引き続き未解消。

## 2026-10-08 E再開：商品価格負値修正の原本直接照合
- [CONFIRMED-SCRIPT / actual script, NOT observed runtime] 正規化原本 `42_内政_行商人システム/ev_M_famima.dat` の `event item_price_fluctuation` は `pushRand(item_random_price)` → `add(item_price,item_random_price)` を実行する。かつての `sub(item_price,item_random_price)` はコメントアウトされている。
- [AUTHOR COMMENT] その直後に「極稀に最終結果が負の値になるのでsubは廃止」と明記。更新履歴ver0.67の人材プレイ負値価格修正と具体的なscript変更が整合する。旧減算案は現行の実行処理ではない。
- [SCRIPT ORDER] 直後にrate=1140/1080/1110/1120/1100を分岐選択し、turn>1かつspot>1時に `mul(price,rate);div(price,1000)` を繰返す。各段での整数除算と後段の商品・外交係数処理は独立に検証する。
- [VERIFY] 現行の全価格が必ず非負になる保証、native `pushRand`/数値型/overflow/係数と丸めによる変化、実商品UI、5個ちょうどの資金境界の結果は未実機。旧バグが今回のscript変更だけで全ケース解決したとは断定しない。
- [GOLDEN PLAN E-CHG-01] 原価0/1/100、RNG端0/99、turn1/2、spot1/2、各price factor・負値初期値、5×表示単価の資金境界を分離。静的期待と旧EXEのactual observedと互換実装のactualを別列で管理。実機PASS0。
- [EVIDENCE] `data/normalized/hakushin067_core/a_default/script/42_内政_行商人システム/ev_M_famima.dat` lines 414–438、`data/T027_MERCHANT_PRICE_PURCHASE.md` §1、作者更新履歴。T027は他レーン所有のためread-onlyのまま。

## 2026-10-13 新E cp101｜T020作者回帰6 fixture設計済みへの網羅率再照合（原作NOT RUN）
[OLDER CLAIM SNAPSHOT] T020の2026-10-08『5/5系統に直接専用fixtureの欠落』は当時T018=約464行の監査結果として保存し、歴史情報なので消さない。一方今回Eが最新版T018（1274行）を全read-only再走査した結果、同じT018内に作者回帰行6件が追加済みだった。昔のGAP判定を現在の状態と取り違えない。
[CURRENT DESIGN COVERAGE 6/6] `tests/T018_GOLDEN_CORPUS.md` 現物理474..479行に `E-CHG-01-PRICE-NEGATIVE`, `E-CHG-02-EDU-CANCEL-ITEM`, `E-CHG-03-BATTLE-SKILL-CLEANUP`, `E-CHG-04A-CPU-TURN-AUTOSAVE`, `E-CHG-04B-POST-VICTORY-RANDOM`, `E-CHG-05-UNCTRL-SELECTION` の6固有テーブル行がそれぞれ1回存在。作者5系統（E-CHG-04はautosaveとpostbattle eventの2実験に分離）は『設計fixtureの直接欠落』だけ解消。紐付く旧原作ゲーム挙動は依然未観測。
[QUALITY/BORDER] T018は先行T026/E-RETRY 4行と作者回帰6行を同表に独立保持。各行はsource仮説、操作/条件、old UI+合法SAVEで可視取得すべきものと実機VERIFYを分離。C-NB01/02/03通常戦闘の実参加や成功を示す資料とは別。
[STATUS MATRIX] 作者5系統=PLANNED 5/5、比較fixture行=DESIGNED 6/6、旧原作実機DYNAMIC OBSERVED=0、actual Golden PASS=0、新EXE strict MATCH=0、new regression actual PASS=0。既設IDに対する被覆監査でありGolden fixture IDを増やさない。昔のT020『T018は欠落』は2026-10-08時点にのみ成立。
[NOT FIXED / SAFETY] 作者0.67負値価格・0.61教師cancel item・追加skill lifetime・CPU autosave/討伐後random event・unctrlTroop CPU変数癖の実動作はすべてVERIFY/NOT RUN。旧T018 AI-CONFUSION/SCENARIO Markdown表行境界の安全拒否は未解決、書換・別path迂回せず既存6行を読んだだけ。A-D/REA/dev_lab/原本/Git/Remote/設定/他automation変更0。
[NEXT] 実機の合法旧save/観測手段が用意されるまではT018へPASS記入しない。DEVLAB-006へ作者回帰6fixtureを独立入力ゲート付きで引継ぐが、Work製品回帰916PASS等を旧作者互換PASSに加算しない。
