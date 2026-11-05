# REA T014 — 保存済みnative根拠による2モード呼出値の照合（2026-10-12 11:42 JST）
- 区分: CONFIRMED-SAVED-STATIC / 実機golden NOT RUN。新規REA/Ghidra実行0・新規VERIFIED0。原本ZIP/EXE不実行・未編集。
- 管理正本/規約/REA README/QUEUE/PROGRESS、最新RUN_RESULT `20261011T153309850Z`、sync `20261011T153958076Z`、既存REA証拠をLocal Compactだけでread-only照合。
- 承認済みcopy SHA256再計算一致: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
## 新規確認（保存済み `exe/T014_NORMAL_LOAD_PROBE.txt`）
- 通常save reader内 `0x45E53A PUSH 1 → 0x45E53E CALL 0x471AF0`、`0x45E547 PUSH 1 → 0x45E549 PUSH ecx → 0x45E54C CALL 0x435550`。外交readerとgraph readerへ双方 mode=1 を渡す。
- 別の保存済みコード区間 `0x45EF0F PUSH 0 → 0x45EF1D CALL 0x471AF0`、`0x45EF25 PUSH 0 → 0x45EF2D PUSH edx → 0x45EF34 CALL 0x435550`。両readerへ双方 mode=0 を渡す分岐を命令列から確認。
- mode=0の呼出は直前 `0x45EEFE SETE AL / 0x45EF01 TEST AL,AL / 0x45EF03 JE 0x45F66E` を経て到達する。無条件に全saveを毎回初期化するとは言えない。
- graph reader `0x435550` のsave済Ghidra callersは `0x45E1E0` と `0x45EAC0`。証拠ID `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`。呼出命令のVAは `0x45E54C` / `0x45EF34` として区別する。
- `0x45EAC0`からは `MOV ECX,[EBP-0x14]`など途中コードが保存され、通常プロローグがない。入口境界・親routine・到達条件は独立Ghidra 5-method証拠未取得のため VERIFY。別個の高水準loader関数2個と断定禁止。
- graph関数既存info `ev_8fc065296a08a2f672a520399680a38404d656f96ecd59f4747278ec964409a4`、assembly `ev_775c749267e95e4682d3e76c638e9a612068de9345aedb4557eabd74e6eaafe2`。mode=0は既存tree clearと3種allocate、mode=1は既存3 global objectに作用する別経路。callee副作用/再初期化範囲はVERIFY。
- 対象T-ID=T014。再実装では diplomacy/graph 両者について mode 0/1 を区別し、root reader全件へ無条件clearを追加しない。旧EXE実機trace未取得。
## 進捗・安全
- 最新sync: Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 12/12、Wave5 16/16＝64/64 STATIC VERIFIED、P0=29/29・P1=35/35。Wave6暫定0/16、候補P0=5/P1=11、TODO16/VERIFY0。今回新規VERIFIED +0。
- 正式QUEUEとPROGRESSは rename EPERMにより古い表示。同期ログ `queueUpdate=STALE_RENAME_DENIED`。失敗rename/sync/別経路上書きを反復せず、新規Wave6登録と重い解析を実行しない。
- 研究DONE9/34（MASTER更新を要優先）、旧EXE実機golden PASS0。ゲーム再実装率は測定していない。
- Local事前測定 11:40:36 JST: CPU1.7%、空きRAM15.62GiB、Java/Ghidra/REA先行process0、active.lockなし。重い解析実行時間0秒、軽量調査時間は未厳密計測。
- REA6.1.0 / Ghidra12.1.4、単一MCPセッション、最大4関数/回、Ghidra900000ms、request960000msの制限変更なし。
- 次回: `0x45EAC0`を単独関数扱いせず既存nativeの親境界・入口xrefs確認、保存済 `0x58E480`など未分類reader用途確認。正式キューが安全に更新できた場合にのみWave6（`0x515750, 0x515790, 0x5159B0, 0x57D180`）を新規4件以内で検討。
- 原本、A〜E、MASTER、T018、他研究、Git/push/公開、MCP/設定、スケジュールは無変更。安全拒否済みアドレス/抽出は非実施。