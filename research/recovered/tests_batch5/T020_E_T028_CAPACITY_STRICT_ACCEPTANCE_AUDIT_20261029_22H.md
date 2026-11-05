# 迫真戦記 E｜T028 退却先候補の容量strict比較 T020受入・回帰（2026-10-29 22H）
研究ID: E-AUDIT-20261029-22H-T020-T028-STRICT-CAPACITY-BOUNDARY-01
状態: PC LOCAL / STATIC source-pinned / SYNTHETIC EXECUTED / VERIFY / NOT READY / original gameplay NOT RUN。
## 出典と差分
- B 22H owner: B-20261029-2213-T028-RETREAT-SPOT-CAPACITY-STRICT-GATE-01、detail `data/T028_RETREAT_SPOT_CAPACITY_STRICT_GATE_NATIVE_20261029_22H.md`、実SHA256 D2E746997C492CE294EFF9BD9B61D7D45C14DBF5FE7030DAC02C624BE5ED26F6。B HANDOFF状態 STATIC/INFERRED/VERIFY/NOT READY。
- B 21H detail実SHA256 EE0831A672E0AFA56D17F4ED278C1B49260C0D3120E47ACB6ABAD4F02A01135A、旧E 21H gate実SHA256 136D5DBDA312ADCACD07558AC7B9CB0D36C97A8F4C4E3710E27C3388154181D8。3出典の現物SHAが新検証器で3/3一致。
- 新E差分: 21Hのcallee戻り0/非0だけではSpot候補の可否を予測できない。B22Hの候補同一・NULL・RTTI・arg2一致・signed32の (0x597A50計数 + 候補+0xB8) < 候補+0x88 を独立ゲート化。等号は即採用しない。
- 原作退却呼出0x5682C3は第3引数0。追加fallback枝は通らなくても別候補の走査余地がある。候補不採用と退却全体の失敗文字列を混同しない。
- 候補採用後の+0xB8インクリメントを単純な参照countと断定しない。予約・占有関連の可能性を保持し、真の所有権/減分writer/可視退却成功は未証明。
- signed32加算が範囲を越える合成条件は `OVERFLOW_VERIFY` として隔離し、負の合計から原作で即採用したという主張を禁止。これは未観測の境界であり原作BUG認定ではない。
## 新規T020成果
- `tests/t020_e_t028_capacity_strict_gate_20261029_22H.py`：E所有の純粋合成判定、元ゲーム・Ghidra・Javaを起動しない。
- `tests/T020_E_T028_CAPACITY_STRICT_CASES_20261029_22H.json`：18ケース。capacity-1/等号/+1、空容量、自己/NULL/RTTI除外、参照不一致、arg3!=0、欠損、overflow、数値型不正を別IDで判定。
- PC `python -B ...`実行結果: SOURCE_PINS 3/3 PASS、SYNTHETIC_CAPACITY_CASES 18/18 PASS、exit errorなし。18件は合成分岐検証であり旧原作・新エンジンの実互換PASSではない。
- コードSHA256 9A6E36AD65892FD7F708AE804C452418D0D336CA36D18AA69601638ABFD18DA4。fixture SHA256 775D2C96E8D9A5739380A2E073BDC1FB04C171C4E61A67F20F264EE668E8FC14。
## T018 Golden / T019
- 原作C-NB02では旧UIによるG0限定記録が既存。G1同run直前未改変SAVE+入力とG2 ACTIVEの実MAP/三陣営/ordered deployed Unit/Troopが同戦闘に結合できない。G3/G4も未完。原作DYNAMIC OBSERVED（Golden認定可能）0、actual Golden PASS0、新旧strict MATCH0。
- T028専用の合法観測は未改変旧EXE・x20前DAT・同SAVE/MAP/入力/条件で候補Spotの可視数・容量の前後・不採用後別候補探索・退却結果・翌tickを採取する。内部+0xB8/0x597A50が合法画面不可視ならUNKNOWN/INELIGIBLE。戦略画面だけのrouteをC-NB02に強制結合しない。
- T019新規原作Wiki/DAT/EXE確定矛盾0。既知GameClear DAT13/TXT2字句検索scope差はRESOLVED、script2優先/phase flag/TXT実load/gwrite復帰/decide11はVERIFY据置。
## 統合・安全・復旧
- MASTER最後の正式checkpoint196/READY596（A115/B229/C136/D116）は前回確認済旧値。34 Task DONE9/IN_PROGRESS21/VERIFY4も旧値で全件再集計なし。B22HはNOT READY、新規正式READY ID 0・MASTER変更0。
- 旧T018表境界、E session-join、T019 XREF、C T026/T032、D T030 TSV、禁止VA0x5710C0および関連拒否はBLOCKED継続、元操作の再試行/他経路迂回なし。今回新安全拒否0、PC接続障害0。
- OFFLINE-UNSYNCEDの全成果意味重複照合は未完。原本EXE/ZIP/DAT/SAVE・A～D/REA/dev_lab/MASTER/Git/Work/設定/自動化に書込なし。
- 本E独立コード/fixture/報告書のみ新規保存。読み戻し・実SHA取得と回帰再実行結果を本runで記録する。
- 次: C-NB02の同run合法G0/G1/G2一次receipt探索を最優先。B22HがREADY化し根拠owner/time/SHA/合意/競合を照合できた場合にのみ正式MASTER検討。加えて0x597A50の値・候補順・+0xB8減分・可視表示はB owner側VERIFYを待つ。
