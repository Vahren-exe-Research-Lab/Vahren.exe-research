# 研究E T020｜退却Spot全木clearの分岐・寿命境界（2026-10-30 03H）
研究ID: `E-AUDIT-20261030-03H-T020-T028-FULLTREE-CLEAR-SPLIT-01`
状態: `STATIC SOURCE-PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY`。原作ゲーム・新エンジン未実行。
## 出典と一対一照合
- 原作B owner研究: `B-20261030-0308-T028-FULL-TREE-CLEAR-POSTORDER-01`、`data/T028_SPOT_FULL_TREE_CLEAR_RECURSIVE_DESTRUCTOR_NATIVE_20261030_03H.md`。実バイトSHA256 `2CE7A4F828C2D749E30E63E7B78A46A8A5B3DEC06E535F5A79F1DB2FB201AB52`。BはVERIFY/NOT READY。
- 先行B02H: `data/T028_SPOT_TREE_ERASE_STRING_RELEASE_NATIVE_20261030_02H.md`、SHA256 `1C95D49A632F3C27B800C774E6CA738A4CF58116D96709587FDC8823225F5AAF`。
- EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` / V9 DB `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` はBの照合値。E本回は元PEとDBの再ハッシュ無し。V9入口資料を再読、旧README/BUILD_MANIFESTに依存せず。
## 新規STATIC受入境界（B03Hから）
- `0x415CF0` full-range成立時 `0x415D0A CALL 0x416870`。partial `0x416220`と区別し、前回E02Hの個別node count--と混同しない。
- `0x41687E/81` node+0x29 nil候補で帰還。valid側は `0x416889 CALL 0x416870` でbranch+8側を再帰し、`0x416892`からbranch+0側を後続反復。名称branch8/branch0は機械上の位置名で、右/左等のゲーム意味ではない。
- `0x41688E..0x4168B0` capacity>=16なら文字列heapに `0x5B6BBB`、どちらの容量でもnodeに同関数をCALL。実free成功・二重解放不存在は未証明。
- `0x415D0F..0x415D23` head3リンクの自己参照復位＋count=0一括reset。partial eraseの条件付きcount--とは別契約。
- `0x416870`の36件E8 caller matchはgeneric helper推定であり、各callerの合法到達、所有コンテナ、同じSpotの+0xB8予約解放は未確認。
## T020新規合成回帰と既存回帰
- `T020_E_T028_FULL_TREE_CLEAR_CASES_20261030_03H.json`: 30例（空木、cap0/15/16/17/128、branch8/branch0/混成、partial/full混同、count不整合、alias/cycle/orphan、nil marker、actual Golden誤認）。
- `t020_e_t028_full_tree_clear_gate_20261030_03H.py`: B02H/B03H source SHA両pinをfail-closedで検査し、構造内の静的CALL候補数・分岐順・full時count0モデルと負例を照合。新規30/30 PASS、source2/2 PASS。
- 既存7本を同一PCで軽量再実行: 21H 8/8、22H 18/18、23H 21/21、00H 18/18、01H 22/22、02H 28/28、03H 30/30。合成145/145、Python 7/7 exit0。`03H`は新規30件であり他115件を新規と二重計上しない。
- モデルは元EXEの正確な再帰実装・heap解放・失敗例外・実ゲーム退却や戦略commitの互換性を証明しない。shared child/cycleは合成fixtureでfail-closedにし、原作BUGと断定しない。
## Golden / T019 / MASTER
- T018合法GoldenのG0には限定的旧原作開始観測あり。同一run G1直前未改変SAVE+入力、G2 ACTIVE時MAP/攻防援軍とordered Unit/Troop、G3/G4実観測の結合証拠なし。正式DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
- T019 GameClear DAT13/TXT2字句検索scope差のみRESOLVED、`script2`優先・phase flag・TXT実読込・`gwrite`復帰・`decide11`用途VERIFY。今回新規確定矛盾0。
- MASTER末尾の最終正式checkpoint196/READY596=A115/B229/C136/D116、新規正式統合0。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値（全件再集計していない）。B03H NOT READYのためMASTER未変更。
## 保存・安全・再開
- E所有の新規fixture/検証器/本報告のみ追加。既拒否T018表境界、E session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0等はBLOCKED、再試行/迂回0。OFFLINE-UNSYNCED全件の意味重複・READY照合は未完了。
- 原本EXE/ZIP/SAVE/DAT、A-D/REA/dev_lab、Git/push、Work、MCP設定、他schedule変更0。今回安全拒否0、PC接続障害0。
- 次は `0x495580`後のUnit+0x1B4参照寿命・Spot+0xB8との独立性、全木clearの実callsite/return時の不変条件をB新証拠で照合。最優先G0/G1/G2同runの合法原作receiptを継続して探索する。
