# 迫真戦記 ver0.67｜REA/T014 上位例外捕捉と仮想CALLの独立静的解析

**独立研究ID**：`REA-OFFLINE-20261022-1433-T014-UPSTREAM-CATCH-VCALL-STATIC-01`  
**実施**：2026-10-22 14時台 JST  
**分類**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**owner**：REA/T014。研究PCの正本、他レーン、原本、Git、スケジュールには書き込まない。

## 1. 接続、資料の健全性、重複の排除

Desktop Commander Local Compactから研究PC上の`MASTER_LEDGER.md`先読を試したが、`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`で失敗。**CONNECTION / rate limit**として記録し、安全拒否とは区別する。PCの通電、最新MASTER、owner/lock、QUEUE/PROGRESS、最新V3/V4の状態、CPU・RAM負荷は今回は不明。復旧ID：`REA-RC-20261022-1433-LOCAL-429-01`。

認可されたChatGPT Libraryの原作`Vahren(2).exe`と`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`を個別に取得し**read-only**で調査した。ZIPの旧検索DB（2026-10-21収録版）はSHA256が同梱BUILD_MANIFESTに一致し、SQLite `PRAGMA integrity_check=ok`。全関数を再解析していない。以前のREA13:38（`REA-OFFLINE-20261022-1338-T014-STACK-EH-LOCAL-LIFETIME-STATIC-01`）とE13:50横断照合を読み、既存の「スタック側デストラクタ」「2経路の所有者差」を新発見として再計上しない。**今回の増分は、そのさらに上位のcatch二経路のEHメタデータ復元と、特定の未解決間接CALLの候補先を実vtable値で確認したこと。**

