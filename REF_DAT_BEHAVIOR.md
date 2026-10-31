# DAT の挙動事典（手書き。2026-10-29 Claude）

DAT（イベントスクリプト）について、実際に確かめた挙動と、機械語から分かった仕様をまとめたもの。
新しく分かったことは、この表の該当行を書き直すか、行を足す（作業日誌だけに書かない）。

確かさ: **実機確認**（ゲームで確かめた）／**静的確認**（機械語で確かめた）／**テストのみ**／**推定**

## ファイルの形

| 挙動 | 確かさ | 出典 |
|---|---|---|
| 文字コードは CP932、改行は CRLF。LF だけの DAT は、数値の行で構文エラーになった | 実機確認 | Codex handoff 2026-10-27（v2 の DAT） |
| 未知の命令名・未知のイベント名・未登録の関数の扱いは機械語で確定済み | 静的確認 | FINDINGS §16 |

## 変数とリスト

| 挙動 | 確かさ | 出典 |
|---|---|---|
| `pushv(@list, n)` で、リストの要素数が n に入る | 実機確認 | FINDINGS §91 |
| `index()` でリストの範囲外を指すと、エラーにならず**最後の要素**が入る | 実機確認 | FINDINGS §91 |
| 数値は `set` で作り、`setv` / `addv` には数値変数の**名前**を渡す。リスト内の文字列は数値として解釈されない | 静的確認 | DAT_GENERIC_UI_SPIKE_PLAN 2026-10-26 |
| 汎用兵の ID（`a030+0` など）もユニット定義表のキーで、能力値と名前が読める | 実機確認 | FINDINGS §91 |
| 能力値名は `level, hp, mp, attack, defense, magic, magdef, dext, speed, hprec, mprec, move`（`setStatus` / `pushStatus` と同じ） | 実機確認 | DAT_UI_V4_SPEC |
| リスト変数の命令（VARIABLE op36〜41） | 静的確認 | FINDINGS §10.2 |

## 選択肢（choice）

| 挙動 | 確かさ | 出典 |
|---|---|---|
| `choice` の選択肢の数は DAT の読み込み時に決まる。実行中にリストから選択肢を増やすことはできない | 静的確認 | FINDINGS §85 |
| 選択肢のラベルでは `&変数&` が展開される | 静的確認 | FINDINGS §85 |
| ラベルの置き場所は 50 個分（index 49 まで、0x8BC11C で終わる）。範囲の検査はない | 静的確認 | FINDINGS §85、Work の work_dat_ui_choice.h |
| `choiceTitle` は、次に置き換えるまで残る | 実機確認 | FINDINGS §90 |
| 選択肢を右クリックしたときの戻り値 | 未確認 | DAT_UI_V4_SPEC §8 |

## 実行の流れ

| 挙動 | 確かさ | 出典 |
|---|---|---|
| `if` は、else が空でも then/else のどちらかを必ず積む | 静的確認 | FINDINGS §1.1 |
| `while` は条件が真の間、本体を積み直して条件を再判定する | 静的確認 | FINDINGS §1.1 |
| `wait`（op9）の動き | 静的確認 | FINDINGS §1.4 |
| ゲーム側からイベントを起動するフック（world / fight / politics） | 静的確認 | FINDINGS §18 |

## DLL との組み合わせで分かったこと

| 挙動 | 確かさ | 出典 |
|---|---|---|
| ゲームは DirectInput でマウスを読むので、ゲーム窓を無効にしても、上に重ねた窓のクリックが下のゲームの選択肢にも届く | 実機確認 | FINDINGS §91 |
| 起動時のデータ読込中は 0x87983C が 1。読込後に DLL を有効にする（自動 arm）。読込中を一度も見なかったときは、タイトル画面が 10 秒続いたら有効にする | 実機確認 | FINDINGS §86、§90 |
| イベント中は、ゲーム本来のステータスパネルの説明表示（マウスを重ねるとスキル説明）が出ない。教育などのイベント中はパネル自体を見られない | 実機確認（ユーザー） | FINDINGS §93.4 |

## Worldイベント：原作ver0.67 SCRIPT限定の横断照合（C/T025,T016）
以下のsourceルートはA-Eレーン正式READYと旧原作Gameplay Goldenを代行するものではない。原作正規化DATの**記述された命令順・対象・条件**のみSTATIC-SCRIPT。VMのevent()/routine() Yield、実queue/FIFO/親復帰、native API副作用、実戦闘・SAVE結果はVERIFY/NOT READY。原作Gameplay Golden PASS=0、strict MATCH=0。

### sci1/sc_freeのMZに関する二組のイベント要求（C-20261016-0023-01）
- main event_world.dat:491-526とfree_ev_world.dat:318-356に同じ構造の2群があり、正側はevent(mz_is_kusakunai6,1,2,3,5,4)の6要求、負側はevent(mz_is_kusasou1..6)の6要求を原文順に記述。後者の条件にはisRoamer(mz)==1のORが含まれる。括弧結合の厳密な実VM演算と両群12命令の同時到達はVERIFY。
- event_00_共通イベント.dat:416-486の12子eventの元scriptは、各zngm/hsgdn/hitokage/togepi/achamo/hassamuについて正側addUnit(child,mz)、負側addUnit(child,sp0)を各1命令ずつ記述。これらを単一の移動や最終所属へ合体しない。各childの実完了・Power/Spot状態は未観測。
- Verified normalized-script SHA256: event_world.dat=523B389E2E985D3924D83246E076343F8AA1EA2C610044B1739E6792EB7E7D9A、free_ev_world.dat=65FC28C64F95CAB0ECED9522D2AC0C98D65BC1BE0B4968A56D78BA190492DD08、event_00_共通イベント.dat=44ECF64B2979D3FBB09EBD62D70602CB9B064348F9CC9526F9C3CECEBBC64110。
- Owner C/T025,T016: C-20261016-0023-01、evidence/T025_MZ_ROAMER_DUAL_RELOCATION_EVENT_ROUTES_20261016.md。既T025§54/62や既A/T006のevent opcode解釈を別の新発見に再計上しない。

