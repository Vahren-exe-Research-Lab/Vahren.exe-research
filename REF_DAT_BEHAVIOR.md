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

### choiceUnitFromList の取消互換（2026-10-30）
- テストのみ（原作DATの読取照合、実機取消比較は未実施）：`43_内政_教育/lecture.dat:1065–1067` は取消時に `yappa_yameru=1` を立て、`@eranda_chara` を保持する。選択結果の置換は成功側1078–1080だけ。
- 互換接続では `clear(@eranda_chara)` を成功分岐内に置く。汎用APIの `@hk_ui_selected` を取消時に空にする契約とは区別する。
- `102_ランダムイベント/randomev51-60.dat:671–676,729–734` は取消判定前に結果を表情処理へ渡す。全呼出元で結果を消して安全とは扱わない。
- 「お前クビや」は共通選択経由だが、「配下一括雇用・実行」は `50_その他新システム/restructuring .dat:664` 以降の全隊長走査と実行確認であり、共通一覧の差替えだけでは対応しない。
- 出典：`dev_lab/docs/DAT_UI_INTEGRATION_ACCEPTANCE.md` の「2026-10-30 完全導入生成と取消互換」。生成物と回帰試験は `_work/dat_ui_profiles_20261030/`。教育・アイテムの実機通し成功を意味しない。

| 挙動 | 確かさ | 出典 |
|---|---|---|
| ゲームは DirectInput でマウスを読むので、ゲーム窓を無効にしても、上に重ねた窓のクリックが下のゲームの選択肢にも届く | 実機確認 | FINDINGS §91 |
| 起動時のデータ読込中は 0x87983C が 1。読込後に DLL を有効にする（自動 arm）。2026-10-31 からは、印が 0・タイトル画面・0xAC0918（コマの時刻）が 0 以外なら読込み済みとみなし、タイトル 0.5 秒で有効にする（読めないときだけ従来の 10 秒） | 実機確認 | FINDINGS §86、§90、R1101§1 |
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

### 教育・解雇・ランダムイベント（2026-11-01 Claude）

| 挙動 | 確かさ | 出典 |
|---|---|---|
| 教育の成功値は `poli_lecture_<id>_main1`（基本 50＋講師・生徒・勢力や領地などの補正）と `main2`（能力差の補正）で `lecture_success` に作る。乱数は茶会の追加分だけ。生徒を選ぶ前に main1・main2 を呼ぶと、本番と同じ値を一覧に出せる（汎用一覧の「補正合計」） | 静的確認（一覧の表示は実機確認） | R1101§5 |
| 解雇の対象は部隊員のうち `isTalent(@u)==0` のもの（poli_vassal_delete）。`storeMemberOfUnit(@隊長,@list)`・`count(@list)`・`subv(@a,@b)`・`dialog()` はこの用途どおり動く | 実機確認 | R1101§5 |
| `delete_chara_choice` は `@chara_list` を消さずに積み増す。繰り返し呼ぶなら先に `clear(@chara_list)` | 実機確認 | R1101§5 |
| 専門学校送り（randomev11-20.dat）の `student_chara_choice` は取消で `yappa_yameru2=1`。原作はこれを見ずに先へ進み、送り出す人が空のまま進んでいた（v1.0 で前の 3 択へ戻すよう修正） | 実機確認 | R1101§5 |

R1101 = dev_lab/docs/DAT_UI_V4_RESEARCH_20261101.md

## E/T019 archive versus installed DAT set provenance (historical source review, 2026-11-02)

- **CURATED_SOURCE_PROVENANCE, not native loader behavior**: existing E ID E-AUDIT-20261024-22H-ARCHIVE-DAT-SOURCE-DRIFT-01, original tests/T020_ARCHIVE_DAT_EXTRA_SCENARIO_PROVENANCE_20261024_22H.md, independently checked source-report SHA256 2AAB084BA4CFBB9AFF9C4471F8A9F5ADE827005272D19AB34B2608CD72ADFD48. Detailed [sanitized E finding](research/intake/E/E-SOURCE-DETAIL-DAT-DRIFT-20261024-22H.md), owner [E source index](research/intake/E/INDEX.md), pinned PR #17 owner head 31ec45291badc2b5678cbdad056362bd2e4f0413.
- Historical original-report evidence described 590 DAT members in a local *candidate* original archive, all 590 matching installed DAT file hashes. The pre-modification installed manifest had **591** DAT files including a research-only extra scenario absent from that archive (2,100 bytes; original owner reported SHA256 64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228). Equality of 590 shared hashes does not establish equal directory *membership*. A 591/591 restore against the old *installed* manifest also fails to prove archive-only provenance.
- Local candidate archive publisher authenticity, runtime DAT loader behavior, loaded-source epoch and impact of the extra scenario remain VERIFY; **the original archive/DAT bytes were not rehashed in this curator run**. No original runtime bug or newly confirmed Wiki/DAT/EXE contradiction is claimed. Strict prebattle provenance needs path membership plus per-file byte SHA and the actual loaded-file epoch before original Golden comparison. Never reinterpret this installed-only research scenario as native release behavior.

