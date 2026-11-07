# 迫真戦記 ver0.67｜REA 19時台 P0：DirectMusic COM失敗と統合V9の例外CALL索引
研究ID：REA-LOCAL-20261026-19H-P0-DMUSIC-COMFAIL-V9-SEH-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-26 JST）
原作研究コピーSHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
統合V9 SHA256：2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 前提と旧成果の区別
MASTER/規約、REA README/QUEUE/PROGRESS/旧RUN・同期ログ、検索README・BUILD_MANIFEST、V3とV9推奨案内、18H成果を先読。
2026-10-11の同期ログWave1～5=64/64。QUEUE/PROGRESSはEPERM後のstale表示。過去64件を今回加算しない。
既知の+0x70配列free未確認(12H)、bad_alloc範囲(15H)、V3で未索引E8×3(18H)は再計上せず、下記の新しい2つの差分のみ報告。

## P0-1：CoCreateInstance失敗後、呼出元が通常処理を続行
0x004BE480内では管理配列を0x004BE4EBで[ESI+0x70]へ保存する。
0x004BE582のCOM生成後、0x004BE588 TEST EAX,EAX → 0x004BE58A JS 0x004BE5E8。
2回目の0x004BE5BAでも0x004BE5C0 TEST EAX,EAX → 0x004BE5C2 JS 0x004BE5E8。
共有出口0x004BE5E8～0x004BE5FAはフレームとレジスタ復元→RET 4。この出口には直接のReleaseや配列freeなし。
親0x004BD2A0の0x004BD3E4 CALLから戻ると0x004BD3E9 LEA、0x004BD3F3 WinAPI CALL、0x004BD3F9 WinAPI結果比較へ進む。直後に子のHRESULTを調べない。
そのためCOM生成が失敗しても、子が例外ではなく通常復帰すれば親は音楽初期化の成否を確認せず後続設定を継続する。
EAXがHRESULTを保持する可能性はあるが親は次のCALLで上書きする。Ghidraのvoid推定を確定ABIとは扱わない。
部分初期化のcleanup到達性、参照保持、実機クラッシュ・リークは未実測でありVERIFY。

## P0-2：統合V9でも3つの既知SEH E8が索引にない
推奨V9のverifyはV9_INDEPENDENT_READBACK_PASS、DBハッシュ一致。
原作PEのE8 siteは0x005B8612→0x005BE999、0x005B862A→0x005BB625、0x005B862F→0x005BB64A。
3件とも原作実バイト・相対アドレス・Capstone CALLが一致。V3/V9両方のnative_callsite / verified_direct_calls / ghidra_refsに0件、V9 function_range所有者も0。
対照0x005B7CA7→0x005BE999は両DBで1件。従って3件の未収録はV3限定ではなくV9にも残る。
V9の未所属E8=0は記録済み索引の分類結果であり、EXE全コード網羅の主張ではない。旧3siteを新規3siteとして二重計上しない。
V9全体が無効との判断でもなく、例外専用コード範囲の限定的補足が必要という確認。DBは改変しない。

## 検査と正式進捗
独立監査37/37 PASS（原作/V3/V9 SHA、PE32、親の継続ASM、COM失敗分岐、3つのE8、V3/V9索引、同期記録）。
証拠JSON排他新規保存とreadback PASS。5種の状態：info/pseudo=INDEX_ONLY_V9、assembly=TARGETED_PE_NATIVE、callers/callees=INDEX_ONLY_KNOWN_SEH_GAP。
新規REA正式VERIFIED=0、正式TODO/VERIFY/BLOCKEDの書込差分0/0/0、Golden実ゲームPASS=0、strict MATCHと完全複製率未測定。
37は静的監査条件数であり関数数ではない。

## 保存・安全・次手
新規ファイル：19Hの限定PROBE.py、独立AUDIT.py、EVIDENCE.json、本STATIC.md、およびREADBACK.md。最後のREADBACKは保存・ハッシュ検証後に記録する。
原本ZIP/EXE/SAVE、MASTER、A～E、QUEUE/PROGRESS、既存RUN、Git/公開先/スケジュールは無変更。新規REA/Ghidra/ゲーム起動なし、Work未使用、拒否対象には触れない。
次回はCOM失敗後に0x004BD2A0/0x00555CD0がcleanupに至る条件と+0x70の別free候補を追跡。SEH3siteはDB owner側へ必要性だけ伝え、既存DB書換え・拒否操作の迂回はしない。
