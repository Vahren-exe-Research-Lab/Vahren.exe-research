# REA｜2026-10-31 15H｜Vorbis post-initialize の戻り値破棄と正常初期化の前提（P0）
研究ID：`REA-LOCAL-20261031-15H-P0-VORBIS-POSTINIT-RETURN-LOSS-STATIC-01`。Owner=REA、Task=T015、状態 **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。
14H `REA-LOCAL-20261031-14H-P0-VORBIS-WRAPPER-DOUBLE-CLEANUP-GATE-STATIC-01` に対する新規差分。13Hの条件付きcleanupリーク、12Hの88h calloc null-write、14Hの二重cleanupを再計上しない。

## 正本・既存成果・安全の確認
- MASTER末尾/レーン規約、REA README/QUEUE/PROGRESS、最新正式 `logs/progress_sync_20261011T153958076Z.json`（64/64）、12H・13H・14H報告と14H evidence、knowledge README/SYNC_STATUSをread-only確認。
- 原作同一研究用PE `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、quick_check=ok。標準V3の既存ポインタは変更せず、V9別名検索CLIを使用。
- 旧 `search_index/README.md` / `BUILD_MANIFEST.json` は既知の現行配置差異で未存在（14H時と同様）。V9の `00_START_HERE_UNIFIED_V9_20261023.md` を使用し、拒否操作の迂回はなし。
- `knowledge/kb.py addr/docs 0x005D4D20` は未命名・研究索引未言及、非公開GitHub `develop` の Vorbis参照文書は本15Hの差分を未収録と照合。直接編集は禁止。
- PC Local接続可、開始時 `active.lock` 無、可用RAM **約18.5GiB**、Java/Ghidra競合プロセス出力なし。CPU負荷・作業全体の所要時間は不明。原作ゲーム、REA/Ghidra新規解析、DLL実行なし。

## 新規差分：post-initの失敗がwrapperの戻り値へ伝搬しない（STATIC）
- `0x005D4D20` は入力outerの `+0x68`（`0x5D4D2A..2F`）、`+0x04`（`0x5D4D37..39`）、`[outer+4]+0x1C`（`0x5D4D3B..40`）の順にNULLを検査し、いずれか欠損なら `0x005D4D31` から **-1** で早期returnする。正常時のみ `+0x14/+0x30`、複数の-1番兵、`[outer+0x68]+0x80/+0x84` を初期化して `0x005D4D81` から0を返す。
- `0x005D5BD0` は `0x005D5BDE -> 0x005D57C0` の結果は検査するが、成功側 `0x005D5BFB -> 0x005D4D20` の戻り値は検査せず、`0x005D5C03 xor eax,eax` で0を返す。したがって**callee -1をwrapperで1へ変換したり伝搬したりしない**。
- 親 `0x005CF970` は `0x005CF9A1`、`0x005CFA10` は `0x005CFA45` でwrapperを呼び、その戻り値のみ検査してから `0x005D4900` を呼び、`outer+0x58=4` へ進める。新規post-init戻り値検査はこの2つの局所経路では確認できない。

## 到達性の限定：通常成功経路での不具合実証ではない
- 上流 `0x005D57C0` は `0x005D57CA..0x005D57D8` でソース `+0x1C` を先に検査し、NULLならouter memset前に1を返す。非NULLならouter 0x70バイトを初期化、`0x005D57F8` calloc戻りを `0x005D5802` で outer+0x68、`0x005D5805` で入力を outer+4 に保存する。
- 同callocが失敗した場合、既知12H `0x005D5820` のポインタ書込が先行するため、**coreが正常に0を返す経路でpost-initの三つのポインタガードが欠損することは、この通常の逐次経路からは示せない**。破損、再入、alias、OOMの実ゲーム到達性はVERIFY。単に「post-init -1を無視する」ことから実ゲームクラッシュ・初期化成功誤判定を主張しない。
- V9は `0x005D4D20` の直接E8呼出元を3件 `0x005D00E3/0x005D0952/0x005D5BFB` と記録。独立PE E8の呼出先とも一致。前2件の周辺制御フローは今回未確認（インストラクション境界を推測して決めない）。ABIは未検証。

## 独立証拠・進捗・KB候補
- 新規 `REA_20261031_15H_P0_POSTINIT_RETURN_PROBE.py` は許可済みPEの対象rangeのみをread-onlyでcapstone表示。監査 `REA_20261031_15H_P0_POSTINIT_RETURN_AUDIT.py` はPE/V9 SHA・SQLite・24命令・8 E8・関数range・3 caller・前件ID等を再照合 **75/75 PASS（2.0364秒）**。
- 証拠 `REA_20261031_15H_P0_POSTINIT_RETURN_EVIDENCE.json` SHA256 `6A98D1CD772975C70AC49E412C45AD9F693D55F9665040A9F64E8A604609AC8F`。独立 `REA_20261031_15H_P0_POSTINIT_RETURN_READBACK_VERIFY.py` はsource/native bytes/E8/Window/SHAを再読取し **52/52 PASS（0.7673秒）**。結果 `REA_20261031_15H_P0_POSTINIT_RETURN_READBACK.json` SHA256 `5ECD3589FFF98E51194ED8D925B65D291C7A9F0ECF82B3836A73C050FB2BB8FF`。
- REA正式「info/pseudo/assembly/callers/callees」新規5種完備 **0**、正式新規VERIFIED **0**、既存正式STATIC VERIFIED **64/64維持**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。原作Golden実測PASS **0**、strict MATCH **0**、完全複製率未測定。
- **KB_CANDIDATE**：未収録 `0x005D4D20` の三段NULLゲートと-1/0、`0x005D5BD0` 成功側での戻り値破棄、両親callerでのwrapper判定・state4移行。STATICは原作機械語の局所分岐のみ、通常到達可能性INFERRED/VERIFY、DYNAMIC=0、READY=NO。統合専任がsource相対path/本ID/PE・V9 SHAを照合してから登録する。REAは共有knowledgeへ書込まない。
- **再開位置**：`0x005D0020` / `0x005D04E0` の他のpost-init呼出元の戻り値扱い、および `0x005D4900` のpost-init状態利用を限定的に追跡。異常な初期化後の現実到達性は別許可GoldenまでVERIFY。
- 今回新規6ファイルのみREA所有範囲へ保存。原本EXE/ZIP/SAVE、共有knowledge、A〜E/MASTER、QUEUE/PROGRESS/旧RUN、Git/公開/Work/スケジュール/設定の変更なし。新規安全拒否・接続障害なし。
