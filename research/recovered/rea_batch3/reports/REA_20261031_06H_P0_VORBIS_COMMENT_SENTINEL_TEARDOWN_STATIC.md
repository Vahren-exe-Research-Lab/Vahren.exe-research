# 迫真戦記 REA｜2026-10-31 06H｜Vorbisコメント配列の終端と途中失敗cleanup（P0）
研究ID: REA-LOCAL-20261031-06H-P0-VORBIS-COMMENT-SENTINEL-TEARDOWN-STATIC-01
owner=REA / 関連Task=T015 / PC-SAVED / STATIC / VERIFY / NOT READY。05HのNULL障害候補は再計上せず、未記録の境界条件と静的範囲を追加検証した。

## 新規独立静的証拠
1. 0x005D4030 の 0x005D40BA inc edi 後、0x005D40BE・0x005D40C8 で二つの _calloc(count+1,4) を呼ぶ。成功した各配列はcount個の有効要素の後に1個のゼロ初期化スロットを持つ（正常なcalloc成功時に限る）。格納先はコメント構造体 +0（文字列ポインタ配列）、+4（長さ配列）、+8（count）、+0xC（vendor）。
2. 0x005D3D00 は +0 が非NULLのときだけ、+8の signed count に従い 0 <= i < count の要素を走査。要素ポインタが非NULLなら0x005D3D2Eから_freeし、0x005D3D3Fでポインタ配列、0x005D3D50で長さ配列、0x005D3D60でvendorを解放する。最後に0x005D3D6A/6C/6F/72で +0/+4/+8/+0xC の4フィールドを0に戻す。
3. 配列確保成功と初期ゼロ化を前提とすれば、type3の途中エラーでは既に作った文字列だけを解放し、未作成のNULL要素を飛ばす。同一構造体への二度目のcleanupも外部別名参照・再入・破損がなければ実質no-opになる。局所静的推論であり実機のメモリ安全保証ではない。05Hで確認したcalloc失敗後の未検査書込は解消されない。
4. 0x005D3CB0 は呼出元0x005D412Cから受け取る長さ(EAX)が0なら直ちに返る。正なら0x005D3CC3でbitreader 0x005E6E10を呼び、0x005D3CC8で戻り値の下位1byteを格納する。負値(-1)検査はこのヘルパー内にない。ただし親関数の残量検査により通常時の読取失敗到達性は未証明（VERIFY）。
5. 関数境界の重要な補正：V9の0x005D3D00は連続114byteではなく、function_rangeに[0x005D3D00..19] 26byteと[0x005D3D20..77] 88byteを持つ。間の0x005D3D1A..1Fは6byteのpadding lea ebx,[ebx]。body合計114byteに対しアドレスspanは120byte。末尾0x005D3D72と0x005D3D77 retの実ASMも照合した。V9自体の欠落ではない。

## 相互参照・重複防止
- 統合V9 tools/v9_coverage.py --inspect：0x005D3CB0 はE8 caller 0x005D412C、callee 0x005D3CC3（→0x005E6E10）、それぞれ1件。0x005D3D00 はE8 callers 0x005CF1FB/0x005CFBB4/0x005CFE61/0x005D4148 の4件、callee _freeの4件。
- GitHub非公開developの GHIDRA_V9_COVERAGE_REPORT.md と KNOWLEDGE_CURATION_PROTOCOL.md、PC knowledge README/SYNC_STATUS、KB addr/docsの両VAをread-onlyで照合。KB名・資料言及は両VAとも未登録。旧05Hのcalloc NULL経路と今回の追加点は独立IDで区別。
- 出典：rea_lab/targets/hakushin067_Vahren.exe、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原作ソース行は無いのでVAを位置指定。V9索引 rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite、SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
- 独立監査：REA_20261031_06H_P0_VORBIS_COMMENT_SENTINEL_AUDIT.py と同EVIDENCE.json。V9関数とE8 site、PE ASM、旧05H記録、正式同期ログ、SQLite quick_checkを検証。**51/51 PASS**、監査0.9094秒。
- RECOVERY-ID: REA-RECOVERY-20261031-06H-SPLIT-RANGE-AUDIT-OTHER-01。監査側の初回失敗：47/48（pe_asm_005D3D72未検出）。誤ってV9の関数body合計114byteを連続VA spanとみなした。V9 function_rangeを確認し、span120byteへ修正、分離2範囲とRET siteを追加した結果51/51 PASS。分類 OTHER / AUDIT-RANGE、再試行は新規安全拒否の迂回ではない。最初の失敗では証拠JSON未保存。補正後にのみ保存。

## KB_CANDIDATE（共有knowledgeには未反映）
owner=REA、task=T015、source=上記EXE SHA/ASM VA、既存研究ID=REA-LOCAL-20261031-05H-P0-VORBIS-CALLOC-NULL-GATE-STATIC-01。候補：0x005D4030 コメント配列count+1ゼロ終端、構造体+0/+4/+8/+0xC、0x005D3D00部分構築cleanup・4フィールドゼロ化、0x005D3CB0 byte-copy戻り値負値未検査。確度 STATIC（各局所命令・E8参照）/INFERRED（安全な二重cleanup・センチネル利用意図）/VERIFY（EOF/メモリ不足/再入）。正式登録・確度昇格は知識ベース統合専任へ委譲。

## 状態と再開位置
既存正式STATIC VERIFIED=64/64維持。今回正式5種証拠完備=0、新規VERIFIED=0、正式TODO/VERIFY/BLOCKED差分0/0/0、原作Golden実測PASS=0、完全複製率は未測定。
PC接続正常、active.lockなし、解析時Java/Ghidra競合なし、前検査時空き物理RAM約18GiB。CPU負荷と総作業時間は不明。新規REA/Ghidra・実ゲーム・危険VAへの操作なし。MASTER、QUEUE、PROGRESS、既存RUN、A-E、共有knowledge、Git、スケジュール変更なし。
次回：0x005E6E10 と 0x005E6F10 のEOF/残量単位を比較し、0x005D3CB0の負値を格納する経路が親0x005D4030の長さガードを通過可能か判定。メモリ不足や異常入力の実機再現は未実測として分離。