### sc_free Worldの初回eventと古いslot参照の候補（C-20261016-0122-01）
- free_ev_world.dat冒頭はstorePlayerUnit(@plau)→storePowerOfUnit(@plau,@plap)→storeNowPower(@now_power)。COM guard内のline108は別slot @bbbへstoreNowPowerし、@now_powerには再代入しない。
- 初回freeのline146-148はevent(firstsetupfree1)→event(chara_create)→event(choice_otherunit)を要求。後段line629-647のisComTurn/pushDiplo/setTruce/setDiploは入口由来の@now_powerと@plapを参照する。@bbbの再取得と初期slotのreadを混同しない。
- 既存sci1 worldの@now_power入口、COM別@bbb再取得やrscとの後段外交有無の差はソース比較に限る。子eventによるscope更新、@plapの値が実際に古くなるか、外交を別勢力に誤適用するかはVERIFY。原作バグ認定0。
- Owner C/T025,T016: C-20261016-0122-01、evidence/T025_WORLD_ENTRY_SNAPSHOT_COM_DIPLO_QUEUE_JOIN_20261016.md。既存World初回setup/COM guard/外交単体と重複新発見にしない。

### randomsetの周期gateと継続処理の分離（C-20261015-1722-01）
- randomset.datの周期本体は適格phase・randomevon==1・turn<=60等で制限される。しかし同ファイルline152-159にあるrandomev_sabo>=1のcounter加算、>=4時の広域eraseSkill(ps_sabo/ps_koyo)とcounter resetは、周期ifを閉じた後の**別の条件枝**。
- line164-182のpes_happy検査も周期if外で、weed1/2/3/なしでHP割合引数97/98/99/96、HPrec加算-30/-20/-10/-60と下限-500のsetStatusを記述。これを4回周期eventだけに内包させない。
- main/free/rsc Worldは重複phase guardより前にroutine(castleset)→routine(randomset)を直接記述。routineがその場で実行された場合でも、処理回数を単純な暦turn数と断定せず、World入場とVM続行を区別する。
- Owner C/T025,T016: C-20261015-1722-01、evidence/T025_RANDOMSET_TAIL_SABO_HAPPY_UNGUARDED_WORLD_20261015.md。既知C1625の周期4、T032の付与命令は再計上しない。実効果と合法重複入場はVERIFY。

### 全Power対象のsabo解除とplayer Unit対象のhappy（C-20261015-1823-01）
- randomset後段のsabo期限満了にはstoreAllPower(@allp)→storeUnitOfPower(@allp,@allu)→eraseSkill(@allu,ps_sabo/ps_koyo)。一方pes_happy側はstoreSkillOfUnit(@plau,@aaa)と@plauを対象にHP/HPrec更新を書いており、二枝の対象集合はソース上明らかに異なる。
- main/free/rsc Worldは各@plauをrandomset前に取得。一方Dreamのev_dream.dat全1062行にroutine(randomset)・routine(castleset)の直接literal呼出は0。別経路・間接起動の不在は保証できないためDreamの全効果不存在を断定しない。
- Verified normalized-script SHA256: randomset.dat=12276C86F1E09733BA97122CCA524BD30C72B06131A7EE7FC81385D9B55017D1、ev_dream.dat=A574E15A843D9BC7432D8667A2F26AEFD7956613B71E6D39AAE3670859BDBEDD。
- Owner C/T025,T016: C-20261015-1823-01、evidence/T025_RANDOMSET_TARGET_SCOPE_DREAM_CONTRAST_20261015.md。sabo>=4、weed効果など直前1722既知の数値は二重READY計上しない。

### castleturnとsiegeturnは別timer（C-20261015-2124-01）
- event_castleset.dat:10-36はPlayerTurnまたは非master NewTurn・非tutorialの適格phaseに加えcastleset==1かつmode>=2でcastleturn加算、5回でreset。別story siege_politic.dat:275-302も類似phaseだがmode!=0でsiegeturnを加算し、mode1=10回、mode2=8回、mode3=5回でreset。二つのcounter・効果・初回latchを統合しない。
- event_castlesetの初回NewTurn/turn1では周期条件が初期flagの書込より先にあり、その同一呼出はcastleturn加算を飛ばし得る。別story siege_startの初期化/周期評価順は違い、合法に両方起動した場合の初回offset差候補がある。mode3の数値上同じ5回は、旧VMで両方が同時発火する証明にはならない。
- Verified normalized-script SHA256: event_castleset.dat=9796862137A83BF006FE909D2E60AC45384B41995835A820F6FE3ACCB90EC450、siege_politic.dat=362CB8553ACDB36F10E5939EDE977A3739AE24FDBF23501E209ED87A4FD255E5。
- Owner C/T029,T025,T016: C-20261015-2124-01、evidence/T029_CASTLE_VS_SIEGE_COUNTER_PHASE_CROSSWALK_20261015.md。個別thresholdは先行T029で既知、今回は同phaseでの初回flag順の交差照合のみ。story/world/VMの実適格呼出回数、原作Gameplay Golden PASS、strict MATCHは未検証（0）。
