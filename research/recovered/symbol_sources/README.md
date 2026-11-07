# 辞書から参照される研究本文の回収

symbols.tsv / structs.tsv の出典列に明記されたdata/*.mdを入口に、原本相対パスと現在SHA256を既存Git管理ファイルの内容SHAと比較した。今回13原本の同一バイト本文は見つからなかった。名前の相違だけで未収録と判定せず、既存の受付本文と現在REFも照合した。

[台帳](SYMBOL_SOURCE_LEDGER.tsv) は10件の原本一致回収と3件の既存資料リンクを区別する。文書が回収されたことと、原作の命令やゲーム挙動を新たに検証したことは別の状態。旧本文のSTATIC/INFERRED/VERIFYと未検証条件を保持する。参照される原作PE、データ、probe、native windowは取得していない。

## 現在の解釈と訂正

- 訓練map初期化・full-range消去・partial helperは [現在のユニット/EXP事典](../../../REF_UNIT_EXP_SUMMON.md) 第6節を併読する。通常の全消去がpartial helperを必ず通るとは扱わない。
- 12Hの候補順位報告の「同点は同じ順位」という一般化は、13Hの固定anchor訂正を優先する。2位以下の同点も要素ごとに順位値が減る例を本文に保存した。[訂正本文](T013_DUAL_SCORE_SORT_ANCHOR_TIE_CORRECTION_NATIVE_20261031_13H.md)
- 16Hの元命令窓の終端はinclusiveとして現在REFで照合済み。ここで再計算した結果ではない。[現在の戦闘AI事典](../../../REF_BATTLE_AI_MORALE.md)
- 乱数record+0x28、候補+0xA14、最終targetを混同しない。19Hの-4..+3は通常の整数化を仮定した範囲で、実機分布ではない。[19H本文](T013_CANDIDATE_A14_PER_NODE_RANDOM_SCORE_NATIVE_20261031_19H.md)

## 既存資料をリンクしたもの

- 17Hのローカル原本には個人絶対パスがあるため原文を複写していない。[既存E担当の受入結果](../../intake/E/E-AUDIT-20261031-17H-T020-T013-DRAIN-RESTORE-CAP-GATE-01.md) と現在REFへリンクする。E本文は上流B原本の全文ではないため、その後、個人パス接頭辞1件を置換した[技術本文の全文整形版](T013_INPUT_DRAIN_RESTORE_LIST_CAP_NATIVE_20261031_17H.md)を追加回収した。[整形証跡](SYMBOL_SOURCE_17H_REDACTION.tsv)に原本と保存版SHAを記録する。
- 11月1日13Hと14Hは、原本SHAと再利用可能な根拠を記載する既存のB担当本文へリンクし、別本文の重複追加を避けた。[13H](../../intake/B/B-OFFLINE-20261101-13H-T011-T024-DISTANCE-SORT-MODE-GATE-01.md)・[14H](../../intake/B/B-OFFLINE-20261101-14H-T011-T024-DISTANCE-COMPARE-BOUNDARY-01.md)
- パネルとFINDINGSは既存の回収版を使う。[パネル](../DAT_UI_V4_STATUS_PANEL.md)・[FINDINGS回収範囲](../findings/README.md)

## 回収本文

| 研究本文 | 現在の取り扱い |
|---|---|
| [T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md](T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md](T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md](T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T013_DUAL_SCORE_RANK_FIELD_NATIVE_20261031_12H.md](T013_DUAL_SCORE_RANK_FIELD_NATIVE_20261031_12H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T013_DUAL_SCORE_SORT_ANCHOR_TIE_CORRECTION_NATIVE_20261031_13H.md](T013_DUAL_SCORE_SORT_ANCHOR_TIE_CORRECTION_NATIVE_20261031_13H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T013_KIND8_RANDOM_PAYLOAD_QUEUE_NATIVE_20261031_15H.md](T013_KIND8_RANDOM_PAYLOAD_QUEUE_NATIVE_20261031_15H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T013_BUCKET_LIST_MERGE_COMPARATOR_NATIVE_20261031_16H.md](T013_BUCKET_LIST_MERGE_COMPARATOR_NATIVE_20261031_16H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T013_CANDIDATE_A14_PER_NODE_RANDOM_SCORE_NATIVE_20261031_19H.md](T013_CANDIDATE_A14_PER_NODE_RANDOM_SCORE_NATIVE_20261031_19H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T013_UNIT18654_LIST_WRITER_ERASE_NATIVE_20261031_20H.md](T013_UNIT18654_LIST_WRITER_ERASE_NATIVE_20261031_20H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |
| [T013_FIRST_HEAD_SENTINEL_COORD_BRANCH_NATIVE_20261031_21H.md](T013_FIRST_HEAD_SENTINEL_COORD_BRANCH_NATIVE_20261031_21H.md) | 原本SHA一致。歴史資料として保持、現在REFを併読 |

原作解析ではなく研究本文の回収と照合を行った。HOLD21の保留名に該当する原本は選ばず、本文中の禁止領域へアクセスしないという運用記録だけはそのまま保存した。未回収の証拠と個人パス入り原本は台帳のlimitationsに残す。今後も出典列の略記や別名を順次照合する。

17Hの全文整形版は、注記と個人パス接頭辞の置換以外の技術本文を保持している。E受入要約の部分リンクと、整形済み全文の収録は別々の台帳行として保持する。

GitHubの[収録コミットdd55d1d](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/commit/dd55d1d4113f5d71d1aab30147f09347aa92845a)から取得し直し、17H全文整形版は注記ブロックと個人パス接頭辞1件の置換以外の技術本文が変わっていないことを確認した。完全一致10本文も原本とのバイト一致を再確認した。