| 出典 | 現物SHA256 |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内`search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |
| 先行REA13:38のJSON | `26B3BD2B9B5FA5FECE8F6FD858C1C5F3CBA6F215976A905DD0954922784325DA` |

**版の注意**：2026-10-22のV4例外関数952件修復は別途検証済みだが、標準入口への昇格はWindowsアクセス拒否により保留というLibrary研究報告がある。**今回のDBは旧オフライン版であり、現行V3/V4の根拠にすり替えない**。V4への再解析・アップグレードを実行していない。

## 2. スタック上のオブジェクト読込：呼出元による例外捕捉を発見

REA13:38の既存証拠は`0x45E1E0`の読込中`0x45E52F → 0x5964C0`、EH state 4からの対象ローカルオブジェクト破棄を示す。今回その**呼出元**`0x45E5F0`の実機械語を追跡し、`0x45E75E → 0x45E1E0`を確認。

`0x45E5F5`の登録EH thunkと、実EXEから復元したMSVC `FuncInfo 0x00656F0C`は `magic=0x19930522`、`maxState=6`、`UnwindMap=0x00656EB8`、`TryBlock数=1`、`tryLow=4/tryHigh=4/catchHigh=5`。catch配列は**`0x45E7B5`**を指す（型情報0、adjectives `0x40`）。CALL前`0x45E73B`でEH状態4を書き込む。

catch内の`0x45E7B9 → 0x5B71DD`はファイル用バッファ解放系へ続き、保存済み機械語では`LoadException`相当の例外オブジェクト構築と**`0x45E7D9 → 0x5B864E`（MSVC C++ throw）**が確認できる。つまり、読込子関数のローカル破棄の後、**すぐ上の親関数が例外を捕捉してファイルバッファを後始末し、別の例外として送出する条件経路**がある。「スタック側は上位へ無条件に生の例外が抜ける」とする旧推論は訂正が必要。実際の例外到達条件、他のcleanup、さらに上の捕捉とゲーム側の状態は依然未検証。

## 3. ヒープ側の上位catchと`FadeOutSheet`の間接CALL

ヒープ読込側の物理関数入口`0x45E7F0`（`0x45EAC0`は内部ブロック候補）の**呼出元**`0x433E80`を追跡。`0x433FC5 → 0x45E7F0`のCALLと、親関数のMSVC `FuncInfo 0x00655394`を確認。`magic=0x19930522`、`maxState=9`、`UnwindMap=0x00655328`、`TryBlock数=1`、`tryLow=0/tryHigh=0/catchHigh=2`、catch handlerは**`0x433FCF`**。先行REA12:30で調査した`0x45E7F0`内部の`0x45F933`のcatchと**別段階**である。すべての失敗が親catchまで届くことは証明しない。

この上位catchは`0x433FD1`で0x34バイトの動的確保を要求し、`0x433FF2`で`0x543A30`（構築処理候補）を呼ぶ。続く`0x433FF7`の**実バイト**が`mov [esi],0x006388D4`（`FadeOutSheet` vtable候補）を示す。`0x434007`からvptrを再取得、`0x434009`で`[vptr+0x18]`、`0x43400C`で**10**をPUSHし、**`0x43400E: CALL EAX`**となる。

この間接呼出しは、原作PEの`0x006388D4+0x18=0x006388EC`から実際に32ビット値を読み取ると**`0x00543AE0`**を指す。`0x543AE0`は`0x543AE9→0x5433D0`を呼び、`+0x30`フィールドを更新する経路があり、終了命令は**`RET 4`**。したがって、当該catchで生成されたオブジェクトが正常に構築され、vptrが保持された条件下では、従来未解決の`CALL EAX`の実装先を**`0x543AE0`へ条件付きで特定**できる。

ただし、その下位`0x5433D0`は別の**未解決間接CALL `0x543428`**を持つ。クラス同定や「画面が必ずフェードする」という動的効果、例外・メモリ不足での到達性、ヒープオブジェクトの最終所有権は**VERIFY**。`0x434010`〜`0x434016`にはcatch継続から親の共通終端へ進む経路があるが、これはゲーム実測の成功を意味しない。

## 4. 関数索引の注意と独立検証

旧Ghidra検索DBには`Catch_All@0045e7b5`および`Catch_All@00433fcf`が**既に独立エントリとして存在する**一方、通常の直接CALL caller索引には**両方0件**。実際のリンクは通常E8ではなくMSVC EH `FuncInfo`のhandler配列による。**「CALL索引0件＝未参照」や「関数自体がDB未登録」は誤り**。通常のCALL、例外メタデータ、JMP/tail-callを混同しない。

独立検証器`verify_rea_t014_upstream_catch_20261022.py`はEXE/ZIP/DBのハッシュとDB整合性、関数疑似CのSHA、原作機械語27箇所、E8相対CALL7箇所、2関数のMSVC EH状態**6+9=15件**、handler配列とvtable raw slot、`RET 4`を検査した。結果：**27/27命令PASS、7/7直接CALL PASS、2件のEH表/15状態PASS、`0x43400E→0x543AE0`条件付き静的対応PASS**。実行時間は約**1.382秒**（検証器のみ）、調査全体は未計測。原作ゲーム・セーブの実行や変更は**0回**、新規Ghidra/REA実行も**0回**。CPU/RAMは研究PC不通につき不明。

## 5. 正式進捗と次の一手

既存Wave1〜5の**64/64 VERIFIEDは過去の報告値**であり、最新PC正本の再確認値ではない。今回新たに`info/pseudo/assembly/callers/callees`の**REA正式5種類証拠をすべて満たした関数は0**、正式新規VERIFIED **0件**、正式TODO/VERIFY/BLOCKED差分**0/0/0**、ゲームGolden PASS **0**、strict MATCH **0**。静的分岐の証拠は原作Goldenの代用にならない。原本・MASTER/QUEUE/PROGRESS・A〜E・T018・dev_lab・Git・Work・既存スケジュールは変更しない。安全拒否済みVA/Wave6/エクスポートは再試行しない。新たな安全拒否は0件。

次回優先は**`0x543428`の仮想dispatch（安全に読める既存静的証拠のみ）**および**`0x45F72C`周辺のヒープ所有権移転**、さらに`0x4D0D8A → 0x45E5F0`上位例外の継続処理。事前に旧証拠・E横断研究との既存ID照合を行い二重計上を防ぐ。

PC接続復旧時は最新MASTER/規約/REA README・QUEUE・PROGRESS・RUN・evidence/active.lock/owner、現行DB/V4保留状態/ハッシュ/競合を**read-only**で比較してから、REA所有範囲へ重複のない差分を**一度だけ**安全な方法で同期する。今回のLibrary記録はPC正本への保存を証明しない。
