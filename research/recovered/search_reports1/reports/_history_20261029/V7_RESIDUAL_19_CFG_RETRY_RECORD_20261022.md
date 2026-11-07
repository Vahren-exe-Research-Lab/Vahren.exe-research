# 残余19候補CFG監査の再試行記録

- 作業ID: `REDEV-V7-RESIDUAL19-GHIDRA-COMPILE-20261022-01`
- 初回失敗: Java補助メソッド `a(String)` に `throws Exception` がなく、GhidraのJavaコンパイルが `AddressFormatException` の未処理で停止。
- Ghidra起動コマンドは終了コード0でも、出力JSONは存在せず、成功とは扱わない。
- ログ: `V7_REMAINING_19_GHIDRA_CFG_20261022.console.log`
- 影響: `-readOnly` で検査したためGhidra・EXE・DBに変更なし。所有する新規Javaスクリプトの宣言のみ訂正。
- 再開: 出力JSON不在を確認し、新しいログ名で同一19候補を再監査する。現状は `RETRY_REQUIRED`。
