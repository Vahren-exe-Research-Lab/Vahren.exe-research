# B/T028｜2026-10-29 03時台・未同期17H資料の部分保存と安全拒否（復旧メタデータのみ）
- RECOVERY-ID: `B-RC-20261029-0301-T028-17H-COPY-SAFETY-01`; Task=T028; owner B; category=SAFETY_REFUSAL; status=BLOCKED / NOT READY.
- 操作日時: 2026-10-29 03:00頃 JST（PC対象ファイルmtime 2026-10-28T18:00:47Z）。
- Library元資料: `/迫真戦記再開発プロジェクト/data/B_T028_MERCENARY_ELIGIBILITY_BOOL_OFFLINE_20261028_17H.md`（66行、既存保全・変更なし）。
- PC対象: `data/B_T028_MERCENARY_ELIGIBILITY_BOOL_OFFLINE_20261028_17H.md`。
- 最後の成功: Desktop Commander Local Compact `write_file(rewrite)` で初めの25行を一度保存、read_fileで25行部分一致を確認。
- 失敗操作: 以降の `write_file(mode=append)` を含む次の呼出しがOpenAI安全性チェックで拒否。詳細な拒否原因は不明、同じ操作を再試行せず。
- 独立状態確認: Local `get_file_info` はPC 25行・2673bytes・appendPosition25を返した。残り41行はPC未保存。
- 保護: PC側25行はPARTIAL/INVALID/DO NOT CONSUME。既存Library全文は保持。元の拒否本文・操作を別tool/shell/path/Remote/ZIP/分割で再提出しない。
- 関連17H検証器・JSONは今回移送未実施。拒否内容を迂回する目的で同主題の資料を転送しない。
- 影響: 10/28 17H研究のPC同期不成立、既B owner/HANDOFFへの正式取り込み未達。既保存研究や既統合IDは二重計上しない。
- 別の10/28 18〜22H独立研究と10/25・10/21〜24の非拒否分は個別安全状態を確認して別途照合可能。
- MASTERはE専有、今回確認した最後の正式cp196/READY596はPC保存の前回値であり再統合していない。
- 原作Gameplay Golden PASS0、strict MATCH0、新B READY0、E統合0、検証器実行0。
- 次の許可された一手: 既存LibraryメタデータとPC正本との読み取り専用重複照合、独立安全資料のみ回収。安全条件が正当に変化するまで当該コピーはBLOCKED。
- 原本ZIP/EXE/DAT/SAVE・他lane/REA/dev_lab/Git/Work/設定/automationは変更しない。

## B-RC-20261029-03H-T028-17H-UNATTRIBUTED-STATE-CHANGE-02｜PC側対象ファイルの後続状態（元安全拒否は維持）
- 後続のLocal `get_file_info` で同名PCファイルは66行・7783bytes、mtime=2026-10-28T18:03:19.796Zへ変化していた。当チャットは安全拒否後に元本文の再送・appendを一切行っていない。
- この更新を実施した主体・方法・安全許可・内容同一性は未確認。**元のSAFETY_REFUSALは取り消さない**。名称/サイズ/行数のみでは正常同期・READYを認定しない。
- PC現在版は `EXTERNAL_CHANGE / PROVENANCE_VERIFY / NOT READY` とし、別の作業の内容をこのチャットの成功として計上しない。今回の調査はmetadata read-onlyのみ。
