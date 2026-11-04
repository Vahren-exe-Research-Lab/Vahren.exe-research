# T018｜原票と監査出力の投影整合性（2026-10-20 16:51 JST）
ID: E-OFFLINE-UNSYNCED-20261020-1651-T018-AUDIT-PROJECTION-01
Owner: E / T018、DEVLAB-006向け受入設計。分類: STATIC / SYNTHETIC TESTED / VERIFY / NOT RUN。公式READY対象外。
【問題】独立CLI e_cli_verdict_guard.py は「records=[{status:REVIEW_READY}], review_ready=1」だけでmetadata REVIEW_ONLYを返す。原票未照合の要約でもメタデータだけを誤受入し得る。原作ゲームのバグではない。
【オフライン修正】t018_audit_binding.py をChatGPT作業環境の独立コピーへ追加。旧golden_preflight.inspectとt018_timeline_audit.inspectをraw JSONから再計算し、claimed auditの全フィールドをnested型を含めて比較する。余分/欠落/改変のある監査をVERIFYとする。
【重要な残余リスク】旧監査出力にはrawのバイトSHAが入っていないため、同一監査投影を生む別の原票でも再計算一致する。今回のCLIは現在読み取ったraw/監査JSONのバイトSHAを結果へ出すが、「監査当時のrawと同一」は未証明。recomputed_report_equalは真正性・動作一致の証明ではない。
【検証】既存525+追加28=553 Python unittest合成PASS/0 FAIL。差し替えJSONで旧ガードREVIEW_ONLY→新検査VERIFYを再現。現行NOT_RUN原票の再計算結果NOT_RUN、CLI終了コード1を検証。
【ChatGPT成果】E_OFFLINE_20261020_1651_T018_AUDIT_PROJECTION_DELTA_553.zip（7 entries / SHA256 78519f55efc0ee1832f03d7186fafba0f5692717b1ea4ea63ca368f167f09bd0）。基盤はE_OFFLINE_20261020_1547_T018_TIMELINE_GUARD_525.zip。追加プログラム/テストはPC未転送。
【PC正本再照合】MASTER checkpoint195 / READY595 A115 B228 C136 D116、595 ID unique/重複0をLocal読み取りで再計数。DONE9/IN_PROGRESS21/VERIFY4は現行MASTER記述、状態を変更していない。
【Golden】C-NB02旧原作のsci1/po2/sp2→sp16 G0合法開戦、G1直前SAVE SHAと操作、G2実MAP/3side/deployed Troop/UnitはNOT RUN。T024比較8件・T020作者変更5系列6条件NOT RUN。原作Gameplay actual PASS0、strict MATCH0。
【受入設計】DEVLAB-006は監査JSON単体やCLI終了0で成功判定せず、case_id/run_id、old rawとold auditと各SHA、timestamp、actual file bytes、G2 relational roster、G1順序、old/new共通初期条件・可視traceを別段階で照合する。不可視情報はUNKNOWN/INELIGIBLE。合成テストを互換性PASSに換算しない。
【所有境界】本ファイルのみE所有として新規保存。MASTER正式READY/checkpointは更新しない。他lane/rea_lab/dev_lab/原本/Git/push/Work/automation変更なし。過去T018表境界安全拒否の元操作は再提出・迂回していない。
【同期残件】PCにあるのはこの日本語設計・実装引継ぎのみ。実装ZIP/28追加テストはPC未同期、DEVLAB直接受領なし。次回最新MASTER・T018・RUN CAPACITYと既存検証器の重複確認後、限定取り込みの可否を決める。
【限界・次優先】原作EXE未起動、PC負荷CPU率は不明、Local terminal session0。C-NB02 G0→G1→G2一次証拠を最優先。次回は本IDの重複、raw-byte固定、原票真正性を優先。
