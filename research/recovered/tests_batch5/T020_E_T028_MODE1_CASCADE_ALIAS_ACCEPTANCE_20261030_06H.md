# 研究E｜T020 mode1二段階cleanupとalias警戒の受入検証（2026-10-30 06H JST）
研究ID: `E-AUDIT-20261030-06H-T020-T028-MODE1-CASCADE-ALIAS-GATE-01`
状態: STATIC SOURCE-PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。新規公式READY統合0。
## 一次資料・同一性・所有権
- B owner: `B-20261030-0615-T028-MODE1-CASCADE-DTOR-01`, `data/T028_RETREAT_MODE1_CASCADE_DTOR_NATIVE_20261030_06H.md`。B owner `data/T028_MORALE.md`、`evidence/LANE_B_HANDOFF.md`の同ID各1出現を読取確認。
- 06H B詳細をEが独立SHA256再計算: `9942B6B3AA22C2CB93850DBFCAF64A01A4BD0B51F0C0C4F9B3970D0751320BDD`、B側保存receiptと一致。BはSTATIC/INFERRED/VERIFY/NOT READY、MASTER代理READY不可。
- 原作EXE SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` とV9 DB SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` はB静的資料の記録値。今回E自身は原PE/DBの再hash・再逆解析をしていない。
- 旧 `search.sqlite` / `README.md` / `BUILD_MANIFEST.json` は現行位置に存在せず、現行は `rea_lab/headless_analysis/CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` が指定する統合V9。旧2026-10-21件数を新規解析数へ混入しない。
## 今回の局所受入条件
- mode0: 0x5984DF/0x598596でdeep cleanupをskip。ただし旧01Hで確認済みの先行tree範囲erase callsiteは保持する。mode0を完全no-opにしてはならない。
- mode1: vectorの候補各要素で0x598543 `0x467DE0` 返値が非NULLなら0x598553/0x598555 `0x463590` cleanupへ、NULLなら当該候補cleanupをskip。0x59855Aでloop indexを復帰する。
- mode1: vector終了後は0x598591/0x5985A2/0x5985A3/0x5985A5から、第2引数primary objectへの別cleanupを試みる。vector空でもこの経路を維持する。
- `0x463590`は既B 10/28のowner索引整理・destructor様・解放callを参照する。各候補とprimaryの指す実メモリが同一の場合、重複破棄の可能性を**警告**し、エンジンの実際のdouble-free発生・防止は推測で確定しない。
- このモデルのtree_calls=1+vector長は原ASM上のcallsite通過を模した理想正常経路であり、木の削除ノード数・実解放完了を表さない。resolverの返値も注入した合成値のみ。
## T020テスト・比較fixture
- 新規 `tests/T020_E_T028_MODE1_CASCADE_ALIAS_CASES_20261030_06H.json` は正常経路30件＋不正型入力拒否9件（計39）。0/1 mode、vector長0/1/2/3/4、NULL、返値順、candidate-primary alias、candidate-candidate aliasを別々に照合。
- 新規 `tests/t020_e_t028_mode1_cascade_alias_gate_20261030_06H.py` は固定期待値とモデルを比較し、B詳細の実SHAとowner/HANDOFF ID一意を検証する。新規39/39 PASS。
- 既存T028 E合成回帰9検証器をすべて独立再実行し227/227 PASS、総合**266/266 PASS、検証器10/10終了コード0**。いずれもSTATICモデルの自己整合性確認であり、新実装/旧原作とのstrict互換PASSではない。
- 実装側 `dev_lab/docs/IMPLEMENTATION_PLAN.md` はread-only参照。0x598450/0x463590の実装対応・ABI・所有権と当該39 fixtureの一対一実装比較は未検証/NOT RUN。
## T018 Golden / T019
- C-NB02の同一合法原作runでG0 UI→G1直前無改変SAVE+入力→G2実MAP・三陣営・順序付きUnit/Troop→G3結果→G4 World差分を採取するまで不適格。同じPIDでも別戦闘時間窓・戦闘前後の構造snapshotを混ぜない。x20改変DATはunmodified original strict用途へ使用しない。
- 新規Gameplay DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0、実原作GAME=NOT RUN。
- T019新規確定矛盾0。GameClear DAT13/TXT2の字句検索scope差のみRESOLVED、script2同名勝者/phase flag/TXT loader/gwrite/decide11用途はVERIFY。今回のalias危険はT019確定ゲームBUGに昇格しない。
## MASTER・安全・次
- MASTER実SHA=`E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3`。最終正式checkpoint196、READY596（A115/B229/C136/D116）、TASK QUEUE34行の独立再集計 DONE9/IN_PROGRESS21/VERIFY4。新規正式READY0、MASTER変更0。
- 既存T018表境界/E session-join/T019 XREF/C T026/T032/D T030 TSV/0x5710C0等の拒否はBLOCKED維持し、別shell/path/tool/Remote/ZIPによる再試行なし。旧OFFLINE-UNSYNCEDの全件重複照合・同期は未完了。
- 今回の許可E所有tests以外への書込なし。原本/他owner/REA/dev_lab/Git/Work/設定/他スケジュール変更なし。最初のPowerShell二重起動引用符失敗はOTHER（未実行・未変更）、通常のLocal read-only PowerShell再実行で復旧。安全拒否0。
- 次はBの`0x467DE0`戻りのowner+0x1A4副作用・候補/primary alias条件・`0x5AC5EC`後段と、合法G0/G1/G2の証拠を照合。B READY未達のため正式統合は行わない。
