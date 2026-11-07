# 迫真戦記 新E｜同名READY receipt IDに異なる原作watchが紐付く問題（2026-10-29 13H）
研究ID: E-AUDIT-20261029-13H-T018-T020-WATCH-READY-ID-ALIAS-01
Owner E/T018,T020 (T019参照)。PC LOCAL / SOURCE BYTE VERIFIED / STATIC CROSSWALK / VERIFY / NOT READY。
## 今回の独立発見（旧成果と区別）
- 2026-10-21に保存された2本の原作watch READY JSONには、**完全に同じ `id=BRIDGE-G0G1-LIVE-READONLY-WATCH-20261021`** が入っている。
- 両者ともPID23272、EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、load_base 0x00050000。
- しかし `trace_file` は別々であり、READY-1初期 attack_count=0/frame_counter=13927/battlefield_ptr=0、READY-2初期 attack_count=1/frame_counter=67655/battlefield_ptr=0x1C995170。
- READY-1 source SHA256=0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C、1062B。
- READY-2 source SHA256=936FBBA2961A46128CD4D4DFD4E93134A8663B127E1625A3C3F721ACD4ABC71B、1065B。
- TRACE-1 source SHA256=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7、76837B。
- TRACE-2 source SHA256=1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46、24759B。
- G0限定receipt SHA256=87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C、1454B。G0の `evidence_sha256` はTRACE-1だけを指す。
## 受入判定とT020 fixture
- 同名 `id` はwatch収集器の論理IDと解釈し、戦闘run一意キーとして使用不可。これは発見した資料のスキーマ/識別境界であって、原作ゲームのBUG確定ではない。
- README/既存E05の時系列ではWATCH-1のmode2/active1開始2026-10-21T14:31:37.765Z、WATCH-2は15:14:40.580Zで、同一PIDでも別戦闘窓。
- 両READYの `native_gameplay_G0_confirmed=false`、`native_gameplay_G1_complete=false`。別G0 receiptのgate_status=PASSは旧通常戦闘の限定確認であって、READY-2への伝播や合法Spot/MAP/名簿の認定不可。
- Golden受入では source file SHA + trace file SHA + process + UTC開始/終了 + EXE/DAT世代 + G1 SAVE/input + G2 MAP/side/roster を別々に照合し、一致未確認は UNLINKED/VERIFY に保つ。
- E-owned tests/T020_E_WATCH_READY_ID_ALIAS_CASES_20261029_13H.json に6負例設計を保存。新しい原作観測も新コードの失敗済payload再試行も行わない。
## 実行・MASTER・T019
- Read-only UTF8 JSON 3件比較で same_id/same_pid=true、different_trace/initial_attack_count/frame_counter=true、両READYのG0/G1=false、別G0のgate_status=PASSを確認。
- 当初PowerShell既定Get-Contentの日本語UTF8扱いでConvertFrom-Jsonが失敗。-Encoding UTF8の同じ許可済読取で回復。OTHER / RECOVERED（安全拒否でない）。
- 既存12H T020回帰8/8 PASS（Python -B unittest、0.032秒）。新13H fixtureは DESIGNED_NOT_RUN、原作ゲームは起動していない。
- 公式MASTER最終checkpoint196、READY596 (A115/B229/C136/D116)。34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値。今回正式READY新規IDなし。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2検索範囲差RESOLVED、script2/phase flag/TXT実読込/gwrite復帰/decide11はVERIFY。
- E原作Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。旧原作構造観測3 session/RAW8/失敗5は合成/Goldと混ぜない。
- 旧T018表境界、E session-join code、T019 XREF、C T026/T032、D T030、0x5710C0、10/28 13H拒否14件はBLOCKED継承、別tool/経路で再試行しない。
- 旧OFFLINE-UNSYNCEDの意味的重複全照合は未完。今回原本EXE/DAT/SAVE/ZIP、他レーン、REA、dev_lab、Git/Work/automation設定の書込なし。
- 検証情報：2026-10-21 BUILD_MANIFEST旧索引は既存証拠。今回原本EXEの独立再ハッシュ/Ghidra実行はNOT RUN。
