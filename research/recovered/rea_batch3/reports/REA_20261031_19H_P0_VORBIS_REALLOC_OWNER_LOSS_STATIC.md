# REA 2026-10-31 19H｜Vorbis list-maintenance realloc失敗時の所有参照喪失（P0）
研究ID: `REA-LOCAL-20261031-19H-P0-VORBIS-REALLOC-OWNER-LOSS-STATIC-01`
Owner: REA / Task T015 / 状態: **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。18Hのbitbuffer teardown研究の後続。既知の15スロット解放、index7例外、NULL slot問題は再発見として数えない。

## 出典と重複
- 認可済み研究用PE: `rea_lab/targets/hakushin067_Vahren.exe`, SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9読取専用: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`。既存入口 `00_START_HERE_UNIFIED_V9_20261023.md`。従来指定README/BUILD_MANIFESTはENOENT（接続障害・安全拒否ではない）。
- 既存18H `REA_20261031_18H_P0_VORBIS_BITBUFFER_TEARDOWN_STATIC.md`、`REF_AUDIO_VORBIS.md`、knowledge/kb.py addr/docs/research、symbols.tsvと照合。既存研究全文中は旧call参照2件だけで、本失敗時の所有権差分は未整理。新発見として計上するのは **失敗時の+0x44上書き条件**のみ。

## 新規STATIC（元PEから独立読み戻し）
- `0x005D49F0..0x005D4A52` は `outer+0x54` の単方向リストを、各ノードの次ポインタ `node+4` を退避してからペイロード・ノード順にfreeし、`outer+0x54/+0x48`をNULLにする。
- `0x005D4A23`は `outer+0x50`を取得、`0x005D4A26/28`で0か検査。**非0の場合のみ** `0x005D4A2A..0x005D4A34`で `realloc(outer+0x44, outer+0x4C + outer+0x50)` を呼ぶ（E8 `0x005D4A34→0x005C30BE`）。
- `0x005D4A39 mov [edi+0x44],eax` は成功判定を介さず、**reallocの戻り値を旧所有ポインタに上書き**する。その後 `outer+0x4C`を加算し、`outer+0x50`をゼロにする。
- 内蔵CRT `0x005C30BE` の元x86でも、非ゼロ要求でHeapReAllocが失敗した場合のNULL返却経路（`0x5C3105/07` 判定、`0x5C3133 xor eax,eax` 等）がある。ただし**要求サイズ0なら `0x5C30DC..E5`で旧領域を解放しNULLを返す正常動作**なので混同しない。
- `0x005D4A60` は `0x005D4A6C` で前記helperを呼んだ後、`0x005D4A77/79`で更新後の `outer+0x44` を検査し、非NULLならfreeする。従って要求サイズが正、旧所有ポインタ非NULL、realloc失敗、別所有者が無い条件では、旧バッファ参照を失いcleanupでもfreeされない**条件付きリーク候補**になる。
- V9 E8 callerは `0x5D4654→0x5D49F0`、`0x5D47A0→0x5D49F0`、`0x5D4A6C→0x5D49F0` の3件。解放側経路 `0x5CF9F3→0x5D4A60`、`0x5CFB96→0x5D4A60` もネイティブ照合。

## INFERRED/VERIFYと先行関数
- `0x005D4980`のV9疑似Cでは、容量不足時に旧バッファをリスト化し、旧使用サイズを `outer+0x50`へ加算し、新しい領域をmallocする。今回確認した `+0x50!=0` の値の由来として整合するが、同関数の全分岐・malloc失敗・ABIは**次回元ASM検証対象**である。未検証のままSTATIC完了へ昇格しない。
- 原作実行でのOOM、割当失敗時の到達性、別エイリアスによる生存、同期状態、reallocの新ハンドラ副作用、サイズ計算のオーバーフロー、実際のリークは**未実測**。再現・攻撃可能性の主張はしない。
- `0x5CF9E0` は `outer+0x1E0/+0x250` の解放と状態2への変更を行うが、Ghidraの `unaff_ESI` はABI未確定。通常ゲーム経路が条件付きリーク前提を満たすかは未証明。

## 証拠・保存・再開
- 独立監査：`REA_20261031_19H_P0_REALLOC_OWNER_AUDIT.py` **47/47 PASS**、V9ではなく原作専用PEから3窓SHA、21命令bytes、8直接E8を確認。機械可読証拠 `REA_20261031_19H_P0_REALLOC_OWNER_EVIDENCE.json`。
- 別プログラム `REA_20261031_19H_P0_REALLOC_OWNER_READBACK_VERIFY.py` による保存後の元PE・証拠照合 **43/43 PASS**。`REA_20261031_19H_P0_REALLOC_OWNER_READBACK.json` に保存。原作ゲーム/Ghidra/REAを起動しない。
- 正式5種info/pseudo/assembly/callers/calleesの**新規完備0**、正式VERIFIED新規0。既存64件を二重計上しない。QUEUE/PROGRESS正式TODO/VERIFY/BLOCKED差分0/0/0。Golden実測PASS0／strict MATCH0／完全複製率不明／READY0。
- 接続正常、`active.lock`なし、Java/Ghidra競合プロセスは観測0、空きRAM開始時約16.07GiB。CPU負荷・総所要時間は不明。共有knowledge、MASTER、QUEUE、PROGRESS、Git、原作/他owner/スケジュールは無変更。
- **KB_CANDIDATE**: `0x005D49F0`, `0x005C30BE`, `outer+0x44/+0x4C/+0x50/+0x54`。source原作SHA・3窓sha・8 CALLをEVIDENCEで提示。既存18Hと重複しないrealloc失敗時の所有ポインタ喪失候補だけを統合専任に委譲。knowledge本体に書き込まない。
- **次**: `0x005D4980` のnative条件分岐・サイズ更新のproducer証拠を確認し、呼出元 `0x005D45E0/0x005D4780` の `outer+0x50` 再現可能条件、`0x005CFA10` のcleanup前状態を分けて検証する。原作Goldenは別工程。
- **RECOVERY-ID `REA-RECOVERY-20261031-19H-LEGACY-INDEX-PATH-ENOENT-01`**（10月31日19時台JST）: 旧指定 `search_index/README.md` と `BUILD_MANIFEST.json` の直接readが両方ENOENT。接続/権限/安全拒否ではなく、現在のV9公式入口 `00_START_HERE_UNIFIED_V9_20261023.md` に別名CLI/DBが実在することを確認したため、原本・拒否済み旧V3置換は不変更。旧名ファイルの内容・旧manifest比較は未実施、研究結果の未保存なし。次回も現行V9の現物とSHAからread-only照合し、旧名ファイルの作成・代替上書きはしない。
