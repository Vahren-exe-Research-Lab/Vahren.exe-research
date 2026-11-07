# 迫真戦記 REA｜2026-10-31 05H｜Vorbis type3 calloc失敗時のNULLガード（P0）
研究ID：REA-LOCAL-20261031-05H-P0-VORBIS-CALLOC-NULL-GATE-STATIC-01
Status：PC-SAVED / STATIC / VERIFY / NOT READY。owner=REA、関連T015（音声）。旧03H/04H成果は再計上しない。

## 新規独立静的証拠（EXE VA/機械語）
1. CRT _calloc（VA 0x005D1C71）は、0x005D1C86 で __calloc_impl（0x005C303C）を呼ぶ。内部は 0x005C307F で HeapAlloc（flag 8=HEAP_ZERO_MEMORY）を実行、0x005C3085でNULLを検査。最終的に 0x005D1CAC でNULLを返す分岐がある。new-handler経由の再試行も存在し、実行時条件は未観測。
2. vendor長 >0：0x005D4061 の calloc(length+1,1) の戻り値は 0x005D4069 で ESI+0xC、0x005D406C でEBXに保存されるが、0x005D407D の mov byte ptr [ebx],al より前にNULL検査がない。確保失敗時はNULL書込に到達し得る。
3. vendor長=0：0x005D406E/4070 の分岐がコピーを飛ばす。comment数=0なら 0x005D40D5/40D8 でリストループも飛ばし、framing bit=1なら 0x005D4142/4145→0x005D415A でtype3は0を返せる。この時 vendor callocがNULLならESI+0xCはNULLのまま。後続type5の 0x005D455B/455E がこれを拒否し-133へ進む。条件付き静的到達性のみ。
4. comment数>0：0x005D40BE/0x005D40C8 の2配列 calloc(count+1,4) は、0x005D4112 の [eax+edi*4] と 0x005D411C の [edx+edi*4] 書込まで、各callocのNULLを検査していない。
5. 個別comment長>0：0x005D4115 の calloc(length+1,1) がNULLなら 0x005D412C → 0x005D3CB0 → 0x005D3CC8 の byte store にNULLが伝播する。長さ0ならhelperの 0x005D3CB8 がコピーを飛ばす。
6. 0x005D3D00 のcleanupにあるNULLガードは、解放時の構造体を守るもので、type3途中の未検査書込を防止しない。

## 監査・出典・進捗
- 研究コピー：rea_lab/targets/hakushin067_Vahren.exe、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原作ソース行番号は存在せず上記VAを出典位置として採用。
- V9：rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite、SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。quick_check=ok、6関数・7 CALL siteのデータと独立PE逆アセンブルを照合。
- 新規資料：REA_20261031_05H_P0_VORBIS_CALLOC_NULL_PROBE.py / REA_20261031_05H_P0_VORBIS_CALLOC_NULL_AUDIT.py / REA_20261031_05H_P0_VORBIS_CALLOC_NULL_EVIDENCE.json。静的監査56/56 PASS、実行0.9178秒。
- 前回04Hの33/33と正式同期ログ（20261011T153958076Z）64/64を照合しただけで、正式VERIFIED追加0、REA5方法(info/pseudo/assembly/callers/callees)新規完備0、正式TODO/VERIFY/BLOCKED差分0/0/0。
- 原作Golden実測PASS=0、完全複製率=未測定。PC接続正常・active.lock無し、確認時空きRAM約7.97GiB。CPU負荷と総時間は不明。ゲーム、新規REA/Ghidraは起動していない。

## KB_CANDIDATE（shared knowledgeとGitHubには未反映）
- 候補VA 0x005D4030：仮ラベル VorbisComment_Type3_Parse。owner=REA、T015、STATIC（ASM局所条件）、VERIFY（失敗時の現実の再現とABI）。既存03HはNULL検査未確認まで。今回CRTのNULL戻り値と複数の後続書込siteを接続した。
- VA 0x005D1C71：CRT _calloc、0x005C303C：__calloc_impl。V9に既存名があるため新規登録として二重計上せず、CALL site 0x005D1C86／0x005D4061／0x005D40BE／0x005D40C8／0x005D4115を追記候補とする。
- code VA 0x005D407D / 0x005D4112 / 0x005D411C / 0x005D3CC8 は潜在的NULL書込位置。STATICな制御経路と実機クラッシュや悪用可能性は別判定。INFERRED / VERIFYのまま。
- source file：本報告、新規AUDIT.py（各PE命令位置の機械照合）、EVIDENCE.json（source SHA・checklist）。KB候補の正式統合・確度昇格は専任統合担当のみ。READY判定しない。

## 未確認と次の対象
- CRT new-handler設定、メモリ枯渇再現、例外処理、上位への伝播、callback再入は未検証。
- 次回P0：0x005D3CB0（reader）/ 0x005D3D00（途中失敗cleanup）、コメント長ゼロとOOMの分離、非実行Golden条件の追加。正式検証には独立安全条件を要する。
- 原本、MASTER、QUEUE、PROGRESS、既存RUN、A-E、共有knowledge、Git、スケジュールへの書込なし。

