# 迫真戦記ver0.67｜REA P0・2026-10-24 20時台
ID: REA-LOCAL-20261024-20H-P0-ARMYCHIP-CHILD-VCALL-ORDER-STATIC-01
判定: PC-SAVED / STATIC / VERIFY / NOT READY。Golden NOT RUN。
原作PE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
使用統合V9 DB SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 先行・重複防止
MASTER先頭・末尾、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、21既存runs目録、最新sync 20261011T153958076Z、旧検索基盤README/BUILD_MANIFEST、統合V9入口を先読。
保存syncのWave1–5=64/64 VERIFIED、旧QUEUE/PROGRESSはEPERMによるstale。既存件数を増減せず今回新規正式VERIFIED0。
19時台の2つのArmyChipBuilder調査スクリプトは既存と判明。19Hの0x004C2933から親+0x04仮想CALLを追った仕事を二重計上しない。今回の独立差分は0x005B0A50内で実行する子要素4仮想CALLとその条件。
新規検索は統合V9を使用。PC標準search_current.pyはV3のままで昇格しない。旧10,268関数DBは先行確認のみ。

## 発見A：4つの子要素vptr CALLIND
0x005B0A50の[EBX+0x44]非0側は[EBX+0x14]～[EBX+0x18]の4B幅要素配列を反復。子要素ESIからvptr=[ESI]を読み、ECX=ESI、EAX=[vptr+offset]、FF D0で呼ぶ。
| CALL site | 子vptr slot | 戻り後の条件付動作 |
|---|---|---|
| 0x005B0B53 | +0x34 | AL分岐は行わない |
| 0x005B0B5C | +0x08 | AL非0で0x005B0B6B→0x004C22B0（flag 0） |
| 0x005B0B77 | +0x48 | AL非0で0x005B0B81→0x004C3E40 |
| 0x005B0B91 | +0x44 | AL非0で[ESI+0x6C]=0、AL=0で0x005B0BA4→0x004C2440 |
各要素の後、0x005B0BAD→0x004BC9C0は無条件CALL。子の実際のクラス・各仮想ターゲットは未特定。親ArmyChipBuilderのvtableと子vtableを混同しない。
V9 ghidra_refsは上記4つのFF D0 siteにレコード0、native_callsiteにもE8直接CALL登録0。ゆえに既存callers/calleesの直接CALL索引だけで動的宛先を解決したとは扱えない。

## 発見B：反復と0x00491870の呼出順
0x005B0BB2/B5で現在のベクトルbegin/endを再取得、0x005B0BBEでindexを増し、0x005B0BC6で長さを再評価。
通常反復終了後0x005B0BCE→0x005B0B05、次に0x005B0B15で0x00491870、0x005B0B29で0x004C22B0（flag 1）を呼ぶ。初めから空の場合も0x005B0B05側へ進む。
0x005B0B39のJBEは0x005B0BD3のvector range error pathへ進む。仮想CALLが生配列へ与える副作用とindex変化による要素処理順はVERIFY。
[EBX+0x44]が0の場合の0x005B0BDD以降は別経路で、今回全体を確定したわけではない。

## 検証・正式進捗
独立監査ファイル: REA_20261024_20H_P0_ARMYCHIP_CHILD_VCALL_ORDER_AUDIT.py。元PEの署名・E8直接ターゲットとV9索引・4つのFF D0・SQLite quick_check・6関数の疑似Cを照合。監査初回/独立再実行とも67/67 PASS（検査項目数であって関数数ではない）。
V9=11,950関数。対象6関数のverified_abi=0。REA正式5種（info/pseudo/assembly/callers/callees）の新規セット完全充足0、新規VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0。Golden実機PASS0、strict MATCH0、完全複製率未測定。
Ghidra/REA/原作ゲーム新規実行0。PC online、active.lockなし、Java/Ghidraプロセス検出なし。空き物理RAM14,052,072KiB（約13.4GiB）、CPU総負荷不明。静的監査再実行1.078秒、研究全体の所要時間未計測。
副次失敗: Python -cとPowerShellの引用符処理が合わず、探索用コマンド2回にSyntaxError。非安全・原本DB変更なし。RECOVERY-ID REA-LOCAL-20261024-20H-CMDQUOTE-01。許可されたLocalの新規.pyによる独立監査で必要な検証を継続。

## 次のP0
(1) 子vptr +0x34/+0x08/+0x48/+0x44のRTTI/実ターゲットを静的に特定。
(2) 0x004C22B0のEAX所属コンテナと+0x64/+0x68配列、0x004BC9C0のESI役割、反復中更新の影響を分析。
(3) 0x00491870のcontext+0x1EED4C/+0x1EED50に関する既存MASTER・担当成果と照合しGolden条件設計（NOT RUN）。
REA所有decomp_task内に新規独立資料のみ保存。原本・MASTER・QUEUE・PROGRESS・既存run/evidence・A〜E・Git・Work・スケジュールは無変更。

