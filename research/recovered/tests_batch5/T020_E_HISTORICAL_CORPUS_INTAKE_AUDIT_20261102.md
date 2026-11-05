# E/T018・T019・T020｜旧研究のGitHub保全監査（2026-11-02 JST）
記録ID: E-RECOVERY-20261102-HISTORIC-E-193-SHA-INTAKE-01
所有者: E / T018,T019,T020。状態: PUBLISHED_INTAKE / NOT_CURATED / STATIC-SOURCE-RECEIPT / VERIFY / NOT READY。
目的: 過去成果の研究ID・原文ハッシュ・参照先と後続curatorの意味審査を一対一で結ぶ。ゲーム原作の実測でも正式READY統合でもない。

## 読取出典・実測
- PRIVATE GitHub正本: ButaMonky/Hakushin067-Research-Knowledge develop。研究目録 RESEARCH_SOURCE_CATALOG.tsv (監査スナップショット)。README、RESEARCH_INTAKE_PROTOCOL、KNOWLEDGE_CURATION_PROTOCOL、SYNC_STATUSを参照。
- PC正本: 00_START_HERE.md、MASTER_LEDGER.md、ANALYSIS_LANES_PROTOCOL.md、E所有T018/T019/T020と、他owner HANDOFF必要部分。PC元ファイルのSHAをGet-FileHash SHA256で実測。
- 旧E研究レポート: 2026-10-20～27/10-30～31早朝 147件 + 2026-10-28～29 46件、計193個の異なるresearch_id。PC実体とdevelop source目録 SHA256一致193/193、同ID重複0。
- 10/28旧E OFFLINE_UNSYNCEDとE_OFFLINE_SYNCの同一byte鏡像6件は別研究に数えない。拒否済みの10/28 13Hの原本操作・未実行/失敗資料をコピーしない。
- tests以下のT018/T019/T020接頭辞MDファイル231件を確認し、develop source catalog掲載227件、未掲載4件はE curator delta1件/入庫受領記録3件（新規native研究ではない）。他領域/巨大資料の網羅とは異なる。

## GitHub保存と読み戻し
- 既存Draft PR #17 https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/17
- owner分離branch intake/E-20261102-0049-t020-17h23h、監査時head 348bff919b2f94e5ebf99a272199606edd2c8ecb、OPEN/DRAFT。
- 既存15 IDに対し193 IDを9件のcrosswalk MDへ収録。元研究ID・相対path・PC実測SHA256・出典行・要点を保全。全文MD/Python/JSONすべてのGitHub複製とは主張しない。
- research/intake/E/E-SOURCE-RECEIPT-INDEX-193-20261102.tsv: 193個のID/相対path/SHA/byte数/横断資料。PC元資料SHA193/193とGitHub読戻し照合済み。
- research/intake/E/INDEX.mdに横断9資料と旧PR #8/#11/#14/#17の入口を作成。全9横断本文のIDとTSV193行を照合して欠落0、追加0、重複0。資料はGitHub全文読戻し一致。
- PR #17に累計208異なるE研究ID。別E Draft PRは#8 6件、#11 6件、#14 8件。合計ステージ済228件（curator未採録）；GitHub develop catalogにあるE11/1 17～20H資料は重複計上しない。
- PR説明はこの件数・今後のcorrections/未採録境界で更新、GitHub側から再取得済。PR #17は非force通常commitだけで、developへmerge/pushしていない。

## 判定・禁止・再開
- MASTER公式最終確認値 checkpoint196、READY596 (A115/B229/C136/D116)。34 Task DONE9/IN_PROGRESS21/VERIFY4は過去確認値で今回全履歴再判定なし。今回MASTER変更0、新規正式READY0。
- 同一合法原作戦闘のG0 UI/実Spot、G1直前SAVE bytes・入力系列、G2実MAP・三陣営・Unit/Troop順序の一次証拠未結合。E DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2は字句検索scope差RESOLVED。script2優先/TXT実読込/phase flag/gwrite後続VERIFY。
- 旧安全拒否のT018表境界、E旧拒否、C T026/T032、D T030、保護VA、B HOLD21、10/25未回収などは解除しない。禁止操作/証拠を別ツール/パス等で取得せず、E以外の所有資料や原本EXE/DAT/MAP/SAVE/ZIP、共有KB、Git develop、Work、scheduleは変更していない。
- 未完了: 193の短縮引用に対するcuratorのsemantic dedup/訂正/原文比較、別owner本拠証拠との一致、元Python/JSON/映像等の正式適格性、MASTER以前の大型インライン履歴/未索引データの完全保全。
- 次の正当な一手: curatorがPR #17のINDEX/193 TSVを入口に、原本SHAと同ID・訂正関係・参照行を審査後、意味差分をREF/dictionaryへ採録。E側は合法G0/G1/G2一次証拠とT019未解決を別研究で継続。
[CURATOR_CONCURRENT_UPDATE E-CURATOR-RACE-20261102-PR17-DEVELOP-ADVANCED-01] 出典: GitHub PRIVATE develop latest 782d5b6add9907e3739b2bc43b8b595f516e9ccf。PR#17 head 348bff919b2f94e5ebf99a272199606edd2c8ecb はdevelop比較ahead24/behind4/status diverged。専任curatorが並行更新したため、Eはrebase/reset/force/mergeせずPRをOPEN/DRAFT/NOT_CURATEDで保全。PR本文にこの競合・再確認条件を追記しGitHubで読戻し。必要な正当な次の一手はcuratorの原資料ID/訂正/SHA差分比較と安全なff-only統合可否判定。

