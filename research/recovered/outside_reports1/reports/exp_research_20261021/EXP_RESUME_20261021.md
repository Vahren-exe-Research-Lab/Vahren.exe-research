# EXP-COLLAB-20261021-2112-01 | RESUME / 未解決と検証仕様

## 最終成功した保存
- `EXP_COLLAB_HANDOFF_20261021.md` 保存/独立readback成功。
- `EXP_CACHED_RECORD_LIFETIME_20261021.md` 元Rレコード析出/破棄の既存CP12再照合。既報として再計上0。
- `EXP_THREE_PRODUCER_CROSSJOIN_20261021.md` 新しい3producerの4段階CALL比較表。
- `EXP_BUILD_AI_EVIDENCE_20261021.py` 26関数ハッシュ・8CALL・32文字列hitのPC静的検証器。
- `EXP_AI_EVIDENCE_20261021.json` 生成ログPASS、26/26コードSHA・8/8直接CALL・DBハッシュ一致/SQLite integrity ok、独立readback成功。
- `EXP_VALIDATE_PRODUCER_PATHS_20261021.py` 3×4site検証器。12/12 PASS、`EXP_THREE_PRODUCER_CALLS_20261021.json`新規生成。
- `EXP_SHARED_INDEX_20261021.md` AI検索用ファイル入口。

## 最重要の未解決
1. 0x547490、0x553390、0x54E7B0でcache lookup 0x577260へ渡す `source BattleUnit, key` がどのように選定されるか。異なる効果pathが同じRを参照する合法入力があるか。
2. 0x577310が返すnode+0x28のRのEXPを、戦闘終了から戦略SAVEへ明示的にコピーする成功経路があるか。単に+1E4B8への直接アクセスが無い事実だけで無転送と断定禁止。
3. 0x55B010 BattleUnitデストラクタが戦闘終了0x493630／0x49B5C0とどの順に結び付くか。中継する間接virtualの具体型と、コピー済みEXPの生存期間。
4. BattleUnit型Unit/SimpleUnit/StaticUnit/SimpleStaticUnitの+0x8C/+0x8Dと陣営+0x48/+0x58への登録および+0x575110による遅延Lv判定の正規条件。
5. 同一召喚元の同名再召喚、別技能同名召喚、別Troop、召喚者死亡時でRを共有・再計算・破棄する違い。
6. 戦略Unit（永続）と戦闘Unit（巨大な一時object）のID一致条件。アドレスのみで同一性判断不可。

## Goldenの最小試験（DESIGNED / NOT RUN）
- EXE/DAT/SAVE/MAP/input/capture SHAを固定。開始前の親unit EXP/Lv、召喚時、子1回命中後、決着直前、陣営Lv更新後、戦略画面復帰、SAVE→LOAD後を比較。
- S1: 召喚だけ、S2: 召喚子のみ命中、S3: 同一キー再召喚、S4: 異なる技能・同一召喚キー、S5: 子死亡、S6: 親死亡。経路と値を別記録し、確認できない内部状態はUNKNOWN。
- 平均経験値・外部DLLフックのPoCに進む前に合法な旧原作実測を作る。原作実機Golden PASS0。

## 検査・所有ルール
- PCの原本・既存Ghidra本体・DB・B/E/Work/rea_lab正本は上書きしない。
- 過去安全拒否: `EXP_WIKI_DRAFT_PC_20261021.md` の未保存続きを含めて、元拒否payloadや特定VAを別tool/別shell/別path等で再試行しない。該当案件は先行RECOVERY-IDどおりBLOCKED。
- 進展は本フォルダ内に新IDでappendし、毎回readbackする。研究B/Eには文書を読んでもらうことで同期、プッシュ通知済みとは言わない。
- 次回の最初: `EXP_SHARED_INDEX_20261021.md`、PC最新MASTER/B HANDOFFと検索DB manifest、最新オフライン派生を重複照合し、別ID/STATUSで再開。

## CP03再開追記
- `0x545CC0` はSkill+0x40のcase4で0x547490へ、`0x552EF0` は+0x40==4で0x553390へ。後者はSkill+0x74回数を0のとき1にfallbackする。上位2CALL/6文字列条件を保存擬似Cから検査してPASS。
- NEXT: `0x552EF0` の間接到達と具体的な合法技能、`0x545CC0` のケース4に入る効果オブジェクトの同一性、2経路が同じRキーを扱うかをGoldenに先立って静的に調べる。

