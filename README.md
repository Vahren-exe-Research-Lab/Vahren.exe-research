# 迫真戦記 ver0.67 研究知識ベース

関数とメモリの意味を調べ、その根拠になった研究本文まで辿るための事典です。人がGitHubで読むページと、AIが検索するデータは同じ辞書・出典から生成しています。

現在の正本はこの非公開リポジトリの `develop` です。公開に向けた整理とローカル文書の回収を進めています。全研究の移管・公開準備の完了を示すものではありません。

## まず調べる

| 調べたいこと | 入口と読み方 |
|---|---|
| 関数・アドレス・グローバル値 | [関数・メモリ事典](reference/README.md)で名前やVAを探し、個別ページの意味・確度・根拠を読む |
| 構造体とメモリの位置 | 同じ事典の[構造体一覧](reference/README.md#構造体フィールド)から型を選ぶ。例：[ScriptEngine](reference/structs/ScriptEngine.md)、[実行時ユニットのHP関連](reference/structs/UnitRuntime.md)。フィールドの説明、読み書き関数、根拠へ進む |
| 研究本文だけにあるオフセット | [所有者＋オフセット索引](reference/FIELD_MENTIONS.md)。`0x`付きの局所表記が対象。正式な型・幅・意味の確定とは区別する |
| 訂正された説明 | [訂正一覧](reference/CORRECTIONS.md)で旧解釈・現在の解釈・根拠を比較する。各関数・フィールドからも辿れる |
| 研究ID・題名・本文 | [回収済み全文書](reference/DOCUMENTS.md)。本文と回収制約を確認する。手元のコピーでは下の検索も使える |
| 呼び出し元・呼び出し先 | 各関数ページの静的CALL一覧。収録済みのV9直接CALLが対象で、間接CALLや全関数の網羅ではない |
| 未回収・保留・原本との対応 | [回収状況](research/recovered/README.md)、[現在のローカル所在](research/recovered/current_inventory/README.md)、[元の目録と収録の照合](research/recovered/COVERAGE.md) |
| PR・Issue・研究チャットに残る成果 | [GitHub上の所在](research/recovered/GITHUB_SOURCES.md)、[定期研究チャットの照合](research/recovered/SCHEDULE_CHAT_CHECK.md)、[旧チャットの回答保全](research/recovered/chat_finals/README.md)、[旧Aの研究報告と参照照合](research/recovered/chat_a_history/README.md)。いずれも取得時点の記録 |

GitHubだけでページと収録本文を読めます。通常の事典検索にも、元PCの大容量DBやゲーム本体は必要ありません。件数は更新されるため、現在値は[生成された事典](reference/README.md)と[本文一覧](reference/DOCUMENTS.md)を参照してください。

## 手元のコピーで検索する

Python 3で、このリポジトリのフォルダから実行します。追加ライブラリやDBの準備は不要です。

```powershell
python -B tools/reference.py search 解雇
python -B tools/reference.py search 0x0055D8F6
python -B tools/reference.py search Vahren.exe+15D8F6
python -B tools/reference.py search ScriptEngine+0x1EED60
python -B tools/reference.py search T014 --json
python -B tools/reference.py callers 0x0055BC60 --json
python -B tools/reference.py callees 0x0055BC60 --json
```

アドレスはver0.67のVA、`Vahren.exe+...` は基準0x400000からの相対位置です。構造体と位置は `構造体名+0xオフセット` と書きます。`ScriptEngine` は研究用のレイアウト名で、原作のC++クラス名ではありません。古い本文の `Unit+185F4` のように `0x` を省いた表記は、`python -B tools/reference.py search Unit+185F4` と元の表記で本文検索します。構造体＋オフセット検索は、正式な辞書項目と本文の `0x` 付き局所表記が対象です。

`--json` は人向けページと同じ根拠・確度・制約を返します。通常の文字列検索は研究本文にも一致し、文書ごとの最初の一致行を表示します。文書は台帳の初出順で最大20件なので、表示が省略されたら研究IDや題名で絞ってください。詳細は[検索と追加・訂正の手順](reference/UPDATING.md)にあります。

## 根拠と未確認事項を読む

辞書の「実機確認」「静的確認」「テストのみ」「推定」は、元研究の確認区分を保っています。関係ごとの根拠には本文のパス・SHA256・行範囲を持たせ、個別ページから確認できます。関数の確度が高くても、全引数・全副作用まで確認済みとは限りません。

本文の文字列一致、アドレス言及、ファイル名の一致、回収成功は、それぞれ発見の手掛かりや保存状態です。動作の確定には使いません。過去の `STATIC`・`INFERRED`・`VERIFY`・合成テスト・`Golden`・`READY` の範囲も、元の記録に従います。古い報告と後日の訂正がある場合は、現在の事典・REFと訂正根拠を併せて確認してください。

原本と保存版の対応は[回収台帳](research/recovered/RECOVERY_LEDGER.tsv)、Git収録物のSHAは[SOURCE_MANIFEST.tsv](SOURCE_MANIFEST.tsv)で追跡します。部分回収・個人情報だけを伏せた保存版・同一内容の別名・未確認の参照先は区別して記録します。原作素材・生成DB・未取得の証拠までGitHubに揃っているとは扱いません。

## 分野から探す

| 分野 | 研究のまとめ |
|---|---|
| ユニット・EXP・訓練・召喚 | [REF_UNIT_EXP_SUMMON.md](REF_UNIT_EXP_SUMMON.md) |
| 技能発動後処理 | [REF_SKILL_POST_ACTION.md](REF_SKILL_POST_ACTION.md) |
| 戦闘AI・士気 | [REF_BATTLE_AI_MORALE.md](REF_BATTLE_AI_MORALE.md) |
| 戦闘乗っ取り・外部結果統合 | [REF_BATTLE_TAKEOVER.md](REF_BATTLE_TAKEOVER.md) |
| DAT・画面部品・詳細パネル | [REF_DAT_BEHAVIOR.md](REF_DAT_BEHAVIOR.md)、[REF_UI_SYSTEM.md](REF_UI_SYSTEM.md) |
| VM・context・時計 | [REF_SCRIPT_VM_CONTEXT.md](REF_SCRIPT_VM_CONTEXT.md)、[主要本文と旧説明の訂正](research/recovered/vm_dispatch_topic/README.md) |
| セーブの処理・通常セーブの形式 | [REF_SAVE_PERSISTENCE.md](REF_SAVE_PERSISTENCE.md)、[REF_SAVE_FORMAT.md](REF_SAVE_FORMAT.md) |
| ランダムイベント | [REF_RANDOM_EVENTS.md](REF_RANDOM_EVENTS.md) |
| RTSシナリオ | [REF_RTS_SCENARIO.md](REF_RTS_SCENARIO.md) |
| 旧シナリオ互換 | [REF_SCENARIO_COMPAT.md](REF_SCENARIO_COMPAT.md) |
| 戦略・内政・教育・商人・防衛 | [REF_STRATEGY_ECONOMY.md](REF_STRATEGY_ECONOMY.md) |
| 音声・Vorbis | [REF_AUDIO_VORBIS.md](REF_AUDIO_VORBIS.md) |

## 新しい発見を足す・誤りを直す

1. 事典と本文を検索し、既存の研究・同内容の別名・後日の訂正を確認する。
2. 本文を状態付きで保全し、研究ID・対象版・元の相対パス・原本と保存版のSHA・確認範囲・未確認事項を台帳に記録する。
3. 根拠を確認した関数・フィールドを `symbols.tsv`・`structs.tsv` に採録する。読み書き等の関係は `reference/relations.jsonl`、明示的な訂正は `reference/corrections.jsonl` に出典付きで記録する。過去の誤説明は訂正済みと明示し、現在の解釈と並べて有効扱いにしない。
4. ページ・本文収録照合表を再生成し、根拠・ハッシュ・検索・収録許可を確認してGitHubへ送る。別コピーでも根拠を読めることを確かめる。

詳しい手順は[追加・訂正](reference/UPDATING.md)、[成果の保全と正式採録](RESEARCH_INTAKE_PROTOCOL_20261101.md)、[担当間の統合方針](KNOWLEDGE_CURATION_PROTOCOL.md)。未整理の候補は[取り込みキュー](research/intake/README.md)へ。保存できたことと正式な知識として採録できたことを分け、新しい研究も同じ流れで蓄積します。

## AI・統合担当へ

まずこの入口、対象の事典ページ、現在のREF、訂正と出典を確認してください。機械処理には `tools/reference.py ... --json` を使えます。本文の取得状態・局所的な所有者名・研究ID共有だけから、型や確度を自動確定しないでください。`UnitRuntime` のような研究用部分レイアウトは具体的なC++クラス同一性を保証せず、型 `unknown` は幅も未確定です。

書き込む場合は[同期状態](SYNC_STATUS.md)と[同期手順](SYNC_PROTOCOL.md)に従い、最新 `develop` と作業開始SHAを照合し、専用の作業ブランチで編集します。他担当のブランチ・原本は変更しません。元の解析を追加する場合は、認可済み研究PCの最新MASTER/HANDOFF・対象原本SHA・既存の保留範囲を確認します。

- [元目録](RESEARCH_SOURCE_CATALOG.tsv)と[現在の所在](research/recovered/current_inventory/README.md)は対象時点・範囲が異なります。
- [重複候補](RESEARCH_DUPLICATE_CANDIDATES.tsv)と[重複の検討](RESEARCH_DUPLICATE_TRIAGE.md)は手掛かりです。同じIDやバイト一致だけで原本を削除しません。
- [V9の未登録関数候補](GHIDRA_V9_COVERAGE_REPORT.md)と[研究分類の旧スナップショット](RESEARCH_INTEGRATION_SNAPSHOT.md)は、今の確定事実数や完了判定へ読み替えません。
- 個人情報・認証情報・ゲーム素材・生成DBは送信対象ごとに確認します。現在はPRIVATEのままで、公開への切替はまだ実施していません。

## 研究PC専用の解析環境

Ghidra・x32dbgへのラベル反映、元SQLiteを使う全文索引の再生成などは、原作と専用データがある研究PC向けです。[従来のPC専用手順と作業履歴](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/b070349917d2692c6a4e6498dc62e9aa3e5097ae/README.md)を固定版として残しています。そこにある旧件数・過去の完了記録・旧更新ルールは当時の情報です。現在の事典の利用・更新には上の入口と現行手順を使ってください。

拡張製品コードは関連する非公開 `HakushinExtensions`、研究知識とその根拠はこのリポジトリで管理します。
