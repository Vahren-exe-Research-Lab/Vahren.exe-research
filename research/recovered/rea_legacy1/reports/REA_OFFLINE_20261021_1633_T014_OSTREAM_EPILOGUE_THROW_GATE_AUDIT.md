# 迫真戦記 ver0.67｜REA独立オフライン静的監査（2026年10月21日 16時台）

**記録ID** `REA-OFFLINE-20261021-1633-T014-OSTREAM-EPILOGUE-THROW-GATE-01`  
**状態** `STATIC / VERIFY / OFFLINE-UNSYNCED / NOT READY`  
**所有範囲** REA独立・T014 P0 `0x42E700`周辺の入出力stream ABI（原本・A～E・MASTER・QUEUEは変更しない）

## 1. 接続・旧成果・検索基盤
- Desktop Commander Local Compactへ正本 `MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、`decomp_task/README.md`、`QUEUE.json`、`PROGRESS.md` の同時先読を試みたが、**`INVALID_ARGUMENT: McpServerError: Session terminated`**。分類 CONNECTION（PC電源断・安全拒否とは断定しない）、復旧ID `REA-RC-20261021-1633-LOCAL-SESSION-TERMINATED-01`。
- 代替正規保存物：Libraryのユーザー提供 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34エントリCRC PASS。`search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`はBUILD_MANIFEST一致、`integrity_check=ok`（1.042秒）、CLI検索スクリプトSHAもBUILD_MANIFEST一致。
- 検索成果が申告する原EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は **manifestの記録値**（EXE現物の再ハッシュなし）。Ghidra12.1.4・内部10,268関数の検索基盤は既存の派生成果で再実行なし。ZIP内`PROGRESS.md`は2026-10-09の旧Wave1で15/16時点、既存runsの最新確認はできない。前回までのWave1〜5=64/64 VERIFIED値は破棄・重複加算せず「過去報告値」と区別する。
- 過去監査Markdown 7件について`_ProcessingThrow`／`0x4295B5`／正規化本文一致の記述は発見できず、今回の**新規差分**は「書込後処理における例外処理中ゲート」と「2種の出力関数で同一の分割エピローグを使う構造」の**照合**。既知のvtable・入出力件数・19バイトhelperの発見は再計上しない。

## 2. 今回の新しい静的根拠 A：例外処理中の後処理抑止
前回`0x4628F0`の書込後処理として挙げた`0x4629DB`の詳細を、実体サブルーチンまで追跡した。

- `0x4629DB` → `0x5B61F2`（CALL site **`0x462A05`**、`thunk_FUN_005b9edb`）→ thunk先 **`0x5B9EDB`**。`0x5B9EDB`のGhidra疑似Cは `__getptd()->_ProcessingThrow != 0` を返す。
- `0x4629DB`の`cVar2 = thunk_FUN_005b9edb(); if(cVar2 == '\0') FUN_0042aa80();` により、**現在CRTが例外処理中でなければ** `0x42AA80`を呼び、**例外処理中ならこの後処理はスキップ**する、という分岐が保存疑似C上で直接確認できる。CALL site **`0x462A10→0x42AA80`**。
- `0x42AA80`は `(offset+0x14のbit2 != 0)`、`(offset+0x0Cのbit2/bit4 == 0)`を満たす場合に間接virtual **`+0x34`** の戻り値`-1`をチェックし、失敗なら`0x426E00`（CALL site **`0x42AAF9`**）へ進む。**この処理は単純な書込バイト数不一致の比較ではない**。`0x426E00`には例外マスクとのAND、および`badbit`→`failbit`→`eofbit`の優先順位に基づいて`std::ios_base::failure`を投げる静的経路がある。
- `0x51CB40`（3バイト）の保存疑似Cは0を返すため、**実行時vptrが以前の別担当検証で確認されたstringbuf表を指す場合に限り**、`+0x34`の返値は`-1`ではなく0になる。ほかのvtable、実際のEOF/失敗状態、復元漏れはVERIFYのまま。

## 3. 新しい静的根拠 B：1バイト書込と複数バイト書込で同じ分割エピローグ
- `0x4294B0`（1バイト書込）→ `0x4295B5`：CALL site **`0x42953C`**と**`0x429583`**。
- `0x4628F0`（複数バイト書込）→ `0x4629DB`：CALL site **`0x4629A9`**。
- **`0x4295B5`と`0x4629DB`はどちらも107バイト**。保存済みGhidra疑似Cから自動ヘッダと関数名だけを除いて正規化すると本文が**完全一致（1.000）**。正規化本文SHA256 `EE0A46A9CA1C7B53B1998E9EF1C11F68787187F449EE7E07DF8A8ABC622C387A`。どちらも `unaff_EBP`/`unaff_EDI`を使い、exception flag→sentry/ios cleanup→`ExceptionList`復元という順序を持つ。
- これらは「単純な処理戻り値を返す独立のC関数」とは限らず、**異なる出力APIに対してコンパイラが似た制御・スタック後処理を生成したもの**と整合する。**同一バイナリバイト列／同一実行時経路／正常return ABIまで証明したものではない**（ASM、CF/SEH、stack cleanup確認が未了）。
- 参考：`0x42E700`読込の終了経路`0x42E7D4`には`unaff_EBP`、sentryの仮想`+8`、`ExceptionList`復元があるが、出力の`_ProcessingThrow`分岐はこの保存疑似Cに出現しない。差異を共通関数の一律置換で潰さない。

## 4. 分岐モデル（STATIC由来、Goldenではない）
- `processing_throw`、`unitbuf flag`、`status bits`、`sync virtual戻り値`を2値化した**16条件**で、`_ProcessingThrow`なら`0x42AA80`を呼ばず、非例外処理中なら呼ぶ。16条件のうち呼出8、条件を全て満たして`0x426E00`候補へ進むのは1。
- `0x426E00`のコードに現れる`in_EAX & exception_mask & 0x17`を32×32=**1,024通り**列挙し、優先順位の分岐条件が一致。これは疑似Cの条件式を再表現した**合成ロジック検査のみ**で、CRT実環境や原作実機での例外検査ではない。
- **同じ1,040条件すべてSTATIC合成検証PASS**。旧EXE実機Golden=0／新旧strict MATCH=0、ゲーム完全再実装率は未測定。

## 5. 5種類証拠の充足・差分計上
- Ghidra検索DBから今回確認した関数は`0x004628F0, 0x004629DB, 0x004294B0, 0x004295B5, 0x005B61F2, 0x005B9EDB, 0x0042AA80, 0x00426E00, 0x0042AA00, 0x0042E700, 0x0042E7D4, 0x0051CB40`（12件）。各関数の本文SHA256とサイズ、および8件の直接CALL siteは別添JSONに収録。利用根拠＝DBの`functions/code_sha256`・`calls`、`indirect_calls`、BUILD_MANIFEST。これらは**REA正規のinfo/pseudo/assembly/callers/callees 5種証拠とは別物**。REAの新規5種一式取得0件、Evidence ID新規0、VERIFIED新規0。ABI・分割エピローグ・EAX/EDX・vptr/virtual呼出先・実ゲーム到達性は **VERIFY**。
- スナップショットの旧報告値：Wave1～5 **64/64 VERIFIED**（P0 29/P1 35）、Wave6暫定 **0/16**（TODO12、関数結果VERIFY0、既拒否BLOCKED4）。今回の**正本TODO/VERIFY/BLOCKED増減0/0/0**。旧MASTER checkpoint195基準研究DONE9/34、IN_PROGRESS21、VERIFY4。いずれも最新PC正本と未照合。
- 新規Ghidra/REA実行時間 **0秒**。SQLite整合性検査の実測は別添JSONに記録、調査全体の所要時間は未計測、PC CPU/RAM負荷・active.lockは **不明**。

## 6. 復旧・未同期・安全な次位置
- CONNECTION拒否ID `REA-RC-20261021-1633-LOCAL-SESSION-TERMINATED-01`、対象=Local Compact `read_multiple_files`でPCのMASTER等の先読、時刻=2026-10-21 16時台JST、試行結果=`Session terminated`。未取得＝最新MASTER/owner/QUEUE/PROGRESS/runs/evidence/lock/CPU-RAM、未保存発見＝今回STATIC差分はPC正本に未同期、影響＝REA正規5種に昇格不可。これは**安全拒否ではなく接続障害**。既拒否VA 0x5710C0..0x571500、既拒否Wave6、REAエクスポートの再試行・回避は行わない。
- PC以外の独立成果はChatGPTコンテナ/Libraryの `REA_OFFLINE_UNSYNCED` へ保存し、readbackを確認する。最新PC正本への書き込みは**行わない**。原本ZIP/EXE/SAVE、A～E/MASTER/T018/dev_lab/Git、既存QUEUE/PROGRESS、Work、既存スケジュールを変更しない。
- **NEXT P0**：`0x4629DB/0x4295B5`の合法な既存ASMを、正常returnとEH unwind経路、EAX/EDX、stack cleanup、`0x462A2E`仮想+8、`0x42AA80`のvirtual+0x34で比較。次点 `0x42ECF0→0x42E700` の64bit EAX:EDX伝播と`0x42E7D4`の共通帰還境界。PC復帰後は最新正本/owner/lock/ID重複/ハッシュ/EPERM履歴を一度確認し、競合がないREA所有差分のみ同期する。
