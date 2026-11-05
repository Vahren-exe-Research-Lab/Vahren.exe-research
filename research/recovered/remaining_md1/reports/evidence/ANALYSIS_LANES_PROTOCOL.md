# 迫真戦記 5レーン定期解析・競合防止（2026-10-08）

## GLOBAL-NON-ABANDON-P0-20261013 — 全レーン・Work/REA/新F向け運用通知
ユーザーの最優先指示: 拒否・接続失敗・競合・時間上限で解析成果を放置しない。自担当の既存HANDOFFへRECOVERY-ID、最後の成功、未保存差分、所有者、再開条件を残して読み戻し、独立作業を続ける。元のTask/READY/Golden境界と担当権限は不変。共通全文: `[USER_HOME]\Documents\AI_SCHEDULE_RECOVERY\GLOBAL_NON_ABANDONMENT_POLICY_20261013.md`。本通知は他チャットへの直接送信ではなく、次回読取時に初めて受領する。
正本: ../MASTER_LEDGER.md。全レーンは毎回、正本のTASK QUEUE/最終checkpointと本規約を最初に読む。原本ZIP/EXE/ゲームファイルはread-only。Remoteは使用せずDesktop Commander Local優先。安全拒否を別shell・別toolで迂回しない。
## 所有権
A / EXE・VM・永続化: T005,T006,T009,T010,T014,T023,T031。これらのTask番号に対応する data/ と exe/ の資料、および evidence/LANE_A_HANDOFF.md だけを新規編集。
B / 戦闘・AI: T011,T012,T013,T024,T028。対応する data/・exe/ のTask資料、および evidence/LANE_B_HANDOFF.md だけを新規編集。
C / 内政・戦略・イベント: T016,T025,T026,T027,T029,T032,T033,T034。対応する data/ と evidence/ のTask資料、および evidence/LANE_C_HANDOFF.md だけを新規編集。
D / RTS・表示・音声・入出力: T015,T017,T030。対応する data/ と evidence/ のTask資料、および evidence/LANE_D_HANDOFF.md だけを新規編集。T007/T008は既存DONE資料を参照のみ。
E / 互換検証・統合: T018,T019,T020、制作側DEV依頼。MASTER_LEDGER.mdと、既存 tests/T018*・wiki/T019* の統合管理を単独担当。他レーン資料はread-only。
## 共有資産の書込
MASTER_LEDGER.md のTASK QUEUE・RUN CAPACITY・checkpoint・分析結果の統合はEのみが書く。A-Dは正本を変更せず、自分が所有する資料と各LANE_*_HANDOFF.mdへ証拠・未解明・Task進捗を保存する。最終的な確定知見はEが重複排除後にMASTERへ統合する。
各hand-off記録は、重複しないID（例 A-20261008-1401-01）、日時、Task、対象原本/位置、CONFIRMED/VERIFY/BLOCKED、根拠、実装への影響、試験条件、再開位置、完成マーカー READY を持つ。追記式で過去レコードを消さない。EはREADYだけを扱い、MASTER内の統合済みIDを確認して二重反映を防止する。
他レーン所有資料は読取のみ。既に他の処理が同じ資料を編集している・予約済み・未確定の場合は自レーンでも破壊的変更せず、その回はread-onlyへ移る。重複Taskは担当レーンへの依頼として記録し、横取りしない。
## PC負荷と安全
5タスクは毎時12分ずつ開始をずらす。ただし開始時差は実行の非重複を保証しない。先行解析が長時間実行中・PC高負荷・ファイル競合の場合は重い新規プロセスを開始せず、自レーンの軽量read-only作業へ切替・またはその回をSKIPPEDと記録する。
同一レーンで先行runが進行中なら二重起動相当の変更を避ける。原本変更、研究領域外書込、Git操作/push/公開、他レーン成果の上書きは禁止。制限時は成果を保存して安全に終了し、スケジュール自体を勝手に無効化しない。
Eは各レーンの未統合handoffを定期的に読み、制作チャット起点のDEV依頼を既存Task IDへ紐付けて優先度を決める。報告時には確定/推測、実機未検証、DONE判定の根拠を厳密に区別する。
## 共通復旧管理への引き継ぎ（RECOVERY-SHARE-V1-20261008）
- 横断管理用のread-only参照先は `[USER_HOME]\Documents\AI_SCHEDULE_RECOVERY\RECOVERY_HUB.md`。このハブは別の復旧管理チャットのみが書き込み、A〜Eは編集しない。
- 各runで操作が安全拒否/timeout/接続失敗/競合により未完了なら、既存の所有範囲にあるA〜D各 `evidence/LANE_*_HANDOFF.md`、Eは `MASTER_LEDGER.md` の次回checkpointへ、`RECOVERY-ID`・Task・操作/対象・ツール・原因・最終成功状態・未完了範囲・再開条件を最小限記録する。記録できない時は応答内で明示し、虚偽の書込成功を報告しない。
- `Status: BLOCKED` / `NOT READY` の記録はEのREADY統合対象外。原因分類は SAFETY_REFUSAL/TIMEOUT/CONNECTION/CONFLICT/OTHER。成功証跡が無ければDONEやREADYにしない。
- 他レーンのファイルや共有ハブへ直接修正・代行はしない。安全拒否を別チャット・別shell・別tool・別pathで迂回しない。独立read-only作業は継続可。復旧管理は担当への安全な再開依頼を整理するだけ。
- 5レーンの開始時刻、所有権、原本read-only、MASTERのE単独編集と全自動化スケジュールの有効状態は従来どおり維持。

