# EXP AI Research Index | 迫真戦記 ver0.67 経験値共有入口

## 最新｜EXP-HITINPUTS-20261022-06：保存復旧・HP変更量とEXP入力の分離
- 本文は既存 `EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md` のCP21～CP25。ZIP追加なし。
- **前回の保存失敗は復旧済み。** ユーザーの再作成依頼を受け同じLocal write_file/同じ元パスで通常保存に成功。`exp_gates_numeric_audit_20261022_05.py` と証拠JSONを作成し、34命令/定数/10関数SHA/590 DATを照合。別collectorで1,972直接設定行まで再読PASS。
- **攻撃:** HP callbackへ渡すECXとEXP分子EDIは別。HP側の最低値・特殊補正、残HPで切り詰めた有効量をEXPへそのまま流用しない。分母はcallback後のUnitData+0x178。
- **回復:** 上限超過分は別に管理し、EXPへは元量を渡す。func=healは固定2%枝。add_allの同一contextでは処理済みflagを共有するため、項目数をそのまま獲得回数としない。
- **原作例:** 限定DAT探索で複数項目回復9定義、うち7定義は明示exp_per=off。残り2定義は継承・実使用未確定。満タン回復の実発動・経験値稼ぎを証明しない。
- 証拠 `EXP_HIT_INPUTS_AUDIT_20261022_06.json`、再読 `EXP_HIT_INPUTS_REPLAY_20261022_06.json`：35命令/5関数SHA/4文字列/9原文再照合PASS。旧計算モデル21/21再実行PASS。ゲーム実測0、原本/DB/archive前後SHA不変。

## 履歴｜EXP-GATES-NUMERIC-20261022-05：獲得禁止条件・丸め・上限
- 本文は既存 `EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md` のCP16～CP20。ZIPは追加しない。
- CP17: 基礎値を先に切上げ→明示exp_per倍率→0.5加算/整数化。1回だけ丸める簡略式との差を合成例で確認。レベル上限判定は共通EXP加算より後。
- CP18: 閾値再計算の条件は低下だけでなく等号を含む。累積閾値の飽和と獲得EXPの32bit加算は異なる処理。
- CP19: +0x18614の初期設定とTroop+0x1Fによる上書き、castle_guard/handle/red生成枝を追跡。MODの直接castle_guard指定は今回未検出。
- `exp_numeric_model_20261022_05.py`: 計算部分の合成21テストPASS。原作実行やbit完全互換の証明ではない。
- 保存済み原作live RAW8件はEXP数値未収録、今回の範囲で共有pointer例も未検出。非atomic資料の限界を明記。
- **当時未保存→CP21で復旧済み:** 初回write拒否とENOENTは履歴として保持。ユーザーの再作成依頼後、同じ通常保存でスクリプト/JSONを作成し独立再照合まで完了。`EXP_RESUME_20261021.md` の同じ復旧ID末尾を参照。
- 当回時点はSTATIC_INSPECTED＋SYNTHETIC_TESTED。CP21で対象部分のSTATIC_NATIVE_REPLAYを追加したが、原作Golden・正式READYへの昇格ではない。

## 履歴｜EXP-SETTLEMENT-20261022-04：共有キー・初期化skip・吸収順序の訂正
- 本文は既存 `EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md` のCP08～CP15へ追記。新しい本文/ZIPを増やさず、CP06の誤解を招く説明も訂正した。
- **優先して読む訂正:** CP09/CP12。回復側の吸収helperはEAX=0。正の強度を渡す攻撃側では通常EXP判定→吸収の順。SimpleUnitの終了判定除外との関係を条件付きで整理。
- **MOD適用範囲:** CP15。590 DATの限定source探索でdrain直接指定13宣言と子孫9宣言はstatus系。正のEXP吸収を行う実使用攻撃技能は未特定。エンジン内の機能を原作MODの確定不具合として扱わない。
- **実使用召喚:** CP10/CP11。キーはadd/add2の召喚先。原作のa004_s重複指定を確認。同じ生存中owner/keyでhitなら同じRを返し、親Lv×召喚倍率の初期化枝を飛ばす。異なる技能IDだから別Rとは限らない。
- **結果処理:** CP13。通常型のレベル確定は自己の+1C8先を更新。結果rootからEXP初期化へ進む候補は中立兵生成と判別。一般的な親還元の有無は未確定。
- 証拠 `EXP_SETTLEMENT_OWNER_AUDIT_20261022_04.json` と独立 `EXP_SETTLEMENT_OWNER_REPLAY_20261022_04.json`：原本61命令/9文字列/3vtable・16関数SHA・4DAT例を再照合PASS。
- `EXP_DRAIN_DAT_USAGE_20261022_04.json`：限定parserの範囲と13＋9宣言、親4宣言を保存。26sourceの原文/SHA読み戻しPASS。完全DAT互換解析ではない。
- 原作実行0、実機Golden0。EXE/現行V3 DB/DAT archiveは前後SHA一致。PC正本への独立研究保存のみ、他owner/MASTER/Work/製品/Git不変更。

