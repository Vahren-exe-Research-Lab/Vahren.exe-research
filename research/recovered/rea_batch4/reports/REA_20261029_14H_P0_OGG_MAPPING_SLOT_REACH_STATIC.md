# 迫真戦記 REA｜2026-10-29 14H Oggモード0 NULLコールバックとmapping間接到達性
研究ID：`REA-LOCAL-20261029-14H-P0-OGG-MAPPING-SLOT-REACH-V9-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。対象ゲームは未実行。今回の新規REA正式5種=0、正式VERIFIED増分=0。
## 既存証拠・環境の照合
- 開始時にMASTER/担当規約/REA README・QUEUE・PROGRESS、最新有効sync、前13H成果を先読。旧Wave1〜5の正式STATIC VERIFIEDは64/64、13H監査は73/73 PASS。QUEUE/PROGRESSは既知のEPERM stale、同期ログを正とする。
- 原作隔離コピー SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` に一致。開始時 active.lock なし、先行Java/Ghidraなし、空きRAM約13.55 GiB。CPU負荷・作業全体の時間は未測定。
- **作業中の外部変更**：2026-10-29 14:46 頃、別担当のユーザー承認済み整理で旧 `search_index/search.sqlite` がごみ箱へ移動。旧CLI呼出しが途中から失敗した。原因は `headless_analysis/CLEANUP_20261029.log` と `00_START_HERE_ACTIVE_RESEARCH.md` で確認した。安全拒否ではない。整理を取り消したり旧DBを復元・再抽出したりしていない。
- その後、現在の正本である統合V9 `HAKUSHIN067_UNIFIED_V9_20261023.sqlite`（SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`）へ読取のみ切替。V9 quick_check=ok、関数0x005DEDF0既存エントリ確認。V9の擬似Cは未修正原版、ABI未検証。
## 今回のP0：間接CALLの実際の参照スロット
- `0x00612E6C` に格納されるポインタは `0x0061AE40` の5関数テーブルを指す（原作PE32のlittle-endian word照合）。
- テーブル各スロットは +0=`0x005DEA60`、+4=`0x005DEBD0`、+8=`0x005DEA30`、**+0x0C=`0x005DEDF0`**、+0x10=`0x005DF7D0`。原作PEで`0x005DEDF0`を保持する32bit wordは`0x0061AE4C`の1地点。
- `0x00612E6C` を静的参照する命令はPE上で3地点。**`0x005D3E31→0x005D3E39→CALL 0x005D3E3C` は+8**、**`0x005D432A→0x005D4334→CALL 0x005D4339` は+4**、**`0x005D4767→0x005D476E→CALL 0x005D4773` は+0x10** を選択。少なくともこの既知3箇所では +0x0C の `0x005DEDF0` を選択しない。
- ただし、関数ポインタの別保管・動的解決・未知の呼出し経路は未排除であり、**`0x005DEDF0` を到達不能・未使用とは断定しない**。ここまでの成果は、前13Hの表同定と二重計上しない補強である。
- `0x005D4160` は `0x005D428F LEA EDI,[EBX+0x620]`、`0x005D42A0 MOV [EDI-0x100],EAX` により**`+0x520`へmodeを書き込んだ後**、`0x005D42A8 JS` および `0x005D42AE CMP EAX,3` / `0x005D42B1 JGE` で範囲外を拒否する。通常成功経路の値は0～2だが、範囲外が失敗後も残存するかは未調査。
- `0x005DEDF0` 内の `0x005DF703`→`0x005DF717 CALL ECX` はモード表+0x14、`0x005DF769`→`0x005DF788 CALL EDX` は+0x18。mode0で両スロットはNULL。**mode0で当該地点に到達することは未証明**、実際のNULL CALL/クラッシュの確認なし。
## 進捗と許可範囲
- 新規静的監査 `REA_20261029_14H_P0_OGG_MAPPING_SLOT_REACH_AUDIT.py`：**40/40 PASS、1.474秒**、SOURCE/V9 SHAとSQLite整合、PEテーブル・機械語17地点・既存結果を照合。初回のmmap.count実装誤りは新規自作監査を修正して再実行し解消。
- 5種の根拠：info=V9 function record、pseudo=既存V9 Ghidra未修正擬似C、assembly=PE局所Capstone、callers=保存済directゼロと表の静的xrefs、callees=保存済参照情報および局所CALL。**新規REA正規5種証拠束は取得していない**。
- 正式STATIC VERIFIED=64/64維持、新規VERIFIED=0、正式TODO/VERIFY/BLOCKED差分0/0/0。原作ゲームGolden実測PASS=0、完全複製率=未測定。別担当が保全する10/28未同期オフライン研究は統合していない。
- 原本ZIP/EXE/SAVE、MASTER、他レーン、QUEUE/PROGRESS、既存runs、Git、公開先、スケジュールは変更していない。REA所有の新規スクリプト・証拠・本報告のみ作成。
- **次回**：`0x005DF7D0`（既知+0x10の実際のmapping consumer）、`0x005D45E0`（CALL 0x005D4773を含む関数）、`0x005D4160` のエラー片付けを照合し、`0x005DEDF0` の+0x0Cスロットへの到達条件・mode0のNULL CALL可否を再評価。
