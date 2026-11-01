# 研究成果のGitHub優先収録規約（2026-11-01 ユーザー明示変更）
研究ID: KB-POLICY-20261101-RESEARCH-INTAKE-PRIORITY-01。対象: 迫真戦記 ver0.67 A/B/C/D/E/REA・専任KB統合。
正本: PRIVATE `ButaMonky/Hakushin067-Research-Knowledge` の `develop`。この規約は研究資料の公開・統合の新手順を定め、原作実ゲームの互換性やREADYを宣言しない。

## 方針: 研究成果を埋もれさせない
- **保存した研究を検索不能なローカル/Libraryだけに残さない**。担当は研究終了時、既収録研究ID・出典SHA・版・訂正関係を調べ、PRIVATE GitHubへの収録、担当固有 intake branchへの保全、または BLOCKED/OFFLINE-UNSYNCEDを記録する。新研究より過去の未同期回収を優先してよい。
- **二段階に分ける**。①`research/intake/<owner>/` は安全確認済み研究の出典・仮説・未検証も状態を明記して保全する（発見可能性）。②`REF_*.md`/`symbols.tsv`/`structs.tsv` は専任curatorが原本を検証・既存訂正と照合した確定事項のみ採用する（知識の信頼性）。①への保管はREADYや実機Goldenの証明ではない。
- Owner A-E/REAは**自分の研究成果・同意済み出典だけ**をPRIVATE GitHubの既存owner別隔離ブランチとPRを可能な限り再利用し、唯一の正規`research/intake/<owner>/`に安全な要約/manifestとして保存してよい（本ユーザー指示に基づく新規許可）。他owner本文、`develop`、共有辞書/REF/生成DBは依然変更不可。curatorだけが吟味して `develop` に ff-only で反映する。READMEや規約の今回の変更はユーザー明示の特例。
- PCオフラインでGitHubだけ使えるときも、現物確認した内容だけを`OFFLINE-UNSYNCED`として隔離branchに保全できる。未確認SHA/原作挙動/PC同期を捏造しない。ブランチ保存も不能ならE担当文書/会話に理由と再開位置を明記する。

## 研究1件の必須記録
`research_id`, `owner`, `tasks`, `observed_at/source_snapshot`, `source_relative_paths`, 実測`sha256`とその検証時刻、`VA / function_range / CALLsite / offsets`（なければnull）、`evidence_kind`（STATIC/INFERRED/SYNTHETIC/VERIFY/DYNAMIC）、`golden_status`, `ready_status`, `prior_ids`, `supersedes/errata`, `limitations`, `next_validation`、既存`REF`/辞書候補。各資料に1行の要約と検索可能な研究IDを入れる。SHAのない実体は`UNVERIFIED_SOURCE`として別扱い。
- 研究本文を保存できる場合は機密を除去したMarkdownと小さな再現手順・純粋fixtureを必要に応じて添付する。**目録だけ**で原文を復元できると主張しない。大きな原資料はSHAと相対パスで参照し、GitHubに全22kファイルを無差別同期しない。
- バックログは`research/intake/README.md`から owner / 日付 /研究ID/保管先 / 入力不足 / 採録済みを追跡する。各実行で旧未収録の確認可能な数件以上を実際に処理し、`PUBLISHED_INTAKE`/`CURATED`/`DUPLICATE_LINKED`/`BLOCKED`/`MISSING_SOURCE`で区別する。量が多くても**未処理件数と続きのID/パス**を維持し、同じ調査を毎時反復しない。
- 定期curatorは新規研究より**残存バックログの安全な入庫・重複/訂正/索引処理**を優先し、取り込める未検証研究も`VERIFY`を保持してGitHubで参照可能にする。重要度でT018 G0/G1/G2・T019修正・B/REAの未同期と未回収を扱う。収録済みIDは再コミットしない。

## 禁止と検証ゲート
- PRIVATE可視性・最終`develop` HEAD・他AIのworktree/lock/dirty・担当所有権を確認してから行う。作業用固有branch、通常commit/push、SHA照合、競合時は停止、`develop`統合はcuratorが ff-only/正常検査後だけ実施。reset/stash/rebase/amend/force、ユーザーworktreeのswitch/上書きは禁止。
- 名前・メール・絶対Windowsユーザーパス・認証情報・Cookie/HAR・生ログ、元EXE/DAT/MAP/ZIP/SAVE、復号セーブ・巨大SQLite/Ghidra生成DB、他者の非公開データをGitHubへ出さない。機密抜き要約と出典SHAに限る。
- **安全拒否された元操作/本文/対象は新許可でも再実行・分割・代替shell/tool/path/Remote/ZIPで取得・出版しない**。拒否ID/影響/既存保存有無のメタデータだけ（保護対象の具体内容を含めず）を残してBLOCKEDを保持。
- STATIC、合成PASS、索引のCALL/XREFは原作実動作ではない。原作合法G0/G1/G2の一次証拠と比較が無ければDYNAMIC OBSERVED/Golden PASS/strict MATCHは0、新しい正式READYは未証明扱い。
- curatorは追記前に同ID/同SHA/版、owner、出典・訂正、機密、lint/テスト、`SOURCE_MANIFEST`、GitHub readbackを点検。結果はGitHubのcommit SHA/リンク/未処理件数/次カーソルで報告する。push拒否・ロック・権限/接続障害は原因別に保全し、別経路で拒否を迂回しない。

## 旧運用との関係
従来`KNOWLEDGE_CURATION_PROTOCOL.md`の「A-E/REAは共有KBへ直接書かない」は**共有辞書・REF・develop正本に限って継続**。`research/intake/<owner>`をprivate隔離branchに保管する行為を新たに許可する。READYのMASTER正式統合は従来通りEのみ。旧スケジュールの有効/停止・頻度は変更しない。Workも自動利用しない。

## 2026-11-02 新旧PRの統合・状態台帳（旧branch例に優先）
- Bの正規入庫先は`research/intake/B/`、旧`research/lane_b/`は読取専用ミラー。ownerの旧PR・新PR・旧standalone historyを研究IDと内容SHA・訂正関係で照合し、余計なPRを新設しない。
- 非線形PRに対してowner rebase/merge/forceを要求しない。curatorが現行develop起点の隔離ブランチに精査済みsanitized blobsを採り、元PR/head SHAを記録する。部分採用PRは未収録IDを残して開いたままにする。
- `PUBLISHED_INTAKE`は原文保全の事実であり`CURATED`・`READY`・原作Goldenを意味しない。独立元ASM/DAT・SHA・先行解釈・訂正まで相互検証できたものだけREF/辞書へ採録する。PC不通/ロック状態不明/単体テスト不能ならGitHub隔離ブランチの未同期チェックポイントで止め、develop到達を宣言しない。
