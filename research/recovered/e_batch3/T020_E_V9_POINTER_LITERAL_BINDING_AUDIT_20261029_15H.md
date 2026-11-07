# E/T020｜V9 SOURCE PINのパス参照先と実ハッシュ計算先の結合監査（2026-10-29 15H）
研究ID：E-AUDIT-20261029-15H-T020-V9-POINTER-PATH-BINDING-01
状態：PC LOCAL / STATIC SOURCE-TEST / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作GAME NOT RUN。
## 入力と重複検査
- 現行ポインタ rea_lab/headless_analysis/CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json、V9 manifest search_index/UNIFIED_V9_INTEGRITY_20261023.json（read-only）。
- 前回E14Hの tests/t020_e_v9_source_epoch_gate_20261029_14H.py を直接読取。V9 DB/CLI/EXEの登録SHA検証と10テストは既存成果、再加算しない。
- 先行E15H同名成果なし。MASTER cp196/READY596、34 Task DONE9/IN_PROGRESS21/VERIFY4は既知の旧値で、全件再集計NOT RUN。
## 今回の具体的な新発見
- E14H admission() は current_database/current_cli について Path(...).name の一致だけを確認する。実ハッシュDB/CLIは IDX/V9 の固定正規パスを別途読んでいる。
- このため、合成ポインタで current_database="other/HAKUSHIN067_UNIFIED_V9_20261023.sqlite" または current_cli="other/search_unified_v9_20261023.py" と書いても、既存 admission() が TRUE になった。
- これは「実ポインタが他所を指す場合の誤認定可能性」であり、現行ポインタの破損・不正ファイルの存在・解析DBが実際に入れ替わった証拠ではない。
- 独立新規 t020_e_v9_pointer_literal_binding_20261029_15H.py を作成。既存のDB/CLI/EXE SHA pinに加え、ポインタ参照文字列が明示的に選択された search_index/ 以下の固定相対パスと完全一致することを要求する。
- directory alias / 親ディレクトリ遡行 / 絶対path / SHA改変 / EXE改変 / 欠落 / non-string / gameplay誤昇格を reject。別形式の有効な参照先は自動受理せず、手動確認待ちとする fail-closed 方針。
## 試験・証拠資格
- PCのPython -B unittestで新13/13 PASS。うちlegacy誤受理2件を再現し、対応する新gate拒否2件を実証。既存E14H 10/10 PASSも別実行で確認。合計23/23、FAIL0。
- 新code SHA256=7A9FC79C2D09CB268429B7FA156B376FFAC9024BF9197C410EC41CEE3BE9F26C（PC現物Get-FileHash）。
- 実行器変更なし。既存E14Hを変更・再解釈せず新独立gateで補強した。source byte identityはGameplayを証明しない。
## Golden・T019・MASTER
- C-NB02 G0合法UI + G1同戦闘直前未改変SAVE/input bytes + G2実MAP/攻防援軍3sideと順序付きUnit/Troopの同一run一次証拠未充足、G3/G4も未充足。
- 原作Golden認定可能DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。旧原作RAW8・3sessionは歴史資料でありGolden0を変更しない。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2 source-scope RESOLVED、script2 winner / phase flag / TXT runtime / gwrite resume / decide11 はVERIFY。
- 今回の正式READY新規統合ID0、MASTER書込0。cp196/READY596(A115/B229/C136/D116)・34 Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値。
## 安全・保存・再開
- 旧T018表境界、E拒否済session-join、T019 XREF、C T026/T032、D T030 TSV、禁止VA0x5710C0、2026-10-28 13H拒否14件をBLOCKED維持。元操作再試行・迂回0、新安全拒否0。
- 旧README・rea_lab/PROGRESS.md・RUN_STATUS.mdは旧配置からENOENT（OTHER; 現行V9 pointerと rea_lab/decomp_task/PROGRESS.mdにより読取確認、拒否操作迂回ではない）。
- OFFLINE-UNSYNCED全件の意味的重複照合は未完。A-D/REA/dev_lab/EXE/DAT/SAVE/ZIP/Git/Work/settings/automation変更0。
- 次：EのV9証拠採用時に本literal path＋real SHA pinを前段確認、なお原作合法G0/G1/G2一次証拠を最優先。SOURCE PIN≠strict MATCH。
