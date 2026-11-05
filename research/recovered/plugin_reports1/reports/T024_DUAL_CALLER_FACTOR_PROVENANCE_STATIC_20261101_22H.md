# 迫真戦記 新B｜0x528DB0 の2 caller における入力係数・分流元の静的差分（2026-11-01 22H JST）
research_id: B-20261101-22H-T024-DUAL-CALLER-FACTOR-PROVENANCE-CROSSJOIN-01
owner: B; tasks: T024,T013(最終対象はVERIFY); evidence_kind: STATIC_V9 / INFERRED / VERIFY; ready_status: NOT READY; golden_status: Original gameplay PASS0 / strict MATCH0 / DYNAMIC0.
## 先行・競合照合
先行B-20261025-1811-T024-AL0-STATE45D-SELECTOR-01は0x5271A0の+0x45D解除とAL分岐を確定。B-20261025-1910-T024-EMPTY-CONTAINER-45D-RESET-01は0x528870の空vector時+0x34Cと0x528A04を確定。B-20261025-2008-T024-TROOP-CLEANUP-GATES-INPUT-01はそのGUI入口を調査済み。11/01 20–21Hは0x528DB0内部のmode0配送gateを確定済み。これらを別発見として再計上しない。
今回の限定差分は、既存2 callerが0x528DB0へ与える**浮動パラメータの産出元と非空vector時の別配送経路を同じ表で対照**したこと。再解析や原作実行なし。
## V9読取専用の関数・CALL証拠
V9入口: rea_lab/headless_analysis/search_index/00_START_HERE_UNIFIED_V9_20261023.md; V9 DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE (既検証manifest値、本run全DB再hashなし)。
target original PE識別 SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (既照合値、本run原PE再hashなし)。
V9 functions/0052/005271A0.c 相当: entry 0x5271A0、body [0x5271A0,0x5276BF] 1312B。0x5272AB E8 00 1B 00 00 -> 0x528DB0 は検証済みdirect CALL。直前に0x542280を呼び返値由来のdoubleを第3パラメータとするGhidra表現。owner+0x430 sentinelとstate+0x26/+0x27、および+0x45Dを通過後、+0x364..+0x368 vectorが非空では0x52727A->0x569730、空では0x5272AB->0x528DB0に分岐する（分岐の演算子やABIは元ASM未再確認）。
V9 functions/0052/00528870.c 相当: entry 0x528870、body [0x528870,0x528A1A] 427B。0x528A04 E8 A7 03 00 00 -> 0x528DB0 は検証済みdirect CALL。Ghidra上は0x5E743Aの返値+定数global[0x62A190]を第3パラメータにする。vector非空では同じ計算をowner+0x478へ保存し0x52893D->0x569730へ、空かつowner+0x34C!=0では+0x45Dを0にして0x528A04へ。空かつ+0x34C==0は早期AL0。
## 差分・意味・訂正
同じ0x528DB0のE8入口でも、0x5271A0側は0x542280由来、0x528870側は0x5E743A+0x62A190由来の値を与える。両方を同一RNG/速度/時間源と仮定して統一しない。両分岐が+0x45Dに触れても、その変更だけで同一AI行動と断定しない。
STATICはV9擬似CとE8元バイトを実照合済みの範囲。浮動パラメータの意味、+0x542280/+0x5E743Aの厳密副作用、direct CALL時のnative ABI、実機での到達・最終対象・RNG時相はVERIFY。vtableと他間接呼出しは未網羅。
source_relative: rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite (実DBはGitHub送信禁止); V9 body entry bytes 1312/427, CLI function 0x5271A0 / 0x528870 と callers 0x528DB0。Ghidra本文の個別SHA256は本run未取得なのでUNVERIFIED_SOURCE、捏造せずcuratorに検証依頼。
KB_CANDIDATE: VAs 0x5271A0,0x5272AB,0x528870,0x528A04,0x528DB0,0x52727A,0x52893D; owner offsets +0x430/+0x18C/+0x45D/+0x34C/+0x364/+0x368/+0x478; param producer 0x542280 vs 0x5E743A+0x62A190。正式辞書採録権はcuratorのみ。
Goldens: 無改変原作EXEと同一DAT/SAVE/MAP/input/RNG/tick、vector空/非空・+0x34C両値・state+26/+27・+45Dのbefore/after、CALLsiteと第三引数のnative実値および0x569730後続、Unit可視行動を採取するまでは0。現時点 Golden0、strict0、READY0。
Recovery: 03H保存UNKNOWN、07H core4未回収、10/25欠落原文/54B相違、HOLD21 SAFETY_REFUSAL継続。禁止VA0x5710C0..0x571500・旧拒否XREF0x5769B0は未接触。旧search_index README/BUILD_MANIFEST ENOENTはV9移行によるOTHER。
Next: 0x542280と0x5E743Aの許可済み独立文書から効果とnative引数を照合、0x528DB0の第3パラメータ消費先、モード別最終行動を原作Goldenで実証。B T011/T012/T013/T024/T028 P0全継続。