## Skill ScriptData super ancestry and parser handoff (2026-11-03)

Six existing B/T011–T012 source research IDs have bounded curator `CURATED_STATIC` crosswalks. Independent authorized-PC original report SHA256 **6/6**, original ver0.67 PE identity SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, targeted PE x86 and permitted V9 E8 CALL sites checked. These are local parser/field and token facts, **not** all-function ABI, effective Skill inheritance, gameplay, Golden, or G4 settlement. Neither source notes nor raw DAT/game files are recopied into develop.

- [`B-20261024-21H-T012-SUPER-EMPTY-GATE-STRRATIO-PARENT-01`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/2daa76fc4178116fb8edae7107554bbfc086a37e/research/intake/B/B-20261024-21H-T012-SUPER-EMPTY-GATE-STRRATIO-PARENT-01.md); original report SHA256 `745F097894BCBECECBB45AF98E6F2F9C5DC810825123303067915515A66DAC6E`: Presence `0x46453F` and getter `0x464B2C` separately E8-call `0x4C1200` after local name/pointer checks (V9 two edges). The original presence bool and integer value are distinct; the historical 50-candidate cap and runtime ancestry remain VERIFY.
- [`B-20261024-22H-T011-T012-SUPER-PARSER-PRODUCER-01`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/2daa76fc4178116fb8edae7107554bbfc086a37e/research/intake/B/B-20261024-22H-T011-T012-SUPER-PARSER-PRODUCER-01.md); original report SHA256 `8CF0B616CDF9686AFF9E7CE0026C4CAAD6DE5E30DE707196D1E2AA731208158D`: Native parser `0x50B8E6 E8->0x5049E0`, literal `super` at `0x62C918`, allocation at `0x505064`, and source/output registration edges `0x505099->0x502DD0`, `0x5050E2->0x4528E0`, `0x5050EE->0x463280`. Instance identity and duplicate-key behavior VERIFY.
- [`B-20261024-2318-T011-T012-SUPER-COLON-CTOR-01`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/2daa76fc4178116fb8edae7107554bbfc086a37e/research/intake/B/B-20261024-2318-T011-T012-SUPER-COLON-CTOR-01.md); original report SHA256 `A4EE9FFFDEC5B7C95CC12644514708E318320938B15F54955046A04EAD7BDA8E`: Native initializer `0x6021D0` references colon bytes `3A 00` at `0x62C450`; parser `0x504FE4` uses object `0x65DC08`. This corrects 22H UNKNOWN comparison-token **conditionally on initializer execution**. Full startup ordering VERIFY.
- [`B-20261025-00H-T011-T012-SUPER-PARENT-STRING-MOVE-01`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/2daa76fc4178116fb8edae7107554bbfc086a37e/research/intake/B/B-20261025-00H-T011-T012-SUPER-PARENT-STRING-MOVE-01.md); original report SHA256 `EA4A2D934D1AA422103B3DCAE2E34E8F04D1ECCFE7E34498AA0427FE225E4A79`: Original `0x505099 E8->0x502DD0` reads a source string; `0x503420 MOV EAX,EBX` / `0x503440 RET` expose a normal-path returned pointer despite earlier void pseudocode. `0x5050AB E8->0x405300` transfers a string to a ScriptData-like destination; exact ABI/alias and following `0x5050FF` token identity VERIFY.
- [`B-20261025-0110-T011-SUPER-LBRACE-PARSER-GATE-01`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/2daa76fc4178116fb8edae7107554bbfc086a37e/research/intake/B/B-20261025-0110-T011-SUPER-LBRACE-PARSER-GATE-01.md); original report SHA256 `F3F37BAC36B005D8AADBF880F07FF5D3BF6460449F0D679960E2374E6C7F15A3`: Initializer `0x6020D0` references raw brace `7B 00` at `0x62C430`. Parser `0x5050FF E8->0x502DD0`, `0x505113 E8->0x416920`, and `0x505137/139` tests/branches toward `0x50517D`. This is a bounded brace-error candidate, not confirmed all-input grammar.
- [`B-20261025-0210-T011-SUPER-BRACE-RETURN-ABI-01`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/2daa76fc4178116fb8edae7107554bbfc086a37e/research/intake/B/B-20261025-0210-T011-SUPER-BRACE-RETURN-ABI-01.md); original report SHA256 `F427DA40BC490C0DDA1076C31CA8CCAD959E20AA9AD3728A7F11218C141A2100`: Corrects 01H: native error-path `0x5051E0 MOV EAX,EDI` then common `0x505200 RET`; upper parser `0x50BA65 MOV EBP,EAX / CMP EBP,EBX` and `0x50BA69 JNE 0x50BB40` show conditional nonzero return. Exact error type, branch polarity, exception and real DAT reachability VERIFY.