## 2026-10-21 新研究 EXP-CACHEKEY-20261021-01 / EXP-SAVETREE-20261021-01
- 最新研究入口: `EXP_SHARED_INDEX_20261021.md` 冒頭の「最新研究」節。**追加ZIPは作らずMD/JSONに保存**。
- 0x579940から文字列キーの長さ・capacity・生byte比較を確認。0x54E7B0のSkill+0x14Cは固定キー文字列+0x13Cのlength、空ならSkill+0x158の候補一覧にfallback。next_orderのraw DAT意味は既存Bと重複。
- 0x57A6E0のノード512byte、埋込みRオブジェクト468byte、検索0x577260 ret0x1C、登録0x577310 ret0x1D4/EAX=Rを原本x86で再確認。外部DLLはGhidraのvoid/引数数をそのまま利用しない。
- SAVE 0x460000 はroot+0x300ノードの+0x28値をポインタとして読んで0x58EFD0を呼ぶ。一方召喚treeはnode+0x28内にRを直接配置。SAVE側経路はRの直列化そのものではないが、別の転送経路の不存在は未確認。
- 新証拠: `EXP_STRING_CACHE_ABI_EVIDENCE_20261021.json` 39/39 native PASS、`EXP_SAVE_TREE_BOUNDARY_EVIDENCE_20261021.json` 10/10 native PASS・直接writer caller 1件一致。
- 次優先: (a) Rと永久UnitDataを結ぶ明示的なEXPコピーsite、(b) 同一親の複数同キー召喚時のR再利用、(c) 親/子死亡後のEXPとnode破棄順序。動的確認まではINFERRED/VERIFY。
- 既安全拒否としてB所有資料に0x579A20を確認。以後そのVAの新規読取・再解析をせず、独立確認可能な他の許可済み証拠を利用。旧拒否済みWiki追記も再提出しない。
- RECOVERY `EXP-RC-20261021-INDEX-EDIT-SYNTAX-01`: 研究索引edit呼出前、JSで予約語newを変数名にしたSyntaxError（OTHER）。副作用/書込0。変数を変更した後に通常のedit_blockで同一索引の見出し更新成功・ツール出力で確認。RECOVERED、未保存差分0。
- 原本Gameplay Golden PASS0、新B正式READY0、E MASTER統合0、Task DONE増加0。

## EXP-20261022-RESEARCH-CHECKPOINT / ローカル研究の継続記録
- 最新入口: `EXP_SHARED_INDEX_20261021.md` 冒頭の2026-10-22節。ZIP更新なし。
- `EXP_WRITER_CENSUS_20261022.json`: 旧Ghidra DBのsource_SHA一致・32関数中拒否範囲0x5710C0は除外、31関数56参照行、代入左辺候補26（意味ラベルは別途要検証）。
- 独立最新V2 CALL索引による直接呼出: 0x466470=3件、0x466BA0=5件、0x58EFD0=1件、0x543E00=6件。既記録より誤差なし。いずれも即時実機到達の証明ではない。
- `EXP_SUMMON_DESTRUCTOR_VTABLE_20261022.json`: 原本vtable先頭0x63A9E4→0x570C90→0x543E00→0x5450C0→0x5454D0→0x4591F0を限定STATIC実証（native7、direct4）。
- `EXP_UNIT_VTABLE_WRITER_SCAN_20261022.json`: 0x56F880の正常パート1,121命令で直接[EBP] vptr storeは0x56F8DDのみ。helper副作用と他サブタイプは網羅外。
- `EXP_RESEARCH_PROGRESS_20261022.md`: 主要静的理解65～75%、実機確認込み仕様解明40～50%は主観的評価。今後の重点約8～10テーマ。実機Golden0。
- `EXP_20261022_VERIFY_ONLY.py`: 4証拠JSON/3報告Markdownの参照と整合を再検査、PASS。原本/既存DBを変更していない。

## RECOVERY EXP-RC-20261022-VTABLE-REGEX-01 / OTHER / RECOVERED
- `EXP_UNIT_VTABLE_WRITER_SCAN_20261022.py`初回は正規表現の閉じ括弧直後に余分な単語境界\bを指定したため0候補・AssertionError。出力JSONは未生成、EXE/DBは無変更。
- 正規表現の1か所のみ修正して通常の正規runを実施、1,121命令のうちvptr write1件、JSON生成・監査PASS。拒否操作の迂回ではない。未保存発見0、次再開は実際のvirtual destructor到達時刻を検討。
- 既存B/E/REA/Work/MASTERの正本変更なし。担当B/Eは本研究を別資料として重複・所有権を検査してから必要時に正式採用。手動通知/プッシュ送信は実施なし。