## E-FOLLOWUP-20261102-CITATION361-VA804-PLAYBOOK｜新たなGitHub成果・採録待ち切分け
- PRIVATE GitHub E owner Draft PR#17のresearch/intake/E/で保全済み193研究IDの9資料から、source行番号最初/最後の計361短縮引用を抽出。Local Compactにより各PC E原資料をread-onlyでUTF8直接読込み、行番号/正規化接頭部を361/361一致検証。全文全行の意味監査ではなく限定的な証跡一致。
- E-VA-MENTION-INDEX-20261102.tsvを混在SHA heading対応で修正し、193 IDのヘッダ検出、参照804行、VA549種類、対象研究ID89件。8? 未確認ではなくGitHub READBACK 804/804の7列/SHA64 hexを確認。全参照はMENTION_ONLY_VERIFY、保護アドレス除外、native関数/READYの新確定なし。
- E-CNB02-GOLDEN-EVIDENCE-ACCEPTANCE-PLAYBOOK-20261102.mdをE専用隔離branchに追加。E G0通常UI/Spot、G1同run直前SAVE+入力、G2実MAP/三side/ordered Unit/Troop、G3終戦、G4Worldを独立区分し、saveとUIの合法時系列未確認、跨PID/同PID別戦闘混同、auto.sav同名別SHA、591/590 DAT source epoch、pixel-only comparatorの誤認を禁止。
- E-PR17-CITATION-AND-CURATOR-RECONCILIATION-20261102.mdでE研究193の原SHA/引用QAとcurator向け審査順序を記録、GitHub readback確認。INDEX.mdから上記3資料へリンク済。
- 同期照合観測: PRIVATE develop 782d5b6add9907e3739b2bc43b8b595f516e9ccf時点のE intakeの17パスがPR#17とGitHub実ファイルbyte/Blob SHA 17/17同一。うち193研究IDのOct28-29 part1 23 IDはdevelopに既に安全入庫されたため、PR#17残り170歴史IDは取り込み候補だが意味的CURATEDではない。
- 現行PR#17はdevelopとdiverged。Eはrebase/reset/merge/forceを実施せず専任curatorへ適格ファイル/厳密owner sourceの審査を依頼。他owner/原本/共有KB/MASTER/Work/scheduleは変更なし。
- STATUS: E DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0、新規正式READY0。旧MASTER cp196、README分類DONE9/IN_PROGRESS21/VERIFY4は最後の確定値であり今回の再集計ではない。
- NEXT: PC Eテスト用Python/JSONの未保全証拠を安全なmetadataだけでinventorizeし、GitHubで検索可能にする。実原作同run G0/G1/G2の一次証拠が無い間は合成モデルだけで互換認定しない。

