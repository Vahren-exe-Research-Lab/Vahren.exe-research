# E 08H tool recovery: non-safety failures (2026-10-30)
RECOVERY-ID: E-RC-20261030-08H-T020-TOOL-PATH-AND-OUTPUT-FORMAT-01
Owner: E/T020。状態 OTHER / RECOVERED / 未保存の新規研究差分0 / 既存安全拒否とは別。
発生1: Local read_fileで旧rea_lab/headless_analysis/search_index/README.mdを要求したがENOENT。2026-10-29の既存整理でREADME/BUILD_MANIFESTの旧名称は非現行。安全拒否ではない。旧pathを作らず、既存の許可済み00_START_HERE_ACTIVE_RESEARCH.mdとCURRENT_ACTIVE_RESEARCH_STATE_LATEST.json、V9統合入口をread-onlyで確認。現行V9 state取得成功。ゲーム・DB・元資料変更なし。
発生2: 既存11本のT028検証器をPowerShellで一括再実行した最初の集計は、出力が一律JSONであると誤認。JSON以外の9本をFAILEDと表示したが、これは出力パース誤判定。再実行時に各検証器のexit codeと先頭出力を個別読み取りし、11/11 exit0を確認（検証コードの失敗は0）。
集計訂正: 21Hの8 routeとは別に3 provenance checksがあるため、旧合成fixture計299を維持、新37で336。3 provenanceチェックを含む総チェック数は339。新規37/37とnative直接E8 5/5も独立確認。
保存/読戻し: 新規E 08H Python/JSON/MarkdownとREADBACK JSONはPC E testsに保存・個別読戻し済み。レポート・検証器のSHAはREADBACKに固定。原作DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
SAFETY_REFUSAL新規0、元拒否T018/T019/C/D/禁止VAの再試行0。正式READY統合0、MASTER cp196/READY596、34Task 9/21/4は今回直接再計数。
NEXT: 同一runの旧合法G0/G1/G2一次観測と、B08H 0x5AC601/0x5AC605境界pointerの保存済一次証拠更新を独立照合。再発防止: 既存検証器のstdout形式を強制的にJSONと仮定せずexit codeとケース計数を分離。
