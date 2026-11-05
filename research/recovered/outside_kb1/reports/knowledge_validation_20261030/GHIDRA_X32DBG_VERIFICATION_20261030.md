# Ghidra / x32dbg 研究知識ベース反映検証（2026-10-30）

作業ID: KB-INT-01-20261030。原作EXE・DAT・MAP・SAVE、正本Ghidraプロジェクトは変更していない。
検証環境: Ghidra 12.1.4、32-bit x32dbg（ローカル導入済み）。検証は解析済みプロジェクトの複製と生成スクリプトだけで実施。

## 1. Ghidra: 実機反映 PASS

- Ghidra既存プロジェクト（解析済み）の完全な複製を dev_lab/_work 配下に隔離。元プロジェクトは未変更。
- headless の noanalysis モードで ApplyKnowledge.java を一度だけ適用・保存。
- 成果: 関数名更新820件、関数新規作成2件、ラベル追加159件、通常コメント1677件、短いコメント209件、構造体7種類、失敗0件。
- VerifyKnowledge.java を readOnly モードで実行し、下記6関数の名称と知識コメントをすべて確認。
  - 0x48D6A0 Battle_ConstructScene
  - 0x550E70 Damage_ComputeAttackDefense
  - 0x54E7B0 Summon_SpawnFromSkill
  - 0x57B870 Ai_SearchTargetCadence
  - 0x460000 Save_WriteFullState
  - 0x5559B0 Window_HandleWin32Messages
- 0x48D6A0 のGhidra関数範囲は 0x48EA5A で終わり、そこに C3（RET）を確認。古い短すぎる境界はこの複製には存在しない。
- 再適用テスト（readOnly）: 関数名の再変更0、新規関数作成0、失敗0。6/6の確認結果も不変。
- Ghidraへ確実に反映できたことを示す結果であり、原作ゲーム動作確認の代わりにはならない。

## 2. x32dbg: 生成スクリプト構文 PASS / GUI反映は未完了

- x32dbgの公式コマンド形式 lbl address, label および cmt address, comment と生成形式が一致することを確認。
- 生成されたラベル978件、コメント560件を検査し、アドレス・辞書参照・引用符・命令構文のエラー0件。
- 旧生成処理には同一VAのコメント命令重複が12件存在し、後続のcmtが先行コメントを上書きする問題があった。
- build_kb.pyで手書き説明と旧コメントを統合し、同じVAにcmtを一度だけ発行するよう修正。短いコメントは元の説明と結合し、先行文の消失を防止した。
- tools/verify_debugger_exports.py と tools/test_debugger_exports.py を追加し、以後の生成時に同じ不具合を検出できる。
- 既存のx32dbgがVahren.exeをデバッグしているときに、元セッションのUI・保存状態は操作しなかった。
- 別コピーのQA実行ファイルに対して独立したx32dbgインスタンスで自動スクリプト適用を試したが、QAプロセスは終了し、検証用DBを生成できなかった。
- さらに確認時点では元々動作していたx32dbgのプロセスも終了していた。両者の関係・原因は不明であり、こちらから既存プロセスを終了する操作は行っていない。
- 既存セッションへの影響を否定できないため、x32dbgの再起動・自動再試行は行っていない。GUIの全件インポートは PASS としない。
- 失敗記録: 作業ID KB-INT-X32-QA-01、状態 BLOCKED (GUI)、未完了: DB保存結果・表示結果の確認、再開位置: 既存デバッグ作業の終了と明示的な保護手順を確認後、分離した実行環境のみで再試験。
- 原作・セーブへの書込なし。隔離したQA用の実行ファイルとログ以外は意図的に編集していない。

## 使用手順（残りの手動UI検証）

1. x32dbgでゲームを起動・一時停止。既存のラベル・コメントDBをバックアップする。
2. Scriptタブで generated/x32dbg_labels.txt と generated/x32dbg_comments.txt を順に読み込む。
3. VA 0x54E7B0 (RVA 0x14E7B0) と VA 0x550E70 (RVA 0x150E70) の表示を確認する。
4. 既存の個別コメントが消えていないか確認する。古いDBが必要なら独立した試験環境から実施する。
5. x32dbg自体の起動停止の原因は未解決。元のデバッグセッションを無断で操作しない。

