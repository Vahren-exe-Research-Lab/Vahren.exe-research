# 迫真戦記 ver0.67｜EXP・召喚・死亡 静的調査／DLL拡張判断
ID: HAKUSHIN-EXP-SUMMON-DEATH-20261021
Owner: independent read-only analysis. 保存先: rea_lab/headless_analysis/search_index。
状態: STATIC VERIFIED（記載した命令／データ／CALL）＋ INFERRED／VERIFY を区別。原作DYNAMIC OBSERVED=0、実機Golden PASS=0、EXE/DLL実装=NOT RUN。
対象: ver0.67 `hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
入力: `search.sqlite`, `CALLGRAPH.jsonl`, `DATA_REFS.jsonl`, 保存済み10,268件の擬似C、既存B T011/T012、REA死亡経路、MASTER cp195をすべて読み取り専用参照。
今回の機械証拠: `EXP_SUMMON_DEATH_MECHANICAL_20261021.json`（21関数、参照・文字列・元コードの該当行付き）。
静的整合性検査: `EXP_SUMMON_DEATH_VALIDATION_20261021.json`（24/24 PASS）。
既存B記録の重複を新規発見・新規READYと計上しない。既存E・B・REA台帳とdev_lab・Gitは編集しない。

## 1. EXPの物理フィールド
- [STATIC VERIFIED] linked/Unit-like object `+0x168` はレベルを表す4-byte整数として `0x58A650` がインクリメントする。旧研究Bにも一致。
- [STATIC VERIFIED] `+0x16C` はEXPと整合する4-byte整数。主加算 `0x551FB2`、drain移転 `0x578DAF/0x578DBB/0x578DCA`、閾値比較と保存・読込の独立証拠を確認。
- [STATIC VERIFIED] `+0x170` は比較閾値で、`0x58A400` が `exp_max`/`exp_mul` から再設定。`0x58A650` は unsigned比較 `+0x16C>=+0x170` を用いる。
- [STATIC VERIFIED] 戦闘Unit `+0x1C8` に別のUnit-like pointerを保存：`0x56F880` の `param_3`。EXP helperはここを経由して `+0x16C` に加算。
- [STATIC VERIFIED] 通常ストリームwriter `0x58EFD0` は `+0x168/+0x16C/+0x170` を個別4バイト値として出力する。reader `0x58E870` は対応fieldを読む経路。
- [INFERRED] `+0x16C` の論理名を経験値とするのは `exp_per`・閾値・levelupとの多重一致から高確度。原ゲームでの正確なUI値、セーブ復帰や全Unit lifetimeは未観測。
- [VERIFY] 戦闘Unit+0x1C8が、召喚獣・変身後Unitで常に戦略ユニットの同一永続個体を指すか、save writerが同一インスタンスを直にserializeするかは未確定。

## 2. EXP計算・加算・成長の経路
- [STATIC VERIFIED] `0x551E50` は context EAX, actor=[ctx], Skill=[ctx+8]。Skill+0x2A8 sentinel(-123456.0)、actor+0x1D0 null、actor+0x18614非zero、ctx+0xC非zeroを早期除外し、通過するとctx+0xCを1に設定する。
- [STATIC VERIFIED] 同関数は入力量比(`param_2/param_3`、0除算時初期0)、Skill+0x40種別、+0x2A8百分率、+0x44/+0x4C、+0x74等から加算量を丸める。+0x2A8=0枝に限り最低10のclamp経路がある。
- [STATIC VERIFIED] linked=[actor+0x1C8]、`0x551FB2` で `linked+0x16C += amount`。ctx+0xCにより同一contextでの二重加算を局所的に抑えるが、別context間の防止は別問題。
- [STATIC VERIFIED] actor+0x8C非0かつlinked+0x16C>=+0x170なら `0x551FD3 CALL 0x58A650`。追加のctx+0xE・`0x571A40` 条件を満たすと `t_levelup` と仮想 `levelup` 通知が実行される。
- [STATIC VERIFIED] `0x58A650` は `level_max`（既定contextフォールバック100）を読み、制限まで+0x168を上昇させ能力更新を実施。`0x58A400` が経験値閾値を計算し直す。多段階レベルアップの反復を持つ。
- [STATIC VERIFIED] `0x599BD0` の Skill+0x2A8 値の格納箇所には `exp_per` 文字列2参照（0x59BD57→0x624CF0、0x59BE41→0x624D08）が存在。off sentinel、on=1.0、整数百分率×0.01の枝を確認。
- [VERIFY] 全モード共通の丸め・オーバーフロー・context再利用、召喚技能に実際に経験値が発生する条件、死亡直前creditの順序は未確定。
## 3. 成功判定を分離すべき4 caller
| CALL site | caller | 役割と根拠 |
|---|---|---|
| `0x547A8C` | `0x547490` | 弾・攻撃／allfunc系の命中contextを作成しEXP helperへ |
| `0x551167` | `0x550E70` | ダメージ計算後の副作用経路 |
| `0x551C6A` | `0x551490` | 回復・状態変更の副作用経路 |
| `0x57F4E9` | `0x57F190` | 召喚/スキル発動のcontextからEXP helperへ |
[STATIC VERIFIED] 上表の4件はSQLite CALLGRAPHの完全一致。呼出箇所の存在は、実プレイですべての攻撃・回復・召喚にEXPが付くという保証ではない。
[VERIFY] param2/param3の厳密な意味、治療/召喚による EXP 獲得が合法技能で何度成立するか、間接callerの網羅性。

### 別経路 drain：中心helper一本では不十分
- [STATIC VERIFIED / B旧ASMと再照合] `0x578B70` の `0x578D99` で `q = unit_drain_mul * amount`。
- `0x578DA7..DBB`: 被害対象の `[Unit+0x1C8]+0x16C` を q 分減らす（不足なら0）。
- `0x578DC1..DCA`: 発生源の `[Unit+0x1C8]+0x16C` に **実減算量に関係なく q 全量**を加算。
- [STATIC VERIFIED] この局所コードには `0x58A650` 直接CALLは無い。別の後段にレベル調整がある可能性まで否定しない。
- [INFERRED] DLLが `0x551E50` だけを監視すると drain、スクリプト強制levelup、その他後段EXP反映を取り逃がす。少なくとも後述複数hook観測が必要。
- [VERIFY] マイナス量・uint32境界・オーバーフロー・同一源と対象・drain後の閾値更新は旧原作未観測。

## 4. 召喚Unit・部隊・参照先
- [STATIC VERIFIED] `0x54E7B0` の `0x54F07A CALL 0x56F880` が新規戦闘Unit風インスタンスを生成する。
- [STATIC VERIFIED] 生成時 `0x56F880` は Unit+0x1C8=param3、+0x1D4=param5、+0x1D0=param6、+0x1CC=0。param6非NULLなら部隊リストから先頭Unitの+0x1C8を採る条件枝があり+0x1CCへ格納する。
- [STATIC VERIFIED] `0x54E7B0` の `0x54F096 CALL 0x568710` が生成Unitと部隊参照の接続経路。 `0x568710` はnormal troop modeでUnit+0x1D0を部隊ポインタへセットし、selected modeではUnit+0x1867Dを立てる経路。
- [STATIC VERIFIED] `0x54E7B0` の部隊ポインタ選択には `oldUnit+0x1D0` を採る枝、別の選択関数を介する枝、部隊memberから選ぶ枝がある。一律に「召喚主本人」を選んでいるとは断定できない。
- [STATIC VERIFIED] `0x54E7B0` 内の生成Unit初期化には `0x58B7F0` 関数も使用。生成Lvの成立を、hitによる経験値獲得と混同しない。
- [INFERRED] +0x1D0はtroopオブジェクトへの所属/関連リンクであり、召喚主の永続的Unit IDではない。+0x1CCはrelated owner-likeリンクだが「召喚主の経験値格納先」の確定ではない。
- [VERIFY] summon masterへの安定した追跡：Skill owner→召喚生成context→param3/param6→現物Unit+1C8/1CC/1D0→戦略Unit ID。部隊混在・複数召喚主・変身・再召喚を独立検査する。
- [VERIFY] 召喚UnitのEXPが固有linked Unitへ加算されるのか、単純同一owner shared storageなのか、生成時スナップショットなのかは一律未確定。
## 5. 死亡・消滅・データ寿命
- [STATIC VERIFIED] `0x575A60` はUnit+0x1867C未設定時に設定し、linked+0x1B1を立て、Unit+0x90を0にする。MissileFlash等と複数virtual呼出を経由し、Unitをある戦闘内管理配列から除去する。
- [STATIC VERIFIED] `0x575DF0` はUnitの複数子領域（+0x540/+0x5B0/+0x800/+0x89C等）をcleanupし、Unit+0x1D0があれば `0x575F6C CALL 0x5684B0`。
- [STATIC VERIFIED] 第一更新から帰った**後で** Unit+0x1867Dを再読し、非0なら `0x575F8C CALL 0x5684B0`。2呼出しの存在は確定だが常時2回呼ぶわけではない。
- [STATIC VERIFIED] `0x5684B0` はselected troop listからUnit+0x1867Cを判定し死者memberを取り除き、+0x1867Dを0にする枝を持つ。REA-20261019-2143の保存ASM限定報告と整合。
- [STATIC VERIFIED] `0x575A60` 内5箇所、`0x575DF0` 内12箇所の間接CALL候補が機械保存された。両関数への**直接callerが索引上0でも未到達とは断定できない**。
- [VERIFY] 召喚獣の消滅経路が毎回この二関数に到達するか、Unit/linkedオブジェクトの destructor/refcount/final-freeアドレス、あとで再利用されるpointer、死亡後の経験値の保存先は不明。
- [VERIFY] dead_event（例0x5789F2→event dispatcher 0x4321B0）・召喚変身スクリプトの遅延イベントと、同一個体IDを再利用するかは別途確認する。
- [INFERRED] DLLで死亡後に経験値を移転したい場合、**死亡時に生ポインタだけ保存する設計は危険**。死亡フラグの変更前に必要値とowner識別子をスナップショットし、フレーム後・撤去後の使用可否を検証する。
- [VERIFY] 死亡→変身→再生成が `linked+0x16C` をどう継ぐかは一般化できない。T024で確認済みfake EU proxyの移動/削除/遅延復帰は特別なscript経路であり、一般的なtransformルールではない。

## 6. 簡易戦闘／CPU同士
- [STATIC VERIFIED] 文字列 `simplebattle` を参照する関数に `0x491870`（文字列0x632040/68/94）と `0x521D90`（0x62B454）がある。
- [STATIC VERIFIED] これら二dispatcherから `0x551E50` への直接CALLは検索範囲では0件。これはその関数内に直接CALLがない事実に過ぎず、間接・下位経路を否定しない。
- [STATIC VERIFIED] `0x58A650` の別caller `0x471E80@0x4723DE` と `0x4A7A90@0x4AB49B` には閾値へ経験値を強制一致させレベルアップさせる経路がある。簡易戦闘処理由来と断言できない。
- [VERIFY] CPU同士のsimplebattleで実際にどのユニットへ何XP/レベルを与えるか、通常戦闘と同じhit context/EXP helperを通すかは未確定。
- [VERIFY] ターン終了時・簡易戦闘終了時・戦闘結果配布時の経験値確定とsaveへの反映契約を原作保存・合法UI観測で特定する。対象EXEの起動は禁止のため本回DYNAMIC OBSERVED=0。
## 7. DLL実現可能性／介入リスク評価（修正実装なし）
| 要件 | 暫定実現可能性 | 介入候補と条件 | 未解明／危険 |
|---|---|---|---|
| A. XP獲得を観測 | 高（通常hitに限定した静的技術評価） | `0x551FB2` 前後／`0x551E50` 正常帰還後のlinked EXP差分、drainの `0x578DAF..DCA` | x86非標準ABI、FPU/レジスタ保存、別context二重処理、再入、間接経路 |
| B. 取得源と受取先特定 | 中（linkのみ）、真の召喚主は未確認 | actor `+0x1C8`、召喚 `0x54E7B0→0x56F880/0x568710`、Troop `+0x1D0` | +1CCが真のownerか／同一Troopで複数召喚主／永続ID／変身後参照 |
| C. 比率配分し他UnitへXP付与 | 条件付き可能、未実装 | +16C 加算と `0x58A650/0x58A400` 後処理の既知枝を参考に | 丸め・上限・閾値・二重加算・死亡タイミング・drain非保存則 |
| D. 死亡後にも移転 | スナップショット方式なら設計上可能 | Unit+1867C立つ前後で読み取り、linked/ownerを安全な外部stateへ退避 | destructor/final-free/ID再利用未同定、後段event callback、pointer失効 |
| E. 通常＋簡易戦闘共通ルール | VERIFY、現時点で実装可否未判定 | 通常hit + simplebattle 結果配布の別入り口で同じ配分serviceへ統合 | simplebattle EXP処理/戦略個体とのidentity/頻度未特定 |
- [INFERRED] **通常戦闘の一部を観測するx86 DLL PoCは合理的な候補**。ただしすべての召喚・変身・簡略戦闘で正しく動くDLLは未設計・未実証である。
- 先にread-only計測を設計し、既知owner ID・同一Unit繰返しhit・死亡時pointer寿命・戦闘終了時EXP/save処理を個別に確定させるべき。
- 監視だけのPoCでも適正な対象ハッシュ、DLL注入同意、原作ゲーム停止時作業、CPU負荷、クラッシュ復旧可能な複製環境が必要。今回は実装/注入/実行を行わない。
## 8. 後続Golden観測計画（設計のみ / NOT RUN）
1. K0 基準：同一原作EXE/DAT/SAVE SHAで実機起動前セーブを複製、移動・敵攻撃なし。Unit/Troop/linked pointer・EXP・Lv・RNG/stateを記録可能な合法条件を確認。
2. K1 通常の単発命中：同一contextの複数副作用と別context2回を区別。551E50入口gate +0xC、linked+0x16C pre/post、+0x170、LvとUI通知が一致するか。
3. K2 heal/MP：回復HPと加算EXP、Skill exp_per=off/on/0/40、+0x74分割とレベルアップ通知を独立採取。
4. K3 summon：召喚主2体・同一Troopと別Troop・同時召喚・未召喚を比較。new Unit ptr、+1C8、+1CC、+1D0、召喚主の永続Unit識別子を紐付け。
5. K4 death：HP0前後→Unit+0x1867C/linked+0x1B1→0x575A60/575DF0/5684B0条件付きCALL→既存pointerの再利用/破棄をフレーム境界で観測。
6. K5 transform/死後召喚：変身前後の戦略Unit ID・保存可能EXPの連続性、生成元が同じ/異なる、event/遅延変更を区別。
7. K6 CPU簡易戦闘：通常と同一出発状態・ユニット・結果でEXP/Lv/セーブを比較し、実際の簡易戦闘結果入口を先に確定。計算が別ならhook二系統を設計。
8. K7 drain：target EXP<q, ==q, >q の3条件、source同一/別、閾値跨ぎ、overflow境界を分離。過剰creditを確認。
9. K8 save/load：各状態でnormal save→reload→次の戦闘後まで Unit+168/16C/170、関連Unit identity、イベント副作用を検証。
- 全ケースについてACTUAL gameplay PASSは0。旧EXE・セーブ・DATの無断実行/変更禁止。ユニットの可視名称と観測ポインタIDの対応が取れない試験はUNKNOWNとする。
- 合法に動的トレースする方法の設計が認可されるまで、メモリread/Hook/DLL実装は先行しない。

## 9. 研究引継ぎ（所有権保持）
- 研究B/T011: Unit+1C8/1CC/1D0 の正しいsummoner/owner identity、再生成とlife cycle（本書§4-5）。
- 研究B/T012: `0x551E50` のEXP計算・drain・levelup連携と文脈flag（本書§2-3）。
- REA: 保存済み死亡二Troop CALL到達条件、0x575F71再読を前提として新static evidenceだけ照合（重複64件の再取得なし）。
- 研究E/T018: original Golden NOT RUN、K0-K8の受入条件と静的/実測の境界。MASTERへはEだけが公式統合可能。
- 本研究は `search_index` の派生証拠として保存。A-E owner台帳・MASTER・REA QUEUE・work request queue・Git・ゲーム原本は変更しない。本ファイルは他のチャットへのライブ通知ではなく、担当者が読み取る引継ぎ文書。
- 継続作業の第一候補：`0x54E7B0` のparam3/param6源をcaller別に再確認し、0x56F880+1C8が戦略実体へ到るパスを合法に静的検査。旧安全拒否済み解析箇所を別tool/pathで再試行しない。
- 新ソースコード改変0、動的原作観測0、虚偽のREADY追加0、BLOCKED新規拒否0。結論は「限定的DLL可否は前向き、汎用EXP連動は識別/寿命/簡易戦闘未解明で保留」。
