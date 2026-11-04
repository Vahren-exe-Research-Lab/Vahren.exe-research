# 迫真戦記 新B｜未同期回収照合とGolden観測適格性ゲート（2026-10-20 12:14 JST）

**復旧ID**: `B-RC-OFFLINE-20261020-1214-LOCAL-SESSION-01`  
**新規オフライン設計ID**: `B-OFFLINE-20261020-1214-01`（正式B証拠IDではない）  
**所有**: Lane B、T012/T013主体、T024/T028との横断試験設計。T011は既存未同期索引の回収対象。  
**状態**: `DESIGN-SYNTHETIC / VERIFY / OFFLINE-UNSYNCED / NOT READY`。新規原作ASM解析・Gameplay実測は行わない。

## 1. 今回の接続と出典の境界

- Localで `[RESEARCH_ROOT]\MASTER_LEDGER.md` を読み込もうとしたところ、`INVALID_ARGUMENT: McpServerError: Session terminated`。これは**接続障害**であり、新たな安全拒否ではない。Remoteへ切替えない。
- 今回Libraryで実際に一覧確認・独立読み戻ししたのは `/迫真戦記再開発プロジェクト/data/T011_T012_T013_T024_T028_OFFLINE_RECOVERY_INDEX_20261020_1117.md`（Library modified 2026-10-20T02:20:29Z、全74行）および `T011_T012_T013_T024_T028_UNSYNCED_RECOVERY_REGISTER_20261020.md`（modified 2026-10-20T02:18:47Z、全77行）。参照した追加の古い資料は `T012_T013_DUAL_CACHE_ORIGIN_AND_V80_BRANCH_MATRIX_OFFLINE_20261019.md`（modified 2026-10-19T06:27:01Z）と旧Library MASTERの検索断片。
- **最後に会話で報告されたPC正本**: checkpoint194（2026-10-20 10:15頃、現run未確認）。**直接確認済みのLibrary MASTER**: 旧checkpoint187、modified 2026-10-18T16:59:36Z。最新正本のTASK QUEUE・予約・統合済みID・最新HANDOFFの差分は**未確認**。
- 2026-10-20 10:15の `B-20261020-1015-01/02` は会話でPC B限定STATIC READY保存済みと報告されているが、現runの独立PC再読なし。今回のREADY/統合に加算しない。
- 保護対象（ZIP/EXE/SAVE）、REA、T018、他レーン、MASTER、Git、設定、スケジュールには書き込まない。禁止されたVA 0x5710C0..0x571500の新規逆解析や安全拒否を迂回しない。

## 2. 未同期記録：2索引の重複防止集計（新規証拠件数ではない）

| 回収グループ | 索引にある研究/監査候補数 | 直接PC保存したと今回確認 | Libraryの既存索引へ回収済み | 状態 |
|---|---:|---:|---:|---|
| 2026-10-19の既存研究ID | 7 | 0 | 7 | 原因別に未同期/部分保存/安全拒否を要照合 |
| 2026-10-20 03:16～09:08の候補 | 15（うち非新規AUDIT1） | 0 | 15 | OFFLINE-UNSYNCED、正式READY未確定 |
| 安全拒否案件（別枠・上記と重複あり） | 8 | 0 | 8件の復旧メタデータ | BLOCKED状態を変えない |
| 10:15報告のPC B限定READY | 2（上の22の外） | 今回0 | 索引中に参照のみ | PC再確認まで現run加算0 |

**候補22件の正確なIDは上記2索引に既存記録済み**。新ファイルへのID全文再列挙は二重管理の原因になるため行わない。意味重複/重なりを次の順に先行照合する。

