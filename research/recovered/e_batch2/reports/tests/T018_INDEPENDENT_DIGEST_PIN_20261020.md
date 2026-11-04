# T018｜監査原票の独立バイトSHA固定照合（2026-10-20 17:44 JST）
ID: E-OFFLINE-UNSYNCED-20261020-1744-T018-INDEPENDENT-SNAPSHOT-PIN-01 / E / T018・DEVLAB-006。
分類: STATIC DESIGN / SYNTHETIC TESTED / VERIFY。公式READY追加0、原作DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
【背景】既存T018投影再計算は監査出力に含まれないraw.original_exe_sha256等が変化しても、監査投影が不変ならREVIEW_ONLYになり得る。前回設計文書が既に限界を明記。
【今回新規】独立オフライン実装 t018_independent_digest_pin.py は事前に別保管された固定票とraw/audit/timeline実バイトSHA＋Python監査器ソースSHAを照合。現在値のみから同時生成したpinでは真正性を保証できない。
【検証】前回553+新19=572合成unittest PASS/FAIL0。zip展開後の独立全件再実行も572 PASS。原作EXEは実行していない。
【実装所在】E_OFFLINE_20261020_1744_T018_INDEPENDENT_PIN_DELTA_572.zip（ChatGPT作業環境）。基盤525＋先行差分553に重ねる。Python実装とテストはPC未同期。
【成功範囲】0=メタデータREVIEW_ONLYかつraw/audit/code固定SHAが一致、1=VERIFY/NOT_RUN、2=不正入力。どの終了値もGameplay PASSではない。
【重要制限】PINの独立した履歴保全、出典・合法旧UI観測、原作実EXE/DAT/SAVE/map/input/capture bytes、同run関連、旧新同条件および可視traceは未認証。pin/資料を一括改変できればこの検査単独では無力。
【Local台帳読戻し】正本MASTER全4484行の正式IDだけ抽出して595件一意/重複0 (A115/B228/C136/D116)。checkpoint195、DONE9/IN_PROGRESS21/VERIFY4は現行記載で未変更。
【B未統合照合】B 17:10 PC回収索引は従来25＋16:09追加1=26候補、全26 IDともMASTER正式登録0。B-20261019-1317-01はHANDOFF拒否、B-OFFLINE-20261020-0316-01はB1015-02と意味重複候補。非READYを正式昇格しない。
【Golden】最優先C-NB02旧sci1/po2/sp2→sp16のG0合法旧UI戦闘/G1直前SAVEと入力/G2実MAP・3side・Troop/Unit全NOT RUN。T024比較8/T020回帰6もNOT RUN。
【T019/REA】ZNM倍率、cook_heal、po/poo、GameClear、重複角度key等VERIFY。REA初期16候補STATIC15/TODO1、新疑似コード対ASM確定差分0。
【DEVLAB受入】監査投影一致・固定票の独立履歴・旧実ファイルSHA・合法旧UI観測・SAVE→攻撃指示差・G2名簿・old/new同初期条件を独立ゲート化。担当直接送達/受領未確認。
【所有権/制限】PC側は本E所有tests新規設計文書だけ保存。MASTER/他owner/REA/DEV/原本/Git/push/Work/automation不変更。既安全拒否の元操作を迂回・再提出しない。
【次回】合法旧C-NB02 G0→G1→G2一次観測導線を優先。pin実装をPCへ同期する前には最新版MASTER・T018・RUN CAPACITYと既存検証器を再読して重複確認。
