# 迫真戦記 REA｜P0 子要素vcallのAL分岐行列（追加派生監査）
ID: REA-LOCAL-20261024-2035-P0-CHILD-VCALL-AL-BRANCH-MATRIX-STATIC-01。状態 PC-SAVED / REUSED STATIC / DERIVED / VERIFY / NOT READY。2026-10-24 20:35 JST。
参照原作SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9検索DB SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
一次出典（今回PE新読込みなし）: `REA_20261024_20H_P0_ARMYCHIP_CHILD_VCALL_ORDER_AUDIT.py` とその67/67 PASS証拠JSON（実バイト照合済みの先行研究）。同じ成功数を再計上しない。
進捗優先順位: P0 0x005B0B91 子要素vtable+0x44のAL分岐契約。+0x34/+0x08/+0x48も同じループの契約として整理。
## 今回初めて整理した派生制御フロー
- `0x005B0B53` +0x34：return直後のAL条件分岐なし（副作用なしを意味しない）。
- `0x005B0B5C` +0x08：`TEST AL,AL`、`0x005B0B60 JE +0x0E -> 0x005B0B70`。AL!=0のみ `0x005B0B6B CALL 0x004C22B0`（flag0）。
- `0x005B0B77` +0x48：`TEST AL,AL`、`0x005B0B7B JE +0x0D -> 0x005B0B8A`。AL!=0のみ `0x005B0B81 CALL 0x004C3E40`。
- `0x005B0B91` +0x44：`TEST AL,AL`、`0x005B0B95 JE +0x06 -> 0x005B0B9D`。AL!=0は`0x005B0B97 MOV BYTE [ESI+0x6C],0`後`0x005B0B9B JMP +0x0C -> 0x005B0BA9`、AL==0は`0x005B0BA4 CALL 0x004C2440`へ接続。
- 通常の各要素末尾は `0x005B0BAD CALL 0x004BC9C0`。3つのAL判定は逐次でshort-circuit構造ではない（calleeが正常に戻る場合）。
- 4つのshort branchは、先行監査でバイト確認された命令から`site+2+disp8`を独立計算して4/4整合。これは新規原作PE照合4件ではなく派生算術検証。
## 3つのAL戻り値の真理値表（実行可能性は未証明）
| +0x08/+0x48/+0x44 | C22B0(flag0) | C3E40 | child+6C=0 | C2440 | C9C0 |
|---|---:|---:|---:|---:|---:|
| 000 | 0 | 0 | 0 | 1 | 1 |
| 001 | 0 | 0 | 1 | 0 | 1 |
| 010 | 0 | 1 | 0 | 1 | 1 |
| 011 | 0 | 1 | 1 | 0 | 1 |
| 100 | 1 | 0 | 0 | 1 | 1 |
| 101 | 1 | 0 | 1 | 0 | 1 |
| 110 | 1 | 1 | 0 | 1 | 1 |
| 111 | 1 | 1 | 1 | 0 | 1 |
上記8行は独立した3分岐の論理的組合せであり、8種類のゲーム内状態が実在・到達可能と確定した意味ではない。
## 事故・作業境界
検索CLI `python search.py function 0x004BC9C0 ...` の開始が安全状態不明として拒否。拒否ID `REA-LOCAL-20261024-2035-CLI-SAFETY-01`。同操作のshell/tool/path差替えによる再試行なし。未取得範囲は0x004BC9C0の新規疑似C/ABI・個別callee内部。
既存正本は`QUEUE.json`ではW2–5がTODOと表示されるが、`logs/progress_sync_20261011T153958076Z.json`は21runを検証しWave1–5の64/64を記録、`STALE_RENAME_DENIED`。新規正式VERIFIED=0、5種完全充足=0、正式TODO/VERIFY/BLOCKED書込差分=0。Golden実測PASS=0・完全複製率未測定。
次は許可された独立論点として、子クラスRTTI/生成元・4スロット各実ターゲットを所有者と照合して調査する。拒否済み0x004BC9C0への別経路再問い合わせは行わない。
PC内原本・MASTER・QUEUE/PROGRESS・既存runs・A–E・Git・Work・スケジュールは変更しない。新規成果はREA所有フォルダへの本ファイルとJSONのみ。CPU負荷/総所要時間不明、REA/Ghidra/ゲーム新規実行0。
