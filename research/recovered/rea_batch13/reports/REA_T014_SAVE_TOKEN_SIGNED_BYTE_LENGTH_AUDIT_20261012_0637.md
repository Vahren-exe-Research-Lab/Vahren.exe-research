# REA T014 セーブ文字列読み込みのsigned-byte判定と255-byte上限（2026-10-12 06:37 JST）
- 区分: 既存Ghidra静的証拠の独立照合。新規Ghidra取得0・新VERIFIED+0。旧EXE実機NOT RUN。
- 対象: 承認済みコピー `rea_lab/targets/hakushin067_Vahren.exe`、今回SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`一致。
- 研究: T014。関数VA `0x4705F0` (Wave5 VERIFIED、保存run `20261011T144115307Z`、length256 bytes)。
- 根拠: `4705F0_procedure_assembly.json` evidence `ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d`。
- 突合: `4705F0_procedure_pseudo_code.json` evidence `ev_3851d07b1e0119564efeb2d7215b9c16ff9a63f274ce843c13ed100dfee38752`。
## 新規局所観察
1. `0x4705F0..0x470608`: 一時バッファ `0xB060F8` を0x400byteゼロ初期化。反復の `0x470610` は `0x470980` を呼び、戻値 `-1` のときは文字を格納しない。
2. `0x47063D..0x470645`: 読んだbyteが0ならNUL終端として終了。0以外なら `CMP AL,0x20; JL` と `CMP AL,0x7F; JG` を経て `0x470653` に到達する。
3. x86の`JL/JG`は**符号付き比較**。従って0x01..0x1Fおよび0x80..0xFFは例外枝へ、0x20..0x7Fは通常枝へ進む。0x7F(DEL)は許容され、単純な「ASCII printable(0x20..0x7E)」や「<0x20のみ禁止」とは異なる。Ghidra pseudoの`(char)< ' '`は高ビット排除を暗黙に含む。
4. `0x470653`でカウンタを1増やし、`0x47065C CMP ESI,0xFF; JL` で反復する。最大255個の非NUL byteを読むと、`0x470669`で添字255へNUL書込し正常側へ進む（stream state異常の分岐が先に発火しない前提）。
5. `0x470654 CMP ESI,0x3E8; JG` の1000-byte guardは、この通常ループの255-byte反復上限のもと到達不能。1000を「実際の入力許容上限」と解釈してはならない。
## 未解決と実装への注意
- 終端NULなし255byte超のstreamを入力したとき、この関数自身は255byteで打ち切るが、残るbyteの消費・次レコード誤整合・最終LoadExceptionは上位reader未検証でVERIFY。
- EOF(`0x470980=-1`)時のstream flag検査と例外が発生する可能性があるため、「EOFを空文字として許容」とは確定しない。
- この局所ルーチンの許容範囲を全セーブ文字列・日本語ゲームテキスト一般へ無条件拡張しない。別APIの文字コード/タグ形式と混同禁止。
## 経過・進捗・安全
- Wave1〜5保存済み64/64（Wave5 16/16、P0 29/29、P1 35/35）、新規+0。Wave6は未登録の16候補0/16（候補P0 5/P1 11、TODO16・関数結果VERIFY0）。
- MASTER最新checkpoint83: 34Task DONE9/IN_PROGRESS21/VERIFY4。旧EXE gameplay golden PASS0。ゲーム再実装率は測定していない。
- PC事前確認: CPU4%、空きRAM16.08GiB、Java/Ghidra0、active.lock無し。新REA/Ghidra実行0秒、軽量照合の全経過時間未計測。
- `QUEUE.json`/`PROGRESS.md`は既往EPERMで古く、最新sync `progress_sync_20261011T153958076Z.json`の64/64・STALE_RENAME_DENIEDを採用。拒否済みrename/抽出・0x5710C0..0x571500を再試行・迂回しない。
- 次回優先: T014で保存済みcaller `0x598980`/`0x5964C0` 等から当該読取ルーチンの実際のキー/ラベルと上位終端処理を分類。Wave6正式開始は安全なキュー更新が確立した後のみ。
- 原本ZIP/EXE、A〜E/MASTER/T018、他研究領域、Git/push/公開、REA setup、MCP設定、既存automationsへの変更なし。
