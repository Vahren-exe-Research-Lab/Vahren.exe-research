# 迫真戦記 新E｜T018/T020 合成Golden captureの意味情報バインディング監査

- 独立ID：`E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01`
- 基準日時：2026-10-28 21:49 JST（予定照合時刻、時刻同期を保証する記録ではない）。担当 E、T018/T019/T020 のみ。
- 状態：`OFFLINE-UNSYNCED / STATIC-OLD-INDEX / SYNTHETIC EXECUTED / VERIFY / NOT READY / ORIGINAL-GAME NOT RUN`
- 所有権：E資料への新規追加のみ。PCのMASTER、A～D、REA、dev_lab、原作EXE/DAT/SAVE/ZIP、Git、設定、Work、スケジュールには変更しない。

## 証拠とアクセス境界

Desktop Commander Local Compactの `_REDEV_RESEARCH` ディレクトリ一覧読み取りは `Session terminated` で失敗。新規復旧ID `E-RC-20261028-2149-LOCAL-SESSION-TERMINATED-01`、分類 `CONNECTION`。これは安全拒否と区別する。PCの最新正本・owner/READY・最新他レーンHANDOFFを取得できていない。拒否済みPC操作の迂回は行っていない。

代わりに、既存の正規Libraryアップロード `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` をファイルID確認後にmaterialize。ZIPの実測SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` と、含まれる `headless_analysis/search_index/search.sqlite` の実測SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` を再確認。SQLiteには `mode=ro&immutable=1`、`PRAGMA query_only=ON`で接続、`PRAGMA quick_check=ok`。Ghidra/Java、原作実機は未起動。EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は2026-10-21のマニフェスト記録値であり今回のEXE現物ハッシュではない。

今回は2026-10-28 20:45 E合成Golden fixtureおよびテストコードの実ファイルを監査。既存ファイルのSHA256が前回の記録値と一致していることを確認し、新規独立fixture・新規検証コードだけを作成した。T018既存表境界やsession-joinといった過去に拒否された領域は再読込していない。

## 今回の具体的な発見：生バイトのSHA一致だけでは「構造化フィールド」の整合性を保証しない

前回20:45の `hardened_synthetic_ready()` は、G0/G1/G2の `capture_b64` を厳格Base64デコードし、記録された各 `capture_sha`、SAVE/input/MAPのハッシュとG1→G0→G2のハッシュ連鎖が正しいことをチェックしている。この改良は有効。しかし `capture_b64` が**可視の `scenario`、`EXE SHA`、`DAT SHA`、`at`、`event_seq`、`sides`、`deployed`（Unit/Troop/座標/名簿順序）などを実際に符号化したデータかどうか**をチェックしていない。

したがって、`capture_b64` と各SHAおよび親ハッシュ連鎖を一切変更せず、構造化情報だけを変更しても、前回ゲートが `True` を返す合成ケースが存在した。具体的には、G2 Unit名変更、Unitの配置座標改変、三陣営のID再割当、出撃名簿の増減・順序変更、G1 SAVE/inputのバイト列とSHAの差し替え、G2 MAPバイト列とSHAの差し替え、run/scenario/EXE/DAT SHAの一括置換が該当する。さらに、非標準のcaptureバイトを再ハッシュして親参照を再生成しても、古いゲートは承認する。

この問題は**前回の構造化合成fixtureの検査不足**であり、原作ゲームまたは新戦闘エンジンの不具合と断定しない。前回から `actual_golden()` はこれらの合成資料を認証しないため、実際のGolden合格を誤計上した証拠もない。

## 新設したE所有の合成検証ゲート

`hakushin-synthetic-capture/v1` という**検証fixture専用の仮想形式**を採用。captureの生バイトは、ステージ名と構造化フィールドの完全なcanonical JSON（sort_keys、余分な空白なし、非有限数値不可、UTF-8）で構成し、受入時に**構造化フィールド全体を正規化して再シリアライズしたバイト列との完全一致**を要求する。`capture_sha`と`capture_b64`自体は循環参照を防ぐためJSON対象から除外するが、G0/G2の `previous_capture_sha` は内容に含める。スキーマにないフィールド追加はバージョン変更なしでは受け入れない。

