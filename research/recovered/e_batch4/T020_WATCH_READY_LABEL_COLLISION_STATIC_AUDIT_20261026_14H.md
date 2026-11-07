# E-AUDIT-20261026-14H-T018-T020-WATCH-READY-LABEL-COLLISION-01
Owner: E / T018・T020。2026-10-26 14時台 JST。STATIC / REAL-SAVED-EVIDENCE BYTE-HASH VERIFIED / VERIFY / NOT READY / ORIGINAL GAME NOT RUN。

## 今回独立確認した差分：READYメタデータの識別ラベル衝突
- 2026-10-21旧原作Watch-1 `BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json` と Watch-2 `BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z_READY.json` は、いずれも `id=BRIDGE-G0G1-LIVE-READONLY-WATCH-20261021`、`pid=23272`、EXE SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- しかし各 `trace_file` と `initial.frame_counter` は異なる。前者13927、後者67655。READY statusはいずれも `ARMED_ALREADY_RUNNING_ORIGINAL_ONLY` であり、ownerのMASTER統合資格を示す `READY` ではない。
- 独立Get-FileHash実値：Watch-1 READY SHA256=`0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C`、Watch-2 READY SHA256=`936FBBA2961A46128CD4D4DFD4E93134A8663B127E1625A3C3F721ACD4ABC71B`。
- 独立Get-FileHash実値：Watch-1 trace SHA256=`9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7`、Watch-2 trace SHA256=`1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46`。
- `BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json` 現物SHA256=`87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C` の `evidence_ready_sha256` はWatch-1の `0CCBC...` と一致し、Watch-2の `936F...` とは一致しない。
- 本件は既存の「同じPIDで別戦闘2回」というE-AUDIT-20261022-0550の証拠を継承し、今回の独立増分は **READY JSONの同一id再利用とsource-ready SHA参照の一対一性を実バイトで確認** した点。実ゲームのバグ・改竄・レコーダの失敗とは断定しない。

## T018受入条件への帰結 / T020レビュー用負例（設計のみ）
- R01: `id` と `pid` と `exe_sha256` だけで照合してWatch-1とWatch-2を同一Golden runとして統合する処理は、複数候補として `AMBIGUOUS_RECEIPT_ID` のレビュー対象。統合成功扱いにしない。
- R02: G0確認JSONの `evidence_ready_sha256` がWatch-1 READY実SHAと一致するため、対応するのはWatch-1だけ。Watch-2の出来事にそのG0確認を移して適用しない。
- R03: `READY.json`というファイル名、および `ARMED...` statusは、E-owner統合READY/旧原作G0-G4 Golden達成の証拠ではない。
- R04: 出典キー候補は `{READYファイル実SHA, trace_file名, trace実SHA, battle_enter/exit UTC}` を必ず個別保持。キー案はE側受入設計であり、旧原作ネイティブの内部battle IDだと確定していない。
- R01-R04は既存実ファイルの手動比較からのT020受入設計であり、新しいコード・合成fixture実行・原作ライブ試験は **NOT RUN**。既安全拒否のsession-join実装の再提出・代理実行はしない。

## Golden/他owner/正本と安全
- Watch-1/2のmode2観測は保存済み限定DYNAMIC副指標。合法旧UIの攻撃元/対象、G1同戦闘直前SAVE実バイト＋入力、G2 MAP実SHA/三陣営/ordered Unit・Troopは全未充足。G3結果/G4戦略World差分も未充足。E新規DYNAMIC OBSERVED 0、actual Golden PASS 0、strict MATCH 0。
- T019新規確定矛盾0。GameClear DAT13件/TXT2件の字句検索範囲差は既存RESOLVED、script2同名勝者/phase flag/TXT実load/gwrite復帰はVERIFY。
- 2026-10-26 14H B/T028空セル・8方向候補資料はSTATIC/VERIFY/NOT READY（read-only）。追加正式READY0。MASTER最後の正式checkpoint196・READY596=A115/B229/C136/D116。34Task DONE9/IN_PROGRESS21/VERIFY4は前回13H確認値、今回全READY ID再列挙なし。
- 旧拒否：T018表境界、E session-join code/DAT受入追記、C T026/T032、D T030 TSV、0x5710C0ほかはBLOCKED維持・迂回なし。13/14H OFFLINE-UNSYNCEDは未正式統合。新安全拒否/接続障害なし。
- 本回は許可済みE-owned T020独立資料のみ書込。原本EXE/ZIP/SAVE/DAT、A-D、REA、dev_lab、MASTER、Git/push、Work、設定・毎時自動化には書込・変更なし。
- NEXT: C-NB02合法同一戦闘G0 UI、G1 SAVE/input、G2実MAP/三陣営/出撃名簿の一次receipt収集。外部owner READY後だけ出典SHA/ID重複/日時/合意/競合を審査しMASTERへ一度だけ反映。