# 保存済みGhidraの追加逆コンパイル解釈：空間判定／event参照先／missile latch（2026-10-10）

**状態**: 保存済み疑似コード＋アセンブリの独立再読およびdev_labの契約試験設計。新Ghidra/REA/旧EXE実行0、原作golden actual PASS0。対象ゲームの旧EXE SHAは保存RUN_RESULT内で `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` と記録されたものを参照（今回の再hashなし）。

## SPATIAL-R1：0x4E7ED0 は2つの探索方式を同一関数内で実装

一次証拠: `runs/20261009T224617297Z/4E7ED0_procedure_pseudo_code.json` （pseudo証拠ID=`ev_5541fff9fcb4b4681426b0f8b59eb115ab466489067bef28bd4a45d6e9c9785b`、assembly証拠ID=`ev_4b52004127ec175ac9c1971618398099d6a721f800f5f5b083599764a1aab2a8`）、同 `4E7ED0_procedure_assembly.json`、`4E7ED0_procedure_info.json`、`T012` saved native owner。
- entry `0x4E7ED0`、Ghidra function body計814byte、basic blocks56、body noncontiguous 2 range。caller2（`0x546F70`,`0x57EB40`）、direct callee4 (`0x44D8F0`, `0x5D1B80`, `0x5E40B0`, `0x5E41E0`)。
- p1+0x3C非zero → 0x4E7EE5..0x4E7F8D **方向オフセット付きの一セル占有チェック**。p2+0x220,+0x224の符号付き座標は `CDQ; AND 31; ADD; SAR 5` で32分割に**0方向丸め**し、p2+0x18688方向indexから`0x62DD20/0x62DD24`の補正を加える。p1+0x40/+0x44の縦横boundsを検査し、p1+0x48のtile pointer表で一つのoccupant pointerを選択。
- 一セルbranchは候補+0x65非0、候補+0x1AE==0、候補+0x1D0 != source+0x1D0、候補+0x1D4 == source+0x1D4の全4条件で1、それ以外0。**このbranch内に距離比較は無い**。所属関連offsetは数字のまま保存し、人間向け「敵」「同陣営」を確定名として与えない。
- p1+0x3C==0 → 0x4E7F99..0x4E8202 **複数セルのradius sweep**。入口でsource p2+0xB0/+0xA8が両方0かつaction counter p2+0x1E530 <global0x65BC5Cならsource effective radiusを0、それ以外ではsource+0x228を採用。その後0x4E7FD3で常に0x20（32）を加算し、向き＋x87 trig/helperからセル探索の窓を組み立てる。source半径を「全tick一定+0x228」としない。
- 近傍セルの各occupantに対してgrid branchと同じ4つのフラグ／関係フィルタの後、0x4E8169呼出`0x44D8F0`（距離関連）＋0x4E8172の定数加算＋0x4E817Bの整数化helperを使用。candidate側はcandidate+0xB0/+0xA8両0かつcandidate+0x1E530 <global0x65BC5Cならeffective reach=0、そうでなければcandidate+0x228。0x4E81AA `CMP EAX,ESI`→0x4E81AC `JL 0x4E81F9`なので**distanceInt < effectiveReach**でのみ1。等号は不成立。
- 非grid側のtrig値／x87丸め、方向補正配列の8要素、0x44D8F0の正確な距離単位はVERIFY。保存Ghidra pseudoは+0x4E7F99のsource判定の一部を表現し損ねるため、assembly優先で契約化。
- dev_lab `spatial_presence_subset.py`：C風signed÷32・方向セル単一占有・共通4フラグ・candidate reach strict <・source reach+32の純粋論理を**6合成テストPASS**。実際のセルグリッド全走査、距離helper、方向表は未実装。存在判定をhit/damage成功へ昇格しない。


## EVENT-R2：0x4321B0 の参照先2判定、3状態のpointer再配線

一次証拠 `runs/20261009T225741694Z/4321B0_procedure_pseudo_code.json` (evidence=`ev_6443778f30890c0e5cb33fc7bbabf54b8cd665a1424f7b354c6bd439dbac2051`) と同assembly (evidence=`ev_56f9a3557ec9eaa37a3dae138562b66cdde8d20a39e915d61d3e8c37709157db`)。特にVA 0x4328E7..0x432B3A。
- 入口`in_stack_0000002c !=0 && engine+0x1EEC44 !=0`はearly special route（0x4321B0のgeneral bodyをskip）。このbranchは同関数内数値writer`0x4637A0`のsite 0x432379、通常の`0x40B200`3 callsitesも通らない。ただし別経路でのhistory更新はVERIFY。以前owner監査の結論と一致。
- 一般経路ではまずVA0x4328E7に `0x40B200` を呼び、戻りALを+0x1EED40/+41/+42の3つのbyte slotへ複写。これは後で実行する2つの参照チェック（VA0x432AA6/0x432AC0）とは**異なる引数文脈**。同じbooleanの使い回しを禁止。
- 2つの参照入力+0x1EED4C/+50がNULLならscene内+0x58へ補完（VA0x4329B6..D4）。+0x1EED54/55/56をまず0初期化。1番目参照の+0x1D非zeroなら+0x1EED54=1で次判定skip。ゼロなら`0x432AA6 CALL 0x40B200`を行いAL!=0なら同様にflag54=1。最初が不成立の時だけ2番目参照+0x1D非zeroを確認し、ゼロなら`0x432AC0 CALL 0x40B200`でflag55=1を判断。
- +0x1EED54/55の組は到達可能なのが(1,0),(0,1),(0,0)だけ。この2フラグと3つの参照slot+0x1E8630/+34/+38から**別の2つのpointer+0x1EED44/+48**が作られる。branch mappingは次の通り：
  - flag54=1 => pointer44=slot+0x1E8630, pointer48=slot+0x1E8634
  - flag54=0かつflag55=1 => pointer44=slot+0x1E8634, pointer48=slot+0x1E8630
  - flag54=0かつflag55=0 => pointer44=slot+0x1E8638, pointer48=slot+0x1E8634
