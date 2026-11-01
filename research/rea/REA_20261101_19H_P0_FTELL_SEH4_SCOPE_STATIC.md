# REA 2026-11-01 19H P0｜CRT ftell の SEH4 scope table と unlock cleanup
- ID: REA-LOCAL-20261101-19H-P0-FTELL-SEH4-SCOPE-STATIC-01
- owner/task: REA / P0-T015 (Ogg FILE* tell callback); status: NATIVE-STATIC / INFERRED-EH / VERIFY / NOT READY
- 原本一致専用コピー: `rea_lab/targets/hakushin067_Vahren.exe`; 既往FULL SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
- V9 composite: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`; 既往SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
- 先行ID: REA-LOCAL-20261101-17H-P0-CRT-FTELL-FRAME-CROSSWALK-STATIC-01（境界・共有EBP helper）；18H invalid-parameter研究は別件かつEVIDENCE追記 SAFETY_REFUSAL で未完成。
## 今回の新規差分（先行17Hを重複計上しない）
1. native `0x005B797C: push 0x0C`、`0x005B797E: push 0x00641260`、`0x005B7983: E8 -> 0x005BB680 (__SEH_prolog4)` を確認。V9 `refs-to 0x00641260` は `0x005B797E` の一箇所（索引限界あり）。
2. 参照される `0x00641260..0x0064127B` の28 bytesを原本一致PEから読取。先頭4 DWORDは `FFFFFFFE,0,FFFFFFD4,0`、続く3 DWORDは `FFFFFFFE,0,005B79D7`。MSVC EH4 scope tableと解釈した場合、後者は「parent=-2 / filter=NULL / cleanup handler=0x005B79D7」の登録候補。EH dispatcher経由の実行は未実測。
3. `0x005B79A9/AC` lock -> `0x005B79B2` [EBP-4]=0 -> `0x005B79B9` __ftell_nolock -> `0x005B79BF` 戻り値保存 -> `0x005B79C2` [EBP-4]=-2 -> `0x005B79C9` で同じ0x005B79D7を通常CALL。 `0x005B79CE` が戻り値をEAXへ復元。
4. `0x005B79D7` は共有EBPの `[EBP+8]` を使い `0x005B79DA -> 0x005BDB44 (__unlock_file)` を呼ぶ後処理。通常成功経路とscope tableの同じcleanupアドレス参照を照合した。親EBP依存なので独立ABIとして呼出可能とはしない。
## 根拠・制約
- 原本限定窓 SHA256: scope 28B `9429146C7EC7BE2CE162AD4D4A2D866F6BCB1839C20C40E6165345D674D1893A`; parent 91B `822EE268456FB08DF2CC348A5D88DB6E84BDABDB874A499DB28E5A923AC6C458`; cleanup 10B `7690F770327F158BB758D9A9BA25EF23B4DDC97D776FA4522A8A64EFA701527B`.
- V9: function 0x005B797C; callees=7 direct E8; refs-to 0x00641260=1。参照数は索引内の件数であって実行回数ではない。
- 静的解釈は「例外時のcleanup候補」であり、runtime例外配送・ロックを必ず解放する保証・実ゲーム故障は未証明。正常経路の確定部分も17H既知として扱う。
- 新規REA正式 info/pseudo/assembly/callers/callees 完備=0、新規正式VERIFIED=0、公式TODO/VERIFY/BLOCKED差分=0/0/0、Golden PASS=0、strict MATCH=0、完全複製率=未測定。旧Wave/64件は再計上しない。
## KB_CANDIDATE / 再開条件
- VA=0x005B797C, EH table=0x00641260, handler=0x005B79D7, calls=0x005B7983/0x005B79B9/0x005B79C9/0x005B79DA, offsets=[EBP-4]/[EBP-0x1C]/[EBP+8]。
- source=本報告＋同ID EVIDENCE.json / AUDIT.py; confidence: scope pointer/record/nonnormal cleanup path=STATIC、runtime EH dispatch=INFERRED/VERIFY。先行17Hに付記する差分であり重複の新関数登録は不要。
- 次：0x005BB6E0 (__except_handler4)のtable cursor読み出しと0x005B797C異常系cleanup条件を既存V9/原本ASMで境界確認。ゲームGoldenは実測が可能な時のみ別途設計。18Hの拒否済みJSON追記を再試行しない。
- 共有knowledge/MASTER/QUEUE/PROGRESS/Git/原本/既存スケジュールは本タスクでは変更しない。統合担当が既存IDとの重複を確認してREF_AUDIO_VORBISへ必要な差分のみ採用する。
