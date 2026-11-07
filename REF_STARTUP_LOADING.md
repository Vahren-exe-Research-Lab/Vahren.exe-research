# 起動直後の終了・DATファイルロックの研究記録

2026年11月3日の調査では、外部プロセスがDATを開いたままにした環境で、Vahren.exeが約1～3秒・終了コード0で消える事例を報告している。正常に起動する隔離版でロック条件を再現し、解除後に再び起動したという記録がある。**今回再実験した結果ではなく、全ての早期終了の原因をDATロックとするものでもない。**

| 確認したいこと | 根拠と限界 |
|---|---|
| 症状と切り分け | [機密除去済み報告22–36行](research/recovered/github_blob5/reports/research/STARTUP_DAT_FILE_LOCK_20261103.md?plain=1#L22-L36)。プラグイン無効化・隔離環境・ファイル一致を当時比較したと報告 |
| ロックと再現の関係 | [同38–44行](research/recovered/github_blob5/reports/research/STARTUP_DAT_FILE_LOCK_20261103.md?plain=1#L38-L44)。使用中DAT・対照ロック・解除後の起動継続を区別して記録 |
| 元の研究文書 | [保存した加工版](research/recovered/outside_design1/reports/dev_lab/_work/summon_exp_20261103/STARTUP_LOCK_ROOT_CAUSE_20261103.md)。報告が引用する原本SHAと回収台帳の原本SHAが一致し、個人パスだけを伏せた版へ辿れる |
| 未確定事項 | [同54–59行](research/recovered/github_blob5/reports/research/STARTUP_DAT_FILE_LOCK_20261103.md?plain=1#L54-L59)。原作側のopen API・共有フラグ、タイトル操作、ゲーム全工程のGoldenは未確認 |

報告は所有アプリの正常終了・再起動を第一選択としており、当時のPIDやハンドル値による自動強制解除を一般手順にしていない。ここには解除コマンドや原作ファイルを置かず、過去の操作指示を自動実行しない。

研究IDは`KB-20261103-STARTUP-FILELOCK-01`。[Issue20の保存本文](research/recovered/issues_3_20/ISSUE_20_BODY.md)と[出典SHA・行範囲の対応表](research/recovered/intake_open_sources_20261105/STARTUP_CASE_SOURCES.tsv)から同じ事例を探せる。ネイティブVAが未特定なので、推測した関数名・メモリ型・呼出関係は追加していない。
