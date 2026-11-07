# 迫真戦記 新B｜T024/T012：AI指示候補からUnitタイマー満了処理への静的接続

- 研究ID: `B-OFFLINE-20261022-1112-T024-T012-ACTION-TIMER-01`
- 復旧/接続ID: `B-RC-20261022-1112-LOCAL-SESSION-TERMINATED-01`
- 実施: 2026-10-22 11時台（JST）。Owner: B / T024, T012（既存T012参照は引用）。
- 状態: `OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。Golden PASS=0、strict MATCH=0、Task DONE追加=0、新規正式READY=0。
- Local: MASTER、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、B data所在への4読取がすべて `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。接続障害。安全拒否ではない。PC正本は読めず、PCへ書込・同期なし。
- 証拠: Library `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` の読み取り専用オフライン写し。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC PASS、34 entries。`search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite `PRAGMA quick_check` = ok。元EXE SHA256はマニフェスト記録値 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（原本再計算は不実施）。10/22 PCのV3 DB・機械語E8とは未照合。

## 今回の独立増分：T024→Unitタイマー→T012既存満了経路

1. `FUN_00577220` VA `0x00577220`（53 bytes）のGhidra擬似Cは、文字列コピー `0x00577237 → 0x00402800` の後、`UnitCandidate+0x1E4F8 = max(unaff_EBX, UnitCandidate+0x1E518)` 相当を書き込む。`ESI`はGhidra未解決レジスタなので、厳密なUnit引数ABIと候補値の生成式はVERIFY。この関数単体で「AI命令実行済み」などとは断定しない。
2. 旧Ghidra `calls` DBでは `0x00577220` の直接callerが5箇所・3関数：`0x004496C4` from `0x00449500`、`0x00449C24` / `0x00449E09` from `0x004498E0`、`0x0044B928` / `0x0044BB11` from `0x0044B240`。前回10時台は最初の1箇所のみ追跡。残り4箇所（ただし原作E8未照合）が今回の増分。
3. `0x00449500`ではContextのUnit候補ベクタ`+0x78..+0x7C`を走査し、`Unit+0x1867C=0`、`+0x1867E=0`、`+0xC0/+0xC8/+0xD0>=0`を満たす候補について `0x004496AF→0x005D1B80`、`0x004496B9→0x0040ED80`、`0x004496C4→0x00577220` と進む。後者に渡る候補値と各modeの切替効果は未確定。
4. **別の命令生成経路** `FUN_0044BBB0` には`0x577220`を呼ばずに `UnitCandidate+0x1E4F8=max(iVar19+1, UnitCandidate+0x1E518)` 相当を直接書くGhidra擬似Cがある。これにより同じUnitフィールドが、少なくとも「共通ヘルパ呼出」と「インライン式」の2経路で更新される候補を得た。ただし直接の機械語照合は未実施。
5. **T012既存事実への接続**：`FUN_0057AA00`（VA `0x0057AA00`）のGhidra擬似Cは、`int* param_1`の `param_1[0x793E]`、すなわちバイトオフセット `+0x1E4F8` に対し、値が正なら1減らし、結果が0なら `0x0057AB22 → 0x0057B380` を呼ぶ。`+0x1E518` (`param_1[0x7946]`) も正なら個別に1減らす。このタイマー減算・0到達時CALL自体は既存T012 native調査に記載済みで、再計上しない。
6. `FUN_0057BE30` VA `0x0057BE30` の既存T012後処理では、限定的なSkill分岐で `+0x1E518=0x4B (=75)` を設定し、`0<+0x1E4F8<75` の場合に`+0x1E4F8=75`へ引き上げる。常時75に初期化する処理ではない。今回の新しい接続は、この既存基準値を上記AI生成式が下限値として参照すること。
7. `FUN_0057B380`（VA `0x0057B380`）の擬似Cは複数のUnit状態・`+0x1E524`等の分岐を評価し、リスト処理、文字列操作、`0x0049EB50`などを通る。従って0到達時のCALLは事実候補でも、実際の効果・ゲーム内命令・RNG・再発動は未確定。旧DBの `0x57AB22` のE8 byteも現行V3と原作ASMでVERIFYが必要。

## 非重複・重要な留保

- `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01` の`0x449500`のUnit条件と`0x4496C4`は既知引用。今回は新たな4 CALL sites、共通helperとインライン式の比較、既存T012の満了ハンドラとの接続が増分。
- 10/21オフラインsnapshot の B HANDOFF/T024 文書には `0x449500` / `0x577220` の完全な同定は見当たらなかったが、PCの10/22最新正本を読めないため「全研究との非重複」は暫定。
- `0x1E4F8`をタイマー候補とするのは既存の正値decrementと0満了CALLによるSTATIC/INFERRED。`0x1E518`が「基準待機時間」であるというゲーム内意味はINFERRED。指示やSkillの実施回数とタイマーステップの比率はVERIFY。
- 無改変原作の実機観測0件、原本実行・書換0件、他lane/MASTER/REA/dev_lab/Git/設定/スケジュール変更0件。過去の安全拒否操作・証拠の再試行や迂回0件。

## 次回P0・原作Golden条件

- PC復帰時：最新MASTER cp/Task Queue/READY、LANE_B_HANDOFFとB T012/T024を読み、当IDの重複・権限・未同期を確認して一度だけ取り込み。現行V3で `0x4496C4`, `0x449C24`, `0x449E09`, `0x44B928`, `0x44BB11`, `0x57AB22` の E8 / JMP / tail-call を区別する。
- 原作ASMで`0x577220`へ入る ESI/EBX/ECX/stack と mode 0/1/2/3/6/7/8 の命令文字列を追い、`0x57B380`の条件・効果（成功/失敗）を特定。`0x44BBB0`インライン経路がどのモードから使われるかを追跡する。
- Golden：無改変EXE/DAT/SAVE/MAPで同一AIモード・Unit・Skill・RNG・入力・更新数を固定し、`+0x1E4F8`初期値 0/1/74/75/76、`+0x1E518` 0/75、Unit状態ガード分岐、連続AI要求が入り直すケースの書込み→減算→0到達→`0x57B380`を観測する。原作実測がない間strict MATCH=0。

## 再現検索（オフラインsearch.sqlite / 読取専用）

```text
python search.py function 0x577220 --max-chars 12000 --limit 1
python search.py callers 0x577220 --limit 20
python search.py function 0x449500 --max-chars 12000 --limit 1
python search.py function 0x57AA00 --max-chars 12000 --limit 1
python search.py callers 0x57B380 --limit 20
python search.py function 0x57BE30 --max-chars 12000 --limit 1
python search.py function 0x44BBB0 --max-chars 30000 --limit 1
```
