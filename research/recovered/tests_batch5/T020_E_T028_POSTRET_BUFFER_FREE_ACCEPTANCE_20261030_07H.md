# 研究E｜T020 T028 mode1後の条件付きvector-buffer解放（2026-10-30 07H JST）
研究ID: E-AUDIT-20261030-07H-T020-T028-POSTRET-BUFFER-RELEASE-01
状態: STATIC / SOURCE-PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。正式READY新規統合0。
## 出典・owner
B: B-20261030-0711-T028-MODE1-POSTRET-BUFFER-RELEASE-01。B-owned詳細 data/T028_RETREAT_MODE1_POSTRET_CONDITIONAL_VECTOR_BUFFER_FREE_NATIVE_20261030_07H.md、owner data/T028_MORALE.md、evidence/LANE_B_HANDOFF.mdをread-only照合。
E独立Get-FileHash: B詳細 3323 bytes / SHA256 A62F2BFC272326AE24A94807637A9F370644995ABF2F1182179E7357A14DB945。B所有owner ID1件、B HANDOFF見出しID1件。B状態VERIFY/NOT READY。
EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187・V9 DB SHA2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDEはB資料の記録値であり、本E回はEXE/DB本体を再hashしていない。
B保存局所PE窓: 0x5AC3A0+0x7A SHA43B013048E6BDE945B84BEFEBBE3EE5124DF98328D829851906F26A68AF2A8DC、0x5AC5E3+0x70 SHA6D421D77C8258538E8567B72C6C24783E877A567FB2780A41B39950010192F35。本E回では窓を再読しておらずBのSTATICを検証条件とする。
## 新規受入条件・以前との差分
通常走査完了: 0x5AC3C4 CMP EDI,EBX → equalなら0x5AC3D1へskip、異なる時だけ0x5AC3C9 CALL0x5B6BBB。通常経路と後段の総副作用は未確定。
早期mode1: 0x5AC3AF Unit+0x77==0 かつ 0x5AC3B5 Unit+0x75==0 の局所gate→0x5AC3B9 JE0x5AC5E3→0x5AC5E7 CALL0x598450(mode1)。これは05/06H既知・二重計上しない。
今回の新site: mode1 helper後0x5AC5EC CMP EDI,EBX/0x5AC5EE JE0x5AC5F9。EDI!=EBXなら0x5AC5F1 CALL0x5B6BBB、等しければこの条件付きcallをskip。
早期mode1後の通常制御フロー: 0x5AC5F9 stack値4、0x5AC609 CALL0x510850、0x5AC61B CALL0x5B6BBB、0x5AC631 JMP0x5AC5B5。実引数/ownership/exception時の到達・実解放の成否はVERIFY。
EDX候補、EDI/EBX、vector ownershipとaliasesの同定なし。合成fixtureのpointer名は**比較時点**のラベルであり、mode1呼出前後の保存や二重解放発生を証明しない。
## E/T020回帰・strict境界
新規 Python t020_e_t028_postret_vector_buffer_free_gate_20261030_07H.py と JSON T020_E_T028_POSTRET_BUFFER_FREE_CASES_20261030_07H.json にて通常/早期それぞれ12条件、非法入力9条件=33件を局所モデルに固定。
ソース実SHA/owner/HANDOFF見出し/fixture ID一意を検証。合成33/33 PASS。既存T028合成10検証器=266/266 PASS、合計11検証器299/299 PASS。各終了コード0。これらは旧原作実ゲーム・再実装と比較した結果ではない。
source_kind=STATIC_SYNTHETIC以外、両flag非0の早期枝、型不正、範囲外、欠落ラベルをreject。conditional buffer freeと尾部の別callsiteを混同せず、releaseの実現成功、メモリ安全性、画面結果をPASSにしない。
## T018 Golden / T019 / MASTER
C-NB02では、合法旧通常UIから同一戦闘G0開始→G1直前未改変SAVE byte SHA+入力時刻→G2旧MAP/3陣営/ordered deployed Troop/Unit→G3可視結果→G4 World差分が必要。同runの画面・時刻・入力・原本EXE/DAT/SAVE/Map・old/new capture SHAを揃える。x20改変DATや別runのwatchをstrict原作へ流用しない。
今回実ゲームDYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。旧EXE起動0、新エンジン比較0。
T019新規確定矛盾0。GameClear DAT13/TXT2の字句探索scope差のみRESOLVED。script2同名勝者/phase flag/TXT runtime loader/gwrite/decide11用途はVERIFY。buffer alias警戒は原作BUGにしない。
MASTER前回E正式checkpoint196/READY596=A115/B229/C136/D116、TASK QUEUE34= DONE9/IN_PROGRESS21/VERIFY4。今回新規READY0、MASTER変更しない。B07研究はNOT READY。
## 安全・次
旧T018表境界、E session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0の拒否は独立BLOCKED据置。旧OFFLINE-UNSYNCED意味的重複/同期は未完了。新規安全拒否0、拒否元再試行・迂回0。書込はE所有testsのみ。Git/push/他owner/原本/REA/dev_lab/Work/設定/automation変更0。
次優先: B担当による0x510850/0x5AC5B5・EDI/EBX割当元と実所有権の一次調査。Eは合法原作G0/G1/G2 receipt獲得・比較runnerの源泉分離、B READY証拠の重複審査を継続。