**Independent PE windows (scope-limited):** `[0x46451C,0x46456C)` SHA256 `31C558ADDB5D0B73DC0950EE8BC553F5B41EA07B72656D7C6721C9F53EB476AD`; `[0x464B09,0x464B59)` `5C520FE838287AB76D5D25380BF3EA471EC1C2DD496A06ACEEA6DC0ADE5176C2`; `[0x504FE4,0x505114)` `677B8A36F5C94DAF1FC698829B9052F3BEAC0E01EE2C310C5DE0CA5DF3624F12`; `[0x5050FF,0x50521F)` `A1719DF39D82F26F111C9EB320D867AFFB81A4BA9A4EA8CB2D6246999DB99A3F`. The last two studies refine prior token and return interpretation, **not** six independent new original-game functions. A source DAT declaration `skill sw_karate_jsb:sw_karate_js` is not proof that this exact native parent lookup/return path ran for that skill. All unobserved initialized-object identity, parent loop bounds, error cases, inherited compiled fields, HP/EXP and G4 output remain `VERIFY`. Original-game Golden PASS 0, strict MATCH 0, new READY 0.

**Search/navigation:** `kb.py addr 0x46453F` and `addr 0x5050EE` (code-site anchors in `symbols.tsv`), this REF, pinned owner sources and source reports; existing V9 is static native call metadata. Next legal B owner cursor: 2026-10-25 03H token continuation and 04H getter return ABI, checked by ID/SHA/errata, not by duplicate file names.

## T012: generic versus senyo Skill declarations (2026-11-03; source-only)