## E-FOLLOWUP-20261102-REPRO337-SHA804-GOLDEN-PLAYBOOK-01｜E研究再利用性・出典検証の続行
- Github E Draft PR#17 (intake/E-20261102-0049-t020-17h23h) にT018/T020 Golden G0–G4統合受入プレイブックを公開、原本E研究10資料とT019正本をPC独立SHAで再照合。元EXE/SAVEの実測やGolden昇格なし。
- 旧193 E研究の9概要から、引用のPC原本参照行を361/361 sample一致確認。SHA193/193は先行値で今回全件hash再実行ではない。異なるSource SHA見出しを修正したVA検索TSVは804参照/549 VA/89 ID、193原本SHA/各概要ルートとのmetadata照合804/804一致。VAはMENTION_ONLYでnative確定ではない。
- PC E tests直下のt020_/T020_/T018_ .py/.json合計340ファイル（Python170/JSON170）をメタデータ棚卸し。LIVE関連2ファイルと旧Stage15関連1ファイルは安全優先で除外。実ファイルSHAを確認した337件（Python168/JSON169、総4,711,598B）の相対path/サイズ/SHAのみGitHubへ保存して直接readback。コード/JSON本体はコピーせず実行せず、TEST PASS0新規。
- 現行KB develop 782d5b6a時点とPR#17は同名17ファイルのGit blob SHA/全文が17/17一致。その内Oct28–29 part1 23 IDは既にdevelop intakeに安全保全済み。193中branch-only候補170、正式REF採録は専任curatorだけ。PRがdivergedのためrebase/reset/force/mergeは一切行わず。
- E所有PR#17のINDEX/PR本文へ研究索引、Golden playbook、source QA、VA/テスト資産索引へのリンクと未採録・誤解しやすい証拠境界を追記しGitHub読戻し済み。
- 追加でB最新HANDOFFをread-only確認。B 2026-11-02の新研究はPUBLISHED_INTAKE/NOT_CURATED、新READY0。A/C/D停止中の過去READYはMASTER既存採録対象と混同せず、今回はMASTER書込0。
- G0旧合法UI/Spot＋G1同run直前SAVE/input＋G2実MAP/三側・出撃の同run一次receiptは依然未取得。E DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0、新正式READY0。T019新規矛盾0。
- 保存済みに含めない: 原本EXE/DAT/MAP/SAVE/ZIP、全文Python/JSON、生成SQLite、保護VA・旧拒否元証拠、他ownerの原文。次はcuratorがbranch-only170 IDの意味/訂正/秘密/根拠を審査。Eの次優先は合法原作G0–G2実測が新たに現存するか差分だけ確認。


## E-FOLLOWUP-20261102-03H-G1G2-REPRO-QA（旧研究IDの再現性確認・追加IDなし）
- 既存Eの2研究ID（2026-10-25 16H G1 chronology / 2026-10-26 10H G2 parity）を最優先再確認。PC原報告SHA256 `230D52901E317BFD0AB08E20027CEC26750658578C7EA29467852004F81F66DF` / `0584365A103610A04ACAA08923AF2CC864ACB6537EE3F677F31ED78107BFC4BB` を2026-11-02 03Hに実ファイルから再計算、一致。
- E専用synthetic Python 5本をPCからSHA再計算し、`python -B` 個別実行: G1 18/18、G2依存11H 15/15・08H 14/14・09H 12/12・10H 14/14。合計73/73 PASS、各exit0、原作のゲーム実行・native GoldenはNOT RUN。
- 10H G2修正は以前の11Hと08/09Hの診断差（sideラベル型不正、map placeholder表記ゆれ）を再現した合成警告補完。原作MAP・3陣営・ordered Unit/Troop・同一run一次根拠なし、G0/G1/G2=NOT QUALIFIED、DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- PRIVATE owner Draft PR #17を再利用。既存`research/intake/E/E-PR17-CITATION-AND-CURATOR-RECONCILIATION-20261102.md`に新§6を通常commit `f131f610ec621cebb9c17fa2caef261525877579`、既存`research/intake/E/E-T020-REPRO-ASSET-RECEIPTS-20261102.tsv`の5件だけをSHA実測・synthetic実行ステータスへ変更 `790d43f3b3e19e68d7ac80d9a190597c73aacbbe`。両ファイルGitHub HEADでreadback、SHA一致。新研究ID0・新PR0・CURATED昇格0。
- GitHub develop最終観測 `0e076eb6c6b22768e1f1636082a6a35f93b513c5`。PR #17比較はahead34/behind5/diverged。curator側の追加1commitはREF_BATTLE_AI_MORALE / SOURCE_MANIFEST / intake READMEのみで、Eの過去193 source mapの新規文面統合と混同しない。ownerはrebase/reset/forceせずdevelop変更0。
- PC `knowledge` checked-out branchは`work/kb-KB-SAVELOAD-20261101`、SHA `a7a7bc300e97429fc58e4c7bfc3eaa311a430e15` と読取確認、切替・書込0。MASTER現行の最後の確定checkpoint196/READY596(A115 B229 C136 D116)、34Task 9/21/4は旧値であり今回再集計・MASTER正式変更0。T019新規確定矛盾0、GameClear字句scope RESOLVED/loader等VERIFY。
- 未回収/次カーソル: E PR#17に含まれる旧193研究IDのうち23が過去develop同一blob、残170 ID/8 crosswalkはcuratorの意味・訂正・元source QA待ち（この数は上記E source-only比較スナップショット）。337 synthetic asset metadata中5スクリプトのみSHA+実行済、他は未検証/コード未収録。G0同一run合法UI+Spot、G1直前SAVE byte+入力、G2実MAP+3陣営+ordered Unit/Troop入手までGoldenを昇格しない。旧拒否・保護VA・A/B/C/D/REA/P0には介入しない。