1. `B-OFFLINE-20261020-0316-01`（時間延長と加速条件） ↔ `B-20261020-1015-02`（10:15報告の時間ゲート複合）。先行READYに包含済みなら前者を新規証拠としない。
2. `B-OFFLINE-20261019-1009-01`（グリッド負座標） ↔ `B-OFFLINE-20261020-0517-01`。同一変換の再発見可能性。
3. `B-OFFLINE-20261019-1217-04`（global scratch clear） ↔ `B-OFFLINE-20261020-0613-01`。同じ一時配列を二重登録しない。
4. `B-OFFLINE-20261019-1217-03`（selector） ↔ `B-OFFLINE-20261020-0409-01`（tie維持）。後者が真の細分化か、旧B証拠に既出か確認する。
5. `B-OFFLINE-20261020-0409-02`（攻撃側距離演算） ↔ `B-OFFLINE-20261020-0908-02`（支援側距離演算）。関数が異なるため即重複とは断定しない。作用点と証拠VAで区別。
6. `B-OFFLINE-20261020-0815-01`（Unit local vector reset） ↔ `B-OFFLINE-20261020-0613-01`（global scratch reset）。異なる配列の可能性があるため、安易に同一にも独立にも認定しない。
7. `B-OFFLINE-20261019-1516-06`の`0x580280`分岐fixtureと本書第3節は別物。本書はcallee解析や既存branch fixtureの再検査ではなく、**Golden証拠をPASSに昇格可能かの受付条件**を初めて分離する設計物。

## 3. 新規設計区画A：T012の「実作用」を誤認しないGolden観測ゲート

旧Bオフライン複合資料の既存前提（本回の新発見ではない）：`0x57E381`以降の条件分岐では、`Skill+0x26F==0`、非ゼロかつ`ESI+0x74==0`（`CALL 0x580280`）、非ゼロかつ`ESI+0x74!=0`（`CALL 0x54F720`）を区別し、共通のvirtual slot `+0x80`へ向かう局所記録がある。ここから**callee実作用・発射成功・HP/MP変化は確定しない**。

**今後のGolden候補を3段階に分類**する：

| 証拠層 | 必要な観測 | 原作UIのみでの受付結果 |
|---|---|---|
| 静的callsite receipt | 分岐条件、`0x580280`/`0x54F720`呼出、slot+80と引数出自 | UIだけでは直接観測できず `INELIGIBLE`。保存ASMのSTATIC/VERIFYに限定。 |
| Gameplay表面 | 同一条件での発射表示、対象、HP変化、MP変化、status、次tick | 旧/新双方の動画または画面＋時刻・入力対応・原本識別があれば**比較候補**。 |
| 内部効果・RNG | callee戻り、内部latch、隠れた乱数消費 | UIから推測でPASSしない。独立した許可済み観測証拠が必要。 |

**重要**: `0x580280`の`CALL`が成立したという静的条件と、「攻撃が成功した」「HPが減った」は別の命題。旧UIの可視結果からcallee個別の因果を単独特定できない場合、局所命題を `VERIFY` に留める。MP fallbackについても`AL0/AL1`や`+0x4C`ゲートの分岐receiptと「発射した」「MPを消費した」を混同しない。

## 4. 新規設計区画B：T013対象探索・支援キャッシュの可視性ゲート

既存保存REA報告で論点となる`0x514D60`、`0x514F10`、`0x57B870`等の候補列挙、tie優先、stealth RNG、global scratch/Unit local vector、24byte候補recordの内部値は、旧ゲーム画面だけでは原則直接見えない。したがって次を分離する。

- 可視Golden候補：ターゲットがUIで明確に識別できるケース、支援の実行、HP/状態変化、次tickの行動、必要な入力と動画時刻。旧/新の比較を同条件で成立させる。
- 内部のみ：`Unit+0x1E580`等の補助ポインタ、record `+0x04/+0x14`、`end=begin`、候補配列容量、乱数消費回数。旧UIから不可視なら `INELIGIBLE`。任意のバイト一致をGolden PASSとして偽装しない。
- stealth候補の列挙順が変わると乱数消費が変わり得るため、**target不一致だけで距離tieの不具合と決めつけない**。候補集合、候補順、乱数初期条件、stealth有効/無効を別の観測条件として記録する。
- 24byte未初期化疑惑はrecord consumerと初期化経路が不明であり、padding・未使用領域・未定義バイトの差分だけで「不具合」やstrict不一致を認定しない。