**CURATED_STATIC_SOURCE_DAT**, limited to the *normalized DAT declaration text*, for existing B ID `B-20261014-1611-01`. This is neither a new research ID nor demonstrated compiled/runtime behavior. Source: [pinned owner PR #18 note](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/3f408e56b9baf31bdb9a68a146a7a2337b76b8c4/research/intake/B/B-20261014-1611-01.md), original report `data/T012_TOONO_GENERIC_SENYO_CHILD_STATUS_20261014.md` SHA256 `A4C46E028F9AE5CA6F227911E9259A9FB9B00E14F47F78487798E4FBC3E16382` (independently rehashed on authorized PC). Prior identity-gate isolated PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` is not used to establish these DAT facts.

- Generic normalized Skill table `30_.../C_*.dat` SHA256 `908FF46FFCF187208ADF1C00051C67738781F099F4C33859E0EDAA52A229E967`, lines **1219, 1226-29, 1231, 1244, 1253-59**: `skill toono_death:sk_ms`, `special=off`, `mp=300`, `sortkey=-400`, `fkey=toono_death*1`, `range_min=50`, `range=200`, `next_last=on`, `next3` names beginning `toono_death_joi,toono_death_so`, `pair_next=toono_death_pr0`, `wait_time=30`. Its `joi` chain references `toono_death_nt1` (line 1385); the separately declared `nt1` (1388-99) has `exp_per=off`, `str=magic*25`, `add_per=15`, `add2=death,fear` and `bom=on`.
- Senyo normalized boss Skill table `32_.../B_2_*.dat` SHA256 `F76D37E94C3D0B11DA4632CB28B5879CB798713E464DCFF710F3E03E1F1E994F`, lines **63, 70-73, 75, 88, 97-103**: `skill toono_death_senyo:sk_ms` shares raw `special=off`, `mp=300`, `range_min=50`, `range=200`, `next_last=on`, `wait_time=30`, but declares `sortkey=0`, `fkey=toono_death*3`, a *distinct* `next3` child-name sequence and `pair_next=toono_death_senyo_pr0`. Its `joi` chain references `toono_death_senyo_nt1` (225); declared `nt1` (228-39) has `exp_per=off`, `str=magic*30`, `add_per=80`, `add2=death,fear`, `bom=on`.
- **Errata and dedup:** root `next3` names ending `nt01` are distinct strings from `joi`'s nested `nt1`; no claim that the latter is a direct root child. Prior `B-20261014-1517-02` is Unit/Class binding, `B-20261013-1322-01` is native `add_per` parsing, `B-20261013-1336-01` distinguishes two conditional RNG paths: those are links, not additional newly curated IDs. These *different declaration values* cannot be promoted to effective child inheritance, 15%/80% status probability, HP/MP damage, EXP transfer, runtime Skill selection, loaded DAT precedence, or proven source ZIP equality. All remain **VERIFY**.
- **Search / evidence boundary:** `kb.py research toono_death --task T012`, `kb.py files --task T012`, or find this REF by `B-20261014-1611-01` and the pinned private owner source. The two small normalized DAT snapshots and report were read only; none of their raw bytes, any game asset, or generated DB was committed. Original-game Golden PASS=0, strict MATCH=0, new READY=0, external G4 result commit unproven. No new `symbols.tsv`/`structs.tsv` entry: these are DAT-only source names, not proven native function/struct symbols.


## T011/T012: distinct b_mp parent, faroff child and SKRN source fields (2026-11-03)

**CURATED_STATIC_SOURCE_DAT** for existing owner ID `B-20261017-1715-01` (source-text scope only). [Pinned B owner PR #18 source](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/3f408e56b9baf31bdb9a68a146a7a2337b76b8c4/research/intake/B/B-20261017-1715-01.md); original authorized-PC report `data/T011_T012_BMP_FAROFF_SKRN_ACQUISITION_SOURCE_20261017.md` independently SHA256-matched `56E507D26BD6E32168EBE1457D448CDC3241792B7D59B806FC311FF5C468B5D6`. No original-game runtime test or new native decode.

- Normalized Skill source `30_.../F13_heal_support.dat` SHA256 `88F4139FBC1544681DF41899FF28F15CFE455E76F29174FD53489ABF6829D8C6`: at L176 `skill b_mp`, and within L186-202 its **raw parent** `attr=mp`, `func=heal`, `range=300`, `str=fix*20`, `mp=-1`, `gun_delay=b_mp*1`, `fkey=b_mp*1`. At L205 `skill b_mp_faroff:b_mp` is a **different child identifier**; L210-11 explicitly override `far=off` and `fkey=b_mp*2`, with **no child-local gun_delay assignment** in L205-213. This cannot prove that inherited effective gun_delay equals the parent's value.
- Normalized Unit source `10_.../33_INU.dat` SHA256 `FBA9C9E867F46439ED28E5A407497F896284301FAC7A8F4427BD2C11E8FC441E`: `unit skrn:base1` at L87, `class=c_skrn` L97, separate `skill` reference to `b_mp_faroff` L118, `leader_skill=b_mp_faroff*1` among others L121 and `delskill=b_mp` among others L122. A parent-removal declaration is not proof the child Skill is removed; the two source names must not be conflated.
- **Links / correction scope:** historical `B-20261017-1517-01` addresses different raw `gun_delay` and direct holder claims; `B-20261017-1413-01` is a distinct holder study. Those IDs are not newly curated here. Compiled Skill inheritance, effective far/fkey/timer, parser and loader order, SKRN legality and gameplay effects remain **VERIFY**; no assumption that normalized DAT equals original distribution ZIP. Native offsets mentioned by owner are *unverified prior leads* and not promoted to a new symbol or ABI.
- **Search:** `kb.py files T011_T012_BMP_FAROFF_SKRN_ACQUISITION_SOURCE_20261017` or search this REF by `B-20261017-1715-01`, `b_mp_faroff`, `delskill`; owner evidence link is pinned above. No DAT assets or complete report copied. Original-game Golden PASS=0; strict MATCH=0; newly formal READY=0; G4 result commit not proved.
