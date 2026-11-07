# E-AUDIT-20261026-1350-T018-T020-G2-PLACEHOLDER-IDENTITY-01
Owner E / T018・T020; T019参照のみ。2026-10-26 13:50 JST。STATIC / SYNTHETIC TEST EXECUTED / VERIFY / NOT READY。
## 今回の固有差分
- 12:53世代の`review(g2)`は出撃名簿の文字列型/空白/重複/陣営横断を確認するが、`unit_visible="unknown"`を一見有効な識別子として扱い、他条件が健全ならissues=[]となる。新旧差を合成負例で実行確認。これは原作のBUGではなくEの「要出典ラベル検証」不足。
- E所有 overlay `t020_cnb02_g2_placeholder_identity_review_20261026_13H.py` は正確な placeholder token（casefold+strip）を Unit/Troop/参加Powerラベル別に REVIEW とする。任意の正規名 `Unknown Soldier` には誤検知しない。旗は `G2_UNIT_ID_PLACEHOLDER_REVIEW` / `G2_TROOP_ID_PLACEHOLDER_REVIEW` / `G2_SIDE_PARTICIPANT_PLACEHOLDER_REVIEW`。
- 判定は常に VERIFY_NOT_GOLDEN、actual_golden_pass=false、strict_match=false。実原作上のラベルと見かけの類似は識別子同一・ポインタ同一を証明しない。placeholder辞書は診断上の約束でありゲーム側仕様ではない。
## 実行／証拠
- 新規13/13 PASS、10/25-10/26の既存7世代89/89 PASS、合計102/102 PASS（PC Python -B unittest -q）。合成テストのみで旧EXE新規起動0、Ghidra全解析0。
- 新script実SHA256: 3A1B5F0A10A5F29657FB2CA93D5A4F5ECC755BAE5B35A207A1087D30B5DB92B4。
- 既存REA `BATTLE_STAGE13_INPUT_COVERAGE_20261022.json` 現物SHA256: 17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB。Stage13の延べ4190 Unit観測でrecord/troop参照あり、位置+0x214/所属side+0x1D4未取得という旧証拠を継承。今回新たな原作RAW採取や全RAW独立照合は行わない。
- B側13H新NOTE `data/T028_FALLBACK_GLOBAL_PAIR_RETABI_NATIVE_20261026_13H.md` 実SHA256: 50739E6AD242100598A4A88DD0A484A6A4A9715F33D2155EF19DDCF7AD3BA0D7。0x4E7770のruntime grid mode別グローバル座標対というBのSTATIC仮説を参照のみ。EはUnit位置/格子占有/G2確定配置へ自動昇格させない。B IDはNOT READYで代理統合0。
## 受入と正本境界
- C-NB02 G0=合法旧UIでの攻撃元・対象と戦闘開始、G1=同一戦闘の直前SAVE実byte SHA＋入力、G2=実MAP SHA/三陣営Power/ordered deployed Unit-Troop/実配置・単一時点が未充足。G3実勝敗/G4戦略World差分未充足。
- 今回新規E gameplay DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。旧Watchの限定native観測とRAW8は歴史的副指標のまま、合成102 PASSを原作PASSへ合算しない。
- MASTER TASK QUEUEをPC上で直接再集計=34（DONE9/IN_PROGRESS21/VERIFY4）。正式cp196・READY596=A115/B229/C136/D116は既存正式値（今回全596 ID再列挙なし）。今回READY追加0、MASTER変更なし。
- T019新確定矛盾0。GameClear DAT13/TXT2は検索範囲差RESOLVED、script2優先順位・phase flag・TXT実読込・GameClear後gwrite復帰はVERIFYを維持。
- 旧T018表境界・E session join/DAT追記・C T026/T032・D T030 TSV・0x5710C0ほか既拒否はBLOCKED維持、別tool/shell/path/Remote/ZIPで再試行しない。過去13H/14H OFFLINE-UNSYNCEDは未正式統合。新拒否0・新接続障害0。
- 今回書込はE-own新T020コードと本資料のみ。MASTER・A-D・REA・dev_lab・原本EXE/DAT/SAVE/ZIP・Git/push・Work・設定・automation変更なし。
- NEXT: placeholder検査追加を続けるより、同一合法C-NB02 runのG0 UI・G1 SAVE/input・G2 MAP/3side/roster実証を最優先。B新T028はREADY後だけsource/owner/時刻/合意/競合/重複をEが再照合し、一度だけ正式統合候補とする。