## 5. 新規設計区画C：T024/T028タイマ交差の試験成立条件

既存の原作script宣言として報告されている`getLimit()>=500`（通常集合/移動）、`getLimit()<500`（終盤加速）、`addLimit(514)`（特定ボス死亡イベント）を混同しない。今後の実機Goldenで次を必須にする。

1. その戦闘に**両イベントが合法に登録**され、死亡時に実際に`addLimit`条件が成立したと確認できること。`chuboss_alc`等のbattle条件を保存済み原文と照合する。
2. `addLimit`前後の残り時間表示、死亡/AI処理の起動順、更新tick、CPUの行動、集合間隔を区別。`addLimit`のAPI実作用と整数境界は未確認。
3. 時間ゲートが成立したことと、AIが実際に集合/逃走/加速したことを分離。定期間隔・隊長生存・既付与スキル寿命など追加条件を漏らさない。
4. UIで通常AIと簡易AIの内部起動を識別できないなら、戦闘画面の移動結果だけを条件付き比較し、特定branch実行PASSとは言わない。

## 6. 合成検証（新規・原作実機ではない）

添付 `test_T012_T013_T024_GOLDEN_ADMISSIBILITY_20261020.py` はPython標準機能のみ使用し、観測情報の有無で `INELIGIBLE` / `NOT_RUN` / `VERIFY` / `MISMATCH` / `MATCH_CANDIDATE` を判定する小規模**設計テスト**である。`MATCH_CANDIDATE` は**正式strict MATCHでもGolden PASSでもない**。原作・再実装両方の可視結果、ソース識別SHA、制御入力、フレーム整合が必要で、どれか欠ければPASSへ進めない。

2026-10-20 12時台、孤立Pythonモデルの**10/10 SYNTHETIC_ADMISSIBILITY_PASS**。原作実機は未起動で、`Gameplay Golden PASS=0`、`strict MATCH=0`、`READY=0`、`MASTER統合=0`。テスト条件はT012実作用、T013 hidden cache、T024合法イベント共起の**受付条件**に限り、実行経路・原作仕様を新たに保証しない。

## 7. 保存・引き継ぎ・次回再開位置

- 今回作成ファイル：本Markdownと上記Python受付検査。Cloudへ追加する場合はLibraryのB所有`/迫真戦記再開発プロジェクト/data/`へ**新規独立ファイル**として保存し、別の読取APIで本文/IDを読み戻す。共有MASTER/既存復旧索引を上書きしない。
- **PC保存**：NO。**PC最新版/HANDOFF照合**：NO。**新しい正式B証拠**：0。**E統合**：0。
- 接続回復時の優先順位：(a) PC最新MASTER/規約/HANDOFF/T011/T012/T013/T024/T028確認、(b) `B-20261020-1015-01/02`の保存/重複チェック、(c) 第2節の重複ペアと安全拒否8件の復旧メタデータ仕分け、(d) 真に独立したB owner増分だけ許可場所へ保存・別読取で検査、(e) EへHANDOFF。安全拒否済みの同一操作/本文を他経路で再提出しない。
- 未解決P0はT012 `0x580280`実作用、MP fallback、Skill+0xA18/A1C・latch・最終攻撃結果、T013 selector/tie/RNG/キャッシュ消費者、T011 cross-kind effective inheritance、T024実際のAI状態、T028 morale効果寿命・タイマAPI実作用。原作Goldenとstrict MATCHは0のまま。
- **PC負荷**：Local非接続で不明。**Local接続障害**：Session terminated。**安全拒否**：本回新規なし、既存BLOCKED継続。**Remote/Work使用**：なし。**自動化設定変更**：なし。

> この資料は独立した検証設計・回収照合の増分であり、保存済みの解析結果の新規再検証、正式B READYまたは旧ゲームGolden成功を意味しない。
