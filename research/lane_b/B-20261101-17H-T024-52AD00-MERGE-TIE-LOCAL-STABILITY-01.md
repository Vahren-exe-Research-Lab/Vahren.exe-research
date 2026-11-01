# B research intake — verified PC-owned evidence
research_id: B-20261101-17H-T024-52AD00-MERGE-TIE-LOCAL-STABILITY-01
owner: B
source_relative_path: data/T024_52AD00_MERGE_TIE_LOCAL_STABILITY_NATIVE_20261101_17H.md
source_sha256_verified_2026-11-02_JST: B548261CF6A0A2C3968F2D7166183351CC3A70C43FDD1C60B5BDD3218656713E
intake_status: PUBLISHED_INTAKE / NOT_CURATED / STATIC-VERIFY / NOT_READY
original_gameplay_Golden_PASS: 0
strict_MATCH: 0
source_note: The research below is the B-owned source report; its historical OFFLINE state describes its original capture. This archive was staged after source-file SHA confirmation on the authorized PC. Native ABI and game behavior remain unproven.

---

# T024｜0x52AD00 連結リスト・マージ同距離分岐（2026-11-01 17H JST）

研究ID：B-20261101-17H-T024-52AD00-MERGE-TIE-LOCAL-STABILITY-01｜owner=B｜Task=T024（T011への位置依存影響）｜STATIC/INFERRED/VERIFY/NOT READY
**接続状態：PC ONLINE。** Local CompactでMASTER、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、T024、knowledge README/SYNC_STATUSを閲覧。HANDOFF直前は02H。旧search_index/README.md・BUILD_MANIFEST.jsonはENOENT（V9移行既知、接続障害ではない）。
**先行重複：** 13Hの距離ソート、14Hの32bit overflow、15HのNaN非推移性、16HのSAR中点丸めは既成果。今回の新規局所結論は同距離の2リスト・マージの左側優先（global stableとは別）。

## 関数・静的制御と証拠
- 原作対象PE SHA-256（V9マニフェスト）：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今run原本を再hash/実行していない。
- V9 search `function 0x0052AD00`: entry 0x52AD00、サイズ129 B、関数範囲0x52AD00～0x52AD80、Ghidra擬似Cは STATIC／ABI未検証。
- 0x52AD35 `E8 F6 B2 FF FF`→0x526030（距離比較）；0x52AD3A `84 C0` TEST AL；0x52AD3C `74 1B` JE comparator=false branch。
- Ghidra保存擬似Cでは comparator false のとき左側ノード `puVar2=*puVar2` に進み、true のとき右側ノードを左側の前へ 0x4C5800 でsplice。後段は残った右suffixを 0x4C5800 で移す。
- 0x52AD4C `E8 AF AA F9 FF`→0x4C5800、0x52AD72 `E8 89 AA F9 FF`→0x4C5800（残りsuffix）。後者の直接CALLを今回V9で追加クロス照合。
- 上位 0x529DC0 のマージ箇所は 0x529EAE / 0x529F04 / 0x529F74 → 0x52AD00 の3 E8直接CALL。以前の0x5296A8・0x529868→0x529DC0は旧13H成果であり再計数0。
- 15H静的証拠の0x526030：通常有限同距離で結果AL=0。したがって**局所マージに入力された左右先頭が同距離なら左側先頭を先に残す**（STATIC + INFERRED）。
- 合成例 left=[5A0,5A1], right=[5B0,5B1] は A0,A1,B0,B1。これは擬似実装の独立算術テストで、原作DYNAMIC/Goldenではない。
- **重要な制限：** 26bin上位マージのrun投入順序、0x4C5800の全副作用、NaN/overflow、alias、元リストの順番は未確定。よって全体ソート安定性は VERIFY のまま。最終AIの攻撃対象や移動先を確定しない。

## 既存根拠・知識照合・KB候補
- 13H旧静的JSON `data/B_OFFLINE_20261101_13H_DISTANCE_SORT_EVIDENCE.json` の機械語bytes・直接CALLと、PC V9 pseudocおよび上位CALLを照合。旧13H JSON SHA256=1C2030F7A1D8EB12A5E97F51509C70FA1BA25ADD600C271A5DA23516939A0205。
- 統合V9 DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。`v9_coverage.py --inspect 0x0052AD00`: E8 caller3/callee3, unresolved0, dictionary登録0。`knowledge/kb.py addr`では未命名・関連索引0。GitHub private developのV9 B REVIEWとcuration protocol読取専用照合。
- KB_CANDIDATE: owner=B/T024、VA=0x52AD00、CALL=0x52AD35/4C/72, 上位0x529EAE/0x529F04/0x529F74、source=V9 0x0052AD00 pseudoc＋元PE命令bytes、STATIC/INFERRED/VERIFY、NOT READY、Golden0、全体安定性未確定。共有KBは専任キュレーターのみ更新。

## 安全・未同期復旧・Golden
- 16H一次報告・証拠JSON・verify.pyをB所有 data/へ保存し実byte SHA照合済（3/3）。16H Libraryの旧readback receiptも別SHAでPCへ保存。**会話内16H最終receiptとは不一致**。詳細は当該B HANDOFF復旧節。16HオフラインHANDOFF deltaの正式統合・7～15H分45成果の同期・3H保存障害は未完了。
- 既存 SAFE134は10/31最終値を継承し今run全件再検証0。HOLD21安全拒否と10/25元文章・GitHub B raw回収gapは継続BLOCKED。今回新安全拒否0、旧拒否迂回0。
- 原作ゲーム実機Golden PASS=0、strict MATCH=0、DYNAMIC=0、新B READY=0、MASTER新統合=0、Task DONE増加0。
- 必要なGolden：ユーザー未改変原作DAT（10/22空手20倍テスト改変を排除）、同SAVE/MAP/input/RNG/tick、同距離左右複数Unit＋異距離混在、実listと後段0x569730/行動/対象観測。DESIGNED/NOT RUN。
- 次回：先に07～15H原ファイルと正本owner/研究ID/矛盾を一度だけ照合・回収。続いて 0x4C5800 のノード操作と 0x529691/0x529851 の基準座標、最終target、T011/T012/T013/T028 P0へ。禁止VA等に非介入。


### 17H補強：0x4C5800 もV9で読取専用確認（同一ID、別READYにはしない）
- 統合V9 `function 0x004C5800` は118B、0x4C5800～0x4C5875。Ghidra擬似C上でノードprev/nextの複数ポインタを書き換え、移動元と移動先listが異なる場合には個数フィールド `+0x4` を増減する。
- `0x4C5819 E8 4F 03 0F 00`→`0x5B5B6D` は要素数上限 `0x3ffffffe` との比較後の例外経路。通常ノードsplice解釈を補強するが、callee ABI未検証・境界到達性VERIFY。
- 元の `0x52AD4C/0x52AD72→0x4C5800` のマージ二経路とは区別し、0x4C5800自体は新規独立Golden/READYには昇格しない。左側優先の結論は有限の同距離かつ正常listの局所分岐に限定。
