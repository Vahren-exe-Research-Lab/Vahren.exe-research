# 迫真戦記ver0.67 機械解析参照の全件棚卸し・PE補助索引（2026-10-21）
- 作業ID: `REDEV-REF-BULK-PE-20261021`。先行: `REDEV-REF-CENSUS-BULK-20261021`。
- 状態: **STATIC VERIFIED / Ghidra READ-ONLY / 元EXE実行なし / 原作セーブ実機比較なし**。
- 採用索引: `REFERENCE_INDEX_AUDITED_WITH_PE_20261021.sqlite`。
- SHA256: `F89E310F16EEBF72F14EBF155A55CF40E90BD74CEA038C3BE084069427098751`。
- 元EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 旧検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
- 古い`search.sqlite`・原作EXE・Ghidraプロジェクト・10,268擬似C・他レーン・MASTER・Work管理コードは変更していない。

## 確定成果（出典の種類で分ける）
1. `ghidra_refs`：Ghidraが記録した**全243,665レコード**。一件単位の独立照合で243,665/243,665一致。参照元238,917箇所。旧索引に収録されなかった条件分岐49,652/無条件JMP11,287/計算JMP864/計算CALL3,492/特殊計算終端3/INDIRECTION1を含む。
2. `pe_highlow_relocations`：PE再配置表の**全57,921件**を読み取り、Ghidraと照合後に別テーブルへ収録。従来のGhidra参照を改変しない。
3. GhidraとのPE照合：`XREF_EXACT`14,827、`XREF_ON_CONTAINING_CODEUNIT`42,383、`NO_GHIDRA_XREF`711。命令内のアドレス値を命令先頭の参照として扱う違いにより、2,020→711へ精密化。
4. PE再配置が指す未分類.textアドレス87、うちGhidra参照と対応なし**72**。Ghidra認識済みCALLとは別の有力な解析手掛かりだが、関数ポインタとは断定しない。
5. `indirect_unresolved`：未解決制御5,144件。関数ポインタ/仮想呼出の具体ターゲットは未確定。
6. `unclassified_text_spans`：未分類.text 47,487 bytes／5,483区間。`unverified_raw_e8`の67候補は確定CALLと混同しない。
7. 雇用画面`0x004D4A50`は直接CALL 8件、`0x004A5B28`/`0x004A5B54`を含む。2件は元Ghidraで関数所属NULL。V2雇用改造DLLは未変更、実機確認待ち。

## 実際に検証した範囲／残る境界
- 元Ghidra関数10,268件の再逆コンパイルは不要。既存プロジェクトを `-noanalysis -readOnly` で利用。
- Ghidra参照243,665件とPE再配置57,921件を、それぞれ出典ファイルから新DBへ**1行ずつ独立再読し全件一致**。
- 新索引 SQLite `PRAGMA quick_check=ok`。旧Ghidra ref数243,665、PE再配置57,921の全件保存。CALLに推定値を入れる操作0。
- 元EXEでE8直接CALL44,888件の呼び先を機械語と再計算し44,888/44,888一致（別V2監査）。
- 製品の実機/原作GoldenはNOT RUN。ソートV2のスクロール/クリック/イベント後再描画の動作保証にはならない。
- 関数bodyに属さない命令18,388、うちE8直接CALL2,678のcaller所属は未決。元GhidraのNULLを維持。
- 生E8候補67中39は既知命令位置を指し、47は線形逆アセンブル時に命令境界を構成。ただし到達可能性の証明なし。
- PE再配置711件は**Ghidra参照無しの絶対アドレス値**。CALL/JMP/イベント到達先などの意味を自動付与しない。
- 本索引が全件カバーするのは「保存Ghidra ReferenceManagerの参照」と「PE HIGHLOW再配置のアドレス値」。動的生成ポインタ・未認識機械語・非再配置定数をすべて発見したとは言えない。

## 再実行・検索
```powershell
$ix = '[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'query_reference_index_with_pe_20261021.py') stats
python -B (Join-Path $ix 'query_reference_index_with_pe_20261021.py') xrefs-to 0x004D4A50 --limit 20
python -B (Join-Path $ix 'query_reference_index_with_pe_20261021.py') pe-to 0x005C3C8A
python -B (Join-Path $ix 'query_reference_index_with_pe_20261021.py') pe-unindexed --limit 40
python -B (Join-Path $ix 'query_reference_index_with_pe_20261021.py') pe-gaps --limit 40
python -B (Join-Path $ix 'validate_reference_plus_pe_index_20261021.py')
```

## 保存された証拠・障害回復
- `REFERENCE_INDEX_AUDITED_WITH_PE_20261021.sqlite`、`REFERENCE_INDEX_AUDITED_WITH_PE_20261021_REPORT.json`、`REFERENCE_INDEX_PE_INDEPENDENT_VALIDATION_20261021.json`。
- `PE_ALL_HIGHLOW_RELOCATIONS_20261021.jsonl`（57,921件）、`PE_ALL_HIGHLOW_GHIDRA_MATCH_20261021.jsonl`（全件Ghidra照合）、`PE_HIGHLOW_UNINDEXED_SUMMARY_20261021.json`。
- `PE_RELOCATION_REFERENCE_GAP_AUDIT_20261021.json`、`UNCLASSIFIED_EXECUTABLE_CANDIDATES_AUDIT_20261021.json`、元の`ALL_GHIDRA_REFERENCES_20261021.jsonl`、全参照DB・報告書。
- 自己テスト実行34/34 PASS（独立再実行）。ただし`selftest.py`に既存`test_report.json`を上書きする副作用があった。
- 復旧ID `REF-RC-20261021-SELFTEST-REPORT-OVERWRITE-01`：この一回により検証経過秒数が8.649→118.577となった。原本オフラインパック同梱JSONとSHA照合し、該当フィールドを復元。再読後元SHA `EDBB2E10BA57930C897E84CE809D9DC7B1E4A7205EE2E69276FD344D308C1467`完全一致。未復旧の既存ファイル差分は確認していない。
- 初回試行で完成済ZIPの再生成は上書き防止により停止。旧ZIPはCRC・21ファイルSHA全件PASS、SHA `679946D3E1D0CBCFE7E1E7A873F54B5F3424CEE56A85102C49AB98A20A4E6FE4`。元ZIPは変更しない。
- 原作EXE・旧search.sqlite・Ghidraプロジェクト・既存Ghidra抽出スクリプトは読み取り専用。解析資産の正規MASTER統合はE担当。外部Workへの自動通信・Git/push/公開は実施しない。
- 次研究優先：(A)関数所属NULLのCFG復元（複製Ghidra上でのみ）、(B)PE再配置から見る未分類.textの再判定、(C)間接CALLの候補先、(D)原作実機での雇用並び替え確認。A〜Dは別案件、今回の静的全参照保存とは区別。