## 履歴｜EXP-ENDTRANSFER-20261022-03：召喚EXPの獲得条件と通常・簡易の差
- 本文: `EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md`。yorozuのtroop/troop2/troop3→通常召喚の部隊設定、簡易2経路の子Troop=NULL、召喚者への独立した発動EXP、配置失敗枝と吸収の例外を整理。
- `EXP_SUMMON_GATES_EVIDENCE_20261022.json`: 原本41site/5文字列/kind4固定1%/590 DAT。85は直接設定行数であり継承後の技能数ではない。
- `EXP_ENDTRANSFER_VALIDATION_20261022.json`: 独立再読PASS、吸収順序の追加3site、SimpleUnit除去のvirtual slotも確認。
- `EXP_TRANSFER_NATIVE_CENSUS_20261022.json`: 595,450命令の限定走査、該当offset151一致。別型・間接別名・除外範囲を含むため全EXP writer証明とはしない。
- 最新CLIは作業中にV3へ更新。根拠は原本PEと記名snapshotを固定し、対象7関数のV2/V3擬似C一致を確認。新規研究はsearch_current.pyの現行DBを先に確認する。
- 重要: 子の通常EXP不成立と親の召喚発動EXPは別。後続Troop変更やdrain等を含め全経験値を0と断定しない。終了時の一般的な親還元は未確定。原作実行・製品変更・ZIP作成なし。


## 履歴｜EXP-SIMPLE-LIFECYCLE-20261022-02
- 本文: `EXP_SIMPLEBATTLE_LIFECYCLE_20261022.md`。簡易戦闘の生成→個体更新→近接/回復→共通EXP加算、登録済みUnitDataへの直接参照、結果処理→2陣営cleanup→召喚R破棄を条件付きSTATICで接続。
- 返値0は決着未確定。1呼出し最大500内部反復/50反復周期の判定を、戦闘終了や実時間と混同しない。
- 証拠: `EXP_SIMPLEBATTLE_LIFECYCLE_EVIDENCE_20261022.json`（直接CALL21/vtable8/原本命令32）。独立再読: `EXP_SIMPLEBATTLE_LIFECYCLE_VALIDATION_20261022.json`（61再確認＋追加命令9＋アドレス同値4）。ゲーム実行試験0。
- 再現: `exp_simplebattle_lifecycle_probe_20261022.py`（既出力上書き拒否）、`verify_exp_simplebattle_lifecycle_20261022.py`（再検査可・既検証結果との差異なら停止）。
- 新規調査の検索正本は `../rea_lab/headless_analysis/search_index/search_current.py` と `HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite`。下の旧search.sqliteは歴史的証拠であり新規参照の第一選択ではない。
- 残りP0: 破棄より前の0x493630/下位イベント内で召喚EXP転送があるか、全CPUモード/遠距離などの分岐、原作実機比較。EXP消滅や完全互換は未確定。ZIP更新なし。


## 2026-10-22の最新研究（ZIPは不要）
- `EXP_RESEARCH_PROGRESS_20261022.md`：8領域の達成度・残り約8～10テーマ。進捗%は主観的スコープ評価、ゲーム再現率とは別。
- `EXP_TYPED_OFFSET_CENSUS_20261022.md`：`+0x16C` 32関数/56行の型別候補整理。数値上の同一offset≠経験値。旧安全拒否対象0x5710C0本文は除外。
- `EXP_SUMMON_DESTRUCTOR_NORMAL_VTABLE_20261022.md`：0x56F880が設定するvtable[0] = 0x570C90→0x543E00→召喚R木解放。実戦闘終了での呼出時刻は未解決。
- `EXP_WRITER_CENSUS_20261022.json`：検索DB実SHA一致、32関数/56行、左辺候補26（Unit EXP writerと同一視禁止）。
- `EXP_SUMMON_DESTRUCTOR_VTABLE_20261022.json`：原本PE native7/7 +直接CALL4/4、vtable entry検証PASS。
- `EXP_UNIT_VTABLE_WRITER_SCAN_20261022.json`：コンストラクタ1,121命令内、`[EBP]`直書きは0x56F8DDの1件。
- `EXP_20261022_VERIFY_ONLY.py`：4 JSON＋3 Markdownをread-onlyで再監査 PASS。原本実機golden 0、正式B READY0、E統合0。



**最新研究（2026-10-21）:** ZIPではなく下記のMarkdown・JSONを直接参照してください。以前のZIPは古いスナップショットとして保管しているだけで、今回新規作成・更新していません。

