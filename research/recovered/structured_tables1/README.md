# structured_tables1 — historical maps and matrices

指定21件（20 TSV・1 JSONL、原本合計152,816バイト）を全文確認し保存。19件は完全一致、2件は損失のない文字コード変換完全版。保存本文合計144,945バイト。重複・全体保留・私有パス編集は各0件。原本、共有台帳、辞書、コード、Gitは変更していない。

入力baseline24d3f3bfb1598d0b6ee1777f75ad59c5f079085a、共有台帳1855行。選定表SHA256 `cbc3d4a4238e38f4ee8429ad69a05f20ae84f29b0951dfa69825fe727861224d`、入力台帳SHA256 `5bcc558a32129d984b2408ec230b6162ee45ba2b928ae706c0729fc4486a561e`。21件とも過去catalogのサイズ・SHA・行数と一致し、今回読み取りのサイズ/mtime安定も確認。根拠・物理LF全範囲・文字コード・BOM・改行・役割・限界はREVIEW_IDENTITYに記載。後続の親統合後も共有ファイルが不変という主張ではない。

対象は著者の識別子一覧、短い分析句の対応表、限定プロパティグラフ、登録/handler/CFG/既定値抽出、boss guardの合成組合せ。原作ファイルやnative全ダンプを取り込んだものではない。T029はsiege_systemの攻城対応表であり、postbattle Castle保留本文とは別。CALLSITESの近傍guardはヒューリスティックで完全条件ではなく、厳密なelse/default分析はDEFENSE_POWER_SKILL_MATRIXに別記される。T033はscenario文字列のXREF分類でrsc3/rsc4表の内容ではない。

UTF-16 BOMのT009_NATIVE_INT_FALLBACKSとT010_BATTLE_CMD_MAPだけは、明示エンディアンでstrict decodeし、同じUnicodeをBOMなしUTF-8へ保存。CRLF/LF・全ての文字を保持し、改行変換・項目修正・再整形は行わない。ENCODING_RECEIPTSは原本SHA/サイズ/BOM/エンディアン、保存SHA/サイズと、元BOM+元UTF16への再符号化=原本全バイト・UTF8再読込=同一Unicodeの証明を記録。原本UTF16バイナリは公開出力に複製していない。

検索導線（新規採用ではない）:
- main opcode9 wait → handler位置0x004A17D8: T006_OPCODE_HANDLERS LF11。関数入口/ABIはこの表だけでは確定しない。
- troop opcode14 skillTroop: T006_TROOP_REGISTRY_INDEX LF26の登録XREF0x004B4645、T010_BATTLE_CMD_MAP LF15のhandler位置0x004B608F。登録位置と処理位置を区別。
- special parser if → callback pointer0x50A5E0: T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK LF7。per-key merge等や公開ABIは未証明。

T006_REGISTRY_RECOVEREDにはOPCODE_HANDLERSと異なる番号（例fadein22対21）が残る。歴史的抽出として完全保存し、無断訂正・自動採用しない。None、空欄、未解決文字列、CFGのU、footerも文字どおり残す。登録XREFをhandlerと誤認せず、表のowner/engine/Unit表記から正式型やUnitRuntime別名を推定しない。旧PASS/READY/確認済みという表記は著者の当時の主張で、今回の実行や確度昇格ではない。

検証: 21件のliteral包含/再解析ポイント検査、原本pins/行数一致、root1855とバッチ内SHA重複なし、全文確認、保存後全バイト/変換再現一致、JSONL21行の構文解析のみを確認。保留対象の具体的本体・依存本文や私有パスは確認されなかった。リンク先native/コード/ログ/スクリプト/原作/資産/DB/アーカイブ/ケースは取得・実行していない。OUTPUT_MANIFESTは自身を除く全出力のサイズ・SHAを照合する。