## EXP-SIMPLE-LIFECYCLE-20261022-02｜この回の最終チェックポイント
- 保存: EXP_SIMPLEBATTLE_LIFECYCLE_20261022.md、同EVIDENCE/VALIDATIONのJSON、probe/verify Python。既存EXP_SHARED_INDEX冒頭を更新。ZIP作成なし。
- 現行DB: HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite、SHA256=20B069B6E002FA0B0098C6BE3BB26F2C6FB971C4D4AC0A717EC109986E7E74BE。元EXE既知SHA一致、両sourceは解析前後不変。
- 新接続A: BattleWnd+0x238 update roster→SimpleUnit virtual+4=545740→545CC0→近接virtual7C=546C90→550E70→551E50、回復551490→551E50。+8C=1で条件付き即時58A650。
- 新接続B: 467DE0が登録ツリーのUnitData*を返す→40F766 EDI保持→40F7A5引数→54436E+1C8。対象分岐ではコピー不要の直接更新。召喚Rとは保存寿命が異なる。
- 新接続C: 40E220の決着非0枝は493630→40F000→48ABF0。2陣営virtual10=514AA0→個体slot0=570C90→既存召喚R解放。493630内のEXP転送有無は未証明。
- 40E2F0は1call最大500内部反復、50周期の判定。0返却は未決着/処理中断の可能性で、引き分け確定ではない。callbackの0枝は表示更新のみ。
- 検査: 元PEと現行索引の直接CALL21、vtable8、命令32が一致。別検証器で61を再読し、配列登録の追加命令9/アドレス同値4も一致。EVIDENCE SHA61226CF42A74BD0C43994CE0D051269DC40F242BBC48F8968B59D3E51142F9C6、VALIDATION SHAADFFA900FAE385DB7ECEA091369403E2B6D66988D4ACD39E5E6F3BB16FA0ED45。
- 再開優先: 493630と下位イベントでR→永久UnitDataへ移るwriter、簡易戦闘の遠距離/特殊技能・全CPUモードの入口、原作同条件EXP比較。生アドレスの一致だけで永続IDとしない。
- 原作実行0、Golden0、正式B READY追加0、E統合0、他owner/Work/原本/Git変更0。今回の新規失敗・拒否なし。過去拒否済み本文/VAの再試行なし。

## EXP-ENDTRANSFER-20261022-03｜通常/簡易召喚の経験値gateと終了処理
- 本文EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md、証拠EXP_SUMMON_GATES_EVIDENCE_20261022.json、独立検証EXP_ENDTRANSFER_VALIDATION_20261022.jsonを保存。
- 原本41site/5文字列/kind4固定0.01、通常modeをyorozu troop/troop2/troop3へ接続。簡易2生成callはECX=0→child+1D0=0→共通EXPの早期returnに対応。
- 簡易主経路0x547490末尾はactor=親、target=親で0x551E50を1site発行。子のRから親への転送ではない。生成loopの外、無効化gateは継続有効。
- 配置helperNULLかつcenter無しの子除去枝が0x547AE0→0x547A68へ合流する。一方候補空はAL=0で帰る。可視成功数と発動EXPは同一ではない（実機未検証）。
- 吸収0x578B70→通常加算0x551E50は別経路・順序。共通gate不成立を全EXP書込禁止と誤認しない。
- 元ZIPのscript590 DATで85直接yorozu指定行（コメント除外）と4具体例を保存。継承後の有効技能数ではない。
- 入力更新: CLIがV2→V3へ切替。V2 native censusとV3追加証拠を版分離、対象7関数の擬似C一致を検証。V3 SHA=0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25。
- EXP_TRANSFER_NATIVE_CENSUS_20261022.jsonは595,450命令/151offset一致/11除外範囲。candidateは意味上のwriterではない。終了本体に直接field無しだけで転送不存在を証明しない。
- 最後の独立検証: 41site+5文字列再読一致、吸収の追加3site、SimpleUnit+58 vtable確認。EXP_SUMMON_GATES_EVIDENCE SHA=24358BF90FF88DE65CE095EA09763E2BB500317089BEFF266050663FFE0911AB。
- 次のP0: 0x568710等による召喚子の後続Troop変更、獲得可能Rと結果0x493630の間接接続、吸収時のR増分・簡易子Lv更新。通常/簡易それぞれ原作実測で確認する。
- 原本実行/製品変更/Git/push/他lane/MASTER/Work/ZIP更新なし。原作比較NOT RUN、完了率%は根拠なく上げない。今回の失敗・拒否による未保存差分なし。