## ユーザー横断最優先・拒否放置禁止（USER-DIRECTIVE-NO-ABANDON-20261013）
- 全研究A〜E・REA・新F・Claude・Workは開始時に `[USER_HOME]\Documents\CHATGPT_OPERATION_RULES.md` の同名節を読む。拒否やWork枠切れ・通信中断で分析・実装・テスト・引継ぎ全体を放置しない。
- 拒否操作の迂回ではなく、担当所有の正式資料/HANDOFFへ証拠・次VA/次処理・未完了範囲・実装への影響・再開条件をID付きで保存し読み戻す。保存できない場合はPC未保存と明示。原作証拠と仮説を混同せず、READY/DONEには昇格させない。
- 重複解析・成果散逸を避け、毎run最初にWork依頼キュー・MASTER・各HANDOFF・予約を読み、既知成果を再取得せず独立した許可済み解析を継続する。Work専用キュー/E専用MASTER/他レーン資料/製品コードの書込権は変えない。
- 本ファイルは共有参照先。チャットへ自動送信された証明ではなく、各チャットが次回読み取った時点で適用する。

## USER-OVERRIDE-B-GITHUB-20261101｜B研究成果のGitHub先行保全（ユーザー明示変更）
- 2026-11-01にユーザーが「解析成果を非公開GitHubへ反映する」ことを明示指示。従来の「BはGit/push禁止」は、B所有T011/T012/T013/T024/T028の**非機密な研究本文・証拠要約**を private `ButaMonky/Hakushin067-Research-Knowledge` の隔離B専用作業ブランチへ保存する操作に限り解除する。この特例は他lane、MASTER、原本や製品コードに拡張しない。
- 毎回、Bの未同期/未回収とsource SHA・既存研究IDを確認し、現在の成果に加えて過去の未統合成果を重複なしで小バッチずつ保全する。B担当が直接書けるGitHubパスは `research/lane_b/` 以下の独立ID別の安全なMarkdown/TSVのみ。共有 `symbols.tsv` / `structs.tsv` / `REF_*` / `SOURCE_MANIFEST.tsv` / `develop` は従来どおり専任知識ベース統合担当だけが変更する。
- BはPRIVATE設定を毎回確認し、別の専用ブランチ（例 `work/b-evidence-YYYYMMDD-HH`）で単独コミット/通常pushし、GitHubからファイル再取得とcommit SHA照合を行う。変更点のPRを統合担当へ引継ぐ。PCの他人の既存Git作業ツリーを切り替えない。原本EXE/ZIP/DAT/SAVE、Ghidra DB、生成SQLite、ログ、秘密情報、個人識別パスは送信禁止。元安全拒否済み操作/同一証拠の迂回は引き続き禁止。
- GitHubに保全しただけなら `GITHUB_STAGED / NOT_CURATED`。統合担当が本体証拠・source SHA・矛盾/重複・情報保護・KB allowlist/manifest/テストを確認後、隔離curation branchとff-onlyで `develop` のREF/辞書に反映して初めて `GITHUB_CURATED`。STATICからDYNAMIC/Golden/READYへ自動昇格しない。
- 各runは `research_id, owner, task, VA/CALL/offset, source_relative, source_sha256, certainty, correction, Golden, READY, GitHub branch/commit/URL, NOT_CURATED原因` を自HANDOFFへ追記・読戻し。GitHub書込不可なら `UNSYNCED` と実際のエラー・再開点を残し、成功を偽装せず、次回も未統合キューを優先する。既存毎時頻度・稼働状態・EのMASTER権限は不変更。

## ユーザー最優先・拒否放置禁止の横断連絡（GLOBAL-CONTINUITY-20261013-1450）
- 2026-10-13ユーザー明示指示。作業拒否・失敗・切断・競合後、停止操作を放置せず、**その回に担当owner資料/HANDOFFへRECOVERY-ID・対象/エラー・最終成功checkpoint・未保存/未commit/未統合・再開条件・独立作業・引継先を保存し読み戻す**。書込自体を拒否された場合はユーザーへの回答内に情報を残し、「記録済み」と虚偽報告しない。
- 始業時に既存RECOVERY-ID・owner HANDOFF・予約・Gitのdirty/staged/committed/unintegratedと最新checkpointを照合し、以前の成功を重複実装・重複統合・二重計上しない。拒否された操作だけをBLOCKEDにして安全に独立できる研究・検証・記録は続行。必要な情報は次ownerとE/Workへ既存HANDOFF/正式キューで伝達する。
- **共有復旧ハブ正本** `[USER_HOME]\Documents\AI_SCHEDULE_RECOVERY\RECOVERY_HUB.md` の`GLOBAL-CONTINUITY-20261013-1450`を必読の横断伝達契約として参照。A〜Dは各レーンHANDOFFのみ、EはMASTER/T018のみなど従来の担当所有権を維持。ハブの以後の正式更新は復旧管理担当。安全拒否を別shell/tool/path/Remote/別チャットで迂回しない。原本・他lane・Work製品・Git/設定/スケジュールを変更しない。本追記はユーザー指定の通信のみで既存Task/READY/DONEの状態変更は0。
