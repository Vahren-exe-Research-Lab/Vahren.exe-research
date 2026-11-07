# 23時台 REA独立静的調査｜保存・拒否・再開記録
研究ID: REA-LOCAL-20261025-2334-P0-FLS-RETURN-ABI-REFUSAL-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY
RECOVERY-ID(1): REA-RC-20261025-2334-FLS-FUNCTION-QUERY-SAFETY-01
RECOVERY-ID(2): REA-RC-20261025-2334-FLS-AUDIT-EXEC-SAFETY-02
接続: Windows Local成功。23:34頃active.lock=false。source SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
DB SHA 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。
書込先: このdecomp_task配下の新規3ファイル + 本記録。既存正本/キュー/ログ/他レーン/原本/Git/スケジュールは変更なし。
保存済み: REA_20261025_23H_P0_FLS_ABI_RECOVERY_STATIC.md（direct readback成功）
保存済み: REA_20261025_23H_P0_FLS_ABI_EVIDENCE.json（direct readback成功）
保存済み: REA_20261025_23H_FLS_WRAPPER_AUDIT.py（direct readback成功）
制限: helper 0x5BC860/0x5BC57C/0x5BC7F2に対する複合関数検索はsafety check拒否。結果なし・再試行なし。
別制限: 新規AUDIT.pyのPython実行はsafety check拒否。**作成のみ／NOT RUN**。8/8などのPASSを主張しない。同じ解析操作を別shell/tool/pathへ切替していない。
実行したのはsearch.py既存DBの絞込検索と保存・読戻しのみ。独立Capstone監査0件、新規5-method証拠0、新規VERIFIED0、原作Golden実測PASS0。
新観察: 0x005BC522はGhidra上voidだが0x005B7CDD callerはEAXを検査するため、戻値ABIと動的関数ポインタ0x0068E010をVERIFY対象として分離。
旧正式64/64は11日の保存済み同期記録（新規計上なし）。13/14時OFFLINE-UNSYNCED維持。
次の合法作業: 既取得証拠をレビューして他レーンへ未統合を通知する。拒否された関数検索/監査実行は迂回しない。ユーザーまたは安全側が許可条件を明示するまでNOT RUN。
PC負荷観測: 空きRAM11.41GiB、CPU20%（単発観測）、研究全体時間未測定。