## EXP-RC-20261022-03-CHAT-EXPORT｜チャット添付用コピーの作成環境エラー
- 対象: PC研究本文を要約した任意のチャット添付用Markdown（PC正本ではない）。
- container.execで/mnt/dataへの出力を試みたが、caas.internal.errors.ClientError。Python実行環境による存在確認も同じClientErrorで失敗。
- 状態: CONTAINER_UNAVAILABLE / CHAT_EXPORT_NOT_VERIFIED。安全拒否・PC書込拒否ではない。同じ実行環境への追加再試行は停止。
- PC上の研究本文、native evidence、独立検証JSON、索引、再開記録は保存済み。研究発見の未保存差分なし。任意の添付コピーだけ未確認。
- sandboxファイルの存在が確認できないため、当回はsandboxリンクを提示しない。再開はPCのEXP_SHARED_INDEX_20261021.mdから可能。

## EXP-SETTLEMENT-20261022-04 / 中間チェックポイント
- 現行V3の結果処理直接graphから中立兵生成0x460940へ到達することを追跡し、monster_level/neutral_*文字列と生成先への引数を原本で確認。召喚EXP還元の根拠とはならない。詳細は既存EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md CP08へ保存。
- 0x575110のactor+1C8→自己UnitData+168加算→同じpointerを58AFA0/58A400へ渡すnative siteを読取。Simple flag+8C=1の早期returnも再確認。次は証拠を統合し、吸収後のLv確定条件を交差検証。
- RECOVERY-ID EXP-RC-20261022-CONTAINER-PROBE-04 / ENVIRONMENT_ERROR: ChatGPT container.execおよびpython.execで解析ライブラリ有無と作業領域を確認しようとしたが、いずれもClientError。ゲーム実行・ファイル作成はしていない。サンドボックスへの成果複製は未実施。PC Localで独立した許可済み研究を継続する。
- PC Pythonにはpefile/capstoneあり、unicornなし。追加パッケージ導入・原作実行・DLL注入は行わない。過去拒否対象は従来どおり除外。新規安全拒否なし。

## EXP-SETTLEMENT-20261022-04 / 最終チェックポイント
- 本文は既存EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.mdのCP08～CP15。旧CP06を訂正。正の吸収は攻撃側で通常EXP判定の後、回復側呼出しはEAX=0。取り違えのあった旧説明を一般則として使わない。
- add/add2→固定文字列/候補一覧→同一live owner/keyのR共有、cache hitによる初期Lv計算skipを原本siteと原作4技能例で接続。別技能IDや別候補位置を別Rとみなさない。
- 575110の終了Lv確定はactor自身の+1C8先。結果rootからEXP初期化へ進む別枝はneutral_* / monster_levelによる新しい中立兵生成と判別。一般親還元の有無は未確定のまま。
- EXP_SETTLEMENT_OWNER_AUDIT_20261022_04.json SHA=B201C5CB9AF30EAE5A9D05FBBB6D9B2B562BBCBB701FE7E410187FB761073073。独立replayを実行し61native/9literal/3vtable/16pseudocSHA/4DAT/11edge出現の一致を確認。EXP_SETTLEMENT_OWNER_REPLAY_20261022_04.json保存済。
- 追加DAT: EXP_DRAIN_DAT_USAGE_20261022_04.json SHA=C986D687855155FD9109DAB576559B9702CC0017F1E425BAAD550F5DC147F76A。590DATの限定解析、直接drain13宣言＋子孫9、親4の計26sourceを再読。全候補func=status、正のEXP吸収を行う原作攻撃技能は未特定。エンジンの潜在挙動をMODで確認済みの不具合としない。
- 次優先は実使用召喚の同キー/別技能/R初期化順の実値、および子Rが実際に増えたケースに限った決着前後の親EXP対照。吸収の動的試験は合法な攻撃技能・到達条件が先に特定できることを前提とする。
- 原作EXE/DAT/セーブの実行・変更0、他owner/MASTER/Work/製品/Git更新0、原作Gameplay試験0。新規ZIP0。今回の確認結果だけで旧進捗%やREADYを引き上げていない。
- RECOVERY EXP-RC-20261022-CONTAINER-PROBE-04は環境ClientErrorのまま。PCの独立記録は保存できているが、この回のsandbox複製は未実施。ダウンロードリンクを捏造しない。

