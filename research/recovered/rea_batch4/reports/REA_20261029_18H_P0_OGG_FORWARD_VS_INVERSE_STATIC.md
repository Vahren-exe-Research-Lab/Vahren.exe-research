# 迫真戦記 REA｜2026-10-29 18H Ogg mapping forward / inverse スロット再分類
研究ID：`REA-LOCAL-20261029-18H-P0-OGG-ENCODE-DECODE-SLOT-CROSSWALK-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作ゲームGolden未実測。従来の「NULL CALL疑惑」は静的条件付きであり不具合確定ではない。
## 先行成果と研究基盤
- MASTER / ANALYSIS_LANES_PROTOCOL / REA README・QUEUE・PROGRESS / 17H証拠と`progress_sync_20261011T153958076Z.json`を確認。QUEUE/PROGRESSは既知のrename EPERMで古く、正式Wave1〜5は保存済みsyncの64/64。17Hのmapping正常count=1〜16は再計上しない。
- 10/29整理後の検索基盤は統合V9。旧search.sqlite・README/BUILD_MANIFESTは存在せず、復元しない。隔離PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
## P0新規：ソース既知のVorbis dispatch契約との独立照合
- PEのmappingテーブル`0x0061AE40`は5スロット: `+00 0x005DEA60` / `+04 0x005DEBD0` / `+08 0x005DEA30` / **`+0C 0x005DEDF0`** / **`+10 0x005DF7D0`**。公式Xiph由来のlibvorbis `mapping0_exportbundle` は **pack / unpack / free_info / forward / inverse** の5スロットであり、この並びと構造的に合致する。
- PEのresidue0テーブル`0x0061AE60`は`+00`、**`+14`、`+18` がNULL**、`+1C=0x005E08A0`。既知の`residue0_exportbundle`でも`pack`、`class`、`forward`がNULLで`inverse`は存在する。よって「mode0でNULL」は**エンコード方向をサポートしない実装の正常な表構成**と整合し、これだけでバグとは言えない。
- 旧16Hの`0x005DF717`（residue表`+14`）と`0x005DF788`（`+18`）は、**mapping +0C=forward の内部**。既知の通常読込では`0x005D4773`がmapping `+10=inverse`を呼び出す。従来「forwardに到達したらmode0でNULL」の静的観測と矛盾しない。
- ソース対照： https://docs.rs/crate/vorbis-sys/latest/source/libvorbis/lib/mapping0.c （mapping0_exportbundle）、https://docs.rs/crate/vorbis-sys/latest/source/libvorbis/lib/res0.c （residue0_exportbundle）。元EXEがこのソースとbyte-identicalだという証明ではなく、**構造・役割の外部独立照合**として使用。
## 上位到達性の追加制約
- V9の`refs-to 0x00612E6C`は **3地点のみ**：`0x005D3E31`（mapping +08/free）、`0x005D432A`（+04/unpack）、`0x005D4767`（+10/inverse）。機械語実装部`0x005D3E39` / `0x005D4334` / `0x005D476E`をCapstoneで独立確認した。
- V9の`refs-to 0x005DEDF0`は**0x0061AE4Cの1件のみ**、`refs-to 0x0061AE4C`は0件、PE HIGHLOW relocationも`0x0061AE4C`1件、native直接E8 CALLは0件。これは**保存済み静的索引で+0Cの使用が見つからない**という限定結論であり、間接alias/動的生成/未認識コードの不存在証明ではない。
- **評価更新**：NULL CALLは「decode経路での既知クラッシュ候補」ではなく、**encode-only forward側へ未知の経路で入る場合の条件付き懸念**へ再分類。優先度は到達性調査のVERIFYを維持し、実ゲーム不具合として登録しない。
## 検証と運用境界
- 新規監査 `REA_20261029_18H_P0_OGG_FORWARD_VS_INVERSE_AUDIT.py`：初回は当方の3個のレジスタ推定違いで **28/31**。原作機械語を読み戻して期待値を修正し、最終 **31/31 PASS・0.832秒**（前回の失敗を隠さず記録）。監査に失敗した初回はEVIDENCE.jsonを作成していない。
- 新規証拠 `REA_20261029_18H_P0_OGG_FORWARD_VS_INVERSE_EVIDENCE.json`：PE関数表、residue表、V9 xrefs、PE relocation、直接CALL、局所ASM、SHAを保存。5種の充足はinfo=既存V9、pseudo=既存V9未修正、assembly=PE局所Capstone、callers=V9 xrefs/0 direct E8、callees=既存V9+PE間接call。**新規正規REA5種束0／新規正式VERIFIED0**。
- 既存正式STATIC VERIFIED=64/64維持、正式TODO/VERIFY/BLOCKED差分=0/0/0。原作Golden実測PASS=0、完全複製率=未測定。研究全体時間・CPU負荷=不明、開始時空きRAM約16.77GiB。active.lockなし、Java/Ghidra先行プロセスは列挙結果なし。新規Ghidra/REA起動なし。
- 原本ZIP/EXE/SAVE、A〜E/MASTER/T018/dev_lab、QUEUE/PROGRESS、既存RUN、検索V9、Git、公開先、スケジュールを変更しない。既存10/28オフライン未同期成果への統合作業なし。
- 次回P0：`0x005DF7D0`に対する実際のinverse側エラー/NULL処理を検証し、`0x005D45E0`の通常 decode 入口と終了契約を静的トレースする。別途`0x005DEDF0`の +0C 経路は**未発見のまま**VERIFY、存在しないと断定しない。
