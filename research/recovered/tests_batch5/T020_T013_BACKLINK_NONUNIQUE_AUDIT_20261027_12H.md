# E-AUDIT-20261027-12H-T020-T013-BACKLINK-NONUNIQUE-01
[OWNER/TIME/STATE] E/T020（T018 Golden誤昇格抑制）、2026-10-27 12時台JST。STATIC / SYNTHETIC EXECUTED / VERIFY / NOT READY。
[PRIMARY] B-20261027-12H-T013-GAMEMANAGER-BACKLINKS-01。B所有 data/T013_GAMEMANAGER_GLOBAL_BACKLINKS_NATIVE_20261027_12H.md（5431B、B保存receipt SHA256=2C4DA4C87D0830B1747A87003F673D41B1B65E39B2B66AB81DED9C4D197F5126）。原作PE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（Bの実byte照合記録、E今回EXE再hashせず）。
[BASELINE] 11H Eテストは M_register=[H+4]+0xC、M_tick=Main+0xC なので [H+4]=Main を必要条件とした。これは登録元HがUnit様S+0xC由来であることや同じruntime instanceの証明ではない。
[B12H NEW] Main=0x008BE2F0、M_tick=0x008BE2FC。Hwin=0x008BE378 の writer 0x004B9F36、Hscene=0x008BE7F4 の writer 0x0048A5F4、Haux=0x00AAD7A4 の writer 0x00471640 は、それぞれ H+4=Main を静的に構築し得る。Hwinは 0x00553B6E で初期化前に+4をzero化する局面もある。
[EXE CALL SITE] B元PE確認 E8 5/5：0x555E3D→0x4B9930、0x4B79B8→0x4B9E50、0x4B79D6→0x48A5B0、0x4B79E0→0x471640、0x4B99E0→0x4C24B0。EはBのASMと領収証をread-only照合、新規Ghidra・PE逆解析0。
[STRICT NEGATIVE] 異なる3種のHが同一Mainを指し得るため、M_register==M_tick を確認しても S+0xC にどのHが入るかは一意にならない。「backlink一致」「manager数値一致」「Unit→holder出典」「初期化段階」「同一run/generation」「合法原作採取」は別のgate。
[T020 EXECUTED] tests/t020_t013_backlink_nonunique_gate_20261027_12H.py と tests/T020_T013_BACKLINK_NONUNIQUE_CASES_20261027_12H.jsonを新規作成。合成fixture11件、unittest5/5 PASS、python -B exit 0。初期化前・wrong backlink・wrong pointer・offset違い・foreign EXE・Unit link未証明・合成を実機扱い・実機証拠SHA不足を負例化。元の11H fixtureは変更しない。
[T020 LIMIT] この検証は合成fixtureの自己整合性テスト。B12H原作writerが当該Heal実行で到達したという主張ではなく、S+0xCのwriter実体・Hの型・動的Task登録先・効果/HPの観測はVERIFY。原作バグ認定0。
[G0/G1/G2] 無改変原作EXE・20倍強化前DATの同一合法旧UI開戦(G0)、同run戦闘直前SAVE実バイト+SHAと入力時刻/操作SHA(G1)、MAP実ID+SHA・攻防支援三side・順序付出撃Unit/Troop名簿(G2)が未揃い。manager一致をG0～G2 receiptの代替にしない。G3実戦結果/G4戦略World差分も未充足。
[GOLDEN] 新規E original DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。実機/旧新比較NOT RUN、新規正式READY統合IDなし。
[T019] GameClear DAT13/TXT2の字句検索source-scope差RESOLVED維持。script2重複定義優先・phase flag・TXT runtime採用・後続gwriteはVERIFY。新規確定矛盾0、既拒否済XREF未再照会。
[MASTER] 最終正式既知checkpoint196・READY596(A115/B229/C136/D116)。34 Task DONE9/IN_PROGRESS21/VERIFY4、ID重複0は11Hに独立確認した旧値を継承（今回READY履歴全件とTASK QUEUEは再集計していない）。B12HはNOT READYなので代理統合しない、MASTER編集なし。
[SAFETY/UNSYNCED] 既存T018表境界/session-join、T019 XREFとE-RC-20261027-0652境界事故、C T026/T032、D T030 TSV、禁止0x5710C0他はBLOCKED継続。拒否済対象を他tool/path/Remote/ZIPで迂回しない。旧OFFLINE-UNSYNCEDは未正式統合。A-D/REA/dev_lab/原本/Git/Work/設定/schedule変更0。
[NEXT] B ownerが合法S+0xC writerを確定した後にHwin/Hscene/Hauxから識別し、同一runで登録/更新のmanagerと生成世代を照合。Eの優先はC-NB02合法G0→G1→G2 receipt確保。B READY後のみowner/hash/time/duplicate/競合確認し正式統合を判断。
