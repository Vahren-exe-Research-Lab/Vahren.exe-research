# REA 定期研究の保存結果メタデータ

2026年10月9日・11日の21回の保存結果を回収した。原作の機械語・疑似コード・素材本体を収録したものではない。旧レコードの `VERIFIED` は当時の5方法の取得状態として保持する。今回の原作再検証、ゲーム実測、関数の意味の新規確定を表さない。

## 保存内容

- `runs/<runId>/RUN_RESULT.json` 21件は原文とバイト一致。原本・収録先SHAは [回収台帳](SCHEDULE_RECOVERY_LEDGER.tsv) に記録した。
- 最新同期ログ1件は個人絶対パス2項目を研究ルート相対表記に置換した派生版。その他の値は保持した。元SHAと派生SHAを区別する。
- JSONの全フィールドを構造検査し、日時、関数VA、担当Task、短いタイトル、状態、証拠ID、取得文字数・件数、エラー分類のみであることを確認。参照された証拠IDから原作出力を取得していない。

## 件数と保存状態の照合

21 RUN_RESULTは67レコード、66種類のVAを含む。62種類のVAにVERIFIEDがあり、4種類は関数境界不一致によるVERIFY。最初の0x550D80のタイムアウトは後続runで成功している。

最新同期ログは64/64、reviewedRuns21、verify0と記録している。キューの保存版を照合した結果、RUN_RESULTのVERIFIED62種類に、以前からの完了扱い2件（0x550E70と0x576E30）を加えると、キュー64件と重複なく一致した。4件のVERIFY旧候補はcandidate_revisionsの元候補と一致し、置換後の4関数は62件に含まれる。[数値照合と入力SHA](ACQUISITION_COUNTS.json)・[キュー保存版](snapshots/QUEUE_20261105_READBACK.json)を参照。これは取得記録の数値整合であり、原作の意味・動作を新しく検証したことではない。

RUN_RESULTには研究本文パスや研究IDのフィールドがなく、methodsごとのevidence_idだけがある。以下の公開済み旧資料との対応を入口に、証拠と本文の対応を補う必要がある。現在のINDEXでrun IDが見つからないことは、発見がGitHubに存在しないことの証明にはならない。

## 既存GitHub資料との対応

照合元はPR16のHEAD `222ace73853916d51dad7c6250cd5772fcfca10f`。旧資料A〜Dの対応表は研究履歴の要約であり、原作出力5種の完全保存を意味しない。

| run ID | PR16旧資料 |
|---|---|
| `20261009T194358486Z` | [A](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_A.md) |
| `20261009T212627835Z` | [C](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_C.md) |
| `20261009T220712454Z` | [A](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_A.md) |
| `20261009T223622536Z` | [D](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_D.md) |
| `20261009T224617297Z` | [D](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_D.md) |
| `20261009T225741694Z` | [A](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_A.md), [B](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_B.md), [C](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_C.md) |
| `20261011T113414092Z` | [B](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_B.md) |
| `20261011T114202395Z` | [D](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_D.md) |
| `20261011T124000308Z` | [C](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_C.md) |
| `20261011T133432356Z` | [A](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_A.md) |
| `20261011T144115307Z` | [A](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_A.md), [C](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/222ace73853916d51dad7c6250cd5772fcfca10f/research/intake/REA/REA_20261010_31_LEGACY_UNKEYED_AND_CORRECTION_C.md) |

残る10runは上記A〜Dのrun ID検索では直接対応が見つからなかった。そのうち1runは初回タイムアウト。関数VA自体は別の辞書・研究本文で既知の場合があるため、未発見・未保存件数として数えない。

## 継続して回収するもの

方法別evidence_idに対応する原作出力、研究IDと本文パス、5方法の証拠ハッシュは未回収・未検証。分母64との数値関係は上記の保存版キューで照合した。保留原資料への迂回取得はせず、取得可能な担当資料・公開済み訂正から照合する。

0x471AF0/0x471D20の旧タイトル「外交」は、現在のREF_SAVE_FORMAT第7節・第9節のターン進行状態という訂正を参照する。旧runのタイトルを現在の意味へ無条件に昇格させない。

キュー本体のVERIFIED16・TODO48と、同期ログのSTALE_RENAME_DENIEDを履歴として保持した。更新に失敗した状態をそのまま現在の未研究件数に使わない。参照されるtmpやinfo.jsonの原作出力本体は取得していない。

## GitHub取得コピーの検証

[収録コミットdd55d1d](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/commit/dd55d1d4113f5d71d1aab30147f09347aa92845a)を別クローンへ取得。779項目のマニフェスト、回収台帳62行の保存版SHA、うち原本一致56行の内容、21run・67記録、673フィールド表記の検索を確認した。初回VERIFYと後続VERIFIEDを両方保持し、キュー64件＝RUN_RESULT62種類＋既存2件の集合関係も入力SHAとともに再照合した。[PR #24](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/24)に変更範囲を記録する。原作出力本体や意味・動作の新規検証は継続課題。