- 次に0x432B49で`engine+0x1EEC4D=1`を設定し、後続event lookup/scene sheet処理がある。これらのpointerがUIで何を表示するか、nested event後の復元順序はVERIFY。これは**scene reference selection contract**であってevent/VM完全互換ではない。
- `dev_lab/event_view_branch.py`: 特殊入口で一般writer/3判定call不到達、一般側は初期評価＋1番目/2番目の順序・短絡、3つのpointer mappingを合成6件でPASS。

## MISSILE-R3：0x546F70内 0x4E7ED0 callerの3状態cacheとMP前帰路

一次保存native `exe/T012_ALLFUNC_FLOW_PROBE.txt` VA0x54714E..0x5471AC。Ghidra `4E7ED0_procedure_callers.json`でもcaller0x546F70と0x57EB40を確認。callee0x57EB40の全面復元は未実施。
- 前提となる複数の上位skill/scene gates（+0x1FC、+0x1EED40等）を通過した局所経路だけを扱う。Unit+0x1E560が2なら0x547157から即0x547480側へ出て、0x4E7ED0を呼ばない。
- +0x1E560が0でなければ0x5471A0へジャンプするため、値1（その他2以外の非ゼロ値も局所では同じ）は空間検査をskip。0の場合のみVA0x547173 `CALL 0x4E7ED0`。
- 0x4E7ED0結果AL非0なら0x54717Cで+0x1E560=2を代入→`AL=0`で0x54718Fまでの早期ret。この経路はSkill+0x278のMP減算0x5471A0を経由しない。AL0なら0x547196でlatch=1を格納して0x5471A0へ進む。
- 0x5471A0では[Unit+0x94] -= [Skill+0x278]、後続のミサイル効果処理が続く。これは**局所callsiteの制御フロー**であり、空間検査のALが「ミサイル命中／成功」である、または全技能でこの処理を通るという結論ではない。
- `dev_lab/missile_latch_subset.py`はlatch=0/1/2・spatial true/false・MP debit境界・predicate呼出数を別traceとし、6合成テストでPASS。

## 未確定・再開点と既存進捗

- このrunの新規Ghidra decompile=0、既存5点静的VERIFIED39/48（Wave1=16/16 Wave2=10/10 Wave3=10/10 Wave4=3/12）。今回の新規成果は**保存済みbinary pseudocode/assemblyの分岐契約精密化**。39/48を全EXE逆解析割合へ換算しない。
- 新しく読む候補：0x57EB40 callerのイベント種類、0x4E7ED0 radius側trig/原距離x87丸め、方向テーブル定数、0x4321B0 nested event再入とpointer復元。利用可能な安全な既存証拠のみを使う。
- 旧ゲームTARGET OBSERVED golden=0、新エンジン strict MATCH=0。上位owner T012/T013/T006/T014/T018の文書はread-only、MASTERはEのみ書込。
- 既往のGhidra batch `run_decompile.ps1`のSAFETY_REFUSALは未解除。別shell/Remote/tool/path等による迂回再試行禁止。原本・A〜E owner/MASTER/T018/Git/スケジュール/設定には変更を加えない。


## PROPERTY-R4：qualifiedキーの存在確認も50-pass上限を持つ（T005）

- 保存済みGhidra `runs/20261009T222501703Z/4693F0_procedure_{pseudo_code,assembly}.json` と `464290_procedure_{pseudo_code,assembly}.json`を照合。既存owner `data/T005_FORMAL_GRAMMAR.md` §Generic ExplicitNull / lookup上限と区別して記録。
- `0x4693F0`のdecompiler pseudoはifの両枝で同じ`FUN_004647D0`を呼ぶように表示するが、assemblyでは0x469426でqualified keyの存在確認`0x464290`をcall。存在時は0x469438 `MOV EDX,EDI`→0x46943A `CALL 0x4647D0`（qualified）、非存在時は0x46944A `MOV EDX,[ESP+0x18]`→0x469450 `CALL 0x4647D0`（base）。**register引数を落とした疑似コードを字面どおり同じ分岐と解釈しない**。
- `0x464290`存在確認はsuper chain解決を含む。assembly `0x464445`でlocal loop countを0へ初期化し、0x464550 `MOV EAX,[ESP+0x14]`→0x464554 `INC EAX`→0x464555 `MOV [ESP+0x14],EAX`→0x464559 `CMP EAX,0x32`→0x46455C `JL 0x464450`。**presence側の繰返しにも上限50**が存在する。別の値取得pathの既知 `0x464B49`の50-pass guardを今回初回発見として二重計上しない。
- `T005`の既存 owner §200–219 は `qualified(current→super) > base(current→super)`、明示null `@`でfallback停止、値取得側50-passを確認済み。今回追加の確認ポイントは**qualified存在チェック側にも独立上限がある**こと、およびGhidra pseudoがregister差を消す注意点。
- `[VERIFY]` 存在確認側countと値取得側countが実際に同じ構造体数を意味するか、欠損parent/cycle/継承段階のend resultは原作動的golden未測定。互換実装に『正式継承最大深度50』を無条件で要求しない。

