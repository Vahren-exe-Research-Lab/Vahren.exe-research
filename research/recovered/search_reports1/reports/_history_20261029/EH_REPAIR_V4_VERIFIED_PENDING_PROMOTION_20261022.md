# 迫真戦記ver0.67｜V4 EH修復は検証完了、PC標準入口の切替は権限拒否で保留

## 最終状態（2026-10-22 02:43:54 JST再検証）
- 作業ID：`REDEV-EH-ORPHAN-REPAIR-20261022`。
- **修復済み**：独立Ghidra `Hakushin067_EHRepair_20261022.gpr`、V4統合DB、V4検索CLI候補、最終オフラインZIP。
- **未切替**：PCの `search_current.py` と `CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` はV3のまま。
- V4マニフェストのACTIVE表記は、完成したV4パッケージ内で使う定義。PCの標準入口がV4に切り替わったという意味ではない。
- 元EXE・元Ghidra・前の修復済みGhidra・V3 DB・ゲーム・DLL・セーブ・戦闘記録器・他レーンは変更していない。

## 今回修復したこと
未所属E8直接CALL 2,040件のうち1,405件を、952個のコンパイラ例外処理ハンドラに対応付けた。既存のゲーム関数へ無理に結合せず、独立関数として登録。952件すべてGhidra再起動後の保存・再逆コンパイルを確認。
- 未所属E8：2,040→635件。未所属JMP：984→32件。
- 内部関数：10,274→11,226（増分はコンパイラ補助処理であり、ゲーム機能952個の解明ではない）。
- 参照総数243,670件とPE再配置57,921件は維持。所有関数を3,309参照／PE関連2,043レコードで更新。
- ネイティブABI検証済みは引き続き3件だけ。EH関数はABI未認証として明示。

## 証拠と検証
- 原PE命令・1,091登録PUSH・943 FuncInfoテーブルを独立照合。
- Ghidra全参照、全関数範囲、PE再配置の全行照合PASS。旧関数と既存ABIの内容は保持。
- CLI14/14、最終ZIPの展開後9コマンド、メタデータ検証器7/7テストPASS。
- 最新確認 `V4_EH_PENDING_PUBLICATION_FINAL_CHECK_20261022.json`：旧V3の正常性、V4のファイルハッシュ、両Ghidraの内容、V4検索を再確認済み。

## 切替の拒否・保留記録
失敗：検証済みV4候補で既存 `search_current.py` を置き換える `os.replace` が **WinError 5 / アクセス拒否**。最初の置換で停止し、現行ファイルの変更は発生していない。旧入口のハッシュと旧V3検証器PASSを再確認した。
記録：`CURRENT_V4_EH_PUBLICATION_20261022.json` は `PUBLICATION_FAILED_ROLLED_BACK`。
読み取り専用のACL調査ではCodexSandboxUsersにReadAndExecuteが表示された。権限設定・所有者・昇格・安全制限を変更して回避していない。
既存の公開スクリプトを同じ条件で繰り返さないこと。実際に書込み／置換が許可されたユーザー環境で、最新版の内容・競合・ハッシュを再照合してから標準入口を切り替える必要がある。

## 切替を行わずに検証済みV4を読む方法
保存フォルダ：`[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index`
```powershell
python -B .\search_current_V4_EH_CANDIDATE_20261022.py stats
python -B .\search_current_V4_EH_CANDIDATE_20261022.py function 0x005E7988
```
V4 Ghidraは一つ上のフォルダの `Hakushin067_EHRepair_20261022.gpr`。標準ポインターを変えなくても、この別名を直接指定して参照可能。

## 他AIへ渡す検証済みオフラインZIP
`HAKUSHIN067_CURRENT_AI_OFFLINE_PACK_V4_EH_FINAL_20261022.zip`
28,110,138 bytes / 23ファイル。
SHA256：`F6BAE3380DDFA4B54871940D7E43CEE2C192DB07F473D0BD0162975B9450420F`
ZIP内の `search_current.py` とLATEST指標はV4を指し、展開先だけで検証・検索可能。原EXE・Ghidra本体・旧DBは同梱しない。完全ZIPはPC保存のみであり、クラウドへの全量同期は未実施。

V4 DB SHA256：`33D7CF2183DEF8A89091D76B625C135040B48EBC56465D365DDF320BFC015B71`
V4 Ghidra .rep fingerprint：`E5E5672BBAD096A41128F7733A258100B0316F609D263A7EC13E473554C30259`

**次回はこの保留記録から再開し、修復と全量解析をやり直さない。標準入口切替と残635件の調査を別タスクとして扱う。**
