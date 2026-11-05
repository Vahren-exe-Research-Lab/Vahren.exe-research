# 研究E T020｜退却Spot treeの文字列容量・erase寿命／合成契約（2026-10-30 02H）
研究ID: E-AUDIT-20261030-02H-T020-T028-SPOT-TREE-LIFETIME-PROVENANCE-01
状態: STATIC OWNER-SOURCE PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作Gameplay未実行。

## 出典・非重複
- Local CompactでMASTER・protocol・A～D HANDOFF・DEV計画・E T018/T019・V9入口・B02H owner詳細をread-only確認。旧search_index README/BUILD_MANIFESTは既知移動済みで参照不可、現行V9を旧2026-10-21索引と混同しない。
- 参照B: B-20261030-0215-T028-SPOT-TREE-ERASE-STRING-RELEASE-01（VERIFY/NOT READY）。詳細SHA256=1C95D49A632F3C27B800C774E6CA738A4CF58116D96709587FDC8823225F5AAF、Local実バイト再計算で一致。
- 元PE SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（B側の元PE検証結果を継承。E本回ではPE実ハッシュ/ASM再抽出なし）。V9 DB=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（B側検証、E再計算なし）。
- 既E01Hのflag前erase-range呼出し・0x415CF0 partial/full分岐は既知として再計数0。新規はB02Hの文字列容量閾値/iterator不正/解放順/条件付きcount減算の受入モデル。

## 一次静的報告からの受入境界
- VA0x4160D5 node+0x1C byte lengthと0x4160E4 node+0x20 capacity、VA0x4160E7 capacity<16ならinline、それ以外heap。長さ比較はprefix一致時のみ、非ASCII実encode/辞書順はVERIFY。
- VA0x416224 node+0x29 byteが非0で0x41622F CALL0x5B5BBA（invalid iterator経路）。実合法到達・画面例外はVERIFY。
- VA0x41646A capacity>=16なら0x416474 CALL0x5B6BBB(buffer)→0x41648F CALL0x5B6BBB(node)。capacity<16は前者を通らず後者へ。free実成功・double free不存在・全消去0x416870での同一動作は未証明。
- VA0x4164A2でcount!=0なら0x4164A6/4A7 count-1、0なら減算なし。元のcountが合法に0/非0になる条件と実観測後countは未証明。
- この分岐情報をSpot+0xB8予約寿命・退却成立・画面文言・入力継続・原作BUGの確定へ直接転用しない。

## T020新規検証
- 新規tests/T020_E_T028_SPOT_TREE_LIFETIME_CASES_20261030_02H.jsonに合成28件（capacity 15/16境界、heap/inline free-call、iterator byte0/非0、count zero/nonzero、prefix、非ASCII、未知/不正値、full-clear・Golden誤認）。
- 独立コードtests/t020_e_t028_spot_tree_lifetime_gate_20261030_02H.pyはB詳細のSHA pinをfail-closedし、1/1 SOURCE_PIN PASS、28/28 SYNTHETIC PASS。
- 既存22H容量18/18、23H予約21/21、00H mode18/18、01H erase22/22を変更せず再実行し79/79 PASS。合計107/107はSYNTHETICのみ。旧EXE実機・新エンジン比較0。
- 新規コードSHA256=14478DB07EA0E650EAED6C5F3CC365DD20F4B117E9CA136E9837B74E9DD94745、fixture SHA256=B416AC5974B27EF835681BD8432E9BB87F8DCC78048E13CCB6D3A270A340DAF0（Local実バイト照合）。

## Golden・T019・MASTER・拒否
- C-NB02 G0合法旧UIの限定的旧観測あり。ただし同run直前未改変SAVE+入力G1、ACTIVE時実MAP・攻防援軍3sideとordered Unit/Troop G2、G3、G4の結合一次証拠不足。Golden認定Gameplay DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2の字句検索scope差のみRESOLVED。script2競合勝者/phase flag/TXT runtime/gwrite復帰/decide11用途はVERIFY。
- MASTER最後の正式値cp196/READY596（A115 B229 C136 D116）。34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値（今回全件再集計なし）。B02H NOT READY、新規正式統合0、MASTER不変更。
- 旧T018表境界、E session-join/T019 XREF、C T026/T032、D T030 TSV、0x5710C0等の拒否BLOCKEDを維持。旧OFFLINE-UNSYNCEDのID/意味完全照合未了。拒否操作の再試行・迂回なし、新規SAFETY_REFUSAL0/接続障害0。
- E所有の新規コード/fixture/本報告のみ書込。原本/他owner/REA/dev_lab/Git/Work/設定/schedule変更0。次はBの0x416870全消去と0x495580後Spot参照寿命の出典更新を監査、同時に合法旧原作G1/G2の同run receiptを優先確認。
