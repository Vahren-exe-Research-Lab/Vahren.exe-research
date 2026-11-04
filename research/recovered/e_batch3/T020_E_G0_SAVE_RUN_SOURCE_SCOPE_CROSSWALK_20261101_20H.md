# 研究E｜C-NB02 G0実機・保存SAVE・別run G2の出典結合適格性監査（2026-11-01 20H JST）
**研究ID** `E-PC-20261101-20H-T018-T019-T020-G012-SOURCE-ROLE-AUDIT-01`。owner E／T018,T019,T020。`STATIC SOURCE RECHECK / LIMITED DYNAMIC SECONDARY / VERIFY / NOT READY`。原作EXE再実行・新規Ghidra・T020 testは **NOT RUN**。
## 原本・状態の読み戻し
- Desktop Commander Local CompactでMASTER、レーン規約、A-D HANDOFF、REA `rea_lab/decomp_task/PROGRESS.md`、DEV計画、E T018/T019/19H、V9最新ポインタ、KB README/SYNCを読取。MASTER SHA256 `E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3`、T018 `CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120`、T019 `102AFAB94359902D5E74E4B8C55D06CD46269B85DB1B7D0A426FCDE2ED6FC25B`を本回Get-FileHashで再確認し前回と一致。
- V9現行指定 `rea_lab/headless_analysis/search_index/CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` は2026-10-29に `HAKUSHIN067_UNIFIED_V9_20261023.sqlite` を選択。旧 `README.md`/`BUILD_MANIFEST.json` がENOENTは移行後の参照差であり、安全拒否・PC接続不良ではない。旧10/23 V9 READMEに残る「currentはV3」記述より最新ポインタ優先。V9の再解析/実行なし。
- GitHub PRIVATE KB `develop` は本回 `ea6779e765245c79a38eb757446b42d7e47f9234`（19Hの`0225b2e1`から進行）。SOURCE_MANIFESTのsymbols SHA256は `AFB91A0188A12199EB3FDD10D79EA4BD318AE20F291902B85106A043E21FECE3` に更新済み。旧19Hの版差所見を現在の差として機械継承しない。研究本文catalogは依然旧1857件のスナップショットで、11/1 E IDの新規収録を確認できず。EからGit/push/KB書込なし。
## 既存原作G0証拠とC-NB02候補の区別
- `rea_lab/headless_analysis/search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json` 現物SHA256 `87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C`、内蔵watch証拠SHA `9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DC5B089E262A7`。PID23272の原作 mode2/active1 は2026-10-21T14:31:37.765392Z、戦略復帰14:33:35.933687Z。ユーザー申告による実攻撃の限定観測あり。
- しかし同G0 JSONは `attacker_spot_id_from_native_memory_verified=false`、`target_spot_id_from_native_memory_verified=false`、`battle_packet_complete=false`。人間向け攻撃地名の報告を、C-NB02の静的 `sci1/po2/sp2→sp16` と同一IDだと変換・確定できない。**既存ファイル内 gate_status=PASS は『実戦闘遷移あり』の局所判定で、EのG0/G1/G2 Golden PASSではない。**
## G1保存資料の出典別照合（値はファイルの保存済み記録、最新SAVE本体の再ハッシュではない）
- `BATTLE_BRIDGE_CURRENT_ORIGINAL_SAVES_20261021.json` 現物SHA `C5FAED1D622C0B246F9FC505CD265714C86EE5D05DC99A5A38295C1CCDDFC1B6`：auto.sav `C09C098C...6B29F`／5,953,848B／mtime 2026-10-21T12:18:00.767970Z。G0 activeより約**2時間13分37秒前**。開始直前SAVEと同じrun・同じ戦闘の証明がなく `G1_UNBOUND`。
- 同ファイルの save1.sav `E80B3474...183AF` mtime 2026-10-19T13:13:28.179017Z（約49時間18分前）、save2.sav `45CCEF30...63F5` mtime 2026-10-10T21:52:19.747500Z（約10日16時間39分前）。過去に読み込まれた可能性は排除できず、時差だけで不適格確定はしないが、同一戦闘直前の証明は **0件**。
- `BATTLE_BRIDGE_AUTO_SAVE_SUFFIX_DIAG_20261021.json` 現物SHA `A28BA58B75D2307B1816DC0530EAC17D8A49AA1CBB6CB214727722DFFB3B42E8` は同名auto.sav/同サイズ5,953,848Bを `EA0D5CC6...5400` と別SHAで記録。2出典を一版に合成禁止。原因（別保存版・mtime変化・転記）は **VERIFY/IDENTITY_CONFLICT**。どちらもG1適格としない。
## G2出典と比較可能性
- `BATTLE_STAGE13_INPUT_COVERAGE_20261022.json` 現物SHA `17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB` の一サンプルは PID28432（G0は23272）、side0=Player/attack、side1=Enemy/defense、side2=Enemy/other_or_empty、side2 power_ptr=0。別PIDの非原子的RAWをG0原子スナップショットへ混合しない。第三sideの存在も第三**勢力**の確証ではない。
- 既存 `BATTLE_STAGE11_CROSSRUN_ANALYSIS_20261022.json` は原作3sessionのうち複数のRAWを別セッションとして記録。C-NB02旧T018の静的 `s16.map` とsave1/2 Spot保存名簿は、実選択MAPや実出撃・Troop一覧に昇格不可。G2実MAP/三陣営/順序付き全出撃と開始frameの同run証拠は未充足。
## T020比較fixture期待判定（本回設計、実行0）
| ID | 境界 | 期待判定 |
|---|---|---|
| S01 | 合法実戦闘mode2遷移あり、攻守Spot実IDなし | G0_MODE_ONLY／C-NB02への同定はVERIFY |
| S02 | auto.savのmtimeのみG0前、run証拠なし | G1_UNBOUND、時差だけで不可能と断言しない |
| S03 | save1/save2にscenario po2等一致、直前証拠なし | G1_UNBOUND、SAVE実体とplay sessionを推定結合しない |
| S04 | 同名・同サイズauto.savに異SHA | IDENTITY_CONFLICT、HASH相互代用不可 |
| S05 | 他PIDのRAWは詳細、G0 PIDと異なる | CROSS_RUN_G2_UNBOUND／原子同run不可 |
| S06 | side2存在・power_ptr=0 | THIRD_POWER_UNPROVEN／3陣営のPowerを補完しない |
| S07 | 静的s16.mapと保存名簿だけが揃う | STATIC_CANDIDATE_ONLY／旧原作Golden非適格 |
| S08 | 新実装側同等SAVE/input/出力の独立観測なし | NO_STRICT_COMPARISON |
## T019・統合・拒否・次
- T019のGameClear DAT13/TXT2は字句検索範囲の既存RESOLVED。script2同名定義勝者/TXT runtime load/後続gwriteはVERIFY。今回の原本Wiki/DAT/EXE再走査・新確定矛盾は0。T020のS01-S08は**DESIGNED_NOT_RUN**で新回帰PASS0。
- MASTER最終checkpoint196、公式READY596（A115/B229/C136/D116）、34 Task DONE9/IN_PROGRESS21/VERIFY4は旧分類・全再集計なし。新規正式READY ID=0。**E gameplay DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0**。B/REA旧限定原作mode観測をE累計に移植しない。
- `KB_CANDIDATE`: `E20-KB-G0-SAVE-G2-PROVENANCE` owner E/T018,T020。元3レーンのsource IDsを新発見数に加算しない。対象VA/CALL/offsetなし、STATIC SOURCE+VERIFY、C-NB02識別子・SAVE version・run間RAWの受入境界をcuratorに引継ぐ。既存E19 3候補と意味重複を審査し、REF側への反映はcurator専任。原本/検索DBはGitHub送信禁止。
- 旧T018表境界、E session join/DAT追記、C T026/T032、D T030、禁止VA0x5710C0等の安全拒否はBLOCKED据置。B HOLD21、10/25未回収、OFFLINE39原文PC未同期を保持。新規安全拒否0。MASTER/T018/T019・A-D/REA/dev_lab・原本EXE/DAT/ZIP/SAVE・Git/push/共有KB・Work・他schedule/設定へ書込なし。
- **次**：E/T020でS01-S08を保存済原本ID・真正性・適格性に結合した受入票として維持。新しい合法旧原作C-NB02 G0地名⇔Spot実ID／G1同run直前SAVE+input／G2実MAP・三勢力・出撃順序の証拠が提供された場合にのみ正式Golden検討。前回成功へ巻き戻さず、認可範囲のみ調査。
## 非安全障害・回復記録（無視せず引継ぎ）
- [RECOVERY-ID] `E-OP-20261101-20H-READONLY-RECOVERED-01`／2026-11-01 20時台 JST。初回read-only `rea_lab/PROGRESS.md`、旧 `search_index/README.md` と `BUILD_MANIFEST.json` はENOENT。対象が移動/置換された参照先の違いで、認可拒否ではない。正規Local Compactで `rea_lab/decomp_task/PROGRESS.md`、`00_START_HERE_UNIFIED_V9_20261023.md`、最新 `CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` を読み直した。出典不足のままV3/V9混同や最新REA READY昇格はしなかった。
- 同一Local Compact内の初回複数Get-FileHash組立がPowerShell `ParserError: ExpectedExpression` となり **ハッシュは未取得**。その後、同じ認可済みread-onlyコマンド経路でファイルを個別にGet-FileHashし、7つの指定出典SHA・MASTER/T018/T019を実バイトで確認した。安全拒否を別shell/tool/pathで迂回したものではない。
- 保存済み: 本T020報告と同名機械可読JSON。未保存の検証成果0、EXE/ゲーム起動0、不可視内部の補完0。再開位置: G0攻守Spot実ID/合法UI時刻と同run G1 SAVE/input・G2 MAP/3side/Unit/Troopの一対一証拠が得られた場合のみ受入審査。

[20H算定訂正] 上記「7つの指定出典SHA・MASTER/T018/T019」は、G0/SAVE/SUFFIX/STAGE13の4資料とMASTER/T018/T019の3資料、**計7ファイル**を指す。別途10ファイルを実SHA照合したという意味ではない。