公式仕様: https://help.x64dbg.com/en/latest/commands/user-database/labelset.html
公式仕様: https://help.x64dbg.com/en/latest/commands/user-database/commentset.html
公式CLI: https://help.x64dbg.com/en/latest/commands/script/scriptexec.html

## リポジトリ保存時の復旧ログ

- 作業ID: KB-INT-GIT-01、日時: 2026-10-30 JST。
- 最初のcheckpointは、Windows PowerShellのSet-Contentが書いたUTF-8 BOM付きローカルGit管理メタデータをjson.loadsが処理できず、JSONDecodeErrorで停止した。
- 未完了範囲: 当該checkpointコミットとGitHubへのpush。失敗時点でソースはステージ前・pushなし。原作と既存研究正本に変更なし。
- 修正: sync_knowledge.pyのメタデータ読取をutf-8-sigにし、BOM有無双方を許容する。強制Git操作や別経路での拒否迂回なし。
- 再開位置: 安全性の再監査、単体テスト、checkpoint実行、private GitHubの作業ブランチSHA照合。
## 2026-10-30追試：領地名2件と隔離x32dbgの最小動作

- 作業ID KB-INT-REMAINDER-20261030。別AIのローカルcommit 4f74996e...から、0x419938 SpotName_DrawTextReady と0x597960 Spot_GetDisplayName を統合用ブランチに追加。元の作業ブランチは無変更。
- symbols.tsv は365件（旧363＋2）。V9関数先頭・コード所有・重複・確度・出典の検査でエラー0／警告0。
- Ghidraの解析コピーへ再適用：関数名更新0、ラベル159、コメント1678、短いコメント209、構造体7、失敗0。
- VerifyKnowledge.javaで0x597960の関数名とKBコメント、0x419938のラベルとKB pre-commentを確認。7関数/7件すべて合格。
- 0x48D6A0の終端0x48EA5AにRET/C3、UnitDef構造体を再確認。原本Ghidraプロジェクトは未変更。

### x32dbgの独立した最小動作検証

- 旧ゲームコピーのQAが途中終了していたため、実際に稼働中のゲームを操作しない方針を維持。
- Windows 32bit Notepadコピーを専用 -userdir のx32dbgへ渡し、lbl・cmt・dbsave の3命令を検証。
- x32dbg自身が作成した .dd32 JSONから、ラベル1件・コメント1件を正確に保存できたことを確認。
- 証拠：dev_lab/_work/kb_x32dbg_smoke_20261030/smoke.dd32、SHA256 7CCD7E09306CA7906DB69763CCFDDACFB26C92626108C22CD340EDEF0EDB9307。
- テスト用x32dbgは指定27秒で終了しなかったため、そのテスト用プロセスのみを停止。既存のゲームや他のデバッガに終了命令を送っていない。
- 直後にゲーム終了を疑ったが再確認により同一PID 4496・同じ起動時刻で継続稼働していた。暫定報告「ゲームが終了した」は訂正する。
- 既存x32dbgユーザーDBは変更していない。元データはx32dbgの圧縮形式であることを確認。
- tools/export_x32dbg_database.py はx32dbg実機のサンプル形式に合わせて generated/x32dbg_knowledge_import.dd32 を作る。980ラベル、562コメント。重複・JSON readback検査PASS。
- DBには個別ゲームのMurmurHashを含めていない。実機Vahren.exeへの980件の反映は未検証。
- 既存の手動ラベルやコメントを上書きする可能性があるため、自動的にdbloadを実行しない。ユーザーDBのバックアップを作ってから手動でインポートする。
- 未完了：実際のVahren.exeをx32dbgで開いた状態での全件表示とユーザーDBの衝突検証。ライブゲームが動作している間は実施しない。
- x32dbgのDB仕様根拠：https://github.com/x64dbg/x64dbg/blob/development/src/dbg/database.cpp