- **最新A:** `EXP_CACHE_STRING_KEY_RECORD_ABI_20261021.md` — 召喚キャッシュは文字列キーで比較。Skill+0x13Cは固定文字列、+0x14Cはその長さ、+0x158は候補一覧。ノードは0x200byte、UnitData埋込は0x1D4byte。0x577260 ret0x1C、0x577310はEAX=R/ret0x1D4。
- **最新B:** `EXP_SAVE_TREE_POINTER_VS_INLINE_20261021.md` — 保存側root+0x300のnode+0x28はUnitData*、召喚Rのnode+0x28は埋込みUnitData。EXP転送の有無は未解決。
- **機械証拠:** `EXP_STRING_CACHE_ABI_EVIDENCE_20261021.json`（原本native39/39 PASS）、`EXP_SAVE_TREE_BOUNDARY_EVIDENCE_20261021.json`（native10/10 PASS・SAVE writer直接caller1件一致）。
- **再現コード:** `EXP_STRING_CACHE_ABI_VALIDATE_20261021.py`、`EXP_SAVE_TREE_BOUNDARY_VALIDATE_20261021.py`（元EXE・DBを読取専用、既出力の上書き拒否）。
- **状態:** STATIC/VERIFY/NOT READY。ゲーム実行によるGolden PASS=0。正式B READY・E MASTER統合・Task DONEは追加0。安全拒否済み範囲の新規解析は中止。



Research ID: `EXP-COLLAB-20261021-2112-01` / Status: `STATIC_VERIFIED_INDEX / VERIFY / NOT READY / GAMEPLAY NOT RUN`
原本識別: SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
SQLite: `../rea_lab/headless_analysis/search_index/search.sqlite`; SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`

## 最初に読む資料
1. `EXP_COLLAB_HANDOFF_20261021.md`: 目的、正本担当、既知、禁止境界、再開位置。
2. `EXP_CACHED_RECORD_LIFETIME_20261021.md`: Rのnode+0x28と破棄連鎖の**既存CP12再検証**（新発見と二重計上禁止）。
3. `EXP_THREE_PRODUCER_CROSSJOIN_20261021.md`: 3producer×4CALLの横断表、共有キー未特定。
4. `EXP_AI_EVIDENCE_20261021.json`: 26関数のコードハッシュ、該当行、直接caller/callee、32個の+0x16C文字列hitの型候補、8CALL照合。自動生成。
5. `EXP_THREE_PRODUCER_CALLS_20261021.json`: 3producer×4段階=12直接CALLの読み取り専用索引によるPASS記録。
6. `EXP_BUILD_AI_EVIDENCE_20261021.py`, `EXP_VALIDATE_PRODUCER_PATHS_20261021.py`: 上記JSONの再現可能な生成・検証器。既存DB不変。
7. `EXP_RESUME_20261021.md`: 研究再開条件／観測すべき原作Golden。

## 先行の正式資料（参照のみ・本研究で改変なし）
- `../MASTER_LEDGER.md`: 正本、研究Eのみ更新可。
- `../evidence/LANE_B_HANDOFF.md`: B所有、既存STATIC/VERIFYや拒否復旧IDを参照。
- `../evidence/ANALYSIS_LANES_PROTOCOL.md`: 所有権／safe writeルール。
- `../dev_lab/docs/WORK_REQUEST_QUEUE.md`: Work管理、今回read-only。
- `../rea_lab/headless_analysis/search_index/P0_SUMMON_EXP_OWNER_REPORT_20261021.md`: 召喚R生成・+0x1C8結合・EXP writerの既証明。
- `../rea_lab/headless_analysis/search_index/EXP_SUMMON_DEATH_RESEARCH_20261021.md`: EXP add/drain/deathの既存機械解析。
- `../data/T011_LEVELUP_11FIELD_RECALC_CACHE_GATE_20261021_17H.md`: B所有・LvUP再計算。
- `EXP_SUMMON_OWNER_RESEARCH.md`: 既存独立研究。既拒否草稿の保存部分を正本としない。

## この研究での進捗を誤読しないこと
- 3 producer × 4 callsites の12 site、および8 core edgesと26関数SHAを検証。これらは **STATIC索引検証数** で、旧EXE Gameplay PASSでも新旧互換PASSでもない。
- 32件は文字列 `0x16C` を含む全関数件数。32件のEXP writerを発見した意味ではない。
- PC E MASTER正式統合追加0、B READY追加0、Task DONE追加0、原作実機Goldens0。
- 原本EXE/DAT/SAVE、既存B/E/Work正本、他レーン資料、Git/push、拒否済み内容は変更・再提出なし。
- **ファイル保存は他チャットへのリアルタイム通知ではない**。別AIはこの絶対フォルダを直接開き、出典のSHAを照合する。オフライン用ZIPは同フォルダに生成予定、manifestに格納する。

## CP03 増分（種別4の上位ディスパッチ）
- `EXP_KIND4_DISPATCH_PRODUCERS_20261021.md`: 0x545CC0 switch Skill+0x40 case4→0x547490、および0x552EF0 Skill+0x40==4→0x553390。後者はSkill+0x74反復制御も記録。
- `EXP_KIND4_DISPATCH_EVIDENCE_20261021.json`: ソース擬似C条件6/6＋2直接CALL、関数コードSHA2/2 PASS。実機到達・真の共有keyはVERIFY。
- `EXP_VALIDATE_KIND4_DISPATCH_20261021.py`: 上記2入口の機械的再現手順。研究CP02のproducer 3件12siteとは異なる上位入口の証拠。
