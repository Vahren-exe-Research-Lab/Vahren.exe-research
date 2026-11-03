> **2026-11-03 E owner intake / sanitized Library source.** Existing research ID `E-OFFLINE-20261101-08H-T018-T020-CALLER-TEMPORAL-IDENTITY-01`. Original Library file `T018_T020_CALLER_TEMPORAL_IDENTITY_AUDIT_20261101_08h.md`; actual raw Library SHA-256 `1688171315BDB14A1487443E476E66E23A8A839983CEE405205AC1CF5F029451` measured 2026-11-03. Original research PC `tests/` same-named report absent on the current authorized PC; PC↔Library SHA equivalence is **not** claimed. The archived text below is historical synthetic/static analysis and its older PC-unavailable statements describe the 2026-11-01 authoring snapshot, not this intake run. 1 line(s) referring to pre-existing protected/refusal scope or sensitive absolute paths omitted; none was used to recover denied material. Git blob is a **sanitized derivative**, not byte-identical to the Library source. No original game was executed; Golden PASS 0, strict MATCH 0, new READY 0, MASTER formal delta 0. **PUBLISHED_INTAKE / VERIFY / NOT_CURATED.**

# 迫真戦記・新E｜T018/T020 caller別戻り値と候補Unit世代の時系列照合（08時台）

- 研究ID: `E-OFFLINE-20261101-08H-T018-T020-CALLER-TEMPORAL-IDENTITY-01`
- owner: E、task: T018/T020。記録スナップショット: 2026-11-01 08時台 JST。
- 状態: **OFFLINE-UNSYNCED / PREVIOUS STATIC EVIDENCE / CONDITIONAL SYNTHETIC EXECUTED / VERIFY / NOT READY**。
- 今回の成果は比較器の**合成仕様**の差分であり、原作機械語や原作ゲームの新規実測ではない。`DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0`。

## 出典・重複確認

- Desktop Commander Local Compactの `MASTER_LEDGER.md` read_file は `McpServerError: Session terminated`。接続障害であり安全拒否ではない。PC最新MASTER/owner/REA/dev_lab/ローカルV9は**未確認**。
- Libraryの前回E所有 `T020_CANDIDATE_IDENTITY_AUDIT_20261101_0745.md` を取得・読取。SHA256 `4BAF63C7636D17145CC3D2B2A3F3FCDB3EB75D52732FF9FC94CAF70653060227`。前回が `0x4E53B0` の3 caller `0x545A02`, `0x57AD8C`, `0x57D982`、Unit+`0x1E570`の32bit保存と第三callerの0/非0判定を静的に照合済み。この発見を再計上しない。
- Library旧E `T020_GOLDEN_CAPTURE_SEMANTIC_BINDING_AUDIT_20261028_2149.md` SHA256 `D46C9DEF81CA661559717EE274D3782B97D16403D1F8B02F00C22B1225D5A56B` を確認。capture contentのcanonical JSON結合は既出。今回は同じ試験の再実行ではない。
- Private GitHub `ButaMonky/Hakushin067-Research-Knowledge` developの `KNOWLEDGE_CURATION_PROTOCOL.md` blob SHA `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`、`symbols.tsv` blob `3fcf2d436c21f3fc91791a91e75c9a800167ca4d`、`SYNC_STATUS.md` blob `f069136afc073d8435daae3797855214fa9d17ef`をread-only参照。PC develop HEADとの一致は未確認。`0x4E53B0`既登録名 `Unit_RefreshTargetLatch`は変更しない。
- EXE source SHA256は先行原作確認記録 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。**今回EXEを再読していない**。2026-10-21旧SQLiteも今回読んでいない。

## 増分：呼び出し種別と時系列世代を混同しない

既存07時台の「32bit候補参照と0/非0判定」区別に対し、**同じ生ポインタが後のframeで別Unit/別召喚世代に再割当され得る場合**の合成比較を追加。実ゲームで再割当が起きたと確認したものではない。

1. `0x545A02` と `0x57AD8C` は `STORE32` モード。両者が非0であるだけでは値の意味一致を主張しない。battle/frame結合後、証拠付きUnit lineageと対応する生成イベント識別子を比較する。別プロセス間の生ポインタ数値の一致・不一致だけで合否を決めない。
2. `0x57D982` は `BOOLEAN_GATE` モード。このcallerの局所条件が使うのは0/非0なので、Unit lineageが未特定でも真偽の**合成ゲート比較**は可能。ただしUnit identityの同一性が証明されたわけではなく `strict MATCH`には昇格不可。
3. 保存したターゲットの `latch_source_spawn_event` と現在の `spawn_event_key` が不一致なら、`STORE32` は `MODEL_STALE_LATCH`。同じポインタ値であっても古いUnitへのlatchを継続利用したとは判定しない。実ゲームの「召喚/破棄」順は未観測であり、この世代情報は追加取得が必要。
4. scenario/battle/frame/source SHA/originの異常は `VERIFY` として隔離。合成資料に`DYNAMIC_VERIFIED`という自己申告を書いても `VERIFY_ORIGIN_UNTRUSTED`。同名表示の照合はUnit lineageの証拠にならない。

