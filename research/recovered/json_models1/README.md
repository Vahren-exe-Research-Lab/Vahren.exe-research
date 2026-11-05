# json_models1 — authored finite models and audit records

指定54パス: 受入53行（新規完全一致本文49件・同一本文alias4件）、全体保留1件。新規保存本文1,776,113バイト。私有パス編集・文字コード変換0件。既存root1877とのSHA一致0件。OFFLINE_UNSYNCEDの4件は先頭の同期配置4件と完全SHA一致し、一つずつの保存先を共用。

入力baseline68a9a917d651dffe23b2e1ee44ae7297f67b3dc7、共有台帳1877行。選定表SHA256 `70abaeda68f4ce2c56ea02c1514814595392d696ea9510b627fe5c84987f2b1d`、入力台帳SHA256 `523d29ac58a0569ac960967365283732a7f8bba2c993bf12a670f87b3a5b4270`。54件の現行SHA・サイズ・行数が過去catalog pinsと一致し、今回の読み取り前後のサイズ/mtime安定も確認した。後の親統合後も共有ファイルが不変という主張ではない。

主題・ヘッダーを先に確認。既知E Oct28_13H NULL-ECX研究のfixtureは先頭600文字（完了LF1–6・LF7途中）で研究IDと元研究を特定し、配列を解析せず全体保留。DEFERREDには識別と境界だけを記録し、本文・抜粋は保存していない。

残る49種はstrict UTF8 decodeとJSON parseで全ノードを読み、全キー・重複を除いた全ての文言・配列次元・object形状・数値範囲を構造化確認した。case ID/ハッシュは形式・個数・重複・値域として確認。全物理LFを手作業で一行ずつ読んだという記録ではない。REVIEW_IDENTITYにノード型別件数、配列長、数値範囲、全文言集合SHA、全キーと確認方法を固定。重複object key・非標準NaN/Infinity定数なし。期待値計算・モデル・ランナー・ケースの実行はしていない。

構成上の確認例: training216行は4×3×3×3×2、EBX72行は3×3×2×2×2、off比較392行は7×7×2×2×2、最大704行は初期count11種×4操作の長さ3全64列。記録された軸でのCartesian被覆を確認しただけで、期待値の正しさ・実機到達性・原作の網羅性を証明しない。rect480行や他の境界/不正型/negative fixturesも条件付き合成データ。wrapper辺・短い命令値/hash窓は著者の限定静的記録で、全native dump・ゲーム資産ではない。inventory133件はファイル名・サイズ・hashのみで参照先を読んでいない。短いbase64はsynthetic/fake fixture文字列で原作資産ではない。

E14H decide fixtureは既に受入済みB14保存報告（b_batch11/data/T028_DECIDE_SELECTOR_FLAG_WEIGHT_NATIVE_20261028_14H.md、SHA0c7954ec4979f19e2d74ee80bf9e0dce7b189d00beaae32ccbec5a21acdbf046）の限定LF1–20と出典を照合。flag75/77の仮定されたcaller結果ラベルとflag74/other1dのdecide3/500・decide11/10|25だけで、保留E13のECX初期値・cleanup前native値/ゲート算法を再構成していない。保留52は追加取得していない。同じVAを理由に範囲全体を保留・採用することもない。

G0/G1/G2結合、source lineage/時相、同一アドレス世代、条件付きAI・tree/counterの有限ケースと受領記録であり、新規発見件数ではない。PASS/READY/native verified/実行済み等は当時の主張。None/unknown/未観測/NOT_RUNを維持し、型・ABI・UnitRuntime別名・原作挙動・Golden・正しさを昇格しない。原本、共有台帳、辞書、コード、Gitは変更せず、リンク先native/Library/コード/ログ/原作/資産/DB/アーカイブ/他ケースは取得・実行していない。

検証: literal包含/再解析ポイント、pins・安定性、root1877/バッチSHA重複、53受入/1保留/49本文/4aliasの整合、保存後49本文全バイト一致、受入53保存先SHA、strict JSON構文と構造化確認、OUTPUT_MANIFESTの全出力サイズ/SHAを確認。manifest自身は一覧から除外。