## RECOVERY EXP-RC-20261022-05-NATIVE-AUDIT-WRITE / 当時BLOCKED→CP21で復旧済み
- 現在は同じ元パスへ通常保存・静的照合・独立再読まで完了。以下は初回失敗時の履歴であり、最新状態は末尾USER-REQUESTED RETRY節および研究本文CP21を参照。
- 対象: EXP-GATES-NUMERIC-20261022-05の新しい原本照合スクリプト exp_gates_numeric_audit_20261022_05.py。
- 試行: Local write_fileで最初の29行を書き込む操作。結果: OpenAI安全性チェックで拒否。理由の詳細はUNKNOWN。
- 直後のget_file_infoはENOENT。スクリプト未作成、対応する証拠JSONも未作成。分割変更・別tool・別shell・別pathで同payload/同保存操作を再投入しない。
- 既存の独立成果: exp_numeric_model_20261022_05.pyは別に保存済み。最初に21件の未実装エラーを確認後、モデルを実装して21テストPASS。ゲーム実行試験ではない。
- 保存済みCP16: +0x18614初期条件、Troop+0x1F上書き、castle_guard/handle/redへの接続候補、原作DAT直接指定数、既存live captureのEXP bytes不足。
- 未完了: 上記native siteとDAT/live receiptを新規の構造化JSONへまとめる自動照合・独立再読。今回の機械語表示はチャットにあるが新JSONに保存済みとは主張しない。
- 次の許可された作業: 既存モデルの再実行・既存文書の独立要約と状態記録。拒否された新規スクリプトの保存は許可条件変更/審査まで保留。原本・他owner・製品コード変更0。

## RECOVERY EXP-RC-20261022-05-NATIVE-AUDIT-WRITE / USER-REQUESTED RETRY
- ユーザーが同じ検証器の再作成・保存を明示依頼。Local write_fileで同じ元パスへ通常の保存を再試行し、今回は成功。設定変更・別toolへの迂回なし。
- 旧拒否payload全文は保存されていなかったため、既存CP16～20の記名siteに基づき読取専用の検証器を再構成した。同一バイトの再送ではない。
- exp_gates_numeric_audit_20261022_05.pyを実行。34 native site / 6 double / 1 control word / 10関数SHA / 590 DATの照合PASS。
- EXP_GATES_NUMERIC_AUDIT_20261022_05.json SHA256=C57DC8DDDB54FB5C4512EE5322A219475E76D3EA5EA99CDEFAC5E224E9371C97を生成。新ゲーム実行0。live RAWのcoverage集計はこのJSONには含まない。
- 旧BLOCKEDは履歴として保持し、今回の対象スクリプトはSAVED_AND_STATIC_CHECKEDへ更新。他の過去拒否案件を一括解除した意味ではない。
- 付随環境確認: container.execによるライブラリ・/mnt/data確認がClientError。PC成果の未保存とは別。サンドボックス添付は今回未確認、同環境での反復はしない。

## EXP-HITINPUTS-20261022-06 / 2026-10-22 03:10 JST 最終チェックポイント
- CP21～CP25を既存本文へ保存。本文SHA256=7C705A8FC1846507E8FA4903AEA2BEA08D00D0234FFF14BF456545607138D73F。索引の先頭を最新06へ更新し、05当時の未保存表示へ復旧済みを明記。
- 前回05の34site等を復旧・別処理から再読。新規06は35native/5関数SHA/4文字列/9DAT原文を独立replayしてPASS。証拠SHA256=4D8A2605CB4BFF291AFA5A91BDC61D1D8144F652C37BB7CAA385D596EBC96B3C。
- 計算モデル21/21再実行PASS。ゲーム実行0/実測Golden0/新旧互換PASS0。原本EXE/V3 DB/DAT archiveの前後SHA不変、他owner/MASTER/Work/製品/Git変更0。ZIP追加0。
- RECOVERY EXP-RC-20261022-06-DAT-CRLF / RECOVERED: 最初の探索regexがCRLF未対応でヘッダ1件しか拾わず目的0件だった。原文改行を検査して原因確定、検索側で改行正規化後16,554ヘッダ/目的9定義へ復旧。原文無変更、初回0件を仕様の不存在とは扱わない。
- PC成果は保存済み。任意sandboxコピー用のcontainer環境はClientErrorのため未使用継続、架空リンクは出さない。
- 次: 原作の対象選別/全弾・全対象でのcontext生成resetとEXPの関係、召喚Rの実増分がある例の決着前後比較。今回のHP処理とEXP入力の分離を、全モードや全技能の挙動へ無条件に一般化しない。
