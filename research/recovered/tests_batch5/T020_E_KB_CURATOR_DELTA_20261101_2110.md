# E研究知識ベース・GitHub再利用性監査（2026-11-01 21:10 JST）
研究ID: E-PC-20261101-2110-T018-T019-T020-KB-CURATOR-DELTA-01
Owner: E / T018,T019,T020。状態: STATIC SOURCE AUDIT / KB_CANDIDATE / VERIFY / NOT READY。原作Golden 0 / strict MATCH 0 / 新規READY 0。
## 1. 検証済み正本
- GitHub: PRIVATE ButaMonky/Hakushin067-Research-Knowledge / develop。最新取得コミット 66ba7dc2f96c6490221d5dd5aa3226d5b70c049a（本監査の観測値、PCローカルdevelop SHAとの一致未判定）。
- GitHub RESEARCH_SOURCE_CATALOG.tsv blob a8035045163df6daf71e824becb9bf0f013a3846。研究資料目録 1,937 records（source SHA/bytes/research ID のメタデータであり原文実体のGitHub保存証明ではない）。
- 11月1日EのPC所有資料 17H=1、18H=1、19H=2、20H=2 の計6 recordsが現GitHub目録から検索可能。前回19H時点の「17–20H未収録」は現時点では解消し、古いスナップショットのまま再報告しない。
- 11月1日Eの OFFLINE-UNSYNCED（03–16H）のresearch IDは現GitHub目録に0件。07–16Hの39ファイルSHA39/39はE17H/18Hの旧検証実績。今回39実体の再照合・PC転送は未実施。
- GitHub research/ に DAT UI v4 の研究本文と通常SAVE解析用再現コードが収録済み。GitHubは全22k研究ファイルのミラーではなく、選別知識・再現可能な限定素材を格納する。
## 2. PC原資料SHA256（本監査で実測）
- MASTER_LEDGER.md: E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3
- tests/T018_GOLDEN_CORPUS.md: CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120
- wiki/T019_CONTRADICTIONS.md: 102AFAB94359902D5E74E4B8C55D06CD46269B85DB1B7D0A426FCDE2ED6FC25B
- E17H  F3014188EC9729B8786569CC1CD8A03585E601C46B3A14F9B594976E4A9637CA / E18H D7A4498270737DC4E756638758BCAB1B9FD0E1EBF68592614D85F08FE66B7245
- E19H  11FF3B1318C85E3748D811BB36EF83962CCF51AA9FAFEE697444150C96F0CF95 / 19H receipt 9B8D894C25219BB428C41FF827812A2E2BF33196EC49504A2324CC33407F44D8
- E20H  21AD936F1A013F88E10E1FE05D51880708247DD1DADAEDB63FD1721DBA4D466F / 20H receipt 577CBDF041F32257C23D7182130F73CB3D447BE9CDF2D3BDE0917857966C9E2C
## 3. Curatorに渡す差分（内容の新発見ではなく索引/原本収録候補）
- E21-KB-G012: T018/T020 G0合法UI開戦・攻守Spot ID、G1同runの直前SAVE/入力、G2実MAP/三陣営/順序付き出撃Unit/Troop。共有不変入力と各run独立の観測を区別する。s16.map、保存Spot数、別PID観測をactualに昇格させない。REF_*の検索可能なE用入口候補。原本SHA・E19H/E20H ID参照。DYNAMIC OBSERVED 0、actual Golden 0。
- E21-KB-T019: T019既存訂正（GameClearのDAT13/TXT2検索範囲差はRESOLVED）と実行優先順位/TXT runtime/後続gwriteはVERIFY。0x50C9A0等の関数ラベルは元ASM・owner同意・既登録検証なしに新規確定登録しない。
- E21-KB-DISCOVERY: 03–16HのEオフライン独立研究を Library の保存記録・E17H/18Hの旧39件台帳で再照合してから、差分だけGitHub source catalogと分野別REFへ収録。複数ファイル/同一IDは1発見として扱い、合成PASSを原作GoldenやREADYへ昇格させない。
- GitHub READMEにはE/T018 Golden比較の専用REF入口が無い。専任curatorが既存REF_BATTLE_TAKEOVERとの差分を審査し、必要なら新規E分野別REFとインデックスリンクを作成。GitHubへの直接push/mergeはE担当範囲外。
## 4. 保護・継続
- 旧安全拒否（T018表境界、C T026/T032、D T030 TSV、禁止VA 0x5710C0等）、B HOLD21、10/25未回収、OFFLINE-UNSYNCEDを維持。別手段による元拒否迂回なし。
- MASTER checkpoint196 / READY596 (A115 B229 C136 D116) / 34 Task DONE9 IN_PROGRESS21 VERIFY4 は直近の旧検証値。今回READY統合・原作ゲーム実行・合成fixture実行はすべて0。
- E所有tests/のこの報告とJSONだけを追加。共有knowledge、MASTER、他owner、Git、原本EXE/DAT/MAP/SAVE/ZIP、Work、設定、毎時スケジュールは変更しない。
次の一手: curatorは66ba HEADとPC knowledgeのSHA/owner/既採用IDを再照合して不足を補う。Eは合法原作同一戦闘G0/G1/G2一次証拠回収を優先。