> E owner historical source; PC source `tests/T020_DEMO_SOURCE_TAIL_PHASE_CROSSWALK_20261024_0153.md`; original SHA-256 `3168957947EA94F2BED5053B1F34732CC43FC000A81AD7C87F782E9A6D60A4D4` (independently checked 2026-11-02); redacted safety-refusal scope. Archived STATIC/SYNTHETIC/VERIFY, NOT_CURATED, not original Golden or READY. Historical test results below were not rerun in this intake.

# 研究E｜T018/T020 DemoPersonソース選択・後段仮想CALLの時相別証拠ゲート
ID: E-AUDIT-20261024-0153-T018-T020-DEMO-SOURCE-TAIL-PHASE-01 / owner E / STATIC CROSSWALK + SYNTHETIC / NOT READY。
## 出典・正本
- PC: Desktop Commander Local Compact。MASTER_LEDGER.md最終実読checkpoint196、READY596=A115/B229/C136/D116（2026-10-22 03時台の正式値）。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧値・今回全件再計算なし。
- 既存規約・A-D HANDOFF・REA PROGRESS/保存RUN・dev_lab実装計画・T018/T019/T020・検索README/manifestを先読。PCオンライン・E testsへの書込のみ。
- 原作EXE識別SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。REA 01:37所有資料が原作PEを照合済み、今回Eは原作PEを再SHAせず。
- REA read-only 2026-10-24 01:37研究本文 SHA256 842397FAEFFFD3860FDE70A46CC024D608FA5AA69B4C4442146727889BE48ED0、JSON証拠 SHA256 A797B683BF88311189F9041D54ABC0AEB7006413549AE3FA0F7171435296D686。両方E側で実バイトSHA再照合2/2 PASS。
- REAの別READBACK文書では指定31命令＋vtable1＋rel32 3を35/35 STATIC検証。REA状態READBACK VERIFIED/STATIC/VERIFY/NOT READY。新正式Wave証拠0・原作Gameplay0。
- REAは統合V9 SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDEを利用。PC標準V3は未変更。今回EはV9/Ghidra再実行なし。
## 新しいEの一対一受入差分
- 0x40F383 E8→0x597B00 の候補sourceを0x8B8E60へ、0x40F398 E8→0x583C70 の候補sourceを0x8B8E64へ保存。探索基点・fallback・比較fieldが異なるため、2つのsourceを同じ選出アルゴリズムとみなさない。
- 0x583CE6→0x597B00はE9 tail JMP。擬似Cの関数呼出風表記からE8 CALL/新規stack frameと推定しない。E側JSON機械検査でselector A/B、tail siteを確認。
- 既存+0x08初期化2件(0x40F3D6/0x40F3F3)→中間処理→+0x0C間接CALL(0x4103D5/0x4103E2)2件。初期化終了=直後callback/継続実行完了としない。
- DemoPerson主vtable [0x63803C]=0x447810 は静的配置。実行時vptr・object identity・関数の正常復帰はVERIFY。+0x14 sourceは選出候補であり実際のUnit/Troopロスターではない。
- 0x4478D5で+0x14 NULLなら0x4478D8→0x44861Aへジャンプし、当該呼出しの+0xA5の0/1再設定を飛ばす。従って旧+0xA5値の残存可能性を排除せず、見かけのフラグだけから新しいsource有効化を確定しない。
- NULLでない場合も+0xA5 zero書込→RTTI→条件付き1書込であり、0/1の意味と戦略への副作用はVERIFY。初期化+0x20=100を後段+0x0C直前も100、HP/士気/勝敗と断定しない。
- G2の合法なMAP・攻撃/防御/支援の三陣営・ordered deployed Unit/Troopは別の旧ゲーム観測でしか満たせない。二つのDemoPerson存在・仮想CALL成功はG2受入不可。
## T020実装と実行（E独立の合成負例）
- fixture: tests/T020_DEMO_SOURCE_TAIL_PHASE_NEGATIVES_20261024_0153.json。SHA256 3A33E5CC102E311D1C12FAD141CA7BD7572FE3014DE215AD77807857CA81C216。
- checker: tests/t020_demo_source_tail_phase_gate_20261024_0153.py。SHA256 9E267A53BCD59927CBE6A20E63FD88D3CC376257B04118E1724C5104AD8DE305。
- 新規16ケースをrun同一性、E9/E8種類、runtime vptr仮定、+0x0C実行、同一呼出し+0x14/+0xA5書込、誤G2昇格で分類。CONTRADICTION_SAME_INVOCATIONは『同一callback実行内』に限る条件で、別処理のwriteとの矛盾を意味しない。
- Local python -B -X utf8 実測: source_sha_verified=2, static_claim_checks=4, synthetic_fixture_pass=16, fail=0。出典・定義の自動照合であり16件の原作実戦ではない。
- 保存後Localのread_multiple_filesでfixtureとcheckerを直接再取得。原作Gameplay NOT RUN、T018 Golden compare runner NOT RUN、actual Golden PASS0、strict MATCH0、E新規DYNAMIC OBSERVED0。
## T019・正式状態・次
- T019新確定矛盾/原作確定バグ0。GameClear DAT13/TXT2は字句検索範囲差のRESOLVEDを維持。script2同名優先・phase flag・TXT実読込・gwrite復帰はVERIFY。
- C-NB02 G0合法旧UI、G1同run直前SAVE実バイトSHA+入力、G2実MAP/3side/ordered roster、G3終了、G4戦略復帰World差分は今回もE完全受入未充足。source/selectorのみで証拠空欄を埋めない。
- 正式READY追加0・MASTER統合0・Task DONE増0。旧OFFLINE-UNSYNCED暫定26研究は未照合/未統合。B 01:10・REA 01:37ともNOT READYなので代理採録しない。
- [SAFETY_HOLD] 以前に拒否された内容・操作は、本入庫の対象外。拒否のメタデータのみ保全し、再試行・代替経路は使用しない。
- NEXT: 合法同run G0/G1/G2のsource-backed receiptsを優先探索。+0x14 source2系統の入力由来・+0x0C前の値変更・runtime vptrはREA所有のVERIFYでありEが代理修正しない。

## fixture判定の狭い適用範囲（実装誤読防止）
- JSONの`kind`は命令site 0x583CE6に対するE9/E8の証拠表示であり、全ての第2source選択でそのジャンプが実行される意味ではない。第2selectorの成功・fallback、遅い+0x0C呼出し、各時相は独立。`tail`は遅い+0x0C仮想CALLの観測有無で、0x583CE6の実行有無ではない。
- `write=seen`は0x4479C5/0x4479F5という既知の+0xA5書込siteが**同じ+0x0C関数呼出しで実際に通過した**という仮定に限定する。外部コードや別時相での+0xA5更新とは混同しない。実機site trace無しの現在値=1だけではCONTRADICTIONとは認定しない。