## 実行結果

- **60/60合成fixture PASS**。3 caller各20件。保存型の比較条件、異なるraw pointer・同じUnit、同じraw pointer・異なるUnit/生成世代、NULL、frame/battle相違、32bit範囲外、証拠欠落、自己申告DYNAMICを含む。
- **9/9メタモルフィック・変異検証PASS**。不正Unit lineage/生成世代/latch/battle/frame/source SHA/範囲外/自己申告を検出。異なるraw pointerでも確定した同じ識別子が保たれる場合だけモデル等価とする対照を確認。
- 初回テストで `BOOLEAN_GATE` に保存型の「lineage欠落要検証」を誤適用した期待値3件が失敗。caller別必要十分条件を修正し、**最終全件PASS**。失敗を隠して原作互換性PASSに数えない。
- これらの `origin="SYNTHETIC_FIXTURE_ONLY"`、source SHAも**合成証拠の値**であり、実機観測証明ではない。E現行runnerへ組み込んでいない。

## T018 C-NB02の合法Golden前提

- G0：未改変の合法原作UIによる実戦闘開始、戦闘run、シナリオ・ターン/phase・時刻・入力の真正な一次証拠。
- G1：同一戦闘の**直前SAVE実バイト**とSHA、実EXE・DAT hash、保存確定→侵攻操作の順序と状態連続性。SAVEの生バイトとRAMの生バイトをそのまま比べない。
- G2：原作実MAPのファイル/ハッシュ、攻守援軍三陣営Power、順序付き出撃Unit/Troop・位置・向き・初期frame。静的候補や表示名を実選択結果に代用しない。
- 候補Unit参照の真正照合が必要なら、同一run/battle/frameの**観測済み**Unit lineage、出撃/召喚/消滅のイベント順、当該latchの記録とその取得元のSHAを追加する。合成fixtureでは代替不能。G3/G4も観測なし。
- 実ゲーム `DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0`を維持する。

## T019 / MASTER / 安全

- T019新規**確定**矛盾0件。既存GameClear DAT13/TXT2の検索範囲差は旧RESOLVED、実際のloader順はVERIFY（今回はWiki/DAT原文の新規再読なし）。32bit値をboolへ縮退する**実装上の潜在的な互換リスク**は、実装照合未完了のため矛盾確定扱いにしない。
- PC MASTER最新が取得不能：旧最終確認checkpoint196、READY596（A115/B229/C136/D116）、34Task DONE9 / IN_PROGRESS21 / VERIFY4。**全部旧値**。今回の新規正式READY統合0件。
- 接続障害ID: `E-CONN-20261101-08H-MASTER-LOCAL-SESSION-TERMINATED-01`。試行: Local CompactのMASTER先頭45行read。応答 `Session terminated`。保存: 本独立成果。未保存: PC正本統合。影響: READY/owner/重複/競合は検証不能。次の許可された一手: PCが自然復帰した後、Local CompactでMASTER最新・レーン規約・HANDOFF・REA保存RUN・E資料を読み、同一ID/owner/時刻/source SHA/合意/競合/READYを確認してから一回のみ正式統合判定。
- 元MASTER・他owner・REA・dev_lab・Git/push・共有KB・原本EXE/ZIP/SAVE・スケジュール・Workは変更しない。

## KB_CANDIDATE（専任curatorへ引継ぎ、登録未確定）

- research ID: `E-OFFLINE-20261101-08H-T018-T020-CALLER-TEMPORAL-IDENTITY-01`、owner E/T018,T020。
- 関連VA: `0x4E53B0`; CALL sites `0x545A02`、`0x57AD8C`、`0x57D982`; 関連Unit offset `+0x1E570`。新たなnative CALL/ASMの発見はない。
- 内容: 保存型callerは非0のポインタ値をboolへ縮退せず、比較時には実証Unit識別子・誕生イベントの時系列を使う。真偽判定callerはidentityの未確定と区別。今回のidentity/spawnの形式は**合成受入案**、原作内部フィールドの断定ではない。
- 出典: 前回07時台E報告SHA256、旧10/28 semantic binding報告SHA256、上記GitHub blob SHA、今回検証器・fixture・receipt各SHA256（manifestに記録）。
- `STATIC=prior only / SYNTHETIC=60 PASS, mutation=9 PASS / INFERRED=temporal reuse hazard / DYNAMIC=0 / Golden=0 / READY=0`。
- 未解決: 実Unit lineageとspawn/消滅証拠、PC最新実装との一対一照合、旧安全拒否、未同期整理。知識ベース重複確認はGitHub read-only範囲、PC最新との差分未確認。