[E-ALL-QUOTE-20261102-795-OUT-OF-795-VALID-01] 2026-11-02。Eのみの旧193研究ID/9 crosswalk（GitHub owner-private PR#17）の全L行短縮引用をGitHub全文から抽出し、Local CompactでPC E原資料UTF-8該当行を直接読取照合。第一段階361件に続き、全引用795/795件一致、ソース不在0、行不一致0。内訳207+195+145+141+107。元source SHA193/193は前回のbyte一致実測、VA参照804/804も別metadata照合済。PR#17 INDEXと品質審査報告に結果追記・GitHub直接readback。これは引用出典真正性の検証で、全意味論/原作実機/元テスト再実行ではない。DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0、新正式READY0。旧拒否・原本・他owner・共有KB・MASTER・schedule不変。Curatorの意味的重複/訂正/REF正式採録は継続未完。


## 2026-11-02 E existing-ID source-detail preservation / PR #17 readback
- Priority delta before write: PRIVATE `develop` observed at `68de6a28d1a5ec739027f4e25e0e67d95f2e8b40`; eight of the E 193-ID historic crosswalk source files absent from develop, one earlier part1 present (170 branch-only IDs at this scoped file-level comparison). This is not a full semantic CURATED ID recount. Knowledge main worktree is `work/kb-KB-SAVELOAD-20261101` and was not switched.
- Three **existing** E source IDs received substantive, sanitized owner-detail notes on the EXISTING PRIVATE Draft PR #17 (`intake/E-20261102-0049-t020-17h23h`), not new IDs or PRs: `E-AUDIT-20261024-22H-ARCHIVE-DAT-SOURCE-DRIFT-01`, `E-AUDIT-20261025-15H-T018-T020-G1-CLICK-SAVE-ORDER-RECONCILIATION-01`, `E-AUDIT-20261026-1350-T018-T020-G2-PLACEHOLDER-IDENTITY-01`.
- Their 2026-11-02 **actual PC owner-report SHA256** matched the existing 193 source index, respectively `2AAB084BA4CFBB9AFF9C4471F8A9F5ADE827005272D19AB34B2608CD72ADFD48`, `36CF7421B927AB785160C9BC3BB3402E7A550B5530145BA62819ADCB0B845B86`, `23F1C78F6BBA3B705D695522F57771B8B252D2258F4C010818018BD6DC90FFC4`. Original ZIP/DAT, historic offline synthetic runners and actual game were NOT rehashed/replayed.
- New GitHub owner-only content commits `d443a2b5` (archive/source-membership), `bcef7c5f` (G0/G1 chronology), `3375d1a6` (G2 placeholders); existing E `research/intake/E/INDEX.md` linked those notes in `d399426b75d211b1341adc17e41a1ec73d753501`. All four files fetched from PR #17 head; ID/report SHA and index links verified, PRIVATE OPEN/DRAFT. Final PR head `d399426b75d211b1341adc17e41a1ec73d753501`. Develop/head diverged (ahead40/behind8), no merge/rebase/reset/force.
- Stage: **3 existing IDs now have fuller PUBLISHED_INTAKE research body, NOT CURATED**, ID delta=0, formal READY delta=0, E original-game DYNAMIC/Golden PASS/strict MATCH=0. MASTER official checkpoint196/READY596 and 34-task 9/21/4 remain prior timestamps, **MASTER unchanged**; T019 original game bug delta 0.
- NEXT: Curator reviews 170 branch-only E historic IDs / eight crosswalk files and these three correction/eligibility notes against current `develop`; no direct E REF/dictionary/develop changes. E next source cursor: remaining old T018/T019/T020 full owner notes whose meaning is only abbreviated in the 193 crosswalk, prioritizing clear rule differences over repeated synthetic PASS. Legal same-run original G0 UI/Spot, G1 immediate SAVE/input, G2 true MAP/3 side/ordered Unit–Troop are still missing. Previous safety denials and protected region remain BLOCKED, no alternate route attempted.
