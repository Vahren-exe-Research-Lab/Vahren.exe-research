# dirty_docs1 — bounded historical worktree snapshots

指定9件から完全一致本文6件・295,628バイトを保存。全体保留3件、既存/今回内SHA重複0件、私有パス編集0件。元のdirty状態を修正・再開・公開したものではない。

入力baseline190bf0987f4a7d14f6e2d0f38fc703996d15b9ec、共有台帳1839行。選定表SHA256 `32820f9aa19cb9120b2843cf0960029cb2b921625cff53b17a3faab38a7ea509`、入力台帳SHA256 `f1ca410fb520081320a5e62b7fc70aac6032bcb3b0dc7a63c81cd4aae0e6921b`。9件のSHA256・サイズ・mtimeが直前選定値と一致し、原本配下包含と再解析ポイント不在を確認。原本・共有台帳・辞書・コード・Git状態は変更していない。入力時点の受領票であり、後の親統合後も共有ファイルが不変という主張ではない。

完全確認: AI REF LF1–228、音声REF LF1–221、SYNC_STATUS LF1–67、modecache取込README LF1–280。取込READMEの残る二版LF1–233/LF1–244は、全文確認済みmodecache版との同一行バイト区間を再利用し、相違する全区間を直接確認。REVIEW_SPANSは各版の全物理行を欠落・重複なく被覆し、同一区間SHAを示す。以前からある未変更本文もこの確認対象に含め、dirty差分だけを本文全体の代わりにしていない。

二つのsymbols.tsvは既知保留内部要約を持ち、TAKEOVER REFは0x4C28D0のTask巡回/NULL経路の具体的内容を持つため全体保留。ヘッダー・見出し・限定パターンの非連続確認範囲はDEFERRED/REVIEW_IDENTITYに記録し、全文ハッシュ計算を全文審査と数えていない。本文・独立抜粋・dirty hunkを保存しない。除外された旧許可リスト.pyは取得していない。

意味差分の確認は適格な6文書だけに限定した読取専用Git diff（--no-ext-diff --no-textconv、fsmonitor無効、任意ロック無効）で実施。追加AI節の3キー0x56AB20/0x569360/0x5699C0、音声節の3キー0x5D48E0/0x5CFF10/0x5CFA10は前回独立一次資料から採用済みの6件。その他は履歴cursor/源流・入力ABI・key-zero等の出典付きクロスウォークであり、この文書だけから追加の一次根拠付きcore採用候補は確定していない。該当取込READMEのE09/10/11等は資料名/IDのポインターのみで、保留された受入本文を再構成していない。

CURATION_READY_STATIC/UNMERGED、manifestのWinError5、過去のPASS/READY/原作命令再確認/ff-only/readback等は当時の著者主張として残す。今回の保存によってpublication gateが通ったことや、原作・ABI・所有者・全体不変条件が再検証されたことにはしない。原作/Native/リンク先/スクリプト/資産/DB/ログ/証拠JSONは取得・実行していない。

検証: 入力9件のpin安定、root1839と今回内のSHA重複なし、受入6/全体保留3、完全版6件の保存後バイト一致、二版の全行レビュー被覆を確認。OUTPUT_MANIFESTは自身を除く全出力のサイズ・SHA256を列挙して照合。