この条件は前回20:45ゲートを削除せず、その上に追加する比較fixture用の保守的条件である。前回ゲートが引き続きG0/G1/G2 SHAおよびG1→G0→G2親リンクを検査する。

**重要な限界**：新しいsemantic bindingも、攻撃者・研究者がJSONとSHAを一式作り直せば通過する。したがって *構造化fixtureとそのcaptureバイトの一致* をテストするだけで、実ゲームの合法UI観測、原作のWorld/Unit状態、未改変SAVEの外部真正性を証明しない。実際の原作capture形式としてこの仮想JSONを押しつけてはいけない。原作観測用の証拠形式・プロセス・外部監査は別途必要。

## T020 合成回帰結果

- 比較fixture **36件**（前回ゲートはPASSしてしまうが新ゲートが拒否する **31件**、前回から拒否するcontrol **2件**、両ゲートで整合的にPASSする再結合した合成control **3件**）。
- 新規テストは **45/45 PASS**。内訳：36 fixture + 9 provenance/suite/static boundary checks。最初の開発実行では配列要素インデックスが文字列のままだったため12件でTypeError。新規コードの独立修正後に再実行し45/45 PASS。最終ファイルには修正済みのコードのみ含む。
- 2026-10-28 16:45（28件）、17:45（46件）、18:49（36件）、19:49（58件）、20:45（36件）を**同一の2026-10-21旧SQLite**に対して独立再実行し **204/204 PASS**。
- 今回実行した合計 **249/249 PASS**、失敗0件。13時台の安全拒否により `NOT RUN` の14 fixtureはこの数に含めていない。
- 証拠分類 `STATIC-OLD-INDEX / SYNTHETIC EXECUTED`。**原作実機DYNAMIC OBSERVED 0、actual Golden PASS 0、strict MATCH 0**。`NOT READY` のため正式統合対象とは認定しない。

## T018・T019と受入条件

T018は引き続き、同一原作戦闘の合法UI G0戦闘開始、G1直前の未改変SAVE＋入力、生MAP・三陣営・ordered出撃Unit/Troopを含むG2を外部一次証拠として対応付ける必要がある。G3戦闘結果・G4戦略World差分も同じ戦闘に結び付ける必要がある。*fixtureの型・SHA・semantic binding合格はactual Golden PASSを意味しない*。

T019新規確定矛盾 **0件**。本監査の31件は原作DAT/EXE/Wiki間の矛盾ではなくE-owned合成検証受入の欠落として分類。前回確認値としてGameClear DAT13/TXT2字句検索範囲差はRESOLVED、`script2`同名定義順序・phase flag・TXT実読込・`gwrite`復帰・`decide11`用途同一性はVERIFY。PC正本からの今回の再確認はできていない。

## MASTER・安全拒否・再開

PC未接続につき、最終既知の **2026-10-28 12時台** MASTER値 `checkpoint196 / READY596 (A115 B229 C136 D116) / 34 Task (DONE9, IN_PROGRESS21, VERIFY4, 既知ID重複0)` を**旧値**として保持。今回新規READY統合 **0件（該当IDなし）**。最新のowner/READY/既統合/ソースハッシュ/合意/競合を照合しておらず、MASTERへの正式反映は実施しない。10月25日以降のOFFLINE-UNSYNCED成果も既統合・重複検査が未完了。

既存の安全拒否 `E-RC-20261028-1353-READONLY-PS-SAFETY-01`、`E-RC-20261028-13H-E13-REPORT-APPEND-SAFETY-02`、旧T018表境界/session-join、T019拒否済みXREF、C T026/T032、D T030 TSV、`0x5710C0` はBLOCKED継続。拒否済み操作を別shell/tool/path/Remote/ZIPで再提出していない。今回の `Session terminated` は `CONNECTION`、新規安全拒否0件。

次のE優先作業は、**PC自然復旧後の許可範囲のE所有T018 runner最新版とのコード・契約差分照合**（拒否済み操作を除く）と、合成fixtureのsemantic一致の受入条件を既存runnerに統合できるかの非破壊検討。並行して、合法原作UI同一戦闘G0/G1/G2一次証拠収集が研究全体の最優先。新E資料は `OFFLINE-UNSYNCED` として独立保存し、既存正本を巻き戻さない。
