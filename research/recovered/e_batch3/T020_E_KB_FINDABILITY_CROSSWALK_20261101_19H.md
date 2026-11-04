# 研究E｜G0-G2/T019研究成果のKB発見性監査・専任curator引継ぎ（2026-11-01 19H JST）
研究ID: E-PC-20261101-19H-T018-T019-T020-KB-FINDABILITY-CROSSWALK-01
owner: E / T018,T019,T020。状態: PC READ-ONLY AUDIT / STATIC+VERIFY / KB_CANDIDATE / NOT READY。新規原作実行・合成試験0。
## 1. 正本と既存成果（今回実バイトSHA256再照合）
- PC MASTER_LEDGER.md SHA256 E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3。最終正式checkpoint196、READY596=A115/B229/C136/D116。34Task DONE9/IN_PROGRESS21/VERIFY4は旧分類・今回再判定なし。
- PC tests/T018_GOLDEN_CORPUS.md SHA256 CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120。
- PC wiki/T019_CONTRADICTIONS.md SHA256 102AFAB94359902D5E74E4B8C55D06CD46269B85DB1B7D0A426FCDE2ED6FC25B。
- PC tests/T020_E_NATIVE_CNB02_JOIN_PREFLIGHT_20261029_09H.md SHA256 EC23B00CD61DE2EEF28C15593E370EA224B36083CA4B508EFF0511C7260CE331。
- PC tests/T020_E_G012_OFFLINE_RECONCILIATION_20261101_17H.md SHA256 F3014188EC9729B8786569CC1CD8A03585E601C46B3A14F9B594976E4A9637CA。
- PC tests/T020_E_OFFLINE_39_ADMISSION_TRIAGE_20261101_18H.md SHA256 D7A4498270737DC4E756638758BCAB1B9FD0E1EBF68592614D85F08FE66B7245。
- 規約: evidence/ANALYSIS_LANES_PROTOCOL.md、A-D HANDOFF、REA PROGRESS、DEV計画、KB README/SYNC_STATUS、V9 CURRENT_ACTIVE_RESEARCH_STATE_LATEST.jsonを読取。現行V9、旧MASTERのV3は歴史記載。
- GitHub private ButaMonky/Hakushin067-Research-Knowledge develop HEAD 0225b2e1cd5c710137a3d921f593d158df06624a (今回read-only確認)。
## 2. 今回新たに確認した検索・同期上の欠落
- GitHub RESEARCH_SOURCE_CATALOG.tsvは現HEADの1,857 source receipts。文字列20261101/E-OFFLINE-20261101の検索一致0。11月1日Eの39ファイル・17H/18H報告の収録をGitHub catalogから確認できない。
- PC側 knowledge/kb.py research 'E-PC-20261101-18H' --limit 3 は表示0件。一方、対応する上記18H report原文はPCに存在しSHA一致。現時点のローカル全文索引に少なくともこの新規E IDが反映されていない。
- 同PCで kb.py docs 0x50C9A0 は既存MASTER/wiki T019/DEV出典を表示し、kb.py addr 0x50C9A0 は名前なし。GitHub symbols.tsvに0x50C9A0/0x557240の完全一致行なし、REF_DAT_BEHAVIOR.md/REF_BATTLE_TAKEOVER.mdにも両VA/T019を検索一致なし。
- PC knowledge/symbols.tsvの実SHA C01924149029DC7AB062A3056E8C7DF00968B126ACE32059E67DE871F456A704、GitHub SOURCE_MANIFEST.tsv収録symbols.tsv SHA256 6F93FECCF52A8415E6466409C715945C4D16645DDFF7D40668112BF0536BCA7D。異なる版でありPCの共有辞書を本Eが更新・同期してよい根拠ではない。PC structs.tsv実SHA 0355C84B03E273AD836CB3BBE37413860F2DF37386ADE08118D31D8FB1A2E083。
- これは「研究内容が消失した」ではなく「新規E報告がGitHub/現PC KB索引から直接発見できない」問題。生成DBの更新とGitHub反映は専任curatorだけが審査する。
## 3. 既存条件との差分（重複除去）
- T018既存§T018-E-20261015-1049 および10/17観測票は G0合法UI、G1同戦闘直前SAVE・入力/押下解放・SHA、G2実MAP・3side・順序付き出撃Unit/Troopを既に要求。16Hの「22未取得」「11追加候補」は22/11新仕様ではない。18H欄別照合で既存受入の主要欄純増0。
- 18H新設計候補: evidence_role={SHARED_IMMUTABLE_INPUT,ORIGINAL_INDEPENDENT_OBSERVATION,REIMPLEMENT_INDEPENDENT_OBSERVATION}。同一bytes/SHAの旧新共有SAVE/MAP入力は入力固定の正当な条件になり得るが、観測出力の同一ファイル実体や未証明別run使い回しは独立一次証拠として不可。Windows FileID/再解析/atomicityはNOT RUN。旧12Hの無条件path重複拒否は要限定。
- 09〜14H合成6ゲートの381/381は15H横断再実行値、16H負例19/19は別既報値。この19Hにどちらも再実行していない。旧実機G0-G2の真正性・strict互換を合成成績で補わない。
- 実機G0: 合法原作UIでsci1/po2(sp2)→sp16侵攻の実戦闘・時刻・battle-key。G1: 同一戦闘の直前SAVE実bytes/SHA、EXE/DAT基線・入力SHAと押下/解放。G2: 実MAP、攻撃/防御/支援の三陣営と出撃Unit/Troop順序・配置/向き。候補s16.mapやsave1/2のSpot保存数を実出撃へ昇格しない。
- 既存10/21 G0 limited native mode転移、watch別戦闘窓、非原子的RAWは構造観測でありE DYNAMIC OBSERVED/Goldenには未加算。GameClear DAT13/TXT2 source-scopeのみRESOLVED。script2同名勝者、TXT runtime読込、gwrite後続はVERIFY。原作確定新矛盾0。
## 4. 専任KB統合担当向け候補（自動昇格禁止）
- KB_CANDIDATE E19-KB-G012: owner E/T018,T020。既存T018 source SHA上記、18H source SHA上記。内容は新規関数発見ではなくG0/G1/G2観測適格性・shared-input/independent-observation区分・GOLDEN=0を分野別REFとして検索可能化する案。元観測未取得/実効HP-MP・VM/RNG等不可視はnull/VERIFY。
- KB_CANDIDATE E19-KB-T019: owner E/T019,T020。wiki T019 source SHA上記。既存STATIC: 原作loader候補0x50C9A0→0x50BF60の*.dat走査、別の0x557240はencode/write可能で第二runtime loaderとしない。GameClear DAT13/TXT2字句scope RESOLVEDだけを反映し、同名定義優先/例外・TXT runtimeをVERIFY。新規VA/CALL発見ではなく既存訂正の索引化提案。
- KB_CANDIDATE E19-KB-DISCOVERY: owner E/T020。source GitHub SOURCE_MANIFEST/catalog, PC 17H/18H SHA上記。new E IDのCatalog/FTS未収録と辞書版差をcuratorへ通知。ref一覧・研究IDを収録後も削除/重複加算せず、原本と生成SQLiteはGitHub送信禁止。
- 新規 VA/CALL/offset 実証0。原作EXE識別SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187は既存manifest値で今回原本再ハッシュなし。
## 5. 状態・安全・再開
- 今回正式READY追加0、MASTER書込0、DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0、T020原作者変更5系列6条件NOT RUN。34Taskは旧値。
- 旧T018表境界、E保存・検索拒否、C T026/T032、D T030 TSV、禁止VA 0x5710C0等は独立BLOCKED。B HOLD21、10/25未回収、11/1 OFFLINE39原文のPC未同期を保持。今回安全拒否0。別shell/tool/path/Remote/ZIPで元拒否を迂回していない。
- 原本EXE/DAT/ZIP/SAVE、A-D/REA/dev_lab、Git/push、共有KB、Work、スケジュール/設定への書込0。GitHubはread-only、専任curatorへ候補を渡すため本E所有文書のみ新規作成。
- 次の許可された一手: (1) curatorがGitHub develop/PC KBのSHA/owner/IDと39件を照合して差分だけ索引化、(2) Eは合法同一戦闘G0/G1/G2一次receiptsを優先確認、(3) 新旧厳格比較は入力・真正性・実観測が揃った場合にのみ実行。
